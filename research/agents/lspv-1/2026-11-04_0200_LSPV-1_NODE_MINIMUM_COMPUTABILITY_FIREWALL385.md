# LSPV-1/385: Node-only proof minima need not be computable

**November 4, 2026, 02:00 PST, America/Los_Angeles.**
**Status:** **PROVED/EXACT** as a restricted computability-theoretic counterexample for a deliberately different fixed proof system (independent specialist review pending); **PROVED/EXACT** normalization-to-computability lemma; **COMPUTATIONAL** two independent finite toy trace checkers; **KNOWN THEOREM** Haken/Cook-Reckhow and undecidability of Turing-machine halting. **OPEN** full LOCAL-CONVERT grammar in preselected `R_mix341`, B1/B2/B3, superpolynomial mixed worst-case minimum, and P versus NP.

## Fixed target and published anchor

**Do not alter `R_mix341`.** Its source clauses are authenticated free leaves; distinct derived RES, support-at-most-three-original-variable AND3, binary GF(2) XOR, justified unary LOCAL-CONVERT, and conservative two-input paid DEF nodes each cost one. Derived DAG nodes have at most two antecedents, and all original source clauses retain identities. LOCAL-CONVERT may present a bounded-support circuit condition, but whether arbitrary uncharged internal gates can be exported through named wires is not completely resolved. The precise source is `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` at blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`.

For any valid UNSAT CNF F, `W_R(F)` minimizes the sum of weights over distinct paid inference nodes in one finite sound complete fixed R; `Wbar_R(N)` maximizes over valid UNSAT binary encodings of length at most N, with the empty maximum zero. The minima exist as nonnegative integers because Resolution is complete and every proof is finite, but existence **does not in itself provide an effective optimizer or a bound on proof payload bits**.

**Published hardness anchor:** For unary PHP(h+1,h), Haken (1985) proves there are c>0,h0 such that for every h>=h0 **every unrestricted shared-DAG ordinary Resolution refutation** has at least 2^(ch) lines. Its unsigned pigeon/slot variables number h(h+1); its signed CNF has m_h=(h+1)+h*binom(h+1,2) source clauses; standard explicit binary-index signed input length N_h=Theta(h^3 log(h+2)). Paid Resolution nodes are >=2^(ch)-m_h. No all-algorithm lower bound follows. Cook's polynomial Extended Resolution PHP and native GF(2) Tseitin proofs defeat a naive transfer to the combined calculus. No published lower bound is reproved here.

B1: forall fixed uniform correct total A, exists polynomial p_A, forall valid UNSAT F, W_R(F)<=p_A(N(F)+T_A(F)).
B2: forall A exists p_A forall N, Wbar_R(N)<=p_A(N+T_A^wc(N)).
B3: SAT in P implies a polynomial Wbar_R bound for the **same preselected R**. All are **OPEN** for `R_mix341`, with B1=>B2=>B3.

## Falsifiers

F1. "A finite minimum with integer paid-node weights is automatically computable from F." **FALSIFIED in a different sound complete, polynomial-time proof-checkable calculus P_H below.**

F2. "Polynomial-time verification of a full proof implies that the existential property 'there is a proof with one paid node' is decidable." **FALSIFIED** when a one-node record can have arbitrarily long, uncharged witness payload.

F3. "A computable cap b(N,q) on bit length of equivalent q-node witnesses is enough to compute the exact minimum by exhaustive search." **PROVED**, including an exact all-input algorithm and worst-case profile computation.

F4. "The counterexample immediately makes W_Rmix341 uncomputable or disproves B3." **FALSIFIED AS AN INFERENCE**. P_H has a global source-dependent terminal rule that R_mix341 expressly disallows. This is a firewall against weak descriptions of 'intrinsic optimum', not an extension of the project calculus.

## Theorem A: polynomial-time proof checker, noncomputable minimum paid-node count

**PROVED/EXACT (elementary computability reduction; external mathematical review pending).**
There exists **one fixed**, sound, complete and polynomial-time-checkable refutational proof system P_H for general encoded CNF, with nonnegative *unit* derived-node weights, and a fixed polynomial-time computable injection e -> F_e into a family of syntactically trivial UNSAT CNFs, such that:

```
W_PH(F_e) = 1 if a fixed universal Turing machine U halts on program e;
W_PH(F_e) = 2 otherwise.
```

Consequently, deciding `W_PH(F)<=1` is r.e.-complete **even when restricted to the always-UNSAT canonical family**, and the integer-valued function W_PH is uncomputable there. Every finite F still has a well-defined attained integer minimum whenever UNSAT. `P_H` is an intentionally adversarial *different* proof system, not a legal rule of `R_mix341`.

**Construction and proof.** Take a standard universal deterministic Turing machine U with a fixed binary description convention and an r.e.-complete halting set H. For each e=e_1...e_l define the canonical *ordered* CNF

```
F_e = (x_1) AND (NOT x_1) AND
      AND_{i=1..l} (x_{i+1} if e_i=1 else NOT x_{i+1}).
```

Use an exact DIMACS header and declared variable bound l+1. The original first two clauses contradict; every other clause references its own fresh variable. The parser extracts e uniquely in polynomial time from signs and positions, rejects malformed sources, and no F_e contains an original empty clause. The encoding length is Theta((l+1)log(l+2)) bits under explicit signed binary indices.

A P_H proof is in exactly one of two modes:
1. **DEFAULT:** a genuine ordinary binary Resolution derivation of the empty clause from source F, with all pivots/source references/derived clauses verified, followed by one compulsory additional paid terminal `FINAL` record referencing that empty-clause conclusion (or an original empty source). All derived Resolution nodes and FINAL cost one each. This makes the system refutationally complete for every UNSAT CNF. For F_e, the two original opposite units resolve directly, so DEFAULT has **exactly two** paid nodes and cannot have fewer by this grammar.
2. **SPECIAL:** one paid terminal `HALT` record whose *explicit, arbitrarily long* payload is a complete valid accepting/halting computation tableau of U on the e extracted from a syntactically exact F_e. Every initial configuration, local transition, tape bound, terminal state and framing field is checked. The verifier never solves general SAT and never invokes a halting oracle; it checks a **finite** supplied computation. Such a record is sound because its accepted source has the contradictory pair (x_1),(NOT x_1), regardless of U. Verifying a supplied tableau is polynomial in the complete written proof length. There is no SPECIAL proof for non-F_e inputs.

If U(e) halts, its finite transcript yields SPECIAL with one paid node. If not, there is no valid SPECIAL proof; DEFAULT exists and has exactly two nodes for F_e. A zero-node proof is not terminal by grammar. Hence the displayed equality holds for every binary e. A total algorithm computing W_PH(F_e) would decide the undecidable halting set, contradiction. Enumerating one-node proof encodings semidecides H, giving r.e.-completeness.

**Scope:** SPECIAL violates the source-local at-most-binary-premise requirements of `R_mix341` and has unlimited evidence behind a unit node. It is included as an adversarial control, never as an admissible `R_mix341` shortcut. This does not show SAT is computationally hard: the entire F_e family is linearly recognizable and its SAT label is trivially UNSAT.

## Theorem B: computable cost-compactness implies computable optimum

**PROVED/EXACT, conditional on explicit computable cost-normalization.**
Let R be any fixed sound complete proof grammar for CNF whose verifier halts on every well-formed or malformed finite certificate and is effective. Suppose there is a total computable function b(N,q) such that for every valid UNSAT input F of length N and every integer q>=0:

```
W_R(F)<=q  =>  F has some valid R refutation of cost <=q
                with a completely encoded proof of <=b(N,q) bits.
```

Then `B_R={(F,1^q): F valid and W_R(F)<=q}` is decidable without assuming SAT in P. Enumerate the finitely many bitstrings of length <=b(N,q) and check them, rejecting malformed and SAT instances. Independently brute-force all Boolean assignments to decide SAT/UNSAT, then scan q=0,1,... until B_R accepts: this computes W_R(F) for each UNSAT F and rejects SAT/malformed. Enumerating every encoded binary string of length <=N, parsing it, classifying it by brute force, and computing W_R gives a total algorithm for Wbar_R(N). No feasible complexity bound is claimed: exhaustive proof enumeration can be astronomical.

A **polynomial** b(N,q) and a polynomial-time proof verifier further give B_R in NP under unary q (already established conditionally for bounded-output Rmix in LSPV-1/364). This does **not** imply B3 or a polynomial N bound on q. The theorem makes precise the previously missing distinction between a *finite* minimum and its effective attainability.

**Application status:** LSPV-4/342 asserts a polynomial node-to-bit bound for R_mix341 under a bounded-output, canonical local-record grammar; LSPV-1/364 already derives the unary-budget NP consequence under that hypothesis. The original LOCAL-CONVERT circuit-valued/observable-wire semantics (LSPV-4/363 and LSPV-1/384 addendum) still need reconciliation before promoting b(N,q)=poly(N+q) to all allowable *original* R_mix341 proof records. Theorem B is a positive, exact transfer for any grammar with a genuinely proved b, not a conclusion that the actual mixed calculus lacks one.

## Finite, independently implemented controls (COMPUTATIONAL)

A deterministic JavaScript producer and independently written Python checker each tested all 85 programs consisting of 0..3 two-bit opcodes from {FLIP, LOOP, HALT, invalid}. They agree on 27 halting and 58 nonhalting toy programs, including both terminating traces and deliberate forged traces; each reports **355 assertions**. Five malformed source cases each undergo three negative checks (15 rejects). A two-paid-node symbolic genuine contradictory-unit Resolution + FINAL fallback is checked for every valid canonical source by the producer. The toy instruction language is explicitly **decidable** and has a bounded local test horizon; the finite controls do **not** prove the universal-TM halting theorem. Both source programs were run locally and the producer and summary were verified against GitHub readback; the independent verifier was run locally and requires readback when its concurrent GitHub create conflict clears.

Artifact paths:
- `experiments/arc/lspv1_385_halting_node_witness.js`
- `experiments/arc/lspv1_385_independent_verify.py`
- `results/raw/arc/2026-11-04_0200_LSPV1_NODE_MIN_COMPUTABILITY385.json`
Seed none, exhaustive toy scope; no main-project hard formula newly generated.

## Corpus, primary literature, duplication and barriers

Read full November 2 12:04 coordination directive, current issue #3 (757 comments), original R_mix341/341, project AGENTS/CODEX/skill, bounded-evidence LSPV-4/342, LOCAL-CONVERT gate-verifier LSPV-4/363, LSPV-1/364/374/375/376/382/383/384 and current LSPV-2/384, LSPV-4/381, LSPV-5/333 issue handoffs. Prior LSPV-1/364 already discusses decidable unary budgets **assuming normalized proof witnesses**; this result adds an explicit uncomputable unbounded-payload control and a separation between optimum existence and optimum computability, not a duplicate polynomial-time certificate search claim.

The actual Grok and Claude locations were independently recovered from the connected repository directory listing. `research/agents/grok/2026-10-12_1859_GROK_FL2.tex` (blob `f2a90a8be0688647c0d0b231875438390e769ca8`) states no universal all-CNF charged compiler; `GROKPROOF/2026-11-04_0116_PROGRESS.md` (blob `ca5a835356eb918b8cb4ab94d14de6174edeab03`) still lists the all-input compiler OPEN. `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` (blob `79e4d4e7e0e3edff3aba8610852c45534bdde128`) distinguishes P/NP worlds; `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4`) proves a crossing-sequence restriction that does not separate arbitrary computation. Neither supplies B3.

Source searches: `minimum proof uncomputable payload halting`, `shortest proof undecidable inference count`, `finite optimum enumeration canonical grammar`, `node evidence domination`; no indexed duplicate of the exact uncomputable-unit-node counterexample was found. Public searches: Cook–Reckhow 1979, Haken 1985, unbounded proof-payload verification, github.com/openai SAT/circuit verification. No useful OpenAI-owned implementation of this model was found. Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36–50, DOI 10.2307/2273702, supplies the polynomially verifiable proof-system framework; Haken, *The Intractability of Resolution*, TCS 39 (1985), 297–308 supplies only Resolution hardness. Standard halting undecidability is the only non-proof-complexity theorem needed.

**Physical ledger:** SPECIAL's q=1 does not pay the transcript's potentially unbounded encoded bit length L, its Theta(L) mandatory input read, local configuration checks (poly(L) time), or the potentially large simultaneous input/certificate buffer; proof discovery is separate and in general not computable at the unit-node optimum. DEFAULT's proof serialization, source-index access, RES checks and FINAL are explicit. There is no FLMV same-machine inference. Theorem B's exhaustive search may use more time/space than any reasonable SAT solver; it is an effectivity theorem, not a resource upper bound.

**B1/B2/B3 audit:** the constructed P_H is a *different* grammar and gives no lower bound, upper bound or counterexample to B1/B2/B3 for original R_mix341. The normalized-witness lemma does not transform rejecting traces from arbitrary correct A into sound R_mix341 refutations. Cook–Reckhow completeness of some proof system under P=NP does not establish B3 for the preselected mixed calculus.

**Next:** settle exact legal LOCAL-CONVERT public-wire syntax and produce either an explicit b(N,q) for every valid R_mix341 q-node proof, or a source-authenticated counterexample to bounded normalization. Independently audit the existing LSPV-1/375 strict ER2 affine compiler. Do not prioritize new hard formulas until this transfer is checked. P versus NP remains OPEN.
