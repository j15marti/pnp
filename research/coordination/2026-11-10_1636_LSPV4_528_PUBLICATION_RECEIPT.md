# LSPV-4/528 GitHub publication and exact-readback receipt

**2026-11-10 16:36 PST | Native-calculus closure | [P2-L4-528] | P versus NP OPEN.**

## New artifacts, complete-content readback PASS

| Path | Git blob |
|---|---|
| research/agents/lspv-4/2026-11-10_1636_LSPV4_NATIVE_XOR_QUOTIENT_CYCLE_AUDIT528.md | b18258b42bf86948ffbdaead7eb46dbd15e4bba6 |
| experiments/arc/lspv4_528_native_xor_quotient_cycle.cjs | 65ca8eb837fab544001e69cef9792e8f3706a794 |
| results/raw/arc/2026-11-10_1636_LSPV4_528_NATIVE_XOR_QUOTIENT_RAW.json | d1ad0ee14aaeca9f11a1ee33b9147ea77e880878 |
| research/coordination/2026-11-10_1636_LSPV4_XOR_QUOTIENT_CYCLE_FIVE_ROLE_HANDOFF528.md | 0be73ba308a6fb68882a85d8775588444042a3fa |

GitHub native contents-API create-file commits, in order: code d4574d1bf47adbb023d6424b23866cd7217927bc, raw dc197dfdc9a8045a5ef422732e7399e48072b812, report 23223e24252e6a2f0223313abd8fb3cd1b83337a, handoff 58b118d0c299eaa93170846a6197ba3ac4b71be1. All four files were fetched again and matched their entire expected UTF-8 strings.

## Root trackers

- proof1.txt: read in full, unchanged, Git blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b.
- proof2.txt: current full content pre-write Git blob eecf92479f7938cd636656eb73acf883070da95c, 945,861 characters; added material [P2-L4-528] after IDEA->SEARCH->ITERATE via SHA-guarded contents update commit 74a3501f951eac4b9988e1f4015ee3c9b15c94cf. Final Git blob 282c42f891b8528e2181a1f50de795e1d5b10e12 and 948,636 characters. Final complete-content readback exact; every preceding character preserved.

## Root main.tex ownership-safe reconciliation

Full ordinary contents-API fetch_file returned zero content bytes despite SHA. Unlike earlier runs, fetching the exact Git blob via fetch_blob succeeded with 1,914,208 characters. The original file had exactly one BEGIN/END LSPV-4 OWNED marker pair. Inserted dated, narrowly scoped LSPV-4/528 LaTeX paragraph before the end marker. Optimistic SHA-guarded update succeeded at commit a64fd4e0ab38ba8d48d41422fb09ebfd0cc757be, old blob 2e5350e20acbff63a4ca1a1d6161c92932f53426, new blob 0fe79071499c352808d792f385c4b66299385f37. Full new blob fetch yielded 1,916,350 characters and matched the exact intended string. Both prefix before insertion and suffix after insertion matched original content exactly. Material outside LSPV-4 ownership markers preserved. Native LaTeX compilation/preflight was not run.

## Computational scope and limitations

Unchanged original /341 producer and recovered fixture checker plus separate /539 strict source-bound reference were reexecuted in hosted V8 with Node adapters and stubbed cryptographic hash. Independent Python 3.13 reconstructed and verified original source, 73 assertions, all 64 assignments and five hostile controls. No full historical R_mix341 checker available. Standalone Node OS CLI file published but not executed as an OS process. No native machine time/peak writable-space measurements.

Quotient-cycle mechanism specializes existing LSPV-5/464; new K4 SOURCE/AND3/XOR witness and k-family resource statistics independently checked. Neither shortest-proof hardness nor P-versus-NP resolution follows.

No identities, roles, schedules, timezone, enabled states, historical rule grammar/weights, or two Route A / three Route B labels changed. Full native grammar [P2-D1], all-rule cost-sound abstract simulation [P2-C3], unrestricted mixed lower bound [P2-B1], and separate B3 [P2-B2] remain OPEN.
