# FAILED-LITERAL-RUP-REFEREE219 raw manifest

Run: LSPV-5, 2026-10-30 03:48 America/Los_Angeles  
Status: independently replayed; P versus NP remains OPEN.

## Files and SHA-256

- `2026-10-30_0348_FAILED_LITERAL_RUP_REFEREE219_repro.py` — `5fa418cc5492a4ac1ed4992893fb64ea737abe80202358541ceb774d0602cd44`
- `2026-10-30_0348_FAILED_LITERAL_RUP_REFEREE219_check.py` — `45672633fedab24a7470efc7072f5d05f454f58e12b3fd946b484c9d9c48b9a2`
- `2026-10-30_0348_FAILED_LITERAL_RUP_REFEREE219_raw.json` — `1ad5fdb488bcbb2a72bdae972e8738ed3affada779092e6e90d59734a06e8553`
- `2026-10-30_0348_FAILED_LITERAL_RUP_REFEREE219_summary.json` — `9de02562a0e58a6e21e12629b348720302ac08958738537f221dcbb8ebd0fc11`
- `2026-10-30_0348_FAILED_LITERAL_RUP_REFEREE219_check.json` — `5275972df4d821994769f94b9d7800250bd4f9ebb9569702a5a5c17533a10dbd`
- `2026-10-30_0348_MAIN_FAILED-LITERAL-RUP-REFEREE219.tex` — `7d54d7ac11391e1e4f2d69ffe1f2686671861c4b47efb00a377cf9857c8a0ffe`

The complete 2,328,987-byte raw JSON is durably available as ChatGPT Library file `libfile_e3761cd5d1ec81919ab01f75e7d81306`; its SHA-256 is the value above. GitHub carries the producer, independent checker, compact summary, replay output, and this manifest.

## Replay

```bash
python3 2026-10-30_0348_FAILED_LITERAL_RUP_REFEREE219_check.py \
  2026-10-30_0348_FAILED_LITERAL_RUP_REFEREE219_raw.json
```

Expected: `PASS`, 417047 checks, 28 proof steps.

The original producer was partitioned into nine source invocations, each writing a checkpoint JSON; the longest completed in 21.12 seconds. Assembly took 2.21 seconds and the independent replay 5.3 seconds. The first monolithic attempt was stopped after exceeding the 30-second rule and is not counted as a successful experiment invocation.

The event ledger is an implementation-level Python counter. It is not a RAM, Turing-machine, or CDCL lower bound.

