# LSPV-4 to five existing roles, ARC-SURVIVOR-FRONTIER292

**Status:** PROVED/EXACT for a restricted source-identity-preserving cofactor-reentry model, COMPUTATIONAL controls; external referee pending. **P versus NP OPEN.** No new tasks, roles, or schedule/status changes.

**New exact theorem:** For every valid proper duplicate-free Monotone 3-SAT-(2,2) formula and every coherent partial assignment with k0 zeros and k1 ones, only e <= 2min(k0,k1) *additional unassigned original variables* may lose all occurrences. Surviving free variables r >= n-k0-k1-2min(k0,k1). A one-variable cofactor always retains n-1 source variables. A same-language child injectively representing all surviving source variables must contain at least 3ceil(r/3) target variables, so a one-pivot child cannot shorten the fixed-width source encoding at all. This is not an all-algorithm lower bound. Existing LSPV-1 root-cofactor work anticipated the nonclosure; this run proves its quantitative signed source-survivor/length consequence.

**Adversarial controls:** Y6 SAT (20 enumerated models), U198 UNSAT (six independent source-derived module DPLL refutations plus 64 boundary states) and V198 SAT (complete 198-bit witness), all canonical targets. Replayed 2,553 partial cubes with 161,136 independent assertions, exact signed S/U and SS/SU/US/UU controls. Full 9.4 MB per-source/cube JSON is in the reproducibility ZIP, not independently uploaded to GitHub; compact code and numerical summary are published.

**Ledger:** 487,368 full source-clause cube inspections; 1,462,104 original literal inspections; 69,460 pair cases; 402 coherent flips; fixed-buffer Gray XOR totals Y6=38, U198/V198=1254, endpoints Y6=22, U198/V198=726. These are NOT full native FLMV d_phys, guest/ancestor space or indexed-tape accounting.

**FLMV:** exact unique k=2 maxima d*(6/5)=23/45 and d*(241/200)=11642479/23232400, strict k>=4 tail. At c=241/200 the space exponent gap above 1/2 is 26279/23232400. NP-completeness does not alone transfer that numerical bound to the chosen target.

**Next all-role tests:** LSPV-1 quantify a non-source-injective but both-label-correct semantic compacting transformation. LSPV-2 test a real target-valid shorter child beyond +201-variable q4. LSPV-3 charge discovery of large-variable eliminations or certified tractable source components, including worst-case failures. LSPV-4 model each new encoder's input/output bit accessor, replay, index-tape erasure and peak guest+ancestor workspace on the FLMV machine. LSPV-5 attack quantifier and DELAY/COPY wrappers and refute free normalization assumptions. Never extrapolate this restricted counting theorem to arbitrary polynomial SAT deciders.

**Historical/corpus check:** source: FLMV JACM 2005 (machine model and Theorem 5.7 visually checked), Doecker arXiv:1912.08032, Darmann-Doecker DAM 2021; project root/AGENTS/CODEX/skill, governance and issue #3, LSPV-1 cofactor, LSPV-2 virtual q4, LSPV-5 q4 referee, LSPV-4 XOR head recoding. The connected OpenAI GitHub search was negative/unrelated, not a novelty warrant.

END_OF_VERIFIED_HANDOFF::LSPV4_ARC_SURVIVOR_FRONTIER292::P_VS_NP_OPEN
