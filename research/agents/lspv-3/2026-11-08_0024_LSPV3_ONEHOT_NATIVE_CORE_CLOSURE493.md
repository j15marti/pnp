# LSPV-3/493 | One-hot Tseitin is unrefutable in the SOURCE/AND3/XOR 3-original-coordinate subgrammar

**2026-11-08 00:24 PST | Route B, certificates | PROVED/RESTRICTED + COMPUTATIONAL; historical mixed checker and full mixed system OPEN; P versus NP OPEN.**

**IDs:** new [P2-L3-493]; evidence/refinement to [P2-D1], [P2-C3], [P2-L3-492] and family ledger [P2-F13]. [P2-B1] and [P2-B2] remain OPEN. Read full /proof1.txt [P1-00], [P1-01] and /proof2.txt, and current issue #3 before the investigation. The two existing Route-A and three Route-B agents, all rules and historical weights are unchanged.

## IDEA, four falsifiers stated before SEARCH

Hypothesis: the exact original one-hot q=2 cubic Tseitin source from Pang §7.1, unlike the bit-encoding used in the recovered /341 SOURCE/AND3/XOR packet, admits no refutation in the **distinct mathematical SOURCE/AND3/XOR subgrammar** with each AND3 input union limited to three original one-hot Boolean variable identifiers, factor-only AND3 parents, exhaustive local exact-affine aliasing, and binary XOR of already authenticated affine rows. This would isolate the genuine typing need for the RES-to-AND3 interface in [P2-L3-492].

F1. Two distinct original vertex forbidden-value clauses or one vertex and one edge clause have support union <=3, allowing a local merge. F2. An isolated vertex three-literal clause itself has an exact nontrivial affine alias. F3. Edge-local factor closure creates a row involving another edge or the contradiction 0=1. F4. The recovered /341 executable authenticates arbitrary original one-hot source clauses and the RES->AND3 port. F1-F3 are disproved in the stated mathematical subgrammar by the theorem below and finite checks. F4 does not hold as an accepted-byte claim: the recovered checker is hardcoded for one-bit signed cubic Tseitin and handles SOURCE/AND3/XOR only; this run makes **no historical input-acceptance claim**.

## SEARCH: original families, actual rule interfaces, peers, and outside controls

The governing five-role handoff (historical commit 4e29ed7646f484707767acb6e63ec5f38afd98a8), latest issue #3 comments, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md were reviewed. Actual prior work includes LSPV-3/492 at research/agents/lspv-3/2026-11-07_2320_LSPV3_ONEHOT_MIXED_SHORTCUT492.md (blob f968a33dcdc75c53e11d9ca2849412a1f1b59189); LSPV-1/498 at research/agents/lspv-1/2026-11-08_0004_LSPV1_RANDOM3_LOCAL_MIXED_RESPC_TRANSFER498.md (blob c99ae09691941c5e2b5a5f2d1dee01da8065dfd8); LSPV-1/481 at research/agents/lspv-1/2026-11-07_0956_LSPV1_DIRECT_SYNTACTIC_LOCAL_BACKSIM481.md (blob cd2ec52e7c0fe352a44d55b8b6dab71637ff08c7); LSPV-5/413 at research/main/2026-11-07_0901_MAIN_HISTORICAL_341_CHECKER_SCOPE_REFEREE413.md (blob a80ba04046046f7b2c71aa451547474bea62d269); LSPV-5/427 at research/main/2026-11-07_2253_MAIN_COMPLETION_ROBUST_TSEITIN_REFEREE427.md (blob b0bb548ab6c0a4d8b767ccc202bd753d5997fbf5); and the original checker experiments/arc/lspv2_341_independent_verify.js (blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0).

Actual Grok file GROKPROOF/2026-11-08_0320_PROGRESS.md and Claude research/agents/claude/world-ledger/README.md plus research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex were inspected as assessments, not theorem authority. The expanded mandatory repositories were actually fetched: konard/p-vs-np README.md (blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95) and scripts/proof_status.json (blob 93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research README.md (blob f397a7747eaca82df3d754d0a4b4bab1fe10f814), METHOD_INDEX.md (blob 18d693ea71dfa433370eb7afbebc3106e32f03e5), PROOF_PORTFOLIO_BRIDGE_REPORT.md (blob 22215cec16cc25bc8e2fa400740418003583c9bc). These include only model-limited claims. Reviewed meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f; tanyongkiam/cake_lpr/README.md blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c; peitl/short-proof/README.md blob 93d2090dba9739bc4983c65ea639a24e1f5e0fab; and openai/math/README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae. Their checkers are not the historical /341 grammar. The Google-branded standalone search interface was not available; indexed web search was actually used, including Pang, Tseitin/Res(PC) and FRAT-XOR source queries. No outside CI or formal proof assistant was executed.

Primary theorem: Shuo Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, October 24, 2026, §7.1, Theorem 7.2(b), Corollary 7.3, https://arxiv.org/html/2610.00837v2 . The theorem gives exp(Omega(h)) for the q=2 one-hot cubic-expander formula in syntactic Res(PC_r/F_p) for fixed r and **p different from 2**. This is a restricted opposite-characteristic proof-size bound; the same-characteristic upper bound is linear. It is not a machine-time bound, nor independently reproduced here.

## Source and separate fragment, exact scope

Let G=(V,E) be any **simple cubic** graph with h vertices and E=3h/2 edges, and b:V->{0,1} have odd total parity. The original Pang one-hot source T(G,b) uses **2E=3h** Boolean variables a_(e,0),a_(e,1). For each edge there are two clauses

$$
(a_{e,0}\vee a_{e,1}),\quad(\neg a_{e,0}\vee\neg a_{e,1}).
$$

For each vertex v, each forbidden assignment s in {0,1}^3 of wrong parity contributes the original width-three clause

$$
D_{v,s}=\bigvee_{j=1}^3\neg a_{e_j,s_j}.
$$

The source has 2E+4h=7h original clauses of width <=3, with explicit indexed length O(h log(h+2)). Odd charge is UNSAT by summing parity at vertices; even charge has 2^(E-h+1) models when G is connected. **This is Pang's one-hot original formula, not an equivalent strict-three one-bit replacement.**

Define C_core^1hot as a separately specified mathematical inference subgrammar: source clauses are factors; a paid binary AND3 may conjoin two factor parents only when the union of their **original one-hot variable identifiers** has size at most three, yielding their exact Boolean conjunction on that union; it may export a GF(2) row only if the factor truth table equals that equation on ALL local assignments; a paid binary XOR may add two already exported affine rows. XOR outputs do not become factors. There is no RES, LOCAL-CONVERT, DEF, subclause weakening, branch/discharge, source-model-only projection, semantic oracle, or paid or free new original axioms. Arbitrary acyclic sharing and rebalancing are allowed. This subgrammar is sound and effective but **incomplete**, and is not the complete preselected R_mix341.

## Theorem 493.1: complete factor closure and affine-row obstruction (PROVED/RESTRICTED)

For every simple cubic G as above, all factors derivable in C_core^1hot are exactly the **4h isolated vertex source factors** and, for each edge e, the three edge-local factors: its positive exactly-one source clause, its negative at-most-one source clause, and their conjunction. No other nontrivial factor can arise. Hence the number of distinct factor predicates in the exhaustive closure is

$$
4h+3E=4h+\frac{9h}{2}=\frac{17h}{2}.
$$

The only nontrivial exact affine-row outputs are the E equations

$$
a_{e,0}\oplus a_{e,1}=1,\qquad e\in E.
$$

They are independent because their supports are pairwise disjoint. Their entire GF(2) span has 2^E rows including the zero equation 0=0, but never 0=1. Thus **no refutation of the odd UNSAT one-hot source exists in C_core^1hot**, irrespective of the number of allowed nodes, sharing or reconvergence.

**Proof.** (i) Two different forbidden patterns at one vertex have even nonzero Hamming distance, hence at least two indicator changes and support union at least five. At different vertices of a simple graph, their support triples overlap on at most one common indicator, again union at least five. (ii) Each vertex source clause uses one indicator on three distinct edges; adding either edge exactly-one source pair adds the opposite indicator and raises the union to at least four. Different edges' two-indicator sources have union four. (iii) Thus the only distinct compatible source-factor pairs under the support<=3 rule are the two edge clauses on the same edge. Their conjunction is the XOR-equals-one predicate; further conjunction with either parent changes nothing. All other local AND3 steps reproduce a prior factor. (iv) A single proper width-three clause has seven satisfying local assignments and cannot equal a nontrivial affine equation (whose truth set has half the assignments). Either edge source clause has three satisfying assignments out of four and is likewise nonaffine. The two edge clauses conjoined have exactly two satisfying assignments and equal the displayed edge equation. (v) Each edge row contains its own pair of variables absent from every other row, so no nonempty XOR combination has zero coefficient vector. In particular the contradictory zero-mask, RHS-one equation is unreachable. QED.

**Important qualification:** This is a *typed relative-incompleteness theorem* for the named fragment. It does NOT establish an infinite minimum for the **sound, complete historical** R_mix341, does NOT prove an all-mixed [P2-B1] lower bound, and does NOT show that every hypothetical completion lacks a short derivation. In fact, [P2-L3-492] provides a 10h-1 paid-node original-source R_ext proof once RES-derived clauses can be used as AND3 factors. The distinction is the missing interface itself.

## ITERATE: independent finite certificates and hostile controls

Python separately implemented whole-source enumeration restricted to exactly-one edge assignments, complete local truth tables, closure of ALL compatible factor pairs, exhaustive exact-affine alias checks, and all combinations of the available edge rows for K4, K3,3, Cube and Petersen. Result: **7,392 assertions, 4 hostile controls rejected**, all passed. Host: 1.84 s, peak RSS 96,264 KiB. Independent Node.js implementation (different factor enumeration and row checks) passed **4,691 assertions, 4 controls rejected**; host: 0.05 s, peak RSS 33,036 KiB. The GitHub-published V8-compatible script was independently executed from its retrieved bytes and passed **37,510 checks, 4 controls rejected** across four graphs. K4/K3,3/Cube/Petersen respectively have 28/42/56/70 original clauses, 34/51/68/85 exhaustive factor predicates, 6/9/12/15 edge equations, 0 odd-charge models and 8/16/32/64 even-charge models. These finite checks corroborate the symbolic theorem; they do not replay Pang's asymptotic lower-bound proof or the historical mixed checker.

Executable: experiments/arc/lspv3_493_onehot_source_and3_xor_closure.js. Raw: results/raw/arc/2026-11-08_0024_LSPV3_493_ONEHOT_LOCAL_CORE_RAW.json. An independently written Python implementation, second Node.js checker, raw outputs and SHA-256 hashes are retained as local reproducibility artifacts. The published code is not presented as the original historical checker.

## Work, depth, bits, and algorithm resources

The closure has O(h) distinct factors and E independent primitive affine rows. Its **full formal XOR span** contains 2^E combinations; generating it exhaustively would incur exponential work/space, while Gaussian elimination certifies consistency and independence in polynomial time. The finite verifiers deliberately enumerate this span only for E<=15. A legal successful R_ext upper-bound certificate has q=10h-1, span <=5+ceil(log2 h) under unit-time unbounded processors, and explicit serialization as conservatively analyzed in /492. The present fragment has no accepted refutation, so no minimum-refutation work/span/space is claimed. Source bits O(h log h); explicit primitive row masks may cost O(h^2) total bits if dense. Actual generation, input/source/index reads, pair scans, closure, row computation, search, serialization, verification and all-phase simultaneous peak storage are separate from the ideal free after-the-fact minimum; measured host costs above are finite only. No same-machine FLMV accounting or general computational hardness inference is made.

## Source-family ledger and precise remaining transfer

| Family | Source encoding and known bound | Strong method used | Missing transfer |
|---|---|---|---|
| Pang q=2 one-hot expander Tseitin | 3h variables, 7h width<=3 clauses; exp(Omega(h)) shared-DAG syntactic Res(PC_r/F3) for fixed r (Pang 2026 preprint) | Core is nonrefutable under this exact no-RES typed fragment; R_ext with RES->AND3 refutes in 10h-1 | Authenticate historical RES parent admissibility, paid conversions and DEF source facets; cannot infer general hard R_mix341 |
| Odd one-bit cubic-expander Tseitin | 3h/2 vars, 4h proper strict3 clauses; exponential ordinary Resolution on suitable expanders | Historical recovered SOURCE/AND3/XOR refutation has 4h-1 paid nodes | No all-rule hardness; this source is a shortcut control |
| Random signed proper strict3 F(n,3,8n) | n variables, 8n iid clauses with replacement; exp(Omega(n)) Res(PC_1/F2) w.h.p. (Pang 2026 preprint) | LSPV-1/498 source-anchored syntactic transfer for restricted R_loc3 | All historical nonlocal AND3, LOCAL-CONVERT, DEF, branching/discharge remain uncovered |
| Haken PHP | Ordinary wide clauses plus collision clauses; exponential ordinary DAG Resolution | Cook ER polynomial refutations | Encoding and full mixed lower-bound preservation require explicit reverse simulation |

**Remaining OPEN:** [P2-D1] exact historical accepted-byte RES/LOCAL/DEF/parent/export ports; [P2-C3] whole mixed source-retracting polynomial normalization or LEGAL typed counterexample; [P2-B1] superpolynomial minimum across all fixed historical rules; [P2-B2] noncircular same-R B3. No other agents, historical rules/weights, schedules or main.tex were modified. P versus NP remains OPEN.
