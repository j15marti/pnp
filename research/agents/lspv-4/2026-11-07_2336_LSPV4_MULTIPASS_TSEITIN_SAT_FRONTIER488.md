# LSPV-4/488: Original-clause cubic-Tseitin multipass SAT frontier
**2026-11-07 23:36 PST | LSPV-4 Route A auditor | PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

**Nodes:** [P2-A4] material new restricted source-SAT streaming evidence; [P2-A2] all-input transformation OPEN; [P2-A5] recursive native FLMV realization OPEN; [P1-01], [P1-03], [P1-04] OPEN. Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] unchanged.

## IDEA -> SEARCH -> ITERATE
**Hypothesis:** Upgrade the prior restricted permutation AUTHENTICATION lower bound (LSPV-4/444, corrected /451) and engineered equality-gadget SAT bound (/486) to a full original signed-3CNF **SAT/UNSAT** multipass bound using already-known clause-minimality of cubic odd-charge Tseitin. This targets ONLY deterministic fixed-order sequential full-pass input, not indexed FLMV machines.

**Four precommitted falsifiers:** F1: an original clause of a connected bridgeless cubic odd-Tseitin is redundant; F2: distinct crossed half-clause sets remain UNSAT; F3: the argument silently assumes exactly one missing and duplicated clause, whereas crosses can alter many; F4: the lower bound is improperly promoted to native indexed-input FLMV. F1,F2 are ruled out symbolically and tested on original signed sources. F3 is prevented by explicitly requiring ALL multiset-corruption inputs (no one-swap promise). F4 is a genuine model boundary, preserved.

**Actually read:** complete root proof1.txt/proof2.txt, current issue #3 including 2026-11-07 LSPV-1/497, LSPV-2/486 and LSPV-3/492; 2026-11-02_1204 five-role handoff (blob c3889a3e514ddbd747150dcb68607013a3b2d154), AGENTS.md (19656af102604d5f0a721d548cf2e4e72a063561), CODEX.md (754999f50de93cdb693ed37bc8110d31e9e698ef), skill (b8df83a7b0b1428f349b0e02ce1387d979e8db7f); LSPV-4/444, /451, /452, /486, /487; LSPV-2/454, /480, /486; actual GROKPROOF/2026-11-08_0320_PROGRESS.md (72edb3140d8ed798d0905a827f85d3428728e396) and Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a). The original source-minimality is already in LSPV-3/429 and LSPV-5/427 and is NOT claimed newly discovered. A similar streaming complexity bound on artificial equality gadgets is already in LSPV-4/486.

**Literature:** Urquhart, *Hard Examples for Resolution*, JACM 34(1),209-219 (1987), DOI 10.1145/7531.8928; Ben-Sasson/Wigderson, *Short Proofs Are Narrow*, JACM 48(2),149-169 (2001), DOI 10.1145/375827.375835; Fortnow/Lipton/van Melkebeek/Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6),835-865 (2005), DOI 10.1145/1101821.1101822; standard deterministic equality/fooling set from Kushilevitz/Nisan, *Communication Complexity* (1997). Public indexed web used, no independently available Google-branded client.

**Actual external files and fixed blob SHAs:** konard/p-vs-np README.md (0e0ec77f83ad6eec1719a96066108b96ac1c2a95), scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5), INDEPENDENT_AUDIT.md (b30515cced93d8911a6415555ee9ec1444502d93); MassimoLauria/cnfgen cnfgen/families/tseitin.py (4bb5fd198fc4a698a5a207f67b36a9591b2a3bab); meelgroup/frat-xor format.md (986a21aa92b62f844ef1fce852193142c41b2b1f); openai/math lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (1ced21f44ad49370d1b812e862c03c3a91d7f836). None supplies a universal charged SAT compiler; external repositories are limited model/format controls, not authorities for P versus NP.

## Exact 3-CNF source and published hardness ledger
Fix a connected bridgeless simple cubic graph G=(V,E) with H even vertices, M=3H/2 edges, and odd-total vertex charges chi. For each vertex v, let incident edges be e1<e2<e3, and let ell_(e,0)=x_e, ell_(e,1)=not x_e. Include exactly the FOUR ORIGINAL proper width-three signed clauses

$$
C_{v,z}=\bigvee_{j=1}^{3}\ell_{e_j,z_j},\qquad z\in\{0,1\}^3,\quad z_1\oplus z_2\oplus z_3\ne\chi_v.
$$

Exactly m=4H distinct clauses, 12H literal occurrences, M=3H/2 variables. Odd total charge makes the full source UNSAT by XORing all H equations. In the tested fixed-width encoding, 8 magic bits, Elias-gamma(M), gamma(m), gamma(w), then 3m signed original fields of width (w+1), w=ceil(log2(M+1)); exact bit length

$$
N=8+g(M)+g(m)+g(w)+3m(w+1),\quad g(u)=2\lfloor\log_2u\rfloor+1=\Theta(H\log H).
$$

A duplicated original clause does NOT make a CNF encoding malformed; every crossed source remains a valid strict proper 3-CNF with redundant occurrences. Suitable growing bridgeless cubic expander sources have 2^{Omega(H)} lower bounds in ordinary shared-DAG RESOLUTION [Urquhart; Ben-Sasson/Wigderson], NOT in Extended Resolution, full historical R_mix341, GF(2) or arbitrary SAT machines. Graphs K4, K3,3, Q3, Petersen, Prism12 are finite semantic controls, not claimed certified asymptotically hard. Choose bridgeless cubic expander subfamilies explicitly: edge expansion ALONE does not logically rule out a fixed-size bridge gadget.

## Lemma 488.1: every original clause is essential (KNOWN; proof restated)
If G is connected bridgeless cubic, G-v is connected. Otherwise a component of G-v with one edge to v creates a bridge; any component needs at least two incident edges, inconsistent with degree 3 and two components. For any forbidden local pattern z at v, fix the three incident edge values to z. The remaining parity equations on the connected G-v have even total RHS: odd global charge and the wrong local z parity cancel. The GF(2) incidence map of connected G-v is onto its even-parity vectors; therefore extend the boundary assignment to satisfy all other vertex equations. This edge assignment falsifies exactly C_(v,z) of the original source. Thus F\{C_(v,z)} is SAT, and every proper clause submultiset of F is SAT. This familiar minimal-UNSAT property is credited to existing project work.

## Theorem 488.2: p-pass deterministic SAT lower bound (PROVED/RESTRICTED)
Let a deterministic program be correct for SAT/UNSAT on *every* m-record multiset of the above original clauses, with ONE FIXED-ORDER READ-ONLY SEQUENTIAL SOURCE TAPE, at most p complete left-to-right passes, and S bits of COMPLETE transferable state (including all work/index/head/cache/scratch and readable output). No source random jumps, randomized fingerprints, free advice, uncounted output as memory, or another input tape. Then with k=m/2:

$$
\boxed{(2p-1)S\ \ge\ \log_2\binom{m}{m/2}-O(1)\ \ge\ m-\log_2(m+1)-O(1).}
$$

**Proof.** For each k-set A of original clause IDs, write A in increasing order as the first half and complement(A) in increasing order as the second half. Diagonal A||complement(A) is the full original odd Tseitin and UNSAT. Any cross B||complement(A), B!=A, omits at least one original clause in A\B, hence is SAT by Lemma 488.1; repeated clauses add no constraints. Every input has identical encoded length and well-formed three-distinct-variable clauses. Therefore the SAT-label matrix is the negation of EQUALITY on binom(m,k) half-sets. Alice holds the first half, Bob the second. Each pass sends the full S-bit machine configuration across the midpoint; Bob returns it to Alice before the next pass. At most 2p-1 full-state messages, and at most one fixed terminal output bit. The diagonal pairs form a deterministic fooling set of size binom(m,k), so any correct protocol requires log2 binom(m,k) transcript bits. This yields the inequality and is precisely the standard equality communication argument applied to original source SAT labels. QED.

**Corollary 488.3:** On this strict sequential-full-pass model, if all-phase state S=O(N^{1/2+o(1)}), then

$$
p=\Omega(N^{1/2-o(1)}/\log N),\qquad
T=\Omega(N^{3/2-o(1)}/\log N)
$$

since at least the first p-1 complete passes must scan N input bits on a worst-case input. This contradicts local O(N^{11/10+o(1)}) time for this restricted scanner, but NOT the original indexed-input FLMV random-access model. Indexed access and algebraic semantic shortcuts remain legal and must be accounted for, never excluded to preserve a lower-bound claim.

## Independent original-clause controls and all-phase audit
Two independent local host-language implementations reconstructed actual signed strict-3CNF graphs K4, K3,3, Q3, Petersen and Prism12. Python exhaustively evaluated 299,584 edge assignments; found all 160 missing-clause satisfying witnesses; checked 7,500 crossed source half-set pairs and ALL 12,870 K4 half-subsets against one fixed complement; checked odd UNSAT and even model counts (8,16,32,64,128). **Python 50,570 counted assertions PASS.** Independently written Node.js: 160 essential signed clauses, 5,750 independent crossed pairs, **23,175 assertions PASS**. Zero failures. Tests do not prove the asymptotic theorem or certify expander hardness; those are separate mathematical/source claims.

| Phase | Charged restriction and remaining gap |
| --- | --- |
| Original/source reads | N=Theta(H log H) bits, every complete left-to-right scan >=N bit reads. |
| Source/INDEX/head | Complete state transfers include every persistent head, buffer, index and cache. The native indexed-input step is OUTSIDE this theorem. |
| Construction, search, failures, preprocessing, recomputation | All work contributes time; all simultaneously live bits contribute S even if subsequently freed. |
| Guests, children, conversions, joins, output | No SAT guest or child compiler produced. Output state accounted, output tape not reusable for free memory. |
| Mixed proof DAG nodes, certificate bits, critical path | N/A; no historical R_mix341 accepted proof or B3 claim. Ordinary Resolution hardness is a separate model. |
| Full native FLMV transfer | OPEN: same-machine all-input solver-dependent contraction, both labels, malformed awareness, recursive closure. |

**Exact reproducibility files:** experiments/arc/lspv4_488_multipass_minunsat.py, experiments/arc/lspv4_488_independent.cjs, results/raw/arc/2026-11-07_2336_LSPV4_488_MULTIPASS_TSEITIN_RAW.json, and ..._INDEPENDENT_JS_RAW.json. The source code is finite host-language semantic verification, NOT a native FLMV instruction trace. Root main.tex was not touched because its nonempty SHA did not yield complete readable contents. Five roles, schedules, enabled states, Route A/B assignment and R_mix341 original grammar/weights remain unchanged.

**Actual advance:** a restricted deterministic p-pass lower bound applying directly to SAT labels on original minimally-UNSAT signed width-three clauses, including the established ordinary-Resolution-hard cubic-expander subfamilies (with bridgelessness). **Verification:** symbolic fooling-set reduction and 73,745 independent counted finite assertions. **Remaining gap:** any universal, all-input recursively iterable fully charged SAME indexed-FLMV machine SAT contraction; Route B mixed all-rule lower bound and noncircular B3 remain OPEN. **P versus NP OPEN.**
