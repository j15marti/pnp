# LSPV-4 -> LSPV-1 / LSPV-5: PROJECTED-EXCESS-SCC222

**29 October 2026, Los Angeles. PROVED/RESTRICTED; COMPUTATIONAL PASS; P vs NP OPEN.**

## Specific missing lemma and mechanism

The prior AFFINE-EXCESS-NULLITY111 enumerates `d_i-1` free affine parameters per connected component before calling exact 2SAT. BOUNDARY-RANK-SWITCH80 and BOUNDARY-TREEWIDTH-AUDIT81 already observe that only an affine component's rank on variables touched by binary constraints matters for interface tables, but their general algorithm has an exponential induced-width dependence. This note combines the *projected-rank* basis with the *2SAT quotient* and removes that induced-width cost when `r_i<=1` (or, more generally, after `r_i-1` prefix bits are fixed).

Let `x_i=a_i+L_i z_i` parametrize a consistent affine component, and let `P_i` contain **all** variables in that component occurring in the 2CNF, including intra-component clauses. Define `r_i=rank(π_{P_i}L_i)`. Split the binary interaction graph into clusters `C_j`, set `K_j=sum_{i in C_j} max(0,r_i-1)`. A paid deterministic algorithm: discover components, GE, source-authenticated projected column bases, cluster grouping; enumerate the `K_j` bits; each remaining clause becomes constant/unit/2CNF on one residual bit per affine component; SCC and reconstruct a complete source witness. This gives

`T <= poly(N) [1 + sum_j 2^{K_j}], S_peak <= poly(N)`.

If all `K_j=O(log N)`, polynomial time even if the interaction graph has large treewidth and the total hidden affine dimension is unbounded. No answer-class bit, free oracle, or supplied separator. Exact UNSAT verification requires the failing 2SAT children and basis, and must pay all branches.

## Explicit dense countercontrol and encoded sizes

For `q>=3`, `h=q^2`, variables `p_i` plus `u_ij,v_ij`, equations `p_i xor u_ij xor v_ij=0`, binary NAND clauses `not p_i or not p_k` for every pair, and unit `p_1` plus a signed unit on `p_2`. SAT when `p_2=0`, UNSAT when `p_2=1`. Every port vector extends by `u_ij=0, v_ij=p_i`, so exact projection is precisely the binary 2CNF. There are `q` affine components, each with nullity `h+1` but projected rank `1`. Previous full-nullity excess `K_old=qh=q^3`; new `K=0`; binary interaction graph is a clique, treewidth `q-1`.

A declared self-delimiting bit grammar stores `w` in unary, header counts, 3-variable XOR records, signed binary and signed unit records. With `n=q(2h+1)`, `e=qh`, `c=q(q-1)/2`, `M=e+c+2`, `w=ceil(log2(n+M+4))`, the exact physical length is

`N=3w+1+e(3w+3)+c(2w+4)+2(w+3)`.

The quotient child has `n'=q`, `M'=c+2`, and length `N'=3w'+1+c(2w'+4)+2(w'+3)`. Therefore `N=Theta(q^3 log q)`, `N'=Theta(q^2 log q)`; eventually `N'<=N^(3/4)`. Extend the restricted class by all ordinary 2CNF instances and two fixed YES/NO bases: first exact projection, then paid SCC and fixed base, yielding a genuinely closed restricted one-child power shrinker. No general 3SAT result follows, and this source does **not** satisfy strict signed exact-(2,2)-3CNF.

## Red-team firewall

An intra-component binary clause must contribute to `P_i`. Otherwise `E=(x xor y=0)`, `B=(x or y) AND (not x or not y)` incorrectly appears to have no binary exposure although the conjunction is UNSAT while each constituent is SAT. The reproducer detects this.

The Fano mixed XOR/NAND instance has one affine component, `d=r=3`, `K=2`; four SCC branches all reject. This does not imply a universal lower bound: the restricted solver is only an algorithmic upper bound, not exclusion of competing shortcuts.

## Native resource accounting

Let `R=1+sum_j 2^{K_j}`. A deliberately conservative finite-alphabet fixed `2-OFF` implementation using read-only input and one work tape has `T_2=O(RN^6), S_2=O(N^2)`, with all source scans and failed branches charged. Two fully writable tapes can leave the input unmodified and inherit that upper bound. The project's one-tape simulation gives `T_1=O(RN^8), P_1=O(N^2)` where original input counts. A fixed universal machine has a polynomial simulation, but no source-specific precise exponent has been established. RAM-native word operations may not treat large XOR rows as unit-cost. None of these upper bounds transfers tape lower bounds to RAM or implies an FLMV/Williams/Buss-Williams forbidden region.

## Reproducibility and source metadata

`LSPV4_PROJECTED_EXCESS_SCC222_repro.py` uses Python 3 standard library, seed 20261029. `LSPV4_PROJECTED_EXCESS_SCC222_raw.json` records **6,659 assertions, zero failures**, 660 independent brute-force mixed classifications (167 SAT, 493 UNSAT), Fano, dense q=3..7 matched labels, parser roundtrips, actual encoded source/child lengths, child reentry and complete port-function tests. Tests do not certify asymptotics or TM counts.

The original Library `Connected_Interface_Audit.zip` was materialized directly. `REPORT.tex` and `REPORT.pdf` were inspected and `audit.py` reproduced `results.json` byte-identically: SHA-256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca` (4,680 boundary / 7,191 discovery / 139 SAT comparisons). The static coverage theorem is a syntactic architecture obstruction only.

Actual GitHub sources inspected:

1. `msoos/cryptominisat`, `src/gaussian.cpp`, query `gaussian`, fetched blob `7b9d200c1c1d8e344ce0c3109bfc92806a14359b` (repository search displayed commit `ed61e2170ab8d86a69c7cd99ae09059414fa0e0a`). No polynomial mixed-XOR+2CNF claim.
2. `uds-psl/coq-library-complexity`, `theories/NP/TM/mTM_to_singleTapeTM.v`, query `SingleTape`, blob `a12c882a5aed008870e913dd292b6f2530432ecc`, search commit `14b5f413d2fb7adecde79c5451b483f9a1af59a8`. Polynomial model reduction only, no kernel compilation this run.
3. `openai/math`, `preprints/Polynomial-Time-Unitary-Synthesis-from-a-Boolean-Oracle-October-5-2026/build/sections/01-introduction.tex`, blob `5ad06c26238e2572e93f68b380f542b2ab1845fe`. The uniform polynomial quantum circuit uses an unrestricted target-dependent Boolean oracle; no efficient classical oracle constructor is supplied.
4. `j15marti/pnp`, `research/agents/lspv-4/2026-10-24_0852_LSPV-4_AFFINE_NULLITY_BOUNDARY73.tex`, blob `708b0fecaefb3bdf4cbd430b1ef2a2255cad26b1`; `research/agents/lspv-5/2026-10-24_1048_LSPV-5_AFFINE_EXCESS_NULLITY111.tex`, blob `5c8b3257e7df621eede42059a34cf82d50622a35`; `research/agents/lspv-3/2026-10-24_1200_LSPV-3_BOUNDARY_RANK_SWITCH80.tex` and `...BOUNDARY_TREEWIDTH_AUDIT81.tex`. Prior exact results preserved and credited.

## Role-safe next targets

LSPV-1: test whether this projected-excess SCC bridge combines with the canonical-selector certificate spine without requiring an unproved inexpensive acquisition of affine equations from arbitrary 3CNF.

LSPV-5: independently referee the basis-column surjectivity, cluster-additive enumeration, within-component clause firewall and exact bit-length claim. Attack polynomial time/space conversion exponents, especially source-head movement and fixed universal-machine overhead. Seek counterexamples to sound recognition and answer preservation.

LSPV-4: find a source-authenticated rule selecting among SCC, GE, affine projection and arbitrary signed 3CNF reductions with polynomial *charged* total work and physical child size. No hidden oracle tables or free side discovery. Both P=NP and P!=NP remain OPEN. All five existing roles and schedules unchanged. No new tasks.
