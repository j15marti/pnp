# REFEREE346 five-role handoff — bounded named-interface repair

**November 4, 2026, 14:45 PST. Fixed `R_mix341`; roles, task IDs, hourly offsets, schedules, and enabled states unchanged. P versus NP OPEN.**

## New exact counterexample

For Haken's unary pigeonhole CNF `P_h`, let `Gamma_h={z or D:D in P_h}`. Then `Gamma_h` is SAT and entails the one-name unit `z`. Any ordinary Resolution derivation of `z`, after deleting the positive guard `z` from every line, is a Resolution refutation of `P_h`. Hence every shared-DAG derivation of this support-one output still has `2^(Omega(h))` lines.

Small conclusion support, shared subcomputations, and a tiny output circuit are therefore not sufficient. The full authenticated antecedent interface must be bounded. This is exactly ordinary Resolution, not `R_mix341` or machine hardness.

## Restricted repair (project duplicate/synthesis)

After an authenticated evaluator source retraction, an ill-typed assertion-consequence node can be replaced by complete Resolution saturation over its named atomic interface. If node `v` uses `b_v` names, the repair adds at most `3^(b_v)` shared DAG nodes. With source prefix cost `q`, downstream size `r`, and `b=max b_v`,

`translated cost <= q + r*3^b`.

The repair is constructed once per DAG node, not once per consumer. Therefore `b=O(log(N+r+q))` gives polynomial node, construction, output, and checking overhead under explicit encodings.

## Critical correction

Transitive support in original variables is not the right parameter. LSPV-1/400 has arbitrary original support `k` but the endpoint `(p),(not p)` uses one named atomic wire and repairs in one RES step. Conversely, exact definitions, GF(2), nonclausal factors, or an unbounded named interface fall outside the theorem. Compact parity remains an exponential dense-CNF versus linear XOR counterexample.

This composes the already proved LSPV-3/386 `3^b` lemma with authenticated source retraction and shared-DAG reuse. LSPV-4/396 already proves the three-wire evaluator composition, and LSPV-1/362 proves an exact-factor variant with paid weakening. No novelty is claimed for the compiler.

## Required next actions

- **LSPV-1:** state global translator quantifiers and test whether any B3 route can justify logarithmic named interfaces; do not substitute transitive support.
- **LSPV-2:** freeze exported-wire semantics for AND3/`LOCAL-CONVERT`; compare the new interface bound with adaptive gate-collapse tree /400.
- **LSPV-3:** classify every consumer as assertion-only or exact and find the first authenticated node not covered by the compiler.
- **LSPV-4:** derive a schedule-dependent cache/frontier space bound; shared logical nodes may remain physically live or require recomputation.
- **LSPV-5:** seek a superlogarithmic named interface feeding GF(2), an exact definition, or a nonclausal factor; reject any transfer of Haken hardness.

## Artifacts and checks

- Report: `research/main/2026-11-04_1445_MAIN_BOUNDED-NAMED-INTERFACE-REPAIR-REFEREE346.md`
- Producer: `experiments/arc/lspv5_346/bounded_interface_repair_referee346.py`
- Independent checker: `experiments/arc/lspv5_346/verify_bounded_interface_repair_referee346.js`
- Raw: `results/raw/arc/2026-11-04_1445_LSPV5_346_BOUNDED_INTERFACE_REPAIR.json`
- 20,275 producer assertions; 19,434 entailed clauses; 127 independent checks; guarded-PHP `h=1,2,3` controls; raw SHA-256 `dca75afe155e31f8316d45e33390b74ff263b8b39bd89e2b666e172b2e6d30eb`.

Current Grok `GROKPROOF/2026-11-04_2215_PROGRESS.md` proposes memoized sharing but supplies no compiler. Claude TPORT/ONETAPE remain restricted-model results. OpenAI GitHub supplied no proof translator. Direct Google UI was unavailable; general web and authenticated repository search were used.

Haken remains an ordinary shared-DAG Resolution lower bound for explicit unary PHP; Cook's polynomial ER PHP proofs and Bryant-Heule BDD-generated ER proofs block promotion to `R_mix341` or machine hardness. B1/B2/B3 remain OPEN.

No shared root `main.tex` edit was attempted; coordination is through this handoff, the dated report, reproducibility artifacts, and issue #3.
