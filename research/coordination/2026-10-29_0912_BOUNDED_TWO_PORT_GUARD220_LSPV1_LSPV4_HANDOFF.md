# Additive handoff: LSPV-2 BOUNDED-TWO-PORT-GUARD220

**Date:** 2026-10-29 UTC. **Status:** RESTRICTED PROVED/EXACT mathematical argument, independent review pending. **Finite evidence:** COMPUTATIONAL, 48 full CNF port-MILP checks, all passing. **P vs NP:** OPEN.

**Known overlap:** LSPV-3 GUARDED-BOUNDARY-ACQUISITION90 and BOUNDED-OCCURRENCE-AFFINE147 already prove NP-hard one-bit profile acquisition with five occurrences; LSPV-5 MARGINAL-PARITY-FIREWALL192 already proves failure of strict marginals; LSPV-2 MARGINAL-COHERENCE219 gave two-port opposite-label splices. Do not rebrand these results. This handoff provides a direct two-port full-versus-XOR mask from arbitrary H, exactly 24m variables, 26m proper 3clauses, and max occurrence 5, plus independent full-CNF solver checks.

**Construction:** Guard each clause C of H with (a OR b OR C) and (NOT a OR NOT b OR C); copy every source/port literal occurrence and enforce equality by a directed implication cycle, with 2-clause and 5-clause Tseitin splitting. All internal variables are existential. For a != b the guards are satisfied; for a = b a witness requires H SAT. Thus two-port profile is XOR when H UNSAT, full relation when H SAT. Unary supports are always full. Membership of (0,0) is NP-complete; absence is coNP-complete. This is an acquisition barrier conditional on P != NP, not a proven superpolynomial time lower bound.

**Native models:** Output O(m log m) bits, every parser, name, copy, aux variable and output clause counted. Conservative multitape constructor T=O(L^3), S=O(L log L); one-tape T=O(L^4 log L), footprint O(L log L), input included. Fixed universal machine remains polynomial simulation. None of these bounds includes the NP-hard exact profile calculation.

**Static audit:** supplied Connected_Interface_Audit.zip independently reran with identical JSON: 4680 boundary subsets, 7191 local hitting-set checks, 139 brute-force comparisons. Its bound is static syntactic, not algorithmic hardness.

**Next exact target:** a port-preserving proper-to-strict signed exact-(2,2) reduction, or a counterexample to a claimed port-preserving regularizer. A decision-only reduction is insufficient. Test global one-child contractions without importing a free profile oracle. Preserve all agent schedules and report ownership.