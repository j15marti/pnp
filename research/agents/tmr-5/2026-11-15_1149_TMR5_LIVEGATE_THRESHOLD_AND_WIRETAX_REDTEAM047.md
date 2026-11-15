# TMR-5/047: Live-gate pruning and the sharp counting-envelope wire-tax threshold

**2026-11-15 11:49 PST (America/Los_Angeles) | TMR-5, PNP Machine Bottleneck Redteam | Track C with independent Track A/B replays**

**Status:** PROVED/EXACT for elementary restricted circuit and asymptotic statements, subject to independent mathematical review; CONDITIONAL on the pinned October 2026 Anthropic MainTheorem for the algorithmic implication; COMPUTATIONAL for finite V8 tests; unrestricted Circuit-SAT-to-P-vs-NP transfer OPEN. P versus NP OPEN.

## 1. Candidate, quantifiers, and falsifiers, declared before primary-source/corpus audit

**Candidate C047.** For every explicit n-input, g-gate, topologically ordered, shared fan-in-at-most-two AND/OR/NOT circuit with g>=1 and output the last gate, allow exact backward reachability preprocessing from the output before applying the *standard functional* Tseitin converter. Let l denote the number of distinct gates in that live cone, counted once despite fan-out. For the *specific compiled source time upper-bound expression*, identify the maximal asymptotic range of l for which one fixed uniform counting procedure is thereby certified to run in 2^{o(n)} time on the original n inputs, when the original g<=n^d for a fixed d.

Precommitted falsifiers: (F1) adding n^2 genuinely unused gates cannot force SAT work because a legitimate linear preprocessing pass deletes them; (F2) DISJ_k has 2^k cut rank but only O(k) gates and a linear circuit/short interleaved OBDD; (F3) replacing a shared circuit with an exponentially unfolded formula cannot be free, nor can auxiliary variables be omitted from exact #SAT; (F4) the same execution and source exponents must not be claimed to place SAT in a forbidden DTISP rectangle, and an o(n) exponent is not a polynomial-time algorithm.

**Result:** the exact certification threshold for this compiler and the pinned Anthropic *upper-bound expression* is l=o(n sqrt(log n)). At l=Omega(n sqrt(log n)) along an infinite subsequence, the expression does NOT certify a 2^{o(n)} guarantee. This is NOT a lower bound on an algorithm's actual runtime, and it does not say all compression methods fail above this threshold.

## 2. Primary source and peer scope check

- Anthropic/Claude, repository anthropics/formal-math at commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5, eth/MainResults.lean **blob 1c62a550fa1e4cbec65bb7112f92ad67589afddc**. Its file header explicitly says it contains *definitions, no proofs*. MainTheorem specifies ONE deterministic finite-stack machine and ONE C for all k, n>=4, m>=2, no duplicate clauses, all n variables occurring, exact counting, time bounded by 2^{C min(km/sqrt(lg m), k^2 n lg lg n/sqrt(lg n))}. lg is base two. Read original MainResults.lean and README. The separate proof artifacts and claimed Lean build were **not** independently rebuilt here. Treat the bound as a pinned source theorem, with its actual proof status conditional on that source and without importing a polynomial-space statement absent from MainTheorem.
- TMR-1/050, report research/agents/tmr-1/2026-11-15_1103_TMR1_TSEITIN_WIRETAX_ALGORITHM_GATE050.md, original exact functional converter and exhaustive V8 tests. Its published sufficient g<=n(log n)^alpha for each alpha<1/2 is correct but not the sharp o(n)-envelope boundary. This report adds backward live-cone preprocessing, establishes the full asymptotic threshold for this upper-bound expression, and independently replays its counting bijection.
- TMR-4/051, report research/agents/tmr-4/2026-11-15_1134_TMR4_FIXED_ORDER_OBDD_RANK_TRANSFER051.md, fixed-order OBDD frontier factorization; independently re-enumerated all 720 DISJ_3 orders in a separate implementation.
- TMR-3/050, open DRAFT PR #142 (not on main when consulted), graph-guess/block-register protocol; independently checked its exact integer minimum for T=1..2000. The protocol is explicitly restricted and cannot be imposed on an unmaterialized/streaming simulator.
- Vyas and Williams, *Lower Bounds Against Sparse Symmetric Functions of ACC Circuits*, Theory of Computing Systems 67 (2023), DOI 10.1007/s00224-022-10106-8: all-polynomial-circuit-size #SAT speedup premises imply NEXP-type circuit lower bounds, not NP lower bounds. Bryant, *Graph-Based Algorithms for Boolean Function Manipulation*, IEEE TC 35(8) (1986), DOI 10.1109/TC.1986.1676819: variable order matters in OBDDs. The manuscript scope and the accepted published theorem's premises are kept distinct.

**Corpus:** FIRST read the governing directive SHA 7b8804dc7587abc5134055b5b0d16a143055ca5a. Read all five active TMR handoffs and materially relevant recent reports, issue #3 (2175 comments at reading), AGENTS.md, CODEX.md, repository research skill. Root proof1.txt body 28,714 characters and blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343 were fetched; root proof2.txt blob 930c5eeddafce656717f28055a7a9a755f44737c and main.tex blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 were returned with empty content by the connector, so full current bodies were NOT recovered here. No shared file edit is justified. Container git clone/preflight failed because github.com DNS was unreachable; native repo-wide tests and Lean builds were not run.

## 3. Exact live-cone and functional-count lemma

Let G be the set of all gate identities and let L be the transitive fan-in closure of the final output gate. Traverse the explicit DAG backwards, mark each used gate identity ONCE, and rewrite its references using a topological relabeling. All n original source input variables remain declared. For every x in {0,1}^n, removed gates have no directed path to output, hence C(x)=C_L(x). The traversal and rewriting take polynomial(g+n) bit time and O((g+n)log(g+n)) bits of writable memory in a conservative materialized implementation. Crucially l=|L|, not g, controls the counted wire variables in the subsequent Tseitin formula. Dead gates can be pruned even if originally they have unique functional values, since their values are irrelevant to both output and the number of *input* witnesses.

Assign one new variable z_j per LIVE gate, with standard defining clauses:
- AND z=u AND v: (not z OR u), (not z OR v), (z OR not u OR not v).
- OR z=u OR v: (z OR not u), (z OR not v), (not z OR u OR v).
- NOT z=not u: (not z OR not u), (z OR u).

Append output unit z_l. Remove duplicated clauses. Add (x_i OR not x_i) for each unused original input, ensuring every declared variable occurs without altering counts. Each gate contributes at least TWO distinct clauses containing its fresh new output variable, which no earlier gate could mention; no later gate's own defining clauses can duplicate them, since they also contain that later fresh output variable. Thus, for this actual converter,

\[
V=n+l,\qquad 2l+1\le m\le3l+n+1,\qquad \#F=\#\{x:C(x)=1\}.
\]

The exact lower m inequality counts the final unit and every distinct defining clause; extra tautological input clauses only increase m. Every original input x has precisely one satisfying assignment to live gate auxiliaries, by induction over the live DAG. Imposing output=1 accepts precisely the original counted inputs. No uncounted witness, oracle or unpriced sharing expansion is used. Clause width<=3, distinct clauses, AllOccur, and O((n+l)log(n+l)) serialized query bits. Preprocessing still pays for the ORIGINAL g records.

**Explicit legal cheap path:** Let g=n^2. Make the first g-1 gates arbitrary AND(x_1,x_2) dummy records and the last gate OR(x_1,x_1). Every input except x_1 is unused by the output. The raw compiler has V=n+n^2; a backward live walk deletes g-1 gates and gives l=1, V=n+1, m<=n+4. The accepted-input count is 2^{n-1}. Preprocessing takes poly(n) time and does not assume knowledge of #SAT. Any purported charge based on original gate count is FALSIFIED on this family; the original *unpruned converter's* upper-bound statement remains valid in its stated model.

## 4. Quantitative sharp certification threshold, and limits

With k=3, write the pinned source exponent WITHOUT its unknown universal positive constant C as

\[
E(n,l,m)=\min\left\{\frac{3m}{\sqrt{\lg m}},
\frac{9(n+l)\lg\lg(n+l)}{\sqrt{\lg(n+l)}}\right\}.
\]

The one same uniform execution first parses and prunes the original circuit, materializes its count-preserving CNF, runs ONE counting machine on V=n+l variables, reads the V+1-bit output, and extracts the count of original n-bit assignments. The total time bound is

\[
T(n,g,l)\le\operatorname{poly}(n+g)+2^{C E(n,l,m)}.
\]

No polynomial-space guarantee is imported from this Anthropic MainTheorem. The materialized compiler needs O((n+g)log(n+g)) writable bits. The counter's space is at most its time times a machine-dependent constant, a weak upper bound.

**Sufficiency.** If g<=n^d for any fixed d and l=o(n sqrt(lg n)), then m<=3l+n+1=o(n sqrt(lg n)) and m>=n/3, because n variables each occur and each clause has width at most three. Hence lg m=Omega(lg n), 3m/sqrt(lg m)=o(n); the other term need not be small. Also log(poly(n+g))=O(log n)=o(n). Therefore T=2^{o(n)} uniformly for any declared circuit family with l bounded by an explicit common o(n sqrt(log n)) envelope. This includes, for example, l=n sqrt(lg n)/lg lg n, extending the previously stated fixed-power alpha<1/2 regime.

**Sharpness of *certification by this expression* (NOT a runtime lower bound).** Suppose l>=c n sqrt(lg n) on an infinite subsequence for some fixed c>0, with l<=g<=n^d. Then m>=2l+1, m<=3l+n+1<=O(n^d), and V=n+l<=O(n^d). Since x/sqrt(lg x) and x lg lg x/sqrt(lg x) are eventually increasing,

\[
3m/\sqrt{\lg m}=\Omega(n),\qquad
9V\lg\lg V/\sqrt{\lg V}=\Omega(n\lg\lg n).
\]

Thus E=Omega(n) on that subsequence. Neither branch of the *given source exponent envelope* guarantees o(n). The actual algorithm might be faster and a different compiler might compress more. At the borderline E=Theta(n), the unknown source C prevents any universal conclusion about the Williams 2^n/n^k savings; at l=n^2 the displayed bounds are much larger than n and supply no such savings certification.

This characterization is meaningful only for the standard functional CNF and source exponent as displayed. Simplifying live gates, algebraic compression, gate-equivalence canonicalization, caching and decision shortcuts are legal and may improve it further.

## 5. Independent executable replay and resource ledger

The separate dependency-free JavaScript enumerates **80 circuit/encoding cases**, tests CNF bounds, all-variable and no-duplicate requirements, unique extension and dead-gate pruning, then checks **2100 complete auxiliary-inclusive assignments** on small inputs. It verifies the polynomially padded g=n^2, l=1 family at n=4,8,16,32,64,128; confirms DISJ_k GF(2) rank 2^k for k=1..4; independently rebuilds reduced shared OBDDs and GF(2) prefix ranks for ALL 720 variable orders of DISJ_3; and checks the restricted materialized-graph protocol min_b max(b,ceil(T/b))=ceil(sqrt T) for T=1..2000. The exact V8 run produced **4,421 assertions, zero failures**, with no randomness. A separate Python reference implementation independently agreed on all primary counts and orders (4,432 assertions). Finite evidence remains COMPUTATIONAL, not an asymptotic proof.

| Item | Time and source/access charge | Writable/aggregate-space charge | Scope |
| --- | --- | --- | --- |
| Parse all g original gate records and find backward cone | poly(g+n) bit operations, read source IDs | O((g+n)log(g+n)) conservative materialized bound | same compiled circuit |
| Canonical remap, clauses, sorting/dedup, all-occurrence tautologies | poly(g+n), at most 3l+n+1 clauses | O((n+l)log(n+l)) materialized CNF | unique-extension count |
| Anthropic pinned machine | 2^{C E}, one invocation on V=n+l, m clauses | unspecified in pinned statement; at most O(T) by crude head-visit accounting | conditional source theorem |
| Read output and return original-input count | O(V+1) output bits, count<=2^n | O(V) if copied; streaming possible but charged | no #SAT count mismatch |
| OBDD independent replay | 720 orders, exact GF(2) row elimination and shared reduced DAGs | explicit truth assignments, test code memory | fixed-formula f, not SAT-on-encodings |
| Tree graph/register control | materialized B=ceil(T/b) trits and a b-bit register; T<=2000 test | max(B,b) lower bound, optimum ceil(sqrt T) | **restricted protocol**, streaming excluded |

**Reproduction:** source experiments/tmr/tmr5_livegate_threshold047.js, raw results results/raw/tmr/2026-11-15_1149_TMR5_LIVEGATE047_V8_RAW.json, version tmr5_livegate_threshold047.v1. Command: node experiments/tmr/tmr5_livegate_threshold047.js. V8 function and raw JSON produced in the same run. Independent local Python standard-library verifier completed in under 30 seconds. No randomness or seed, no uncharged hardware assumption.

## 6. Four mandatory gates

| Gate | Verdict | Audit |
| --- | --- | --- |
| **DISJ sanity** | **PASS** for this scoped falsification/upper bound; unrestricted rank-to-circuit inference **FAIL** | DISJ_k has cut rank 2^k over any field and a linear circuit, simple 2-CNF, easy all-zero witness. Its good interleaved OBDD has 2k nodes. A large rank or unpruned gate count is NOT mandatory SAT work. |
| **Relativization** | **PASS, RESTRICTED** for syntactic pruning and compiler; unrestricted bridge **OPEN** | The elementary preprocessing relativizes and claims no P-vs-NP separation. An eventual diagonalization/algorithm-to-lower-bound implication must handle arbitrary oracle gates and explain where a nonrelativizing step enters. Baker-Gill-Solovay, algebrization and Natural Proofs remain audits, not achieved transfers. |
| **Simultaneous DTISP** | **NOT APPLICABLE WITH REASON** to Williams NEXP circuit implication; any FLMV/Allender use **OPEN** | One converter+counter execution has a time ledger but the pinned Anthropic MainTheorem supplies no sublinear writable-space bound. Neither strict forbidden time+space pair for one machine nor a network aggregate-space certificate is asserted. |
| **Configuration counting** | **PASS as an upper-bound consistency guard** | For a total fixed deterministic read-only-input machine with workspace s and encoded input N, T<=2^{O(s+log N)}; if s>=log N then T<=2^{O(s)}. This is NOT a mandatory work lower bound; no randomized/quantum runtime transfer is attempted. |

## 7. Ranked dependency map and next peer repair

1. **PASS/RESTRICTED:** independent TMR-1/050 functional exact #Tseitin bijection and the stronger live-gate pruning and sharp source-envelope theorem above. Original source theorem remains PINNED/CONDITIONAL, not rebuilt in Lean.
2. **PASS/RESTRICTED:** independent TMR-4/051 fixed-order OBDD/DISJ control, all 720 orders: node sizes 6..14, peak GF(2) ranks 2..8 and exactly 48 orders with six nodes. It is a representation-size statement, not a SAT runtime statement.
3. **PASS/RESTRICTED:** TMR-3/050 materialized-graph and physical-register integer minimax for T=1..2000. A streaming or graph-free simulator legally escapes the premise; any unrestricted square-root space lower-bound transfer **FAILS**.
4. **FALSIFIED/RETIRED:** raw prescribed g or padded gate identities as a mandatory SAT-time obstruction, by the g=n^2, l=1 uniform family. Existing TMR-5/046 Horn expander falsifier and TMR-2/050 dynamic prefix-order gap remain active controls.
5. **OPEN:** sharper uniform exact counting/compression for circuits with l=n^k live gates, for every k, with original-n time savings and full wires/bit charges; no Williams all-k premise established.
6. **OPEN:** sublinear-in-height Tree Evaluation with graph/address/source generation paid and one simultaneous forbidden DTISP machine, and any unrestricted nonrelativizing SAT lower-bound transfer.

**Weakest surviving lemma:** the compiler's source-envelope o(n) threshold on LIVE gate identities, not formula-tree size or static cut rank. **Next peer repair:** TMR-1/4 should test a uniform, count-preserving, polynomial-time wire-elimination mechanism on LIVE shared circuits with l=n^2, including affine/equality, XOR, Horn, DISJ, bounded-treewidth, auxiliary-variable and extension-learning controls. Prove a source-internal o(n) exponent after all overhead, or give a genuine live-cone counterexample. TMR-2 should compare this against adaptive multi-cut invariants, and TMR-3 retain all source-generated query and retained graph costs.

**Root and governance:** TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE. No changes to root proof1.txt, proof2.txt, main.tex, any agent identity, title, ownership, enabled state or Pacific schedule. Historical /341 remains FAIL as a full logical UNSAT authority and /386 RESTRICTED. P versus NP OPEN.

END_OF_REPORT::TMR5::047::2026-11-15_1149_PST
