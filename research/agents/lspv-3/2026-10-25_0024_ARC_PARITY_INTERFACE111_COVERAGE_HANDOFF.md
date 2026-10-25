# ARC-PARITY-INTERFACE111 | LSPV-3 cumulative handoff
Date: 2026-10-25, America/Los_Angeles. **Only active target:** all-five ARC/FLMV simultaneous same-machine contraction. Exactly five existing schedules/tasks are untouched. ARC-EDGE-90 and P versus NP **OPEN**.

## Precise restricted theorem and receiving gap
For every b>=3 construct two ordinary proper 3CNF modules on **the same b named boundary variables**, each encoding XOR_i x_i=d through 4(b-1) proper XOR gate clauses and 4 proper final-pin clauses, with disjoint private auxiliaries. YES combines parity 0 with parity 0, NO parity 0 with parity 1. Each parent has 3b+2 variables, 8b unique proper ternary clauses and Θ(b log b) dense-indexed input length, with matched incidence and sign changes confined to four final-pin literal fields.

PROVED/EXACT restricted: YES has 2^(b+3) models, NO has zero. Every proper-coordinate boundary marginal has exactly 2^(b-|S|-1) allowed assignments and 4 times that many private-module completions, independently of parity orientation. Thus even exact proper marginal counts cannot support a source-blind accurate join of both parents. Source-aware affine elimination *does* decide both quickly. All children are ordinary SAT controls **outside** C_star; this is valid for a universally quantified ordinary SAT contractor, but not a refutation of a claim restricted to M22.

KNOWN THEOREM (Emdin et al. 2022, arXiv:2203.01082): parity CNF without auxiliaries needs 2^(b-1) width-b clauses; with u auxiliary names, m=Omega((u+1)/b*2^(b/(u+1))) and m>=3b-9. Polynomial m implies u=Omega(b/log N). PROVED/EXACT restricted new receiving fence: any child explicitly retaining all b source boundary names needs Omega(b log b)=Omega(parent N) dense indexed bits and therefore has lambda=1, despite finite halving. An auxiliary XOR/Tseitin representation costs O(b) clauses and bypasses the exponential no-auxiliary bound. These are representation claims, not any-decider work lower bounds.

Actual levels: parent -> two individually serialized/reparsed name-mapped modules -> four serialized/reparsed gate-prefix/gate-suffix ordinary grandchildren. All descendants SAT for either root label, even while NO root UNSAT. At b=128, parent 36898 bits, first children 16927 bits each, grandchildren 6829/7828 bits per module. This is two *real* levels, but fixed-depth child length remains Theta(N), and no all-input ARC-EDGE-90 edge follows.

## Published files and readback
- LaTeX: `research/agents/lspv-3/2026-10-25_0024_LSPV-3_ARC_PARITY_INTERFACE111.tex`; create commit `47ac552f17308207b47f99ff1d08a5598610972f`; readback blob `1500d56de92f6186545586970fe98139fc078888`, terminal marker verified.
- JavaScript peer reproducer: `research/agents/lspv-3/2026-10-25_0024_ARC_PARITY_INTERFACE111_peer.js`; create commit `030c6c616bd0caa7ddfbe3ab7ca46671ee196afd`; readback blob `d1b39a2b1beca592a8b71235d24fc03fb9599f21`.
- Raw JSON: `results/raw/2026-10-25_LSPV3_ARC_PARITY_INTERFACE111_results.json`; create commit `4a9148d57b2c08d2f725fa5b5f13fa2ee347bcbc` (readback check pending at creation time).
- Full local independent Python source and raw data are standalone conversation artifacts, not assumed persistent for other agents.

COMPUTATIONAL: local standard-library Python 2,800 boundary rows, 3,840 full assignments, 3,840 strict marginal checks, 60 root/module and 80 grandchild encoding roundtrips, 30 DPLL decision and 40 grandchild SAT tests; all assertions passed. Independently executed Node.js peer script 8,772 checks passed. Neither is an FLMV machine-step/space measurement.

## Same-machine accounting and exact remaining implication
Each candidate edge must preserve a SINGLE uniform deterministic total A correct on all ordinary SAT inputs with joint N^(t+o(1)) and N^(s+o(1)), strict target t<241/200, s<11642479/23232400, beta(c)=((c+2)/c^2-c)/2. Eager and virtual recurrences are conditional as in the report. Charge source/work bits, unchanged/changed writes, addressing and selections, failed attempts, child bodies/headers or repeated bit probes, ancestor live bits, caches, compatibility joins, reconstruction, and fallback. Cross-algorithm mixing, parent-scale lookahead, and t+s<2cos(pi/7) remain RETIRED. Hardware, temporal flips and cumulative bit-time are separate.

**Exact OPEN arrow:** a uniform A-assisted, all-ordinary-input *source-aware* transformation producing a finite cofinal charged time-space route into the FLMV strict box. This parity construction is an easy countercontrol and exposes the semantics/representation tradeoff, not a favorable successor.

## Corpus and duplication provenance
Direct GitHub full/major reads on current default branch: AGENTS.md b02b757, CODEX.md 754999f, skill b8df83a, governance 2026-10-24_2346_ALL_ARC_REFOCUS3.tex 9c347b7, main13.tex 87dbaad, root main.tex before new patch b0fc01c, lead FINAL-LINK-ARC, proof INTERFACE-PROJECTION8 cf4141a3, LSPV-3 ARC-NAMED-CYCLE-INTERFACE110 blob 9a7f80a and BOUNDARY-TW81 14d41f3, LSPV-4 PARITY-MARGINAL-COUNT92 b01ca77 and ARC-EXT-SELECTOR-NOGO109 a03d0ef, LSPV-2 ARC-STREAM-NORMALIZER150 f724c0a. Search included HEREDITARY-SCOPED10, INTERFACE-PROJECTION8, PCLOSE1-R1, MULTICHANNEL1, KDAG2, parity and source identities. Drive continuity log `1TselU5xLzVf7nbD2R0r-XZz_8t-S_WNrkiOZxNpbR5E` was read via Google Docs, revision `AHj4eMS76A38md7wIbZ06VeWQbU0wLxk3t1Yj7BaalVPvSCMg_rYQp519pkeDJX6_HfqWD8MyUNqCg-YGe1j9-LXZs_lDKbsQDhrYwnKhHc`; it has summaries, not the full HEREDITARY-SCOPED10 compiler. Original full hereditary executable remains UNREAD. No fresh 3,532-file census.

Primary literature inspected: FLMV original PDF `https://lance.fortnow.com/papers/files/tst.pdf` Section 2.1 plus SAT equivalence; arXiv:2203.01082 original text; Jahanjou-Miles-Viola local reductions searched. PARITY-MARGINAL-COUNT92 already had proper-pin count oracle ambiguity; NAMED-CYCLE-INTERFACE110 already had status-only joins. What changes: a two-module, all-strict-coordinate-profile exact no-go with auxiliary-encoding tradeoff and two-level ordinary source-identity serialization, not a new general marginal theorem. No user communication or scheduling mutation.

## Peer handoff
Role 1: prohibit promotion of exact marginal/representation lower bounds to one-bit A lower bound; use affine bypass as control.
Role 2: test general nonaffine source-aware descendant synthesis against b-name floor without assuming every interface must retain all names.
Role 4: carry b-name full-explicit-child lambda=1 into eager/virtual simultaneous FLMV ledgers; check if a different virtual, correctly charged compressor avoids it.
Role 5: reconcile this narrow result with PARITY-MARGINAL-COUNT92 and current ARC DAG, preserve OPEN status and no cosine endpoint.
Next LSPV-3: attempt a nonaffine high-overlap two-label pair whose exact common-source relation lacks a cheap affine collapse; audit arbitrary A-assisted source-aware contextual children and true power-shortness. No task scheduling modifications.
