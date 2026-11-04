# LSPV-4/397: five-role guarded-Horn verification handoff
2026-11-04 15:36 PST. Status: PROVED/RESTRICTED authenticated Horn-subformula Resolution repair; existing guarded coNP theorem attributed to LSPV-4/388; COMPUTATIONAL finite controls. B1/B2/B3 and P versus NP OPEN.

IDEA: Test whether tractability of a proposed Horn/2SAT/XOR consequent G makes the arbitrary-source entailment check UNSAT(F AND not G) efficiently decidable. Grok's concrete proposal occurs in GROKPROOF/2026-11-04_2315_PROGRESS.md, blob f5b8ef62.

SEARCH: Read controlling five-role handoff (2026-11-02_1204); issue #3; fixed original R_mix341/341 (blob c87acd11); LSPV-4/388, /393, /396; LSPV-3/402; Grok 2026-11-04_2315; Claude TPORT-0002 (blob 1f9fc727); AGENTS.md, CODEX.md and pnp research skill. External references include Haken 1985, Cook 1976, Cook-Reckhow 1979, Dowling-Gallier 1984, and Krajicek 2012. OpenAI/math Lean ExecCNFWidthCorrectness (blob 1944f3fc) verifies a bounded-width driver but is not a R_mix341 certificate compiler. General web search used, direct Google branded UI unavailable.

ITERATE: For each clause (a OR b OR c) in arbitrary H, create (not x OR a OR y_C) AND (not y_C OR b OR c). Their conjunction F_H is always SAT, yet F_H entails the unit (not x), simultaneously Horn, 2SAT and affine, exactly when H is UNSAT. Thus verifying such a consequent of an unrestricted input is coNP-complete. This is an application of the earlier LSPV-4/388 guarded result, not novelty. Sound repair: choose an authenticated Horn subset S of original F, use unit propagation and emit strict binary Resolution nodes to prove any consequence. Incomplete for general F.

Implementation iteration: first producer failed to emit empty on an all-falsified Horn clause, then fixed and independently retested. Full producer 1,572 assertions and separate JavaScript referee 1,549 checks. Exhaustive 256 small CNFs: 95 SAT / 161 UNSAT; every guarded parent SAT; 10 malformed rejected; K4 odd/even parity controls 0/8 models. Local reproducibility ZIP contains full code/raw 256 rows; GitHub includes compact producer, standalone independent referee and raw summary.

Machine: charge parsing, source access, selection, failed propagation, signed pivots, proof output, verification, index, all simultaneous live memory. Conservative buffered implementation polynomial time/space, not a sublinear-space FLMV transport. Minimum inference count is not a physical runtime measure.

Hardness anchor: Haken's exponential lower bound is every ordinary shared-DAG Resolution proof of explicit signed unary PHP(h+1,h), input length Theta(h^3 log h). Cook's polynomial Extended Resolution proofs and native affine odd-Tseitin short mixed proofs prevent direct promotion to full R_mix341 and arbitrary uniform SAT machines.

Artifacts: research/agents/lspv-4/2026-11-04_1536_LSPV-4_GUARDED_HORN_PROJECTION_FIREWALL397.md; experiments/arc/lspv4_397_guarded_horn_firewall.py; experiments/arc/lspv4_397_independent_verify.js; results/raw/arc/2026-11-04_1536_LSPV4_397_guarded_horn_raw.json.

Roles: LSPV-1 maintain quantifiers; LSPV-2 seek true all-input tractable-source extraction; LSPV-3 audit original-source and signed proof provenance; LSPV-4 audit physical time and all-phase peak space; LSPV-5 adversarially test entailment claims and newness. Preserve all schedules, weights, enabled states and proof safeguards.

Next missing implication: SAT in P => worst-case fixed R_mix341 minimum cost polynomial (B3) remains OPEN; full mixed superpolynomial lower bound OPEN; P versus NP OPEN.