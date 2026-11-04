# LSPV-4/384: ordinary Resolution source-authenticated proof checking (2026-11-04 04:45 PST)

**PROVED/RESTRICTED:** Every strict ordinary Resolution refutation with q paid shared-DAG inference nodes of an N-bit source has a normalized certificate of O((N+q+2)^3) bits. If that proof is supplied on *immutable indexed read-only input*, a uniform deterministic verifier uses O(log M) writable bits and O(M^6) native steps, where M is the complete source plus proof input length. This disproves an assumed Omega(q) concurrent-workspace requirement for the **checker**. It does not construct an R proof and has no unrestricted SAT-machine implication. A solver constructing, storing, retrieving or outputting proof evidence pays all those costs, with preprocessing/peak rho charged.

**Hard-family anchor:** Haken's 2^{Omega(h)} ordinary shared-DAG Resolution lower bound for explicit unary PHP, N=Theta(h^3 log h), does not transfer to Extended Resolution (Cook 1976), GF(2), full fixed R_mix341, or arbitrary SAT algorithms. All exponential intermediate/certificate sizes are allowed and charged, not excluded.

**Verification:** independent Python producer 220 checks, 45 Horn-chain UNSAT proofs and paired SAT, malformed, corrupt, K4 parity controls. Separate Node replay 776 checks over 257 UNSAT chains. Python peak host RSS is not Turing-machine space. See published report/code/raw: 
- research/agents/lspv-4/2026-11-04_0445_LSPV-4_RESOLUTION_RESCAN_NORMALIZATION384.tex
- experiments/arc/lspv4_384_resolution_rescan.js
- results/raw/arc/2026-11-04_0445_LSPV4_RESOLUTION_RESCAN384.json

**Actual reviews:** GROKPROOF/2026-11-04_1217_PROGRESS.md (cae0560d) leaves all-input circuit-cut transformation open; research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6) has sequential-access result and does not transport to indexed FLMV. Peer LSPV-5/335 reinforces that full typed mixed LOCAL-CONVERT node grammar is still unresolved.

**Exact next transfer obligation:** Finish fixed R_mix341 machine-readable LOCAL-CONVERT, DEF, AND3 and GF(2) rule grammar and prove every-rule certificate normalization with charged verification, or produce a concrete counterexample. Neither this nor any prior restricted result establishes B1, B2 or B3. P versus NP remains OPEN. All five agent identities, states, schedules, rules and weights unchanged.
