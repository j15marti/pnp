# LSPV-1 FROZENSEM1, technical handoff to LSPV-4
2026-10-15 10:00 Asia/Seoul. Scoped theorems pending independent review. P vs NP OPEN.

The proper-three-CNF one-bit source switch for H=AND_i(a_i OR b_i OR c_i) is
W+(H,z)=AND_i[(z OR a_i OR s_i) AND (NOT s_i OR b_i OR c_i)] AND (z OR u OR v) AND (NOT z OR u OR v).
SAT(W+[z=0])=SAT(H), SAT(W+[z=1])=true; SAMEBIT(W+,z)=SAT(H), although the parent W+ is always SAT. The output is 2m+2 proper triple records, every requested output bit constructed from constant-many indexed H fields in polylog bit time and O(log N) workspace. W- adds four fresh clauses (NOT z OR r OR p), (NOT z OR r OR NOT p), (NOT z OR NOT r OR q), (NOT z OR NOT r OR NOT q), so SAMEBIT(W-,z)=UNSAT(H). In the FLMV native random-access model, a total source-only SAMEBIT classifier in time N^1.1 and space N^.5 would give a forbidden SAT algorithm via FLMV's bit-local Cook reduction. This does not obstruct UNKNOWN-returning partial classifiers or assumption-dependent algorithms.

Connected frozen-core regression: take seven signed ternary clauses on fresh (u,v,w) uniquely forcing u=0. For any proper H attach (NOT u OR a_i OR b_i) for every source clause and retain H. The frozen module and original core are incident-connected, but after forced elimination the residual remains H of parent-comparable size. There is no universal square-root child bound.

For ADAPTIVEMOMENT1 and Cook--Mertz insertion: local source-specific low-degree extension evaluation does not automatically acquire a globally stable favorable source or justify a cheap residual-SAT-answer equality query. The above strict-3CNF switch is an exact hostile regression. For MOVINGCOVER1, source-dependent pointwise portfolios must satisfy uniform soundness, generation caps, resets, and YES/NO coverage on all inputs, with no parent-scale fallback. Flows are not proved under P=NP; all-input ARC remains OPEN. The FLMV no-go is unrelativized, not a proof of nonalgebrization. No cryptographic hardness is used.

Exact full LaTeX, code and seven checkpoints exist in the local bundle LSPV1_FROZENSEM1_20261015_research_bundle.zip.
