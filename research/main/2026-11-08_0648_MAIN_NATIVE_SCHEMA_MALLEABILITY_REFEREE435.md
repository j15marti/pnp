# LSPV-5/435 | Recovered `/341` schema-malleability firewall for branching claims

**2026-11-08 06:48 PST | LSPV-5 independent red team | PROVED/RESTRICTED source-code theorem + COMPUTATIONAL exact-checker replay | P versus NP OPEN.**

**Material proof-chain node:** new `[P2-L5-435]`, refining `[P2-D1]`, `[P2-D3]`, `[P2-L3-491]`, `[P2-L3-499]`, `[P2-L3-502]`, and `[P2-L5-420]`. Full historical grammar `[P2-D1]`, all-rule normalization `[P2-C3]`, full-mixed superpolynomial minimum `[P2-B1]`, and noncircular same-calculus B3 `[P2-B2]` remain **OPEN**. Cross-route `[P1-01]`, `[P1-03]`, and `[P1-04]` remain **OPEN**.

## IDEA: hypothesis, assumptions, prediction, and falsifiers

**Initial hypothesis.** A branching/shared proof packet can reduce historical $W_{R_{\rm mix341}}$ only if the authenticated native grammar has a context-introduction/discharge mechanism. I predicted that the exact recovered checker would reject branch/context/discharge syntax absent from its two recognized paid rules.

Precommitted falsifiers:

1. an exact recovered-checker packet with authenticated assumption contexts or a paid split/discharge rule is accepted;
2. ordinary Resolution derives legal unit-assumption discharge without an explicit discharge opcode;
3. branch/context annotations change the recovered checker's result or checked work;
4. an actual semantic-field mutation such as `rule: SPLIT`, one-parent inference, corrupt source, or noncontradictory sink is accepted.

**Search falsified the initial formulation by (2).** `[P2-L5-420]` and LSPV-3/448 already prove the standard proof-to-proof Resolution deduction transform: a Resolution refutation under one unit assumption can be converted to the opposite unit or contradiction without adding a `DISCHARGE` opcode. The revised question is narrower and checker-specific: does acceptance authenticate branch annotations, or merely ignore them?

## SEARCH: exact state, primary sources, and change-aware corpus review

### Project sources actually read

- Complete `proof1.txt`, blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; complete `proof2.txt`, initially blob `f643862b27cfb6fbb23564933cc25acaded47b0e`; current issue #3 through its latest page.
- Governing five-role handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`; `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`; `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`; repository research skill blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`.
- Exact recovered checker `experiments/arc/lspv2_341_independent_verify.js`, blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`; exact balanced packet `results/raw/arc/2026-11-07_2224_LSPV3_491_BALANCED_341_PACKET.json`, blob `481423a2f5271ab600bbc2f9a526fe62523239a9`.
- LSPV-5/420 sink-ancestry and Resolution-discharge audit; LSPV-5/434 context-lifted proposed-calculus report; LSPV-3/491, /499, /502 recovered-checker reports; LSPV-1/505 common-isotropic guard report; LSPV-4/495 Route-A peer handoff and report.
- Current Grok file `GROKPROOF/2026-11-08_0320_PROGRESS.md`, blob `72edb3140d8ed798d0905a827f85d3428728e396`; Claude world-ledger README, blob `de75a371ce3143a4495e6892df7fb04794a6b708`.

The local repository preflight script could not be run because this workspace did not contain a Git checkout; all exact project reads and writes used the GitHub connector. Root `main.tex` again returned blob `68188a24badda635a5983fda1c381cdb694fd497` with zero readable content bytes, so it was not edited.

### Required external repositories: pinned, change-aware review

Both newly required repositories were unchanged from the preceding run:

- `konard/p-vs-np` head `ecedd2b45f1c524d85c00b2da27a9c140025550c`; `README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95`; `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`. Its finite-machine formal results do not supply historical `/341` grammar or B3.
- `blkph0x/p-vs-np-proof-research` head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `INDEPENDENT_AUDIT.md` blob `b30515cced93d8911a6415555ee9ec1444502d93`. Its restricted experiments do not authenticate this checker.

Relevant proof/checker corpus was also unchanged: `meelgroup/frat-xor` head `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, `format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; `tanyongkiam/cake_lpr` head `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`, README blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; `peitl/short-proof` head `2c524cfceecf68b56f51d23f6b63255b502856d3`; `openai/math` head `4eaee87548250b2682affda7d05d947c05554bae`; `anthropics/formal-math` head `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. No build or authoritative external checker execution was claimed.

Primary sources reviewed:

1. Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2: the lines and rules are syntactic, and size is DAG nodes. Its lower bounds are for specified $\operatorname{Res}(\operatorname{PC}_r/\mathbb F_p)$ systems, not arbitrary JSON annotations or historical $R_{\rm mix341}$.
2. FRAT-XOR `format.md`: the grammar enumerates recognized record forms, and XOR steps are checked by a designated backend. It is a distinct format, not authority for `/341`.
3. `cake_lpr` README: the verified checker has explicit invocation, toolchain pins, and failure behavior. A verified checker for a different grammar does not authenticate ignored `/341` metadata.

Actual web queries targeted Pang's theorem, the FRAT-XOR syntax, CakeML/LPR trust boundaries, and Res(lin) rule definitions. No Google-branded native search client was available; this limitation is explicit.

### Duplication and contradiction audit

- `/420` already eliminated an unreachable-proof-padding attack and independently validated pure-Resolution unit discharge. Neither result is re-claimed.
- `/491` already established exact recovered-checker acceptance for balanced unconditional SOURCE/AND3/XOR packets.
- `/499` added an external source binder and range firewall; `/502` proved a post-acceptance affine-mask quotient. Present work concerns a different dimension: **unread JSON properties and forged descriptive/version fields**.
- `/434` is valid only in its distinct proposed context/extension calculus. Present work blocks treating an accepted `/341` packet with added annotations as historical authentication of `/434`.

## ITERATE: exact theorem and proof

Let $V$ be the exact recovered checker blob above, and let $\pi(P)$ be the projection of JSON packet $P$ onto every property actually read by $V$: graph, charges, clause records, proof IDs, `parents`, `rule`, factor/affine payloads, deletion witnesses, even witness, properties, and summary. The source contains no read of `context`, `assumptions`, `discharged`, `branchDAG`, `rule_alias`, or `paid_weight_override`; its only paid rule branch is

$$
\texttt{rule = AND3}\quad\text{or}\quad\texttt{rule = XOR},
$$

and every other actual `rule` value throws `unknown rule`.

**Theorem `[P2-L5-435]` (schema projection).** For every JSON packet $P$ parsed successfully and every metadata extension $M(P)$ that changes no property in $\pi(P)$,

$$
V(M(P))=V(P).
$$

**Proof.** JavaScript object property lookup is extensional in the properties requested by the program. Inspecting the complete checker gives a finite set of reads. The execution path, values used in every assertion, constructed maps, ancestor set, source-essentiality tests, output object and serialization therefore depend only on $\pi(P)$. Adding or replacing properties outside that projection cannot alter any expression evaluated by $V$. Conversely, changing the actual `rule`, parent arity, source literal, or sink row reaches an explicit rejection assertion. This proves the claim for the exact source blob, not for an imagined historical full parser. $\square$

**Corollary.** Exact checker acceptance authenticates the unconditional SOURCE/AND3/XOR proof actually read. It does **not** authenticate branch scope, assumption discharge, native weights supplied in extra fields, the top-level `version`, or the prose `definition`. An accepted packet may contain such text, but it has no checked semantic force. A future branching format needs either a strict schema rejecting unknown fields or an explicit canonical projection/hash plus a separate branch/context validator.

This is **not an unsound accepted refutation**: each accepted mutant retained the same valid unconditional proof. It is a provenance/schema malleability counterexample to promoting ignored annotations into native rules.

## Exact computation and hostile controls

The unmodified recovered checker was executed as a Node process on the exact 197,431-byte packet. Baseline: 30,714 checks; stdout SHA-256 `af477923155e6e4340a643a4df5b437751b443f03993bbc04dbe73c8587bf7be`.

Python generated eight byte-distinct mutants and required stdout to be byte-for-byte identical to baseline:

1. forged `version` and `definition` claiming native SPLIT/DISCHARGE;
2. cyclic ignored branch DAG with one omitted AND case;
3. one-sided context on every inference;
4. inconsistent `x=0,x=1` context at each sink;
5. fake assumption/discharge/join annotations;
6. branch-local source annotations;
7. declared cross-branch reuse;
8. fake rule alias and zero-weight override.

All eight accepted with identical output. Four semantic mutations rejected: actual `rule: SPLIT`, one-parent inference, noncontradictory sink, and corrupt source literal. An independently authored JavaScript replay accepted six ignored-field mutants, rejected the same four semantic classes, and statically confirmed the six branch-related field names are absent from checker source.

Python elapsed 1.68 seconds in the first recorded run, later reproduced after canonical-path fallback repair; peak Python RSS 14,044 KiB. Each checker subprocess was individually bounded to 15 seconds and the full run remained below 30 seconds. Logical nodes did not change; explicit bytes increased by up to 23,754 in the fake-rule-alias mutant. This reinforces `[P2-D3]`: checked logical work and unvalidated evidence bytes are different resources.

## Established-family / theorem / encoding / method ledger

| Family | Exact encoding and size | Published hardness model | Known shortcut/control | Remaining transfer |
|---|---|---|---|---|
| Odd-charge cubic Tseitin, recovered packet | One edge variable per edge; four proper signed width-3 forbidden-parity clauses per vertex; $E=3h/2$, $4h$ clauses, encoded length $\Theta(h\log h)$ with compact IDs | Exponential ordinary shared-DAG Resolution on suitable expanders; not full mixed hardness | Exact accepted SOURCE/AND3/XOR proof has $4h-1$ paid binary nodes for bridgeless fixtures | Historical RES/DEF/LOCAL/context grammar and all-rule hardness remain open |
| Pang random proper 3-CNF | Published random width-3 family with linear clause density and exact theorem parameters in arXiv:2610.00837v2 | Exponential size in specified syntactic $\operatorname{Res}(\operatorname{PC}_1/\mathbb F_2)$ | Affine guards, extensions, Resolution and mixed shortcuts must all be admitted when legal | No lower-bound preservation into full historical $R_{\rm mix341}$ |
| Pang q=2 one-hot Tseitin | Three Boolean indicators per edge and seven clauses of width at most three per cubic vertex: $3h$ variables, $7h$ clauses | Exponential only in the stated $\operatorname{Res}(\operatorname{PC}_r/\mathbb F_3)$ model/expander hypotheses | Project R-cast/RES-to-affine constructions are upper controls in distinct calculi | Historical cross-type ports and exact source-preserving transfer open |

Certified UNSAT, proof-size hardness, and empirical/checker acceptance are kept separate. None of these restricted results is an arbitrary-algorithm lower bound.

## Resource ledger

- Logical work: unchanged paid node counts and checker output for accepted metadata mutants.
- Explicit evidence: packet reads from 197,431 bytes to at most 221,185 bytes; every byte was parsed by JSON, but the added properties were not semantically checked.
- Construction/search: Python deep-copy/serialization plus 13 bounded Node checker runs; independent JavaScript performed 11 runs and static source checks.
- Verification: baseline 30,714 assertions per accepted/rejected execution until completion/failure; exact semantic mutation failures recorded.
- Source/index/head: full local packet/checker reads; no native FLMV machine interpretation claimed.
- Peak space: Python recorded 14,044 KiB; Node child peaks were not separately instrumented and are not hidden inside logical work.
- Publication/readback and GitHub source acquisition are charged administratively, not mistaken for $W_R$.

## Tracker and manuscript disposition

`proof1.txt` was fully reviewed and has no material change. `proof2.txt` has a material evidence/gap refinement: add `[P2-L5-435]` and state that ignored branch/context fields cannot authenticate historical branching rules. The exact complete prospective tracker is saved before the SHA-guarded update, then the current blob is refetched, merged conflict-safely and read back completely. Affected IDs are posted to issue #3.

Root `main.tex` could not be safely reconciled because the connector returned zero content bytes for blob `68188a24badda635a5983fda1c381cdb694fd497`; it was left untouched.

## Actual advance, status, and precise next gap

**Actual advance:** an exact source-code theorem plus two independent executions show that recovered-checker acceptance is invariant under arbitrary unread branch/context/discharge metadata, including forged version/definition claims. Actual semantic rule mutations still reject. This establishes a precise authentication boundary and prevents an accepted unconditional packet from being misreported as accepted historical branching evidence.

**Precise next gap:** locate original historical bytes specifying RES, DEF facets, LOCAL-CONVERT, exported/private wires, and any context/discharge interface, then produce an accepted packet in that exact grammar or a legal typed counterexample. Only then can `[P2-C3]` attempt a full source-retracting normalization; `[P2-B1]` and noncircular `[P2-B2]` remain independently OPEN. **P versus NP remains OPEN.**

## Reproducible artifacts

- `experiments/review/lspv5_435_native_unknown_field_malleability.py`
- `experiments/review/verify_lspv5_435_unknown_field_malleability.mjs`
- `results/raw/review/2026-11-08_0648_LSPV5_435_NATIVE_SCHEMA_MALLEABILITY_RAW.json`
- `research/coordination/2026-11-08_0648_LSPV5_NATIVE_SCHEMA_MALLEABILITY435_HANDOFF.md`

## Primary references

1. Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, 2026.
2. Ben-Sasson and Wigderson, *Short Proofs Are Narrow--Resolution Made Simple*, JACM 48(2), 2001.
3. Urquhart, *Hard Examples for Resolution*, JACM 34(1), 1987.
4. FRAT-XOR format specification, `meelgroup/frat-xor/format.md`, pinned above.
5. `cake_lpr` verified-checker README and pinned CakeML/HOL4 release information, pinned above.
