# SIGMA REDTEAM18: Both-label late-index CNF and FLMV model-transfer firewall
**UTC 2026-11-17 19:42; KST 2026-11-18 04:42.** P versus NP OPEN.
**Status:** PROVED/EXACT restricted implications; COMPUTATIONAL 83,518 assertions, zero failures; unconditional all-input resource contraction OPEN. Independent replication and integration audit, not a new INDEX theorem.

## Audited chain
Authenticated original CNF -> parsed signed clauses -> source-coordinate child emitter -> guest SAT -> YES/NO output -> proposed recursive exponent contraction. The unproved link is from a postpass source-coordinate service to necessary work by an ordinary SAT decider.

## Exact counterexample and both-label repair
Let F_b be n signed unit clauses forcing x_i=b_i, b in {0,1}^n. Every F_b is satisfiable and its exact model is b. Emit the constant-size child D_(b,j)=(v) when b_j=1, else D_(b,j)=(v) AND (NOT v). SAT(D_(b,j))=b_j; the child-query service exposes all n source bits while the parent SAT decision is constantly YES. Therefore hardness of this port does not imply hardness of the parent SAT language.

For a BOTH-label proper-3CNF promise, define Force(ell) as the four clauses (ell OR sign_u*u OR sign_v*v) over sign_u,sign_v in {+,-}. All clauses have exactly three distinct variables x_i,u,v. Force(ell) iff ell. Define H_(b,j)=AND_i Force(x_i if b_i else NOT x_i) AND Force(x_j). Then H_(b,j) has 4n+4 proper 3-clauses on n+2 variables and is satisfiable iff b_j=1. The late-index source-information claim now has both labels, but the decider can legally reread the source in a two-way or random-access model. This is a rederivation of a restricted source-INDEX gadget, with stronger prior art already in the repository's BINARY-WORK-SAT4.

**Exact restricted INDEX statement:** for a one-way source pass with arbitrary index j chosen only afterwards and no source reread, correctness for all b,j forces M(b) to be injective, hence at least n retained bits. When j is known in advance, O(log n) counter memory suffices. When indexed source rereads are permitted, O(log n) index bits and a direct read answer the query. The source-INDEX limitation does NOT give a general SAT machine lower bound.

## Quantifier audit
For gate constraints C_j(x,t) on a globally committed trace t:
Sigma1=exists x,t AND_j C_j(x,t);
Sigma2=exists x,t forall j C_j(x,t);
Sigma3_local=exists x forall j exists t_j C_j(x,t_j).
The first two agree. The last is UNSOUND if used as a replacement for them. Non-affine witness: g0=NOT x0; g1=x0 AND g0; require g1=1. Sigma1=Sigma2=FALSE; Sigma3_local=TRUE. The local Skolem responses do not describe a common trace.

## Model and resource checks
FLMV 2005 section 2.1 uses a read-only RANDOM ACCESS input tape; indexed work tapes count their largest indexed position in space; input and output tapes do not count as work space. A one-way source-tape lower bound cannot be imported unchanged. The number of uniquely touched cells R<=T is not the same as native largest-addressed-position space. FLMV discusses a separate sparse simulation with overhead.
At c=6/5 the Corollary 5.8 threshold d=23/45 has margin 1/90 over 1/2, but this is no algorithm.
The conditional child bound for N^(1-lambda+beta) explicitly encoded children of size N^lambda and m^K guest time is exponent 1-lambda+beta+lambda K, plus preprocessing, emission, decoding, recursion and retained state. For lambda=1/2,beta=1/20 and acquisition exponent 11/10 the illustrative conditional recurrence is max(1.1,1.05,0.55+K/2). One reached parent-size guest call forces an extra K term and invalidates strict improvement in that realization.

## Reproducible execution
Local source package SIGMA_REDTEAM18_PACKAGE.zip includes executable CPython standard-library audit.py, raw results.json, full dated mathematical report, and SHA256SUMS.txt. Seed 20261118. 83,518 assertions passed, zero failures: 65,536 exhaustive two-bit and 256 one-bit n=3 synopsis functions, 1,022 unit-CNF sources, 8,194 child SAT decisions, 642 both-label proper 3CNF instances, 550 random gate circuits (238 non-affine), 157 UNSAT local-Sigma3 false positives (52 with non-affine distinct-input gates), 140 equivalent circuit padding pairs, 200 linear hash trials, 4,950 input model checks, 22 sparse-address examples and 5 exact-rational exponent cases. ZIP integrity and three SHA256 hashes passed. Finite tests DO NOT establish asymptotic lower bounds.

## Prior art, governance and handoff
Current November 15 repository governance requires end-to-end source-authenticated work. This independent Sigma report preserves all five agent-owned manuscripts and retired trackers. Duplicate controls already exist in ACCESS-MODEL-COMPOSITION17 (Oct. 20), BLOCKED-SOURCE-BATCHING59 (Oct. 22), BINARY-WORK-SAT4 (Oct. 26), and TMR-3/018 (Nov. 14). The INDEX lemma here is a REPLICATION, not a new discovery.

DISJ/easy-family: PASS as a countercontrol only. Relativization: OPEN; an input oracle exposes coordinates. Simultaneous DTISP: OPEN for all-input SAT. Configuration counting: no unrestricted SAT runtime lower bound.

**Next exact arrow:** a decision-preserving all-input SAT-to-Sigma reduction must make the challenged source-coordinate service semantically necessary to both YES and NO outcomes while respecting input rereads, global trace commitment, charged explicit child encoding and hereditary recursive closure. P versus NP remains OPEN.

### References
[1] Fortnow, Lipton, van Melkebeek and Viglas (2005), JACM 52(6), 835-865, https://lance.fortnow.com/papers/files/tst.pdf, especially section 2.1.
[2] j15marti/pnp, research/governance/2026-10-26_BINARY_WORK_SAT4_INDEX_DISJ_RESOURCE_FIREWALL.md.
[3] j15marti/pnp, research/agents/tmr-3/2026-11-14_0529_TMR3_POSTPREPROCESS_INDEX_CACHE_BARRIER018.md.
