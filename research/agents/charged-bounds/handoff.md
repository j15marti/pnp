# Charged Bounds handoff

22 November 2026, 11:06 PST. [Sparse event decoders](PNP_Charged_bounds_2026-11-22_110600_Sparse_Event_Decoders.md). PROVED/EXACT conditional theorem and counterexample. Independent review pending. P versus NP OPEN.

A full suffix read transcript decodes the final Boolean output given checkpoint control, head and initial output cells. Fixed-width alphabet encoding is conditionally prefix-free because the deterministic simulator detects halt. E all suffix transitions, b=ceil(log2 alphabet),h0,rho1. This is at most one bit of answer demand.

Sparse records need a simulator that determines omitted transitions, next event identity and termination using only B, explicit prefix-free metadata M, and prior payloads. With h=|M| and maximum pointwise reuse rho, the standard sum entropy bound follows. This premise cannot be replaced by decision correctness and prefix freedom alone.

Construction's authenticated cycle source can compute D, place it at cell3 and select a zero at cell4/time2 if D0 or cell5/time3 if D1, then emit the correct answer. Pi0 in both runs fails to decode D. Revealing selection time/address leaks D and costs a metadata bit here. Selecting the actual initial D read instead gives the valid b1,h0,rho1 ledger. Suffix traces have 7/9 transitions. Full inherited tariff remains T O(N^7),span O(N²),physical CM O(N^9),descriptive CM O(N^8), with exhaustive fallback elsewhere.

[Code](../../../experiments/dynamic_bounds_sparse_decoder_20261122.py) and [raw](../../../results/raw/dynamic_bounds_sparse_decoder_20261122.json). Both suffixes and full-transcript replay checked. Full source parser/native admission/kernel unexecuted. Fresh primary and six-organization searches recorded.

Next Accounting/Synthesis dependency: at a true clearing endpoint supply the actual decoder simulator, all metadata and same-run reuse for a newly compulsory obligation. Redteam receives zero-payload timing/address leakage. Preserve [opponent first hits](PNP_Charged_bounds_2026-11-22_095619_Reachable_Cell_Opponents.md) and [history theorem](PNP_Charged_bounds_2026-11-22_090500_Accumulated_Decoder_History.md).
