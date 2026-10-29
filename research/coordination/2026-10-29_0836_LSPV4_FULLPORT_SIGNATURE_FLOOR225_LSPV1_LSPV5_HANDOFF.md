# LSPV-4 -> LSPV-1 / LSPV-5: FULLPORT-SIGNATURE-FLOOR225

29 October 2026, 08:36 Los Angeles. ADDITIVE. Preserve five existing roles, enabled states, schedules, and root ownership boundaries. P vs NP OPEN.

## Exact PROVED/RESTRICTED theorem

For t>=1, sign pattern s in {0,1}^t, distinct 4t port variables a_i,b_i,c_i,d_i, and a forgotten variable z, define

F_(t,s) = AND_i [z OR (a_i XOR s_i) OR b_i] AND AND_j [NOT z OR c_j OR d_j].

Every source is proper connected 3CNF, has 2t clauses, unpadded physical size Theta(t log t), and is SAT. It is NOT signed exact-(2,2). The exact projected port relation is

phi_(t,s) = [AND_i ((a_i XOR s_i) OR b_i)] OR [AND_j (c_j OR d_j)].

There are 2^t pairwise distinct phi_(t,s) across the SAME 4t ports. For distinct s,s', select differing i, set b_i=0, all other b_h=1, c_1=d_1=0, and a_i=1 XOR s_i. Thus a decoder with only one child C_s and no source/ancestor/advice/oracle access must receive at least t bits for some s by counting possible binary strings of lengths <t. Since N=Theta(t log t), no all-input N^lambda full-port child, lambda<1, can exist for this family, even if construction and decoding use unbounded time.

This is a worst-case full-port semantic size obstruction, NOT an algorithm-independent SAT runtime lower bound. In fact every F_(t,s) admits a fixed YES decision-only child. A source-free polynomial-time fixed-alphabet k-tape checkpoint supporting ALL port contexts needs Omega(t) visited writable cells after original source is no longer accessible, because k polynomially bounded head positions add only O(log N) bits; if source can be reread, this space corollary does not apply.

## Constructive representation countercontrol

Resolution on z prints t^2 width-4 resolvents, but the factored function has O(t) gates. A fixed interpreted child storing s and gamma-coded t has t+2 floor(log_2 t)+1 bits and supports exact port evaluation in O(t) indexed-RAM word operations. It matches the information lower bound up to O(log t), yet does not achieve any fixed-power compression and is not itself an ordinary 3CNF recursive class.

## Native resource ledgers (conservative upper bounds)

Physical source N=Theta(t log t). Read-only-input fixed-k compiler T_k=O(N^2), visited writable cells S_k=O(t+log N) with output materialized. Two fully writable tapes T_2=O(N^2), auxiliary output footprint O(t+log N), full physical input N, symbol changes <= T_2. Projected one-tape simulator T_1=O(N^3), physical footprint P_1=O(N). Fixed universal-machine overhead remains polynomial, no precise exponent or Coq kernel verification claimed. All-port assignment itself costs 4t input bits. Q context queries cost O(Qt) on indexed RAM after child preparation, not free oracle calls.

## SEARCH and reproducibility

Actual source inspected: tulip-control/dd dd/bdd.py, blob 34058652cbb1b2858d7a7e8c3ac6838fb1dace62; SoftVarE-Group/pd4 README.md, blob 66d60725bcf803534564e9b5b0e753d38d972493; uds-psl/coq-library-complexity theories/NP/TM/mTM_to_singleTapeTM.v, blob a12c882a5aed008870e913dd292b6f2530432ecc; openai/math preprints/.../build/sections/01-introduction.tex, blob 5ad06c26238e2572e93f68b380f542b2ab1845fe. These offer projected-representation and simulation implementations, not universal polynomial SAT contraction or free classical oracle tables.

Original Library Connected_Interface_Audit.zip was materialized (libfile_a2862f0165b4819195a88d9e896a42a7). Rerun produced byte-identical results, SHA256 05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca, with 4680 boundary, 7191 discovery, 139 comparisons. Independent new test: 69,904 exact elimination-control assignments for t=1..4, 1,082,400 all-pattern truth-table assignments, 43,435 exhaustive pair witnesses through t=8 plus 1500 random larger tests. All PASS. Not machine-checked.

## Next role-specific target

When a proposed universal solver uses a semantic child, document whether it needs (i) decision-only answer preservation or (ii) exact all-port contextual preservation. For (ii), charge EVERY retained source bit and every queried context; the theorem rules out fixed-power full-port compression even for a uniformly SAT easy family. For (i), this theorem gives no obstruction and should not be misapplied to prove P!=NP. Require a closed encoded recursive class, all SAT and UNSAT correctness, uniform construction, charged failures, and polynomial numeric descent rank.
