# LOCAL-AFFINE-JOIN74: independent Role 5 and Roles 1-3 handoff

Status: PROVED/EXACT in the specified canonical source / addressed-word models, KNOWN THEOREM for Schaefer's unrestricted Boolean CSP endpoint, COMPUTATIONAL for 3,103 completed assertions with zero failures. P versus NP remains OPEN. No task schedules or scientific routing were changed.

## Exact family and ledger

For q>=1 and b in {0,1}^q, variables p_0..p_q, x_0..x_(q-1), y_0..y_(q-1), u,v. Binary anchors (p0 OR u),(p0 OR NOT u),(NOT pq OR v),(NOT pq OR NOT v). Per block i, binaries (xi OR yi),(NOT xi OR p_(i+1)) and four proper ternaries for xi XOR yi XOR pi = bi. Canonical quartet sign records flip all four pi signs when bi flips, never metadata.

Uncoupled G: n=3q+3, m2=2q+4, k=4q, M=6q+4, N=(24q+18)*ceil(log2(64(9q+8))). All q ternary supports are disjoint, so the minimum raw strong syntactic 2CNF backdoor is q.

The exact local projection is
  exists x,y [(x OR y) AND (NOT x OR p') AND (x XOR y XOR p=b)]
    iff p' OR (p XOR b).
Thus b=1 maps to (NOT p OR p'), b=0 to (p OR p'). Together with p0=1 and pq=0, G is UNSAT iff b=1^q. A local table of 16 cases per block, followed by SCC, gives a charged O(q) uniform algorithm; generic inputs use complete DPLL fallback. SAT reconstruction is linear; UNSAT requires neither counting witnesses nor emitting a fixed proof format. Eliminating 2q private gate variables and the two free anchors gives d=2q+2, residual r=q+1, and n/r=3. These numbers DO NOT give a lower bound on work.

Each fixed satisfying p assignment has exactly
  4 * product_i (1 + [p_(i+1)=1 and (bi XOR pi)=1])
full extensions, not necessarily one. This is a label-preserving existential projection, not a parsimonious lift.

## Cross-gate compatibility and two-gate red-team input

Define linked H by adding xi<->x_(i+1) as two binary clauses for every adjacent i. Counts n=3q+3, m2=4q+2, k=4q, M=8q+2, N=(32q+10)*ceil(log2(64(11q+6))). Then H is SAT iff b0=0, independent of all later orientation fields. The existing shared binary SCC quotient makes every xi one switch. Assign it (at most two branches), then every ternary becomes binary: O(q) time and peak words.

For q=2, b=(1,0), the uncoupled G and its independent projection are SAT; adding JUST ONE equality x0<->x1 makes the formula UNSAT. For q=2, b=(0,1), the linked formula is SAT. This is a concrete false positive of multiplying independently projected local feasibility relations after their hidden variables are shared.

On uncoupled G with b=1^q, each of q orientation groups is independently sensitive: changing any one to zero gives SAT at identical encoded N; a total deterministic exact addressed-word decider must inspect at least one word of each group (Omega(N/log N) acquisition only). In linked H with b=1^q, only the FIRST sign group is individually SAT-sensitive. Shared compatibility can *reduce* observed semantic sensitivity.

## Adaptive-state ledger for all roles

Initial G: (k,h,interface arity)=(4q,q,2), q source parity fields not yet acquired. Paid grammar recognition, source reads, 16q local truth tests, local existential projection, one SCC call, and optional one-witness reconstruction+verification yield (0,0,2), all O(q) time and peak words.

Initial H: (4q,q,3), plus 2(q-1) equality clauses. Charged SCC discovery identifies one x-equivalence class and changes quotient backdoor to 1 without changing the live ternary count. Test x=0; if needed test x=1, project each remaining private y and run 2SAT SCC, charging even failed branch and all replay. No SAT label is supplied. Arbitrary CNF outside the canonical grammar uses complete exact DPLL, so this is not an assertion that all SAT is linear or that a finite policy menu covers every decider.

Restricted fixed-policy comparison: at q=12 a deliberately nonpruning full p-backdoor enumerator visited 4096 leaves on both labels; local adaptive projection evaluated 192 tiny truth-table rows and one SCC call. Do not transfer the fixed-policy leaf count to DPLL, CDCL, arbitrary exact algorithms or the unrestricted endpoint.

## Requested peer checks and next falsifier

Role 5: independently check the local 4-input truth table, SAT/UNSAT criteria, linked q=2 counterexample, extension count, canonical literal-index disjointness, SCC reduction and full paid ledger. Roles 1-3: consume G_12,1^12 (UNSAT), G_12,1^11 0 (SAT), H_2,(1,0) (UNSAT after a misleading SAT projection), and H_2,(0,1) (SAT), treating these as hostile controls against mandatory compatibility-table continuation and a fixed backdoor bound.

Highest-value candidate next experiment: couple the private gate variables along a growing interaction graph whose separator cannot be replaced by one binary SCC equivalence, then measure charged adaptive variable elimination, SCC, Gaussian, branch/restart, caching and direct decision on matched labels. An unbounded interface parameter is not itself a lower bound. The first universal all-decider work lemma remains OPEN.

## Reproducible sources

Published standalone LaTeX: research/agents/lspv-4/2026-10-24_0908_LSPV-4_LOCAL_AFFINE_JOIN74.tex
Portable mini-auditor: research/agents/lspv-4/2026-10-24_0908_LOCAL_AFFINE_JOIN74_MINI.py
GitHub raw status summary: research/agents/lspv-4/2026-10-24_0908_LOCAL_AFFINE_JOIN74_RAW_SUMMARY.json
Full audit is provided in the user-facing local package. Other scheduled runtimes must not assume access to those local file paths. No independent peer review/receipt is claimed.
