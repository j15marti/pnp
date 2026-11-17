# SELMASK-SIGMA3-1 | 2026-11-18 07:03 KST
Circuit-SAT / Sigma2 / Sigma3. **P versus NP OPEN.**
**Status:** PROVED/EXACT scoped theorems; COMPUTATIONAL 20,950 checks, zero discrepancies; all-input uniform hereditary A -> Phi(A) OPEN. No independent external peer review.

## Mechanisms proposed
1. INDEX-PORT: logarithmic selector can expose q independently attainable Boolean port statuses.
2. MUX-SERIAL: parse a canonical explicit selector circuit, execute ordinary Circuit-SAT children serially and cache exact reachability.
3. MUX-CACHE: charge retained all-context status mask versus on-demand decisions.
4. SHARED-CORE: adversarial reconvergence, padding, solver delay, wrong quantifier ordering and guest/source readback.

## Project and primary sources checked
Read sigma-primary BLOWUP_BUDGET_1 and AUTOENC_SIGMA3_1, sigma-redteam SIGMA19_CLIQUE_PORT_FIREWALL, review/spines CONTRACTION_ACQUISITION1, and TMR-2's T5 CSP handoff. Literature: Fortnow--Lipton--van Melkebeek--Viglas, JACM 2005, Corollary 5.8 and §2.1 (https://lance.fortnow.com/papers/files/tst.pdf); Williams, STOC 2024 (https://doi.org/10.1145/3618260.3649723); Charwat--Woltran, FI 2019 (https://doi.org/10.3233/FI-2019-1810); Beyersdorff--Blinkhorn, TOCL 2020 (https://doi.org/10.1145/3355995).

## Definition
Let q>=1, selector b have w=ceil(log2(q+1)) bits, globally chosen outer bit g, and ordinary Boolean child circuits F_{g,i}(z) for i=1..q. Define M(g,b,z)=TRUE when b=0 or b>q, and M(g,b,z)=F_{g,b}(z) for 1<=b<=q. The final existential z genuinely depends on b. The anchored unquantified SAT answer is always YES (select b=0). For fixed g, let s_g be the q-bit status mask, bit i=1 iff SAT(F_{g,i}).

## Theorem A | sharp all-context mask
**PROVED/EXACT (source-free, port-only model).**
For fixed g: forall b exists z M(g,b,z) iff s_g=1^q.
With outer g: exists g forall b exists z M(g,b,z) iff s_0=1^q or s_1=1^q.
For every subset S of active selector indices, the port-only restricted existential query equals [s_g & S != 0], and the universal query equals [s_g & S = S]. Such port-only restrictions are closed under repeated subset intersection.

All 2^q status masks occur by setting F_{0,i}=TRUE or FALSE independently. All anchored sources have the SAME initial SAT answer. Therefore any fixed decoder, without later source access, that receives only a retained finite binary summary and answers all future equality contexts b=i needs at least q bits for some source (pigeonhole/INDEX). The q-bit mask is sufficient. This is not computational hardness: these branches are easy constants, a source-backed decoder may reread them, and a write-only stream can output q bits without retaining them as counted workspace. Restricting private z or changing a component is outside the hereditary port-only guarantee.

## Theorem B | explicit selector restricted contraction
**PROVED/EXACT conditional asymptotic upper bound; same-machine physical realization still requires audit.**
Assume P=NP and choose ANY fixed correct ordinary Circuit-SAT decider A with unknown K>=1,L:
T_A(m)<=m^(K+o(1)); S_A(m)<=m^(L+o(1)).
On canonical source-authenticated explicit mux circuits of length N, suppose q<=N^(1/2+o(1)), each F_{g,i} has encoded length <=N^(1/2+o(1)), and all child encodings can be streamed/materalized from the source with O(N polylog N) preprocessing/total emission. The uniform evaluator stores 2q status bits, emits one child to counted workspace, runs A, discards the child and guest state, and decides the correct Sigma3 prefix. Explicit buffer, input-index tapes, guest time/space, scans, syntax and encoding are charged:

T(N)<=N^(max(1,1/2+K/2)+o(1)),
S(N)<=N^(max(1/2,L/2)+o(1)).

For K>=1 the restricted time exponent is at least 1/10 below target max(11/10,3/5+K/2); space meets target. The general q=N^delta, child=N^(1-delta) *mask-retaining* ledger is T exponent max(1,delta+(1-delta)K), space exponent max(delta,1-delta,(1-delta)L). The latter upper-ledger matches max(1/2,L/2) uniformly over all L only at the balanced delta=1/2, for this implementation. Not an impossibility theorem for on-demand or compressed-source algorithms.

**Scope:** No source-to-canonical-mux compiler exists for arbitrary unpadded ordinary Circuit-SAT. Every F_{g,i} may be arbitrary and need not itself be mux-normal. The positive theorem does NOT establish an all-input recursively eligible transformer. Fallback A on rejected inputs leaves original K unchanged. Quantifier prefixes are preserved: g is globally committed and z adapts to b; uniquely determined gate traces supply no independent strategy speedup.

## Counterexamples and controls
- **Quantifier reorder:** q=2; F_{0,1}=[z=0], F_{0,2}=FALSE, F_{1,1}=FALSE, F_{1,2}=[z=0]. Then exists g forall b exists z M is FALSE, but forall b exists g,z M is TRUE, despite unique local witnesses.
- **Padding:** An m-length SAT core can be embedded inside N=m^(2+o(1)) mux source. The N-exponent bound does not create speedup on original m. A literal guest of length m can still charge m^K, and blindly calling m padded siblings can cost m^(K+1).
- **Reconvergence:** A shared parent-size DAG F connected to all selector branches is not q independent half-size children. Duplicated equal guests may be memoized; neither q forced calls nor cheap factorization is automatic.
- **Affine/constant shortcut:** The information bound survives easy sources and is not a SAT running-time lower bound.
- **Source access:** Any source-backed on-demand strategy or output-transfer method must be independently charged. FLMV Cor.5.8 applies to arbitrary SAT on its random-access TM, not this restricted promise language.

## Executed falsifiers and reproducibility
Two independent Python standard-library programs completed **20,950 assertions, zero discrepancies**. 900 random direct Sigma3 truth-table instances, 533 true / 367 false; exhaustive 256 selector masks q=8, 256 unique local response patterns; rational resource checks and explicit false positive on moving global g. Separately 120 genuine topological AND/OR/NOT gate DAGs, maximum 128 gates, were generated and exhaustively checked on every (g,b,z): 5,944 assertions. Direct QBF/matrix evaluator: 15,006 assertions.

Full proof report and self-contained executed scripts: local artifact `SIGMA_SELECTOR_MASK_20261118_0703KST_bundle.zip`. SHA256: REPORT.md 8ce3f723ddad883dc8273ee0614e160edd2108c7f8a63ebcacbdb879b5627f94; test_selector_mask.py c9735cc183aec979ed6e88ec2a1f28c15d38b09002ad5778b91dd22326a8460e; test_gate_mux.py 355fcf1adbe9a79d06c3df57f136f2d4a55029902e53131cde13749dafb63ac8.

## Handoff
Next load-bearing arrow: derive, or falsify, an actual near-linear-size ordinary Circuit-SAT -> source-authenticated, small-guest, globally coherent normal-form compiler for ALL inputs, with charged source/child-bit access, no mandatory parent-size A calls, retained mask/strategy memory, and hereditary closure on each ordinary generated child. Stress-test latent one-port UNSAT, K_k/NAE non-affine incidence, T5 CSP, pad/interpreter-A, reconvergence, affine and source replay. Do not edit other agents' manuscripts, trackers or schedules.
**P versus NP OPEN.**
FINAL_VERIFICATION_SENTINEL_SELMASK_SIGMA3_1_20261118_0703KST
