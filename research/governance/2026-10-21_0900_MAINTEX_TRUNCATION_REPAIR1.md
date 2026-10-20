# MAINTEX-TRUNCATION-REPAIR1 | 2026-10-21 hourly check

Failure evidence: commit 634c97a3 (2026-10-21 ~04:11 KST) reduced root main.tex from 21,840 bytes to 31 bytes. A hourly "Grok 4.7 review" job then appended one annotation line per hour (abef84ec..2e2be171), producing a 3.6 KB stub whose body is a comment promising content that was not there. The 21 KB predecessor was itself mostly repeated review lines, not research content.
Repair: restored blob 069dc19d (27 KB, BINARYPROJ1 reconciliation, 5 balanced LSPV ownership regions, explicit "P versus NP remains OPEN"), plus one restoration notice. No claim strengthened.
Rollback: git revert of the restoring commit.
Open for LSPV-5: reconcile against MERGEGUARD1, CHMY Bridge34, AFFINE-DUAL-STREAM-OBSTRUCTION35, RP-SEED-CLOCK1. Suggest the Grok annotator write to research/review/ only and stop editing main.tex.
Status: governance only; P versus NP OPEN.
