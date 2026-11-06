# LSPV-4/449: High-girth expander edge cuts have only constantly many gauge classes
**2026-11-06 13:36 PST | Route A primary | PROVED/RESTRICTED (graph-theoretic corollary) + COMPUTATIONAL | P versus NP OPEN**

## IDEA -> SEARCH -> ITERATE
Initial hypothesis: on a published Resolution-hard high-girth cubic expander family, the many UP-open branches counted by LSPV-4/447-448 might nevertheless collapse to a small set of valid gauge-equivalence classes under LSPV-2/452, even when all branching choices and sharing are permitted.

**Falsifiers:** (F1) a cyclic residual component can have fewer vertices than the original girth; (F2) edge expansion fails to charge the deleted cut edges surrounding a small residual component; (F3) no component larger than half the graph exists at the stated k threshold; (F4) an example with k<h*g admits two cyclic components, invalidating the strict one-orbit claim. The proof excludes F1-F4; cube at equality k=h*g=4 has b=2 and shows strictness matters.

**Search correction:** The initially attempted unannotated source-only logspace recognizer was **DUPLICATE**, not a new theorem: LSPV-2/441 and /442 already handle canonical and unordered/unannotated source, including variable renaming, and LSPV-4/423 already handles source-authenticated partial cofactor decision via Reingold. The initial 92-instance experiment is retained only as an independent control in the attached archive, not published as a new result. The research target was revised to the girth-expansion/gauge-orbit interaction below.

## Exact certified family and legal shortcuts
For a connected simple 3-regular graph G=(V,E) with H vertices, M=3H/2 edges, Boolean edge variables x_e and vertex charge chi_v, use the original four proper signed 3-CNF clauses at each v with a<b<c:
$$
C_{v,p,q}=\ell_p(x_a)\lor\ell_q(x_b)\lor\ell_{p\oplus q\oplus 1\oplus\chi_v}(x_c),\qquad p,q\in\{0,1\},\quad \ell_0(x)=x,\ \ell_1(x)=\neg x.
$$
This has 4H clauses and 12H signed literals; the fixed-width original-edge-ID packet has N=Theta(H log H) bits. Every connected source is SAT iff XOR_v chi_v=0. With odd charge on a growing cubic constant-edge-expander, ordinary **shared-DAG Resolution** has size 2^{Omega(H)} under Urquhart's published expander hypotheses; the Ben-Sasson-Wigderson width-size route is an additional ordinary Resolution control. This theorem **does not** transfer to Extended Resolution, full historical R_mix341, Res(XOR), or arbitrary SAT machines. GF(2) source parity, clause preprocessing, shared branch reasoning, and paid extensions remain legitimate shortcuts.

For existence of infinite degree-3 expanders with logarithmic girth use Morgenstern (1994), *Existence and Explicit Constructions of q+1 Regular Ramanujan Graphs for Every Prime Power q*, JCTB 62:44-62, taking q=2; note its hypotheses on the particular graph family. The Ramanujan eigenvalue bound gives a fixed positive edge-expansion constant by standard spectral Cheeger bounds. Detailed graph presentations/edge-label encodings and hard-instance certificates were not generated in this run; the theorem applies conditional on explicit family expansion and girth parameters. Finite controls below are not infinite-family hardness certificates.

## Theorem 449.1 (PROVED/RESTRICTED)
Let G be a connected simple cubic graph on H vertices, girth g, edge-expansion
$$
h=\min_{\varnothing\ne U\subseteq V,\ |U|\le H/2}\frac{|\delta_G(U)|}{|U|}>0.
$$
Delete an arbitrary set S of k original edges, with k<=H/2 and 2k<hH. Let b be the number of **cyclic** connected components of G-S. Then
$$
\boxed{1\le b\le 1+\frac{2k}{hg}.}
$$
If additionally k<hg, then **b=1**.

**Proof.** Since G has 3H/2 edges, after k<=H/2 deletions at least H edges remain, so G-S is not a forest and b>=1. If every residual component C had |C|<=H/2, its original boundary is contained in S. Edge expansion and double counting imply
$$
hH\le\sum_C|\delta_G(C)|\le 2k,
$$
contrary to 2k<hH. Hence there is a unique giant component C_0 with |C_0|>H/2. Every other cyclic component C contains a simple cycle and has at least g vertices. Its original edge boundary satisfies |delta_G(C)|>=h|C|>=hg, and every such boundary edge belongs to S. Summing the boundaries of all non-giant cyclic components charges each selected edge at most twice:
$$
(b-1)hg\le\sum_{\substack{C\ne C_0\\ C\ \mathrm{cyclic}}}|\delta_G(C)|\le 2k.
$$
For the strict corollary k<hg, no single non-giant cyclic component is possible because its boundary would require at least hg>k *distinct selected edges*. Thus all cyclic components are inside C_0, so b=1. QED.

## Corollary 449.2: the branch-count lower bound is not a distinct-work bound
LSPV-2/452, using the ordinary GF(2) incidence gauge relation on **original** cubic Tseitin cofactors, proves that all unit-propagation-open branches of a k-edge split form precisely 2^{b-1} equivalence classes under complementing unassigned edge variables. Combining with Theorem 449.1 yields
$$
\boxed{\#\text{gauge orbits}=2^{b-1}\le 2^{2k/(hg)}.}
$$
If k<hg there is exactly one orbit. This class count coexists with LSPV-4/447's lower bound 2^{ceil(k/3)} on **raw UP-open branches** and does not contradict that bound.

On an established cubic expander family with h>=h_0>0, g>=gamma log H, and original encoding N=Theta(H log H), setting k=ceil((3/5)log_2 N) gives **O(1) gauge orbits**, even though raw UP-open branches number at least N^{1/5-o(1)}. A connected odd-charge Tseitin source has no SAT cofactor, yet may have many UP-open branches. The global GF(2) test also decides it without branching. This is a *favorable sharing/shortcut control*, not superpolynomial work hardness, not a native proof-calculus cost bound, and not a same-machine SAT contraction.

## Exact computational checks
Python generated K4, cube, Petersen, and Heawood cubic graphs, independently enumerated every edge subset up to k=min(4,H/2), computed exact rational edge expansion by enumerating vertex subsets, computed girth by BFS, and checked the theorem for **10,304** subsets. It checked **9,809** strict one-orbit cases k<hg and **9,809** unique-giant cases 2k<hH. A separately implemented Node.js referee rebuilt all four graphs, independently recalculated girth/expansion/components, and reproduced all three counts. Exact finite h values: K4=2, cube=1, Petersen=1, Heawood=1; girths: 3,4,5,6 respectively. The cube has a four-edge cut separating two 4-cycles: at k=hg=4, b=2, demonstrating why the condition is strict. The Python program separately generated and authenticated eight complete original signed 3-CNF sources, with even/odd charges, using the existing /449 auxiliary source auditor. No asymptotic family or native FLMV trace is certified by these finite host tests.

The initial, explicitly **duplicate**, source-only recognition control exercised 92 signed 3-CNF packets: 26 accepted, 66 rejected, 138 Python assertions, 132 independent JS assertions. An erroneous negative test was found during construction: uniformly renaming an edge ID is a *valid* source isomorphism, not source corruption; the hostile control was repaired to change only one quartet. This is an affirmative shortcut-preservation test, not a discovery of a new hard family.

## Resource and transfer audit
* **Original-source acquisition:** binary-encoded 4H original signed clauses, their read/index/head costs; no free graph header, implicit promise or fabricated annotation. In the finite host tests entire graph is materialized, so reported Python/Node memory does NOT establish any FLMV peak-space bound.
* **Preprocessing:** the exact expansion/girth calculation in the finite enumerator uses exponential vertex-subset enumeration; it is an **offline theorem validation**, never part of a proposed SAT compiler. Operational algorithms need not compute h or g to use an authenticated gauge transformation.
* **Child discovery and generation:** no universally valid smaller ordinary CNF child was built. Syntax-only branch cofactors remain Theta(N) unless further reductions are authenticated; virtual ports and explicit children are distinct machine representations.
* **Sharing:** 2^{b-1} is a semantic count of gauge classes, NOT a count of original-source-authenticated native R_mix341 inference nodes or a physically free memoization scheme. Legal cross-branch reuse requires compatible assumptions and paid conversions, references, retrieval, storage, joins and any necessary replays.
* **Time and peak:** constructing gauge witnesses or checking membership via Reingold's L connectivity costs deterministic polynomial time of unspecified exponent and O(log N) abstract workspace on suitably specified read-only representations; compiling it onto the exact FLMV indexed machine with all costs and a local N^{11/10} bound is OPEN. Any opaque arbitrary SAT guest on a length-Theta(N) representative retains its charged running time and space. A compact orbit label does not magically shrink guest input.
* **Branch logic:** SAT parent is an OR over SAT child cases; refuting by a split requires BOTH UNSAT branches. This graph isomorphism does not add any discharge/weakening/split rule to historical R_mix341.

The Route A universal target
$$
t'\le\max(11/10,3/5+t/2),\qquad s'\le\max(1/2,s/2)
$$
for **EVERY** uniform total correct all-input SAT decider remains **OPEN**, including malformed encodings, recursive self-applicability, guest simulation, failed policies, source authentication, and all-phase simultaneous peak. Conditional exact FLMV arithmetic at (t,s)=(6/5,1/2): beta(6/5)=23/45, gap=1/90. Route B's full fixed mixed-calculus Wbar lower bound and noncircular B3 are **OPEN**. **P versus NP OPEN.**

## Actual searched artifacts and sources
* Project: governing Nov 2 handoff (blob c3889a3e), current issue #3 (including LSPV-2/452), AGENTS.md (19656af1), CODEX.md (754999f5), research skill (b8df83a7), LSPV-4/423, /444, /448; LSPV-2/441, /443, /452 and its current handoff. Initial /442 result already subsumed first idea, corrected.
* Actual Grok: `GROKPROOF/2026-11-02_0617_GROK_CONTRIBUTION.tex` (blob 319726c0, OPEN numerical transport). Actual Claude: `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex` (blob b7150bb9, distinct alternation-trading portfolio model).
* Required external repositories: `konard/p-vs-np/proofs/complexity/README.md` (7ee9a11e, one-tape finite-machine model, not FLMV), `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` (18d693ea, bounded and conditional techniques, no P/NP separation). Relevant code: `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` (4bb5fd19), `meelgroup/frat-xor/README.md` (38a137bc), `tanyongkiam/cake_lpr/README.md` (e94f45e9), `berkeley-abc/abc/README.md` (88a9d1a3), `openai/math/README.md` (cc5b0a03). These do not supply the missing uniform A->Phi(A) bridge. No Google-branded search or native FLMV runtime was used; indexed web searches and local Python/Node executions were used.
* Primary: Urquhart, *Hard Examples for Resolution*, JACM 1987 (DOI 10.1145/7531.8928); Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM 2001 (DOI 10.1145/375827.375835); Morgenstern, *Existence and Explicit Constructions of q+1 Regular Ramanujan Graphs for Every Prime Power q*, JCTB 1994 (DOI 10.1006/jctb.1994.1054); Reingold, *Undirected Connectivity in Log-Space*, JACM 2008 (DOI 10.1145/1391289.1391291); FLMV, *Time-Space Lower Bounds for Satisfiability*, JACM 2005 (DOI 10.1145/1101821.1101822).

**Actual advance:** a precise girth/expansion bound on *distinct* shared gauge classes of UP-open cofactors, incorporating the strongest known source-authenticated shortcut. **Verification:** complete restricted proof and two finite independent enumerations. **Remaining gap:** uniform fully charged ordinary-SAT child contraction; no universal lower bound is claimed.