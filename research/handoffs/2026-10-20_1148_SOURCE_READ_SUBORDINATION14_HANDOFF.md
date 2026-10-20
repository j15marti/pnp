# SOURCE-READ-SUBORDINATION14 handoff

Timestamp: 2026-10-20 11:48 KST. **P versus NP remains OPEN.**

New exact synthesis:

1. Source-dependent advice computed from charged source reads introduces no alphabet factor `B`: couple the entire pipeline along the single zero-source execution. Divergence probability is at most `E[1-C(N-u,k)/C(N,k)] <= kE[u]/N`.
2. For `M=N^a`, reads `N^r`, retention `N^z`, generation `Mp^B,p^E`, and one fixed MMW solver `(C,D)`, the composed exponents are
   `t=max(r,a(1+max(B,C+1)/kappa))`,
   `s=max(z,a max(E,1,D)/kappa)`.
3. At `a=6/5`, a full scan is subordinate to output; only `r>=241/200`, `z>=1/2`, or `B/kappa>=1/240` directly fails the strict box. Existing `Omega(N/(wk))` named-read bounds are accounting firewalls, not main-route lower bounds.

Assignments: :00 give one target generator with `(r,z,B,E)`; :12 test no-rewind consumption; :24 separate ARC reads from retained state; :36 force one strict threshold or retire the attack; :48 preserve model boundaries.

Root `main.tex` was not edited: blob `7022882d7a8df0cd8672ea7b603780b6a932f14f` still contains a literal truncation marker.
