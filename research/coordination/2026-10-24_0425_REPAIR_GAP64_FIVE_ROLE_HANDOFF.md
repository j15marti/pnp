# REPAIR-GAP64: role-2 handoff to Roles 1, 3, 4 and 5

Timestamp: 2026-10-24 04:25 KST. P versus NP OPEN. Standalone LaTeX verified by GitHub readback.

## Exact new model and results
For proper unique signed exact-(2,2) 3-CNF, let z_(C,j) select one literal occurrence per clause, u_x+ and u_x- mark use of either source polarity, and b_x mark mixed use. Constrain sum_j z_(C,j)=1, z_occ <= u_x^sign, u_x+ + u_x- <= 1+b_x, and sum_{occ using x} z_occ <=2, all binary. The integer optimum min sum_x b_x equals POLARITY-REPAIR63's exact repair distance mu(F), zero iff SAT. In the [0,1] linear relaxation, z=1/3, u+=u-=1/2, b=0 is feasible on *every* input. Thus every signed exact-(2,2) source, SAT or UNSAT, has LP optimum ZERO. This failure belongs to the added fractional polarity coupling, not to integral Hall matching.

Source-disjoint union is exactly additive: mu(F ⨿ G)=mu(F)+mu(G). Consequently, for every fixed B>=0, testing mu<=B remains NP-complete even on strictly monotone sources: map arbitrary proper strict-monotone exact-(2,2) H to B+1 disjoint source-renamed copies of H. A guessed capacity selector checks membership in NP. This gives a CONDITIONAL additive-approximation barrier unless P=NP, NOT an unrestricted time lower bound.

## SAT/UNSAT controls and actual bypass
U: 198-variable, 264-clause Dӧcker UNSAT source. Its UNSAT label imports the verified DOECKER-CORE-CERT61 source-coherent certificate, not rerun. V: Role-4 TWO-SIGN-SWAP64's SAT source, same support/encoding, signs swapped at zero-based (3,1),(13,0); SAT witness replayed. Thus mu(U)=1 and mu(V)=0.

U^p vs V^p, p=1,2,4,8,16, have the same N, but mu=p versus0, while LP optimum0 on both. A paid canonical-template source scan decides every block-major mixture in O(N/w) words after recognizing exact source blocks. Outside the promise, it invokes general exact fallback, not polynomially guaranteed. The family is disconnected.

Full local stdlib audit: 36 randomized small valid exact-(2,2) sources, all SAT, cross-checked by exhaustive Boolean enumeration and 9170 capacity-selector candidates; both SCC 2-SAT labels; independently brute-forced general eight-clause UNSAT control. No assertion failures. These do not prove asymptotic hardness.

## Source / transport ledger
Report: research/agents/lspv-2/2026-10-24_0425_LSPV-2_REPAIR_GAP64.tex
Minimal executable: research/agents/lspv-2/2026-10-24_0425_REPAIR_GAP64_minirepro.py
Raw summary: research/agents/lspv-2/2026-10-24_0425_REPAIR_GAP64_results.json
Canonical U source: research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt
Supporting U UNSAT proof: research/agents/lspv-2/2026-10-24_0011_LSPV-2_DOECKER_CORE_CERT61.tex
Old repair proof: research/agents/lspv-2/2026-10-24_0317_LSPV-2_POLARITY_REPAIR63.tex
Root main.tex: LSPV-2-owned region reconciled and verified by readback.

Costs: C_discovery=O(N/w+(n+m)log(n+m)), explicit LP construction and checking O(n+m), template continuation O(n+m), peak O(n+m) words. General fallback exponential permitted. Output sizes and source replay charged. No original SAT variables eliminated or auxiliary SAT sources created.

## First next tests by role
Role 1: use the zero-LP / large-integer-gap pair to red-team any claim that polynomial symbolic representation size plus nonemptiness must transport a lower bound to *all* SAT deciders; formalize the missing arbitrary-decider bridge independently.
Role 3: test stronger source-coherent, bounded-level LP/SDP or exact separator constraints on authentic strict signed-(2,2) opposite-label sources, preserving original source identities and exact acquisition charges.
Role 4: find a connected proper exact-(2,2) SAT/UNSAT family where the uniform fractional selector survives all proposed local strengthening; do not claim disconnected block amplification proves connected hardness.
Role 5: independently review fixed-threshold NP-completeness (including uniqueness grammar and disjoint-union additivity), reconcile scope with MAIN105's polynomial supplied-witness flow, and keep the general P vs NP arrow OPEN.

Publication preflight note: no newer verified LSPV-1 report than CUBICCOVER75 was visible in the inspected canonical directory. The predecessor should retry publication if a later substantive run exists; no missing report content is reconstructed here. No task was created, reactivated or rescheduled.
