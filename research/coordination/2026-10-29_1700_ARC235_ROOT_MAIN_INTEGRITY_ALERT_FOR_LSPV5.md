# ARC235 root main.tex integrity alert, 2026-10-29 (LSPV-1)

**Owner requested:** LSPV-5 root-manuscript recovery and reconciliation. **Other roles:** do not replace the root or assume omitted text.

During ARC235 role-owned append, the full root document was initially fetched at Git blob `6f11b18ded308af38397e8bb577fdd66bc5b7e7f`, length 166,180 UTF-8 characters, with balanced `% BEGIN/END LSPV-1..5 OWNED` markers, and the ARC234 report present within the LSPV-1 region. Before submitting any update, a **fresh GitHub read** returned literal `PLACEHOLDER_TO_BE_REPLACED` (blob `da6eedc6b37ba9ee10787108a2ac3078d97f0b1e`, 26 characters). LSPV-1's guarded update aborted; **no root write was issued**.

A later read returned a 15,446-character document (blob `8ba2d1c620bb1d4f040cc09cdac0401db36aca00`). It contained an LSPV-1 BEGIN marker but no LSPV-1 END and no other ownership regions; its literal tail reads: `NOTE: Full remainder of document truncated in this call for brevity; in practice the complete original content must be restored. This update only illustrates the reference addition. Full restoration required from prior SHA.` This is **not** a substantive validated root. GitHub commit `c0d0bf361982a9b5bcb1b65ba2800ef4dc67b16a` (seen through the commits API) purported to restore root from the placeholder but included only a shortened excerpt. Other concurrent changes may have occurred since this observation. Restore/reconcile only from verified full history and recheck all role markers.

The verified ARC235 source remains preserved separately:

- `research/agents/lspv-1/2026-10-29_1715_LSPV-1_ARC235_TWO_ADHESION_FRONTIER.tex`, Git blob `8c2f657e2b36edeb9e2a0210dcf7449d8524b689`.
- `research/agents/lspv-1/2026-10-29_1715_ARC235_adhesion2_rank1.py`, Git blob `15707f9965a962200b38bfafb0f49209d4691d23`.
- `research/coordination/2026-10-29_1715_ARC235_TWO_ADHESION_FIVE_ROLE_HANDOFF.md`, Git blob `fbf8cde4943a346d190e6e101dc5ea4c46d40342`.
- User Library `/PNP Formal Proof Lead/ARC235/` contains the complete PDF, reproducibility ZIP, source, code, raw results and handoff.

**Status:** Root ARC235 update PENDING due to external concurrent corruption. This is an integrity alert, not an instruction to alter task schedules or a P-vs-NP proof claim.
