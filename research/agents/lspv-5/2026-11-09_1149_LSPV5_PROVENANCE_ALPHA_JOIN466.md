# LSPV-5 / 466 — provenance-aware alpha join at shared-DAG reconvergence

**Role:** LSPV-5 independent red team, Route B primary  
**Pacific time:** 2026-11-09 11:49 PST  
**Status:** **PROVED/RESTRICTED + COMPUTATIONAL**  
**Global status:** P versus NP remains **OPEN**.

## Actual advance

Independent branch-local alpha canonicalization is not compositional at a
reconvergence.  It can (i) identify two different paid auxiliary origins and
thereby undercharge the union, or (ii) give two names to one shared ancestor
and thereby lose count-once sharing.  Merely putting every branch in a disjoint
namespace repairs (i) but necessarily duplicates shared ancestors.

The exact name-identity repair is a provenance join: identify two branch
occurrences iff they carry the same immutable definition origin; inject all
other origins into disjoint namespaces.  For arbitrary nonnegative origin
weights it preserves the count-once union cost exactly.  This is the
name/provenance component of the single-global-permutation discipline in
[P2-L1-541].  It does **not** establish historical rule semantics, source
entailment, legal assumption discharge, or a full-calculus lower bound.

## IDEA

### Initial hypothesis

Assume each paid definition occurrence has an immutable origin and source
identifiers are fixed.  A branch-local canonicalizer that renames the first
live private origin to `a0`, the second to `a1`, and so on cannot safely be
joined using only those local names.  A global provenance quotient should be
both collision-free and exactly count-once.

### Precise falsifiers

1. Equal branch-local canonical names always imply equal concrete origins.
2. Identifying different private origins cannot reduce paid union cost or
   permit cross-definition reuse.
3. Freshening the complete namespace of every branch never duplicates a
   common ancestor.
4. Historical auxiliary freshness and shared reconvergence are irrelevant to
   [P2-C3]/[P2-D1].

Falsifiers 1--3 fail by explicit witnesses below.  Falsifier 4 is rejected
only at the abstract-interface level: the exact historical grammar and checker
remain unavailable, so no stronger authentication claim is made.

## SEARCH

### Governing project evidence read

Fresh main at start: `e835d16134a5f241d89d964d7103bea4ce69264a`.
Both trackers were read completely: `proof1.txt` blob
`96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and `proof2.txt` blob
`1a87cf2b7c62641aea2d937ca48249e2477c3acc`.  Current issue #3, the five-role
handoff, AGENTS.md, CODEX.md, `.codex/skills/pnp-research/SKILL.md`, actual
Grok and Claude files, LSPV-1/541, LSPV-3/539, LSPV-2/524, and LSPV-5/465 were
read.  Exact relevant tracker IDs are [P2-D1], [P2-C3], [P2-B1], [P2-B2],
[P2-L1-541], [P2-L5-463], [P2-L5-464], and [P2-L5-465].

The full /541 report is stronger than its short tracker summary: its finite
budget cutoff already assumes positive lower-bounded non-source cost and no
zero-cost action carrying unbounded fresh syntax.  Therefore an unbounded
zero-cost allocator is **not** a counterexample to /541 as actually stated.
The revised target is the explicit join obstruction that explains why /541
requires one global permutation rather than independent branch maps.

### Primary literature

* Cousot and Cousot, *Abstract Interpretation* (POPL 1977),
  <https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml>: the soundness
  direction is concrete-to-abstract overapproximation; a missing concrete
  transition invalidates a negative certificate.
* Gabbay and Pitts, *A New Approach to Abstract Syntax with Variable Binding*,
  Formal Aspects of Computing 13 (2002), DOI
  <https://doi.org/10.1007/s001650200016>: alpha-equivalence is represented by
  permutation actions and freshness, not by unrelated local string choices.
* Parrow et al., *Modal Logics for Nominal Transition Systems* (CONCUR 2015),
  DOI <https://doi.org/10.4230/LIPIcs.CONCUR.2015.198>: nominal states and
  labels support equivariant transition/bisimulation reasoning.  This is a
  conceptual control, not an R_mix341 theorem.
* D'Silva, Haller and Kroening, *Abstract Conflict Driven Learning* (POPL
  2013), <https://www.kroening.com/publications/view-publications-dhk2013-popl.html>,
  and *Abstract Satisfaction* (POPL 2014),
  <https://www.kroening.com/publications/view-publications-dhk2014-popl.html>:
  deduction, abduction, propagation, learning and refinement operate relative
  to a specified abstract domain.  They do not justify erasing provenance or
  import a proof-complexity lower bound.

Google-compatible primary search was available through the web search
service.  Queries covered nominal alpha equivalence, nominal transition
systems, and SSA branch joins.  Search snippets were not treated as theorem
authority.

### Required repository review

Pinned current heads and inspected paths:

| Repository | Head | Inspected evidence | Relevance |
|---|---|---|---|
| `konard/p-vs-np` | `ecedd2b45f1c524d85c00b2da27a9c140025550c` | `README.md` | Explicit finite-machine scope; no P-vs-NP authority. A guessed root `PROOF_STATUS.md` returned 404 and is recorded as unavailable. |
| `blkph0x/p-vs-np-proof-research` | `7dedc73f758dfbdc072e7aa29dfc08505761ebd5` | `METHOD_INDEX.md` | Status ledger expressly scopes “proved”; no provenance join theorem for R_mix341. |
| `meelgroup/frat-xor` | `18cd6bc17af10a9891c10a846ce966166f9fe0dc` | `format.md` | XOR steps have explicit checker semantics; a theory tag is not permission for an uncharged shortcut. |
| `tanyongkiam/cake_lpr` | `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2` | `README.md` | Built checker and toolchain pins; no historical R_mix341 accepted-byte execution. |
| `peitl/short-proof` | `2c524cfceecf68b56f51d23f6b63255b502856d3` | `README.md` | Finite shortest-Resolution encoding; its scope is not the mixed calculus. |
| `MassimoLauria/cnfgen` | `24e633bdbed0d0998493bee99c42faf480c7dc96` | `cnfgen/families/tseitin.py` | Exact odd-charge Tseitin instance generator control. |
| `openai/math` | `4eaee87548250b2682affda7d05d947c05554bae` | `README.md` | Repository calls some outputs raw research data; no transfer authority. |
| `anthropics/formal-math` | `16a5ce41304fcdaea4e0be7c132e1c361dc26da5` | `README.md` | Per-project Lean/toolchain pins; formalization badges do not imply this bridge. |

The two required P-vs-NP repositories and the rotating proof/checker/family/
formalization corpus showed no relevant delta that closes [P2-D1], [P2-C3],
[P2-B1], or [P2-B2].

## ITERATE

### Concrete and abstract domains

For a fixed source $F$, a concrete proof state is an acyclic directed
hypergraph whose occurrence vertices carry

$$
(\text{native rule},\Gamma,\text{source provenance},\text{name},
 \text{definition origin},\text{premises},w_R).
$$

The concrete join of two branch sub-DAGs is their union, identifying the
already shared occurrence/origin vertices.  Its paid definition cost is

$$
\operatorname{cost}_O(P_0\cup P_1)
=\sum_{o\in O_0\cup O_1}w(o).
$$

The abstract domain keeps the occurrence hypergraph and contexts, replaces
concrete spellings by atoms, and retains an immutable origin map.  The
abstraction $\alpha$ maps each concrete origin to one abstract atom globally.
The concretization $\gamma$ contains all source-fixing nominal permutations
that preserve origin equality, rule labels, hyperedges, and contexts.  Thus
$P\in\gamma(\alpha(P))$; the approximation direction is an overapproximation
of concrete spellings, not an erasure of origin identity.

At a join, form the quotient of the disjoint branch union by

$$
(0,o)\sim(1,o')\quad\Longleftrightarrow\quad o=o'.
$$

This is the provenance pushout/union: common origins are identified exactly;
private origins remain distinct.  The abstract charge is the first-use weight
of each quotient origin.

### Restricted join theorem

**Theorem (proved/restricted).**  For any two branch origin sets $O_0,O_1$
and nonnegative origin weights $w$, the provenance join preserves origin
identity iff it is concrete identity and satisfies

$$
\operatorname{cost}^{\#}(\alpha(P_0)\sqcup_O\alpha(P_1))
=\sum_{o\in O_0\cup O_1}w(o)
=\operatorname{cost}_O(P_0\cup P_1).
$$

**Proof.**  The quotient classes are in bijection with $O_0\cup O_1$: the two
copies of an origin in the intersection form one class, and each private
origin forms one class.  Summing $w$ once per class is therefore exactly the
union sum.  Equality of quotient classes is equality of immutable origins by
construction.  QED.

This proves the cost inequality required for this component with equality.
It does not prove that conclusions, contexts or source entailment are legal.

### Minimal counterexamples

1. **Private collision.**  Left has origin $u$ with definition $u:=x$; right
   has different origin $v$ with $v:=\neg x$.  Each first private origin is
   locally `a0`.  Syntactic union identifies them and charges one unit instead
   of two, while also allowing incompatible definitions to leak.
2. **Shared split.**  Left encounter order is $(p,s)$ and right is $(s,q)$.
   The same shared origin $s$ is locally `a1` and `a0`.  A name-only join no
   longer recognizes the shared ancestor.
3. **Blind duplicate.**  Both branches contain only shared origin $s$.
   Disjoint branch namespaces charge two units although the concrete shared
   DAG charges one.

Hence neither local-name equality nor branch-wide disjoint freshening is a
cost-sound general join.

### Transformer audit boundary

The repair constrains every relevant native transformer without changing the
historical calculus:

| Rule family | Required abstract action | Current status |
|---|---|---|
| source / Resolution | preserve source IDs, occurrence premises and context; create no fresh definition origin | interface specified; historical bytes not replayed |
| DEF facets / AND3 | allocate one globally fresh immutable definition origin and retain its defining inputs/facets | interface specified; exact historical selectors still OPEN |
| GF(2) | retain row/source provenance and any paid auxiliary origin; never merge merely equal semantic rows | interface specified; exact mixed simulation OPEN |
| LOCAL-CONVERT | retain exported/private-wire origin maps through conversion and reconvergence | precise historical clauses still OPEN under [P2-D1] |
| split/discharge | preserve $\Gamma$ and all AND obligations; join only compatible discharged facts | no silent rule added; native derivation remains OPEN |

An abstract-satisfaction or ACDL layer may propagate or learn over this domain,
but any transformer that forgets origins can reproduce the private collision;
one that namespaces all branches can reproduce the shared double charge.

### Independent computation

Producer:
`experiments/review/lspv5_466_provenance_alpha_join.py`  
Independent verifier:
`experiments/review/verify_lspv5_466_provenance_alpha_join.mjs`  
Raw:
`results/raw/arc/2026-11-09_1149_LSPV5_466_PROVENANCE_ALPHA_JOIN_RAW.json`

For five origins there are 325 nonempty partial-permutation branches and
105,625 ordered branch pairs.  Results:

| Check | Count |
|---|---:|
| local-name collision | 103,340 |
| shared-origin split | 99,360 |
| definite naive cost undercount | 27,980 |
| blind disjoint-namespace overcount | 104,645 |
| provenance cost failures | 0 |
| provenance identity failures | 0 |

The Node verifier independently replayed the three minimal controls and the
aggregate zero-failure predicates: PASS.  SHA-256 values are
`e378682590315fe7a104f26558b2b518102a3b9ebddd2569b2134c6656c8490d`
(Python),
`9ba283f5886c9f7d63a357a41c20acf4a3b2b7cea313f85f4a9ffc59c6b368b9`
(Node), and
`a5322dfc748ba461d8107adfc7705f95bbaf244b7ce053882cf5d017a15c9255`
(raw JSON).

### Hard-family and shortcut ledger

| Family | Exact encoding / size | Established theorem scope | Known shortcut | Remaining transfer |
|---|---|---|---|---|
| cubic odd-charge Tseitin 3-CNF | one edge variable; four width-3 clauses per degree-3 vertex forbid assignments of the wrong parity; odd total charge is UNSAT; $m=4|V|$ clauses | exponential ordinary DAG-Resolution size on suitable expanders (**PROVED-RESTRICTED**, not all algorithms) | GF(2) Gaussian elimination / native XOR is polynomial | prove cost-nonincreasing coverage of every historical mixed rule, including provenance-aware join |
| pigeonhole controls | standard pigeon and collision clauses; non-3 clauses require a lower-bound-preserving conversion, not mere equisatisfiability | Haken ordinary Resolution lower bound only | Cook extended Resolution is mandatory short-proof control | no full R_mix341 retraction authenticated |
| mod-3 / ER controls | prior exact local one-hot adder packets and fresh-origin definitions | local upper-bound control only | compact adders, sharing, extension variables | provenance join must not merge independent adder origins or split shared gates |

Certified UNSAT, restricted proof-size hardness, and empirical solver behavior
remain distinct.

## Resource ledger

The exhaustive Python run used 0.648 s wall time and 10,624 KiB reported peak
RSS; the raw payload is 3,428 bytes.  Producer/verifier source sizes are 6,465
and 943 bytes.  Logical join work is one set-union/quotient pass plus one charge
per distinct origin; the experiment explicitly materializes all 105,625 test
pairs.  Retrieval included the two complete trackers, current head/tree,
issue #3, governing reports, eight external repository heads and inspected
files, and primary-paper pages.  The failed guessed `PROOF_STATUS.md` fetch is
recorded above.  Network/source reads, parsing, local generation, verification,
publication, issue write and final readback are separate phases; no discovery
cost is charged into the ideal proof minimum.

## Tracker effect and remaining gap

Material evidence is added as **[P2-L5-466]** and refines [P2-C3] and [P2-D1].
It independently validates the global-permutation proviso of [P2-L1-541] and
is compatible with the occurrence/history separation in [P2-L5-464].  It does
not alter [P2-B1] or [P2-B2]: both remain **OPEN**.

The precise remaining gap is a rule-by-rule, source-authenticated,
context-correct abstraction/normalization for **every** historical
R_mix341 rule with a noninflating cost map, followed by a genuine lower bound
on the resulting abstract minimum.  A noncircular same-calculus B3 transfer is
also still absent.  P versus NP remains **OPEN**.

## Publication and readback

Conflict-safe publication advanced `main` from
`e835d16134a5f241d89d964d7103bea4ce69264a` to artifact commit
`a829e8a7eb7924c50effaa6e4a19896f161dbab1` using an expected-head lease.
The updated `proof2.txt` blob is
`5d67fd46cd8091c3b9ee7d798d07b3f1cd605b63`; `proof1.txt` remained exactly
blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`.  `main.tex` was rebuilt from
the complete 1,811,818-byte prior file and only the unique LSPV-5-owned region
changed; complete readback matched the constructed 1,813,117-byte file and
both outside-region byte strings exactly.  Every new artifact, the tracker
append, and the manuscript insertion matched full readback byte-for-byte.

Issue #3 comment `6750024786` was posted and REST readback matched the exact
saved outbox; URL
<https://github.com/j15marti/pnp/issues/3#issuecomment-6750024786>.
No task, title, schedule, timezone, enabled state, role allocation, grammar or
weight changed.
