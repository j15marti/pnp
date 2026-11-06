# LSPV-4/429: Source-authenticated private-tail autarky and charged common-core sharing

**November 5, 2026, 20:40 PST | Route A PRIMARY | PROVED/RESTRICTED source/port lemma | COMPUTATIONAL finite tests | universal FLMV contraction OPEN | P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE

Hypothesis: a legal structural shortcut defeats the no-reuse full-read-footprint cache of LSPV-4/428 with an original-source-authenticated, low-workspace projection. Three falsifiers: (F1) a sparse tail identifier aliases a core variable; (F2) an unproved positive-tail witness or corrupt source gets a false shared label; (F3) exact matching of sibling cores secretly stores whole inputs or uses unproved hash collision resistance. After primary and project review the claim was narrowed: **autarky elimination is known**, and /428 had explicitly noted this shortcut. The advance is a fixed streamed binary grammar, authenticated lazy child port, native resource proof and independent finite validation. LSPV-2/433's typed inert-scan erasure is a separate complementary repair.

## Fixed source grammar

Binary source: 8-bit magic `10101110`, positive unary threshold `1^b0`; one or more core proper three-literal clauses tagged `10`; zero or more private tail three-literal clauses tagged `11`; final `00`. A literal is a sign bit (0 positive), unary binary-ID length `1^k0` with k>=1, and a canonical k-bit ID beginning with 1. Reject bad magic/terminator, trailing bits, improper clause ordering or noncanonical IDs. For every core literal demand ID **bit length <=b**, every tail literal ID bit length **>b**, and at least one **positive** tail literal per tail clause. This is a specially encoded 3-CNF source subclass, NOT the fixed historical R_mix341 calculus or a new rule for it.

**Theorem 429.1 (PROVED/RESTRICTED).** With G the conjunction of core clauses and T of tail clauses, the authenticated source satisfies

$$
mathrm{SAT}(Gland T)iffmathrm{SAT}(G).
$$

Indeed every core ID is <2^b, every tail ID >=2^b, so variable sets are disjoint. Assign TRUE to all tail variables: every tail clause has a true positive literal. Every satisfying assignment of G extends to G and T, and every model of G and T restricts to G. No SAT/equivalence oracle is used.

**Theorem 429.2 (PROVED/RESTRICTED).** On FLMV's read-only indexed input and writable random-access/index tapes, a deterministic scanner processes the entire input in O(N) sequential native steps and O(log N) *highest-position physical* workspace on dense packed tapes; it stores positions, ID lengths, signs and flags but never numerical variable IDs. Sparse 1025-bit ID values are therefore legal with O(log N) storage. Record cut position P before the first tail (or terminator). The exact projected child has bits source[0..P-1] followed by `00`. Each virtual guest bit or end-of-input probe is served by at most O(log N) native indexed operations, dense O(log N) address scratch and a charged source read. No full input/child is copied into writable workspace. With a fixed total correct indexed guest A, full parsing and guest simulation obey

$$
T_{mathrm{proj}}(N)=O!left(N+T_A(P+2)log^{O(1)}Night),qquad
S_{mathrm{proj}}(N)=O!left(log N+S_A(P+2)ight).
$$

Every indexed-head movement, address write/erase, repetition, error path, guest frame, and all-phase peak must be charged. This is a concrete *conditional special-class* virtual port and not an all-input resource contraction. For malformed sources reject. For other well-formed CNFs the valid fallback is to call A on the original input, with no claimed exponent improvement.

**Portfolio corollary (PROVED/RESTRICTED).** Given q already authenticated virtual children of length <=L, check each source in full and compare projected core bits **exactly**, not merely by hash. When all core encodings agree, one guest call on the common core labels all q children. Deterministic source verification and comparison takes O(qL polylog N) indexed native steps, additional physical workspace O(log N) plus a single guest workspace/port frame; emitting q labels sequentially costs O(q) and no q-bit working array. Mutated core bytes force a distinct guest call. For q=N^(3/5+o(1)), L=N^(1/2+o(1)), source checking and comparisons cost N^(11/10+o(1)): **they saturate rather than violate the local FLMV ceiling**. This proves neither a universally available portfolio nor a recursively valid join.

## Hard-family and shortcut ledger

For a cubic connected edge expander G_H with H even vertices, one variable per edge and charge c_v at each vertex, forbid the four incident edge assignments whose parity differs from c_v. Exactly 3H/2 edge variables, 4H proper width-three clauses and N_H=Theta(H log H) bits with polynomially numbered edges. Odd total charge certifies UNSAT by summing all vertex equations over GF(2). Published Urquhart (1987) and Ben-Sasson/Wigderson (2001) results imply exponential **ordinary DAG Resolution** size for suitable growing expander families under their graph/encoding hypotheses. These are not universal computation or mixed-calculus lower bounds. The previously verified 4H-1 paid-node mixed AND3/GF(2) refutation on eligible bridgeless odd sources remains a mandatory shortcut. CNFgen's actual `cnfgen/families/tseitin.py` implements per-vertex parity clauses. Finite K4/cube controls used here are not certified growing asymptotically hard graphs. No 3-CNF hardness-preservation transfer from an unrelated encoding is presumed.

## Host-language finite verification

Python producer: four 16-child portfolios (K4 and cube, each even/SAT and odd/UNSAT charges), 64 distinct strings, 16 children per portfolio and one authenticated projected common core per portfolio. Baseline full-read latest-anchor guest calls: 64. After legal projection: 4. Exhaustive K4 SAT checks on one-tail controls; 36 malformed source rejections (nine types x four), four valid mutated-core comparison rejections, one 1025-bit sparse-identifier source. Python instrumented source reads: 48,544 across 64 portfolio inputs, all bytes/indices covered. 370 producer assertion groups. Independently implemented Node.js checker reconstructed core clauses and encodings, verified source SHA-256 and passed 279 assertions. Computed source/workspace counters are model proxies, **not physical FLMV Turing-machine measurements**; a host Python source string is not charged as writable space in the formal read-only tape model.

## Actual search/corpus continuity

Read `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, the 2026-11-02 five-role handoff, current issue #3, LSPV-4/427,/428, LSPV-2/432,/433, actual `GROKPROOF/2026-11-05_1913_PROGRESS.md` and `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`. Both requested repos actually inspected: `konard/p-vs-np/proofs/complexity/README.md` sha 7ee9a11 (finite one-tape, not FLMV), `scripts/proof_status.json` sha 93b77ed; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` sha 18d693e and `PROOF_PORTFOLIO_BRIDGE_REPORT.md` sha 22215ce (bounded projectors, no universal interface). Relevant `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` sha 4bb5fd; `meelgroup/frat-xor/README.md` sha 38a137b (proof-checker not all-machine theorem); `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` sha 1ced21f (costed particular driver). Primary FLMV PDF Section 2.1 text-read and page 4 screenshot checked, `https://lance.fortnow.com/papers/files/tst.pdf`. Bryant, Tan, Heule, SAT 2025, DOI 10.4230/LIPIcs.SAT.2025.8 supplies an independently established certified projected knowledge compilation framework with Skolem witnesses; it is not a universally cheap projection guarantee. Indexed web searched FLMV model, SAT autarkies, certified projection, Tseitin Resolution. Google-branded interactive search not available. No novelty claim follows from failed searches.

**Precise remaining gap (OPEN).** Some syntactically eligible portfolios can be safely shared at the claimed local resource budget, but arbitrary valid inputs do not admit a demonstrated uniformly findable, source-authenticated, both-label/malformed-aware recursively iterable family of small SAT children. The fallback may have size N, so the universal t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2) FLMV contraction is NOT established. B1/B2/B3 and fixed R_mix341 transfer remain independent OPEN obligations. No tasks, schedule, weights, root main.tex or other role regions altered. P versus NP OPEN.

References: [1] Fortnow, Lipton, van Melkebeek, Viglas, JACM 52 (2005), DOI 10.1145/1101821.1101822; [2] Urquhart, JACM 34 (1987), DOI 10.1145/7531.8928; [3] Ben-Sasson/Wigderson, JACM 48 (2001), DOI 10.1145/375827.375835; [4] Bryant/Tan/Heule, SAT 2025, DOI 10.4230/LIPIcs.SAT.2025.8.
