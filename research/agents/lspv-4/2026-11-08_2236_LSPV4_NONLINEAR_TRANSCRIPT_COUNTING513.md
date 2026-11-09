# LSPV-4/513 | Nonlinear virtual-child trace-compatibility counting firewall

**2026-11-08 22:36 PST | Route A PRIMARY | PROVED/RESTRICTED + COMPUTATIONAL; P versus NP OPEN.**

**Exact proof-chain nodes:** proposed [P2-L4-513] refines [P2-A4], [P2-L4-512], peer LSPV-2/513; [P2-A2] universal contraction and [P2-A5] recursively iterable same-machine applicability remain OPEN. Companion [P1-01], [P1-03], [P1-04] and Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. No changes to historical R_mix341 grammar/weights or the existing five-agent 2A/3B allocation.

## IDEA, falsifiers before search

Hypothesis: extending the affine exact-read kernel of LSPV-2/513 and the output-aware repair of LSPV-4/512 to **arbitrary polynomial-time evaluable nonlinear virtual-child transducers** loses the affine-coset counting guarantee. For unrestricted descriptor width, merely counting replay-compatible descendants can encode #3SAT.

Four falsifiers: (F1) all same-transcript descriptor sets remain affine despite nonlinear child bits; (F2) the construction silently changes the original K4 strict proper 3-CNF or admits a satisfying child; (F3) the putatively invisible tag sign bits are in fact read by the designated source validator, or distinct descriptors encode the same child; (F4) the derived compatible-descriptor count differs from 2^n+#SAT(phi). A resource falsifier is any assertion that #P-hardness at unbounded k rules out brute-force enumeration when k=O(log N).

## SEARCH and scope of external sources

Read both complete live trackers on main before work: proof1.txt initial Git blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; proof2.txt initial blob b68565137846a1737299ddbce69ae2a178da0e84 (641,663 characters). Reviewed coordination issue #3, governing five-role handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (c3889a3e514ddbd747150dcb68607013a3b2d154), AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, peer research/agents/lspv-2/2026-11-08_2112_LSPV2_AFFINE_VIRTUAL_READ_KERNEL513.md (8b4c94ec1836e6c0cb159959e8614f9d85af1f5b), and research/agents/lspv-4/2026-11-08_2203_LSPV4_OUTPUT_OBSERVABLE_TRACE_FIREWALL512.md (f9773f5bd34255dfc249221533c59fd00a5c26c4). Checked historical /507, /508, /510R and /505 controls rather than treating their parity/padding results as new.

Actual peer files reviewed: GROKPROOF/2026-11-08_1130_PROGRESS.md (6942a99f176e996e9542f0386b7aa7fe2ce89e70); research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727d3e2b009cba7afec2a93beb62959dd67). External repository/path/blob change-aware controls: konard/p-vs-np README.md 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json 93b77ed3d8fe456f81c690035f45f07910a247f2 (finite-model formalization); blkph0x/p-vs-np-proof-research METHOD_INDEX.md 18d693ea71dfa433370eb7afbebc3106e32f03e5 and INDEPENDENT_AUDIT.md b30515cced93d8911a6415555ee9ec1444502d93 (scoped methods); MassimoLauria/cnfgen/cnfgen/families/tseitin.py 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (Tseitin original clauses); meelgroup/frat-xor/format.md 986a21aa92b62f844ef1fce852193142c41b2b1f (different, extended proof grammar); openai/math/CONTENTS.md 7e1ed90ac5a666f1bbecb22027387c4ad79e9d03 (no relevant same-machine contractor). Public web and GitHub searches were used; separate Google-branded service unavailable. No formal prover or official R_mix341 checker replay.

Primary: Fortnow, Lipton, van Melkebeek, Viglas, JACM 52(6) (2005), https://lance.fortnow.com/papers/files/tst.pdf §2.1 PDF page index 3, visually inspected (indexed INPUT/WORK, index erasure, one-way OUTPUT). Urquhart, JACM 34(1) (1987) and Ben-Sasson/Wigderson, JACM 48(2) (2001), strictly ordinary shared-DAG Resolution hardness of suitable *growing expander* odd-charge Tseitin families. Counting #3SAT is #P-complete (Valiant 1979 and standard subsequent parsimonious #3SAT reductions); the present reduction is **polynomial-time Turing**, not parsimonious.

## ITERATE: non-affine read-cylinder counting theorem (PROVED/RESTRICTED)

Let phi be an arbitrary 3-CNF on n named Boolean variables z_1,...,z_n with m>=1 clauses C_j. The descriptor is d=(b,z) in {0,1}^{n+1}. Fix a contradictory odd-charge cubic K4 Tseitin original *strict proper 3-CNF* core (six edge variables, sixteen original clauses). Append m independent, fresh-variable proper 3-clauses D_j and n+1 independent, fresh-variable proper 3-clauses E_i. All fresh triples are disjoint from the K4 core and each other. Their second and third literals remain positive. The sign of the first literal of D_j is the efficiently computable nonlinear bit

$$
w_j(b,z)=b\land\neg C_j(z).
$$

The sign of the first literal of E_i is the descriptor bit d_i. Thus **every descriptor yields a distinct original signed proper width-three 3-CNF source** because E_i distinguish d, and every source is UNSAT because of the unchanged odd K4 core.

The canonical source uses an 8-bit magic, prefix-free gamma fields for m, n+1, total number of variables and clauses, and fixed-width binary literal IDs plus one sign bit per occurrence, followed by a two-bit terminator. Source length M=O((m+n)log(m+n)). The decoder can cap all header counts by the *physically scanned* source length, rejecting oversized or truncated sources without constructing astronomically large counters. This capped native parser is not implemented in the finite verifier.

Define a fixed total deterministic guest A: verify the original odd K4 core and the canonical fresh-variable padding/tag layout, with indexed reads that **skip E_i first-literal sign positions**, all of whose possible polarities are legal; explicitly read every D_j first-literal sign bit and copy it briefly to a low private WORK bit before clearing it; output UNSAT on recognized sources; on other sources run an independent total correct general SAT/malformed decider B (brute force suffices to establish unconditional total correctness, and a polynomial B is available only conditionally if SAT in P). The guest does not depend on phi and can be uniform for all m,n. Its restricted recognized-source run is polynomial time with O(log M) auxiliary counters plus one transient WORK bit under a properly charged indexed parser, but no native implementation or all-input fallback contraction is asserted.

Let d_0=(0,0^n) and let C_phi be the set of descriptors whose **genuine step-aligned observed guest input values and transient WORK configurations** agree with the anchor's entire recognized-source run. All header, identifier, original-core, other signs and outputs are fixed. The E_i tag sign bits are not observed. Consequently

$$
d\in C_\phi\iff\forall j:\;w_j(b,z)=0
\iff b=0\;\lor\;\phi(z)=1.
$$

Therefore

$$
\boxed{|C_\phi|=2^n+\#\mathrm{SAT}(\phi).}
$$

The function computing |C_phi| from the compact transducer description is in #P (guess d; verify all m clauses and transcript agreement in polynomial time), and #P-hard under a polynomial-time **one-query Turing reduction**: subtract the known 2^n to recover #3SAT(phi). It is #P-complete under polynomial-time Turing reductions, **not** claimed parsimoniously complete. Example: phi(z)=z gives exactly three compatible descriptors, not a power of two; hence this set is not an affine coset and no formula 2^(k-rank) applies.

This is a **counting complexity barrier for enlarging the restricted affine transducer language**. It proves NO runtime or workspace lower bound for arbitrary SAT solvers: the guest family is uniformly recognizable and trivially UNSAT, and a code-aware compiler may ignore its deliberately read sign bits. For the FLMV proposal q=N^(3/5+o(1)) and k=O(log N), brute-force enumeration of all q descriptors is polynomial, so this #P statement does not block the stated exponent contraction by itself. Universality, same-machine cost, all-input correctness, malformed handling and recursive closure remain separate.

### Established hard-family transfer control

For any suitable expanding cubic graph with H vertices, replace K4 by its established odd-charge strict3 Tseitin core F_H with 4H clauses, 3H/2 variables and an authenticated O(H log H) binary encoding. With independently satisfiable fresh-variable padding/tag clauses P_d, ordinary shared-DAG Resolution minimum is exactly preserved:

$$
S_{\mathrm{Res}}(F_H\land P_d)=S_{\mathrm{Res}}(F_H).
$$

Upper bound: ignore P_d. Lower bound: restrict every fresh variable so all P_d are true, and restrict each Resolution inference without increasing its distinct-node count. This is a known restriction transfer (already used in LSPV-4/510R), not a mixed R_mix341 or general-machine hardness transfer. The counting construction merely uses this established family as an honest source/control, not as evidence against all algorithms.

## Independent finite verification and accounting

Independent Python generator and Node.js verifier passed. Python: 30 formulas, 652 **distinct** encoded virtual children, 25 non-affine compatible-set sizes, 180 malformed/structural mutation rejections, 377,804 explicitly materialized encoded child bits, 374,516 observed bit comparisons, maximum 649 bits per child. Five named cases were independently reproduced in Node: phi=z => K=3; phi=(z)&(not z) => K=2; phi=(z_1 or z_2) => K=7; phi=z_1 & z_2 => K=5; a four-clause UNSAT two-variable control => K=4. Original K4 core had zero satisfying assignments; deliberately flipping the first core sign produced two. Python and Node each generated their own signed original source representation; named cases matched exact source lengths 315,394,392,412,450 bits and compatible counts. These are hosted symbolic transcript checks, not native FLMV or official R_mix341 replay.

Separate charges: symbolic logical clauses 16+m+n+1 per source, explicit source bits M, per-child source construction O(M), per-child source read comparisons <=M, total hosted enumeration O(2^(n+1) M), recognition+index queries must charge O(M polylog M) operations and O(log M) scratch in a native realization, while storing all q children takes qM WORK bits or source recomputation; guest B fallback can take exponential time/space, cache retention, misses, conversions, failed attempts, simultaneous buffers and full peak are NOT bounded by these finite runs. A completed source/read transcript is a restricted cache certificate, not a lower bound for the minimal semantics-preserving computation.

The mathematical falsifiers F1 and F4 were met by explicit non-affine 3/7/5 counts; F2 and F3 were rejected by signed source / tag/corrupt controls. No result closes full [P2-A4] or [P2-A2]/[P2-A5].

**Result:** A genuinely nonlinear virtual-child replay-counting restriction embeds #3SAT, and the affine 2^(k-r) formula cannot be generalized without additional structural assumptions. **P versus NP OPEN.**
