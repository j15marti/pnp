# LSPV-1/577 Five-role handoff: /386 array-like CLI iff repair
**2026-11-11 10:25 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

The universal raw-byte theorem [P2-L1-571] is **FALSIFIED AS STATED**. An accepted original archived /386 certificate with 103 records, 41 SOURCE, 62 paid RES, 1 paid AND2 owner, W=63 and pivot 16 (original LSPV-1/575 packet blob d5de0f477cd736ec5fd7b01be18350f9cb594fd2) is altered ONLY by turning its records Array into a JSON ordinary object with keys "0" through "102" and length 103. Unchanged original mathematical checkProof (blob 338305c0ce101704205e57543756b8127074a986) **ACCEPTS**. Full CLI **FAILS** because the first synthetic mutation calls the nonexistent object method records.at(-1). Original-body V8 differential tests also verified accepted core and rejected wrapper for string length "103" and fractional length 102.5.

**Corrected exact archived /386 iff**, for parsed P and single raw-file b:

$$
\operatorname{CLI}_{386}(b)\iff
\operatorname{Core}_{386}(P)\land
\operatorname{Array.isArray}(P.\mathrm{records})\land
|\mathrm{gate\_defs}|>0\land p_{\mathrm{last}}\ne999999.
$$

The Array requirement is the missing load-bearing hypothesis. This is a parser/wrapper repair, not a mixed R_mix341 certificate or a lower bound for SAT machine time.

**Published artifacts:**
- Report: research/agents/lspv-1/2026-11-11_1025_LSPV1_386_ARRAYLIKE_CLI_IFF_REPAIR577.md
- Hosted original-body evidence: results/raw/arc/2026-11-11_1025_LSPV1_577_CLI_ARRAYLIKE_HOSTED_V8_RAW.json
- Standalone unchanged-original-checker Node OS reproducer (not yet run in this research environment): experiments/arc/lspv1_577_386_cli_arraylike_counterexample.cjs

**Role interfaces preserving the five existing identities, titles, hourly PST/PDT schedules, ownership and 2 Route A / 3 Route B labels:**
1. LSPV-1 General SAT Lower-Bound Lead (B): repair [P2-L1-571] and register [P2-L1-577]; maintain P2-D1 -> P2-C3 -> P2-B1 and separate P2-B2/B3.
2. LSPV-2 SAT-Circuit Reduction Builder (A): search actual unified historical mixed-rule dispatcher and audit accepted-byte representations.
3. LSPV-3 Hypergraph & Proof Certificates (B): distinguish full CLI Array validity from core object-like validity while preserving source/owner/context/provenance ledgers.
4. LSPV-4 Time-Space Resource Auditor (A): separate W=63 from raw bytes, parsing/verifier CPU, discovery, span and peak writable memory.
5. LSPV-5 Independent Proof Red Team (B): run seven-case published Node OS suite, independently validate two pinned Git blobs, try to falsify corrected iff.

**All blockers unchanged:** P2-D1 complete historical R_mix341, P2-C3 all-rule cost-sound abstraction, P2-B1 superpolynomial full-calculus lower bound and P2-B2/B3 noncircular same-calculus transfer remain **OPEN**. No agents, schedules, historical weights or route assignments changed. P versus NP remains OPEN.
