# TMR-5/007: independent TMR-4/008 review and a three-bit-radius extension

**Date:** 2026-11-13 19:45 PST (America/Los_Angeles). **Role:** TMR-5 independent redteam and canonical synthesis. **Repository:** `j15marti/pnp`, main. **Statuses:** TMR-4/008 observation-set and pair-certificate claim **PROVED/RESTRICTED after independent mathematical review**, conditional on the declared input-head interface and valid source grammar; executed finite checks **COMPUTATIONAL**. New TMR5-TR7 three-bit-radius lemma **CANDIDATE pending TMR-1 or TMR-4 second review**. General superpolynomial deterministic SAT time bound and P versus NP **OPEN**.

## 1. Direct original-peer audit and precise repaired claim

Read the original TMR-4/008 report, exact JavaScript source and raw JSON, not just the peer handoff. Its proper 3-CNF source uses, in each independent three-variable block, all seven clauses banning tuples 1 through 7 plus a duplicate clause banning tuple 3. Every declared variable is covered by strictly positive proper three-dummy filler clauses. Under the explicit unary header `1^N 0 1^M 0`, each of the M clause records comprises three fields of one sign bit and w identifier bits, with `L=N+M+2+3M(w+1)`.

**Independent mathematical verdict:** The all-zero core/all-one dummy assignment satisfies the source. A one-bit sign change in an original block can either leave tuple 0 unbanned or make another formerly forbidden tuple available. A legal one-bit identifier mutation cannot destroy satisfiability by the original even-popcount ID construction and the all-positive filler. In each block, changing the two sign bits of the *duplicate* tuple-3 clause changes its forbidden tuple from 3 to 0, leaving all eight tuples forbidden. The r pairwise disjoint input-coordinate pairs are therefore valid same-length opposite-label differences. The deterministic transcript coupling is valid: if neither member of some pair were ever read on the SAT source, its UNSAT neighbor would have an identical complete execution. Arbitrary work tapes, rereads, output behavior, and adaptive access are allowed, subject only to the per-transition charged input observation cap q. Thus any correct fixed finite total deterministic multitape decider must satisfy

$$
T_A(x_r)\ge\left\lceil\frac rq\right\rceil.
$$

The TMR-4/008 MAY domain is sound for **every** concrete transition by revealing at most q previously unseen source positions at cost one or taking a zero-cost stutter. Correct terminal labels can be connected only after each certified pair has been hit. With `tau(V)` the minimal additional hitting-set cardinality, the potential `Phi(star_V)=ceil(tau(V)/q)`, `Phi(goal)=0` obeys `Phi(a)<=cost(a,b)+Phi(b)` for every reveal, stutter and terminal edge. The minimum abstract path cost equals `ceil(r/q)`; the source-bound initial state and both concrete terminal labels are handled. These are **restricted source-observation** facts, not a theorem that source labels must be computed by this abstraction or that its lower bound is superlinear. The complete concrete configuration remains unchanged in the simulation relation, but the abstract ghost set is an analysis aid, not work memory of A.

**Correction of a possible overreading:** TMR-4/008's statement "zero singleton" applies only to syntactically valid one-bit *literal-field* mutations, not to all binary header bits. No claim is made about two-bit identifier mutations or a universal absence of semantic sensitivity.

## 2. New theorem candidate TR7: no one- or two-sign-bit UNSAT neighbors, but many disjoint three-bit obstructions

Retain TMR-4/008's strict grammar, even-parity encoding and positive dummy fillers. In each independent three-variable block change only the final duplicate forbidden tuple: use mask list

$$
1,2,3,4,5,6,7,7
$$

rather than `1,2,3,4,5,6,7,3`. Let `z_r` denote the resulting SAT source. It has the **same exact** N, M, w, L and variables as the original /008 instance for each r. The all-zero core assignment and all-one dummy assignment satisfy `z_r`.

**Claim A:** Every Hamming-one literal-sign/identifier mutation that stays within the strict grammar is SAT, by the unchanged even-parity fresh-ID argument and positive fillers.

**Claim B:** Every same-length source obtained by changing *at most two literal-sign positions*, and no other positions, remains SAT. A filler clause remains true with all dummy variables equal to one, because it starts as three positive literals and at most two of them can be negated. For a core block, tuple 0 is the only absent forbidden tuple and tuple 7 is duplicated. If no changed clause bans 0, the all-zero core assignment remains valid. Otherwise one clause originally banning a nonduplicated tuple m in {1,2,3,4,5,6} has been changed to ban 0, and at most one sign change remains if m has Hamming weight one. If that remaining change affects another clause, that clause's original forbidden tuple becomes available unless the changed clause originally banned duplicate tuple 7. But a single sign change of mask 7 can produce only 3, 5 or 6, whereas m has weight one. Thus some nonzero tuple remains unbanned. If the first change consumes two flips, m itself becomes available and no other clause changes. Hence every block admits a satisfying local assignment. Other blocks can use zero.

**Claim C:** For each block g, change precisely the three sign positions of its final duplicate tuple-7 clause, turning tuple 7 into tuple 0. The block now bans all eight possible tuples, hence the entire formula is UNSAT. The r three-element difference sets `D_g` are pairwise disjoint, have the same length and valid grammar, and force every correct physical-source-reading A to inspect at least one coordinate from each. Consequently

$$
\tau(\{D_g\}_{g<r})=r,\qquad
T_A(z_r)\ge\left\lceil\frac rq\right\rceil.
$$

The least number of *sign-bit flips* required to change `z_r` from SAT to UNSAT is **exactly three**. This is not a claim about arbitrary multi-bit variable-ID changes, header mutations or a source-independent computational requirement. In both families `L=\Theta(r\log r)`, and the original core sign+ID-field count is `Q=24r(w+1)`. Thus the certified runtime lower bound is only `\Omega(L/\log L)`. Both families can be authenticated and evaluated by a single fixed fully paid polynomial-time structured fast path, with a correct exhaustive fallback on other inputs. They are explicit barriers to promoting low-order local sensitivity into superpolynomial processing.

The genuinely new increment is the **radius-two sign-ball robustness with an exact three-bit opposite-label threshold** while keeping growing disjoint certificate number. TMR-4/008 already supplied the pair threshold; no credit is claimed for its prior source construction or for the standard concept of block sensitivity.

## 3. Executed tests and distinctions

Two independent implementations were actually executed, with zero assertions failing.

**Native Python independent implementation:** `/mnt/data/tmr5_1945/tmr5_triple_radius_review007.py` was written without copying peer code. It generated complete strict binary sources, independently parsed them, checked the all-declared-IDs-used grammar, enumerated all single-sign mutations for seven sizes r=1,2,3,4,6,8,12, and **all 13,377 distinct two-sign-position mutations for r<=4**. For each changed source, local 3-variable SAT was checked exhaustively per block; dummy filler clauses were checked under all-true dummy values. It also checked 5,136 single-bit original-core ID neighbor witnesses and 36 triple-flip UNSAT certificates. A separate extra=3 baseline checked 36 original /008 two-bit UNSAT certificates and 1,101 one-sign controls. Largest complete source had 3,304 bits. Native Python exercised the standalone source-level algorithm, not a physical TM or generic fallback.

**Separate hosted V8 reimplementation:** Independently authored JS was directly run as a function, with the precise function text serialized into the published standalone Node-compatible JavaScript artifact `experiments/tmr/tmr5_triple_radius_review007.cjs`. It reproduced the same totals and zero failures. Published raw: `results/raw/tmr/2026-11-13_1945_TMR5_TRIPLE_RADIUS007_RAW.json`. Its independent parser and local-eight-assignment SAT check do not import or call the peer's code. This is **hosted V8 execution**, not evidence of native Node execution of the published file, a wrapper around another source, or native physical multitape transition simulation. The native Python executable was run separately and stored in the local outbox; the GitHub JS is the independently published reproducer.

No solver portfolio exclusion, all-length performance measurement, physical-machine transition count, LaTeX compilation, generic Horn/2-SAT/Gaussian-elimination suite or arbitrary-encoded-instance hard-case proof was executed. A constant-size block table and the positive filler pattern make the family easy; general polynomial SAT remains unproved.

## 4. Literature, dependencies, and next unresolved implication

Primary records consulted independently: Noam Nisan, "CREW PRAMs and Decision Trees," *SIAM J. Comput.* 20(6) (1991), 999-1007, https://doi.org/10.1137/0220062, concerns block sensitivity and CREW PRAM/decision-tree measures, **not unrestricted multitape SAT hardness**; Harry Buhrman and Ronald de Wolf, "Complexity Measures and Decision Tree Complexity: A Survey," *Theoretical Computer Science* 288 (2002), 21-43, https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf, distinguishes sensitivity from block sensitivity; Patrick Cousot and Radhia Cousot, "Abstract interpretation," POPL 1977, author bibliographic source https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml, explains conservative abstract semantics and their limitations. The concrete edgewise potential proof above is original to TMR-4/008 and reviewed here, not attributed to these papers.

Other contemporary dependencies: TMR-1/009 and TMR-2/009 strict identifier bit sensitivity; TMR-3/008 batch-locality single-head transport product (still CANDIDATE pending independent proof audit); TMR-4/007 certificate-prefix costs; TMR-5/006 compact affine/global parity hostile control. The strongest verified chain is `explicit valid opposite-label source differences -> forced paid source observations -> at most linear-size input-information cost`. The further arrow `source information or restricted crossing -> all-polynomial-exponent processing necessity for every fixed correct machine` remains **OPEN**. In particular, the exact input-bit measure L, all-length totality, constant program, both label correctness, arbitrary polynomial work space and same-machine T/S must remain quantified in any next claim.

**Next single target:** TMR-1 or TMR-4 independently prove or falsify TR7's radius-two argument. TMR-3 should receive a separate exact cut-and-paste/encoding review, and TMR-4 must isolate a program-dependent post-acquisition processing invariant which cannot be discharged by a compact block SAT table, GF(2), source reordering, rereading or recomputation. Do not infer separation from either scoped theorem.

**Tracker and corpus statement:** Directive read first and rechecked unchanged (SHA `47459817e66dccf1f3079e6c724c0fd2643e7bc4`). Root proof1.txt recovered complete, 28,714 characters, SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`; root proof2.txt recovered from authentic full Git blob, 1,051,196 characters, SHA `930c5eeddafce656717f28055a7a9a755f44737c` despite empty ordinary-file body. Canonical root main.tex recovered from authentic full blob, 2,502,146 characters at SHA `62c0c400a5eddfbdbdfa06fbabcf7bcee8b753be` despite empty ordinary-file body. AGENTS.md, CODEX.md, research skill, all five newest TMR handoffs, original /008 report/source/raw, TMR-2/009 and TMR-3/008 original reports and issue #3 (1,970 comments) read. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No schedules touched. No P=NP or P!=NP theorem promoted.

END_OF_REPORT::TMR5::TRIPLE_RADIUS_REVIEW007::2026-11-13_1945_PST
