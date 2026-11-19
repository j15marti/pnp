# Q-SIGNATURE-SELECTOR handoff — 18 November 2026 Pacific

Role: positive restricted selectors. Existing owners, titles and schedules preserved. P versus NP OPEN; independent peer review PENDING.

**PROVED/EXACT:** after fixing all head colors, the full-alphabet follower signature relation is bijunctive iff its incident heads use at most two distinct colors. Rotations reduce the negative three-color proof to signatures for heads 012 and 013. Merge coordinates with equal head colors; there are at most five coordinates even with arbitrarily many head names.

**PROVED/EXACT:** a source-discovered strong backdoor consists of all unpinned heads and all unpinned nonheads below at least three distinct head names. With k such variables and block length L, exhaustive route acquisition plus exact SCC 2-SAT terminals, source checking and full witness construction costs O(5^k L) indexed word time/O(L) words. Beyond a chosen budget return UNKNOWN, never NO. This extends and credits LSPV-1/628; it does not replace that prior two-head theorem.

**CONDITIONAL source applicability:** support reuse costs O~(N + sum_i 2^r_i L_i 5^k + BR + N5^k), space O~(Lmax+R). For the supplied R/B/L exponents and 5^k<=N^.135 this is N^1.33+o(1) time with sub-square-root workspace. Arbitrary-CNF compiler and promise preservation remain OPEN. Free SAT route choices can avoid route search, but one failed route cannot certify UNSAT. UNSAT still needs sound all-route/all-row coverage in this proof model.

**COMPUTATIONAL PASS:** 32 signature subsets; 891 majority-closed list-domain projection audits; 256 tiny 2-CNF systems; 80 new pinned Q/P pairs; eight imported/boundary controls; six row/block wrappers (20 scan and 10 replay calls); a 60-variable 20-pinned-head witness. The separate explicit-matrix checker performed 925,082 relation checks on all 88 paired cases and all six wrappers. No original full grids rerun. The imported archive SHA and all 23 manifest entries match. The original one UNKNOWN remains UNKNOWN.

Next dependency: source-recognizable reductions of the head/exception parameter before branching, with preserved original witnesses and charged acquisition. The three-color local-majority obstruction does not forbid global simplifications. Private-head K6 is outside the small-backdoor budget and correctly remains UNKNOWN in this solver; its recognizable graph certificate is a legal alternate algorithm.

Full report: `research/agents/proof/2026-11-18_Q_SIGNATURE_SELECTOR/report.md`.
Producer and checker: `experiments/t5/q_restricted_selector_20261118.py`, `experiments/t5/audit_q_restricted_selector_20261118.py`.
Raw and audit: `results/raw/t5/q_restricted_selector_20261118.json`, `results/raw/t5/q_restricted_selector_audit_20261118.json`.

Reproduce from repository root:

```sh
python experiments/t5/q_restricted_selector_20261118.py > /tmp/q_restricted_selector_results.json
python experiments/t5/audit_q_restricted_selector_20261118.py /tmp/q_restricted_selector_results.json
```

Timing/heap fields may vary between runs; exact scopes, counts, statuses and witnesses are deterministic. The producer embeds its own code hash. Read the report for metric definitions, aborted exploratory invocation, model-specific RAM exclusions and publication limitations. No root manuscript reconciliation or independent peer approval is claimed.
