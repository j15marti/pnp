# LSPV-1/396: IMPLICIT-ROW VALIDATION AND THE G1 COST-TRANSFER FRONTIER

**November 4, 2026, 11:00 PST, America/Los_Angeles.**

**Status:** PROVED/EXACT elementary coNP-completeness theorem for a deliberately separate succinct proof-stream **verification model**, specialist mathematical review pending. PROVED/EXACT conditional implication about proof-system simulation. COMPUTATIONAL: two independent finite checkers. CONDITIONAL for the typed X3 simulation as specified in LSPV-1/375. OPEN for full unchanged R_mix341 and B1/B2/B3. P versus NP is OPEN.

The exact five active roles, schedules, enabled state, ownership, historical artifacts and R_mix341 inference rules/weights are unchanged.

## 1. IDEA -> SEARCH -> ITERATE

**IDEA (before search).** Try to convert an arbitrary **circuit-implicit, source-authenticated Resolution proof** into a polynomial-node proof in the existing mixed calculus, not by unrolling an exponentially long proof. Hypotheses: an explicit local validity checker for each circuit-addressed inference; the input source remains unchanged; every exported wire and helper definition receives its legal cost. Falsifiable prediction: if each described inference is locally simple, checking the whole succinct proof and reflecting it into the normalized mixed fragment should be a routine polynomial-size/effective translation.

**SEARCH and effect on hypothesis.** The original fixed R_mix341 (LSPV-2/341, blob c87acd11) and LSPV-1/375 (blob 92e5a295) establish a constructive polynomial node comparison only for the explicitly bounded-output fragment X3 and its embedded binary-gate Extended Resolution ER2, not opaque full-R LOCAL-CONVERT. REFEREE334 shows that polynomial proof-bit conversions alone do not preserve paid outer-node counts; REFEREE342 gives architecture-specific positive-pin/mux source retraction but does not prove short reflection.

A crucial **primary 2026 finding** is Fleming, Grosser, Pitassi and Robere, *Provable Reductions in TFNP* (arXiv:2606.27931, June 30, 2026), Theorem 1.1: [EF, DAG Resolution], also called general implicit Resolution, is polynomially equivalent to the quantified sequent system G1. The paper emphasizes that G1 is believed stronger than EF, without proving a separation. Its explicit correctness proof is important: not every circuit that merely claims to describe a proof is valid. The 2020 Kiesl/Rebola-Pardo/Heule/Biere paper establishes polynomial ER simulation for DRAT and DPR and does **not** authorize free checking of arbitrary implicit inference streams.

**ITERATE.** The initial predicted automatic normalization is unsupported. Replace it with (i) a concrete coNP-complete **succinct all-row legality** problem despite constant-time explicit local checks and (ii) a precise implication: a uniform polynomial-time compiler from all [EF, DAG Resolution] proofs into X3, followed by the existing X3-to-ER2 compiler, would p-simulate G1 in ER2. This is a formal obstruction to claiming universal compact-representation reflection as a mere encoding lemma, **not** a proven impossibility or separation.

## 2. Exact source, grammar and an unconditional finite-logic theorem

Fix the three-clause signed CNF
$$
F_*=(x\lor y)\land(x\lor\neg y)\land(\neg x).
$$
It is UNSAT. Its authenticated source clauses are C1=(x OR y), C2=(x OR NOT y), C3=(NOT x), with fixed signed-index binary encoding. Ordinary binary Resolution applied to C1 and C2 on pivot y yields (x), then resolves with C3 to produce the empty clause. These are legal RES in R_mix341, but the *succinct indexed stream below is NOT a legal additional R_mix341 inference rule*.

Input to the **separate stream-validation problem** is an arbitrary valid CNF D on n variables a1,...,an (encoded as explicit signed literal lists). Its evaluation circuit has size O(|D|), with n input bits indexed by a in {0,1}^n. At every index a, a circuit produces the following **claimed** Resolution record:
$$
\begin{array}{ll}
\mathrm{left}(a)=C_1, & D(a)=0,\\
\mathrm{left}(a)=C_3, & D(a)=1;\\
\mathrm{right}(a)=C_2,\quad \mathrm{pivot}=y,\quad \mathrm{claimed\ resolvent}=(x).
\end{array}
$$
The complete expanded stream has 2^n candidate records. The stream grammar declares its entire list valid only when **every** row is a valid instance of ordinary signed binary Resolution. A malformed D or missing/ill-typed record is rejected. This is a proof-stream integrity format with mandatory rows, not a minimization claim about F_*.

**Theorem 396A (PROVED/EXACT, elementary).** The language of D for which **every** circuit-described Resolution record is locally legal is coNP-complete under polynomial-time many-one reductions. It remains coNP-complete with the unchanged fixed three-clause UNSAT source F_* and a row grammar exposing only constant-size source IDs, a pivot and a claimed resolvent.

**Proof.** If D(a)=0, the left clause is C1 and the claimed inference RES_y(C1,C2)=(x) is legal. If D(a)=1, the left clause is C3=(NOT x), which contains no positive y, so the claimed pivot inference is illegal. Thus every row is valid if and only if forall a, D(a)=0, which is equivalent to D being UNSAT. The map D to the evaluating circuit and fixed row template has polynomial output length. CNF-UNSAT is coNP-complete, giving hardness. The complement has witness a such that D(a)=1, and checking its invalid row takes polynomial time in |D|; hence membership in coNP. QED.

**Interpretation.** Even a constant-size **explicit** inference verifier does not imply polynomial-time universal checking of a succinct circuit-described list of exponentially many alleged inferences. The example uses mandatory possibly redundant rows; F_* already has a two-step ordinary Resolution refutation. Consequently it is **not** a hard family, does not lower-bound W_Rmix341, and gives NO unconditional superpolynomial runtime lower bound. A polynomial-time algorithm for the new succinct checking language would imply P=NP, not a contradiction already known.

## 3. Conditional compiler frontier from a current published theorem

Let I=[EF, DAG-Resolution] be the explicit Cook-Reckhow proof system whose certificates consist of a succinct circuit describing a Resolution proof plus an EF correctness proof. Let X3 be the normalized, explicitly typed RES+DEF+AND3/local-convert+native-XOR **fragment** from LSPV-1/375, without arbitrary uncharged opaque exported circuits. For input bit length N, LSPV-1/375 gives a **constructive** polynomial translation of every explicitly supplied q-node X3 refutation into a same-source ER2 refutation with at most p(N+q) paid nodes and polynomial encoded output bits. It also fixes all charged helper gates. This statement is limited to X3, not every interpretation of full R_mix341.

**Theorem 396B (PROVED/EXACT logical implication; compiler premise OPEN).** Suppose ONE fixed, uniform polynomial-time procedure C, given **any** valid I proof sigma of any UNSAT signed CNF F, produces a fully explicit X3 refutation of **the same** F with complete output length and node count bounded by one polynomial in N+|sigma|. Then ER2 polynomially **p-simulates** I and therefore p-simulates G1 (using Fleming et al.'s polynomial equivalence). If the compiler is assumed only to yield the **existence** of short X3 proofs, without an algorithm computing them, the justified conclusion is **length simulation** rather than p-simulation.

**Proof.** Compose C with the uniform polynomial explicit X3-to-ER2 translator of Result 375. The first output has polynomially bounded full bit length by assumption, so the second runs in polynomial time and emits polynomially many ER2 instructions and evidence bits. All outputs retain F and every local inference is soundly replayed; both translators use a single fixed program, not a per-input proof oracle. This is exactly the definition of p-simulation I to ER2. By Theorem 1.1 in Fleming et al., I and G1 are polynomially equivalent, giving ER2 p-simulation of G1. Removing effectivity leaves only existence and cannot justify p-simulation. QED.

**Logical firewall:** It is an **OPEN research question**, not a proved separation, whether EF p-simulates G1. The theorem does not establish that such C fails. Nor does it imply that the unchanged **full** R_mix341 is no stronger than ER2; that would require settling full LOCAL-CONVERT port semantics and a polynomial R_mix341-to-ER2 compiler. Conversely, requiring arbitrary correct uniform SAT *deciders* to produce X3 proofs would be a different and generally weaker proposed bridge (B3). No equivalence between these demands is assumed.

## 4. Three falsifiers and hard-family calibration

**F1.** "Every circuit-succinct proof stream is polynomial-time checkable because each explicit row has a constant-time RES checker." **NOT JUSTIFIED:** Theorem 396A makes the claimed universal check coNP-complete for a syntactically precise mandatory-row format. It does not prove P != NP.

**F2.** "A compiler only has to bound the number of outer nodes; it may output exponentially large opaque node payloads." **FALSIFIED as a cost/bit-transfer claim** by the packed-proof example of LSPV-5/REFEREE334. Theorem 396B explicitly requires polynomial complete output bits and runtime. Unrolling an exponential stream costs its actual encoded output length, construction, access, validation and simultaneous memory.

**F3.** "Published exponential ordinary-Resolution hardness carries over to full R_mix341 and then to all SAT algorithms." **FALSIFIED as an inference:** Haken (1985) proves for some c>0 and h0 that every h>=h0 and every ordinary *shared-DAG Resolution* refutation of the standard unary PHP(h+1,h) has at least 2^(ch) lines. Its signed CNF has h(h+1) variables, (h+1)+h*binom(h+1,2) clauses, and N=Theta(h^3 log(h+2)) bits under explicitly indexed signed-literal encoding. Free source leaves subtract at most the clause count from a paid-derived-node bound. Cook (1976) gives polynomial Extended Resolution refutations. Since ER2 is an embedded paid DEF+RES subsystem of R_mix341, no corresponding Haken lower bound for the mixed minimum follows. Odd-charge cubic Tseitin is additionally linearly refutable by native GF(2), despite known ordinary Resolution lower bounds.

## 5. Independent computational checks, with limitations

COMPUTATIONAL: a no-dependency JavaScript producer exhaustively enumerated all 2^8=256 subsets of the eight non-tautological signed clauses on two variables used for D (95 SAT, 161 UNSAT). It verified, for all four assignments per D, that row validity is the logical complement of D(a), recorded 2,818 local assertions and produced an immutable JSON ledger. An independently written Python checker evaluated literal truth and signed Resolution separately. It passed 1,548 assertions on the 256 cases, rejected five malformed-D shapes, and rejected four deliberately corrupted records (wrong label, truncated case set, altered fixed source, changed invalid-row count). The published producer was re-evaluated after GitHub readback and reproduced the ledger. Finite tests do not prove coNP-completeness or any asymptotic SAT lower bound.

For D of encoded length m and n appearing variables, the compressed evaluator/row circuit is O(m) gates, while explicit enumeration contains 2^n row records (Omega(2^n) bits even before row indices). A straightforward fully charged enumerator performs O(2^n poly(m)) time and requires an n-bit assignment counter plus working evaluation data; output is streamed or materialized with its genuine time/space cost. This is **one upper bound**, never an unconditional lower bound on all algorithms. Certificate evidence length, parsing, bit access, construction, correctness checking, proof optimizer discovery, and all-phase peak workspace are separate from the number of paid logical R_mix341 nodes. Preserve the materialized-child envelope s'<=max{rho,eta,lambda,lambda*s}, with rho covering every local phase.

## 6. Corpus, literature and external assessments

**Original project actually read:** November 2 12:04 directive at blob 033b54b8; issue #3 through REFEREE342; AGENTS.md blob 19656af1; CODEX.md blob 754999f5; .codex/skills/pnp-research/SKILL.md blob b8df83a7; LSPV-2/341 original R at c87acd11; LSPV-1/375 at 92e5a295; Red Team REFEREE299 at 71e3f22, REFEREE318 at d5164f4, REFEREE334 and REFEREE342 at 10b41ff5. Existing project reflection-family results /353, /357 and /361 were recognized as prior sufficiency/equivalence work, **not** republished. The new scoped increment is the simple fixed-source coNP-complete **all-row audit** and its explicitly delimited G1 simulation consequence, rather than new SAT proof hardness.

**Primary external sources actually read/search-checked:** A. Haken, *The Intractability of Resolution*, TCS 39 (1985), 297-308, DOI 10.1016/0304-3975(85)90144-6. S. Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4) (1976), 28-32. S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36-50. J. Krajicek, *A Note on SAT Algorithms and Proof Complexity*, IPL 112 (2012), 490-493 (its soundness-provability condition is not waived). B. Kiesl, A. Rebola-Pardo, M. Heule, A. Biere, *Simulating Strong Practical Proof Systems with Extended Resolution*, JAR 64 (2020), 1247-1267, DOI 10.1007/s10817-020-09554-z. N. Fleming, S. Grosser, T. Pitassi, R. Robere, *Provable Reductions in TFNP*, arXiv:2606.27931 (June 30, 2026), introductory Sections 1-1.1 and Theorem 1.1.

**Exact web research queries:** "Extended Resolution Extended Frege p equivalent proof systems polynomial simulation Tseitin proofs"; "polynomial size resolution proofs parity equation addition Tseitin encoding XOR gates linear"; "Jan Krajicek 2012 A note on SAT algorithms and proof complexity reflection D4 pdf"; "Haken 1985 intractability of resolution pigeonhole lower bound Cook 1976 extended resolution PDF". General web search returned the primary paper and published paper pages; one university publication page timed out. A dedicated direct Google-branded search was unavailable and is **not** claimed.

**Exact OpenAI GitHub searches:** in org openai: "SAT proof checker resolution", "extended Frege Lean", "proof system implicit resolution", and "SubexponentialSAT ExecCNFNodeSearchCosts". The concrete source actually read is openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean at blob 1ced21f4: it charges an actual node-search program with its visit log, but does not prove a generic R_mix341 compiler, implicit proof verification algorithm, B1, B2 or B3. No relevant OpenAI-owned all-proof compiler was found.

**Grok report actually read:** GROKPROOF/2026-11-04_1518_PROGRESS.md, blob 4e2bb9d9. Its proposed universal fully charged same-machine ARC/FLMV transformation remains OPEN; its restricted circuit-cut conclusions do not establish the present compiler. **Claude report actually read:** research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex, blob 9a5b05d6. It concerns restricted sequential one-tape time-space behavior, not B3 or universal proof normalization. These are research evidence, not substituted mathematical authority.

## 7. Exact B1/B2/B3 status and next decisive obligation

Fix unchanged R=R_mix341, authenticated original clauses free, each distinct paid RES/AND3/XOR/LOCAL-CONVERT/DEF shared-DAG node unit weight, and valid general CNF input strings with malformed strings separately rejected. The proof-node minimum and its worst-case function are
$$
W_R(F)=\min_{\pi:\ F\vdash_R\bot} \sum_{v\in\pi\ \mathrm{paid}} 1,\qquad
\overline W_R(N)=\max_{F\in\mathrm{UNSAT},\,|\langle F\rangle|\le N}W_R(F).
$$
Let A range over fixed uniform total correct SAT/UNSAT/malformed deciders, and T_A^wc(N)=max_{|x|<=N}T_A(x). The following remain OPEN:
$$
\begin{aligned}
B1:\ &\forall A\,\exists p_A\,\forall F\in\mathrm{UNSAT},\
W_R(F)\le p_A(|F|+T_A(F)),\\
B2:\ &\forall A\,\exists p_A\,\forall N,\
\overline W_R(N)\le p_A(N+T_A^{wc}(N)),\\
B3:\ &\mathrm{SAT}\in P\Longrightarrow \overline W_R(N)=N^{O(1)}
\quad\text{for this SAME preselected R.}
\end{aligned}
$$
B1 implies B2 implies B3, but none is proved. Also OPEN is a superpolynomial worst-case lower bound for this full R. The next exact work is to identify the **native** LOCAL-CONVERT exported-port grammar and attempt its polynomial all-proof explicit ER2 compiler, with any remaining implicit-proof step charged and accompanied by an explicit correctness/reflection certificate. Do not import implicit certificates as free R_mix341 nodes, and do not assume an ER/G1 simulation result as settled.

**No claim of P != NP. P versus NP remains OPEN.**
