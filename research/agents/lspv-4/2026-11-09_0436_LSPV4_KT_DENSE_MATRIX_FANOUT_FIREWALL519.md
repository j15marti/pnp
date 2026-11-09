# LSPV-4/519: Dense KT-link-matrix fanout is a charged obstruction to a particular Route-A compiler

**November 9, 2026, 04:36 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**Exact nodes:** new [P2-L4-519] refines [P2-L2-518], [P2-L4-518] and resource obligation [P2-A4]. Universal all-input transformation [P2-A2], same-machine recursive applicability [P2-A5], and [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. Also [P1-01], [P1-03], [P1-04] remain OPEN.

## IDEA -> SEARCH -> ITERATE

**Initial claim.** A link-based compiler that emits an independent *full dense pairwise linking matrix* for each one of q virtual original-3CNF Tseitin children cannot meet the desired local time/WORK budgets, but an authorized sparse/shared description avoids this representation-specific barrier.

**Falsifiers stated before research.** (F1) In the actual Koenig-Tsvietkova Figure-2 construction, a clause component contributes nonzero pairwise linkage or two clause components cross. (F2) Changing a source-local vertex charge changes variable IDs, clause counts, packet length or the KT number of link components. (F3) A dense V-by-V binary matrix can be separately emitted on a serial output tape with fewer than V^2 symbol writes, or simultaneously occupy fewer than V^2 one-bit WORK cells. (F4) Shared/sparse references satisfy a contract explicitly requiring q *independent* dense matrices, or the KT matrix alone still correctly classifies an odd/even-charge SAT pair.

**Governing continuity, actual reads.** Both full root trackers: proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2.txt research-stage blob 0b22a21374fdf7008cbd142f499a08a5cd3bdc61 (718668 chars); issue #3 and recent coordination comments; original five-role 2026-11-02_1204 handoff; 2026-11-09 knot/link five-role handoff blob 0289edb73d1e38492f0693844667be59d4152785; AGENTS.md blob 4ae902888754d0b06ba4ce1aaeca0657a92b46a9; CODEX.md blob 754999f50de93cdb693ed37bc8110d31e9e698ef; .codex/skills/pnp-research/SKILL.md blob b8df83a7b0b1428f349b0e02ce1387d979e8db7f; peer LSPV-2/518 blob 9ccffb3c74c8295ffbf777582c992f6a92b00f57, LSPV-2/517 blob c943791453d9f6bcb1db6c933b7cd7fa1bc48d58, and LSPV-4/518 blob d0daf3a10a06cc966db2328f16b4a056ef5514db. Actual Grok GROKPROOF/2026-11-08_1130_PROGRESS.md (6942a99f176e996e9542f0386b7aa7fe2ce89e70) and Claude research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex (79e4d4e7e0e3edff3aba8610852c45534bdde128) read. No new FLMV transfer in either.

**Primary literature checked at source.** D. Koenig and A. Tsvietkova (2021), *NP-hard problems naturally arising in knot theory*, Theorem 1, https://arxiv.org/pdf/1809.10334 pp.3–6 including PDF page images: n variable Hopf pairs, m separately banded commutator clause loops, 2n+m components and <=2n+m(64n+10) crossings. This is a 3-SAT Karp reduction to unlink-as-sublink, not a SAT-time or proof-size lower bound. Urquhart (1987), *Hard Examples for Resolution*, DOI 10.1145/7531.8928, establishes **ordinary DAG Resolution** expander-Tseitin proof hardness only. Fortnow, Lipton, van Melkebeek and Viglas (2005), DOI 10.1145/1101821.1101822, is the matched indexed-input time/space lower bound, not a free conversion theorem. Exact project proof [P2-L2-518] confirms KT's canonical complete pairwise matrix is Hopf blocks plus zero clause block; unlike all topology, the matrix does not see clause support or signs.

**Repositories checked at actual paths/blobs.** konard/p-vs-np scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5) and INDEPENDENT_AUDIT.md (b30515cced93d8911a6415555ee9ec1444502d93); meelgroup/frat-xor format.md (986a21aa92b62f844ef1fce852193142c41b2b1f); openai/math CONTENTS.md (7e1ed90ac5a666f1bbecb22027387c4ad79e9d03). CNFgen cited by peer but attempted presumed-main fetch failed; not claimed independently re-read. No independent Google-branded engine, native FLMV machine, actual knot-diagram checker or historical R_mix341 checker used.

**Iterated result.** F1 requires the specific published *canonical band-separated* link, not arbitrary links. F2 passed source-exact tests. F3 is an elementary bit-output and WORK-high-water lower bound, with separate interfaces treated explicitly. F4 defeats any SAT claim based only on this representation and permits valid compressed controls.

## Exact family, encoding, and known shortcuts

Fix connected simple cubic G with H even vertices and E=3H/2 edges (variables). Each vertex XOR equation is represented by FOUR original proper signed ternary clauses; for zero charge forbid local assignments 001,010,100,111, and a charge flip changes only the FIRST literal polarity in each of four clauses. Thus C=4H strict-three clauses. The original binary source is 8-bit magic 10110110, unary 1^E 0, twelve H literal records with w=ceil(log2(E+1)) ID bits plus a sign bit each, terminal 01. It has
$$
M=8+E+1+12H(w+1)+2=\Theta(H\log H).
$$
For a formal parent N=M^2 take r=floor((3/5)log2 N)<=H-1, q=2^r=Theta(N^(3/5)) descriptor children, changing only r vertex charges. Every source has identical M, E, C, and strict original 3CNF syntax. XOR of all vertex equations yields SAT iff charge XOR is zero; connectivity gives sufficiency by GF(2) incidence rank H-1. Half the q children are SAT and half UNSAT. The odd-charge cubic-expander subfamily has Urquhart's ordinary Resolution lower bound, but polynomial-time GF(2) elimination is a valid shortcut. No lower bound against general algorithms or full R_mix341 follows.

In the canonical KT link there are
$$
V=2E+C=7H
$$
components. The full symmetric mod-2 pairwise linking matrix is exactly E nonzero Hopf 2-by-2 blocks plus C zero rows/columns, independently of SAT label. It contains
$$
V^2=49H^2\text{ entries, }\quad 2E=3H\text{ nonzero entries.}
$$
The published KT crossing upper bound is <=2E+C(64E+10)=384H^2+43H; this is an UPPER bound, not an observed native cost.

## PROVED/RESTRICTED output/WORK lower bounds for a specified compiler

If a candidate compiler MUST emit an independent dense V-by-V binary linking matrix for EACH virtual child on a serial write-only OUTPUT tape, then the total number of output writes satisfies
$$
T_{\mathrm{dense\ fanout}}\ge qV^2=49qH^2
=\Theta\left(\frac{N^{8/5}}{(\log N)^2}\right)=N^{8/5-o(1)}.
$$
This defeats an O(N^(11/10)) **local** time allowance. It is also asymptotically incompatible with the whole proposed t'<=max(11/10,3/5+t/2) for any fixed guest exponent **t<2**. For t>=2, or a different output contract, this time contradiction does not apply.

If the FULL matrix is simultaneously materialized on binary WORK rather than streamed, the all-phase high-water has
$$
S_{\mathrm{dense\ WORK}}\ge V^2
=\Theta\left(\frac N{(\log N)^2}\right)=N^{1-o(1)}.
$$
Thus the suggested s'<=1/2 local bound fails, and max(1/2,s/2) fails for s<2. OUTPUT is not WORK. Printing an output does **not** imply a WORK-space high-water lower bound. No blanket time/space claim is made for every SAT algorithm.

## Legal upper controls, sharing, and correctness

An explicit list of E Hopf pairs uses O(E log V) bits; with a decoder agreed in advance, a two-number parametric description (E,C) uses O(log V) bits. A serial counter-based generator streams the entire matrix with O(log V) WORK and O(V^2 polylog V) time (counting sequential WORK head overhead, no unit-cost arbitrary jumps). If q consumers legally accept a shared object and references, one dense matrix plus q reference IDs can use O(V^2 polylog V+q log q) time rather than qV^2. All reference/check/reconstruction costs and peak simultaneous buffers must still be charged. Replacing independent full packets by references is **not legal** unless the interface specifies it.

More decisively, the KT matrix is identical for opposite SAT/UNSAT charge assignments. Hence no D(Lk(F),E,C) can decide those original strict3 sources. A stronger topology/diagram, source input, or guest SAT calculation is needed, at its real cost. The present result is a representation-dependent compiler falsifier, not a SAT computational lower bound, no all-input solver, no native R_mix341 inference, and no noncircular B3 bridge.

## Independent computational checks and resource ledger

Two separately implemented host verifiers tested original strict proper ternary sources: Python 508 assertion groups, independently written Node.js 1,524, exact agreement of per-graph counts and SHA-256 source/matrix hashes. K4 (H=4,M=209,V=28,V^2=784,q=8), triangular prism (6,380,42,1764,16), cube (8,503,56,3136,32), pentagonal prism (10,626,70,4900,64). In total 120 original signed 3CNF sources, 60 SAT/60 UNSAT; Python brute-force edge assignments and connectedness, JS independently GF(2) row reduction; sixteen malformed/header/truncation controls per implementation rejected. All PASS. Python/Node are HOST implementations and hold explicit arrays, not native small-space FLMV benchmarks or diagram isotopy certificates. They check the link-matrix formula analytically, not a diagram. The downloadable conversation archive contains both full verifiers and raw result JSON.

Source parser/index/head/read costs and malformed fallback: only FINITE host checks, not a native bound. Internal output counter for a compressed matrix: O(log V) cell upper control with polynomial tape overhead. Dense per-child OUTPUT: qV^2 paid writes. Dense simultaneous WORK: V^2 paid cells. Cache/shared references: only if a declared representation is accepted, with lookup and retention paid. Additional diagram building, original source authentication, guest A simulation, failed policies, ancestor buffers, source conversion, correctness of stronger invariants and recursive compiler remain OPEN. Neither physical time nor proof weight is inferred from linking rank.

**Remaining:** [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-C3], [P2-B1], [P2-B2], [P1-01], [P1-03], [P1-04] all OPEN. Historical R_mix341 rules/weights, all five roles and identities, schedules, enabled states and 2 Route A / 3 Route B allocation preserved. P versus NP OPEN.
