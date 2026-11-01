# REVERSE-DUAL-PARAMETERIZED-CONTROLLER: five-role research handoff
Date: 2026-10-31 18:25 America/Los_Angeles (PDT).
Status: KNOWN THEOREM (cofactor/separator composition), PROVED/EXACT elementary target-language residual-hardness reduction, COMPUTATIONAL finite Y6 audit; all-input ARC, numerical FLMV transfer and P versus NP OPEN.

## Scope, source and obstruction
The sole NP-complete hardness target remains every *valid* duplicate-free, proper, clausewise-monotone 3-SAT-(2,2) formula of Döcker, plus rejection of every malformed source. Clauses contain three distinct same-polarity variables; each source variable has exactly two positive and two negative occurrences. All original clause IDs and variable/sign provenance are retained. Ordinary *residual cofactors are not generally members of this grammar*. This note does not construct an arbitrary-A to Phi(A) contraction, power-short children, or a target-normalizing re-encoder.

Exact obstruction: backward semantic labels SAT/UNSAT and exact separator masks cannot be supplied to a forward adaptive selector for free. They must be constructed by sound rules with acquisition, proof and machine costs.

## First exact theorem: dual cofactor backward equations
For an original valid source F, a coherent partial assignment p, and an unassigned original variable x, let R(F,p) be the original-source-authenticated simplified CNF. Define V(p)=1 iff some full assignment extending p satisfies every original clause F. Then
  V(p) = V(p union {x=0}) OR V(p union {x=1}),
  NOT V(p) = (NOT V(p union {x=0})) AND (NOT V(p union {x=1})).
Proof: every completion fixes x to precisely one of its two values. This is an elementary complete partition, with no assumption on the source's polarity or syntax. Terminal SAT requires a verified complete original-source witness; terminal UNSAT requires a sound contradiction/refutation, not an unsuccessful bounded search. A certified UNSAT child never makes its parent UNSAT without the other child.

An adaptive state is a finite deterministic source-indexed object
  z=(F,p,original clause IDs,derived proof DAG,input/index/head positions,cache,policy history,retained tapes).
The measured state-dependent parameter vector is
  kappa_obs(z)=(residual variables and clauses, certified tractable classes, actual separator/decomposition, certified backdoor/depth, affine rank when correctly recognized, live interface bits, source read count, policy tests/failures/switches, child sizes/query indices, proof/cache/replay bits, peak writable/index space, logical and physical XOR diagnostics).
Acquisition of each coordinate is charged. The unavailable semantic optimum (shortest witness, cheapest complete refutation, exact future cost, etc.) belongs only to an OFFLINE oracle benchmark, never a controller input.

## Second exact theorem: bidirectional separator certificate cover
Suppose a coherent cofactor is represented by r source-authenticated clause components F_i(X_i,B), where all interiors X_i are pairwise disjoint and may meet only in an explicitly verified separator B of size b. For a boundary assignment beta define
  P_i(beta)=1 iff there exists an assignment to X_i satisfying F_i|beta.
Then
  SAT iff exists beta in {0,1}^b with AND_i P_i(beta)=1,
  UNSAT iff for every beta in {0,1}^b there exists i with P_i(beta)=0.
Proof: assignments to distinct interiors combine uniquely once their shared boundary beta agrees. For UNSAT, each beta has a component for which no interior completion exists. The backward SAT object is a nonempty intersection of extension masks with local witnesses; the backward UNSAT object is a *complete cover* of the boundary hypercube by independently certified local refutations. A failed solver budget is not a certificate. The covering enumeration is exact even when individual local UNSAT certificates are long.

For a materialized explicit profile, at least 2^b boundary entries are represented; that is a representation-specific cost, NOT a universal machine lower bound. A streamed evaluator charges r*2^b actual component calls and their source reads, proof generation/validation, child encoding, and index movement. Space is peak live space, not the sum of all completed calls. Symbolic/compressed masks may save space/time, but their discovery and verification are charged. Neither small b nor a small final profile bounds the difficulty of a component, since b=0 is compatible with an arbitrary hard component.

## Third exact reduction: backward extendibility with one assigned bit remains NP-complete
Let EXT1 consist of pairs (G,p) with G a valid canonical target formula, p a valid coherent partial assignment fixing at least one variable, and some satisfying completion of G extending p. EXT1 belongs to NP (check grammar, assignment and clauses). Given an arbitrary canonical source F, construct the disjoint union G=F AND Y6' with fresh, properly renumbered variables, where Y6 is the valid eight-clause six-variable M22 control:
  (123),(145),(246),(356),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6).
Set p to fix the fresh Y6' variable corresponding to x1 to zero, leaving all other variables free. The fixed gadget has exactly 10 satisfying completions, so (G,p) is extendible iff F is SAT. Disjoint union preserves clause uniqueness, sign monotonicity, and the exact 2-positive/2-negative occurrence quotas. The construction is polynomial time; malformed F is mapped to a fixed invalid NO encoding after polynomial grammar checking. Hence EXT1 is NP-complete by the established NP-completeness of F's target language. This is an elementary reduction, not a new complexity separation.

Consequence: working backward from known terminal answers is an exact *proof-planning framework*. Treating full backward extendibility labels as free state features would smuggle in the original NP-complete decision problem. The theorem does not rule out a polynomial algorithm, since P versus NP is OPEN.

## Same-canonical-source SAT/UNSAT residual controls
Y6 is independently known to have 20 complete satisfying assignments, though neither all-zero nor all-one is satisfying (each falsifies 4 of 8 original clauses). For
  p_U=(x2=0,x3=1,x4=0,x5=0)
the only surviving original source clauses are
  C2=(x1), C3=(x6), C6=(not x1 OR not x6).
Split left {C2}, right {C3,C6}, boundary B={x1}. The left SAT profile is {1}, right SAT profile is {0}, and their intersection is empty. The exact UNSAT boundary cover is beta=0 -> C2 refuted, beta=1 -> (x6) AND (not x6) refuted. This refutes a partial cube in a SAT *parent*, not the original full formula.

For
  p_S=(x2=0,x3=1,x4=0,x5=1)
surviving original clauses are C3=(x6), C6=(not x1 OR not x6). With boundary B={x6}, left profile {1}, right profile {0,1}; their intersection {1} yields a complete source witness with x1=0,x6=1.

Exhaustive 3^6=729 coherent partial states: 529 extendible, 200 nonextendible. All 6*3^5=1458 choice points satisfy both dual backward recurrences. Separate independent bit-mask verifier confirmed the same figures without importing the producer. Disjoint Y6 and fresh Y6 with fresh x1=0 has 20*10=200 full witnesses, checking the reduction's satisfiable side. The previously certified canonical U198 UNSAT and V198 SAT fixtures remain both-label hostile controls; their large certificates were NOT rerun in this supplementary experiment. Do not confuse a residual UNSAT label with a canonical UNSAT source label.

Producer: experiments/arc/reverse_dual_2026_10_31/reverse_dual_exact.py
Independent checker: experiments/arc/reverse_dual_2026_10_31/verify_reverse_dual_independent.py
Raw summary: results/raw/arc/2026-10-31_1825_REVERSE_DUAL_PARAMETERIZED_summary.json

## Four falsifiers and verdicts
F1: FREE-BACKWARD-LABEL. Ask for exact SAT/UNSAT profile at an arbitrary nonempty partial source. FALSIFIED as a free parameter by the EXT1 NP-completeness reduction. This is not a conditional P!=NP theorem.
F2: BOUNDARY-WIDTH-ONLY. Give an arbitrary source as one component with B empty. Its interface width is zero and its interior SAT task is still NP-complete. FALSIFIED as a universal runtime bound.
F3: AUTOMATIC-TARGET-HEREDITY. The Y6 cofactor with three residual clauses is not a valid canonical (2,2) source. FALSIFIED for literal deletion/cofactoring as a target-child compiler. An explicit valid low-cost re-encoder remains OPEN.
F4: SAVED-NODES-IMPLY-SAVED-WORK. Existing LSPV-3 GATE286 reduced search nodes while increasing matching acquisition cost. FALSIFIED for that implementation; real time/space selection costs must be tracked.

## Parameterized adaptive controller, not an oracle
At every state: validate original grammar once with paid reads; apply sound certified terminals (empty clause, unit propagation, short conflict cores, actual complete witness); test tractable classes with actual recognition costs (2-SAT/Horn/dual-Horn/XOR), discovered backdoors and verified separators; choose a bounded action using *observable* parameters and charge unsuccessful trials; if certified decomposition is available, compute/prune exact boundary extensions with real recursive calls and proof provenance; otherwise branch on an original variable with BOTH ordinary residual children; combine SAT via OR and UNSAT via AND; use exhaustive fallback for total correctness. SAT and UNSAT certificate strategies may have distinct cost/depth parameters. Online controller actions cannot assume knowledge of the true value V(p).

A sequential abstract accounting upper bound for one explicit separator evaluator is:
  T <= T_validate + T_discover + T_policy + sum_beta sum_i [T_restrict(i,beta)+T_decide(i,beta)+T_check(i,beta)+T_access(i,beta)] + T_join + T_output.
  S_peak = max_t {all simultaneously live writable/index/proof/cache/ancestor/guest/selector bits at step t}.
If b=O(log N), discovery is polynomial and every local component is decidable uniformly in polynomial time with charged access, this route is polynomial on that CERTIFIED restricted family. None of these hypotheses has been proved for all canonical instances. Native FLMV time and space would require faithful bit-tape/index simulation and a hereditary ordinary-SAT machine; current Python work counters are OFFLINE.

## Relation to the single ARC/FLMV spine
The target remains a single uniform source-authenticated compiler Phi for arbitrary correct total SAT deciders A of unknown K,L:
  K' <= max(alpha,gamma+lambda*K), L' <= max(sigma,lambda*L).
The proposed (1.1,0.6,0.5,0.5) constants would conditionally approach (1.2,0.5), strictly forbidden by the actual FLMV region *if* Phi were constructed and the numerical SAT-to-canonical transfer/direct bound were proved. Neither follows from backward DP, clause hardness, or target NP-completeness. All malformed strings must reject; recursive residuals require correct ordinary-child polarity, verified low-overhead target re-encoding, or proof that Phi is an ordinary-SAT decider closed under recursive use. Do not treat previous alpha/lambda fixed-point algebra as a completed contraction.

## Corpus, literature and duplicate check
- Primary: Janosch Doecker, Monotone 3-Sat-(2,2) is NP-complete, 2019, https://arxiv.org/abs/1912.08032 .
- Primary: Dreier, Ordyniak, Szeider, SAT backdoors: Depth beats size, JCSS 142 (2024), https://doi.org/10.1016/j.jcss.2024.103520 .
- Primary: Gaspers et al., Backdoors into Heterogeneous Classes of SAT and CSP, AAAI 2014, https://doi.org/10.1609/aaai.v28i1.9111 .
- Primary: Ganian, Szeider, New width parameters for SAT and #SAT, Artificial Intelligence 295 (2021), https://doi.org/10.1016/j.artint.2021.103460 . In particular, conflict-graph treewidth alone is not a free FPT route.
- Primary: Fortnow, Lipton, van Melkebeek, Viglas, Time-Space Lower Bounds for Satisfiability, JACM 52(6) (2005), https://lance.fortnow.com/papers/files/tst.pdf .
- Project pre-existing and CREDITS: research/main/2026-10-30_0648_MAIN_HITTING-TREE-COMPOSITION-REFEREE222.tex already formalized sound interface DP with paid decomposition. research/agents/lspv-3/2026-10-31_0324_LSPV-3_INTERFACE_SOURCE_SELECTOR_GATE272.tex already diagnosed interface-policy acquisition. research/agents/lspv-3/2026-10-31_0529_LSPV-3_HORN_AFFINE_MIXED_GATE274.pdf documents adversarial mixed tractable components. research/agents/lspv-1/2026-10-31_1655_LSPV-1_ARC_MONOTONE_THREE_CORE286.tex already contains the Y6 partial contradiction. This handoff does NOT claim novelty for cofactor OR/AND, boundary composition, or local clauses; the incremental work is combining the exact two-sided certificate-cover interpretation, explicit one-fixed-bit hardness firewall and state-dependent controller contract in one auditable specification.
- Web searches (2026-10-31 PDT): "SAT dynamic programming tree decompositions forward backward messages"; "SAT parameterized backdoors heterogeneous Horn affine bijunctive"; "New width parameters SAT conflict graph"; "Döcker Monotone 3-SAT-(2,2)"; "FLMV SAT time space lower bounds". GitHub searches in j15marti/pnp: "forward reverse interface DP", "HITTING-TREE-COMPOSITION-REFEREE222", "SWAP6"; in github.com/openai: "SAT dynamic programming", "DPLL", "reverse dynamic programming". OpenAI results chiefly unrelated repositories or preprints, no directly applicable canonical target implementation identified. Absence of a search hit does not imply novelty.

## Five-role handoff, no schedule or role change
LSPV-1: prove the exact SAT/UNSAT dual proof-DAG invariant and the correct child-polarity theorem, then test any proposed hereditary target compilers.
LSPV-2: implement source-authenticated dual-mask composition with per-action measured acquisition/query costs and checked ordinary/target child conversions.
LSPV-3: seek truly observable *dynamic* certificate parameter bounds, including SAT/UNSAT asymmetric profiles; test mixed Horn/XOR, high-width easy orbits, no-free-selector controls.
LSPV-4: charge indexed source/child accesses, variable-length encodings, simultaneous retained tape and FLMV transfer; challenge target blowup.
LSPV-5: independently audit certificate-cover quantifier order, DELAY/COPY/RECOMP wrappers, true machine costs and contradictory assumptions.

No existing automations were created, resumed, disabled, or rescheduled. This is a coordination-only append; the role-owned main.tex regions remain unchanged for their owners to review. P versus NP remains OPEN.
