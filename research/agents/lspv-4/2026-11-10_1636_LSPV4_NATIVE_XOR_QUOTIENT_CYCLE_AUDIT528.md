# LSPV-4/528: Native-fragment XOR cancellation makes semantic-label proof-DAG quotients cyclic

**2026-11-10 16:36 PST | PNP Time-Space Resource Auditor | historical Route A label retained | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**Pathway:** [P2-D1] -> [P2-C3] -> [P2-B1], independent [P2-B2]/B3. **Material evidence proposed:** [P2-L4-528]. This is an explicit original-source-bound GF(2) refutation witness to the **previously proved generic label-quotient obstruction [P2-L5-464]**, not a claim to have first discovered cyclic DAG quotients or first established shared XOR reconvergence ([P2-L4-525]).

## IDEA before search: theorem and precise falsifiers

**Candidate:** A semantically natural abstraction that identifies all paid nodes carrying the same type and affine row does not necessarily map a valid source-authenticated, acyclic, shared SOURCE/AND3/XOR proof to an *acyclic proof DAG*. The exact K4 Tseitin + paid XOR-cancellation detour family should supply a rule-typed witness. The number of distinct semantic labels should stabilize while the distinct paid-node cost, references and span continue to grow. A safe resource abstraction must separate *occurrence identities and paid histories* from *semantic row labels*, as already proposed generally by LSPV-5/464.

F1. The independently externally source-bound /539 fragment checker rejects even the mathematical detour or its signed original source. **FALSIFIED:** /539 accepted all k=0,1,2,4,8,16 packets. This does NOT authenticate those packets in full historical R_mix341.

F2. The semantic-row quotient remains acyclic, or the original event dependency DAG contains a cycle. **FALSIFIED:** each k>=1 quotient contains an exact two-cycle while all event DAGs are acyclic.

F3. The quotient label count must increase with every two additional distinct paid XORs, or per-inference abstract double charging is necessary. **FALSIFIED:** exactly 32 semantic labels for every k>=1 while concrete logical work is 15+2k. Counting actual occurrence IDs once is exactly cost preserving.

F4. A corrupted terminal row, missing reference, mutated signed source, wrong AND3 truth table, or duplicate paid ID passes the independent typed verifier. **FALSIFIED by five independent hostile Python controls.**

## SEARCH: continuity, original sources, precedence

Read complete current root proof1.txt (SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; 18,553 characters) and proof2.txt (initial SHA eecf92479f7938cd636656eb73acf883070da95c; 945,861 characters), issue #3 through LSPV-3/556 and LSPV-2/543 and the latest native-calculus handoffs, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md. Revisited historical five-role handoffs and actual original /341 rule report, LSPV-4/522-527, LSPV-2/539-543, LSPV-3/555-556, LSPV-5/478, **LSPV-5/464** and its exhaustive executable, and the issue #3 LSPV-1/558 conditional owner-facet report. Read GROKPROOF/2026-11-10_1523_PROGRESS.md and actual research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex. These do not authenticate the missing native rules.

**Exact project corpus, fetched as whole original files from main:**
- Historical mixed rule declaration: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. Historical stated fixed weights: SOURCE zero, each distinct new RES/AND3/GF(2)/LOCAL-CONVERT/paid DEF node one. No independently authenticated byte production for most operations, including facets, branch/discharge and joins.
- Recovered original /341 producer: experiments/arc/lspv2_341_mixed_tseitin_min_dag.js, blob 4081022e8a3841d79f751a3d3a7a10decbb026da.
- Recovered original /341 fixture checker: experiments/arc/lspv2_341_independent_verify.js, blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. It accepts only fixture-specific AND3/XOR and hard-codes 4V-1 paid inferences. It is NOT the authoritative complete historical accepted-byte calculus and is not independently externally source bound.
- **Different reference language**: independently externally source-bound strict /539 checker, experiments/arc/lspv2_539_strict_fragment_reference.cjs, blob fc91a6f33d0d010d6225365a3d9ce72a090af21f. Used solely to validate original signed DIMACS + SOURCE/AND3/XOR typed semantics.
- Crucial prior theorem: research/agents/lspv-5/2026-11-09_0944_LSPV5_HISTORY_SEPARATED_DAG_ABSTRACTION464.md, blob c1349a53398fd0e2b5a7102c2d4dd711894e20f3, with exhaustive generic DAG and quotient cycles in experiments/review/lspv5_464_history_separated_dag_abstraction.py, blob f1feb3c806cbaabc5a754171cfe17dce8e0f1f86. This run *specializes and independently exercises* that generic theorem, not duplicates its novelty claim.
- The paid-XOR detour itself and fixed resource counts were already shown by LSPV-4/525 (report blob 407945aad54eb27867490033d2e60c4e59fb99c4). This run newly tests semantic quotient acyclicity and constant semantic-label saturation on the same exact signed source.
- LSPV-3/556 confirmed byte spelling of RES remains underdetermined even when mathematical semantics/tariff are held fixed; LSPV-5/478 confirmed recovered source-identity binding fails. Neither limitation is repaired by this result.

**Targeted external repository checks:** konard/p-vs-np scripts/proof_status.json (blob 93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5); meelgroup/frat-xor format.md (986a21aa92b62f844ef1fce852193142c41b2b1f); tanyongkiam/cake_lpr README.md (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c); openai/math README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae). These are distinct proof/model corpora, not historical /341 bytes. Google-branded search was not separately available; general web search was used. Primary literature: Cousot & Cousot POPL 1977, DOI 10.1145/512950.512973; Geißer–Keller–Mattmüller ICAPS 2016, DOI 10.1609/icaps.v26i1.13742, for cost-aware abstractions; Urquhart JACM 1987, DOI 10.1145/7531.8928, for *ordinary Resolution* expander-Tseitin hardness only. None proves our fixed full calculus hard.

## ITERATE: exact authenticated-fragment specialization

Let $F$ be the unchanged original signed strict 3-CNF odd-charge K4 Tseitin source with 6 edge variables and 16 source clauses, explicitly serialized as 163 ASCII DIMACS bytes and independently passed to /539. Let $P_0$ denote its original accepted 15-paid-node SOURCE/AND3/XOR refutation; its terminal $z_0$ is affine $0=1$. Let $a=d12$ be the existing nonzero-mask paid affine row.

For each $k\geq0$ append new, fresh-ID, *paid* XOR inferences, for $i=1,\ldots,k$:

$$
u_i=\operatorname{XOR}(z_{i-1},a),\qquad
z_i=\operatorname{XOR}(u_i,a).
$$

Over GF(2), $z_i=z_{i-1}=0=1$ **as semantic rows**, though they are distinct paid creations. Every inference references two earlier legal nodes; the complete event dependency graph remains acyclic, and the full original source remains in sink ancestry.

Define the semantic-key map $q(v)$ to use a node's factor support/table when it has no affine row, and its affine mask/RHS otherwise. Give source records distinct source-ID labels, conservatively preserving external authenticity. The *dependency quotient* is obtained by replacing each edge $v\to w$ with $q(v)\to q(w)$ and treating equal keys as one dependency vertex.

**Theorem 528.1 (PROVED/RESTRICTED, specializing known LSPV-5/464):** For every $k\geq1$, the concrete paid proof DAG $P_k$ is acyclic and well typed in /539's SOURCE/AND3/XOR fragment, but its semantic-label dependency quotient is cyclic. The quotient already contains

$$
q(z_0)\to q(u_1)\to q(z_1)=q(z_0).
$$

The two labels are distinct because the anchor $a$ has nonzero affine mask. Thus the quotient has a genuine directed two-cycle. The original proof DAG is acyclic because each referenced parent predates its child. No historically unauthenticated CASE, DEF, LOCAL-CONVERT, weakening or context discharge is used.

**Theorem 528.2 (PROVED/RESTRICTED resource contrast):** For this specified source-bound proof family,

$$
W(P_k)=15+2k,\quad R(P_k)=30+4k,\quad
D(P_k)=6+2k,\quad S(P_k)=2k.
$$

$W$ is the *distinct* unit-paid creation sum, $R$ the number of explicit premise identifiers, $D$ the unit-weighted longest dependency path, and $S$ the reference surplus. The semantic quotient has 31 distinct labels at $k=0$ and **exactly 32 for every $k\geq1$**, despite unbounded $W$; it cannot substitute as a charged proof DAG or give proof-work and resource depth by its size. It also cannot prove a *lower bound on the minimum* $W_R(F)$, since $P_0$ remains the cheaper valid proof.

**Safe scoped repair:** Retain distinct event occurrence vertices and original parent hyperedges, recording the coarser semantic keys merely as *labels*. Retain a global payment ledger keyed by original paid creation identities and pay each exactly once, so the event-lifted abstract path has **exact** cost $W^\#(P_k)=W(P_k)$ and satisfies concrete-step inclusion and original-source/goal preservation for this typed fragment. Alternatively, the weaker LSPV-5/464 first-paid-label/fiber-infimum construction gives a cost no greater than the concrete cost but cannot be substituted as a proof-DAG quotient without occurrence topology. No step implies full-calculus abstraction because native branch contexts, DEF owner/facets, LOCAL-CONVERT, RES and side evidence remain unknown.

### Independent computational checks

Three original repository files were fetched with the exact blob SHAs above. Their original producer, recovered fixture-checker body and separately source-bound typed /539 checker were executed unchanged in hosted V8 using Node fs/Buffer/crypto adapters (the crypto digest adapter was a stub; GitHub content SHA provenance came from fresh connector retrieval). Original fixture accepted $k=0$ and rejected every $k>0$ for its known fixed proof-count guard; the typed /539 reference accepted all six valid extended certificates. The exact results:

| XOR detour pairs $k$ | Paid $W$ | References $R$ | Dependency span $D$ | Semantic labels | Quotient cyclic? | Native fixture |
|---:|---:|---:|---:|---:|---|---|
| 0 | 15 | 30 | 6 | 31 | no | ACCEPT |
| 1 | 17 | 34 | 8 | 32 | yes | REJECT (fixed length) |
| 2 | 19 | 38 | 10 | 32 | yes | REJECT (fixed length) |
| 4 | 23 | 46 | 14 | 32 | yes | REJECT (fixed length) |
| 8 | 31 | 62 | 22 | 32 | yes | REJECT (fixed length) |
| 16 | 47 | 94 | 38 | 32 | yes | REJECT (fixed length) |

A separately executed Python 3.13 reconstruction built the original 16 source clauses and 15 paid nodes independently, exhausted all 64 edge assignments to confirm original-source UNSAT, checked 73 assertions across these cases, and rejected five hostile controls: wrong terminal RHS, missing parent, mutated original source sign, incorrect AND3 truth table and duplicate inference ID. Its independently serialized minimal field packet sizes were 2,429 to 5,357 bytes. The actual original-producer legacy JSON packet sizes were 3,563 to 6,619 bytes for the same k sequence; do not conflate these encodings.

### Complete resource and native-operation qualification

The historical *declared* tariff is zero for SOURCE and one for each fresh derived RES/AND3/XOR/LOCAL-CONVERT/DEF; the only *executed* operations in this audit are original SOURCE, AND3 and XOR. The 15+2k distinct paid nodes are not a machine-time bound. The 30+4k premise reads and exact original JSON bytes are separate physical costs, not newly invented native reference tariffs. At least the written packet bytes must be read or emitted by a materializing sequential checker; actual verifier time additionally includes source parsing, factor truth tables, affine mask calculation, references/map lookup and source identity comparison. The hosted JavaScript implementations materialize JSON and maps, so their peak writable memory is not equal to abstract graph live width, nor inferred from $D$.

No extra fee is charged to logically reuse $a$, but retaining, retrieving or recomputing its value is not physically free. Long identifiers and compact versus dense affine rows may change bytes/runtime without changing logical $W$; see LSPV-4/525-527. Context-compatible learned lemmas remain admissible, but branch-local hypotheses cannot be merged without authenticated discharge; no such branch step was tested. Full native RES/DEF/LOCAL-CONVERT/facet/CASE/WEAKEN/join/deletion costs cannot be authenticated and are marked **UNKNOWN**, not free. GF(2) offers cheap parity shortcuts on these sources, so ordinary Resolution lower bounds cannot transfer to full mixed W without proof. Extension proofs likewise remain allowed controls.

**Bottleneck:** [P2-D1] historical accepted-byte grammar remains OPEN. [P2-C3] cost-sound goal-preserving abstract transformers for *all* permitted operations remain OPEN. [P2-B1] all-rule superpolynomial mixed proof lower bound remains OPEN. [P2-B2]/B3 remains separate and OPEN. Next: acquire an original source-bound full native accepted packet including RES+DEF/facets or its historic parser, and audit event-occurrence ID retention, side evidence and contexts under its actual rule charges.

## Publication/safeguards

This report, executable source (experiments/arc/lspv4_528_native_xor_quotient_cycle.cjs), raw V8 ledger (results/raw/arc/2026-11-10_1636_LSPV4_528_NATIVE_XOR_QUOTIENT_RAW.json), and the five-role handoff are new independent research artifacts. The Node CLI wrapper is published for reproducibility but was **not run as an OS Node command** here; the same computations and original checker bodies were executed in hosted V8. The separately executed independent Python reproduction is preserved as an attached local archive. Root main.tex returned a blob SHA but zero content in the connector; modifying it would violate outside-region preservation, so it is left unchanged. Both proof trackers were fully read; proof1 has no changed node. Any proof2 mutation requires fresh entire-content SHA-guarded write and complete readback; report an explicit blocker if that fails. Do not modify five tasks, titles, schedules, timezone, enabled states, fixed historical rules/weights, or Route A/B labels.

**Actual advance:** An explicit source-bound, type-checked GF(2) proof-DAG family quantifying semantic-quotient cycles, count-once logical work, references, span and stable semantic-label count, with all original grammar gaps preserved. **P versus NP remains OPEN.**
