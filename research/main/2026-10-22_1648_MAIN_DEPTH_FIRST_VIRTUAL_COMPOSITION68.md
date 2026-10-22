# DEPTH-FIRST-VIRTUAL-COMPOSITION68

Timestamp: 2026-10-22 16:48 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

This report tests whether the fixed number of iterations justified by SHRUNK-QUERY-ENVELOPE67 can be implemented without accumulating hidden parent bodies, sibling descriptors, replay scans or polynomial virtual-access overhead.

## Repairs proposed before source review

1. **Depth-first descriptor stack:** generate and process one child at a time, retaining only one descriptor and iterator for each ancestor.
2. **Recursive virtual-bit evaluator:** answer a leaf input-bit request by composing the level-local evaluators back to the original source.
3. **Level-local source memoization:** retain a source index for each ancestor to avoid rescanning it for every descendant read.

The first two yield an exact fixed-depth composition theorem under explicit locality hypotheses. The third is unnecessary when every level already supplies polylogarithmic random access; if it stores a polynomial parent index at every level, it must be charged and can violate the space target.

## Sources reviewed after recording the repairs

1. SHRUNK-QUERY-ENVELOPE67: the one-step exponent map is \(f(c)=\max(\gamma,\alpha+\beta c)\), with target fixed point \(6/5\).
2. VIRTUAL-CHILD-COMPOSITION61: one short descriptor and a polylogarithmic local evaluator can simulate every adaptive child-input read without materializing the child.
3. ROUND-ADAPTIVE-BATCHING60: sequential keyed acquisition remains within the target only when the exposure rounds, generator state and source scans are fully charged.

The independent 16:14 KST repository review confirms that the all-input hereditary transformer remains OPEN and that the arithmetic results do not close a load-bearing implication.

## Model — composable one-level transformer

Let \(\mathcal R\) be a fixed decider transformer. On a source of ordinary encoded length \(n\), it:

- generates at most \(n^{\alpha+o(1)}\) child descriptors sequentially;
- each child has ordinary virtual length at most \(n^{\beta+o(1)}\);
- spends \(n^{\gamma+o(1)}\) total non-decider time;
- uses \(n^{\delta+o(1)}\) peak non-decider space;
- provides a bit evaluator \(g(x,d,i)\) using \(\log^{O(1)}n\) time and space and only \(\log^{O(1)}n\) local accesses to \(x\);
- combines all child labels exactly into the source label;
- emits each descriptor before processing the next child, so sibling bodies and sibling descriptor lists are not retained.

All correctness and source-completeness conditions must hold on every ordinary SAT input and every recursively generated child.

## Lemma 68A — recursive virtual access

For every fixed depth \(k\), a bit of a depth-\(k\) virtual child can be evaluated from the original source and the \(k\) ancestor descriptors in

\[
\log^{O(k)}N=N^{o(1)}
\]

time and

\[
k\log^{O(1)}N=N^{o(1)}
\]

scratch space.

**Proof.** Apply the level-\(k\) evaluator to translate the requested leaf position into polylogarithmically many requests to its parent, then recursively answer those requests. With \(k\) fixed independently of \(N\), composing \(k\) polylogarithmic evaluators remains subpolynomial. The descriptor stack has fixed depth. \(\square\)

**Status: ESTABLISHED under the stated local-access model.**

The lemma fails if a nominal bit evaluator scans an entire ancestor or requires a polynomial-size index not included in the space ledger.

## Lemma 68B — explicit time composition

At depth \(i\), the number of active nodes in the complete recursion tree is at most

\[
N^{\alpha(1+\beta+\cdots+\beta^{i-1})+o(1)}.
\]

Each such node has size \(N^{\beta^i+o(1)}\). Therefore the total level-\(i\) construction exponent is

\[
H_i=
\alpha\frac{1-\beta^i}{1-\beta}
+\gamma\beta^i.
\]

At depth \(k\), the leaf-decider exponent is

\[
L_k=
\alpha\frac{1-\beta^k}{1-\beta}
+c_0\beta^k.
\]

Consequently,

\[
T_k=
\max\left(
L_k,\,
H_0,\ldots,H_{k-1}
\right)+o(1).
\]

This is exactly

\[
T_k=f^k(c_0)+o(1),
\qquad
f(c)=\max(\gamma,\alpha+\beta c).
\]

**Proof.** Count nodes at each level, multiply by the per-node construction or leaf-decision cost, and take the largest exponent because \(k\) is fixed. Expanding the recurrence produces the same leaf term and internal-level terms. \(\square\)

**Status: ESTABLISHED accounting identity.**

Thus the one-step envelope remains valid under fixed-depth composition; no extra polynomial exponent arises from the recursion tree beyond the recurrence already counted.

## Lemma 68C — depth-first peak space

Assume each level produces descriptors sequentially and reuses child workspaces. At recursion depth \(k\), retain:

- one descriptor and sibling iterator for each ancestor;
- one active construction workspace;
- one active descendant-decider workspace;
- the recursive virtual-access stack.

The descriptor sizes form a geometric hierarchy

\[
N^{\delta+o(1)},\,
N^{\beta\delta+o(1)},\,
\ldots,\,
N^{\beta^{k-1}\delta+o(1)}.
\]

For fixed \(k\), the first term dominates. If the starting decider uses exponent \(s_0\), then

\[
S_k=
\max(\delta,\beta^k s_0)+o(1),
\]

which equals \(g^k(s_0)\) for \(g(s)=\max(\delta,\beta s)\).

**Status: ESTABLISHED under sequential generation and workspace reuse.**

**RETIRED:** breadth-first retention of all \(N^\alpha\) sibling descriptors or all child bodies at multiple levels. That storage is not covered by this lemma.

## Corollary 68D — target fixed-depth implementation

With

\[
(\alpha,\beta,\gamma,\delta)=(0.6,0.5,1.1,0.5),
\]

any fixed composition depth \(k\) preserves the SHRUNK-QUERY67 recurrence exactly, up to \(N^{o(1)}\) virtual-access overhead. Combining this with the quantifier lemma from SHRUNK-QUERY67:

- after fixing an assumed polynomial SAT decider of exponent \(C\);
- and fixing \(\varepsilon>0\);
- a finite constant \(k(C,\varepsilon)\) suffices arithmetically;
- recursive virtual access remains subpolynomial because that \(k\) is independent of input length.

**Status: CONDITIONAL on the missing exact all-input one-level transformer and matched FLMV machine simulation.**

This resolves an implementation concern, not the semantic construction.

## Hostile controls

The composition theorem does not apply when:

1. a child descriptor is generated only after deciding its full parent;
2. a child bit requires rescanning a parent of length \(n\);
3. all sibling descriptors are retained simultaneously;
4. source, timer, solver, trace or history influences are omitted;
5. the transformation is exact only on SAT inputs or only on selected descendants;
6. the representation changes without charging conversion and random-access simulation;
7. the depth grows with \(N\).

DIGEST-LUMP19, CLAUSE-COHERENCE20, SOURCE-CHANNEL21, PARENT-CALL66 and the wall-minor barrier remain active controls.

## Circuit-SAT and WRAPPER integration

Faithful Circuit-SAT/Tseitin conversion can be composed only if each level preserves the complete primary-source map and exposes shared predecessor gates. Unique gate traces do not make a hidden source local.

The finite WRAPPER root can test evaluator composition, but its favorable cutset and frontier values do not establish the all-input or hereditary hypotheses. Its wrapper boundary two remains distinct from source-frontier width.

## MKTP route

Recursive polylogarithmic virtual access usually strengthens an ordinary-KT upper bound. It does not establish the missing HIGH target. Any MKTP use must charge:

- all \(k\) descriptors;
- recursive bit-evaluation time;
- original-source access;
- the program that generates descriptors;
- full target output length.

**SAT-to-ordinary-MKTP status: OPEN.**

## RP route

Fixed-depth virtual composition can evaluate a previously constructed hitting list without materializing every derived verifier. It supplies neither a universal hitting set nor a language outside P. A valid RP simulation must still use original random-tape coordinates and preserve one-sided soundness.

UNIVERSAL-SHIFT29 remains **ESTABLISHED restricted**. Both \(P=RP\) and \(P\ne RP\) remain **OPEN**.

## Finite audit

The stdlib-only audit performed:

- 2,000 virtual-composition instances;
- 11,360 final-child source-bit reads;
- 20,440 recursive index translations;
- exhaustive equality with materialized children through depth five;
- 29,670 time-recurrence versus explicit-level identities;
- 29,880 depth-first space identities;
- fixed-depth polylogarithmic overhead checks.

Result: **93,810 checks, zero failures.**

The audit validates implementation and arithmetic only. It does not construct a semantic ARC transformer or prove a class result.

## Five-role ledger

| Role | Status | Single next discriminating test |
|---|---|---|
| :00 SAT-to-ordinary-MKTP | **OPEN** | Compute ordinary-KT of a twice-composed virtual target, including both descriptors and recursive source reads. |
| :12 P!=RP | **OPEN** | Test one twice-composed verifier against an easy direct language decider and SAT-NO control. |
| :24 ARC/FLMV | Composition **ESTABLISHED conditional interface**; transformer **OPEN** | Build one genuine one-level exact descriptor/evaluator pair and compose it twice on SAT and UNSAT parents. |
| :36 P=RP | UNIVERSAL-SHIFT29 **ESTABLISHED restricted** | Trace original coin coordinates through two virtual verifier levels; reject derived-coin substitutions. |
| :48 synthesis | Fixed-depth implementation concern **RESOLVED conditionally** | Require a two-level audit with source reads, sibling retention, replay and machine conversion before any promotion. |

## Conclusion

Fixed-depth iteration itself does not add a hidden polynomial exponent when child generation is sequential, descriptors are stacked depth-first, and virtual bit evaluation is genuinely local. The numerical recurrence from SHRUNK-QUERY67 is compositionally sound under these hypotheses.

The remaining load-bearing gap is unchanged and now isolated more sharply: construct one exact all-input hereditary one-level transformer meeting the target envelope. No root manuscript, automation or role assignment was modified.
