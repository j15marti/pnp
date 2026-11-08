# LSPV-4/498 | Exact Hamming-distance authentication floor for the established signed cubic-Tseitin source
**November 8, 2026 09:36 PST | Route A resource auditor | PROVED/RESTRICTED + COMPUTATIONAL; P versus NP OPEN.**

**Exact nodes:** candidate new [P2-L4-498] refines [P2-A4], with original source [P2-L4-497] and peer LSPV-2/495, /496, /497. [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN. Peer [P2-D1], [P2-C3], [P2-B1], [P2-B2] unchanged.

## IDEA -> SEARCH -> ITERATE
**Hypothesis declared before literature/code review:** the signed, exact fixed-field SAT equality reduction of LSPV-2/495 is not only a promise-access separation, but its authenticated source language has minimum binary Hamming distance at least eight. Hence exact or bounded-error randomized black-box membership testing must physically read a linear number of independent input positions on every valid member. This addresses the [P2-A4] input-authentication stage, NOT arbitrary-SAT time hardness.

**Falsifiers:** F1: two distinct authenticated originals at fixed H have binary distance below eight; F2: one-bit corruption is still a member of the same fixed family; F3: adaptive bounded-error membership can distinguish all single-bit mutants while probing o(N) positions of an accepted member; F4: source packet order or representation differs from the original /495 encoding, invalidating an apparent finite control.

**SEARCH and continuity:** Read both entire root proof trackers, governing Nov 2 five-role handoff, AGENTS.md, CODEX.md, repository pnp-research skill, current issue #3 and latest peer comments, LSPV-2/495, /496, /497, LSPV-4/497, actual GROKPROOF/2026-11-08_0930_PROGRESS.md (blob e3e8c9657e0f2b2e0751752135cf2558e28183cf), and actual Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67). External pinned review: konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 (finite-machine only); blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 (restricted method index); MassimoLauria/cnfgen cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (original parity CNF); meelgroup/frat-xor format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f (different XOR certificate grammar); openai/math README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae (formalization caveat). Public web searches reviewed original FLMV JACM 2005; Urquhart JACM 1987; Ben-Sasson/Wigderson JACM 2001; Marcus/Spielman/Srivastava Annals 2015; Reingold/Vadhan/Wigderson Annals 2002. No separate Google-branded search client or native FLMV executable; no PDF full-text review. None of these repositories asserts the missing universal Route A contraction.

## Source/theorem/model ledger
**Source:** Existing LSPV-2/495 exact ORIGINAL signed, strict proper, duplicate-free 3-CNF, on connected cubic bipartite graphs with H vertices, m=H/2 matching edges, fixed public odd charge, L-then-R vertex packets, four parity clauses per vertex. Every matching edge j uses ID 2j+1+a_j on L and 2j+1+b_j on R (j zero based); each nonmatching edge has a globally fixed ID in H+1..2H. Local IDs are numerically sorted in each clause; each source consists of 4H original clauses, 12H literal fields. Binary source: magic 11100011, unary H and 2H, W=ceil(log2(2H+1)) variable-ID bits plus sign per field, trailer 10:
$$
N(H)=3H+12+12H(W+1)=\Theta(H\log H).
$$
There are exactly 2^(2m) distinct recognized source strings per fixed graph, one for every pair (a,b). **Known:** source SAT iff a != b; each diagonal a=b is original odd-charge Tseitin UNSAT. On suitable cubic-expanding families, ordinary shared-DAG Resolution proof size is 2^Omega(H) (Urquhart and Ben-Sasson/Wigderson), not full mixed calculus or general machine hardness. MSS establishes existence of degree-three bipartite expanders, not the efficient graph/matching enumerator U required for uniform logspace source recognition. Existing strong shortcuts: GF(2) parity elimination, ER, LSPV-4/497 indexed detection and LSPV-2/496 randomized streaming fingerprint; retain as upper controls. A public fully checked signed-source generator costs its actual time and space. This report establishes an intrinsic bit-probe floor for *untrusted, independent, complete membership tests* only.

## Theorem 498.1: exact weighted Hamming geometry (PROVED/RESTRICTED)
For two source strings s(a,b) and s(a',b') for the SAME fixed graph, H, matching order, charge and header, write
$$
\delta_j = \operatorname{popcount}((2j+1)\oplus(2j+2)).
$$
Because matching IDs remain smaller than all nonmatching IDs, changing a_j changes exactly four copies of the W-bit ID field, without moving any sign or packet field. Their total bit-distance is 4 delta_j. The endpoint fields for distinct j and sides are disjoint. Consequently the exact distance is
$$
d_H(s(a,b),s(a',b')) =
4\sum_{j=0}^{m-1}\delta_j
\bigl(\mathbf 1[a_j\ne a'_j]+\mathbf 1[b_j\ne b'_j]\bigr).
$$
Adjacent odd/even integers necessarily differ in the low bit and at least one carry bit, so delta_j >= 2. At j=0, the binary encodings of 1 and 2 differ in exactly two bits. Therefore, whenever at least one matching edge exists:
$$
\boxed{d_{\min}(\mathcal C_{G,H})=8.}
$$
Proof uses exact original field order, no guessed variable incidence or unauthorized proof rule. In particular EVERY 1-bit mutation of EVERY recognized member is outside this fixed specialized source language.

## Theorem 498.2: randomized full-source authentication floor (PROVED/RESTRICTED)
Fix any member s of length N. Let B be any adaptive *indexed-bit-query* algorithm that distinguishes membership in the exact specialized language with two-sided error at most epsilon < 1/2 on EVERY N-bit input, and no extra trusted source-dependent side channel. For each i, y_i=s xor e_i is a nonmember by Theorem 498.1. Couple B(s) and B(y_i) under identical random coins. The transcripts and outputs agree unless the machine probes bit i. As membership acceptance probability differs by at least 1-2epsilon, the probability, on s, of probing i is >=1-2epsilon. Summing over the N positions:
$$
\boxed{\mathbb E[\#\text{ distinct bit positions queried}\mid s]\ge (1-2\epsilon)N.}
$$
At epsilon=1/3 this is N/3 expected distinct queries for every authenticated member. Zero-error algorithms must read every bit with probability one. Actual host indexed input reading costs >= one transition per requested bit on a unit bit-probe model; the FLMV machine may require more per request. This is a **linear input-authentication lower bound**, not a superlinear SAT solver lower bound or an impossibility for a compiler that constructs and authenticates its children by construction. OUTSIDE must not be called MALFORMED: many outside sources remain legitimate arbitrary CNF inputs needing general SAT processing.

## Independent finite checks and real falsifier
An independently authored Python source generator plus separate GitHub-published JavaScript V8 verifier enumerate all 64 K3,3, all 256 cube Q3 and all 16,384 Heawood accepted sources, for 16,704 total recognized strings. The 36,867 tested distinct pairs all satisfy the exact weighted metric, with observed min distance eight; 252,786 independent single-bit mutations were checked and none was another member. Original word lengths: 390, 612, 1062 bits. Python authenticated first UNSAT original SHA256 against LSPV-2/495 on ALL three graphs:
K33 5dc81af61477fdf2e4f9e3c72135ce0489dea80c6873868f6d0bd6d9ef882ef8;
Q3 80b0e7b161e48d81f4b477770a162130f325a87b95fbe739864d7046b2f3a7a1;
HEAWOOD 2c098df7e943ad86450c3929ff0d9325f93935cabbde59cdc1ba7d9c839630c0.
Independent JavaScript and Python counts agree exactly. **Hostile falsifier F4 was genuinely triggered during initial test:** nonmatching Heawood edges were generated in insertion order rather than the original peer's lexicographic order. The initial Heawood SHA differed, although the algebraic metric still held; corrected both implementations, reexecuted and verified the source SHA before publication. An initial sparse pair sample missed the min-distance witness; corrected to include explicit one-coordinate neighbors, retained all failed pilots as described. All final checks passed. No native FLMV instruction-level machine, general CNF oracle or R_mix341 checker was run.

## Fully charged resource ledger and limits
For an *untrusted* fixed-grammar member: logical inference nodes = 0, proof certificate bits = 0, source queried N distinct bits (deterministic zero-error) or expected >=(1-2epsilon)N for two-sided error, INDEX/head arithmetic must be separately charged, WORK high-water may be O(log N) for a parser with public local graph generator U but requires its actual T_G and S_G. Local malformed/header parsing, graph traversal, packet construction, checking, output and eventual fallback cannot be skipped. An indexed parser with full source verification and public polylog-time U can achieve O(N polylog N) time, O(log N) WORK, hence the **input-read exponent one is tight** for this exact source-authentication stage (not guaranteed uniform without U). For q independent, separately supplied untrusted children of M bits each, independently verifying each membership takes Omega(qM) reads in aggregate, which at q=N^(3/5), M=N^(1/2) reaches N^(11/10); this DOES NOT apply to shared/trusted or compiler-generated children and is not an all-input SAT recursion lower bound. There are no independent child executions, branch searches, caches or recomputation in this verifier. Native guest time, guest input construction, source conversion and all-phase simultaneous peak for an arbitrary A remain unproved. The specific Route A targets t'<=max(11/10,3/5+t/2) and s'<=max(1/2,s/2) are not established here.

## Findings and scientific status
**Actual advance:** exact weighted-Hamming geometry and an input-wise bounded-error query lower bound for a pre-existing published Resolution-hard-source encoding's authenticated *specialized membership*. The result is elementary and no originality beyond scope-specific instantiation is claimed. It strengthens [P2-A4] authentication accounting. **Not advanced:** universal same-machine contraction [P2-A2]/[P2-A5]; source-model transfer to historical mixed R_mix341 [P2-D1]/[P2-C3], all-rule Wbar_R lower bound [P2-B1], noncircular B3 [P2-B2]. Fixed historical grammar and weights, 2 Route A/3 Route B, all five agent identities, schedules and enabled states remain unchanged. P versus NP OPEN.

**Artifacts:** experiments/arc/lspv4_498_hamming_authentication.cjs (published, independent V8 replay), results/raw/arc/2026-11-08_0936_LSPV4_498_HAMMING_AUTH_RAW.json (published), independent_hamming_audit.py and independent_raw.json (local reproducibility bundle), five-role handoff research/coordination/2026-11-08_0936_LSPV4_HAMMING_FIVE_ROLE_HANDOFF498.md. No main.tex changes.

**References:** Urquhart, *Hard Examples for Resolution*, JACM 1987 DOI 10.1145/7531.8928; Ben-Sasson/Wigderson, *Short Proofs Are Narrow*, JACM 2001 DOI 10.1145/375827.375835; Fortnow/Lipton/van Melkebeek/Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 2005 DOI 10.1145/1101821.1101822; Marcus/Spielman/Srivastava, *Interlacing Families I*, Annals Math 2015 DOI 10.4007/annals.2015.182.1.7; Reingold/Vadhan/Wigderson, *Entropy Waves*, Annals Math 2002 DOI 10.2307/3062153.
