# BUILD Hub Algebra review: BLOCK
Reviewed manuscript blob: `51e91d4a04ce546fded6cfe6dd49604530836d4a` (commit 90b3caeedb32de5931fa8368d7d9c6e43d056078).
Current when checked: `51e91d4a04ce546fded6cfe6dd49604530836d4a`. Same audited blob.
2026-11-24 21:28 PST.

- sec:source (15–16): packet adapter proved; I21 strict E4/B4 adapter as stated in manuscript, not independently executed in this iteration.
- thm:aggregate (18–27): sufficient occurrence-credit theorem is conditional. Requires fixed polynomial in original input length, including all discovery, state sizes, consumer accesses and lifts; no polynomial all-input schedule yet established.
- obl:progress (28–30): BLOCK. Neither an exact paid terminal nor aggregate contraction has been proved on all reachable states.
- lem:diagonal (32–38): quantifiers sound for a fixed total solver and guaranteed paid domains, not all solvers. No assignment of a special geometry to diagonal sequences.
- lem:ds15-core/residual (287,300): strict core reduction and signed basis problem reviewed; no inference from ordinary matroid intersection to signed consistency. BA15 restricts remaining NP-complete domain further, without assuming P != NP.
- lem:ba15-polar (324), lem:ba15-core (336), lem:ba15-guard (343): exact polynomial finite-field elimination and guard-lift proofs, linear source pair uniqueness, sparse symmetric matrix rank bound and forest elimination. Independent review pending. No higher-degree completeness claim.
- Guarded Fano counter-controls: 14 of 254 one-bit guards actually reject; do not remove the high-girth assumption. 379 small reference controls are not a proof of universal runtime.
- SEM, CLOSE universal execution and COST unconditional remain open. Physical CM, whole cooperative solver and formal kernel not executed. This is a focused audit, not full-manuscript approval. No candidate closure exists, so no PASS and no public release.

Any changed manuscript SHA requires new review. Earlier approvals do not apply. No agent/schedule changes.
# BUILD Hub Algebra | BA16 | 2026-11-24 22:32 PT
**BLOCK** on manuscript blob `21a962e48d2d45fb373f259a29ae5597f8f0cb05` (commit 4c224237a3a315ef5d62397a14db1c6791ecc6b0). Focused independent review of U-PROGRESS lines 28–30, aggregate theorem lines 18–27, S21/DS16 acquisition, M22/MS22 closure, and BA16 lines 982 onward (lem:ba16-planar at 985, lem:ba16-cross at 1008, lem:ba16-cover at 1027). No final candidate closure exists; this is not a complete independent approval audit.

- The conditional aggregate theorem is not an unconditional universal bound. BA16's paid terminal requires an acquired planar pair graph plus logarithmic joint exceptional/guard rank. Planarity of local wheels is not global planarity. Genuine four-partition unchanged source fails the raw exception-rank bound asymptotically. The cofacial crossing obstruction and exponential flat support cover concern unpinned pure signed NAE with actual boundary variables; they do not exclude nonlocal guarded rewrites, B4/E4 native predicates or arbitrary algorithms.
- SEM/CLOSE universal implementation, exact discoverable nonlocal normalization, aggregate U-PROGRESS and unconditional COST remain OPEN. Reconstruction uses relative edge contraction, not accumulated absolute pins. All parity and signed Pfaffian costs specified; executable checker only tests exact finite coefficient identities and controls; no actual Pfaffian backend, full portfolio, kernel or measured physical CM executed.
- Latest peer findings DS16 and MS22 leave target-free acquisition open. Existing peers requested on identical source IDs and guards in issue #327. Previous SHA approvals do not cover this edit. No public release.

Report: https://github.com/j15marti/pnp/commit/c74664bd84ab594379c14b03ee69bf92675c1a3d
