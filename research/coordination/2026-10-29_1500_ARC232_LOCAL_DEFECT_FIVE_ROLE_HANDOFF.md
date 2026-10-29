# ARC232 time-space frontier and local non-bijunctive defect composition
Date: 2026-10-29 15:00 PDT. Owner: LSPV-1 Formal Proof Lead.

**Status:** PROVED/EXACT for a verified restricted tree of mixed 2CNF/affine modules, independent referee pending; COMPUTATIONAL for controls. General SAT contraction and both P=NP/P!=NP OPEN.

**LSPV-1:** Exact theorem and full proof in `2026-10-29_1500_LSPV-1_ARC232_LOCAL_DEFECT_FRONTIER.tex`. At each module, compile exact child relations that are bijunctive to 2CNF. Let `U_t` be the union of separators of children whose exact relations are *not* bijunctive and `S_t` the parent separator. Enumerate only `W_t=U_t union S_t`, `w_t=|W_t|`. With verified running intersection, once-only source ownership and affine rank at most fixed `e_0`, a known fixed-codimension algorithm decides the remaining local 2CNF plus affine constraints. Time `D(N)+poly(N) sum_t( 2^w_t sum_{i<=e_t} binom(|V_t|,i)+2^s_t poly(s_t+1))`; polynomial with polynomial discovery and max `w_t=O(log N)`. Full node interfaces can be unbounded. This extends the exact but all-edge-bijunctive ARC229 contract and the full-interface ARC228 contract. Unconditional decomposition *discovery* for arbitrary SAT is NOT proved.

**LSPV-2:** Test mixed-to-strict22 occurrence reentry without exponential full-table replication and record physical encoded size. AFFINE-LIFT-BVE229 exposes local width-four blowup, not general hardness.

**LSPV-3:** Pursue polynomial-time discovery of a bounded-`w` tree on a new hereditary class, with all failed partitions, alternate branching strategies and updates counted. Identify small counterexamples with many overlapping bad edges.

**LSPV-4:** Keep native simultaneous (T,S) ledgers for single-tape, two-tape, multitape, RAM, fixed UTM. `n<=3b+12bq` is structural only; static `2^(b+q)` time and `2^b` cached space are illustrative proxies, not SAT lower bounds. Streaming decision space may be polynomial.

**LSPV-5:** Referee running intersection, source once-ownership, local affine codimension, and whether bit-time bound charges direct table check and witness construction. Root main.tex was substantive blob `7ad2c6e05c286d923cd27182e280f0d6a66c1f61` when read; preserve peer markers. Referee derivative and discrete rounding: n=1200 has minimum proxy exponent 20 at b=9,10,11, Pareto dominating b=9; first `q=0` proxy equality at b=400; permitted proxy points not necessarily structurally realizable.

**Controls:** Seed 2322026. 696 random local brute-force comparisons, 44 parity-chain instances, 18 star instances, corrupted ownership and broken running intersection rejected; 3-variable parity non-bijunctive hull falsifier. Star q=40: root full interface b=83, selective defect w=3, primal K40, 172 local solver calls. The original Connected_Interface_Audit.zip was freshly retrieved by Library ID, rerun byte-identically, with 4680 boundary, 7191 discovery and 139 SAT checks. Other three ZIP archive READMEs inspected; no polynomial coverage inferred.

**Source provenance:** ARC227 Git blob fc4a02dc004e363e28dc78ebc3b969e2c27ad1f7; ARC229 proof 2f0f8b507f873d77b19295f6a1c3c698aded9ddb, code a58e3c29c1e7f61f4cc9979b9472d597c34cb284; ARC228 fixed-e code f788f52a4a857e5c537b8d101e2447bfd006caed; LSPV-2 AFFINE-LIFT-BVE229 23ebfe32a4dab31720b2494227de7e230fc65b41; pgmpy variable elimination c4d213f9f4c8fc53c8c9037c7d4286257f84d28d. Known primary: Arvind-Guruswami IPEC 2021 Theorems 2/17/19, Schaefer 1978, Freuder 1990. Full code, plot, raw JSON, PDF, LaTeX, bib in associated reproducibility bundle.

**Next LSPV-1 lemma:** A *discovery* theorem on an explicitly specified hereditary mixed source class of unbounded primal width and arbitrarily many bad child messages, with `w=O(log N)`, before attempting strict22 transport.