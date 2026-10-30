# LSPV-1 MIXED-EXTREME-FOREST245, role-addressed handoff (2026-10-30 01:55 PDT)

Active issue: https://github.com/j15marti/pnp/issues/3. Equity issue #2 remains paused. Preserve the existing five task identities, enabled states, hourly :00/:12/:24/:36/:48 stagger, and role ownership.

## PROVED/EXACT restricted, independent referee pending

Let E_{jk}=U_j intersect S_k for distinct ORIGINAL proper signed 3CNF source clause indices j,k. Source occurrences x_{i,j} are shared globally; a local S means 3/3 true and U means 0/3 true, not ordinary disjunctive SAT. Deduplicate identical nonempty mixed event cubes with original clause-pair provenance. For any forest T on event IDs define H_T(a)=1-sum_i 1_{E_i}(a)+sum_{ij in T}1_{E_i∩E_j}(a). Pointwise H_T(a)<=1_{F(a) or F(complement a)} for every coherent original assignment a. Hence #SAT>=max(0,2^(n-1)E H_T); positive B yields a deterministic polynomial-time source-verified witness by conditional expectations. This is a particular Hunter (1976) event-union theorem transfer, NOT a new general SAT algorithm.

Explicit proper 3CNF n=8,m=12 separation source in the report: endpoints 0^8 and 1^8 fail, 47 models, original mixed-pair Gamma=69/32>the earlier threshold 2, one-sided U forest=-1/16, but the mixed U_j∩S_k forest is +5/64. Exactly 74 original feasible ordered clause pairs give 72 distinct event cubes, and a verified witness is reconstructed. Source is NOT strict exact-(2+,2-).

## FALSIFIED/RETIRED as a new pruning mechanism

Every one-pivot source resolvent cube from (x or A),(not x or B) is already rejected by ordinary unit propagation: if the resolvent A or B is false, parents become opposite units or one is empty. Incompatible SS/SU/US/UU extremes alone do not make two source clauses ordinarily unsatisfiable. New cube pruning must be multi-parent and survive UP, ideally also 2SAT SCC.

## COMPUTATIONAL, same-realization evidence

The local 11-family Python package has full original clause-indexed S/U, both inversions, per-occurrence targets, every pair matrix, selected compatible/incompatible triples, coherent 0^n/1^n, partial and multiple flips and per-clause N0..N3, resolution source parents and prohibited cubes, verified witnesses and replayed UNSAT branches. Independent 140-family check: 7,404 original pair modes, 4,072 triples, 206,685 pivot cubes and full pointwise forest enumeration PASS. Same-input baseline UP-DPLL vs controller: n8 SAT 4 nodes/284 selected work versus 0/24,633; W1 strict22 UNSAT 151/11,075 versus 151/365,835. Thus new certificate power does not imply speed. Counts are CPython selected logical events, not TM steps; same-run memory/elapsed time in full raw JSON. Diagnostic source enumeration is accounted separately.

## Explicit role handoffs

LSPV-1 Formal Proof Lead: referee deduplication, the 2-to-1 model-count factor, and conditional integer arithmetic. Seek multi-parent UP/2SAT-resistant source-cube theorem.

LSPV-2 Circuit & Reduction Builder: source-authenticated mixed-event update DAG and learned clause construction; compare with CDCL without hiding preprocessing costs.

LSPV-3 Adaptive Certificate Theorems: test conditional mixed forest under pinned original cubes, with both SAT and UNSAT hostile controls. Do not infer UNSAT from negative B.

LSPV-4 Circuit Resource Auditor: optimize quadratic-in-events Prim comparison costs, charge failed/positive attempts and memory; compare against real CDCL wall time and peak RAM.

LSPV-5 Formal Proof Red Team: independent attempt to break the theorem under duplicate mixed events, tautological parents, source renaming, XOR/Tseitin; recover the root main.tex from a verified substantive Git blob, not its placeholder.

## Corpus review, duplication, root integrity, next lemma

Actual issue #3 read; AGENTS.md blob 19656af1, CODEX.md 754999f5, research skill b8df83a7, ARC244 blob abf005ea, ARC243 checker 1817421c, LSPV-2 source 400cf95f, LSPV-3 6d678114, LSPV-4 e21c9bce, original W1/S15 fixture and primary Hunter/Kullmann/Beame-Kautz-Sabharwal. Hunter, source conflict graphs, one-pivot resolution known; adopt them as prior methods. Reject negative forest bound as UNSAT or local extreme inconsistency as global UNSAT. Root main.tex freshly read at blob bb7ddae5, currently only 'PLACEHOLDER_FULL_CONTENT_FROM_/tmp/main.tex', no authorized ownership region. Do not overwrite; LSPV-5 recovery, root reconciliation PENDING.

Readback-verified standalone public proof: research/agents/lspv-1/2026-10-30_0155_LSPV-1_MIXED_EXTREME_FOREST245_PUBLIC.tex, Git blob 359a13754f77af175d886d3fa4f1a9f2e0852137.
Readback-verified independent checker: research/agents/lspv-1/2026-10-30_0155_LSPV-1_MIXED_EXTREME_FOREST245_compact.py, Git blob acbb7f192aece504046ccc09de532810c7000eb5.
Compact summary: research/agents/lspv-1/2026-10-30_0155_LSPV-1_MIXED_EXTREME_FOREST245_summary.json.

Full local reproducibility ZIP contains 4-page PDF, expanded LaTeX, full 11-case Python, finite-control checker, source-indexed raw JSON, SHA256 manifest. Persistent Library direct-path upload failed with container_session_unavailable; do not claim Library copy verified. All files available in conversation sandbox.

NEXT OPEN LEMMA: find an unbounded polynomially recognizable strict22 SAT+UNSAT family with source-authenticated multi-parent partial-cube refutation surviving UP+2SAT SCC that improves total charged work. P=NP and P!=NP OPEN.
