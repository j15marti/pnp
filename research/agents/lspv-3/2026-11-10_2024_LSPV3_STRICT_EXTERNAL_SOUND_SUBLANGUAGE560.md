# LSPV-3/560: Sound externally bound typed fragment of recovered native /341 checker

**November 10, 2026, 20:24 PST | LSPV-3 Hypergraph & Proof Certificates | Historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## IDEA and falsifiers

**Candidate [P2-D1]:** Although the recovered original /341 checker is not sound for arbitrary decoded packets, a separate, explicitly source-bound and strictly typed sublanguage of its actual SOURCE/AND3/XOR fragment is sound against SAT-source forgeries. This repairs an *explicitly different trusted-language predicate*, not the unrecovered full historical R_mix341 grammar.

Falsifiers declared before searching: (F1) any of seven original native fixtures fails the typed guard; (F2) the LSPV-3/557 accepted SAT-source forgery passes it; (F3) string charges, non-array supports, aliased IDs, changed externally bound literals or ghost affine coordinates evade it; (F4) a verified native AND3/XOR step within the typed sublanguage is nevertheless semantically unsound. The first three are executable controls and F4 is addressed symbolically.

## Sources, duplication control and scope

Read both root proof trackers, issue #3 and current coordination comments, AGENTS.md, CODEX.md, repository pnp-research skill, historical original declaration, original producer and checker, LSPV-3/542, /551, /557, /558, /559, LSPV-1/561-562, LSPV-2/546, Grok progress and the relevant five-role handoff. The historical declaration at research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex has blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. The *unchanged* original producer and checker are respectively blob 4081022e8a3841d79f751a3d3a7a10decbb026da and blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. Main's full recursive Git tree contained 16,097 entries; only the original /341 producer/checker and byte-identical archival copies in the reviewed paths supplied historical executable authority. A complete five-rule historical parser was not found; another branch or archive might contain one.

Change-aware sources reviewed: konard/p-vs-np README blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95; blkph0x/p-vs-np-proof-research README blob f397a7747eaca82df3d754d0a4b4bab1fe10f814; GROKPROOF/2026-11-10_0415_PROGRESS.md blob 7905ee4ff3ac9018d3650a45250fccd1f0768f47. The first two distinguish restricted models/promise algorithms from unrestricted P vs NP; none supplies the missing parser. Primary literature: Cook-Reckhow (1979), Cousot-Cousot (1977), D'Silva-Haller-Kroening (2014).

LSPV-3/554 already proved unqualified original-checker acceptance unsound; LSPV-3/558 built one canonical proof for externally signed cubic-parity sources; LSPV-3/559 proved the recovered checker has only AND3/XOR dispatch. Here the quantifier is over *every accepted strictly typed and externally source-bound packet*, not only one constructor's outputs. This is a new restricted language boundary, not historical byte-grammar authentication.

## Theorem 560.1 (PROVED/RESTRICTED)

Fix the original /341 fixture checker V and a separately supplied ordered list F of signed 3-CNF clauses. Define L_T(F) to include only parsed fixture objects satisfying ALL these additional conditions:

1. All graph endpoints, charges, signed source literals, clause vertex/pattern, support indices, truth tables, and affine RHS values are type-checked exact safe integers with stated ranges. In particular charges and row RHS values are *numeric* 0 or 1, not coercible JSON strings, and support is an array of distinct numeric coordinates.
2. Source clauses equal the separately supplied signed F element by element. Source identifiers are unique canonical strings s0,s1,...; paid IDs are globally fresh canonical strings d0,d1,...; all parent IDs have these canonical forms.
3. The only paid fragment opcodes are AND3 and XOR. Each AND3 factor has at most three typed coordinates and an exact eight-bit truth table; every present affine row has a canonical nonnegative hex mask with no high bits outside E original coordinates and numeric Boolean RHS; XOR outputs always have rows.
4. The original checker still performs its full checks of cubic graph, local source patterns, chronological parent existence, actual conjunction truth tables, exact affine aliases and sums, deletion controls, ancestry, proof length and final row mask zero/RHS one.

For *every* finite separately supplied signed source F and parsed P,

$$
\left(P\in L_T(F)\ \land\ V(P)=\mathrm{accept}\right)
\quad\Longrightarrow\quad F\in\mathrm{UNSAT}.
$$

**Rule-by-rule proof.** Every source factor is the clause's truth function on the exact signed external literals. Assume all earlier factors/rows are implied by F. The original verifier computes every AND3 output truth table by exhaustive conjunction of its two existing parents on the union support. Since the typed output support is an exact duplicate-free numeric coordinate set, the local check is globally faithful. An optionally annotated GF(2) row is checked on every support assignment; with an E-bounded row mask and verified variable support, this local equivalence extends to all E-dimensional assignments. Each XOR inference verifies exactly the GF(2) sum of two earlier implied equations. Thus every paid step remains entailed by F. Fresh IDs and chronological existing-parent references establish a well-founded shared-DAG induction. The final row is 0=1 and cannot be satisfied. Therefore F has no model. QED.

The theorem is for the **decoded** typed sublanguage, not raw JSON byte identity, SHA authentication or duplicate-key lexical uniqueness, and it does not declare every originally accepted packet legal. In particular, excluding malformed but originally accepted packets is *not* a cost-sound overapproximation of that unsound acceptance language. The trusted goal predicate has been replaced by semantic source-certified acceptance; missing historical rules remain unknown.

## Typed fragment alpha/gamma and cost

For this fragment alone, concrete configurations retain signed external source, exact source and paid IDs, immutable paid occurrence identities, chronological parent DAG, factor support/tables and affine rows. The abstraction alpha preserves these data but interprets each factor as its exact Boolean function on its typed support and each affine row as its exact pair (mask,RHS). Gamma contains the typed configurations with exactly those retained semantics and identifiers. Each native AND3 or XOR transition maps to exact abstract truth-table conjunction or row sum, preserving goal reachability and concrete-step inclusion. New paid occurrences have abstract cost one; references to already paid nodes have cost zero, with their owner paid once. Therefore on this restricted grammar

$$
w^\#(\alpha(C),\alpha(C')) \le w(C,C')
$$

with equality for every new AND3/XOR occurrence. This is a restricted abstract-simulation lemma, **not a complete CEGAR or negative certificate for historical R_mix341**. No free branching/discharge or unverified conversion is introduced.

Certificate logical work q is distinct from bytes B, parsing, construction/search, verification time, parallel span and machine peak writable space. The separately bound source and proof both require actual reading. No RAM/FLMV physical space bound or unrestricted SAT lower bound follows.

## Exact executed controls and publication

New runnable guard/test program: experiments/arc/lspv3_560_typed_native_fragment_firewall.cjs, blob 2b122d7cec3ff7b62e1202622f8c22fd6ff79422. The exact original producer and checker source bodies ran in V8 with only fs/vm I/O adapters, without changes to the original mathematical verification code. The original seven-fixture baseline passed 30,714 original checks. All seven original typed graph fixtures passed the new guard; seven independently modified packets were rejected for string charge, string support, numeric ID, external source mismatch, noncanonical row syntax, ghost coordinate and unsupported RES rule. The original checker still accepted a string-charge mutation (30,714 checks) and correctly rejected a RES opcode as unknown. These are 16 additional audit controls, not 30,714 newly devised tests.

Separately, the exact previously published LSPV-3/557 **satisfiable** source packet was accepted by the unchanged checker (3,273 assertions) with 47 purported paid nodes; witness 101001000000100000 satisfied all 48 original clauses. The new guard rejected its nonnumeric charge immediately. Independent numeric-charge alteration was also rejected because the packet's IDs are numeric rather than the new guard's required canonical strings. The trusted sublanguage therefore excludes this concrete false-positive without asserting a proof in the historical full calculus.

Published executable and raw evidence were each checked by complete Git content readback:
- results/raw/arc/2026-11-10_2024_LSPV3_560_TYPED_FRAGMENT_RAW.json, blob 777614f826940eea71992160c955d0e3a2e2c011.
- results/raw/arc/2026-11-10_2024_LSPV3_560_FALSIFIER_REPLAY_RAW.json, blob c8d2ddaee9c2233df3a429a932181d26832ea45b.

The published full Node program was executed as its precise JS body inside connected V8, not as a separate OS Node subprocess. This distinction is retained for independent reproduction.

## Gaps and next target

[P2-D1] **OPEN**: authoritative accepted-byte syntax still missing for Resolution, LOCAL-CONVERT, DEF owner/facets, exported/private interfaces, branching and discharge. [P2-C3] **OPEN**: all-rule cost-sound abstraction including every legal shortcut missing. [P2-B1] **OPEN**: no superpolynomial full-calculus proof minimum established. [P2-B2]/B3 **OPEN**: no noncircular transfer from SAT in P to polynomial minimum work for this SAME calculus. P1-01, P1-03, P1-04 and P versus NP remain OPEN.

**Next decisive target:** find the actual original mixed five-rule parser or a source-authenticated, historically accepted paid DEF owner with facet-to-RES consumer. An independently invented grammar, including this typed firewall, cannot close P2-D1.

## References

[1] Cook, S. A., and Reckhow, R. A. The Relative Efficiency of Propositional Proof Systems. Journal of Symbolic Logic 44 (1979), 36-50. DOI: 10.2307/2273702.

[2] Cousot, P., and Cousot, R. Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints. POPL (1977), 238-252. DOI: 10.1145/512950.512973.

[3] D'Silva, V., Haller, L., and Kroening, D. Abstract Satisfaction. POPL (2014). DOI: 10.1145/2535838.2535868.

[4] Original /341 project declaration, producer/checker, and LSPV-3/554, /557, /558, /559, with pinned blob SHAs above.
