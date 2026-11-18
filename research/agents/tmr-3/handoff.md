# TMR-3/088 compact handoff | 2026-11-18 09:27 PST | signature-quotient Kpq exact counting

**Role/state unchanged:** TMR-3 / PNP Time-Space Tradeoffs; 5-symbol beat relation R(x,y) iff y-x in {1,3} mod 5; same title, ownership, enabled state, hourly schedule, safeguards. P versus NP OPEN.

**Closed dependency C3-T5-CRITICAL-CORE088:** All simple connected oriented complete bipartite source graphs have polynomial-time exact T5 counting, despite unbounded treewidth and no degree-2 interior paths. Let a,b be counts of distinct orientation signatures on each side. If a+b>5, UNSAT by necessary distinct-color injection of signature representatives; otherwise min(a,b)<=2. Each selected signature class can use at most two colors, so support tuples enumerate at most 15^2/5=45 cyclic-translation orbits. Exact counts include all original labeled vertices via h_m({x})=1 and h_m({x,y})=2^m-2 and per-opposite-vertex admissible choice counts. No false general-hardness claim.

**Two controls:** all-forward Kpq has Z=5(2^p+2^q-2); at K1000,1000 this is 303 digits, 2,000 vertices, 1,000,000 arcs and treewidth 1000. Identity-oriented K3,3 is 3-regular bipartite T5-UNSAT because a=b=3. Both examples are easy source-specific certificates and do NOT demonstrate generic necessary work. All previous /085-/087 easy alternatives remain valid.

**Simultaneous source-recognized sequential one-tape symbolic upper bound:** T(N)=O((N+1)^8), S_peak(N)=O((N+1)^3) bits, including authentication, graph access, table/class construction, arithmetic, addressing, head movement and exact output; unrecognized inputs use exact 5^n polynomial-space fallback. These are constructive bounds, not executed native TM microcode.

**Execution:** full independent reference Python 1,236 deterministic assertions, zero failures, twice byte-identical; compact published implementation 610 exact exhaustive checks, plus 200 random cross-implementation comparisons. Standalone two-page LaTeX section compiled locally; entire combined manuscript compilation and independent review remain open. Published report: research/agents/tmr-3/2026-11-18_0927_TMR3_T5_SIGNATURE_QUOTIENT088.md; compact code: experiments/tmr/tmr3_t5_signature_quotient088_repo.py; audit: results/raw/tmr/2026-11-18_TMR3_T5_SIGNATURE088_AUDIT.json. Local complete reproducibility ZIP available in current run.

**Four gates:** DISJ PASS restricted constructive; relativization NOT APPLICABLE to separation; DTISP PASS restricted simultaneous upper, no lower-bound arrow; configuration counting upper-bound consistency only. /341 FAIL full UNSAT, /386 RESTRICTED. No SAT time-space lower exponent has been transferred via an exact reduction. General T5 NP-complete by Bang-Jensen, Hell, MacGillivray (1988), https://doi.org/10.1137/0401029.

**Next:** C3-T5-SIGNATURE-PERTURB089. Inspect near-complete Kpq with h deleted cross edges and determine which signature-injection witnesses remain sound; do not apply the Kpq signature theorem unconditionally once an arc is missing. Consider a fully charged FPT exact h-edge repair or counterexample.

END_OF_HANDOFF::TMR3::2026-11-18_0927_PST

---

# TMR-3/087 compact handoff | 2026-11-18 08:24 PST | chromatic cores resistant to /086

**Role unchanged:** TMR-3, PNP Time-Space Tradeoffs; exact T5 CSP, R(a,b) iff b-a in {1,3} mod 5. Prior safeguards and manuscripts retained. No schedule changes. P versus NP OPEN.

**Closed dependency:** C3-T5-AFFINE-RESIDUAL-HARD-CORE087. A new explicit family D_s is any single-edge orientation of canonical Mycielski mu^s(C5). Source parameters n_s=6*2^s-1, m_s=(21*3^s-12*2^s+1)/2, chi=s+3, minimum degree=s+2. For every s>=3, Z_T5(D_s)=0. In particular s=3 has (n,m,cycle rank)=(47,236,190). No private path compression or affine union occurs; remaining root count r=n. Nevertheless exact source-derived canonical recognition is polynomial-time and yields ZERO. Same-realization conservative recognized-family one-tape bounds T=O((N+1)^6), S_peak=O((N+1)^2) bits. No microcode execution claim.

**Existence theorem:** for every h>=3 there exists a simple oriented source with girth>h, chromatic=h+6, min-degree and treewidth>=h+5, UNSAT for T5, whose every <=h-vertex induced subsource is an oriented forest with exact count 5^c*2^(v-c). Erdős high-girth high-chromatic existence plus vertex-critical induced subgraph. This excludes solely bounded-size forbidden-induced-subsource recognition, NOT global algorithms. The high-girth construction is nonconstructive.

**Finite audit:** local Python reference 17,436 assertions, 0 failures, byte-exact repeated JSON; all 17,343 1-, 2-, 3-vertex induced subsources in the s=3 core SAT; source recognizer adversarial duplicate/loop/wrong-size rejection and reversal acceptance; independent exact small forest controls. Standalone three-page LaTeX compiled. Full manuscript compilation, actual one-tape microcode, independent review OPEN. DISJ restricted falsifier; relativization not a separation; DTISP constructive upper only; configuration counting no general LB. /341 FAIL /386 RESTRICTED. No numeric SAT->T5 exponent transferred.

**Current artifacts:** research/agents/tmr-3/2026-11-18_0824_TMR3_T5_CHROMATIC_CORE087.md; experiments/tmr/tmr3_t5_chromatic_core087_repo.py; results/raw/tmr/2026-11-18_0824_TMR3_T5_CHROMATIC_CORE087_AUDIT.json; appended main3_PNP_TIME_SPACE_TRADEOFFS.tex.

**Next dependency:** C3-T5-CRITICAL-CORE088: source-authenticated residual SAT/UNSAT examples escaping private paths, affine closure and the canonical chromatic shortcut; check all primal, dual and Fourier alternatives before a necessary-work claim.

END_OF_HANDOFF::TMR3::2026-11-18_0824_PST

---

# TMR-3/086 compact handoff | 2026-11-18 07:22 PST | private-path core and affine closure

**Role and source**: TMR-3 / PNP Time-Space Tradeoffs; original fixed five-symbol T5 homomorphism CSP, R(a,b) iff b-a in {1,3} mod 5. Identity, ownership, manuscript and existing hourly schedule unchanged. P versus NP OPEN.

**Closed dependency**: C3-T5-IRREDUCIBLE-CORE086. For every original digraph, decompose all indegree=outdegree=1 interiors into maximal branch-to-branch directed paths and pure directed cycles. The exact original-coloring count is product of cycle traces times sum over branch colors of integer M^length endpoint weights. For decision, private paths length >=4 impose no endpoint restriction. Short path supports S1={1,3}, S2={1,2,4}, S3={0,2,3,4}. Intersect supports and propagate singleton modular differences with potential DSU; detect contradictions exactly. When all path endpoints lie within one affine class, exact count is 5^r times product of fixed path weights. Otherwise enumerate 5^r root colors with original factors. This is a source-derived uniform solver, not an assumed preprocessing oracle.

**High-width source counterexample**: for ANY H, retain every arc u->v and add a private two-step u->p->v. Direct+2-step support intersection forces v-u=+1 and p=u+3. Thus Z(H+)=5^c if the edge-potential system is consistent, else zero. For H=oriented K_{k,k}, source n=2k+k^2,m=3k^2, treewidth>=k, count=5. k=100 original source n=10200,m=30000, count5. Three-cycle gadget is UNSAT even though directed triangle is SAT. Graph/treewidth cannot be a universal necessary-work proxy.

**Same-run resource analysis**: On encoded input N and r final affine roots, a deterministic blank-start single-tape realization admits symbolic T(N)=O((N+1)^12(1+5^r)), S_peak(N)=O((N+1)^4) bits. Closed form does not enumerate 5^r. All graph scans, failed union rounds, integer factors, addresses, caches, output are charged. No native TM microcode executed.

**Executed evidence**: full reference 1296 assertions, zero failures; compact repository implementation 704 independent checks, zero failures. Exhaustive 512 directed 3-vertex graphs, seeded random exact brute force, path extensions, loop/opposed, pure cycles, 15 disconnected family copies, SAT and UNSAT controls. Standalone 2-page section compiled; entire owned manuscript compilation and independent mathematical review OPEN.

**Gates**: DISJ PASS restricted width-falsifier; relativization N/A to separation; simultaneous DTISP PASS restricted same-realization upper bound; configuration counting PASS upper-bound sanity only. /341 FAIL as full UNSAT; /386 RESTRICTED. No quantitative SAT-lower-bound exponent transfer. Authenticated branch head of /085 predecessor retained and stacked draft planned; main not merged.

**Artifacts**: report research/agents/tmr-3/2026-11-18_0722_TMR3_T5_IRREDUCIBLE_AFFINE_CORE086.md; compact solver experiments/tmr/tmr3_t5_irreducible_core086_repo.py; audit results/raw/tmr/2026-11-18_0722_TMR3_T5_AFFINE_CORE086_AUDIT.json; updated main3_PNP_TIME_SPACE_TRADEOFFS.tex.

**Next**: C3-T5-AFFINE-RESIDUAL-HARD-CORE087. Source-discovered hard candidates surviving *both* private path suppression and affine closure, and all legal primal/dual/Fourier alternatives.

---

# TMR-3 compact handoff | 2026-11-18 00:20 PST | adhesion-two clique gluing /079

**Identity**: TMR-3 / PNP Time-Space Tradeoffs; fixed five-symbol beat-relation CSP takes precedence. Five prior TMR identities, titles, ownership, existing active hourly schedules and guards unchanged; no automation edited. Original source T5 graph on Z5; no algorithmic separation. P versus NP OPEN.

**New dependency closed in restricted form**: C3-T5-ADHESION-TWO079. Authenticated source graph with indegree-zero hubs plus private three-parent sinks, each sink producing the original exact ternary factor w(a,b,c). Enumerate empty/singleton/adjacent-pair clique separators in the factor primal graph, using virtual boundary edges of size at most two, never virtual CSP factors. Child-to-parent message has at most 25 entries and excludes color sums over the shared boundary. At separator-prime pieces require relative factor cover C of size <=t such that each ternary factor has two fixed hubs and every binary child message has at least one. Assign boundary plus cover colors, then sum all remaining hubs independently. Pay for decomposition, failed separator and cover search, input rereads, exact arithmetic, retained 25-entry messages, head motion and output. Cover DFS has no exponential cache.

**Complete restricted SAME_REALIZATION**: T(N)=O((N+1)^14[1+(t+1)3^t+5^(t+2)]), S_peak(N)=O((N+1)^5) bits, both for one deterministic blank-start locally headed machine. Fallback on incidence budget failure is exact 5^|H| hub enumeration; on arbitrary inputs exact forest enumeration O(poly(N)2^(n-c)), polynomial space.

**Countercontrols**: K4 atom with four original private sinks produces a nonrank-one 5x5 two-hub boundary message with row (26,0,6,6,0) and minor 676. A path of r such K4 atoms glued along whole two-hub edges has n=6r+2 and m=12r, no articulation vertices, strong-two-cover >=2 ceil(r/2), constant relative cover <=3. Exact count is 1^T M^r 1 for a genuine 25x25 transfer M, not an independent pair decomposition. At r=120, 722 vertices, 1440 arcs and 157 digits. 149 local deterministic assertions, zero failures; eight separate 25-state transfer cases and four NetworkX articulation crosschecks passed. Full executed source SHA256 af4a50a8c10a1685baad88b05e4fbf50cef6911e445b037c4d6f53251c3397c7, verified identical by GitHub readback.

**Manuscript repair**: the prior /078 owned TeX had two document endings and a truncated line at a_i. In-place update restored /078 mathematics and appended /079, yielding one begin/end document pair and matched theorem/proof/lemma environments. Historical well-formed preceding sections retained; complete LaTeX compile remains OPEN.

**Gates**: DISJ PASS restricted; relativization/algebrization NOT APPLICABLE to a separation; simultaneous DTISP PASS restricted for the upper bound; deterministic configuration counting PASS only as upper-bound consistency. Preserve affine/Horn/treewidth, low-degree, module/twin, cache/recompute, selector/padding, all prior easy-family controls; /341 FAIL as full UNSAT, /386 RESTRICTED. No exact numeric SAT lower-bound transfer. Native TM microcode, external peer review and whole-manuscript compile OPEN.

**Authoritative /079**: research/agents/tmr-3/2026-11-18_0020_TMR3_T5_CLIQUE_ADHESION_TWO079.md; experiments/tmr/tmr3_t5_adhesion_two079.py; experiments/tmr/tmr3_t5_adhesion_two079_independent.py; compact results JSON in results/raw/tmr. PR stacked on /078. **Next**: C3-T5-HIGHER-ADHESION080, larger clique/nonclique separators and conditioned interface treewidth with correct source-discovery and space accounting.

---

# TMR-3 compact handoff | 2026-11-17 20:21 PST | T5 separator / local strong-two-cover gluing /077

**Identity and priority.** TMR-3 / PNP Time-Space Tradeoffs. Current five-symbol beat-relation CSP user directive governs; November 15 end-to-end manuscript ownership and compatible safeguards preserved. Existing `main3_PNP_TIME_SPACE_TRADEOFFS.tex` edited in place, other owners and retired trackers untouched. Exactly the five existing agents, titles, enabled states and hourly America/Los_Angeles schedules unchanged. P versus NP OPEN.

**NEW C3-T5-STRONG-COVER-GLUING077: PROVED/EXACT RESTRICTED; independent mathematical review OPEN.** For authentic original digraphs consisting of indegree-zero hubs H and private indegree-three/outdegree-zero sinks, each original sink supplies the exact integer weight w(a,b,c)=|{z in Z5:R(a,z)R(b,z)R(c,z)}| in {0,1,2}. A genuine source-derived separator S of at most b hubs divides the triple-primal hypergraph into components B_i. A local relative strong two-cover C_i subset B_i of at most t hubs meets every original triple e touching B_i in at least 2 of S union C_i. For fixed separator/cover colors, every factor then has at most one free interior variable; exact original-count component messages multiply across components and sum over separator colors. Duplicate private sinks are distinct multiplicative factors, isolated hubs contribute 5.

**Complete same-realization upper bound, including discovery:**
`B(h,b)=sum_{j=0}^{min(b,h)} binom(h,j)`;
`T(N)=O((N+1)^12 [1+B(h,b)(t+1)3^t+r 5^(b+t)])`;
`S_peak(N)=O((N+1)^4) bits`.
All input authentication, every failed separator and cover attempt, graph/component construction, factor evaluation, source seeks, indices, arithmetic precision, retained state and exact output are charged on ONE sequential deterministic locally headed blank-start machine. The search enumerates S and uses 2/3-way budgeted cover branching; successful count streams assignments and does not prestore huge tables. For fixed b,t this is polynomial. **NOT FPT in variable b** because separator enumeration includes h^b. Nonmember/missing-budget cases use a correct original-arc forest-difference fallback in O(poly(N)2^(n-c)) time and polynomial space; valid loops/opposed arcs are recognized exact zeros, malformed inputs rejected.

**New infinite family G_r, beyond global cover bound.** One central hub a, and for each i three hubs b_i,c_i,v_i and three private sinks with triples (a,b_i,v_i),(a,c_i,v_i),(b_i,c_i,v_i). Original n=1+6r, m=9r; global minimum strong two-cover tau2=1+2r, while S={a}, each C_i={b_i,c_i} has local cover 2. Exact count `Z(G_r)=5*28^r`; direct fixed-color local product distribution 1*8+6*2+8*1=28. At r=40: 241 original vertices, 360 arcs and exact count `38484979364170447062492137914782951187182927182409110650880` (59 digits). This confirms global cover size is a poor necessary-work measure; it does not imply hard general T5.

**Actual finite executions.** Full locally executed CPython reference `/mnt/data/tmr3_t5_separator_glue077.py`, revision tmr3-t5-separator-glue077-v1, seed 202611172021, SHA256 `50aad4cd6f4036dc0a3282791b86fadedc5ab62435064dd3976d0cd9bfa7da40`, ran twice byte-identically with **341 checks, zero failures**. Full byte-exact raw Git blob `6538c77b2903573150d8bf41d96ea5ae8cce0116`, SHA256 `80c87a47e72303287b83296cfc70d086df96d497535181d1b0c6f5435c4bcd9e`. An independent readable compact repository Python implementation, blob `69bc3ed86a3c472c2209839d2a2c7b5c4c775901`, was locally executed with **152 comparisons, zero failures**; its raw exact Git blob `72543e13f97abb76b5caf0d9465e9a86a69d95be`. A full native Turing machine, local repository checkout/preflight, complete manuscript LaTeX build and independent mathematics review were not executed. Finite evidence is COMPUTATIONAL, separate from the symbolic proof.

**Current branch artifacts** (source readback verified before PR creation):
- `main3_PNP_TIME_SPACE_TRADEOFFS.tex` full updated SHA `226e2b9a0974c744ad97930399c35d5faaec6bdb`
- `research/agents/tmr-3/2026-11-17_2021_TMR3_T5_SEPARATOR_STRONGCOVER_GLUE077.md`
- `experiments/tmr/tmr3_t5_separator_glue077_repro.py`
- `results/raw/tmr/2026-11-17_2021_TMR3_T5_SEPARATOR_GLUE077_FULL_PY_RAW.json`
- `results/raw/tmr/2026-11-17_2021_TMR3_T5_SEPARATOR_GLUE077_REPRO_PY_RAW.json`
- archived exact preceding handoff `research/agents/tmr-3/archive/handoff_pre_2026-11-17_2021_T5_076.md`
- `research/agents/tmr-3/handoff.md` (this file)
This branch is `research/tmr3-t5-separator-glue077-20261117`, based on unmerged /076 PR #247. Do not claim main merge.

**Mandatory gates:** DISJ PASS restricted for positive constructive exact upper, no static-rank-to-necessary-work claim; relativization NOT APPLICABLE WITH REASON to any separation; simultaneous DTISP PASS restricted same-run upper only, lower-bound arrow OPEN; configuration counting PASS as deterministic upper-bound consistency only. Horn/2SAT, affine/Gaussian, bounded treewidth, module/twin, degree-two, selector, uniqueness, auxiliary, padding/product, compact caching/recomputation, all lawful alternatives and natural-proof/algebrization barriers remain admitted. /341 FAIL full UNSAT; /386 RESTRICTED. General T5 NP-complete by Bang-Jensen, Hell, MacGillivray (1988), DOI 10.1137/0401029, but no quantitative sparse SAT reduction/runtime exponent is inherited. P versus NP OPEN.

**ONE next load-bearing dependency:** C3-T5-TREE-ADHESION078. Source-derive and charge a tree of overlapping separator blocks, correctly count shared hub variables and produce efficient local interfaces without assuming the decomposition as input. Prove or falsify one exact interface transition next run.

END_OF_HANDOFF::TMR3::2026-11-17_2021_PST
