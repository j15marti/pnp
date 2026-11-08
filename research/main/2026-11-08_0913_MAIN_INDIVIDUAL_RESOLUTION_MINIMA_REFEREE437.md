# LSPV-5/437: exact individual Resolution minima do not close the joint shared-DAG gap

**2026-11-08 09:13 PST | PROVED/RESTRICTED + COMPUTATIONAL | Route B independent red team | P versus NP OPEN**

**Affected tracker IDs:** new `[P2-L5-437]`; evidence/gap refinement of `[P2-L1-508]` and `[P2-L1-507]`. Governing open nodes `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]` remain OPEN. Route-A nodes `[P1-01]`, `[P1-03]`, `[P1-04]` were reviewed and have no material change.

## IDEA: proposed repair and prior falsifiers

Initial hypothesis: the source-retraction theorem in `[P2-L5-436]` might extend without overhead from context-free ordinary Resolution DAGs to branching/reconvergent chains. Assumptions were exact historical split/discharge bytes, context-labelled lemma reuse, both sides of every AND split, and original-source authentication. Prediction: every legal branching proof could be substituted and retracted with no more paid nodes. Four precise falsifiers were fixed before search:

1. substitution erases a branch assumption without an authenticated native discharge;
2. a shared lemma is reused under a context that does not justify its assumptions;
3. one required side of an AND split is omitted;
4. the historical accepted bytes contain no context/split/discharge rule supporting the proposed translation.

Search found only polynomial proof-system simulations, not the needed node-preserving native historical translation. The hypothesis was therefore narrowed, not promoted: independently optimize the newest *context-free* ordinary-Resolution control `[P2-L1-508]`, where no split/discharge rule is assumed.

## SEARCH: authenticated project, literature, repository and tool review

### Project continuity and exact tracker reads

- Initial scheduled-run main head `51e5c515c60d52fe4753f45dcfe00ff19cb34487`; later prewrite head `6899b3f62d50d1f1a2d91275067c47e77f144f46`.
- `proof1.txt` was read completely: blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 UTF-8 characters.
- `proof2.txt` was read completely initially at blob `8c744c3c90ed364cb34e1b217d3d1012c294ebd0`, then refetched completely before writing at blob `6aa2a009f92d275db416fe86ac670acae32a3f31`, 455,553 characters. The exact second prewrite is preserved at `research/main/outbox/2026-11-08_0913_LSPV5_437_PROOF2_PREWRITE_EXACT.txt`.
- Governing five-role handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, current issue #3 through page 14 plus empty page 15, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, latest LSPV-1/3/4/5 reports and handoffs, `GROKPROOF/2026-11-08_1130_PROGRESS.md` (blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`), and `research/agents/claude/world-ledger/README.md` (blob `de75a371ce3143a4495e6892df7fb04794a6b708`) were actually read. Paths were discovered from the repository rather than guessed.
- Exact peer inputs: `[P2-L1-507]` report `research/agents/lspv-1/2026-11-08_0800_LSPV1_RECONVERGENT19_RES_UPPER507.md` (blob `92044b7862f7bf7f1b4e6cbece6b5e2263a8566b`), verifier `experiments/arc/lspv1_507_reconvergent19.cjs` (blob `18a3f1019b3ad9f940b58ac321de7afdcd8c70c1`); `[P2-L1-508]` report blob `d81b6f8a5dc5a5a9daaf4665a48aec60a37aec0d`, verifier blob `9c1d6adbe5543d1dd1c856d20b9e85ef36f3179f`; `[P2-L3-505]` report/code/raw blobs `04a339fa37479131da2e18ebc13000bb29427d7c`, `3af7b71fbe78b6a9f7b579928dbe9d20bd55fa14`, `fca0bf1d464998b69939847f995018c4cf4f0f38`.

Evidence-path audit: `[P2-L1-508]` cites raw blob `9a7417975fe1da902feef91b0e17829eba222898`. Direct blob fetch succeeded and returned the advertised 438-assertion JSON. Fetching the cited path `results/raw/arc/2026-11-08_0828_LSPV1_RELATIVE_SOURCE_CRITICALITY_RAW.json` from current `main` returned HTTP 404. Thus the evidence content exists as an orphaned/reachable-by-SHA blob, but its reported repository path is not currently readable. This is a publication-path gap, not a mathematical counterexample.

### Primary literature and actual queries

Queries included `DPLL clause learning Resolution polynomial simulation branching proof DAG`, `shortest Resolution proof SAT encoding Peitl Szeider`, `Resolution DAG source leaves multi-root lower bound`, and `PySAT proof logging get_proof DRUP`. Actual theorem/format reads included:

- Beame, Kautz and Sabharwal, *Towards Understanding and Harnessing the Potential of Clause Learning*, JAIR 22 (2004): DPLL gives tree-like traces; clause learning/restarts can polynomially simulate Resolution under stated models.
- Buss, Hoffmann and Johannsen, *Resolution Trees with Lemmas* (2008): unrestricted DAG Resolution equivalences are model-qualified; regular restrictions matter.
- ECCC TR23-052 (2023): merge-resolution/CDCL simulation can have linear overhead and some quadratic overhead is necessary.
- Peitl and Szeider, *Finding the Hardest Formulas for Resolution*, JAIR 72 (2021), and the corresponding shortest-proof SAT encoding.

These results support only polynomial simulations in specified systems. They do not authenticate a zero-overhead branching/discharge extension of historical `R_mix341`. A dedicated Google-branded client was unavailable; public web research was used and that limitation is recorded rather than disguised.

### Required and rotating repository review

Change-aware exact-file review found no relevant delta closing the historical native-rule or B3 gaps:

| Repository/path | Blob | Result for this run |
|---|---|---|
| `konard/p-vs-np/scripts/proof_status.json` | `93b77ed3d8fe456f81c690035f45f07910a247f2` | Explicitly tracks allowed axioms/proof status; no authenticated `R_mix341` simulation. |
| `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` | `18d693ea71dfa433370eb7afbebc3106e32f03e5` | Method inventory only; no accepted P-versus-NP proof. |
| `blkph0x/p-vs-np-proof-research/INDEPENDENT_AUDIT.md` | `b30515cced93d8911a6415555ee9ec1444502d93` | Uniform constructive transfer remains open. |
| `meelgroup/frat-xor/format.md` | `986a21aa92b62f844ef1fce852193142c41b2b1f` | Provisional FRAT-XOR theory format; a separate grammar/checker, not historical authority. |
| `tanyongkiam/cake_lpr/README.md` | `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c` | Verified LPR checking has an explicit CakeML trust boundary; no same-calculus B3 bridge. |
| `peitl/short-proof/short.py` | `6508dae79e341d7015949d5919de29a132fbf267` | Actual shortest-proof SAT encoding inspected and reused as a methodological control. |
| `pysathq/pysat/README.rst` | `fefde10b1426a92a21425029892f3f49466bf03c` | Solver API/proof-logging capability only; a solver result is not a universal lower bound. |
| `openai/math/README.md` | `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` | Formal-math research tooling, unrelated to the missing transfer. |
| `anthropics/formal-math/README.md` | `1df53bfc14a022088d1b5757698f692bf79390b4` | Lean-project/toolchain information, no relevant theorem. |

Repository titles, build badges and claimed solutions were not treated as authority. Google and code execution are claimed only where actually available; local Python and Node executions are itemized below.

## ITERATE: exact individual minima, and why they do not add

Use exactly the `[P2-L1-507]/[P2-L1-508]` 16 original proper signed 3-CNF clauses on variables 1 through 7 and the three advertised goals

$$
Q_0=(-1,-3,7),\qquad Q_1=(1,-7),\qquad Q_2=(3,-7).
$$

An exhaustive 128-assignment deletion check independently recovered these exact goal-relative indispensable-source sets:

$$
\begin{aligned}
E_0&=\{S02,S03,S05,S07,S10,S11,S13,S14\}, &&|E_0|=8,\\
E_1&=\{S00,S01,S08,S09,S12\}, &&|E_1|=5,\\
E_2&=\{S00,S01,S02,S03,S04,S06,S08,S09,S10,S11,S12,S15\}, &&|E_2|=12.
\end{aligned}
$$

For every cited source, the raw artifact contains a total assignment satisfying all other 15 sources while falsifying the corresponding goal. Therefore every sound source-authenticated derivation of that goal must have all sources in its $E_i$ ancestry.

**Binary-fanin lower lemma.** In an acyclic dependency DAG for one root, with $m$ indispensable source leaves and $q$ non-source nodes of indegree at most two, there are at most $2q$ premise edges. Every source and every non-root derived node in the root ancestry has outdegree at least one, so there are at least $m+q-1$ edges. Hence $q\ge m-1$.

The Python dynamic program independently enumerated every exact non-tautological binary-Resolution tree obtainable by partitioning the relevant indispensable leaves. It found floor-meeting source-indexed witnesses of 7, 4 and 11 nodes. The 11-node $Q_2$ certificate is a genuine improvement over deriving $Q_2$ through the 12-node portion of the published joint 19-node proof. Consequently, in **ordinary exact binary Resolution only**,

$$
W_{\mathrm{Res}}(Q_0)=7,\qquad W_{\mathrm{Res}}(Q_1)=4,\qquad W_{\mathrm{Res}}(Q_2)=11
$$

for this fixed source interface, where each goal is optimized separately.

Independent Node replay performed 145 assertions: all 128-assignment deletion controls, every oriented inference and topological premise, exact root ancestry, and three corrupted pivot/source/goal controls passed. The historical `/341` checker was **not** run.

### Independent challenge and revised claim

The individual minima cannot be summed. A valid joint DAG may share derived nodes, and `[P2-L1-507]` already derives all three roots in 19 nodes, less than $7+4+11=22$. Conversely, a lower bound of 11 for the hardest individual root does not improve `[P2-L1-508]`'s joint arity floor 13. Six exact 18-node SAT-encoding cases (three choices for the last goal under two solvers) were attempted and interrupted at the scheduled-run host-time budget without SAT/UNSAT status; they are failed search policies, not evidence. The defensible revised claim is therefore only the exact individual triple `(7,4,11)`. The joint minimum remains **COMPUTATIONALLY OPEN within `13 <= q <= 19`**.

This context-free audit neither proves nor refutes the initial branching hypothesis. Without authenticated native split/discharge bytes and context scope rules, the `[P2-L5-436]` source-retraction theorem must remain restricted to ordinary shared-DAG Resolution.

## Family/theorem/encoding/known-method/remaining-transfer ledger

| Family/control | Exact 3-CNF encoding and size | Established theorem/model | Legal shortcuts and controls | Remaining transfer |
|---|---|---|---|---|
| Odd-charge cubic-expander Tseitin | One edge variable per edge; each degree-3 parity constraint expanded to its four falsifying-assignment width-3 clauses. For $h$ vertices: $3h/2$ variables, $4h$ clauses, $\Theta(h\log h)$ binary bits. | Exponential ordinary shared-DAG Resolution lower bound for suitable expanders (Urquhart; Ben-Sasson--Wigderson width/size framework), model-qualified. | GF(2) elimination and the declared source-local factor proof are mandatory upper controls. | Transfer through every legal historical `R_mix341` rule and branching/shared context remains OPEN. |
| Haken pigeonhole | Standard PHP CNF is not native 3-CNF; any 3-CNF reduction needs a cited lower-bound-preserving simulation, not equisatisfiability alone. | Exponential ordinary Resolution lower bound for the stated PHP encoding. | Cook's polynomial extended-Resolution proofs are mandatory shortcut controls. | No unrestricted mixed-calculus lower bound follows. |
| `[P2-L1-507]/[P2-L1-508]` cancellation gadget | Exact 16 signed proper width-3 clauses, 7 variables; satisfiable with 8 models. | No hardness theorem. New exact **individual** ordinary-Resolution minima `(7,4,11)`; existing joint `13..19` sandwich. | Sharing saves at least 3 nodes versus the sum of individual minima; 19-node reconvergent proof remains the best authenticated joint upper. | Exact joint optimum, historical native acceptance, full mixed transfer and B3 remain OPEN. |

Certified UNSAT, proof-size hardness and empirical solver difficulty are separate categories. The current gadget is SAT and is only an interface/upper-control test. No restricted proof lower bound is described as hardness for all algorithms.

## Shared-DAG, OR/AND and resource accounting

- The three goal obligations are an AND: all must appear. Alternative proofs of a fixed goal are OR choices, and the ideal minimum may choose the best legal one after the fact at no discovery charge.
- The published certificates are context-free Resolution DAGs. No case-split, weakening, discharge, or branch-local-to-global rule is added to historical `R_mix341`.
- Distinct inference-node work, critical-path span and realizable schedules remain separate. The individual witnesses have 7/4/11 nodes; their depths and storage are reported in raw form rather than conflated with the 19-node joint span-four certificate.
- Python DP: 1.56 seconds wall time on the recorded host run, 14,464 KiB maximum RSS, 27,212 aggregate reachable `(source-mask,clause)` states across the three searches, 7,470-byte raw JSON. Node replay: 145 assertions and three hostile controls.
- Charged phases include complete tracker/source/head/index reads, source parsing, 128-assignment deletion searches, tree-state construction, inference verification, raw/report/handoff/output generation, publication reads/writes, and full readback. The PySAT environment install and six interrupted joint-optimizer processes are charged failed policies. Caches and solver memory are not converted into a claimed machine exponent.
- An exploratory 19-node SAT-encoded witness replay used 72,163 clauses, 5,263 variables, 43.72 seconds and about 70,180 KiB RSS; it only reproduced the known upper certificate. The unfinished 18-node searches have no status and are excluded from mathematical evidence.
- No FLMV same-machine claim is made. No inference-weight value is converted automatically into time or space.

## Status and handoff

**Actual advance:** exact goal-relative ordinary-Resolution minima `(7,4,11)` with explicit source-indexed witnesses, independent deletion authentication and corrupt-certificate controls; plus identification of a current 404 path for the otherwise retrievable `[P2-L1-508]` raw blob.

**Publication artifacts:**

- `experiments/review/lspv5_437_individual_resolution_dp.py`
- `experiments/review/verify_lspv5_437_individual_resolution.mjs`
- `experiments/review/raw/lspv5_437_individual_resolution_results.json`
- `research/coordination/2026-11-08_0913_LSPV5_INDIVIDUAL_RESOLUTION_MINIMA437_HANDOFF.md`

**Precise remaining gap:** prove or refute the joint 18-node bound in ordinary Resolution; authenticate historical native RES/LOCAL/DEF/split/discharge bytes; then either prove a lower-bound-preserving translation across **all** legal mixed rules or exhibit a legal shortcut. Independently, a noncircular same-calculus B3 implication remains OPEN. `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]` remain OPEN. **P versus NP OPEN.**
