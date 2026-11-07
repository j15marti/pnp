# LSPV-1/474 | Quadratic Boolean-span obstruction for peelable hard-family subformulas

**2026-11-07 PST | Route B | PROVED/RESTRICTED symbolic theorem; COMPUTATIONAL independent finite controls. P versus NP OPEN.**

## Exact proof-chain nodes and scope

This materially strengthens [P2-B14] (linear original-source provenance floor from LSPV-1/473) from *affine* to **all nonzero multilinear GF(2) polynomials of degree at most two**. It is recorded as [P2-B15]; dependencies are [P2-B1] OPEN (all-mixed superpolynomial minimum), [P2-D1] OPEN (historical R_mix341 accepted bytes/grammar), [P2-C3] OPEN (full mixed translation), [P2-B2] OPEN (same-fixed-calculus B3), and [P2-D2] (whole shared AND/OR DAG cost definition). This is NOT an unconditional mixed-calculus lower bound.

## IDEA: falsifiable proposal before research

Hypothesis: the leaf-variable induction of [P2-B14] can be lifted beyond affine GF(2) equations to all **quadratic** original-variable Boolean polynomial identities, without adding any R_mix341 rule.

Falsifiers:
1. A peelable proper signed 3-CNF H has a nonzero degree-2 polynomial P(X) that vanishes on every H model.
2. A leaf-elimination induction leaves a nonzero degree-1 coefficient P1 supported only on the falsifying assignment to the two other literals.
3. A nonpeelable source has a degree-2 consequence despite having a source support structure mistaken for peelable.
4. A branch-local unit implication is incorrectly promoted to an unconditional original-variable equation or to a historical accepted native proof.

The first two are refuted by Theorem 474.1. The third is a positive hostile control; the fourth remains forbidden by assumption scope. No hypothetical native rule or uncharged source inference is used.

## SEARCH: governance, historical origin, literature, and repositories

Read complete root proof1.txt and proof2.txt, issue #3 and current peer comments; AGENTS.md, CODEX.md and the pnp-research skill; 2026-11-02 five-role refocus at historical commit 4e29ed7646f484707767acb6e63ec5f38afd98a8; LSPV-1/473 (blob b62cb5c2b14bf58dfa7ae59647fff5f8df77536b), original LSPV-2/341 (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb), LSPV-3/436 (blob 4d3cfc1747df53916a2aa5ee67421181495360b4), LSPV-3/472, LSPV-5/409, Grok GROKPROOF/2026-11-07_1119_PROGRESS.md and actual Claude research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex. The source /341 specifies RES, AND3, XOR, LOCAL-CONVERT and paid conservative DEF semantically, but does not settle facet selectors or accepted-byte grammar; LSPV-3/436 already exhibits a completion fork. Thus [P2-D1] remains OPEN.

Pinned third-party evidence: konard/p-vs-np README 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 (finite-machine educational model, no P-vs-NP proof); blkph0x/p-vs-np-proof-research METHOD_INDEX 18d693ea71dfa433370eb7afbebc3106e32f03e5 and REVIEW_ADDENDUM 6a7cc2f8962d3fcfcfc1778b1d3d8f5dc8d56d70 (different parity, relaxation and SAT artifacts); meelgroup/frat-xor format.md 986a21aa92b62f844ef1fce852193142c41b2b1f; tanyongkiam/cake_lpr README e94f45e9aa000cd9ada12f4c771ac9daf28fe53c; peitl/short-proof README 93d2090dba9739bc4983c65ea639a24e1f5e0fab; openai/math README cc5b0a03bca6c742f045d683b6647a6f44ef2cae. None is the historical native R_mix341 checker.

Primary literature/public indexed searches included Chvátal–Szemerédi (1988) random 3-CNF Resolution hardness, Carenini ECCC TR26-158 (published 2026-08-30) random 3-CNF Res(k), Cook–Reckhow (1979) proof-system quantifiers, and searches for peelable CNF low-degree polynomial identities, acyclic CNF, and polynomial-calculus degree lower bounds. Related published literature includes Ordyniak–Paulusma–Szeider, *Satisfiability of Acyclic and Almost Acyclic CNF Formulas* (2013), and Gryaznov–Talebanfard (2024) random 3-CNF bounded-depth Frege work; neither was taken as proof of this precise statement. Novelty relative to all literature is NOT established. Google-branded search was unavailable; public indexed web search and GitHub connector reads were used. A git clone via the local runtime failed DNS; connector access succeeded.

## THEOREM 474.1: degree below clause width is impossible under peeling

Let H(X) be a proper signed **width-w CNF**, w>=2, with distinct variables within each clause. Suppose its clause-variable incidence hypergraph can be deleted by repeatedly removing a clause containing a variable occurring in no other *remaining* clause (degree-one peeling). Then H is satisfiable and **no nonzero multilinear Boolean polynomial P(X) over GF(2), of total algebraic degree <w, vanishes on every satisfying assignment of H**.

Proof. Work in the Boolean ring GF(2)[X]/(x_i^2-x_i), whose multilinear functions have unique algebraic normal forms (ANFs). Induct on number of clauses. For empty H all assignments are available; evaluation on the whole Boolean cube is injective. Otherwise peel a clause C whose unique currently occurring variable is v. Rename its literal to z (either v or 1+v; this affine substitution preserves degree) and write C as z OR ell_1 OR ... OR ell_{w-1}, with the other w-1 literals on distinct variables. Let H'=H\{C}; z is absent from H', and H' remains peelable.

Suppose a polynomial P vanishes on Mod(H) with deg P <w. Uniquely decompose P=P_0(X')+z P_1(X'), where deg P_0<w and deg P_1<w-1. For any assignment satisfying H' and any ell_i=1, C is true for **both** z=0 and z=1. Evaluating P at both z values gives P_1=0 there. Consequently each polynomial ell_i P_1 vanishes on ALL H' models: if ell_i=0 its product is zero, and if ell_i=1 then P_1=0. Since deg(ell_i P_1)<=w-1<w, the induction hypothesis forces ell_i P_1 to be the **identically zero Boolean polynomial**.

Thus as a Boolean function P_1 is supported only where ell_1=...=ell_{w-1}=0. A nonzero polynomial with that support is divisible, in the Boolean function ring, by q=product_i(1+ell_i). Since the ell_i are on w-1 distinct variables, the unique ANF of q times any nonzero function of the remaining variables has degree at least w-1. This contradicts deg P_1<=w-2. Hence P_1=0. Every H' model extends to an H model by choosing z to satisfy C; therefore P_0 vanishes on Mod(H'), and induction gives P_0=0. Thus P=0. In particular Mod(H) is nonempty, since the constant polynomial 1 would otherwise vanish on its empty model set. QED.

The degree threshold is sharp: for **one** proper width-w clause C, its unique falsification indicator is a nonzero Boolean polynomial of degree w vanishing on all models of C.

### Corollary 474.2: published Resolution-hard random 3-CNF

Use the same exact signed proper random 3-CNF model as [P2-B14]: n original variables, m=8n distinct clauses chosen from 8*binom(n,3) signed ternary possibilities, binary encoded length N=Theta(n log n). Chvátal–Szemerédi establish UNSAT and 2^{Omega(n)} ordinary shared-DAG Resolution refutation size with high probability for the appropriate fixed-density random model. LSPV-1/473 proved by an explicit 2-core union bound that there is fixed delta>0 such that with high probability **every** source subset of size <=delta*n is peelable. Applying Theorem 474.1 to each such subset yields

$$
|S|\leq\delta n\ \Longrightarrow\
\forall P\in\mathbb F_2[X]\text{ multilinear},\
0<\deg(P)\leq2:\quad F_S\not\models P(X)=0.
$$

The stronger formulation excludes *all nonzero polynomial functions of degree <=2*, including constant 1; the display states positive degree for convenience. The result is a **linear original-clause-support floor** for any sound, unconditional, source-transparent original-variable degree<=2 identity. It is NOT a proof-degree lower bound on general polynomial-calculus proofs, not a bound on arbitrary higher-degree local factors, and not a superpolynomial node-work lower bound.

### Branching, shared DAGs, and auxiliary wires

For any legally discharged branching/shared DAG, a global conclusion must be entailed by the union of actual original source ancestors. Under that source-authentication assumption, <=delta*n source leaves cannot entail a nonzero quadratic original-variable identity or false. A branch-local identity under extra assumptions need not hold globally. For example, source (x OR y OR z) has seven models and full degree-2 evaluation rank, while branch assumptions not x, not y force z. Exporting z without discharge is invalid. Sound conservative definitions may impose quadratic identities on **fresh auxiliary wires**, which the original-variable corollary does not forbid. Paid arity, native LOCAL-CONVERT, explicit evidence, and branch discharge are not authenticated by this semantic theorem.

## ITERATE: independent finite checks and adversaries

A separate Node.js model-row Gaussian rank program and independently written Python model-column bitset rank program were executed locally. Exhaustive proper signed 3-CNF subsets with n=4/k<=2 and n=5/k<=3: 85,928 formulas, 54,576 peelable, 31,352 nonpeelable. On every peelable formula the degree<=2 evaluation matrix has full column rank. Local Node additional n=6 deterministic samples: 512 cases (total 86,440; 54,795 peelable), source branching falsifier, a nonpeelable two-clause quadratic-resolvent control, all eight single-clause degree-3 sharpness controls, odd K4 Tseitin UNSAT with 16 indispensable clauses and even K4 with eight models. Local Node: 109,632 assertions PASS, 0.65 s wall, 36,652 KB peak RSS. Independent Python: 109,161 assertions PASS, 1.49 s external wall, 95,876 KB peak RSS. Independently published V8/Node-compatible standalone: 85,928 formulas, 54,576 peelable, 109,158 assertions PASS, exact GitHub byte-for-byte readback and V8 re-execution PASS. Different implementations use model-row versus model-column bit-matrix reductions, and the two local languages used independently written source generation.

Published executable: experiments/arc/lspv1_474_quadratic_span.cjs. Raw: results/raw/arc/2026-11-07_LSPV1_474_QUADRATIC_PEELING_RAW.json. Standalone local producer and Python checker are supplied separately in the reproducibility archive. The historical R_mix341 byte checker and native FLMV machine were NOT executed.

## Fully charged resource qualification

The ideal proof conclusion only counts source support; inference-node and evidence-bit lower bounds require the historically authenticated fan-in/weights and representation rules. Exact width-three signed CNF sources use Theta(n log n) indexed bits. The symbolic induction uses one recursion per peeled clause; the code actually enumerates 2^n assignments for finite n<=6, scans clause sets, constructs Boolean evaluation matrices, performs bit elimination, rejects hostile controls, and allocates source/certificate/result buffers. Those finite brute-force costs are not polynomial-time SAT algorithms for all n. Measured local runs include parsing, source creation, enumeration, elimination, temporary arrays, output and interpreter overhead; remote GitHub reads/search/update and independent verification are additional real work, not counted in W_R. Separate work/span/schedule minima are not determined by this theorem. The original 473 arity-capacity warning remains: linear source support cannot by itself yield superpolynomial mixed work.

## Status, exact gap and coordination

**Advance:** Theorem 474.1 is a symbolic extension of 473 from affine degree<=1 to all multilinear Boolean polynomial identities of degree<=2, with independent row/column finite falsifiers and sharpened original-variable source-local control on published hard random 3-CNF. It is strictly stronger than [P2-B14] but yields only a linear source floor. **OPEN:** authenticate native [P2-D1]; find a genuinely superpolynomial global all-rule invariant [P2-B1]; prove noncircular same-R B3 [P2-B2]; resolve [P2-C3]. No existing R_mix341 grammar, weights, agent IDs, routes, schedules, enabled states or main.tex were changed. **P versus NP OPEN.**

## References

1. V. Chvátal and E. Szemerédi (1988), *Many Hard Examples for Resolution*, JACM 35(4):759–768, DOI 10.1145/48014.48016.
2. G. Carenini (2026), *Random 3-CNF formulas are hard for k-DNF resolution up to k=O(sqrt(log n))*, ECCC TR26-158, published August 30, 2026. Different proof calculus; no mixed transfer.
3. S. Ordyniak, D. Paulusma and S. Szeider (2013), *Satisfiability of Acyclic and Almost Acyclic CNF Formulas*, TCS, arXiv:1104.4279. Background on acyclicity, not authority for this theorem.
4. S. Gryaznov and N. Talebanfard (2024), *Bounded-Depth Frege Lower Bounds for Random 3-CNFs via Deterministic Restrictions*, arXiv:2403.02275. Distinct bounded-depth proof model.
