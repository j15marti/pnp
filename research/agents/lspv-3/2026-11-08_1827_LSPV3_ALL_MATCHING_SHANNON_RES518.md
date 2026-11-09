# LSPV-3/518 | Uniform Shannon Resolution upper bound on all Q_n matching CNFs

**November 8, 2026, 18:27 PST | Route B | PROVED/RESTRICTED (ordinary Resolution) + COMPUTATIONAL (independent finite controls). P versus NP OPEN.**

**Exact tracker IDs:** new [P2-L3-518]; refines [P2-L3-517], [P2-L3-516], [P2-D3], [P2-C3]. [P2-D1], [P2-C3], [P2-B1], [P2-B2] all OPEN. Route A and proof1 unaffected.

## IDEA, registered falsifiers

Hypothesis: the four-record external XLRUP versus m-paid-node observation in [P2-L3-517] does NOT entail superpolynomial cost relative to original input length on this matching family, because EVERY Q_n matching CNF has an ordinary-Resolution proof with fewer than 2m paid nodes, even without access to XOR or DEF.

Falsifiers: (1) a matching-edge clause is falsified by other than exactly its two endpoints; (2) a Shannon split needs an uncharged weakening/discharge or wrong-pivot RES; (3) legal sharing evades the m-1 source-ancestry floor; (4) some matching invalidates the directional upper bound. All four falsifiers were addressed within the separately declared ordinary-RES model, not the historical accepted-byte checker.

## SEARCH, sources and scope

Read both complete current root trackers, current issue #3 and the governing 2026-11-02 five-role handoff (historical commit 4e29ed7646f484707767acb6e63ec5f38afd98a8), AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md. Reused LSPV-3/516 and /517, peer LSPV-1/520 and /521, red-team LSPV-5/448. Historical declaration: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. Its mathematical RES is ordinary binary resolution; the original accepted-byte grammar is still unavailable.

Actual Grok GROKPROOF/2026-11-08_1130_PROGRESS.md blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70 and Claude research/agents/claude/world-ledger/README.md blob de75a371ce3143a4495e6892df7fb04794a6b708 were read. Neither provides the native mixed grammar.

Pinned relevant current external files:
- konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json 93b77ed3d8fe456f81c690035f45f07910a247f2. Its scope is a finite-machine model and conditional/formal status, not R_mix341.
- blkph0x/p-vs-np-proof-research README.md f397a7747eaca82df3d754d0a4b4bab1fe10f814 and METHOD_INDEX.md 18d693ea71dfa433370eb7afbebc3106e32f03e5, REVIEW_ADDENDUM.md 6a7cc2f8962d3fcfcfc1778b1d3d8f5dc8d56d70; bounded/promise and parity-polytope controls only.
- meelgroup/frat-xor/format.md 986a21aa92b62f844ef1fce852193142c41b2b1f specifies external multi-hint XLRUP; tanyongkiam/cake_lpr/README.md e94f45e9aa000cd9ada12f4c771ac9daf28fe53c; peitl/short-proof/README.md 93d2090dba9739bc4983c65ea639a24e1f5e0fab. External formats/checkers do not supply missing native conversion. openai/math/README.md cc5b0a03bca6c742f045d683b6647a6f44ef2cae and anthropics/formal-math/README.md 1df53bfc14a022088d1b5757698f692bf79390b4 were checked for claimed/model scopes.
- Primary literature rechecked by web search: Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 revised 24 October 2026 (fixed-r, opposite-characteristic syntactic Res(PC), NOT historical mixed); Urquhart, JACM 1987; Ben-Sasson and Wigderson, JACM 2001; Cook and Reckhow 1979. A separate Google-branded portal and the authoritative R_mix341 checker were not used.

## Exact original-source family and theorem

Let M be any perfect matching of Q_n, n>=2. Put m=2^(n-1). Each edge {a,b} differs in one coordinate j. Introduce its ORIGINAL signed clause

$$
C_{\{a,b\}}=\bigvee_{i\ne j}
\begin{cases}
x_i,&a_i=0,\\
\neg x_i,&a_i=1.
\end{cases}
$$

This width-(n-1) clause is falsified at exactly a and b. Every assignment is in exactly one matched edge, so exactly one original clause fails at every assignment. F_M is minimally UNSAT, with exactly two satisfying assignments upon deleting any clause. Only n=4 is strict 3-CNF; higher n is a focused proof-conversion control, NOT a claimed asymptotically hard 3-SAT family.

Let d_j(M) count matching edges in coordinate j, so sum_j d_j(M)=m. Define W_Res as the minimum distinct paid binary Resolution inferences over ALL valid original-source shared-DAG refutations, with unit inference weights and free source clauses.

**Theorem 518.1, PROVED/RESTRICTED:**

$$
\boxed{
m-1\le W_{\mathrm{Res}}(F_M)
\le 2m-1-\max_jd_j(M)
\le (2-1/n)m-1.
}
$$

**Proof.** The lower bound is the already established [P2-L3-517] binary source-capacity lemma: a connected source-ancestry DAG with m indispensable source vertices and q paid binary nodes requires at least m+q-1 ancestor edges, but has at most 2q, hence q>=m-1. This holds with sharing and reconvergence.

For the NEW upper bound, choose the last decision variable j maximizing d_j. Traverse the complete n-level binary assignment tree; at leaf a reference exactly the original source clause for a's matching edge. In each partial assignment context, inductively maintain a derived clause falsified by ALL completions of that context and containing only already fixed variables. If one child clause does not mention the split variable x, reuse THAT existing clause as the parent (no new inference, case/discharge, or weakening). Otherwise the child clauses contain the complementary literals x and not x, so one sound, correctly oriented ordinary Resolution yields a clause falsified by the entire parent context. Deduplicate same-sign resolvent literals by standard set representation; never change the rule weights. At the empty prefix the conclusion is the empty clause.

Of the 2^n-1 possible binary-tree internal nodes, at least d_j have two leaf siblings that are the endpoints of a matching edge in direction j. These siblings reference the SAME original clause, so require no inference; more aliases can only lower the paid count. Prune unreachable construction steps and renumber every remaining charged inference in topological order. Thus q<=2m-1-d_j. The maximum direction has at least m/n edges. This constructs a tree-like RES proof of depth <=n, valid as an upper control even against a more general shared-Resolution minimum. Branches exist in the proof-generation algorithm only. The emitted proof contains no case-split or assumption-discharge steps.

## ITERATE: execution, independent falsification and exact resources

Executed the published ECMAScript in V8, then re-fetched its exact Git blob and re-executed. Exhaustively enumerated all 272 Q4 matchings and all 24 GLOBAL variable orders for each, testing each original clause, all 16 assignments, signed pivots, resolvents, source ancestry, acyclicity, final empty conclusion and the stated bounds. Best GLOBAL-order constructed-cost histogram: 136 with 7 nodes, 96 with 9, 32 with 11, eight with 13. These are NOT exact unrestricted Resolution minima. In particular, [P2-L3-516] gives 232 seven-node Q4 proofs with less restricted branching; the statistics are not in conflict.

34 deterministic larger matching controls at n=5..8 also passed. There were 1,224 verified deliberate rejections of corrupted pivots, conclusions, original source polarity and malformed matching involutions. Independently written/executed Python checked all 272 Q4 matching sources plus 16 further n=5..8 controls using a different ordinary-RES producer and checker. Its heuristic-order counts differ as expected because it does not search all orders; ALL matching and theorem assertions passed. These finite checks support the theorem; the proof, not enumeration, covers all n and matchings.

Published executable path experiments/arc/lspv3_518_qn_shannon_res_bound.cjs, blob 5e3ffa153a66b59775ff3d03cf741cf7f2ebdfd8, and raw results results/raw/arc/2026-11-08_1827_LSPV3_518_QN_SHANNON_RES_RAW.json, blob 13ebfd07da000c42e0ff63e5b6ffd9e6f83f287b. Independent Python and JSON remain separately attached reproduction artifacts; neither is falsely represented as published in GitHub. No authoritative R_mix341 or CakeML checker was executed.

**Work, bits, depth and machine space.** Original explicit source contains m(n-1) signed literal occurrences and O(mn log n) ASCII DIMACS bits. The certificate construction visits 2m leaves and computes at most 2m-1 inferred clauses, with O(mn^2) conservative naive word/bit-work accounting including clause-copy normalization, excluding prior research discovery. A proof-trace-only encoded packet storing original source refs, two parent refs and pivot uses O(m log m) bits beyond source; an explicit per-line signed-literal packet uses O(m(n log n+log m)) bits. A fully materialized verifier retains O(mn) literal entries plus input/output packets and uses polynomial parsing, recomputation and checking time. Its ideal weighted critical path is at most n under an unbounded-processor model; that does not measure sequential time or actual peak space. Construction, input parsing, output, independent checking, wasted exploratory global orders and corrupted tests were executed and are extra costs outside W_Res. Native TM steps, host RSS and same-FLMV-machine charge were not measured. No free lookup, oracle, or auxiliary facet is invoked.

## Family, theorem, known shortcut, remaining transfer

| Family and encoding | Hardness theorem and system | Verified applicable shortcut | Missing transfer |
| --- | --- | --- | --- |
| Odd cubic expander Tseitin, 4h proper signed 3-clauses, 3h/2 edge vars | Exponential ordinary shared-DAG RES for appropriate expander graphs, Urquhart 1987 and BSW 2001, not all-machine hardness | Declared SOURCE/AND3/XOR upper 4h-1 paid nodes, prior [P2-L3-509] | Authenticate all historical mixed rules [P2-D1]/[P2-C3] |
| Opposite-characteristic mod3 cubic Tseitin, 57h/2 padded strict3 sources, 9h/2+1 vars | Pang 2026v2 exponential fixed-r syntactic Res(PC_r/F2), under preprint assumptions | LSPV-1/520 ER2 O(h log h) schema with LSPV-5/448 zero-factory repair; full exact native packet OPEN | DEF/RES/LOCAL-CONVERT ports and all-legal normalization |
| Q_n perfect-match CNF, m width-(n-1) clauses, n=4 strict3 only | Source indispensable gives m-1 binary-node floor; four-record XLRUP external format [P2-L3-517] uses 2m original hint IDs | NEW uniform ordinary RES at most (2-1/n)m-1 paid nodes, polynomial in original input size | No XLRUP-generic simulation or full historical native acceptance established |

**Interpretation:** The prior four-external-record versus m-native-node contrast is an inference-record *arity* distinction, not a superpolynomial source-length separation on this family. The result does NOT prove a universal polynomial normalization from arbitrary XLRUP traces into R_mix341.

**Safe-publication limitation:** root main.tex current blob 63b54c9988cc83533472a05c25bda2ab48b5e4ca returned ZERO content bytes. No partial overwrite. Repository-scoped preflight was not run on an actual local checkout because the isolated runtime cannot fetch the repo. All rules, historical weights, five tasks, identities, schedules, enabled states and two-Route-A/three-Route-B allocation remain unchanged.

**Next decisive step:** recover and validate original accepted-byte RES→AND3/LOCAL-CONVERT/DEF original-source provenance, private/exported ports, all paid facets and assumption discharge. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. **P versus NP remains OPEN.**
