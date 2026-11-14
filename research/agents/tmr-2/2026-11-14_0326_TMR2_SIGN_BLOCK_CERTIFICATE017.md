# TMR-2/017: source-aware query certificates, zero singleton sensitivity, and disjoint sign-block necessity

**Pacific timestamp:** 2026-11-14 03:26 PST (America/Los_Angeles). **Role:** TMR-2 Information Necessity, j15marti/pnp main. **New symbolic claim TMR2-SBC17:** CANDIDATE/RESTRICTED pending TMR-5/TMR-1 independent review, with a complete argument below. **Finite hosted V8 and independent local native CPython tests:** COMPUTATIONAL. **Unrestricted superpolynomial 3-SAT machine bound and P versus NP:** OPEN.

## 1. Exact machine and quantifier scope

Let A be any ONE fixed finite, total, uniform deterministic multitape machine, with fixed alphabet and finitely many writable tapes, deciding a fixed explicit binary encoding of proper 3-CNF formulas on ALL input lengths. There is one locally moving read-only original-input head, initialized at left endmarker position 0; L data bits lie in physical cells 1,...,L, with right endmarker L+1. In every charged transition the machine reads only symbols at current head positions, moves each head by at most one cell, and charges all preprocessing, tape storage, rereads, recomputation, output, and malformed-input handling. Define Q_A(x) to be the set of immutable source DATA bit positions actually read during the COMPLETE halting run on x. The source and all heads are part of the actual machine configuration. No online/one-pass restriction, free oracle, ROM lookup, unbounded word operation, forced certificate output, or workspace bound is imposed.

The separation target is NOT assumed: for each correct A, each integer k>=1, C>0, L0, find valid F with |F|>=L0 and T_A(F)>C(|F|+1)^k. Our result proves only lower bounds of order at most L on a specially structured family. All quantifiers and resource bounds refer to the SAME A and SAME F.

**Lemma TMR2-QUERY17 (exact transcript certificate).** For any x of length L and any same-length y satisfying y_j=x_j for all j in Q_A(x), the COMPLETE run of A on y is identical to its run on x, including every input-head move, work-tape update and terminal label. Therefore, if x and y have opposite correct labels, Q_A(x) intersects D(x,y)={j:x_j!=y_j}. In particular, if there are d pairwise disjoint sets B_i of bit positions and same-length valid opposite-label sources y_i differing from x only within B_i, then |Q_A(x)|>=d and T_A(x)>=d (for one current-cell source head; for h heads, T>=d/h with the exact h-port charge).

**Proof.** Couple the deterministic runs from their IDENTICAL initial internal state and equal source lengths. Inductively, their finite controls, work tapes, work heads and source-head positions agree, since every source cell read by the x-run belongs to Q_A(x) and has the same symbol in y. Thus each next concrete transition agrees, including the halt. If labels are opposite, at least one cell of D must occur in Q_A(x). Distinct disjoint B_i require distinct observed source positions. This is a statement from initial-state determinism and all-input correctness, not a false assertion that arbitrary source-blind intermediate checkpoints are reachable on every alternate source. QED.

This is a **query/certificate** lower bound, not a lower bound on post-query semantic processing. It is at most L for every length-L input because full sequential acquisition visits all L bits in O(L) source-head moves. Correctly observing every bit and correctly DECIDING SAT are different tasks. Nisan 1991 and Buhrman/de Wolf 2002 discuss the corresponding decision-tree measures in their exact query models; the source-bound TM transcript lemma above is proved directly and does not inherit any restricted-model runtime separation.

## 2. Strict proper-3CNF family with independent opposite-label sign blocks

For n>=1, start with a minimally unsatisfiable **Horn 2-CNF** chain

$$
G_n=(x_1)\ \wedge\
\bigwedge_{i=1}^{n-1}(\neg x_i\vee x_{i+1})\
\wedge\ (\neg x_n).
$$

Replace each unit base clause (a) by FOUR proper 3-clauses, with two fresh auxiliary variables u,v unique to the gadget:

$$
(a\vee u\vee v),\quad
(a\vee u\vee\neg v),\quad
(a\vee\neg u\vee v),\quad
(a\vee\neg u\vee\neg v).
$$

Replace each binary base clause (a\vee b) by TWO proper 3-clauses with fresh z:

$$
(a\vee b\vee z),\qquad(a\vee b\vee\neg z).
$$

Call the resulting ordered proper 3-CNF H_n. It has

$$
N=2n+3\text{ variables},\qquad m=2n+6\text{ clauses}.
$$

Each clause contains three DISTINCT variables. The auxiliaries are disjoint between gadgets. Existential elimination of each gadget's private variables recovers its original unit or binary clause. Hence H_n is UNSAT, since G_n forces x_1=...=x_n=1 and also \neg x_n.

**Every clause in H_n is sign-pivotal.** For any clause j, flip the sign of its designated private auxiliary literal (u in a unit-gadget clause, z in a binary-gadget clause), leaving all other clauses unchanged. The two-clause gadget now duplicates a clause, making its formerly impossible base-false case satisfiable. The four-clause unit gadget likewise duplicates one of its other clauses, leaving one (u,v) assignment allowed when its base literal is false. Because G_n is MINIMALLY UNSAT, its other base clauses can all be satisfied while the selected base clause is false: before the first unit, take all x_i=0; at implication index i, take x_1,...,x_i=1 and x_{i+1},...,x_n=0; at the last unit, take all x_i=1. Fresh auxiliaries then satisfy every other gadget. Thus each one-sign-flipped H_n is SAT. This is an all-n symbolic construction, not an experimental inference.

For integer r>=1 define

$$
F_{n,r}=\bigwedge_{c\in H_n}\ \bigwedge_{t=1}^{r} c^{(t)},
$$

where c^(t) is an exact, separate ordered copy of c, with identical variable IDs. The executed artifact uses equivalent copy-major ordering. F_{n,r} is UNSAT. For each original clause j, flip its designated auxiliary sign in ALL r copies, making a valid SAT source F'_{n,r,j}. Let B_j consist of precisely these r sign-bit positions. The m sets B_j are pairwise disjoint.

For r>=2, flipping ANY SINGLE sign bit in the encoded F_{n,r} leaves at least one complete intact H_n copy, so every same-layout singleton sign-bit neighbor remains UNSAT. Yet flipping the r-bit block B_j yields SAT for EVERY j. Consequently, over the sign-bit positions,

$$
s_{\mathrm{sign}}(F_{n,r})=0\quad(r\ge2),\qquad
bs_{\mathrm{sign}}(F_{n,r})\ge m,\qquad
|Q_A(F_{n,r})|\ge m.
$$

Here the last bound follows from the EXACT source-aware transcript lemma, not a RAM-query assumption. The first two statements distinguish singleton sensitivity from disjoint-block sensitivity; we make no claim about arbitrary header-bit sensitivity, alternative 3-CNF encodings, or equality of full block sensitivity.

### Binary representation and physical movement charge

Use the fixed, all-length grammar: Elias-gamma positive integers N and M in a header, followed by M records, each containing THREE pairs of a fixed-width w=ceil(log2(N+1)) variable index and ONE literal sign bit. Variable IDs must be in 1,...,N, indices in a clause must be distinct, and malformed strings have a designated label. This is a conventional explicit binary record grammar for all proper 3-CNFs, not an encoding that hardcodes the chain. Flipping a designated sign bit preserves length, parsing, index validity and the other signs.

Writing g(t)=2 floor(log2 t)+1, the exact length of F_{n,r} is

$$
L_{n,r}=g(2n+3)+g(r(2n+6))
+3r(2n+6)(w+1)=\Theta(rn\log n).
$$

Therefore, for fixed r, EVERY eligible correct A must read at least m=2n+6=Omega(L/log L) distinct source bits on F_{n,r}. Moreover B_m, the sign block of the LAST clause of the first copy, lies at physical positions no smaller than

$$
p_{n,r}=g(N)+g(rm)+3(m-1)(w+1)+2w+2.
$$

The source head starts at 0 and moves at most one cell per transition. The opposite-label source differing ONLY on B_m forces a read of one of these physically late cells. Thus

$$
T_A(F_{n,r})\ge p_{n,r}=\Omega(L_{n,r})
\qquad\text{for each FIXED }r.
$$

The exact last-cell lower bound may differ by one transition depending on whether movement and current-cell read are charged in the same or consecutive transitions; the displayed safe bound T>=p holds in either locally moving convention. For fixed r, p/L tends to 1/r. Neither the query-count nor local-head-distance bound is superlinear.

**Crucial falsifier:** This is a gadget expansion of an elementary Horn 2-SAT contradiction. A ONE fixed all-input correct deterministic 3-SAT decider may check in polynomial source-head time whether its parsed formula is exactly F_{n,r} or one of the single complete block-flip neighbors (for, say, r=1,2,3), return the symbolically proved UNSAT/SAT label in these cases, and otherwise run a generic exhaustive exact solver. The recognition can use ordinary O(log L)-bit counters and polynomially many paid scans. It is correct for ALL inputs, includes malformed handling, is fixed across all n, and is polynomial on this entire special family. Thus a large collection of disjoint valid SAT alternatives, even with zero singleton sensitivity, does NOT compel superpolynomial processing time.

## 3. Explicit hostile controls and model-transfer gaps

* **Auxiliaries and proper 3-CNF:** Every original clause is width three with three distinct IDs, yet its existential projection is a Horn/2-CNF clause. An argument charging the full expanded hypergraph while ignoring cheap elimination fails.
* **Duplicates and shared work:** For r>=2, one changed literal is INERT for SAT/UNSAT, although r coordinated changes alter the label. An adversary must retain block structure, not sum singleton charges. Checking the repeated chain and sharing its summary is polynomial.
* **Renaming/padding:** Consistent variable renaming, sign convention changes and extra repeated clauses preserve the cheap structure; source length and geometric probe charges change. No universal hard UNSAT family is inferred.
* **GF(2), 2-SAT, bounded treewidth:** The construction is already a 2-SAT/Horn compression control; a Gaussian-elimination solver would be another allowed, not compulsory, representation on affine instances. Existing factored-compatibility results on Horn/affine and small interfaces remain restricted, not model-independent lower bounds.
* **Rereads/cache/recomputation:** Q_A records the actual complete input-query set, regardless of repeated visits, storage, work tape encoding or adaptive read order. The argument places NO limit on polynomial workspace. A machine can reread its source after discarding information, consistent with TMR-2/016's wash wrapper.
* **Exact unrestricted bridge:** Transcript necessity holds for ANY correct fixed local-head multitape A under the declared encoding, without requiring identical checkpoints or one-pass behavior. Transfer to nonlocal random-access input, multiple heads, other encodings and a superpolynomial decision-work lower bound is OPEN. h read-only heads yield at most h new data-bit reads per charged step; a nonlocal port needs a quantitatively charged compiler.

## 4. Actually executed reproducibility and status

**Hosted V8 direct execution (published exact function):** n=1,...,14; r=1,2,3; 882 independent disjoint-clause-block opposite-label pairs; 1,764 altered sign bits; 588 unchanged-UNSAT singleton controls for r>=2; 42 encoding/parser roundtrips; 511 independently implemented general DPLL SAT/UNSAT checks at n<=7; 3,822 internal work checks; ZERO failed assertions. Corrected-length formulas span L=108 through L=1,858 among reported controls. These experiments check valid strict-3CNF source encoding, symbolically prescribed witnesses and semantic labels, NOT a physical full SAT Turing-machine microstep emulator.

**Independently written native CPython LOCAL-ONLY test:** n=1,...,14 and r=1,2,3; 882 clause blocks, 588 singleton controls, 511 DPLL checks, 2,352 internal checks, ZERO failures; executed in 0.179 seconds. Python source/raw reside only in the automation's temporary runtime and are NOT shared as GitHub artifacts. Finite testing is COMPUTATIONAL. The **all-n** argument is mathematical and remains CANDIDATE pending independent review.

**Read corpus:** latest 2026-11-13 12:49 PST superseding five-TMR directive; authentic full proof1.txt (28,714 chars) and proof2.txt Git blob (1,051,196 chars despite blank fetch_file); full main.tex Git blob (2,528,412 chars despite blank fetch_file); AGENTS.md, CODEX.md, repository skill, issue #3 through TMR-1/017, all five current TMR handoffs, original TMR-2/016 report/code/raw, original TMR-2/015, TMR-1/017, TMR-3/015, TMR-4/017, TMR-5/014 reports and historical 2026-11-11 affine/factored compatibility source. Older LSPV role mandates superseded, historical results retained.

**Primary sources at precise scope:**
1. Noam Nisan, "CREW PRAMs and Decision Trees," *SIAM Journal on Computing* 20(6):999-1007 (1991), DOI: https://doi.org/10.1137/0220062. Relates block sensitivity to QUERY/parallel complexity, not arbitrary SAT-machine time.
2. Harry Buhrman and Ronald de Wolf, "Complexity Measures and Decision Tree Complexity: A Survey," *Theoretical Computer Science* 288(1):21-43 (2002), DOI: https://doi.org/10.1016/S0304-3975(01)00144-X. Definitions of certificate, sensitivity and block sensitivity; no P!=NP claim.
3. The elementary Horn 2-SAT equivalence and proper-3CNF gadgets here are **proved above** rather than imported as an uncharged complexity reduction.

**Trackers:** TRACKERS REVIEWED; NO MATERIAL CHANGE. This result supplies a restricted query lower bound and an easy-algorithm falsifier, but closes no P1-01/P1-03/P1-04 or P2 unrestricted all-exponent arrow. Neither tracker is edited. Canonical root main.tex is left for TMR-5 whole-document synthesis, and all its historical sections are preserved. No task/schedule changes.

**ONE next target for TMR-2:** Can an input-aware *processing-after-acquisition* obligation be proved on every correct uniform SAT decider without reducing to source-query certificate complexity, without assuming merged checkpoints, and without excluding elimination of private auxiliaries? TMR-3 should evaluate same-trace charges, TMR-4 source-bound all-transition refinement, and TMR-5 independently check each sign-flip gadget, the disjoint block hitting argument and the physical late-bit index.

END_OF_REPORT::TMR-2::017::2026-11-14_0326_PST
