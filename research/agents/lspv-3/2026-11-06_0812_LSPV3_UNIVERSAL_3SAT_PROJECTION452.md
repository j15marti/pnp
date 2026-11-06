# LSPV-3/452: Universal 3-CNF projection and lower-bound transfer

**2026-11-06 08:12 PST | Route B | KNOWN THEOREM / PROVED-RESTRICTED / COMPUTATIONAL / OPEN.** P versus NP OPEN. This is a new report on old source families, not a claimed new universal SAT lower bound. Role allocation 2 Route A / 3 Route B, schedules, identities, historical weights and root manuscript remain unchanged.

## Idea -> falsifiers -> tested revision

Hypothesis: source-authenticated existential interface projection is universal over 3-CNF and can be implemented *without changing* historical R_mix341 by paid native Resolution nodes. A lower-bound invariant still requires **all-rule** proof backtranslation, not just a semantic reduction.

Four falsifiers: (F1) exact projection disagreement with brute-force models; (F2) pure affine summary of general OR3; (F3) treating DP elimination work as a lower bound over shared mixed proofs; (F4) assuming the exact interface class is polynomial-time recognizable. Outcomes: F1 passed theory and 53,706 exhaustive finite comparisons; F2 false via affine-closure obstruction; F3 false on original cubic K4 source (27-31 DP-RES versus 15 authenticated mixed nodes); F4 false even for one visible bit (NP-complete nonempty-affine projection recognition).

## Universal projection (KNOWN THEOREM)

For arbitrary 3-CNF $F(L,B,R)=F_L(L,B)\land F_R(B,R)$, disjoint internal sets $L,R$ yield

$$
\exists L,R\,F=(\exists L\,F_L)\land(\exists R\,F_R).
$$

Thus UNSAT iff the two exact interface relations have empty intersection. This is an algebraic identity and **not an additional historical proof rule**.

For a selected $x$,

$$
F=F_0\land\bigwedge_i(x\lor A_i)\land\bigwedge_j(\neg x\lor B_j)
\quad\Longrightarrow\quad
\exists x\,F\equiv F_0\land\bigwedge_{i,j}(A_i\lor B_j).
$$

All non-tautological resolvents have two parent clauses and a pivot; they can be introduced through paid native RES nodes. Iterate over every variable. For UNSAT the empty clause arises, with original-source-labelled ancestry and shared subproofs charged once. This proves completeness of a particular source-authenticated **upper-bound algorithm**, which may create exponentially many clauses.

For literals regarded as Boolean polynomials over $\mathbb F_2$, $q_C=\prod_{\ell\in C}(1+\ell)$ is a clause-violation indicator. The formula indicator is $f_F=\prod_C(1+q_C)$ in the Boolean quotient $x_i^2=x_i$. Exact elimination of a Boolean variable is

$$
\mathcal E_x f = f|_{x=0}+f|_{x=1}+f|_{x=0}f|_{x=1}.
$$

The OR is nonlinear: no generic GF(2)-only proof may be silently inferred from this semantic formula.

## Rigorous barriers (PROVED/EXACT)

**Affine impossibility:** existential projection of a conjunction of linear GF(2) equations remains affine and therefore is closed under the ternary operation $a\oplus b\oplus c$. The satisfying assignments $100$, $010$, $110$ of $x\lor y\lor z$ violate this: their XOR is $000$, which falsifies the clause. Thus pure XOR with arbitrarily many existential auxiliary variables cannot exactly encode even one general 3-clause.

**Classification hardness:** Given arbitrary 3-CNF $G(y)$, let $F(x,y)=(x)\land G(y)$. The one-bit existential interface $\{x:\exists y\,F(x,y)\}$ equals $\{1\}$ if $G$ is SAT and $\varnothing$ otherwise. Every nonempty one-bit Boolean relation is affine. Hence deciding nonempty-affine projection is NP-complete for 3-CNF of width at most three. The fixed-width classification of blkph0x/p-vs-np-proof-research is a relevant independent hypothesis source; this particular $k=1$ proof is elementary and independently checked mathematically.

**General weak work sandwich:** for UNSAT $F$, if every paid, sound inference has at most two genuine premises and all source clauses used by a refutation are source-labelled, put $u(F)$ = the number of clauses in a smallest UNSAT subformula. The source-ancestry graph gives $u(F)-1\le W_R(F)$ under unit weights. A particular paid DP Resolution derivation supplies a finite upper bound $W_R(F)\le U_{\mathrm{DP}}(F)$. This sandwich applies in the declared semantic binary-premise model; its lower term is at most linear and cannot prove superpolynomial growth.

## Reused published family and exhaustive finite results (COMPUTATIONAL)

Original LSPV-3/450 **odd K4 cubic-Tseitin** strict 3-CNF fixture, six edge variables, sixteen clauses, 163 ASCII DIMACS bytes, original SHA-256 **ea08104837e167b9ebd06d8f50442d828e3ba4d81f79dff8c14a09ba30050096**. Odd original has zero models out of 64 valuations; flipping only the parity requirement of the first vertex produces an even-charge companion with exactly eight models.

- Exhausted all **17,902** formulas formed from at most four of the 26 proper clauses over three variables: all **53,706** one-variable exact projection comparisons passed.
- Exhausted **720** variable elimination orders for odd K4. Under the producer's deterministic duplicate-parent selection and ancestry pruning, paid RES nodes range **27-31**, with **144** orders realizing 27. This is **not** an optimum over arbitrary Resolution proofs, only the tested complete elimination schedules.
- Full original source-label and oriented RES parent checking in the Python producer: 91,290 assertions. Independently written Node.js checker: 360 assertions and three corrupt-certificate rejections.
- Project's earlier MIXED-TSEITIN-MIN-DAG341 establishes **15** global unit-node mixed AND3/XOR minimum for bridgeless cubic K4. The DP result is a strictly worse valid construction, NOT evidence of a lower bound for the full calculus.
- Actual run resources measured on Linux: producer 3.84 s wall / peak 97,296 KiB RSS; independent checker 0.04 s wall / peak 27,508 KiB RSS. Source parse, all generated/unused clauses, proof construction, verifier, intermediate states, output and failed-policy overhead belong to **actual algorithm** cost, not ideal $W_R$.

The reproducible full producer, independent checker, raw original-source proofs, machine ledger, report, and SHA-256 manifest are preserved in the conversation artifact LSPV3_452_UNIVERSAL_3SAT_PROJECTION_REPRO.zip. The historical authoritative byte checker was **not** run. Native acceptance beyond the declared RES rule is **not** claimed.

## Exact hard-family ledger and surviving model gap

| Family | 3-CNF / size | Certified lower bound | Strongest shortcut / missing transfer |
|---|---|---|---|
| Cubic odd-charge expander Tseitin | Yes, $h$ cubic vertices, $3h/2$ variables, $4h$ signed strict 3-clauses, $\Theta(h\log h)$ indexed bits | Exponential ordinary shared-DAG Resolution for appropriate expanding graphs | Declared mixed AND3/XOR has $4h-1$ nodes on bridgeless cubic graphs; no resolution-to-mixed lower bound |
| Braun bit-PHP | **No:** original clauses have width $2\ell$, $n=2^\ell$ holes, $(n+1)\ell$ bits, $n\binom{n+1}{2}$ clauses | 2026 revised **preprint** Theorem 1.1 claims $S>\exp(n/(32768\ell^2))$ for unrestricted DAG $\mathrm{Res}(\oplus)$ when $\ell\ge32$ | His system excludes defining extension axioms. Ordinary equisatisfiable strict-3CNF gadgetization is not a size-lower-bound preservation proof; nested DEF is open |
| PHP (Haken) | Usual PHP has wider clauses; exact 3-CNF reduction needs proof simulation | Exponential ordinary Resolution | Polynomial Extended Resolution, not a mixed lower bound |

**Promising universal restricted invariant:** Braun preprint Theorem 9.1 gives a general dimension bound for every DAG $\mathrm{Res}(\oplus)$ proof (under its theorem's specific PC-degree separation hypothesis):

$$
\dim U\le (3S+|J|)\binom{v-h(k+1)-1+k}{k}.
$$

Every ordinary 3-clause is also a disjunction of affine equalities, hence a linear clause for that restricted system. A sufficiently large polynomial space $U$ separated from low-degree PC consequences would yield a genuine lower bound **for $\mathrm{Res}(\oplus)$**, not for R_mix341. Establishing $U$ and simulating nested DEF, LOCAL, AND3, sharing and original-source ports remain open. The preprint itself identifies nested definitions as an unresolved extension-removal problem. Its formalization claims were reviewed at paper level, not independently replayed here.

## Required proof-backtranslation direction, OPEN

For an established hard source $H_k$ in system $S$ and its polynomial-size 3-CNF image $G_k=T(H_k)$, transferring hardness requires:

$$
\forall\pi\in\operatorname{Ref}_{R_{\mathrm{mix341}}}(G_k)\quad
\exists\pi'\in\operatorname{Ref}_{S}(H_k):
W_S(\pi')\le p(|H_k|+W_R(\pi)).
$$

Then a lower bound for $W_S(H_k)$ would constrain **every** legal R proof of $G_k$. Equisatisfiability of $T$ alone does NOT imply the displayed simulation. If a compiler's overhead is polynomial only in explicit proof *bits*, a separate polynomial certificate-bit normalization in $|G_k|+W_R(\pi)$ is needed to get a node-weight bound. Charge long IDs, source reads, nested definitions, references, temporary growth, recomputation, and branch scope; never silently change the R_mix341 grammar. OR alternatives choose one derivation, AND obligations require both incompatible branches unless legally discharged, and shared DAG nodes are charged once.

This experiment supplies a universal **upper-bound framework**, a rigorous affine obstruction, an NP-hard classification control, and a useful restricted lower-bound research target. It does **not** establish a superpolynomial all-rule $\overline W_R$, a noncircular B3 or P!=NP. Those remain OPEN. Root main.tex was left unchanged because complete safe contents were unavailable.

## Source/corpus audit

Project original R_mix341 semantic grammar: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd11; LSPV-3/451 report blob 3b3ef722; November 2 five-role governing handoff, current issue #3, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md. External repositories inspected: konard/p-vs-np/scripts/proof_status.json SHA 93b77ed3; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md SHA 18d693ea and affine-projection theorem SHA 4aba9d94; meelgroup/frat-xor/format.md SHA 986a21aa. FRAT-XOR warns that the current cake_xlrup accepts XOR but not BNN and is not an R_mix341 native proof format. OpenAI GitHub indexed search found no relevant native grammar transfer. Actual Google-branded search unavailable; general indexed web/literature search used. No current full root main.tex bytes; no unsafe root edit.

Primary references: Haken, *TCS* 39 (1985) 297–308; Ben-Sasson & Wigderson, *JACM* 48 (2001) 149–169; Schaefer, STOC 1978; Bova et al., IJCAI 2016; Mikša & Nordström, *JACM* 71(6) (2024); Braun, arXiv:2609.23015 revised October 22 2026 (preprint, not silently treated as peer reviewed); project LSPV-2/341 and LSPV-3/451.