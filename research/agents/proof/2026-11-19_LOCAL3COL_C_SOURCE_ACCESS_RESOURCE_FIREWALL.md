# Proof lead: LOCAL3COL-C1, strict-C local-access reduction firewall
**2026-11-19, America/Los_Angeles.** Status **PROVED/EXACT** fixed-width 3-CNF reduction; **COMPUTATIONAL** finite testing; **CONDITIONAL** simultaneous time-space transfer; **OPEN** source-encoding/machine-model transfer and P vs NP. Independent external mathematical audit pending.

## Exact construction
Strict-C relation: R(a,b) iff (b-a) mod 5 in {1,3}; C(x,y,z)=R(x,y)R(y,z)R(z,x) OR R(x,z)R(z,y)R(y,x), three distinct names per clause. C accepts exactly 30/125 ordered value triples; do not confuse Q, S, P controls.

For every fixed-width indexed 3-CNF F with v>=1 variables and m>=1 3-literal clauses, construct a graph H3:
1. Base triangle of vertices T,F,B. Per Boolean variable x use two adjacent vertices x,not-x, both adjacent to B, forcing complementary T/F values.
2. Per clause (a OR b OR c), introduce binary s and not-s as a second complementary pair. Replace that clause by NAE(a,b,s) and NAE(not-s,c,F). Each NAE has a triangle of new vertices, each one adjacent to the corresponding literal vertex. Three Boolean terminal colors admit such a triangle coloring iff not all three are equal.
3. Add U,V adjacent to each other and to every old vertex to form H5. Proper 5-coloring of H5 iff proper 3-coloring of H3. Replace each edge {u,w} by C(h_e,u,w), fresh head h_e. Exactly exists h C(h,u,w) iff u != w.

The reduction satisfies, for **every** such F:
F SAT iff H3 3-COLOR iff H5 5-COLOR iff the resulting strict-C instance K(F) SAT. Every Boolean witness extends to an explicit full strict-C coloring; every strict-C witness projects back via the base T/F colors. The source graph has V3=3+2v+8m and E3=3+3v+15m. H5 has V5=5+2v+8m and E5=10+7v+31m. K(F) has exactly V_C=15+9v+39m named variables and M_C=10+7v+31m strict-C clauses.

## Fresh random-access source lemma
The i-th K(F) clause triple can be computed without materializing the expanded graph or C source: map i to one of five fixed segments, 3 base edges, 3v variable edges, 15m clause edges, one apex-apex edge, or 2(3+2v+8m) apex-old edges. Clause segment arithmetic identifies its **single corresponding** source triple of literals. For fixed-width random-access literal-array encoding, this uses O(log(v+m)) auxiliary bits and polylogarithmic bit operations/source accesses per output symbol. A variable-width, nonindexed source does **not** inherit this guarantee without an additional adapter. Physical input/output and any actual proof or witness verification are charged.

**Girth/criticality firewall:** the base graph and apices introduce triangles, hence the resulting strict-C incidence graph has girth six. This construction does not preserve high-girth or clause-minimal UNSAT promise families, and it supplies no lower bound for their SAT deletions.

## Executed falsification controls
Reproducible script SHA256 `95dde7d7a82743a54b1d7b70bd12043ea7dbb55dfd816648ad0c73d37473145d`; deterministic seed 20261119; standard Python, no dependencies. Independent direct edge builder matched **51,311/51,311** indexed edges on 300 randomly constructed 3-CNFs (1..5 variables, 1..8 clauses). Exhaustively checked 30/125 strict-C triples, 25 head-pair projections, 8/8 NAE triangle rows, and 8/8 OR-to-two-NAE rows. Complete Boolean enumeration yielded 286 SAT and 14 UNSAT; **286** complete strict-C witness colorings satisfied **48,289** checked original C clauses. Three UNSAT controls were refuted independently at the intermediate 3-color level with **4,453** total recursive calls, not full C-backtracking. Maximum C source was 372 variables, 293 clauses. Approximate wall time 2.45s, Python tracemalloc peak 371,632 bytes (not formal working-space metric). The full script, source/witness samples, raw result JSON, and checksum manifest are available in the run's local ZIP, `T5C_Lead_Local_Access_Reduction_20261119.zip`. The complete local report is `T5C_LEAD_LOCAL_REDUCTION_RESOURCE_AUDIT_20261119.md`. Full source itself was not committed here.

## Connection to unrestricted time-space bounds (CONDITIONAL pending exact source-model audit)
A total uniformly clocked and sound deterministic K(F) decider/witness-finder using time N^{1.33+o(1)}, writable space N^{.5+o(1)}, plus the verified polylog virtual-source access, would imply a fixed-width 3-SAT decider in n^{1.33+o(1)} time and n^{.5+o(1)} space. A sound one-sided solver that is guaranteed to return decisive verified output on **every** instance of its targeted polarity within the same uniform bound is also a total decider by timeout; wrong-path output must be rejected.

Buss and Williams, *Computational Complexity* 24 (2015), DOI 10.1007/s00037-015-0104-9, certify in their alternation-trading random-access framework SAT not in DTISP(n^c,n^.5) for c at/below a reported 1.34070 threshold (see published table, with explicit refutation at 1.34070). **The last transfer gate** is to certify that the paper's source language/representation reduces to our exact fixed-width indexed 3-CNF language with near-linear size and polylogarithmic local random-access bits, not requiring linear writable offsets. Until that is checked, the numerical contradiction for arbitrary bit encodings is **CONDITIONAL**. Even if certified, this rules out just the simultaneous (1.33,.5) total solver in that machine model, not all polynomial time and not P=NP. It has no direct application to promised intrinsic-critical/growing-incidence-girth C instances.

For shared row/block layout R<=N^.195, B<=N^.65, private size<=N^.35, full sequential child enumeration costs N^{.845+.35a+o(1)} for local complete decision time m^a, plus repeated input materialization up to N^1.195 and all other charges. The 1.33 goal through this scan needs a<=97/70=1.385714..., a condition **not** implied by an arbitrary polynomial SAT seed. Sequential local writable space m^s fits N^.5 only for s<=10/7 and only if all other live buffers/workspace are separately controlled.

SAT correct path: one common z and all private witnesses, fully verified. UNSAT: for **every legal z**, find and validate some truly refutable block, not only rows in a sampled/incomplete list. A child index alone is not an UNSAT certificate. A supplied k-bit correct path is different from deterministic discovery: full enumeration may take 2^k verified replays, including failed branches and negative children, and alternating strategies require all universal branches.

## Prior work, literature and handoff
Reviewed user Library `t5_strict_research.pdf` pages 1-3, GitHub `research/agents/lspv-3/2026-11-19_0039_LSPV3_STRICT_C_CRITICAL_GIRTH_FIREWALL.md`, and `research/agents/recovery/2026-11-19_1144_PATH3/handoff.md`. The distinct new contribution is explicit fully indexed 3-CNF-to-C reduction with exact constants and independently verified complete C witnesses. Historical critical-girth claims and S/C local transfers are not relabeled.

Single priority gate: have resource-bounds and independent-audit agents certify/refute the SAT-to-fixed-width-3CNF random-access bit-model link and the exact Buss-Williams theorem convention. Critical-graphs agent should audit incidence girth 6 and failure of criticality. Obstruction-cover and witness-search agents should check any claimed sublinear shared-row buffer or answer-advice transfer. Do not transfer restricted resolution, treewidth, cover rank or finite timing bounds to unrestricted execution.

References: Buss & Williams (2015), https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/; Fortnow et al., JACM 2005 DOI 10.1145/1101821.1101822; Williams, *Computational Complexity* 15 (2006) 433-470 DOI 10.1007/s00037-007-0221-1.

**P versus NP OPEN.** No existing task, schedule, owner manuscript or older file changed.
