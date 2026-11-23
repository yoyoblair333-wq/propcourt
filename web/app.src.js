// PropCourt web app. Reads the live studionet contract with genlayer-js and lets a visitor
// open a demo account, preview and request a payout with a per-browser burner key (testnet only).
import { createClient, createAccount, generatePrivateKey } from "genlayer-js";
import { studionet } from "genlayer-js/chains";

export const CONTRACT = "0x6Af674cF2196B7a9067380F74666C94352bFf485";
const RPC = "https://studio.genlayer.com/api";
const EXPLORER = "https://explorer-studio.genlayer.com";
const KEY = "propcourt.studionet-burner.v1";
const WEI = 10n ** 18n;
const RULE_NAMES = { profit_target_bp: "Profit target", max_daily_loss_bp: "Max daily loss", max_loss_bp: "Max loss",
  min_trading_days: "Min trading days", consistency_bp: "Consistency (best day ≤)" };

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const plain = (v) => {
  if (v instanceof Map) return Object.fromEntries([...v].map(([k, x]) => [k, plain(x)]));
  if (Array.isArray(v)) return v.map(plain);
  if (typeof v === "bigint") return Number(v) <= Number.MAX_SAFE_INTEGER ? Number(v) : v.toString();
  return v;
};
const gen = (wei) => {
  const w = BigInt(wei || 0);
  const whole = w / WEI, frac = (w % WEI).toString().padStart(18, "0").replace(/0+$/, "").slice(0, 4);
  return frac ? `${whole}.${frac} GEN` : `${whole} GEN`;
};
const usd = (cents) => (cents < 0 ? "-$" : "$") + (Math.abs(cents) / 100).toLocaleString("en-US", { maximumFractionDigits: 2 });
const short = (a) => (a ? a.slice(0, 6) + "…" + a.slice(-4) : "");
const ruleVal = (k, v) => (k === "min_trading_days" ? `${v} days` : `${v / 100}%`);

const reader = createClient({ chain: studionet });
let writer = null, account = null, programs = [];

function burner() {
  let k = localStorage.getItem(KEY);
  if (!k) { k = generatePrivateKey(); localStorage.setItem(KEY, k); }
  account = createAccount(k);
  writer = createClient({ chain: studionet, account });
  $("me").textContent = account.address;
  return account;
}

async function read(fn, args = []) {
  return plain(await reader.readContract({ address: CONTRACT, functionName: fn, args }));
}

async function fund(addr) {
  await fetch(RPC, { method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "sim_fundAccount", params: [addr, 10 * 1e18] }) }).catch(() => {});
}

async function send(fn, args, label) {
  const log = $("log");
  if (!writer) burner();
  log.textContent = `${label}: funding test key…`;
  await fund(account.address);
  log.textContent = `${label}: sending…`;
  try {
    const hash = await writer.writeContract({ address: CONTRACT, functionName: fn, args, value: 0n });
    log.innerHTML = `${esc(label)}: tx <code>${esc(hash)}</code> sent, waiting for validators…`;
    const r = await writer.waitForTransactionReceipt({ hash, status: "ACCEPTED", interval: 4000, retries: 200 });
    const res = r?.consensus_data?.leader_receipt?.[0]?.execution_result ?? r?.result_name ?? "";
    log.innerHTML = `${esc(label)}: tx <code>${esc(hash)}</code> accepted (${esc(res)}).`;
  } catch (e) {
    log.textContent = `${label} failed: ${String(e?.message || e).slice(0, 300)}`;
  }
  await refresh();
}

function programCard(p) {
  const v = p.verdict || { rules: {}, clauses: [] };
  const rules = Object.entries(p.rules).filter(([, x]) => x).map(([k, x]) => {
    const st = (v.rules || {})[k] || "-";
    const q = (p.quotes || {})[k];
    return `<dt>${esc(RULE_NAMES[k])}</dt><dd>${esc(ruleVal(k, x))} <b class="${st === "MATCH" ? "ok" : "no"}">${esc(st)}</b>${q ? `<br><q>${esc(q.slice(0, 160))}</q>` : ""}</dd>`;
  }).join("");
  const clauses = p.clauses.map((c, i) => `<dt>Clause ${i}</dt><dd><q>${esc(c)}</q> <b class="${(v.clauses || [])[i] === "PRESENT" ? "ok" : "no"}">${esc((v.clauses || [])[i] || "-")}</b></dd>`).join("");
  const cls = p.status === "ACTIVE" ? "ok" : p.status === "PENDING" ? "warn" : "no";
  return `<article class="card">
    <h3>#${p.id} · ${esc(p.name)} · ${esc(p.product)} <span class="tag ${cls}">${esc(p.status)}</span></h3>
    <dl>
      <dt>Rules page</dt><dd><a href="${esc(p.rules_url)}" target="_blank" rel="noopener">${esc(p.rules_url)}</a></dd>
      ${rules}${clauses}
      <dt>Split · clock</dt><dd>${p.split_bp / 100}% to trader · trading day = UTC${p.day_offset_min >= 0 ? "+" : ""}${p.day_offset_min / 60} h · review ${p.review_minutes} min</dd>
      <dt>Pool</dt><dd><b class="ok">${gen(p.balance)}</b> · reserved ${gen(p.encumbered)} · paid ${gen(p.paid)} · ${p.accounts} account(s)${p.demo_capital_usd ? ` · demo accounts $${p.demo_capital_usd.toLocaleString()}` : ""}</dd>
    </dl></article>`;
}

function payoutRow(r, now) {
  const rep = r.report || {};
  const br = rep.breaches || [];
  let act = "";
  if (r.status === "PENDING_REVIEW" && now > r.review_ends) act = `<button data-act="finalize" data-id="${r.id}">Finalize (firm silent)</button>`;
  else if (r.status === "PENDING_REVIEW") act = `<span class="muted">firm review until ${esc(r.review_ends.slice(11, 16))} UTC</span>`;
  else if (r.status === "DECIDED" && now >= r.challenge_ends) act = `<button data-act="finalize" data-id="${r.id}">Finalize</button>`;
  else if (r.status === "DECIDED") act = `<span class="muted">appeal window until ${esc(r.challenge_ends.slice(11, 16))} UTC</span>`;
  const cls = r.status === "PAID" ? "ok" : r.status === "PENDING_REVIEW" || r.status === "DECIDED" ? "warn" : "no";
  return `<tr>
    <td>#${r.id}</td><td>acct #${r.account_id}</td>
    <td>net ${usd(rep.net_profit_cents)} · ${rep.trading_days} days · worst day ${usd(rep.worst_day_cents)} · best day ${(rep.best_day_share_bp / 100).toFixed(0)}%<br>
      ${br.length ? `<b class="no">breach: ${esc(br.join(", "))}</b>` : `<span class="ok">no numeric breach</span>`}</td>
    <td><b class="${cls}">${esc(r.status)}</b></td>
    <td>${r.ground ? `<code>${esc(r.ground)}</code><br><span class="muted">${esc(r.reason)}</span>` : "-"}</td>
    <td>${r.label ? `<b class="${r.label === "SUPPORTED" ? "no" : "ok"}">${esc(r.label)}</b>${r.appeals ? " (after appeal)" : ""}` : ""}${r.why ? `<br><span class="muted">${esc(r.why)}</span>` : ""}</td>
    <td class="ok">${gen(r.amount)}${r.capped ? " (capped)" : ""}</td><td>${act}</td></tr>`;
}

async function refresh() {
  try {
    const [stats, progs, pays] = await Promise.all([read("stats"), read("list_programs"), read("list_payouts")]);
    programs = progs;
    $("stats").textContent = `${stats.programs} program(s) · ${stats.accounts} account(s) · ${stats.payouts} payout request(s) · appeal window ${stats.challenge_minutes} min`;
    $("programs").innerHTML = progs.map(programCard).join("") || "<p class='muted'>No programs yet.</p>";
    const now = new Date().toISOString().slice(0, 19) + "Z";
    $("payouts").innerHTML = pays.map((r) => payoutRow(r, now)).join("") || "<tr><td colspan=8 class='muted'>No payout requests yet.</td></tr>";
    const demos = progs.filter((p) => p.demo_capital_usd > 0 && p.status === "ACTIVE");
    const cur = $("prog").value;
    $("prog").innerHTML = demos.map((p) => `<option value="${p.id}">#${p.id} ${esc(p.name)} · ${esc(p.product)}</option>`).join("");
    if (cur) $("prog").value = cur;
    if (account) {
      const bal = await read("balance_of", [account.address]);
      $("bal").textContent = gen(bal);
      $("withdraw").disabled = BigInt(bal) <= 0n;
      const mine = localStorage.getItem(KEY + ".acct." + $("prog").value);
      $("myacct").textContent = mine ? "#" + mine : "-";
    }
  } catch (e) {
    $("stats").textContent = "Could not read the contract: " + String(e?.message || e).slice(0, 200);
  }
}

function day(offset) {
  const d = new Date(Date.now() - offset * 86400000);
  return d.toISOString().slice(0, 10);
}
function tr(dOff, oh, ch, pnl, sym = "EURUSD", side = "buy", lots = 100) {
  return [`${day(dOff)}T${oh}:00:00Z`, `${day(dOff)}T${ch}:00:00Z`, sym, side, lots, pnl];
}
const SAMPLES = {
  clean: () => [tr(9, "09", "11", 120000), tr(8, "09", "12", -80000), tr(7, "10", "11", 150000), tr(6, "09", "10", 60000), tr(5, "13", "15", 150000)],
  hedged: () => [tr(9, "10", "11", -10000, "EURUSD", "sell"), tr(9, "09", "12", 90000), tr(8, "09", "10", 100000), tr(7, "09", "10", 100000)],
  daily: () => [tr(9, "09", "10", 300000), tr(8, "09", "10", -260000), tr(8, "11", "12", -260000), tr(7, "09", "10", 600000)],
  weekend: () => {
    const now = new Date();
    const back = ((now.getUTCDay() + 2) % 7) + 7;           // a Friday at least a week ago
    const fri = new Date(Date.now() - back * 86400000).toISOString().slice(0, 10);
    const mon = new Date(Date.now() - (back - 3) * 86400000).toISOString().slice(0, 10);
    return [[`${fri}T19:00:00Z`, `${mon}T02:00:00Z`, "XAUUSD", "buy", 50, 200000], tr(back - 4, "09", "10", 50000), tr(back - 5, "09", "10", 50000)];
  },
};

document.addEventListener("click", (ev) => {
  const s = ev.target.closest("button[data-sample]");
  if (s) { $("log_in").value = JSON.stringify(SAMPLES[s.dataset.sample](), null, 0).replace(/\],\[/g, "],\n["); return; }
  const b = ev.target.closest("button[data-act]");
  if (b) send(b.dataset.act, [Number(b.dataset.id)], `${b.dataset.act} #${b.dataset.id}`);
});

$("open").addEventListener("click", async () => {
  const pid = Number($("prog").value);
  if (!pid) return;
  await send("open_demo_account", [pid], "open demo account");
  // find our account id: newest account for us on this program
  const st = await read("stats");
  for (let i = st.accounts; i >= 1 && i > st.accounts - 50; i--) {
    const a = await read("get_account", [i]);
    if (a.program_id === pid && a.trader.toLowerCase() === account.address.toLowerCase()) {
      localStorage.setItem(KEY + ".acct." + pid, String(i));
      break;
    }
  }
  refresh();
});

$("preview").addEventListener("click", async () => {
  const pid = Number($("prog").value);
  const p = programs.find((x) => x.id === pid);
  try {
    const out = await read("preview", [pid, p ? p.demo_capital_usd : 100000, $("log_in").value]);
    $("prev").textContent = JSON.stringify({ report: out.report, conduct_facts: out.facts, payout: gen(out.payout) }, null, 1);
  } catch (e) {
    $("prev").textContent = "Preview failed: " + String(e?.message || e).slice(0, 300);
  }
});

$("request").addEventListener("click", () => {
  const aid = Number(localStorage.getItem(KEY + ".acct." + $("prog").value) || 0);
  if (!aid) { $("log").textContent = "Open a demo account first."; return; }
  send("request_payout", [aid, $("log_in").value], "request payout");
});
$("wallet").addEventListener("click", () => { burner(); refresh(); });
$("withdraw").addEventListener("click", () => send("withdraw", [], "withdraw"));
$("addr").innerHTML = `<a href="${EXPLORER}/address/${CONTRACT}" target="_blank" rel="noopener"><code>${CONTRACT}</code></a>`;
$("log_in").value = JSON.stringify(SAMPLES.clean()).replace(/\],\[/g, "],\n[");
if (localStorage.getItem(KEY)) burner();
refresh();
setInterval(refresh, 30000);
