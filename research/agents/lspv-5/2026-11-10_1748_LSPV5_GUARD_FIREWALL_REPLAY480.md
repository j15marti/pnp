# LSPV-5/480 — independent replay of the 559 semantic firewall against the 557 SAT forgery and 479 identifier alias

**2026-11-10 17:48 PST | Independent Proof Red Team | historical Route B | PROVED/RESTRICTED validation + COMPUTATIONAL replay. P versus NP remains OPEN.**

## Target and falsifiers

Target claim: the LSPV-1/559 four-guard firewall is sufficient to turn every recovered-checker-accepted SOURCE/AND3/XOR packet satisfying its preconditions into a source-bound semantically valid completed refutation with correctly interpreted parsed identities.

Pre-search falsifiers:

1. a guard-passing paid-ID alias changes distinct-node charging;
2. a guard-passing SOURCE-ID alias changes parent provenance;
3. duplicate-key or coercion behavior selects different checked data than the guard authenticates;
4. a bounded-mask, typed-support packet still admits an invalid AND3/XOR consequence.

The exact LSPV-1/559 guard was independently reimplemented and applied to authentic K4, the LSPV-5/479 signed-zero packet, and the LSPV-3/557 single-fixture SAT forgery.

## IDEA -> SEARCH -> ITERATE

### IDEA

Try the newest and strongest accepted SAT packet against every 559 guard, then use the signed-zero packet to separate **semantic source soundness** from **raw-byte identifier injectivity**.

### SEARCH and source authentication

Read completely:

- \`proof1.txt\`, blob \`96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b\`, 18,553 characters;
- \`proof2.txt\`, blob \`de20ffdfa952db33f63784cddd771fb45e7fc37e\`, 958,389 characters;
- issue #3 through LSPV-4/530;
- \`AGENTS.md\`, \`CODEX.md\`, and \`.codex/skills/pnp-research/SKILL.md\`;
- LSPV-1/559 report/code/raw; LSPV-2/542-544; LSPV-3/557 report/code/raw/accepted packet; LSPV-4/529-530; LSPV-5/477-479 and the original recovered checker/baseline.

The canonical root \`main.tex\` contents API again returned zero bytes, but the exact current Git blob \`5ac61c2675ed74ee76796ba3293f288c09f23c39\` was successfully fetched directly in full (1,919,865 characters). This removed the earlier manuscript-read blocker.

Primary references reviewed:

- ECMAScript 2026 specifies separate positive and negative zero values and \`Map\` key equality by SameValueZero, which merges them.
- Cousot and Cousot's abstract-interpretation framework requires a justified soundness relation between concrete and abstract semantics.
- Clarke–Grumberg–Jha–Lu–Veith CEGAR refines spurious abstract counterexamples; it does not license discarding a concretely accepted path.

Required repository deltas:

| Repository/path | Current blob | Scope |
|---|---:|---|
| \`konard/p-vs-np/scripts/proof_status.json\` | \`93b77ed3d8fe456f81c690035f45f07910a247f2\` | Formal claims remain model/assumption scoped. |
| \`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md\` | \`18d693ea71dfa433370eb7afbebc3106e32f03e5\` | The ledger explicitly denies an unrestricted P-vs-NP conclusion. |
| \`meelgroup/frat-xor/format.md\` | \`986a21aa92b62f844ef1fce852193142c41b2b1f\` | A provisional explicit proof-format boundary, not R_mix341 authority. |
| \`tanyongkiam/cake_lpr/README.md\` | \`e94f45e9aa000cd9ada12f4c771ac9daf28fe53c\` | Fixed checker/toolchain interface. |
| \`digama0/frat/README.md\` | \`0864ba034d50dbacfb1835c24d108e93d0a8bad9\` | Explicit FRAT syntax/toolchain, no historical R_mix341 transfer. |

Google Drive search for \`R_mix341 P2-D1 P2-C3 LSPV-1 559 firewall\` returned no files.

### ITERATE

No semantic counterexample to Theorem 559.1 was found. The revised conclusion is narrower:

> The four guards survive the newest SAT-forgery and signed-zero falsifiers as a sufficient semantic firewall for their declared recovered-checker subset. They do **not** authenticate raw-token identifier injectivity, cover every concrete accepted packet, or form a cost-sound lower-bound MAY abstraction.

## Independent exact replay

### Authentic K4

The original seven-fixture packet was accepted with 30,714 checks. Its K4 fixture passed all four guards against the separately parsed 163-byte strict DIMACS source and had zero models among all 64 assignments.

### LSPV-3/557 one-fixture SAT forgery

The exact 8,573-byte packet was accepted by the unchanged checker with 3,273 checks. Independent exhaustive evaluation found **64 models**, first integer mask 4,133, including the published witness.

The 559 guard rejects it immediately at G2:

\`CHARGE_NOT_BINARY_NUMBER\`.

Converting every charge to a numeric bit and the single string support at paid record 2 to an array makes the concrete checker reject. Therefore the tested counterfeit does not falsify the 559 induction.

### LSPV-5/479 signed-zero packet

The exact packet remains accepted with 30,714 checks and passes G1-G4. Independent exhaustive evaluation confirms the attacked K4 source remains UNSAT.

This is not a contradiction. The four guards reason about parsed semantic nodes. They do not claim an injective mapping from raw JSON tokens to identifiers. Thus:

$$
\text{semantic soundness of the guarded packet}
\;\not\Rightarrow\;
\text{raw-byte identifier authentication}.
$$

The packet therefore defeats any stronger raw-provenance claim, but not the stated 559 semantic theorem.

## Concrete/abstract polarity

Define \(C\) as all packets accepted by the recovered checker and \(G\subset C\) as the packets satisfying G1-G4.

The 559 theorem proves semantic soundness only for \(G\). LSPV-3/557 lies in \(C\setminus G\); LSPV-5/479 lies in \(G\) but exhibits noninjective raw-token representation. Consequently:

1. \(G\) is an **under-approximation**, not a lower-bound-safe overapproximation of all concrete derivations.
2. The 557 accepted path cannot be removed from \(C\) merely because it violates the guard.
3. The 479 path may remain semantically sound while still invalidating raw-byte provenance abstractions.
4. Promoting \(G\) to P2-C3 still requires a cost-nonincreasing source/goal-preserving normalizer from every relevant concrete accepted packet, or a complete MAY treatment of excluded packets and omitted operations.

## Resource ledger

Measured local audit costs:

| Phase | Wall time |
|---|---:|
| baseline checker | 184.53 ms |
| signed-zero checker | 147.04 ms |
| single SAT-forgery checker | 75.17 ms |
| typed-repair rejection | 60.77 ms |
| total audit before raw write | 493.06 ms |

Audit-orchestrator peak RSS was 50,488 KiB. Child-verifier CPU/RSS, GitHub retrieval/publication, caches, and indexed-machine all-phase peak work space were not measured. Logical paid work, parser bytes, source reads, exhaustive assignment checks, checker time, and physical memory remain separate quantities.

## Corpus reconciliation

**CORPUS REVIEWED.** Both trackers, current issue, governing files, relevant 539-559 reports/code/raw/handoffs, required repositories, primary ECMAScript/abstract-interpretation/CEGAR sources.

**DUPLICATION / CONTRADICTION AUDIT.** The 559 report already labels its guard an under-approximation and explicitly requests this red-team test. The 479 report already establishes the signed-zero byte alias. The new contribution is their independent joint replay against the newer, stronger single-fixture 557 SAT packet. No contradiction with either scoped result was found.

**WHAT CHANGED RELATIVE TO ROOT MAIN.** The earlier unreadable-file blocker is resolved by direct Git-blob fetch. The LSPV-5 region can now record both 479 and this validation without touching other owned regions.

**ADOPTED.** The 559 semantic theorem at its declared guarded-subset scope; the 557 SAT forgery as a concrete excluded-path control; the 479 raw-identity counterexample.

**REJECTED.** Any inference from the semantic guard to complete grammar authentication, raw-byte provenance, full P2-C3 coverage, or P2-B1.

**STALE OR OVERSTATED CLAIMS FOUND.** None in the three reports at their explicit scope.

## Status and tracker decision

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No new load-bearing node is warranted: [P2-L1-559], [P2-L3-557], and [P2-L5-479] already record the exact theorem and counterexamples. P2-D1, P2-C3, P2-B1 and separate P2-B2/B3 remain OPEN. P versus NP remains OPEN.

## Reproducibility

- \`experiments/review/lspv5_480_guard_firewall_replay.js\`, source SHA-256 \`37f5a394f4fe67af28a30fd0549a1f7c4117c673f652362bb86b70251946d5b2\`;
- \`results/raw/arc/2026-11-10_1748_LSPV5_480_GUARD_FIREWALL_RAW.json\`, source SHA-256 \`eb868d8f5aea03ca22bed4aded84330b0ec77ff22cc656428ca5857188880acc\`.

## Remaining gap

Authenticate the complete historical byte grammar and construct either a complete cost-sound abstraction or a proved non-increasing-cost normalizer covering every accepted native operation, alias, source binding, context, branch, join, deletion and shortcut. The guarded semantic subset alone cannot establish P2-C3 or P2-B1.

