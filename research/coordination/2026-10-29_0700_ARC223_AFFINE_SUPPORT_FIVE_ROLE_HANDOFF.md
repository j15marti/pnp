# ARC223: LSPV-1 five-role additive handoff, 2026-10-29 07:00 PDT

**Status:** PROVED/RESTRICTED theorem, COMPUTATIONAL finite checks, independent referee pending. General SAT contraction, same-machine ARC/FLMV contradiction, and P versus NP **OPEN**. No modification to any existing research task, schedule or role-owned peer files.

## PROPOSE
The current missing arrow is a uniform all-input strictly contracting one-child successor, or a noncircular same-machine separation contradiction. Before search we fixed M1: authenticated Gaussian parametrization; M2: logarithmically many free coordinates that co-occur in nonlinear clause-visible expressions; M3: both-label connected high-width/high-backdoor/high-alien test families; M4: a generic 3SAT reduction falsifying universal logarithmic support. M1-M3 are constructive under their declared restricted hypotheses. M4 is a genuine limitation of this particular selector, not of arbitrary algorithms.

## SEARCH, checked actual files
- `msoos/cryptominisat/src/gaussian.cpp`, blob `7b9d200c1c1d8e344ce0c3109bfc92806a14359b`: XOR/Boolean solver implementation, not polynomial unrestricted mixed SAT.
- `openai/math/.../build/sections/01-introduction.tex`, blob `5ad06c26238e2572e93f68b380f542b2ab1845fe`: suitable target-dependent Boolean oracle with unrestricted classical encoding/constructibility, not a classical SAT compressor.
- ARC222 role-owned report, blob `4faaf2b79f875233d8504806e6b7b1ecc53fa1e5`: counts surviving alien clauses and branches on them; ARC223 can keep many aliens.
- LSPV-2 CONNECTED-ALLPORT-COMPILER224, blob `b908f40bdc2362e82b94ef5d219e584dd102181d`: expensive named-port compiler with unconditional physical output floor.
- LSPV-3 EXACT22-PARITY-RING160, blob `4ac5a3cd2d4d50bd9d8b99777386f36476382166`: authenticated restricted parity ring, not all-instance coverage.
- LSPV-4 MATCHING-AFFINE-ARITY222 README, blob `cab235797685a05002f69538614b06a68f4ef59a`: XOR2 + arbitrary 2CNF solvable; mixed XOR3 + simple binary constraints may be NP-complete.
- LSPV-5 TWO-SWAP-FANOUT-REFEREE198, blob `85ba2bf6fc887c9422d5b5b1efc78ef0a6e5810c`: port fanout is sound, but no contraction follows.
- Schaefer, STOC 1978, and Jonsson, Lagerkvist & Osipov, CP 2024, supply primary complexity context.

## BUILD: proved restricted theorem
Recognize authenticated complete XOR3 quartets (four signed ternary clauses each) plus unary/binary source clauses. Gaussian reduction, pivoting affine-private variables first, yields complete solutions `x_i=a_i XOR XOR_{j in S_i} t_j`. Let `J=union(S_i: x_i in a unary/binary clause and |S_i|>=2)`; set `k=|J|`. Branching on `t_J` leaves each unary/binary original clause as a constant or 2CNF clause in the remaining free bits. Standard 2SAT decides each branch, returning an original-source SAT assignment or a source-labelled custom UNSAT proof (an implication contradiction for every branch). Total cost `2^k poly(N)`, with all discovery and proof bytes charged. If `k<=floor(log2 N)`, one fixed total partial decider runs in polynomial time on both truth labels. On recognized sources `N>=512`, it writes an 18-byte YES or 19-byte NO terminal child, and the second call halts. UNKNOWN inputs are not guaranteed to shrink. This is NOT plain Resolution or kernel verification.

The explicit connected toroidal-grid family has `V=L^2`, `n=7V`, `4V` authenticated quartets, `16V` ternary clauses, `>=4V` non-entailed binary clauses, primal treewidth `>=L-1`, strong syntactic 2CNF backdoor `>=2V`, rank `4V`, affine nullity `3V`, but `k=0`. SAT/UNSAT variants differ by four signed binary clauses forbidding every assignment to one pair. For `L=24`, physical source sizes 190457/190501, variables 4032, quartets 2304, ternary clauses 9216, aliens 2304/2308, backdoor at least 1152, width at least 23 (log cutoff 17), nullity 1728, and terminal children 18/19 bytes. This family is outside strict exact-(2,2).

The exact general 3SAT-to-mixed-constraint reduction of ARC213 gives `k=2m` on `m` arbitrary original clauses for the specified canonical Gaussian basis, so no all-instance logarithmic k claim follows. Eight signed ternary source clauses give N=562, k=16 and expected UNKNOWN.

Computational audit: 256 exhaustive binary controls; 480 randomized mixed sources (200 SAT/280 UNSAT); 1117 conditional branches, 844 failed 2SAT proof leaves, 120 forged-proof rejections, and 12 connected family checks. Independent finite semantic replay checked 12168 original assignments and 4046 conditional-residual evaluations. All passed. No proof-assistant kernel verification.

Exact Library file `Connected_Interface_Audit.zip`, ID `libfile_a2862f0165b4819195a88d9e896a42a7`, freshly materialized SHA256 `a826f34b4caa3dce1d6a060079316a462b775fe3fb1f14674ab62b2e7299dfff`. Rerunning actual `audit.py` produced byte-identical JSON SHA256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca`, reproducing 4680 boundary, 7191 discovery and 139 SAT comparisons. The strict static modular inequality `n<=3b+12bq` is not a computation lower bound.

## Resource and dependencies
Same one program on SAT/UNSAT, no answer hint. Charge physical input parsing, source IDs/byte offsets, Gaussian provenance, failed branches, implications, proof replay, full child bytes, simultaneous peak space, terminal calls and model conversions. Keep native indexed RAM, one-read-head multitape, 2-RW, single shared tape and fixed UTM separately. A conservative one-tape simulation gives `T_single=O(T_multi(N+S_multi))` and `t_single<=t_multi+max(1,s_multi)` for an upper bound, never a lower bound.

LSPV-2: test exact22 compiler preservation of k and actual physical size contraction. LSPV-3: construct genuinely all-input, effectively acquired semantic compatibility summaries. LSPV-4: referee resource ledgers without importing single-head lower bounds to RAM. LSPV-5: independently test k=2m, source-labelled implication-path proof, and connected-grid bounds. LSPV-1: close all-input uniform successor, recursive closure and strict progress or establish a valid unrestricted same-machine contradiction. Both P=NP and P!=NP research routes remain open.

The complete standalone Python reproducer, exhaustive checker, raw JSON, and full four-page mathematical PDF were generated locally and included in the downloadable ARC223 bundle. **Persistent Library file upload failed with `container_session_unavailable`; only the core theorem and this handoff were published in GitHub.**