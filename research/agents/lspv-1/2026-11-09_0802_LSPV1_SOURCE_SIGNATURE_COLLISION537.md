# LSPV-1/537: source-signature collision barrier for cost-sound abstract refutation search

**2026-11-09 08:02 PST | Route B | CANDIDATE (self-contained symbolic theorem, independent peer review pending) + COMPUTATIONAL finite source/authentication tests. P versus NP OPEN.**

**Proof-chain nodes:** proposed [P2-L1-537] refines methodological gap [P2-C3] and all-rule lower-bound obligation [P2-B1]; [P2-D1] native grammar and [P2-B2] noncircular same-calculus B3 remain OPEN. No Route A claims.

## IDEA, falsifiers, search, iteration

**Candidate before searching.** An abstraction of *all* fixed-calculus proof constructions that retains only source satisfiability, number of variables, number of proper width-three clauses, width profile and exact fixed-width encoding length cannot certify unbounded proof-work lower bounds on established odd-Tseitin families. The reason should be an explicit same-signature easy-UNSAT collision, not an unsupported argument about many abstract states.

**Four prespecified falsifiers:** (1) no duplicate-free proper 3-CNF easy control shares the claimed exact source statistics and bit length; (2) its seven Resolution steps use absent source clauses or an illegal pivot; (3) a best-correct may transition cannot replay a cheaper concrete proof from the collision class without exceeding native charges; (4) the proposed abstract interface in fact retains original-source provenance or a hidden source parameter, in which case the claimed collision premise is false.

**SEARCH.** Read complete current root `proof1.txt` (blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`) and `proof2.txt` (at first read `55d8f52ed492610a167d71e8bc9654bb97d2bebc`), governing `research/coordination/2026-11-09_ABSTRACT_INTERPRETATION_NEGATIVE_FIVE_ROLE_REFOCUS.md` (blob `8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b`), actual issue #3 and recent peer comments, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, 2026-11-02 original handoff, LSPV-1/536, LSPV-4 cost-partition report (blob `73131062bf74e65c39897594ef7341254210e78b`) and LSPV-5/462 (blob `dd57b460466ac3e210b8f6bcd83912a2b2b0b1fa`). The peer theorem concerns **paid-node history collision**; this run addresses the independent **source-signature collision** in the initial state. Read actual `GROKPROOF/2026-11-09_1230_PROGRESS.md` and `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` as scoped context, not as evidence for this lemma. Queried current `konard/p-vs-np/README.md` (blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95`), `blkph0x/p-vs-np-proof-research/README.md` (blob `f397a7747eaca82df3d754d0a4b4bab1fe10f814`), `meelgroup/frat-xor/README.md` (blob `38a137bca4d4ab6443703d4c31fba5783021c581`), `tanyongkiam/cake_lpr/README.md` (blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`) and `openai/math/lean/docs/378.md` (blob `223bbe187394bffca8a2c7ba1656538bfba26e3b`). Primary-publication landing pages and theorem abstracts checked through public web search: Urquhart, *Hard Examples for Resolution*, JACM 34(1), 1987, doi:10.1145/7531.8928; Atserias--Dalmau JCSS 2008; Keller et al., IJCAI 2016; D'Silva--Haller--Kroening POPL 2013. The full primary PDFs were not independently re-audited in this run; the governing handoff records its earlier PDF review. Public web search was available; a separate direct Google Search session was not. The repository preflight scripts were not run because the environment had no GitHub DNS access for a local clone, so source/artifact fetches and writes used the GitHub connector. No external native mixed checker, Lean build or source-format equivalence was performed.

## Exact full-configuration and abstraction interface

Fix an effective, sound, source-authenticated, nonnegative-weight proof calculus $R$ before the input. A concrete proof-construction configuration is

$$
s=(F,D,\mathcal C,\Gamma,\Delta,\operatorname{src},P,c),
$$

where $F$ is the **original binary source**, $D$ is a finite acyclic typed proof DAG, $\mathcal C$ its available conclusions, $\Gamma$ records branch contexts and their scopes, $\Delta$ holds auxiliary definitions and globally fresh identities, $\operatorname{src}$ binds every axiom to the original input, $P$ is the set of previously paid distinct node identities, and $c$ is cumulative native cost. Transitions include every authenticated legal rule and all legal zero-cost reuse/closure; paid insertion is charged once and never charged again merely because a node is reused across branches. A global goal is a completed original-source refutation with legally discharged assumptions.

The **theoretical best-correct may abstraction** for a function $\alpha:S\to A$ contains a projected edge $a\xrightarrow{c^\#}b$ for every concrete edge $s\xrightarrow{w}t$ with $\alpha(s)=a$, $\alpha(t)=b$, and $0\le c^\#\le w$. Its edges range across **all sources with the same initial abstract signature**. The abstract goal includes every projected concrete goal. This defines a sound (possibly noncomputable) relaxation of all legal rules, sharing, auxiliaries, contexts and zero-cost transitions. No charge, semantics or legality of historical $R_{\mathrm{mix341}}$ is redefined. A practical checker still needs separate authentic rule transformers. A formula-specific transformer secretly retaining $F$ is **not** the source-erasing quotient considered here.

### Theorem 537.1: cheap-source collision bound

For any two valid UNSAT original inputs $F,E$ with equal initial abstract states $\alpha(s_F)=\alpha(s_E)$, and for any source-parametric best-correct may abstraction of the **same fixed calculus**,

$$
d^{\#}(\alpha(s_F),G^{\#})\le W_R(E).
$$

**Proof.** Choose a completed legal $E$ refutation of cost $W_R(E)$ if attained (or a sequence arbitrarily close to the infimum). Topologically construct its paid shared DAG. Every concrete step projects to a permitted abstract step of no greater charge; every source/assumption/legal-goal state has an abstract image. Its projected path begins at $\alpha(s_E)=\alpha(s_F)$ and reaches an abstract goal. Therefore the abstract shortest-path cost is at most the chosen $E$ cost. Taking the infimum proves the claim. Since every actual $F$ refutation also projects, $d^\#\le W_R(F)$, but the cheap $E$ trajectory prevents this relaxation from establishing a bound larger than $W_R(E)$. This uses no tree unfolding, double counting, finite-width assumption or auxiliary-variable cutoff. QED.

**Necessary discrimination consequence.** To certify $W_R(F)>B$ via a source-parametric distance relaxation, its initial abstract class must contain **no** legal UNSAT source $E$ with $W_R(E)\le B$. This is a necessary precision condition, not sufficient for a lower bound. It is independent of the LSPV-5/462 requirement to distinguish fresh paid-node insertion from cached reuse.

## Established hard family and explicit easy collision

Let $G_h$ be any connected cubic graph on even $h\ge4$ vertices, with $n=3h/2$ edge Boolean variables and one odd-charge vertex. For each vertex, use the **four proper signed 3-clauses** excluding the local assignments whose incident-edge parity disagrees with its charge. The original Tseitin source $F_h$ has exactly $m=4h$ duplicate-free proper 3-clauses and is UNSAT because summing all vertex equations gives $0=1$ over GF(2). For suitable cubic expander families, Urquhart's classical result gives $2^{\Omega(h)}$ ordinary Resolution refutation size; its model is ordinary DAG Resolution, **not historical mixed $R_{\mathrm{mix341}}$**.

Reindex edges so the three edges of a selected vertex are variables 1, 2, 3. Construct a second source $E_h$ using all eight proper signed clauses on $(x_1,x_2,x_3)$, one further proper positive clause $(x_1\lor x_2\lor x_j)$ for every $j=4,\ldots,n$, and then arbitrary new, pairwise distinct proper 3-clauses until exactly $m=4h$ source clauses are present. There are enough slots because $4h-8\ge n-3$. Both sources use exactly $n$ variables, have exactly $m$ distinct width-three clauses, and are UNSAT.

The eight-clause core has a legal **seven-step ordinary Resolution refutation**: resolve on variable 3 in four pairs to obtain four binary clauses, on variable 2 in two pairs to obtain opposite units, then on variable 1 to derive the empty clause. It uses precisely eight authenticated source leaves, seven paid binary inferences, and a three-step inference critical path. With the native ordinary Resolution step weight $w_{\mathrm{Res}}$, $W_R(E_h)\le7w_{\mathrm{Res}}$ whenever the fixed calculus includes that rule at that weight (plus any **native** source-record charge, if present). Bit-time for reading the entire source remains separate.

For a declared binary encoding, prefix the positive integers $n,m$ by Elias-gamma codes; each clause then uses one marker bit and three literals of one sign bit plus $b=\lceil\log_2(n+1)\rceil$ identifier bits. Both sources have **identical exact bit length**

$$
N_h=\ell_\gamma(n)+\ell_\gamma(m)+m(1+3(1+b))=\Theta(h\log h).
$$

Thus an abstraction whose initial signature contains only $(\operatorname{SAT-status},n,m,[3]^m,N_h)$ equates $F_h$ and $E_h$ and cannot certify even an unbounded work lower bound on the Resolution-hard expander $F_h$. The same collision remains an upper control for any stronger fixed calculus containing Resolution; its actual $W_R(F_h)$ could be **much smaller** than ordinary Resolution because of GF(2), definitions, reconvergence or extension shortcuts.

## CEGAR iteration and independently checkable controls

A complete source-authenticated replay of $E_h$'s seven-step proof against $F_h$ fails: the selected cubic vertex contributes exactly **four** of the required eight signed triple clauses; four indispensable source leaf identities are absent. Refining the initial abstraction with the **eight-bit source-membership vector for these signed triple clauses** separates $F_h$ and $E_h$ and removes this specific spurious abstract trace. It does **not** establish any positive distance after refinement, since other legal mixed derivations may exist. The original heuristic was too coarse; the revised requirement is source-provenance discrimination plus paid-history/context discrimination, not just semantic classification and formula size.

Reproducible independent executable: `experiments/arc/lspv1_537_semantic_signature_collision.cjs`; raw: `results/raw/arc/2026-11-09_0802_LSPV1_537_SEMANTIC_COLLISION_RAW.json`. JavaScript exhaustive tests for K4, prism, cube and Petersen: all four odd-charge sources UNSAT, all four easy controls UNSAT, even-charge model counts respectively **8,16,32,64**, the seven-step core proof accepted against its own eight source leaves, its reuse as an original-source proof on each odd Tseitin rejected for four missing clauses, wrong-pivot negative controls rejected, and **36 check groups passed**. Matching bit lengths were **222,400,530,658 bits**, respectively. Independent standard-library Python implementation locally checked 56 grouped assertions on the same four graphs with exhaustive assignment enumeration; the Python script is a local fallback, **not** an externally published independent R checker. Neither implementation authenticates the historical mixed rule grammar or its exact weights.

**Falsifiers:** (1) failed: exact (n,m,width,N) matches hold in declared encoding; (2) failed: seven Resolution steps have exact antecedents and pivots in $E_h$; (3) failed: best-correct may projection replays legal $E_h$ steps without increasing cost; (4) is a **valid scope distinction**: source-specific abstract transitions retaining original clauses/provenance defeat the collision premise, as they should.

## Resource, branch and bridge ledger

| Resource or bridge | Result / limitation |
| --- | --- |
| Abstract all-rule transition coverage | Defined via best-correct may quotient of the *complete* concrete system; sound by construction, but not an executable transformer or authenticated $R_{\mathrm{mix341}}$ grammar. |
| Logical shared work | Cheap control seven distinct Resolution nodes; source leaves 8; no assumption branches, no duplicate charge. Full mixed optimum **not computed**. |
| Evidence bits | $N_h=\Theta(h\log h)$ input, a constant-size seven-node proof with logarithmic pointer/identifier costs. Source parsing remains $\Omega(N_h)$ actual bit work. |
| Search/construction/verification | Finite executable uses exhaustive $2^n$ truth evaluation plus source checks. Real time measured only for small controls; no worst-case SAT runtime conclusion. |
| Parallel span | Three paid Resolution levels in the cheap control under unlimited parallelism and free source availability; physical parallel schedule not measured. |
| Peak memory | Finite scripts materialize sources/proof arrays; observed high-water not instrumented, hence **no measured peak-space bound**. |
| Zero-cost reuse / auxiliary definitions | Allowed in concrete transition schema and its may projection, not omitted to improve the putative bound. |
| R exact native grammar / [P2-D1] | Still OPEN. Neither finite checker is the authoritative mixed checker. |
| Full all-rule lower bound / [P2-B1] | Still OPEN; collision theorem blocks one class of *abstract* attempts, not short actual mixed proofs. |
| Same-R transfer / [P2-B2] | B1 pointwise, B2 worst-case and B3 conditional all OPEN; no SAT-in-P implication or arbitrary-machine lower bound. |
| Route A | All-input same-machine iterative contraction untouched and OPEN. |

**Handoff:** LSPV-3 should make the eight signed source-facet membership test and correct context scopes part of native typed abstract transformers; LSPV-5 should challenge the source-collision theorem's source-parametric assumption and test a stronger quotient retaining source fingerprints plus paid histories; LSPV-2/4 may use the pairs as SAT/UNSAT/size-matched hostile controls but must not import any proof-cost result as a machine-time lower bound. Native $R_{\mathrm{mix341}}$ accepted-byte semantics, weights and all previously authorized roles remain fixed. Root `main.tex` returned zero content for a nonempty-looking blob and was left unchanged for safety.

**TRACKERS REVIEWED; MATERIAL METHOD-EVIDENCE CHANGE PROPOSED FOR [P2-L1-537] IN proof2.txt; proof1.txt NO CHANGE.** Final tracker publication status must be reconciled separately with current head+SHA and full readback.

**Actual advance:** Theorem 537.1 supplies a parameterized necessary source-discrimination criterion for any source-erasing cost-sound all-rule abstraction, plus an explicit seven-step same-size, same-bit-length hostile control on an established Resolution-hard 3-CNF family. It is an abstraction precision barrier, not the requested superpolynomial mixed lower bound. P versus NP OPEN.

### Primary references

1. A. Urquhart, *Hard Examples for Resolution*, Journal of the ACM 34(1):209-219, 1987, doi:10.1145/7531.8928 (ordinary Resolution).
2. A. Atserias and V. Dalmau, *A Combinatorial Characterization of Resolution Width*, JCSS 74(3):323-334, 2008 (ordinary Resolution width/game).
3. T. Keller, F. Pommerening, J. Seipp, F. Geisser and R. Mattmuller, *State-Dependent Cost Partitionings for Cartesian Abstractions in Classical Planning*, IJCAI 2016 (admissible cost partition, not native proof calculus).
4. V. D'Silva, L. Haller and D. Kroening, *Abstract Conflict Driven Learning*, POPL 2013 (solver-class abstraction, not an arbitrary-decider lower bound).
