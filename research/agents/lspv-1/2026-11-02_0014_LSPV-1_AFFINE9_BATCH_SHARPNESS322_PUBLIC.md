# LSPV-1 AFFINE9-BATCH-SHARPNESS322
**2026-11-02 00:14 PST | Formal Proof Lead. PROVED/EXACT scoped corollary, COMPUTATIONAL independently checked. P versus NP OPEN.**

## Exact obstruction and falsifiers
The preceding LSPV-1 SOURCE-DISJOINT-BATCH-PROJECTION321 obtains a source-clause-disjoint pivot set of size at least n/9 and a valid existential residual with at most m clauses, width <=4 and literal records <=3m+4|I|. Does a cleverer independent-pivot selector guarantee *more* than n/9, or at least one strict clause/literal decrease? Both claims are FALSE for a specific infinite canonical family. This is a restricted local projection result, not an unrestricted decision lower bound.

Four falsifiers: (1) universal independent-pivot density >1/9, false; (2) universal source-independent DP literal-count descent, false; (3) local projection inflation entails expensive SAT decision, false; (4) equal Boolean cofactor SAT labels or exact model counts imply continuation equivalence, false.

## Canonical affine-plane source and formal theorem
Use the affine plane AG(2,3), with nine points (r,c) and the twelve three-point lines in the four directions (0,1),(1,0),(1,1),(1,2). Sign the first two parallel classes positive and the last two negative. This gives valid canonical **B**:
```
Positive: (123) (456) (789) (147) (258) (369)
Negative: -(159) -(267) -(348) -(168) -(249) -(357)
```
Every variable appears precisely twice per sign, every clause is a distinct proper width-three same-sign clause, and every pair of variables occurs together in exactly one source clause. The primal graph is K9. The affine plane and one-pivot 4-resolvent theorem were already used in LSPV-2 AFFINE-LIFT-BVE229, and are *not* claimed novel.

For t>=1 let B_t be t variable-disjoint renamed copies of B. Then n=9t, m=12t and alpha(primal(B_t))=t. Every maximal original-source primal independent set I therefore has exactly t=n/9 pivots. For every such I, simultaneous source-clause-disjoint exact Davis-Putnam elimination yields a noncanonical G_I with **exactly 12t clauses, 40t literal records, max clause width four**, and
```
forall surviving z: G_I(z) = OR_{b in {0,1}^I} B_t(z,b).
```
This is a continuation-exact identity on the surviving names, not a hereditary canonical successor. In particular, the general upper bounds m_G<=m, L_G<=3m+4|I| and |I|>=n/9 are **jointly tight** for this declared first-stage policy.

**Proof.** Each of the t primal components is K9, so an independent set chooses at most one point per component, and maximality chooses one each. Every selected point x lies in two positive and two negative source lines whose eight other variable names are all distinct (unique pair-on-line property). Its positive remainders A1,A2 and negative remainders B1,B2 satisfy
```
exists x F(x,z) = F_away(z) AND ((A1 AND A2) OR (B1 AND B2))
                  = F_away(z) AND AND_{i,j in {1,2}}(Ai OR Bj).
```
The four resolvents are distinct mixed-sign four-literal clauses, without tautologies or duplicates, and cannot be subsumed by untouched monotone source ternaries. Each pivot replaces four ternaries with four quaternaries, increasing literal occurrences by exactly four. Disjoint batches commute. QED.

In an explicitly declared fixed-width grammar using gamma n,m headers, source body (12t)(1+3w) and child body (12t)+40t(1+w') signed-literal fields, for t=2^k both w=w'=k+4 and both header lengths match. Child-minus-source **bit length is exactly 4tw+40t>0**. This is an encoding-specific *output expansion*, not a lower bound on the minimum equivalent circuit or on SAT decision work.

## Exact same-original CNF versus Circuit-SAT and reverse Shannon
The canonical source-private fan-in-two OR-of-three AND-of-m clauses evaluator has 3m-1 gates, thus B uses 35 and B_t uses 36t-1. Its signed unordered input pairs never repeat, so the previously defined restricted same-pair reuse architecture saves zero gates; other architectures (matching/global factoring) remain permitted and may be smaller. No unrestricted gate minimum or SAT decision lower bound follows.

Exhaustive source enumeration gives #SAT(B)=18 and #SAT(B_t)=18^t. For pivot x1, both cofactors have exactly 9 satisfying assignments, but their (f0,f1) table on the remaining 8 names has (0,0):239, (1,0):8, (0,1):8, (1,1):1. Equal current SAT labels and equal counts do not establish continuation equivalence. On the very same original B, pins (x1,x2,x3,x4)=(1,1,1,0) leave **2 SAT extensions**, versus (0,1,1,0) **0**. No original clause is initially empty. The UNSAT pins give source units C4->x7=1, C8->x6=0, C12->x5=0, contradicting positive C2=(x4 OR x5 OR x6). An independent 32-leaf original-clause falsification cover checks all remaining assignments. Unit-first DPLL host implementation: SAT 2 nodes/96 literal inspections; UNSAT 1 node/52 inspections, not native FLMV timings.

An exact template-and-grammar recognizer can decide the entire ordered B_t family in polynomial work without recovering assignments, with exhaustive fallback on nonmembers and malformed rejection. Thus simultaneous sharpness of independent-batch projection and literal expansion **does not** imply generalized necessary decision hardness.

## All-input quantifiers and full charges
For one fixed source-authenticated algorithm, local executed work is
```
W_D(F)=C_grammar+source/index/head+C_primal+selector+failed/switch
      +C_resolution/child/output/provenance+proof/GE/cache/replay/guest
      +sum_{actually tested z} C_evaluate(G,z).
```
The one-phase fully paid exhaustive continuation has W_D<=P(N)2^(n-|I|)<=P(N)2^(8n/9), and polynomial simultaneous peak writable/index/ancestor/guest space for an explicit G, with a fixed polynomial P. This is exponential total work and not an ARC/FLMV native time-space result. The original clause count does not decrease, and the derived width-four G is noncanonical, so the original n/9 argument cannot be recycled freely. Earlier LSPV-2 M22-LOWSPACE-DP-BATCH152 separately gives a two-round noncanonical projection theorem and must be credited.

No representation-independent universal lower bound for *every* correct decider A has been established; a correct A need never use this pivot selection. No all-input polynomial-time exact controller, unknown-exponent arbitrary-A -> Phi(A) power-short compiler, or strict same-machine numerical FLMV transport is known. P versus NP remains OPEN.

## Verification
A fresh source algebra producer and independent no-import checker passed **335,348 assertions**, including exact SAT/Circuit-SAT truth tables, full 512 assignments on B, 65,792 surviving-assignment projection comparisons on B_1 and B_2, exhaustive 2^18 independence checks on B_2, 264 original SS/SU/US/UU pair modes on B and 264 on F9, 6,144 complement identities, the 32-leaf UNSAT cover, 156 single-bit binary source payload mutations, 10 malformed strings, historical F9 70 and Y6 20 model checks. Constructed and checked t=1,2,3,4,8. U198/V198 certificates are inherited, not freshly rerun. Logical XOR is OFFLINE only, not an internal oracle.

**Preflight / prior art:** verified five-role 19:50 forward-reverse directive, older decision-only/integrated five-role directives, source 321, LSPV-2 152 and 229, AGENTS/CODEX/repo skill, current issue #3. Web searches: affine plane STS(9), variable elimination SAT, Döcker 2019; project GitHub queries 'Steiner', 'affine plane', 'K9 primal', 'independent set sharp'. github.com/openai 'Steiner triple system SAT variable elimination': no relevant indexed result (not evidence of novelty).

**References:** [1] Döcker (2019), arXiv:1912.08032. [2] Eén/Biere, SAT 2005, DOI:10.1007/11499107_5. [3] Wolfram MathWorld, Steiner System, https://mathworld.wolfram.com/SteinerSystem.html. [4] j15marti/pnp LSPV-2 AFFINE-LIFT-BVE229 (2026-10-29). [5] j15marti/pnp LSPV-2 M22-LOWSPACE-DP-BATCH152 (2026-10-25). [6] Fortnow et al., JACM 2005, DOI:10.1145/1101821.1101822.

**Report limitations:** restricted elementary theorem; external referee pending; root only inside LSPV-1 ownership; no agent schedule/identity/status changed.

END_OF_VERIFIED_REPORT::LSPV-1::AFFINE9_BATCH_SHARPNESS322::P_VS_NP_OPEN
