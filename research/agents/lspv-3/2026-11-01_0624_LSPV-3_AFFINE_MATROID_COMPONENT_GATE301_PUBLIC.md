# LSPV-3 GATE301: Basis-invariant affine matroid components

**2026-11-01 06:24 PST. PROVED/EXACT restricted theorem (external referee pending), COMPUTATIONAL independent finite checks, P versus NP OPEN.**

## Precise target and newly tested obstruction

All *originals* are valid duplicate-free proper Döcker Monotone 3-SAT-(2,2), every clause with three distinct same-sign literals and each variable with exactly two positive and two negative occurrences; malformed strings are rejected. Following the verified 01:48 five-role handoff, the 01:44 saturated-cycle terminal, GATE297 affine projection and GATE300 acquired quotient-width DP, this run asks whether affine quotient-factor width is an invariant computational obstacle. It is not. A dense, invertible change of nullspace coordinates can make an easy factor family look high-width.

## Restricted exact theorem and proof

Let p be a coherent source-original variable assignment, with no falsified original clause. Authenticate an original-clause-edge-disjoint odd residual binary cycle family and δ=2f-u-η-ν=0. The previously proven saturated-cycle theorem represents the original-source SAT completions as an affine exterior GF(2) solution set E intersect the selected original cycle clauses. If E is consistent, put x=x0+Bz, z in GF(2)^d, d=f-rank(E). Substitute in each selected source cycle clause. Remove constant-TRUE literals/clauses and constant-FALSE literals, and collect nonzero affine literal linear forms Λ in the d coordinates. Let h=rank(span Λ).

Form the binary representable vector matroid of these linear forms. Union forms lying in a common matroid circuit and further union forms occurring in the same remaining original cycle clause. Let W1,...,Wc be the resulting independent direct-sum subspaces with dimensions h1,...,hc and let Mi be the number of basis evaluations in Wi satisfying all cycle clauses assigned to that component. Then

```
#SAT(F extending p) = 2^(d-h) * product_i Mi.
```

Proof: vector-matroid circuit connectivity produces the finest direct-sum decomposition of the declared forms. Clause merging preserves direct-sum independence, and every selected clause depends on a single block. Independent basis evaluations can be combined uniquely, and every assigned evaluation of the h-dimensional form span has exactly 2^(d-h) lifts in E by rank-nullity. The authenticated delta-zero saturated-cycle theorem verifies that E together with cycle clauses is exactly the original-source completion set. Thus the factor count is exact, including zero and nonzero cases. The multiset of block dimensions is invariant under any invertible coordinate change; the chosen bases need not be. Nonlinear semantic simplification could yield a finer decomposition, so this theorem is NOT optimal-computational-cost or universal-hardness assertion.

Acquisition: Gaussian elimination and fundamental-circuit dependence enumeration plus clause-scope disjoint-set unions are deterministic polynomial time in the explicit source length. Exhaustive component evaluation costs poly(N)*(1+sum_i 2^h_i), plus paid acquisition, witness lifting and full original-clause checking. The certified terminal is polynomial when the **acquired** max_i h_i=O(log N); otherwise a bounded attempt returns UNRESOLVED and the exact controller retains its sound fallback. No arbitrary-A->Phi(A) or all-input polynomial guarantee.

## Three decisive falsifiers

F1, FALSE: connected source incidence forces one affine component. Take the valid canonical Y6 positive supports {123,145,246,356}, negative supports {124,136,235,456} with x2=0,x3=1,x5=0. It has δ=0, one authenticated odd cycle, exterior x4=1, and exactly 3 completions satisfying NOT(x1 AND x6). Join r copies through swaps of pinned-false negative occurrences in already-covered source clauses. The resulting original canonical source is connected with n=6r, m=8r, ν=r, h=d=2r, r independent affine form components of dimension two, and exactly 3^r residual models.

F2, FALSE: raw primal quotient-factor width measures invariant hardness. In 2r affine coordinates let z=(I+J)t, where J is all-ones. Since 2r is even, (I+J)^2=I over GF(2). Each old coordinate z_i becomes XOR of every new coordinate but t_i. The two-coordinate nonlinear clause for each copy now mentions **all** 2r new coordinates, yielding raw factor primal width 2r-1, while the acquired form-matroid decomposition still consists of r two-dimensional independent blocks. Full 2^(2r) projection enumeration is replaced by 4r component candidates, with paid polynomial acquisition; this family is EASY, not a SAT lower-bound family.

F3, FALSE: outside-cycle parity consistency is enough for SAT. The authentic valid F9 original has 70 root models, but its six-pin δ=0 cube has eight completions and none satisfy all original cycle clauses. Its exterior affine system is consistent; the exact component terminal correctly returns UNSAT and independent exhaustive checking agrees.

r | source n | cycles | projected points | cycle edge tickets | component candidates | exact cube models
---|---:|---:|---:|---:|---:|---:
1 | 6 | 1 | 4 | 3 | 4 | 3
2 | 12 | 2 | 16 | 9 | 8 | 9
4 | 24 | 4 | 256 | 81 | 16 | 81
8 | 48 | 8 | 65,536 | 6,561 | 32 | 6,561
12 | 72 | 12 | 16,777,216 | 531,441 | 48 | 531,441

These are candidate counts for different policies, NOT native time measures. For the r=12 SAT residual, UP-first DPLL used 25 nodes, 2,952 clause scans and 5,550 literal tests. The new policy made 7,140 triangle candidate checks, 576 grammar/residual literal reads, and further GF(2), matroid and verification work. No end-to-end speed dominance is claimed.

## Independent verification, inherited proof controls, ledger

A no-producer-import independent verifier passed: 4,680 fully evaluated pinned original assignments across r=1..4; 376 original-source SS/SU/US/UU clause-pair modes; 60 original signed occurrence S/U targets and inversions; 64 original complement-histogram identities; 388 change-of-basis Boolean checks; six malformed rejects; and 30 component/rank crosschecks. Authenticated U198 UNSAT modular proof replay checked all 64 boundary cases and 3,666 local refutation nodes; V198's 198-bit witness satisfied all 264 original clauses. The restricted new policy did NOT solve those large roots. Full original-indexed status/extreme records, flip trails and offline logical XOR are in the complete archive.

Charged in experimental proxies: grammar/source scans, cycle discovery, GE row operations, nullspace basis, fundamental circuits, factor scope discovery, failed candidate evaluations, witness checks and DPLL baseline. NOT CHARGED/NOT PROVED in the FLMV native indexed-TM model: addressed original/child bit access, output, tape-head movement, physical XOR, all guest A calls, ancestor retention and simultaneous peak writable/index space. Noncanonical residual children are not a hereditary power-short canonical M22 transformer. DELAY/COPY/RECOMP and unknown K,L remain hostile controls. Numerical FLMV transfer also needs a fully charged model-compatible reduction or direct applicable theorem; NP-completeness alone cannot provide it. P=NP and P!=NP remain OPEN.

## Searches, provenance, and next theorem arrow

Verified project preflight: root AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, main.tex, REDIRECT1, CONTRACT1, signed saturation theorem, GATE297, GATE299/300, and issue #3. Web searches for Döcker 1912.08032, FLMV JACM 2005, Darwiche/Marquis knowledge compilation and affine model counting. Separate Github searches: j15marti/pnp `affine projection`, `factor graph`, `saturated cycle`; openai/math `Gaussian elimination`, `SAT XOR`; msoos/cryptominisat `xor clause components`. Primary references: https://arxiv.org/abs/1912.08032 ; https://doi.org/10.1145/1101821.1101822 ; https://doi.org/10.1613/JAIR.989 ; https://ijcai.org/proceedings/2024/367 . Matroid decomposition, affine elimination and decomposable model counting are known method families: no novelty claim about their general techniques. GitHub connector read access worked; local container DNS and Library upload-back failed.

Full Python producer, no-import verifier, source-indexed controls, original U198/V198 proof fixtures, raw JSON, and SHA256 integrity manifest are in the separate GATE301 reproducibility archive. The public `compact301.py` reproduces the connected-source and dense-basis falsifiers (not the full solver). Next: acquire matroid components without a dense kernel basis and compare the paid selector on hostile truly hard connected sources; main arbitrary-A->Phi(A) hereditary canonical ARC/FLMV arrow remains OPEN.

`END_OF_VERIFIED_REPORT::LSPV-3::AFFINE_MATROID_COMPONENT_GATE301::P_VS_NP_OPEN`
