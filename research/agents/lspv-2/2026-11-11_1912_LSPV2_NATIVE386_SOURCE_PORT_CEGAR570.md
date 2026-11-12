# LSPV-2/570: Original /386 source-bound, signed-port and paid-history CEGAR subprocess replay

**2026-11-11 19:12 PST | PNP SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED necessary-condition theorem + COMPUTATIONAL exact original-OS differential | P versus NP OPEN**

## One construction, four falsifiers, prior-art boundary

**CEGAR570:** Pin the unchanged archived `/386` SOURCE/paid AND2 owner/free DEF facets/strict signed RES checker and a separately supplied, unchanged 17-clause signed K4 DIMACS source. From the previously accepted W29 certificate, construct three actually accepted paths (baseline, paired final port reorientation, terminal-live duplicate paid inference) and six actual rejected paths (forged SOURCE sign, one-sided signed pivot reversal, one-sided parent order reversal, underpayment, gate-output/guard collision, forward parent). Build a sequence of reference-only necessary-condition abstractions, concretely replay each byte packet against the original checker in real Node OS subprocesses, and refine exclusively on observed rejected packets. This is **bounded-corpus CEGAR-style replay**, not discovery of the general mixed-calculus grammar or an autonomous all-input search.

F1: the unchanged checker rejects paired-orientation or terminal-live paid duplication. F2: a sound necessary-condition refinement eliminates any original accepted path. F3: the original checker accepts the forged SOURCE, wrong signed ports, underpaid cost, colliding owner wire or forward dependency. F4: the clause-value abstract charge exceeds the original concrete W on an accepted test. None occurred. Existing LSPV-2/564 proved restricted RES orientation equivalence; /565 proved a restricted step-cost abstraction; /549 proved that independent /341 and /386 checker acceptance cannot be composed. **The incremental contribution here is the executed, source-pinned, multi-stage CEGAR/replay program and complete 9-case original-OS discriminating corpus, not priority for these earlier lemmas.**

## Authority and external source

- Unchanged original checker: `experiments/arc/lspv2_386_independent_verify.js`; Git blob `338305c0ce101704205e57543756b8127074a986`.
- Accepted W29 seed: `results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json`; Git blob `318c52d99977ea4e91bc8554051138a700c1dc94`.
- Separately pinned signed CNF: `results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf`; Git blob `e8bc4300f1f4518cb447edaf3f699bcee4839803`; SHA-256 `3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c`. Its exact 17 signed clauses were independently compared with all 17 original SOURCE occurrences before executing the checker.
- That checker **does not** implement historical AND3/GF(2)/LOCAL-CONVERT/context/branching/discharge or even the /341 fixture grammar; no substituted checker is called historical R_mix341.

## Restricted abstraction inclusion and cost theorem

For certificates over the **fixed externally bound signed K4 source and fixed in-band K4 spec**, define `A0` as a liberal may-parse; `A1` additionally requires the complete original signed SOURCE occurrence multiset and the exact pinned spec; `A2` additionally requires each signed RES inference `(A,B,p)` to satisfy `p in A`, `-p in B` and the exact canonical non-tautological resolvent; `A3` additionally requires chronological parents, fresh distinct paid gate-owner identities and their legal inputs, valid record references, nonnegative identifiers, and exact historical /386 summary-cost counters. Each condition is a necessary condition in the verbatim original checker. Its in-band parity self-test and other incomplete reference facets are **not** silently turned into a hypothetical full-rule grammar. Within this restricted fixed-source domain,

```
Accepted386(F) subseteq A3 subseteq A2 subseteq A1 subseteq A0.
```

Proof: source validation and summary checks appear explicitly in `checkProof`; legal RES signed orientation/resolvent checks are executed on every RES record; declaration freshness, record chronology and exact counted costs are checked on every accepted packet. The source hash is fixed outside the checker before these predicates. Adding necessary conditions cannot exclude a true accepted packet of this fixed-source subset. This is a theorem about this implementation and its declared source domain, **not** a full-history R_mix341 abstraction theorem.

Define `seen` as previously established exact signed clause values and `D` as previously charged distinct paid gate owners. The reference abstract charge for a legal RES record is 0 if its signed conclusion is in `seen`, otherwise 1; free SOURCE/DEF facets cost 0; each new paid owner identity costs 1 once. The original concrete /386 charges 1 for every RES occurrence and one for each declared paid owner. Hence by induction over any legal prefix with the same fixed source and valid declarations:

```
W_hat(prefix) <= W_386(prefix).
```

The abstract value quotient is a **lower work charge**; it does not claim that a free reuse can generate an invalid missing dependency. Parent relations and signed ports remain available for native replay. In the original W30 live-duplicate accepted packet, `W_386=30` and `W_hat=29`. Retaining the genuine paired-orientation W29 path shows that the signed-port refinement preserves a real, previously established shortcut. This finite replay does not establish that the abstract system is complete for full mixed-rule refutations.

## Exactly executed Node OS outcomes

Node.js v22.16.0 executed the unchanged source in **9 actual OS subprocesses**, not a hand-written checker. Three original certificates were accepted; six corrupted ones were rejected. The 3 accepted runs executed **10,682 original-checker assertion groups** and **33 bundled negative corruption checks**. All nine outcomes matched their predeclared polarity. The W29 paired-orientation accepted packet is 2,868 bytes; the W30 duplicate accepted packet is 2,919 bytes and its exact SHA-256 is `b8634a75ad72fb18d9750370f54485cc16af2e66b725c76e0bcb959f375f53f4`.

| Reference stage | Retained candidate packets | Genuine original accepts retained | Spurious native rejects still admitted |
|---|---:|---:|---:|
| A0 liberal MAY | 9 | 3 | 6 |
| A1 exact SOURCE/spec | 8 | 3 | 5 |
| A2 signed RES legality | 5 | 3 | 2 |
| A3 fresh owners/accounting | 3 | 3 | 0 |

This is exhaustive **for the nine predeclared corpus packets only**, not for all legal source-bound certificates. A3 remains an overapproximation, and passing A3 does **not** imply native acceptance. The underpaid packet has a claimed W28 but is rejected by native accounting; its A0-A2 abstract value charge W29 is not a cost-soundness counterexample because it is *not a legal concrete proof*. Keep logical work, certificate bytes, construction time, span and peak space separate. The Node measurements refer only to test-subprocess time, not an all-input SAT complexity claim.

## Executables and accepted-byte artifacts

- Executable reference-stage/unchanged-original-OS replayer: `experiments/arc/lspv2_570_native386_cegar_port_source.cjs`; pins all three authoritative prerequisite file blobs; rerun from repository root with `node experiments/arc/lspv2_570_native386_cegar_port_source.cjs`.
- Immutable compact actual OS manifest: `results/raw/arc/2026-11-11_1912_LSPV2_570_NATIVE386_CEGAR_OS_COMPACT.json`; includes nine exact SHA-256 packet digests, original verdict/rejection reasons, three positive assertion totals and all four stage candidate sets.
- Full timing/stdout raw regenerated by runner at `results/raw/arc/2026-11-11_1912_LSPV2_570_NATIVE386_CEGAR_OS_RAW.json` (locally executed but not separately committed to the repository).
- Accepted W30 live duplicate: `results/raw/arc/2026-11-11_1912_LSPV2_570_VALID_W30_LIVE_DUPLICATE.json`. Exact rejected signed-pivot falsifier: `results/raw/arc/2026-11-11_1912_LSPV2_570_INVALID_WRONG_SIGNED_PIVOT.json`.
- Dated coordination: `research/coordination/2026-11-11_1912_LSPV2_NATIVE386_CEGAR_FIVE_ROLE_HANDOFF570.md`.

## Research corpus, barriers and status

Reviewed full `proof1.txt` and `proof2.txt`; issue #3 through contemporaneous LSPV-1/586, LSPV-3/582, LSPV-4/555 and LSPV-5/499; `AGENTS.md`, `CODEX.md`, project skill and actual LSPV-2/539-549 and 562-569 reports; historical /341 and /386 checker sources and existing corpus. Compared primary sources: Cook and Reckhow, JSL **44** (1979) 36-50, DOI [10.2307/2273702](https://doi.org/10.2307/2273702); Cousot and Cousot, POPL (1977) 238-252, DOI [10.1145/512950.512973](https://doi.org/10.1145/512950.512973); Clarke, Grumberg, Jha, Lu and Veith, CAV (2000) 154-169, DOI [10.1007/10722167_15](https://doi.org/10.1007/10722167_15); the distinct [FRAT-XOR external format](https://github.com/meelgroup/frat-xor/blob/main/format.md) and the separate project CANON proposals. **No theorem transfer** from any external proof language establishes missing R_mix341 syntax.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1, P2-C3, P2-B1, separate P2-B2/B3 and P1-01/03/04 remain OPEN. No arbitrary input SAT machine theorem or full-calculus minimum lower bound follows. No agents, schedules, historical weights, Route A/B allocations or ownership boundaries were changed. Exactly the original five intended research roles remain the target; this run creates no new automation.

**Next decisive target:** acquire the original single-rule dispatcher accepting genuine source-bound RES-to-AND3 or paid DEF-to-LOCAL-CONVERT transitions and replay it with both valid port certificates and corrupted controls. Until acquired, unknown rules remain MAY, not excluded.

**P versus NP remains OPEN.**
