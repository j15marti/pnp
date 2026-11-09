# LSPV-3/536 addendum: authenticated full root main.tex reconciliation

2026-11-09 08:38 PST | Route B | Source preservation/status only.

The original LSPV-3/536 role-owned research report correctly recorded that fetch_file(main.tex) returned zero characters despite a valid blob identifier. A subsequent, separate retrieval through the **same exact current main-branch blob SHA** using the GitHub blob endpoint succeeded and returned the COMPLETE 1,790,543-character document.

The root file contained exactly one % BEGIN LSPV-3 OWNED and one % END LSPV-3 OWNED marker. The cost-sound partition-abstraction paragraph was inserted **entirely inside that existing specialist region**, preserving every character outside it.

Optimistic-concurrency write used the complete original blob SHA fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba. The successful commit was ab4fadccf6ede02cad6ca26495d5439af1ef6be7; the complete updated blob is abb3480f2272852c4184e90d5a7c9d1a5d9de213, 1,792,725 characters. Independent full fetch_blob readback was byte-for-byte identical to the expected merged content. Exact outside-region comparison PASS, balanced markers PASS, OPEN status PASS. No other owner's region, root governance, historical inference weight, or agent/task configuration changed.

This addendum supersedes only the temporary statement **"root main.tex not edited"** in the historical /536 report and first issue comment. It changes no mathematical status. Exact abstract theorem remains a restricted recasting of the existing linear /341 bound. [P2-D1], [P2-C3], [P2-B1], [P2-B2] and P versus NP remain OPEN.

<!-- LSPV3/536 MAIN READBACK END -->
