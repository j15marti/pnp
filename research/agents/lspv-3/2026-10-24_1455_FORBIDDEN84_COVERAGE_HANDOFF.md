# FORBIDDEN-COMPUTATION84: additive coverage and gap handoff

P versus NP remains OPEN. This is a focused application of recovered computational exclusions, not a new exhaustive archive search or an all-input SAT contractor.

## Verified publication
- Report: `research/agents/lspv-3/2026-10-24_1455_LSPV-3_FORBIDDEN_COMPUTATION84.tex`, initial commit `2347572f501ed309e06f2c8e81c88c4e3f02d6bb`, blob `309a24ef1a503b5463225defa90ee16d9962e55a`. Full body and closing sentinel read back in two line ranges.
- Compact independent reproducer: `research/agents/lspv-3/2026-10-24_1455_FORBIDDEN84_minirepro.py`, commit `16bf65431760b932dd6afa74cfa439b4bf458264`.
- Expanded five-page local PDF, full standard-library DIMACS audit, both deterministic runs, 30 ordinary-CNF controls, and raw JSON are in the downloadable FORBIDDEN84 package. Local paths must not be assumed shared across runtimes.

## Exact mathematical application
For one fixed uniform all-input SAT machine in the FLMV random-access model, take total acquisition/discovery time D<=N^(a+o(1)), complete exact-join time J<=N^(b+o(1)), and peak simultaneous workspace W<=N^(s+o(1)). If (max(a,b),s) is forbidden, the combined contract cannot hold. This excludes a universal cheap normalizer-plus-joiner; it does NOT refute a restricted forest solver or prove an all-input successor.

Use beta(c)=((c+2)/c^2-c)/2 and strict witness c>max(1,t). The full FLMV Theorem 5.7 family is also available: f0=1, f_(ell+1)=c*f_ell/(1+f_ell), beta_ell=min((1/f_ell-c)/ell,c^(-ell)). A fixed integer ell and strict c may certify additional endpoints.

Examples with exact proof witnesses:
- t=6/5, s=1/2: c=241/200, ell=2; threshold=11642479/23232400.
- t=5/4, s=3/10: c=63/50, ell=2; threshold=157453/396900.
- t=3/2, s=1/20: c=151/100, ell=4; threshold=13827784249/207954240400. The ell=2 curve misses this point.
- t=31/20, s=1/50: c=39/25, ell=5; threshold=317297489/11278024875.

## Storage-sensitive sparse-join ledger
At most N^gamma components, support size N^alpha, pair cost N^chi, signature length N^lambda, acquisition N^a, other live workspace N^sigma give
 t=max(a,gamma+2alpha+chi), s=max(sigma,gamma+alpha+lambda)
for sequential pair tests. Cache-all-pairs adds gamma+2alpha to s. A whole source copy adds 1. Full witness lifts and graph indexes remain charged.
Hypothetical profile (a,gamma,alpha,chi,lambda,sigma)=(1.1,.4,.1,.6,0,.5): streaming pairs -> (1.2,.5), excluded; pair cache -> (1.2,.6), not excluded by this family; source copy -> (1.2,1), not excluded. Non-exclusion never proves existence.

## Computation
Full audit: 194 assertions; 30 proper-3CNF finite controls, 15 SAT and 15 UNSAT; no discrepancies. Exact arithmetic checks reference fractions, 61 curve points, nine envelope points, ten pairs, three storage modes, three streamed-normalizer profiles. Envelope search certifies its infinite tail using beta_ell(c) <= (1/(c-1)-c)/ell, not an unjustified index cutoff. Two runs produced identical full raw JSON.
Raw SHA-256: `86141c40dae838cbc8eb2ad3377b4ad616f4b207308eb2638fddedc2ba69816e`.
Compact remote reproducer is smaller than the full audit. No formal Turing-machine memory measurement is claimed.

## Coverage delta
Full or targeted source review: AGENTS.md, CODEX.md, repository research skill; main13.tex lines 1-240; mathematical portions of root main.tex; FLMV-CURVE-FRONTIER115; ARC-STREAM-FENCE117; SPARSE-BOUNDARY-SUPPORT83; COFINAL-QUANTIFIER-ENDPOINT116. Retrieved head before writes: 7ec2564bff10a6d4e2339726e33e8b9dc7f9697b; initial peer reads pinned to 5bef483e7684555b2a87057e27b78d080873f871. Primary FLMV PDF checked at model, transfer, recurrence (14), Theorem 5.7, Corollary 5.8; pages 4,6,17,18 visually checked.
No new Drive corpus search, tree-wide inventory, 3532-file rerun, or HEREDITARY-SCOPED10 full-source retrieval is claimed. Raw-network access failed DNS; repository-wide preflight/validation scripts were not run. Root main.tex is not reconciled in this focused application run; this additive role-owned handoff is available for synthesis without overwriting others.

## Gap acceptance
FILLED/KNOWN: matched FLMV family and strict endpoint certificates.
PROVED/EXACT within stated model: paid acquisition/join composition exclusion; full-family infinite-tail arithmetic certificate. Independent peer review pending.
PARTIAL/RESTRICTED: sparse forest joins, scoped-stream consumers and recursive accounting.
FALSIFIED/RETIRED: cosine product endpoint; memory-blind entry; free boundary relations.
OPEN: actual all-input favorable achievable-pair edge or conditional cofinal finite-hit route. Existing polynomial word-RAM bounds with unspecified exponents do not fill it.

Next artifact: original full HEREDITARY-SCOPED10 compiler, focusing on arbitrary-input discovery, exact shared-boundary coherence, indexed child bits, and generator/ancestor memory. Adaptive alternative representations remain legal; all policy selection and switching costs must be included. No task schedule was changed.
