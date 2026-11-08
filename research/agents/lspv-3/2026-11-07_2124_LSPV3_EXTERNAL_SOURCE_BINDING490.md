# LSPV-3/490 | External original-source binding for the recovered /341 certificates

**2026-11-07 21:24 PST | Route B (LSPV-3).** Status: **PROVED/RESTRICTED** deterministic source-binding and clause-region probe theorem, **COMPUTATIONAL** exact recovered historical-byte checker replay and 324 original-clause substitution controls, **OPEN** for accepted-byte full historical R_mix341, all-mixed lower bounds and P vs NP.

**Tracker IDs:** new [P2-L3-490]; refines open [P2-D1] and resource distinction [P2-D3], relates to [P2-C3], [P2-B1], [P2-B2], [P2-L5-413], [P2-L5-419], [P2-L5-425], [P2-L3-489]. Proof1 [P1-01], [P1-03], [P1-04] unchanged.

## IDEA and predeclared falsifiers

**Hypothesis.** The exact recovered /341 SOURCE/AND3/XOR checker verifies a *self-contained* specialized Tseitin packet, not an independently supplied original CNF. Its acceptance cannot serve as an externally source-authenticated refutation until an exact CNF equality/identity check is added. Any deterministic exact two-input binder accepting the original source and rejecting all one-clause satisfiable substitutions must inspect every indispensable source-clause region on the original input path.

Falsifiers: (F1) checker already takes and compares a second external DIMACS input; (F2) the packet's alleged source is not independently checked even against its own specialized graph/charge constraints; (F3) a clause substitution cannot preserve byte length and yield SAT; (F4) a deterministic binder can skip a modified region on the baseline execution but reject the same-length mutation without trusted external metadata or an oracle. F1 is false on source-code inspection, F2 is false after exact 30,714-check replay, F3 is false for 324 explicit SAT mutants, and F4 contradicts deterministic transcript identity.

## SEARCH: recovered bytes, project and literature

Read both complete shared trackers and coordination issue #3. Start-of-run root tracker blobs: proof1.txt `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, proof2.txt `e2e15d8632676257a4cbfcf8ca8ca3b2cd09b011`. Reviewed `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, `AGENTS.md`, `CODEX.md`, and `.codex/skills/pnp-research/SKILL.md`; LSPV-3/477,/478,/479,/486,/489, LSPV-1/495, LSPV-5/412,/413,/419,/425, actual `GROKPROOF/2026-11-08_0320_PROGRESS.md` and `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`.

Authentic original rule statement: `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. Recovered verifier: `experiments/arc/lspv2_341_independent_verify.js` blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`. Preserved source/proof packet: `results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json` blob `fe27fe1011d0021e721ccaeb747ed58da65d7464`.

The original checker invokes `JSON.parse(fs.readFileSync(process.argv[2]))` to read **one** self-contained packet. Its real source verification reconstructs clauses, graph, charge, local truth tables, deletion witnesses and proof references **from inside that packet**. Its standalone `validateCNF` tests synthetic malformed controls; no independently supplied original-CNF file or digest is compared to the packet. This is an interface distinction, NOT an assertion that the original specialized checker accepts false self-contained Tseitin derivations. It also does not define an accepted RES/DEF/LOCAL-CONVERT byte grammar.

Required external change-aware file reads: `konard/p-vs-np/scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` and `RESIDUAL_EQUIVALENCE_BARRIER_REPORT.md` blob `464135966173cfc650d2fcd21160df744e63c0b2`; `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; `tanyongkiam/cake_lpr/README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; `peitl/short-proof/README.md` blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab`; `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`; `anthropics/formal-math/eth/Challenge.lean` blob `6297ab1398884550253bdd1475704729d02ce89b` (explicit sorry). These repositories are hypothesis and checker-format controls, not authority for R_mix341. Public indexed search examined Haken 1985, Chvatal--Szemeredi 1988, Cook/ER and FRAT-XOR. A distinct Google-branded research interface was not used; no PDF was analyzed.

## ITERATE: theorem 490.1, exact external-source binding (PROVED/RESTRICTED)

Let P be a self-contained specialized packet accepted by a source-sound verifier V, whose internal clause list is C(P). Let F be a separately supplied, independently parsed CNF, and let M(F) denote the *multiset* of original literal clauses, preserving duplicate multiplicities, with declared variable bound. Define the **distinct** adapter

$$
 B(F,P) = V(P)\land [M(F)=M(C(P))]\land[n(F)=n(P)].
$$

Then whenever B accepts and V's accepted packet denotes an UNSAT source, F is UNSAT. Proof: literal multiset equality makes F and the accepted source semantically identical; the additional variable-bound check binds source syntax. The code compares sorted, signed literal arrays (preserving duplicate clauses), not merely a hash, unsound probabilistic fingerprint or equisatisfiability. Original clause order may permute; ID mappings remain packet-internal. This adapter does **not** add any inference rule, prove generic correctness of V, or authenticate historical RES/LOCAL-CONVERT/DEF.

The original V(P) has no second F argument. Therefore acceptance of V(P) alone has no logical relation to an arbitrary external source G (which could be SAT). This is a missing two-input **protocol binding**, not a discovered UNSAT-soundness counterexample to V in its original one-packet scope. The exact original verifier was successfully executed in V8 on unchanged published code and packet: 30,714 checks, seven fixtures.

## Theorem 490.2: clause-region read lower bound (PROVED/RESTRICTED)

Fix an odd-charge Tseitin F on a connected simple bridgeless cubic graph with h vertices. Its m=4h distinct original strict three-literal clauses are each indispensable (LSPV-2/341): deleting any one produces a SAT source. Encode each external DIMACS clause in a disjoint, fixed-width padded region so that replacements can preserve the exact source length and header. For each clause i, replace it with a same-length valid tautological clause (u OR NOT u OR v), without changing any other bytes. Call the resulting SAT input F_i.

Let D be **any deterministic source-reading verifier**, supplied the same fixed packet P, which accepts (F,P) and rejects every (F_i,P), without an authenticated side channel containing F and without semantic oracle calls. On its execution against F, D must read at least one bit/token in **every one** of the m distinct clause regions. Otherwise, if it skips region i, the execution transcript on F_i is identical step-by-step to that on F and must also accept, contradiction. Thus

$$
 \boxed{\text{External clause-region probes on }F\ge m=4h.}
$$

The same argument holds in a fixed-width binary signed-literal encoding. This is an Ω(m) **source-binding read** lower bound for this fixed-packet comparison task, not a lower bound on arbitrary SAT decision time, the ideal paid-node W_R, certificate discovery, or all source bit reads. It is independent of legal branching, shared proof DAGs and GF(2) shortcut choices.

## Exact finite controls and independently recovered checker

The new separate `experiments/arc/lspv3_490_external_source_bind.cjs` parser/binder was executed directly against the *exact published 197,514-byte original packet*, with both labels and deliberately hostile external-source mutations. Every checked deleted-clause SAT witness was independently tested against all remaining source clauses and a tautological substituted clause; each external mutation preserved the whole source string length and changed only one clause region.

* Exact original recovered verifier: **30,714 checks PASS** for seven historical packet fixtures, executed from the fetched original JS source and fetched original packet (no reimplementation).
* Distinct proposed adapter: **1,320 checks PASS**, 337 intentional rejection controls; **324 independently witnessed satisfiable same-length one-clause mutants**, counts K4 16, K3,3 24, cube 32, Petersen 40, prism6 48, prism16 128, bridged pair 36. The last graph has four nonessential clauses and is a falsifier for all-essential extrapolation.
* K4 exact external DIMACS size **539 bytes** under the adapter's fixed-field serializer; the SAT mutant also **539 bytes**, with deleted-clause witness `000000`. The unchanged packet verifies, but the new external-source binder rejects that SAT source as differing from packet clauses. A permutation of external source clauses is accepted because multiset equality is exact.
* Malformed and corrupted external-input controls: wrong header, wrong variable bound, unterminated clause, wrong clause count, nonnumeric literal, changed source literal, valid but SAT source substitution. Rejections are scoped to adapter, not to historical checker.

**Resource ledger.** The existing bridgeless odd-Tseitin mixed *declared-semantic* proofs have ideal W=4h-1 unit nodes using known GF(2) shortcuts, and exact source-indispensability; this run did NOT regenerate or alter their proof-DAG nodes. New binder: input parsing, scanning and sorting clause keys, exact multiset comparison and reading the entire supplied packet are all paid real operations; a standard deterministic implementation uses O(B+N log N) bit-time up to representation-dependent logarithmic key comparisons and O(B+N) bit-storage with B=packet bits and N=external source bits, conservatively O((B+N)^2) time and O(B+N) space. Parsing/serializing, full proof verification (the unchanged checker), output, failed controls and peak host overhead are not part of ideal W. Independent host V8 execution is not same-machine FLMV time/space. All tests deterministic, no randomness or optimizer cutoffs. No exact host RSS/time claim is made.

## Certified family/theorem/encoding/known-shortcut/remaining-transfer ledger

| Family | Original source encoding | Published/fixed-model theorem | Applicable known shortcut | Remaining gap |
|---|---|---|---|---|
| Odd-charge cubic-expander Tseitin | h vertices, 3h/2 edge variables, four proper strict 3-clauses per vertex, O(h log h) indexed bytes | Exponential **ordinary DAG Resolution** size on suitable expanders (Urquhart 1987; Ben-Sasson--Wigderson 2001); LSPV-2/341 proves exactly 4h-1 derived nodes in its declared mixed semantics for bridgeless cubic graphs | 3 paid AND3 per vertex + h-1 GF(2) XOR; source essentiality yields the m-region external binding lower bound | Native all-rule parser and proof normalization [P2-D1], [P2-C3] |
| Chvatal--Szemeredi random 3-CNF | n variables, 6n independently sampled proper signed triple clauses, Θ(n log n) bits | Exponential **ordinary Resolution** with high probability at c=6; not all-proof-system hardness | Ordinary RES, paid DEF, local conversions, algebra, ER and shared DAGs must be permitted | No superpolynomial all-mixed Wbar bound [P2-B1] |
| Pang 2026 random strict 3-CNF | F(n,3,8n), n variables, 8n width-three clauses, Θ(n log n) indexed bits | Reported exponential syntactic Res(PC_r/F_p) for specified parameters | Full historical RES/AND3/GF(2)/DEF may be stronger | Proof-system preserving transfer [P2-C3] OPEN |
| PHP | Classical CNF, not assumed strict 3CNF | Haken 1985 exponential ordinary Resolution | Cook 1976 Extended Resolution short proof | Need exact lower-bound-preserving reduction if converting to strict 3CNF |

Primary source links: https://doi.org/10.1145/48014.48016 ; https://doi.org/10.1016/0304-3975(85)90144-6 ; https://arxiv.org/abs/2610.00837 ; https://github.com/meelgroup/frat-xor/blob/main/format.md ; https://github.com/tanyongkiam/cake_lpr . No claim of new academic novelty for deterministic transcript/probe argument.

## Publication, coordination and open status

GitHub report `research/agents/lspv-3/2026-11-07_2124_LSPV3_EXTERNAL_SOURCE_BINDING490.md`; executable `experiments/arc/lspv3_490_external_source_bind.cjs`; raw JSON `results/raw/arc/2026-11-07_2124_LSPV3_490_SOURCE_BINDING_RAW.json`; five-role handoff `research/coordination/2026-11-07_2124_LSPV3_SOURCE_BINDING_FIVE_ROLE_HANDOFF490.md`. Executable blob **b113119b7b87dac7510603804d91918e80f301b0** and raw blob **72da0d58124e0ece67448d854756160721eaa5fb** were created from executed bytes. The exact original checker and original fixture packet were fetched by original blobs and independently re-executed in this run.

[P2-D1] native accepted-byte full R_mix341 grammar, [P2-C3] whole-mixed normalization and exported ports, [P2-B1] all-rules superpolynomial Wbar_R, [P2-B2] noncircular same-calculus B3 remain **OPEN**. No historical rule/weight changes, no new agents, no task/schedule/allocation edits, and no root main.tex edit (full safe retrieval not available). **P versus NP OPEN.**
