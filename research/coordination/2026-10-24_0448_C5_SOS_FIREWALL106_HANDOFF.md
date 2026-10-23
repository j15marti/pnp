# C5-SOS-FIREWALL106 handoff

Status: **PROVED/EXACT in the declared degree-four equality-SOS model; P versus NP remains OPEN.**

## Result

- Exact coefficient reconstruction verifies both local C5 identities.
- Every degree-four pseudoexpectation has `E[Y]=2` on a C5.
- The predecessor canonical degree-two functional has `E2[Y]=25/12` on the bare C5, so it cannot extend.
- The bare C5 is nevertheless SAT, with 30 labelled 3-colourings and `Y=2` on every colouring. Canonical nonextension is therefore not an UNSAT or hardness signal.
- The 12-vertex controls independently enumerate to 0 and 108 colourings, with 44 and 28 five-cycles. The six orbit equations have rank six and yield `(t,6t-2,t,2-4t,2-4t,t,t)`; PSD requires both `t >= 7/18` and `t <= 1/4`.
- The audit does **not** independently replay Role 4's separate 2.67MB/1,776-square certificate.

## Ladder/transport consequence

This is a restricted proof-system/representation theorem. It supplies no unrestricted deterministic time lower bound. A fixed refuted core is constant; disjoint replication has linear construction and direct template/component recognition. Any transport still needs

`L_old <= R + H + Q*tau*T_new^{<=}(g)`

with a positive remainder after source reads, recognition, construction, proof work, replay, and shared computation.

## Resources

- Program: `experiments/review/c5_sos_firewall106_audit.py`
- Raw: `results/raw/review/C5_SOS_FIREWALL106_raw.json`
- Report: `research/main/2026-10-24_0448_MAIN_C5_SOS_FIREWALL106.tex`
- 494 exact assertions, zero failures, about 21 seconds, Python standard library; peak space not measured.

## Highest-value next lemma

For one fixed NP-complete encoding, prove a source-charged all-decider acquisition/continuation dichotomy with a representation-independent obstruction `r(F)`, a positive transport remainder, and `r(F)/log N` unbounded on a growing family. C5-SOS-FIREWALL106 rules out canonical degree-two nonextension as that obstruction.
