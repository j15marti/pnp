# ARC-SELECTOR-SPACE-FIREWALL23 handoff

**Status:** restricted selector theorem PROVED/EXACT; independent peer review pending; P versus NP OPEN.

For `q=2^n`, there is a bit vector `y` requiring more than `floor(q/(16n))` gates over the complete binary Boolean basis. A proper-3CNF forcing family `F_y` fixes `q` designated variables to `y`; the new ARC negative-Horn/binary-XOR decomposition leaves both factors separately satisfiable and their conjunction exact. With padded input length

`N_n = 2^ceil((5/3)(n+log2(n)+10))`,

the mandatory designated-variable selector has more than `N_n^(1/2)` gates for all sufficiently large `n` (the finite audit first sees this at `n=156`). Thus “every child/factor has a witness” cannot be upgraded for free to one materialized square-root-space witness-selector circuit. This is only a representation firewall: `y` is explicit in the source, direct indexed access or streaming can bypass selector materialization, and the formulas are easy. It proves no SAT time/space lower bound.

- **:00 MCSP:** attempt an explicit, source-checkable ordinary KT target rather than this nonconstructive counting `y`; forbid an `M`-bit side table.
- **:12 Universal Solver:** audit whether any certificate/portfolio merely stores the whole selector; record certificate acquisition and peak space.
- **:24 ARC:** seek a correct all-input Horn/XOR gluing rule that uses indexed source access without materializing a selector; charge two recursive iterations.
- **:36 Red team:** attack explicitness and the padding/encoding ledger; exhibit a streaming/direct-access bypass and confirm that it does not yield the desired contractor.
- **:48 Synthesis:** keep this result as a quantifier/representation firewall only. The weakest arrows remain total deterministic `R_k` and the all-input hereditary ARC successor.

Audit: `experiments/review/2026-10-20_arc_selector_space_firewall_audit.py`; 1,108 checks, zero failures; no randomness.

