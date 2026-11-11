# LSPV-2/561: Terminal-live paid-Resolution fanout split and exact congruence quotient

**2026-11-11, 10:12 PST | SAT-Circuit Reduction Builder | historical Route A retained | PROVED/RESTRICTED + COMPUTATIONAL. P versus NP remains OPEN.**

## Target, candidate, falsifiers

**P2-D1 -> P2-C3, restricted authenticated /386 calculus only.** Construct two *distinct* paid native Resolution records with identical oriented inferences, both reachable from the final empty clause, with the identical signed source and source-clause set. Develop a conservative reference inverse replayer that merges only identical paid inference signatures, not arbitrary equal conclusions. Test against the unchanged original archived /386 checker (blob `338305c0ce101704205e57543756b8127074a986`).

F1: The original checker rejects a repeated paid RES identity. F2: One duplicate is dead to the terminal sink. F3: Source provenance, summary counters or chronological parent edges fail after splitting or coalescing. F4: An underpaid, malformed pivot, forged source, incorrect parent sign or future parent is incorrectly admitted.

The result supports an **identity-sensitive exact cost replayer**. It is not a lower bound, not full R_mix341 accepted-byte closure, and not a claim that clause-set-only overapproximation is inherently cost-unsound.

## Accepted-byte experiment

Start from LSPV-2/560's already checked, canonical, 3,092-byte signed K4 certificate (Git blob `3843187f0ccccf8f04cc049e25a8de1df91ce194`). It has 17 signed SOURCE records, two zero-extra-paid DEF facets, one globally paid conservative AND2 gate owner and 30 paid RES records, with 49 proof records and `W=31`.

The original RES row `r_20` has signed result `[-1,-4,-5,-7]`, pivot `-8`, parents `[19,1]`, and two direct downstream users, original rows 22 and 24. Insert a *second* identical RES record immediately after row 20. Remap all later parent indices to account for the insertion. Redirect only original user 24 (now row 25) to newly inserted row 21, leaving original user 22 (now row 23) depending on row 20. Both paid identities occur in the terminal contradiction's transitive parent cone.

The original signed SOURCE records, gate owner, DEF facets, terminal empty clause and the entire set of signed derived conclusions are unchanged. Only one extra, separate paid proof-record identity appears. Recompute the checker-authenticated summary as 17 SOURCE, 2 facets, **31 RES**, one paid owner, 50 records and **W=32**. The new exact UTF-8 JSON packet is 3,153 bytes.

The original archived /386 `checkProof` function, executed unchanged in hosted V8 with dependency/input compatibility adapters, accepted the packet. Its complete original mathematical validity checks and the odd/even K4 source audit ran. The exact published Node.js tool additionally invokes the unchanged original CLI in real OS subprocesses when executed from a checkout, but that newly published tool's complete OS run was **not observed in this run**.

## Restricted theorem: identical paid RES coalescence

Let `P` be any parsed proof accepted by the archived /386 checker. Suppose two *nonterminal* rows `i<j<last` have kind `RES` and identical ordered parent record indices, oriented pivot and signed result clause. Produce `P'` by replacing every subsequent reference to row `j` by row `i`, removing row `j`, monotonically reindexing all remaining row indices, and recomputing the six checked summary counters, without modifying SOURCE bodies or owner definitions.

Then

$$
\operatorname{Accept}_{386}(P)\Longrightarrow\operatorname{Accept}_{386}(P'),
\qquad W_{386}(P')=W_{386}(P)-1.
$$

**Proof.** The earlier row `i` has precisely the same checked clause and exact ordered parent inference as `j`; therefore it is a legal replacement wherever `j` was used. The replacement is always chronologically earlier. Every remaining RES still has the same valid signed pivot orientation and resolvent. The original source set and mandatory source-occurrence coverage are unchanged, as are gate owner declarations, their freshness, dependencies and facet legality. The terminal empty row is preserved because `j` is nonterminal. The original checker imposes no assumption contexts, branch scopes or deletion semantics. Its summary fields can be recomputed and exactly one distinct paid RES identity disappears. This establishes acceptance and exact one-unit reduction. QED.

In the concrete split certificate, this inverse produces the original 3,092-byte certificate **byte for byte** under the established canonical one-line JSON serialization plus newline. This is a restricted normal form, **not** a proof that minimum /386 work is 31.

The identity signature must include at least the paid operation, ordered parent identities, pivot and signed result. A genuine mixed calculus could additionally require source hashes, rule ports, contexts, wire visibility, freshness, discharge/branch obligations and local transformation state. Do **not** apply this quotient to those unauthenticated rules without a separate simulation proof. In an abstract **lower-bound** search a cheaper clause-only MAY path can be cost-sound (`W_abs<=W_concrete`), but it is not an *exact* concrete-transition replay and must not be equated with exact paid work.

## Replayer and CEGAR boundary

The published reference code reconstructs split and coalesced histories with explicit chronological index mapping, signed clause provenance, globally charged owner and RES records, unchanged SOURCE occurrences, and the full terminal shared-parent ancestry. Its alpha carries the typed rows, clause vectors, ordered parent IDs and global paid sets; gamma is restricted to parsed /386 packets satisfying the authenticated source/owner and resolution checks. The concrete split adds one paid identity, while the exact congruence contraction removes one, preserving terminal acceptance. This is a model-specific quotient transformer, not a full-calculus alpha/gamma theorem.

A cheaper candidate suggested by collapsing *only equal conclusion strings* is not automatically spurious: in a context-free resolution fragment it may correspond to a genuine legal substitution. CEGAR must preserve such legal shortcuts. Requiring exact parent/pivot congruence is a safe sufficient contraction, not a claim that all less restrictive contractions are illegal.

## Original-checker differential results

The unchanged original mathematical checker was called 11 times in hosted V8: **3 ACCEPT and 8 REJECT, all 11 expected outcomes**, 4,317 internal mathematical assertion groups total. Valid controls: source W31 / 49 records / 3,092 bytes, live split W32 / 50 records / 3,153 bytes, exact coalescence inverse W31 / 49 records / 3,092 bytes. Both live identities reached the terminal empty clause. Under the program's RES-edge-depth convention the three positive packets have depth 9 (not physical machine span).

The eight rejected falsifiers were underpaid RES, wrong RES summary count, wrong total row count, invalid second pivot, false second resolvent, self/future parent, forged SOURCE clause, and two same-sign parents. The original `checkProof` function was not changed. **This run does not claim execution of the original checker as an OS subprocess for the newly generated 3,153-byte packet.**

Physical machine construction/verification time, input reads, hash computation, certificate bits, physical peak memory, logical depth, and paid proof work are separate ledgers. `W=32` is **not** a 32-step algorithm for SAT. The 61-byte certificate increase is not a time-space lower bound.

## Reproducibility and primary references

- Original archived /386 checker: `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`.
- Reference replayer plus original Node CLI differential test: `experiments/arc/lspv2_561_native386_paid_fanout_congruence.cjs` (run `node experiments/arc/lspv2_561_native386_paid_fanout_congruence.cjs /tmp/pnp561`).
- Complete accepted UTF-8 packet: `results/raw/arc/2026-11-11_1012_LSPV2_561_ACCEPTED_LIVE_PAID_RES_FANOUT.json`.
- All 11 original-body outcomes: `results/raw/arc/2026-11-11_1012_LSPV2_561_ORIGINAL_CORE_V8_TESTS.json`.
- Prior proof and controls: LSPV-2/539 through /560, especially /549's noncomposition firewall and /560's source-complete terminal cone; issue #3; root `proof1.txt`, `proof2.txt`; `AGENTS.md`, `CODEX.md`, repository research skill. Peer LSPV-1/575, LSPV-3/573, LSPV-4/546 and LSPV-5/491 informed current model boundaries.
- S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), https://doi.org/10.2307/2273702.
- P. Cousot and R. Cousot, *Abstract Interpretation*, POPL (1977), https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml.
- Official external FRAT-XOR/XLRUP specification: https://github.com/meelgroup/frat-xor/blob/main/format.md; verified LRUP checker https://github.com/lammich/lrat_isa. These are **different proof grammars** and cannot authenticate historical R_mix341 rules.

## Reconciliation and open arrows

**What changed:** a fully terminal-live, separately paid identical-RES duplicate accepted by the original /386 checker and its provably sound context-free exact-congruence inverse, with executable test generator and raw falsifiers. **Adopted:** archived checker /386, fixed original-source audit, source-complete cone /560 and no-free-owner accounting. **Rejected:** treating a shared signed clause as a unique paid proof-record ID for exact replay. **Retired:** no current full-calculus claim.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1] and separately [P2-B2]/[P2-B3] remain OPEN. The full historical R_mix341 dispatcher supporting RES-to-AND3, DEF-to-LOCAL-CONVERT, context, branch and discharge is still missing; other rules remain conservative MAY possibilities. No theorem permits inference from this restricted proof normalization to a universal SAT lower bound or B3. The historical two Route A / three Route B assignment and all five existing agent titles, schedules, timezone, weights and ownership boundaries were left unchanged.

**P versus NP remains OPEN.**
