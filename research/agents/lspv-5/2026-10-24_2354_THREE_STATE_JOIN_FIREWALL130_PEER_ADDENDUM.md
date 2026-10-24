# LSPV-5 post-publication peer addendum: INTERVAL-PIN-COVER90

Timestamp: 2026-10-24 23:54 Asia/Seoul. P versus NP OPEN. ARC-EDGE-90 OPEN.

Role 4 published `INTERVAL-PIN-COVER90` concurrently with the Role 5 readback. Its theorem body was independently checked and is **accepted only in its declared restricted promise/source-linked-oracle model**:

- The canonical implication chain is SAT iff at least one orientation field is zero.
- Partitioning orientations into consecutive intervals gives the exact OR identity `SAT(parent) iff OR_j SAT(interval_j)`.
- Each interval child is an ordinary proper-3CNF in the same promise family.
- On the all-one source, a deterministic adaptive controller making `r` direct reads and interval-status calls covering at most `K` positions satisfies the exact cover bound `r + KQ >= q`.
- With `K=ceil(sqrt(q))`, the recognized promise has the same favorable square-root recurrence audited in MULTIBIT-ENDPOINT129.

This does **not** change the all-input status. The chain is source-linear decidable, its interval oracle is explicitly source-linked rather than a free ordinary SAT call, and an arbitrary-input fallback retains the original exponent. The result is compatible with THREE-STATE-JOIN-FIREWALL130: interval children aggregate by an easy OR, whereas the exact-one family has named cyclic global compatibility that cannot be inferred from local three-state feasibility or arc consistency. No reviewed construction combines both power-short ordinary children and exact global gluing on every ordinary input.

Status: **PROVED/EXACT restricted theorem accepted; all-input transfer OPEN; no independent rerun of Role 4's subsequently published finite script is claimed here.**
