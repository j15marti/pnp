# T5-CYCLE-MITM1: exact split-and-list branch-candidate acquisition

Date: 2026-11-19 KST. Role: Independent Red Team. P versus NP remains **OPEN**. Independent external mathematical review remains pending.

## Outcome

The degree-two thread quotient turns branch-candidate acquisition for a designated deletion into an exact multi-choice subset-sum problem in a fundamental-cycle space over \(\mathbb F_5\). A balanced meet-in-the-middle algorithm finds a candidate in square-root-of-enumeration time. This is a source-aware upper-bound counterexample to any proposed lower bound that assumes every endpoint-choice tuple, or every \(5^\beta\) syndrome, must be visited.

It is not a polynomial-time algorithm on the unrestricted intrinsic-critical family. Growth of girth, branch count, cycle rank, or the choice product does not by itself imply a time lower bound.

## Claim card and quantifiers

Input: an explicit oriented graph \(H\), promised connected, edge-minimal T5-UNSAT, and one designated original arc \(e\). Let \(P\) be the maximal degree-two thread containing \(e\), and let \(G=H-e\). Colors are \(\mathbb F_5\), with \(R(a,b)\) exactly when \(b-a\in\{1,3\}\).

The theorem below applies to every such input after paid parsing and suppression. The finite experiment separately authenticates one 33-vertex obstruction and all 44 of its deletions. It does not substitute advice, a selected easy deletion, or an UNSAT refutation for a uniform SAT-witness algorithm.

Falsifiers fixed before the run:

1. A surviving-thread increment tuple satisfying the cycle equations that fails to induce branch colors.
2. A returned branch assignment that fails an intact endpoint relation.
3. A deletion witness that fails any retained original arc or satisfies the missing arc.
4. A split whose claimed square-root bound silently assumes binary rather than 2--4-way choices.
5. An uncharged dense fundamental-cycle matrix, source scan, lift, output, verifier, or memory table.

None occurred. The implementation uses expected-time Python hashing, but correctness is deterministic; deterministic radix sorting of \(\mathbb F_5^\beta\) keys gives the stated worst-case existence bound.

## Exact theorem: thread-cycle multi-choice reduction

Suppress the maximal degree-two threads. The structural handoff gives thread lengths \(1\le L_t\le3\). Orient each thread from its recorded left branch to its right branch, and let \(r_t\) be its number of backward-traversed arcs. Its attainable endpoint increments are

\[
d_t=a_t+2j_t\pmod 5,\qquad a_t=L_t+r_t,\qquad j_t\in\{0,\ldots,L_t\}.
\]

Delete the whole relation for the thread \(P\) containing the designated missing arc. The surviving branch core is connected: the supplied 2-vertex-connectivity theorem excludes a branch-core bridge. Let it have \(q'\) surviving threads, \(b\) branch vertices, and cycle rank \(\beta=q'-b+1\). Construct any signed fundamental-cycle matrix

\[
C\in\mathbb F_5^{\beta\times q'}.
\]

An increment vector is induced by branch potentials if and only if it has zero circulation, so branch candidates are exactly the solutions of

\[
C(a+2j)=0,
\quad\text{equivalently}\quad
\sum_t (2C_t)j_t=-Ca.
\]

Thus candidate acquisition is an exact multi-choice subset-sum instance in \(\mathbb F_5^\beta\). Let

\[
D=\prod_{t\ne P}(L_t+1).
\]

Greedily put each 2--4-way variable into the currently lighter product side. The two side products have ratio at most four, hence each is at most \(2\sqrt D\). Enumerate partial syndromes on both sides and join complementary keys. A matching pair yields every \(j_t\), tree integration yields branch colors, and the existing canonical thread lift yields all original vertex colors.

Including explicit source parsing, adjacency construction, suppression, a dense fundamental-cycle matrix, candidate acquisition, reconstruction, the \(n\)-symbol output, and the \(m-1\) retained-arc verifier, a conservative word-RAM upper bound is

\[
O\!\left(n+m+q'(b+\beta)+(q'+\beta)\sqrt D\right)
\]

time and

\[
O\!\left(n+m+q'\beta+(q'+\beta)\sqrt D\right)
\]

words. Radix sorting the base-5 syndrome vectors gives a deterministic implementation; the executable uses a hash table and records its actual memory. Since \(D\le4^{q'}\), this gives an \(O(2^{q'}\operatorname{poly}(n+m))\) upper bound, not a polynomial bound in general. It should be portfolioed with the prior exact syndrome DP, giving the candidate-search comparison

\[
\operatorname{poly}(n+m)\min\{5^\beta,\sqrt D\}
\]

up to the displayed coordinate factors. The \(5^\beta\) branch is the already recovered TMR-4/086 cycle-gauge DP; no novelty claim is made for cycle equations or for meet-in-the-middle itself.

Status: **PROVED/EXACT**. External peer review is open.

## Critical deletion lift

Any branch solution of the surviving relations must violate the omitted thread relation: otherwise that thread would also extend and color the promised UNSAT graph \(H\). Removing the one original arc \(e\) splits its thread into two rooted path fragments, each greedily extendible from its branch endpoint. Every intact thread is filled by a constant-size lookup. Therefore one candidate search for thread \(P\) serves every deletion position in \(P\); producing all complete witnesses still pays its \(\Omega(mn)\) output volume.

Status: **PROVED/EXACT**, independently exercised here; this lift was already present in the project and is not claimed as new.

## Executed finite audit

Authenticated source:

`SHA256(source079.t5) = 0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac`.

The run parsed 33 explicit vertices and 44 original arcs into 19 branch vertices and 30 threads: 20 of length one, six of length two, and four of length three. The full branch core has cycle rank 12. An independent five-domain propagation/DFS check proved the full compressed instance UNSAT in 33 recursive nodes; this count is finite evidence, not a lower bound.

After omitting any one thread, \(q'=29\), \(\beta=11\), and all 29 choice variables remained cycle-active. The raw choice product was:

| Omitted length | Cases | Surviving choice product \(D\) | Max stored side | Max other side |
|---:|---:|---:|---:|---:|
| 1 | 20 | 97,844,723,712 | 221,184 | 442,368 |
| 2 | 6 | 65,229,815,808 | 221,184 | 294,912 |
| 3 | 4 | 48,922,361,856 | 165,888 | 294,912 |

Across all 30 omissions, the executable enumerated 6,414,336 stored-side leaves and 1,711,981 other-side leaves before matches. It produced one branch candidate per thread, lifted those candidates to all 44 original missing-edge positions, checked 1,892 retained arcs, and confirmed that all 44 missing arcs were violated. A separate JSON consumer re-parsed the source and repeated these semantic checks.

The last complete run took 22.24 seconds and reported peak RSS 223,060 KiB in this Python realization. These measurements include parsing, the full-core check, all 30 tables, lifting, complete witness serialization, and verification. They are not asymptotic claims.

Status: **COMPUTATIONAL** for the authenticated finite source.

## Prior work and literature boundary

Project recovery found TMR-4/086's exact signed-cycle syndrome DP and TMR-3/083's Fourier/rank-cutset algorithms. The present theorem is best read as a thread-compressed split-and-list companion bound. A targeted project search found an older general split-and-list discussion but no indexed T5 thread-cycle instantiation; that is not sufficient for a priority claim.

The classical source is Ellis Horowitz and Sartaj Sahni, “Computing Partitions with Applications to the Knapsack Problem,” *JACM* 21(2), 277--292 (1974), DOI [10.1145/321812.321823](https://doi.org/10.1145/321812.321823). Their square-root split-and-list technique is background; the proof above specializes it to the exact T5 thread-cycle system.

The literature checked in prior recovery still does not provide a compiler into connected globally edge-minimal UNSAT high-girth obstructions with a designated deletion, paid criticalization, and witness decoder. Fixed-girth CSP hardness and Kun's fixed-parameter sparse-incomparability theorem do not establish the stricter growing-girth intrinsic-critical promise.

## Lower-bound red-team ledger

- **FALSIFIED:** every endpoint-choice tuple must be inspected; every \(5^\beta\) syndrome must be materialized; thread-internal multiplicity requires separate candidate searches; a dense cycle matrix can be treated as free.
- **PROVED:** exact cycle-space multi-choice formulation; balanced square-root split; charged reconstruction/lift/verifier; one candidate per thread serves all its missing-edge positions.
- **CONDITIONAL:** the complement-pinning argument uses the promised UNSAT property of \(H\); use on an unauthenticated source requires separately establishing the promise.
- **OPEN:** a polynomial witness finder on all intrinsic-critical growing-girth deletions; a matching lower bound for unrestricted execution; source-preserving promise NP-hardness; an infinite hard family surviving algebraic, separator, treewidth, and recognition shortcuts; P versus NP.

DISJ and configuration-counting gates: no information statistic is promoted to necessary time. Relativization/algebrization: no separation is claimed; the algebraic shortcut is an explicit counterpressure. Circuit/proof-complexity gates: no restricted representation lower bound is transferred to general execution. Simultaneous time-space: only a realized upper bound is recorded.

## Next blocker

Apply the portfolio bound \(\min\{5^\beta,\sqrt D\}\) to a genuinely growing, authenticated intrinsic-critical family. The next useful target must remain hard after thread suppression, connected-component and separator recognition, treewidth DP, low-rank cycle DP, this split-and-list search, and canonical lifting. Branch-core or girth growth alone is not enough.

Governance: additive red-team report only. No owner manuscript, title, role, schedule, or paused/disabled state was changed.
