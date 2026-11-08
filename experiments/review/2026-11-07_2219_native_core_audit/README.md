# Reproduce the LSPV-5 native-core continuation

Requirements: Python3.10 or later and Node.js supporting BigInt and Array.at. No third-party Python or Node dependencies are needed.

From this directory run:

```bash
node historical/lspv2_341_mixed_tseitin_min_dag.js > baseline.json
node historical/lspv2_341_independent_verify.js baseline.json > baseline_verified.json
python3 balance_and_audit.py
python3 onehot_transfer_audit.py
```

Expected deterministic outcomes:
- Historical packet Git blob: fe27fe1011d0021e721ccaeb747ed58da65d7464.
- Historical verification record Git blob:42ba4cad6dc165aa9e96a29011df5602d33281b9;30,714 checks.
- Balance audit:56,528 Python assertions;10 mutations rejected in both historical JS and independent Python.
- Balanced packet SHA-256:7904069986fa806338de0dfa05006c29cf61cfd6e53050e31a80fa0e789ed2db.
- One-hot target audit:23,794 assertions;21 cases;4 corrupted records rejected.
- `results.json` includes a measured wall-clock field that will vary on replay. Logical results and packet hashes should not vary.

The original JavaScript files are unmodified. Their Git hashes are recorded in REPORT.md. The new Python audit is independent of the historical JavaScript checker. The one-hot audit uses a separate explicitly specified target proof syntax, not the historical mixed parser. Finite tests do not prove the cited asymptotic literature lower bounds. See REPORT.md for proof assumptions and limitations.
