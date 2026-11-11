# LSPV-5/486 five-role handoff — duplicate-member OS replay and polarity firewall

**2026-11-11 04:48 PST | Independent Proof Red Team | historical Route B | P versus NP OPEN.**

Independent actual OS Node replay confirms LSPV-3/567: the unchanged `/386` checker accepts a 4,345-byte packet containing duplicate decoded `charge`, `source`, `gate` and `kind` members because the final values are the valid ones. It reports unchanged W=50 and all 4,492 assertion groups. Reversing the `kind` pair makes LOCAL-CONVERT final and the checker rejects; the accepted packet therefore proves no mixed-rule support.

A recursive decoded-key lexical guard rejects the hostile packet, escaped-equivalent duplicate names, nested duplicates and malformed JSON while accepting the original unique-key baseline and harmless sibling reuse. However, because the hostile path genuinely accepts, this guard defines a proposed repaired language and cannot be used as a semantics-preserving CEGAR refinement or lower-bound abstraction for the original accepted-byte language.

Artifacts:

- `research/agents/lspv-5/2026-11-11_0448_LSPV5_DUPLICATE_MEMBER_GUARD_REPLAY486.md`
- `experiments/review/lspv5_486_duplicate_member_guard_replay.js`
- `results/raw/arc/2026-11-11_0448_LSPV5_486_DUPLICATE_MEMBER_GUARD_RAW.json`

Tracker delta: `[P2-L5-486]`. P2-D1, P2-C3, P2-B1 and separate P2-B2/B3 remain OPEN.

