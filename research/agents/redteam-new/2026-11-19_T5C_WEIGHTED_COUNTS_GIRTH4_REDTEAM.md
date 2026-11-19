# Strict T5 red-team: full weighted counts, exponential rarity, and k=1 incidence-girth correction

2026-11-19 Pacific | Independent adversarial audit | **P vs NP OPEN**

## Findings and exact theorem

**FALSIFIED (prior fixture report):** `research/agents/redteam-new/2026-11-19_T5C_MATCHED_COVER_VALIDITY_GATE.md` stated that six incidence graphs (CLOSED and OPEN for k=1,2,3) all have girth 6. For k=1 OPEN, common physical clause 0 is C(h0,t0,a1_0), and new closing physical clause 14 is C(h14,t0,a1_0). The factor-incidence graph has the actual 4-cycle t0, clause0, a1_0, clause14, t0. Thus girth=4. CLOSED k1 and both variants k>=2 have girth6. The matched-pair SAT/UNSAT claim is unaffected. This is *incidence* girth, not primal graph girth; fresh heads do not erase the duplicated endpoint pair.

Canonical R(a,b) iff (b-a) mod5 in {1,3}, and strict C is the unoriented directed 3-cycle. C accepts exactly 30/125 triples. The independent quadratic identity is C(a,b,c) iff [(a-b)^2+(b-c)^2+(c-a)^2] mod5 =1. Three variable NAMES per clause are distinct; assignments may reuse VALUES elsewhere.

**PROVED (exact private-head multiplicity):** Let w(u,v)=number of h in Z5 satisfying original C(h,u,v). Then w(u,u)=0; w(u,u±1)=2; w(u,u±2)=1. At u=0, admissible heads for v=1,2,3,4 are respectively {2,4},{1},{4},{1,3}. Hence for any graph edge-private-head source F_G, its *full* satisfying-vector count is
`#C(F_G)=sum_{z:V->Z5} product_{uv in E} w(z_u,z_v)`.
This is not a constant multiple of ordinary graph 5-coloring counts.

**PROVED (exponentially rare SAT yet O(n) witness):** For any tree with e edges, its private-head strict-C source has 2e+1 active variables, exactly 5*6^e complete SAT assignments, and density (6/25)^e among all 5^(2e+1) vectors. Root color (5 choices), then each parent has exactly 6 child-color/head pairs. A deterministic traversal constructs and verifies one complete witness in O(e) source operations. Exponential SAT density alone does NOT establish difficult SAT-witness search, even without graph criticality.

**PROVED (matched pair exact full-C counts):** Each K6-minus-terminal-edge wire has four interiors, 14 edges, terminals forced equal in every proper 5-coloring. For fixed common terminal color, the 24 interior permutations each contribute weight (16 from duplicate terminal/interior links)*(8 from interior clique)=128. Thus a wire has 3072 full head completions. The final OPEN edge to the first interior vertex contributes a weighted final factor 4608 because half its permutations admit 2 heads and half 1. For k chained wires:
- OPEN SAT: exactly `5 * 3072^(k-1) * 4608` full strict-C vectors.
- CLOSED UNSAT: exactly 0.
- CLOSED with final physical clause deleted: `5*3072^k` assignments on the active vocabulary; `25*3072^k` on the fixed original vocabulary if the now-unused final head counts as a free variable.

The earlier `5*24^k` figure counted only shared graph colorings, not complete original-C witnesses. OPEN k=1,2,3,4,8 full-vector counts are 23040, 70778880, 217432719360, 667953313873920, 59488217268686865114354155520. Density for k8 is 1.3585e-79, yet the indexed recognizable source has a trivial O(k) SAT-witness constructor. These exact counts do not imply a uniform solver for arbitrary C.

**PROVED (group invariant):** C is preserved under each of the ten transformations x -> ±x+t over GF5. Any satisfying vector for a formula containing at least one clause contains three different values, so its group orbit has size ten. Hence the number of satisfying assignments to the full named variables is divisible by ten. This is a consistency check, not an algorithmic lower bound.

## Executed independent audit

Two Python standard-library programs, `audit.py` and nonimporting `verify.py`, use independent original R-C and quadratic GF5 predicate implementations. All 125 C triples agree; 1250 translation/reflection checks pass. Full tree assignment counts for e=1,2,3 exhaustively match 30,180,1080. The entire k1 matched pair is independently enumerated over all 5^6 shared assignments, with strict-C head weights. A separate per-color transfer matrix confirms diagonals 3072 and 4608 for all five colors. Independent BFS confirms OPEN k1 girth4 and all other tested variants girth6.

For CLOSED k=1,2,3,4,8, the two scripts construct and independently replay 257 complete physical-clause deletion witnesses, with **18,933 original physical-C evaluations**. Every deleted original C clause is FALSE in its witness and all retained clauses TRUE. The full source fixtures, all witness vectors, exact raw JSON, executable audit and independent checker, operation counts and SHA256SUMS are in the conversation artifact `T5C_Redteam_Weighted_Count_Girth_Audit_20261119.zip`. Deterministic, no seed.

## Complexity and transfer firewall

The finite generating grammar, sources, all failed constructions, full output and the materialized quadratic witness ledger are charged. Construction/replay of each known-source witness is O(k) word work, but publishing all deletions is Ω(k^2) output and memory in the attached implementation. No anonymous arbitrary-label recognition guarantee, sublinear peak space, row-cover algorithm, or unrestricted lower bound is claimed. The family has Θ(N) shared graph variables and 5^Θ(N) literal rows, exceeding R<=N^.195. Neither this result nor a source-criticality/girth statement resolves P vs NP.

Prior work read: linked matched-cover report, rank/row report, S->C criticality failure, cycle-rank solver; user Library `t5_strict_research.pdf` pages1-3. ZIP `t5_strict_research_package.zip` not recovered. Literature inspected: Buss and Williams (2015), Figures 8.2/8.3; Williams (2006), Theorem2.1; Abbott, Zhou and Hare (1994), critical graph constructions.

**Handoff:** Check physical repeated endpoint pairs in all future incidence-girth certificates, and use full weighted strict-C counts rather than shared-color counts in counting/marginal arguments. Existing strong negative lower-bound inferences remain OPEN. P vs NP remains OPEN.
