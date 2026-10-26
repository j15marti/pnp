# LSPV-3 SOURCE-LOCAL-RAM-TAPE-CERT136 | Lead and red-team handoff
Date: 2026-10-26 16:17 PDT. Status: **PROVED/EXACT RESTRICTED**, independent mathematical review pending. **P versus NP, ARC-EDGE-90 and affordable all-UNSAT coverage remain OPEN.**

## New theorem, exact scope
For each unequal-pair canonical signed exact-(2P,2N)-3CNF equality source E_m(a,b), there is a 40-original-clause UNSAT subset (19 original Q clauses and one signed forcing clause from each corresponding LEFT/RIGHT side at any mismatch). The checked constant-template Resolution refutation has 343 records, specifically 78 source introductions and 265 authenticated resolution steps, maximum clause width seven. Since all source IDs, clause names and line pointers cost O(log N), the source-authenticated proof length is O(log N). On a **unique mismatch**, both force-sign clauses are essential: deleting either makes the entire signed exact22 source SAT, hence any UNSAT original-source clause subset must include both. This is NOT an arbitrary derived-child / general semantic DAG lower bound.

The exact user-designated source E_m has 168m variables, 224m signed proper distinct ternary clauses, and fixed indexed bit length N=3w+3+672m(w+1), w=ceil(log_2(168m+1)); SAT iff a=b, LEFT-GAP-RIGHT source geometry. Direct RAT probes of matching signs permit deterministic promise decision and proof generation in N^{1+o(1)} time with O(log N) writable/index bits. This refutes any claim that tape physical transport is necessary for indexed RAM verification.

## Distinct verification, guessing, acquisition and models
A verified signed source-clause Resolution proof is sound on all properly parsed ordinary SAT inputs, but these small certificates are guaranteed only for the equality promise family. On a syntactically validated canonical source, indexed proof authentication is polylogarithmic, while an all-input well-formedness pass costs N^{1+o(1)} bit time. Fixed-k one-input-head sequential tape verifier can scan N input bits, retain forty O(log N)-bit source clauses and check the constant proof in N^{1+o(1)} time and O(log N) work cells. M1 single shared read/write tape initially holds N+P bits, total footprint N+O(log N), and must physically traverse the Theta(N)-separated two-shore sign clauses; this verification does NOT inherit the deterministic equality decision near-quadratic bound.

A **total deterministic** finder emitting a refutation exactly when a!=b decides equality; the pre-existing EXACT22-TAPE-TRANSPORT1 crossing sequence result transfers to M1 (Omega(N^2/log N)) and Mk sequential-head (T(S+log(T+N)+1)=Omega(N^2/log N)). It does not transfer as a native bound to RAT; one-head tape and multiple-head/RAT quantities are not interchangeable. For coNTIME only, guessing is permitted under a length-only cap with rejected verifier outcomes mapped to accepting branches, and all invalid/timeouts clocked. P=NP supplies only unknown polynomial K, never d=1.802.

## Reproducible tests
Report: `research/agents/lspv-3/2026-10-26_1617_LSPV-3_SOURCE_LOCAL_RAM_TAPE_CERT136.tex`.
Code: `research/agents/lspv-3/2026-10-26_1617_SOURCE_LOCAL_RAM_TAPE_CERT136_repro.py`.
Raw: `research/agents/lspv-3/2026-10-26_1617_SOURCE_LOCAL_RAM_TAPE_CERT136_raw.json`.
The stdlib code constructs and fully checks 34 equal/unequal canonical encoded cases at m=1,2,4,8,16: 10 SAT witness controls, 24 UNSAT 343-record authenticated Resolution controls; Q has exactly 244 truth assignments, all three source ports false. Two signed original-name proper3CNF descendants serialized and reparsed; modified signed source clauses and false pivots rejected. Two reruns agree in SHA256 `9965d14ea4d15cf94d1e79a4c2dd13b4213af6f4d78a0ad4e6a4ebf0defc0e64`. Measured Python RAM usage is not a TM space measurement.

## Required peer checks
LSPV-1: review certificate existential vs total deterministic finder quantifiers, dual ledger directions, and whether near-linear standard parsing is adequate for the declared model.
LSPV-5: independently validate fixed-width same-length encoding, 40 genuine source clauses, two-shore clause essentiality on a unique mismatch, and no improper transfer from proof length/tape crossing to all-input indexed SAT hardness.
LSPV-2/4: contrast fixed indexed clause offsets with signed source circuit/pinned output growth and scan-before-solve wrappers. No third-party messages and no task/schedule changes were made.
