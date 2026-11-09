# LSPV-5/450: `/449` DEF-facet ownership boundary and proposed ownerized replay

**2026-11-08 19:50 PST | Route B independent red team | PROVED/RESTRICTED semantic normalization and source-boundary rejection; COMPUTATIONAL independent replay; historical `R_mix341`, all-rule lower bound, B3, and P versus NP remain OPEN.**

**Affected proof-chain IDs:** new `[P2-L5-450]`, refining `[P2-L5-449]`, `[P2-L1-522]`, `[P2-L3-520]`, `[P2-L1-520]`, `[P2-D1]`, `[P2-C3]`, and `[P2-F6]`. `[P2-B1]` and `[P2-B2]` remain OPEN. `proof1.txt` was reviewed and is unchanged.

## IDEA: initial hypothesis, prediction, and registered falsifiers

Initial hypothesis: the exact ER2 packet `[P2-L5-449]` might fail to transfer even at the semantic level because six OR-building gates use signed literals as inputs, whereas the historical `AND3`/`DEF` grammar might allow only unsigned variables or price signed ports differently.

Registered falsifiers were:

1. the historical grammar explicitly permits arbitrary conservative two-input Boolean gates, so each signed-input AND is just a truth table on two unsigned variable IDs;
2. an existing LSPV-1/3 historical accepted-byte trace instantiates the same gates and facets;
3. a native constant-size simulation replaces all signed gates with authenticated facet-owner references at the declared weights;
4. the `/449` packet in fact uses only positive inputs after exact expansion.

Falsifier 1 fired. The original `/341` declaration allows `DEF` to introduce one fresh variable as an arbitrary two-input Boolean gate. The initial signed-port concern is therefore not a semantic obstruction. Search exposed a sharper serialization defect: the published `/449` raw packet represents every definition facet as a free `SOURCE` line and contains no `DEF` record at all. This contradicts `/341`'s explicit boundary that only original DIMACS clauses are free and that later uses reference the paid definition owner, unless a separate facet-selector byte grammar is supplied. No such historical accepted-byte grammar is present in `/449`.

## SEARCH: current state, primary sources, and repository deltas

### Project state and exact artifacts

- Complete `proof1.txt` read at blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; complete `proof2.txt` read at prepublication blob `6fa6cb7ddd7defc53ffdd0bd41ae678ec4a50514`.
- Historical governing handoff read at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`; file blob `033b54b87b7cbe94912af5cf67daa52859143a07`. Current issue #3 and peer comments through `[P2-L1-522]`, `[P2-L2-510]`, and `[P2-L3-520]` were read.
- `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`, `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, research skill blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`, red-team mode blob `c211e9f545f94b636b119f1e721b475a31e925f9`, and protocol blob `25b38dc02bc0b0331ed03b0a4c7ff1b1e2a4ed00` were read completely.
- Original historical declaration: `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. It declares free original sources, paid unit `DEF`, and later references to the charged definition, but does not freeze a finite accepted-byte facet-selector language.
- Peer source packet: `research/agents/lspv-1/2026-11-08_1900_LSPV1_MOD3_VERTEX_LOCAL_SOURCE_RES522.md`, blob `ab0cd2db22f67ed57486d5048fc804813a39d5b0`; executable blob `9675adb8d277c0aef30fff18204e208db434f8be`, raw blob `0d19c78d5de3641c230c69a2e8591044feb6cf5c`.
- Peer hard-family core: `research/agents/lspv-3/2026-11-08_1925_LSPV3_MOD3_21CLAUSE_STRICT3_PORT520.md`, blob `a15fde0a43606450d07fe22b50e1a0645954ef72`; executable blob `49248d99619503d27b8e1939980cc33bb72d3654`, raw blob `c5b25ee9c861c2918d5a165532eee4d1b96f2b98`.
- Target packet: `research/main/2026-11-08_1851_MAIN_ONEHOT_MOD3_RESOLUTION_PACKET_REFEREE449.md`, blob `687128b76215b443b9a0cf8989418bbe3505d59a`; raw packet blob `48951eeb36f8990c978284855a462496777754b9`.
- Actual Grok `GROKPROOF/2026-11-08_1130_PROGRESS.md`, blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`, and Claude TPORT reports at blobs `b7150bb9ed964affd5fb90ecd24b0aa35d600bf9` and `1f9fc727d3e2b009cba7afec2a93beb62959dd67` were read. Neither authenticates the historical mixed byte grammar or supplies B3.

The local preflight was executed. The scheduled scratch directory is not a repository checkout, so it reported missing root `main.tex`, skill, `AGENTS.md`, and `CODEX.md`. GitHub complete-file reads were used instead. Root `main.tex` metadata returned blob `87081775f78ee61032a55abc8ffce806bedff245` but zero content bytes; under the publication safeguard it was not overwritten. A durable LSPV-5 insertion fallback is published separately.

### External corpus and primary literature

Change-aware repository pins: `konard/p-vs-np` `ecedd2b45f1c524d85c00b2da27a9c140025550c` with proof manifest blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research` `7dedc73f758dfbdc072e7aa29dfc08505761ebd5` with method index blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `meelgroup/frat-xor` `18cd6bc17af10a9891c10a846ce966166f9fe0dc` with format blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; `cake_lpr` `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`; `short-proof` `2c524cfceecf68b56f51d23f6b63255b502856d3`; `digama0/frat` `aa18581497830b49a6ab6cbc9e0dc778c14885b5`; `openai/math` `4eaee87548250b2682affda7d05d947c05554bae`; and `anthropics/formal-math` `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. None supplies an exact historical `R_mix341` facet-owner port or noncircular B3.

CryptoMiniSat head `97c6efeae45d93c45d2ebc3e4e83c2014c79513d` was a fresh delta. Its inspected commit changes solver heuristics, QDIMACS parsing, release/build configuration, and versioning; it provides no historical rule serialization. The direct README-at-commit fetch failed, but the complete commit metadata and patches were available and inspected. This access limitation is not disguised as a review of unavailable content.

Primary research searched and scoped:

- Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, §7.1 and Theorem 7.2(b): exponential DAG size for fixed opposite-characteristic `Res(PC_r/F_p)` on the stated mod-$q$ Tseitin expander family. This is restricted proof-system hardness, not historical mixed hardness.
- Cook's 1976 extended-Resolution pigeonhole result and Cook--Reckhow 1979: extension variables can yield short proofs in stronger systems, while `NP=coNP` supplies some polynomially bounded proof system, not necessarily this fixed one.
- FRAT/XLRUP primary format material: original clause IDs, derived clause IDs, and theory IDs are explicitly different namespaces; hints do not silently turn theory-owned constraints into original clauses. This supports keeping source identity and facet ownership explicit, but it is a distinct external calculus.

Indexed public web search was available. A separate Google-branded interface was not available and is not claimed.

## Family/theorem/encoding/known-method ledger

| Family | Exact encoding and size | Established theorem/model | Known legal shortcuts and controls | Remaining transfer |
|---|---|---|---|---|
| Pang modulo-three core `[P2-L3-520]` | Cubic oriented graph with $h$ vertices and $3h/2$ edges; three original Boolean atoms per edge; one positive ternary ALO per edge and 18 proper negative ternary forbidden-flow clauses per vertex. Exactly $39h/2$ strict 3-clauses on $9h/2$ variables; $N=\Theta(h\log h)$. | Pang Theorem 7.2(b), transferred by literal clause-subset inclusion: $\exp(\Omega(h))$ DAG size in fixed opposite-characteristic $\operatorname{Res}(\operatorname{PC}_r/\mathbb F_2)$ for fixed $r$ and the stated expander family. | `[P2-L3-520]` reconstructs every deleted AMO using 12 ordinary RES nodes. `[P2-L1-522]` exposes nine vertex clauses in an exact 18-RES local packet. `[P2-L5-449]` supplies a declared ER2 mod-3 adder. Matching-characteristic algebra and ER definitions remain shortcut controls. | Compose the source packets and adder with authenticated DEF owners, exact facet selectors, LCA cancellation/congruence, and a historical checker. Restricted hardness does not transfer to the stronger mixed system. |
| Ordinary odd cubic Tseitin | Four proper signed ternary clauses per vertex on $3h/2$ edge variables; $4h$ clauses. | Exponential ordinary shared-DAG Resolution size on appropriate expanders. | Historical `/341` declarative `AND3` plus GF(2) gives a linear source-explicit parity refutation. | Mandatory family-failure control: ordinary Resolution hardness cannot establish full mixed hardness. |
| Cook pigeonhole principle control | Standard unary PHP CNF. | Haken exponential ordinary Resolution; Cook polynomial Extended Resolution. | Paid extension variables and shared clauses. | Any proposed mixed lower bound must survive every historically legal extension shortcut, not exclude it. |

Certified UNSAT, certified proof-size hardness in a named model, and empirical solver difficulty remain distinct. No empirical difficulty claim is used.

## ITERATE: exact audit and revised claim

### Theorem 450.1 — signed-input semantic obstruction is falsified

Let $a,b$ be distinct underlying variable IDs, let $\ell_a\in\{a,\neg a\}$ and $\ell_b\in\{b,\neg b\}$, and introduce fresh $q$ with

$$
q\leftrightarrow(\ell_a\wedge\ell_b).
$$

This is an ordinary two-input Boolean function of the unsigned pair $(a,b)$. Its exact clausal facets are

$$
(\neg q\vee\ell_a),\qquad(\neg q\vee\ell_b),\qquad
(q\vee\neg\ell_a\vee\neg\ell_b).
$$

Because `/341` declaratively permits an arbitrary conservative two-input gate, all 15 `/449` gates have legal semantic truth tables. Exhaustive extraction found nine `++`, three `+-`, zero `-+`, and three `--` input-polarity patterns, corresponding to three distinct four-row truth tables. Every gate has distinct absolute input IDs and a globally fresh topologically later output. This proves only semantic admissibility, not a historical byte encoding or facet-reference interface.

### Theorem 450.2 — raw `/449` is not a source-authenticated historical trace as serialized

The compact `/449` certificate has 184 records:

- 53 records marked `SOURCE`;
- exactly eight genuine original input clauses;
- 45 defining facets marked `SOURCE`;
- zero records marked `DEF`;
- 131 oriented `RES` records.

All 45 facet clauses are absent from the eight-clause original input. Under `/341`'s stated rule that only original DIMACS clauses are free source-labelled axioms, these lines cannot be free `SOURCE` records. Consequently the raw packet as serialized cannot itself be a source-authenticated historical `R_mix341` proof. This is a precise original-source-boundary rejection, not an assertion about an unavailable parser.

The audit built a separate proposed grammar `PROPOSED-FACET-OWNER-450`: eight original sources, 15 paid DEF owners, three exact facet views per owner, and the same 131 RES nodes. It replays every parent, oriented pivot, conclusion, and target. In that explicitly new facet-addressable grammar the distinct paid-node work remains

$$
15+131=146.
$$

The adapter demonstrates that the defect is repairable with no asymptotic or node-count increase *if* historical nodes expose authenticated facet views. It does not prove that the historical accepted-byte language has such references, selector costs, or identity rules. Therefore `[P2-D1]` and `[P2-C3]` remain OPEN.

### Independent replay and hostile controls

The producer validates the original compact certificate SHA-256 `919b1df5f1a79c205199b4a6fa5b4d65962e88d49f5cd0acf016f9cdf8a45857`, reconstructs all owners, and replays the ownerized packet. Separately authored Python and Node.js verifiers independently replayed eight original sources, 45 owner facets, 15 DEF truth tables, and 131 oriented RES records. Both passed.

Hostile controls all rejected:

- one facet modified to include an alien literal;
- one required facet removed;
- one RES pivot changed;
- one DEF changed to repeated absolute input IDs;
- the raw packet presented to the original-source boundary with 45 nonoriginal free sources.

Peer executables were independently rerun from their exact GitHub blobs. LSPV-1/522 reproduced 24 cases, 3,360 JS checks, nine exact targets, and the 18-node local optimum. LSPV-3/520 reproduced 24 strict3 cases, 216 twelve-RES AMO packets, 648 rejected corruptions, 48 modulus controls, and 58,488 Node assertions. Neither peer code nor this run executes an authoritative historical checker; all three reports state that limitation.

Raw ownerized artifact size is 58,378 bytes. Producer time was 0.00628 seconds with 11,520 KiB `ru_maxrss` in this runtime. These measurements cover the local typed audit only. Literature retrieval, source/head/index reads, parsing, peer replay, failed first executions, code creation, output, publication, tracker rewriting, and readback are additional actual work. The ideal minimum still excludes discovery cost; no FLMV time/space inequality is inferred from proof weights.

## Barrier audit, status, and next target

- **FALSIFIED/RETIRED at semantic level:** signed literals themselves do not block `/341`'s arbitrary two-input `DEF` rule.
- **PROVED/RESTRICTED:** raw `/449` violates the declared free-original-source boundary because it labels 45 nonoriginal facets as `SOURCE` and contains no `DEF` records.
- **PROVED/RESTRICTED + COMPUTATIONAL:** a distinct proposed ownerized grammar replays exactly 15 paid DEF plus 131 paid RES nodes with independent Python/Node verification.
- **OPEN:** historical byte tags, owner-qualified facet selectors, reference/application charges, LOCAL/GF(2)/AND3 consumer identity, full source-to-LCA composition, all-rule superpolynomial $\overline W_R$, and noncircular same-calculus B3.

Relativization, algebraic access, arbitrary branching, reconvergence, extensions, and matching-characteristic shortcuts remain legal controls. The result is a proof-format/source-provenance boundary, not an arbitrary-machine lower bound.

**Next decisive target:** recover an actual historical accepted-byte `DEF` record with an owner-qualified clause-facet selector and run the 15-owner `/449` packet through that checker. If no such historical serialization exists, `[P2-D1]` must remain an explicit missing-definition blocker rather than being repaired by CANON2R convention.

Root `main.tex` was not edited because the connector returned its blob but no content bytes; overwriting an unreadable root file would violate the preservation contract. A durable proposed LSPV-5 insertion is saved for later conflict-safe reconciliation.

**P versus NP remains OPEN.**

## Artifacts

- Producer/audit: `experiments/review/lspv5_450_def_facet_owner_audit.py`.
- Independent Python verifier: `experiments/review/verify_lspv5_450_def_facet_owner.py`.
- Independent Node verifier: `experiments/review/verify_lspv5_450_def_facet_owner.mjs`.
- Raw complete ownerized packet: `results/raw/arc/2026-11-08_1950_LSPV5_DEF_FACET_OWNER_AUDIT450_RAW.json`.
- Handoff: `research/coordination/2026-11-08_1950_LSPV5_DEF_FACET_OWNER450_HANDOFF.md`.

## Primary references

1. Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, https://arxiv.org/abs/2610.00837.
2. Stephen A. Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4), 1976.
3. Stephen A. Cook and Robert A. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44(1), 1979, https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf.
4. Marijn Heule et al., *A Flexible Proof Format for SAT Solver-Elaborator Communication*, TACAS 2021, https://pmc.ncbi.nlm.nih.gov/articles/PMC7979213/.
