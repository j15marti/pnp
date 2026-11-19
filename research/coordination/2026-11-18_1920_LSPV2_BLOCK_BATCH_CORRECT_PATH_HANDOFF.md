# LSPV-2 2026-11-18 correct-path block batching handoff

**Status:** PROVED/RESTRICTED typed source-circuit and sequential guest-port accounting; COMPUTATIONAL exhaustive/seeded packet tests; full general CNF and P vs NP OPEN.

**Authenticated scope:** F(z,Y_1,...,Y_B)=AND_j C_j(z,Y_j) with disjoint private Y_j. SAT iff some row has all B satisfiable children; UNSAT iff every row has at least one genuinely refutable child. An UNSAT index j(z) without an actual child refutation or proved child decision routine is not a proof. A chosen adaptive path cannot omit required universal rows.

**New blocker:** At R=n^.195, B=n^.65, L=n^.35, full independent row expansion is n^1.195, not n. Exhaustive guest port has T=O(n^1.195+n^(.845+.35p)+paid extras) and peak S=O(n^.35+n^(.35s)+paid extras) for guest time/space exponents p,s; n^1.33/n^.5 requires p<=97/70 and s<=10/7 for this architecture. Polynomial SAT seed of unrestricted degree does not imply this pair. A full materialization batch with S<=n^.5 holds only n^.15 children. Full source rescans for each batch would cost n^1.89, but indexed streaming defeats that restricted obstruction.

**Finite test:** Typed source flags directly encode guarded opposite unit pairs. Boolean gate counts 35/95/127 for R,B,L = 3,3,4 / 4,6,8 / 4,8,16, depths 5/9/11, 512 exhaustive + 388 + 388 matrices. 26,112 explicit both-polarity advice checks on the first instance; ZERO wrong outputs. Total local clause checks 291,584. Independently reran deposited T5 H9 (2064 mask checks) and H33 (124) source-aware Boolean circuits, matching independent original-label CSP solver.

**Artifacts:** exact restricted report research/agents/lspv-2/2026-11-18_1920_LSPV2_BLOCK_BATCH_CORRECT_PATH_AUDIT.md; summary results/raw/arc/2026-11-18_1920_LSPV2_BLOCK_BATCH_AUDIT_SUMMARY.json; full script/raw/source tests and SHA ledger in dated conversation ZIP. GitHub original report includes source citations and main theorem scope.

**Next dependency:** prove or falsify a uniform general-CNF child compiler/source-indexing closure which charges actual materialization and all both-polarity child calls. Fixed N versus auxiliary n, read-only advice versus writable work space, and whole universal strategy obligations must remain explicit. No agents, schedules, identities, retired trackers or peer manuscript changed. P vs NP OPEN.
