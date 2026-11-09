# LSPV-3/537: all-facet affine-hull threshold and a sound local AND3 reduced product

**2026-11-09 09:30 PST | LSPV-3 Hypergraph & Certificates | Route B | PROVED/RESTRICTED + COMPUTATIONAL. P versus NP remains OPEN.**

**Proof-chain IDs:** [P2-L3-537] (new scoped evidence), [P2-L3-536], [P2-D1], [P2-C1], [P2-C3], [P2-B1], [P2-B2], and unchanged [P1-01], [P1-03], [P1-04]. This paper does **not** update the historical rule grammar, costs, tasks or role allocation.

## IDEA: candidate and four falsifiers (stated before search)

**Candidate.** The affine-only abstraction that computes the GF(2) affine hull of each signed original clause and then intersects those hulls is too coarse even to recover one cubic Tseitin vertex parity row. A local 8-bit Boolean-factor reduced product with original clause provenance and distinct paid-node history recovers the row after exactly three *declared* binary AND3 joins. This is a local factor/interface theorem, not a global proof-work lower bound.

- F1: some strict subset of the four signed cubic parity facets already entails a nontrivial affine equation;
- F2: the entire set of four facets fails to define exactly the intended parity row;
- F3: a claimed three-node AND3 construction cannot be independently replayed from four ORIGINAL source clauses with exact Boolean truth tables and identities;
- F4: literature or original repository already contains precisely this all-facet affine-hull threshold and its costed local abstract transformer, rather than only closely related source counting or affine-hull cautions.

F1--F3 were ruled out by symbolic argument and independent finite replay. Targeted repository searches located related /341 source-capacity, /414 affine-annotation and /437 affine-hull nonidentifiability controls but no identified report stating this exact all-facet threshold. This is **not** a claim of global novelty. F4 remains subject to peer review and broader literature.

## SEARCH: actual provenance and model

Read the governing *2026-11-09_ABSTRACT_INTERPRETATION_NEGATIVE_FIVE_ROLE_REFOCUS.md* (blob 8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b); **both complete live trackers** at startup (proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2.txt blob 6ebdadebef786b1e75294a556d7718c3e8436a20); issue #3 and its latest LSPV-3/536, LSPV-5/463 comments; AGENTS.md blob 4ae902888754d0b06ba4ce1aaeca0657a92b46a9; CODEX.md blob 754999f50de93cdb693ed37bc8110d31e9e698ef; .codex/skills/pnp-research/SKILL.md blob b8df83a7b0b1428f349b0e02ce1387d979e8db7f; original R_mix341 semantic text in research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb); LSPV-3/536 and /414; LSPV-1/437 and /537 tracked evidence; LSPV-5/463; actual GROKPROOF/2026-11-09_1230_PROGRESS.md (blob 0ee19c6b2fdf92b64427ab737fe563346779c828) and research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex (blob 79e4d4e7e0e3edff3aba8610852c45534bdde128). All actual reads; no scratch persistence assumed.

Original declared /341 has free, indexed source clauses; unit-paid at-most-two-premise AND3 exact truth-table conjunction over at most three **original** variables; XOR from two bona-fide rows; Resolution; one-input LOCAL-CONVERT; and paid conservative two-input DEF, but does not specify a complete accepted-byte grammar for every port/facet/branch. The recovered /341 checker accepts only a restricted SOURCE/AND3/XOR sublanguage. It is NOT an authority for RES-parent AND3, DEF facets, or branch discharge. These remain [P2-D1] OPEN. Unknown native steps must be may-overapproximated, not excluded.

Required change-aware corpus: konard/p-vs-np scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 (both are scoped/hypothesis inventories, not proof authorities); meelgroup/frat-xor format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f (XLRUP external grammar; its checker presently accepts XOR but not BNN according to the format document); tanyongkiam/cake_lpr README.md blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c (November 1 2026 last planned LPR release); MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (published Tseitin family generator); openai/math README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae (heterogeneous verification). No independent Google-branded search service was available; general web literature search was used.

**Literature and transfer scope.** Cousot--Cousot (POPL 1977, DOI 10.1145/512950.512973): sound overapproximation/fixpoint framework, not a proof-cost theorem. D'Silva--Haller--Kroening, *Abstract Satisfaction* (POPL 2014, DOI 10.1145/2535838.2535868): lattice-based SAT/SMT semantics; not every possible SAT algorithm. Giacobazzi--Ranzato--Scozzari, *Making Abstract Interpretations Complete* (JACM 2000, DOI 10.1145/333979.333989): pointwise/fixpoint completeness and refinements; does not automatically supply a cheap concrete checker. CEGAR (Clarke et al., JACM 2003) and cost-partitioned planning (Keller et al., IJCAI 2016; Pommerening et al., ICAPS 2017) are relevant architectures, not ready-made same-R lower bounds. Atserias--Dalmau (JCSS 2008) characterizes **Resolution** width via existential pebble games, not the full mixed system.

**Established family ledger.** For connected bridgeless cubic expander graphs with h vertices, the standard odd-charge Tseitin CNF has n=3h/2 edge variables, m=4h signed strict 3-clauses, and binary indexed input length O(h log h). Source equation at v is XOR of its three incident edge bits equal to charge(v). Urquhart (JACM 1987, DOI 10.1145/7531.8928) gives exponential ordinary shared-DAG Resolution length for qualifying expander constructions, corroborated by Ben-Sasson--Wigderson (JACM 2001, DOI 10.1145/375827.375835) width-size methods. That scoped lower bound **does not** transfer to all /341 mixed rules. The known declared /341 GF(2) shortcut uses exactly 3h AND3 and h-1 XOR nodes, for 4h-1, and is retained as an upper-bound control. The present theorem concerns only its local clauses, not an unconditional proof-hardness transport.

## ITERATE: all-facet affine threshold (symbolic proof)

Fix k>=2 original Boolean variables x_1,...,x_k, charge c in {0,1}, and let T_c be the 2^(k-1) assignments with parity c. For every forbidden tuple a outside T_c, let C_a be the signed width-k clause falsified **only** by a. Define F_S=AND_{a in S} C_a for S a subset of the forbidden tuples, with model set M_S.

**Theorem 537.1 (PROVED/RESTRICTED, exact local result).**

$$
\operatorname{Aff}_{\mathbb F_2}(M_S)=
\begin{cases}
\mathbb F_2^k,&S\subsetneq(\{0,1\}^k\setminus T_c),\\
T_c,&S=\{0,1\}^k\setminus T_c.
\end{cases}
$$

**Proof.** If even one forbidden tuple is omitted, at least 2^(k-1)+1 Boolean assignments remain. Every proper affine subspace of F_2^k has cardinality at most 2^(k-1); hence the affine hull must be the entire space. If all forbidden tuples are excluded, exactly T_c remains, which is itself an affine hyperplane. QED.

**Corollary 537.2, affine-only meet is incomplete.** Every single proper width-k clause with k>=2 has full affine hull. Therefore the strategy "compute Aff(Mod(C_i)) individually and combine using only affine-space intersection" returns TOP for *every* proper strict 3-CNF, even when that formula is an established odd Tseitin UNSAT source. This demonstrates absence of precision in one abstract domain, **not absence of a concrete cheap proof and not an algorithmic lower bound**. In particular,

$$
\operatorname{Aff}(A\cap B)\ne\operatorname{Aff}(A)\cap\operatorname{Aff}(B)
$$

in general; affine closure does not commute with conjunction.

**Theorem 537.3, paid local factor transformer.** In the declared *bounded three-original-variable AND3 fragment* (not yet the authenticated full byte grammar), keep the exact 8-bit truth table for a source-local factor and an original-source label set P. A valid paid binary AND3 step forms (table(A) AND table(B), P_A union P_B) and pays one newly identified node. A GF(2) annotation is permitted only when the resulting truth table is *globally exactly* an affine equation, verified over all eight assignments. If a rule has extra context/interface dependencies, they must be recorded or conservatively overapproximated. This transformer is exact for the declared AND3 step: concrete truth-function intersection agrees bit-for-bit; ancestry union does not delete a source; the new paid-node identity appears exactly once. Reuse of a cached node is zero additional logical work but must reference its original identity. The two-premise AND3 tree over the four genuine parity source facets uses three nodes and derives the row; any strict facet subset still has full affine hull, so an annotated nonzero parity row on that subset would be invalid.

This is **not** a proof that a full /341 refutation requires three nodes per vertex, since other native rules, auxiliaries and shared cross-vertex proofs may exist. The prior /341 global m-1 bound and upper-bound construction remain separate results.

**CEGAR control.** A purported one-facet-to-XOR-row shortcut is spurious: at least one model of that single source clause falsifies the proposed parity row. Refinement from an affine-only domain to (three-variable truth-table, source provenance, paid-node identity, context) rejects it by exact truth-table replay. A full-calculus CEGAR would also need native RES/LOCAL-CONVERT/DEF/branch interfaces; the present checker deliberately does **not** pretend to supply those.

## Executed independent verification and resource ledger

Published **JavaScript** experiment: experiments/arc/lspv3_537_affine_facet_threshold.cjs (blob 7de78fc0b028919a830f69a16b7e71c0f48febe1); fetched verbatim from GitHub and executed again in a separate V8 context. Independently authored **Python** implementation executed locally; saved in this run's durable reproduction package with its raw output.

Both implementations exhaustively tested ALL clause-facet subsets for k=2,3,4,5 and both parities: respectively 8, 32, 512, 131072 cases, **131,624 subset/charge cases total**. Exactly two full-facet cases per width had affine dimension k-1; every proper subset had dimension k. The JavaScript verifier performed 132,996 assertion events, checked two four-source, three-AND3 certificates, and rejected six corrupt parent/ID/annotation cases. The Python verifier performed 135,054 assertion events, rejected 14 altered local certificate controls, and verified 64 truth assignments on both odd-charge UNSAT and even-charge SAT K4 originals (odd 0 models, even 8 models). The locally measured Python execution took 15.803 seconds and reported peak process RSS 96,012 KiB. These are host measurements, not native machine asymptotics or official historical checker execution.

**Coverage exclusions:** no official historical /341 checker execution, no accepted-byte test for RES-parent AND3 or DEF, no authenticated branching/discharge, no arbitrary identifier/auxiliary bit lengths in the finite local optimizer, and no general malformed DIMACS corpus beyond the independently declared typed-source controls. Exhaustion is parameter-bounded (k<=5); the theorem for all k>=2 is symbolic. k>3 is a mathematical extension, **not** an enlargement of /341's AND3 rule. K4 is a small SAT/UNSAT control, not a certified hard expander instance.

**Work versus time/span/evidence.** The exhibited three-parent-conjunction tree has three distinct paid nodes, four source records, six paid premise references, and depth 2 under free unlimited parallelism. No source clause is logically charged. Signed k-facet encoding uses O(k 2^k) literal bits plus IDs; a single local three-variable truth table uses 8 bits, plus support masks/IDs/context and paid node metadata. The exhaustive Python optimizer stores each current <=2^k point set and recomputes the GF(2) basis, and its enumeration cost grows doubly exponentially in k; this cost is **not** the proof cost. Discovery, original-source acquisition, validation, serialization, reference lookup, failed controls, cache maintenance, actual time and peak space are separate ledger entries. The unrestricted /341 minimum excludes discovery cost by design.

No component cost bound was added to the source-partition bound; doing so would risk double-charging the same AND3 nodes. A future cost-partitioned reduced product must prove sum_i c_i(e)<=w(e) for every native step, including zero-cost reuse.

## Status, publication, and precise next implication

**Actual advance:** Theorem 537.1 identifies an all-facets-or-nothing GF(2) information threshold for exact parity CNFs, and Theorem 537.3 supplies a locally exact AND3 factor/provenance/paid-history transformer. This is a **different** result from /536's source-component counting, /463's OR-branch join polarity, /462's paid-history erasure and /437's whole-model affine nonidentifiability.

**Verification:** symbolic proof plus two independent exhaustive implementations; GitHub JavaScript source exact readback and separate V8 execution. Report/code/raw/handoff publication status and tracker/main/issue reconciliation are recorded in a follow-up handoff if writes succeed; do not treat a pending write as done.

**Exact remaining gap:** authenticate complete historical [P2-D1], develop cost-sound inclusion for every RES/AND3/XOR/LOCAL-CONVERT/DEF/facet/branch transition in a whole shared-DAG reduced product [P2-C3], then find a noncircular **superpolynomial** invariant [P2-B1] and independent same-R decider-to-proof B3 [P2-B2]. Neither Route A nor the unrestricted P versus NP problem is resolved.

P versus NP remains OPEN.
