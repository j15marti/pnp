# LSPV-1/539: adaptive source-membership CEGAR precision bound

2026-11-09 09:41 PST | Route B | PROVED/RESTRICTED (mathematical source-query theorem), COMPUTATIONAL (finite replay). P versus NP OPEN.

Affected nodes: [P2-L1-539] refines [P2-L1-537] and [P2-C3]. Historical [P2-D1], full-calculus [P2-C3], worst-case mixed [P2-B1], same-R B3 [P2-B2] remain OPEN.

## IDEA, prediction, falsifiers

Candidate: an abstract proof-cost analyzer retaining only size and responses to fewer than h individual original-clause-membership probes cannot certify cost greater than seven Resolution inferences for an odd-charge cubic Tseitin source. F1: fewer than h probes can touch one missing local clause at every vertex (false by pigeonhole). F2: no four unqueried original clauses remain outside a selected vertex while retaining exact n,m,N (false). F3: the completed eight-signed-triple core has no authenticated seven-Resolution refutation (false by explicit certificate). F4: LSPV-1/537 already quantified every adaptive transcript (false: its single-collision theorem and seven-step core are prior work, but not this all-transcript adversary).

## SOURCE REVIEW AND DEPENDENCIES

Read the governing Nov 9 five-role abstract-interpretation refocus, both full root trackers, issue #3 including peer updates, AGENTS.md, CODEX.md, repo pnp-research SKILL.md, historical LSPV-2/341, LSPV-1/386, /537, /538, LSPV-3/536 and /537, LSPV-5/462 and /463, Grok Nov 9 progress and Claude Oct 28 world ledger. Repository content search queried clause membership query lower bound, source query adversary Tseitin, adaptive source membership. Earlier source acquisition and one-pair collision results exist; no identical all-adaptive-transcript theorem was identified in this targeted review, not a claim of outside novelty. Root main.tex nonempty content was recovered using its authenticated Git blob despite an empty contents-API response.

External repository files directly fetched: konard/p-vs-np README.md SHA 0e0ec77f83ad6eec1719a96066108b96ac1a95 and scripts/proof_status.json SHA 93b77ed3d8fe456f81c690035f45f07910a247f2, finite-machine results only; blkph0x/p-vs-np-proof-research METHOD_INDEX.md SHA 18d693ea71dfa433370eb7afbebc3106e32f03e5, restricted claims only; meelgroup/frat-xor format.md SHA 986a21aa92b62f844ef1fce852193142c41b2b1f, XOR checker formats; MassimoLauria/cnfgen/cnfgen/families/tseitin.py SHA 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab, parity-source generator; openai/math lean/docs/378.md SHA 223bbe187394bffca8a2c7ba1656538bfba26e3b, unrelated restricted subexponential algorithm statement. Primary: Urquhart 1987, Hard Examples for Resolution, JACM 34(1):209-219, DOI 10.1145/7531.8928, exponential lower bound only for ordinary DAG Resolution on selected expander Tseitin formulas; Atserias and Dalmau 2008, A Combinatorial Characterization of Resolution Width, JCSS 74:323-334. Methodology references Cousot and Cousot POPL 1977; Clarke et al. JACM 2003. No complete historical native grammar has been found, and no full external proof-checker execution is claimed.

## THEOREM 539.1: adaptive indistinguishability

Fix any finite simple cubic graph G with h even vertices, distinct three-edge neighborhoods, and any odd total charge. Its standard proper signed 3-CNF Tseitin source F has n=3h/2 edge variables, m=4h distinct width-three clauses, and is UNSAT. At each vertex v exactly four other proper signed triple clauses M_v are absent, and these M_v are pairwise disjoint across vertices.

For **every** set Q of fewer than h individual membership queries of the form "is this particular signed width-three clause present?", there exists an UNSAT proper signed 3-CNF E on the same original variables with exactly n variables, m clauses, identical original encoded length N under a fixed-width signed-literal encoding, and the same response to every q in Q, such that E has a source-authenticated seven-node ordinary binary Resolution refutation.

**Proof.** Since |Q|<h and the h sets M_v are disjoint, some v has Q intersect M_v empty. Of the 4(h-1) original clauses not at v, at least 4(h-1)-|Q|>=3(h-1)>=9 are unqueried. Delete any four and insert M_v. These four inserted clauses were absent in F and unqueried; the four deleted were present and unqueried. The exact member/nonmember oracle transcript stays unchanged, and m stays 4h. All original variables continue to appear: each edge originally appears in four clauses at each endpoint, eight in total, and at most four total clauses were deleted. At v, all eight possible signed triples now occur. Resolve four complementary pairs on the third variable to obtain four binary clauses; then resolve two pairs on the second variable to obtain x and not-x; the last Resolution derives the empty clause. This is seven distinct binary Resolution inferences with all eight leaves authenticated against E. The complete core makes E UNSAT.

For encoding, Elias-gamma encode the positive header n,m, and serialize every strict clause using one clause marker plus three signed identifiers of 1+ceil(log2(n+1)) bits each, including a sign bit. Any two such n-variable, m-clause width-three formulas have exactly

$$
N_h=\ell_\gamma(n)+\ell_\gamma(m)+4h[1+3(1+\lceil\log_2(n+1)\rceil)]=\Theta(h\log h).
$$

The source-signatures (n,m,N) match. Membership answers for any adaptive deterministic algorithm with fewer than h probes also match: run it on F, obtain Q, construct E afterwards, then induct on the identical sequence of answers. For randomized algorithms fix the random tape. The theorem is an adversarial pair per transcript, not one E working against every Q simultaneously.

## COROLLARY 539.2: source-parametric cost-sound abstraction obstruction

Let R be a sound proof calculus with free authenticated original source clauses and ordinary binary Resolution inference weight w_RES. Let a source-parametric may abstract transition system cover every legal source-authenticated shared refutation DAG with abstract transition cost no greater than concrete cost, preserve all legal goals, and depend on the source only through (UNSAT,n,m,N) and a chosen transcript Q of <h individual clause-membership answers. Theorem 539.1 gives an E sharing this initial abstract signature with F. Projecting E's complete seven-node Resolution proof through the cost-sound may relation yields

$$
d^\#(\alpha_Q(F),G^\#)\le 7w_{\rm RES}.
$$

Thus this restricted abstract analyzer cannot prove a strict lower bound above 7w_RES for F. Under **only the separately declared** exhaustive-at-most-binary-unit R_mix341 semantic calculus of historical LSPV-2/341, a simple bridgeless cubic F has W=4h-1>7. This demonstrates a true abstraction precision gap for that declared model. The authoritative accepted-byte full R_mix341 grammar remains unauthenticated. Neither this query-model bound nor Resolution hardness transfers to SAT machine runtime or a superpolynomial all-rule bound.

An h-query adversarial control querying one absent clause from every vertex blocks the completion **strategy** but does not show sufficiency of h probes to certify a positive bound. A full-source or feature-rich analyzer is outside the restricted information model.

## ITERATE: finite evidence and adversarial controls

Executed a fresh standard-library Python reproducer with seed 539. It tested K4 h4,n6,m16; triangular prism h6,n9,m24; cube h8,n12,m32; Petersen h10,n15,m40. Their odd-charge original model counts were all zero; even-charge controls have respectively 8,16,32,64 models. Each graph had 96 sampled membership transcripts of length <h. For K4 all

$$
\sum_{k=0}^{3}\binom{160}{k}=682801
$$

subsets were exhaustively checked for an available vertex and at least four removable unqueried original clauses. Independent JS checks separately enumerated these 682801 K4 sets plus 200 further prism/cube cases. An independently authored JS verifier replayed 12 exact source-authenticated seven-step Resolution proof witnesses, exact query responses, missing-leaf and wrong-pivot rejection; 76 grouped assertions PASS. The Python producer ran 1548 grouped assertions in 3.139 seconds and its process max RSS was 96912 KB. No historical R_mix341 checker, third-party Lean source, or native FLMV machine benchmark was run.

Local exact reproducibility files used in this run: lspv1_539_probe_collision.py (SHA256 23e650c554debfe6ae7862cee9d4ac4776d8d1a1a79756f2903ce2bf0279d038); verify_lspv1_539_independent.cjs (SHA256 ea671f469db48d92fbe2ffa96d8d78b550fd16e56d725c60134a854c1e628ce9); lspv1_539_probe_collision_raw.json (SHA256 471d0f7ea9cde494af06c3fe17f594ffb1f6bc84407ba194329f6200eeafbdee). GitHub test/control port in experiments/arc/lspv1_539_abstract_membership_check.cjs. Full local raw contains original clauses, sampled oracle transcripts and independent proof witnesses; GitHub compact JSON preserves checked totals.

## RESOURCE AND PROOF-STATUS LEDGER

(i) SOURCE-PROBE ABSTRACT ANALYZER: PROVED/RESTRICTED only, at least h membership probes required to evade this one completion attack; not a general bit-query lower bound. (ii) ALL LEGAL HISTORICAL R_mix341: P2-D1/P2-C3/P2-B1 OPEN. (iii) ANY SAT ALGORITHM and same-R B3: P2-B2 OPEN. Route A recursively iterable same-machine FLMV OPEN. W minimizes all legal branching/shared DAGs with free after-the-fact choice and pays distinct nodes once. No branching or sharing was needed for the cheap control, so the seven-node DAG is a valid upper-bound control whenever RES is permitted. Inference nodes 7, critical path 3, source eight leaves, evidence bits 7 records with O(log N) pointers plus N source bits; native construction, parsing, search, source reads, output, certificate checking and physical peak space are distinct additional resources. The 682801 subset test is analyst-side falsification, not paid logical proof work. No numerical machine-time bound follows from abstract path distance.

CORPUS REVIEW: verified previous /537 source collision and /538 side-read, /341 linear mixed shortcut, /536 cost partition, /462 paid history, /463 branch join and current /537 affine facet. DUPLICATION AUDIT: prior eight-clause seven-RES control reused, novel conditional quantifier is all adaptive transcripts <h. WHAT CHANGED RELATIVE TO ROOT MAIN: restricted source-query precision obstruction added, no historic status promotion. ADOPTED: exact-source provenance and cost nonexpansion. REJECTED: all-machine hardness inferred from information loss, and any invented new grammar. STALE CLAIMS: no existing theorem promoted.

Next native task: LSPV-3 authenticate complete exhaustive source dependencies, context/facet ownership and paid histories for RES, AND3, GF(2), LOCAL-CONVERT, DEF; LSPV-5 independently attack transcript model and source side reads, branch joins, free reuse; LSPV-1 seek a truly superlinear all-rule source-sensitive invariant and noncircular same-R B3. All five identities, schedules, historical weights and 2 Route A / 3 Route B allocation preserved. P versus NP OPEN.
