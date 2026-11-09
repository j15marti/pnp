# LSPV-3/538: exact ceiling of the source-partition-only cost abstraction

**2026-11-09 10:25 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**Proof-chain IDs:** proposed [P2-L3-538], prior [P2-L3-536] and [P2-L3-537], red-team [P2-L5-464], and unchanged OPEN [P2-D1], [P2-C3], [P2-B1], [P2-B2]. Unchanged [P1-01]/[P1-03]/[P1-04].

## IDEA and four precommitted falsifiers

Candidate: the coarsest binary-source partition abstraction used in the /536 cost argument has *exact* abstract goal distance m-1 on any m essential-source problem, independent of its actual clause semantics. Thus it cannot establish superlinear work; the intended CEGAR repair must add information constraining legal merges, not repeatedly recompute the same partition potential.

F1: a native legal step merges >2 source components at unit cost, or free steps join components (historical full-grammar blocker); F2: a partition-only abstract path can reach a single component in <m-1 charged merges; F3: arbitrary pair merges fail to make a length-(m-1) path in the specifically defined may system; F4: a claimed concrete replay of the constructed path finds every merge legal under actual native rules. F2 and F3 are disposed of symbolically, while F4 is falsified immediately in the published PHP controls. F1 prevents promoting the scoped abstraction to the historical full mixed calculus.

## SEARCH and priority source ledger

Read **both complete** root trackers (startup proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; proof2.txt startup blob 1d73b3c3ada2bcb044b13d70dd9487222640acb8), the 2026-11-09 abstract-interpretation refocus (blob 8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b), issue #3 (latest read included LSPV-1/540 and LSPV-5/464), AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md. Read exact historical *semantic declaration* research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb); prior /536, /537, LSPV-5/463, /464, LSPV-1/539; GROKPROOF/2026-11-09_1230_PROGRESS.md; Claude world-ledger source identified in root tracker. Do not treat the declared semantic list as an authenticated accepted-byte parser.

Targeted GitHub rechecks: konard/p-vs-np scripts/proof_status.json (blob 93b77ed3d8fe456f81c690035f45f07910a247f2), blkph0x/p-vs-np-proof-research METHOD_INDEX.md (blob 18d693ea71dfa433370eb7afbebc3106e32f03e5); meelgroup/frat-xor format.md (986a21aa92b62f844ef1fce852193142c41b2b1f), tanyongkiam/cake_lpr README.md (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c), MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd198fc4a698a5a207f67b36a9591b2a3bab), openai/math README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae). None supplies native historical R_mix341 authentication.

Primary literature: Haken 1985, *The Intractability of Resolution*, TCS 39:297-308 (ordinary Resolution PHP exponential). Urquhart 1987, *Hard Examples for Resolution*, JACM 34:209-219 (qualifying expander Tseitin). Cook 1976's ER PHP upper bound and modern independently described ER speedup (Sonobe 2022, DOI 10.3390/a15120479) are mandatory controls. Atserias--Dalmau 2008 (DOI 10.1016/j.jcss.2007.06.025) applies width games to **Resolution**; Giacobazzi--Ranzato--Scozzari 2000 (DOI 10.1145/333979.333989) concerns abstract completeness; cost-partitioned planning (Pommerening et al., ICAPS 2017, DOI 10.1609/icaps.v27i1.13806) gives a methodology, not a same-R lower bound. D'Silva--Haller--Kroening abstract conflict-driven learning is a related SAT abstraction method, not automatic proof-work hardness. Separate Google-branded search unavailable; general web search used.

## Theorem 538.1: exact partition-only abstraction distance (PROVED/RESTRICTED)

Fix m>=1 distinct essential original-source identities. Define the **particular coarse MAY relaxation** A_m to retain only a partition pi of these m sources. Initially pi is discrete. An abstract charged binary merge may replace *any* two blocks by their union, at cost one; include paid non-merging self-steps if needed to cover concrete legal inferences and zero-cost references as stutters. The abstract goal is any one-block partition, deliberately dropping the semantic empty-clause requirement. Then:

$$
d_{A_m}(\pi_0,\mathrm{Goal})=m-1.
$$

Proof: every merge lowers block count by exactly one, hence at least m-1 are necessary. Conversely, sequentially merge block 1 with blocks 2,...,m, which is a valid abstract MAY path with exactly m-1 merges. This is a **relaxation**: those pair joins need not correspond to any genuine inference. Any sound lower bound obtained solely from this goal-distance abstraction is therefore at most linear in number of sources. It cannot distinguish a published Resolution-hard family from an easy one having the same m. This extends /536's one-sided source-component invariant by proving the **matching abstract upper bound for this particular domain**, not a new concrete lower bound.

**Soundness qualification:** Under /536's exhaustive two-parent and no-free-cross-merge restrictions, every concrete step has a same-or-less-expensive abstract image: charge one for a real binary merge, stutter for a non-merge, reuse at zero. Every concrete completed refutation on an m-clause minimally UNSAT source maps to one block. Consequently d_A <= W_R, but only for such an authenticated rule subset; unknown LOCAL-CONVERT side reads, DEF facets, branching/discharge and any free multi-source joins must be conservatively admitted, potentially yielding an even smaller abstract minimum.

## Established hard-family controls and encoding

**Haken PHP:** standard unary PHP from n+1 pigeons to n holes has n(n+1) variables, m=(n+1)+n*binom(n+1,2)=Theta(n^3) source clauses, one at-least-one width-n clause per pigeon and one binary exclusion for every pigeon pair/hole. Each source clause is individually essential (deletion admits an explicit matching or one collision). Haken gives an exponential ordinary shared Resolution proof-size bound for the standard encoding, while A_m gives m-1. This PHP is **not claimed to be strict 3-CNF** for n>3; no reduction lower-bound transfer is asserted. Cook ER is a stronger-system polynomial-proof shortcut. For n=2,3, replay original PHP clauses exactly, no bespoke source family.

**Urquhart cubic Tseitin:** a suitable odd-charge cubic expander has h vertices, 3h/2 original edge variables, 4h strict 3-CNF parity-facet clauses and O(h log h) indexed source bits. Ordinary DAG Resolution is exponentially hard on qualifying graphs; declared AND3/GF(2) proof already has 4h-1 paid nodes. Therefore the Resolution lower bound cannot be transferred into the full mixed calculus. A_m gives 4h-1 on these essential sources, matching the declared shortcut, and cannot reveal more.

## Finite CEGAR counterexample (COMPUTATIONAL)

For PHP_3^2 (three pigeons/two holes) m=9 and A_9 reaches its artificial connected goal in 8 abstract merges; for PHP_4^3 m=22 and A_22 reaches it in 21 merges. The *first* proposed source pair is two different positive pigeon-at-least-one clauses: they share **no complementary Resolution pivot**, and their union has >3 distinct original variables, so that particular two-parent merge is not native RES or declared AND3. A typed CEGAR refinement can ban this proposed RES-specific transition, provided all other legal rule types are retained. The exhibited abstract path is spurious; this does **not** show the actual minimum proof sizes for those instances.

The finite Python generator independently enumerated all 64 and 4096 Boolean assignments (both sources UNSAT), checked all 9 and 22 clause-deletion SAT witnesses and paid partition counts, PASS, 0.006884 s wall, observed host peak maxrss 95768 KiB (includes process/container baseline, not intrinsic algorithm memory). Independently authored Node.js verifier reconstructed all clauses and passed 139 assertions, including three corrupted source/cost/deletion-witness controls for each n. This is not an authoritative historical R_mix341 execution.

## New precision requirement and exact remaining gap

A source partition by itself cannot yield superlinear work. The next abstraction must retain a **legal-merge feasibility component**: exact source-authenticated clause/affine/factor conclusions, premise hyperedges, contexts, DEF facets and fresh-port/interface semantics, all at native paid-node costs. Its rule-by-rule may inclusion must hold even with sharing, reconvergence, high-width rows, zero-cost closures, large IDs and abstract auxiliary renaming. CEGAR can remove a spurious typed RES join only after an exact rule-specific non-applicability proof. It must not assume all other rules are illegal.

No tracked B1/B2/B3 proposition is promoted. [P2-D1] full native grammar remains OPEN; [P2-C3] all-rule source/cost-sound transformer remains OPEN; [P2-B1] superpolynomial minimum work remains OPEN; [P2-B2] noncircular same-R B3 remains OPEN. Route A universal same-machine FLMV transfer is independent and OPEN. Historical weights, five roles, 2 Route A/3 Route B remain untouched. P versus NP remains OPEN.


## Verification addendum: complete witness publication

The compact result summary is published at \`results/raw/arc/2026-11-09_1025_LSPV3_538_PARTITION_CEILING_RAW.json\` (blob \`b3aade9e8b335481fa654b506b23fb9bb197ac60\`). The **complete 20,374-byte witness record** needed by the second verifier, including every signed source, all 31 source-deletion witnesses and each abstract merge, is at \`results/raw/arc/2026-11-09_1025_LSPV3_538_FULL_WITNESS_RAW.json\` (blob \`24e805964999c8ce59b312e17d1207ce887fc083\`). The independent verifier is at \`experiments/arc/verify_lspv3_538_partition_ceiling_independent.cjs\` (blob \`1f6eee32661d1ceea3965742a974dbb3e41ddf61\`). It was independently executed against the published full witness record in V8: **PASS, 139 checks**. The separately published concise generator \`experiments/arc/lspv3_538_partition_ceiling.mjs\` was fetched and independently replayed in V8: **PASS, 78 checks**. The local Python generator and independent Node.js checker, plus the full JSON, were run in the working container; none is the authoritative historical checker.

**Final publication and remaining gap.** All role-owned report/code/raw/handoff files, full tracker/outbox and main.tex owned-only reconciliation were read back exactly; issue #3 posted and verified. Historical grammar [P2-D1], complete all-rule transformer [P2-C3], superpolynomial all-rule mixed minimum [P2-B1], and noncircular same-R B3 [P2-B2] remain OPEN. P versus NP remains OPEN.
