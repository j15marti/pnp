# LSPV-4 handoff 359: sparse variable-header cost firewall

**November 3, 2026, 04:36 PST.** Additive role-specific evidence for the fixed **worst-case minimum derivation** program. General CNF-SAT remains the target. Do not alter (R_{\mathrm{mix341}}), task identities, enabled states, schedules, other roles' ownership, or the shared mathematical handoff. P versus NP remains OPEN.

## Status and exact result

**PROVED/EXACT, elementary but model-relevant.** A syntactically valid CNF may declare (n=10^d) variables with just one occurring literal (x_n) and (O(d)) source bytes. A naive all-input compiler that emits `exists x1 ... xn : F` must write at least (10^d=2^{\Omega(N)}) quantifier tokens. It is **not** a polynomial-time construction, even though the source `(x_n)` is SAT and `(x_n) AND (not x_n)` is UNSAT with a one-node Resolution contradiction.

**PROVED/EXACT repair.** Parse the source and assign consecutive names only to *occurring* variable indices. At most (N) names and literal occurrences are needed. The existential TQBF query has (O(N\log(N+2))) bits and can be generated in polynomial total bit operations, including parsing, sorting, variable renaming, indexing and output. Unused declared variables are irrelevant to the SAT label. All-phase materialization may still have `rho >= 1`; this is not an FLMV space contraction.

**KNOWN theorem, independently verified:** The LSPV-1 QBF-ORACLE-B3-NONRELATIVIZATION360 result already combines TQBF with Haken's Resolution lower bound to refute the *oracle-relative* B1/B2/B3 for pure Resolution. Run 359 does not assert novelty for that barrier. It adds the concrete exponential-header failure and independent all-input query/code/resource audit.

## Finite, separately checked controls

PHP_(k+1)^k, k=1,2,3: (variables,clauses,source bytes,QBF query bytes) = (2,3,26,42), (6,9,76,146), (12,22,200,379). All UNSAT, and all 34 source-clause deletions plus 70 one-sign flips are SAT. Explicit authenticated, *nonoptimal* Resolution upper proofs use 2, 11 and 46 inference nodes. Three source headers naming 1,000,000,000 variables but mentioning at most one produce tiny queries of 8, 18, 26 bytes (SAT, SAT, UNSAT). Three ordinary SAT cases, ten malformed inputs and five corrupted proof records pass their expected labels. The independent no-import Node referee passed **770 checks**.

Host metrics: 0.106 seconds, 96,396 KiB peak Python RSS; 29,428 KiB independent Node RSS. These are **not** native indexed-TM space counts. Oracle evaluation is not paid in the relativized model, cannot be silently imported into an ordinary decider, and is not a logical rule in the fixed mixed calculus.

## Four falsifiers

1. Header-bound quantification has polynomial output on every valid source: **FALSIFIED**.
2. Renaming only occurring variables changes SAT: **REJECTED** by exact semantics and finite controls.
3. A forged oracle answer is an accepted source-independent refutation: **REJECTED** by independent proof replay and corruption controls.
4. Oracle-relative B2 failure automatically disproves ordinary B2/B3 for full Rmix341: **INVALID TRANSFER**. Original B2/B3 and the mixed superpolynomial worst-case bound remain **OPEN**.

## Artifacts and next arrow

- [Role-owned LaTeX report](../agents/lspv-4/2026-11-03_0436_LSPV-4_SPARSE_HEADER_ORACLE_AUDIT359.tex)
- [Standalone compact reproducer](../../experiments/arc/lspv4_359_sparse_header_oracle.py)
- [Raw summary ledger](../../results/raw/arc/2026-11-03_0436_LSPV4_SPARSE_HEADER_ORACLE_AUDIT359_summary.json)

The complete local reproducibility package includes the full Python source, raw source/proof DAGs and SAT witnesses, and separately written JavaScript referee. Relevant older result: LSPV-1 [QBF-ORACLE-B3-NONRELATIVIZATION360](../agents/lspv-1/2026-11-03_0256_LSPV-1_QBF_ORACLE_B3_NONRELATIVIZATION360.tex).

**Next:** Audit the newest LSPV-1 reflection-to-mixed-calculus restriction checker with the same fully charged all-input discipline and no unproved machine-correctness leap. No task change. B1/B2/B3 and P versus NP remain OPEN.
