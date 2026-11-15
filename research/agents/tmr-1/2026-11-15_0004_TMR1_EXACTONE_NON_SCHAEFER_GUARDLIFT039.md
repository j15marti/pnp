# TMR-1/039: Arbitrarily many essential, non-Schaefer interface variables do not inherit Resolution hardness as interpolant complexity

**2026-11-15 00:04 PST | GUARDLIFT071 | TMR-1, PNP Machine Model Lead**

**Scientific status:** PROVED/RESTRICTED for exact propositional equivalence, common-variable Craig interpolation and native shared-DAG Resolution inference counts. Independent peer mathematical review OPEN. Finite executable checks COMPUTATIONAL. Transfer to arbitrary deterministic SAT machines, a superpolynomial fusion-safe initial potential, and P versus NP remain **OPEN**.

## 1. Candidate and falsifiers fixed before corpus/primary-source review

**Candidate:** Generalize TMR-1/038's one-literal guarded interpolation counterexample to a growing common-variable interface that is simultaneously (i) genuinely non-Horn, non-dual-Horn, non-bijunctive, non-affine, (ii) sensitive to every shared coordinate, and (iii) still computable by a polynomial-size circuit. Prove native Resolution hardness survives while the uniquely forced separator is easy. This **falsifies the proposed implication** that a non-Schaefer growing separator plus a Resolution-hard source is enough to force a hard interpolant or a fusion tariff.

Advance falsifiers: **F1** a SAT base CNF could make the proposed A-side projection larger than its target; **F2** the B-side might not be the exact complementary projection, destroying uniqueness or UNSAT; **F3** guard sharing could enable a native Resolution shortcut, invalidating the restriction lower bound; **F4** an efficient authenticated XOR, a source-aware SAT machine or a cheap proof mode could make the selected native proof-cost lower bound irrelevant to the same-system universal-machine transfer. F1-F3 are resolved at the exact claimed scope; F4 is a real cross-system firewall, not a counterexample to the native theorem.

## 2. Complete construction and encoding

Let F(Y) be any **UNSAT** CNF on private variables Y. Let X=(x_1,...,x_k), k>=3, be disjoint shared variables. Define the exact-one-of-k predicate

$$
J_k(X)=1 \quad\Longleftrightarrow\quad \sum_{i=1}^k x_i=1.
$$

Write its standard CNF as D_0 AND the D_{ij}, with

$$
D_0=x_1\vee\cdots\vee x_k, \qquad D_{ij}=\neg x_i\vee\neg x_j\quad(1\le i<j\le k).
$$

There are q_k=1+binom(k,2) D-clauses. Define

$$
A_{F,k}(X,Y)=\bigwedge_{D\in\operatorname{CNF}(J_k)}\ \bigwedge_{C\in F}(D\vee C).
$$

Define the X-only B side, which excludes precisely the k singleton satisfying assignments of J_k:

$$
B_k(X)=\bigwedge_{i=1}^k\Bigl(\neg x_i\vee\bigvee_{j\ne i}x_j\Bigr)=\neg J_k(X).
$$

Set G_{F,k}=A_{F,k}\wedge B_k. Every displayed source clause is authenticated as an actual literal list; no free semantic oracle or shortening of the proof grammar is assumed. The source is *not* asserted to be proper 3-CNF: widths include k+3, five, and k. A finite standard signed-literal encoding has length L equal to the actual serialized number of literals times O(log(number of variables)); private identifiers, repeated source blocks, and B are all charged if one later discusses machine time.

**Concrete qualified system R:** ordinary non-weakening Resolution over the complete explicit source G. States are shared-DAG sets of source/derived clauses with their source provenance, paid inference identities, pivots and final empty-clause status. A legal native paid operation resolves two available parents on a valid signed pivot, adds one derived clause, and costs one inference; source axioms may be reused without a paid inference (the standard inference-count convention). Unknown other operations are NOT presumed illegal in a larger proof system or physical machine. Goal: derive the empty clause with an authenticated source-inclusive shared Resolution DAG. This qualification is different from the older /341 FAIL authority, /386 restricted authority, Q-XOR3, and unrestricted SAT machines.

## 3. Main theorem, exact proof

**Theorem GUARDLIFT071.** For any UNSAT CNF F over private Y, any k>=3, and standard native Resolution inference-count minimum S_RES:

1. Both A_{F,k} and B_k are separately satisfiable, while G_{F,k} is UNSAT.
2. Every Craig interpolant of A_{F,k} versus B_k over their common variables X computes *exactly* J_k. In particular, there is a circuit of O(k^2) elementary Boolean gates for the unique separator.
3. With q_k=1+binom(k,2),

$$
\boxed{S_{\mathrm{RES}}(F)\le S_{\mathrm{RES}}(G_{F,k})\le q_k S_{\mathrm{RES}}(F)+k^2.}
$$

The right inequality counts inference steps, not source axiom reads or serialized proof bytes, and preserves shared-DAG reuse.

**Proof of items 1-2.** Distributivity for a fixed D gives

$$
\bigwedge_{C\in F}(D\vee C)
\equiv D\vee\bigwedge_{C\in F}C
\equiv D,
$$

because F is UNSAT. Consequently A_{F,k} is equivalent as a Boolean function on (X,Y) to J_k(X), independently of Y. The formula B_k is exactly NOT J_k. The X projection of A is therefore the J_k=1 set, and the X projection of B is its complement. A separator I satisfies A implies I and I implies NOT B, forcing J_k implies I implies J_k. Both sides have assignments (e.g. x_1=1, all other x_i=0 for A, and all-zero X for B). Computing a running count capped at 2, or positive OR plus pairwise exclusion, gives an O(k^2) circuit.

**Proof of the left inequality.** Restrict every shared x_i=0. D_0 becomes false, so its complete guarded source block becomes F; every pairwise D_{ij} becomes true, and every B_i becomes true. Thus the restricted joint source is **exactly F**, with duplicates/tautologies ignored. Restricting a standard Resolution proof can only remove or simplify lines, never increase the number of native inference steps. Hence S_RES(G)>=S_RES(F). Importantly, this is a source-preserving restriction argument, not a proof lower bound for an arbitrary SAT program.

**Proof of the right inequality.** Take a shortest shared-DAG Resolution derivation of empty from F. For each of the q_k guards D, copy its derived clauses with D appended. On any private pivot y, the valid source-local resolution

$$
(D\vee E\vee y),\quad(D\vee E'\vee\neg y)
\ \vdash\ D\vee E\vee E'
$$

lifts each original inference exactly once. Its lifted conclusion is D. This gives all q_k guards after at most q_k S_RES(F) inferences. For each i, start with the actual B_i source and use the acquired pairwise guards D_{ij} to eliminate each positive x_j, j!=i, deriving the unit -x_i in k-1 inferences. Finally resolve D_0 successively against the k negative units to derive empty in k inferences. Thus the post-lift work is k(k-1)+k=k^2. Shared source DAGs are copied q_k times, not expanded as proof trees. QED.

## 4. Non-Schaefer control and growing hard family

J_k is sensitive to every shared input x_i (all-zero versus the singleton e_i). For k>=3, let e_1,e_2,e_3 be three distinct singleton satisfying assignments: e_1 AND e_2 =0 (violates the Horn closure test); e_1 OR e_2 has two ones (violates dual-Horn closure); coordinatewise majority(e_1,e_2,e_3)=0 (violates bijunctive/2-SAT closure); e_1 XOR e_2 XOR e_3 has three ones (violates affine closure). These are **semantic** failures, not merely syntactic mixed signs. Nonetheless J_k is O(k^2), a valid compact shared representation.

For an independently fixed family F_H of odd-charge Tseitin 3-CNF contradictions on connected cubic constant-expansion graphs with H vertices, the source has 4H clauses, 3H/2 edge variables, and native Resolution size 2^{Omega(H)} by Ben-Sasson--Wigderson [1], Theorem 4.1 and Corollary 4.1 of the original 1999 ECCC version (printed p.10; journal JACM 48(2), 2001). Choose k=H. Then G_H is an explicit guarded CNF family with O(H^3) clauses, O(H^3) literal occurrences, and standard literal-list encoding length

$$
L_H=\Theta(H^3\log(H+2)).
$$

It follows that

$$
S_{\mathrm{RES}}(G_H)\ge 2^{\Omega(H)}
 =2^{\Omega((L_H/\log L_H)^{1/3})},
$$

yet its *unique* interpolant is non-Schaefer exact-one on H shared variables with O(H^2) circuit size. This is a **restricted exponential native Resolution lower bound** paired with an easy circuit, not a circuit lower bound. An explicit uniformly constructible cubic-expander sequence is required for the explicit-family claim; otherwise the same assertion is a family-of-expanders statement.

A fixed complete uniform SAT decider can soundly recognize the source grammar of these wrappers and directly validate the authenticated odd-charge Tseitin core: check all four local clauses per cubic parity block, edge incidence twice, the odd global charge, the guard matrix, and B. If validation succeeds, output UNSAT; otherwise fall back to exhaustive deterministic SAT. This uses polynomial time on this family, not on all formulas. Thus any positive unconditional machine-cost tariff proportional to the exhibited Resolution lower bound is refuted on G_H. The entire algorithm is total and correct, though its generic fallback is exponential.

## 5. Executed reproducible checks and hostile controls

**Exact byte-identical ES2020 verifier:** experiments/tmr/tmr1_exactone_guardlift071.js. Executed inside a native V8 JavaScript isolate, not as a compiled physical Turing machine. It runs exhaustive two-private-variable CNF source subsets (all 256 combinations of eight nonempty non-tautological clauses), classifies 161 UNSAT and 95 SAT, constructs shortest-by-saturation base Resolution DAGs for the UNSAT subset, derives and independently verifies all 644 lifted proof transcripts for k=3,4,5,6, checks every X,Y truth assignment for the A/B projections, validates every parent and signed pivot, and tests the exact inference budget. Additional falsifiers include SAT base F, malformed/missing-complement behavior, and the Horn/dual-Horn/Krom/affine closure witnesses. **160,229 assertions, zero failures**; maximum constructed transcript 186 lines. Raw evidence: results/raw/tmr/2026-11-15_0004_TMR1_GUARDLIFT071_V8_RAW.json.

Finite tests verify implementation and small logical cases only. General theorem rests on symbolic distributivity, authentic proof lifting and the standard restriction lemma, not the finite output. The exact published script was run before commit from its in-memory source; the independent postpublication execution check is separately recorded.

## 6. Provenance, exact comparison, dependency status

- NEW relative to TMR-1/038: **growing** k-coordinate common interface, **non-Schaefer** unique separator, general q_k-copy guard-lift theorem and k^2 appended refutation, explicit quantitative L_H relation. TMR-1/038 established only one literal z with S(F)<=S(A AND B)<=S(F)+2. This report does not claim interpolation theory as a new mathematical field result.
- TMR-2/038: a different nonaffine cofactor/autarky firewall. Its global UNSAT satisfaction relation has one cofactor; ours explicitly partitions into A and B, with nonaffine shared separator but a cheap circuit. Both are hostile controls.
- TMR-3/038, TMR-4/039 and TMR-5/035: proof-record macro, mode choice, fused output-event and alternate Resolution DAG controls show why a selected native proof cannot be charged to a physical SAT machine or an authority allowing authenticated XOR.
- LEAD-0029 Lipschitz audit: do not translate exponentially long semantics or expensive selected derivations into forced actual work. An all-step tariff valid for arbitrary SAT machines would have to allow the polynomial recognizer and possible compact shared syntax.
- Primary [1] E. Ben-Sasson and A. Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, ECCC TR99-022 (1999), Theorem 4.1/Corollary 4.1, printed p.10, https://eccc.weizmann.ac.il/report/1999/022/download ; journal JACM 48(2), 149-169 (2001), DOI https://doi.org/10.1145/375827.375835. Original PDF page was screenshot-inspected.
- Primary [2] J. Krajicek, *Interpolation Theorems, Lower Bounds for Proof Systems, and Independence Results for Bounded Arithmetic*, Journal of Symbolic Logic 62(2), 457-486 (1997), DOI https://doi.org/10.2307/2275541, publisher abstract examined. Feasible interpolation supplies a circuit **upper bound** from a proof; it does not supply the converse. No numerical theorem from [2] is imported into GUARDLIFT071.

**Dependency map:** source authentication PASS for the stated explicit native clauses; native Resolution guard-lift PASS restricted; Craig separator uniqueness PASS; k-growing non-Schaefer semantic controls PASS; original Tseitin native lower bound KNOWN THEOREM; direct fusion initial gap from separator **FAIL on this family** (cheap O(k^2) interpolant); stronger proof authority/transcript/physical-machine transfer **OPEN**; superpolynomial **machine** lower-bound family **OPEN**; P versus NP **OPEN**.

### Peer next target

**TMR-2:** Search for a source-aware *joint separation* family with no polynomial-size interpolant after compact affine/nonlinear circuit quotients; mere non-Schaefer syntax or many essential interface bits cannot suffice. **TMR-3:** Audit whether recognizing the exact guard grammar on a locally moving machine is polynomial under explicit input/work-cell charges. **TMR-4:** Derive exact fusion tariff rows for the lifted D proof and the direct O(k^2) interpolant, preserving cheaper mode choices and all zero-cost edges. **TMR-5:** Independently audit the k^2 refutation derivation, the restriction lemma on shared DAGs and the L_H=Theta(H^3 log H) encoding count.

**Trackers:** Both root proof1.txt and proof2.txt, and canonical main.tex fully recovered (proof2 and main by Git blob SHA), inspected, and not modified. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No schedule changes. No promotion of an OPEN transfer to main.

END_OF_REPORT::TMR1::039::GUARDLIFT071::2026-11-15_0004_PST
