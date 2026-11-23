#!/usr/bin/env python3
"""
live_run.py - deploy PropCourt to GenLayer studionet and run the full story on real pages.

    python scripts/live_run.py [--contract 0x...] [--demo-url URL] [--out docs/live/run.json]

Throwaway keys are created (and funded for free with sim_fundAccount) and kept in
.propcourt/keys.json, which is gitignored. Every value written to the output file is
what the chain returned. Re-running resumes: steps with a tx hash are not sent again.

Real page: FTMO's public Trading Objectives page (https://ftmo.com/en/trading-objectives/),
which lists the 2-Step and 1-Step products with different numbers. The conduct-clause
part uses the PropCourt demo firm's rules page on GitHub Pages (--demo-url), a clearly
labelled demo firm, because FTMO's objectives page carries no conduct clauses.
"""

import argparse
import json
import os
import sys
import time

from eth_account import Account
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet
from genlayer_py.types import TransactionStatus as S

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS = os.path.join(ROOT, ".propcourt", "keys.json")
WEI = 10**18
WPU = 10**14                     # 1 USD of profit = 0.0001 test GEN
EXPLORER = "https://explorer-studio.genlayer.com"
FTMO = "https://ftmo.com/en/trading-objectives/"

P_2STEP = {"name": "FTMO", "product": "2-Step", "url": FTMO,
           "rules": {"profit_target_bp": 1000, "max_daily_loss_bp": 500, "max_loss_bp": 1000,
                     "min_trading_days": 4, "consistency_bp": 0}, "clauses": [], "demo": 0, "fund": 3 * WEI}
P_WRONG = dict(P_2STEP, rules=dict(P_2STEP["rules"], max_daily_loss_bp=400), fund=0)   # adversarial: 4 % is not on the page
P_1STEP = {"name": "FTMO", "product": "1-Step", "url": FTMO,
           "rules": {"profit_target_bp": 1000, "max_daily_loss_bp": 300, "max_loss_bp": 1000,
                     "min_trading_days": 0, "consistency_bp": 5000}, "clauses": [], "demo": 0, "fund": 1 * WEI}
HEDGE = "Hedging, holding opposite positions in the same instrument at the same time, is not allowed."
WEEKEND = "Positions may not be held over the weekend; close all trades before the Friday market close."
P_DEMO = {"name": "PropCourt Demo Firm", "product": "Demo Evaluation", "url": None,
          "rules": {"profit_target_bp": 0, "max_daily_loss_bp": 500, "max_loss_bp": 1000,
                    "min_trading_days": 3, "consistency_bp": 0}, "clauses": [HEDGE, WEEKEND], "demo": 100_000,
          "fund": 3 * WEI}


def T(day, oh, ch, pnl, sym="EURUSD", side="buy", lots=100):
    return [f"2026-11-{day:02d}T{oh:02d}:00:00Z", f"2026-11-{day:02d}T{ch:02d}:00:00Z", sym, side, lots, pnl]


# $100k: 5 days, +$4,000, worst day -$800 (limit $5,000)
CLEAN = [T(2, 9, 11, 120_000), T(3, 9, 12, -80_000), T(4, 10, 11, 150_000), T(5, 9, 10, 60_000), T(6, 13, 15, 150_000)]
# 1-Step consistency: best day $7,000 of $10,000 = 70 % > 50 %
LUMPY = [T(9, 9, 10, 700_000, "XAUUSD"), T(10, 9, 10, 200_000), T(11, 9, 10, 100_000)]
# opposite EURUSD positions open at the same time on 2 Nov
HEDGED = [T(2, 10, 11, -10_000, side="sell"), T(2, 9, 12, 90_000), T(3, 9, 10, 100_000), T(4, 9, 10, 100_000)]
# clean, closed every day: a "weekend" denial has nothing to stand on
DAYTRADER = [T(9, 9, 10, 80_000), T(10, 9, 10, 70_000), T(11, 14, 15, -20_000), T(12, 9, 11, 90_000)]


def say(*a):
    print(*a, flush=True)


def hexs(tx):
    h = tx.hex() if hasattr(tx, "hex") else str(tx)
    return h if h.startswith("0x") else "0x" + h


def jsonable(x):
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    if isinstance(x, (bytes, bytearray)):
        return "0x" + bytes(x).hex()
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    return str(x)


def keys():
    os.makedirs(os.path.dirname(KEYS), exist_ok=True)
    if os.path.exists(KEYS):
        with open(KEYS) as fh:
            k = json.load(fh)
    else:
        k = {}
    for role in ("firm", "trader", "trader2", "trader3"):
        if role not in k:
            k[role] = "0x" + bytes(create_account().key).hex()
    with open(KEYS, "w") as fh:
        json.dump(k, fh)
    return {r: Account.from_key(v) for r, v in k.items()}


def submit(send, attempts=5):
    for i in range(attempts):
        try:
            return send()
        except Exception as e:
            if i == attempts - 1:
                raise
            say(f"  submit failed ({str(e)[:140]}); retrying in 10s")
            time.sleep(10)


def summarize(t):
    cd = t.get("consensus_data") or {}
    votes = sorted((cd.get("votes") or {}).values())
    lr = cd.get("leader_receipt")
    lr = lr[0] if isinstance(lr, list) and lr else (lr or {})
    blob = json.dumps(jsonable(t))
    err = None
    i = blob.find("[EXPECTED]")
    if i >= 0:
        err = blob[i:i + 160].split('"')[0].split("\\")[0]
    return {"status": t.get("status_name"), "result": t.get("result_name"),
            "execution": lr.get("execution_result"), "votes": votes, "error": err}


def wait(client, tx, until=S.ACCEPTED):
    client.wait_for_transaction_receipt(transaction_hash=tx, status=until, interval=5000, retries=360)
    return client.get_transaction(tx)


class Run:
    def __init__(self, path):
        self.path = path
        self.s = json.load(open(path)) if os.path.exists(path) else {}
        self.s.setdefault("network", "studionet (chain 61999, https://studio.genlayer.com/api)")
        self.s.setdefault("steps", [])

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as fh:
            json.dump(jsonable(self.s), fh, indent=1)
            fh.write("\n")

    def do(self, client, label, send):
        for st in self.s["steps"]:
            if st["step"] == label and st.get("tx"):
                say(f"[skip] {label}: {st['tx']}")
                return st
        say(f"[send] {label}")
        tx = hexs(submit(send))
        st = {"step": label, "tx": tx, "sent_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        self.s["steps"].append(st)
        self.save()
        t = wait(client, tx)
        st.update(summarize(t))
        self.save()
        say(f"  {tx} {st['status']} {st['result']} exec={st['execution']} votes={st['votes']} err={st['error']}")
        return st


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract")
    ap.add_argument("--challenge-minutes", type=int, default=3)
    ap.add_argument("--demo-url", default="https://yoyoblair333-wq.github.io/propcourt/demo-firm-rules.html")
    ap.add_argument("--skip-demo", action="store_true")
    ap.add_argument("--out", default=os.path.join(ROOT, "docs", "live", "run.json"))
    a = ap.parse_args()
    k = keys()
    run = Run(a.out)
    cl = {r: create_client(chain=studionet, account=acct) for r, acct in k.items()}
    run.s["roles"] = {r: acct.address for r, acct in k.items()}
    for r, acct in k.items():
        if not run.s.get("funded_" + r):
            cl[r].fund_account(acct.address, 20 * WEI)
            run.s["funded_" + r] = True
    run.save()
    firm = cl["firm"]

    addr = a.contract or run.s.get("contract")
    if not addr:
        code = open(os.path.join(ROOT, "contracts", "prop_court.py"), encoding="utf-8").read()
        st = run.do(firm, "deploy", lambda: firm.deploy_contract(code=code, args=[a.challenge_minutes]))
        t = firm.get_transaction(st["tx"])
        addr = (t.get("data") or {}).get("contract_address") or t.get("recipient") or t.get("to_address")
        run.s["contract"] = addr
        run.s["challenge_minutes"] = a.challenge_minutes
        run.save()
    run.s["explorer"] = f"{EXPLORER}/address/{addr}"
    say("contract", addr)

    def read(fn, args=None):
        return firm.read_contract(address=addr, function_name=fn, args=args or [])

    def w(role, label, fn, args, value=0):
        c = cl[role]
        return run.do(c, label, lambda: c.write_contract(address=addr, function_name=fn, args=args, value=value))

    def register(label, p, url):
        return w("firm", label, "register_program",
                 [p["name"], p["product"], url, json.dumps(p["rules"]), p["clauses"], 8000, WPU, 60, 3, p["demo"]],
                 value=p["fund"])

    progs = [("program #1 FTMO 2-Step (declared 5/10/10 %, 4 days)", P_2STEP, FTMO),
             ("program #2 FTMO 2-Step, adversarial: declares 4 % daily loss", P_WRONG, FTMO),
             ("program #3 FTMO 1-Step (3 % daily, 50 % consistency)", P_1STEP, FTMO)]
    if not a.skip_demo:
        progs.append(("program #4 PropCourt Demo Firm (conduct clauses, demo accounts)", P_DEMO, a.demo_url))
    for i, (label, p, url) in enumerate(progs):
        if read("stats")["programs"] < i + 1:
            register("register " + label, p, url)
    for i, (label, _p, _u) in enumerate(progs):
        w("trader", f"verify_program #{i + 1} (consensus)", "verify_program", [i + 1])
        run.s.setdefault("programs", {})[str(i + 1)] = read("get_program", [i + 1])
        run.save()

    tr = run.s["roles"]["trader"]
    # 1. FTMO 2-Step: clean log; the firm cites a numeric rule that was not broken -> overruled by code
    if read("stats")["accounts"] < 1:
        w("firm", "open_account #1 on program #1 ($100k)", "open_account", [1, tr, 100_000])
    if read("get_account", [1])["requests"] < 1:
        w("trader", "request_payout #1 (clean log)", "request_payout", [1, json.dumps(CLEAN)])
    if read("get_payout", [1])["status"] == "PENDING_REVIEW":
        w("firm", "deny #1 citing rule:max_daily_loss_bp (false)", "deny",
          [1, "rule:max_daily_loss_bp", "Payout denied: the account breached the Maximum Daily Loss."])
    # 2. FTMO 1-Step: consistency breach measured by code
    if read("stats")["accounts"] < 2:
        w("firm", "open_account #2 on program #3 ($100k)", "open_account", [3, tr, 100_000])
    if read("get_account", [2])["requests"] < 1:
        w("trader", "request_payout #2 (best day 70 % of profit)", "request_payout", [2, json.dumps(LUMPY)])
    if not a.skip_demo and run.s["programs"].get("4", {}).get("status") == "ACTIVE":
        # 3. demo firm: hedged log, firm cites the hedging clause -> consensus
        if read("stats")["accounts"] < 3:
            w("trader2", "open_demo_account #3 on program #4", "open_demo_account", [4])
        if read("get_account", [3])["requests"] < 1:
            w("trader2", "request_payout #3 (hedged log)", "request_payout", [3, json.dumps(HEDGED)])
        if read("get_payout", [3])["status"] == "PENDING_REVIEW":
            w("firm", "deny #3 citing clause:0 hedging (consensus)", "deny",
              [3, "clause:0", "On 2 Nov the trader held a EURUSD sell while a EURUSD buy was open: that is hedging."])
        # 4. demo firm: day-trader log, firm cites the weekend clause -> consensus
        if read("stats")["accounts"] < 4:
            w("trader3", "open_demo_account #4 on program #4", "open_demo_account", [4])
        if read("get_account", [4])["requests"] < 1:
            w("trader3", "request_payout #4 (closed daily)", "request_payout", [4, json.dumps(DAYTRADER)])
        if read("get_payout", [4])["status"] == "PENDING_REVIEW":
            w("firm", "deny #4 citing clause:1 weekend (consensus)", "deny",
              [4, "clause:1", "The trader held positions over the weekend in breach of our rules."])
        for rid, role in ((3, "trader2"), (4, "trader3")):
            r = read("get_payout", [rid])
            if r["status"] != "DECIDED":
                continue
            while time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) < r["challenge_ends"]:
                say(f"  waiting for challenge window of #{rid} to close at {r['challenge_ends']}")
                time.sleep(20)
            time.sleep(15)
            w(role, f"finalize #{rid}", "finalize", [rid])
    run.s["payouts"] = {str(i): read("get_payout", [i]) for i in range(1, read("stats")["payouts"] + 1)}
    for role in ("trader", "trader3"):
        bal = int(read("balance_of", [run.s["roles"][role]]))
        run.s["balance_before_withdraw_" + role] = str(bal)
        if bal > 0:
            w(role, f"withdraw ({role})", "withdraw", [])
    run.s["programs"] = {str(i): read("get_program", [i]) for i in range(1, read("stats")["programs"] + 1)}
    run.s["stats"] = read("stats")
    for st in run.s["steps"]:
        try:
            st["latest"] = summarize(firm.get_transaction(st["tx"]))
        except Exception as e:
            st["latest"] = {"error": str(e)[:120]}
    run.s["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    run.save()
    say("wrote", a.out)


if __name__ == "__main__":
    main()
