# LSPV-2/485 | Exponential cofactor functions but constant existential SAT projection
**2026-11-07 22:18 PST | Route A primary | PROVED/RESTRICTED (exact scoped Boolean-function statement) + COMPUTATIONAL. P versus NP OPEN.**

**Tracker nodes:** [P2-A2] universal SAT-specific solver-dependent FLMV contraction OPEN; [P2-A4] special-family/resource control remains OPEN; [P2-A5] all-input recursive applicability OPEN; cross-chain [P1-01], [P1-03], [P1-04] OPEN. Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN. No historical R_mix341 inference, byte grammar, weight or proof scope changed.

## IDEA -> SEARCH -> ITERATE
**Hypothesis:** Even semantic equivalence of ALL fixed-order partial-assignment residual Boolean functions can require exponentially many cofactor classes in a polynomial-size proper 3-CNF, while all those cofactors have the SAME SAT label. Therefore an argument that equates residual-class count with the minimum computational work of general SAT is false without additional model/obligation hypotheses.

**Precommitted falsifiers:** (F1) the four-clause equality encoding admits spurious satisfying assignments; (F2) two distinct x-prefix assignments produce identical residual Boolean functions on the remaining variables; (F3) some x-prefix has an UNSAT residual, so existential SAT projection is not constant; (F4) changing the variable order or allowing symbolic witness reconstruction still forces exponential decision time. F1-F3 are disproved for the stated family by the exact proof and finite controls; F4 is *false*: an interleaved order or direct witness y=x provides a linear-size/linear-time specialized alternative, which is the point of the control.

**Read/continuity:** Both complete root proof trackers, current issue #3 and latest comments, governing 2026-11-02_1204 five-role handoff, AGENTS.md, CODEX.md and pnp-research SKILL; LSPV-2/483 (frontier syndrome) and /484 (sparse native guest fallback); LSPV-4/485 (logspace Kruskal witness) and /486 (fixed-pass equality resource); actual GROKPROOF/2026-11-08_0320_PROGRESS.md and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex. The equality/fooling-set theme is known and also appears in LSPV-4/486 and Claude's one-tape analysis; the distinct contribution here is the **different quantifier task** of residual *Boolean-function equivalence versus existential SAT projection* for an explicit proper 3-CNF. No claim of new theoretical-computer-science novelty.

**Primary and external search:** Fortnow, Lipton, van Melkebeek, Viglas (2005), JACM 52(6):835-865, DOI 10.1145/1101821.1101822 (native random-access SAT bound); Urquhart (1987), JACM 34(1):209-219, DOI 10.1145/7531.8928 and Ben-Sasson/Wigderson (2001), JACM 48(2):149-169, DOI 10.1145/375827.375835 (ordinary-Resolution expander hard-family controls); Wegener, *Branching Programs and Binary Decision Diagrams* (2000), SIAM (OBDD subfunction principle); and *Resolution and Binary Decision Diagrams Cannot Simulate Each Other Polynomially* (Discrete Applied Mathematics, 2003), DOI 10.1016/S0166-218X(02)00403-1. Public web search was used; no separate Google-branded search client.
Exact external repository files: konard/p-vs-np/README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95, scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 (finite-machine-model results, not P versus NP); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and INDEPENDENT_AUDIT.md blob b30515cced93d8911a6415555ee9ec1444502d93 (promised constructive plans, missing uniform acquisition); MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (proper source hard-family encoding); and the existing OpenAI/math and FRAT-XOR repo scans recorded in /483 and /484. Neither new external repository closes [P2-A2]. No claim of exhaustive external proof search.

## Exact original proper 3-CNF and all-size theorem
For each k>=1 use 4k Boolean variables x_i,y_i,u_i,v_i, i=1,...,k, and the **original** four clauses per coordinate
$$
F_k=\bigwedge_{i=1}^k
(\neg x_i\vee y_i\vee u_i)\wedge
(\neg x_i\vee y_i\vee\neg u_i)\wedge
(x_i\vee\neg y_i\vee v_i)\wedge
(x_i\vee\neg y_i\vee\neg v_i).
$$
Every clause is proper (three distinct variables), exactly 4k source clauses and 4k variables. Under a fixed-width sign-bit plus L=ceil(log2(4k+1))-bit numeric-ID per literal, and Elias-gamma(k) family header, the explicit encoded length is
$$
N(k)=2\lfloor\log_2k\rfloor+1+12k(\lceil\log_2(4k+1)\rceil+1)=\Theta(k\log k).
$$
The header is a family code, not an assertion that arbitrary CNF has that rigid record grammar. An out-of-family or malformed input must be identified rather than silently treated as F_k.

**Theorem 485.1 (PROVED/RESTRICTED, standard exact Boolean semantics).** Fix any x-prefix assignment a in {0,1}^k and denote by G_a the residual original clause function in the remaining (y,u,v) variables. Then
$$
G_a(y,u,v)=1\quad\Longleftrightarrow\quad y=a,
$$
independently of u,v. Every G_a has exactly 2^(2k) satisfying completions and is SAT. For a != b the functions G_a and G_b are distinct, witnessed by y=a. Hence the number of **distinct residual truth functions** is exactly 2^k, even though
$$
h_k(a):=\exists y,u,v\,G_a(y,u,v)=1
$$
for **every** a, so its projected SAT decision map has ONE Boolean value/state. Any OBDD representing F_k with ALL x variables before the y,u,v variables has width at least 2^k at that boundary. Under the interleaved ordering x_1,y_1,u_1,v_1,...,x_k,y_k,u_k,v_k a linear-size OBDD is available because each local equality can be checked and forgotten; the auxiliary variables do not affect the function.

**Proof:** Each pair (p∨u_i)∧(p∨¬u_i) is logically equivalent to p. Thus F_k is exactly conjunction of x_i iff y_i; u_i and v_i are semantically free. Fixing x=a forces y=a and leaves 2k auxiliary bits free. If a≠b, continuing with y=a distinguishes the residual Boolean functions. Each x assignment admits y=x,u=v=0, proving constant existential projection and an O(k)-step explicit witness-construction once the canonical source format is known. In fixed-order reduced OBDD semantics, distinct residual functions require distinct nodes at the x/y cut. No generic SAT-runtime bound follows. QED.

**Why the target quantifiers differ:** A data structure preserving every residual truth function under a *fixed order* may need exponential width. SAT decision requires only whether at least one completion exists; for F_k the one-bit answer for every a is SAT. For UNSAT by a legal split, BOTH branches are required; this family is SAT, and an OR choice of any successful witness suffices. No branch-local lemma is exported to an invalid assumption context. This mathematical control is NOT an accepted native R_mix341 proof DAG and has NO fixed-weight cost claim.

## Known hard-family ledger (mandatory source distinction)
Published control: connected 3-regular epsilon-expander G_H with H vertices, 3H/2 edge variables and odd total Tseitin charge, expanded as four signed proper 3-CNF clauses per vertex: 4H clauses, N=Theta(H log H) bits with polynomially bounded identifiers. For suitable expander families, ordinary DAG Resolution has exp(Omega(H)) size lower bounds via expansion/width (Urquhart 1987; Ben-Sasson/Wigderson 2001) under that proof model. The same parity constraints permit linear-size GF(2) *semantic* refutation and specialized polynomial-time/logspace decision, so no R_mix341 or arbitrary SAT lower bound is inferred. This run's F_k is **only a deliberately easy counterexample/control** and must never be relabeled certified hard. Equisatisfiable 3-CNF encoding by itself is not proof-hardness preserving. Existing project LSPV-2/442, LSPV-4/485 and /486 already supply stronger original-clause implementation controls.

## Independent finite execution
Python source: experiments/arc/lspv2_485_equality_cofactor_independent.py, run locally and passed **10,967** assertions: exact all a,y pairs through k=6, all auxiliary completions through k=4, and five malformed-clause structural controls. Independent JavaScript: experiments/arc/lspv2_485_equality_cofactor_independent.cjs, executed as authored in a V8 isolate, passed **10,962** assertions under the corresponding exact enumeration. Both agree for k=1..6 on 2^k residual functions, 4^k models per cofactor, and a single projected SAT value. No randomness. Raw: results/raw/arc/2026-11-07_2218_LSPV2_485_COFAC_PROJECTION_RAW.json. The all-size theorem follows by the explicit literal identity, not by extrapolation of the finite checks.

## Resource and native-model accounting
Representation claim: any x-first exact OBDD stores at least 2^k distinct post-prefix nodes, which is a space lower bound **for that representation only**, not a lower bound on any Turing-machine SAT decider. Specialized canonical-recognition plus witness construction can be implemented with read-only source, O(log N) counters and repeated scans, polynomial time; no native FLMV execution or native R_mix341 checker was run. Logical truth-function count, explicit certificate bit cost, construction time, index/head reads, caches, failed policies, source parsing, verification, output, recomputation and all-phase WORK+INDEX peaks are **not interchangeable**. Executed host V8/Python test counts are not FLMV time/space measurements. No child portfolio A->Phi(A) was constructed, no t' or s' achieved, and no unrestricted computational lower bound obtained.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Full current root files checked. The stronger quantifier separation is a focused counterexample/representation warning to audit existing [P2-A4] evidence, without changing P2-A2/P2-A4/P2-A5 status, dependencies or the required universal transfer; no root tracker edit. Root main.tex returned an unreadable/empty payload for a nonempty blob and was not touched.

**Next falsifier:** For an authenticated published hard expander-Tseitin 3-CNF family, exhibit an exact solver-dependent computation-derived subproblem quotient, preserving SAT/UNSAT/malformed correctness, then prove *native* same-machine total construction/guest cost and recursive closure. This family is a shortcut control, not a new hardness premise. [P2-A2], [P2-A5] and [P2-A4] remain OPEN; P versus NP OPEN.
