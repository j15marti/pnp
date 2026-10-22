# SHRUNK-QUERY-ENVELOPE67

Timestamp: 2026-10-22 15:48 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

This report isolates the exact exponent and quantifier requirements for the strictly-smaller-query semantic compiler left open by SEMANTIC-PARENT-CALL-CIRCULARITY66. It does not construct that compiler.

## Repairs proposed before source review

1. **Fixed shrinkage:** require every decider query to have length at most \(N^{\beta+o(1)}\) for a fixed \(\beta<1\), rather than \(N^{1-o(1)}\).
2. **Bounded query envelope:** permit \(Q=N^{\alpha+o(1)}\) calls and charge their complete sequential running time.
3. **External finite bootstrapping:** iterate one fixed uniform decider transformer a finite number of times chosen after fixing the assumed polynomial decider, instead of building a fastest-solver selector that discovers its exponent.

The first two give an exact numerical target. The third removes unknown starting exponent \(C\) as an independent existential obstacle, conditional on the missing uniform transformer.

## Sources reviewed after recording the repairs

1. SEMANTIC-PARENT-CALL-CIRCULARITY66: full-parent or \(N^{1-o(1)}\)-scale calls cannot certify a fixed exponent contraction.
2. Corrected SMALL-INTERFACE-EXACT-JOIN64: for its restricted certified class, \(\alpha=0.6\), \(\beta=0.5\), overhead \(\gamma=1.1\), and sequential peak-space floor \(1/2\).
3. The independent 15:14 KST repository review: no load-bearing implication is closed; it independently identifies a strictly-smaller-query semantic quotient as the highest-value open target.

## Lemma 67A — general shrunk-query envelope

Assume a uniform transformer \(\mathcal R\) takes any deterministic SAT decider \(A\) with

\[
T_A(n)=n^{c+o(1)},\qquad S_A(n)=n^{s+o(1)}
\]

and, on an \(N\)-bit input:

- performs \(Q=N^{\alpha+o(1)}\) sequential calls to \(A\);
- every call has ordinary input length at most \(N^{\beta+o(1)}\);
- all construction, source acquisition, validation, virtual access, output and replay together cost \(N^{\gamma+o(1)}\) time;
- non-decider peak space is \(N^{\delta+o(1)}\);
- child calls are sequential, so their workspaces are reused.

Then the certified transformed exponents are

\[
c'\le \max(\gamma,\alpha+\beta c)+o(1),
\qquad
s'\le \max(\delta,\beta s)+o(1).
\]

**Proof.** Each child call costs at most

\[
(N^{\beta+o(1)})^{c+o(1)}=N^{\beta c+o(1)}.
\]

Multiplying by \(N^{\alpha+o(1)}\) calls gives \(N^{\alpha+\beta c+o(1)}\). Add the charged overhead and take the larger exponent. Sequential workspace reuse gives the stated space maximum. \(\square\)

**Status: ESTABLISHED accounting lemma.**

The statement assumes the children are genuine ordinary instances and that the arbitrary decider can access each child with the claimed model costs.

## Corollary 67B — strict improvement frontier

For a starting exponent \(c\), the envelope is strictly below \(c\) exactly when

\[
\gamma<c
\quad\text{and}\quad
\alpha<(1-\beta)c.
\]

Thus fixed exponent improvement requires \(\beta<1\). With \(\beta=1\) and \(\alpha\ge0\), the second inequality is impossible, recovering PARENT-CALL66.

**Status: ESTABLISHED.**

## Lemma 67C — fixed point and iteration

For fixed \(0\le\beta<1\), define

\[
f(c)=\max(\gamma,\alpha+\beta c).
\]

Its least attracting fixed point is

\[
c_*=\max\left(\gamma,\frac{\alpha}{1-\beta}\right).
\]

If \(c_0>c_*\), the iterates \(c_{k+1}=f(c_k)\) decrease to \(c_*\). Above the overhead floor,

\[
c_k-\frac{\alpha}{1-\beta}
=
\beta^k\left(c_0-\frac{\alpha}{1-\beta}\right).
\]

For the SMALL-INTERFACE64 target

\[
(\alpha,\beta,\gamma)=(0.6,0.5,1.1),
\]

the fixed point is

\[
c_*=\max(1.1,0.6/(1-0.5))=1.2=\frac65.
\]

The sequential space recurrence

\[
g(s)=\max(0.5,s/2)
\]

has fixed point \(1/2\).

Therefore a genuine all-input transformer with these fixed parameters would, after finitely many compositions, place SAT in

\[
DTISP\!\left(N^{6/5+\varepsilon},N^{1/2+\varepsilon}\right)
\]

for every fixed \(\varepsilon>0\), subject to the exact endpoint-machine and encoding transfer.

**Status: CONDITIONAL on the missing uniform all-input ARC transformer and matched FLMV model.**

This does not establish the transformer or the contradiction.

## Quantifier lemma — unknown \(C\) need not be discovered

Assume \(P=NP\). Then there exists a particular deterministic SAT machine \(A\) and some finite exponent \(C\). If \(\mathcal R\) is one fixed uniform correctness-preserving transformer whose code and parameters do not depend on \(C\), then for every fixed \(\varepsilon>0\) there exists a finite integer \(k=k(C,\varepsilon)\) such that

\[
\mathcal R^k(A)
\]

has exponents at most \((6/5+\varepsilon,1/2+\varepsilon)\).

The proof may choose \(k\) after existentially fixing \(A\) and \(C\). The machine itself does not need to infer \(C\), race all algorithms, or certify that it is fastest. Each \(k\) is a finite constant in the resulting machine description.

This conclusion fails if:

- \(\mathcal R\)'s correctness or parameters depend on knowing \(C\);
- the number of levels grows with input length;
- a composition hides parent-scale calls, source acquisition or ancestor state;
- the machine/model translation changes between levels.

**Status: ESTABLISHED quantifier fact; application CONDITIONAL on a uniform transformer.**

**RETIRED as a necessary ingredient for this conditional bootstrapping:** a fastest-correct certified universal solver. Such a solver may be useful operationally, but unknown \(C\) is not the load-bearing mathematical gap once a fixed transformer exists.

## What remains constructive

The actual all-input transformer must simultaneously prove:

1. exact SAT and UNSAT joint-label reconstruction;
2. maximum query length \(N^{1/2+o(1)}\), not \(N^{1-o(1)}\);
3. at most \(N^{0.6+o(1)}\) calls;
4. total non-decider overhead \(N^{1.1+o(1)}\);
5. peak non-decider space \(N^{1/2+o(1)}\);
6. source completeness, virtual bit access and bounded adaptive rounds;
7. heredity under every recursively generated child;
8. the same FLMV machine and ordinary encoding at every level.

SMALL-INTERFACE64 supplies these only for a certified restricted class. Equality localization, polynomially many exhaustive restrictions, clause selectors and parent-call semantic collapse have each been retired as universal compilers.

## Circuit-SAT and WRAPPER audit

Changing between Circuit-SAT and faithful Tseitin 3CNF does not alter the exponent envelope. Gate sharing and unique traces affect representation size and source access, which must be included in \(\alpha,\beta,\gamma,\delta\); they do not supply the missing exact transformer.

The audited WRAPPER root remains a finite easy fixture with incomplete boundary summaries. It cannot validate the all-input or hereditary quantifiers.

## MKTP route

The envelope is useful as a hostile accounting template for generators, but it does not produce an ordinary-KT HIGH target. A source-indexable construction with \(N^\beta\)-scale evaluators is generally evidence toward KT-LOW unless a separate counting or diagonal argument establishes HIGH on the required label.

**SAT-to-ordinary-MKTP status: OPEN.**

## RP route

The same arithmetic can charge a proposed hitting-list simulation: list size contributes \(\alpha\), verifier-evaluation length contributes \(\beta\), and construction contributes \(\gamma\). But no universal hitting list or language outside P follows from the envelope.

UNIVERSAL-SHIFT29 remains **ESTABLISHED restricted**. Both \(P=RP\) and \(P\ne RP\) remain **OPEN**.

## Finite audit

The stdlib-only audit checked:

- 988 starting exponents from \(1.3\) through \(100\);
- nine accuracy targets for each starting exponent;
- 1,000 triples \((\alpha,\beta,\gamma)\);
- sequential space convergence;
- 101,000 parent-scale controls with \(\beta=1\).

Result: **121,781 checks, zero failures.**

The audit validates arithmetic only. It supplies no ARC compiler, class inclusion or separation.

## Five-role ledger

| Role | Status | Single next discriminating test |
|---|---|---|
| :00 SAT-to-ordinary-MKTP | **OPEN** | Apply the \((\alpha,\beta,\gamma,\delta)\) ledger to the best SAT-sensitive ordinary-KT target and construct its shortest indexed evaluator. |
| :12 P!=RP | **OPEN** | For one candidate verifier family, publish hitting-list size, original-coin evaluation length, source access and deterministic bypass. |
| :24 ARC/FLMV | Envelope **ESTABLISHED**; transformer **OPEN** | Construct one exact all-input child family meeting \((0.6,0.5,1.1,0.5)\) without parent-scale calls. |
| :36 P=RP | UNIVERSAL-SHIFT29 **ESTABLISHED restricted** | Check whether its parameters remain bounded under verifier replacement and dummy padding. |
| :48 synthesis | Unknown-\(C\) issue **CONDITIONALLY RESOLVED** | Audit uniformity across two explicit transformer compositions, including ancestor state and machine encoding. |

## Conclusion

The numerical and quantifier side of the ARC route is now sharp:

\[
c_*=\max\left(\gamma,\frac{\alpha}{1-\beta}\right).
\]

The target parameters land exactly at \(6/5\) time and \(1/2\) space. Unknown starting exponent \(C\) is not an independent blocker if one fixed all-input transformer exists. The remaining gap is wholly constructive and semantic: build that transformer with exact labels, strict shrinkage, heredity and full same-machine charges.

No root manuscript, automation or role assignment was modified.
