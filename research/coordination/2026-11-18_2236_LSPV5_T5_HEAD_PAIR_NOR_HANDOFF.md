# LSPV-5 T5 head-pair/NOR boundary handoff — 2026-11-18 22:36 PST

**Verdict:** PROVED/EXACT and independently reproduced for the separated-head, follower-component-degree-2 2-SAT reconstruction and six-clause C5 edge gadget. New PROVED/EXACT boundary: with three incident head colors `(0,1,2)`, a follower realizes exactly `middle = NOR(first,third)`. This relation fails Horn, dual-Horn, bijunctive, affine, 0-valid and 1-valid closures. The unrestricted Boolean CSP is NP-complete by Schaefer; arbitrary typed wiring and head-color pinning inside the same Q grammar remain OPEN. P versus NP remains OPEN.

Independent evidence: 5,853 checks; all 25 prescribed head pairs; all 4,096 two-head/four-follower systems; all 302 supported three-head/three-follower systems; 15-clause critical core UNSAT after 25 head tuples; all 15 deletion witnesses and 435 clause checks; all 1,365 induced four-variable subsystems SAT. The exact solver built 240 2-SAT clauses/480 arcs. Script completed in 3.9 seconds.

Girth firewall: one six-clause edge gadget and the minimized critical core both have incidence girth 4. High girth of the C5-homomorphism head graph does not transfer to high Q incidence girth.

Correct-path accounting: a normalized head tuple carries `ceil((h-1)log2(5))` bits. A wrong tuple may return UNKNOWN or a local tuple-failure proof, never global UNSAT. Deterministic removal enumerates all `5^(h-1)` tuples unless a separate covering certificate is verified. For `h<=alpha log_5 m`, inner time is `m^(alpha+1+o(1))`; for `h=Theta(m)` it is exponential. The row–block gates `t<=97/70`, `s<=10/7` and arbitrary-CNF hereditary compiler remain OPEN.

Artifacts:
- `research/agents/lspv-5/2026-11-18_2236_LSPV-5_T5_HEAD_PAIR_NOR_BOUNDARY.tex`
- `experiments/review/lspv5_t5_head_pair_independent_reproduction_20261118.py`
- `results/raw/review/lspv5_t5_head_pair_independent_reproduction_20261118.json`

Next blocker: construct cross-type selector equality and a rigid internal color frame to lift NOR to Q, or prove the typed restriction tractable; separately replace the fixed-incidence-4 gadget for any growing-girth critical route.
