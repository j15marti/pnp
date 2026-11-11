# LSPV-3/557: Single-fixture SAT source accepted by pinned /341 checker, including its own negative harness

**2026-11-10 17:24 PST | Hypergraph & Proof Certificates (Route B) | PROVED/RESTRICTED exact original-code acceptance + COMPUTATIONAL ten negative controls | P versus NP OPEN**

## Claim, precedence and falsifiers

**Candidate tied to [P2-D1].** Earlier LSPV-3/551 used a two-fixture packet in which the first, original UNSAT K4 fixture supplied the original checker's built-in deletion-witness mutation test. Can one remove that entire auxiliary K4 fixture and make the **one satisfiable-source fixture** withstand the checker's complete self-test harness, while leaving the original verifier body exactly unchanged? A successful result would strengthen the operational SAT-source acceptance finding by making it self-contained, but would not authenticate historical mixed-rule syntax.

F1: the original verifier's built-in negative witness test fails when every deletion witness is null. **True for the naive one-fixture packet; repaired below.** F2: no genuine source-deletion witness exists for the satisfiable target formula. **False:** the all-zero assignment falsifies exactly original clause 0 and satisfies the other 47. F3: numeric node IDs alter parent lookup or distinct first-use charges. **False** on original-body execution with IDs 0..94 and all 47 paid nodes. F4: dropping unconsumed metadata or the benign K4 fixture disables mandatory checker negatives or invalidates the fake sink. **False** in the final 8,573-byte accepted single-fixture packet and ten hostile controls.

## Original sources and exact trust boundary

Pinned original producer `experiments/arc/lspv2_341_mixed_tseitin_min_dag.js`, blob `4081022e8a3841d79f751a3d3a7a10decbb026da`; original recovered verifier `experiments/arc/lspv2_341_independent_verify.js`, blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`; original /551 two-fixture accepted SAT packet `results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json`, blob `706947c767361e7c979b8208677eb983d33838f4`. The declared five-family mathematical system comes from `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. This original recovered executable dispatches SOURCE/AND3/XOR **only** and is not the full authoritative R_mix341 proof-language checker.

Prior literature/control work: Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, J. Symbolic Logic 44 (1979), 36–50; Cousot and Cousot, *Abstract Interpretation*, POPL 1977; D'Silva, Haller and Kroening, *Abstract Conflict Driven Learning*, POPL 2013. Exact external source review rechecked `konard/p-vs-np/scripts/proof_status.json` (blob `93b77ed3...`), `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` (blob `18d693ea...`), `meelgroup/frat-xor/format.md` (blob `986a21aa...`) and CakeLPR README (blob `e94f45e9...`); none supplies missing historical mixed byte grammar. Relevant original project reports /537, /551–556, LSPV-1/559, LSPV-2/544 and LSPV-4/529 were compared to avoid rediscovery. Grok 2026-11-10 15:23 UTC and Claude world-ledger 2026-10-28 were read.

## Theorem 557.1: one authenticated operational counterexample packet

Let `F` be the exact connected, bridged 12-vertex, 18-edge signed proper 3-CNF of /551. It has 48 numeric, distinct-width-three original clauses. The complete assignment

$$
a=\texttt{101001000000100000}
$$

satisfies **48/48** clauses. In contrast, the all-zero assignment `z=0^18` satisfies 47/48 original clauses and falsifies **only clause 0**, which has literals `[1,2,13]`. Therefore `z` is a valid deletion witness for source clause 0 even though `F` itself is SAT.

Construct a **single-fixture** JSON packet by taking only /551's SAT fixture, removing unreferenced metadata, replacing original/source identifiers `s0..s47` by exact JSON integer IDs `0..47`, replacing proof IDs `d0..d46` by `48..94`, and rewriting every parent and deletion reference consistently. Preserve the 47 AND3/XOR inference semantics, the malformed charge `"1"` and malformed AND3 support string `"012"`. Set `deleted[0].assignment = "000000000000000000"`, all other deletion assignments null, and `properties.essential=1`. Provide a one-element `summary` array, as the original checker compares only its length.

**Exact acceptance result:** The 8,573-byte compact packet passes the **unchanged pinned original checker** in a V8 isolate with only Node I/O/stderr/stdout wrappers substituted, yielding 3,273 passed original assertions. Its source is SAT under the explicit witness above. All five original built-in mutation tests, including the deletion-witness mutation, now run on this same SAT fixture rather than on a separate UNSAT fixture. Ten additional hostile modifications were rejected, including changing charge `"1"` to numeric 1, restoring the typed support array, corrupting the AND3 table, sink, parent, source, deletion witness, even-parity witness, parent arity or clause count.

The original /551 13,324-byte packet required two fixtures. This result removes that auxiliary benign fixture, eliminates its dependence in the original negative-control harness, and reduces packet bytes by 4,751 (35.7%), while retaining 47 paid inference records and the same satisfiable original source. The new record is not a minimum-length claim.

**Reason:** In the unchanged checker, charge parity computation bitwise-coerces `"1"` to one while local clause authentication uses a strict comparison to the string. The support-string `"012"` passes an `includes(12)` substring test but is iterated as the characters 0, 1, 2. Thus it falsely authenticates a parity row incompatible with the actual original clauses. These defects are not legal inference rules of the intended fixed calculus.

## Sound abstraction consequence and cost ledger

The packet is a **genuine accepted terminal of the recovered fixture checker** but not an UNSAT refutation of its literal source. Therefore any cost-sound abstract-proof construction must keep `acceptedByRecoveredFixture` separate from `semanticallyProvesUnsat`; otherwise it violates goal soundness. In CEGAR, reproducing this original acceptance reveals a real implementation flaw, not a legitimate shortcut in the mathematically intended system. A strict typed, independently source-bound kernel would reject the two malformed fields; a distinct kernel cannot be silently substituted for the historical grammar.

Logical paid creation work: 47 distinct AND3/XOR records (same as /551), count once. Explicit wire/source certificates and packet length: 8,573 bytes (a **byte count**, not space usage). Construction, identity renaming, source checking, repeated checker negative controls, and complete V8 object storage were paid during this finite audit but no native machine-work-time or peak-space asymptotics are asserted. Free optimal proof selection, zero-cost source reading and shared-DAG references remain separate from this operational fixture.

## Executed evidence, reproducibility and publication

The original verifier **body** was fetched at its pinned Git blob and invoked via `new Function` in the connected V8 code runtime with only `require(fs)`, `process.argv`, and `console.log` stubs. It passed 3,273 original assertions on the one-fixture packet. Ten independent hostile packets were rejected. Separate direct Boolean evaluation verified both the SAT assignment (48/48) and the deletion witness (47/48). The new standalone `experiments/arc/lspv3_557_single_fixture_reproducer.cjs` was syntax-parsed under V8, but not executed as a native Node operating-system subprocess during this run; it reads the pinned original files and repeats the experiment with native Node for independent reproduction. A full repository local checkout and its preflight script were unavailable because the container cannot resolve github.com; direct GitHub connector preflight read both trackers, AGENTS.md, CODEX.md and the repo skill.

Code: `experiments/arc/lspv3_557_single_fixture_reproducer.cjs`; exact JSON packet: `results/raw/arc/2026-11-10_1724_LSPV3_557_SINGLE_SAT_PACKET.json`; complete raw ledger: `results/raw/arc/2026-11-10_1724_LSPV3_557_SINGLE_SAT_RAW.json`. All reference identifiers and source bytes are preserved in the committed packet.

**Material difference:** earlier /551 required a separate benign fixture to pass the original checker's own mutation harness; this result directly passes it on the SAT source. **Remaining gap:** P2-D1 still requires historical accepted-byte RES, LOCAL-CONVERT, DEF/facets, exported/private interfaces and branching/discharge with a sound, external-source-bound checker. Full P2-C3/P2-B1 and B3 remain OPEN. P versus NP OPEN.
