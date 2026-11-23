# Live evidence (GenLayer studionet)

Rendered by `scripts/evidence.py` from [`docs/live/run.json`](live/run.json), which `scripts/live_run.py` wrote from chain data. Studionet is a test network: GEN here has no value. All keys are throwaway test keys.

| Item | Value |
|---|---|
| Contract | `0x6Af674cF2196B7a9067380F74666C94352bFf485` |
| Explorer | https://explorer-studio.genlayer.com/address/0x6Af674cF2196B7a9067380F74666C94352bFf485 |
| Network | studionet (chain 61999, https://studio.genlayer.com/api) |
| firm (throwaway key) | `0xE7fd753cF1101BE80c43165FdA4b4c8E92FCA841` |
| trader (throwaway key) | `0x89730A91050EE853c6e7A6cD5385589548A6c603` |
| trader2 (throwaway key) | `0x6661FBa5AeB4aEDB7E7316D5CC24B28DE178028e` |
| trader3 (throwaway key) | `0xe8B2001a4390c0c8f96702591193BDf29d2A5581` |

## Transactions

| Step | Tx | Status | Consensus | Execution | Validator votes |
|---|---|---|---|---|---|
| deploy | `0x6cfaba9b544d01d75525ec4f6bc25e1f74038cff904d3b9992281011468cd66a` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, agree, agree |
| register program #1 FTMO 2-Step (declared 5/10/10 %, 4 days) | `0x3db0bc48d600b964414fe423fed8381af7a7d4fa1fa923b68ffda07650b61623` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| register program #2 FTMO 2-Step, adversarial: declares 4 % daily loss | `0xfa6758a68e3c081303f6072665575426dc2182c20eb8b1edbf966bf5ad316efa` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| register program #3 FTMO 1-Step (3 % daily, 50 % consistency) | `0xd9de0a7d2ce3bdec9638b98b16fc92b494455f49041bf26690e42b89ff0a2248` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| register program #4 PropCourt Demo Firm (conduct clauses, demo accounts) | `0xeb1843bfea4683558edf38becddb3e8b07aa5cfcbb6606aa80a5e708308bd9cb` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, agree, agree |
| verify_program #1 (consensus) | `0x4e134021b002463028a8d72c78b291fa3906babc0b4d1f7b08e8e1b00cd80753` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| verify_program #2 (consensus) | `0x49db8cd18bdce3c07f09ace25e4ad5afcf8bc568ddc77627921787b9423fef89` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| verify_program #3 (consensus) | `0xe80ba1b67e7d3a054861f6236ab7b2ac5503e0b60f9f8fa5f6e9724b5b0e8027` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| verify_program #4 (consensus) | `0x3beed80a58f439ca4fcc1d8b7c41fda0ea4f6d4dda57850ccd5854bf2d050ef5` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| open_account #1 on program #1 ($100k) | `0x82f815c3dce362a252b18aef3ea18d228e91d0051f05d89151fbd6e1aa1a5773` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, agree, idle |
| request_payout #1 (clean log) | `0x6d8e96d3235e92ae1f978dfb8ec9d128dd567f26fcd7f0df5c16a7a11d1ae94e` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, agree, idle |
| deny #1 citing rule:max_daily_loss_bp (false) | `0x9016b3eb36dda38906c02118e82acfd7a599c914f0c86beb8b15b1db7309000d` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, agree, idle |
| open_account #2 on program #3 ($100k) | `0x17157bc0b6fb26ba3dc6cbaf51a4c4b993ec6aad3a3dbec20d54f0ec2811ee77` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, agree, idle |
| request_payout #2 (best day 70 % of profit) | `0x5f1222d4f0386ab56e811790aea18a2d0459803ef2d24ebbc4a5443055046b2d` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| open_demo_account #3 on program #4 | `0xbba19e0965c9a94bd3e77199d24ea500a1a8989a734f6a76e60f20d280ce156b` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, agree, idle |
| request_payout #3 (hedged log) | `0x97979a338dd9f5f2a134dd334335f57365d976e649dd965f9bdce43c2afea029` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| deny #3 citing clause:0 hedging (consensus) | `0xbef22a8243d522d160a33cfeb403e8fa11edff403522aab2a65346913964222a` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| open_demo_account #4 on program #4 | `0xdb3a80fb539cc15454b3b5964dac62fa92dffecf4cf965eb791c785b856968f6` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, agree, idle |
| request_payout #4 (closed daily) | `0x88db812a55d5b72267aecbea52d3bde54b4dc1250ea72c64d94a10b36d9aabe7` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, agree, idle |
| deny #4 citing clause:1 weekend (consensus) | `0x6446e880affe9983861962ecc1d5e777f0d9aa53590fadb62022b26e666081c1` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| finalize #3 | `0x80c4b80e3e6143ba9bc7f4ecaebd3763156a1ed2cc545f247205623a3bc459c5` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| finalize #4 | `0x7aa6dc525c296c41d6c8d5803e77130056348904c3a31add1e8c86ea5e1414c0` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| withdraw (trader) | `0x2745dfe4a307b89bb01bc48ffa08f9dd0fc60ae06e30f1e1e5c9ec5d77d6f970` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, agree, agree |
| withdraw (trader3) | `0xc82dd2d601723659dab1a024dbe5c1b74938c0e556031695193ae5b06de5919d` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |

## State read back from the contract

### challenge_minutes

```json
3
```

### programs

```json
{
 "1": {
  "accounts": 1,
  "balance": "2680000000000000000",
  "clauses": [],
  "created_at": "2026-11-23T04:38:47Z",
  "day_offset_min": 60,
  "demo_capital_usd": 0,
  "encumbered": "0",
  "firm": "0xE7fd753cF1101BE80c43165FdA4b4c8E92FCA841",
  "free": "2680000000000000000",
  "id": 1,
  "name": "FTMO",
  "paid": "320000000000000000",
  "product": "2-Step",
  "quotes": {
   "max_daily_loss_bp": "and the Maximum Daily Loss Amount , which is 5% of the Initial Simulated Capital.",
   "max_loss_bp": "and the Maximum Loss Amount , which is 10% of the Initial Simulated Capital.",
   "min_trading_days": "The Minimum Trading Days rule requires the trader to achieve at least 4 Trading Days.",
   "profit_target_bp": "10% for the FTMO Challenge 5% for the Verification This rule applies to both phases (FTMO Challenge and Verification) of the FTMO Challenge: 2-Step ."
  },
  "reading_notes": {
   "_page": "25960 chars, model saw 14000 from offset 5695",
   "consistency_bp": "not stated",
   "max_daily_loss_bp": "ok",
   "max_loss_bp": "ok",
   "min_trading_days": "ok",
   "profit_target_bp": "ok"
  },
  "review_minutes": 3,
  "rules": {
   "consistency_bp": 0,
   "max_daily_loss_bp": 500,
   "max_loss_bp": 1000,
   "min_trading_days": 4,
   "profit_target_bp": 1000
  },
  "rules_url": "https://ftmo.com/en/trading-objectives/",
  "split_bp": 8000,
  "status": "ACTIVE",
  "verdict": {
   "clauses": [],
   "rules": {
    "max_daily_loss_bp": "MATCH",
    "max_loss_bp": "MATCH",
    "min_trading_days": "MATCH",
    "profit_target_bp": "MATCH"
   },
   "status": "ACTIVE"
  },
  "verified_at": "2026-11-23T04:39:22Z",
  "wei_per_usd": "100000000000000"
 },
 "2": {
  "accounts": 0,
  "balance": "0",
  "clauses": [],
  "created_at": "2026-11-23T04:38:56Z",
  "day_offset_min": 60,
  "demo_capital_usd": 0,
  "encumbered": "0",
  "firm": "0xE7fd753cF1101BE80c43165FdA4b4c8E92FCA841",
  "free": "0",
  "id": 2,
  "name": "FTMO",
  "paid": "0",
  "product": "2-Step",
  "quotes": {
   "max_daily_loss_bp": "Maximum Daily Loss Amount , which is 5% of the Initial Simulated Capital.",
   "max_loss_bp": "Maximum Loss Amount , which is 10% of the Initial Simulated Capital.",
   "min_trading_days": "The Minimum Trading Days rule requires the trader to achieve at least 4 Trading Days.",
   "profit_target_bp": "10% for the FTMO Challenge"
  },
  "reading_notes": {
   "_page": "25960 chars, model saw 14000 from offset 5695",
   "consistency_bp": "not stated",
   "max_daily_loss_bp": "ok",
   "max_loss_bp": "ok",
   "min_trading_days": "ok",
   "profit_target_bp": "ok"
  },
  "review_minutes": 3,
  "rules": {
   "consistency_bp": 0,
   "max_daily_loss_bp": 400,
   "max_loss_bp": 1000,
   "min_trading_days": 4,
   "profit_target_bp": 1000
  },
  "rules_url": "https://ftmo.com/en/trading-objectives/",
  "split_bp": 8000,
  "status": "REJECTED",
  "verdict": {
   "clauses": [],
   "rules": {
    "max_daily_loss_bp": "MISMATCH",
    "max_loss_bp": "MATCH",
    "min_trading_days": "MATCH",
    "profit_target_bp": "MATCH"
   },
   "status": "REJECTED"
  },
  "verified_at": "2026-11-23T04:39:42Z",
  "wei_per_usd": "100000000000000"
 },
 "3": {
  "accounts": 1,
  "balance": "1000000000000000000",
  "clauses": [],
  "created_at": "2026-11-23T04:39:05Z",
  "day_offset_min": 60,
  "demo_capital_usd": 0,
  "encumbered": "0",
  "firm": "0xE7fd753cF1101BE80c43165FdA4b4c8E92FCA841",
  "free": "1000000000000000000",
  "id": 3,
  "name": "FTMO",
  "paid": "0",
  "product": "1-Step",
  "quotes": {
   "consistency_bp": "the Consistency rule requires that your Best Day does not represent more than 50% of your total profit .",
   "max_daily_loss_bp": "Maximum Daily Loss Amount , which is 3% of the Initial Simulated Capital.",
   "max_loss_bp": "Maximum Loss Amount , which is 10% of the Initial Simulated Capital.",
   "profit_target_bp": "The Profit Target for the FTMO Challenge is calculated as 10% of the Initial Simulated Capital."
  },
  "reading_notes": {
   "_page": "25960 chars, model saw 14000 from offset 7608",
   "consistency_bp": "ok",
   "max_daily_loss_bp": "ok",
   "max_loss_bp": "ok",
   "min_trading_days": "not stated",
   "profit_target_bp": "ok"
  },
  "review_minutes": 3,
  "rules": {
   "consistency_bp": 5000,
   "max_daily_loss_bp": 300,
   "max_loss_bp": 1000,
   "min_trading_days": 0,
   "profit_target_bp": 1000
  },
  "rules_url": "https://ftmo.com/en/trading-objectives/",
  "split_bp": 8000,
  "status": "ACTIVE",
  "verdict": {
   "clauses": [],
   "rules": {
    "consistency_bp": "MATCH",
    "max_daily_loss_bp": "MATCH",
    "max_loss_bp": "MATCH",
    "profit_target_bp": "MATCH"
   },
   "status": "ACTIVE"
  },
  "verified_at": "2026-11-23T04:40:03Z",
  "wei_per_usd": "100000000000000"
 },
 "4": {
  "accounts": 2,
  "balance": "2824000000000000000",
  "clauses": [
   "Hedging, holding opposite positions in the same instrument at the same time, is not allowed.",
   "Positions may not be held over the weekend; close all trades before the Friday market close."
  ],
  "created_at": "2026-11-23T04:39:14Z",
  "day_offset_min": 60,
  "demo_capital_usd": 100000,
  "encumbered": "0",
  "firm": "0xE7fd753cF1101BE80c43165FdA4b4c8E92FCA841",
  "free": "2824000000000000000",
  "id": 4,
  "name": "PropCourt Demo Firm",
  "paid": "176000000000000000",
  "product": "Demo Evaluation",
  "quotes": {
   "max_daily_loss_bp": "Your losses on any one trading day may not reach 5% of the initial account balance.",
   "max_loss_bp": "Your balance may never fall by 10% or more below the initial account balance.",
   "min_trading_days": "You must trade on at least 3 trading days before requesting a payout."
  },
  "reading_notes": {
   "_page": "1049 chars, model saw 1049 from offset 0",
   "consistency_bp": "not stated",
   "max_daily_loss_bp": "ok",
   "max_loss_bp": "ok",
   "min_trading_days": "ok",
   "profit_target_bp": "not stated"
  },
  "review_minutes": 3,
  "rules": {
   "consistency_bp": 0,
   "max_daily_loss_bp": 500,
   "max_loss_bp": 1000,
   "min_trading_days": 3,
   "profit_target_bp": 0
  },
  "rules_url": "https://yoyoblair333-wq.github.io/propcourt/demo-firm-rules.html",
  "split_bp": 8000,
  "status": "ACTIVE",
  "verdict": {
   "clauses": [
    "PRESENT",
    "PRESENT"
   ],
   "rules": {
    "max_daily_loss_bp": "MATCH",
    "max_loss_bp": "MATCH",
    "min_trading_days": "MATCH"
   },
   "status": "ACTIVE"
  },
  "verified_at": "2026-11-23T04:40:28Z",
  "wei_per_usd": "100000000000000"
 }
}
```

### payouts

```json
{
 "1": {
  "account_id": 1,
  "amount": "320000000000000000",
  "appeals": 0,
  "capped": false,
  "challenge_ends": "2026-11-23T04:44:02Z",
  "closed_at": "2026-11-23T04:41:02Z",
  "decided_at": "2026-11-23T04:41:02Z",
  "facts": {
   "hedged_overlaps": 0,
   "longest_hold_hours": 3,
   "max_lots_x100": 100,
   "max_trades_in_one_day": 1,
   "share_under_60s_bp": 0,
   "shortest_hold_seconds": 3600,
   "symbols": [
    "EURUSD"
   ],
   "trades": 5,
   "weekend_holds": 0
  },
  "filed_at": "2026-11-23T04:40:53Z",
  "ground": "rule:max_daily_loss_bp",
  "id": 1,
  "label": "",
  "reason": "Payout denied: the account breached the Maximum Daily Loss.",
  "report": {
   "best_day_cents": 150000,
   "best_day_share_bp": 3750,
   "breaches": [],
   "capital_cents": 10000000,
   "limits_cents": {
    "max_daily_loss": 500000,
    "max_loss": 1000000
   },
   "max_drawdown_cents": 0,
   "net_profit_cents": 400000,
   "target_reached": false,
   "trades": 5,
   "trading_days": 5,
   "worst_day_cents": -80000
  },
  "review_ends": "2026-11-23T04:43:53Z",
  "status": "PAID",
  "trades": [
   [
    "2026-11-02T09:00:00Z",
    "2026-11-02T11:00:00Z",
    "EURUSD",
    "buy",
    100,
    120000
   ],
   [
    "2026-11-03T09:00:00Z",
    "2026-11-03T12:00:00Z",
    "EURUSD",
    "buy",
    100,
    -80000
   ],
   [
    "2026-11-04T10:00:00Z",
    "2026-11-04T11:00:00Z",
    "EURUSD",
    "buy",
    100,
    150000
   ],
   [
    "2026-11-05T09:00:00Z",
    "2026-11-05T10:00:00Z",
    "EURUSD",
    "buy",
    100,
    60000
   ],
   [
    "2026-11-06T13:00:00Z",
    "2026-11-06T15:00:00Z",
    "EURUSD",
    "buy",
    100,
    150000
   ]
  ],
  "trades_hash": "e2ef8a205e537603d4970aef6ad17e10d1d15f95c8d3f368f6987ec1d6c44adb",
  "why": "denial overruled by code: max_daily_loss_bp was not breached"
 },
 "2": {
  "account_id": 2,
  "amount": "0",
  "appeals": 0,
  "capped": false,
  "challenge_ends": "",
  "closed_at": "2026-11-23T04:41:26Z",
  "decided_at": "",
  "facts": {
   "hedged_overlaps": 0,
   "longest_hold_hours": 1,
   "max_lots_x100": 100,
   "max_trades_in_one_day": 1,
   "share_under_60s_bp": 0,
   "shortest_hold_seconds": 3600,
   "symbols": [
    "EURUSD",
    "XAUUSD"
   ],
   "trades": 3,
   "weekend_holds": 0
  },
  "filed_at": "2026-11-23T04:41:26Z",
  "ground": "",
  "id": 2,
  "label": "",
  "reason": "",
  "report": {
   "best_day_cents": 700000,
   "best_day_share_bp": 7000,
   "breaches": [
    "consistency_bp"
   ],
   "capital_cents": 10000000,
   "limits_cents": {
    "max_daily_loss": 300000,
    "max_loss": 1000000
   },
   "max_drawdown_cents": 0,
   "net_profit_cents": 1000000,
   "target_reached": true,
   "trades": 3,
   "trading_days": 3,
   "worst_day_cents": 100000
  },
  "review_ends": "",
  "status": "BREACH",
  "trades": [
   [
    "2026-11-09T09:00:00Z",
    "2026-11-09T10:00:00Z",
    "XAUUSD",
    "buy",
    100,
    700000
   ],
   [
    "2026-11-10T09:00:00Z",
    "2026-11-10T10:00:00Z",
    "EURUSD",
    "buy",
    100,
    200000
   ],
   [
    "2026-11-11T09:00:00Z",
    "2026-11-11T10:00:00Z",
    "EURUSD",
    "buy",
    100,
    100000
   ]
  ],
  "trades_hash": "527628ed20c874a1449a23236dd69aa3cdd97cd2ff1b21afb27ba0f67436b950",
  "why": ""
 },
 "3": {
  "account_id": 3,
  "amount": "224000000000000000",
  "appeals": 0,
  "capped": false,
  "challenge_ends": "2026-11-23T04:44:59Z",
  "closed_at": "2026-11-23T04:45:26Z",
  "decided_at": "2026-11-23T04:41:59Z",
  "facts": {
   "hedged_overlaps": 1,
   "longest_hold_hours": 3,
   "max_lots_x100": 100,
   "max_trades_in_one_day": 2,
   "share_under_60s_bp": 0,
   "shortest_hold_seconds": 3600,
   "symbols": [
    "EURUSD"
   ],
   "trades": 4,
   "weekend_holds": 0
  },
  "filed_at": "2026-11-23T04:41:50Z",
  "ground": "clause:0",
  "id": 3,
  "label": "SUPPORTED",
  "reason": "On 2 Nov the trader held a EURUSD sell while a EURUSD buy was open: that is hedging.",
  "report": {
   "best_day_cents": 100000,
   "best_day_share_bp": 3571,
   "breaches": [],
   "capital_cents": 10000000,
   "limits_cents": {
    "max_daily_loss": 500000,
    "max_loss": 1000000
   },
   "max_drawdown_cents": 10000,
   "net_profit_cents": 280000,
   "target_reached": false,
   "trades": 4,
   "trading_days": 3,
   "worst_day_cents": 80000
  },
  "review_ends": "2026-11-23T04:44:50Z",
  "status": "DENIED",
  "trades": [
   [
    "2026-11-02T10:00:00Z",
    "2026-11-02T11:00:00Z",
    "EURUSD",
    "sell",
    100,
    -10000
   ],
   [
    "2026-11-02T09:00:00Z",
    "2026-11-02T12:00:00Z",
    "EURUSD",
    "buy",
    100,
    90000
   ],
   [
    "2026-11-03T09:00:00Z",
    "2026-11-03T10:00:00Z",
    "EURUSD",
    "buy",
    100,
    100000
   ],
   [
    "2026-11-04T09:00:00Z",
    "2026-11-04T10:00:00Z",
    "EURUSD",
    "buy",
    100,
    100000
   ]
  ],
  "trades_hash": "081a0f262908e4ebcd03442eec32b94d73913bef29dc53ae02d9b26de4be4016",
  "why": "The facts show one hedged overlap in EURUSD, establishing simultaneous opposite positions in the same instrument prohibited by the clause."
 },
 "4": {
  "account_id": 4,
  "amount": "176000000000000000",
  "appeals": 0,
  "capped": false,
  "challenge_ends": "2026-11-23T04:45:37Z",
  "closed_at": "2026-11-23T04:46:11Z",
  "decided_at": "2026-11-23T04:42:37Z",
  "facts": {
   "hedged_overlaps": 0,
   "longest_hold_hours": 2,
   "max_lots_x100": 100,
   "max_trades_in_one_day": 1,
   "share_under_60s_bp": 0,
   "shortest_hold_seconds": 3600,
   "symbols": [
    "EURUSD"
   ],
   "trades": 4,
   "weekend_holds": 0
  },
  "filed_at": "2026-11-23T04:42:28Z",
  "ground": "clause:1",
  "id": 4,
  "label": "NOT_SUPPORTED",
  "reason": "The trader held positions over the weekend in breach of our rules.",
  "report": {
   "best_day_cents": 90000,
   "best_day_share_bp": 4090,
   "breaches": [],
   "capital_cents": 10000000,
   "limits_cents": {
    "max_daily_loss": 500000,
    "max_loss": 1000000
   },
   "max_drawdown_cents": 0,
   "net_profit_cents": 220000,
   "target_reached": false,
   "trades": 4,
   "trading_days": 4,
   "worst_day_cents": -20000
  },
  "review_ends": "2026-11-23T04:45:28Z",
  "status": "PAID",
  "trades": [
   [
    "2026-11-09T09:00:00Z",
    "2026-11-09T10:00:00Z",
    "EURUSD",
    "buy",
    100,
    80000
   ],
   [
    "2026-11-10T09:00:00Z",
    "2026-11-10T10:00:00Z",
    "EURUSD",
    "buy",
    100,
    70000
   ],
   [
    "2026-11-11T14:00:00Z",
    "2026-11-11T15:00:00Z",
    "EURUSD",
    "buy",
    100,
    -20000
   ],
   [
    "2026-11-12T09:00:00Z",
    "2026-11-12T11:00:00Z",
    "EURUSD",
    "buy",
    100,
    90000
   ]
  ],
  "trades_hash": "b45a10d920ae0d1c975f3a8b39f31c72963518528f955f10ff6701f9bf4f3e8d",
  "why": "The facts show weekend_holds = 0, with a longest hold of only 2 hours across 4 trades, so nothing shows a position held over the weekend as the clause prohibits."
 }
}
```

### balance_before_withdraw_trader

```json
"320000000000000000"
```

### balance_before_withdraw_trader3

```json
"176000000000000000"
```

### stats

```json
{
 "accounts": 4,
 "challenge_minutes": 3,
 "labels": [
  "SUPPORTED",
  "NOT_SUPPORTED"
 ],
 "max_appeals": 1,
 "max_trades": 300,
 "owner": "0xE7fd753cF1101BE80c43165FdA4b4c8E92FCA841",
 "payouts": 4,
 "programs": 4,
 "rule_keys": [
  "profit_target_bp",
  "max_daily_loss_bp",
  "max_loss_bp",
  "min_trading_days",
  "consistency_bp"
 ],
 "schema": "propcourt.v1"
}
```

Run finished at 2026-11-23T04:47:00Z.
