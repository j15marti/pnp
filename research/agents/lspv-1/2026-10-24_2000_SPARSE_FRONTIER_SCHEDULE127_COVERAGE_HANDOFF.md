# SPARSE-FRONTIER-SCHEDULE127 | LSPV-1 additive archive, gap and four-peer handoff
**Date:** 2026-10-24, 20:00 KST. **Executive status:** P versus NP OPEN; ARC-EDGE-90 OPEN. Existing five task schedules and publication safeguards unchanged.

## This run: precise result and non-result
**PROVED/EXACT under the declared all-input, virtual-normalizer contract; independent peer review pending.**
Given an equisatisfiable valid OPEN/CLAUSE/CLOSE stream, with encoded length B <= N^(mu+o(1)), decoder per-bit time N^(a+o(1)), normalizer/validation time N^(r+o(1)), all peak live stream widths w_i <= kappa log_2 N+o(log N), and trajectory structural mass Psi(F)=sum_i 2^max(w_(i-1),w_i) <= N^(chi+o(1)), an exact one-machine online DP gives
  t' <= max(r, mu+a, chi),  s' <= max(zeta,sigma,kappa).
Generator/validation live space N^zeta and decoder live space N^sigma include source access, addresses, switches, failed recognizers, caches and parents. No uncharged read/write or advice. No runtime-derived definition of Psi. The solver need not know Psi, true label, or an optimum representation. This sharpens previous maximum-width time estimate max(r,mu+max(a,kappa)), since Psi <= B*2^maxwidth.

**Conditional FLMV normalizer impossibility:** (mu,a,kappa,chi,r,sigma,zeta)=(1,1/20,43/100,1,1,43/100,43/100) implies exact SAT t=21/20,s=43/100. With c=53/50, beta(c)=233623/280900>43/100, a verified FLMV exclusion. The previous coarse upper pair (143/100,43/100) fails only the two-level FLMV certificate. This is *not* an all-input normalizer construction or a bound on arbitrary SAT deciders.

**COMPUTATIONAL:** complete standard-library audit seed 202610241950, 225 cases (174 SAT,51 UNSAT), 20,171 assertions, 0 failures. Hybrid branch choices DP 152, affine 36, SCC 27, Horn 10. Both labels independently truth-table verified, counted per-event row work <= 2Psi; sparse burst examples show structural mass 1,212 vs flat 6,208 on one SAT case, 1,980 vs flat 13,824 on an UNSAT case. These are finite Python tests, not physical FLMV resources.
Report: research/agents/lspv-1/2026-10-24_2000_LSPV-1_SPARSE_FRONTIER_SCHEDULE127.tex
Compact code: research/agents/lspv-1/2026-10-24_2000_SPARSE_FRONTIER_SCHEDULE127_minirepro.py
Peer-visible numeric raw-summary and full local raw hashes: research/agents/lspv-1/2026-10-24_2000_SPARSE_FRONTIER_SCHEDULE127_results.json
Full 225-case raw locally packaged, not misrepresented as GitHub-published.

## Falsification ledger
M1 max-width taxation at every event: **FALSIFIED/RETIRED as necessary work**, due weighted table visits (restricted model). M2 virtual normalization evades FLMV even when structural mass small: **FALSIFIED for the specified hypothetical universal contract**, not all deciders. M3 new cyclic parity post-acquisition lower bound: **DUPLICATE/REJECTED** by prior exact LOCALPARITY1 and latest Role4 BLOCK-CLOSED-ORACLE85 with paid direct parity scan. The model fails to universalize because arbitrary algorithms can change representation or decide directly.

## Independent peers integrated
Role 2: original SELECTOR-SPLIT119 gives exact source-preserving affine+bijunctive encoding and separately satisfiable small children; compatibility remains NP-complete. SCC-ODD-ORBIT120 is a positive polynomial restricted algorithm for 2-CNF plus one global parity, independent audit pending. Do not infer all-input ARC. 
Role 3: PIN_PROFILE_JOIN_FIREWALL89 and inherited context/source-probe results show anonymous local profiles can lose SAT label; named shared identity must be restored.
Role 4: BLOCK-CLOSED-ORACLE85 exhibits connected XOR cycle with parity-even SAT, odd UNSAT, same strict-subset SAT and block-closed counts, but linear source-aware exact decision; do not republish as new or claim hard post-read gluing.
Role 5: NAMED_PROFILE_IDENTITY125 reconstructs ordinary formula from named truth profiles; two-level local pin recursion is information-idempotent, hence names restore original CSP join. RESOURCE-SCHEDULE-BRIDGE provides conditional same-machine schedule simulation, not universal SAT speedup. Existential cofinal endpoint is a separation-equivalent sufficient arrow, not proven closure.

## Archive, exact sources and coverage type
**FULL connector content reads:** AGENTS.md blob c5265db..., CODEX.md 754999..., .codex/skills/pnp-research/SKILL.md b8df83a..., root main.tex initial SHA 3d9a493a..., main13.tex SHA 87dbaad5..., LSPV-1 previous VIRTUAL-FRONTIER-FENCE124 SHA 3edd3e..., old LOCALPARITY1 053cc4..., old LB-0022, latest LSPV-1 ADAPTIVE-LOCAL-DEPTH126 handoff ec0cfa..., LSPV-2 SELECTOR-SPLIT119 66a633... and SCC-ODD-ORBIT120 fb8256..., LSPV-4 BLOCK-CLOSED-ORACLE85 handoff 562b35..., LSPV-5 NAMED_PROFILE_IDENTITY125 a305dee... and RESOURCE_SCHEDULE_BRIDGE 127499....
**FULL Drive text** of original ARC precursor Google Doc https://docs.google.com/document/d/1QirzuNPCG-CrE3EX6WweqsPdDbtoblCDEE4YI0HGyC0 . 
**BOUNDed searches / NOT EXHAUSTIVE:** GitHub searches weighted frontier sum, virtual stream width, HEREDITARY-SCOPED10, local cycle parity, Tseitin and named profiles; Google Drive title searches HEREDITARY and SCOPED yielded continuity/related files, but full original generator not located. Library semantic search for generator returned reports/PDFs and no exact code. The SCOPED Drive search had a provider continuation token and was **not exhausted**; no global absence inference.
**INHERITED ONLY:** pinned 55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640, 3,532 files hash/keyword-crawled; this does not imply every original theorem body was mathematically reviewed. Repo current tree beyond bounded searches, full older revision history, archived Google Drive LOG/BOOL/SIL/PROVED_EXACT, and original HEREDITARY-SCOPED10 program remain unread.
**Primary literature:** Fortnow et al JACM 2005 Theorem 3.1/Corollary 5.8 original author-hosted PDF and 2000 DIMACS source; Arnborg--Corneil--Proskurowski 1987 standard bounded-width context. The new mass formula is elementary schedule accounting, not a novel global complexity lower bound.

## Canonical gap IDs and next necessary implication
- ARC-EP-90 **FILLED KNOWN THEOREM:** original FLMV indexed-read-only-input forbidden endpoint. Retired universal product test t+s<2cos(pi/7).
- ARC-META-90 **FILLED abstract implication:** finite cofinal achievable-pair routes into a forbidden region would contradict P=NP. This is separation-equivalent in strength, not an independent contraction lemma.
- ARC-VIRTUAL-MASS127 **FILLED restricted conditional theorem, review pending:** exact stream DP upper bound by Psi and typed generator costs. No all-input normalizer constructed.
- ARC-PARENT-GLUE **OPEN:** extract a source-preserving SAT/UNSAT parent join with ordinary child semantics, including hard opposite-label minimal-UNSAT hostile pair.
- ARC-EDGE-90 **OPEN, highest priority:** from an arbitrary fixed uniform all-input exact SAT decider, establish existence of one jointly achievable better time/space pair (or cofinal finite route) reaching FLMV, allowing arbitrary state-adaptive representations, with all bit work and peak live workspace charged.
- ARCH-HEREDITARY-SCOPED10 **UNREAD / PROGRAM UNRECOVERED:** retrieve original complete code; continuity log only establishes restricted hereditary scoped-stream result. Its prior runtime paths are not presumed shared.

**Next falsifiable experiment:** two-level source-consistent virtual-child producer on MINIMAL-UNSAT-PROJECTION20 opposite-label pair and connected PIN89 U/V controls. Measure real serialized ordinary child bits, source reads, source identity, rule selection/switching, ancestor/live buffers, and Psi on full resulting event schedule. If source IDs discarded, the PIN89 counterexample applies. If retained, NAMED125 leaves original CSP join. Neither alone gives ARC-EDGE-90.

**Publication guards:** immutable timestamped role files; root LSPV-1 only, fresh current SHA, other agent regions untouched; no task creation or rescheduling. P versus NP OPEN.
