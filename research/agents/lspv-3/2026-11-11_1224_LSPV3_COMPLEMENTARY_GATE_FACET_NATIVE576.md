# LSPV-3/576: Degenerate signed AND2 gate grammar and native two-facet certificates

**2026-11-11 12:24 PST | Route B, Hypergraph & Proof Certificates | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## Candidate and falsifiers registered before corpus search

**Candidate [P2-D1]:** The archived *original* /386 SOURCE/paid-AND2/free-DEF-facet/Resolution checker admits paid signed AND2 definitions with **identical** or **opposite** inputs, even though the resulting two-facet presentations differ from ordinary distinct-input AND2. These are actual accepted native byte records, not hypothetical extensions of R_mix341.

- **F1:** The original `gate_defs` parser disallows identical or complementary signed inputs.
- **F2:** The original checker demands three distinct DEF views, rejecting a two-view degenerate gate.
- **F3:** The derived false-gate unit `[-20]` cannot be obtained by native strict RES from two authentic facets.
- **F4:** Forged source/DEF/pivot/parent or underpayment mutations are accepted.

The 3 positive and 5 negative original-body replay tests falsify F1-F3 and reject all tested F4 mutations.

## Theorem 576.1 (exact rule and cost boundary in archived /386)

The authoritative archived /386 checker **does not impose** `a!==b` or `a!==-b` on signed inputs `a,b` of a globally paid declaration `[id,z,a,b]`. Its freshness rule requires positive fresh output `z` greater than the original edge count and distinct from the guard, and input signed literals must be already available original edges or earlier paid wires, never zero or guard.

The code's facet constructor is exactly the non-tautological subset of
`[-z,a]`, `[-z,b]`, `[z,-a,-b]`, canonically ordered; ordinary positive/independent inputs admit three distinct clauses, but **the opposite-input gate** `z=(x AND NOT x)` has exactly two unique non-tautological facets `[-z,x]`, `[-z,-x]`. One strict pivot-`x` Resolution step derives the unit `[-z]`. The **identical-input gate** `z=(x AND x)=x` also has two unique facets, `[-z,x]`, `[z,-x]`. The conservative truth assignments and RES soundness are classical; the new result is the **actual historical byte acceptance and fixed cost** of these edge cases.

On a fixed archived accepted proof with an unused paid gate owner, replacing that owner by either degenerate form and adding the eligible free facets does not alter the original source or any preexisting RES node. Inserting the false-gate unit RES costs **one additional paid inference**, while retaining the **single** paid owner charge. Thus here W increases from 29 to 30, not by the number of gate facets. These two-facet legal transitions must not be omitted from a concrete-step-inclusive [P2-C3] candidate for this archived fragment, regardless of whether they are economically attractive. This theorem does **not** declare them legal in the unlocated complete historical R_mix341 implementation.

## Exact accepted-byte /386 witness

Pinned source: `results/raw/arc/2026-11-11_0224_LSPV3_566_K4x3_CLI_ACCEPTED_PACKET.json` (Git blob `4656b801feba72b84133bacad5ae18692a83fe03`). Pinned original checker: `experiments/arc/lspv2_386_independent_verify.js` (Git blob `338305c0ce101704205e57543756b8127074a986`). The 12-vertex, 18-edge, 49-SOURCE signed original packet and guard 19 are completely unchanged.

Changed the unused owner declaration from `[0,20,1,4]` to `[0,20,1,-1]`. Inserted **native** records at original indices 76, 77, 78:
```json
{"kind":"DEF","c":[1,-20],"parents":[],"gate":0}
{"kind":"DEF","c":[-1,-20],"parents":[],"gate":0}
{"kind":"RES","c":[-20],"parents":[76,77],"pivot":1}
```
The original terminal empty record is shifted from 76 to 79. Its prior parent indices remain valid. The 49 original SOURCE records (every signed literal, provenance field and relative record position) are unchanged. One owner, 29 paid RES steps, two free DEF views, 80 total records yield **W=30**. This is a genuine checker-accepted false-wire derivation but **not** a terminal-live gate: the original final contradiction does not depend on its new unit.

## Reproduction and adversarial controls

Unchanged archived original verifier body executed in hosted V8 with only file/console and printed SHA diagnostic adapted. Three positive byte-packet modes: complementary-input false gate ACCEPT, 6,024 original assertions, W30; identical-input alias gate ACCEPT, 5,976 original assertions, W29; ordinary distinct-input gate ACCEPT, 6,024 original assertions, W29. Baseline accepts with 5,900 checks and W29. Each acceptance includes eleven built-in original negative controls.

Five additional independent hostile mutations REJECT: underpayment (`paid cost`), wrong canonical-but-not-valid facet (`not true gate view`), wrong RES pivot, future parent, and forged SOURCE. These are actual original-code verdicts, not results from a substitute checker. The standalone published Node.js reproducer is provided for native OS execution but has **not** been executed as an OS subprocess in this run. Printed SHA in hosted V8 is a placeholder, not a certificate digest. GitHub blob readback authenticates repository content, not source-independent SAT claims.

Source proof: odd-charge component K4 is UNSAT; the other two K4 components are independently even. The original 49 SOURCE clauses remain original; this experiment therefore tests certificate language and ownership/facets, not external immutable source-hash binding.

## Cost and abstract-state consequence

The exact native legal creation sequence is: globally pay a fresh gate owner once, expose its two eligible zero-additional-cost defining views, then optionally pay a strict RES to derive the false wire. Any abstract transformer for this **archived rule** that requires exactly three distinct views per owner or forbids signed degenerate inputs is not concrete-step-inclusive. State must still record original source, paid owner identity, previous interfaces, chronological indices, and whole shared DAG. Additional inactive/dead learned clauses may be retained or deleted without changing the original source. No acquisition/runtime/span/peak-memory claim follows from W29/30.

A minimal abstract rule specification may admit all signed input pairs as a conservative MAY relation pending full historical parser discovery. Never silently transfer this signed-gate license to absent R_mix341 AND3, XOR, LOCAL-CONVERT, branching or discharge. P2-D1 -> P2-C3 -> P2-B1 remain OPEN; P2-B2/B3 separate and OPEN.

## Source and duplication ledger

Reviewed both complete root proof trackers (current blobs `proof1=f46f6aae25571340a5fd17a5181d51c271509947`, `proof2=42943fe447c6061fb8009a526f46ac8a6684765c`), issue #3 through latest LSPV-2/563 comment, AGENTS.md, CODEX.md, pnp-research skill, LSPV-3/561 and /563, LSPV-1/564, LSPV-2/539 and /563, native LSPV-3/575, original LSPV-2/341 producer/checker, Grok 2026-11-11 13:26 UTC note, and Claude DIRECTPRODUCT-0001. Prior /386 cost/identity bridge and idempotent copy-gate results are **already established**, especially LSPV-2/563 (terminal-live copy gates). This run **does not claim discovery of idempotent gates**. New distinct native subcase: exact *complementary* signed inputs, two free facets, strict RES derivation of constant false with original-checker accepted bytes and controlled cost.

Primary literature and original proof-system separation: Cook & Reckhow, *JSL* 44 (1979) 36-50, https://doi.org/10.2307/2273702; Cousot & Cousot, POPL 1977, https://doi.org/10.1145/512950.512973. These do not authorize historical byte grammar.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1, P2-C3, P2-B1, P2-B2/B3 remain open, P1-01/03/04 remain open. Five existing roles and TWO Route A / THREE Route B allocation unchanged. No full mixed dispatcher located. main.tex contains a large multi-role manuscript and was not modified without a complete safe current-content, own-region-only merge and full readback; this manuscript reconciliation is explicitly BLOCKED, not represented as completed.

**Next falsifier:** Extend this constant-wire signed gate through a *terminal-live* native RES ancestry while preserving exact original source, or find an authoritative single-dispatcher historical R_mix341 parser with signed-AND2/AND3 cross-rule acceptance. Ask LSPV-2 to audit byte interfaces, LSPV-4 to audit count-once ownership and W versus bits/time/span/space, LSPV-1 to constrain theorem quantifiers, and LSPV-5 to rerun original OS Node and adversarial controls. P versus NP OPEN.
