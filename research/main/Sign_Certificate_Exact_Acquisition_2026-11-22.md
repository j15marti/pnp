# Exact shortest-obstruction acquisition with arbitrary sound computation

**Date:** 2026-11-22 (America/Los_Angeles). **Named target:** SIGN-CERTIFICATE-EXACT1. **Status:** PROVED/EXACT, within the deterministic, independently addressable signed-literal bit-input contract; finite audit performed; unrestricted P versus NP OPEN.

## Result

For ordinary Boolean CNF with an explicit *independent sign bit for each literal occurrence*, with the source clause-variable incidence template and any supplied partial assignment held fixed, the minimum number of input sign-bit observations sufficient to certify an UNSAT answer is exactly the total number of signed occurrences in a smallest-weight UNSAT subset of the original clauses. In particular, for strict 3-CNF with three distinct variables per source row,

\[
\boxed{C^-_{\mathrm{sign}}(F,\rho)=3\,\mu(F,\rho)},
\qquad
\mu(F,\rho)=\min\{|K|:K\subseteq F,\ K|_\rho\text{ is UNSAT}\}.
\tag{1}
\]

This lower-bounds **actual distinct bit observations** on the single execution of *every fixed correct deterministic solver*, including solvers that use any sound combination of clauses, arithmetic, shared preprocessing, memoization, proof discovery, or an unanticipated polynomial-time shortcut. It does not prescribe a proof system or an assignment-enumeration routine. It says nothing about additional inference cost after the observations. The bound is at most the number of sign bits in the source, hence is at most linear in complete encoded input length.

The result is a precise answer to one notion of *minimum distinguishable information* in the optimized variable-erasure study. It is not a general time lower bound beyond source acquisition, a property of strict symmetric T5 (whose clauses contain no sign bits), or an unrestricted P versus NP separation.

## 1. Exact model and quantifiers

An instance has an ordered clause-variable incidence template \(\tau=(V,C_1,\ldots,C_m)\), with each row listing \(w_j\) distinct names. An independent sign bit accompanies every literal occurrence. Holding \(\tau\) fixed, every assignment \(z\in\{0,1\}^{L}\), \(L=\sum_j w_j\), is a valid CNF source \(F_z\). A partial assignment \(\rho:V\rightharpoonup\{0,1\}\) is fixed as additional input. An algorithm may examine the full encoded source including headers, row identifiers, all signed literals, and pins, and it may use arbitrary deterministic computation. Only observations of sign bits are counted by this source-information theorem. All other work is separately charged to an implementation.

The solver is **correct for every signed assignment \(z'\)** of this fixed incidence template, for both SAT and UNSAT labels, with the same \(\rho\). In particular, no all-UNSAT promise, exact-(2,2) occurrence balance, or unique-reference-violation promise is given to the solver. If additional syntax restrictions exclude sign flips, the theorem cannot be transferred without new legal alternatives.

For an UNSAT source, a negative sign-bit certificate is a set \(Q\) of sign positions with their observed values such that every valid source agreeing on those positions is UNSAT under \(\rho\). Write \(\mathrm{full}(Q)\) for source rows *all* of whose sign positions lie in \(Q\). Let \(K(Q)\) be the conjunction of those original fully specified rows.

## 2. Exact certificate equivalence

**Theorem 1.** For every fixed \(\tau,\rho\), UNSAT sign setting \(z\), and sign-position set \(Q\),

\[
\boxed{Q\text{ certifies UNSAT}\iff K(Q)|_\rho\text{ is UNSAT}.}
\tag{2}
\]

**Proof (sufficiency).** If the fully specified clauses alone are inconsistent with the pins, no changes to the other clauses can produce a model.

**Proof (necessity).** Assume the fully specified clauses admit a completion \(a\) of \(\rho\). For each other source clause \(C_j\), at least one literal occurrence has an *unqueried* sign bit. Set that bit so its literal is true under \(a\). Leave all queried sign bits unchanged and choose all other unqueried sign bits arbitrarily. Each not-fully-specified clause is now true under \(a\), and each fully specified clause was true already. Thus the resulting valid signed CNF has a model, agrees with every observation in \(Q\), and refutes the claim that \(Q\) certifies UNSAT. No two clauses share a sign bit, so these choices never conflict. QED.

**Corollary 1 (weighted and strict width).** Every certificate contains every sign position of an UNSAT source subset, and every such subset provides a certificate. Therefore

\[
C^-_{\mathrm{sign}}(F,\rho)
=\min_{K\subseteq F:\ K|_\rho\mathrm{\ UNSAT}}\ \sum_{j\in K}w_j.
\tag{3}
\]

For width exactly three, this is precisely (1). Partial evidence acquired across many source clauses **cannot** replace a full inconsistent subset under this independently free-sign input contract. This is an input-indistinguishability result, not a limitation of logical inference.

**Corollary 2 (every fixed solver, same run).** Fix any deterministic solver \(A\) correct on all legal inputs. On one UNSAT input, let \(Q_A\) be the *distinct sign-bit addresses actually accessed* during its entire run, including preprocessing. Any other source agreeing on those addresses induces exactly the same run and output. Therefore \(Q_A\) must certify UNSAT, and

\[
\boxed{|Q_A(F,\rho)|\ge3\mu(F,\rho).}
\tag{4}
\]

Repeated reads, cached or copied values, cross-clause sharing, and alternative inference all remain legal; they cannot erase a necessary first observation, but an observation is not charged twice merely because its information is used several times. If a primitive input read obtains up to \(b\) sign bits, at least \(\lceil3\mu/b\rceil\) such operations are required. The \(3\mu\) bound is measured in distinct acquired bits, and conversion into machine steps must preserve the machine's read capacity.

## 3. Shared-obstruction recursion without branch-work addition

For a released Boolean variable \(x\), let \(\mathcal M_0,\mathcal M_1\) be the families of all inclusion-minimal original-row UNSAT subsets in the two value slices \(\rho\cup\{x=0\}\) and \(\rho\cup\{x=1\}\). The preceding shared-obstruction result gives

\[
\mathcal M_{\rho}=\operatorname{Min}_{\subseteq}
\{K_0\cup K_1:K_i\in\mathcal M_i\}.
\tag{5}
\]

Consequently the source-sign certificate bound is

\[
\boxed{C^-_{\mathrm{sign}}(F,\rho)
=3\min_{K_0\in\mathcal M_0,K_1\in\mathcal M_1}|K_0\cup K_1|.}
\tag{6}
\]

Shared source rows count once. Crucially, an optimal union can use a non-minimum-size core from an individual slice if doing so improves overlap. Equations (5)-(6) are semantic identities and an observation minimum, **not** instructions for the machine to visit both branches or materialize either slice.

## 4. Full-resource ledger

Write \(T_A\) for charged bit-machine transitions, \(s_t\) for live auxiliary bits including addresses and retained caches, \(S_A=\max_t s_t\), and

\[
CM_{\mathrm{aux}}=\sum_{t=0}^{T_A}\max\{1,s_t\}.
\]

If each primitive read delivers at most one independent sign bit and other transitions are charged, then on the *same execution*

\[
\boxed{T_A\ge3\mu,\qquad CM_{\mathrm{aux}}\ge3\mu.}
\tag{7}
\]

For a convention physically retaining all \(N\) input bits throughout, \(CM_{\mathrm{phys}}\ge N(T_A+1)\ge3N\mu\). This physical CM bound includes input residence and must not be substituted into small-initial-auxiliary-state exclusions. These inequalities are source-access bounds, not independent additive computation obligations. They do **not** prove \(T\ge3\mu+\mathrm{proof\ length}\), a growing space lower bound, or a superpolynomial lower bound. Since \(3\mu\le3m\le O(N)\), every possible such sign-only certificate demand has a linear ceiling in the complete input length.

After the last needed observation, no additional local inference can be declared compulsory merely from (1). A solver may have completed sufficient joint computation during its paid observations. A large number of possible residual cases or alternative cores therefore does not automatically yield an additional cost.

## 5. Optimized release profile: 15 variables, 20 clauses

Use the prior guarded compiler \(F(H)\):

\[
\begin{aligned}
G_1&=(p\vee x\vee a),&G_2&=(p\vee x\vee\neg a),\\
G_3&=(p\vee\neg x\vee b),&G_4&=(p\vee\neg x\vee\neg b),
\end{aligned}
\]

and replace each \(C=(\ell_1\vee\ell_2\vee\ell_3)\in H\) by

\[
(\neg p\vee\ell_1\vee s_C)\wedge(\neg s_C\vee\ell_2\vee\ell_3).
\]

The four guards force \(p=1\), and \(F(H)\) is SAT iff \(H\) is SAT. For UNSAT \(H\), \(\mu(F(H))=4+2\mu(H)\). The all-zero reference violates one guard. Erase \(a\), then all other variables except \(p,x\), then \(x\), then \(p\). Each level is a separate fresh input.

For \(H\) the complete eight-clause cube over three variables, \(n_F=15,m_F=20\). The exact source minimum-core and *necessary sign-observation* profiles are:

| Unknown variables | Minimum original-row core \(\mu\) | Necessary distinct sign-bit observations \(3\mu\) |
|---:|---:|---:|
| 0 | 1 | 3 |
| 1 through 13 | 2 | 6 |
| 14 | 4 | 12 |
| 15 | 20 | 60 |

The finite audit verifies not just minimum cores but the **pointwise sign sensitivity** of these specific input strings: precisely 3, 6, 6, 6, 12, 60 sensitive sign positions at tested levels 0,1,6,13,14,15. For the remaining first 13 levels the two pinned opposite-unit guards prove the same symbolic six-bit profile. The full 20-row formula is minimally UNSAT and therefore every one of its 60 literal signs is individually critical to the SAT label. The core size is not a runtime formula: all pre-final levels have a cheap fixed four-guard refutation and a correct recognizer with a general fallback, whereas the last level preserves an arbitrary 3-SAT decision.

## 6. Strong controls: sensitivity can vanish while the certificate stays large

Repeat each of the two contradictory guard rows twice, at pins \(p=x=0\):

\[
(a)\land(a)\land(\neg a)\land(\neg a).
\]

Every *individual* sign flip leaves another opposite pair, so **no literal-sign bit is individually sensitive**. Nevertheless the smallest UNSAT source subset uses two rows, so every correct solver must read at least six distinct sign bits by Theorem 1. The exhaustive twelve-bit audit finds a minimum negative certificate size of six and 225 certificate sets; every one of the 4,096 observation subsets was tested with a constructive SAT alternative where applicable. This proves that individual-bit sensitivity alone is too weak. One must retain all alternative obstructions and their shared evidence.

## 7. A growing, completely sign-sensitive family that is easy to refute

For \(k\ge2\), consider the low-width implication chain

\[
(x_1)\land \bigwedge_{i=1}^{k-1}(\neg x_i\vee x_{i+1})\land(\neg x_k).
\tag{8}
\]

It is minimally UNSAT: deleting the first unit permits all zeros, deleting the last unit permits all ones, and deleting implication \(i\) permits a prefix of ones followed by zeros. Convert to strict 3-CNF using the standard independent padding gadgets: replace each unit \(D\) by all four \(D\vee(\pm a)\vee(\pm b)\) clauses with fresh \(a,b\); replace each binary clause \(E\) by \((E\vee z_i)\land(E\vee\neg z_i)\) with a private fresh \(z_i\). Call the result \(P_k\).

The padded formula is minimally UNSAT, because deleting one of the four unit-gadget rows permits the originally forbidden unit assignment with one suitable auxiliary pair, while deleting one of a binary-gadget's two rows permits its forbidden assignment with one suitable \(z_i\). All other parts can be satisfied by the same prefix witness. Exactly

\[
\boxed{n(P_k)=2k+3,\quad m(P_k)=2k+6,\quad C^-_{\mathrm{sign}}(P_k)=3(2k+6).}
\tag{9}
\]

Yet one uniform correct SAT solver can recognize this entire explicitly ordered family by a single fully charged source scan, output UNSAT on a verified match, and use any complete SAT algorithm as a fallback on all other inputs. For these inputs it uses \(\widetilde O(N)\) time, \(O(\log N)\) auxiliary space, and \(\widetilde O(N)\) auxiliary cumulative memory under the indexed input model. A linear-size logical resolution certificate is also available by first deriving the two endpoint units and each implication, then propagating along the path. Hence maximum source-sign sensitivity does not imply hard incompatibility synthesis.

The executable audit independently checks \(k=2,3,4,5,6,7\), including global UNSAT and a separate SAT deletion witness for every row. Each witness is also verified to satisfy the source after flipping *each* of that row's three literal signs.

## 8. Exact scope of what remains open

Theorem 1 establishes unconditional acquisition across every sound deterministic algorithm under the stated source-bit variation contract. It does **not** establish a superpolynomial cost of deriving the verdict after or during those observations. The proof explicitly permits algebraic shortcuts, matching, parity cancellation, circuit evaluation, cached interpretations, and any other legal computation.

The next load-bearing lemma, **POST-ACQUISITION-INCOMPATIBILITY1**, must show a compulsory charge that cannot be prepaid by the sign observations or shared preprocessing. Its proof must quantify over a *fixed all-input correct solver*, one hard family with both SAT and UNSAT neighboring inputs, one physical execution, and a bound on how often actual machine events can discharge the proposed obligations. A potential defined only for a preferred inference DAG or for an exact reusable relation is not sufficient, since the final decision need not materialize either object.

The strict T5 input language has a fixed, unsigned relation. Consequently the present independently flippable sign-bit alternatives are not in that language. A T5 transfer would need new legal source edits or a compiler/reduction preserving the relevant resource regime and both labels. Similarly, in exact-(2,2) signed 3-CNF, a one-bit sign flip can violate the occurrence promise. No such transfer is asserted.

The source-information measure here is sharply characterized and capped at \(O(N)\). Any superpolynomial resource-lower-bound program must now isolate computation beyond this source-access certificate, or find a different information demand with an independently proved compulsory decoder and bounded event reuse. P versus NP remains OPEN.

## Finite evidence and references

The script `audit_sensitivity.py` and immutable generated `audit_sensitivity_results.json` were executed and checked together. Four small observation-mask spaces were exhausted: 8 one-guard masks, 64 two-guard masks, 4,096 duplicated-guard masks, and 4,096 four-guard masks. The script also tests all literal flips on the final 20-row source and the six symbolic chain sizes. This is a finite audit, not a formal verification of the general theorem or of the machine implementation.

[1] Harry Buhrman and Ronald de Wolf. *Complexity Measures and Decision Tree Complexity: A Survey*. Theoretical Computer Science 288(1):21-43, 2002. https://doi.org/10.1016/S0304-3975(01)00144-X. Standard sensitivity, certificate, and deterministic decision-tree concepts. The exact signed-CNF identity above is independently derived here.

[2] Stefan Szeider. *Minimal Unsatisfiable Formulas with Bounded Clause-Variable Difference are Fixed-Parameter Tractable*. Journal of Computer and System Sciences 69 (2004). https://www.ac.tuwien.ac.at/files/pub/szeider-jcss-2004.pdf. Background on minimal unsatisfiability and certification. No algorithmic optimality is inferred here.

[3] P versus NP project. *Optimized Boolean Erasure and the Final Pin*, `research/main/Optimized_Boolean_Erasure_and_Final_Pin_2026-11-22.md`, commit `6b2209794e725302c504a31b67815aadf25560d5`. The guarded construction and source-core profile are adopted from that verified predecessor.

[4] P versus NP project. *Shortest Obstructions and Charged Incompatibility*, `research/main/Shortest_Obstructions_and_Charged_Incompatibility_2026-11-22.md`, commit `f2df35984424e038de224c401daec634f83c47b1`. The inclusion-minimal shared-union identity is adopted; no implicit sum of slice execution costs is introduced.
