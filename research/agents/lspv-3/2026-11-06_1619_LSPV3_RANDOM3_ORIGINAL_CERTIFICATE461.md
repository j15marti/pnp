# LSPV-3/461: Original-source UNSAT certificates for established random 3-CNF

**2026-11-06 16:19 PST | Route B | COMPUTATIONAL exact finite certificates, KNOWN source-capacity lemma.** Historical R_mix341 accepted-byte DEF/LOCAL grammar, all-rule superpolynomial lower bound and B3 are OPEN. P versus NP OPEN.

## Idea, four falsifiers, revision

Previous LSPV-3/458–460 used the established Chvátal–Szemerédi 8n random strict-3-CNF grammar but did not certify particular sampled sources as UNSAT. Hypothesis: instantiate original 460 SHA256-counter sampler at n=12 and 16, prove actual source UNSAT by complete enumeration and a strictly oriented original-source Resolution DAG, and exhibit individual clause-deletion witnesses for an extracted inclusion-minimal UNSAT core (MUS).

Falsifiers fixed before experiment: (F1) a sample has a satisfying assignment; (F2) a RES proof uses a foreign source, invalid pivot, forward reference or nonempty root; (F3) a reported MUS clause has no satisfying deletion witness; (F4) mutated source/sign/encoding or malformed/corrupted trace passes checking. The independent verifier rejected F1–F4 for both fixtures.

## Established-family/theorem/encoding/known-method/transfer ledger

**Chvátal–Szemerédi 1988, JACM 35(4), DOI 10.1145/48014.48016:** m=8n IID indexed clauses from all 8 binom(n,3) proper signed width-3 clauses, with repetition allowed. N=O(n log n) bits in indexed encoding. Published asymptotically almost-sure exponential lower bound is for **ordinary unrestricted shared-DAG Resolution**, NOT finite sampled sources, paid-definition R_mix341 or arbitrary SAT algorithms. Pang 2026 arXiv:2610.00837v2 establishes additional random strict-3-CNF bounds for a particular fixed-degree Res(PC_r/F_p) model with PC-degree assumptions, not full paid DEF/LOCAL. Our seed-11 SHA256-counter fixtures use the exact grammar but are deterministic pseudorandom, not mathematically IID.

**Mandatory controls:** cubic-expander odd Tseitin is strict3 and ordinary Resolution-hard, yet has an exact 4h−1-node R_mix341 AND3/GF(2) proof in project LSPV-2/341. Haken PHP lower bounds ordinary Resolution while Cook ER supplies polynomial-size proofs in a stronger system. Braun's bit-PHP lower bound is for Res(XOR) without extension axioms and starts at width 2ell, with no automatically preserved strict3 lower bound. We use legal known shortcuts as upper-bound controls, not forbidden derivations.

## Verified original-source finite results

| fixture | original proper-3 clauses | original SHA256 DIMACS | inclusion-minimal UNSAT core | strict oriented paid RES DAG | unit-span | conditional MUS floor |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| n=12, seed=11 | 96 | db3a96cb859a53044971dfe5f19bd8fb9a4d0d3072a0b626b94fe1f6719d070f | 21 | 33 | 7 | 20 |
| n=16, seed=11 | 128 | bd2b1d07ce6607dc420a64124803c5b08624c81fbc37c94fc3fb6ba0aa70edf7 | 34 | 84 | 10 | 33 |

Both full original inputs were independently UNSAT-checked by complete evaluation of all 2^n assignments. The producer greedily extracts an inclusion-minimal, NOT minimum-cardinality, core; every retained source clause has its own explicit deletion-satisfying assignment. The independently written checker regenerates signed sources/bytes from the SHA256 stream and validates original hash, all deletion witnesses, strict binary Resolution pivots and exact resolvents, topological acyclic references, empty-root ancestry, absence of unused paid nodes, and witness-conditioned SAT controls. The proof uses only historical RES, so no unverified LOCAL/DEF port. The original full formula has a valid refutation since the refuted core is a subformula.

Independent Node replay: **4,278 assertion groups PASS**, 16 deliberate content/proof/witness mutations and 10 malformed DIMACS controls rejected. Original full-source figures are **upper** proof bounds, not minimum-cost hardness certificates. Actual historical authoritative R_mix341 accepted-byte checker was NOT executed.

## Generalized work/branch-sharing accounting

Under **source transparency and sound, conservative, at-most-binary-premise unit-paid rules**, for every clause-minimal UNSAT formula H with r indispensable clauses, every valid shared refutation DAG needs q≥r−1 paid nodes and weighted unit span ≥ceil(log2 r). This is the existing LSPV-2/341 and LSPV-1/378 theorem, not a new proof, and accommodates shared/reconvergent DAGs and best free post hoc choice, assuming all premises are explicitly charged. Historical LOCAL/DEF accepted-byte ancestry remains unverified, so do not apply the floor unconditionally to ambiguous full-calculus rules.

$$
20\le W_R(H_{12})\le33,\qquad33\le W_R(H_{16})\le84.
$$

The displayed lower floors apply to **extracted MUS sources H**, not the larger original sources F. For originals only W_R(F12)≤33, W_R(F16)≤84 are established. An optimal alternative proof can use another subcore or any legal shortcut. No discovered work bound is superpolynomial.

## Resource/evidence ledger

n12: original DIMACS 990 bytes, 47 generated candidate RES nodes before pruning, 33 surviving paid nodes, maximum 23 live DP clauses, ~0.95s producer time, 96,140 KB measured process RSS. n16: DIMACS 1402 bytes, 190 candidates, 84 useful paid nodes, max 76 live clauses, ~20.21s producer and 96,268 KB RSS. Full raw JSONs contain source DIMACS, original indexed clauses, MUS source IDs/deletion witnesses, proof DAG and SAT control. Independent verifier for both fixtures measured ~0.12s and 38,132 KB process RSS. Full machine accounting additionally charges source acquisition/hash/indexing, exhaustive SAT checks, greedy MUS search, trial policies, bit representations, proof serializing, checker, reference lookup, storage/recomputation and output. Unit logical work and ideal parallel span are not actual same-machine time or space.

## Search / peer review / actual dependencies

Read governing refocus handoff blob c3889a3e; current issue #3; AGENTS.md, CODEX.md, skill; historical native /341 blob c87acd11; LSPV-1/378 blob 369be0bc; LSPV-1/455 blob e73b7675; role LSPV-3/460 handoff blob 012f40a1; Grok GROKPROOF/2026-11-04_2315_PROGRESS.md blob f5b8ef62 and Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727; konard/p-vs-np/scripts/proof_status.json blob 93b77ed3; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea; meelgroup/frat-xor/format.md. These do not authenticate historical export syntax or prove a B3 compiler. Indexed general-web literature and GitHub searches were used; standalone Google-branded search was not. No external Lean/full checker execution claimed.

## Open transfer

Next exact arrow: for chosen **established** hard 3-CNF family, prove a source-authenticated polynomial backtranslation from arbitrary complete historical R_mix341 derivations, including all paid DEF, LOCAL, XOR, RES and valid shared branching, into its restricted lower-bound model, OR identify a legal mixed shortcut showing failure. The independent B3 bridge SAT in P => polynomial worst-case minimum for this SAME calculus remains OPEN. No root main.tex, task, schedule, role, weight or allocation changes. All five roles remain two Route A and three Route B.

**Reproduction:** both full raw proofs, SHA256 manifest, original Python producer and independently implemented Node verifier are in the conversation's named reproducibility archive `LSPV3_461_RANDOM3_ORIGINAL_SOURCE_CERTIFICATES.zip`. Repository has role report and compact raw ledger; complete fixture bytes are distributed in that archive.