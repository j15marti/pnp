# ADAPTIVE-LOCAL-DEPTH126: LSPV-1 owned cumulative coverage and gap handoff
**UTC date:** 2026-10-24. **Status:** P versus NP OPEN; ARC-EDGE-90 OPEN. No task, cadence, routing or notification change.

## Accepted new restricted theorem
For all integers k>=0, build a connected duplicate-free proper 3CNF pair U_k,V_k of equal parameters
n=51+2k, m=36+k, N=(4m+2)ceil(log2(64(n+m+1))), opposite labels UNSAT/SAT, and identical ordered **source-anonymized isolated-clause** truth profiles p_i. Any deterministic, adaptive or randomized, finite terminating controller whose observation queries depend only on these profiles, chosen original clause index and local history has identical coupled transcripts for both parents even with arbitrarily deep *clause-local* pin recursion, caching, interleaving and representation changes. Its maximum error on the pair is >=1/2. Proof: growing guarded-connected pair from Role 3 + transcript induction; role 5 already proved exact two-level idempotence. **NOT** all-decider coverage: a source-aware machine can directly read IDs; cross-clause grouped queries may work. No lower bound beyond this channel.

## Construction and reproducibility
Role 3 base: U contains eight sign patterns on one scope (v1,v2,v3); V uses those same eight sign patterns on eight disjoint triple scopes. Both append 24 guard-bridges (g OR vi OR v(27+i)), i=1..24, plus four clauses of the exact unit gadget U(g;v26,v27). g=v25 is forced true. For every padding j<k add (g OR v(52+2j) OR v(53+2j)) to both; all clauses remain distinct and every variable occurs in one connected component. The original Role 3 full profiles and Role 5 named identity are dependencies, not newly discovered.

Finite audit (independent DPLL with pure-literal/unit propagation plus adaptive clause-local testing):
k=0,1,4,32; (n,m,N)=(51,36,1898),(53,37,1950),(59,40,2106),(115,68,3836). All pair labels verified and all indexed local profiles equal; 512 adaptive local queries per formula per k with maximum tested depth 3 were identically answered; all 36*8*13=3744 pinned-grandchild clause profiles checked for k=0. DPLL search nodes at k=0: U 7, V 1. Zero failed Python assertions. No FLMV physical bit-time/peak-space measurement is claimed.

Published:
- LaTeX: research/agents/lspv-1/2026-10-24_1900_LSPV-1_ADAPTIVE_LOCAL_DEPTH126.tex
- Reproducer: research/agents/lspv-1/2026-10-24_1900_ADAPTIVE_LOCAL_DEPTH126_minirepro.py
- Raw results: research/agents/lspv-1/2026-10-24_1900_ADAPTIVE_LOCAL_DEPTH126_results.json
- This handoff: research/agents/lspv-1/2026-10-24_1900_ADAPTIVE_LOCAL_DEPTH126_COVERAGE_HANDOFF.md

## Gap to evidence map
- **FILLED (KNOWN THEOREM):** matched random-access FLMV SAT time-space forbidden endpoint (paper DOI 10.1145/1101821.1101822). Two-level margin beta(c)=((c+2)/c^2-c)/2 strictly decreases; earlier t+s<2cos(pi/7) as universal SAT endpoint is **FALSIFIED/RETIRED**.
- **FILLED (elementary PROVED/EXACT, independent review pending):** existential finite-hit implication from a jointly achievable (K,K) to a verified FLMV box. This implication alone is not a SAT contraction theorem. Role 5 COFINAL116 identifies its separation-equivalent strength.
- **FILLED (RESTRICTED, this run):** arbitrary finite adaptive/randomized isolated-clause profile protocols fail even on connected growing equal-profile opposite-label parents.
- **PARTIAL/RESTRICTED:** LSPV-2 SELECTOR-SPLIT119 gives a source-correct affine/2-CNF encoding but parent gluing is original NP-complete decision; LSPV-3 PIN89 gives connected local-profile collision; LSPV-4 NESTED84 gives correct nested virtual bit access but no parent-count gluing; LSPV-5 NAMED125 gives reversible named profiles and exactly the original Boolean CSP join.
- **CONDITIONAL:** max-affine, typed multichannel and lazy/virtual frontiers require a fully charged all-input exact parent-child construction not supplied by the interface arithmetic.
- **OPEN ARC-EDGE-90:** a single correct uniform all-input same-machine resource successor or cofinal finite route; all source bits/indices, choice/switching, child bits, headers, compatibility, ancestors, caches, failed attempts, full bit work and peak live bits charged.
- **OPEN archival dependency:** original ARC-HEREDITARY-SCOPED10 executable; a Drive continuity log contains only a specific restricted scoped-stream report, not its program bytes. No local path from its prior runtime may be assumed available.

## Full vs keyword vs unavailable coverage for this run
FULL GitHub connector reads: AGENTS.md blob c5265db06c0f; CODEX.md blob 754999f50de9; .codex/skills/pnp-research/SKILL.md blob b8df83a7b0b1; main13.tex blob 87dbaad5e189; main.tex at start blob 1b052627a452; lead FINAL-LINK-ARC report blob 582b5429f038; Role 3 PIN89 report blob f0f1713e7e49; Role 4 NESTED84 report blob c62e80e0a97f; Role 5 NAMED125 report blob a305dee0cf14; Role 1 ENDPOINT125 handoff blob 66706aaca9e4. Role 2 SELECTOR-SPLIT119 text was read in its current root-main owned region, not a separately verified original report. One guessed Role 2 report path returned 404; no absence is inferred from that.
FULL Drive reads: ARC precursor document 1QirzuNPCG-CrE3EX6WweqsPdDbtoblCDEE4YI0HGyC0, continuity log 1TselU5xLzVf7nbD2R0r-XZz_8t-S_WNrkiOZxNpbR5E.
Keyword search only: GitHub ARC-EDGE-90, NAMED-PROFILE-IDENTITY125, MINIMAL-UNSAT-PROJECTION20, HEREDITARY-SCOPED10, COFINAL116. Drive exact HEREDITARY-SCOPED10/ARC-HEREDITARY yielded only continuity log. Targeted searches are not exhaustive.
Inherited only: prior pinned 55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640 hash-verified 3,532-file keyword census. Selective proof-body read is explicitly not exhaustive. Entire LOG/PROVED_EXACT/BOOL/SIL/Manuscript archive not completed this run; no absence inference.

## Competing spine ranks
1. ARC/FLMV: independent forbidden endpoint, correct conditional contradiction, decisive all-input contraction OPEN.
2. Knowledge compilation/proof-system: restricted theorems, unrestricted decider extraction OPEN.
3. UWI/universal selector: witness-cost characterizations, independent lower-bound transfer OPEN.
4. WRAPPER/clocks/hashes: provenance constructions, no unconditional arbitrary-decision cost obstruction.

## Next exact test
Demand a source-consistent cross-clause interface with an explicit bounded-size, bounded-fanout ordinary-child construction; a proved SAT/UNSAT parent gluing law; and all-input charged t/s machine accounting. Before exponent work, force it to distinguish the growing connected same-local-profile U_k,V_k **and** Role 4's periodic same-count U_d,V_d through two levels. If the compiler retains all named profiles, Role 5's linear invertibility leaves the original SAT/CSP join; no missing expense may be called free. If it discards names, this run's local-depth theorem supplies opposite-label failures. Check adaptive switches to SCC, affine, Horn, cache/direct decision and source read.


## Post-publication source recovery: Role 2 original verified
After the initial report write, GitHub filename search located the correct original path \`research/agents/lspv-2/2026-10-24_1812_LSPV-2_SELECTOR_SPLIT119.tex\` (blob \`66a63373b5c7b3e7bbe1e732d12ec4f7e166f9ec\`), and it was read in full. The earlier attempted \`...1825...\` path was simply a bad guessed timestamp, not an unavailable original. The report proves a source-coherent all-input affine-XOR3 and bijunctive split on \(3m+n\) variables, \(m\) independent XOR3 rows, and \(6m\) binary clauses, and an ordinary proper-3CNF encoding with \(16m\) clauses and \(9m+n\) variables. Each individual child and each entire affine/bijunctive component is independently satisfiable on both parent labels. The shared compatibility conjunction is equivalent to the source proper 3SAT instance. This confirms and strengthens the Role-2 contribution already integrated; it does not change Theorem 1, the ranking, or ARC-EDGE-90's OPEN status. Full text read, not a snippet.

Historical standalone report is an immutable snapshot of the pre-correction evidence list; this additive handoff records the subsequent original-source recovery without claiming earlier access.
