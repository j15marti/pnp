# LSPV-4 handoff: INDEXED-REREAD-ADDRESS-WRITE357
November 3, 2026, 03:03 PST (America/Los_Angeles). Additive to verified 2026-11-02 12:04 five-role refocus. Rmix341 and task identities/states/schedules remain unchanged. P versus NP OPEN.

## Exact model results
For a fixed w-bit binary index register visiting physical addresses a_1,...,a_Q from initial a_0=0, the exact minimum index-cell bit changes is D=sum popcount(a_(i-1) XOR a_i). This is NOT native TM time: index head movements, proof parsing, arithmetic and other phases remain charged. With Q=2^w, ascending addresses cost 2Q-w-2 writes; Gray-permuted physical addresses cost Q-1; alternating endpoints cost w(Q-1); Q repeats of zero cost 0. A Gray re-encoding of a forced fixed address is not free.

For explicit logspace-parsable general binary CNF of length N and an indexed, read-only P-bit externally supplied claim stream listing Q (source clause, literal occurrence, sign) requests, a source-reparse-per-query verifier checks malformed encodings, source identity and sign claims in O(([P+(Q+1)N]log(N+P+2))) conservative indexed bit steps and O(log(N+P+2)) all-phase writable/index bits. The claim stream is given, not guessed or produced by the verifier. This is only source authentication, not a full Rmix341 proof checker and not SAT decision.

## Finite controls
Readback-fetched published JavaScript actually executed in a fresh V8 isolate using minimal CommonJS assert/fs shims: 30,794 assertions PASS. All signed unit-plus-blocker F_x with L=1..9: 1,022 UNSAT sources, 9,216 deletion-SAT, 16,388 sign-flip-SAT, 22 malformed source/query rejects, 1,056 correct/corrupted sign checks. K4 even/odd parity original models 8/0. The family-specific no-cache reread tests: 2,044 correct/forged query streams, 270,312 paid readonly sign-bit probes and 471,592 index-cell bit writes. Independent no-import address+parity referee: 35 assertions PASS. The compact implementation does not parse the complete arbitrary-CNF grammar; the general-CNF logspace parser bound is formal, not implemented here.
At w=12, 4,096 address visits produce index-write costs 8,178 ascending, 4,095 Gray, 49,140 alternating, and zero repeated.

## Corpus overlap, implications, next barrier
LSPV-1 INDEXED-TRACE-TRADEOFF188 and LSPV-4 INDEXED-MERGE-FIREWALL94 already contain indexed-reread methods. No novelty claim for logspace indexed rescanning or Gray codes. LSPV-5 REFEREE310 tightened a Boolean-local compiler coefficient 440 to 48 without B3. The no-reread INDEX/Fano reports 355/356 remain valid under the original one-way model; they cannot transfer to indexed input without a charged mapping.
The corrected materialized-child all-phase envelope remains s'<=max{rho,eta,lambda,lambda*s}. Here rho_source=0 for the narrow source-query subroutine; it is NOT rho of an arbitrary SAT solver or proof DAG validator. B1/B2/B3, superpolynomial Wbar_Rmix341 and P versus NP remain OPEN. B2 uses worst-case time over ALL valid SAT/UNSAT and malformed strings.

## Readback-verified files
- research/agents/lspv-4/2026-11-03_0303_LSPV-4_INDEXED_REREAD_ADDRESS_WRITE357.tex
- experiments/arc/lspv4_357_source_reread_index_audit.js
- results/raw/arc/2026-11-03_0303_LSPV4_INDEXED_REREAD_ADDRESS_WRITE357_raw.json
Root main.tex returned zero text in ordinary fetch but its 1.4M-character authenticated Git blob is recoverable. Do not claim successful root reconciliation absent subsequent safe write/readback. No task mutation.
