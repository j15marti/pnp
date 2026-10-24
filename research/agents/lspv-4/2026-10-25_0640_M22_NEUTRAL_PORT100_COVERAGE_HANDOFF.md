# LSPV-4 M22-NEUTRAL-PORT100 | 25 October 2026 06:40 KST

**Status:** PROVED/EXACT for add-only original-clause deletion and neutral M22 type repair. COMPUTATIONAL finite verification. Independent mathematical review pending. Ordinary-SAT ARC-EDGE-90 and direct post-acquisition lower-bound arrows OPEN. P versus NP OPEN.

## Canonical target
C_M22: unique proper three-variable OR clauses, each wholly positive or negative, each active variable exactly two positive and two negative appearances. bar(C) reverses signs but keeps OR. C_star excludes fully complement-paired formulas only. Partial pairs, disconnected and easy cases are permitted. L_star is satisfying C_star encodings, rejects malformed. k=active variables, m=4k/3, N=Theta(k log(k+2)). NP-completeness is Döcker's original theorem plus canonical Y anchor, not an unconditional time lower bound.

## Three falsifiable proposals and exact result
H1 (no neutral fresh-variable type restorer) FALSIFIED: the nine-clause, six-fresh-variable port gadget G+ exists. For a deleted positive clause (x,y,z), introduce fresh a,b,c,d,e,f; positive clauses (a,y,z),(x,b,c),(a,d,e),(b,d,f),(c,e,f), negative clauses (-a,-b,-d),(-a,-c,-f),(-b,-c,-e),(-d,-e,-f). For a negative deleted clause reverse all signs. Every old port assignment extends. Positive extension multiplicities for 000..111: 6,16,16,16,10,23,23,23; explicit witnesses in LaTeX report.

H2 (independent variable-by-variable repair) FALSIFIED by mod-three charge: within each connected component of the **newly added** clause-variable graph, sum over old-variable signed deficits is 0 mod 3. Deleting one positive or negative source clause leaves three deficits of charge +1 or -1; all three must meet in one new repair component. No isolated 1- or 2-port completion exists in the specified add-only model.

SHARP FLOOR: For a one-clause deletion and unchanged other original clauses, if h auxiliary names and p,q newly added positive/negative clauses restore the exact signed quotas, 3p=3+2h and 3q=2h. Thus h=3u, (p,q)=(1+2u,2u). u=0 only reintroduces the deleted original clause. u=1 forces two duplicate negative triples on the same three auxiliary variables, forbidden. Therefore genuine fresh repairs need h>=6 and p+q>=9. The exhibited G+ achieves both. This is NOT a global optimum for batch repairs that share auxiliaries.

H3 (type restoration implies fractional-size shrinkage) FALSIFIED for this add-only compiler. For d>=1 deleted original clauses, independent gadget copies create (k',m')=(k+6d,m+8d), with exact equivalence SAT(repaired child)=SAT(original with these clauses removed) and final grammar C_star. Indexed length obeys
N'-N=3(m+1)(w'-w)+24d(w'+1)>0,
where w=ceil(log2(k+1)), w'=ceil(log2(k+6d+1)). For 1<=d<=m, N'=Theta(N), never N^(lambda+o(1)) with lambda<1. Two distinct original-clause deletions compose exactly over two levels with k''=k+12, m''=m+16 but do not reconstruct SAT of the original parent.

## SAT and UNSAT controls, bit-resource ledger
A standard-library full local auditor ran 1,384 assertion-accounted checks, all passing: Y 20 models; fully paired H 18; exhaustive 12-variable model counts for all 16 single deletions; 56 two-level ordered Y deletions; two full 18-variable enumerations; all 255 nonempty Y deletion masks. GitHub's original Döcker U blob f9dda41a810ad8e02bd553f2711a26a4050861f9 was separately checked through the connector: 198 active variables, 264 clauses, proper unique monotone, sign quotas satisfied. UNSAT(U) is IMPORTED from published primary source. U disjoint union Y is an UNSAT control; deleting clauses only from Y leaves U and the UNSAT conclusion unchanged. No claim to re-enumerate 2^198 assignments.

For one deleted clause and charged index: stream O(N polylog N) elementary bit work and O(log N) controller bits; explicitly storing ordinary output requires Theta(N') live writable bits and Omega(N') output writes. Source reads, unchanged writes, address/control, selector discovery, switches, failed attempts, replay, caches and ancestor buffers are charged. Actual flips, cumulative bit-time, gates/wires/switches, program/representation size are separate and not measured. Any multi-delete selector must pay for its representation and selection. For a single fixed total uniform adaptive A, retain T_A(F)=C_A(F,R)+T_finish,A(F,R) and peak simultaneous space. No independent exhaustive residual list is used, so R_search is not set. Neither larger search-state count nor the gadget's representation cost implies mandatory SAT decision time.

## Corpus manifest, originals and duplication
READ directly: AGENTS.md (c5265db), CODEX.md (754999f), research skill (b8df83a), main13.tex, root main ownership conventions, Lead FINAL-LINK-ARC, LSPV-4 original PC22_ALLFIELD1 (0aa4113), CP22LIFT1 handoff (15a8b74), COMPONENT-CLOSURE97, CP22-GAUGE-FIREWALL98 (be78fff), TRANSPARENT99 (24ef2fe), Role1 M22-BALANCED-SMALL139 (b6ced21), Role3 MAXDEFECT-FACTOR101 (e334000), Role5 ENFORCER-PORT-FIREWALL139 (0ee08e3), and original U (f9dda41). Predecessor Role3 report sentinel and body GitHub readback verified.

Bounded GitHub searches: neutral clause-restorers, nine-clause repair, mod-3 regularity, HEREDITARY-SCOPED10, CP22LIFT1, PC22_ALLFIELD1. No exhaustive absence claim. Inherited 3,532-file pinned SHA/keyword survey at 55a3fcc remains inherited, not rerun. Unread: historical main2..main14 bodies, historical revisions, Drive LOG/PROVED_EXACT/Manuscript/BOOL/SIL full pagination, source-only continuity, complete original HEREDITARY-SCOPED10 executable, many archived results.

LITERATURE: Döcker 2019 arXiv:1912.08032 original M22 language and fully paired SAT theorem; FLMV JACM 2005 DOI 10.1145/1101821.1101822 matched random-access SAT forbidden region. PC22LIFT1 proves proof-system Cutting Planes translation via nonmonotone signed regular formulas, NOT a general SAT-decider runtime edge. No signed-to-monotone automatic transport.

## Report, reproducibility and publication
Full report: research/agents/lspv-4/2026-10-25_0640_LSPV-4_M22_NEUTRAL_PORT100.tex
Portable mini checker: research/agents/lspv-4/2026-10-25_0640_M22_NEUTRAL_PORT100_MINI.py
Machine-readable full-local-audit summary: research/agents/lspv-4/2026-10-25_0640_M22_NEUTRAL_PORT100_RESULTS.json
Full independently executed local auditor SHA256: 9b49e8c208262106f035342178927eaacaf394b27eeba5ffef77c7f9b2e9c341. Full result SHA256 bf77699858180e20daeeb126985876af27c766d0e245b1314fbdcd2a28608924. The portable GitHub mini and local full auditor are different executables; do not conflate their check counts.

## Exact receiving obligations and statuses
FILLED / restricted: exact monotone M22 neutral child adapter for ANY clause deletion; exact one-deletion minimal h>=6, 9-new-clause floor, mod-3 connectivity; two-level semantic composition.
CONDITIONAL: using this adapter inside a separately proved all-input source-consistent reconstruction.
FALSIFIED / retired: deletion children automatically preserve C_star with no added material; independent one-port repairs; add-only repair is fractional-size ARC contraction; retired cosine time-plus-space endpoint.
OPEN ARC-EDGE-90: a favorable uniform all-input ordinary-SAT simultaneous time-space successor and cofinal finite-hit route into verified FLMV t<241/200 and s<11642479/23232400. OPEN DIRECT-POST: Phi over complete states with independently large starting value and bounded decrease per charged operation for every adaptive policy. P versus NP OPEN.

NEXT: construct a truly variable-eliminating source-consistent M22 type-restorer or prove impossible under explicitly universal adaptive operations; test two levels, both labels and boundary compatibility, and charge every length, source read, cache, replay and live ancestor. Preserve alternative symbolic, affine, Horn, SCC, direct and caching routes.
