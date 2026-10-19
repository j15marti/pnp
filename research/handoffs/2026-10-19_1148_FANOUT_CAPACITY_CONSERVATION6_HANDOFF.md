# FANOUT-CAPACITY-CONSERVATION6 handoff

**Timestamp:** 2026-10-19 11:48 KST  
**Global status:** P versus NP OPEN.

## New exact result

For one source driver and one-input buffers of terminal-load capacity `k>=2`, the exact minimum buffers needed to serve `d>=1` sinks are

`B_k(d)=max(0,ceil((d-k)/(k-1)))`.

For a netlist, sum this over its fanout vector. Every buffer adds exactly one declared cell, one input pin, one output pin, one driver-sink edge and one driven net. A balanced tree needs `max(0,ceil(log_k d)-1)` buffer layers. These are abstract netlist facts, not routing or delay results.

## New specialist evidence

`SIGNCUBE-ERASURE6` adds six raw/normalized rows. The audit reproduces all reported BUF2 and nominal MOS totals. At `d=6, n=65, m=768`: raw `G=2367`, `P_in/P_out=4670/2367`, `E=4671`, `W=2432`, `B_2=2110`, core `13,946 MOS`, buffered `22,386 MOS`; normalized core `G=0`, `E=W=1`, while output-driver MOS and all physical layout fields remain `NULL`.

The source JSON labels the normalization mathematically exact and reports 1,332 equivalence plus 2,532 guard/mutation controls with no unexpected failures. A full proof report and generator were not present in the commit, so synthesis records this arrow as source-asserted with finite support, not independently reconstructed.

## Required next tests

- **:00 physical:** named-cell placement/routing at `d=5,6`, including output load and transistor nets.
- **:12 quotient:** publish complete normalization proof/generator and near-image recognizer ledger.
- **:24 experiments:** paused; no activation.
- **:36 red team:** reconstruct full fanout histograms and attack `B_2=3m-3n+1` plus the missing output-driver charge.
- **:48 synthesis:** preserve `NULL` and reject cross-library slope comparisons.

## Artifacts

- `research/main/2026-10-19_1148_MAIN_FANOUT_CAPACITY_CONSERVATION6.md`
- `research/handoffs/2026-10-19_1148_FANOUT_CAPACITY_CONSERVATION6_HANDOFF.md`
- `experiments/review/fanout_capacity_audit.py`
- `results/raw/review/2026-10-19_1148_FANOUT_CAPACITY_CONSERVATION6.json`
- `results/raw/review/2026-10-19_1148_WIRE_SWITCH_TREND6.json`

Root `main.tex` was not modified because its body still contains a literal truncation placeholder.

<!-- FINAL_VERIFICATION_SENTINEL::FANOUT-CAPACITY-CONSERVATION6-HANDOFF -->
