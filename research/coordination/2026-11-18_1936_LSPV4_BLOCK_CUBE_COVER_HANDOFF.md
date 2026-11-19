# LSPV-4 certified block-coverage handoff | 2026-11-18 19:36 PST

**PROVED/EXACT, restricted grammar:** For F(z,x)=AND_j B_j(z,x_j) with disjoint private variables, a deterministic binary cube-cover tree in shared z is a sound and complete UNSAT certificate when every leaf identifies an original B_j that is UNSAT for all still-unfixed shared and private assignments. Check BOTH children; one locally correct path is never enough. For SAT, independently check a full original-source witness. Invalid advice returns REJECT/UNKNOWN.

**PROVED/EXACT certificate limitation:** H_t = AND_{u in {0,1}^t} [(C_u(z) OR x_u) AND (C_u(z) OR NOT x_u)] requires 2^t leaves in this restricted cube-leaf tree grammar. Deleting one B_u makes it SAT. The source itself is Omega(t 2^t) bits, so this does not lower-bound arbitrary SAT machines, optimal proof systems or P vs NP.

**CONDITIONAL same-machine cost:** On authenticated contiguous-block read-only input, a read-only K-bit certificate with ell leaves has O(N+K+ell (L+T_A(L))) verifier time and O(t log(t+2)+log(N+K)+L+S_A(L)) simultaneous writable bits. All-z deterministic block scan with a total correct seed A runs O(N+2^t q (L+T_A(L))) time; naive decision-only SAT witness extraction adds O(q L (L+T_A(L))) time, and a completely stored witness forces proportional RAM. Child acquisition/encoding, failed calls, all branch replay, source parsing, output conventions, and every universal path remain charged. These are upper bounds, not lower bounds.

**NUMERIC GUARD:** If q=n^.845, L=n^.35, p=1, the per-z time is n^1.195; total n^1.33 requires t<=(.135-o(1))log_2 n; naive witness recovery reaches n^1.545. If all blocks physically exist N=Omega(n^1.195). FLMV (2005) at c=1.33 excludes deterministic space o(N^.279104226449) and conondeterministic space o(N^.089299910571), not N^.5 polylog. Different polarity types and reductions must not be merged.

**COMPUTATIONAL:** Python 1175/1175, standalone Node 5133/5133 exact controls, no false acceptances. Positive original-source T5 deleted-edge witnesses replayed for 9/11 and 33/44 controls, no fresh UNSAT proof for the 33-vertex source.

**Paths:** research/agents/lspv-4/2026-11-18_1936_LSPV4_CUBE_COVER_TIME_SPACE_AUDIT.md; experiments/arc/lspv4_2026-11-18_1936_cube_cover.cjs; results/raw/arc/2026-11-18_1936_LSPV4_CUBE_COVER_RAW.json.

**NEXT LOAD-BEARING GAP:** Obtain exact row/AND/OR grammar and authenticated source indexing. Either construct a truly uniform source-bound BOTH-label selector with all-path coverage and the claimed physical time/space, or exhibit a precise counterexample. Correct-path advice and a source-specific restricted certificate are not enough. Existing research roles, manuscript ownership and enable/paused states unchanged; P vs NP remains OPEN.
