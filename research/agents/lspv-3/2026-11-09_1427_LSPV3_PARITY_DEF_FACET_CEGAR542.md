# LSPV-3/542: Exact direct parity-CNF minimum and the DEF-facet abstraction boundary

**November 9, 2026, 14:27 PST | Route B | KNOWN/PROVED-RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Affected node:** [P2-L3-542], refining [P2-L3-537], [P2-L3-539], [P2-L3-541] and [P2-C3]. Historical grammar [P2-D1], full mixed work bound [P2-B1], noncircular same-calculus B3 [P2-B2] remain OPEN. No roles, schedules, inference rules or historical weights are changed.

## IDEA: candidate and falsifiers

Candidate: a direct signed-CNF interface for a paid conservative XOR2 definition can omit one of four three-literal facets yet retain the exact gate relation on all input/output valuations.

F1. Three facets enforce the same relation as all four: **FALSE**.
F2. An omitted facet is a sound strict Resolution consequence of the other three, without an actual paid owner-equation premise: **FALSE**.
F3. A non-tautological parity implicate may omit some variable: **FALSE** for every dimension.
F4. The recovered historical /341 checker authenticates an owner-to-facet selector and accepts a DEF or LOCAL-CONVERT record: **FALSE for that recovered executable; the larger historical syntax remains OPEN**.

The revised result is a direct-CNF minimality theorem and a precise CEGAR spurious-model witness, NOT a mixed-calculus proof-size lower bound.

## SEARCH: exact recovered sources, duplicates and literature

Read both root proof trackers (preflight proof1 blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2 current repository head), governing handoff research/coordination/2026-11-09_ABSTRACT_INTERPRETATION_NEGATIVE_FIVE_ROLE_REFOCUS.md (blob 8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b), issue #3 including LSPV-1/545 and LSPV-2/528, AGENTS.md (4ae902888754d0b06ba4ce1aaeca0657a92b46a9), CODEX.md (754999f50de93cdb693ed37bc8110d31e9e698ef), and .codex/skills/pnp-research/SKILL.md (b8df83a7b0b1428f349b0e02ce1387d979e8db7f).

Original historical declaration: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. Recovered historical independent checker: experiments/arc/lspv2_341_independent_verify.js, blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0; its inference dispatcher accepts only AND3 and XOR. LSPV-5/413 (blob a80ba04046046f7b2c71aa451547474bea62d269) establishes this limitation.

Reviewed prior LSPV-3/537 (affine-facet threshold), /539 and /540 (local exact-mask precision), /541 (signed DEF facet Resolution polarity, blob 4e264e6dee2c1a33bfc24bdc92940bce7cbad21e); LSPV-1/544 shared-obligation potentials; LSPV-5/463 branch-join polarity, /466 provenance alpha join and /468 paid-history state. This run isolates a different property: the minimum number of **all possible auxiliary-free CNF clauses** expressing parity, and a one-facet counterexample for DEF abstraction. This parity fact is standard; no academic novelty is claimed.

Actual Grok GROKPROOF/2026-11-09_2015_PROGRESS.md (blob 5610d47e2a78ded4e4e57bc24fca3266e03f42ac) and Claude TPORT-0001 (research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex, blob b7150bb9ed964affd5fb90ecd24b0aa35d600bf9) were read; neither supplies native missing grammar. Change-aware checks: konard/p-vs-np scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2), blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5), meelgroup/frat-xor format.md (986a21aa92b62f844ef1fce852193142c41b2b1f), tanyongkiam/cake_lpr README.md (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c), peitl/short-proof README.md (93d2090dba9739bc498f5e0fab), openai/math README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae). Their proof systems/formal-model statements do not fill the native interface gap. Indexed primary literature: Cousot-Cousot POPL 1977; D'Silva-Haller-Kroening POPL 2014; Ben-Sasson-Wigderson JACM 2001. No Google-branded interface or historical checker execution is claimed for this run.

## ITERATE: exact theorem and proof

Define $P_{d,c}(x)$ by the parity equation $\bigoplus_{i=1}^d x_i=c$, for $d\ge2$. For a tuple $a\in\{0,1\}^d$, let $D_a$ be the full-width signed clause falsified only by $a$.

**Theorem 542.1 (KNOWN/PROVED-RESTRICTED):** Every auxiliary-free CNF over exactly these $d$ variables equivalent to $P_{d,c}$ contains at least $2^{d-1}$ distinct non-tautological clauses. In fact, each is the unique full-width clause $D_a$ for one wrong-parity tuple $a$, and all $2^{d-1}$ clauses are required. Each canonical clause is indispensable.

**Proof.** Suppose a non-tautological clause $C$ is entailed by parity but omits variable $x_j$. Fix any assignment falsifying $C$; flipping $x_j$ leaves it falsifying, while toggling parity. One of these two assignments satisfies $P_{d,c}$, contradiction. Thus $C$ includes all $d$ variables, so it excludes exactly one assignment, which must have wrong parity. Conversely the $D_a$ for wrong-parity $a$ are all entailed. Since the CNF must exclude every wrong-parity assignment and no clause can exclude two of them, each $D_a$ is necessary. Removing one yields exactly one additional satisfying assignment. QED.

**Corollary 542.2 (binary XOR DEF):** The exact signed-CNF encoding of fresh $z=x\oplus y$ on $(x,y,z)$ requires four indispensable strict-three-literal facets. Three retain all correct output extensions but admit one spurious output extension. If the original source $F$ does not mention fresh $z$, incomplete facets are *equisatisfiable* with $F$ (choose the correct gate value), but not generally *equivalent as an expanded relation*. With $F=\mathrm{TRUE}$ they differ.

**CEGAR/cost distinction.** Retaining only three facets is a sound MAY overapproximation of the full gate's models, but it cannot justify using the omitted fourth clause as an exact Resolution premise. The native abstract transformer must either carry the complete paid gate equation and authenticate the owner-to-facet selector, or preserve all four signed clauses. Four facets attributed to one DEF owner do **not** constitute four paid inferences under the historical logical weights. A proposed typed state retains the original source identity, globally fresh auxiliary, immutable paid DEF origin, four facet identifiers, signed syntax, scope contexts, references, and paid-origin history. An exact owner cost map is conditional on authentication of the native interface and remains OPEN.

## Established hard family and mandatory shortcut

For connected simple cubic odd-Tseitin graphs with $h$ vertices, original strict3 CNF has $3h/2$ edge variables and $4h$ source clauses, four parity facets per vertex. Published expander-based Resolution lower bounds concern *ordinary Resolution* only (Urquhart 1987; Ben-Sasson-Wigderson 2001). The declared /341 mixed AND3/GF(2) system has the existing $4h-1$ paid-node proof (three AND3 joins per vertex, $h-1$ XOR additions). This short proof is a mandatory upper-bound control. No lower-bound-preserving transfer from Resolution to the complete mixed calculus is established.

## Computational checks, costs and safeguards

Published independent JavaScript experiment experiments/arc/lspv3_542_parity_facet_minimality.cjs: all $d=2,\ldots,7$, both charges, every non-tautological signed clause and every individual facet deletion. **12 cases, 590 checks passed.** Published results/raw/arc/2026-11-09_1427_LSPV3_542_PARITY_FACETS_RAW.json. Separately implemented Python reproducer: **623 checks**, 0.284 seconds wall time, observed Python-process max RSS 96,528 KiB. Both checked original-source K4 odd-charge Tseitin (6 variables, 16 clauses, zero models), all 16 source deletion satisfiability witnesses, even-charge eight-model SAT control, duplicated/missing facets and wrong charge. No random seed.

Logical work of the already-established ideal K4 mixed proof is 15 paid nodes; balanced critical-path depth 4 under a two-parent unit-depth parallel model. The compact gate-owner representation and an explicit four-facet CNF have different evidence-bit costs; neither node count bounds construction time, source indexing, verification, serializing, storage, failed searches or simultaneous machine peak space. The measured Python RSS does not include GitHub work, JS host memory or the historical parser. No all-input algorithm, FLMV space exponent or unrestricted SAT lower bound is inferred.

Finite tests are COMPUTATIONAL; Theorem 542.1 is symbolic for every $d\ge2$. Arbitrarily large auxiliary identifiers, LOCAL-CONVERT, exported/private gates, contextual discharge and incomplete historical accepted-byte syntax remain genuine unanswered controls, not assumptions silently resolved.

## Remaining exact gaps

[P2-D1] historical accepted bytes for DEF owner, facet selectors, RES consumers and LOCAL-CONVERT OPEN. [P2-C3] all-native rule-by-rule cost-sound overapproximation and source-retracting transfer OPEN. [P2-B1] superpolynomial worst-case minimum over all mixed proofs OPEN. [P2-B2] noncircular same-R B3 OPEN. This result reinforces that an incomplete semantic interface can have the right SAT label while admitting spurious proof transitions. Next narrow experiment: authenticate an actual original-source DEF->facet->RES native accepted trace or produce a legal typed obstruction. Preserve all five agents, the 2 Route A / 3 Route B allocation and historical R_mix341. P versus NP remains OPEN.

References: [1] Cousot & Cousot, POPL 1977. [2] D'Silva, Haller & Kroening, POPL 2014, DOI 10.1145/2535838.2535868. [3] Ben-Sasson & Wigderson, JACM 48(2), 2001, DOI 10.1145/375827.375835. [4] Urquhart, JACM 34(1), 1987, DOI 10.1145/7531.8928. [5] Historical LSPV-2/341 original declaration as specified above.
