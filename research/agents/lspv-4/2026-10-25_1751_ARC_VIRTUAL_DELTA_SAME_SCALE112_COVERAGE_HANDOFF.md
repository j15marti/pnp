# ARC/FLMV five-role additive handoff: VIRTUAL-DELTA-SAME-SCALE112
Date: 2026-10-25 08:51 UTC (01:51 America/Los_Angeles, 17:51 Asia/Seoul).
Owner: LSPV-4. All five roles remain assigned ONLY to the ARC/FLMV simultaneous time-space spine. No scheduler or enabled-state modifications.

## New exact results, scoped
1. Fixed-slot ordinary 3CNF with indexed read-only root: assigning d variables of max occurrence Delta touches <= Delta*d clause records. A source scan plus deleted-ordinal and changed-record tables yield exact ordinary restriction bits with O(Delta*d*log N) live writable/index bits and O(Delta*d*polylog N) source/bit-access work for each query, after a charged O(N polylog N) scan. All child syntax, arity, zero padding, and SAT/UNSAT OR reconstruction are exact.
2. Crucial: the small descriptor is NOT the ordinary SAT guest input. That input has L>=N-(Delta*d)(2+3w). With M22 Delta=4 and d=2, L=N-O(log N)=Theta(N); four virtual grandchildren cannot justify exponent lambda=1/2.
3. Given a supplied A with joint ordinary-SAT exponents (t,s), the two-level virtual architecture has only generic exponent upper bounds max(1,t), s (plus subpolynomial terms). A padded guest A_D performing L^D actual steps on every input forces Omega(N^D) invocation cost on these leaves, disproving the proposed ARC bound for THIS architecture, not every existential route.
4. Different dummy forward/reverse source-read prefixes can be prepended to one fixed A with O(N polylog N) work and O(log N) space, preserving (t,s) for t>=1 while reversing access order. Trace order alone is not an invariant.

## Evidence
Report: research/agents/lspv-4/2026-10-25_1751_LSPV-4_ARC_VIRTUAL_DELTA_SAME_SCALE112.tex
Independent peer code: research/agents/lspv-4/2026-10-25_1751_ARC_VIRTUAL_DELTA_SAME_SCALE112_peer_repro.py (101 cases / 84,053 checks, finite).
Compact raw/checksums: research/agents/lspv-4/2026-10-25_1751_ARC_VIRTUAL_DELTA_SAME_SCALE112_raw.json.
Full locally reproduced Python test: 106 sources, 250,222 exact bit/SAT reconstruction assertions, zero failures, seed 1122026. SAT 73, UNSAT 32, large source structural 1. The 384-variable, 512-clause source had N=19,488 bits and an L=19,374 bit grandchild with 307-bit descriptor proxy. Python object memory is NOT measured FLMV writable space. Raw full JSON checksum SHA256=1bee0e7940b77194a8fdd8db0db52f438ec869cadd0f873b7f00814b38086681; full source code checksum SHA256=2e7cdb9972a0b78f8a3af041cef1cc32b302d952ab01eb3626673ddf2d405c7a.

## Preflight and original bodies
Read AGENTS.md, CODEX.md, pnp-research SKILL, current root main.tex blob f8b4c435, main13.tex, 2026-10-08_0032_LEAD_FINAL-LINK-ARC, EAGER-LAZY-FRONTIER34, MODELBRIDGE-0011, predecessor TRACE-SHANNON111, and LSPV-5 ARC-BRANCH-SELECTOR-TRILEMMA159 and Role 2 PADDED-GUEST-GATE157. Primary originals examined directly: Fortnow et al. original PDF Section 3, Theorem 3.1, Corollary 3.2, Corollary 5.8; Williams 2006 PDF opening model/scope. The prior 3,532-file keyword census was NOT repeated and limited fetches are NOT exhaustive archive review. Direct container Git clone failed DNS, so repository originals were accessed via GitHub connector instead.

## Rejection and coverage ledger
FILLED RESTRICTED: exact bounded-edit ordinary child bit accessor; syntax/semantic correctness; two-level virtual ancestor/descendant readback; source length bound.
CONDITIONAL: all-input same-exponent wrapper includes direct parent fallback on high-occurrence inputs, hence not an ARC edge.
FALSIFIED/RETIRED: call descriptor the short ordinary SAT query, treat raw trace order as difficulty invariant, treat two shallow M22 pins as a universal fractionally-short route.
OPEN: a proved all-input hereditary actual short ordinary instance family with all setup, discovery, source and unchanged writes, child generators, ancestor buffers, caches, failed routes and gluing fully charged in ONE FLMV realization.
UNREAD: detailed HEREDITARY-SCOPED10 generator and full source-version comparison with 2026-10-25 peer reports not present at this checkpoint.

## Concrete role handoff
Roles 1-3: any semantic compression candidate must output a TRUE fractionally shorter ordinary SAT input, rather than a short descriptor for a long virtual input; verify bad high-occurrence sources.
Role 5: independently check proof that a random-access virtual accessor has O(log N) bit space but leaves the guest's exponent multiplied by lambda=1; do not transport Cstar-only bounds to arbitrary ordinary SAT.
Role 4 next: seek a source-complete semantic quotient with exact short input and no parent-scale A call, or falsify one precise candidate.

The FLMV matched strict box remains t<241/200, s<11642479/23232400. A single fixed uniform exact total ordinary SAT machine must achieve both coordinates; ARC-EDGE-90 and P versus NP OPEN.
