# SELECTOR-ADVERSARY1: explicit row/block falsifiers and correct-path audit

19 November 2026, 12:22 Asia/Seoul. Independent red-team construction. P versus NP remains **OPEN**. External independent mathematical review is pending.

## Target

The input is an authenticated ordinary CNF in the supplied layout

\[
F(z,y)=\bigwedge_{i<B}F_i(z,y_i),\quad
R\le N^{.195+o(1)},\ B\le N^{.65+o(1)},\ |F_i|\le N^{.35+o(1)},
\]

with disjoint private variable sets after fixing \(z\). The selected chain is source -> residual -> bad-block acquisition -> authenticated local NO check -> all-row coverage -> UNSAT output, with SAT output \(z\) plus every private witness. Precommitted falsifiers were: no globally bad block; full shared support in every block; a full-range but compact affine selector; and an arbitrary selector table smaller than square-root workspace.

## Exact selector-realization theorem

**PROVED/EXACT, ordinary CNF, independent review pending.** Let \(f:\{0,1\}^h\to[B]\) be any total function. There are blocks with mutually disjoint private variables such that, for every row \(a\), exactly block \(f(a)\) is UNSAT after \(z=a\).

Define the mismatch clause

\[
g_a(z)=\bigvee_{j:a_j=0}z_j\ \vee\!
\bigvee_{j:a_j=1}\neg z_j.
\]

For every \((i,a)\) with \(f(a)=i\), put into block \(i\), using fresh \(u_{i,a}\),

\[
(g_a\vee u_{i,a})\wedge(g_a\vee\neg u_{i,a}).
\]

At \(z=a\) this is \(u_{i,a}\wedge\neg u_{i,a}\); at every other row \(g_a=1\). Totality of \(f\) gives exactly one failed block per row. The construction has \(2R\) clauses and \(O(Rh)\) literal occurrences. Even the worst block has \(O(Rh)=N^{.195+o(1)}<N^{.35}\) length. Fresh satisfiable private gadgets can pad every block to \(N^{.35+o(1)}\); \(N^{.65+o(1)}\) blocks then give length \(\Theta(N)\) without changing row semantics.

Thus the layout permits every selector function, but this is not hardness. Its full table uses

\[
R\lceil\log_2B\rceil=O(N^{.195}\log N)=o(N^{.5})
\]

bits. Selector materialization alone cannot violate square-root workspace. Acquisition and sound local NO verification are the possible bottlenecks.

## Dense affine falsifier

**PROVED/EXACT.** For even \(h\), let \(f(z)=(J+I)z\) over \(\mathbb F_2\), so \(f(z)_j=\bigoplus_{k\ne j}z_k\). This map is invertible: if \((J+I)x=0\), every coordinate equals total parity \(s\), while even \(h\) gives \(s=hs=0\), hence \(x=0\).

A private Tseitin XOR circuit in block \(t\), followed by the clause \(f(z)\ne t\), makes block \(t\) UNSAT exactly at \(f^{-1}(t)\). Every shared bit is semantically relevant to every block: flipping any bit at its unique bad row changes the image. Yet the selector is evaluated in \(O(h^2)\) bit operations and \(O(h)\) live bits, or faster using total parity. Full support, full range, and maximum row variation coexist with a compact algebraic selector.

The checker constructed every CNF for \(h=2,4\), solved all \(16+256\) residuals independently by DPLL, observed exactly the predicted bad block, and checked 72 support incidences. These runs are **COMPUTATIONAL** evidence for the implementation; the symbolic proof above is the theorem.

## Matched SAT one-hole control

**PROVED/EXACT.** Delete one affine target block \(t^*\). Exactly \(z^*=f^{-1}(t^*)\) now makes every remaining block SAT; each other row retains its unique bad block. The checker verified this for \(h=2,4\).

This unique SAT row is still easy: source headers expose the missing target, affine inversion finds \(z^*\), and private XOR-gate values stream from it. A full assignment can contain \(\Theta(N)\) output bits and costs \(\Theta(N)\) output time, though only a current-block buffer is needed. Candidate acquisition, workspace, and output are separate resources.

## Charged source-aware upper bounds

| Component | Guard-table family | Dense affine family |
|---|---:|---:|
| Parse/authenticate padded source | \(O(N)\) time; streaming state plus current record | same |
| Selector representation | \(R\lceil\log B\rceil=o(N^{.5})\) bits | \(O(h^2)\) circuit bits |
| Evaluate all rows | \(O(R\log B)\) after table build | \(O(Rh^2)\) |
| Local NO check | two guarded clauses, \(O(h)\) | XOR circuit, \(O(h^2)\) |
| Peak writable workspace | \(N^{.35+o(1)}\) | \(N^{.35+o(1)}\) |
| Failed attempts | none; naive core scan is \(N^{.39+o(1)}\), below the paid \(O(N)\) parse | none after affine recognition |

Padding and authentication are paid. These are easy-control upper bounds, not arbitrary-CNF algorithms. Earlier sparse-checkpoint work also shows that a full \(N\)-bit rescan per row is \(N^{1.195+o(1)}<N^{1.33}\); indexing is not the missing theorem.

## Correct paths, polarity, and wrong paths

| Interface | Required output | Wrong-path soundness | Deterministic replay |
|---|---|---|---|
| SAT existential path | \(z\) and private witnesses for every block, or a source program emitting them | reject if any original clause or source binding fails | a universally sound \(k\)-bit verifier of cost \((V,S)\) enumerates in \(O(2^k(V+k))\) time and \(O(S+k+\log V)\) space |
| UNSAT path for fixed \(z\) | block \(i\) plus a declared-system refutation of \(F_i\!\upharpoonright_z\), or a charged exact NO child | reject unverified index, invalid proof, malformed row, or wrong binding | the same enumeration for that row; multiply by \(R\) for every row |
| UNSAT whole strategy | table/circuit \(S(z)\) plus sound local NO evidence for all rows | reject a missing universal row or any failed local proof | enumerating an \(A\)-bit strategy is \(2^A\), not \(2^k\); otherwise charge every universal branch |
| Free polarity routing | correct parent or child polarity | no uniform wrong-path obligation unless imposed separately | answer advice for decision; only output construction and checking remain |

UNSAT has prefix

\[
\forall z\ \exists i\ \forall y_i\ \neg F_i(z,y_i).
\]

One supplied root-to-leaf path proves at most one row. Adaptive existential choices require a whole strategy or fully charged traversal of universal branches. A favorable alternating path is not a decision algorithm.

A read-only random-access certificate is an extra input whose length, addresses, reads, and verification time must be paid. Standard nondeterminism does not allow free two-way access to guessed bits; a rereadable guess must be stored. Deterministic enumeration stores the current \(k\)-bit candidate. One-way streaming is different and valid only when the verifier consumes each bit once.

## Sourced simultaneous RAM exclusions

The following sources use uniform random-access Turing-machine/RAM-style models with read-only input and charged writable tapes, up to stated polylogarithmic simulations. Their \(n\) is encoded input length.

| Polarity/model | Exact sourced statement | Consequence here |
|---|---|---|
| Deterministic SAT decision | Buss--Williams certify \(c=1.34070\) at space exponent \(\epsilon=.5\) in their alternation-trading table. | A full all-CNF \(n^{1.33+o(1)}\)-time, \(n^{.5+o(1)}\)-space deterministic decider is excluded. A promised-layout specialist does not inherit this without a reduction. |
| Nondeterministic SAT | Fortnow excludes simultaneous \(n^{1+o(1)}\) time and \(n^{1-\epsilon}\) space for every fixed \(\epsilon>0\). | Polarity-correct, but it does not exclude \(n^{1.33}\) time and \(n^{.5}\) space. |
| Nondeterministic UNSAT / tautologies | Diehl--van Melkebeek--Williams: if \(c^2d<4\), tautologies cannot have both an \(n^c\)-time nondeterministic algorithm and an \(n^d\)-time, \(n^e\)-space nondeterministic algorithm for some \(e>0\). Setting \(c=d\) gives \(d<\sqrt[3]4=1.587401\ldots\). | At time \(1.33\), the positive space exponent is unspecified, not \(0.5\). No NO-side \((1.33,.5)\) exclusion follows. |
| Explicit coNTISP point | FLMV Corollary 6.5 gives \(d(c)=(1+c)/c^2-c\). At \(c=1.10\), \(d=0.635537\ldots\); it is nonpositive by \(c=1.33\). | Supports a \((1.10,.5)\) NO-side point after reduction slack, not \((1.33,.5)\). |
| Proof-system refutation | Resolution/Frege/etc. lower bounds restrict that certificate system. | No unrestricted runtime lower bound follows without a costed simulation into that system. |

Sources: [Buss--Williams](https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/samCCC-cr.pdf), Theorem 2/table at \(\epsilon=.5\); [Fortnow](https://lance.fortnow.com/papers/files/npvsnl.pdf); [FLMV](https://lance.fortnow.com/papers/files/tst.pdf), machine model and Corollary 6.5; [Diehl--van Melkebeek--Williams](https://research.cs.wisc.edu/techreports/2007/TR1601.pdf), Theorems 1--2 and Section 2.1. The last explicitly denies free two-way access to guessed bits.

## The \(1.33\) proposal and arbitrary CNFs

**FALSIFIED inference.** A generic polynomial SAT seed \(T(m)=m^K\) does not imply the one-step row scanner runs in \(N^{1.33+o(1)}\). The recovered charged recurrence

\[
T(N)\le N^{1.195+o(1)}+N^{.845+o(1)}T(N^{.35+o(1)})
\]

needs \(K\le97/70=1.385714\ldots\). Arbitrary polynomial \(K\) is insufficient. Convergence to exponent \(1.30\) is conditional on a uniform hereditary compiler for every residual; none is known. A known-clock, sound one-sided specialist complete on all inputs of one polarity itself yields a total decider by timeout and verification.

**OPEN extension.** The realization theorem encodes arbitrary selectors but makes local contradictions syntactically easy. It gives no arbitrary-CNF compiler, hard local verifier, or hereditary closure. Conversely, it blocks lower bounds based only on selector entropy, full support, row variation, or table size.

## T5 control

The existing 33-vertex, 44-arc T5 source was rechecked, not rediscovered. All 44 deletion witnesses and five rotations passed 9,680 original-arc tests; each falsified exactly its designated missing arc. This demonstrates cheap verification of a supplied correct path and a fivefold quotient, not uniform acquisition. The affine family gives the analogous Boolean warning: global variation may still have a compact algebraic algorithm.

## Prior work, gates, and status

Fresh project reads covered PATH3 recovery, WRAPPER_INDEX_REPLAY1, ROW_BLOCK_SPECIALIST72_STATUS, the compact selector-tree generator, and the SAT-only selector firewall in j15marti/pnp. The new result is not another selector-tree size count: it realizes every selector as an ordinary supplied-layout CNF and proves the full table fits below square-root workspace. No local checkout existed, so preflight and LaTeX compilation were not run. No TMR identity was supplied for this assignment, so no peer-owned living manuscript was changed; this is an additive red-team report.

| Gate | Status | Reason |
|---|---|---|
| DISJ sanity | PASS | no rank/entropy-to-hardness inference; all adversaries have cheap algorithms |
| Relativization | PASS for construction; OPEN for a separation bridge | no P-vs-NP conclusion |
| Simultaneous DTISP | PASS for displayed upper bounds and cited model-specific exclusions | same execution supplies time and peak space |
| Configuration counting | PASS | used only as an upper-bound consistency check |
| Algebrization/Natural Proofs | NOT APPLICABLE | no unrestricted circuit lower bound |

**PROVED/EXACT:** arbitrary selector realization; affine full-support selector; \(o(N^{.5})\) selector table; affine one-hole SAT control; correct-path quantifier separation and enumeration upper bound.

**COMPUTATIONAL:** 272 affine residual checks, 72 support checks, an eight-row arbitrary permutation, five scaling points, and 9,680 T5 arc checks.

**CONDITIONAL:** any lower-bound transfer requires the same uniform model, encoding, promise-removing reduction, and exponent slack.

**FALSIFIED/RETIRED:** fixed bad block; universally small support; selector range/entropy implies hardness; selector table exceeds square-root space; one favorable UNSAT path is a whole strategy; generic polynomial seed implies \(1.33\).

**OPEN:** arbitrary-CNF hereditary layout compiler; uniformly sound local NO acquisition in target resources; sourced NO-side \((1.33,.5)\) exclusion; source-aware full SAT witness costs; external peer audit; P versus NP.

## Evidence and next blocker

- adversarial_selector_audit.py, SHA-256 638572a1d5952c60c10ecf62685285a78e5cdb32073737d3872bc89101c6346a.
- adversarial_selector_audit_results.json, SHA-256 7953de4e7f1c4467e787153dbcdba9eb0994166dd5d556969d271a172a66a011.
- T5 source SHA-256 0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac.

**Next blocker:** characterize a nontrivial local-residual class with source-authenticated, uniformly sound NO-certificate acquisition for every row and closure under the claimed child recursion. Selector combinatorics alone cannot supply it.
