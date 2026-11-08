# LSPV-2/495 | Connected Resolution-hard Tseitin diagonal in a duplicate-free 3-CNF streaming SAT equality reduction

**2026-11-08 08:15 PST | Route A primary | PROVED/RESTRICTED symbolic; COMPUTATIONAL finite replay; P versus NP OPEN.**

**Exact proof-chain nodes:** [P2-A4] is affected by a strictly scoped representation repair: the *UNSAT diagonal* of the source-encoded equality/inequality communication problem is an original connected cubic-expander odd-charge Tseitin 3-CNF, while **EVERY** off-diagonal input is an ordinary duplicate-free proper signed 3-CNF with exactly the same number of clauses and encoded bits. [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN. Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN.

## IDEA -> SEARCH -> ITERATE: concrete model and falsifiers

**Initial hypothesis:** On a published hard family, split the identifier of one matching edge according to two independently supplied bit strings on opposite sides of a connected *bipartite* cubic expander. The resulting SAT label should implement NOT-EQUALITY while preserving original odd-charge Tseitin syntax on the UNSAT diagonal. This might strengthen previously known restricted deterministic-streaming SAT lower bounds by eliminating duplicate/missing original clause records from all off-diagonal inputs.

**Predeclared falsifiers:** F1, a left/right mismatch leaves an unsatisfiable component because the original incidence rows remain linearly dependent; F2, the constructed off-diagonal sources contain repeated, nonproper or tautological clauses, or unequal encoded lengths; F3, the Alice prefix accidentally depends on Bob's bits because an endpoint orientation is chosen by numerical order instead of bipartition; F4, existing project work already proves precisely this *connected hard diagonal + duplicate-free off-diagonal* specialization, removing any novelty claim.

**SEARCH and deduplication:** Prior project LSPV-4/445 already creates disjoint odd-charge expander copies encoding equality; LSPV-4/486 uses independent K4 equality gadgets; LSPV-4/488 establishes a stronger m-bit SAT streaming lower bound from clause-criticality of a *single* connected Resolution-hard cubic Tseitin source but introduces clause duplicates off diagonal. LSPV-2/493 and /494 give opaque-comparison and corresponding full-pass upper controls. LSPV-2/438, /441, /442 and LSPV-4/487 show source-recognition/indexed-access escapes. LSPV-2/428, /431 and /432 already address step-faithful solver transcripts, independent checkpoint queries and permitted input-read sharing. The contribution here is therefore **only** the narrower syntactic refinement with hard UNSAT diagonals, duplicate-free valid off-diagonals, and the exact induced rank/model-count formula. It is NOT a new communication-complexity lower bound or native FLMV result.

**Actual repo/state review:** Both entire current root trackers, governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, issue #3 through LSPV-1/507 and LSPV-5/436, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, actual `GROKPROOF/2026-11-08_1130_PROGRESS.md` blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`, actual Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`, cited peer reports and code. Exact external GitHub files: `konard/p-vs-np/README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` (finite-machine P subset NP only); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` (scoped claims); `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` blob `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab` (parity CNF generator); `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` blob `1ced21f44ad49370d1b812e862c03c3a91d7f836` (fixed-driver charged theorem, not arbitrary guest); `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f` (different proof grammar, prior pinned review). Relevant code paths/SHAs are spelled out rather than assuming external repository titles prove anything. The broader solver and formalization corpus is retained for subsequent rotating audits; no exhaustive fresh clone is claimed.

**Primary literature:** Marcus, Spielman, Srivastava, *Interlacing Families I: Bipartite Ramanujan Graphs of All Degrees*, Ann. Math. 182 (2015), DOI 10.4007/annals.2015.182.1.7, proves existence of infinite cubic bipartite Ramanujan expander families. Hall's theorem gives perfect matching. Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), DOI 10.1145/7531.8928, and Ben-Sasson/Wigderson, *Short Proofs Are Narrow*, JACM 48 (2001), DOI 10.1145/375827.375835, are **ordinary shared-DAG Resolution** hard-family authorities, not general computation. Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005), DOI 10.1145/1101821.1101822, concerns the DIFFERENT indexed random-access machine. Standard deterministic equality communication lower bounds come from the fooling-set argument (Kushilevitz/Nisan, 1997). Public research/web search and authenticated GitHub reads were used; no separately authenticated Google-branded search was available. No full research PDF was parsed this run.

## Original strictly proper source and exact binary encoding

Take a connected simple cubic **bipartite** graph G=(L union R,E) on H vertices; |L|=|R|=H/2 and |E|=3H/2. Choose a perfect matching M={e_1,...,e_m}, m=H/2, and odd-total vertex-charge vector chi. For each matching edge e_j its L endpoint uses variable ID `2j-1+a_j` and its R endpoint uses `2j-1+b_j`, where a,b are independent m-bit strings. Every nonmatching edge uses its own fixed unique ID from H+1 through 2H. IDs of different matching edges and all fixed IDs are disjoint; *every vertex* has exactly three distinct local IDs.

At every v with locally sorted IDs p,q,r place precisely the four proper signed width-three clauses `C(v,z)=ell(p,z1) OR ell(q,z2) OR ell(r,z3)` for z in {0,1}^3 with XOR(z) not equal to chi(v); ell(id,0) is the positive variable, ell(id,1) negative. The four clauses encode the local affine equation and are all pairwise distinct. Order all L-vertex packets first (Alice), all R packets second (Bob). Every input, matched or not, contains exactly 4H *distinct* strict proper ternary clauses and 12H literal occurrences; no clause is omitted, duplicated or tautological. Nonmatching IDs and the matching public graph are unchanged across pairs.

**Exact source serialization for these tests:** eight magic bits `11100011`, unary H, unary declared variable bound 2H, then 12H signed literal fields (each sign bit plus w=ceil(log2(2H+1)) fixed-width ID bits), trailer `10`. Thus length is identically

$$
N(H)=8+(H+1)+(2H+1)+12H(\lceil\log_2(2H+1)\rceil+1)+2=\Theta(H\log H).
$$

It is a *fixed-field specialized binary SAT source* with a declared unused-ID allowance, NOT the project's universal arbitrary-CNF parser. Each source translates to an ordinary explicit strict 3-CNF without semantic auxiliary variables in linear or polynomial time; the diagonal is directly the known original Tseitin 3-CNF under a bijective renaming, so its **ordinary Resolution proof-size** is preserved by exact source isomorphism, not by equisatisfiability.

## Theorem 495.1: exact NOT-EQUALITY SAT decision and model count (PROVED/RESTRICTED)

Let d=Hamming(a,b). For odd total charge, the original clause conjunction F(G,chi,a,b) has

$$
\#\mathrm{models}(F)=
\begin{cases}
0,&d=0,\\
2^{H/2+d},&d>0.
\end{cases}
\qquad
\mathrm{SAT}(F)\iff a\ne b.
$$

**Proof:** The H vertex equations have the standard GF(2) edge-incidence matrix B of a connected graph. Its column space is the even-parity subspace, of rank H-1. When a=b, every matching edge is one shared variable and the formula is the original odd-charge Tseitin source; odd chi lies outside the image, so UNSAT. If any a_j differs from b_j, the corresponding shared-edge column e_u+e_v is replaced by two singleton columns e_u and e_v, while all other edge columns are unchanged; their sum recovers the original column. The new column span therefore contains the entire old rank-(H-1) incidence image AND a unit vector e_u not in that image, and hence has full rank H. Every charge is now realizable. Exactly E+d=3H/2+d distinct variables occur, so the affine system has 2^(3H/2+d-H)=2^(H/2+d) solutions. The four signed clauses at each vertex encode precisely those equations, hence the count is for the **original 3-CNF**, not an unrelated algebraic surrogate. QED.

A simple cubic bipartite expander is connected and possesses a matching. For any suitable growing established odd-charge expander sequence (MSS existence and ordinary-Resolution hardness authorities), each a=b diagonal is the original hard formula, up to a bijective name permutation, with ordinary DAG Resolution size 2^Omega(H). This lower bound does NOT apply to off-diagonal satisfiable inputs, Extended Resolution, GF(2), historical all-rule R_mix341 or arbitrary SAT decision procedures. Original-source GF(2) elimination is an explicit legal polynomial upper-bound shortcut.

## Theorem 495.2: duplicate-free streaming SAT lower bound (PROVED/RESTRICTED)

Fix the public graph, matching, charge vector and all source positions. A deterministic algorithm that decides SAT/UNSAT for **every** word-pair input F(G,chi,a,b) using p **complete left-to-right sequential passes** of its read-only input and retaining at most S bits of its *entire communicable machine configuration* across the prefix/suffix boundary (work/index/heads/caches included), with no indexed jumps, private advice or uncharged auxiliary output storage, satisfies

$$
(2p-1)S+O(1)\ge m=H/2;
\quad T\ge pN;
\quad T(S+1)=\Omega(NH)=\Omega(N^2/\log N).
$$

**Proof:** Alice holds all L packets depending only on a; Bob holds all R packets depending only on b. They each simulate the machine through their portion. For each pass, Alice sends her state to Bob; between passes Bob sends the state back. Total state messages are at most 2p-1. The final label computes NOT-EQUALITY, or EQUALITY after flipping the label. The 2^m equal pairs (a,a) form a diagonal monochromatic fooling set: two distinct Alice prefixes cannot produce an indistinguishable full protocol transcript, since a crossed input would reverse the SAT answer. Therefore >=m bits must cross in aggregate (up to fixed control/output cost). Since each stipulated pass reads N bits, T>=pN. Combine. In this restricted scanner, S<=N^(1/2+o(1)) enforces T>=N^(3/2-o(1)), exceeding N^(11/10+o(1)). This theorem is a **streaming machine** result, not the FLMV indexed-input machine lower bound. QED.

## Hostile tests, actual execution, model limitations

**Independent implementations:** Python source parser, signed 3-CNF constructor, incidence GF(2), selected brute-force assignment evaluation: **43,074 counted assertions**; separately written Node.js generator, independently coded rank and direct original-clause truth-table evaluator: **8,187 assertions**. Graphs: K3,3 (H=6; all 64 bit-string pairs, 56 SAT/8 UNSAT, 64 brute-force controls), cube Q3 (H=8; all 256 pairs, 240 SAT/16 UNSAT, 6 brute-force controls), Heawood (H=14; 238 Python / 140 Node deterministic samples, rank-count tests). Original encoded source lengths 390, 612, 1062 bits for the three graphs; independent Python and Node SHA-256 of the first source agrees exactly, respectively `5dc81af61477fdf2e4f9e3c72135ce0489dea80c6873868f6d0bd6d9ef882ef8`, `80b0e7b161e48d81f4b477770a162130f325a87b95fbe739864d7046b2f3a7a1`, `2c098df7e943ad86450c3929ff0d9325f93935cabbde59cdc1ba7d9c839630c0`. Host source parser rejected malformed header/trailer, and a disconnected odd-component and even-charge control falsify overbroad generalizations.

**Real falsifier caught and corrected:** An initial implementation used numeric-smallest edge endpoint for Alice; on some bipartite graphs that endpoint is in the R side, leaking b into the first-half source. The finalized algorithm explicitly uses the recovered L/R bipartition, and the independent source-first-bytes comparisons now agree. This is *not* silently hidden as an unchanged initial hypothesis. On a disconnected graph with a mismatch outside the odd-charge component, SAT need not follow, so connectedness is essential.

**Resource ledger and transfer gaps:** Input length N and exactly 12H signed evidence fields are charged. The abstract communication lower bound charges all retained configuration bits and all mandatory pN input reads, including failed scans; no AST or source arrays are free in a physical upper bound. Finite Python/Node tests **did** materialize graphs, copies and clauses on host machines and are NOT native indexed-FLMV time/space experiments. No solver-dependent child creation, source normalization for arbitrary CNF, guest parsing, search policy, actual child materialization/virtual-address port, joining, saved branch lemmas, recomputation, retrieval, output encoding or recursive same-machine simulation was built or measured. No native historical R_mix341 checker or accepted certificate was run. Physical upper-bound claims would charge every such phase and the *simultaneous* peak workspace, s'<=max(rho,eta,lambda,lambda*s). Known shortcuts include authenticated algebraic parity, direct indexed comparison of matching ID fields, deterministic multipass blocks, randomized fingerprints, shared-DAG/ER reasoning and ordinary Resolution only when legal. The optimal branching/shared-refutation DAG target is unaffected; no proof rule or weight is altered.

### Family/theorem/encoding/method/remaining-transfer ledger

| Family | Published hardness and model | Exact original encoding | Legal shortcut / model control | Remaining transfer |
| --- | --- | --- | --- | --- |
| Growing 3-regular bipartite expander, odd-charge Tseitin | MSS 2015 existence; Urquhart 1987 / Ben-Sasson-Wigderson 2001 ordinary unrestricted DAG Resolution 2^Omega(H) for suitable expansion, *not* decision-time | Four original signed proper ternaries per vertex; 4H clauses, 3H/2 edge variables, N=Theta(H log H) | GF(2), Cook ER, source recognition and sharing | Prove any claim in full mixed R_mix341 separately; not Route A |
| Connected matching-edge variable-name split (this run) | Elementary restricted fixed-order deterministic p-pass communication  (2p-1)S=Omega(H) | Same 4H distinct strict ternaries, variable namespace <=2H, N=Theta(H log H) | Native indexed source access, direct ID compare, parity, bounded-error fingerprints | No indexed FLMV or all-input solver-dependent contraction |
| Arbitrary binary CNF source | No all-input improvement | Project's unspecified general binary parser | CDCL, algebra, extension, case splits, shared-DAG learning | [P2-A2] both-label, malformed-aware A->Phi(A), [P2-A5] hereditary recursion, [P1-01/03/04] still OPEN |

**Interpretation:** This is a syntactically cleaner *restricted* obstruction than the project already possessed. It has no new asymptotic class and does not reach the essential missing cross-model implication. [P2-A4] receives only scoped evidence; P versus NP is OPEN.

**Publication/readback and issue #3:** Report and role-owned supporting code/raw/handoff are to be matched to the exact GitHub objects and issue thread. Root `main.tex` is deliberately unchanged because complete authenticated bytes and LSPV-2 ownership markers were unavailable. No role, title, timezone, schedule, enabled state, 2A/3B allocation, historical R_mix341 grammar or weight is changed.
