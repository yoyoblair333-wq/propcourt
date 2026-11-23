#!/usr/bin/env python3
"""
evidence.py - render docs/LIVE_EVIDENCE.md from docs/live/run.json.

    python scripts/evidence.py

Re-reads every transaction's latest status from studionet, then writes the table and
the contract state the live run read back. Nothing is typed in by hand.
"""

import json
import os

from genlayer_py import create_client
from genlayer_py.chains import studionet

from live_run import ROOT, jsonable, summarize

LIVE = os.path.join(ROOT, "docs", "live")
EXPLORER = "https://explorer-studio.genlayer.com"
SKIP = {"steps", "roles", "network", "contract", "explorer", "finished_at"}


def main():
    run = json.load(open(os.path.join(LIVE, "run.json")))
    c = create_client(chain=studionet)
    for st in run["steps"]:
        try:
            st["latest"] = summarize(c.get_transaction(st["tx"]))
        except Exception as e:
            st.setdefault("latest", {"error": str(e)[:120]})
    with open(os.path.join(LIVE, "run.json"), "w") as fh:
        json.dump(jsonable(run), fh, indent=1)
        fh.write("\n")
    out = ["# Live evidence (GenLayer studionet)", "",
           "Rendered by `scripts/evidence.py` from [`docs/live/run.json`](live/run.json), which "
           "`scripts/live_run.py` wrote from chain data. Studionet is a test network: GEN here has no value. "
           "All keys are throwaway test keys.", "",
           "| Item | Value |", "|---|---|",
           f"| Contract | `{run['contract']}` |",
           f"| Explorer | {EXPLORER}/address/{run['contract']} |",
           f"| Network | {run['network']} |"]
    for r, a in run.get("roles", {}).items():
        out.append(f"| {r} (throwaway key) | `{a}` |")
    out += ["", "## Transactions", "", "| Step | Tx | Status | Consensus | Execution | Validator votes |",
            "|---|---|---|---|---|---|"]
    for st in run["steps"]:
        L = st.get("latest") or st
        votes = ", ".join(L.get("votes") or [])
        out.append(f"| {st['step']} | `{st['tx']}` | {L.get('status')} | {L.get('result')} | "
                   f"{L.get('execution')} | {votes} |")
    out += ["", "## State read back from the contract", ""]
    for k, v in run.items():
        if k in SKIP or k.startswith("funded_"):
            continue
        out += [f"### {k}", "", "```json", json.dumps(v, indent=1, sort_keys=True), "```", ""]
    out.append(f"Run finished at {run.get('finished_at', '?')}.")
    with open(os.path.join(ROOT, "docs", "LIVE_EVIDENCE.md"), "w") as fh:
        fh.write("\n".join(out) + "\n")
    print("wrote docs/LIVE_EVIDENCE.md")


if __name__ == "__main__":
    main()
