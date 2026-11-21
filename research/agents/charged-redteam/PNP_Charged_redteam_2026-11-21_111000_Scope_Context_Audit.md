# Redteam: scope-context audit and exponential enumeration of a constant
2026-11-21 11:10 PST, America/Los_Angeles.

## Selected claim, result and review status
**T5-SCOPE-CONTEXT-AUDIT1** audits Discovery's T5-CONTEXT-ORBIT1 at commit **1274ba70556d11dcea569a65b728ba256f5f6f07**, [report](https://github.com/j15marti/pnp/blob/1274ba70556d11dcea569a65b728ba256f5f6f07/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-21_105100_Scope_Restricted_Contexts.md), blob caa855fafdd89ba107fa099004791e600cd30ac4.

**PROVED/EXACT restricted reconstruction:** the ordered restriction of the accumulated map to the full declared scope is a sound memo key. The fixed-k view-scope bound survives. No in-model counterexample to the published upper bound is found. Retain its exact scope, authentication, identity-root, created-record and typed-closure premises.

**PROVED/EXACT boundary family:** a legal history with M=2d+1 records on v=3d variables has Q=3*2^d-2 reachable restricted contexts and 2^(d+1)-1 nodes under the specified unoptimized expansion, yet its target is constant true, with minimum ordinary DLDD size ONE. All handles admit constant-size semantic completions. Thus interpreting this compiler's Q or output size as a lower bound on minimum completion is **FALSIFIED/RETIRED**. The peer already warns against that inference; this is a reproducible strengthening of its boundary, not a retraction of its theorem.

**COMPUTATIONAL:** standalone code, no peer imports, checks all scopes and permutation-composition contexts through v4 (9523 cases,4286 nontrivial repeated restricted keys); the new family d1..12 has exact predicted Q;584 assignments at d1..3 pass. Finite tests are supplementary.

Review provenance: new reconstruction and independent implementation, but the SAME continuous assistant session authored the peer report. This is NOT external independent review. External adversarial review remains pending. No universal scalar-to-DLDD bridge or unrestricted lower bound is promoted.

ONE next dependency: **T5-LARGE-SCOPE-CONTEXT1**, Discovery owner, Synthesis tracking: obtain a paid structural upper bound on large-scope contexts, or an independently proved minimum-DLDD lower bound for a legal compact typed family. Large Q is insufficient; the constant family below must be retained as a control.

## Exact quantifiers and model reconstructed
For every fixed deterministic correct counter A in the peer's typed architecture, every strict-C NAND bipartite graph instance X, and the same actual execution of paid work W, let v be the Boolean universe and M all created record identities, including initialization and final target closure. M<=c_A(W+v+1). Dependencies point to older identities; rebuilt records get new IDs.

Native nodes are constants with possibly nonempty free scopes, literals, NOT, read-once decisions and decomposable binary Boolean operators. Child scopes are contained in parent scope; decomposable children have disjoint declared scopes. A decision label is outside both child scopes, and parent scope is their union plus the label. A view u=(b,h) has an explicit full-universe permutation h and exact declared scope S_u=h(S_b). All counts retain declared free variables. A source-residual reuse needs paid exact mapped-source authentication, not count/hash equality.

Starting all M handles with the identity on their scopes, Q counts the distinct pairs (record identity, ordered restriction of accumulated map). The claim is O(Q) native expansion and cumulative closed extension/positive-part defect O(MQ). If every VIEW scope is <=fixed k, Q<=M(1+v^k) for v>=1; use max(1,v) for v0. Native roots may have scope larger than k. No depth bound or small global permutation group is assumed.

Separately fix A,K>0,a>=1 independently of X and the proposed cap T_A(N)<=KN^a on the handoff's deterministic fixed-alphabet sole-tape model. Compiler costs are not A's actual costs. A typed final handle is required; scalar-only termination is outside this claim.

C is the symmetric30-tuple relation of all permutations of012,123,234,340,401 over Z5. Ordered R has40 tuples, defined by the first value winning once and losing once in the tournament where i beats i+1 and i+3. C is equivalent to R(x,y,z) AND R(y,x,z), but no conversion is made here. Historical S/Q results are not substituted.

Exact encoding:
N=n+2+2floor(log2(m+1))+3m ceil(log2(n+1)),
for unary n, gamma(m+1), and one-based fixed-width triple IDs. In the NAND image n=v+5,m=v+e+5,Z=10 #IS(H). These instances are all SAT; neither the compiler nor this control proves a decision separation.

Four falsifiers:
1. Full maps agreeing on S_u induce different descendant restricted maps or different values.
2. A legal fixed-k history reaches a scope>k node in a nonidentity context.
3. Context enumeration is substituted for minimum extension size or actual charged solver work.
4. Free scopes, deleted/rebuilt identities, joint outputs or final closure are omitted from the proof/accounting.

## Independent proof reconstruction
Write p~_u q iff p(i)=q(i) for every i in S_u. For a native edge u->b, S_b subset S_u implies p~_b q. For a view u=(b,h), h(S_b)=S_u implies p(h(i))=q(h(i)) for every i in S_b. Therefore p composed with h ~_b q composed with h. This is the crucial congruence: outside-scope disagreement cannot return through legal descent. It is an exact map statement, not semantic hashing.

Induction on older record IDs now proves that Expand(u,p) and Expand(u,q) have the same renamed predicate and declared scope whenever p~_u q. Constants retain the entire mapped free scope; injectivity preserves binary decomposability and decision read-once typing. NOT commutes with renaming. A view maps the base before the outer context, so the order is p composed with h. The ordered restricted tuple plus identity therefore determines a compiler subproblem. A set of images is not enough.

Every native key yields O(1) DLDD nodes; a view aliases the recursively returned pointer. The finite closure has Q keys, proving O(Q). Expanding each prefix from scratch bounds each closed extension by O(Q), regardless of the current retained library. At most M normalized producing/closure events give sum kappa_j=O(MQ), hence sum max(kappa_j-cq_j,0)<=O(MQ). This is deliberately an upper bound. Analytical history is not free physical storage.

For fixed k, before a path's first view, context remains identity on successively smaller scopes. At and after that view, scope size is at most k: views preserve size and native edges decrease it. Thus a node of scope>k can only have its identity context. Smaller nodes have at most (v)_s<=v^k injective maps. Summation proves M(1+v^k). This argument depends on identity starts; a test harness beginning arbitrary roots under arbitrary permutations cannot use the high-scope identity conclusion. The peer explicitly distinguishes those test calls, so no correction is required.

## Legal exponential-Q family with a one-node optimum
For each integer d>=1 use Boolean variables x_1,...,x_d, y_1,...,y_d, z_1,...,z_d. Define:
- u_0 is TRUE with declared scope {x_1,...,x_d}.
- h_i exchanges x_i and y_i and fixes every other variable.
- w_i=View(u_(i-1),h_i).
- u_i is the decision on z_i with low child u_(i-1) and high child w_i.
Build i=1,...,d, always using fresh record IDs.

There are M=1+2d records. Inductively
S_(u_i)={x_1,...,x_d} union {y_1,...,y_i} union {z_1,...,z_i}.
The view scope replaces x_i by y_i in S_(u_(i-1)); z_i is absent from both children. The decision's declared scope is exactly their union plus z_i. All dependencies decrease, all maps are explicit bijections, and read-once typing holds. Decisions need not have disjoint child scopes. Thus this is legal in the claimed architecture. View scopes grow with d; it is not a counterexample to the FIXED-k corollary.

All predicates are TRUE by induction. Every map preserves truth and a decision with two true children is true, even when the children's declared scopes differ. Missing variables remain free. The final u_d is TRUE on all3d variables and counts2^(3d), not1. One true sink with that declared scope is an ordinary DLDD representation. Scope metadata costs O(d log d) explicit bits; one Boolean node is not one physical bit.

To count contexts at u_i, later decisions j>i independently choose whether h_j is accumulated. These d-i swaps commute and their x_j coordinates are in S_(u_i), so all2^(d-i) restrictions are distinct. The same count holds at w_i, for i>=1. At u_0 there are2^d contexts. Earlier permutations cannot be introduced when descending from u_i before reaching a smaller record. Starting every handle at identity adds no keys: each such state already occurs along choices of later low branches from u_d. Therefore
Q=2^d+2 sum_(i=1)^d 2^(d-i)=3*2^d-2.
Native keys are the u_i only, so the unoptimized compiler creates
sum_(i=0)^d 2^(d-i)=2^(d+1)-1 nodes.
This is 2^Theta(M), while minimum DLDD size is1. The smallest member of THIS family is d1,v3,M3,Q4; no universal minimality claim about all counterexamples is made.

A scope-preserving constant-propagation pass certifies each record true directly from its children. It constructs each handle as a true constant with the correct scope, so each semantic extension needs at most one native node and sum kappa_j<=M. It never enumerates Q. Consequently the actual completion defect is at most O(M), despite an exponentially large compiler upper bound O(MQ). The rejected inference is large enumeration => large minimum extension, not the published O(MQ) ceiling.

## Actual strict-C source and fixed solver control
This is not merely an unrelated Boolean circuit. Use the edgeless NAND image on v=3d graph vertices, all placed in the left bipartition. Its full clause list is
C(a_i,a_(i+1),a_(i+2)) for i=0,...,4,
and C(a_0,a_1,X_j) for j=1,...,3d.
There are n=m=3d+5 variables/clauses with full initial domains and distinct variable names in every clause. In each of the ten anchor frames each X_j has two choices independently, so Z=10*2^(3d). Its Boolean normalized predicate is exactly TRUE on3d variables. The labels x,y,z above enumerate these graph variables. No primitive pin or uncharged domain restriction is added.

A fixed correct solver can authenticate this canonical edgeless source, create the displayed redundant history if desired, propagate truth with scopes, and output10*2^(3d). On other valid inputs it may use a correct exhaustive typed Shannon method. This defines one total fixed solver with polynomial work on the exhibited family; no global polynomial cap is asserted for that solver. In particular, the example does not mix executions to prove a time-space lower bound.

Let H=N+O(d^2 log(d+2)) cover source, O(d) explicit full maps/scopes, pointer IDs, counts and history. Repeated sequential scans suffice to build/authenticate the history and perform the constant propagation within a conservative O(H^4) sole-tape time and O(H) simultaneous span, hence O(H^5) physical CM for THIS easy-family execution. Counts have O(d) bits. An optimized solver need not create the redundant history at all. No claimed per-input lower demand may forbid that shortcut.

For d1, exact source n8,m8,N112,count80. Source counts for d1..12 in raw evidence use the symbolic frame/domain argument, NOT new full T5 assignment enumeration. The asymptotic family is an easy control, retained rather than labeled hard.

## New reproducible evidence
Run Python3 with assertions enabled:
```
python experiments/t5_redteam_scope_audit2_20261121.py > results/raw/t5_redteam_scope_audit2_20261121.json
```
Code SHA256:438fc1419349c59b2c3810ef784f1192acd47d11804d3ef411ecbbc1b5a06922.
No peer module or external package is imported. Full accumulated contexts are enumerated FIRST and projected afterward, unlike the peer's restricted-key recursive compiler. Thus the new Q evidence does not use the optimization under audit as its own oracle. A separate assignment evaluator transports assignments at views.

The scope-composition stage covers all subsets S and permutations h,p for v0..4, grouping full contexts by their ordered restriction to h(S), and verifies equal keys give equal compositions restricted to S. This exercises every placement of forgotten variables in those universes, not only cyclic/dihedral generators. Counts:9523 cases,4286 duplicate-key agreements. The symbolic congruence proof establishes the general result.

The new family runs d1..12. Selected rows:
| d | M | Q | Unoptimized native nodes | Minimum native nodes |
|---|---:|---:|---:|---:|
|1|3|4|3|1|
|3|7|22|15|1|
|6|13|190|127|1|
|12|25|12286|8191|1|

All584 assignments for d1..3 satisfy the directly evaluated root. For larger d the script checks the constant-propagation induction and exact context counts, not exponentially many assignments. The prior181352-case peer experiment is NOT rerun: it already covered its finite DAGs; this run checks a different invariant enumeration and a new exponential-gap family.

Recovered original peer code blob a2fa47ef61226411ad5a053e8e13380e6d39c9ad, raw blob d5ffdfc8ee007da83bdfdad7de364c661b2b277c. Its code hash ca45bfd0eb1cf2d10c8fcfb4842e9a4aa1068c386af03c70982806d45aad00e0 and prior dependency pin remain unchanged. No solver benchmark, circuit minimization search or proof-kernel build is claimed; the one-node optimum is proved explicitly.

## Resource ledger, controls and same-execution caps
Parsing and source authentication include all N bits and exact mapped residual/scope certificates. Our edgeless source has a direct syntactic recognizer; general source matching is not free. Discovery, failed maps, parameter choice, representation changes and adaptive switches belong to W. Unsupported operations leave the theorem's scope without being illegitimate algorithms.

Queries, real accesses, source rereads, map scans, pointer/address bits and head travel are charged. Scope metadata, retained input, history, cache and count buffers coexist; one physical shared object counts once. Rebuilding deleted records costs work and new identities. Native count arithmetic includes free variables and output10*2^(3d); write all answer bits and terminator. An analytical exponential expansion is not physical work that A is forced to execute.

For the SAME fixed A,N,K,a under a hypothetical polynomial cap retain:
S=O(N^a); physical CM=O(N^(2a)); minimum-description CM=O(N^(a+1)); encoded-input count-map circuit gates=O(N^a log N).
The fixed-k representation upper bounds N^(a+k),N^(2a+k) remain distinct. No cap is exceeded, no demands are added/multiplied, and no exponent or unrestricted algorithm class is excluded.

Controls tied to this audit:
- Free scopes are essential to the new family and counts; removing them changes the modeled counting task.
- Sharing and renaming create the exponential enumeration; semantic constant simplification removes it legally.
- Native NOT complements this true predicate to false with a constant-size representation; it does not make complement hard.
- Affine/Tseitin scalar algorithms still need no typed handles; the proof never compiles Gaussian answers universally.
- Private-leaf trees, matching and forced-domain formulas retain cheap evaluators; their residual multiplicity is not compulsory work.
- Relocation affects access cost, not the congruence; no original-cut return is assumed.
- Full-state output entropy remains zero; decision witnesses or answers to virtual queries are not mandatory services. This all-SAT source makes no UNSAT or decision separation claim.
UNKNOWN from failed source authentication remains distinct from UNSAT. Hash equality verifies evidence integrity only.

DISJ: NOT APPLICABLE; no communication demand. Relativization: OPEN for unrestricted transfer; no nonrelativizing step. Simultaneous DTISP: PASS for distinct compiler/A ledgers; no violation. Deterministic configurations: PASS for scope, no runtime inference from state counts. Natural Proofs/algebrization: no unrestricted circuit lower bound or claimed barrier bypass.

## Recovery and fresh searches
Base15d61b216e5741297b178ddaba6904be14c55806. Fresh mandatory-file fetches match the complete prior continuous-session reading: baseline a886f3387a8676b9cc86afbf3bebf22630109d49, assignment776c2622d69dbcbb1c7c0d1361f299970fb7f1cc, AGENTS01f05d238736da1a3a2a10c9586be3d882751212, CODEX15639f62a254aa9cd36a949b9f9d81985e5ed538, research instructions6f37fc1a1713b01abd91794d5523fb05a57efa2f. The141084-byte baseline SHA256 c9a3a0f362c72dfad7548b0cd44723853f105dcdc6a4f9ea5fef4559d3bb2a33 is not independently recertified. Recovered own10:15 report/handoff7828332b62ebf590507c0c4cca8ff2a2f11b096c and peer complete proof/code/raw. Issue324 read through Bounds comment7067699804; its zero-atom lemma is not a premise or a second audited target.

Fresh primary searches: “Variable Shift SDD trimming constants identical vtree2020”; “Beame DLDD definition decision NOT decomposable2017”.
Read [Beame–Li–Roy–Suciu TODS42(1),2017 Def2.4](https://homes.cs.washington.edu/~beame/papers/numsat-journal.pdf), DOI10.1145/2984632, for the native model. Constants, read-once decisions, NOT and decomposable binary Boolean operations are allowed; no arbitrary scalar compiler follows.
Read [Nakamura–Denzumi–Nishino SEA2020 article22, Theorem6 and Definition7](https://drops.dagstuhl.de/storage/00lipics/lipics-vol160-sea2020/LIPIcs.SEA.2020.22/LIPIcs.SEA.2020.22.pdf). Its sharing theorem requires isomorphic vtrees and compressed trimmed VS-SDDs; its trimming rules distinguish raw construction from reduced representation. This is an analogy, not an imported DLDD minimum-size theorem.

Fresh connected query “decision diagram variable permutation constant simplification” under anthropics,openai,xai-org,google,google-research,google-deepmind. No matches in the first five except transient Google429; Google retry returned none. DeepMind returned irrelevant Concordia memory data at d7da4499dd323fc51fce10b38105b3d17fb3651c, not a theorem. No instructions in dataset snippets were followed.

Web fallbacks: site:github.com/anthropics “decision diagram” simplification; corresponding OpenAI and DeepMind queries; site:github.com/xai-org “permutation” simplify; site:github.com/google-research “decision diagram”; site:github.com/google “decision diagram” constant folding. No applicable official Anthropic/OpenAI/xAI/DeepMind result found in this bounded screen. Google XLS tools documentation mentions a BDD statistics tool, not a lower-bound invariant.

Promising official repository inspected: [google-research/r_u_sure README](https://github.com/google-research/r_u_sure/blob/50d7018b8543a8314bf182ac286666ce39140aa4/README.md), commit50d7018b8543a8314bf182ac286666ce39140aa4, blob3099bc38fa959acd85ef8af2385eef4827f58027. Read fully. It describes utility decision diagrams for uncertainty-aware code suggestions and links notebooks. Its optimization objective is not exact T5 counting and the README supplies no applicable scope compiler theorem. No code imported or build run. “Official organization repository” does not mean officially supported product; the README explicitly disclaims product support.

Ownership remains grounded in verified corporate domains/cross-links recovered in this continuous session: [Anthropic](https://github.com/anthropics), [OpenAI](https://github.com/openai), [xAI](https://x.ai/open-source), [Google Research](https://research.google/pubs/implicit-rate-constrained-optimization-of-non-decomposable-objectives/), [DeepMind](https://deepmind.google/blog/open-sourcing-mujoco/), [Google](https://developers.google.com/optimization). Third-party name matches were not accepted as official sources. Searches are bounded relevance screens, not exhaustive absence or mathematical certification.

## Return to originating role
Discovery/Synthesis: retain T5-CONTEXT-ORBIT1 exactly as a restricted upper bound, including fixed-k scope discipline. Add the family above to T5-LARGE-SCOPE-CONTEXT1 controls. It demonstrates exponentially large Q on a one-node target even inside the all-SAT NAND image; a future negative result must prove minimum representation demand after legitimate simplification, not just measure this compiler.

Publication is confined to Redteam report/handoff and uniquely named code/raw. No local checkout, so preflight/LaTeX were not run. No TMR ownership, manuscript or schedule/enabled-state edits. External independent review remains pending. **P versus NP remains OPEN.**
