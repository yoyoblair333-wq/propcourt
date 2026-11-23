# PropCourt

**Prop-firm payouts judged against the firm's own published rules, on GenLayer.**

Funded-trader ("prop") firms publish their rules and then decide alone whether a trader broke them. A payout denied over a vague or unpublished rule is the most common complaint in the industry, and the trader has nobody neutral to ask. PropCourt takes the three decisions that matter out of the firm's hands:

| Decision | Who decides | How |
|---|---|---|
| **Which rules apply** | GenLayer consensus, once, at registration | Validators read the firm's public rules page and must agree, rule by rule, that each declared number and conduct clause is really on it. The program is then frozen. |
| **Whether a numeric rule was broken** | Plain code | The trade log is measured on the firm's trading-day clock. A firm citing a numeric rule the code shows was *not* broken is overruled on the spot. |
| **Whether a conduct clause was broken** | GenLayer consensus, on denial | Validators judge the cited clause against facts computed by code (hedged overlaps, weekend holds, hold times), never the raw log. The burden is on the firm. |

- Live app: https://yoyoblair333-wq.github.io/propcourt/
- Live contract (studionet): `0x6Af674cF2196B7a9067380F74666C94352bFf485`
- Live evidence: [docs/LIVE_EVIDENCE.md](docs/LIVE_EVIDENCE.md) (raw: [docs/live/run.json](docs/live/run.json))

## Who it is for

- **Funded traders.** A payout denial must cite a rule the firm actually published. A denial the rules don't back pays out automatically.
- **Prop firms that want to be trusted.** A PropCourt-verified program proves the rules can't change after signup and that disputes go to a neutral process. That is a selling point in a market that is full of chargebacks and bad reviews.

## How it works

1. **Register a program.** The firm calls `register_program`. It gives the firm name, the product label as the page writes it (e.g. `2-Step`), the rules page URL, the numbers it enforces and up to 3 conduct clauses quoted from the page. It also sets the trader's profit split, the trading-day clock (e.g. CET = UTC+60 min) and a review window. The attached value funds the payout pool.
   - Numbers it can enforce: `profit_target_bp`, `max_daily_loss_bp`, `max_loss_bp`, `min_trading_days`, `consistency_bp`.
2. **Verify (consensus).** Anyone calls `verify_program`. The program becomes `ACTIVE` only if every declared number is `MATCH` and every clause is `PRESENT`. Otherwise it is `REJECTED`, or `UNREADABLE` if the page can't be read. An ACTIVE program never changes. New rules mean a new program, and existing accounts keep theirs.
3. **Open accounts.** The firm calls `open_account`; demo programs allow `open_demo_account`.
4. **Request a payout.** The trader submits the closed-trade log: `[open UTC, close UTC, symbol, buy|sell, lots×100, P&L cents]`. `measure()` runs in code. Any numeric breach gives `BREACH` and nothing is reserved. Otherwise the payout (net profit × split) is reserved from the pool and the firm has the review window.
5. **The firm reviews.**
   - `approve` pays the trader.
   - `deny("rule:<key>", reason)` is decided by code at once. If the log didn't break that rule, the denial is overruled and the trader is paid.
   - `deny("clause:<i>", reason)` starts a consensus round that returns `SUPPORTED` or `NOT_SUPPORTED`. The losing side may `appeal` once inside the challenge window. Then `finalize`: SUPPORTED releases the reservation back to the pool, NOT_SUPPORTED pays the trader.
   - Silence past the review deadline: anyone may `finalize`, and the trader is paid.
6. **Withdraw.** The trader withdraws the balance. The firm can only withdraw unreserved pool funds.

## How consensus is used

**Rules round (`verify_program`).** Each validator, on its own fetch of the page:

- reduces the HTML to text itself, keeping the content of collapsed product tabs that a text render drops;
- picks the slice of the page that best covers the product;
- asks its model for each rule's value **for that product** with a **verbatim quote**.

Deterministic code then keeps a value only if the quote is on that validator's copy of the page and the number is one of the whole numbers printed in the quote, so 5 never matches inside 50. Every enforced rule is reduced to `MATCH`, `MISMATCH` or `NOT_STATED`. Clauses are checked by plain code as `PRESENT` or `ABSENT`; whitespace, case and punctuation are ignored.

A validator accepts the leader only if:

- the status vector `{status, rules, clauses}` is exactly equal to its own, and
- every quote the leader stores is on its own copy too.

The model never sees the firm's declared numbers, so it cannot "agree" with them.

**Conduct round (`deny` with `clause:<i>`).**

- The model sees three things: the pinned clause, the firm's reason fenced as untrusted text, and facts computed by code from the log. It never sees the raw trades.
- The facts are: hedged overlaps (opposite sides of one symbol open at once), weekend holds, shortest hold, share of trades under 60 s, maximum trades in one day, maximum lots and symbols.
- Validators must agree on the label exactly.
- An unclear, unparseable or "insufficient" answer counts as `NOT_SUPPORTED`, because the burden of proof is on the firm.

## Live run (studionet)

FTMO's public [Trading Objectives page](https://ftmo.com/en/trading-objectives/) lists several products with different limits on one page. It was read by validators; FTMO is not involved and PropCourt is not affiliated with any firm. The conduct-clause rounds use the [PropCourt Demo Firm](https://yoyoblair333-wq.github.io/propcourt/demo-firm-rules.html), a clearly labelled demo page. FTMO's objectives page has no conduct clauses.

| # | What happened | Result |
|---|---|---|
| Program 1 | FTMO **2-Step**, declared 10 % target, 5 % daily, 10 % max, 4 days | **ACTIVE**: all four MATCH, each with the exact sentence from FTMO's page stored on-chain |
| Program 2 | Adversarial: FTMO 2-Step declaring a **4 %** daily loss | **REJECTED**: `max_daily_loss_bp` MISMATCH (the page says 5 %) |
| Program 3 | FTMO **1-Step**, declared 3 % daily, 10 % max, 50 % consistency | **ACTIVE**: the 1-Step numbers, not the 2-Step ones from the same page |
| Program 4 | Demo firm, 2 conduct clauses | **ACTIVE**: rules MATCH, both clauses PRESENT |
| Payout 1 | $100k 2-Step account, +$4,000 over 5 days, worst day −$800. The firm denies citing "Maximum Daily Loss" | **PAID**: *denial overruled by code: max_daily_loss_bp was not breached*. Trader withdrew 0.32 test GEN |
| Payout 2 | 1-Step account, best day $7,000 of $10,000 | **BREACH**: `consistency_bp` (best day 70 % > 50 %), measured by code, nothing reserved |
| Payout 3 | Demo account; a EURUSD sell open inside a EURUSD buy. The firm cites the hedging clause | **SUPPORTED** by consensus → **DENIED** after the challenge window, reservation back in the pool |
| Payout 4 | Demo account closed out every day. The firm cites the weekend clause | **NOT_SUPPORTED**: *weekend_holds = 0, longest hold 2 hours* → **PAID** |

Every transaction hash, validator vote and the full state read back from the chain are in [docs/LIVE_EVIDENCE.md](docs/LIVE_EVIDENCE.md).

## State design

- **Program:** firm, name, product, rules URL, declared rules and clauses, split, conversion, trading-day offset, review window, demo size. Also status, the verified status vector, the stored quotes and the leader's reading notes. Pool fields: `balance`, `encumbered` (reserved for open requests) and `paid`.
- **Account:** program, trader, capital, request ids.
- **Payout:** canonical log and its sha256, the deterministic report, the reserved amount, status, the firm's ground and reason, label, rationale, appeals and timestamps.

Integrity rules:

- One log can't be submitted twice.
- A new log must start after the previous request's last trade.
- One open request per account at a time.
- A reservation is capped at the free pool, so the pool can never go negative.
- A firm can never withdraw reserved funds.

## Quickstart

```bash
pip install -r requirements-dev.txt
genvm-lint check contracts/prop_court.py
pytest tests/direct -q                      # 110 direct-mode tests (real GenVM SDK, web + model mocked)
python scripts/live_run.py                  # deploy + full story on studionet (free test GEN)
python scripts/evidence.py                  # re-render docs/LIVE_EVIDENCE.md from chain data
cd web && npm install && npm run build      # rebuild docs/app.js (the GitHub Pages app)
```

## Try it in the browser

1. Open https://yoyoblair333-wq.github.io/propcourt/ and click **Create / load test key**. This makes a studionet burner key in your browser, funded by the free test faucet.
2. Pick the Demo Firm program and click **Open demo account**.
3. Load a sample log (clean, hedged, daily-loss breach, weekend hold) and click **Preview**. Preview is a free view call that shows exactly what the code measured.
4. Click **Request payout**. A breach is refused at once. A clean log is reserved and, after the 3-minute review window, **Finalize** pays your test key.

## Honest scope

- The trade log is the trader's closed-trade statement. Measures are on realized (closed-trade) P&L because the contract has no intraday equity feed.
- The conduct round judges code-computed facts, so a clause about something the log can't show (e.g. copy trading between people) cannot be SUPPORTED.
- Testnet only. Not financial or legal advice. MIT licence.
