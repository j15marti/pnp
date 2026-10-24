# INTERVAL-FACTOR134 | additive LSPV-1 archive, evidence and gap handoff

**Timestamp:** 2026-10-25 00:58 Asia/Seoul. **Statuses:** restricted PROVED/EXACT mathematical reduction; KNOWN THEOREM polynomial graph-factor feasibility; finite COMPUTATIONAL cross-check; ARC-EDGE-90 OPEN; P versus NP OPEN. No schedules, publication guards or other agents' files changed.

## Exact recovered link and contribution

The predecessor SIGNED-DEGREE2-MATCH133 handles **signed exact-one** source clauses with each variable in at most two source clauses, via ordinary weighted matching with mandatory degree-one choice nodes for opposite polarities. The current extension permits **each clause independently to require any interval** (L_jle #mathrm{true literals}le U_j). The source-to-graph mapping retains original variable identity:

* degree-one variable: clause to private leaf, leaf degree ([0,1]);
* degree-two same-polarity: edge between clause vertices;
* degree-two opposite-polarity: fresh choice vertex degree exactly 1 connected to the two clause vertices;
* clause vertex: degree interval ([L_j,U_j]).

Every feasible graph factor corresponds to one compatible source assignment, both directions. A polynomial ((g,f))-factor method supplies a deterministic polynomial decision algorithm. This is a **restricted upper bound**, not a source of all-input ARC contraction. Standard matching/factor theory is prior art, not a new algorithmic complexity theorem.

With (k(H)=|{v:	ext{source occurrence degree}ge3}|), branching on exactly those variables gives (2^{k(H)}mathrm{poly}(|H|)) time, polynomial space. This parameter is source-defined, independent of runtime and label. It is not uniformly small for arbitrary SAT.

**Additional parity lemma:** if every variable occurs exactly twice and clause demands are exact (b_j), with (h) variables of opposite signs across occurrences, then SAT requires (sum_j b_jequiv hpmod 2). A matched connected (K_4) source has SAT exact-one and exact-two all-positive instances; changing one literal sign makes each UNSAT with unchanged unsigned incidence, size, names, and threshold vector. The factor algorithm still solves both efficiently.

## Falsifiable gap-to-evidence ledger

| Gap | Candidate | Evidence and model match | Status |
|---|---|---|---|
| G134-M1 | Signed exact-one matching extends to arbitrary signed interval cardinality requirements at source occurrence degree at most two | Complete graph reduction, both-way witness proof. Finite independent source/factor tests. Classical polynomial (g,f)-factor theorem. | **FILLED restricted / PROVED EXACT** |
| G134-M2 | Factorization gives a favorable successor of an arbitrary uniform exact SAT pair | General source may have linear (k(H)), branching costs (2^k), recognition+fallback preserve exponent, general ordinary encoding and peak memory uncontracted. | **OPEN** |
| G134-M3 | Many source cycles, parity contradictions, and signed conflicts force universal post-read computation | Explicit polynomial factor shortcut and linear parity rejection; no all-decider time lower bound. | **FALSIFIED as a general inference** |
| ARC-EDGE-90 | Finite all-input charged cofinal route to verified FLMV forbidden box | No reviewed source supplies any such edge, including this report. | **OPEN** |

## Quantifiers, machine and fixed endpoint

Let (mathcal E) consist only of pairs ((t,s)) witnessed by **one fixed uniform total exact ordinary-SAT machine**, correct on **every input** in the FLMV indexed random-access TM model, with simultaneous (N^{t+o(1)}) time and (N^{s+o(1)}) counted space. Under P=NP some finite ((K,K)) belongs to (mathcal E) for all sufficiently large diagonal (K). A cofinal finite route into (t<241/200, s<11642479/23232400) suffices; route edges may be existential and different, with finite depth depending on fixed (K) not uncharged input length. The old (t+s<2cos(pi/7)) test remains **FALSIFIED/RETIRED**. No general source-code compiler or discoverable exponent is necessary for the existential target, although any concrete implementation must pay all source and workspace costs.

## Peer contributions integrated this run

1. **LSPV-2 OVERLAP-CUT128**, full original read, file blob e7c68239: exact compatible boundary-pair count (2^{|S_icup S_j|}), a refinement of the overcount (2^{|S_i|+|S_j|}) for supplied scoped streams, not all-input SAT.
2. **LSPV-3 SCOPE-ALIAS-COMPLETENESS96**, original read, blob a2242d6c: per-clause fresh scopes lose global source identity until equality links are restored and charged, not a certified all-input normalizer.
3. **LSPV-4 PARITY-MARGINAL-COUNT92**, original read, blob b01ca77c: exact counts on every strict primary-pin projection may be independent of orientation, leaving source-bit acquisition; this does not force superlinear post-acquisition work.
4. **LSPV-5 STRICT-SUBJOIN-STATUS131**, original read, blob db4a8d4f: all 15 proper exact-one module-subjoin SAT bits coincide for opposite-label parent formulas; named relation joins recover the label but require paid compatibility.
5. **LSPV-1 SIGNED-DEGREE2-MATCH133**, predecessor original read: signed exact-one matching is strictly subsumed by the new interval ((g,f))-factor reduction.

## Corpus manifest, duplicates, failed sources, and unread queue

**Direct full-text/source inspection:** AGENTS.md SHA c5265db0, CODEX.md SHA 754999f5, research skill SHA b8df83a7, main13.tex SHA 87dbaad5; current root main.tex SHA ccf69112 before this run's own reconciliation; listed five peer originals above and the 2026-10-24_0648 MAIN weighted transcript report. Current repository listing sampled latest reports in all five LSPV directories, research/main, tasks. GitHub term search `HEREDITARY-SCOPED10` returned 99 bounded hits, mostly summaries; content search is not exhaustive. Google Drive exact search `HEREDITARY-SCOPED10` returned one continuity-log document and its original relevant entry was read. Original Google Drive ARC existential source 1QirzuNPCG-CrE3EX6WweqsPdDbtoblCDEE4YI0HGyC0 was read, along with relevant continuity entry 1TselU5xLzVf7nbD2R0r-XZz_8t-S_WNrkiOZxNpbR5E. No new executable original was established. Prior 3,532-file pinned snapshot hash/keyword census is **inherited**, not repeated or promoted to complete theorem review.

**Still unread:** full main2-main12 and main14 sequence, many root historical revisions, tasks file bodies, broad Drive LOG/PROVED_EXACT/BOOL/SIL pagination, remaining GitHub results and older source bodies. Empty-file status was not inferred from unsuccessful discovery. HEREDITARY-SCOPED10 original implementation remains **unrecovered**, but its continuity summary reports valid sublog-width scoped streams only.

**Primary literature:** FLMV (JACM 2005) for model-matched forbidden endpoint; Gabow (TALG 2018) for polynomial graph-factor/matching algorithms; Shao--Zivny (Mathematical Programming 2026) for graph factor intervals; Johannsen (JSAT 2020) for established two-occurrence backdoor context. Direct transfer only for signed interval degree-two factor feasibility. No oracle, proof-system or quantum result was imported as a general SAT runtime lower bound.

## Reproducibility and typed bit resource limits

GitHub full finite audit: `research/agents/lspv-1/2026-10-25_0058_INTERVAL_FACTOR134_full_audit.py`. Local run used standard library, seed 202610240858. **3,395** sources, **2,388 SAT / 1,007 UNSAT**, **22,196** assertion-accounted tests, **zero failures**; all (2^{12}) (K_4) sign assignments tested for parity necessity. An independent compact peer audit `2026-10-25_0058_INTERVAL_FACTOR134_minirepro.py` tests 1,032 exact configurations and matched K4 controls. The full audit enumerates factors, **not** an implementation of polynomial matching. Typed bit-resource dimensions (primitive bit work, source/work reads/writes, complete-state flips, peak writable bits, bit-time, program/representation size) are theoretically bounded or charged in the symbolic proof, but **not physically measured** by this Python test.

## Next artifact and precise gap

Highest-priority missing implication: a fully charged, source-coherent, all-input uniform exact SAT transformation from a polynomial achievable resource pair to a favorable simultaneous pair, or a cofinal finite route, entering an FLMV forbidden region. For the next test, inspect Role 2's `OVERLAP-CUT128` exact schedule code and Role 5's `STRICT-SUBJOIN-STATUS131` original counterexample alongside the remaining original `HEREDITARY-SCOPED10` archive locations; ask whether any proposed factor/interface child is truly **ordinary-source shorter in encoded bits** and still preserves the named parent join without a full-size fallback.

**Publication safeguard:** publish the LaTeX report and both scripts and raw aggregate, verify readback, then reconcile only LSPV-1-owned root-main section with freshly fetched SHA, preserving other regions. P versus NP OPEN.
