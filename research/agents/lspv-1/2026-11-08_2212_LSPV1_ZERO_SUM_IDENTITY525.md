# LSPV-1/525: Verified source-authenticated zero-adder congruence packet

**November 8, 2026, 22:12 PST | Route B lead | PROVED/RESTRICTED in signed-AND2/Resolution ER2-OWNER, COMPUTATIONAL independently replayed. Historical R_mix341, B3 and P versus NP remain OPEN.**

**Proof-chain IDs:** NEW [P2-L1-525], refining [P2-L1-524], [P2-L3-523], [P2-L1-520], [P2-F6], [P2-C3]. Principal [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. No change to [P1-X1].

## IDEA: predictions and falsifiers stated before investigation

Hypothesis: the original-source and paid-definition zero certificate LSPV-1/524 can be extended into a source-authenticated proof of $0+A=A$ for **three arbitrary original-variable Boolean indicators** $A=(A_0,A_1,A_2)$, without any one-hot assumptions on $A$. The additional work should require 15 signed two-port Boolean definitions and at most 30 binary Resolution inferences.

Falsifiers: (F1) alpha-renaming previous auxiliary variables to reserve new original inputs changes a source or breaks Resolution pivots; (F2) repeated absolute gate input IDs, ownerless defining facets, or branch-local assumptions appear; (F3) any derived equality clause lacks an exact oriented-Resolution derivation or has a source-satisfying countermodel; (F4) a certificate for the declared ER2 calculus is mistakenly promoted to the historical R_mix341 checker.

**Iteration record:** An initial experiment checked output semantics but not every old pivot after alpha-renaming. The first independent verifier detected F1: old Resolution *pivot IDs* had not been renamed, even though their clauses had. That invalid attempt was **not published**. The correction consistently renames every old paid DEF wire, signed literal and RES pivot. The independent full proof verifier then passed. This is a substantive provenance repair, not merely additional finite numerical testing.

## SEARCH and provenance

Read both complete root trackers (initial Git blobs: proof1 `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, proof2 `26d237586463109ecec3247d3c337b5572ece584`; concurrent proof2 changes handled by fresh SHA-guarded final read). Read current coordination issue #3, governing five-role handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` blob `c3889a3e514ddbd747150dcb68607013a3b2d154`, `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`, `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, repo skill `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`, and frozen /341 definition `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`.

Reused LSPV-1/524 exact producer `experiments/arc/lspv1_524_strict3_inverse_cancellation.js` blob `3fa42e25e02d05b9a915458a7f780e59fd828c12`, independent LSPV-3/523 source-to-inverse port `research/agents/lspv-3/2026-11-08_2125_LSPV3_CORE_TO_INVERSE_ER2_PORT523.md` blob `d765f8634a6234276eeb1bc3423644ab79a05b65`, and the red-team /450 defining-facet ownership objections. Actual independent comparison sources inspected: `GROKPROOF/2026-11-08_0930_PROGRESS.md` blob `e3e8c9657e0f2b2e0751752135cf2558e28183cf`, and `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`; their scopes differ.

Primary literature checked by public web search: Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, revised 24 October 2026, Theorem 7.2(b), Corollary 7.3. Its exponential hard-family claim concerns fixed-r syntactic Res(PC_r/F2) on opposite-characteristic mod3 Tseitin over expander graphs, not historical R_mix341. Search queries `onehot zero identity adder resolution`, `zero plus onehot packet` and `congruence sum zero ER2` located relevant /449, /520 and /524 precedent; an identical 115-paid-node source/owner proof was not located, without a novelty claim.

Required repository review: `konard/p-vs-np/README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95`, `scripts/proof_status.json` `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research/README.md` `f397a7747eaca82df3d754d0a4b4bab1fe10f814`, `METHOD_INDEX.md` `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `meelgroup/frat-xor/format.md` `986a21aa92b62f844ef1fce852193142c41b2b1f`; `tanyongkiam/cake_lpr/README.md` `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; `openai/math/README.md` `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`. All have different trust, model or proof-system scopes and do not authenticate native mixed rules. Google-branded separate search was unavailable; public web search worked.

## ITERATE: native-style proof construction (separately specified ER2)

Retain the seven original signed proper width-3 clauses of /524 on $x_1,x_2,x_3,z$ (original IDs 1..4); declare three additional independent original port variables $A_0,A_1,A_2$ with IDs 5,6,7. These new variables are unconstrained by this **local** original source, as they would be independently constrained elsewhere in the full Tseitin formula. Alpha-rename the old charged aux IDs $j\ge5$ to $j+3$, consistently across gate ports, clause literals, and RES pivot IDs. The original SOURCE clauses and line indices remain unchanged; paid aux IDs become 8..26. The old signed zero literals are

$$
Z=(-22,-24,-26),\quad \vdash Z_0,\quad \vdash\neg Z_1,\quad\vdash\neg Z_2,
$$

with actual derived source-authenticated clause records (91,104,117), not an assumed zero oracle.

Introduce nine paid fresh signed-AND2 terms $t_{ij}=Z_i\wedge A_j$. For $i=1,2$, the negative units $\neg Z_i$ and exact owner facets derive the six units $\neg t_{ij}$. In each output bucket $k\in\mathbb F_3$, create two paid signed NOR gates representing $f_k=\neg(t_{0k}\vee t_{1,k-1}\vee t_{2,k-2})$, where subscripts are taken mod 3. Resolution with $Z_0$ and the defining back-facet derives $t_{0k}\vee\neg A_k$. Four more oriented RES steps and the off-term units derive $f_k\vee A_k$; two further RES steps derive $\neg f_k\vee\neg A_k$. Thus **both exact clauses** establish $-f_k=A_k$ for each $k$ without one-hot hypotheses on $A$.

The six exact output clauses are in records (161,163), (174,176), (187,189). The construction uses 15 new paid definitions, and 27 newly paid binary Resolution steps: six off-term-unit, three positive-term-lift, twelve NOR-positive, six NOR-negative. Total full certificate: **34 DEF + 81 RES = 115 paid distinct inference nodes**, 7 SOURCE clauses, 102 owner-qualified defining FACET records, **190 total records**. Critical-path RES depth is **13**, not a physical parallel machine time. Valid branches can share old zero deductions; a reused lemma is unconditional here, not leaked from a branch-local context. All six goals are actual inference nodes, not free semantic assertions.

**Independent execution:** A separately authored checker parsed/reconstructed every original source, signed DEF port/facet, owner metadata, acyclic oriented RES line and exact goal; independently checked **13,718 assertions**. Exhaustive evaluation of all 128 original-variable assignments found **48** source-satisfying and **80** source-rejected assignments; every source-satisfying assignment satisfies all six derived clauses and the bit identities. Six mutations of pivot, conclusion, facet owner, original source, gate-port uniqueness and goal list were rejected. The original failed pivot-renaming candidate was caught before publication and corrected.

## Family/theorem/shortcut/remaining-transfer ledger

Selected established family: one-hot mod3 Tseitin on cubic expanders with nonzero total charge. Original strict-3CNF source with LSPV-1/518 degree-preserving padding is size $N=\Theta(h\log h)$; Pang's 2026 preprint gives $\exp(\Omega_r(h))$ DAG-size lower bound **only** for fixed-r syntactic Res(PC_r/F2), assuming the cited PC-degree/expansion hypotheses. Known shortcuts include matching-characteristic Res(lin_F3), Cook extended Resolution, source-local mixed GF2 for odd binary Tseitin, paid Boolean gate and shared-DAG reasoning. The current module is an ER2 upper-control, not an all-rule lower-bound transfer and not a refutation of the full formula. Its seven padded original clauses are NOT the 21-clause unpadded CORE of LSPV-3/523: a charge-paid CORE-to-local substitution remains required for full source authentication.

**Open transfers:** [P2-D1] historical accepted-byte grammar and private/exported facet scopes; [P2-C3] full native system and global LCA cancellation/congruence composition; [P2-B1] superpolynomial worst-case minimum under ALL legal mixed rules; [P2-B2] noncircular SAT-in-P implies poly-bounded same-R proof minimum. No restricted certificate implies arbitrary algorithm hardness or B3.

## Complete resource and publication ledger

The abstract evidence has 115 distinct paid nodes, 190 records, 34 explicit definitions, 81 Resolution edges, 102 owned facet references. The raw proof is 39,992 UTF-8 characters; generator and independent verifier are 3,372 and 3,257 characters. Building, source/commit lookup, SHA-pinning, parsing, source validation, search/policy, raw serialization, failed candidate, six mutation tests, writing, readback and any cache/reference retrieval carry additional actual implementation work. No physical timing, all-phase simultaneous peak RSS, or FLMV same-machine exponent was measured or asserted. When scaling, actual ID bit widths, source bytes, index reads, outputs and retained/recomputed DAG nodes must be separately charged. Logical paid-work count is not a bound on all-input computation.

GitHub `main` artifacts (published/read back):
- `experiments/arc/lspv1_525_zero_sum.cjs`, blob `1d6334fa5712f374bd0455445cd1bb40ac6a2fe0`;
- `experiments/arc/verify_lspv1_525_zero_sum.cjs`, blob `573fdf3b3e98b6d804d54319e6e02ede2182d96d`;
- `results/raw/arc/2026-11-08_2211_LSPV1_ZERO_SUM525_RAW.json`, blob `e03314f7afe400871ab2c512d82f0b3815a76ea0`.

Root `main.tex` not edited: complete original was not available for byte-safe ownership region editing. Historical grammar, weights, role identities, exact five-agent allocation, schedules and enabled states not changed. Tracker and issue receipts are recorded separately. **P versus NP OPEN.**
