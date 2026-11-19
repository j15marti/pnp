# TMR-5/060: a linear-size, log-depth universal ceiling for exponential padding

**November 15, 2026, 22:55 PST.** Role: TMR-5 / PNP Machine Bottleneck Redteam. Named dependency: **C1g-EXP-PADDING-NP-GATE**, the nonuniform-circuit end of TMR-1's actual encoded-input-to-counting-to-hierarchy chain. **PROVED/EXACT, restricted to the specified exponential-padding operation; external mathematics peer review OPEN.** Finite implementation evidence is **COMPUTATIONAL**. **P versus NP OPEN**.

## Candidate, quantifiers, model, falsifiers

For every language \(W\subseteq\{0,1\}^*\), including an undecidable language, every fixed integer \(c\ge1\), and every input length \(M\), define the *entire* padded language
\[
P_c(W)=\{x\,1\,0^{\,2^{c|x|}-|x|-1}:x\in W,\ |x|\ge1\}.
\]
Circuit inputs are the actual \(M\) source bits, not a preauthenticated promise. Fan-in-two gates are AND, OR and NOT with hardwired Boolean constants; nonuniform source truth-table bits may appear only as circuit constants/advice. The candidate is a correct all-input source-to-output family with at most \(4M\) noninput gates and \(O(\log M)\) depth, even when the unpadded \(W\) is incomputable. Also seek a linear-node OBDD and a logspace *advice* evaluator. No uniform circuit constructor for arbitrary \(W\) is asserted.

Falsifiers assessed before construction: (F1) a malformed delimiter/suffix or a non-power padded length accepted; (F2) an arbitrary prefix \(x\) output assigned incorrectly; (F3) a hidden factor \(n\) in the gate *count* from DNF-like truth-table expansion; (F4) smuggling uniformity, NP membership or ordinary uniform small-space access into a nonuniform truth-table construction.

## End-to-end theorem and full proof

**Theorem (C1g-LINEAR-PADDING-CEILING).** For every \(W,c,M\) above, the characteristic function of \(P_c(W)\) at length \(M\) has a nonuniform shared fan-in-two Boolean circuit of at most \(4M\) noninput AND/OR/NOT gates and depth \(O(\log(M+2))\). It also has an OBDD in the natural input order with at most \(2M\) internal nodes and is in nonuniform \(\mathrm{AC}^0\) with \(O(M)\) unbounded-fan-in gates and \(O(M\log(M+2))\) literal wires. Under conventional read-only polynomial advice, \(P_c(W)\in\mathrm{L/poly}\). None of these claims implies a uniform polynomial-time decision algorithm for \(W\), or that \(P_c(W)\in\mathrm{NP}\).

*Proof, authentic length handling.* If no integer \(n\ge1\) satisfies \(M=2^{cn}\), the length-\(M\) function is identically zero, computed by one hardwired zero output. Otherwise \(n=\log_2(M)/c\) and \(2^n\le M\). For arbitrary \(M\)-bit input \(z\), legality means precisely: \(z_n=1\), every bit \(z_{n+1},\ldots,z_{M-1}\) is zero, and the first \(n\) bits belong to \(W_n\). Every other input must be rejected; this is not a promise shortcut.

*Proof, fixed-prefix function.* Fix the \(2^n\)-bit truth table \(b_a=[a\in W_n]\) as **nonuniform constants**. Construct a complete binary Shannon/multiplexer tree on \(z_0,\ldots,z_{n-1}\). The leaf corresponding to prefix \(a\) is the hardwired constant \(b_a\); each internal node is
\[
\operatorname{MUX}(z_j,L,R)=(\neg z_j\land L)\lor(z_j\land R).
\]
Compute each \(\neg z_j\) only once, using \(n\) NOT gates; each of the \(2^n-1\) internal nodes takes exactly three fan-in-two gates (two AND, one OR). By induction on tree height, the root equals \([z_{<n}\in W_n]\). This is an actual generated shared gate DAG, never a DNF with \(n\) new gates per truth-table row. Its depth is at most \(2n+O(1)\).

*Proof, suffix authentication and exact gate budget.* Let \(r=M-n-1\), necessarily nonnegative. If \(r\ge1\), compute OR of the \(r\) tail bits by a **balanced** binary OR tree using \(r-1\) gates, negate it, AND with the delimiter bit, then AND with the prefix root. Thus the entire count is
\[
g=n+3(2^n-1)+(r-1)+1+1+1
 = 3\cdot2^n+M-2\le4M-2.
\]
If \(r=0\), this can occur only for \(c=n=1,M=2\); the count is \(1+3(2^1-1)+1=5\le 4M\). The longest suffix OR path is \(O(\log(r+1))\); the overall circuit depth is \(O(n+\log M)=O(\log M)\). Wires are at most twice the gate count plus input/output references. The correct output follows from the two predicates' conjunction, including rejection of malformed strings. The same DAG explicitly costs \(O(M)\) stored nodes and \(O(M)\) edge records; unlike a count oracle, no free intermediate object exists.

*Proof, actual OBDD and advice.* A complete prefix decision tree has \(2^n-1\) internal query nodes and truth-table-labelled leaves. Every rejecting leaf points to terminal zero; every accepting leaf shares one node querying the required delimiter, followed by a single shared chain checking all \(r\) tail bits against zero. This is a read-once ordered branching program with \(2^n+r\le2M\) internal nodes, and is correct on every \(M\)-bit input. Separately, for each valid length \(M\) place the \(2^n\)-bit table \(b\) on a read-only advice tape, and otherwise use empty advice. One fixed deterministic algorithm with the integer constant \(c\) built into control uses a binary counter to authenticate length \(M=2^{cn}\), scans the input for delimiter/suffix correctness while retaining the first \(n\) bits as a table index, scans the locally moving read-only advice head to that index, outputs its bit, then halts. On one matched execution its total sequential time is conservatively \(O(M^3)\) and writable workspace \(O(\log(M+2))\), with the input and advice heads/counters actually charged. The **read-only advice contains up to \(M\) bits**; if physical stored advice is counted as aggregate memory rather than the conventional L/poly workspace convention, total storage is \(O(M)\). This is nonuniform L/poly, not uniform L. For unbounded-fan-in circuits, the \(W_n\) truth-table DNF uses at most \(2^n\) AND gates, one OR, shared \(n\) input inversions and one full suffix AND, giving nonuniform AC0 gate count \(O(M)\) but up to \(O(M\log M)\) wires; it is not a fan-in-two *DNF* size claim.

**Consequence.** The earlier correct TMR-1/059v2 argument bounded \(P_c(W)\) by \(O(M\log M)\) using a DNF for the unpadded \(n\)-input function. The complete source-to-output multiplexer construction improves this to **\(O(M)\)** for every \(W\) and every length \(M\). Thus this particular exponential padding operation cannot support even an eventual **superlinear** unrestricted-circuit lower bound, much less a superpolynomial one. The actual TMR-1 C1f conditional \(E^{NP}\) lower bound remains a different, unpadded and unrefuted statement. This is a stronger **scope-preserving ceiling** for the named C1g attempted NP transfer, not a claim about all padding reductions or all nonuniform NP languages. The identity is a standard Boolean/Shannon expansion; project-specific novelty is only its exact integration with the authentic C1g padding interface and gate/space audit.

## Executed independent evidence

Actual CPython local executable: \`experiments/tmr/tmr5_linear_padding060.py\` (revision \`TMR5_PAD_LINEAR060_PY_v1\`, Git blob \`2d67d48e3745b7a0fceb4bea3f35659e7bb90027\`, seed 20261116). It constructs a real fan-in-two gate list, evaluates each gate on each tested **complete** input word, compares with an independently written string/authentication predicate, checks the \(4M\) budget and balanced depth. Eight parameter settings \((n,c)=(1,1),(1,2),(1,3),(1,4),(2,1),(2,2),(3,1),(4,1)\), with \(M\le16\); exhaustive truth tables for \(n\le3\); eight structured/seeded tables for \(n=4\); all \(2^M\) input words for each selected table. **312 truth tables, 1,901,904 full circuit/output comparisons, zero failures**. Largest case \(M=16,n=4,c=1\) has 62 gates against 64 allowed. Immutable raw: \`results/raw/tmr/2026-11-15_2255_TMR5_PAD_LINEAR060_PY_RAW.json\`, Git blob \`d980fc7949604e61010d775df0c88a13abcea1e7\`. This is finite COMPUTATIONAL evidence; the all-\(M\) proof is the symbolic argument above. Native Turing-machine microcode, Lean/nanoda, repo-wide preflight and LaTeX were **not executed**.

## Same-realization resource ledger and exact controls

The nonuniform construction stages are table hardwiring (advice length \(2^n\le M\)), source-bit prefix selection (exact \(3(2^n-1)+n\) gates), full suffix authentication (at most \(M-n+1\) gates), one output conjunction, and emitted output bit. These gate sets are disjoint, shared NOT gates and prefix nodes counted once. The OBDD separately has a complete prefix tree plus a single shared suffix checker. The advice-TM is a **different declared nonuniform computational realization**, not conflated with the circuit gate count; its same-run time \(O(M^3)\), writable peak \(O(\log M)\), and physically stored read-only advice \(O(M)\) are separately identified. No SAT oracle, query access to an unknown W, polynomial-time uniform circuit discovery, caching for free, or counting of parallel span as work is used. The algorithm to generate the *circuit from an arbitrary W* is not necessarily computable; that is exactly why the theorem is nonuniform.

## Four mandatory gates

| Gate | Verdict and reason |
|---|---|
| DISJ sanity | **PASS.** Applies equally to W equal to a DISJ characteristic language; it gives a cheap *padded* representation, never a hard DISJ or original SAT circuit lower bound. Existing linear DISJ circuits remain legal. |
| Relativization | **PASS for the nonuniform upper and scope barrier.** It works for every W, including oracle-dependent W; a relativizing P-versus-NP separation is not attempted. Nonrelativizing, algebrization and Natural Proofs obligations for a distinct NP-hardness route remain OPEN. |
| Simultaneous DTISP | **PASS only for the explicit read-only-advice TM's upper ledger; NOT APPLICABLE to a forbidden-uniform-DTISP inference.** Its T and peak writable S are from one advice-bearing realization. Unrestricted uniform transfer remains OPEN. |
| Deterministic configuration counting | **PASS as upper-bound sanity** for the deterministic total advice-TM: with advice length \(A\le M\) and \(s=O(\log M)\) work, configurations are \(2^{O(s+\log(M+A))}\), consistent with polynomial halting time. It gives no work lower bound or randomized/quantum claim. |

Controls: arbitrary W includes Horn, 2-SAT, affine/Gaussian, bounded-treewidth, equality, autarky, products and uncomputable truth tables. Renaming, unique assignments, field/basis choices, selector/projection, padding, auxiliaries, sharing, caching, alternate compact circuits and count-normalization remain legal; no tensor rank or SAT assignment/source confusion is used. /341 remains FAIL for full UNSAT authority, /386 RESTRICTED.

## Ranked dependency table and one next target

| Rank | Pipeline | Current status |
|---|---|---|
| 1 | TMR-1 source/solver/FinTM2/hierarchy | C1g exponential-padding to NP-style circuit lower bound now **FALSIFIED even for superlinear target**, via universal \(O(M)\) nonuniform circuit. C1f unpadded conditional \(E^{NP}\) bound still separate; fresh pinned Lean 4.33.1 and nanoda rebuild, and model/hierarchy semantic transfer OPEN. |
| 2 | TMR-2 authenticated dynamic counting | Two-stage bilinear span and TMR-5/059 raw-input extension remain PROVED/RESTRICTED; arbitrary mixed nonlinear input and any necessary-work lower bound OPEN. |
| 3 | TMR-3 checkpoint provider/evaluator | Existing authentic source services and Williams graph enumeration scoped; generic adaptive paid provider plus genuinely improved evaluator OPEN. |
| 4 | TMR-4 cost-sound compiler | In-tree shared-core/liveness OBDD construction PASS restricted; general reconvergent-core interface and converse necessity OPEN. |

**ONE next highest-value target:** independently rebuild the unchanged pinned Anthropic \`MainResults.mainTheorem\` with actual Lean 4.33.1, transitive \`#print axioms\`, Comparator and nanoda kernel logs on a functioning Linux executor, then separately verify the physical FinTM2-to-\(E^{NP}\) transfer. Previous GitHub action attempts failed *before steps*, not as a mathematical proof rejection. No agents or schedules changed.

## Primary sources and evidence

1. TMR-1 original C1g/059v2 report, \`research/agents/tmr-1/2026-11-15_2012_TMR1_UNIVERSAL_PADDED_PPOLY059_V2.md\`, and owned \`main1_PNP_MACHINE_MODEL_LEAD.tex\` on draft PR #197. The earlier \(O(M\log M)\) claim remains correct but nonoptimal.
2. The elementary Boole/Shannon expansion \(f=(\neg x\land f_{x=0})\lor(x\land f_{x=1})\), given and proved by direct truth-table cases above, does not assume the modern SAT source theorem.
3. Anthropic pinned \`eth/MainResults.lean\` and \`eth/Solution.lean\`, commit \`16a5ce41304fcdaea4e0be7c132e1c361dc26da5\`, for the **different conditional** counting chain; this mathematical upper bound requires neither source theorem nor kernel acceptance.
