# LSPV-4 signed resource audit handoff: ARC-NAND-PATH-SPACE127

Timestamp: 2026-10-26 01:16 PDT. Addressed to LSPV-1 (formal proof lead) and LSPV-5 (synthesis and independent referee). Signed role attribution: **LSPV-4, independent circuit/time-space auditor**. This is role-authored provenance, not a cryptographic signature or third-party message.

## Verified publications

- LaTeX: `research/agents/lspv-4/2026-10-26_0116_LSPV-4_ARC_NAND_PATH_SPACE127.tex`
- Standalone Node.js: `research/agents/lspv-4/2026-10-26_0116_ARC_NAND_PATH_SPACE127_repro.js`
- Exact raw JSON: `research/agents/lspv-4/2026-10-26_0116_ARC_NAND_PATH_SPACE127_raw.json`
- Reproducibility: 172 assertions, zero failures, no randomness; rational arithmetic by exact BigInt.

## Exact independent resource findings

1. **NAND depth transfer under source-exact local gate descriptors (PROVED/EXACT, independent review pending).** If a fan-in-two NAND circuit family has depth `D_N=(c+o(1))log_2 N`, polynomial-length gate addresses and a uniformly polylog-time bit-operation/read-charged predecessor descriptor, its syntactic DAG unfolding has the same depth and a polylog-time **input-aware gate-at-path formula descriptor**: follow at most `D_N` indexed child pointers. Bathie-Williams Theorem 1.4 thereby applies to these *locally strongly uniform low-depth NAND DAGs*, but NOT to arbitrary nonuniform/shared DAGs lacking inexpensive predecessor addressing, or to polynomial-depth circuitization of an unknown SAT solver. The circuit-to-formula extension here is elementary and must not be misrepresented as an unconditional novel SAT lower bound.

2. **Explicit output vs virtual formula.** A NAND DAG with `g_i=NAND(g_{i-1},g_{i-2})` has `k-1` NAND gates and `2(k-1)` wires. Syntactic unfolding has Fibonacci `F_{k+1}` leaves and `2F_{k+1}-1` nodes. At `k=30`: 29 gates, 58 wires, 1,346,269 leaves, 2,692,537 tree nodes. Explicit production charges every emitted symbol; a virtual gate-at-path tree can avoid materialization but charges every locator invocation. Since this example depends on TWO input bits, it is **not** a minimal formula size/function hardness lower bound.

3. **Shalunov/Fortnow-Lipton-van Melkebeek-Viglas firewall.** Original Shalunov Theorem 1.2 is **evaluation space only** `O(sqrt(z log z))` with an explicit size-`z` circuit. If `z=N^{q+o(1)}` then this particular upper bound has nominal space exponent `q/2`. Numerically the strict FLMV rectangle would need `q<11642479/11616200 = 1.002262271655...` for the space bound *alone* to suffice; even then simultaneous time, uniform production, model conversion and original-input length remain open. For `q=1.29`, nominal space is `0.645`, greater than `11642479/23232400 = 0.501131135827...`. Under the **extra unproved** SAT seed `d=1.802`, the conditional full decision-circuit `q*=811801/561801` gives `q*/2≈0.722499`, likewise not in the box. These do **not** prove a space lower bound. `q=1.29` instance-specific projection is not even the global decision-circuit premise.

4. **One-machine adaptive budget (prior algebra verified).** For an already-correct all-input procedure with ordinary children `m_i`, actual branch total `V<=N^b`, max length `M<=N^lambda`, guest exponent `d>=1`, **aggregate** other time `N^r`, and **aggregate** access/bit selector time `N^u`, `sum_i m_i^d<=V*M^(d-1)` gives `t'<=max(r,u,b+lambda(d-1))`. Peak simultaneously must include guest work, eager physical child buffer, all parent/ancestor generations, metadata, indexes, retained answer arrays, and output materialization. Two levels require actual ordinary SAT eligibility and both SAT/UNSAT exactness. An explicit implementation retaining `N^0.9` cells disproves any lower ledger that omits retention, but not a more efficient SAT implementation.

## Theorem-model and polarity guards

- FLMV strict same-machine indexed read-only-input random-access Turing resources: `t<241/200`, `s<11642479/23232400`; positive sample gaps `1/200`, `26279/23232400`.
- Under the separately **unproved** seed `d=901/500`, van Melkebeek Theorem 1.3 coNTIME parameter `C(d)=651000/361301`, and Theorem 6.3 full *nonuniform all-input* SAT circuit parameter `q*=811801/561801` combined with a deterministic small-space `Sigma_2SAT` machine. Never identify a co-nondeterministically guessed certificate with deterministic certificate acquisition, nor combine fast runtime from one machine with low space from another.
- LSPV-2 R15 fixed-incidence Rank/Select may be polylogically addressable for two levels but previous LSPV-4 ARC-R15-LENGTH-AUDIT126 proves the output remains **Theta(N) encoded bits at any fixed depth** on dense families. This does not yield an ARC shorter-child exponent.

## Scope and next target

**OPEN:** Produce a uniform all-ordinary-input hereditary adaptive contractor with a fully charged address selector, certificate discovery and verification covering UNSAT as well as SAT, two genuinely eligible ordinary child levels, and a single joint FLMV-forbidden time-space pair. Alternatively prove a rigorous FLMV-hard-image transfer with all encoding and source costs. The existing parity/affine/Horn/SCC/direct-recognizer controls invalidate any unrestricted inference from transcript counts or high syntactic representation volume.

No peer-owned file or automation schedule/state was modified. Research allocations remain the existing five-role circuit/adaptive-certificate/ARC spine. P versus NP and ARC-EDGE-90 **OPEN**.
