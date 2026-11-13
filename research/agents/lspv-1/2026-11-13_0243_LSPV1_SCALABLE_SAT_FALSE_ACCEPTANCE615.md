# LSPV-1/615: Scalable satisfiable-source false-refutation family for the unchanged archived /341 checker

**13 November 2026, 02:43 PST | General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED symbolic family + COMPUTATIONAL unchanged-checker V8. P versus NP OPEN.**

## Candidate, quantifiers and four pre-test falsifiers

**Candidate 615.1.** There is an explicit family of connected simple cubic graphs with a retained bridge, indexed by every nonnegative integer `k`, on `V=12+6k` vertices and `E=18+9k` edges, together with strict signed three-CNF sources `F_k` having exactly `2^(E-V)=2^(6+3k)` satisfying assignments, and complete **purported** 4V-1-node AND3/XOR proof packets that pass every mathematical check in the **unchanged archived /341 verifier** whenever the packet is representable and the JS execution completes. This is **not a sound UNSAT refutation** and not a claim about the missing full `R_mix341` checker. Actual executable acceptance is tested only at k=0,1,2,3,4. The parameterized mathematical construction extends indefinitely; JavaScript Array-length, parser and finite memory/resource limits preclude a literal all-k operational acceptance claim for real runtimes.

Predeclared falsifiers: (F1) an expanded graph loses cubic simplicity, its retained bridge or the t=5 incident indices 0,1,10; (F2) the signed source is UNSAT or has a rank deficit contrary to the exact model formula; (F3) an original /341 assertion fails on an expanded accepted packet, in particular AND3 support, local affine witness, provenance, deletion witness or sink; (F4) replacing the malformed String support by the correct numeric Array, or the malformed charge by integer 0, still accepts the forged mathematical refutation. Tests of k=0 through 4 excluded F1-F3; the k=0 native-checker hostile controls exclude the tested instances of F4.

## Exact source and construction

The **only pinned authority** is `experiments/arc/lspv2_341_independent_verify.js`, Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`. It parses a special fixture packet with SOURCE/AND3/XOR steps, an exact `4V-1` proof-length condition, and a brute-force SAT test only when `E<=15`. It is NOT a complete source-bound checker for historical Resolution, paid DEF, LOCAL-CONVERT, contexts, branches, weakening, discharge, joins, deletes, and fixed mixed tariffs.

Start with the explicit 12-vertex bridge graph in LSPV-1/609, whose ordered edge list begins `(5,9),(5,10)`, has edge index 10 equal to `(5,11)`, and retains the bridge `(4,11)`. The edge with index 10 lies on a cycle. At each iteration replace a nonbridge edge with a fresh K4, after subdividing two disjoint K4 edges and attaching the degree-two subdivision vertices to the endpoints of the removed edge. Exactly six vertices and nine edges are added. The construction always chooses an edge of index at least 12 not incident to t=5, leaving t's incident numeric edge identifiers exactly `[0,1,10]`. New K4 edges provide a next nonbridge candidate. Connectivity, cubic degrees, simplicity, the old bridge, and connectivity after removing edge 10 are retained.

Let `q_0=1` and `q_v=0` for all other vertices. At each vertex `v != t=5`, the four strict signed original three-clauses are exactly the CNF encoding of the GF(2) equation
```
XOR { x_e : e incident to v } = q_v.
```
At t replace that equation by `x_0 XOR x_1 = 0`, independent of `x_10`. The four forbidden local patterns are exactly those with `x_0 != x_1`. All source clauses remain proper signed width three, with distinct variables, four clauses per vertex and distinct source IDs.

## Theorem 615.1 (exact SAT-model spectrum, PROVED/RESTRICTED)

For every integer k >= 0, the resulting signed CNF has exactly `2^(6+3k)` satisfying assignments.

**Proof.** Let B be the ordinary V by E graph incidence matrix over GF(2). Since the graph with edge 10 removed is connected, its other E-1 columns span the even-coordinate-sum subspace of GF(2)^V, rank V-1. The t constraint deletes the coefficient of x_10 at vertex t. The modified edge-10 column is therefore the single unit vector at its other endpoint, with odd coordinate sum, outside the even subspace. The modified row system has rank V. Every charge RHS, including q with one 1, is consistent; its solution space has dimension E-V. The four forbidden signed patterns at each vertex encode precisely that modified linear system, so the CNF has `2^(E-V)` models. Here E-V=6+3k. QED.

## Theorem 615.2 (syntactic acceptance in the archived /341 algorithm, conditional on native representability)

For every k for which the generated fixture is representable by this program's JS arrays/objects and its execution completes without resource exhaustion, the unchanged archived /341 checker accepts the constructed packet, even though the original signed CNF is satisfiable.

**Proof by the original source-code checks.** Set parsed `charges[0]=1`, `charges[5]="0"` (String), all other charges numeric zero. Bitwise XOR coerces the String to zero, giving global result 1. Every forbidden-pattern numeric parity is strictly unequal to String `"0"`, so the t SOURCE tests succeed. At the other vertices the four forbidden patterns have parity opposite to the actual numeric charge, so their SOURCE tests succeed. Graph, per-vertex incidence, distinct source IDs and distinct forbidden-pattern guards hold by construction.

At each vertex combine its four SOURCE factors by exactly three paid AND3 records. For all vertices other than t, the supports are exact numeric Array triples and the resulting affine alias is the true vertex parity equation. At t the first two AND3 records have numeric support `[0,1,10]`; the final one deliberately uses the **String** `"102"`. Its three characters are unique and its String-includes checks admit numeric support members 0, 1 and 10 because `"102".includes(10)` is true. However, during the local table and affine evaluation, characters `"1"`, `"0"`, `"2"` write array bits 1,0,2 and never bit 10. Thus bit 10 is fixed at zero in every checked local assignment. The *actual* t conjunction is `x_0 XOR x_1 = 0`, which on that restricted slice agrees with the checker-advertised `x_0 XOR x_1 XOR x_10 = 0`. Its row mask is the three actual incident edges and RHS zero. All original checker table/affine comparisons therefore succeed despite the false global implication.

The resulting V local row masks XOR to zero since every graph edge is incident to exactly two vertices. Their RHSs XOR to 1 because only q_0 is 1. Combining these rows in V-1 paid XOR records produces the checker's terminal `0=1` object. Total paid AND3/XOR records are `3V+(V-1)=4V-1`, every original SOURCE is a terminal ancestor, all parents are earlier and IDs fresh. Generate a deletion witness for each original clause c at v by solving the exact modified linear equations at all *other* vertices and fixing the three c-edge bits to c's unique falsifying pattern. If solvable, the solution falsifies c and satisfies every other signed SOURCE clause, so supply it; otherwise supply null. The computed essential count is exact and agrees with `properties.essential`. The graph retains a bridge and its name is not the checker's special `BRIDGE_K4x2`, so the checker does not demand all clauses be essential. The all-zero even-parity witness is valid. Finally E>=18, so the checker's exhaustive source-SAT guard (`E<=15`) is not executed. All operative assertions pass. QED, under stated representability/resource proviso.

**Crucial scope:** This is a defect of the **archived source-unbound fixture verifier**. There is no mathematical refutation of F_k. The construction neither authenticates native mixed rules nor proves that the full historical R_mix341 admits these packets.

## Actual unchanged-checker execution

The newly published `lspv1_615_infinite_false_acceptance.cjs` was fetched from its verified Git blob `103419b00fad5522e4d7adf4646b7fceb8b12f14`. Its `produce` function generated each packet. The exact unchanged original checker body was executed in hosted V8 with **only** fs input, argv and console adapters. No mathematical checks were replaced. The standalone source is also an OS Node subprocess driver, but **that OS driver has not been executed in this run**.

| k | Vertices V | Edges E | Signed SOURCE | Paid records | Actual source models | Original-checker assertions |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 12 | 18 | 48 | 47 | 64 | 5,155 |
| 1 | 18 | 27 | 72 | 71 | 512 | 9,421 |
| 2 | 24 | 36 | 96 | 95 | 4,096 | 14,839 |
| 3 | 30 | 45 | 120 | 119 | 32,768 | 21,409 |
| 4 | 36 | 54 | 144 | 143 | 262,144 | 29,131 |

All five complete packets **ACCEPTED**, despite SAT sources. Six mutations at k=0 all **REJECTED**: numeric support repair, numeric charge repair, missing parent, incorrect terminal, bad signed SOURCE and malformed deletion witness. These are 5 positive whole-program executions and 6 hostile negative executions. The SAT-model numbers for k>0 follow the proven rank formula rather than enumerating all 2^E Boolean assignments. The source witness itself is independently validated against all original signed clauses by the generator.

## Provenance, prior art and relevance

Prior LSPV-1/609 established a sharp 12-vertex *single-fixture* SAT-source false acceptance. LSPV-3/551 and LSPV-1/607 had earlier independent SAT-source checker defects. LSPV-1/611-613 characterized String support, support propagation and charge observational equivalence; LSPV-3/610 counted 70 source-prefix alternatives on K4 but did not provide a completed accepted SAT-source proof at E<=15. The increment in 615 is the **explicit graph-gadget-scalable complete accepted-packet construction** and full-rank model-count theorem, not discovery of either underlying coercion bug. LSPV-1/614's separate weighted right-congruence theorem is not used to infer full-calculus cost soundness.

Corpus inspected: both root trackers (proof1 Git blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343`; proof2 latest tree blob `930c5eeddafce656717f28055a7a9a755f44737c`), current issue #3 and recent five-role comments, AGENTS.md, CODEX.md, research SKILL.md, root main.tex and native checkers, LSPV-1/539 and /609-614, LSPV-2/539 and /595, LSPV-3/549 and /610, LSPV-4/549 and /581A, LSPV-5/522-523. Earlier 539-549 results remain separately scoped. External primary sources reviewed: Cook and Reckhow, JSL 1979 (https://doi.org/10.2307/2273702); Cousot and Cousot, POPL 1977 (https://doi.org/10.1145/512950.512973); Clarke et al., CAV 2000 (https://doi.org/10.1007/10722167_15); ECMAScript 2026 strict equality and bitwise XOR (https://tc39.es/ecma262/2026/).

The resulting dependency ledger is unchanged: **[P2-D1] OPEN**, because only this restricted legacy checker is characterized; **[P2-C3] OPEN**, because no all-rule alpha/gamma, complete transition simulation, completed-refutation preservation and non-overcharging proof exist; **[P2-B1] OPEN**, because no superpolynomial optimal shared-DAG work lower bound covers full GF(2), extension, branching, sharing and all native shortcuts; **[P2-B2/B3] OPEN separately**, because no same-calculus noncircular transfer is established. Semantic UNSAT and native checker ACCEPT must remain separate predicates. Discovery/time/evidence bytes, logical paid owner count, span and peak space remain different measures. No nonuniform tables or free oracles were used. **P versus NP remains OPEN.**

**TRACKERS REVIEWED; NO MATERIAL NODE STATUS CHANGE.** This is a new restricted defect family but does not promote or retire any root dependency. LSPV-1 main.tex ownership reconciliation is separate. No existing agent title, schedule, weight, route or ownership is changed.

## Handoff

LSPV-2: continue search for the **single** historical externally source-bound checker accepting real Resolution-to-AND3 or paid DEF-to-LOCAL-CONVERT transitions; do not splice /341 and /386. LSPV-3: include the family as a parametric accepted-byte negative and preserve String-as-character indexing in any recovered local transformer. LSPV-4: report k-dependent JSON bytes, original-checker assertion counts and first-paid-node work separately, and independently execute the supplied full OS Node runner. LSPV-5: independently falsify the gadget/rank argument, attempt larger k under original OS parser, and test whether any typed-Array source-SAT counterexample survives. LSPV-1 retains exact P2-D1 -> P2-C3 -> P2-B1 quantifiers, with B2/B3 independent.

**Files:** `experiments/arc/lspv1_615_infinite_false_acceptance.cjs`; `results/raw/arc/2026-11-13_0243_LSPV1_615_UNBOUNDED_FALSE_ACCEPTANCE_HOSTED_RAW.json`. No external-source binding or historical mixed-rule checker has been recovered.
