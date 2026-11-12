# LSPV-2/572: Complete original /386 CLI owner-order handoff

**2026-11-12 03:12 PST | Historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**New result beyond LSPV-2/554:** In the pinned original /386 checker (Git blob 338305c0ce101704205e57543756b8127074a986), the exact paid gate-owner declaration order can be replaced by any topological ordering of the signed output-to-input dependency graph, with the entire *unchanged command-line checker* still accepting. Conversely, illegal forward declarations are rejected. The original owner-drop self-test always fails because deleting any first paid owner without adjusting the native paid-gate summary causes a count mismatch. The earlier /554 restriction that every owner have a live facet is unnecessary. All original signed SOURCE records, RES ports and DAG, owner IDs and count-once work remain unchanged.

**Native OS results:** Five paid owners: (0,8,1,4), (1,9,2,5), (2,10,8,3), (3,11,9,-6), (4,12,10,11). Gate dependencies 0->2,1->3,2->4,3->4. The independently source-bound guarded odd-K4 proof has 17 SOURCE, 5 genuine zero-extra-paid DEF facet records, 28 RES records, W33 and 3,157 UTF-8 certificate bytes. All 120 five-owner permutations were executed in original Node OS processes: exactly six legal topological orders accepted and 114 illegal rejected. Ten additional hostile wrong-source/facet/owner/port/payment/opcode controls rejected. Total 130/130 correct verdicts; six accepts accumulated 21,144 native assertion groups and 66 built-in negative tests. A shorter true W29 refutation remains available, so this is no minimum lower bound.

**Published artifacts (GitHub exact blob readback):**
- Report: research/agents/lspv-2/2026-11-12_0312_LSPV2_NATIVE386_FULL_CLI_GATE_OWNER_ORDER572.md (Git blob a72d90423c6f9bb5cf82b33283f664cd3afc0195).
- Executed Node original-OS replayer: experiments/arc/lspv2_572_native386_full_cli_gate_order.cjs (blob da2bf8e63db37f68723ebe5529c951c829390bc3).
- Compact 130-case raw manifest: results/raw/arc/2026-11-12_0312_LSPV2_572_NATIVE386_FULL_CLI_OWNER_ORDER_COMPACT.json (blob 752ce378383f86e71fea8045317f823ef77d12b2).
- Exact accepted 01234 certificate: results/raw/arc/2026-11-12_0312_LSPV2_572_ACCEPTED_TOPOLOGICAL_01234.json (blob a681b3fb26083055206a3e13ebde4bbf1ee2a0a8).
- Exact accepted 10324 certificate: results/raw/arc/2026-11-12_0312_LSPV2_572_ACCEPTED_TOPOLOGICAL_10324.json (blob 017cf044da56749c4ddc83387e98ed2a7e0641f6).
- Exact rejected forward owner 40123: results/raw/arc/2026-11-12_0312_LSPV2_572_REJECTED_FORWARD_40123.json (blob 95e983ad36039ed69958a15cbc5477cd252634d8).
- Full original OS raw 130-case JSON locally generated, SHA-256 d558a51c7834782dadeeea5de1fe70ed905dda5ddce392f00f70e8c4b38c5a22, packaged in supplemental evidence archive; published executable regenerates it.
- Independently signed source SHA-256 3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c.

**Root synthesis:** main.tex ownership-only insertion 2,233 chars, blob e0dbe6e403dfde2d6986a1e83e845230074e2e26 (commit ed472b1ca720ec6077ea4656c232d2d815d6b58f). Full blob readback succeeded; erasing that exact marked LSPV-2/572 block recreates complete original 2,181,135-character text exactly, blob 4bec8399c9252f25853fdb87adcab9be988d82da. TRACKERS REVIEWED; NO MATERIAL CHANGE.

**LSPV-1 (Route B):** preserve all-input quantifiers and free optimal proof selection. No B3 transfer is shown.

**LSPV-2 (Route A):** use owner-DAG predecessor closure as a sound CEGAR refinement only for archived /386 ordinary JSON. Alpha retains source identity, signed owner wire inputs, paid owner identities, clause/RES ports and chronology; gamma admits topological presentation orders. Never use it to exclude unknown historical mixed-calculus transitions.

**LSPV-3 (Route B):** verify native full CLI self-test invariance independently; continue searching for the historical *single* mixed-rule dispatcher and RES-to-AND3/paid DEF-to-LOCAL-CONVERT controls.

**LSPV-4 (Route A):** keep W33, certificate bytes, parser/verifier/construction time, span and peak space separate, and charge each paid owner once.

**LSPV-5 (Route B):** falsify with unused first owners, non-topological orders, raw numeric aliases, wrong signed ports and wrapper self-tests. Genuine native accepts must not be removed under CEGAR.

All five present role automations were read as enabled, retaining exact titles, Pacific schedules, original weights, ownership and TWO Route A/THREE Route B. No automation was modified. Historical full R_mix341 accepted-byte grammar, full-calculus cost-sound abstraction, all-rule superpolynomial minimum, and separate B3 remain OPEN. P versus NP remains OPEN.

**Next acquisition:** a single authoritative original checker accepting genuine, source-bound mixed RES-to-AND3 or DEF-to-LOCAL-CONVERT shared dependency, with accepted and corrupted-port controls.
