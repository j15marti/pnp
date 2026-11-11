# LSPV-5/490: Independent OS replay separates the `/386` proof core from its self-test accepted-byte language

**2026-11-11 08:52 PST | LSPV-5 Independent Proof Red Team | historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## IDEA, SEARCH, and revised target

The run began with the candidate that every raw JSON number token `1` in an accepted packet could be coherently replaced by exact noninteger binary64 aliases. Four falsifiers were stated: any coordinated rejection, any parsed-object difference, any ancestry/cost difference, or acceptance immediately outside the rounding cell.

Current corpus search then found the more load-bearing unexecuted obligation in LSPV-1/574: a 10-vertex bridge-Tseitin certificate whose full original `/386` OS replay had explicitly been left to LSPV-5. The run therefore revised its target under IDEA -> SEARCH -> ITERATE:

> Independently replay `/574`; reconstruct terminal ancestry and source UNSAT from the original packet; then try the cheapest native shortcut by deleting its syntactically unused paid owner and repairing the summary from $W=103$ to $W=102$.

Precise revised falsifiers:

1. the exact published packet fails in the unchanged original CLI;
2. terminal ancestry contains all 41 SOURCE records rather than 37;
3. the reported 36-clause signed core is SAT or a one-clause deletion remains UNSAT;
4. coordinated deletion of the unused paid owner is accepted by the full CLI.

Falsifiers 1--3 failed. Falsifier 4 produced a sharper model split: the exact original `checkProof` core accepts the repaired $W=102$ packet, but the full original CLI rejects it because its bundled `gate_defs.shift()` corruption becomes a no-op on an empty owner list.

## Exact authority and independent reconstruction

- unchanged checker: `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`, SHA-256 `22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113`;
- exact LSPV-1/574 packet: Git blob `1efb525f0c84dfffb626c00e592f4952cc796c69`, 25,773 bytes, SHA-256 `8a44341472d17ed969111c0e22ffca1868d237730c5807e2137e57be2c0159eb`;
- peer theorem/report: `research/agents/lspv-1/2026-11-11_0756_LSPV1_574_NATIVE_BRIDGE_SOURCE_ANCESTRY.md`, blob `e6e175efd2b3b4e9107c64da1e1009fc604ee5ab`.

The LSPV-5 audit independently traverses parents backward from the terminal empty clause, replays all 102 signed Resolution steps, enumerates the complete 16-variable guarded source, enumerates the terminal-source core, and finds a model after deleting each of its 36 non-guard clauses.

| Independently checked object | Result |
|---|---:|
| SOURCE records present | 41 |
| SOURCE records in terminal ancestry | 37 |
| SOURCE records outside terminal ancestry | `1, 2, 21, 22` |
| Full-source models | 0 |
| Reduced-core models | 0 |
| Core single-clause deletion witnesses | 36/36 found |
| Resolution records replayed | 102 |
| Total proof records | 143 |
| Declared paid owner output | 17 |
| Occurrences of owner output in proof clauses | 0 |
| DEF facets | 0 |

Thus `/574`'s central theorem reproduces: full SOURCE presence is required by the checker, but SOURCE presence does not imply membership in the terminal proof cone. The four dead SOURCE records are genuine original clauses, not forged or omitted premises.

## Accepted-byte replay and hostile controls

The exact 25,773-byte packet was passed to the unchanged checker through a real OS Node subprocess. It accepted with:

$$
N_{\mathrm{SOURCE}}=41,\quad N_{\mathrm{RES}}=102,\quad
N_{\mathrm{owners}}=1,\quad W=103,
$$

143 records and 11,806 original assertion groups, including all 11 bundled corruption tests.

Seven hostile packets rejected:

| Hostile | Full-CLI result |
|---|---|
| coordinated owner deletion and summary repair to $W=102$ | reject: `accepted a corrupted proof` |
| owner deletion with stale summary | reject: `gate paid count` |
| owner retained with zero-owner summary | reject: `gate paid count` |
| signed SOURCE corruption | reject: `wrong source 1` |
| terminal pivot `999999` | reject: `bad pivot signs 142` |
| dangling terminal parent | reject: `bad parents 142` |
| terminal opcode `AND3` | reject: `record kind or clause at 142` |

The coordinated owner-deletion result is not a logical proof failure. Executing the exact original `checkProof` function body without the later CLI harness accepts the same repaired packet with 102 Resolution nodes, zero owners, and $W=102$. The full CLI then runs this mutation:

```js
o => { o.gate_defs.shift() }
```

and requires it to be rejected. When `gate_defs=[]`, `shift()` changes nothing; the cloned packet remains valid, so the CLI raises `accepted a corrupted proof`. Hence nonempty owner state is enforced by a meta-test, not by terminal proof dependence or a native inference premise.

## Concrete/abstract semantics and cost polarity

Two distinct concrete systems must not be conflated.

### Full CLI accepted-byte system

A complete configuration contains

$$
C_{\mathrm{CLI}}=(b,J(b),i,K,D,G,S,A,q,M),
$$

where $b$ is the raw packet, $J(b)$ the parsed object, $i$ the record cursor, $K$ known clauses, $D/G$ definition maps, $S$ authenticated SOURCE occurrence state, $A$ the assertion counter, $q$ the main phase, and $M$ the pending bundled-mutation obligations. Acceptance requires both the proof replay and rejection of every mutation in $M$.

A sound abstraction for this system must retain at least:

- all mandatory SOURCE identities, even terminal-dead ones;
- the terminal ancestry separately;
- the owner table and exact paid count;
- whether each bundled mutation is effective and rejected;
- all rule/context data actually read by the checker.

The $W=102$ owner-free path is abstractly tempting but concretely rejected by the full CLI. CEGAR may refine it away **only for this declared full-CLI language**, with the concrete replay above as evidence.

### Core proof-checking system

For the exact original `checkProof` body alone, the mutation state $M$ is absent. Its coordinated owner-free packet is genuine and accepted at $W=102$. An abstraction that excludes it merely to inherit the full-CLI owner floor would underapproximate the core language.

Therefore the abstraction/concretization pair depends on which system is the claimed historical calculus. A transformer cannot silently use the core's logical rules while importing the CLI's extralogical paid-owner floor, or use the CLI accepted bytes while discarding mutation obligations. This is a direct P2-D1 definition blocker and a P2-C3 completed-refutation-preservation blocker.

For either declared concrete system, cost-soundness still requires

$$
\operatorname{cost}^{\#}(\alpha(P))\leq \operatorname{cost}(P).
$$

The terminal-cone abstraction alone is incomplete for the full CLI because it drops four mandatory SOURCE records. Conversely, packet cardinality and record count imply no physical memory lower bound without a separate live-storage or pebbling theorem.

## All-phase resource ledger

| Phase/resource | Charged observation |
|---|---|
| source/head reads | current governance, both trackers, issue #3, current peer/Grok/Claude reports and required repositories |
| input evidence | exact 25,773-byte packet plus 6,345-byte checker |
| parsing/source authentication | complete packet parse, 41 SOURCE checks and graph/source reconstruction |
| logical replay | 102 paid Resolution nodes; one CLI-required paid owner; $W=103$ |
| core shortcut | owner-free exact core acceptance at $W=102$; not full-CLI acceptance |
| ancestry | backward traversal of 143 records; 37 live SOURCE ancestors |
| independent source check | exhaustive $2^{16}$ guarded assignments; 36 deletion-model searches |
| hostile verification | seven full OS subprocess rejects plus 11 bundled mutations in the positive run |
| construction/output | canonical hostile serialization, hashing, raw JSON ledger and report output |
| caching/retrieval | filesystem and Node runtime caches not isolated |
| peak space | not measured; no RSS or minimum-space claim |
| elapsed time | positive CLI about 0.13 s; hostile runs about 0.05--0.09 s on this host; not asymptotic evidence |

Logical work, verification work, raw bytes, assertion count, terminal ancestry, and physical space remain separate measures.

## Literature and corpus reconciliation

Cook--Reckhow supplies the proof-system rigor framework, but does not identify this archived CLI as the historical mixed calculus. Cousot--Cousot requires the abstraction to match the declared concrete semantics. Clarke et al. permits CEGAR refinement only after the candidate path is shown spurious for that concrete system. None authorizes transferring the CLI self-test owner floor into the core calculus.

Current peer work reviewed includes LSPV-1/574, LSPV-2/559, LSPV-3/572, LSPV-4/544, LSPV-5/489, and relevant 539--549 and later artifacts. LSPV-2/559 independently confirms the external-source-binding gap; LSPV-3/572 authenticates a fixed-source cycle-space quotient only for `/386`; LSPV-4/544 separates byte-query verification from native $W$. Grok's 2026-11-11 review and Claude's WORLD-LEDGER retain all unrestricted arrows as OPEN.

Change-aware required-repository review found no new commits since the previously pinned states: `konard/p-vs-np` pushed 2026-11-03, `blkph0x/p-vs-np-proof-research` 2026-10-20, and `meelgroup/frat-xor` 2026-10-23. Their scoped formalisms do not define the missing mixed dispatcher. Connected-drive search returned no relevant native-calculus artifact.

## Status

- **PROVED/RESTRICTED:** for the exact packet, all 41 SOURCE records are present but only 37 lie in terminal ancestry; records 1, 2, 21 and 22 are terminal-dead.
- **COMPUTATIONAL:** exact original OS CLI accepts the packet at $W=103$ with 11,806 assertions; all seven hostiles reject.
- **PROVED/RESTRICTED:** the exact original proof core accepts coordinated deletion of the syntactically dead owner at $W=102$, while the full CLI rejects solely through its no-op corruption-harness condition.
- **OPEN:** authentication of the complete historical $R_{\mathrm{mix341}}$ grammar, all-rule cost-sound abstraction, P2-D1, P2-C3, P2-B1, separate P2-B2/B3, and P versus NP.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The result sharpens the already-open concrete-semantics gap but does not change a tracker dependency or proof status.

## Reproduction

```bash
node experiments/review/lspv5_490_bridge_owner_cli_split_audit.js
```

Artifacts:

- `experiments/review/lspv5_490_bridge_owner_cli_split_audit.js`
- `results/raw/arc/2026-11-11_0852_LSPV5_490_BRIDGE_OWNER_CLI_SPLIT_RAW.json`
- `research/coordination/2026-11-11_0852_LSPV5_BRIDGE_OWNER_CLI_SPLIT490_HANDOFF.md`

