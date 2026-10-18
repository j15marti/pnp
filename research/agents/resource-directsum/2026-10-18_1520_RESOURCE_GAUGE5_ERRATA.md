# RESOURCE-GAUGE5 publication verification and code provenance

Date: 2026-10-18, 15:20 Asia/Seoul.

The principal mathematical report at research/agents/resource-directsum/2026-10-18_1520_RESOURCE_GAUGE5.tex was published and read back with the required header and final sentinel. The executable source at experiments/meta/2026-10-18_RESOURCE_GAUGE5.py was published and read back independently. The test output aggregate is at results/raw/meta/2026-10-18_RESOURCE_GAUGE5_summary.json.

**Correct SHA-256 of the published executable source:** 144db57820aff9f46f3344f89f20738772c8dd077cb16e3e76064b57405936bb.

The original report text has the older pre-portability hash 52d44b7c21bd8f01d42a69916629854301f692e9b56158f86bc69ab9accaa055. The code was updated to write generated raw output beside the executing script, rather than at a hardcoded container path; mathematical tests and totals did not change. The new hash supersedes that older report hash.

The full machine-readable raw JSON named RESOURCE_GAUGE5_20261018_raw.json was generated and preserved locally, but its direct GitHub publication was rejected by safety checks. The published summary JSON includes all principal aggregate counts and a reproduction command. Running the published script recreates the full JSON.

Proof status: PROVED/EXACT only for the specified restricted-model lemmas, pending independent review. P versus NP remains OPEN.
