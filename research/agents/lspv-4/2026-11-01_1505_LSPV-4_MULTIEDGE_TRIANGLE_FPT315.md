# LSPV-4 MULTIEDGE-TRIANGLE-FPT315
**2026-11-01 15:05 PST | Circuit Resource Auditor**

**PROVED/EXACT restricted source-labelled multigraph FPT packing lemma built on a KNOWN polynomial simple-graph algorithm; COMPUTATIONAL exhaustive independent controls; external mathematical review pending. All-input P versus NP OPEN.**

## Obstruction and falsifiers
The exact delta-zero saturated-cycle terminal needs original-clause-labelled edge-disjoint odd residual cycles. A valid Döcker duplicate-free proper monotone 3-SAT-(2,2) **original** has degree-four source incidence, yet its ordinary binary residual is a **multigraph**: distinct positive/negative clauses may leave equal endpoint pairs. The polynomial simple-graph packing theorem cannot simply be applied by erasing those copies. Candidate falsifiers were (F1) projection to one edge per pair preserves the optimal triangle certificate, **FALSIFIED**; (F2) source-labelled maximum packing always needs exponential computation, **FALSIFIED when multiedge excess d=O(log N)**; (F3) an individual pin can change the optimum-triangle delta by Omega(n), **FALSIFIED**; (F4) optimising triangle acquisition solves the all-input SAT controller, **NOT PROVED/INVALID inference**.

## Exact theorem A: bounded multiedge-excess FPT
For any valid canonical original F and coherent source-variable assignment p with no falsified original clause, construct the binary residual multigraph G: each uncovered width-two residual clause is an edge (u,v,j), where j is its unchanged original clause ID. Choose the smallest-ID representative for each unordered endpoint pair, and let E0 be the resulting **simple** edge set. Let X be the remaining original-clause edges, d=|X|. Let T_X be all source-ID triangles that touch at least one edge of X.

**Theorem:** `|T_X|<=4d` and the maximum number of original-ID edge-disjoint residual triangles can be found **exactly** in `2^(4d)poly(N)` time and polynomial writable space, using the existing polynomial simple-graph maximum edge-disjoint-triangle algorithm for degree <=4.

**Proof:** The canonical (2+,2-) quotas imply maximum residual degree 4, counting parallel edges. Each extra edge uv belongs to a parallel class of multiplicity >=2, so each endpoint has at most two other incident edges. A triangle through that extra edge requires a pair of those remaining incident edges with the same third endpoint, so there are at most 4 possibilities. Over all extra edges, |T_X|<=4d. Enumerate every subset Q of these at most 4d triangles and reject Q if two triangles share a source edge ID. Remove used representative edges from E0 and run the **known** polynomial maximum edge-disjoint triangle algorithm for simple maximum-degree-four graphs on the remainder, returning |Q|+nu_simple(E0 minus used representatives). Every labelled packing has a unique subset Q consisting of the packed triangles that touch X; its other packed triangles use only E0. Conversely every enumerated joined packing is valid. Taking the maximum yields the exact labelled optimum. Storing one subset, simple oracle, best certificate and provenance needs polynomial space. QED.

**Literature firewall:** McKay and Manlove, *Packing K_r's in bounded degree graphs*, Discrete Applied Mathematics **352** (2024), 20–32, https://arxiv.org/html/2209.03684v2, Theorem 5, incorporates the earlier Caprara-Rizzi polynomial EDK3 result for **simple** graphs at maximum degree 4. It does **not** automatically treat source-labelled multigraphs. This report's extension is a proved elementary parameterized reduction, not a claim to invent polynomial simple-graph triangle packing. The compact accompanying finite checker uses brute-force simple packing; it is **NOT** an implementation of the cited polynomial-time oracle.

## Exact theorem B: bounded local drift
Let nu*(p) be the **true maximum labelled triangle packing**, and delta*(p)=2f-u-eta-nu*(p) with source-covered minority signed counts eta. Upon one coherent original-variable pin that produces no falsified original clause, let r be the number of prior binary source edges incident on x and h_new the number of new binary edges created from ternary clauses. Then `-r <= nu*(child)-nu*(parent) <= h_new`, because deleting or adding one edge changes the maximum edge-disjoint packing by at most one; source quotas give r<=4, h_new<=2.

More sharply, if x is pinned TRUE, put s+=previously covered positive occurrences of x and s-=covered negative occurrences, a=2-s+ (# uncovered clauses newly covered), h=min(s+,s-), and z=change to minority-covered counts of other free variables. Then 0<=z<=2a and
`delta*(child)-delta*(parent)=-2+a+h-z-[nu*(child)-nu*(parent)]`.
Using r<=a+(2-s-) and h_new<=2-s- gives the **exact universal interval**
`-6 <= delta*(child)-delta*(parent) <= 4`.
Pin FALSE is sign symmetric. This bounds per-step change in the optimum-triangle certificate budget; it **does not** make delta monotonic or bound total branching work. It does not necessarily hold for arbitrarily reselected nonmaximum greedy certificates.

## Concrete valid F9 counterexample, original-source both labels
Take F9 positive triples (156),(238),(135),(469),(247),(789) and negative triples -(468),-(167),-(234),-(358),-(129),-(579), exactly two occurrences of each sign per original variable. For p={x1=1,x4=0,x5=1,x8=0}, binary edge IDs and endpoints are
`(1:2-3),(3:6-9),(4:2-7),(5:7-9),(7:6-7),(10:2-9),(11:7-9)`.
Original clauses 5 and 11 are distinct **opposite-polarity** parallel edges between 7 and 9. Least-ID projection picks 5, and its maximum simple triangle packing has size **1**. A valid source-ID packing `(3,7,11),(4,5,10)` has size **2**, is maximum and gives delta*=-1. Direct original-clause enumeration verifies UNSAT. Thus collapsing the two clauses is not valid even as a maximising packing shortcut, much less a semantic CNF simplification.

On the **same F9 original**, p_S={x1=0,x3=0,x5=1,x6=0,x7=0,x8=0} has **2** SAT extensions; p_U differs only in x1=1 and has **0**. Producer UP-DPLL checks require one node/48 literal probes and one node/46 probes respectively. Enumeration of the three free variables yields the full falsified-original-clause UNSAT leaf cover. Large nominal policy portfolios are not mandatory work on these easy cubes.

## Independent exhaustive experiments
A full self-contained producer and independent no-import checker in the local reproducibility archive tested ALL 19,683 F9 and 729 Y6 original-variable coherent cubes. The producer independently compared the decomposed optimum against direct exact packed-subset search and checked **70,197 F9** and **2,016 Y6** unfalsified single-pin transitions. The independent verifier checked the packed optimum with an independently written three-edge combination enumerator and brute subsets, passing **34,095 assertions**, including 376 SS/SU/US/UU original clause-pair extremes, all full-assignment complement identities, original model totals 70 F9 and 20 Y6, six malformed grammar rejects and same-source SAT/UNSAT leaves.

| Original | cubes | non-falsified cubes | cubes with d>0 | max d | nu*>0 cubes | observed delta* drift |
|--|--:|--:|--:|--:|--:|--|
| F9 | 19,683 | 12,683 | 1,535 | 2 | 556 | -5 to +2 |
| Y6 | 729 | 545 | 77 | 2 | 4 | -4 to +1 |

Source-labelled triangle multiplicity is real: 3 F9 cubes have an optimum strictly greater than the least-ID simple projection. These finite tests do not imply all-input hardness or the polynomial oracle's runtime.

## Charged native-machine recurrence and strict numerical firewall
The actual all-input controller's total work must charge grammar/headers, source bits, index/address tape writes and erasure, head moves, paired-endpoint sorting, triangle discovery, **every one of the 2^(4d) failed/accepted Q attempts**, simple packing oracle, GF(2)/matroid proof arithmetic, proof readback, cache/replay, policy selection/switching, child output/access and guest DELAY/COPY/RECOMP. Peak space is the maximum **simultaneously live** ancestor/cache/selector/proof/oracle/index/head/output/guest state. For every state z:
`W(z) <= C_grammar+source+index+head(z)+sum_attempted C_policy+failed(z)+C_GF2+proof+cache(z)+C_triangle(z)+sum_evaluatedChildren(C_encode+access+guest(z,y)+W(y))`.
The exact triangle stage has the parameterized bound above, but the inherited delta-zero affine terminal still may enumerate `3^nu` branch systems, and Shannon fallback may cost `2^n poly(N)`. This is not an all-input polynomial bound.

Neither the published simple-graph oracle nor the finite Python experiments prove a native FLMV indexed random-access SAT decider with time exponent 6/5 and peak writable-space exponent 1/2. In particular an adjacency representation may require Omega(E log N) bits. The exact prior FLMV comparison points d*(6/5)=23/45 and d*(241/200)=11642479/23232400 remain model-specific. Hypothetical locally addressable target reductions need `(6/5)b+rho<241/200`, `b/2<11642479/23232400` and separately charged setup/space. LSPV-4 FIXED-TILE-PORT-CONGRUENCE314 provides a **pure** 131-slot tile and a port congruence obstruction; it did not authenticate all mixed gadgets or the upstream arbitrary SAT-to-signed-(2,2) bit-local normaliser. NP-completeness alone cannot supply the numeric bridge. No arbitrary unknown-exponent A->Phi(A) universal hereditary contraction has been proved.

## Corpus, literature and GitHub duplication checks
Read first the 01:48 integrated handoff and 01:44 exact delta-zero report, then current AGENTS/CODEX/pnp-research skill, root full 1.1-MB authenticated Git blob, issue #3, LSPV-2 LINEAR-TRIANGLE-ACQUISITION302 (bounded neighbor enumeration, already known), latest LSPV-4 FIXED-TILE314 and ORDER313, LSPV-5 LOGSPACE-ANONYMOUS-CYCLE274 and LSPV-3 GATE312. Project GitHub queries: `maximum edge disjoint triangle packing`, `edge-disjoint triangles delta 4`, `maximum triangle`, `greedy triangle selection`. Separate github.com/openai query: `triangle packing` located general triangle-removal material but no applicable authenticated residual-M22 implementation; absence proves no novelty. Primary web/Google: `maximum edge disjoint triangles packing NP hard bounded degree`, `McKay Manlove 2024 edge-disjoint triangle simple max degree 4`, `SAT time space indexed input FLMV Theorem 5.7`. Main sources: McKay-Manlove 2024 DOI 10.1016/j.dam.2024.03.010; Chapuy et al. *Packing Triangles in Weighted Graphs*, DOI 10.1137/100803869; Döcker arXiv:1912.08032; FLMV JACM 52 (2005) DOI 10.1145/1101821.1101822. No local checkout for repository preflight; independent stand-alone scripts and remote GitHub readback substituted.

**P versus NP OPEN. No new task IDs, schedule, enabled-state or research-priority alterations.**
END_OF_VERIFIED_REPORT::LSPV4::MULTIEDGE_TRIANGLE_FPT315::P_VS_NP_OPEN
