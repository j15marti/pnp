# LSPV-4/440 | Original-source Hamilton-cycle Tseitin fast-path control

**2026-11-06 06:36 PST | Route A | PROVED/RESTRICTED and COMPUTATIONAL | P versus NP OPEN**

## IDEA → SEARCH → ITERATE and falsifiers
Hypothesis: An original strict 3-CNF subfamily containing proven ordinary Resolution-hard instances can be source-authenticated and SAT/UNSAT-decided in near-linear time and logarithmic physical workspace, without uncharged connectivity, graph sidecar, or an algebraic oracle. The candidate is Hamilton cycle plus perfect matching cubic Tseitin, with endpoint pair encoded in matching-edge variable IDs. Falsifiers: (1) incorrect cubic/connected/source matching authentication; (2) sign and ID tampering evading checking; (3) graph-index or work tape requiring H cells, or more than N^(11/10) local work; (4) inability to relate any growing expander-hard 3-CNF to the language, or illegitimate promotion to universal SAT hardness.

Compared to LSPV-2/441-/444 and LSPV-4/439, this result supplies a new, locally indexed *original-clause-only* syntactic sublanguage for which a connectedness certificate is implicit in the source cycle, plus exact near-linear validation and an explicit SAT witness algorithm. Source recognition for arbitrary unordered strict CNF and general all-input SAT contraction are **not** obtained.

## Exact source and hardness-family ledger
Let H>=6 be even, and V={0,...,H-1}. Cycle edge e_i joins vertex i to (i+1) mod H and has variable ID i+1. Choose any perfect matching of V with no cycle edges; give matching pair u<v its unique original edge-variable ID J(u,v)=H+1+uH+v. Every vertex v has source literals from three distinct edges a_v=e_((v-1) mod H), b_v=e_v, c_v=J(min(v,M(v)),max(v,M(v))). The first two edge IDs in the original source are (v-1 mod H)+1 and v+1. For sign function ell_0(x)=x and ell_1(x)=not x, include exactly four strict ternary original clauses at v:

$$
C_{v,p,r}=\ell_p(a_v)\lor\ell_r(b_v)\lor\ell_{p\oplus r\oplus1\oplus\chi_v}(c_v),\quad p,r\in\{0,1\}.
$$

No 3-CNF reduction or extension variable is used. Each quartet exactly represents the GF(2) equation a_v xor b_v xor c_v=chi_v. The original clause grammar is fixed before H and before the charges.

Binary source packet: 8 magic bits 10100101, unary H, unary w where w=floor(log2(H^2))+1, then 4H vertex-grouped clauses in (p,r) order (0,0),(0,1),(1,0),(1,1); each clause is three (w-bit unsigned ID, 1 sign bit) pairs in (a,b,c) order; trailer 01. Hence

$$
N=8+(H+1)+(w+1)+12H(w+1)+2=12H(w+1)+H+w+12=\Theta(H\log H).
$$

The source uses O(H) distinct variables, but matching ID values reach H^2 and are never allocated as dense coordinates. The matching edge ID itself identifies both endpoints by integer quotient and remainder, so it is not an untrusted separate graph annotation.

**KNOWN restricted proof-size hardness:** Urquhart (JACM 1987) gives 2^{Omega(H)} *ordinary shared-DAG Resolution* length for odd-charge Tseitin on suitable cubic expanders; Ben-Sasson and Wigderson (JACM 2001) provide a width-size framework. By Robinson and Wormald (1994), almost all cubic graphs are Hamiltonian, and Kolesnik and Wormald (2014) establish positive edge expansion for almost all random 3-regular graphs. Their intersection supplies suitable graphs for all sufficiently large even H. Relabel a Hamilton cycle to e_0,...,e_(H-1); the remaining edges form a perfect matching. Injective edge-variable renaming preserves ordinary Resolution proof size. Thus the source-only language contains growing odd-charge strict 3-CNF instances requiring 2^{Omega(H)}=2^{Omega(N/log N)} ordinary Resolution nodes. This is a **nonconstructive hard-instance-existence statement**, not a uniform enumerator of certified hard graphs. The source-only decision method below works for ALL valid graphs of this form, including these hard members. ER, GF(2), native mixed R_mix341 and arbitrary SAT computation are not subject to that Resolution lower bound.

## Theorem 440.1, PROVED/RESTRICTED
There is a deterministic exact *source-membership* test and SAT/UNSAT labeler for the above binary packet language with

$$
T(N)=O(N\,\operatorname{polylog}N),\qquad S(N)=O(\log N)
$$

on the FLMV-style read-only indexed-input random-access machine, charging index address construction/erasure, full source reads, output, and peak physical work-tape space. Nonmembers are REJECTED as nonmembers, not claimed UNSAT; general CNF needs its own charged fallback.

**Membership proof.** Fully parse magic, header, framing and trailer; for each original quartet verify the 12 width-(w+1) literal fields, two cycle IDs and fixed p,r signs, common matching ID and exact four sign patterns under one inferred chi_v. Decode matching ID m via m-H-1=uH+z and require 0<=u<z<H, v in {u,z}, other endpoint nonadjacent on cycle. Use one indexed source lookup at the *other vertex's first-clause matching field* to verify reciprocal ID agreement. Every vertex has exactly one such edge and reciprocal endpoint binding, so the edges form a perfect matching; the cycle is original-source-authenticated and ensures connectivity.

**Both-label proof and constructive SAT witness.** XORing the H equations makes every original edge cancel, so odd total charge is UNSAT. For even charge set *every matching edge to zero* and cycle edge e_0=0; for v=1,...,H-1 assign e_v=chi_1 xor ... xor chi_v. All equations v>=1 hold and the v=0 equation holds exactly when the total charge xor is zero. The witness may be streamed in edge-ID order with only logarithmic counters.

**Physical charge.** Each input address and the partner lookup are computable with O(log N) bits by direct arithmetic on the fixed-width layout. Every source literal field is authenticated in O(polylog N) indexed steps; only a constant number of O(log N)-bit counters, addresses and the charge parity remain live, including all authentication phases. An optional O(N)-bit output witness is write-only and not copied into work tape. No native FLMV instruction trace was produced, so the precise constant/polylog implementation overhead is not measured.

## Independent finite validation
21 exact packets for H in {6,8,10,12,24,64,128} and three charge patterns passed producer membership, both labels, exact source length and packet hashing. Every H<=10 packet had exhaustive assignment validation; all H<=12 sign mutations, matching/cycle ID, header and trailer hostile controls were rejected. Producer: **1,374 assertions**. Separately authored Node.js checker independently reconstructing the full original signed clause sets and packet SHA-256: **37,044 assertions**. Raw JSON SHA-256 fead11b31620bd80edb5c0ba6dd4b9170f9930ad98f7edd5bf037f5d104960fe. Python host source-request instrumentation saw roughly 1.07N requests, not native FLMV time or space. Tested finite graphs are **not** asymptotic hardness certificates. Full producer, independent checker, source fixtures, raw output and SHA-256 manifest are in the reproducibility ZIP.

## Resource/transfer audit
There is no proof DAG minimum, native R_mix341 certificate, new split/discharge rule, optimizer search or guest execution. Source acquisition and authentication are explicitly charged: O(N polylogN) work, O(logN) workspace, zero external graph annotation. Failed recognition and a generic SAT fallback are separate and unbounded by this theorem. No q-child materialization, caching, shared-DAG reuse, retrieval, recomputation, guest-state simulation, or any claimed reduction of an arbitrary solver's own time/space occurs. The result therefore **does not** imply the desired all-input recursively iterable same-machine recurrences

$$
t'\le\max(11/10,3/5+t/2),\quad s'\le\max(1/2,s/2).
$$

The already verified conditional FLMV margin at (6/5,1/2) is 1/90, but construction of an all-input A->Phi(A) remains OPEN. This work is a strongest-algebraic-shortcut control that cannot be excluded when minimizing legal work. Route B's full native mixed all-rule minimum, noncircular same-calculus B3, and P versus NP remain OPEN.

## Sources actually reviewed
Primary: Urquhart (1987) DOI 10.1145/7531.8928; Ben-Sasson/Wigderson (2001) DOI 10.1145/375827.375835; Robinson/Wormald (1994) DOI 10.1002/rsa.3240050209; Kolesnik/Wormald (2014) DOI 10.1137/120891265; FLMV (2005) DOI 10.1145/1101821.1101822. Project: Nov 2 five-role governing handoff (historical commit 4e29ed7), issue #3 through LSPV-2/444, AGENTS.md, CODEX.md, pnp-research skill, LSPV-4/439, LSPV-2/441-/444, actual GROKPROOF/2026-11-06_1220_PROGRESS.md and research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex. Repositories inspected: konard/p-vs-np/proofs/complexity/README.md (finite one-tape, not FLMV), blkph0x/p-vs-np-proof-research/METHOD_INDEX.md and CERTIFIED_RESIDUAL_QUOTIENT_REPORT.md (certified incomplete quotient), MassimoLauria/cnfgen/cnfgen/families/tseitin.py, openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (bounded concrete driver only). No Google-branded direct search or external repository code execution was done. All five roles, tasks, schedules, and historical inference weights unchanged.

**Precise remaining gap:** construct a valid universal both-label malformed-aware compiler producing *genuinely smaller* SAT inputs of at most N^(1/2+o(1)) for every uniform polynomial SAT guest, with fully charged branching and joins, or rigorously falsify a stated candidate architecture. P versus NP OPEN.
