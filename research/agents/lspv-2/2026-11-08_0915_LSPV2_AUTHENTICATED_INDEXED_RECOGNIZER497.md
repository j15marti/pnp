# LSPV-2/497 | Complete specialized source authentication and padded-fallback falsifier

**2026-11-08 09:15 PST | Route A | PROVED/RESTRICTED under stated uniformity premise U; COMPUTATIONAL finite | P versus NP OPEN.**

**Exact nodes:** [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04]; Route B peer references [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Entire root proof1.txt was read at blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2.txt at blob 6aa2a009f92d275db416fe86ac670acae32a3f31, then rechecked after peer edits at blob 8f16ca0b2fda81b05ff4ca3d82c68dcb1e801183. No tracker edit by LSPV-2. Five 2A/3B agents, historical native R_mix341 rules/weights, IDs, schedules, enabled states, and ownership unchanged.

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis:** Existing LSPV-2/495 original signed connected cubic Tseitin split-source syntax admits a *complete fixed-grammar* three-label parser using indexed reads and no stored a/b bit strings. The previous LSPV-4/497 indexed detector was explicitly promise-only and accepted a corrupted trailer; fill that exact gap without pretending a specialized grammar is general SAT. Then challenge a fastpath plus unmodified general-decider fallback using arbitrarily padded correct guests.

**Four falsifiers announced before source review:** F1 source fails exact strict3 syntax or SAT iff a!=b; F2 a malformed header/trailer/packet is accepted by the proposed complete membership checker; F3 the claimed logspace algorithm needs an uncharged graph table, advice or state holding H bits; F4 an unchanged fallback guest A with deliberate polynomial delay still satisfies the contraction bounds.

**Actual source review:** Both complete trackers; coordination issue #3 and latest peer comments; governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md; AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md; original LSPV-2/495, /496, LSPV-4/497 and its failed-trailer control; actual GROKPROOF/2026-11-08_1130_PROGRESS.md blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70; actual Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67. No other peer manuscript region was written.

**Required external pinned GitHub original files:** konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 (finite-machine P subset NP); blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 (scoped results only); MassimoLauria/cnfgen cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (Tseitin parity generator); berkeley-abc/abc README.md blob 88a9d1a316dd9751acade746de315fd1e6e6c362 (circuit DAG upper-control tools); meelgroup/frat-xor format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f (distinct certificate format); openai/math CONTENTS.md blob 7e1ed90ac5a666f1bbecb22027387c4ad79e9d03 (research index, not PNP authority). Public web literature searches used; separate Google-branded client unavailable. No PDF full text or claimed independent formal proof replay.

**Primary sources (exact scope):** Marcus/Spielman/Srivastava, Interlacing Families I, Annals of Mathematics 182 (2015), doi:10.4007/annals.2015.182.1.7, gives infinite cubic bipartite Ramanujan existence but does NOT automatically give a logspace-uniform graph/matching enumerator. Urquhart, Hard Examples for Resolution, JACM 1987, doi:10.1145/7531.8928; Ben-Sasson/Wigderson, Short Proofs Are Narrow, JACM 2001, doi:10.1145/375827.375835, apply to stated ordinary DAG Resolution model. Fortnow/Lipton/van Melkebeek/Viglas, Time-Space Lower Bounds for Satisfiability, JACM 2005, doi:10.1145/1101821.1101822, applies to their deterministic indexed random-access machine, not the narrower multi-pass streaming lower bound of /495.

## Original 3-CNF family, encoding and exact control

Use the exact established LSPV-2/495 original signed strict proper 3-CNF source. Let G be connected simple cubic bipartite with H even vertices, perfect matching edges j=0..m-1, m=H/2, and fixed odd charge vector chi. At matching edge j, left local ID is 2j+1+a_j and right local ID is 2j+1+b_j; nonmatching edges use distinct IDs H+1..2H. At each vertex sort the three IDs and emit the four original signed width-three parity clauses for sign triples z with XOR(z)!=chi(v), in lexicographic order. Emit all left vertex packets followed by right packets. Fixed specialized binary grammar: eight magic bits 11100011; unary H (1^H 0); unary 2H (1^(2H) 0); 12H fields consisting of sign bit and W=ceil(log2(2H+1)) unsigned ID bits; trailer 10.

$$
N=8+(H+1)+(2H+1)+12H(W+1)+2=3H+12+12H(W+1)=Theta(H log H).
$$

Every accepted source has exactly 4H pairwise distinct original proper 3-CNF clauses with no auxiliary variables. The prior incidence-rank proof gives SAT(F) iff a!=b, with zero models for a=b and 2^(H/2+d(a,b)) models otherwise. On the diagonal, variable-renamed odd-charge expander Tseitin has exponential **ordinary DAG Resolution** size for established expanding families. No lower-bound preservation is asserted for historical full R_mix341, Extended Resolution, GF(2), or arbitrary SAT algorithms.

## Theorem 497.1: exact fixed-grammar all-bit authentication, conditional uniformity

**Hypothesis U:** ONE total uniform deterministic algorithm decides whether H belongs to the supported graph family (returning OUTSIDE if not) and, for supported H, computes the public graph's vertex packet order, matching index, the two fixed nonmatching IDs, both matching endpoints and local odd-charge bit from (H,v) or (H,j) with time T_G(H) and space S_G(H). No growing advice table or source-independent semantic oracle. MSS existence alone does not discharge U for a selected expander sequence.

**Claim:** There exists a fixed three-label indexed-input classifier correct for EVERY binary string relative to this specialized grammar, outputting MEMBER_SAT, MEMBER_UNSAT or OUTSIDE. With all source/index/head arithmetic and state charged:

$$
S_member(N)=O(S_G(H)+log(N+1)),\quad
T_member(N)=O(N polylog N + H T_G(H) polylog N).
$$

If U has polylog H time and O(log H) space this is N^(1+o(1)) time and N^o(1) space. Polynomial T_G yields only polynomial total time. OUTSIDE can be a well-formed arbitrary CNF, so it must NOT be mislabeled malformed as a general SAT input.

**Proof:** First test exact magic, unary length/bound, byte-exact total field count and trailer. At each vertex of the prescribed public packet order, compute its matching j, local charge, and two fixed nonmatching IDs using U. Read the first unsigned ID (always the smallest sorted local ID). Reject unless it is exactly 2j+1 or 2j+2. That bit determines all three local IDs and all four signed ternary parity clauses. Construct their twelve fields one at a time and compare ALL twelve source fields, rejecting on mismatch. Thus every valid specialized source is recognized, and every accepted byte string is an allowed family member. In a second indexed pass, use U to find both endpoints of each matching j and reread only the first ID field of the two authenticated packets. They all agree exactly when a=b, deciding SAT/UNSAT by the previously proved original-source rank identity. Only counters, two IDs, addresses, source/index heads and U's workspace coexist: O(S_G+log N) bits. The first full source scan and all indexed rereads, graph recomputation, output, and reference costs are included.

**Important boundary:** Python and JS use ordinary strings, graph objects and source arrays. Their actual heap peak is not the symbolic logspace bound and they are not native FLMV machine executables.

## Theorem 497.2: naive unchanged-guest fallback cannot universally contract

Define Psi(A) to run the above checker and answer authenticated members immediately, but on every OUTSIDE source run unchanged general-CNF decider A(x). This preserves SAT/UNSAT/malformed semantics only if A already does; it is not automatically an improvement. **Assume SAT in P** and fix some uniform total correct A0 with time O(N^d). For any integer K>max(2,d), let A_K spend Theta((N+1)^K) native transitions in an O(log N)-counter delay loop, then execute A0 and return its exact result. A_K remains correct and polynomial time, with worst-case exponent K. Arbitrarily large ordinary valid general-CNF sources are outside the specialized grammar; Psi(A_K) calls the unchanged A_K there, hence has worst-case time Omega(N^K). But

$$
K > max(11/10,\ 3/5+K/2) \quad (K>2).
$$

So this fully charged fastpath+unchanged-fallback wrapper fails the required Route A contraction for correct padded guests. This is a strictly scoped, conditional counterexample to a *particular architecture*, not an impossibility for code-aware optimization, native all-input solver-dependent contraction, or P!=NP.

## Executed finite controls and independent replay

Original signed graphs: K3,3 H=6 N=390, cube Q3 H=8 N=612, Heawood H=14 N=1062. Python independently tested 512 genuine sources: 360 SAT, 152 UNSAT, 72 independent GF(2) rank SAT controls and 33 corrupted/malformed specialized sources, 1,641 assertion groups. Independently authored Node implementation checked all 512 labels and 33 mutations, 1,647 assertions; SHA256 of original first-source bytes matched /495 on every graph. Additional standalone compact V8 verifier, published here as experiments/arc/lspv2_497_authenticated_indexed_v8.js, was executed both before and after fetching its exact GitHub blob e5bf0d3379b915052bb43eca295c24bca0ffa1e7: 512 cases, 360 SAT, 152 UNSAT, 33 corrupted negative cases, **1,569 independent V8 assertions passed**.

**Real development falsifier:** A Q3 matching edge is left-oriented but numerically descending. Initial Python generator incorrectly assumed all matching pairs were already ascending unordered edge keys, failed the graph test; repaired by canonicalizing only undirected edge keys and retaining left/right ownership. The complete three-way test was rerun. No silent exemption.

Original Python/Node scripts, raw results and checksums accompany this run's reproducibility archive. GitHub V8 source is smaller but separately replayed. The recovered historical R_mix341 checker and native FLMV indexed machine were NOT executed; no accepted R_mix341 branching certificate, no all-input reduction, no guest source conversion, no child construction, no recursive composition or proof optimum was claimed.

## Family/theorem/shortcut/transfer ledger

| Family | Exact encoding, theorem/model | Strong known shortcut | Remaining transfer |
| --- | --- | --- | --- |
| Signed odd-charge cubic-expander Tseitin | 4H original proper 3-CNF clauses; N=Theta(H log H). Exponential ordinary shared-DAG Resolution size on expander source. | Original XOR/GF(2), Extended Resolution, shared DAG and indexed decisions remain legal upper controls. | No R_mix341 all-rule lower bound [P2-B1], source-to-mixed simulation [P2-C3] or B3 [P2-B2]. |
| LSPV-2/495 split matching edge source | All 4H original signed clauses distinct, SAT iff a!=b, diagonal ordinary Resolution hard. Specified deterministic full-pass sequential streaming TS=Omega(N²/log N), not FLMV. | /496 randomized prime fingerprint; LSPV-4/497 indexed promise-only; current fixed-grammar indexed authenticated classifier. | U generator uniformity not established from MSS existence; no arbitrary-CNF handling or universal solver contraction [P2-A2]. |
| Haken PHP | Established ordinary Resolution lower bound on native PHP CNF (Haken 1985), not automatically a strict3 simulation. | Cook ER definitions and algebraic shortcuts must be admitted if legal. | Exact 3-CNF lower-bound-preserving direction, full R_mix341 all-rule transfer and B3 all OPEN. |

**All-phase accounting:** symbolic source validity tests, full 12H field scan, indexed matching rereads, graph/matching generator U and re-computation, heads, index/high-water, counters and output are counted in theorem. Host finite allocations are explicit limitations. General fallback can cost guest N^K and violates target. None of rho, eta, lambda and guest-simulation overhead needed by an actual recursive contraction is supplied by this special-case algorithm. Exact [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN; Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN. **P versus NP remains OPEN.**
