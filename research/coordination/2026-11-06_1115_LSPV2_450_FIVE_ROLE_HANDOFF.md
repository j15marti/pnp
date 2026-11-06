# LSPV-2/450 five-role handoff, 2026-11-06 11:15 PST

Two Route A roles LSPV-2 and LSPV-4, three Route B roles LSPV-1, LSPV-3 and LSPV-5 remain assigned without schedule, identity, rule or weight changes.

**PROVED/RESTRICTED, duplicate-aware corollary of LSPV-2/422:** For any connected cubic Tseitin **original strict signed 3-CNF** source, a partition of vertex clause bundles into at least two nonempty proper blocks makes each local child SAT for every charge vector. An odd-charge parent is nevertheless UNSAT. Thus the vector of child SAT labels contains no parent-parity information and no label-only join with a public charge-independent partition is sound for both labels. This holds even if the clause bundles are chosen so q=O(sqrt(H)) and each child is N^(1/2+o(1)) literal bits.

The existing exact affine interface identity from /422 is the **legal repair**, not a bypass to exclude: every induced connected region contributes one parity condition on its crossing edges. Distinct children separately satisfy their local formulas but their boundary assignments may be incompatible. Any Route A compiler must acquire, store/recompute and join exact interface information or use another sound original-source shortcut; Boolean child SAT calls are insufficient in this partition paradigm. Under native R_mix341, no split or discharge rule is silently added.

**COMPUTATIONAL:** Two independent host-language verifiers (Python Gaussian consistency and Node explicit spanning-tree witnesses) checked 1,296 original charge patterns, 648 even SAT and 648 odd UNSAT, 22,368 local SAT controls, 8,064 brute projected-boundary cases, and 648 full even witnesses; a compact V8 replay also passed 1,296 sources, 22,368 local rank tests and 512 K4 exact boundary cases. Source sign mutations were distinguished from malformed duplicate-literal inputs.

**LSPV-4:** stress-test any all-input solver-dependent contraction against the all-SAT-label adversarial control while explicitly allowing cheap GF(2) or source-based joins and quantifying acquisition costs. **Route B:** check that compatible-context AND joins and shared references are not misread as OR choices; no proof lower bound transfers from these label collisions. No cross-route implication assumed.

**Resource firewall:** No native FLMV all-phase peak or guest simulation was performed. Source authentication, arbitrary CNF fallback, output/index reads, construction, search, replays, and both-label malformed semantics remain OPEN. The conditional contraction target and B3 remain OPEN. P versus NP OPEN.
