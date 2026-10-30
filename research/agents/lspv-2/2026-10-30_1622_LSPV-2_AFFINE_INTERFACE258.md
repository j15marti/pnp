# LSPV-2 AFFINE-INTERFACE258
October 30, 2026, 4:22 p.m. PDT (America/Los_Angeles).

**Status: KNOWN THEOREM TRANSFER, COMPUTATIONAL independent finite checks; independent mathematical referee pending. The arbitrary-A -> Phi(A) hereditary ARC contraction, P=NP and P!=NP remain OPEN.**

## Scope and provenance

This is a module of the single integrated adaptive parameterized residual-SAT / actual FLMV forbidden-region program, not an independent P versus NP route. Reviewed verified UNIVERSAL-PARAMETERIZED-FLMV-REDIRECT1, UNIVERSAL-PARAMETERIZED-FLMV-CONTRACT1, AFFINE-SMALLBIAS-DESCENT-GATE2 (restricted MCSP affine no-go only), CONSTRUCTION-STRENGTHEN17, ARC-LINEAR22-SATURATION1, root main.tex, AGENTS.md, CODEX.md, the repository pnp-research skill and coordination issue #3. Prior mathematical components: LSPV-2 AFFINE-GUARD257 (complete original-clause parity signatures), LSPV-2 INTERFACE-GUARD256 (same-boundary component DP), LSPV-3 FRONTIER-TWO-SWEEP259 (verified full-interface messages). Original primary literature: Laitinen, Junttila, Niemelä, arXiv:1207.0988 (complete DPLL/XOR); Soos, Enhanced Gaussian Elimination in DPLL-based SAT Solvers (2012); Dreier, Ordyniak, Szeider, JCSS 142 (2024) on depth backdoors; Fortnow, Lipton, van Melkebeek, Viglas, JACM 52(6) (2005), Theorem 5.7. Neither GE nor full-interface DP is new.

## Four falsifiers

1. **Scalar-component SAT is not global SAT**: (x) and (not x) are individually SAT but not jointly.
2. **Dropping the shared-private hypothesis breaks affine projection**: (p XOR x=0) and (p XOR x=1) each project to every value of x separately, but jointly are inconsistent. The controller must merge both rows in one private component.
3. **Affine-only classification is unsound**: two tested CNFs have identical complete source-extracted XOR constraints yet opposite SAT labels due to leftover ordinary clauses.
4. **Implicit boundary compression is not an ARC contraction**: retaining a small affine description of admissible boundary assignments does not create a physically smaller ordinary SAT child or supply arbitrary-A time/space bounds.

## Exact lemma

Let F be an ordered proper signed CNF with original clause indices. Only when every falsifying assignment of one parity occurs as an original width-2 or width-3 clause on identical variable support S, extract the equivalent equation XOR(S)=1-p, where p is the excluded assignment parity. Record every original source-clause parent.

Supply and verify boundary variables B. Compute private components P_i from the scopes of **all** original clauses and extracted rows after removing B, so no clause or equation touches two private components. Original clauses split into F_B (boundary-only) and F_i (boundary-plus-component). Authenticated affine rows split into E_B and E_i. Let Q_i(beta)=exists private P_i such that E_i(beta,P_i), computed by genuine GF(2) elimination of all private columns, and let Q(beta)=E_B(beta) AND all Q_i(beta). This is an affine system on B.

**Theorem (exact both-label criterion, proof checked for this restricted construction):**

SAT(F) iff there exists beta with Q(beta), F_B(beta), and SAT(F_i[beta]) for every component i.

If Q is inconsistent, source F is UNSAT. If Q has rank r and |B|=b, exactly 2^(b-r) common-boundary assignments satisfy Q; only these require original-clause component decisions. Each SAT component witness is joined on the SAME beta, then all original source clauses are checked. Each failed beta records an original boundary-clause contradiction or a complete source-clause UP-DPLL refutation for one component. All omitted beta are excluded by authenticated XOR-combination rows. No UNSAT cofactor is promoted to parent UNSAT without all beta being covered.

**Proof:** Full source sign patterns characterize exactly the forbidden assignments, so each extracted equation is logically equivalent to its source block. GE eliminates private columns without changing the existential projection of each affine subsystem. Disjointness of private variables permits conjunction of the existential projections. A source satisfying assignment restricts to a Q-admissible beta and satisfies every original component; conversely original-clause component witnesses for a common beta join into one satisfying source assignment. The affine boundary solution space has cardinality 2^(b-r) by rank-nullity. Inconsistent zero row has a source-equation XOR parent trace. This proves both directions.

Rows of width 1 and 2 produce certified original-variable implications. In the 14-variable bridge instance, a derived clause (not x1 OR x2) has an independently replayed **17-node ordinary resolution DAG**, rather than only a GF(2) assertion. Every source equation records actual original clause indices; every projected row records equation XOR provenance. Retained original-clause S/U and inversion controls are secondary adverse checks.

## Reproducible finite evidence

The complete producer and separate independent checker passed **29 same-source instances (17 SAT, 12 UNSAT)**. Adverse controls include 2-SAT, Horn, incomplete XOR, SAT and UNSAT parity bridges, source variable/polarity renamings, high-width easy sources and random proper 3CNF.

The independent checker, which does not import the producer, verified 86,798 coherent full assignments, 684 full XOR block truth-table tests, 1,548 exact private-existential boundary projections, 94 source-row provenance equalities, 102 resolution proof nodes, 16,896 implied-clause checks, 9,860 original clause-pair SS/SU/US/UU states and original S/U, global endpoints and flip trails.

A connected bridge source uses 14 variables, 12 source-authenticated three-variable XOR blocks and 50 original clauses. Its boundary has b=8 and projected rank r=6, leaving **4 of 256** common-boundary assignments. Two versions on the **same affine skeleton** have 2 source models (SAT) and 0 source models (UNSAT). A supplied 50-clause ordinary-CNF source UNSAT example is independently checked by enumeration and the boundary-refutation proof. The local source parity and ordinary resolution traces are included in the full archive.

Aggregate 29-control UP-DPLL searched-node counts: 93 baseline, 48 hybrid. Selected instrumented event counts: 10,471 baseline, 12,425 hybrid. Aggregate Python runtimes were approximately **0.01774 s baseline versus 0.03249 s hybrid**. Thus the hybrid reduced searched nodes but increased time and overall metered work. The raw ledger includes source scanning, parity recognition, full component discovery, row elimination and bitwidth charges, attempted boundaries, switching, final source verification, DPLL branching, proof tree and Python peak allocation. These are NOT native FLMV machine time-space bounds.

## ARC audit and next step

FLMV Theorem 5.7 is a simultaneous time-space exclusion for the same uniform deterministic random-access Turing-machine realization, not a bound on the number of failed leaves. The audited conditional ARC coefficients (alpha,gamma,lambda,sigma)=(11/10,3/5,1/2,1/2) have fixed point (6/5,1/2), lying strictly inside the project-audited FLMV box at c=241/200, d=11642479/23232400. But no uniform all-input arbitrary-A -> Phi(A) transformer is constructed. Here Gaussian elimination can cost polynomially more than the claimed N^1.1 local budget, the hybrid retains a 2^(b-r) fallback, and **no physical ordinary SAT child of length N^(1/2) is produced**. DELAY/COPY/RECOMP wrappers remain unresolved as a global contraction obligation. The affine MCSP no-go is restricted and has no unrestricted SAT-hardness implication.

**Next target:** Combine this exact rank quotient with LSPV-3's charged forward/reverse frontier DP and LSPV-2's guarded component-profile updates, measuring all acquisition and replay costs before considering a physical power-short ordinary child. No task identity, schedule, enabled state, or unauthorized manuscript region was changed.

**Reproducibility:** GitHub compact independently executable control at experiments/arc/2026-10-30_1622_LSPV2_AFFINE_INTERFACE258_compact.py; compact raw summary at results/raw/arc/2026-10-30_1622_LSPV2_AFFINE_INTERFACE258_summary.json. Complete Python producer, independent full verifier, 29-case JSON with source proof trees, four-page LaTeX/PDF report, .bib, SHA256 manifest: LSPV2_AFFINE_INTERFACE258_2026-10-30.zip, SHA256 7a6676e0e93fd8495985fcb4a86ba503ccf099b48fac017bb01828bea06f3c37. Repository full archive publication is pending if the connector cannot read the local container bytes.

END_OF_VERIFIED_REPORT::LSPV-2::AFFINE-INTERFACE258::P_VS_NP_OPEN
