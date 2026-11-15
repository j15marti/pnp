# TMR-5/037: NAE rank and authenticated circuit-guard composition

**Run start:** 2026-11-15 01:43 PST, America/Los_Angeles. **Governing directive:** research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md, blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6.

**Verdict:** PROVED/RESTRICTED symbolic composition, independent peer review OPEN. Original finite V8 replay is COMPUTATIONAL. No P versus NP conclusion. No change to proof trackers, canonical main.tex, or scheduled agents.

## 1. Claim and falsifiers fixed before literature and corpus audit

**Candidate:** The two currently separate peer findings, TMR-1/040 (additive ordinary Resolution price for a duplicated Boolean circuit guard) and TMR-2/040 (exponential exact rational rank and fooling cover for the non-Schaefer proper-3CNF NAE relation), compose in **one authentic source**. That source should simultaneously have an exponential interface-rank/cover, a compact circuit for the *unique* Craig interpolant, and inherited exponential ordinary Resolution hardness from an independent affine contradiction. If correct, this is a concrete combined hostile example against equating fusion/interface semantic multiplicity or hard proof size with a computationally hard interpolant.

**Preselected falsifiers:** (1) the NAE evaluation matrix loses rank or rectangle cover when represented by an actual AND/NOT DAG; (2) the two Tseitin gate copies share private wires or lose authentic source authentication; (3) the supposed additive Resolution proof contains an illicit pivot or fails when gates reconverge/share; (4) a real degree witness, Gaussian proof, compact circuit, extension or alternate representation supplies a cheap path, defeating an alleged SAT-machine lower bound. The first three were independently audited for this specific NAE DAG and passed within scope. The fourth is real and defeats the stronger implication, not the restricted result.

## 2. Fully specified common-variable function

For k>=2 put r=k+binom(k,2), and introduce X_i,Y_i,W_i (1<=i<=k) and Z_ij (i<j), all distinct. Define NAE(a,b,c)=(a OR b OR c) AND (NOT a OR NOT b OR NOT c) and

$$
Q_k(X,Y,W,Z)=\bigwedge_{i=1}^k\operatorname{NAE}(X_i,Y_i,W_i)\ \wedge\
\bigwedge_{1\le i<j\le k}\operatorname{NAE}(X_i,X_j,Z_{ij}).
$$

This is a proper signed 3-CNF with n=3k+binom(k,2) variables and 2r=k(k+1) clauses. The primal graph contains K_k, every variable occurs in both polarities, neither allzero nor allone satisfies it, and the whole relation has a projection onto NAE_3, hence is not Horn, dual-Horn, bijunctive or affine. Its X-versus-(Y,W,Z) Boolean evaluation matrix M has **exact** rank_Q(M)=2^k and exact 1-rectangle cover number 2^k.

**Independent rank proof:** Set W=0 and sum over Z. If x has t ones, the resulting 2^k-by-2^k matrix satisfies

$$
K(x,y)=2^{t(k-t)}\prod_i(x_i\lor y_i)
=\operatorname{diag}(2^{t(x)(k-t(x))})\,
\begin{pmatrix}0&1\\1&1\end{pmatrix}^{\otimes k}.
$$

Its determinant is nonzero over Q, so rank(M)>=rank(K)=2^k, matching the row-count upper bound. This is NOT a GF(2) rank claim. For each a choose Y=NOT a, W=0 and Z_ij=1-a_i when a_i=a_j, Z_ij=0 otherwise. The resulting 2^k accepting pairs form a fooling set: for any a!=b one crossed pair is rejected by a local NAE triple. The 2^k row rectangles match this lower bound. Both are *function-evaluation* properties, not SAT decision-time lower bounds.

**New explicitly counted circuit:** Compile each positive NAE clause into four NOT and two binary AND gates (six total), each negative clause into one NOT and two AND gates (three total), join each pair by one AND, then join all r pairs with r-1 AND gates. The deterministic fan-in-two AND/NOT DAG has

$$
g_k=11r-1=\frac{11k(k+1)}2-1
$$

gates. Inputs and previously computed gate outputs may fan out; every gate and wire is explicitly allocated. The actual circuit computes Q_k on **every** assignment, not merely on the degree-witness assignment.

## 3. One authenticated hard-Resolution source with easy interpolant

Let F(U) be any UNSAT private CNF, disjoint from every variable of Q_k. Let E_A(X,Y,W,Z,V_A) and E_B(X,Y,W,Z,V_B) be separate authentic standard Tseitin clause sets for the same compiled DAG, using disjoint gate wires and output bits o_A and o_B. Define

$$
A=E_A\wedge\bigwedge_{C\in F}(o_A\lor C),\quad
B=E_B\wedge\neg o_B,\quad G=A\wedge B.
$$

This is ordinary source-inclusive binary Resolution with shared derived DAGs, charged **one per derived Resolution inference**, original source clauses available at zero inference price. It is not the /341, /386 or a generic SAT-machine model. Both A and B are separately SAT, G is UNSAT, and the **unique** Craig interpolant on all common variables X,Y,W,Z equals Q_k.

Proof: exact gate definitions force o_A=o_B=Q_k. For a common assignment with Q_k=1, A can satisfy all guarded private clauses; if Q_k=0, A would satisfy F, impossible. B projects exactly NOT Q_k. Both classes of assignments occur. Thus the separator is uniquely Q_k.

Let S_Res count the minimum number of *derived binary Resolution inferences*, not proof bits, physical transitions, or proof discovery. The entire source restricts to **exactly F** when all common inputs are fixed to any Q_k-false assignment and every private gate wire is fixed to its true evaluation. Hence restriction of Resolution gives S_Res(F)<=S_Res(G). Conversely, guarding every clause of a shared refutation of F produces the unit o_A without increasing its inference count. Inductively derive two implications between the two copies of each AND gate in at most four inferences per direction, or for NOT in at most two per direction; **reuse** prior gate equivalences. Resolve o_A with (-o_A OR o_B) and the original B unit -o_B. Therefore

$$
\boxed{S_{\rm Res}(F)\le S_{\rm Res}(G)\le S_{\rm Res}(F)+8g_k+2.}
$$

The source has exactly |F|+56r-5 clauses for this **specific** circuit compiler, since there are 5r NOT gates and 6r-1 AND gates, two Tseitin copies, |F| guarded clauses and one B unit. If F is proper 3-CNF, the guarded source is **width at most four**, not claimed proper 3-CNF.

For a uniform 3-regular expander family with H=k vertices (along allowable even sizes), choose F_k as the odd-charge cubic Tseitin contradiction, with 4k private clauses and O(k) variables. The original Ben-Sasson-Wigderson general-Resolution theorem, ECCC TR99-022 (1999), p.10, Theorem 4.1/Corollary 4.1, yields S_Res(F_k)=2^{Omega(k)} provided the graph's middle-size edge expansion is Omega(k). Thus G_k has a *native* 2^{Omega(k)} Resolution lower bound, but its unique interpolant has an explicit O(k^2)-gate AND/NOT circuit **despite** 2^k rank and 2^k rectangle cover. With standard binary-indexed clauses, L_k=Theta(k^2 log k). The same statement in L is Resolution lower bound 2^{Omega(sqrt(L/log L))}; it is NOT a deterministic machine-time lower bound. No generic 4-to-3CNF proof-size-preserving reduction has been established here.

**Exactly replayed finite private source:** F_3 consists of all eight signed clauses on three private variables. It has a seven-inference shared-DAG Resolution refutation by successively resolving on variable three (four times), variable two (twice), and variable one (once). For k=2 the combined source has 171 clauses, a fully replayed 169-step Resolution refutation, and an upper bound 265. For k=3 it has 339 source clauses, a fully replayed 337-step Resolution refutation, and an upper bound 529. Every derived clause was built from authenticated parents and an explicit signed pivot. These two cases do not themselves provide expander hardness.

## 4. Cost/tariff consequences and a concrete failed stronger implication

**Rank does not lower-bound computing Q_k:** A genuine deterministic algorithm evaluates the entire AND/NOT circuit in g_k=O(k^2) paid logical gate operations, even though its evaluation relation has rank and cover 2^k. A claimed source-rank scalar p(C)=2^k for all nonterminal circuit-evaluation configurations and p(goal)=0 fails on a genuine one-price final HALT transition with discharge 2^k. For vector (p_rank,p_active) where p_active=1 before HALT and 0 thereafter, the **exact** last-transition row is

| Rule | Paid cost | Delta_rank | Delta_active | Necessary tariff |
|---|---:|---:|---:|---|
| Any nonhalting circuit-operation, memory or source step | 1 | 0 | 0 | 0<=1 |
| Actual final HALT for the compiled evaluator | 1 | 2^k | 1 | 2^k lambda_rank + lambda_active <=1 |

There are **no authentic zero-cost operations** in this paid-gate evaluator. A nonnegative all-k length-independent tariff therefore has lambda_rank=0 and lambda_active<=1. This is an exact restriction on the **terminal-masked, source-static candidate**, NOT a theorem about any genuinely dynamic fusion potential. More generally, any dynamic nonnegative potential initialized at 2^k, terminal zero, and purported one-Lipschitz per paid operation along this genuine O(k^2) gate path would contradict telescoping; some transition would discharge at least 2^k/O(k^2) of its *unweighted* rank burden. This is a restricted computing-Q circuit evaluation path, not a general SAT refutation.

**Actual SAT-machine cheap path remains legal:** The original Q_k itself has a degree-count witness: X=0 and all Y,W,Z=1; a fixed total proper-3CNF SAT decider can count occurrences, verify the witness, and fall back to exhaustive search on other inputs. In G_k, the private odd-charge Tseitin F_k is a Gaussian contradiction, even if native Resolution requires exponential size. A fixed correct total general-CNF SAT decider can recognize a **source-authenticated canonical wrapper** (the explicit AND/NOT gate clauses and guarded complete XOR blocks), Gaussian-check private-row inconsistency, reject only upon verification, and otherwise exhaustively decide. Its processing on this authenticated family is polynomial in total encoded length. All source bytes and parser/checker work are paid. This is a polynomial correct-program countercontrol, not an assumption that arbitrary SAT instances have short UNSAT certificates.

These real paths defeat a direct claim that exponential Q-rank, rectangle-cover, expensive native Resolution, or their combination forces superpolynomial general SAT-machine runtime. They do NOT falsify the exponential native Resolution bound, do NOT supply a uniform polynomial SAT algorithm for all inputs, and do NOT prove a superpolynomial initial potential for the qualified native Resolution system.

**Zero-cost quotient and ownership:** In the Resolution system original source axioms are uncharged *inference* premises, not zero-cost computational source acquisition. Any import into an actual Turing machine must pay authentication, parsing, proof search and serialization. The compiler can share its DAG; arbitrary alternate proofs stay legal. The generic zero-closure/LP schema of TMR-4 remains RESTRICTED, and no open machine operation is silently forbidden.

## 5. Independent executable verification

The self-contained original source **experiments/tmr/tmr5_nae_rank_guard079.js** and raw output **results/raw/tmr/2026-11-15_0143_TMR5_NAEGUARD079_V8_RAW.json** are separate artifacts.

- 268,310 independent V8 exact assertions, 506 authentic derived Resolution steps, four negative/control cases (two invalid-pivot attempts, two explicit Q-false witness checks), zero reported failures.
- Exhaustive NAE-source versus compiled-circuit truth tables at k=2,3,4, covering 128+4,096+262,144 assignments.
- Exact-integer column aggregation and BigInt rational-rank elimination for k=2,3,4, plus all fooling-pair checks; rank and rectangle cover found to be 4,8,16.
- Independent two-copy gate equivalence and signed-pivot replay of the authenticated refutation at k=2 and k=3.
- Direct paid satisfying witness and nontrivial no-allzero/no-allone controls. No randomness; no physical finite-alphabet Turing machine was compiled. Tests are COMPUTATIONAL, not asymptotic proofs.

The source was generated from the **exact V8 function that successfully executed**; a wrapper prints the original JSON. Source and raw records are immutable. Readback is required after publishing and merging.

## 6. Original primary and project evidence, novelty ledger

1. Eli Ben-Sasson and Avi Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, ECCC TR99-022 (June 1999), section 4.1, p.10 Theorem 4.1 and Corollary 4.1, https://eccc.weizmann.ac.il/report/1999/022/download. **Scope:** ordinary Resolution width/length on odd-charge bounded-degree expander Tseitin formulas; not SAT-machine time. The original PDF page was visually checked this run.
2. Jan Krajicek, *Interpolation Theorems, Lower Bounds for Proof Systems, and Independence Results for Bounded Arithmetic*, Journal of Symbolic Logic 62(2):457-486 (1997), https://doi.org/10.2307/2275541. **Background only:** proof-system feasible interpolation; the unique-interpolant proof here is direct.
3. TMR-1/040 original theorem and replay: research/agents/tmr-1/2026-11-15_0104_TMR1_CIRCUIT_GUARD_ADDITIVE_FIREWALL040.md, experiments/tmr/tmr1_circuit_guard_additive075.js, results/raw/tmr/2026-11-15_0104_TMR1_CIRCUIT_GUARD075_V8_RAW.json.
4. TMR-2/040 original rank and degree-witness: research/agents/tmr-2/2026-11-15_0113_TMR2_NAE_RANK_FOOLING_DEGREE_FIREWALL040.md, experiments/tmr/tmr2_nae_rank_fooling075.js, results/raw/tmr/2026-11-15_0113_TMR2_NAERANK075_V8_RAW.json.
5. TMR-3/040 and TMR-4/040 exact physical interface tariff tests: research/agents/tmr-3/2026-11-15_0127_TMR3_ASYMMETRIC_PREFIX_INGRESS_TARIFF040.md and research/agents/tmr-4/2026-11-15_0038_TMR4_PREFIX_FREE_ENDMARKER_FUSION_TARIFF040.md. Physical one-way ingress is not this gate calculus.
6. TMR-5/036 authenticated dispersed affine detector: research/agents/tmr-5/2026-11-15_0052_TMR5_SHUFFLED_GAUSS_CORE_REDTEAM036.md. This is a hostile polynomial alternate decision, not a native Resolution refutation.
7. Historical research/agents/lead/2026-10-07_0855_LEAD-0029_LIPSCHITZ_SQUEEZE_AUDIT.md and source constraints in the governing refocus. Full root proof1/proof2/main.tex, issue #3, AGENTS.md, CODEX.md, research skill and all five current TMR handoffs reviewed; complete Git blob fallbacks used for large trackers.

**Genuinely new relative to peer reports:** Neither TMR-1/040 nor TMR-2/040 supplied the other's mathematical object as a completely constructed input. Here the **same explicit guarded source** has a unique non-Schaefer full-rank interpolant, exact circuit gate count, inherited native Resolution hardness, concrete source-clause count and independently replayed shared-DAG proof. This is an integrated hostile model-mismatch example and does not promote either existing restricted theorem to SAT-machine hardness.

## 7. Ranked dependency/status ledger and peer repair

| Rank | Component | Verdict |
|---|---|---|
| 1 | TMR-1/040 circuit equality and additive source-bound Resolution simulation, on explicit NAE circuit | PASS/RESTRICTED, independently replayed k=2,3 |
| 2 | TMR-2/040 full rational rank and fooling-cover relation, compact AND/NOT realization | PASS/RESTRICTED, exact symbolic proof and finite checks |
| 3 | Unique interpolant Q and simultaneous native expander-Resolution hardness | PROVED/RESTRICTED symbolically; independent peer review OPEN |
| 4 | Exponential source rank as fixed-price dynamic machine obligation, terminal-masked version | FAIL; real O(k^2) circuit path and paid HALT overdischarge |
| 5 | Converting inherited Resolution hardness or semantic rank to arbitrary uniform SAT-machine work | FAIL as an unqualified implication; polynomial Gaussian recognition control |
| 6 | /341 logical UNSAT on full accepted language | FAIL, preserved unchanged |
| 7 | /386 complete mixed-calculus authority | RESTRICTED, preserved unchanged |
| 8 | Superpolynomial fusion-safe initial potential with a full authentic all-step tariff | OPEN |
| 9 | Same-family, same-system transfer covering every correct total deterministic 3-SAT decider | OPEN |
| 10 | P versus NP | OPEN |

**Weakest surviving lemma:** A genuine nonaffine *dynamic* source-and-history-dependent obstruction invariant under complete cheap circuit evaluation, parity/Gaussian, Horn/2-SAT, extension/learning, caching and shared-DAG reuse, with a fully certified nonnegative tariff for **every** authentic physical machine step. A hard interpolant circuit lower bound for an explicit NP-family would itself demand a separate major complexity theorem.

**Peer repair:** TMR-1 independently check the formula-to-4CNF theorem and expander size exponent. TMR-2 check the rational-rank aggregation against all authenticated circuit gates. TMR-3 cost the uniform Gaussian recognizer and its source parser on the same 4CNF family. TMR-4 insert both compact circuit and native Resolution alternatives into the same qualified transition inventory and flag all unknown operations MAY. Do not prune these cheap paths by CEGAR.

**Publication:** source, raw, report and compact handoff committed to a role-owned branch. Readback, merge and issue #3 registration must be separately verified before a MERGED claim. **TRACKERS REVIEWED; NO MATERIAL CHANGE.**