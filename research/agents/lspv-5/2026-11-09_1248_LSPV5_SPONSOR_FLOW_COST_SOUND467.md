# LSPV-5 / 467 — Hall/max-flow sponsor certificates for whole-DAG cost soundness

**Role:** LSPV-5 independent red team, Route B primary  
**Pacific time:** 2026-11-09 12:48 PST  
**Status:** **PROVED/RESTRICTED + COMPUTATIONAL**  
**Global status:** P versus NP remains **OPEN**.

## Actual advance

A rule-local or branch-local cost check is insufficient for a shared proof
DAG: two abstract charges may each fit a concrete paid node when inspected
separately, yet jointly overdraw that node's count-once weight.  This report
gives an exact global certificate for the accounting layer.

For a fixed concrete proof $P$ and proposed abstract image $P^\#$, make a
bipartite **sponsor graph**.  Abstract charged nodes have demands $c(u)$;
concrete distinct paid nodes have capacities $w(v)$; an edge $(u,v)$ exists
only when the rule/context/provenance simulation permits $v$ to sponsor $u$.
If a feasible flow meets every abstract demand without exceeding any concrete
capacity, then

$$
\operatorname{cost}(P^\#)\leq\operatorname{cost}_R(P).
$$

By max-flow/min-cut, feasibility is equivalent to a weighted Hall inequality
for every set of abstract charges.  This makes the global count-once
obligation independently checkable.  It is an accounting theorem, not a
historical R_mix341 rule-coverage or semantic-soundness theorem.

## IDEA

### Initial hypothesis

Assume a concrete source-authenticated shared refutation and a proposed
abstract image with explicit rule/context/provenance eligibility.  A global
capacity allocation should be sufficient for cost nonexpansion, whereas
individual per-path inequalities should fail on a shared ancestor.

### Precise falsifiers

1. Every collection of individually cost-safe path simulations remains
   cost-safe after reconvergence.
2. Duplicating one shared concrete ancestor into two charged abstract
   occurrences can still preserve count-once cost.
3. A global sponsor allocation can exist even when some abstract subset has
   demand exceeding all its eligible concrete capacity.
4. Passing this accounting certificate alone authenticates historical rule
   coverage, semantic conclusions, context discharge, or B3.

Falsifiers 1 and 2 fail by the two-demand/one-capacity witness.  Falsifier 3
is excluded by the exact max-flow/min-cut characterization.  Falsifier 4 is
false: the certificate is deliberately separated from transformer semantics
and universal rule coverage.

## SEARCH

### Governing project evidence read

Fresh starting head: `ba59d0578e36eacef0be44ff5c6783708293b3b3`.
Both complete trackers were read: `proof1.txt` blob
`96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 characters) and
`proof2.txt` blob `b003d81526fd99265ae9072254b5ba94fb30deae`
(806,201 characters).  Also read the November 9 abstraction refocus blob
`8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b`, current issue #3 through comment
`6750753471`, AGENTS.md, CODEX.md, the complete repository research skill,
the requested knot/link handoff, the governing November 2 handoff, complete
root `main.tex`, actual current Grok file
`GROKPROOF/2026-11-09_1230_PROGRESS.md` blob
`0ee19c6b2fdf92b64427ab737fe563346779c828`, and actual Claude file
`research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob
`9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`.

Material peer reports read directly:

* [P2-L1-542], source-exact polynomial-evidence Tseitin macro in a distinct
  calculus, report blob `949f8ab4b2f4ee39ea0568f058f1f9fd45e9a4f5`;
* [P2-L2-525], original-variable CDCL-to-RUP MAY projection and its CEGAR
  addendum, report blob `5587e41d588583894c427cd2b5b1bf2815c335b1`;
* [P2-L2-526], the original-source RAT/DRAT-minus cost-abstraction firewall,
  report blob `ed4033544834d4d49d0e1d14b463808f8ca26ad9`, as published on the later
  current head `e95e962c9e5ed9a63469da1f516eb0450ec707c0`;
* [P2-L3-540], exact width-three local factor-domain precision, report blob
  `fe1456d56f790b951dafed231c1c4064d86bf016`;
* [P2-L5-464] occurrence/history separation, blob
  `c1349a53398fd0e2b5a7102c2d4dd711894e20f3`;
* [P2-L5-466] provenance alpha join, blob
  `6377759d8746728eed3c738274afad28de1a9890`;
* LSPV-4's earlier cost-partition theorem and shared-node falsifier at commit
  `dba0f8b8f4215ad8d6e78813ceccba365f30cc90`.

The present result is not a repetition of the LSPV-4 theorem.  That theorem
assumes an already supplied per-transition partition.  The new result
characterizes exactly when an arbitrary collection of abstract DAG charges
admits **some** globally compatible partition, with context/provenance
eligibility and a checkable violating cut when it does not.

Before publication, a conflict-safe reread found later head
`e95e962c9e5ed9a63469da1f516eb0450ec707c0` and complete `proof2.txt` blob
`eace1c9c6ef5a36b99b70f7655c0056ffd36ca22` (808,680 characters), including
[P2-L2-526].  That restricted RAT firewall reinforces, but does not extend,
the rule-by-rule eligibility requirement.  `proof1.txt` remained unchanged.

### Predecessor write check

Git history contained no verified LSPV-4 write after [P2-L4-522] at 07:50 PST;
the expected later predecessor result was absent at this preflight.  The issue
#3 handoff requests a retry of the existing write only.  No task, schedule,
identity, timezone, title or enabled state was changed.

### Primary literature

* Cousot and Cousot, *Abstract Interpretation* (POPL 1977),
  <https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml>: the concrete-to-
  abstract simulation direction is load-bearing; omitting a concrete behavior
  invalidates a negative certificate.
* D'Silva, Haller and Kroening, *Abstract Conflict Driven Learning* (POPL
  2013), <https://www.kroening.com/papers/popl2013.pdf>, and *Abstract
  Satisfaction* (POPL 2014), <https://www.kroening.com/papers/popl2014.pdf>:
  deduction, abduction, quantification, propagation and learning are relative
  to a declared abstract domain; neither paper supplies a mixed-proof lower
  bound or B3.
* Keller et al., *State-Dependent Cost Partitionings for Cartesian
  Abstractions in Classical Planning* (IJCAI 2016),
  <https://ijcai.org/proceedings/2016/448>, plus the authors' full-proof report
  <https://ai.dmi.unibas.ch/papers/keller-et-al-tr2016.pdf>: admissible sums
  allocate transition costs across abstractions, and context-dependent
  partitioning retains information lost by action-only partitions.
* Pommerening et al., *Heuristics for Cost-Optimal Classical Planning Based on
  Linear Programming* (IJCAI 2015),
  <https://ijcai.org/proceedings/2015/612>: the standard nonnegative condition
  is that allocated abstract action costs sum to no more than the original
  action cost.

The project mapping from path planning to complete shared proof DAGs is new
work in this report and is not attributed to those papers.  The capacitated
Hall statement is proved below from max-flow/min-cut, so no external theorem
scope is imported silently.

### Required repository review

Fresh heads and actual inspected files:

| Repository | Head | Evidence / relevance |
|---|---|---|
| `konard/p-vs-np` | `ecedd2b45f1c524d85c00b2da27a9c140025550c` | `README.md` blob `0e0ec77f...`; finite-machine scope only |
| `blkph0x/p-vs-np-proof-research` | `7dedc73f758dfbdc072e7aa29dfc08505761ebd5` | `METHOD_INDEX.md` blob `18d693ea...`; bounded/promised status ledger |
| `meelgroup/frat-xor` | `18cd6bc17af10a9891c10a846ce966166f9fe0dc` | `format.md` blob `986a21aa...`; explicit XOR checker rules, no free historical import |
| `tanyongkiam/cake_lpr` | `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2` | `README.md` blob `e94f45e9...`; compiled checker/toolchain scope |
| `CakeML/cakeml` | `afeab35152069a3711598630be9fbdcec9cf29bc` | current diff changes integer division/modulus rounding, not proof-cost sponsorship |
| `peitl/short-proof` | `2c524cfceecf68b56f51d23f6b63255b502856d3` | shortest Resolution only |
| `pysathq/pysat` | `bf246f36581e5d5ed1aa6eacf11e5d6fd4b664bc` | solver/cardinality toolkit, not a general lower-bound theorem |
| `MassimoLauria/cnfgen` | `24e633bdbed0d0998493bee99c42faf480c7dc96` | exact odd-charge Tseitin generator control |
| `openai/math` | `4eaee87548250b2682affda7d05d947c05554bae` | README warns of heterogeneous verification stages |
| `anthropics/formal-math` | `16a5ce41304fcdaea4e0be7c132e1c361dc26da5` | per-project Lean/toolchain pins; no bridge authority |

The two required P-vs-NP repositories and the rotating checker/solver/family/
formalization corpus contain no result closing [P2-D1], [P2-C3], [P2-B1] or
[P2-B2].  Current CakeML changes are unrelated to the active gap.

## ITERATE

### Concrete and abstract domains

For fixed source $F$, the concrete domain consists of complete legal
source-authenticated acyclic proof hypergraphs $P$.  Each distinct paid node
$v\in V(P)$ carries fixed native weight $w(v)\geq0$, rule label, premises,
source provenance, definition origin and context.  Its cost is

$$
\operatorname{cost}_R(P)=\sum_{v\in V(P)}w(v).
$$

An abstract candidate $P^\#$ is another acyclic occurrence hypergraph with
charged nodes $u\in U(P^\#)$ and nonnegative demands $c(u)$.  Its semantic
labels may overapproximate concrete conclusions, but goal mapping, every AND
premise, legal contexts, reconvergence and provenance remain separate proof
obligations.

The accounting abstraction is the tuple

$$
\alpha_{\rm cost}(P)=(P^\#,E,c,w),
$$

where $E\subseteq U\times V$ records **eligible sponsorship**.  Eligibility
must be justified by the concrete-to-abstract rule simulation and compatible
context/provenance.  The concretization $\gamma_{\rm cost}$ contains concrete
proofs for which such an image and a feasible sponsor flow exist.  For a
cost-sound lower-bound abstraction, every legal concrete proof must belong to
that concretization; adding abstract proofs or eligibility edges may lower
the abstract minimum and is safe but can destroy precision.  Removing a legal
concrete image or inflating its abstract cost is unsafe.

### Sponsor-flow theorem

**Theorem 467.1 (PROVED/EXACT for the declared accounting interface).**  Let
$f(u,v)\geq0$ be supported on $E$ and satisfy

$$
\sum_{v:(u,v)\in E}f(u,v)=c(u)\quad\text{for every }u,
$$

and

$$
\sum_{u:(u,v)\in E}f(u,v)\leq w(v)\quad\text{for every }v.
$$

Then $\operatorname{cost}(P^\#)\leq\operatorname{cost}_R(P)$.

**Proof.**  Sum the demand equalities over $u$, interchange the finite sums,
apply each capacity inequality, and sum over $v$:

$$
\sum_u c(u)=\sum_{u,v}f(u,v)
\leq\sum_v w(v).
$$

No branch or shared node is counted twice because each concrete capacity is a
single global constraint.  QED.

**Theorem 467.2 (weighted Hall characterization).**  Such a flow exists iff
for every $X\subseteq U$,

$$
\sum_{u\in X}c(u)\leq\sum_{v\in N(X)}w(v),
$$

where $N(X)$ is the set of eligible sponsors adjacent to $X$.

**Proof.**  Necessity follows by summing the flow from $X$.  For sufficiency,
build a network with source-to-$u$ capacity $c(u)$, infinite-capacity eligible
edges $u\to v$, and $v$-to-sink capacity $w(v)$.  Every finite cut is bounded
below by total demand exactly when the displayed inequalities hold.  The
max-flow/min-cut theorem gives a flow saturating every source edge.  Rational
weights follow by scaling; integer weights admit an integer flow.  QED.

### Whole-system transfer corollary

Let the legal abstract system contain an image of **every** legal concrete
goal proof, and let every image carry a sponsor certificate.  Then

$$
W^\#(F)\leq W_R(F).
$$

Therefore a genuine abstract lower bound $W^\#(F)>B$ implies
$W_R(F)>B$.  The conclusion is invalid if even one historical rule or legal
goal image is missing.  Spurious abstract proofs only decrease $W^\#$ and are
safe for soundness, although they may prevent proving a useful bound.

### Minimal falsifiers and controls

1. **Local-safe/global-unsafe sharing.**  Two abstract unit charges are both
   eligible only for one concrete unit-capacity shared lemma.  Each charge fits
   individually; together demand 2 exceeds capacity 1.  This is the minimal
   violating Hall cut and rejects tree-unfold double charging.
2. **Valid fractional partition.**  Scale the same concrete unit weight by two
   and give each abstract copy demand one.  Rescaling gives $1/2+1/2=1$ and a
   feasible flow, matching LSPV-4's valid cost partition.
3. **Safe collapse.**  One abstract unit charge eligible for either of two
   concrete unit nodes has a flow and costs 1 versus concrete cost 2.  The
   undercharge is cost-sound but may be semantically spurious.
4. **Context-erasure warning.**  Erasing contexts adds sponsor edges and makes
   a two-by-two example flow-feasible; exact compatibility leaves both charges
   dependent on one sponsor and exposes the overload.  Passing the numeric
   certificate with erased contexts is not semantic proof validity.

### Native-rule transformer obligations

The sponsor interface does not change any rule.  For each authenticated
native transformer it imposes the following accounting condition:

| Historical family | Required sponsor evidence | Status |
|---|---|---|
| source / Resolution | every abstract Resolution charge assigned within the concrete node's capacity; source reads retain IDs | exact byte transformer still OPEN |
| AND3 / DEF facets | all abstract definition/facet charges share the fresh concrete definition-node capacities without overdrawing them | freshness/provenance aided by [P2-L5-466]; grammar OPEN |
| GF(2) | every row conversion/addition/extraction charge sponsored by an actual native paid node; algebraic reuse charged once | shortcut must remain visible; exact full rule OPEN |
| LOCAL-CONVERT | exported/private outputs retain origin and context eligibility; total abstract sub-DAG charge fits converter capacities | historical outputs/facets OPEN |
| split/discharge/reference | zero-cost reuse stays zero; both AND branches and discharge legality preserved; shared capacity global | no silent rule addition; native derivations OPEN |

[P2-L1-542] is a mandatory rule-language control: if its external one-node
`TSEITIN-CLOSE` macro were included in the concrete calculus, the abstract
goal charge must fit that one node.  It is not a historical R_mix341 rule, so
the control diagnoses grammar scope rather than a historical shortcut.

### Independent computation

Producer:
`experiments/review/lspv5_467_sponsor_flow_cost_sound.py`  
Independent verifier:
`experiments/review/verify_lspv5_467_sponsor_flow_cost_sound.mjs`  
Raw:
`results/raw/arc/2026-11-09_1248_LSPV5_467_SPONSOR_FLOW_RAW.json`

All nonempty eligibility graphs with one to three nodes per side were tested,
with abstract demands in $\{1,2,3\}$ and concrete capacities in
$\{0,1,2,3\}$.  Python and independently written Node max-flow/Hall replays
agreed on all 635,532 cases:

| Result | Count |
|---|---:|
| feasible | 128,854 |
| infeasible | 506,678 |
| Hall/max-flow mismatches | 0 |
| individually safe but globally unsafe | 97,001 |

Both implementations accepted the scaled partition, separate-sponsor and
safe-collapse controls; both rejected shared duplication and the exact-context
overload.  SHA-256:
`c0a0afa9037e34bf19b01d7d43503063ba346ef91213c885861e48ed520d0616`
(Python),
`652c6bd91afd3126d700b23a08666be6d1d36af319d32bdfbb6ce50c68a2ba3e`
(Node), and
`b2342fae328d911c484629372ec13776feac51afb8c39ae3bec35b7615b318ba`
(raw JSON).

### Hard-family and shortcut ledger

| Family | Encoding / size | Established scope | Known method | Remaining transfer |
|---|---|---|---|---|
| cubic odd-charge expander Tseitin | edge variable per graph edge; four proper width-3 forbidden-pattern clauses per cubic vertex; $3h/2$ variables, $4h$ clauses, $N=\Theta(h\log h)$ | exponential ordinary shared-DAG Resolution on suitable expanders only | GF(2) elimination; declared mixed AND3/GF(2) proof is linear; external /542 macro is one node in a distinct calculus | sponsor graph for every authenticated historical mixed transformer plus a useful invariant |
| original-variable RUP/CDCL class [P2-L2-525] | source 3-CNF, no fresh variables/RAT/ER/XOR | restricted conflict lower bound via Resolution simulation | restarts, learning, deletion and sharing included; GF(2)/ER excluded | does not cover full R_mix341 or arbitrary SAT algorithms |
| RAT/DRAT-minus firewall [P2-L2-526] | proper original 3-CNF; one model-changing RAT addition and reordered-parity controls | published restricted separation plus checked finite witnesses | RAT action need not have any source-rooted Resolution consequence image | confirms that sponsor eligibility must be proved rule by rule; does not authenticate historical R_mix341 |
| pigeonhole | standard PHP source; any conversion to proper 3-CNF needs cited lower-bound preservation | Haken ordinary Resolution only | Cook extended Resolution short proofs mandatory | no authenticated full mixed retraction |
| local width-three factors [P2-L3-540] | exact 8-bit truth masks for three-variable factors | local exactness requires 255 states under singleton contexts | coarser MAY domains allowed with spurious paths | representation precision is not proof cost or machine time |

Certified UNSAT, restricted proof-size hardness, empirical difficulty and
full-calculus minimum hardness remain distinct.

## Resource ledger

The Python exhaustive run executed 635,532 cases in 9.605 s and reported
10,880 KiB peak RSS.  The raw JSON is 3,728 bytes; producer and verifier are
7,508 and 3,420 bytes.  The Node verifier independently replayed the complete
case set and passed; `/usr/bin/time` was unavailable, so no independent Node
peak-RSS claim is made.  Logical certificate verification is one max-flow or
all-subset Hall check on an explicitly materialized sponsor graph; this does
not bound discovery or representation cost for an asymptotic family.

Source/index/head reads, tracker/main retrieval, literature/repository
retrieval, parsing, case construction, Python verification, Node verification,
output, publication, issue write and readback are separate phases.  External
repository review included ten current heads and actual relevant files; the
CakeML diff was inspected rather than inferred from its title.  No search,
failed policy, cache, retrieval or output work is charged into the ideal
logical proof minimum.  Any implemented upper bound must charge all of them,
plus references, retention/recomputation and simultaneous peak space.

## Tracker effect and precise remaining gap

Material evidence is added as **[P2-L5-467]**, refining the accounting
interface of [P2-C3] and building on [P2-L5-464], [P2-L5-466] and LSPV-4's
cost-partition control.  It does not change the OPEN status of [P2-D1],
[P2-C3], [P2-B1] or [P2-B2].

The immediate gap is to construct semantic transformers and sponsor
eligibility for **every** historical R_mix341 rule and prove that every legal
concrete goal proof receives an image.  Only then can a family-level abstract
invariant be used to prove a superpolynomial minimum.  The noncircular
same-calculus B3 bridge remains separately OPEN.  P versus NP remains **OPEN**.

## Publication and readback

Publication pending conflict-safe current-head merge and full readback.
