# LSPV-2 safety handoff: root MAIN placeholder

Date 2026-10-29 UTC. Scientific status P versus NP OPEN. No changes to schedules or agent states.

During EXACT22-PORT-WIRES221 publication, before reconciliation, root main.tex was fetched from j15marti/pnp and found to contain exactly 20 ASCII characters:

```
$(cat /tmp/main.tex)
```

The current blob SHA is 7f5da7b86108191ad7b1393ef311c588cf710ada. It has no ownership markers, so no LSPV-2-only patch is possible. This appears to be an accidentally committed literal shell substitution, not the actual TeX document. Do not treat the placeholder as mathematical MAIN.

An earlier intact GitHub read in the same run returned the 62,081-character root MAIN with blob SHA 8a1f134a115052f40247f64bfc9fa1bd4d2dddaf, with all five ownership markers. LSPV-5 is the authorized whole-document synthesis owner and should restore/reconcile from an independently verified commit or historical version, preserving all concurrent role edits, before LSPV-2 modifies its marked region. Do not blindly force a historical blob over newer authorized work.

The LSPV-2 standalone theorem and Python/raw artifacts were committed under research/agents/lspv-2/2026-10-29_1025_* and verified at exact local Git blob SHA. The role coordination note is research/coordination/2026-10-29_1025_EXACT22_PORT_WIRES221_LSPV1_LSPV4_HANDOFF.md. One separate bibliography .bib GitHub upload was blocked by safety checks; full bibliography is available in Library /P vs NP/2026-10-29_1025_EXACT22_PORT_WIRES221_refs.bib and package zip.

Status: MAIN reconciliation PENDING. P vs NP OPEN.
