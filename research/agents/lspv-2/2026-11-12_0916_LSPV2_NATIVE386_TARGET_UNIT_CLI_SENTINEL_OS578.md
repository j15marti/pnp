# LSPV-2/578: fixed-source target-unit Resolution, a live 999999 gate, and an original-checker CLI counterexample

**2026-11-12 09:16 PST | LSPV-2 SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED in a specified finite Resolution construction + COMPUTATIONAL exact original-checker OS replay. P versus NP OPEN.**

## Target, concrete construction and preregistered falsifiers

**Candidate [P2-D1/P2-C3]:** On the independently authenticated signed guarded odd-charge K4 source, derive a pair of opposite signed units with a shared, count-once Resolution DAG; route the pair through a fresh, genuinely live AND2 owner whose new output wire is numerically 999999. Test whether changing ONLY the final signed pivot orientation separates the archived original /386 mathematical checker from its complete command-line acceptance predicate. Use the resulting CEGAR counterexample as a strict full-CLI state-distinguishability control without inventing any historical R_mix341 rule.

F1: the projected units or conservative defining facets are not valid under the independently signed original source. F2: the two terminal orientations yield identical complete-CLI outcomes, or no final positive-sentinel proof reaches the mathematical checker. F3: original-checker validation lets a forged SOURCE, underpayment, wrong owner, forward parent, incorrect signed pivot, or counterfeit AND3 opcode through. F4: a minimum among deterministic target-unit Davis–Putnam schedules is improperly promoted to an unrestricted shared-DAG or mixed-rule lower bound. F1-F3 are rejected by exact native replay; F4 is deliberately not claimed.

## Authority and exact source binding

The unchanged original archived checker is `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`, in the original project repository. It accepts only SOURCE records, conservative paid AND2 owner declarations with free valid DEF facets, and strict signed binary Resolution, with an additional complete-CLI negative-test wrapper. **It is not an authoritative unified checker for historical R_mix341.** The other unchanged archived `/341` checker, Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`, accepts a different SOURCE/AND3/XOR fixture dialect and cannot be silently composed with `/386`.

The external original source is `results/raw/arc/574_k01_SIGNED_SOURCE.cnf`, SHA-256 `3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c`. The exact executable verifies all 17 signed SOURCE clauses in order against these external bytes, rather than trusting a claimed summary or embedded source. It pins the original checker Git blob and source SHA, then uses actual OS Node.js subprocesses. No new grammar is called historical.

## Construction and restricted replay lemma

Fix the seven original variables: six edge variables and guard 7, with signed original SOURCE occurrences C_0,...,C_16. For each target original edge variable t in {1,...,6}, run deterministic Davis–Putnam elimination on the six **other** variables, in each of their 6! orders. For every eliminated variable p, retain each new non-tautological exact signed resolvent from one positive-p and one negative-p parent; globally intern identical clauses. When elimination completes, recover the ancestors of both singleton clauses [t] and [-t], and topologically emit their shared proof DAG.

**Lemma 578.1 (restricted, proved by algorithmic induction).** Every emitted paid node is an exact signed Resolution inference from two earlier nodes; all SOURCE occurrences retain their external identity; a shared derived clause is paid once; and both target units follow from the original source. This follows by induction on each elimination step and the ancestor-first emission order. The finite exhaustive **DP-scheduling** minimum of the union ancestor DAG, across 4,320 tested (target, order) combinations, is 28 paid RES nodes, attained for t=1 and elimination order (2,3,6,5,4,7). This is **not** a minimum over all shared-DAG proofs or the complete mixed calculus.

For t=1 define a genuinely live, globally fresh conservative AND2 owner

    owner 0: z = x_1 AND x_1, z=999999,

whose permitted free defining facets include `[999999,-1]` and `[-999999,1]` (canonically sorted as `[-1,999999]` and `[1,-999999]` under the checker's canonical order). Using the derived units [1] and [-1], two further paid Resolution steps derive [999999] and [-999999] from their respective valid facets. A final paid Resolution derives the empty clause. Every first payment is counted once, even though both unit branches share ancestors and the two free facets share one paid owner.

The resulting 50 records comprise 17 SOURCE, 2 free defining facets and 31 paid RES. There is one charged owner, hence

    W = 28 + 2 + 1 + 1 = 32.

This is an **upper witness**, not an all-proof minimum. No branch assumption, weakening, discharge, join, deletion or unrecognized opcode is assumed legal.

**Theorem 578.2 (verified original-checker same-source CLI asymmetry).** Starting from this exact certificate, (a) final parents ([z],[-z]) and signed pivot `+999999` pass the unchanged original mathematical checker but fail the unchanged complete CLI; (b) exchanging just those parents and using pivot `-999999` passes both the mathematical checker and the complete CLI, with identical source, shared paid DAG and W=32; (c) uniformly replacing the live fresh wire with 1000000 and recanonicalizing clauses yields a full-CLI accepted `+1000000` proof of W=32. This is consistent with, and gives an independent cheaper fixed-source control for, the already proved sentinel-wrapper condition in LSPV-1/567 and LSPV-1/591. **Those prior reports have priority for identifying the sentinel defect.**

Proof of the core equivalence is the ordinary signed Resolution identity, with the original plus/minus orientation and two singleton parents both explicitly verified by the original checker. The CLI rejection follows directly from the original source: its first bundled hostile mutation forcibly writes 999999 into the final pivot, producing a no-op on the +999999 proof; its negative-control checker then raises `accepted a corrupted proof`. On negative pivot or 1000000 the mutation genuinely breaks the signed-pivot antecedent requirement. No additional logical inference charge is introduced.

## Exact executed corpus

The published byte-for-byte script `experiments/arc/lspv2_578_native386_target_unit_os.cjs` (Git blob `e03d3c5f3380503d82d5f037eab64c9eead5e295`) was executed on Node.js v22.16.0 with the unchanged original checker as OS subprocess, not a replacement parser. An independently launched second OS process called the verbatim mathematical `checkProof` body, extracted from the same pinned source and with only an entrypoint appended.

Across 4,320 deterministic target-unit schedules, the ancestor-Resolution-count distribution was: 28 (144), 30 (144), 32 (576), 34 (720), 38 (720), 42 (720), 46 (1296). Every target had a best schedule with 28 paid RES. This counts one specified constructive family and must not be interpreted as a hard-instance minimum.

Of nine byte-exact tested certificates, three passed the original mathematical checker. Of these, two passed the unchanged full CLI and one, the positive-999999 terminal pivot, was rejected by the CLI. Six hostile certificates were rejected by both. The two accepted CLI certificates jointly completed **6,920 original-checker assertion groups**, including 22 original bundled negative tests. The full CLI acceptance cases are the negative-999999 certificate (3,153 bytes; SHA-256 `23bbc894ef85c7c946c8d646239b3754cf08edfb76eb3ee26771d5aeab0bd854`) and the positive-1000000 certificate (3,158 bytes; SHA-256 `3320ebca2a34bd8d1c3a98fd3eecf2a7ede7eb27d48cbc9e218507cc8279b39e`). The rejected core-valid +999999 witness is 3,152 bytes; SHA-256 `abbb460f3ca2925291b30df13a57d460ff2aa9b9b089e220e0548b6ad02f1f85`.

The compact GitHub ledger is `results/raw/arc/2026-11-12_0916_LSPV2_578_NATIVE386_TARGET_UNIT_OS_COMPACT.json`; executing the exact program generates the nine complete packet files and its full raw manifest `578_native386_raw.json`.

## P2-C3 abstract-transition consequence and resource separation

There are **two distinct acceptance relations** in the same archived original implementation: the native mathematical core and its CLI wrapper. An abstraction that retains the unordered pair of signed terminal units and abstract payment set, but forgets orientation of the final signed pivot, can be exact for the **core** Resolution relation yet **not** exact for the complete CLI. Its concretization includes both byte presentations, so it must conservatively retain the valid CLI `-999999` successor; for exact CLI replay it must add the terminal-sentinel predicate, or preserve the oriented final port.

The abstract charge of an already paid shared node is zero on reuse. Charging source premises zero, the two genuinely new unit-conversion RES one each, the final RES one and the newly declared paid gate once reproduces W=32. A state that forgets which owner has already been paid can overcharge shared reuse, while an unsound forced-duplicate rule may suppress a genuine shorter proof. Unknown mixed-calculus transitions remain conservative **MAY** alternatives, at zero cost floor until their fixed historical tariffs and scope are authenticated. This restricted example proves no all-rule alpha/gamma simulation.

Logical work W=32 is not 3,153 certificate bytes, serialization/construction work, source acquisition, actual Node CPU time, verifier operations, dependency-graph span, or peak physical memory. No asymptotic physical time or space bound is inferred from a finite proof. The six possible target-unit relabels are not an all-input complexity statement.

## Corpus and prior-art audit

Read both current root trackers `proof1.txt` and `proof2.txt`, issue #3 (including current peer tail), `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, LSPV-2/539 and relevant 541-549 controls, /566 and /568-577, latest role handoff /577, original /341 declaration and both archived checkers, plus LSPV-1/567 and /591. LSPV-2/575 already enumerated complete seven-variable DP **refutations**; /576 established 28 tree-RES for one fixed source; this work instead targets both opposite *units* simultaneously before deliberately introducing a live fixed-sentinel paid definition. LSPV-2/566 already established conditional alpha renaming for this original checker; LSPV-1/567 and /591 already discovered and characterized the sentinel. Adopt exact source provenance, canonical signed ports, shared DAG first-payment and conservative gate semantics; reject source-nonessential pruning, arbitrary mixed-tag substitution and wrapper requirements as mathematical proof rules.

Primary literature consulted for proof-system checks and abstract refinements: Cook and Reckhow (1979), DOI `10.2307/2273702`; Cousot and Cousot (1977), DOI `10.1145/512950.512973`; Peitl and Szeider, optimal Resolution proof search (JAIR 2021), DOI `10.1613/jair.1.12589`. Separately compared external `meelgroup/frat-xor`, `tanyongkiam/cake_lpr`, `konard/p-vs-np`, and `blkph0x/p-vs-np-proof-research` through existing authenticated project source ledgers. None can authenticate historical R_mix341 accepted-byte syntax.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The exact instance and CLI implementation discrepancies do not change P2-D1, full P2-C3, P2-B1, separate B2/B3 or P1-01/03/04. Root `main.tex` must be changed only within LSPV-2 owned markers after fetching complete fresh content and blob, with full readback; no unsafe partial overwrite is authorized. No historical rule/weight, title, agent identity, timezone, ownership or two Route A/three Route B allocation is changed.

**Next decisive artifact:** locate the single original full R_mix341 checker with a genuine source-authenticated RES-to-AND3 or DEF-to-LOCAL-CONVERT edge, accepted byte witness and corrupted signed-port control, then extend concrete-to-abstract replay without conflating this /386 sibling's CLI wrapper with proof mathematics. **P versus NP remains OPEN.**
