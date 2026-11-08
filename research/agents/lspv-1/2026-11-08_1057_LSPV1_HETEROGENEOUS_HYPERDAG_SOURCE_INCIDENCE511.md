# LSPV-1/511: heterogeneous-inference proof-hyperDAG incidence and source-essentiality barrier

**2026-11-08 10:57 PST | Route B LSPV-1 | PROVED/RESTRICTED combinatorial theorem and semantic source-necessity lemma; COMPUTATIONAL independent checks | P versus NP OPEN**

**Affected tracker node:** new [P2-L1-511], refining [P2-L1-510], [P2-L1-509], [P2-F13], [P2-B12]. **Unchanged OPEN:** [P2-D1], [P2-C3], [P2-B1], [P2-B2], and Route A [P1-01], [P1-03], [P1-04]. **Current peer-certified finite bound:** [P2-L5-440] replaces the older /510 15..19 interval by **17..19** for the *fixed 16-source, three-goal ordinary Resolution* problem. No new bound on 17/18 is claimed.

## IDEA, before literature search, and falsifiers

**Initial hypothesis:** replace the binary-only identity of [P2-L1-510] by an exact AND-incidence identity for mixed heterogeneous inference rules; combine it with assignment-level source deletion witnesses to determine which source-necessity bounds continue to hold under sound conservative extensions. Prediction: arity-3 or higher rules can make the binary 15-inference floor invalid, while a correctly weighted heterogeneous floor and original-source necessity remain sound.

F1. A legal source-explicit graph with a 3-antecedent inference contradicts the proposed exact identity.
F2. Sharing/reconvergence, multiple simultaneous conclusions or unary rule applications break it.
F3. A model of all but one original clause violating a required conclusion does NOT extend to a declared conservative auxiliary definition.
F4. Applying the new combinatorial bound purports to prove a superpolynomial lower bound or assumes a historical R_mix341 rule/cost without authenticating it.

## SEARCH: live project, primary sources and implementation controls

Read live complete \`proof1.txt\` (blob \`96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b\`) and \`proof2.txt\` (prepublication blob \`d897a6e16ccac7b3ef7f2598df69559f4bda71fa\`), current coordination issue #3 and most recent peer comments. Reviewed the governing November 2 five-role handoff, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md; the actual LSPV-1/510 report/code; [P2-L5-439]/[P2-L5-440] peer finite exact-Resolution analyses and [P2-L3-507]/[P2-L5-441] paid-CAST repair; Grok \`GROKPROOF/2026-11-08_1130_PROGRESS.md\` and Claude \`research/agents/claude/world-ledger/README.md\`. The Grok note is stale relative to /510, and is a critique, not authority. Google index searches and arXiv primary paper inspection were available.

Primary theorem control: Shuo Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (24 October 2026), Theorem 7.2(a), states almost-sure exponential lower bounds for $\mathcal F(n,w,\Delta n)$ in $\mathrm{Res}(\mathrm{PC}_r/\mathbb F_p)$ at fixed $w\ge3,\ \Delta\ge2^w$. In particular $w=3$, $\Delta=8$, $p=2$, $r=1$ qualify. Its exact scope is shared-DAG *restricted proof size*, not arbitrary computation, and its 2026 status is preprint. See https://arxiv.org/html/2610.00837v2. The exact signed proper 3-CNF source has $n$ variables, $8n$ clauses, and $O(n\log n)$ indexed bits. Published Haken PHP Resolution hardness and Cook extended-Resolution PHP shortcuts, together with Urquhart expander Tseitin and the project's linear parity shortcut, prohibit transferring a Resolution lower bound just by equisatisfiability or model similarity.

Inspected the actual \`konard/p-vs-np\` README and \`proofs/complexity/README.md\` (finite one-tape machine formalization of P subset NP, not universal model equivalence), and \`blkph0x/p-vs-np-proof-research\` README and \`proof_producing_cdcl_lab/PUBLIC_SAT_BASELINE.md\` (original-source RUP acceptance, 114 runs, no lower bound); also \`meelgroup/frat-xor/README.md\` and \`format.md\` (XLRUP, no current BNN acceptance and no RAT support), \`peitl/short-proof/README.md\` (single-goal shortest Resolution via PySAT), and \`openai/math/README.md\` (raw research artifacts and variable formalization status). Paths were inspected on default branch; no unverified theorem was imported from them. PySAT installation for an expanded finite search was attempted and failed due to network/DNS unavailability; no exhaustive 17/18-node search is claimed.

## ITERATE: exact mixed-arity identity

**Proposition 511.1 (elementary graph theorem, PROVED/RESTRICTED).**
Fix any finite, source-explicit, acyclic derivation DAG, pruned to the union of the ancestors of all required goals. Each paid inference vertex $v$ has $d(v)\ge0$ *cited premise incidences* (all required AND premises); OR alternative derivations are resolved by selecting one legal instance, not adding unused alternative edges. Let $m$ denote free source leaves, $q$ the number of paid vertices, $e=\sum_v d(v)$ the premise incidences, and $c$ weakly connected components of the underlying undirected multigraph. Let $\mu=e-(m+q)+c$ be its nonnegative cycle rank. Then

$$
\boxed{\sum_{v\ \mathrm{paid}}(d(v)-1)=m-c+\mu.}
$$

**Proof:** Euler's incidence count gives $\mu=e-(m+q)+c\ge0$ for an undirected multigraph. Since all premise edges terminate at paid nodes, $e=\sum_v d(v)$. Subtract $q$. This counts shared parents once as vertices and each actual premise reference as an edge. A unary inference contributes zero; ternary contributes two; zero-antecedent paid inference contributes minus one. Any free new axiom must be a source leaf. Proof DAG acyclicity is independently required by inference validity, not supplied by Euler counting. **This generalizes /510's binary-only equation; the graph-counting principle itself is classical and is not claimed novel.**

**Corollary 511.2 (weights).** If all historically legal rules satisfy, for a fixed $\alpha>0$ independent of the input and proof,
$w(v)\ge\alpha(d(v)-1)$ (automatic for $d(v)\le1$ when weights are nonnegative), then

$$
W_R(\pi)=\sum_v w(v)\ \ge\ \alpha(m-c+\mu)\ \ge\ \alpha(m-c).
$$

If a uniform maximum arity $D>1$ and uniform minimum positive inference weight $w_*>0$ are authenticated, the coarser count is $q\ge(m-c)/(D-1)$ and weighted work at least $w_*(m-c)/(D-1)$. These conclusions are **conditional on the actual native rule arities and weights**. If some high-arity rule is free, $\alpha$ may be zero and the bound becomes vacuous. No weights, grammar or rules of historical R_mix341 are revised here.

**Proposition 511.3 (original-source deletion necessity, PROVED/RESTRICTED).** Let $S$ be original source clauses and $Q$ required output conclusions. Suppose for each $C\in S$ there is an assignment $a_C$ satisfying $S\setminus\{C\}$ but violating at least one output in $Q$. In ANY sound source-authenticated proof system with conservative fresh definitions extending every original assignment and legal assumption discharge, every derivation jointly establishing $Q$ must cite $C$ somewhere in its complete provenance DAG. Otherwise extend $a_C$ to satisfy all definitions and premises of the purported proof; soundness would force all outputs $Q$, contradiction. This is semantic original-source necessity, **not** proof-size hardness. For a branch-local proof, the model argument applies only after the branch assumptions are properly discharged; incompatible contexts cannot be merged.

The existing 16-clause original signed 3-CNF cancellation gadget (seven original variables and three target clauses, [P2-L1-507] through [P2-L1-510]) has all 16 such deletion witnesses, verified anew. Therefore its 16 source facets remain jointly indispensable under *any sound conservative definitional extension*, not just ordinary Resolution. The established legal 19-inference binary Resolution output macro has $m=16,q=19,e=38,c=1,\mu=4$. Its up-to-date **finite ordinary Resolution minimum interval is 17..19**, from peer [P2-L5-440]. A distinct abstract legal-arity structural control joins 17 source leaves by eight ternary paid nodes with $m=17,q=8,e=24,c=1,\mu=0$; this is an exact sharpness witness for the arity bound, **not an R_mix341 derivation**.

## Consequences for Route B

Arity and source essentiality alone can certify **at most a linear-in-source-count** lower bound when the native system has bounded arity and positive fees. On the existing 4h-clause odd-charge cubic-expander Tseitin 3-CNF (3h/2 variables; $O(h\log h)$ indexed bits), the declared local AND3/GF(2) mixed construction already has $4h-1$ binary paid nodes (as analyzed in [P2-B12]); expander ordinary Resolution hardness does not survive as an all-rule claim. Any genuinely superpolynomial B1 target must force additional paid work beyond mere source connectivity under *every* mixed shortcut. This does **not** prove that no stronger invariant exists.

**B3 remains independent and OPEN:** $\mathrm{SAT}\in P$ does not automatically produce short certificates in the *same preselected* R_mix341. This run neither assumes polynomial formalized correctness of arbitrary deciders nor introduces a new proof system. The B1/B2/B3 distinction remains as originally fixed.

## Verification and resource ledger

Independent Python (140,654 assertions, 2,400 deterministic heterogeneous DAG trials, all sixteen exact source-deletion witnesses, real 19-step signed-pivot Resolution replay, three malformed graph controls and branch-scope controls) and independently implemented JavaScript (171 checks and the same finite witnesses/graph controls) PASSED. **The programs are finite tests; the general proposition is proved by the displayed mathematical derivation.** Original-source model checking uses 128 seven-bit assignments. A failed attempt to install PySAT is recorded, and no authoritative historical checker was executed.

Ideal graph work is exactly $q$ paid vertices with $\sum_vd(v)$ explicit premise references; weighted work uses historically fixed fees only if authenticated. Critical-path depth is separately the longest paid dependency path. Actual machines additionally charge reading all source bits, building and parsing the proof, witness or proof search (including unsuccessful branches), construction of auxiliary definitions, IDs/references, output serialization, checker execution, caches/retrieval and simultaneous peak memory. Those physical costs were **not** measured by ideal graph identities and imply no FLMV same-machine exponent or arbitrary-algorithm time lower bound. In a practical encoding, evidence bits depend on all node/parent IDs and clause literals. Root \`main.tex\` remains untouched: complete safe read and ownership reconciliation were not performed.

## Family / theorem / encoding / known shortcut / missing transfer ledger

| Family | Exact source / certified theorem scope | Mandatory shortcut control | Remaining transfer |
|---|---|---|---|
| Pang random proper $3$-CNF, $m=8n$ | Width 3; $n$ original variables; $N=O(n\log n)$; Pang Theorem 7.2(a): $\exp(\Omega(n))$ size in $\mathrm{Res}(\mathrm{PC}_1/\mathbb F_2)$ almost surely, *preprint premise* | Shared DAGs already included; unrestricted extension variables and full nonlinear conversions require separate legal simulation | [P2-C3], [P2-B1] OPEN |
| Expander odd-charge cubic Tseitin strict 3-CNF | $h$ vertices, $3h/2$ edge variables, $4h$ original width-3 signed clauses, $N=O(h\log h)$; expander Resolution exponential | Declared-semantic local parity aggregation refutation of $4h-1$ binary paid nodes; native R_mix341 acceptance not established here | [P2-D1], [P2-C3] OPEN |
| Haken PHP ordinary Resolution | Standard pigeonhole CNF, exponential ordinary Resolution DAG size | Cook extended-Resolution polynomial refutation, explicit fee/provenance needed | No general all-mixed transfer; B3 OPEN |
| 16-clause 7-variable circuit output gadget | SAT source, three entailed conclusions; **not** a hard UNSAT family; all 16 clauses individually source-essential | 19-node legal Resolution certificate; current peer lower bound 17 | Exact 17/18 and historical checker replay OPEN |

**Publication:** new [P2-L1-511] is justified only as this general-arity accounting and sound conservative source necessity; all core proof status nodes remain OPEN. Tracker edits (if made) are optimistic-concurrency, current-SHA and full readback only; neither task schedules nor historical R_mix341 grammar/weights may change. P versus NP remains OPEN.
