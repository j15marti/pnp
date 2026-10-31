# LSPV-3 CUT-ACQUISITION266 full raw record

The exact bytewise raw JSON source is published in twelve consecutive GitHub files in this directory named
`2026-10-30_2224_LSPV3_CUT_ACQUISITION266_raw.part01-of-12.txt` through `...part12-of-12.txt`.
Their bytewise concatenation was fetched back from GitHub and compared to the original 219243-byte experiment output: **exact match**. Reconstruct in any POSIX shell:

```sh
cat results/raw/arc/2026-10-30_2224_LSPV3_CUT_ACQUISITION266_raw.part??-of-12.txt > 2026-10-30_2224_LSPV3_CUT_ACQUISITION266_raw.json
sha256sum 2026-10-30_2224_LSPV3_CUT_ACQUISITION266_raw.json
python experiments/arc/2026-10-30_2224_LSPV3_CUT_ACQUISITION266_independent.py 2026-10-30_2224_LSPV3_CUT_ACQUISITION266_raw.json
```

Expected SHA-256: `7eba9f3f736a07d4e777ae0a3f1cf5c65d99a4009e0e4ef1ac4f465de7d58ac0`. All 12 GitHub parts, the formal report, producer, checker, summary, and handoff have exact-content GitHub readback. The original full raw JSON and the complete reproducibility ZIP are also in Research Library `/P-vs-NP/`. The selected event counts are Python logical-event proxies, not native FLMV indexed Turing-machine instruction/space certificates. The restricted theorem does not supply an all-input hereditary SAT shrinker. P versus NP remains OPEN.
