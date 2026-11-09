# LSPV-4/518: Authenticated Tseitin charge-parity streaming work-stack upper control

**2026-11-09 03:36 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Nodes.** New evidence [P2-L4-518], refining [P2-L2-517], [P2-L4-508], [P2-L4-517]. All-input [P2-A2], full native resources [P2-A4], recursive applicability [P2-A5], and Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. Root proof1 nodes [P1-01], [P1-03], [P1-04] remain OPEN.

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis.** LSPV-2/517 proves 2^k different completed input-read traces for any correct independent guest execution over source-local parity charges. A *different*, direct shared semantic algorithm can still emit all q=2^k SAT labels in O(q) total sequential-tape work, using parity and no completed-trace cache. We should distinguish label-only output from explicit child-CNF output, then charge every physical source/WORK/OUTPUT phase.

**Predeclared falsifiers.** (F1) A charge flip changes original IDs/widths or other than exactly four first-literal signs. (F2) Any decoded proper strict 3-CNF label disagrees with charge parity. (F3) DFS parity enumeration needs nonadjacent WORK jumps, excessive WORK high-water, or fails parity restoration. (F4) A claimed fast bound hides source authentication, qM mandatory explicit-output bits, or simultaneous parent/child storage.

**Continuity.** Read both root proof trackers completely at research-stage SHA proof1.txt 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2.txt fba76512d502cdf2f405a336a7fc43068f40ea50. Read issue #3 including current LSPV-2/517 and LSPV-4/517 peer comments; AGENTS.md (4ae902888754d0b06ba4ce1aaeca0657a92b46a9), CODEX.md, .codex/skills/pnp-research/SKILL.md; governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (c3889a3e514ddbd747150dcb68607013a3b2d154); peer research/agents/lspv-2/2026-11-09_0317_LSPV2_LOCAL_CHARGE_PARITY_READ_FIREWALL517.md (c943791453d9f6bcb1db6c933b7cd7fa1bc48d58) and research/agents/lspv-4/2026-11-09_0303_LSPV4_DEFERRED_PIN_QUERY_OPTIMUM517.md (5ac6a5ccd253f45a1da6ea45ed399fd704af615a); GROKPROOF/2026-11-08_1130_PROGRESS.md (6942a99f176e996e9542f0386b7aa7fe2ce89e70); actual Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a); and the newly governing research/coordination/2026-11-09_KNOT_LINK_TOPOLOGY_SAT_FIVE_ROLE_HANDOFF.md (0289edb73d1e38492f0693844667be59d4152785). Claude's sequential-access SAT lower-bound does not transfer to a highly restricted parity-label enumerator or to random-access FLMV SAT.

**Research/source checks.** Urquhart (1987), Hard Examples for Resolution, JACM 34(1), 209–219, DOI 10.1145/7531.8928, is an ORDINARY shared-DAG Resolution expander/Tseitin lower bound. Fortnow–Lipton–van Melkebeek–Viglas (2005), Time-Space Lower Bounds for Satisfiability, JACM 52(6), 835–865, DOI 10.1145/1101821.1101822, gives the indexed-input machine and the joint lower-bound target, not a certificate-to-machine translation. Actually read MassimoLauria/cnfgen/cnfgen/families/tseitin.py (blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab), konard/p-vs-np README.md (0e0ec77f83ad6eec1719a96066108b96ac1c2a95) and scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5) and INDEPENDENT_AUDIT.md (b30515cced93d8911a6415555ee9ec1444502d93); meelgroup/frat-xor README.md (38a137bca4d4ab6443703d4c31fba5783021c581); openai/math CONTENTS.md (7e1ed90ac5a666f1bbecb22027387c4ad79e9d03). Checked current web primary abstracts and 2025 Cheng et al. arXiv:2509.13120 pairwise-mod-2 link-hardness shortcut, which cautions against assuming higher-order linking is necessary. No separately authenticated Google-branded search, historical R_mix341 checker, or native FLMV instruction-level execution was performed. These sources are not unrestricted P-vs-NP proofs.

**Iteration.** F1–F3 survived an independent symbolic reconstruction; F4 required replacing the tempting unit-cost random-access Gray-code update by an adjacent-cell DFS on sequential WORK, and splitting labels-only from full child-materialization interfaces. The corrected result is an upper control, not a hard-family machine lower bound.

## Exact original strict 3-CNF and known hardness

Fix a connected simple cubic graph G with n even vertices and m=3n/2 edge variables. Each vertex equation on its 3 incident edges, XOR of three edge variables equals charge b_v, is represented by four ORIGINAL proper 3-clauses forbidding the opposite parity. For b_v=0, the forbidden local triples are 001, 010, 100, 111. Changing the vertex charge toggles exactly FOUR first-literal sign bits, keeping IDs and clause length fixed.

The binary packet is 8-bit magic 10110110, unary 1^m0 count, four ordered ternary clauses per vertex, each literal with unsigned w=ceil(log2(m+1))-bit ID followed by one sign bit, and terminal 01. Therefore

$$
M(n)=8+m+1+12n(w+1)+2=\Theta(n\log n).
$$

With k=n-1 independently variable vertex charges and last charge fixed, rank of the graph incidence matrix over GF(2) proves, for every r<=k and validated base charges b,

$$
\operatorname{SAT}(F_{b\oplus(d,0^{n-r})}) \iff
\bigoplus_v b_v \oplus \bigoplus_{i=1}^r d_i = 0.
$$

Odd-charge expander instances in Urquhart's published family have exponential *ordinary Resolution* proof-size lower bounds, not SAT algorithm hardness, GF(2) hardness, mixed R_mix341 hardness, or an inherited lower bound through another encoding. K4 and prism graphs below are finite source/format controls only, NOT certified asymptotic hard families. Algebraic XOR/Gaussian elimination is a mandatory legal semantic shortcut.

## PROVED/RESTRICTED: sequential-WORK streaming labels

For any VALIDATED member of this connected cubic Tseitin family and a chosen r<=n-1 charge coordinates, a deterministic finite-control transducer with sequential constant-alphabet WORK and write-only OUTPUT can emit all q=2^r classifications in lexicographic descriptor order. Its enumeration performs exactly 2q-2 downward and 2q-2 upward *adjacent depth-head* moves, O(q) state updates, q OUTPUT symbol writes, and uses O(r) enumeration WORK cells.

**Proof.** Store a depth-r binary-tree DFS stack with a constant-size frame per level taking states unvisited, zero-subtree completed, and one-subtree completed. The finite controller retains one current parity bit initialized from validated base charges. Every descent increases depth by one WORK cell, toggling parity only on the 1 edge. Every ascent decreases depth by one, undoing the same toggle. At a leaf output 1 (SAT) precisely when running parity is even, else 0 (UNSAT). Induction over the current path gives the correct charge parity at each leaf; the DFS visits each binary descriptor leaf once in lexicographic order. A full binary tree with q leaves has 2q-2 edges; each is traversed once down and once up, giving exactly 4q-4 adjacent WORK moves. The parity is restored at root, and peak frame position is r+1. This construction requires neither q stored guest traces nor q fresh guest executions. It does NOT contradict the physical completed-read-query claim of [P2-L2-517], which concerns a different algorithm.

**Original-source authentication.** A conservative fixed-tape algorithm can sequentially parse canonical bounded-unary header and original ordered clause groups, check IDs, degrees, duplicate/reused edges, graph connectivity, and extracted charges by repeated record scans. Malformed or unexpectedly long inputs are rejected using length-bounded scans; temporary parsed graph and BFS storage O(M) bits. An intentionally conservative high-level physical upper ledger is O(M^2) sequential-tape transitions and O(M) maximum WORK high-water for this special recognizer. The symbolic hosted verifiers DO NOT constitute a native instruction listing or a proof of the exact FLMV fixed-track conversion constant. Including this phase, the restricted recognizer plus output transducer has the bound

$$
T_{\rm labels}(M,r)=O(M^2+2^r),\qquad S_{\rm all\ phases}(M,r)=O(M+r).
$$

On malformed or off-template input this device returns unsupported, NOT a general correct SAT classification. A generic correct decider A as fallback would require its full independently charged time and space. Thus no all-input contraction follows.

**Explicit original child packets.** If a consumer insists on writing each entire child 3-CNF source, the serial OUTPUT interface alone requires Omega(qM) writes. A sequential mutable M-bit child buffer with exact four-position flips per charge-tree edge, each implemented by charged O(M) WORK scans, plus an O(M) full copy to OUTPUT at each leaf attains

$$
T_{\rm children}(M,r)=O(M^2+qM),\qquad S_{\rm all\ phases}=O(M+r).
$$

This charges output, source read, buffer, tape moves and the simultaneous parent/child state; no free random WORK access is assumed. Any subsequent guest simulation, child conversion, cache retrieval, replay, failed policy, or recursively invoked SAT solver is ADDITIONAL. There are no failed policies or guest calls in this specified specialized output routine, rather than free unaccounted operations.

**Route-A exponent control.** Let formal parent N=M^2, select r=floor((3/5)log2 N) <= n-1 for sufficiently large n, so q=2^r=Theta(N^(3/5)) and child length M=N^(1/2). On this restricted family alone:

$$
T_{\rm labels}=O(N),\quad T_{\rm children}=O(N^{11/10}),\quad S_{\rm all\ phases}=O(N^{1/2}).
$$

This matches the intended LOCAL output exponents, not an all-input A-dependent t' or s' contraction, and in particular proves no recursive same-machine applicability. Serial outputs imply work and critical-path span at least q symbols or qM bits, respectively; no independent parallel speedup of a serial output tape is assumed.

## Exact checks and machine-resource ledger

Independent Python independently encoded, decoded, and brute-force edge-assignment-checked 840 original signed strict-three charge descendants on K4, prism3, prism4, prism5, with 4,316 assertion groups and 20 malformed/corrupt controls PASS; source lengths M=209,380,503,626. Python code SHA256 c30e12b2e8b5cec6f909aef91214a9aaf9775e23969f7c3f47e90c981db84651 and raw JSON SHA256 2e457532efbf900b09199210d11dfb918d71c198d7a432babfacf715ef3c8cd9; both are in the conversation reproducibility archive.

The separately authored GitHub JavaScript verifier experiments/arc/lspv4_518_streaming_parity_workstack.js (blob 6d6367265f27570fb2d98773e761df59e7df05d2) independently checks all 840 packet descendants, 20 malformed controls, 10,213 assertion groups, and exact adjacent stack-edge counts. Published raw results results/raw/arc/2026-11-09_0336_LSPV4_518_WORKSTACK_JS_RAW.json (blob d33e415e22b15020ab3a55558961b1782dc8bae3). Both PASS, not an execution of native FLMV or historical R_mix341.

| Phase | Label-only bound | Explicit child-packet bound |
|---|---|---|
| Physical source INPUT and identifiers | M bits, charged bounded-unary parser | same |
| Full source validation / graph BFS / malformed | O(M^2) time, O(M) peak bits | same |
| Local choice/policy search/failed proposals | no search/failures by fixed selected coordinates | same |
| Semantic arithmetic | 1-bit charge parity, source-derived | same |
| Descend/reconverge/WORK stack | 4q-4 adjacent head moves; O(r) WORK | O(q) DFS edges plus O(M) charged WORK scan per edge |
| Source/INDEX conversion and retrieval | source parsed once; zero guest or INDEX jumps in enumeration | sequential physical M-bit child buffer |
| Cache, replay, recomputation | none required by this algorithm | buffer updated, no q-cache |
| Output | q labels; at least q serial writes | q*M original-source bits; at least qM writes |
| Guest simulation / all-input fallback | **NOT PERFORMED**, unrestricted cost OPEN | **NOT PERFORMED**, unrestricted cost OPEN |
| All-phase peak simultaneous WORK | O(M+r), includes parsing and stack | O(M+r), includes mutable source buffer |
| Work versus critical-path span | serial q-output lower bound | serial qM-output lower bound |

The logical source contains 4n original 3-CNF clauses, each 3 literals; explicit packet has exactly M bits. No proof-DAG paid inference nodes are asserted; if future certificates are introduced their complete bit lengths and all native rules will be charged separately. The user-requested optimal-choice shared-DAG relaxation remains intact.

## Remaining transfer / publication limitation

The universal, malformed-aware, both-label, effective, recursively iterable SAME-FLMV-machine transformation must operate for every arbitrary total correct polynomial-time SAT decider A, on every binary source, including all guest operations, virtual child materialization/lazy reads, failed policies, cache, storage, output, source authentication, and full all-phase peak. No such transformation is constructed here. The recurrence t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2) remains CONDITIONAL. [P2-A2], [P2-A4], [P2-A5], [P2-B1], [P2-B2], [P2-D1], [P2-C3] remain OPEN; P versus NP remains OPEN.

Root main.tex returned SHA fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba but zero file content, so preserving other agent regions byte-for-byte could not be proved. It was deliberately not edited. The user-requested knot/link candidate is read and logged, not promoted to a theorem. No tasks, identities, schedules, states, Route allocations, R_mix341 grammar or weights were changed.
