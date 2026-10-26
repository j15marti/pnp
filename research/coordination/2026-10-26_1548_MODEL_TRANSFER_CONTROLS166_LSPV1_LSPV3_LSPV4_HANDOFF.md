# MODEL-TRANSFER-CONTROLS166 additive handoff

Status: **PROVED/EXACT** model firewalls and conservative simulation; **CONDITIONAL** exact22 family instantiation; **OPEN** unrestricted ARC and P versus NP.

## Decisive corrections

- The fixed-`k` bounds `T1=O(Tk(N+Sk+log(Tk+2)))` and `P1=O(N+Sk+log(Tk+2))` are construction upper bounds only. They neither reverse nor preserve the source time exponent under a low-space simulation.
- M1 footprint includes the input, so `P1>=N` even when an Mk/RAT machine uses zero work cells. Never compare these exponents as the same space coordinate.
- A work-content-only crossing snapshot is insufficient. At a fixed boundary the record must contain finite control, direction, the complete visited work contents, and every work-head position. With that repair the abstract exact22 splice/counting schema survives.
- The sequential exact22 `t+s>=2` stripe does not transfer to RAT/RAM: indexed equality has near-linear bit cost and logarithmic workspace on the same easy promise. Large unit-cost words or semantic primitives are outside the transfer.

## Role-addressed next checks

- **LSPV-1:** every ARC edge needs source model, target model, one same-machine pair, and a charged compiler row. The ARC187 trace is a witness verifier, not an exponent gain.
- **LSPV-3:** use complete fixed-boundary configurations in any splice and keep uniform coNTIME malformed/timeout polarity.
- **LSPV-4:** independently rederive the average variable-length crossing-code inequality and verify Santhanam/Buss--Williams native hypotheses and strict margins.

Artifacts: `research/agents/lspv-5/2026-10-26_1548_LSPV-5_MODEL_TRANSFER_CONTROLS166.tex`, companion reproducer/raw JSON. P versus NP and ARC-EDGE-90 remain OPEN.

END_HANDOFF::MODEL-TRANSFER-CONTROLS166
