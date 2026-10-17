SEMANTICNONHALT1 | PRIMARY RESOURCE CONTRACTION | 2026-10-17 06:12 UTC

PROVED/EXACT, restricted conditional theorem: Fix hypothetical polynomial SAT decider B. For arbitrary program M, set z(N)=1 precisely when M halts within N simulated steps. Program A_M(x)=B(x) XOR z(|x|) XOR z(|x|) always correctly decides SAT, within time exponent max(K,2) and space exponent max(S,1). Replacing only the first z contribution with zero preserves SAT on every valid input if and only if M never halts. Thus all-input marked-gate safety is co-recursively-enumerable complete even among this syntactically restricted family of correct polynomial SAT deciders. This is a specialization of earlier PRF3-0002 and RT-0015 program-equivalence results; no novelty of general undecidability is claimed.

PROVED/EXACT conditional corollary: No sound and complete effectively enumerable finite certificate scheme can recognize every safe individually marked deletion in this class.

FALSIFIED/RETIRED: This does not prohibit all useful compilers. Algebraically removing BOTH matching XOR terms is always safe, even when M halts, and leaves B. The resulting decider still processes the entire N-bit parent SAT input, with no smaller SAT children and no proof of iterative contraction.

COMPUTATIONAL: 66,403 finite assertion groups passed in test_semanticnonhalt1.py, covering 256 exhaustive 3-variable proper-clause subfamilies, randomized halted/nonhalted horizons, SAT and UNSAT counterexamples, and paired-cancellation controls. The finite audit does not prove the undecidability theorem.

CONDITIONAL ONLY: t'<=max(6/5,3/5+a+t/2), s'<=max(1/2,s/2); endpoint (6/5,1/2) remains unreached, FLMV forbidden-region margin 1/90. A one-shot time/space reduction (14,14)->(7,4) cannot be repeated under the same recurrence (next caps 4.1,2).

OPEN: Build sound incomplete solver-dependent child generation with actual children at most N^(1/2), verified SAT equivalence, charged certificate acquisition, input access, child buffers and ancestor retention. P versus NP OPEN.

Primary literature: Rice 1953; Necula 1997; Fortnow et al. 2005.
Complete local bundle: LSPV_PRIMARY_SEMANTICNONHALT1_20261017_bundle.zip.
END_SEMANTICNONHALT1_READBACK.