# TMR-5/079: long local-UNSAT support on polynomial-time recognizable five-symbol CSP DAGs

Date: November 17, 2026, 20:42 Pacific. Owner TMR-5, PNP Machine Bottleneck Redteam. Dependency **D5-T5-DAG-LOCAL-UNSAT-SUPPORT-TO-MANDATORY-WORK**. Status **PROVED/EXACT RESTRICTED** symbolic, independent external mathematics review **OPEN**; finite testing **COMPUTATIONAL**. P versus NP OPEN.

## Precisely scoped candidate and falsifiers, established before targeted corpus search

For every p,q>=2, construct an original-source T5 graph F_{p,q} by taking two internally disjoint directed s-to-t paths of p and q arcs and replacing each directed arc u->v by u->v, u->w, w->v with fresh w. Hypothesis: exact five-symbol homomorphism count equals 5 when p=q (mod 5), otherwise zero; every NO subgraph omitting any one of p+q path-terminal vertices is SAT; a uniform *unannotated* exact-source recognizer decides both labels and outputs the correct original-vertex count. Potential falsifiers: a false or non-unique forced-triad extension; hidden edge identification or cycles; a residual local-UNSAT graph after removing a path terminal; a descriptor/oracle or superpolynomial work in source recognition or integer output.

Prior adjacent result TMR-2/072 already constructs a source-recognized mixed family by adding a directed forced-triad **cycle** to a core, including high representation width. This TMR-5 family instead uses an entirely directed **acyclic** input, bounded degree and an arbitrarily growing *minimum vertex support for UNSAT*. The template-algebra identity itself is not novel; its combination with a DAG, matched YES/NO scalar statistics, and complete subgraph-support audit is the new restricted control.

## Lemma: exact transfer and counts

Use Sigma=Z5 and R(a,b) iff (b-a) mod 5 in {1,3}. The product R(a,b)R(a,w)R(w,b), summed over w, is exactly [b=a+1 mod5]: the direct arc allows differences {1,3}, a two-step path {1,2,4}; for difference +1 there is exactly one witness w=a+3. Consequently every original gadget triangle uniquely imposes a +1 increment.

Along the two paths, t=s+p and t=s+q in Z5. Therefore, including every actual original terminal AND private witness,

    #Hom(F_{p,q},T5)=5 * [p=q (mod 5)].

For p=q mod5 all five root choices induce a unique complete source witness. Otherwise no source witness exists. The graph has V=2(p+q), E=3(p+q), max total source degree 4, no directed cycles, undirected connectedness, primal treewidth exactly 2, and undirected cycle rank p+q+1. Every local gadget is a transitive source triangle; all arcs point forward under a topological order s, intermediate path vertices with their witnesses, then t. The single large undirected cycle is between the two parallel paths; the other p+q independent cycles come from transitive triangles.

## Lemma: large minimal UNSAT vertex support

Let U contain all path terminal vertices, including s,t; |U|=p+q. If an edge/vertex subgraph H of F_{p,q} excludes at least one vertex of U, the large undirected cycle connecting the two s-to-t chains is broken. The remaining undirected blocks are single edges or subgraphs of transitive triangles, glued along at most articulation vertices. A transitive directed triangle embeds in T5 after prescribing any one of its three vertex labels, by rotating the unique triangle embedding. Rooting the block-cut forest and propagating along articulation vertices gives a T5 homomorphism of every such H. Hence **every UNSAT subgraph has at least p+q vertices**. In particular, for any fixed k there are NO instances where every source subgraph with at most k vertices is SAT.

This does NOT say that deleting any one arc or private witness restores SAT, nor imply that any particular k-consistency, proof system or arbitrary algorithm fails.

For h>=2 set t=2h+5. Sources F_{h,h+5} (YES) and F_{h+1,h+4} (NO) share identical vertex count 2t, arc count 3t, maximum total degree 4, triangle count t, treewidth 2, and cycle rank t+1. On the NO source there is no unsatisfiable subgraph of fewer than t vertices. This defeats any proposed **sufficient necessity argument** relying only on these scalar counts, the presence of both labels, directed acyclicity, or an absence of short UNSAT subgraphs. It cannot defeat a separately specified worst-case lower-bound invariant that genuinely incorporates source-aware algorithms.

## Exact unannotated recognition and same-realization resource account

Authenticate the complete canonical source with header "p t5 n m", ordered "v i" rows for all i and lexicographically sorted distinct "a u v" rows. Invalid encodings are rejected. On recognized sources there is one s with in/out degrees (0,4), one t with (4,0), p+q private witnesses with degrees (1,1) and p+q-2 internal terminals with degrees (2,2). For each proposed witness w identify its unique predecessor u and successor v, require the original arc u->v, and ensure all three source arcs account for every actual input arc *exactly once*. Remove witnesses only for analysis, then check that the remaining original direct arcs form precisely two internally vertex-disjoint directed s-to-t paths, each length at least 2, whose union covers all terminal vertices. This procedure recognizes arbitrary source vertex relabelings without using a supplied generator or promise certificate. Its output count is exactly 5 or 0 depending on p-q mod5, and a satisfying witness can be constructed and validated. A valid nonmember requires a correct exhaustive generic fallback, and need not be polynomial-time decidable.

With complete canonical input length L, the explicit vertex/arc rows imply n,m<=L. For a standard blank-start locally headed deterministic multitape machine, one conservative **joint** upper ledger including parsing, malformed rejection, row-count checks, adjacency/source indexing, failed checks, all access/address work, reconstruction, comparing original arcs, the modulo-five computation, exact count or witness, final validation, output, and all retained state is

    T_member(L) = O((L+1)^5),   S_peak_member(L)=O((L+1)^2) bits.

The generic valid-nonmember fallback may take exponential O(5^n poly(L)) time with polynomial writable space. The Python parser is a finite tested implementation, not a native TM microstep proof; the corresponding mathematical total parser can charge digit-length/row-count validation before parsing huge decimal headers. No claim that source DAGs in general are in P follows; TMR-1/078 already proves NP-hardness on DAG inputs.

## Actually executed independent finite tests

Local CPython standard library, deterministic fixed seed **202611172042** for unannotated vertex relabelings; source revision **tmr5-t5-two-path-dag079.py.v1**. Fully backtracked all **49** source parameter pairs 2<=p,q<=8, obtaining exactly the symbolic 0/5 counts. Independently tested all **17,248** induced vertex subsets omitting at least one path terminal in two NO instances F_{2,3}, F_{3,4}; every one was satisfiable. Verified source graph sizes and topological orders, individual internal-terminal deletions, and **420** parser/recognition controls covering **84 arbitrary relabelings**, **84 valid edge deletion nonmembers**, **252 malformed encodings**. Top-level check count 580; zero failures. The final local execution took 9.07 seconds; Python bytecode compile succeeded. Source local SHA256 61af3b91ed0774f252e32652c0848f6786fc41d00546dc9635a2398befed6cf3; full local JSON SHA256 9f113c6f6e7e9acc556ff5ea3c0e70de9c1cbbacce18a60810906402d6768c59. Published repository source and JSON were separately **read back**, but no repo-preflight, full LaTeX build, Lean/nanoda or independent external reviewer was executed. These are finite COMPUTATIONAL controls, not a proof of all-parameter correctness.

Artifacts: experiments/tmr/tmr5_t5_parallel_dag079.py and results/raw/tmr/2026-11-17_2042_TMR5_T5_PARALLEL_DAG079_RAW.json. The locally generated full unabridged report and exact executed code/raw are also preserved in TMR5_079_DAG_LOCAL_UNSAT_evidence.zip.

## Four gates, controls, and ranked chain

**DISJ sanity PASS restricted as a false-positive control**: many directed-acyclic high-cycle local constraints and long vertex-minimal UNSAT support coexist with polynomial exact source decision. This does not imply general solver hardness. **Relativization PASS for the fixed finite combinatorial proof**, unrestricted NP-separation transfer OPEN. **Simultaneous DTISP PASS solely for the same-run restricted upper ledger**; a forbidden resource-pair lower bound is NOT APPLICABLE. **Deterministic configuration counting PASS as an upper-bound check only**, not necessary work, not automatic randomized/quantum transfer. Natural Proofs/algebrization remain OPEN for any later unrestricted circuit transfer, not applicable to a claimed lower bound here. DISJ, Horn, 2-SAT, affine/Fourier, treewidth, unique-solution, equality, autarkies, product/padding, source inversion/quotient, adaptive FBDD/OBDD, compact tensors, caching and direct methods are all legal. Historical /341 FAIL full UNSAT authority; /386 RESTRICTED.

Ranked arrows: (1) TMR-1 specific T5 NP-completeness KNOWN THEOREM, explicit scoped 3SAT->T5 reduction PROVED/EXACT, all-algorithm SAT lower bound OPEN. (2) TMR-2 forced-triad modular quotient and source-aware cofactor results RESTRICTED; local-support-to-mandatory-work FALSIFIED here. (3) TMR-4 costed OBDD/cover compilers remain restricted upper bounds; any reverse necessity claim OPEN. (4) TMR-3 specialized exact counting/Fourier algorithms remain restricted upper bounds; generic checkpoint provider and improved evaluator OPEN.

**ONE next load-bearing dependency**: formulate and audit a quantitative source-decision necessary-work statement on genuine mixed YES/NO T5 instances **after** source-recognized triangular successor compression, mod-5 consistency, DAG decomposition and all adaptive or direct alternatives. Any candidate must exclude or account for this explicitly easy but locally deceptive family. P versus NP OPEN.

Sources: Bang-Jensen, Hell, MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3), 1988, 281-298, DOI:10.1137/0401029; Hell and Nesetril, *On the Complexity of H-Coloring*, JCTB 48, 1990, 92-110. The fixed T5 has two distinct directed triangles 0->1->2->0 and 0->3->4->0, satisfying the primary 1988 semicomplete-target dichotomy hypothesis.
