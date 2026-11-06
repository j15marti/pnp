# LSPV-4/435: Reversible DFS edit replay replaces depth-banked Tseitin state

**2026-11-06, America/Los_Angeles (PST). Route A primary. PROVED/RESTRICTED mathematics, COMPUTATIONAL host-language tests; peer review pending. Universal FLMV contraction, same-system B3, and P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE: specific hypothesis and falsifiers

Hypothesis: the depth-banked epoch arrays in LSPV-4/434 are unnecessary for *depth-first* evaluation of an authenticated shared-base cubic Tseitin family if every child edit descriptor is immutable, exactly replayable from the actual read-only parent source, and independent of the mutable charge bank. A single mutable H-bit parity bank can be restored by applying the same XOR edits on exit, without retaining whole ancestor banks.

F1: repeated flips to one vertex or duplicate edits defeat rollback. **NO:** XOR is self-inverse even with multiplicities. F2: siblings, grandchildren, and return to the original parent corrupt parent literals. **NO** in the declared DFS interface, by induction and independent finite checks. F3: an edit generator may read the *current mutable bank*, invalidating replay. **YES:** an explicit adaptive witness makes rollback wrong; an immutable/regenerable descriptor is a necessary premise of this repair. F4: the work/index tape high-water, all input reads, and the descriptor catalog are uncharged. **NO** under the stated model: one H-cell fixed-tape bank, paid index construction/erasure, O(D log N) stored source *pointers*, and the complete descriptor catalog included in input length. No claim is made for unbounded descriptor-construction memory or guest state.

## Chosen published family and shortcut ledger

Let G=(V,E) be a connected simple cubic graph with H vertices and M=3H/2 edge variables. With public incident edge IDs a_v<b_v<c_v and charges chi in {0,1}^H, the exact original strict signed 3-CNF has, for each vertex v, the four clauses
$$
C_{v,p,r}(\chi)=\ell_p(x_{a_v})\vee\ell_r(x_{b_v})\vee\ell_{p\oplus r\oplus1\oplus\chi_v}(x_{c_v}),\qquad p,r\in\{0,1\},\quad\ell_0(x)=x,\quad\ell_1(x)=\neg x.
$$
There are 4H three-literal clauses without extension variables. The authenticated LSPV-2/437 fixed-field encoding has
$$
N_H=8+(H+1)+(M+1)+2Mw+12H(w+1)+2=\Theta(H\log H),\quad w=\max(1,\operatorname{bitlength}M).
$$
Connectedness yields SAT iff the charge XOR is zero. Odd parity is a mathematical UNSAT certificate. Published exponential lower bounds for *ordinary shared-DAG Resolution* concern suitable growing cubic expander Tseitin graphs (Urquhart 1987; Ben-Sasson/Wigderson 2001). K4, cube and Petersen here are finite semantic controls, not asymptotic hard-family certificates. Known AND3/GF(2) derivations give short permitted mixed-calculus upper-bound controls, conditional on authenticating historical R_mix341 native rules. ER, Resolution, algebraic and branching alternatives cannot be excluded to protect a lower-bound claim.

## Theorem 435.1: a one-bank stack-backtracking source port (PROVED/RESTRICTED)

Assume an authenticated read-only original formula and source-bounded depth-first portfolio tree. Every directed tree edge e has an immutable child descriptor with a repeatable sequence of in-range vertex IDs E_e=(v_1,...,v_{r_e}). Its length and individual entries can be obtained from the read-only parent using O(polylog N) native indexed time and O(log N) physical scratch, independently of the mutable bank and any guest output. A uniform public graph incidence accessor and original source-charge accessor have the same limits. The complete encoded descriptor data count toward the *actual parent input length N*. The tree depth is D, all visited edge occurrences sum to R edits, and Q source-bit/charge-port requests occur.

Initialize a single contiguous H-bit writable bank B(v)=0. On entering edge e, scan E_e and flip B(v) for every occurrence. On returning, rescan **the identical** E_e and flip those cells again, in any order. At a depth-d node the virtual source charge is
$$
\chi_v=b_v\oplus B(v)=b_v\oplus\bigoplus_{e\text{ on active root-to-node path}}\ \bigoplus_{u\in E_e}[u=v].
$$
This invariant holds after every enter and exit. Each edit is undone by a second XOR application, including repeated and unsorted entries. The parent bank is restored exactly after child completion, so all 4H original signed clauses are reconstructed bit-for-bit (not just equisatisfiably). The method supports DFS and nested parent lifetimes, **not** arbitrary simultaneous lookups to completed branches, general shared-DAG reconvergence, or source-dependent adaptive replay.

For a fixed number of FLMV indexed work tapes, choose a densely addressed one-bit-per-vertex bank on one tape. Each edit writes a binary work index, jumps, erases the index tape, reads and writes one bit. Every charge-sensitive input query likewise pays for source/index construction, jumps, erasures, and output. The source parser and descriptor authenticator must be charged separately. With all polylogs referring to the complete parent baseline N and declared operation count, the *port-only* bounds are
$$
T_{\rm port}=O((H+R+Q+D+q)\operatorname{polylog}(N+H+R+Q+q)),\qquad
S_{\rm port}\le H+O(D\log(N+H+R+Q+q)).
$$
Here q is the number of visited child edges; the 2R physical toggles and q enter/exit frame operations are included. The fixed input catalog is read-only input and is not a free oracle. The work/index high-water includes the entire H-cell capacity even when mostly zero. Unlike /434, there are **no H*D epoch banks** and each query accesses one active bank rather than D separate banks. The repair improves /434's space DH(ceil(log2(q+1))+1) and charge-port query overhead DQ, but *only under the stronger replayability premise*.

## Explicit falsifier of an overbroad repair

Let B=(0,0,0,0). A generator that says "toggle vertex 0 if B(0)=0, otherwise vertex 1" first emits vertex 0 and changes B to (1,0,0,0). Regenerating the instruction at exit now emits vertex 1, leaving B=(1,1,0,0) instead of restoring zeros. Therefore merely saying "run the same code again" does NOT suffice: the edit stream must be independently regenerable from immutable source/descriptor data, or its exact contents must be retained and fully charged. This precisely falsifies a general adaptive-policy replay claim without ruling out legal alternative schedules.

## Conditional full-wrapper ledger and remaining transfer

For any actual guest decider A on child lengths L_j, the conceptual bound is
$$
T_{\rm wrapper}\le V(N)+P(N)+J(N)+O(N_{\rm output})+
O((H+R+Q+q+D)\operatorname{polylog}N)+\sum_j O(T_A(L_j)\operatorname{polylog}N),
$$
only after independent source authentication V, actual policy acquisition and failures P, join/case-combination correctness and cost J, guest input-head simulation, and output work have been demonstrated. The all-phase physical space must include
$$
S_{\rm wrapper}\le \max\{S_V,S_P,S_J,\ H+O(D\log N)+S_{\rm simultaneously\ live\ guest/ancestor}\},
$$
and it cannot simply substitute this port-only bound for the desired recurrence. In particular, dynamically acquired source descriptors, retries, whole-child materialization, guest-state retention, and temporary buffers can exceed this claimed port bound. The current fixed-graph descendants **do not shrink**: no all-input recursively iterable transform or correct arbitrary SAT/UNSAT/malformed fallback has been constructed. Incompatible branch-local assumptions are never shared without legal discharge. No changes to R_mix341 or its weights are proposed.

## Independent finite computation, provenance and limitations

A deterministic Python producer (seed 202611060136) traversed 40 nodes per graph, 3-way depth-three trees on K4/cube/Petersen, with 39 immutable read-only-catalog child descriptors and 134 edit IDs per graph. It executed 268 toggles per graph, exactly balanced index writes/erasures, all 4H original clauses at each node, and returned to each ancestor exactly. It reported **15,014 grouped comparison units** and 54 brute-force leaf SAT checks on K4/cube. Both charge parities appeared. The independent Node.js referee read exact immutable-fixture event streams and independently reconstructed clause hashes, all 120 snapshots, 804 edit transitions and corrupted-clause/illegal-generation controls: **3,418 checks PASS**. The producer host language physically holds catalog tuples and sample clauses; its counters are *not* a measured native FLMV machine trace. The theoretical fixed-tape upper bound explicitly requires only input pointers be stored and each descriptor entry reconstructed by paid indexed reads.

The adversarial adaptive-generator witness, noncubic source, out-of-range edit, empty-stack exit, and corrupted source-literal sign were rejected or exposed as intended. An ordinary syntactically valid but out-of-family CNF must remain OUT_OF_FAMILY, distinct from MALFORMED. No authoritative historical R_mix341 checker was executed.

## Actual search and continuity record

Read governing five-role handoff blob c3889a3; current issue #3 through LSPV-2/438; AGENTS.md; CODEX.md blob 754999f5; pnp-research skill blob b8df83a; LSPV-2/437 blob 2033e9d and /438 blob df2d557; LSPV-4/434 blob 6e5a5d0; actual Grok REWIRE file blob d06a2d5 and GROKPROOF 2026-11-06_0515_PROGRESS.md blob 93f9202; Claude TPORT file blob b7150bb. Required third-party heads: konard/p-vs-np ec edd2b (proofs/complexity/README.md blob 7ee9a11; one-tape model, not FLMV), blkph0x/p-vs-np-proof-research 7dedc73 (METHOD_INDEX.md blob 18d693e; AFFINE_BOUNDARY_DESIGN.md blob ed4f4a9; affine model not unrestricted CNF). Reviewed CNFgen/cnfgen/families/tseitin.py blob 4bb5fd1, meelgroup/frat-xor/README.md blob 38a137b and openai/math/README.md blob cc5b0a. Original FLMV PDF §2.1 machine model visually checked, with indexed *work*-tape jumps and index erasure; §3.1 local-input-bit reconstruction noted. Literature: FLMV JACM 2005 DOI 10.1145/1101821.1101822; Urquhart JACM 1987 DOI 10.1145/7531.8928; Ben-Sasson/Wigderson JACM 2001 DOI 10.1145/375827.375835; Driscoll/Sarnak/Sleator/Tarjan JCSS 1989 DOI 10.1016/0022-0000(89)90034-2 (general persistence control, not a free machine conversion). Indexed web search used; Google-branded search not independently executed. Repeat of the algebraic XOR undo idea is elementary and no novelty is claimed.

**Root manuscript blocker:** main.tex SHA 5a93dce returned zero readable characters to authenticated fetch_file. No edit or overwrite of any root or peer region was attempted; owner reconciliation awaits complete bytes. All five tasks, titles, schedules, allocation (LSPV-2/4 Route A; LSPV-1/3/5 Route B), native rules and inference weights remain unchanged.

**Advance:** paid, correct one-bank DFS XOR replay replaces depth banks under explicit immutable descriptors, with a precise adaptive replay counterexample. **OPEN:** every-A all-input uniform recursively iterable same-machine A-to-Phi(A) contraction at t'<=max(11/10,3/5+t/2) and s'<=max(1/2,s/2), full V/P/J/guest/peak ledger, and separate B3. P versus NP OPEN.
