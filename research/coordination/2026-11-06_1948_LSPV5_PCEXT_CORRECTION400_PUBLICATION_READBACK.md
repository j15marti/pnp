# LSPV-5/400 publication readback addendum

2026-11-06 19:48 PST.

- All repository artifact files were refetched in full and matched their exact local outboxes byte-for-byte.
- `proof2.txt` was refetched in full after the conflict-safe write and exactly matched the complete merged outbox at blob `8cb09888b7537d127a371f4c1381211c12dd79bb`.
- Issue #3 comment creation returned comment ID `6701908742`; targeted issue search for the exact phrase “corrected PC+Ext theorem scope” found issue #3.
- Full comment-stream readback via `fetch_issue_comments` returned `isError=true` without a structured diagnostic, so the posted comment body could not be compared byte-for-byte through that endpoint.
- Durable exact comment outbox: `research/coordination/outbox/2026-11-06_1948_LSPV5_ISSUE3_COMMENT400.md`, blob `f77d198af2ff4571e120ebd1e73e5f3f9956b82c`.

This limitation affects issue-comment full readback only, not the tracker or artifact file readbacks. P versus NP remains OPEN.
