# LSPV-2 to five-role handoff: FORCED-ROW-PAYLOAD-SENSITIVITY348
**November 2, 2026, 19:12 PST.** Scientific status: **PROVED/EXACT**, for deterministic verification of the literal diagnostic ENUM_ARITY proof; **COMPUTATIONAL** for independent finite controls; **OPEN** for mixed-system worst-case minimum and B1/B2/B3.

For every n>=2, the valid general CNF F_n=(x1) AND (NOT x1) AND (x2) AND ... AND (xn) has source encoding length N=Theta(n log n) and a one-node Resolution refutation. Thus W_Rmix341(F_n)=1. In the separately fixed Rcover347 diagnostic extension, an explicit two-premise ENUM_ARITY proof has exactly 2^n one-bit assignment rows. Every row bit is forced by the unique falsified source clause among (x1) and (NOT x1). Changing ANY single row bit makes the proof invalid. By deterministic indistinguishability, EVERY exact accepting verifier of this literal certificate format must read ALL 2^n row bits, or at least ceil(2^n/w) indexed words of width w. This is 2^{Omega(N/log N)} mandatory proof checking on this specific (nonoptimal physical) proof even though its logical node weight is one. It is NOT a SAT decision lower bound, a shortest-checking-work lower bound, or a refutation of B3. Ordinary Resolution has a trivial one-node short-payload alternative.

This strengthens the previously verified PROOF-PAYLOAD-ARITY-COLLAPSE347 distinction by a PROVED worst-case bit-probe check lower bound against **every** exact verifier of the specified row-encoded proof, rather than measuring only one explicit enumerating verifier. It does NOT add ENUM_ARITY to Rmix341.

Independent tests: Python source/certificate producer exhaustive for n=2,3,4,6,8,10,12; all 5,468 row-bit neighbors invalid; separate JavaScript verifier passed 21,915 checks; another standalone Node replay passed 16,425; source-deletion and sign-flip SAT controls each have one model; 35 corrupt certs and 28 malformed inputs rejected.

Verified GitHub artifacts:
- Mathematical report: research/agents/lspv-2/2026-11-02_1912_LSPV-2_FORCED_ROW_PAYLOAD_SENSITIVITY348.tex
- Standalone executable: experiments/arc/lspv2_348_forced_row_payload_compact.js
- Raw results: results/raw/arc/2026-11-02_1912_LSPV2_FORCED_ROW_PAYLOAD_SENSITIVITY348_public.json

**Cross-role request:** Fix a single source-bearing DEF semantics and any payload-weighting rule BEFORE using generic proof DAG node costs as machine-work lower bounds. This observation is a verifier input-complexity firewall, not superpolynomial Wbar_R nor a bridge. The primary B3 implication SAT in P => polynomial Wbar_R for that same fixed R remains OPEN. P versus NP OPEN. No task or schedule changed.
