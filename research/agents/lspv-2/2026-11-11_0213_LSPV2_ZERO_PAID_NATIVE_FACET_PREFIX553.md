# LSPV-2/553: Original archived /386 zero-paid defining-facet prefix and exact cost-simulation obligation

**2026-11-11 02:13 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED original-code theorem + COMPUTATIONAL hosted-V8 exact-packet differential | P versus NP OPEN**

## Candidate construction and four falsifiers

**P2-D1/P2-C3 candidate:** For the genuinely accepted original archived `/386` guarded odd-K4 certificate from LSPV-1/568, prepend `k` identical *free* defining-facet records for a previously paid gate owner, before even the first SOURCE record, shift every preexisting chronological parent index, and keep each original source and paid inference unchanged. Test whether the unchanged original checker and its complete hostile-test wrapper accept the packet at exactly the same work tariff.

Registered falsifiers: F1, the checker demands that SOURCE records precede all DEF facets; F2, repeating a zero-additional-charge facet incurs additional paid logical work; F3, shifting positional parent indexes breaks chronology, a native RES premise, or the goal; F4, a wrong facet, missing owner, forged source, wrong payment, or unshifted parent is accepted. F1–F3 are refuted by the accepted packet family. F4 is excluded in the explicitly tested corruptions. No claim is made for missing historical mixed rules.

## Authentication and actual code path

The unchanged original archived `experiments/arc/lspv2_386_independent_verify.js` is pinned by Git blob `338305c0ce101704205e57543756b8127074a986`. The original-source-bound LSPV-1/568 full-CLI accepted seed is `results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_CLI29.json`, blob `e3eb2a46857776089ab83f4ad50159ef622d2869`. The signed original is guarded odd-charge K4: six edge variables, 16 original guarded source clauses, the guard source `[7]`, zero satisfying assignments, `h=4`, guard `7`, 17 SOURCE records, and 28 paid RES inferences. Its `gate_defs` is exactly `[[0,8,1,4]]`: a separately paid conservative owner for `z_8=x_1 AND x_4`. That owner is deliberately unused by the original 28-step RES proof, and raises full-CLI cost from core 28 to accepted 29 because the archived wrapper's built-in gate-owner deletion mutation must change the certificate (prior LSPV-4/535 and LSPV-1/568).

**Code inspection:** `checkProof` parses *all* `gate_defs` into `defs,gids` **before** sequentially checking `records`. It accepts every `kind:'DEF'` record with `parents:[]` and an exact canonical defining facet for any previously declared gate owner. Its DEF branch checks neither source-record chronology nor uniqueness of already-emitted facets. It increments `ndefviews`, not `nres` or `defs.size`. The final payment is `nres+defs.size`. This is an **authenticated behavior of the separate archived /386** only; the intended complete `R_mix341` checker has NOT been located.

The first defining facet of owner `[0,8,1,4]` is precisely `[1,-8]` under the original clause order comparator. For every tested `k` the resulting first `k` records are
```json
{"kind":"DEF","gate":0,"c":[1,-8],"parents":[]}
```
They can precede every SOURCE record. Their owner is still paid once through `gate_defs`, not once per facet occurrence.

## Theorem 553.1: front-loaded zero-paid facet prefix transport (PROVED/RESTRICTED)

Fix this original accepted /386 seed `P_0`. For an integer `k>=0` within the JavaScript representability and actual available-resource limits, construct `P_k` by:

1. Prepending `k` identical legal `DEF` facet records `[1,-8]`, all with no parents and `gate:0`.
2. Replacing every preexisting record's chronological parent reference `j` with `j+k`; preserving every preexisting `kind`, signed clause, `pivot`, `source`, and gate identity.
3. Incrementing only `summary.def_views` and `summary.live_records` by `k`.

Then the archived /386 `checkProof` accepts `P_k`, and the complete archived /386 command-line checker with its original eleven hostile tests accepts every physically executable `P_k` for which its seed-level hostile mutations remain effective. It has exactly

$$
N_{\mathrm{SOURCE}}(P_k)=17,\qquad
N_{\mathrm{RES}}(P_k)=28,\qquad
N_{\mathrm{facet}}(P_k)=k,
$$

$$
N_{\mathrm{record}}(P_k)=45+k,\qquad
N_{\mathrm{owner}}(P_k)=1,\qquad
\boxed{W_{386}(P_k)=28+1=29}.
$$

**Proof by inspection and positional induction:** `gate_defs` is interpreted before any proof record, so all prepended facets have a valid owner and valid canonical clause. Each new facet is parentless and satisfies the same original `DEF` check; no uniqueness condition exists. The old first SOURCE moves from record 0 to record `k`, and its original signed clause and source label are unchanged. For any original RES record `i` with parents `a,b<i`, its new record position is `i+k`, its parents `a+k,b+k<i+k`, and its previously checked signed clauses, pivot and strict resolvent remain exactly those of the original. This preserves every old DAG edge (a bijective translation by `k`), every original SOURCE occurrence, and the empty terminal clause. Exactly `k` new DEF records increment the two mechanical summary counters. The number of owner declarations and RES records is unchanged, so count-once paid logical work is exactly 29. The original full CLI's eleven built-in hostile mutations act on the same sink, original owners, original source constraints and parsed summary; for the tested values they reject all eleven hostile variants. This is not a theorem that arbitrary extra proof records can be inserted, or that an actual finite Node process accepts inputs beyond its memory/array limits.

**Restricted inverse:** For this family only, delete its known `k` unused prefix facets, subtract `k` from each surviving chronological parent, and decrement the two summary counters. This recovers the byte-level canonical `JSON.stringify` encoding of `P_0`, preserving the same signed SOURCE, DAG, sink and W. This is a deliberately restricted cost-nonincreasing normalization, not universal free-facet elimination or a full-rule normal form.

## Executed native-body matrix and concrete falsifiers

The archived original source was run in hosted V8, with a virtual file-input adapter, a semantically equivalent clone adapter for its built-in negative tests, and an **output-only noncryptographic digest placeholder**. No mathematical checker branch, source generator, RES evaluator, payment rule, or bundled hostile mutation was changed. All six positive packets passed the **complete CLI** including eleven original negative controls; all ten targeted hostile variants were rejected.

| k | accepted | bytes after exact JSON.stringify | total records | paid W | original assertions (full CLI) |
| ---: | :---: | ---: | ---: | ---: | ---: |
| 0 | yes | 2866 | 45 | 29 | 3542 |
| 1 | yes | 2916 | 46 | 29 | 3125 |
| 2 | yes | 2966 | 47 | 29 | 3167 |
| 4 | yes | 3066 | 49 | 29 | 3251 |
| 16 | yes | 3655 | 61 | 29 | 3755 |
| 64 | yes | 5968 | 109 | 29 | 5771 |

Hostile controls: incorrect facet, undefined gate, deliberately wrong RES parent reindex, nonempty facet parents, altered original signed SOURCE, wrong paid total, wrong free-facet count, removed paid owner, wrong terminal clause and wrong record count. Each was **REJECTED** by the same original CLI. Raw exact results include individual original error strings and all sixteen verdicts.

A byte-exact accepted `k=1` packet and a rejected `k=2` wrong-facet packet are published. The new standalone executable pins the original checker and seed by Git blob, generates all sixteen raw JSON byte packets under optional `--emit`, computes actual SHA-256 in Node, and invokes the original archived script using **actual OS Node subprocesses**. This standalone OS-subprocess mode was **not executed in the current hosted environment**; its JavaScript parses successfully and all corresponding original-body V8 controls were executed. No physical runtime or peak-RAM measurement is claimed.

## P2-C3 transformer obligation: exact costs versus evidence bytes

Let a concrete prefix configuration record include the immutable original signed-source binding, complete parsed gate owner bank (charged once), chronological record cursor, all prior record indices, sign/pivot-checked strict RES dependencies, context (empty in /386), terminal sink and resource ledger. Define an **exact restricted** abstraction `alpha_386` that retains owner identity, each positional RES parent, source provenance and the sink, charging `1` on each distinct RES and each paid owner and `0` on every SOURCE or DEF facet. The resulting complete-path cost for all `P_k` is `W#=29=W`; the terminal refutation is preserved. The concretization `gamma_386` includes all original byte encodings that the exact original /386 parser accepts for that typed configuration, **not** a fabricated mixed-rule accepted-byte language.

If an abstraction instead charges `1` per DEF record, its image has

$$
W^{\#}_{\mathrm{facet-paid}}(P_k)=29+k>29=W_{386}(P_k)\quad (k>0),
$$

violating the necessary **non-overcharging** polarity for all-refutation lower bounds. A cheap abstract shortcut that skips the prefix can be sound only after an explicit cost-nonincreasing normalization, as above. Conversely, the increasing accepted record lengths and JSON bytes show why proof cost alone cannot be substituted for input/certificate bits, construction time or peak writable memory. On the actual OS checker `fs.readFileSync` and `JSON.parse` materialize the file, but runtime and exact peak space were not measured. All resource measures must be charged separately.

**CEGAR:** The corrupted parent-offset packet is a *spurious* path relative to original /386, and exact chronological parent/pivot RES replay eliminates it without deleting the valid front-facet paths. By contrast the repeated DEF facet paths are native-accepted, so an abstraction may normalize them by the proved restricted inverse but may not classify them as illegal. This example is a local transition-normalization control, not a superpolynomial lower bound.

## Research comparison, source and barrier audit

Read root `proof1.txt` and complete root `proof2.txt`, coordination issue #3 and its recent comments, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, LSPV-2/539–552 and associated primary original code/corpus, LSPV-4/535–538, LSPV-5/483, LSPV-1/568, LSPV-3/565, and latest dated five-role handoffs. **Prior art:** LSPV-4/536 already established owner-charged nested paths and dead-facet deletion, and LSPV-1/568 already supplied the 29-paid accepted seed; neither result is claimed as novel. **New increment:** the original archived checker accepts **an arbitrarily extendible run of zero-charge duplicate facets before all SOURCE records** (within machine representability), while retaining a fixed 29-paid proof, plus a native exact prefix normalization and ten hostile differential controls. No analogous source chronology behavior has been authenticated for /341, full R_mix341 or external XLRUP.

Primary literature/source comparisons: Cook–Reckhow (1979), `https://doi.org/10.2307/2273702`, is about a specified proof system and its efficiency, not an R_mix341 grammar. Cousot–Cousot (1977), `https://doi.org/10.1145/512950.512973`, and Clarke et al. CEGAR (CAV 2000), `https://doi.org/10.1007/10722167_15`, frame abstract simulation/refinement but do not prove our missing full-calculus simulation. The primary FRAT-XOR/XLRUP format `https://github.com/meelgroup/frat-xor/blob/main/format.md` explicitly specifies original and deletion IDs; its syntax is a **different** calculus, not a native /386 or R_mix341 dispatcher. External repository proof attempts `konard/p-vs-np` and `blkph0x/p-vs-np-proof-research` cannot substitute for source-authenticated original checker bytes. SAT-hardness, oracle, relativization/algebrization, and natural-proofs barriers remain wholly unaddressed; no decision-model transfer follows.

## Publication, verification limits and status

- Runner: `experiments/arc/lspv2_553_zero_paid_facet_prefix.cjs`.
- Hosted V8 full 16-case raw ledger: `results/raw/arc/2026-11-11_0213_LSPV2_553_NATIVE_FACET_PREFIX_HOSTED_RAW.json`.
- Exact accepted k=1 packet: `results/raw/arc/2026-11-11_0213_LSPV2_553_ACCEPTED_PREFIX_K1.json`.
- Exact corrupted k=2 packet: `results/raw/arc/2026-11-11_0213_LSPV2_553_REJECTED_WRONG_FACET_K2.json`.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The new control clarifies a known free-facet charge/scheduling boundary and does not change any load-bearing theorem status. `P2-D1`, `P2-C3`, `P2-B1`, separate `P2-B2/B3`, `P1-01/03/04`, and P versus NP remain **OPEN**. Do not modify the five existing research automations, titles, time zones, inference weights or historic two Route A/three Route B assignments.

**Next decisive target:** recover one authentic **single** mixed-rule checker accepting a source-bound RES-to-AND3 or DEF-to-LOCAL-CONVERT transition, with at least two corrupted-port negatives; only then extend the complete-calculus abstract transformer.
