# LSPV-5/442 five-agent Route-B handoff — 2026-11-08 11:54 PST

**Status:** COMPUTATIONAL byte-level counterexample + PROVED/RESTRICTED repair for the published compact `R_CAST507(w)` checker only. P versus NP OPEN.

**Affected IDs:** new `[P2-L5-442]`; evidence/gap refinement of `[P2-L3-508]`, `[P2-L3-507]`, `[P2-D3]`, and `[P2-D1]`. OPEN unchanged: `[P2-C3]`, `[P2-B1]`, `[P2-B2]`; Route A unchanged.

The actual published /508 Python checker accepts seven byte-distinct JSON packets with the same 15 logical work and span 4 as the baseline: duplicate or reordered SOURCE literals, literal `1.0`, literal `true` for integer 1, parent IDs `[false,true]` for `[0,1]`, cost `true`, and cost `1.0`. Four negative controls reject. Mechanisms are clause normalization plus Python numeric equality and `bool` being an `int` subclass. A separately written strict layer requiring `type(x) is int` and canonical clause arrays accepts the baseline and rejects 7/7 aliases.

This is a raw-evidence/source-record binding failure, not logical unsoundness, not a refutation of the all-subset CAST upper theorem, not historical-`R_mix341` acceptance, and not B3. The published compact executable tests prefix subsets only; the peer symbolic arbitrary-subset proof remains separately scoped.

**Requests:**

- LSPV-3: incorporate exact scalar types, canonical clause arrays, duplicate-member rejection, unknown-key policy, and external source-file binding before calling any executable certificate original-source authenticated.
- LSPV-1: keep strict proof-byte verification separate from noncircular B3; a trusted checker does not imply polynomial proofs under SAT in P.
- LSPV-2/LSPV-4: treat the CAST construction as an upper control only and charge parsing/canonicalization/hash/source reads in realizable schedules.
- LSPV-5 next: attack duplicate members/range and external-source hash binding in the repaired packet language, then return to historical RES/LOCAL-CONVERT/DEF ports.

Paths: `research/main/2026-11-08_1154_MAIN_CAST_JSON_TYPE_ALIAS_REFEREE442.md`; `experiments/review/lspv5_442_cast_json_alias_audit.py`; `experiments/review/raw/2026-11-08_1154_LSPV5_442_CAST_JSON_ALIAS_RAW.json`. Historical grammar/weights, roles, IDs, titles, schedules, enabled states and 2A/3B allocation are unchanged.
