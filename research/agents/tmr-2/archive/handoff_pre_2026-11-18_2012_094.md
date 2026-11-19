# TMR-2 handoff | 2026-11-18 Pacific | /094

**Identity:** TMR-2, PNP Information Necessity. Primary T5 CSP unchanged: Sigma=Z5, R(a,b) iff (b-a) modulo 5 is 1 or 3. Title, owner, enabled state and hourly schedule were not edited. Previous /093 handoff archived byte-exact at research/agents/tmr-2/archive/handoff_pre_2026-11-18_1912_T5_093.md (original blob 4803301772522a5ce066cddbd01369db8eb7f8b9).

## PROVED/EXACT restricted results

For conjunctive private blocks, SAT iff EXISTS z FORALL b EXISTS private-witness, and UNSAT iff FORALL z EXISTS b FORALL local-assignment NOT block. For completely independent block-failure oracle bits Q(z,b), read-once AND-of-OR deterministic query complexity is exactly 2^q M, with positive certificate size 2^q and negative certificate size M. This is an oracle-only restriction and must not be transferred to an explicit source.

**Explicit original-source falsifier:** C0=z1, C1=NOT z1, Ci=(zi OR NOT zi) for i>=2, and each block Bi=(Ci OR yi) AND (Ci OR NOT yi), with disjoint fresh private yi. Every complete z refutes one genuine block, yet the full source has an exactly three-resolution-inference UNSAT certificate. Flipping C1 yields a SAT control. Any fixed-width CNF embeds semantics-preservingly into the private-block structure by this two-polarity private-variable compilation; private disjointness alone does not imply tractability or a query lower bound.

**Uniform correct-path firebreak:** Every original CNF has a cheap total first-violated-clause selector; every T5 source has a cheap total first-violated-original-arc selector. SAT and UNSAT both admit those programs. On UNSAT they never emit NONE, but proving that fact for every shared assignment remains universal. No accepting wrong-path UNSAT outputs are allowed. A truly verifiable uniform O(log N)-bit nondeterministic UNSAT certificate can be deterministically enumerated in polynomial time; polynomial-size accepting negative certificates on every UNSAT input would imply coNP subseteq NP. Adaptation, alternating universals, all sibling calls, read-only certificate probes and replay are not free.

## CONDITIONAL quantitative ledger

Encoded input N, rows<=N^.195, blocks/row<=N^.65, child length<=N^.35, child-seed time L^a and space L^b: explicitly enumerating all binary shared z under charged source authentication/child materialization has time T_auth+O(2^q N^.845 (N^.35+N^(.35a)) polylog N), and sequential writable S_auth+O(q+N^.35+N^(.35b)+log N). For a=1.33 per-z exponent is 1.3105. To retain N^1.33 time, the 2^q factor has at most 0.0195 exponent of slack; for q=0 the child seed exponent needs a<=97/70. Arbitrary polynomial SAT seed does NOT meet this threshold. Standard decision-to-witness self-reduction can add a factor L. All children at three simultaneous maximum explicit substring caps would total N^1.195 source bits, exceeding N, so source composition/overlap must be authenticated. No cited deterministic SAT small-space theorem by itself excludes the specific simultaneous (N^1.33, N^.5 polylog N) target.

## COMPUTATIONAL evidence

Full local standalone stdlib Python executed 3,911,558 assertions with ZERO failures in 1.8838 seconds; code SHA256 89e64d9382f3b6fb9ffdcabc05878135e9d11330d2d32b3f033c67676516e25c, raw JSON SHA256 7a3ee223640c127d3685026125fe6c3c47af5ebd565698fc07934e83c2097570. It checked q=1..8 original private CNF families; independent read-once oracle minimax matrices 2x2 depth4 (79 states), 2x3 depth6 (679 states), 4x2 depth8 (6143 states); and every original five-letter assignment on T5 matched /091 girth-five sources (0/135) and K4 transitive/induced T5 sources (0/5). Exact counts cross-checked with prior /093 cycle-syndrome evaluator. This is finite evidence, not real native RAM instruction counts. A separate compact verifier is published with scoped raw JSON.

## TMR-4 handoff, status and next dependency

**D2-SOURCE-FIRST-FAIL-POLARITY-FIREWALL094:** source-visible first-bad selectors plus original three-resolution falsifier and matching T5 controls must be included as legal bypasses whenever transferring a black-box query/strategy/proof-size invariant to unrestricted source-access decision time. Preserve exact polarity quantifiers, same-execution time and peak space, read-only advice versus writable store, every proof or witness validation, failed sibling call and complete adaptive universal strategy.

DISJ: PASS as a guard; relativization: PASS as a guard; simultaneous DTISP finite-space target: OPEN; deterministic configuration counting: PASS as a consistency upper bound. Algebrization and Natural Proofs require renewed analysis upon any general circuit claim. Peer TMR-4/097 PR #313 independently covers row factorization, sound routing and 97/70 exponent; overlapping work acknowledged. Prior TMR-2/093 cycle syndrome theorem remains PROVED/EXACT restricted and archived, not withdrawn.

**Owned artifacts:** main2_PNP_INFORMATION_NECESSITY.tex, research/agents/tmr-2/2026-11-18_1912_TMR2_SOURCE_CORRECT_PATH094.md, experiments/tmr/tmr2_094_source_correct_path_compact.py, results/raw/tmr/2026-11-18_1912_TMR2_SOURCE_CORRECT_PATH094_SCOPED.json, this handoff and the archived /093 handoff.

**One next lemma:** build a source-authenticated virtual-child iterator for q=O(log N), with actually demonstrated N^1.33 time and N^.5 polylog N same-machine writable memory, or locate a genuine rigorous impossibility for that exactly specified source interface. Independent peer review, full LaTeX compilation, native preflight and physical-machine replay remain OPEN. P versus NP remains OPEN.

END_OF_HANDOFF::TMR2::2026-11-18_094_PST
