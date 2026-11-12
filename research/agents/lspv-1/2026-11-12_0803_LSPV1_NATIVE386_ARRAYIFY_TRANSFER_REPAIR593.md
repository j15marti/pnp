# LSPV-1/593: Arrayification is necessary in the claimed universal core-to-CLI proof lift

**2026-11-12 08:03 PST | General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED pinned-checker theorem + COMPUTATIONAL hosted original-body replay. P versus NP OPEN.**

**Affected obligations:** P2-D1 restricted accepted-byte semantics and P2-C3 concrete-state/CEGAR precision. P2-B1 remains OPEN, and P2-B2/B3 remain separately OPEN. No full historical `R_mix341` rule has been authenticated.

## Pre-search candidate and falsifiers

**Candidate.** The LSPV-4/542 universal *explicit transformation* (fresh unused owner if absent, final signed pivot reversal if needed) is incomplete for some raw JSON packets accepted by the original /386 mathematical core. Its output is still a numeric-indexed **object** rather than an **Array**, and the complete CLI crashes during an embedded hostile mutation. A new zero-paid Arrayify transformation, composed before /542's original repair, restores the universal parsed-packet claim with the same at-most-one extra paid owner.

**F1:** the numeric-key object with length 45, or its string/fractional-length counterparts, fails original mathematical `checkProof`. **F2:** the unmodified /542 transformation passes full CLI without changing that object into an Array. **F3:** Arrayify changes signed SOURCE occurrences, RES parents, paid owner identities or exact work. **F4:** Arrayify plus the existing gate-owner and pivot repairs still fails the 11 original CLI mutations, including the pivot +999999, or accepts a forged source. The eight hosted differential cases refute F1-F4 in their represented subclasses. The universal result below follows separately from pinned-source inspection, not finite coverage.

## Original authority, prior work and precise contradiction

The exact original sibling /386 checker is `experiments/arc/lspv2_386_independent_verify.js`, Git blob **338305c0ce101704205e57543756b8127074a986**. The original accepted guarded K4 witness is `results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json`, blob **318c52d99977ea4e91bc8554051138a700c1dc94**. An independently supplied ordered signed source is `results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf`. The fixture has 17 signed SOURCE records, 28 RES deductions, one terminal-dead paid owner, 45 records and W=29.

**Prior work, not rediscovered:** LSPV-1/577 already proved the exact Array.isArray condition in the original full CLI; LSPV-5/505 independently replayed its counterexample and falsified LSPV-1/591's stale unqualified two-condition theorem. LSPV-4/542 previously proved the at-most-one owner transfer using the incomplete /571 criterion, and explicitly quantified over *every parsed core-accepted packet*. LSPV-2/574 already gave ownerless W28 mathematical-core refutations and W29 wrapper-accepted versions. LSPV-1/590 supplies a distinct pruning theorem that retains an original owner sentinel.

**New correction:** Apply the already proved /577 object counterexample **to the exact /542 transformation itself**, then prove a corrected universal transform with explicit Arrayify and replay its conjunction with owner/pivot repairs, including string/fractional object-length cases. Do not attribute discovery of the wrapper type defect or ownerless padding to this report.

## Proposition 593.1: the literal /542 transformation is not universal

Take the original W29 K4 packet. Delete its unused AND2 owner and reduce `summary.paid_gates` to 0 and `summary.paid_total` to 28. Convert `records` to a JSON object with numeric keys 0 through 44 and `length:45`. Every original SOURCE, RES clause, source index, pivot, parent and summary.live_records remains unchanged. The unchanged pinned mathematical checker accepts it with **W=28**.

Apply precisely the *two steps printed in LSPV-4/542* without altering `records`: append a legal paid unused AND2 owner [0,8,1,2] and increment the two paid summary fields, then conditionally reverse a final +999999 pivot (not needed for this initial K4). The new mathematical core accepts with W=29. The complete unchanged CLI nevertheless rejects because its first hostile mutation invokes `records.at(-1)` on a plain object. Thus the *literal universal transform* /542.1 is **FALSIFIED as unqualified** over all parsed core-accepted packets.

This does **not** refute /542's existential work inequality; a corrected representative exists.

## Theorem 593.2: exact arrayification and at-most-one charged repair

Fix the pinned /386 original implementation and any finite ordinary JSON value P for which the original `checkProof(P,{control:true})` accepts. Let N be the number stored in `P.summary.live_records`. Define the uncharged container normalization

```javascript
A(P).records = Array.from({length:N}, (_,i) => P.records[i]);
```

with every other parsed value unchanged. Let T(P) be the subsequent original /542 construction: if the gate-owner bank is empty, add one fresh unused, source-legal conservative AND2 owner with inputs original variables 1 and 2 and increment the two paid counters; if the terminal signed RES pivot is numeric +999999, negate it and reverse the ordered parent references. No other record may be changed.

Then for **every** such core-accepted parsed P,

$$
\operatorname{CLI}_{386}(T(A(P)))=\mathrm{ACCEPT},
\qquad
W(T(A(P)))=W(P)+\mathbf{1}_{\{\mathrm{gate\_defs}(P)=\varnothing\}}.
$$

The original in-band source specification, ordered signed SOURCE occurrences, all existing RES nodes, all original owners and facets, all assumptions available in this restricted grammar (none), and all source/proof-DAG parent identities remain intact. Only the proof-record **container** (possibly), one fresh terminal-dead owner (possibly), and orientation/order of the terminal RES parents (possibly) change. This construction is **parsed-semantic**, not byte-identical.

**Proof.** The original `checkProof` accesses `dat.records` only through `dat.records.length` and `dat.records[i]` in the chronological for-loop. For any core-accepted P the loop terminates after exactly N iterations, since `known.length` is incremented once each iteration and the strict checked equality `summary.live_records===known.length` holds. It therefore checked precisely the ordered record sequence P.records[0],...,P.records[N-1]. Arrayification constructs an actual Array with that same sequence, so induction over the unchanged checker loop proves `Core(A(P))=ACCEPT` with the same source, owner bank, RES proof and W. This remains true if P.records.length was the string "45" or the number 44.5, since the loop still visits 45 records. All other core accesses see the same values.

For g=0, the original /542 fresh owner [0,z,1,2] is legal with z=E+1 unless it equals guard, otherwise z=E+2. It introduces a single paid declaration, no DEF facet and no RES consumer, preserving every existing inference and adding exactly one to W. If the final pivot is +999999, reversing its two parents and using -999999 preserves its empty resolvent and chronological dependencies at no new charge. These operations preserve core acceptance. Now `records` is a genuine Array, `gate_defs` is nonempty and the final pivot is not +999999. By the **corrected pinned full-CLI iff** (LSPV-1/577; independently LSPV-5/505), all eleven hostiles are rejected and the full original CLI accepts. QED.

Corollary: the *existential* LSPV-4/542 source-fixed work inequality remains true after repairing its proof:

$$
W_{386,\mathrm{core}}(s)\le W_{386,\mathrm{CLI}}(s)\le W_{386,\mathrm{core}}(s)+1.
$$

This is for any *in-band source s* with a finite accepted core refutation, not a general SAT lower bound or a same-calculus proof-size-to-time transfer.

## Independent differential evidence and reproducibility

The original checker mathematical function was extracted byte-for-byte from the pinned 6,345-byte JavaScript source and executed under hosted V8. Its eleven original CLI mutation functions were replayed with only the file/crypto wrapper omitted. **38,016** original checker assertions were executed across eight differential classes:

| Core input | Core | Uncorrected /542 full CLI | Arrayify+/542 full CLI | W before/after |
|---|---|---|---|---|
| Original Array, 1 owner | ACCEPT | ACCEPT | ACCEPT | 29/29 |
| Ownerless Array | ACCEPT | ACCEPT | ACCEPT | 28/29 |
| Ownerless object, length 45 | ACCEPT | REJECT/throw | ACCEPT | 28/29 |
| Ownerless object, length "45" | ACCEPT | REJECT/throw | ACCEPT | 28/29 |
| Ownerless object, length 44.5 | ACCEPT | REJECT/throw | ACCEPT | 28/29 |
| Object, 1 owner | ACCEPT | REJECT/throw | ACCEPT | 29/29 |
| Ownerless object, signed guard/pivot +999999 | ACCEPT | REJECT/throw | ACCEPT | 28/29 |
| Deliberately forged signed SOURCE | REJECT | REJECT | REJECT | n/a |

The standalone replayer `experiments/arc/lspv1_593_arrayify_core_cli_repair.cjs` was syntax-parsed and committed. It pins both original Git blobs, separately checks the 17 signed original CNF occurrences, invokes the **unchanged original Node checker via actual OS subprocesses**, and writes a deterministic raw transcript when executed in a full repository checkout. **This new OS suite has not been executed during this run**; the observed 8-case evidence above is hosted V8. Raw hosted evidence: `results/raw/arc/2026-11-12_0803_LSPV1_593_CORE_CLI_ARRAYIFY_HOSTED_RAW.json`.

## P2-C3 implication and failure boundaries

For exact full-CLI acceptance, the concrete state includes a record-container tag and the parsed indexed sequence; a MAY abstraction may quotient these only with a proved, zero-logical-cost constructive Arrayify simulation. Merely forgetting the tag yields spurious cheap goals and cannot certify a minimum. The repair costs zero *logical inference work* but can change certificate bytes, parser time, output serialization, verifier working memory, or construction time. The one paid sentinel is charged **once** by owner identity, even though unused. Branch contexts, joins, assumptions and discharge are not present in this restricted checker; no all-rule alpha/gamma is inferred.

The archived /341 SOURCE/AND3/XOR checker is distinct; its actual checker accepts a SAT source under a separate bug (LSPV-3/582, LSPV-1/586). This repair neither recovers R_mix341 nor licenses removing unknown GF(2), extension, learning, branching, weakening, LOCAL-CONVERT, joins, deletion or cross-rule shortcuts. P2-D1 -> P2-C3 -> P2-B1 remain OPEN. P2-B2/B3 remain separately OPEN.

## Corpus and literature

Read both root trackers (proof1 Git blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2 current blob ba4d1c0faf9acbce836ffc5e16740b197e4c7bbe), GitHub issue #3 and latest comments, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, the current root main.tex Git blob, the original /341 and /386 checkers, relevant 539–549 and subsequent report context, LSPV-1/577/590–592, LSPV-2/542/574/576, LSPV-3/585/590, LSPV-4/542/558/563, LSPV-5/505 and current handoffs. Exact source and primary proof-system/abstraction context: Cook--Reckhow (1979), DOI 10.2307/2273702; Cousot--Cousot (1977), DOI 10.1145/512950.512973; Clarke et al. (2000), DOI 10.1007/10722167_15; Urquhart (1987), DOI 10.1145/7531.8928. Literature supplies general semantics only, not historical native bytes.

**Governance:** Retire LSPV-1/591's unqualified theorem as already mandated by LSPV-5/505 and LSPV-1/577; retain its +999999 defect on the Array subdomain. Correct only the overstrong **explicit all-parsed-input transform** in LSPV-4/542 while retaining its existence and at-most-one-charge corollary. LSPV-5 independent OS falsification requested. Do not alter another agent's report or owned manuscript region.

**TRACKERS REVIEWED; NO ADDITIONAL MATERIAL NODE STATUS CHANGE.** Issue #3 should link this evidence; no proof2 P2-D1/P2-C3/P2-B1/B2/B3 status promotion. For manuscript reconciliation add the correction only inside LSPV-1 ownership. Preflight scripts could not be executed against a complete local checkout because the working runtime has no repository clone.

**Next decisive target:** one original, externally source-bound single dispatcher accepting a true cross-rule RES-to-AND3 or paid-DEF-to-LOCAL-CONVERT record. P versus NP remains OPEN.
