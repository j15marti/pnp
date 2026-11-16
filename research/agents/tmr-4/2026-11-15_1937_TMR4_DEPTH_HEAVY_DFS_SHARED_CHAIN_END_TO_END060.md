# TMR-4/060: authentic shared-DAG depth-heavy DFS versus depth spill

Date 2026-11-15 19:37 PST, owner TMR-4, Tracks A/C. Governing directive 2026-11-15_END_TO_END_AGENT_MANUSCRIPTS, blob 8451d955f6cd5397de0895f8ebb46e30818842c3. Status PROVED/EXACT RESTRICTED with external mathematical review OPEN; finite audit COMPUTATIONAL. P versus NP OPEN.

## Candidate and four falsifiers, pre-search

Named dependency D4-LOW-CONGESTION-DISCOVERY after /059. For every integer m>=1, authenticate an actual source circuit C_m with real shared gates, derive a topological priority DFS without supplied layout, and compile its authentic gate/input schedule to a complete labelled OBDD. Claim original-source live width <=3, OBDD nodes <=8n, and both terminal values and exact labelled-path count, although the existing /059 depth schedule requires live width >=2m on the identical input. This closes the discovery dependency ONLY for the displayed infinite shared-DAG family, not for all shared circuits.

Falsifiers: (1) recurse into a shallow sibling before an accumulator predecessor, potentially retaining one value per recursive level, so use decreasing actual gate depth; (2) duplicate/recompute rather than charge real shared gate identities; (3) collapse distinct 0/1 labelled arcs and lose exact counting multiplicity; (4) malformed source, duplicate keys, huge declared input count or cyclic/dead gates bypass authentication. A genuine algebraic streaming shortcut is admitted, not declared spurious.

## Authenticated input, construction and theorem

Canonical ASCII JSON has exactly n,gates,out. There are n original input identities and g distinct binary gates, each with exactly id,a,b,op, where op in 0..15 encodes its original four-entry truth table. Gate records may have arbitrary order. All n inputs/g gates must reach one gate output; no cycles, invalid reference or duplicate key. Reject malformed words, not as UNSAT. Verify n<=2g BEFORE n-indexed allocation. The executable actually authenticates the complete source and reverses all gate record IDs in this family.

For every m>=1 set n=2m+1, g=4m, a_0=x_0, and for i=1,...,m define

    h_i = x_(2i-1) XOR x_(2i)
    p_i = a_(i-1) AND h_i
    q_i = a_(i-1) XOR h_i
    a_i = p_i OR q_i.

Output a_m. Every h_i is consumed by two genuine gates and a_(i-1) is also shared, so this is not a fanout-one formula tree. The original source includes nonaffine AND and OR gates. However the function is semantically easy, since a_i=a_(i-1) OR h_i. Therefore

    #C_m = 2^(2m+1) - 2^m.

The depth schedule of /059 introduces all 2m new pair-input identities at gate depth one, before any h_i evaluation, forcing original-signal live width >=2m. This is a prescribed-layout obstruction only, NOT an all-algorithm lower bound.

Compute gate depth d(g)=1+max depth of its genuine gate predecessors, original inputs depth zero. Recursively visit output predecessors in descending depth order, ties by stable ID. Emit each original source identity in postorder EXACTLY ONCE, retaining the emitted value until its last genuine consuming gate. For every i>=2, the accumulator predecessor is deeper than local h_i; in the first module the source input x0 has depth zero and may be visited after h_1, which changes no width bound. The DFS nevertheless completes genuine modules in order i=1,...,m. Between modules the only live original source value is the preceding accumulator. During a module, at most that accumulator plus two new inputs coexist (3); after h_i the input values expire; after p_i the live triple is accumulator,h_i,p_i; evaluating q_i retires accumulator,h_i, leaving p_i,q_i; evaluating a_i retires p_i,q_i. Thus **w_DFS<=3 for all m**, excluding separately charged constant physical scratch.

Compile exact source events to an OBDD by splitting on each actual input event (both 0 and 1 labelled arcs), executing subsequent original gate events deterministically, and retiring only values after their real last use. The retained tuple determines every remaining actual source computation. Induction over ALL n+g source events proves exact value preservation, both terminal labels and correspondence of each complete source assignment to one complete labelled OBDD path. Parallel labelled arcs remain two paths for counting purposes. Therefore

    V(B(C_m)) <= n * 2^w <= 8(2m+1)
    #accepting labelled paths = #C_m.

For every field K and any prefix of this discovered input order, the original assignment matrix factors through at most 2^w genuine retained-source tuples. Hence rank_K(prefix)<=2^w<=8. No inference to arbitrary equivalent circuits, optimal OBDDs, general SAT solvers or a required source space lower bound. This is a construction, not a free-answer abstract transition.

## SAME_REALIZATION upper resource ledger

Let L be all authentic source bits, M=n+g, A=n2^w<=8n and

    B=O(L+(M+nM)ceil(log2(M+2)))
    D=1+L+B+O(A(w+n+ceil(log2(A+2)))).

A single fixed locally headed deterministic multitape machine can authenticate source bytes, check malformed structures before excessive allocation, discover depths and priorities, traverse original gate IDs with a visited set, find exact last uses, materialize true OBDD 0/1 arcs, maintain <=n+1-bit exact path count integers, and emit result plus validation. Conservative simultaneous bounds **T_total=O(D^5)** and **S_peak=O(D)** account for reads/seeks/heads, decimal IDs, parsing, invalid paths, graph checks, discovery/failed checks, DFS stack, retained source values, shared objects once, temporary scratch, branching states, caches, counting arithmetic and real output. Here L=Theta(m log m), D=O(m^2 log m), so both are polynomial in L on this family. General valid circuits may have w=Theta(n), and OBDD compilation can be exponential. Python semantic testing does not constitute an executed physical machine trace.

The proposed source-to-OBDD chain never silently changes original-input counting to full wire-variable counting. Any future Tseitin CNF conversion must charge the actual auxiliary variables, wires and functional constraints.

## Actually executed independent finite evidence

Local CPython 3 standard library, deterministic exhaustive, revision tmr4-dfs-shared-chain060.release1, seed not applicable, **10,952 checks, zero failures**, 2,728 complete source assignments, 5,456 genuine 0/1 OBDD path replays, five malformed-source rejections including huge n and duplicate keys. Each assignment was compared against independent original source recursive evaluation and the closed form; both ordered OBDDs were checked for exact accepted/rejected path counts and actual node bounds.

The exact executed code is experiments/tmr/tmr4_dfs_shared_chain060.py, Git blob 81cead7009c0094ee94a571b3a4ade6469149f7e, matching the local git hash-object. The complete locally produced sorted-key raw JSON is results/raw/tmr/2026-11-15_1937_TMR4_DFS_SHARED_CHAIN060_PY_RAW.json, Git blob 5df58227b08a0105b0484106a18ad9cb3cbd7eb6, again matching local bytes.

| m | Depth live width | DFS live width | Depth OBDD nodes | DFS OBDD nodes |
|--:|--:|--:|--:|--:|
| 1 | 3 | 3 | 5 | 5 |
| 2 | 4 | 3 | 19 | 11 |
| 3 | 6 | 3 | 71 | 17 |
| 4 | 8 | 3 | 271 | 23 |
| 5 | 10 | 3 | 1055 | 29 |

These are UNREDUCED constructed representation sizes, never minimal OBDD lower bounds. Finite tests are COMPUTATIONAL. No local repo checkout means no repository preflight. Native locally headed Turing microtrace, independent external mathematics review, LaTeX compilation and Lean kernel all NOT RUN.

## Four mandatory gates

| Gate | Verdict and reason |
|---|---|
| DISJ sanity | PASS restricted. DISJ_k has rank 2^k but linear depth-two circuits. Any unrestricted static-rank hardness transfer FAILS; this is only an upper compiler. |
| Relativization | PASS intermediate; NP separation OPEN. DFS and register replay are relativizing. No purported nonrelativizing NP step; algebrization and Natural Proofs issues remain OPEN. |
| Simultaneous DTISP | PASS for this ONE physical upper cost ledger; lower-bound implication OPEN. Both T and peak S are charged for the same complete run, no strict FLMV contradiction. |
| Deterministic configuration counting | PASS upper-bound guard. T<=2^{O(S+log L)} for a total read-only-input deterministic machine, NOT a necessary-work lower bound nor randomized/quantum theorem. |

Controls retained: DISJ, Horn, 2-SAT, affine/Gaussian, bounded treewidth, equality, autarky, products, padding, auxiliaries, selectors, unique-solution rank-one tensor and every real compact/streaming/recomputation path. Invertible local basis maps preserve rank; Walsh-Hadamard is not invertible over F_2. Randomized Valiant-Vazirani isolation is charged. /341 remains FAIL as full logical UNSAT authority, /386 RESTRICTED. P versus NP OPEN.

Original sources reviewed: Sethi, Complete Register Allocation Problems, SIAM J. Comput. 4(3), 1975, DOI 10.1137/0204020; Bryant, Graph-Based Algorithms for Boolean Function Manipulation, IEEE Trans. Comput. 35(8), 1986, DOI 10.1109/TC.1986.1676819. Original project evidence: /059 authentic shared-DAG theorem/code, TMR-2/058 shared-edge trace and TMR-1/058 source compiler. This is NOT claimed to be a new universal register-allocation algorithm.

**ONE NEXT D4-LOW-CONGESTION-CERTIFICATION (OPEN):** Find a polynomial-time checkable source-local certificate, actually constructible without external advice, guaranteeing O(log L) depth-heavy DFS live width for a broader unbounded genuine shared-gate DAG class, preserving the fully paid end-to-end counting and decision compilation. Arbitrary-algorithm reverse necessity remains OPEN.
