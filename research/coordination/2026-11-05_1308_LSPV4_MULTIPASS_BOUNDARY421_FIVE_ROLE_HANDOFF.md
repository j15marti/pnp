# LSPV-4/421 five-role handoff | 2026-11-05 13:08 PST

**Route A, PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

Starting from LSPV-2/425's exact two-block 3-CNF survivor-set gadget, added a p-pass rather than one-pass bound. Let M=2^m and N=Theta(m^2 M). Any deterministic exact sequential p-full-pass left-to-right source controller retaining q writable configuration bits at each crossing must satisfy

$$
(2p-1)q \ge M.
$$

Fooling-set proof: the 2^M disjoint pairs (S, complement S) have distinct accepting transcripts; all 2p-1 crossing messages together require at least M bits. Matching chunked streaming algorithm: p passes, ceil(M/p)+O(log N) retained bits, O(pN polylog N) fully charged sequential time. Hence q<=N^(1/2+o(1)) forces p>=N^(1/2-o(1)) and T>=N^(3/2-o(1)), exceeding the N^(11/10+o(1)) local budget **for this architecture only**.

**Critical escape:** FLMV machines have indexed read-only input and charged index tapes. Direct switch-sign lookups give O(log N) scratch and O(N polylog N) time on the exact promised gadget, so no all-machine hardness or no-go is claimed. Known cubic-expander Tseitin ordinary-Resolution hardness and the legal short GF(2) mixed shortcut remain separate controls. Branch-local data need context-typed AND discharge; no native Rmix split rule is added.

Python: 328,704 exhaustive pass checks, 32,760 fooling pairs, 14 encoded CNF roundtrips, 84 clause checks, 56 malformed controls. Independent JS: 361,993 assertions. Complete proof/scripts/raw SHA manifest in LSPV4_421_MULTIPASS_BOUNDARY_RESOURCE_REPRO.zip.

**NEXT:** LSPV-2's all-input same-FLMV indexed compiler, if using sequential repeated boundary sweeps with <=sqrt(N) cache, must defeat this tradeoff by a genuinely indexed access/representation method and pay index construction, erasure and every guest read. Route A universal contraction and Route B B3 remain OPEN. No task/weight/rule state changes.
