# ARC-RESTRICTION-COVER118: Role 2 cumulative coverage and gap handoff

Timestamp: 2026-10-24 16:12 Asia/Seoul. Proof spine: ARC/FLMV cofinal finite-hit. P versus NP OPEN. No schedule, task count, or external messages altered.

## Exact result and novelty audit

Given proper signed exact-(2,2) 3-CNF with n original sources and m=4n/3 distinct three-literal clauses, assigning k variables and doing only raw literal conditioning leaves at least m-2k clause records; at least m-4k untouched original clauses remain distinct. Therefore a SOURCE-DEPENDENT family of Q partial-assignment cylinders that covers the FULL Boolean cube and whose ordinary raw children have <=ell surviving records must have Q>=2^((m-ell)/2). Under simple duplicate-cleanup, Q>=2^((m-ell)/4) still follows. Model-specific result, NOT general SAT running time.

For F_q = q disjoint three-variable parity-even quartets, each original variable appears exactly twice positively and twice negatively. F_q has 4^q satisfying source assignments. Any source-dependent raw partial-assignment family that covers EVERY satisfying assignment, with <=ell original residual clauses per child, has Q>=4^(q-ell). For ell=N^b, b<1, ordinary source length N=Theta(q log q) makes Q>=2^Omega(N/logN). The same source is recognizable and decidable by an affine shortcut in polynomial time. FULL SOLUTION COVER is not needed for a SAT root bit. A label-only ARC edge is therefore NOT excluded.

Prior duplication: 2026-10-06 LEAD-0027 WILLIAMS-LANDING-COMPILER already proved formula-INDEPENDENT full-valuation cylinder coverage q*2^ell>=2^n and small-summary guards. The signed polarity floor and the source-dependent strict-(2,2) all-witness affine-quartet variant are the present additions, not a new independent all-decider lower bound. 2026-10-24 CHILD-SCALE-PREFIX117 already exposed hereditary child log-width denominator failure.

## Model/resource guard

E is a set of simultaneously attainable (time,space) polynomial exponent pairs, each supported by ONE fixed uniform exact ordinary SAT decider in the matched random-access bit TM. The forbidden FLMV box near (6/5,1/2) remains published; the invalid universal cosine t+s endpoint is retired. The constructive cofinal all-input successor is OPEN.

BIT-RESOURCE1 counts elementary bit work, read-only source reads, workspace reads/writes, actual value-flips separately, peak live writable bits, cumulative bit-time, and program/representation bits. Eagerly emitting Q ordinary children requires >=Q output bit operations. It does not require Q live child buffers or Q-times-space. A virtual child requires exact charged random-access decoding. Source-aware affine, Horn, SCC, direct decision, caching and failed switches are admissible alternatives. A finite menu is NOT all-decider coverage.

## Experiment and peer-reproducible artifacts

Standalone report: research/agents/lspv-2/2026-10-24_1612_LSPV-2_ARC_RESTRICTION_COVER118.tex
Compact minirepro: research/agents/lspv-2/2026-10-24_1612_ARC_RESTRICTION_COVER118_minirepro.py
Raw summary: research/agents/lspv-2/2026-10-24_1612_ARC_RESTRICTION_COVER118_results_summary.json

The extended separately packaged standard-library audit completed 2,594 checks, zero failures: 480 fixed-seed five-variable inputs independently checked against truth tables; five exact solution-cover controls; affine family scaling through q=2048; signed partial restrictions on strict 198/264 opposite-label sources; a fully independent 537-node source refutation replay and source SAT witness replay. The longer executable, exact source, checker, certificate, and SHA manifest are in the user-visible package. Do not assume transient local attachment paths are available in other agents' runtimes; peers can recover benchmark source and certificate through canonical repository paths, and rerun compact minirepro directly.

## Corpus manifest, full versus selective reading

Full primary originals reviewed: main13.tex (blob 87dbaad5e18932b1db7fca57fc40e0ac020a6f49); LEAD FINAL-LINK-ARC (582b5429f038602f7f8faffabba6d23527cf2ce1); LEAD-0027 WILLIAMS-LANDING-COMPILER (5fea1f11ae4dd0c91f36b1d082434844354345e5); LSPV2 CHILD-SCALE-PREFIX117 (42b08e1a82dff59889a9aa98c4035f4b58a163b2). Drive native PROOF-SYNTHESIS-0013 was fully fetched, 22,010 characters: https://docs.google.com/document/d/1QirzuNPCG-CrE3EX6WweqsPdDbtoblCDEE4YI0HGyC0 .

Targeted/partial: current root main.tex (SHA 9afd01b452578f4e5f1c49a8b1a6e2f612fca551, targeted Role2 region), main9/12/14, latest Role1 ARC-CHANNEL-CURVE119, Role3 SELECTOR-ARC-MARGIN85, Role4 SELECTOR-CAPACITY-BIT-LEDGER81, TORUS-EXACT22-FRONTIER116, AGENTS, CODEX, skill. Directory metadata surveyed for all four specialist dirs, research/main, coordination, tasks, explorations. Current source full-tree crawl not rerun: the 3,532-file SHA/keyword corpus inventory at pinned 55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640 is inherited and manual reviews remain selective. GitHub code search returned earlier LEAD cover guard, so no novelty claim for generic cylinder counting. A malformed search query returned GitHub API 422; no absence was inferred from that failure.

Unexhausted: Google Drive LOG/PROVED_EXACT/Manuscript/BOOL/SIL pagination, many old main2--main12 sections, and original HEREDITARY-SCOPED10 compiler. The continuity log's local path is not a shared implementation. Existence/nonexistence not established by present searches.

## Gap-to-evidence

FILLED (restricted pure conditioning): signed source retention, full-valuation and disjoint affine all-witness cover lower bounds.
PARTIAL/RESTRICTED: BIT-RESOURCE1 emitting-child work accounting and tested hybrid policy.
CONDITIONAL: cofinal finite-hit implication under an ACTUAL achievable all-input route.
FALSIFIED/RETIRED: treating model-cover hardness as universal root-SAT time hardness; polynomial-space cosine product endpoint.
OPEN: every charged all-input favorable ARC pair transition, semantic child gluing, general high-width source-aware reduction with machine-matched peak space.

Next: recover original arc_hereditary_scoped10.py; execute TWO levels on connected high-width SAT/UNSAT sources. Determine whether its children form a raw complete partial-assignment cover. If so, apply this exact firewall; if not, document its proof of semantic coverage and bit-decoder, charged work/space, and model preservation. Compare PCLOSE1-R1 and KDAG2 only after obtaining full original bodies.
