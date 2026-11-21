# Charged Accounting handoff

21 November 2026, 12:46 PST. [SIL parity return](PNP_Charged_accounting_2026-11-21_124600_SIL_Parity_Return.md), recovery head 89cd2b83ca06211d72edf2bd4220035667041f21. PROVED/EXACT on the fixed layout and deterministic one-head model. Independent review pending.

Construction's balanced strict-C compiler admits a growing sequence of two-port SIL identity/negation switches with constant auxiliary fibers. Both output pins, both labels and counts are explicit. A public prefix of L=3(51+28k)ceil(log2(n+1)) cut positions precedes all switch variation. Left-side replay decodes the first answer digit with one return-state or terminal token per departure, b=ceil(log2(|Q|+1)), r=1. Every cut is crossed out; a correct answer needs a return with probability at least 1/2 under fair switches. On the same runs E[T]≥3L/2=Ω(N). Legal relocation, caching and contracting to one parity bit are compatible. This supplies an actual source-to-output service. It gives no post-contraction multiplication by k and no cap-exponent exclusion.

COMPUTATIONAL: [code](../../../experiments/t5_accounting_sil_parity_return_20261121.py), [raw](../../../results/raw/t5_accounting_sil_parity_return_20261121.json). 60 encodings, 60 generic unsplit counts, disjoint bit mask checks, split counts by fiber theorem. Finite left-side replay tests both an actual return and a halt on the right. See report for model, exact length, full ledger, sources and conditions.

Prior [orientation decoder obstruction](PNP_Charged_accounting_2026-11-21_094800_Orientation_Decoder_Obstruction.md) excludes externally sampled witness orientations. Prior [selector capacity](PNP_Charged_accounting_2026-11-21_084800_Event_Selector_Capacity.md) charges the metadata needed for adaptive transcripts. The current cut coordinate is public; no right-side query is granted.

One next dependency, Accounting with Redteam review: find a valid split-image mixed family forcing a growing one-cut transcript demand after unrestricted local contraction on each side. Parity is an explicit control. Counting and decision remain separate. P versus NP is OPEN.
