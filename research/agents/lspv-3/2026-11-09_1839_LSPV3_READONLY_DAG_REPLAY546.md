# LSPV-3/546: Read-only contextual DAG replay and the FLMV verifier-space boundary

**November 9, 2026, 18:39 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## IDEA (registered before tests), four falsifiers

**Candidate:** An explicit, source-authenticated shared proof DAG with logarithmic-space checkable local rules can be reverified from a read-only certificate with small dense native work space by recomputation, even if its paid node count is exponential in the source size. This gives a precise *verifier* time-space theorem, NOT a deterministic SAT-decider space bound.

Falsifiers: (1) forged original clause or changed source accepted; (2) one CASE branch used twice, cyclic parent, or undischarged context accepted; (3) revisiting an ancestor improperly counted as new logical work or a full DAG secretly stored in the alleged low-space schedule; (4) auxiliary certificate input length B confused with original SAT source length N, or NP existential acceptance confused with universal UNSAT closure.

## SEARCH and continuity

Read the complete current root proof1.txt and proof2.txt, current issue #3, AGENTS.md, CODEX.md, pnp-research skill, governing 2026-11-09_1624 assumed-time handoff (blob 644b0d4745f2edeb8718c7e536a7da995b36b36f), earlier abstract-negative handoff (8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b), actual peer LSPV-3/544 and /545, LSPV-5/472, LSPV-1/549/550, Grok 2026-11-09_2015_PROGRESS.md and Claude 2026-10-28_1326_CLAUDE_TPORT-0001.tex. Existing indexed-tape and DFS-tree examples are not claimed as newly discovered.

Primary paper, inspected directly: Fortnow, Lipton, van Melkebeek and Viglas, JACM 52 (2005), 835-865, DOI 10.1145/1101821.1101822, https://lance.fortnow.com/papers/files/tst.pdf . Section 2.1 charges *maximum non-index work-tape position ever read/indexed*, not just occupied cells; read-only source/evidence is not charged but writable index tapes are. Theorem 5.7 and Corollary 5.8 address deterministic time-space exclusions by distinct parameters and require a precisely matched model. Primary abstract methods: Cousot & Cousot (POPL 1977), D'Silva/Haller/Kroening (POPL 2014), Clarke et al. (JACM 2003), standard recomputation/pebbling principles. Later small-space bounds up to c<2cos(pi/7) differ from the positive-space beta formula.

Change-aware actual external paths: konard/p-vs-np scripts/proof_status.json (blob 93b77ed3d8fe456f81c690035f45f07910a247f2), blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5), meelgroup/frat-xor format.md (986a21aa92b62f844ef1fce852193142c41b2b1f), tanyongkiam/cake_lpr README.md (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c), openai/math README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae). None defines historical R_mix341. The cake_lpr README notes its Nov 1, 2026 final planned release and forthcoming replacement. No native historical checker or full FLMV machine executed.

## ITERATE: Theorem 546.1, local-checkable proof DAG read-only replay

**PROVED/RESTRICTED.** Let F be an independently supplied binary CNF source (length N) and P a read-only, explicitly encoded, topologically indexed *finite DAG* refutation certificate (length B bits), with dependency depth d, maximum premise arity r>=2, and q globally distinct paid inference identities. Suppose each syntax-sensitive, source-authenticated local inference predicate (including assumption scope, signed conclusion, original clauses, provenance and references) is checkable in O(log(N+B)) auxiliary writable bits and polynomial time using indexed read-only access. A root is a false conclusion under empty assumptions, AND premises are all checked, and a parent node number is smaller than its child. Then a deterministic checker of the **pair (F,P)** exists with

$$
S_{\mathrm{native,verify}}=O((d+1)\log(N+B)),
\qquad
T_{\mathrm{verify}}=O((1+r+\cdots+r^d)(N+B)^a)
$$

for a constant a fixed by the local predicates. This is a dense contiguous-work-stack implementation on the FLMV-style machine; its native high-water is bounded by its contiguous stack and scratch footprint. This statement is conditional on local-logspace rule checking, NOT established for the complete historical mixed grammar.

**Proof:** Depth-first recursively verify each referenced node from the read-only certificate. Each frame stores its O(log(N+B))-bit index, child ordinal and restart position, plus local scratch O(log(N+B)); only d+1 frames coexist. Strictly decreasing references prohibit cycles. Replay all AND children, never accepting a lone successful child. A shared node may be read/recomputed repeatedly, increasing time, but paid logical inference nodes remain globally distinct and are counted once. The maximum number of visits is bounded by 1+r+...+r^d. Read-only addressing, restart, scanning, comparisons, output and construction are paid in verification time; the input and certificate themselves are additional **read-only evidence**, not included in the standalone SAT input. Sound local inference induction from exact original clauses and context discharge proves root UNSAT. The ideal proof work is a separate sum over distinct paid identities under the fixed calculus, not verifier visits.

**Important limitation:** A deterministic SAT decider A_P receives F alone. This theorem constructs a verifier for (F,P). Neither proof discovery nor producing/reading B bits from source alone is free. Consequently S_ver cannot become S_A_P without an all-input, both-label, same-machine compiler and all-phase accounting. The proof DAG and the abstract collecting-state set also give no lower bound on A_P working memory. NP witness acceptance is existential; UNSAT closure in this audit requires *all* branches.

## Actual independent finite controls

A separate typed CASE/LEAF audit calculus was specified (NOT historical R_mix341). LEAF under a complete signed context Gamma cites an **original clause falsified by that assignment**. CASE(x) accepts a false parent Gamma only after BOTH children Gamma+{x} and Gamma+{-x} have closed. The root must have empty Gamma. Source is supplied independently and compared exactly. Acyclic IDs, source indices and contexts are checked.

For the established cubic Tseitin 3-CNF encoding with odd vertex charge, K4, prism6 and prism8 give respectively 16, 24, 32 original ternary clauses on 6, 9, 12 edge variables. Each has zero satisfying assignments; even-charge counterparts have 8, 16, 32. Independently written JS tested 46 assertions, Python 36 assertions/groups. Corruptions of source, clause ID, CASE partner, parent cycle and assumption scope were rejected; malformed zero/repeated-variable strict-3CNF and 30-digit noncanonical numeric root-ID controls were also rejected; even-charge SAT controls cannot close. JS code is in experiments/arc/lspv3_546_readonly_recomputation_checker.cjs; independent Python is in the downloadable reproduction. **Both executed implementations materialize their entire proof object; neither measured native low-space machine operation.**

| Original graph | Tree positions | Paid CASE | Depth | JS explicit evidence bits |
| --- | ---: | ---: | ---: | ---: |
| K4 | 127 | 63 | 7 | 57,672 |
| Prism6 | 1,023 | 511 | 10 | 521,984 |
| Prism8 | 8,191 | 4,095 | 13 | 4,886,304 |

The prior *declared-semantic* K4 mixed AND3/GF(2) proof has 15 nodes and remains a legal shortcut upper-bound control at its verified scope; these enumerative CASE proofs are not minimum historical refutations.

## Resource and abstract-interpretation polarity

A complete concrete configuration includes the immutable source and any separately supplied certificate; machine and deterministic/nondeterministic mode; program state, every work/index tape cell and head, read-only head position, high-water H, current live occupancy L, elapsed steps t, signed branch context, source provenance, paid identities and available shared DAG. An abstract alpha records exact authenticating source labels and safe intervals for t, H, L and graph/context state; gamma includes *all* complete configurations consistent with them. For each admissible step require Post(gamma(a)) subseteq gamma(Post-sharp(a)); unknown historical rules must be overapproximated, not deleted. Sound upper H_high dominates the supremum H across represented runs; sound universal lower H_low does not exceed their infimum. Abstract state cardinality and certificate length do not convert into machine-space lower bounds.

The published beta(c)=((c+2)/c^2-c)/2 is positive for c<about 1.52138, with beta(6/5)=23/45 and beta(6/5)-1/2=1/90. Exponent-only ratio N^(1/90) at N=10^6,10^12,10^24,10^60 equals approximately 1.1659, 1.3594, 1.8478, 4.6416. These are NOT bytes, effective constants, or finite-size SAT evidence. Higher FLMV levels extend to c<phi, and later small-space-only improvements reach about 1.80194; none supplies the missing upper S_A_P. SAT in P never grants c=6/5.

## Status and remaining exact arrows

**New:** general quantified read-only shared-DAG verifier bound with original-source/context/AND preservation and explicit auxiliary-input transfer firewall, generalizing earlier tree-only space tests. **Verified:** symbolic stack induction; 46 independent JS + 36 Python finite controls. **Still OPEN:** [P1-01], [P1-03], [P1-04], [P2-A2], [P2-D1], [P2-C3], [P2-B1], [P2-B2]. The historical grammar, full mixed abstract transformers, superpolynomial all-rule minimum and noncircular same-R B3 remain missing. No new agents or changes to schedules, weights, roles or task states. P versus NP OPEN.


**Publication addendum, 18:43 PST:** A separate source-authenticated K4 local-lemma DAG was added to the independent JS program. A paid CASE node is referenced through two distinct zero-cost scope-strengthening WEAKEN nodes and is reverified on both routes, but charged once as a distinct proof node; a second CASE merges those routes. Seven total nodes, two distinct paid CASE IDs. The local signed-context lemma was accepted, but the same nonempty-context root was rejected as global UNSAT; a forged branch context was also rejected. **WEAKEN is explicitly a test-only admissible audit rule and is NOT promoted to historical R_mix341.** Total JS checks now 46. Verified source code blob ca959a2322f5baa9c7f2c109395dad71605353f4.
