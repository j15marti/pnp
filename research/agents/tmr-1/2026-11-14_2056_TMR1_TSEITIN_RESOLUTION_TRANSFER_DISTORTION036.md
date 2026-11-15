# TMR-1/036: Exponential distortion of a SAT-machine-to-Resolution transfer on explicit cubic Tseitin expanders

**2026-11-14 20:56 PST | TSEITIN-TRANSFER-GATE058 | PNP Machine Model Lead**

**Scientific status:** PROVED/RESTRICTED conditional only on the cited *established* expander construction and Resolution size theorem. This is a **no-go theorem for a model-changing simulation**, not a new SAT lower bound and not a claim of originality for the old expander or parity results. Native small-instance experiments are **COMPUTATIONAL**. Independent TMR-5/TMR-4 review OPEN. **P versus NP OPEN.**

## 1. Candidate and fixed falsifiers before source search

**Candidate:** A universal, initial-and-goal-preserving, all-transition cost-underestimating simulator from an arbitrary correct deterministic SAT machine to the native, SOURCE/RESOLVE-only Resolution calculus Q-RES-H cannot exist, even when restricted to a deterministic polynomial-time constructible family of ordinary proper 3-CNF instances. In fact a simulation must incur exponential cost distortion on a particular correct total SAT machine.

Falsifiers: (1) the expander source is not an authenticated proper 3-CNF; (2) the claimed exponential proof size uses a stronger or different proof calculus than native shared-DAG Resolution; (3) the purported fast algorithm assumes free graph/charge metadata, misclassifies even-charge or disconnected controls, or fails on malformed/off-family inputs; (4) extensions, GF(2), cached shared intermediate relations, or zero-cost macro rules are smuggled into the allegedly Resolution-only output. All four are explicitly controlled or declared model changes below.

**What is new relative to the project corpus:** Previous LSPV-2/422, LSPV-4/423 and MAIN/REFEREE367 already recorded expander Tseitin Resolution hardness, polynomial algebraic recognition, and a restricted branch-calculus-to-Resolution equivalence. TMR-1/035 already demonstrated cheap-prefix/fallback grafts and terminal masking. This run does **not** claim those facts are new. The present additional contribution is an **explicit quantitative lower bound on the blowup of any whole-trace SAT-machine-to-native-Resolution cost simulation**, including an all-length total decider, fully source-parsed two-label recognition, and a formal counterexample to an alleged all-step no-greater-cost simulation. This sharpens the independent same-system transfer ledger; it does not repair the OPEN transfer to an unrestricted calculus.

## 2. Exact primary-source theorem ledger

| Original theorem | Exact statement used, model and qualification |
|---|---|
| Ben-Sasson and Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, JACM 48(2), 2001, **Definition 4.1, Lemma 4.2, Theorem 4.4, Corollary 4.5**, printed pp.155-156; **Corollary 3.6**, p.155; https://doi.org/10.1145/375827.375835 ; author-readable https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf | For connected 3-regular graph G of H vertices with linear edge expansion and odd vertex charge, the authentic 3-CNF Tseitin contradiction has 4H initial width-three clauses and 3H/2 edge variables. Every **ordinary, shared-DAG propositional Resolution** refutation has size at least 2^(aH) for some expansion-dependent a>0 (for sufficiently large H). Proof size counts derived lines, not general SAT-machine steps or stronger algebraic rules. |
| Mohanty, O'Donnell and Paredes, *Explicit Near-Ramanujan Graphs of Every Degree*, SIAM J. Comput. 51(3), 2022, abstract and existence theorem; https://doi.org/10.1137/20M1342112 | For every constant degree d>=3 and eps>0 there is a **uniform deterministic polynomial-time** generator outputting a d-regular graph on Theta(n) vertices with nontrivial eigenvalues bounded in absolute value by 2 sqrt(d-1)+eps. Choose d=3, eps=1/20, giving <3 and a fixed positive spectral gap, hence constant edge expansion. No advice or nonuniform graph table is needed. |
| Original project evidence: LSPV-2/422, LSPV-4/423, MAIN/REFEREE367, TMR-1/035, TMR-2/035, TMR-4/036, TMR-5/032 | Restricted prior results and hostile controls only. None establishes a universal all-transition cost-respecting SAT-machine-to-native-Resolution map. /341 FAIL as full logical authority; /386 RESTRICTED and not substituted. |

**Source measures:** H=|V(G)|; e=3H/2 Boolean variables; 4H exact proper ternary clauses; L=Theta(H log(H+2)) bits under an explicit signed-binary literal-index encoding. The graph-generator input parameter is **not** SAT length L, and H is not MCSP truth-table length N=2^n.

## 3. Fully qualified systems and explicit growing family

**Q-TM (qualified physical model):** One fixed finite total deterministic multitape machine with a read-only authenticated binary input tape, finitely many finite-alphabet work tapes, full control and head positions, complete writable workspace, output label, and every actual transition of unit cost, including parsing, indexing, input rereading, Gaussian computation, reencoding and fallback. The only zero-cost edges in the *physical* machine are mathematical identities; no free oracle, answer table, or free source acquisition. Every valid SAT instance receives a correct SAT/UNSAT label; malformed encodings are rejected by the input grammar.

**Q-RES-H (qualified and RESTRICTED source-bound proof model):** State records exact source CNF and all authenticated SOURCE clause IDs, shared derived clauses and parent pointers, globally paid derivation identities, assumptions and active obligations, and terminal empty-clause status. Authentic SOURCE references and existing-node reuse cost zero *native inference units*, RESOLVE pays one per newly derived binary resolvent, and zero-cost HALT_UNSAT is permitted only after deriving the empty clause. Neither arbitrary GF(2) row addition nor extension/learning macros are rules here. This Q-RES-H is ordinary Resolution in paid-inference size, NOT a standalone complete both-label SAT machine. Comparing Q-TM physical transitions with Q-RES-H native inferences requires a **new sound transfer theorem**, which is precisely what is falsified for a too-strong form.

**Explicit family:** For the deterministic degree-3 expander G_m output by the cited graph generator, let H_m=|V(G_m)| and select the lexicographically first vertex v0. Set charge b(v0)=1 and b(v)=0 otherwise. Introduce one Boolean x_e for each edge. At each vertex with incident edges e1,e2,e3, impose x_e1 XOR x_e2 XOR x_e3=b(v) using exactly the four proper width-three CNF clauses forbidding the wrong parity. Let F_m be their conjunction in canonically sorted clause/literal order. Then F_m is UNSAT by XORing all vertex equations, since each edge occurs exactly twice yet the right-hand side XOR equals one. H_m=Theta(m), L_m=Theta(H_m log H_m), and the generator and CNF encoder are polynomial-time uniform.

By the quoted Corollary 4.5 and the 4H source-clause count, the minimum number of **new paid RESOLVE inferences** is

$$
\overline W_{\rm QRES}(F_m)\ \ge\ 2^{\Omega(H_m)}-4H_m\ =\ 2^{\Omega(L_m/\log L_m)}.
$$

Subtracting source lines is necessary because native SOURCE is priced zero; the exponential lower bound survives.

## 4. Explicit correct fixed all-length machine with a fast path on the hard-Resolution family

Construct one fixed total deterministic machine A_XOR. It parses the *entire original formula bytes*, with no trusted Tseitin annotation or preloaded graph. Group clauses by their exact sets of three distinct variable IDs. Accept the special form only if each group consists of exactly the four different clauses defining one of the two parity relations, each variable appears in precisely two distinct groups, and no additional source clause exists. Interpret groups as graph vertices, variables as edges and group parity as vertex charges. Test connected components, XOR charges inside **each** component, and output SAT iff all components have even charge. If any syntax or incidence check fails, use exhaustive search on the original CNF; this fallback makes A_XOR a correct, fixed, total decider on all lengths, including both ordinary SAT and UNSAT labels. Charge its parsing, data structures, graph search and fallback in the ordinary Q-TM model. All of the fast-path computations admit ordinary deterministic multitape implementations in L^c steps for some fixed finite c, without an unbounded-word primitive.

**Correctness of the fast path:** Each authenticated 4-clause triple is equivalent to its stated GF(2) vertex equation. The edge-incidence matrix of each connected undirected graph over GF(2) has column space exactly the even-parity vectors. Thus the system is solvable iff the XOR of charges of each connected component is zero. On F_m the charge is odd, so A_XOR rejects correctly after polynomial work. The same source parser accepts the even-charge controls and returns SAT, and it catches two disjoint odd components even though their aggregate global charge is even.

Consequently, for some fixed c,

$$
T_{A_{\oplus}}(F_m) \le L_m^{c}
\qquad\text{for all sufficiently large }m,
$$

where A_XOR is **one fixed total all-input correct SAT decider** and is permitted exponential runtime off this family. This is an unconditional easy-family statement, **not** SAT in P.

The authenticated algebraic contradiction can also be derived by H_m-1 row-XOR operations; storing and updating length-O(H_m) incidence rows costs at most polynomial bit work. This is a **different proof system** and must not be assigned zero Q-RES-H inference cost.

## 5. NEW TSEITIN-TRANSFER-GATE058 quantitative simulation obstruction

**Theorem (PROVED/RESTRICTED, based on original primary theorem).** Suppose for each m a compiler maps the entire terminating concrete Q-TM execution of A_XOR on F_m to a correct, source-bound Q-RES-H derivation of the empty clause from precisely F_m, retaining all original source bindings, shared identities and required goals. Suppose the paid Q-RES-H work of the output is at most

$$
g(L_m)\,T_{A_\oplus}(F_m)+b(L_m)
$$

for nonnegative functions g,b, and b(L) is bounded by a fixed polynomial. Then, for all sufficiently large m,

$$
\boxed{\quad g(L_m)\ge 2^{\Omega(L_m/\log L_m)}.\quad}
$$

In particular no **polynomial-distortion**, nor **cost-underestimating all-step**, initial/terminal-preserving Q-TM-to-Q-RES-H simulation exists for every correct SAT decider.

**Proof.** By source authentication and terminal preservation, the compiler's output is an actual ordinary Resolution refutation of F_m, not a formula in a stronger system or an unverified bitstring. The cited width/size lower bound gives at least 2^(aH_m)-4H_m paid RESOLVE nodes. The assumed compiler cost gives at most g(L_m)L_m^c+b(L_m). Because L_m=Theta(H_m log H_m), and any fixed polynomial b is negligible relative to 2^(aH_m), rearrangement forces g(L_m)>=2^(Omega(L_m/log L_m)). For an all-step simulator that maps each physical transition to a finite abstract Resolution path of cost at most its physical one-step increment, telescope the paths, deduplicate shared paid lines and use zero-cost terminal preservation to obtain g=1,b=0, contradicting the bound. QED.

**Quantifier warning:** This disproves the proposed **universal simulation to this restricted R**. It does NOT disprove the existence of some other stronger, sound and complete R with a polynomial SAT-to-R transfer, nor provide a lower bound on arbitrary Q-TM SAT deciders. If SAT were in P, this restricted Resolution family would remain hard; a decider does not inherently output a Resolution refutation. No claim is made about /341 or /386 native mixed proof systems.

## 6. Connection to fusion-Lipschitz tariff program

Any proposed fusion initial obstruction p(F_m) inherited from native Resolution size, used as a universal Q-TM runtime lower bound, fails the **same-system all-step transfer gate** on A_XOR. The failure is not an omitted zero-cost SCC or a defect fixable by CEGAR: the cheap algorithm is genuine and its parity operations are authentic Q-TM steps. The R-only tariff may be perfectly sound within Q-RES-H, but its initial bound cannot be imported into arbitrary SAT-machine work.

A repaired candidate must either (i) define obstructions directly on complete **Q-TM configurations** and prove a step tariff for every possible transition, or (ii) qualify a stronger source-bound proof calculus with authenticated, paid affine/Gaussian/extension/learning/branch/sharing operations, prove a new lower bound **for that same calculus**, and then independently prove a total both-label machine-to-calculus transfer. The known Resolution expander lower bound is inapplicable after arbitrary strengthening; odd-charge Tseitin becomes polynomial there.

**Dependency map:**
- PASS, RESTRICTED: deterministic uniform 3-regular expander existence and exact 3-CNF Tseitin encoding, published Resolution hardness.
- PASS, RESTRICTED: one fixed total all-input correct SAT decider with polynomial runtime on this recognized family.
- FAIL: universal Q-TM-to-ordinary-Resolution trace simulation with polynomial or lower cost.
- OPEN: any authentic dynamic SAT fusion measure, complete rule inventory, full machine cost-sound potential, superpolynomial all-decider initial gap, or same-system transfer for a genuinely stronger calculus.
- RETAIN: /341 FAIL logical authority, /386 RESTRICTED guarded system. They are not silently repaired or substituted.

**Weakest next lemma / peer request:** TMR-4 and TMR-5 should independently verify the lower bound on distortion and the source-parser correctness. TMR-3 should audit authentic Gaussian elimination's *bit-level* cost, not one-cost semantic XOR. TMR-2 should define one residual component that becomes small on this source-recognizable affine family while retaining a nontrivial tariff on genuinely hard CNF families, and test the strongest compact sharing/fusion rules.

## 7. Computation, provenance and preflight

**Original native CPython actually executed** at /mnt/data/tmr1_tseitin_transfer_gate058.py using independent source parser and symbolic XOR; saved raw stdout at /mnt/data/tmr1_tseitin_transfer_gate058_raw.json. It passed **121 assertion groups, zero failures**, including even/odd K4, K3,3, cube and prism formulas; 40 renamings/reshufflings, 10 missing-clause malformed controls, 10 exhaustive truth-assignment tests, and a two-disconnected-odd-component control. These finite results are COMPUTATIONAL, not verification of the asymptotic theorem. Published **self-contained clean reconstruction** at experiments/tmr/tmr1_tseitin_transfer_gate058.py was **not natively rerun byte for byte**. A provenance file records the original SHA256 and this identity limitation; raw JSON is a faithful compact transcription, not represented as byte-identical capture.

Source: experiments/tmr/tmr1_tseitin_transfer_gate058.py
Raw summary: results/raw/tmr/2026-11-14_2056_TMR1_TSEITIN_TRANSFER058_NATIVE_RAW.json
Provenance: results/raw/tmr/2026-11-14_2056_TMR1_TSEITIN_TRANSFER058_PROVENANCE.json

Controlling directive read FIRST, blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6; Nov13 replacement; root proof1 complete SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; root proof2 authentic recovered blob 930c5eeddafce656717f28055a7a9a755f44737c of 1,051,196 chars; root main.tex authentic recovered blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 of 2,545,859 chars; AGENTS/CODEX/pnp-research skill; all five current TMR handoffs; latest issue #3; original LEAD-0029, LSPV-2/422, LSPV-4/423, MAIN/REFEREE367, TMR-1/035, TMR-4/036, TMR-5/032 inspected. No changes to any task, schedule or proof authority.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex unchanged pending independent TMR-5 review. Unrestricted P versus NP and every load-bearing all-machine arrow remain OPEN.

END_OF_REPORT::TMR1::036::2026-11-14_2056_PST
