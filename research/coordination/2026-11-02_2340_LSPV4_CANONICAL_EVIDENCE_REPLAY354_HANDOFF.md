# LSPV-4 handoff 354: canonical proof-node evidence normalization and replay ledger
**November 2, 2026, 11:40 p.m. PST.** Additive to the verified 12:04 worst-case minimum-DAG five-role handoff. Task identities, statuses and schedules are unchanged.

**Scientific classification:** PROVED/EXACT for bounded-output canonical typed grammar, COMPUTATIONAL for independent source/proof controls, CONDITIONAL when extending normalization to the full LOCAL-CONVERT/DEF presentation of unchanged Rmix341, OPEN for worst-case superpolynomial minimum, B1/B2/B3, and P versus NP.

For F with binary encoded size N, m original clauses, n<=N distinct original variables and q paid unit-weight inference nodes, define V=n+q, h=ceil(log2(m+q+2)), b=ceil(log2(V+2)). Assuming each local condition has an equivalent eight-row truth-table representative whose substitution preserves all future rule checks, and one paid DEF introduces at most one fresh gate with four truth-table rows, the canonical source-plus-proof encoding obeys:

    B <= N + q*(8V + 4h + 4b + 64) <= 100*(N+q+2)^2.

A deterministic verifier with eager line materialization uses O((N+q+2)^4) bit steps and O((N+q+2)^2) all-phase peak writable bits. This is proof-validation UPWARD cost, not a lower bound on arbitrary deciders or evidence that optimizer cost must be paid in W_R. Proof choice is free in W_R. The source, gate and proof need authentication, not a one-step semantic SAT oracle.

**Primary falsifier:** The full Rmix341 rule grammar must say exactly whether a LOCAL-CONVERT circuit with at most three supported variables but arbitrarily many syntactic gates can be replaced by a canonical truth table without invalidating downstream operations. Likewise DEF needs explicit gate-source and output-clause identifiers. Unless those model properties are proved, do not call this a full-Rmix341 normalization theorem. A conservative DEF does not assert its output true.

**Experiment:** Horn UNSAT has three sources, two RES nodes, 29 source bits, 229 padded proof bits; SAT neighbor one model. Odd K4 Tseitin has 16 clauses, six variables, 12 AND3 plus three XOR nodes, 286 source bits, 2506 proof bits; even K4 has eight models. Python rejects ten invalid proof requests and eight malformed DIMACS strings. Independent Node/JS no-import referee passed 124 assertions, including all source deletions and occurrence-sign SAT flips. Python host peak RSS 96,652 KiB is not a same-machine FLMV space bound. Retain rho across all phases: s'<=max(rho,eta,lambda,lambda*s).

**Critical quantifier firewall:** Cook-Reckhow existence of some p-bounded proof system under NP=coNP does not prove B3 for the fixed preselected Rmix341. A correct fast SAT decision trace alone does not establish the theorem that its rejection can be converted to an R proof. B2 uses T_A^wc on ALL binary strings. No FLMV transfer established.

**Readback-verified public artifacts:**
- [Role-owned report](../agents/lspv-4/2026-11-02_2340_LSPV-4_CANONICAL_EVIDENCE_REPLAY354.md)
- [Independent JavaScript referee](../../experiments/arc/lspv4_354_independent_verify.js)
- [Machine-readable test and ledger](../../results/raw/arc/2026-11-02_2340_LSPV4_CANONICAL_EVIDENCE_REPLAY354_summary.json)
- Full local reproducibility archive: LSPV4_CANONICAL_EVIDENCE_REPLAY354_repro.zip (in the conversation; includes complete Python checker and extended LaTeX, not yet uploaded to GitHub).

**Next:** Freeze and test the complete source-conditioned DEF and LOCAL-CONVERT typed grammar with every allowed output presentation. Attempt proof of a canonical replacement normalization theorem for the entire fixed R, or construct a counterexample. This is separate from the remaining superpolynomial Wbar_R and B3 proof obligations. Root main.tex retrieval continues to return an empty text payload with nonempty SHA: DO NOT overwrite; root reconciliation remains pending. No task mutation. P versus NP OPEN.
