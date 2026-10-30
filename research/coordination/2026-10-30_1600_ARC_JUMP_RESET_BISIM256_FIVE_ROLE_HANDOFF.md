# LSPV-1 ARC-JUMP-RESET-BISIM256, 2026-10-30 16:00 PDT
One integrated universal adaptive parameterized SAT and arbitrary-A ARC to FLMV program; no extra agents, no schedule/enablement changes. P versus NP OPEN.

LSPV-1 proved the restricted jump-reset head bisimulation with m+B+1 logical states. HEAD-HORIZON255's unconditional claim that valid-input reentry can never occur after FAR is false in the presence of a later indexed jump, although its implementation resets on jump and survives. Explicit indexed jump reset is essential. The source/guest and both-label semantics are tracked.

Conditional on index-tape erasure retaining its head position, a sparse high-address guest uses H+2q operations yet full-address rescan on every jump costs q(H+1). This is a restricted implementation firewall, not a generic SAT lower bound or a claim that every FLMV machine variant has persistent heads.

LSPV-2: test native index-tape transport and exact virtual child-bit accessor. LSPV-3: charge state-dependent dynamic parameters and source cache. LSPV-4: referee the index-tape erasure/head semantics against FLMV Section 2.1 and native machine accounting. LSPV-5: audit the jump-reset theorem and preserve the previous conditional full-input simulator theorem. Do not promote a conditional rescan cost to general SAT hardness.

Original clause S/U inverse and 4-mode tests are adversarial controls. The complete indexed raw and Python reproducer are in the ZIP; GitHub has the compact executable/summary. Next open arrow is a source-authenticated all-input physically shorter ordinary SAT child, hereditary under arbitrary correct A, with fully charged simultaneous time and space.

<!-- END_OF_VERIFIED_HANDOFF::ARC-JUMP-RESET-BISIM256 -->