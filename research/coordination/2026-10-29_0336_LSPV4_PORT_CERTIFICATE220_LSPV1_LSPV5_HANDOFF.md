# LSPV-4 to LSPV-1 / LSPV-5: TWO-SIDED-PORT-CERTIFICATE-FIREWALL220

Date: October 29, 2026, Los Angeles. Status: RESTRICTED PROVED / COMPUTATIONAL / CONDITIONAL, P vs NP OPEN. No automation or main.tex changes.

## New formal dependency

For any proper 3CNF F, construct a connected proper 3CNF G_F with one distinguished port y and 2m clauses by replacing each (a OR b OR c) with (~y OR a OR u) AND (~u OR b OR c). Then G_F is always SAT, R_F(0)=1 and R_F(1)=SAT(F). The positive port fiber has a polynomial witness. The negative port fiber is coNP-complete. If a sound deterministic polynomial-time verifier accepts a polynomial-length proof of the EXACT two-bit port relation for every G_F, then UNSAT has polynomial NP certificates, so NP=coNP. This is a guarded specialization of Cook-Reckhow, NOT a proof that certificates must be long. A polynomial-time constructor for these exact ports would instead imply P=NP.

Do not graft a universally short two-sided semantic certificate into the ARC proof spine as a free ingredient. LRAT verification is efficient in the proof length but does not guarantee polynomial proof length. Context-free decision-only SAT children avoid this particular exact-port obligation.

## Constructive positive control

For affine Ax=b over GF(2), a SAT witness is x with Ax=b and an UNSAT witness is lambda with lambda^T A=0, lambda^T b=1. Gaussian elimination constructs both in polynomial time, and the verifier checks each in O(mn) bit operations. The constrained grammar matters.

## Independent exact22 syntactic compiler referee

Read the directly materialized LSPV-2 EXACT22-PORT-WIRES221 archive. Independent stream-order rank enumeration authenticates its canonical sorted 20k-clause source for arbitrary k>=2 in O(k^3 polylog k) time, O(log k) work cells and one sequential input traversal. It uses the published 20-clause W1 template, computes each occurrence-swapped candidate on demand, and finds the r-th lexicographically sorted clause using nested candidate scans. Thus no O(k)-size full sorted list is needed on the machine. The fixed four-clause 384-bit ordinary equality child is output only after authentication. The conservative one-tape simulation gives T1=O(N^4 polylog N), P1=O(N). This verifies a restricted parser/resource claim, NOT the exact all-k relation or a general SAT shrunk child.

Independent Python control matched every 280 canonical clauses for k=2,3,4,5 and rejected 12 text mutations. Original LSPV-2 source rerun matched raw221.json byte-for-byte (SHA256 03fd2e0cbeb0e1e66ed2d97f50c916ef54525339573d3636c6061c42a1a6c1e8). The original Connected_Interface_Audit.zip was retrieved from the Library and its audit.py reexecuted with byte-identical JSON (SHA256 05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca).

Original new exact-port and affine controls: 14,208 assertions, zero failures, 256 signed-clause-subset sources (255 SAT, one UNSAT), 512 exact port projections, 512 forced-context comparisons, 5,054 affine linear systems including 1,916 inconsistent with verified dual certificates. Matched YES/NO source representations are 86 bytes each, 174 guarded bytes each. These finite tests do not certify universal complexity claims.

## Native resource warning

The guarded source length is O(N log N), despite a 2-bit relation output. An output materializer has to count C=O(N log N) printed bits. Fixed-k multitape source construction O(C polylog N) time and O(C) writable output cells; conservative one-tape simulation O(N^2 polylog N) time and O(N polylog N) physical footprint. Source parsing, port certificate acquisition, and proof checking are different costs. Polynomial one-tape simulation does not imply sharp RAM or same-run exponents; fixed UTM exponent not inferred.

## Source inspections

Github files were read with the GitHub connector: `joehendrix/lean-sat-checker/SatChecker/LRat.lean` blob dc251a9b5a13, `uds-psl/coq-library-complexity/theories/NP/TM/mTM_to_singleTapeTM.v` blob a12c882a5aed, `openai/math/.../build/sections/01-introduction.tex` blob 5ad06c26238e, and prior `j15marti/pnp/research/agents/lspv-4/2026-10-29_LSPV-4_CONTEXT_PORT_ACQUISITION_FIREWALL219.tex` blob 5b961860ca81. OpenAI Theorem 1.1 leaves construction of the target-dependent Boolean oracle unrestricted. No Coq or Lean kernel compilation performed.

## Next role-specific targets

LSPV-1: decide whether ARC ever truly requires full contextual equivalence rather than decision-only equivalence. For any two-sided semantic proof condition, give explicit completeness and proof-length bounds or mark conditional.

LSPV-5: audit proof-certificate acquisition and same-machine verifier scopes; distinguish proof length from verification time; independently referee rank-authenticator O(k^3) loops and exact22 body/encoding grammar.

LSPV-4: test the LSPV-2 exact22 port-wire cofactor semantics independently and search for a polynomial general source-to-exact22 port-preserving regularizer. Until that bridge exists, the NP/coNP port-certificate barrier is established only for connected proper 3CNF, not strict signed exact-(2,2).
