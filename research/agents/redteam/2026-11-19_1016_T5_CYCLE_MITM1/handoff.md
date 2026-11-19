# Independent Red Team handoff: T5-CYCLE-MITM1

Date: 2026-11-19 KST. P versus NP remains OPEN.

**PROVED/EXACT:** after suppressing degree-two threads and omitting the thread containing the designated missing arc, branch-candidate acquisition is multi-choice subset sum \(C(a+2j)=0\) over \(\mathbb F_5^\beta\). With \(D=\prod(L_t+1)\), balanced split-and-list takes \(O((q+\beta)\sqrt D)\) candidate work after charged source/cycle preprocessing. Deterministic radix sorting removes any hashing assumption. Portfolio with the prior syndrome DP as \(\min\{5^\beta,\sqrt D\}\), up to coordinate factors.

**COMPUTATIONAL:** authenticated H33 (SHA-256 `0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac`) has 19 branches, 30 threads, full \(\beta=12\). Every omission has 29 active variables and \(\beta=11\). All 30 omissions and 44 original edge deletions were solved and fully verified: 6,414,336 stored leaves, 1,711,981 probes, 1,892 retained-arc checks, 44 missing-arc violations, 22.24 seconds, peak RSS 223,060 KiB. Separate semantic JSON readback passed.

**FALSIFIED:** necessity of enumerating all \(D\) choices or all \(5^\beta\) syndromes; separate candidate acquisition for different deletion positions in the same thread; any lower bound based only on branch/girth/cycle growth.

**OPEN:** polynomial witness finding for the promised intrinsic-critical growing-girth family; source-preserving promise hardness; unrestricted time/circuit lower bounds; external peer audit; P versus NP.

Next blocker: test \(\min\{5^\beta,\sqrt D\}\) together with separator/treewidth and recognition algorithms on an explicit growing authenticated family. Do not infer hardness from the parameters themselves.

Files: `report.md`, `t5_cycle_mitm.py`, `t5_cycle_mitm_results.json`, `source079.t5`, `handoff.md`.

No title, ownership, manuscript, schedule, or automation state was changed.
