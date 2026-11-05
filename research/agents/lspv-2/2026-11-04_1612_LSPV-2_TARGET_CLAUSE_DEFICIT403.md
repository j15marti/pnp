# LSPV-2/403: Target-clause codimension improves bounded-port Resolution reflection

**November 4, 2026, America/Los_Angeles.** Role: PNP SAT-Circuit Reduction Builder (unchanged). **Status:** PROVED/EXACT for a declared source-only Resolution clause-consequence lemma and source-essential R_mix341 minimum; COMPUTATIONAL independent finite controls; CONDITIONAL for application to the extensional-port subgrammar; OPEN for full R_mix341 transfer, B1/B2/B3 and P versus NP. Independent specialist proof review is pending.

## IDEA (before searching) and falsifiers

LSPV-2/402 replaces each semantically justified bounded-original-support node by at most 3^k ordinary Resolution inferences. Proposal: when a semantic node exports **one proper original-variable clause C**, count only **unfixed** original variables d=k-|vars(C)|. Prediction: a sound consequence of a k-variable CNF can be represented by a *subclause* of C after at most 2^d-1 strict Resolution inferences without weakening, and this sharper bound is tight under all legal R_mix341 operations for a deliberately constructed minimally UNSAT source.

Falsifiers: F1, a valid single-clause consequence requires more than 2^d-1 Resolution nodes; F2, single-clause source essentiality does not survive arbitrary shared DAGs, gate definitions, GF(2), or nonmonotone steps; F3, falsely charging an exponential in d as an exponential in encoded input bits N; F4, treating multi-clause semantic factors or opaque LOCAL-CONVERT circuit payloads as single-clause outputs. The last is an explicit scope restriction, not an assumed normalization.

## SEARCH: exact corpus, primary research and previous work

Read **first** the user-approved Nov.2 five-role directive research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, then issue #3, AGENTS.md (blob 19656af1), CODEX.md (754999f5), .codex/skills/pnp-research/SKILL.md (b8df83a7), fixed R_mix341 definition research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (c87acd11), own previous /402, peer LSPV-3/404 (0a04bf6a), /403 (6aa16021), LSPV-1/401 (e1049a6e), and Red Team REFEREE315 and REFEREE333. The local 3^k saturation argument is **already proved** by LSPV-3/401 and reused in LSPV-2/402. The source-fan-in m-1 lower bound is **already proved** by LSPV-2/341 and retained. What is new in this project run is the clause-specific 2^d translation, its tightness against every unit-paid binary-premise mixed proof, and the refined local-reflection inequality below; it is not claimed as an academically novel proof-complexity technique.

Read actual GROKPROOF/2026-11-04_2315_PROGRESS.md (blob f5b8ef62), reporting an OPEN fully charged universal ARC resource-contraction map, and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6), proving restricted sequential-access lower bounds. Neither proves B3. Grok's Omega(N^1.1) versus N^(1.1+o(1)) inference is not accepted as a strict contradiction.

Web queries: "Haken intractability resolution 1985", "Cook Reckhow 1979 relative efficiency propositional proof systems", "Kiesl Rebola-Pardo Heule Biere 2020 simulating strong practical proof systems extended resolution", "Fleming Grosser Pitassi Robere Provable Reductions in TFNP 2026", and "bounded semantic inference local truth table resolution simulation 3^k". Read publisher pages for Cook--Reckhow and Kiesl et al. and the text of Fleming et al. (2026). Cook--Reckhow's theorem concerns existence of SOME p-bounded proof system under NP=coNP. Kiesl et al. prove polynomial ER simulations of DRAT/DPR; they do not furnish a polynomial ordinary Resolution backtranslation. Fleming et al. establish a relation between implicit Resolution and G1, with certified correctness, not a free implicit-conversion rule. Direct Google-branded search was unavailable: general web search was performed instead. Authenticated github.com/openai search query "SAT resolution proof checker" yielded unrelated matching repository content, no claimed new theorem or compiler. OpenAI repository implementations were not used as a mathematical premise.

## Fixed model and proved clause-target lemma

Keep original R_mix341: explicit valid signed-index CNF; original clauses as free authenticated leaves; every distinct RES, exact AND3, binary GF(2), justified LOCAL-CONVERT, or conservative binary DEF node has cost one; any new inference has at most two incoming proof premises. Auxiliary definitions and temporary growth are legal. The precise full LOCAL-CONVERT payload grammar is still unresolved, so the next theorem is about **ordinary Resolution**, not all native R rules.

**Lemma 403.1 (single-clause Resolution consequence, PROVED/EXACT).** For EVERY finite proper-clause CNF Gamma over a k-variable set X and EVERY proper target clause C using c distinct variables of X, if Gamma models C, there is a strict source-authenticated shared-DAG Resolution derivation, without weakening, of a clause D subseteq C requiring at most

$$
\boxed{2^{k-c}-1}
$$

new binary Resolution inference nodes. k and c refer to distinct original variables, not exported private ports. The input may be SAT or UNSAT; when C is empty and Gamma is UNSAT, this is a refutation. A consequence represented by a stronger D is admissible for subsequent semantic entailment.

**Proof.** Assign the c variables of C uniquely so that C is false. Branch on the remaining d=k-c variables. At each complete leaf, the assumed entailment guarantees that some original clause of Gamma is false; choose such an original source clause. Every literal of this chosen clause lies in the full-assignment blocker. Process the binary assignment tree bottom-up. When the clauses returned by two children respectively contain the complementary signed pivot literals, resolve and delete the pivot, producing a proper clause. If either returned clause lacks its branch pivot, inherit that clause without a new inference. By induction, the returned clause at each internal node lies in the union of C and the blocker of its path, and is entailed by Gamma. At the root it is a subclause of C. There are at most 2^d-1 internal nodes, and no step invokes weakening, semantic oracle, or a free derived axiom. This is standard DPLL-to-Resolution lifting, made explicit for a *specific* target clause.

**Corollary 403.2 (restricted refinement of /402).** In the /402 extensional-port and complete adaptive gate-collapse setting, suppose r nodes are strict RES, a set S_1 of other semantic nodes each exports **one** proper clause C_j, and S_f denotes the remaining factor/equation nodes. After every leaf substitution, let k_j count the union of ORIGINAL supports of the antecedent relations and conclusion and c_j the number of distinct original literals in C_j; let d_j be the maximum (k_j-c_j) over leaves. For factor nodes let k_j be the maximum full original support. Then:

$$
W_{\mathrm{Res}}(F)\le L\left[r+\sum_{j\in S_1}(2^{d_j}-1)+\sum_{j\in S_f}3^{k_j}+1\right]-1.
$$

The proof repeats /402, using Lemma 403.1 for one-clause nodes and /401 saturation for multi-clause factors. It is conditional on the SAME extensionality, substitution, justified-port, source-authentication, and no-free-hidden-wire requirements as /402. A compact original-support-independent circuit payload does NOT become free. For large c_j, this improves the previous per-node 3^{k_j} bound; if d_j=0, no paid Resolution step is required because some antecedent clause already subsumes C_j.

## ITERATE: tightness and exact finite/global mixed-calculus minimum

For every integer d>=1 let Y=(y_1,...,y_d), u fresh, and for a in {0,1}^d write B_a(Y)=OR_j(y_j if a_j=0 else NOT y_j), the signed clause falsified precisely by a. Define

$$
\Gamma_d=\bigwedge_{a\in\{0,1\}^d}(u\lor B_a(Y)),\qquad
Q_d=(\neg u)\land\Gamma_d.
$$

Gamma_d entails (u). The 2^d clauses of Gamma_d are collectively indispensable for this entailment: removing the one indexed by a permits the assignment u=0,Y=a. Their binary-merge Resolution derivation of (u) has exactly 2^d-1 paid nodes. Every binary-premise derivation of (u) or a subclause must use all 2^d original source clauses and therefore has at least 2^d-1 paid nodes. **The 2^d-1 bound in Lemma 403.1 is sharp.**

Moreover, Q_d has m=2^d+1 **indispensable** sources. The same deletion witnesses work for each Gamma_d source, and deleting (NOT u) permits u=1. Any legal R_mix341 refutation DAG must include all m leaves because each is indispensable, and an at-most-binary-premise DAG joining m distinct source ancestors into a single contradiction requires at least m-1=2^d paid nodes, EVEN with sharing, GF(2), DEF, temporary growth and other legal binary-premise moves. A strict Resolution merge tree for Gamma_d, followed by one resolution with (NOT u), attains this bound:

$$
\boxed{W_{R_{\mathrm{mix341}}}(Q_d)=W_{\mathrm{Res}}(Q_d)=2^d}\quad(d\ge1).
$$

**Warning:** Q_d is NOT an asymptotically hard SAT family in encoded length. There are 2^d+1 explicit clauses of length O(d), hence conventional signed-index source length N_d=Theta(d 2^d log(d+2)). The exact lower bound 2^d is at most linear in source-clause count and **does not** imply superpolynomial Wbar_R or machine hardness. Its only purpose is a tight test of the proposed clause-target transfer rule.

## Verification and model controls

Python independent producer: exhaustive hypercube instances d=1,...,6, separate resolution replay certificates for Gamma_d=>u, all 2^d+1 source deletion SAT witnesses, both original UNSAT and deletion-SAT labels, and six malformed/corrupted attempts rejected. Its certificates for d<=4 and SHA-256 digests for d<=6 are in the raw JSON. Additional entailed-clause controls include unit, binary and empty targets. Independent Node.js checker: enumerated all 256 CNF subsets of the 8 proper nonempty signed clauses on two variables, all 9 proper target clauses, **1,857** entailment cases certified, with **555** compiled RES nodes overall. It independently rebuilt and checked Q_d for d=1,...,6 and found exact paid minima 2,4,8,16,32,64 via source indispensability. No discrepancies. These are COMPUTATIONAL controls; universal proofs are given above. Malformed source and forged-pivot cases are rejected; an UNSAT derivation on any SAT control is unsound.

Logical distinct-node count and physical computation are separate. A naive proof compiler scans up to |Gamma| encoded bits at each of 2^d leaves, performs literal/index accesses, generates and verifies at most 2^d-1 new clause records, and writes up to O(2^d k log(k+|Gamma|+2)) bits. An eager implementation can require O(|Gamma|+2^d k log(k+|Gamma|+2)) peak writable bits, not free RAM; streaming/recomputation can reduce this at different costs. A paid-node optimum does not pay the optimizer's discovery cost. If any FLMV conversion uses these numbers, it must separately charge all phases and keep s'<=max{rho,eta,lambda,lambda*s}, with rho>=1 if N-bit preprocessing is allocated.

## Established lower bounds and actual bridge effect

Haken (1985) establishes: for constants c>0,h0, EVERY h>=h0 and EVERY ordinary unrestricted shared-DAG Resolution refutation of explicit unary PHP(h+1,h), with h(h+1) variables, m_h=(h+1)+h*binom(h+1,2) clauses and N_h=Theta(h^3 log(h+2)) signed indexed source bits, has >=2^(ch) lines. It says NOTHING directly about arbitrary uniform SAT algorithms or R_mix341. Cook (1976) gives polynomial Extended Resolution PHP refutations. The clause-target refinement applies only to legal typed fragments, so it cannot retroactively exclude ER or wide GF(2) shortcuts.

B1/B2/B3 remain unproved for R_mix341. No polynomial-cost reflection from unrestricted compact representations to ordinary Resolution has been established. The next decisive step is to authenticate full LOCAL-CONVERT output types and distinguish single-clause conclusions from multi-clause and opaque-circuit conclusions; then either prove a polynomially charged native compiler or produce a legal mixed-rule counterexample. Preserve exact five roles and schedule, do not modify calculus.

## Paths / publication

Role-owned standalone report: research/agents/lspv-2/2026-11-04_1612_LSPV-2_TARGET_CLAUSE_DEFICIT403.md.
Producer: experiments/arc/lspv2_403_target_clause_producer.py. Independent checker: experiments/arc/lspv2_403_independent_checker.js. Raw: results/raw/arc/2026-11-04_1612_LSPV2_TARGET_CLAUSE403_raw.json and _independent.json. Handoff: research/coordination/2026-11-04_1612_LSPV2_TARGET_CLAUSE403_FIVE_ROLE_HANDOFF.md. Root main.tex readback returned zero content despite a nonempty SHA; it must NOT be overwritten on a partial/empty retrieval. Repository reconciling is therefore documented as blocked, pending safe full-blob access.

**P versus NP remains OPEN.**

## References

[1] Haken, *The Intractability of Resolution*, Theoretical Computer Science 39 (1985), 297-308, DOI 10.1016/0304-3975(85)90144-6.
[2] Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4) (1976), 28-32.
[3] Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, Journal of Symbolic Logic 44(1) (1979), 36-50, https://doi.org/10.2307/2273702 .
[4] Kiesl, Rebola-Pardo, Heule, Biere, *Simulating Strong Practical Proof Systems with Extended Resolution*, Journal of Automated Reasoning 64 (2020), 1247-1267, https://doi.org/10.1007/s10817-020-09554-z .
[5] Fleming, Grosser, Pitassi, Robere, *Provable Reductions in TFNP*, 2026, https://arxiv.org/abs/2606.27931 .
