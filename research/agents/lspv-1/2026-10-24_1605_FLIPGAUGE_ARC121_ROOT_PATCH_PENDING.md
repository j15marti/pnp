# Root main.tex LSPV-1 reconciliation pending (FLIPGAUGE-ARC121)

**Status: WRITE BLOCKED, NOT RECONCILED.** Report, executable compact reproducer, results summary and science handoff are verified on GitHub under the same timestamp stem. The separate attempt to update only the LSPV-1 ownership region in root `main.tex` was blocked by connector safety checks. No root commit or successful root readback is claimed. Do not overwrite other roles or the document body. Root `main.tex` was read at blob `9afd01b452578f4e5f1c49a8b1a6e2f612fca551` before the blocked write; it can change concurrently.

## Intended placement and exact scientific update

Insert after `% BEGIN LSPV-1 OWNED` and `\\section{LSPV-1 (structure and charged acquisition)}`, before ARC-CHANNEL-CURVE119, without deleting or modifying other content:

```latex
\\paragraph{FLIPGAUGE-ARC121 (24 October 2026): a complete-state bit-activity firewall.}
\\textbf{PROVED/EXACT in a deterministic autonomous bit-local machine model, independent review pending.}
For one halting execution with $T$ genuine steps and faithful complete configurations $C_i$,
define $\\Delta=\\sum_{i<T}d_H(C_i,C_{i+1})$.
Deterministic nonstuttering gives $T\\le\\Delta$; when one primitive changes at most
$b$ complete-state bits, $T\\le\\Delta\\le bT$.
This is a model-specific identity, not a separate SAT lower bound or new FLMV endpoint.
An FLMV indexed read may erase a long index tape in a single macrostep, so
bit-local simulation is not free.
\\textbf{COMPUTATIONAL:} 2,046 bitstring traces and five paired formula controls
agreed, zero failures. Ten zero source bits require ten charged reads and ten
unchanged accumulator writes but zero accumulator flips; complete address/control
activity remains charged. A 174,592-assignment strict-clause-child SAT/UNSAT
reproduction duplicates the earlier MINIMAL-UNSAT-PROJECTION20 firewall.
\\textbf{ARC-EDGE-90 OPEN; P versus NP OPEN.}
Verified report, code, raw summary, and peer handoff:
\\path{research/agents/lspv-1/2026-10-24_1605_LSPV-1_FLIPGAUGE_ARC121.tex}
and adjacent same-prefix files.
```

## Reconciliation guard

Refetch current root blob SHA and full body. Replace or insert only inside the unique LSPV-1 marked region. Verify exact outside-region byte preservation, balanced BEGIN/END LSPV-1..5 markers, and the executive OPEN status. Commit and read back only after authorization succeeds. This is a work item, not evidence of a completed root edit.

<!-- END_OF_PENDING_ROOT_PATCH::LSPV-1::FLIPGAUGE_ARC121 -->
