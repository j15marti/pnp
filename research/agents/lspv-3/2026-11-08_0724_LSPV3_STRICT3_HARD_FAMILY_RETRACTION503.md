# LSPV-3/503: Strict-3CNF hard-family retraction and exact mixed upper control

**November 8, 2026, 07:24 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Proof chain:** new scoped [P2-L3-503], refining [P2-D3], [P2-C3], and [P2-F13]. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. [P1-01], [P1-03], [P1-04] unchanged.

## IDEA: hypothesis and pre-search falsifiers

Hypothesis: a published Resolution-hard strict signed 3-CNF odd Tseitin family admits a focused three-clause strict3 source expansion that (i) provably preserves the old Resolution lower bound via an actual proof-backtranslation, (ii) preserves original-source authentication, and (iii) has an exact linear minimum in a separately declared, stronger mixed calculus.

1. The gadget may fail proper signed width-three syntax or exact SAT/UNSAT preservation.
2. One external clause may become dispensable, invalidating the binary-ancestry lower bound.
3. Equisatisfiability might not give a polynomial-size Resolution proof backtranslation; an explicit direction-preserving map must be constructed.
4. A RES-derived clause may be disallowed as an AND3 factor by historical R_mix341. Such an edge must not be relabeled historical.

## SEARCH: primary research and actual corpus

The baseline is the standard odd Tseitin contradiction on **connected bridgeless cubic graphs**, especially a published family of constant-degree expanders. For h vertices, it has 3h/2 edge variables and 4h proper signed width-three clauses; binary-index source length is Theta(h log h). Ben-Sasson and Wigderson, *Short Proofs are Narrow—Resolution Made Simple*, J. ACM 48(2) (2001), 149-169, https://doi.org/10.1145/375827.375835, relate proof width to DAG Resolution size. On expander Tseitin instances with the required width lower bound this yields 2^{Omega(h)} **ordinary DAG Resolution** hardness, not SAT-algorithm hardness. Haken PHP and Cook extended Resolution remain controls.

Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (October 24, 2026), https://arxiv.org/abs/2610.00837, supplies further **different-proof-system** hard families. Pang's one-hot encoding is NOT the signed-edge encoding used here. Braun arXiv:2609.23015 and FRAT-XOR (https://github.com/meelgroup/frat-xor/blob/main/format.md) are distinct algebraic and proof-format controls.

Read both complete root trackers, coordination issue #3, governing five-role handoff, actual LSPV-3/434, /497, /499, /502, LSPV-5/412 and /435, LSPV-1/505, LSPV-4/495, AGENTS.md blob 19656af102604d5f0a721d548cf2e4e72a063561, CODEX.md 754999f50de93cdb693ed37bc8110d31e9e698ef, project skill b8df83a7b0b1428f349b0e02ce1387d979e8db7f, actual GROKPROOF/2026-11-08_1130_PROGRESS.md blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70 and Claude world-ledger blob 79e4d4e7e0e3edff3aba8610852c45534bdde128. The original LSPV-2/341 checker is blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. Original balanced packet is blob 481423a2f5271ab600bbc2f9a526fe62523239a9. No source supplies the missing historical RES/DEF/LOCAL-CONVERT accepted-byte production.

Change-aware review: konard/p-vs-np/scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 (model-scoped P subset NP, not NP subset P); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 (restricted family/method research); meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f (explicit different XOR proof schema); tanyongkiam/cake_lpr/README.md blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c (Nov 1, 2026 checker-release boundary); GitHub openai/math repository available, no historical native grammar. GitHub code search and web literature search were executed. A separate native Google-branded client was not available. No external CI badge was treated as a proof of this claim.

## ITERATE: exact source gadget and certified directions

Fix any odd-charge signed cubic Tseitin source T(G,b). Choose **one** original three-literal clause

$$
C=\ell_1\lor\ell_2\lor\ell_3.
$$

Replace it with three proper signed width-three clauses over two globally fresh variables u,v:

$$
A=(\ell_1\lor\ell_2\lor u),\qquad
B=(\neg u\lor\ell_3\lor v),\qquad
D=(\neg u\lor\ell_3\lor\neg v).
$$

Write H(G,b,C) for the changed source. It has exactly **3h/2+2 variables and 4h+2 clauses**. Two source-authenticated, oriented ordinary Resolution inferences yield

$$
\operatorname{RES}_v(B,D)=(\neg u\lor\ell_3),\qquad
\operatorname{RES}_u(A,\neg u\lor\ell_3)=C.
$$

Both results are clauses with duplicate literals coalesced. Also B AND D is logically equivalent to (NOT u OR ell_3), so existential elimination of u,v recovers C. But that equisatisfiability does not prove hardness preservation.

### Theorem 503.1: actual Resolution proof backtranslation

Define a **literal substitution** sigma(u)=ell_3, sigma(v)=0, leaving original edge variables unchanged. The gadget A maps to original C, B and D map to tautologies, and every other original clause remains unchanged.

For ANY ordinary shared-DAG Resolution proof pi of H, process its inference nodes topologically. Each substituted clause is represented by a previously derived **subclause**, or is discarded when tautological. At a Resolution step, if both transformed parent representatives retain the substituted complementary pivot, resolve them once. If one has lost that pivot by subsumption, reuse that stronger parent because it is already a subclause of the substituted conclusion. If a parent became tautological, either the conclusion is tautological or the other parent subsumes it. For a pivot becoming a Boolean constant, use the standard restriction case. No step needs more than one new Resolution inference, and sharing persists. The final empty clause is unchanged.

This proves the **nonexpansive proof-size direction**

$$
S_{\rm Res}(T(G,b))\le S_{\rm Res}(H(G,b,C)).
$$

In particular, on established expander Tseitin families for which ordinary unrestricted DAG Resolution has size at least 2^{Omega(h)}, the transformed **strict-3CNF** family inherits the SAME model lower bound:

$$
S_{\rm Res}(H_h)\ge 2^{\Omega(h)}=
\exp(\Omega(N/\log N))
$$

for indexed source bit length N=Theta(h log h). This is a proper proof-size lower-bound transfer, not an unproved consequence of equisatisfiability. It does NOT transfer to arbitrary SAT computation, Res(XOR), extended Resolution, or full historical R_mix341.

### Theorem 503.2: exact unit-paid mixed minimum in a DISTINCT calculus

Every original clause of T is essential: when one forbidden vertex pattern is restored, prescribe its three incident edge values; the remaining charges are consistent on connected G-v. In a bridgeless cubic graph G-v is connected, since a cut vertex of degree three would create a bridge. Thus deleting any original clause makes T satisfiable.

For unchanged clauses of H, extend the corresponding T-deletion model through the satisfiable gadget C. For each of the three gadget clauses, take a T\{C} witness falsifying ell_1,ell_2,ell_3. The gadget reduces to (u) AND (NOT u OR v) AND (NOT u OR NOT v). Deleting respectively A,B,D yields the witnesses u=0; (u,v)=(1,0); and (u,v)=(1,1). **All m=4h+2 clauses of H are individually indispensable.**

Define a **separate** fixed sound, complete and effective typed calculus R_bridge503: free authenticated original-source clauses; unit-paid binary ordinary RES; unit-paid AND3 on two exact Boolean factor/clause views whose union support has at most three original Boolean coordinates; and unit-paid binary GF(2) addition of already certified affine rows. A RES-derived clause can be used by AND3 through an explicitly allowed exact clause view. This extensional view is a DECLARED R_bridge503 typing rule, **not historical R_mix341**. Resolution ensures completeness; no source-aware oracle or uncharged derivation is allowed.

Derive C from H with 2 paid RES nodes. For each of h vertices, combine four original clauses into its exact three-bit parity factor in 3 AND3 nodes, yielding h affine rows. Combine those rows with h-1 XOR nodes, obtaining 0=1 because total charge is odd. Therefore

$$
W_{R_{\rm bridge503}}(H)\le 2+3h+(h-1)=4h+1.
$$

In ANY sound explicit binary-premise inference DAG proving this H UNSAT, every indispensable original clause must be an ancestor of the sink. With m source leaves and q paid two-parent inference nodes, the dependency graph is undirected-connected and has at most 2q edges. Hence m+q-1 <= 2q, or q >= m-1. With exactly unit weights and no hidden multi-premise source-access rule, this yields the **exact** result

$$
\boxed{W_{R_{\rm bridge503}}(H)=4h+1=m-1.}
$$

The inequality includes arbitrary legal sharing and reconvergence. This is not a historical all-rule R_mix341 lower bound. Adding a mandatory paid CAST between a RES clause and an AND3 factor changes the constructed upper bound by +1 and removes the exact-equality assertion for that different grammar.

## Independent verification, hostile controls, resource accounting

The published dependency-free JS reproduction (experiments/arc/lspv3_503_strict3_source_retraction.cjs; blob 85801666e30b67132f02af2236904c20188e842d) passed **1,278 assertions, 40 source choices (16 K4 and 24 K3,3), and 80 adverse checks**. Every expanded source had 18 (K4) or 26 (K3,3) individually essential strict3 clauses. Logical constructions have exactly 17 or 25 paid nodes.

An independent full Node.js typed proof verifier executed 40 cases, accepted explicit RES/AND3/GF2 proofs, checked all source-to-sink ancestry, AND3 truth tables and affine aliases, and rejected **200** adversarial mutations. Its K4 packet serialized to 1,464 bytes and K3,3 to 2,097 bytes; depth 6 in both. Independent Python replay verified all 16 K4 clause replacements, original odd UNSAT, 8 even-charge satisfying models, even-charge expanded SAT, and exact gadget retraction. A separate Python Davis–Putnam Resolution proof producer and substitution translator generated all 16 K4 expanded proofs, then produced valid smaller or equal ordinary Resolution proofs of the original sources: external total source+inference records 56–83, converted records 47–51. This directly exercises the quantified backtranslation at finite sizes, not the published asymptotic theorem.

The exact original LSPV-2/341 **SOURCE/AND3/XOR checker** logic was re-executed in V8 on its original balanced packet and passed **30,714 original assertions over seven fixtures**, including its malformed controls. It was **NOT** run on new RES-to-AND3 packets because that byte grammar is unavailable. New JavaScript is an independent verifier, not an execution of the historical full mixed checker.

Machine resource ledger: q=4h+1 is **logical nodes only**, with one charge per distinct inference and no duplicate shared-node charges. A source has O(h log h) literal bits; node ID/reference lists O(h log h) bits; dense affine masks can contribute O(h^2) bits across all rows. Deterministic construction and local rule checking are polynomial in h with explicit mask processing (at most O(h^2) bit operations in simple dense implementations); graph input reads, construction, sorting, verification, conversion, output, caches and simultaneous peak space are not free. Exhaustive finite SAT deletion checks explicitly spend exponential time in the test instances and do not give an all-input SAT algorithm. Weighted critical path differs from minimum work; simple balanced logical depth <=4+ceil(log2 h). No same-machine FLMV claim follows.

**Raw file:** results/raw/arc/2026-11-08_0724_LSPV3_503_SOURCE_RETRACTION_RAW.json, blob b518952c1c6ed88c5c7d37313aa066a399598397. Independent full Node/Python checks and raw substitution translator are also archived locally for reproduction.

## Status and unresolved transfer

Actual advance: a rigorous published-family strict3 source-expansion lower-bound preservation proof in **ordinary Resolution** plus an exact, differently typed mixed-system upper-control. This sharpens [P2-C3] without settling it.

The decisive missing historical artifact is still **[P2-D1]**: an authentic accepted-byte RES-derived clause-to-AND3 factor record with its conversion costs, and DEF/LOCAL-CONVERT/private/exported-port/assumption-discharge productions. All-rule historical [P2-B1] and noncircular same-calculus B3 [P2-B2] remain OPEN. No inference weights, five-agent role allocation, tasks or manuscript regions were modified. **P versus NP remains OPEN.**
