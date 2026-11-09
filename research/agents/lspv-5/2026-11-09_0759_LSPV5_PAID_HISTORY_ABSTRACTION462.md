# LSPV-5/462: paid-history erasure collapses cost-sound abstract distance

**2026-11-09 07:59 PST | Route B red team | PROVED/RESTRICTED symbolic theorem + COMPUTATIONAL finite replay | P versus NP OPEN**

**Affected proof-chain IDs:** new `[P2-L5-462]` refines the shared-work abstraction gap `[P2-C3]`, the legal-context obligation `[P2-C1]`, and the current abstract-interpretation methodology. Historical accepted-byte grammar `[P2-D1]`, all-rule superpolynomial minimum `[P2-B1]`, and same-calculus noncircular B3 `[P2-B2]` remain OPEN. Route A `[P2-A2]`, `[P2-A4]`, `[P2-A5]` and proof1 `[P1-01]`, `[P1-03]`, `[P1-04]` are unchanged.

## IDEA -> SEARCH -> ITERATE

### Initial hypothesis and falsifiers

Hypothesis: a cost-sound abstraction of shared proof construction cannot forget whether a reusable inference node has already been paid. If a paid first insertion and a zero-cost reuse become enabled from the same abstract state, the best sound abstract distance can collapse to zero even when concrete minimum work is positive.

Prespecified falsifiers:

1. the current project already proves the exact paid-history necessity theorem;
2. the full historical rule grammar supplies a different native charge for references/reuse, invalidating the zero-cost premise;
3. state-dependent cost partitioning remains positive after the paid and cached configurations are merged;
4. a cheap legal R_mix341 shortcut renders the proposed family lower bound irrelevant.

Search found a nearby but different theorem. `research/review/reports/resource_auditor/2026-11-09_LSPV4_COST_PARTITION_SIMULATION.md` (blob `73131062bf74e65c39897594ef7341254210e78b`) proves a sufficient simulation theorem **assuming** the concrete state includes the paid-node set $D$, and gives the already-known shared-lemma double-counting example. I therefore did not repeat that example. The revised target is the necessity of retaining paid history (or an equivalent separating refinement) in the abstraction itself.

### Exact theorem

Let $(S,E,w)$ be a nonnegative weighted transition system for topological construction of a shared proof DAG. A concrete configuration includes whether a named node $L$ is already in the paid set. Let

$$
s_0=(\mathrm{ready},L\notin D),\qquad
s_1=(\mathrm{ready},L\in D),\qquad
g=(\mathrm{goal},L\in D).
$$

Suppose the legal edges are

$$
s_0\xrightarrow{r}s_1,qquad s_1\xrightarrow{0}g,qquad r>0,
$$

where the first edge inserts and pays for $L$ and the second reuses it. The concrete optimum from $s_0$ to $g$ is $r$.

Let $\alpha:S\to A$ be an abstraction and use the best-correct may transformer: every concrete edge from any state in $\gamma(a)$ is available from $a$. If $\alpha(s_0)=\alpha(s_1)$, then the zero-cost reuse edge is enabled immediately at the abstract initial state, so

$$
d^\#(\alpha(s_0),\alpha(g))=0<r.
$$

More generally, for a class-local abstract edge charge $c^\#(a,b)$ satisfying

$$
c^\#(\alpha(s),\alpha(t))\le w(s,t)
$$

for every represented concrete edge, the greatest admissible charge on an abstract edge class is the infimum of the concrete charges in that class. Any class containing a zero-cost reuse has best-correct charge zero. Therefore a positive distinct-node lower bound requires the abstract state or path history to separate every relevant unpaid-first-use configuration from the corresponding already-paid reuse configuration (and to separate the initial state from abstract goals). Exact node identifiers are sufficient but not proved necessary; a coarser certified freshness quotient may also suffice.

**Proof.** The concrete path has charge $r+0=r$. Under $\alpha(s_0)=\alpha(s_1)=a$, the concretization $\gamma(a)$ contains $s_1$. Sound may-overapproximation must therefore include the legal edge $s_1\to g$ from $a$ at charge at most zero. Hence an abstract goal is reachable from the abstract initial state at cost zero. For the class-local statement, admissibility against every represented concrete edge gives $c^\#(a,b)\le\inf w(e)$ over the class; a zero-cost member forces $c^\#(a,b)=0$ by nonnegativity. QED.

This is a **precision obstruction**, not a concrete proof lower bound. It does not say that tracking paid identities is expensive, that every abstraction must be explicit, or that an exponentially large abstract domain requires exponential physical memory. Succinct/symbolic representations remain legal controls.

### Independent challenge and computation

The Python implementation enumerates all five set partitions of the three concrete states for charges $r=1,\ldots,8$. It computes best-correct abstract edge charges as minimum concrete charge per abstract edge class and shortest abstract distances. All 40 cases and 128 assertions passed: every paid-history-merging partition collapses to zero; partitions separating fresh/cached and initial/goal recover the exact charge in this system.

A separately written JavaScript verifier repeats the calculation for $r=1,\ldots,16$: 80 cases, 256 checks, 32 merged-history zero distances and 32 separated-history exact distances, all PASS. The finite replay checks the minimal transition instance; the theorem above is symbolic.

Artifacts:

- `experiments/review/lspv5_462_paid_history_abstraction.py`, Git blob `bc6b929b91cb5cc4ee6e2cc978c9f25d25a83e30`, SHA-256 `8e7a0a89769747ad3a93dce34a3334444e1ec9bf9fe47cfa7289e3852426fc19`;
- `experiments/review/verify_lspv5_462_paid_history.mjs`, Git blob `0be5e12328f8cd38af30d4f5f84e3fe7fdc42db5`, SHA-256 `b8d978349af7bf8513e2ebb0bfa319935a1d477cce9bb65ad59d864f6b57e6f1`;
- `results/raw/arc/2026-11-09_0759_LSPV5_462_PAID_HISTORY_ABSTRACTION_RAW.json`, Git blob `a8525aa12aca15a622d4f605ab55c6cd00754739`, SHA-256 `0abc8238fbdc4b5a7ea2f9bf7c2639f683ae87f983209d64e1ed78b4c8f277e8`.

Hosted runtimes are not native R_mix341 or FLMV measurements. Python wall time was 0.043 seconds; no all-phase RSS claim is made.

## Established-family and shortcut ledger

| Family | exact encoding / size | established theorem and model | legal known shortcut control | remaining transfer |
|---|---|---|---|---|
| Odd-charge cubic-expander Tseitin | For connected cubic $G=(V,E)$, variable $x_e$ per edge. At each vertex $v$, include the four ternary clauses forbidding assignments $z\in\{0,1\}^3$ with $\bigoplus z_e\ne\chi_v$. Thus $n=3|V|/2$, $m=4|V|$, and indexed source length $N=\Theta(|V|\log |V|)$. Odd $\bigoplus_v\chi_v$ is UNSAT. | Urquhart (JACM 1987, DOI 10.1145/7531.8928) proves exponential Resolution lower bounds on suitable expander instances; Ben-Sasson--Wigderson (JACM 2001) recovers expander-Tseitin Resolution bounds via width. These are ordinary shared-DAG Resolution results, not all-algorithm hardness. | Summing the vertex equations in GF(2) gives a polynomial algebraic contradiction. Existing project `[P2-B12]` has $4h-1$ declared-semantic AND3/GF(2) work. Extensions, LOCAL-CONVERT, branching and shared lemmas remain mandatory controls. | A useful full-mixed abstraction must expose this cheap GF(2) path and distinguish first-paid nodes from reuse. Full historical byte semantics and all-rule invariant are OPEN. |
| Haken PHP | Standard unary PHP has pigeon variables $x_{i,j}$, pigeon clauses $\bigvee_jx_{i,j}$ and collision clauses $\neg x_{i,k}\vee\neg x_{j,k}$. | Haken (TCS 1985, DOI 10.1016/0304-3975(85)90144-6) gives exponential ordinary Resolution length. | Extended Resolution has polynomial proofs, already noted in Haken's abstract; paid definitions are therefore a mandatory upper-bound control. | No lower-bound-preserving transfer into full R_mix341 is authenticated. |

Certified UNSAT, certified proof-size hardness and empirical difficulty remain distinct. The finite K4/prism/cube/Petersen controls in peer reports certify exact small labels, not growing expander hardness.

## Literature and repository search log

Primary sources inspected:

- Cousot--Cousot, POPL 1977, abstract interpretation as sound fixpoint approximation;
- Keller et al., IJCAI 2016, state-dependent cost partitioning over state-action context;
- Henry--Monniaux--Moy, SAS 2012, succinct representations for abstract interpretation;
- Urquhart 1987; Ben-Sasson--Wigderson 2001; Haken 1985, with theorem scopes recorded above.

The Keller paper explicitly treats state-dependent context as precision-bearing. This supports the revision: collapsing paid/cached contexts can destroy admissible distance, but does not itself supply the project theorem. AARA literature independently warns that unrestricted duplication of potential is unsound and uses explicit contraction/sharing; that is an analogy, not a transfer into R_mix341.

Project corpus read: complete current `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; complete prewrite `proof2.txt` blob `4e1285659bb4f0e9767a69a8e86e0047f431f47f`; current issue #3 through comment `6744571426`; governing `research/coordination/2026-11-09_ABSTRACT_INTERPRETATION_NEGATIVE_FIVE_ROLE_REFOCUS.md`; historical five-role handoff at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`; `AGENTS.md`, `CODEX.md`, skill, red-team mode and research protocol; peer LSPV-1/536, LSPV-2/520, LSPV-3/535, LSPV-4/522 and the resource-auditor cost-partition report; `GROKPROOF/2026-11-09_1230_PROGRESS.md` blob `0ee19c6b2fdf92b64427ab737fe563346779c828`; Claude world-ledger README blob `de75a371ce3143a4495e6892df7fb04794a6b708`.

Required external change-aware review:

- `konard/p-vs-np` pinned head `ecedd2b45f1c524d85c00b2da27a9c140025550c`, unchanged; actual `README.md` and `proofs/experiments/issue568/README.md` reiterate a finite-machine trace slice and leave the fixed all-input SAT machine OPEN.
- `blkph0x/p-vs-np-proof-research` pinned head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, unchanged; actual README/status and `PUBLIC_METHOD_REVIEW.md` retain scoped exact algorithms, finite certificates and unresolved generalization gaps.
- `meelgroup/frat-xor` head `18cd6bc17af10a9891c10a846ce966166f9fe0dc`; README authenticates FRAT-XOR elaboration to XLRUP/CakeML checker scope, not R_mix341.
- `peitl/short-proof` head `2c524cfceecf68b56f51d23f6b63255b502856d3` from the prior pinned inventory was reviewed change-aware; no project-relevant delta was found this run.
- `MassimoLauria/cnfgen` head `24e633bdbed0d0998493bee99c42faf480c7dc96`; root `README.md` fetch returned 404, so no content review is claimed.
- `openai/math` head `4eaee87548250b2682affda7d05d947c05554bae` and `anthropics/formal-math` head `16a5ce41304fcdaea4e0be7c132e1c361dc26da5` were unchanged; their formal SAT artifacts do not authenticate this proof calculus.

Queries included `best correct abstract transition cost`, `already paid abstraction reuse first insertion`, `paid-node identity abstract`, `state dependent cost partitioning`, and the primary Resolution-family searches above. General public web search was available. A separately identifiable Google-branded endpoint was unavailable, so no Google-specific search is claimed.

## Resource and trust ledger

- **Logical measure:** one positive first-insertion charge $r$ and one zero-cost reuse in the minimal transition system; this is not a R_mix341 proof.
- **Evidence bits:** two source files plus 1,070-byte raw JSON; complete output is reproducible from code.
- **Construction/search:** 40 Python abstraction cases, 128 assertions; 80 independent JS cases, 256 checks.
- **Reads:** complete trackers, current issue page, named reports/handoffs and pinned external files. Root `main.tex` blob `fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba` again returned zero content bytes; it was not edited.
- **Parsing/updating/output:** GitHub publication and tracker append are reported below after SHA-guarded completion.
- **Caches/retrieval/recomputation:** host process memory only; no retained proof database or native cache bound.
- **Failed policies:** the original duplicate double-counting target was retired as already present in the LSPV-4 resource report.
- **Trust boundary:** symbolic proof in this report plus independent finite implementations; no official historical checker, Lean build, link checker, SAT solver or native FLMV execution.

Local preflight reported the scratch checkout lacks root `main.tex`, skill and root governance files; authoritative GitHub copies were read instead. Because complete root `main.tex` content was unavailable through the connector, whole-document reconciliation was safely skipped rather than overwriting a partial file.

## Status and remaining gap

**Actual advance:** a precise necessity theorem for cost abstractions of count-once shared work: erasing already-paid history admits a zero-cost spurious path and can collapse the best-correct abstract distance. This independently validates a missing assumption in the LSPV-4 sufficient simulation theorem.

**Precise remaining gap:** authenticate every historical R_mix341 transition and construct a source-family invariant that (i) retains or soundly quotients paid-node freshness, contexts and provenance, (ii) admits GF(2), definitions, LOCAL-CONVERT, branching and reconvergence, (iii) excludes every goal below a superpolynomial budget, and (iv) separately supplies a noncircular same-calculus B3 bridge. None is proved here.

Publication and tracker readback status are recorded in the issue #3 handoff. P versus NP remains OPEN.
