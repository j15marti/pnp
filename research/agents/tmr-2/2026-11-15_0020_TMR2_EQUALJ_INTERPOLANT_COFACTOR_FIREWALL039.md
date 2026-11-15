# TMR-2/039: Exponential local interface cofactors and native Resolution hardness coexist with a linear-size interpolant

**2026-11-15 00:20 PST | EQUALJ072 | PNP Information Necessity**

**Status:** PROVED/RESTRICTED for the exact Boolean, restriction, and native Resolution statements; independent mathematical review OPEN. Executed finite tests COMPUTATIONAL. Arbitrary fixed deterministic SAT-machine lower bound, superpolynomial fusion-safe potential, and P versus NP OPEN.

## 1. Candidate and preselected falsifiers

**Candidate under test.** Strengthen the earlier TMR-2/038 local-interface proposal by combining exponential *locally authenticated* Boolean cofactors, semantic non-Schaefer behavior, and a source whose ordinary Resolution refutations are exponentially large. Test whether these properties force a hard shared-variable Craig interpolant or an admissible positive per-cofactor tariff.

Falsifiers stated before searching sources: (F1) exponentially distinct residuals may admit a small *shared* equality/comparison circuit; (F2) a cheap Gaussian/XOR or preprocessing mechanism may recognize unsatisfiability without exploring the residuals; (F3) the guarding transformation may fail to preserve source Resolution hardness under a legal restriction; (F4) complement encoding with private extension variables may inadvertently change the projected B relation, invalidating the unique interpolant. F1 and F2 are realized. F3 and F4 are ruled out for this exact construction by proof and finite tests.

## 2. A completely specified shared interface

Take any unsatisfiable CNF `F(U)` on private variables `U`. For k>=2, let `X=(x_1,...,x_k)`, `Y=(y_1,...,y_k)`, and `Z=(z_1,z_2,z_3)` be disjoint shared variables, and let

$$
I_k(X,Y,Z)=\left(\bigwedge_{i=1}^{k}(x_i\leftrightarrow y_i)\right)\land J_3(Z),
\qquad J_3(Z)\equiv (z_1\vee z_2\vee z_3)\land\bigwedge_{i<j}(\neg z_i\vee\neg z_j).
$$

Its literal CNF `D_k` contains `q_k=2k+4` clauses: two binary equality implications per coordinate, one ternary at-least-one clause, and three negative binary at-most-one clauses. Write each clause as `D`. Define

$$
A_{F,k}(X,Y,Z,U)=\bigwedge_{D\in D_k}\bigwedge_{C\in F}(D\vee C).
$$

On the B side, construct a *separate private* fan-in-two gate circuit for `NOT I_k`: compute `v_D=AND_{\ell\in D}(NOT \ell)` and `v=OR_{D\in D_k}v_D`. Translate each AND/OR gate into its standard three clauses of width at most three enforcing exact equivalence, and add the output unit `v`. Call that explicit CNF `B_k(X,Y,Z,V)`, where `V` consists entirely of B-private gate outputs. It has O(k) gates, clauses and variables; the constraints uniquely determine the gate values given the common inputs. The complete source is `G_{F,k}=A_{F,k} AND B_k`. Neither source asserts proper three-CNF globally: A clauses may have width up to six when F is three-CNF. B itself has width <=3. All source bytes, gate definitions, private variables and accepted interfaces must be charged in a physical model.

## 3. Exact theorem EQUALJ072 (restricted, mathematical proof)

For every unsatisfiable F and k>=2:

**(a) Exact projections and unique interpolant.** For every D, by distributivity,
$$
\bigwedge_{C\in F}(D\vee C)\equiv D\vee F\equiv D.
$$
Thus `A` is equivalent to `I_k` as a full Boolean function, including all U assignments. The B gate equivalences force a unique extension V and project to `NOT I_k`. Both A and B separately have models, while G is UNSAT. Since the shared projections are complementary, any Craig interpolant separating them is exactly `I_k`. An explicit fan-in-two circuit evaluates the k equality comparisons and the fixed J_3 test with **O(k)** gates, even when the source F is Resolution-hard.

**(b) Exponential *nonzero* local cofactor diversity.** For every assignment `a in {0,1}^k` to X, the residual interface relation `R_a(Y,Z)=I_k(a,Y,Z)` is nonzero (choose Y=a and Z=(1,0,0)). For distinct a,b, these relations differ at the common witness (Y=a,Z=(1,0,0)), since R_a=1 and R_b=0. Hence

$$
\left|\{R_a:a\in\{0,1\}^k\}\right|=2^k,\qquad p_{\rm local}=2^k-1.
$$

This is *not* the full unsatisfiable G satisfaction relation, which is identically zero. It is a local authenticated A/B shared-interface projection before the final AND join. In particular p_local stays exponentially large even though the **same** interpolant has a linear-size shared circuit. The J_3 factor makes the interface semantically non-Horn, non-dual-Horn, non-bijunctive and non-affine: fixing X=Y=0 reduces to J_3, whose closure under AND, OR, majority and three-way XOR is violated by one-hot Z assignments.

**(c) Native Resolution lower-bound inheritance.** Let S_RES count derived non-weakening Resolution inferences in one shared source-authenticated DAG, and give source clauses zero inference cost. Then

$$
\boxed{S_{\rm RES}(G_{F,k})\ge S_{\rm RES}(F).}
$$

Fix X all zero, Y=(1,0,...,0), Z=(1,0,0); assign every private B gate its forced value on this shared input. Exactly one guard in D_k is false, namely `(x_1 OR NOT y_1)`; the other guards are true. B is fully satisfied. The restricted source is precisely F (up to discarded true clauses). Restriction of a Resolution refutation yields a refutation with no more inferences, after deleting degenerate lines. This does **not** assert a lower bound for any other proof calculus or arbitrary SAT algorithm.

**(d) Optional hard-source amplification with exact measures.** Select F_H as odd-charge cubic-graph Tseitin three-CNF on any fixed bounded-degree 3-regular expander sequence with H vertices, four width-three clauses per vertex and O(H) private variables. The Ben-Sasson--Wigderson width/size method, Theorem 4.1 and Corollary 4.1 on printed p.10 in ECCC TR99-022, gives `S_RES(F_H)=2^{Omega(H)}` for constant-degree expansion. With k=H, the guarded source has `(2H+4)4H=Theta(H^2)` A clauses of width <=6 and O(H) B clauses. Under ordinary binary variable-ID/sign encoding its length is

$$
L_H=\Theta(H^2\log H).
$$

Therefore `S_RES(G_{F_H,H}) >= 2^{Omega(H)} = 2^{Omega(sqrt(L_H/log L_H))}`, **in ordinary native Resolution only**. The unique interpolant still has O(H) Boolean circuit size and 2^H distinct local X cofactors. This is a conditional use of the published expander-Tseitin lower bound, not a newly proven unrestricted lower bound.

## 4. Genuine cheap execution and tariff consequence

There is a fixed total correct deterministic SAT algorithm that first authenticates the guarded CNF recipe, including literal order/IDs, the full four-clause parity-block pattern for an embedded three-variable XOR system, a verifiable odd-sum/even-incidence XOR contradiction, and every B gate-definition clause. On inputs passing authentication, it rejects because the authenticated private F is UNSAT. On all other inputs it falls back to exhaustive SAT search. Its accepted fast path is polynomial in the **entire encoded source length** L (a deliberately conservative L^O(1) bound for finite-alphabet parsing, comparisons and Gaussian parity checks); all formula bytes, definitions and rereads are charged. Uniform construction does not require deciding graph expansion, and malformed cases go to the total fallback.

The known binary parity-block family passes this sound recognizer; in particular the hard-source expander instances do. This is an **algorithm-specific polynomial fast family**, not a general polynomial SAT solver. It demonstrates that even native Resolution hardness plus an exponentially diverse non-Schaefer interface does not force a large *physical-machine* cost on that family.

In the native deterministic SAT-machine transition system all steps cost one and zero-cost closure is identity. Suppose a nonnegative terminal-zero all-step tariff `Phi` starts with a fixed positive coefficient `lambda_local` on `p_local=2^k-1` (with other initial components nonnegative). Telescoping on the fast path yields the necessary condition

$$
\lambda_{\rm local}(2^k-1)\le W_A(G_{F_k,k})\le (L_k+1)^c
$$

for some fixed c and constant factor, hence **no k-independent positive lambda_local** is sound across this family. This argument does not depend on whether the overdischarge happens at the final halt or earlier. A dynamically recomputed genuine cost-to-go may be 1-Lipschitz, but cannot retain the exponential initial value on these fast executions. A source-only Resolution potential is different and still requires an independent same-system bridge.

## 5. Mandatory hostile controls and scope

- **Gaussian/affine:** private F is recognized as contradictory parity equations, solved polynomially without enumerating 2^k cofactors. A symbolic shared equality circuit of O(k) gates also computes I_k.
- **Horn, dual-Horn, Krom, Schaefer:** the interface includes exact-one-three, violating all four semantic preservation criteria despite containing binary equality clauses. Non-Schaefer is not computational hardness.
- **Treewidth/separators:** splitting the comparison at X,Y exposes 2^k distinct residuals but an O(k)-gate circuit; bounded-treewidth dynamic programming or another shared representation is legal.
- **Autarkies, equality/union-find:** equality rows are an explicit cheap mechanism; any quotient treating them as separate expensive residual obligations is falsified. No speculative autarky removal is needed for this counterexample.
- **Extensions, learning, preprocessing and sharing:** B uses authentic private extension gates, whose exact CNF is checked. A/B common computation is shared, not duplicated per X-cofactor; learning and preprocessing may find cheaper paths and cannot be suppressed.
- **Padding, renaming, source rereads, caching and recomputation:** no inference from expanded syntax or arbitrary assignment count to machine time; the upper algorithm reads and checks the full finite source. Duplicated/source-padding and alternate identifier encodings are not lower-bound evidence.
- **Historical verifier:** `/341` remains FAIL as general logical UNSAT authority, `/386` remains RESTRICTED; neither is used to authenticate this construction.

## 6. Executed tests and reproducibility

The exact ES2020 function in `experiments/tmr/tmr2_equalj_guard_cofactor072.js` was executed natively in V8; **92,807 assertions, zero failures**. For k=2,...,6 it checked q_k, guard-source clause counts, B Tseitin width and linear gate counts, full B complement extension over all 2^(2k+3) shared assignments, exact projected A and joint UNSAT over all private assignments through k=4, corrupted-gate rejection for k<=3, all 4^k cofactor distinguishing pairs, and a full source restriction leaving precisely the eight-clause private contradiction. The eight-clause laboratory F is the conjunction of opposite three-variable parity constraints; these finite tests do **not** execute the large expander Resolution lower bound or a compiled native Turing machine.

Executable: `experiments/tmr/tmr2_equalj_guard_cofactor072.js`. Original raw stdout: `results/raw/tmr/2026-11-15_0020_TMR2_EQUALJ072_V8_RAW.json`. The published JS function is serialized from the **same executed** function and is Node-runnable; independent rerun from GitHub is requested.

## 7. Prior-work ledger, primary-source scope and next exact target

| Source | Status relevant here |
| --- | --- |
| `research/agents/tmr-2/2026-11-14_2321_TMR2_NONAFFINE_COFSEP_AUTARKY_FIREWALL038.md` | PROVED/RESTRICTED, exhibited **global** cofactor mass on an easy SAT family and noted global-UNSAT triviality. This report instead treats complementary local projections of an actual UNSAT conjunction. |
| `research/agents/tmr-1/2026-11-15_0004_TMR1_EXACTONE_NON_SCHAEFER_GUARDLIFT039.md` | PROVED/RESTRICTED, hard private Resolution source with O(k^2) exact-one interpolant. New here: 2^k **nonzero distinct local cofactors**, exact B-private linear gate encoding, simultaneous non-Schaefer and hard-source controls, and the polynomial-time authenticator bypass. |
| Ben-Sasson and Wigderson, *Short Proofs are Narrow*, ECCC TR99-022 (June 1999), Theorem 4.1 and Corollary 4.1, printed p.10; https://eccc.weizmann.ac.il/report/1999/022/download/ | KNOWN restricted Resolution expander-Tseitin theorem, original page checked by screenshot. No claim about arbitrary deterministic machines or stronger proof systems. |
| Krajicek, *Interpolation theorems, lower bounds for proof systems...*, J. Symbolic Logic 1997, abstract at https://doi.org/10.2307/2275575 | Feasible interpolation background only; **no external theorem is needed** for uniqueness/linear circuit, both proved directly. |
| TMR-3/038 MACROINGRESS067, TMR-4/039 MODEJOIN067, TMR-5/035 MODEALT068 | All restricted: authenticated XOR/macro and mode-sharing shortcuts reinforce that selected proof formats do not lower-bound actual SAT-machine time. |

**New relative to prior work:** the simultaneous triple `2^k nonzero local interface cofactors + native Resolution-exponential private source + O(k) unique non-Schaefer interpolant` and the explicit sound polynomial recognizer show the local-interface salvage from TMR-2/038 still lacks a fusion-safe tariff. This is a new counterexample construction, **not** an independent proof of native source hardness.

**Peer requests:** TMR-1 check guard restriction, separate projected languages, and exact shared-variable interpolant; TMR-3 charge the fixed parity-source authenticator on actual finite-alphabet tapes; TMR-4 insert the O(k) comparator and full authenticated B extensions into all-step MAY/zero-closure tariff rows; TMR-5 independently replay k=2..6 and challenge the hard-source restriction plus expander input-length conversion.

**Weakest remaining lemma:** a *dynamically state-dependent*, AND-aware and source-authenticated fusion component whose per-step discharge survives arbitrary compact circuits, algebra, learning, and shared recomputation, together with a **same-system** link to every correct deterministic SAT decider. Neither this construction nor any cofactor count supplies it. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root `main.tex` not modified. P versus NP OPEN.
