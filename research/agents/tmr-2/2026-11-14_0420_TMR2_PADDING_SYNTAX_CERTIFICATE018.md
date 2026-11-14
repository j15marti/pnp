# TMR-2/018: syntactic padding certificates can be almost the entire input while SAT is polynomial-time

**Pacific timestamp:** 2026-11-14 04:20 PST (America/Los_Angeles). **Agent:** TMR-2 Information Necessity. **New statement:** TMR2-SYN18, CANDIDATE/RESTRICTED with complete symbolic proof, awaiting independent TMR-5 or TMR-1 review. **Independent review target:** TMR-1/018 exponential-padding lemma. **Executed evidence:** COMPUTATIONAL. **General standard-encoding 3-SAT lower bound and P versus NP:** OPEN.

## 1. Exact machine and source model

Fix one explicit polynomially recognizable proper-3CNF binary encoding E. On valid E-strings x of L original data bits, define the injective padded formula representation

$$
p(x)=1^L0x0^{2^L},\qquad
N=|p(x)|=2L+1+2^L.
$$

Only a string of this exact form with x a valid E-source is a valid padded formula. Its SAT/UNSAT label equals the label of x; all other binary strings are MALFORMED. The suffix is syntactic padding, not additional clauses or a promise of free storage. A is ONE fixed finite total uniform deterministic multitape decider across ALL N, with one locally moving read-only input head beginning at the left marker, finite control and alphabet, arbitrary finitely many locally moving writable tapes, and physically charged transitions. The last data bit is at cell N. Count all real reads, head movements, parsing, memory, assignment enumeration, work-tape copying and malformed-input handling.

The all-exponent target for the honest source encoding E remains, without alteration,

$$
\forall A\ \forall k\ge1\ \forall C>0\ \forall L_0\
\exists F\in\mathrm{Valid}(E):
|F|\ge L_0,\quad T_A(F)>C(|F|+1)^k.
$$

No restricted result below implies this target.

## 2. New theorem: compulsory syntactic observation but inexpensive computation

**TMR2-SYN18 (symbolic theorem, independent review pending).** Let y=p(x) be any valid padded formula, with L=|x| and N=2L+1+2^L. Every correct total fixed deterministic *tri-label* decider A that distinguishes SAT, UNSAT and MALFORMED must physically read each of the 2^L data cells

$$
D_L=\{2L+2,\ldots,N\}
$$

during its complete execution on y. Hence its original-source observation set Q_A(y) satisfies

$$
|Q_A(y)|\ge 2^L=N-2L-1=(1-o(1))N,
$$

and a locally moving single original-input head started at left cell 0 must take at least N transitions to reach and observe the final data cell (in a read-before-move convention at least N+1 transitions are required).

**Proof.** Fix any j in D_L. The same-length string y^{(j)} obtained by changing exactly the jth zero suffix bit to 1 is not a padded valid formula, since the unary header and extracted x are unchanged, while its required suffix is no longer all zeros. Therefore A(y^{(j)})=MALFORMED, whereas A(y) is SAT or UNSAT. Suppose A did not read j in its entire run on y. Its run on y^{(j)} would have precisely the same current-cell input observations at each step. Induction on deterministic physical configurations gives exactly the same control, work tapes and work-head and original-input-head locations, then the same terminal label, a contradiction. This is a same-source-length complete-trace argument. It does **not** assume equal intermediate workspaces of independently reached prefixes, online input arrival or a compulsory particular SAT procedure. The j are distinct; thus all 2^L positions are necessary. The final data position is N, giving the physical head-distance charge. QED.

**Binary-output strengthening and limitation.** If invalid encodings are simply rejected rather than given a third label, the same necessity holds on every padded SAT source y: flipping a suffix bit changes YES to NO. On a valid padded UNSAT source the invalid neighbor also receives NO, so this two-label argument does **not** compel the suffix queries. Neither distinction permits counting the syntactic bits as compulsory SAT-specific semantic processing.

**Sharp counteralgorithm.** Independently checking TMR-1/018's construction, a single fixed total ordinary multitape decider can (i) make paid input scans to count actual N and verify the exact header, source and 2^L zero suffix; (ii) reject malformed strings before doing exponential work on the extracted x; and (iii) for valid strings copy x and enumerate assignments to its r literal occurrences, rejecting inconsistent repeated-variable choices and checking all clauses. Since E is explicit, r<=L and L<=log_2 N on valid y, so 2^r<=2^L<=N. A straightforward local-head implementation has

$$
T_{B}(y)=O(N(1+\log N)^c),\qquad
S_{B}(y)=O(\log N)
$$

for some fixed c, including all physical parsing, counting, buffer movement, assignment checks and output. For malformed y of actual length N, counting its length first, then checking its header and suffix, bounds the entire parse polynomially in N without allocating 2^L cells. This is a *uniform* decision algorithm, not a nonuniform lookup table, hidden oracle or an algorithm for ordinary unpadded 3-SAT. The construction works for both SAT and UNSAT x, including Horn, 2-SAT, affine/XOR, high-treewidth, products and auxiliary variables because the uniform exhaustive fallback is exact.

Thus the acquisition lower bound can be essentially maximal in N while the decision problem is in P relative to N. The large query count is caused by validating a rigid padded representation, not by nontrivial SAT semantics. Decoding the padded answer back into a standard E-input requires writing 2^L output bits to construct p(x); that E-to-p conversion is not polynomial in L. The non-honest encoding does not undermine P versus NP for E.

**Scope gap:** The statement permits polynomial workspace and unrestricted input rereads, but is a falsifier for *padding-invariant or syntactic-source-observation-only* bottlenecks, not an arbitrary-machine superpolynomial lower bound. No compulsory cost beyond reading/validating the given source is established. The special subclass used for finite tests has easy semantic classification and does not claim an unrestricted SAT solver.

## 3. Peer audit and why the result is additive

TMR-2/017's exact transcript certificate lemma is valid at its declared same-length, same-initial-state, deterministic model: any opposite-label neighbor differing only on never-read cells would force the same trace and answer. TMR2-SYN18 reuses that independently proved induction with **invalid** neighbors, explicitly separates ternary malformed correctness from two-label SAT membership, and quantifies how almost all observed cells can be syntactic rather than semantically decisive. TMR-2/017 used *valid* opposite-label neighbors in duplicated Horn gadgets and showed query complexity Omega(L/log L); it never asserted this new padding-syntax theorem.

TMR-1/018's polynomially balanced, two-way polynomial-translation safeguard survives this independent mathematical check. TMR-1's broader equivalence Q_E iff no fixed polynomial valid-input decider is a reformulation of P!=NP for honest E, **not** a proof. Exponential padding is outside the theorem's balanced-translation hypotheses. This report adds no independent confirmation of a complete physical generic machine compiler, but gives a fully specified uniform algorithm at the standard symbolic multitape level.

Hostile alternatives considered: scanning once, copying x to writable tape, unrestricted rereading, a compact global Horn/2-SAT/GF(2) invariant, a bounded-treewidth solver, sharing a subcomputation, disjoint products, renaming, and extra auxiliary variables all preserve the scoped theorem and its polynomial-N upper bound. They can avoid expensive SAT processing, but not the requirement to distinguish an actual altered suffix bit from the unaltered *valid* source. Nonuniform advice and unbounded-word operations are not needed.

## 4. Actual independent execution

The separately authored, OS-native CPython audit **executed** exactly the code published at `experiments/tmr/tmr2_padding_certificate018.py`. It uses a restricted binary payload: each payload bit means a proper three-distinct-variable four-clause gadget forcing the sign of one shared variable. It includes independent exhaustive Boolean evaluation of expanded proper 3-CNF gadgets. The padded scanner reads only the physically current source cell using a locally moving head. Its read/head-movement ledger is physically checked, whereas Python string parsing, allocation and brute-force evaluation are **not** presented as exact Turing-machine transition counts.

* 511 complete valid payloads of lengths n=0..8: 17 SAT and 494 UNSAT, with 95,064 actual current-cell reads and 96,086 modeled charged read-head transitions.
* 6,613 one-bit zero-suffix corruptions, exhaustively for n<=6 and with first/middle/last suffix controls for n=7,8, were all MALFORMED; 631,526 corrupt-source current-cell reads and 644,752 charged scanner transitions.
* 1,533 malformed-length or delimiter controls, plus 30 independently brute-force checked proper three-distinct-variable gadget families; zero failed assertions.
* Largest constructed padded input N=273 bits. Deterministic fixture digest SHA256: `e4e9db677c2d1525fcadebc0ad4b077fcc1babf97f5d1116efe1c940cbd2d172`.

The native test is finite COMPUTATIONAL evidence. It does not execute a generic E-3SAT compiler, native universal machine, full Horn/2-SAT/GF(2) benchmark, or all real counting micro-operations. The infinite-length claims rest on the symbolic proofs, and require independent TMR-5 review.

## 5. Primary source scope and recovered project evidence

Primary complexity references freshly checked for exact scope:

1. H. Buhrman and R. de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, Theoretical Computer Science 288(1):21-43, 2002, DOI https://doi.org/10.1016/S0304-3975(01)00144-X . This is **query/certificate complexity**, not an unrestricted SAT time lower bound.
2. L. Berman and J. Hartmanis, *On Isomorphisms and Density of NP and Other Complete Sets*, SIAM Journal on Computing 6(2):305-322, 1977, DOI https://doi.org/10.1137/0206023 . Polynomial-time encodings/isomorphisms, not arbitrary exponentially padded encoding invariance.
3. TMR-1/018 original, `research/agents/tmr-1/2026-11-14_0400_TMR1_PADDING_ENCODING_FRONTIER018.md`; TMR-2/017 original `research/agents/tmr-2/2026-11-14_0326_TMR2_SIGN_BLOCK_CERTIFICATE017.md` and original executed source/raw. The present report independently audits the central source-aware inference.

Current directive first read and rechecked by authenticated GitHub file SHA `47459817e66dccf1f3079e6c724c0fd2643e7bc4`. Root proof1.txt full 28,714 characters and blob SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`; proof2.txt complete authentic Git blob **1,051,196 characters** and SHA `930c5eeddafce656717f28055a7a9a755f44737c` (contents endpoint returned a misleading empty body); canonical main.tex authentic Git blob 2,530,965 characters and SHA `91b4e582c16cb7f60c9aa1ea2aebf09cd4caa2c6`. AGENTS.md, CODEX.md and the pnp-research skill were read; historical older LSPV role rules in those files are superseded by the newer directive. Current five TMR handoffs and issue #3 through TMR-1/018, peer original TMR-4/018 and TMR-5/015 were inspected; original counterexamples involving inexact physical source fetch and syntactic normalizers remain preserved.

**Publication:** This report and its executable and immutable raw evidence are separate files in the repository. Recheck each with GitHub readback. The source and raw were locally saved before publication. A full repository checkout/preflight, generic TM compiler, independent OS-native peer JS replay, and LaTeX compilation were not executed. Neither historical proof tracker nor canonical main.tex is modified.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The central unrestricted all-exponent computational-processing arrow remains OPEN; neither P=NP nor P!=NP has been established.

**Next target for TMR-2/TMR-5:** Replace syntactic/first-read certificates with a source-aware *processing* invariant that remains nontrivial under polynomially balanced encodings and arbitrary polynomial workspace, and first falsify it against once-copied inputs, Horn/2-SAT/Gaussian elimination, aggressive sharing, source rereading and early speculative computation.

END_OF_REPORT::TMR-2::018::2026-11-14_0420_PST
