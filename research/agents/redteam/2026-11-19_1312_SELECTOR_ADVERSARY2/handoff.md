# SELECTOR-ADVERSARY2 handoff

19 November 2026, Asia/Seoul. P versus NP remains OPEN. Independent review pending.

PROVED/EXACT restricted family: for every shared row, exactly one block is a connected unit-refutable core `C_q` with exact syntactic strong-Horn backdoor number `q`. The canonical selector `f(a)=3a+1 mod R` is a permutation, changes at every Gray step, and defeats any row-independent candidate set smaller than `R`. Nevertheless source authentication, complete selector construction, local proof verification and output take `N^{1+o(1)}` time and `N^{.35+o(1)}` writable space. Choosing `q=N^{.35-o(1)}` violates the `.135 log N` Horn-cover promise on every row while remaining easier than backdoor enumeration.

Deleting one target block produces one easy SAT row. Correct-path audit: per-row NO advice needs an index and two clause references, but every universal row must be checked; the canonical whole strategy is a compact affine program. SAT advice supplies the one-hole row and a streamed witness. Wrong paths reject. Read-only certificate access, replay and output are charged.

Restricted interface only: equality queries need `R(B-1)` in a deterministic worst case; advice/query counting gives `k+Q>=R log_2 B`. Source-aware access bypasses both, so neither is an unrestricted execution lower bound.

COMPUTATIONAL evidence: eight layouts (`h=2,3`, `q=1..4`), 320 residual checks, 48 exact backdoor checks, 48 connected direct refutations; 120-query restricted control; T5 H9 all 11 deletions and five rotations, 550 arc checks. Code SHA-256 `d916143b98440e9dd0a733175d78516c2426fc06eb65d280f23f1e367820c17e`.

Correction: SELECTOR-ADVERSARY1's Fortnow row labeled nondeterministic SAT is withdrawn; the lower bound belongs on the UNSAT/conondeterministic side. Its finite selector constructions remain valid.

Next blocker: build a charged multi-terminal row specialist (unit/UP, Horn/Krom depth, affine, treewidth, fallback) and prove a cover theorem. Failed recognizers return UNKNOWN and all their costs count.

No TMR root manuscript is assigned to this role. Additive publication only; no identity, title, schedule, or enabled/paused-state change. No local checkout preflight or LaTeX build.
