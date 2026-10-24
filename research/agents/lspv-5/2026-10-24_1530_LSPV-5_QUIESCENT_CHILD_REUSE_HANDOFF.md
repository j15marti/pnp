# QUIESCENT-CHILD-REUSE: additive LSPV-5 handoff

Date: 2026-10-24. P versus NP remains OPEN. Existing tasks and schedules unchanged. The source reports were read through the connector; no third-party messages were sent.

## What was built

The actual archived INTERFACE-PROJECTION8 construction is a valid scoped 3CNF event stream, not a general ordinary-input normalization. The independent new implementation materializes one ordinary block body and all boundary FORCE gadgets once. It enumerates boundary assignments in Gray order; each transition updates exactly four sign fields. A child is immutable during each solver call. The fixed exact child decider is restarted cleanly, with all work and input reads charged. There is no uncharged assumption interface, persistent learned solver state, free child input tape, full-source variable directory, or complete pair-compatibility table.

Exact reachable-boundary joining is maintained using only old/new frontier bitsets. Declared variable lifetimes are validated before use. Both SAT and UNSAT paths are covered. Incoming reachability is observed information, not a label oracle.

For source length N, block bits b, live width omega, p_j=|I_(j-1) union I_j|, Q=sum 2^p_j, Lmax=tilde O(b+omega):

T <= tilde O(N + Q + Q*T_A(Lmax));
S <= tilde O(b + 2^omega + S_A(Lmax));
child-generation writes <= tilde O(N + Q).

This reduces the old full-rebuild construction charge tilde O(Q*Lmax) when the certified template is available. It does not lower necessary solver reads or imply a total-runtime improvement by the measured write ratio. At b=N^.5 and omega<=log2(N)/20 it reproduces the same restricted recurrence max(1,.6+t/2), max(.5,s/2). The all-input scope gap is unchanged.

Generation writes remain input order on nondegenerate sources. Thus this is not a total-write exponent .5 result. Low peak space and low cumulative writes are different.

## Exact proof status and receiving gaps

- PROVED/EXACT within the scoped contract, complete proof; independent review pending: ordinary child pin encoding, four-field updates, stable read-only simulation, exact global boundary joining, charged buffer/index accounting.
- FILLED only for this restricted implementation: child access without per-probe parent replay, no free ordinary input buffer, no complete all-pairs boundary relation stored.
- RETIRED as a universal write lower bound: every related child must be fully copied before each call. EAGER-LAZY-FRONTIER34 remains a valid upper-bound implementation, not an invalid theorem.
- OPEN: favorable ordinary-input representation acquisition, global small-space addressing, ordinary non-affine high-width cases, and a cofinal all-input route to the FLMV region.
- No universal compiler, unknown exponent discovery or fixed rule menu is imposed as logically necessary. The constructed machine is uniform; theorem parameters are analysis-only where appropriate.

## Reproducibility

Run the published standard-library script with --quick. It executed successfully in approximately 26 seconds in this environment; wall clock is not used as a complexity bound. The optional larger suite was not run. Development syntax errors were corrected before either successful suite run; no failed test was silently discarded.

Final executed source SHA-256: ffef8f7a55219bda70c1919be66995ac400a36e16f29c741e9b93d04e7911052.
Published source Git blob: fb2a54fd81827d9b380459e99e62166b88c1efa3; independently computed local Git blob agrees exactly.
Full local per-case raw SHA-256: 33681f9d51b87e565028e34c79c109a373d05386939d2db84264bc002746029a.

19,616 assertion-accounted checks, zero failures; 400 complete cases, 386 SAT and 14 UNSAT. Includes 8,805 pinned-child brute-force comparisons and 8,805 exact comparisons with fresh serialized buffers. Additional checks reject malformed scope and mutation during a live solver call. High-width/Horn controls select the exact fallback with all failed recognition/source work counted.

Matched q=32 parity controls (each label): 468 calls; rebuilding those children would write 44,418 words; reuse writes 6,390; delayed child solver reads 88,836 words. Peak child 107 words, packed frontier bound 32 bits, plus local maps, generator state and actual solver workspace. SAT/UNSAT solver literal visits differ: 2,843,651 and 2,750,502. The 85.6% reduction is in generation writes only.

Benchmark event construction uses full first/last occurrence metadata and is not the hypothetical small-space input normalizer. Small tests do not claim to satisfy omega<=log N/20. Python sets/dictionaries and audit logs are finite-test instrumentation, not exact physical memory measurements; deterministic maps and packed bitsets are used in the proof.

## Archive coverage increment

Fresh full retrieved sources:
- .codex/skills/pnp-research/SKILL.md, blob b8df83a7b0b1428f349b0e02ce1387d979e8db7f.
- research/main/2026-10-21_0648_MAIN_ARC_EAGER_LAZY_FRONTIER34.md, blob 0f72a05f5592d9ed1825a39bbfa02bc51dbc69c8.
- research/agents/proof/2026-10-20_2124_ARC_INTERFACE_PROJECTION8_STATUS.md, blob cf4141a3664d1be92acc21122c15905f9cce11f6.
- research/agents/lspv-3/2026-10-24_1424_SPARSE83_COVERAGE_HANDOFF.md, blob 2e25523886cc14fe890068399f0e379f642af892.

Root main.tex lines 1-45 only, current blob fd8858769196417295e34b7761fef4772f5e86d2. Prior main13, AGENTS/CODEX and RESOURCE-SCHEDULE-BRIDGE bodies supplied in this conversation reused, not newly retrieved in full. Searches: EAGER-LAZY-FRONTIER34 (8 selected results) and INTERFACE-PROJECTION8 (6 selected results). Prior-chat retrieval used only as a lead to sources. No claim of exhaustive current coverage or repetition of the inherited 3,532-file hash crawl. No full earlier scoped-compiler source recovered.

Primary checks: FLMV author PDF, Section 2.1 and Corollary 5.8, screenshot pages 3 and 17 (zero-based), and parsed source discussion. Primary publication abstracts of Een/Sorensson 2003 confirm incremental related-problem solving is prior work; no new general incremental-SAT novelty is claimed. Gray enumeration, FORCE gadgets and frontier joining are familiar ingredients. This contribution is their explicit ordinary-input and joint-resource combination for the archived candidate.

## Publication and pending root reconciliation

Report creation commit a6bfec042857d4e5ce31be8dd8ca66f2f8ee12f5; report blob 2c848bc49f05b5651b6843a0d91dfce9889f2530.
Auditor creation commit fe205800cc029b76cbd4d5e111e83b2bb6282d37; exact published blob matches executed bytes.
Result-summary creation commit 4a5f246e1ee17819bf0972d1d701b1afd48cc790. Verify its readback and this handoff before calling them remotely verified.
Full six-page PDF, complete per-case JSON and executable are attached in the user's downloadable bundle. That local bundle is not assumed to be present in peer runtimes; published code regenerates the raw per-case results.

No full local repository checkout exists for repository preflight. Direct raw-file retrieval failed due to network name resolution. A full current root body was not safely materialized; no partial reconstruction or overwrite was attempted. Root main.tex remains unchanged, and reconciliation is explicitly PENDING.

Suggested additive paragraph for the LSPV-5 owned region, after fetching the complete current body and fresh SHA:

```tex
\paragraph{Quiescent ordinary-child reuse.}
For supplied valid scoped CNF, one block body and its boundary FORCE gadgets
can be retained across sequential exact solver calls. Gray enumeration
changes exactly four literal fields between calls; the buffer remains
immutable during each call. With boundary-union assignments Q, block size b
and live width omega, generation costs tilde O(N+Q), total time is
 tilde O(N+Q+Q T_A(Lmax)), and peak space is
 tilde O(b+2^omega+S_A(Lmax)). The same scoped recurrence follows; no favorable
ordinary-input normalizer is proved. The 19,616-check audit passes, and
matched q=32 controls reduce generation writes from 44,418 to 6,390 while
retaining 88,836 delayed-solver input reads. Independent review is pending.
P versus NP remains OPEN.
```

## Single next target for shared-spine work

Recover and inspect the complete HEREDITARY-SCOPED10 ordinary-input generator, not just its continuity summary. Require an actual source addressing and representation-acquisition contract on connected, high-width non-affine inputs. If the source stream is supplied for free, or stored in full outside the workspace budget, it does not fill the ARC edge. Test quiescent reuse only after that contract, including live ancestors, failed normalizers and regenerated metadata.

END_OF_QUIESCENT_CHILD_REUSE_HANDOFF
