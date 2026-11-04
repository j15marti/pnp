# Living log: worst-case minimum derivation cost  W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi)

Status discipline: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.
**P versus NP remains OPEN.** No superpolynomial W_R bound for a sufficiently strong fixed R, and no bridge SAT in P => W_R <= poly(N), is established by this log.

## 2026-11-04 12:50 UTC  (routine "DAG proof", scheduled run)

**Corpus reviewed:** research/main/...REFEREE334 (node-to-bit normalization, Pack(R) separation, B1/B2/B3 classification), the 2026-11-04 LSPV-1/388, LSPV-2/389, LSPV-4/384 handoffs (names only; bodies not re-verified this run), AGENTS.md allocation notes.

**Literature check (KNOWN THEOREM / pointers, not verified line-by-line):**
- Res(parity) is the smallest fragment of AC0[2]-Frege without a superpolynomial size lower bound. 2025-26 ECCC progress is depth-restricted only: exponential bounds for bit-PHP at depth up to about n^{1.5-eps} (ECCC TR25-118), n^{2-eps} (Bhattacharya-Chattopadhyay), a constrained bit-PHP method for larger polynomial depth (ECCC TR26-007), SETH-type bounds (ECCC TR25-188), and lifting plus a pure quadratic size bound (CCC 2026, Itsykson-Podolskii-Shekhovtsov). No new superpolynomial result for unrestricted Res(parity), bounded-depth Frege with parity, or Extended Frege was found.
- Relevance: any fixed R containing XOR/Res(parity)-type rules inherits "no known superpolynomial lower bound" as a hard frontier; depth-restricted hard families are the only currently usable anchors for hostile-control tests.

**Assessment of the proposed bridge (CANDIDATE, unchanged):**
- For a fixed natural R, "SAT in P => W_R <= poly" is not supported: Resolution already has Haken's exponential lower bound on PHP, and P=NP does not contradict it. The bridge is only plausible for R that p-simulates every polynomial-time SAT trace, which is p-optimality-level (REFEREE334 item 4). For the existential version (some R_M for the decider M) the bridge is trivial: proof = accepting computation trace. So the load-bearing open arrow is: a lower bound for a *fixed* strong R together with a simulation of all poly-time deciders by R. Both remain OPEN.
- Free choice of the optimal derivation does not weaken the lower-bound direction (agreed; search cost only adds work), but it also does not help the bridge, since the bridge needs an upper bound on min cost from an algorithm.

**Next target (suggestion):** formalise the weakest R for which the trace-simulation hypothesis is checkable (e.g. R = Resolution + explicit Cook extension with paid DEF nodes) and test it on the depth-restricted Res(parity) hard families above.

Changes relative to root main.tex: none (no ownership region touched). Claims not strengthened.
