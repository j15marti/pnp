# LSPV-3/540 | Exact local-factor abstraction requires eight bits
**2026-11-09 12:26 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Proof-chain:** new [P2-L3-540], refining [P2-L3-539] and the local domain-precision dependency [P2-C3]. Native historical grammar [P2-D1], all-rule abstraction [P2-C3], superpolynomial mixed lower bound [P2-B1], and B3 [P2-B2] remain OPEN.

## IDEA and pre-search falsifiers
Candidate: in the **declared** /341 local AND3 *semantic fragment*, a deterministic compositional summary that determines exactly whether a conjunction is empty against **every singleton context** must distinguish all 255 non-TRUE three-variable Boolean factors. This makes /341's eight-bit local truth mask information-theoretically optimal **for the stated exactness contract**.
Falsifiers: (1) some proper factor cannot be built from original proper signed 3-CNF clauses via unit-paid binary AND3; (2) some distinct factors are not distinguished by singleton intersection; (3) a summary with <255 states satisfies the exact contract; (4) the argument relies on an unauthorized global source/branch merge. (1)-(3) fail symbolically and computationally; (4) is explicitly excluded by scoping this to the local semantic factor, not full proof states.

## SEARCH and continuity
Read governing abstract-negative five-role handoff (blob 8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b), proof1.txt (96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and proof2.txt (69ada15786a8695e74459386a76d732a97ed9c84), issue #3, AGENTS.md, CODEX.md, project research skill, current LSPV-3/539 and LSPV-5/466, actual Grok progress and Claude world ledger. Full proof2 is approximately 800K UTF-8 characters: read via the authenticated GitHub connector; this report cites exact nodes, not only chat summaries.

The actual /341 declaration is `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb): binary unit-paid AND3 computes exact truth-table conjunction on at most three **original** variables, sources are free, and XOR tags require exact row equivalence. It does not fix the historical byte production for the word 'condition'. LSPV-5/412 (`research/main/2026-11-07_0748_MAIN_AND3_PARENT_GRAMMAR_REFEREE412.md`, blob b99084b9e1534654207042d00d6645361dfc5863) shows the grammar ambiguity is substantive. Here every join uses only source-clause or earlier AND3 factor views, as in the /341 exhibited trace; no claim of accepted-byte checker replay.

Primary papers inspected through retrieved records: Cousot & Cousot POPL 1977 (abstract soundness), Giacobazzi-Ranzato-Scozzari JACM 2000 DOI 10.1145/333979.333989 (completeness), D'Silva-Haller-Kroening POPL 2014 DOI 10.1145/2535838.2535868 (abstract satisfaction), Clarke et al. JACM 2003 DOI 10.1145/876638.876643 (CEGAR), Ben-Sasson-Wigderson JACM 2001 DOI 10.1145/375827.375835 (Resolution width/size), and Urquhart JACM 1987 DOI 10.1145/7531.8928 (qualified expander Tseitin Resolution hardness). These do not authenticate the historical mixed checker.

Targeted current repository review: `konard/p-vs-np` code search reached `scripts/check_proof_status.py` at ref ecedd2b45f1c524d85c00b2da27a9c140025550c; root proof_status.json lookup returned 404; `blkph0x/p-vs-np-proof-research:REPORT.md` blob 67d3d3b455737d262b1c9e690adf0f6f65bbaefb directs to its current method index; `meelgroup/frat-xor:format.md` blob 986a21aa92b62f844ef1fce852193142c41b2b1f separates theory IDs and documents checker limitations; `openai/math` README at ref 4eaee87548250b2682affda7d05d947c05554bae is verification background, not a rule source. Google-specific search was unavailable; conventional web and authenticated GitHub were used.

**Hard-family control:** qualifying connected cubic expander odd-charge Tseitin strict 3-CNF has n=3h/2 edge variables, m=4h proper three-clauses, N=O(h log h) encoding, exponential ordinary DAG Resolution lower bounds under the source theorem's expansion assumptions. The /341 declared mixed AND3/GF(2) proof is 4h-1 unit-paid nodes. No unrestricted hardness inference follows. Cook ER, FRAT-XOR, PHP, reconvergent sharing, and extension variables remain mandatory shortcut controls.

## ITERATE: theorem and constructive proof
Let X={0,1}^3, let D summarize any independently presented factor A subset X, and require an exact deterministic predicate for `(A intersect C == empty)` using only `summary(A), summary(C)`, for all local factors and contexts C. (Equivalent: exact abstract conjunction followed by exact empty test.)

**Theorem 540.1 (PROVED/RESTRICTED):** even for the 255 proper A subsetneq X, at least 255 different summary values and thus at least ceil(log2(255))=8 fixed-length binary bits are necessary. Eight-bit masks suffice.

Proof: For A != B choose point p in their symmetric difference, and context C={p}. Exactly one of A intersect C and B intersect C is empty. If summary(A)=summary(B), the deterministic summary-only predicate could not distinguish them. Hence the map must be injective on the 255 proper factors. Seven bits encode at most 128; eight bits suffice by exact bitwise intersection and zero test. QED.

**Lemma 540.2 (original-source strict-3-CNF realizability):** For p=(p1,p2,p3) let C_p be the ternary clause with literal x_i if p_i=0 and not x_i if p_i=1, false exactly on p. Any proper factor A has original source formula F_A = conjunction of C_p over p not in A. It has 1 to 8 distinct proper 3-clauses; a binary left-fold of the clauses uses precisely (8-|A|)-1 paid AND3 joins, all legal in the declared local fragment. Singleton {p} uses 7 clauses and 6 paid joins. All antecedents are original source or earlier AND3 IDs, with full source provenance and no free inferences. QED.

**Corollary (distinct hypothetical AND-k calculus, not /341):** when exact AND-k supports all k-bit exclusion clauses, the 2^(2^k)-1 non-TRUE factors are pairwise observable and require at least 2^k fixed-length summary bits. This is about exact generic independent factor representations, not general SAT time or compact structured circuit factors.

**CEGAR witness:** masks A=105 and B=104 differ on assignment 000. Singleton context mask C=1 yields A&C=1 (nonempty), B&C=0 (empty). A uses 3 paid joins; B uses 4; context uses 6; optional final join costs one more. These are exhibited *unoptimized* DAGs, not minimum costs for combined inputs. Prior /539 already showed insufficiency of affine hull + model count; /540 adds a **matching lower bound** on exact local summary bits.

## Independent checks, resource ledger, and trust boundary
Python and separately implemented Node.js reconstruct all 255 source-factor traces, eight singleton traces and every one of 32,385 unordered factor pairs. All distinguish. Python: 105,620 check calls, 0.034 s, 96,920 KiB peak RSS, five deliberate corrupt-trace rejections and four malformed-input rejections. Node: 108,366 checks, 33,604 KiB RSS, five corrupt-trace rejections. No random seeds. This is finite confirmation; the unrestricted local theorem follows from the symbolic proof. Neither implementation is the historical checker.

Logical cost r-1 for r original clauses; 2 parent references per paid AND3; shared inference identity charged once. Reference IDs, source authentication, node serialization and proof/hash evidence bits add to the eight mask bits. Construction/search, reading, parsing, checking, output, and peak simultaneous memory are *not* free for any implemented solver. The observed runtimes concern only these bounded local verifiers. No cutoffs are being extrapolated to arbitrary variables or arbitrary auxiliary syntax.

**Limitations:** A sound MAY abstraction need not be exact and may have fewer than 255 states; then this theorem does not show its nonreachability power. A global abstraction can store information outside the local factor summary. Neither original historical LOCAL-CONVERT/DEF accepted-byte syntax, an empty-factor terminal goal rule, cross-branch discharge, nor universal source-retraction is authenticated. A proof-construction invariant excluding all legal mixed refutations under a superpolynomial budget has not been found.

**Actual advance:** minimum sufficient and necessary number of binary bits for the exact local AND3 factor domain, with source-authenticated strict 3-CNF constructions.
**Validation:** symbolic pairwise-separation proof, exhaustive independent Python and Node checks.
**Publication:** see companion code/raw and handoff; tracker and manuscript status in coordination issue #3.
**Remaining gap:** [P2-D1], [P2-C3], [P2-B1], [P2-B2] are OPEN. P versus NP OPEN.
