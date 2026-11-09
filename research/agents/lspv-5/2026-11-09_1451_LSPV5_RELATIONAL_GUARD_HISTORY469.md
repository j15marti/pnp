# LSPV-5/469: separate legality/history marginals erase the greatest cost-sound charge

**2026-11-09 14:51 PST | Route B independent red team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

Affected proof-chain evidence: new **[P2-L5-469]**, refining [P2-L5-468],
[P2-L1-545], [P2-L2-528], [P2-L3-542] and the still-open [P2-C3].
[P2-D1], [P2-C3], [P2-B1] and [P2-B2] remain **OPEN**.  Historical
$R_{\mathrm{mix341}}$ grammar and weights are unchanged.

## Actual advance

This run proves a smallest relational-abstraction obstruction.  A proof-state
analysis may separately retain every possible logical-legality bit and every
possible paid-history bit, yet lose the correlation that determines the
greatest uniform cost-sound charge.  For one action of positive native weight
$w$, the two relations

$$
X=\{(1,0),(0,1)\},\qquad
Y=\{(1,1),(0,0)\}
$$

have identical logical and history marginals $\{0,1\}$, while their greatest
safe charges are $w$ and $0$.  The Cartesian product of the marginals adds the
spurious legal-and-already-paid pair $(1,1)$ to $X$, forcing zero charge.

For $n$ independent coordinates there are $2^n$ relations with the same two
full-cube marginals and $2^n$ distinct exact charge vectors.  This is a sharp
precision separation for the marginal product.  It is **not** a time, space,
evidence-size or proof-minimum lower bound: the family is represented by an
$n$-bit correlation mask.

## IDEA and falsifiers, fixed before SEARCH

**Initial candidate.** Independent logical and paid-history marginals are not
enough for cost-sound negative-proof tests; the abstraction must retain a
relation between rule legality and whether the corresponding origin is already
paid.

1. **F1:** the marginals determine the greatest safe conditional charge.
2. **F2:** replacing a conditional minimum by the unconditional history
   minimum loses no useful precision.
3. **F3:** enlarging a relation to the Cartesian product of its marginals can
   still assign positive charge safely to every legal concrete transition.
4. **F4:** exponentially many relational behaviors by themselves imply a
   proof-size or machine lower bound.

F1--F3 are falsified symbolically and by two independent executables.  F4 is
falsified by the explicit $n$-bit correlation-mask representation.  The
revised claim is therefore a restricted **necessity-of-correlation** theorem,
not a complexity lower bound.

## SEARCH: continuity, literature and external evidence

### Governing and peer artifacts read

Both live trackers were read completely at immutable preflight head
`e5372075b15512d50c3347d6cdab15aa1d4a774c`: `proof1.txt` blob
`96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, and `proof2.txt` blob
`4106d64f49353c8bd6d5ad8ec9f8615e9ba81744`.  Also read: issue #3 through
1,519 comments; the November 9 abstract-interpretation handoff blob
`8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b`; the November 2 governing
five-role handoff; `AGENTS.md` blob `4ae902888754d0b06ba4ce1aaeca0657a92b46a9`;
`CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`; and
`.codex/skills/pnp-research/SKILL.md` blob
`b8df83a7b0b1428f349b0e02ce1387d979e8db7f`.

The exact current peer reports were read, not inferred from summaries:

- [P2-L1-545], `research/agents/lspv-1/2026-11-09_1400_LSPV1_COMPLETE_UNIFORM_HYPERGRAPH_GAP545.md`: additive atomic potentials can have an unbounded gap in a distinct complete-uniform cover system, while a succinct nonlinear paid-history potential is exact.
- [P2-L2-528], `research/agents/lspv-2/2026-11-09_1413_LSPV2_HORN_SELECTOR_RUP_CHECKPOINT_NPC528.md`: a compact exact guard may represent exponentially many checkpoints; reachability can be NP-complete, but the unrestricted source has a one-record RUP shortcut.
- [P2-L3-542], `research/agents/lspv-3/2026-11-09_1427_LSPV3_PARITY_DEF_FACET_CEGAR542.md`: a missing XOR facet is a sound MAY model overapproximation but cannot be used as an exact Resolution premise.
- [P2-L5-468], `research/agents/lspv-5/2026-11-09_1356_LSPV5_COUNT_ONCE_HISTORY_STATE468.md`: exact deterministic count-once charging needs the paid-history state.
- LSPV-4 cost-partition simulation, `research/review/reports/resource_auditor/2026-11-09_LSPV4_COST_PARTITION_SIMULATION.md`: its sufficient theorem assumes the full concrete state already contains the paid-node set.
- Actual Grok `GROKPROOF/2026-11-09_2015_PROGRESS.md`, blob
  `5610d47e2a78ded4e4e57bc24fca3266e03f42ac`, and actual Claude
  `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`; neither supplies the missing mixed-calculus transfer.

### Primary literature and exact scope

Search queries included “abstract interpretation reduced product Cousot primary
paper”, “trace partitioning abstract interpretation”, “Abstract Conflict
Driven Learning POPL 2013”, “Abstract Satisfaction POPL 2014”, and “Making
Abstract Interpretations Complete”.  Indexed primary-source search was
available; a distinct Google-branded interface was not.

- Cousot & Cousot, *Abstract interpretation* (POPL 1977), models sound
  abstraction by ordered domains and monotone transformers; consistency of an
  overapproximation does not imply completeness.
- D'Silva, Haller & Kroening, *Abstract Conflict Driven Learning* (POPL 2013,
  DOI 10.1145/2480359.2429087), abstracts conflict-driven solver operations.
- D'Silva, Haller & Kroening, *Abstract Satisfaction* (POPL 2014, DOI
  10.1145/2535838.2535868), characterizes model sets using fixed points of
  deduction, abduction and quantification transformers.  It does not assert a
  proof-cost lower bound or same-calculus B3 implication.
- Giacobazzi, Ranzato & Scozzari, *Making Abstract Interpretations Complete*
  (JACM 47(2), 2000), treats pointwise and fixpoint completeness and complete
  shells/cores under stated continuity or monotonicity hypotheses.  Exactness
  of an abstract domain is distinct from its implementation cost.
- Mauborgne & Rival, *Trace Partitioning in Abstract Interpretation Based
  Static Analyzers* (ESOP 2005, DOI 10.1007/978-3-540-31987-0_2), explicitly
  retains history-selected partitions to recover correlations lost by ordinary
  reachability abstraction; its state/traces framework does not prove a proof
  lower bound.

### Required repositories, pinned change-aware

The required repository files were refetched and were unchanged from their
pinned blobs: `konard/p-vs-np/README.md` `0e0ec77f...` and
`scripts/proof_status.json` `93b77ed3...`;
`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` `18d693ea...`;
`meelgroup/frat-xor/format.md` `986a21aa...`;
`tanyongkiam/cake_lpr/README.md` `e94f45e9...`;
`peitl/short-proof/README.md` `93d2090d...`;
`marijnheule/drat-trim/README.md` `eb6ffcc4...`;
`msoos/cryptominisat/README.md` `76369887...`;
`openai/math/README.md` `cc5b0a03...`; and
`anthropics/formal-math/README.md` `1df53bfc...`.
They provide proof formats, implementations or scoped claim ledgers, not the
historical accepted-byte grammar, all-native cost simulation, or B3.

## ITERATE: concrete and abstract domains

Let a complete concrete proof configuration be

$$
s=(F,\Gamma,V,E,D,M),
$$

where $F$ is the authenticated original source, $\Gamma$ records assumption
contexts, $(V,E)$ is the acyclic shared proof hypergraph already constructed,
$D$ is the set of immutable paid origins already charged, and $M$ contains the
typed rule metadata (signed premises, pivots, facets, affine rows, freshness,
exported/private wires and references).  A concrete rule step is legal only
when its full native guard holds.  Its incremental logical charge is zero on a
legal reuse and the historical weight on first insertion.

For the theorem, choose $n$ candidate action identities.  Feature maps give
$g(s)\in G=\{0,1\}^n$, where $g_i=1$ exactly when action $i$ is currently
legal, and $h(s)\in H=\{0,1\}^n$, where $h_i=1$ exactly when its paid origin
is already in $D$.  The concrete uncertainty domain is

$$
\mathcal C=\mathcal P(S),\qquad
\eta(X)=\{(g(s),h(s)):s\in X\}\subseteq G\times H.
$$

The **relational** abstract domain is
$\mathcal A_{\rm rel}=\mathcal P(G\times H)$ ordered by inclusion, with
$\alpha_{\rm rel}=\eta$ and
$\gamma_{\rm rel}(R)=\{s:(g(s),h(s))\in R\}$.  Larger sets are less
precise MAY overapproximations.  The **independent marginal** domain is

$$
\mathcal A_{\rm marg}=\mathcal P(G)\times\mathcal P(H),\quad
\alpha_{\rm marg}(R)=(\pi_G R,\pi_H R),\quad
\gamma_{\rm marg}(A,B)=A\times B.
$$

Thus $R\subseteq\gamma_{\rm marg}(\alpha_{\rm marg}(R))$: the polarity is
a sound MAY overapproximation, but generally not an exact one.

For a fully authenticated concrete rule $r$, the best correct MAY transformer
would be

$$
T_r^\#(A)=\alpha(\operatorname{post}_r(\gamma(A))).
$$

For action $i$ with positive first-use weight $w_i$, define
$\Delta_i(h)=0$ if $h_i=1$ and $w_i$ otherwise.  On a relation $R$ containing
at least one legal pair, the greatest uniform cost-safe lower charge is

$$
c_i^*(R)=
\min\{\Delta_i(h):(g,h)\in R,\ g_i=1\}.
$$

This conditional minimum—not the unconditional minimum over $\pi_HR$—is the
cost component of the best relational transformer.

### Native-rule transformer audit

| Historical or proposed step | Required concrete guard/update | Status in this run |
|---|---|---|
| authenticated source read | exact source bytes/ID, clause identity; no invented paid origin | feature obligation stated; no new grammar |
| paid DEF and facet use | global freshness, exact signed facets/owner, scope; first owner use updates $D$, facet reuse is correlated with owner | historical facet selector bytes **OPEN [P2-D1]** |
| oriented Resolution | both signed parents available in compatible contexts, exact pivot/orientation; fresh conclusion updates $V,E,D$ | generic conditional-charge theorem applies after authentication |
| AND3 | every required premise is an AND hyperedge, local truth-table output and contexts retained; first node use updates $D$ | declared semantic control, accepted-byte coverage incomplete |
| GF(2) | exact affine rows, parity and source provenance retained; first row inference updates $D$ | mandatory shortcut; generic theorem does not omit it |
| LOCAL-CONVERT | exact payload, exported/private wires, source entailment and references; all generated origins updated | grammar/payload bound **OPEN [P2-D1]** |
| zero-cost reference/reuse | same immutable origin, justified context, no new node charge | must retain legality/history correlation |
| split/discharge/weakening | only if natively derivable; branch assumptions and all AND cases retained | not silently added to historical calculus |

This table is an obligation ledger, not a claim that the missing transformers
have been authenticated.  Omitting any legal native rule invalidates a
whole-calculus lower-bound transfer.

## Theorem 469.1: greatest conditional charge

**PROVED/RESTRICTED.**  For every nonempty relation $R$ and action $i$ legal in
at least one represented state, $c_i^*(R)$ is the greatest constant $c$ such
that

$$
c\le\Delta_i(h)
\quad\text{for every }(g,h)\in R\text{ with }g_i=1.
$$

**Proof.**  The displayed minimum is at most every member of the finite set,
so it is safe.  Any larger constant exceeds its minimum-achieving member and
is unsafe.  This also gives the cost inequality needed for a negative-proof
transfer: if every concrete transition is represented, its abstract charge is
at most its concrete incremental charge.  Summing in a topological order of
the distinct nodes of a shared proof DAG preserves count-once charging;
multi-premise legality remains an AND guard.  Therefore every concrete proof
$P$ maps to an abstract proof $P^\#$ with

$$
\operatorname{cost}(P^\#)\le\operatorname{cost}_R(P).
$$

Only after complete goal and rule coverage is proved does an abstract minimum
greater than $B$ imply that no concrete proof of cost at most $B$ exists.

## Theorem 469.2: marginal indistinguishability

**PROVED/RESTRICTED.**  Separate logical and paid-history marginals do not
determine $c_i^*$.  The one-coordinate relations $X,Y$ displayed above have
the same marginals but $c^*(X)=w$ and $c^*(Y)=0$.  Hence any charge function
depending only on those marginals and safe for all compatible relations must
return zero.

**Proof.**  In $X$, the unique legal pair is $(1,0)$, so the action is unpaid
and costs $w$.  In $Y$, the unique legal pair is $(1,1)$, so it is already
paid and costs zero.  Both projections are $\{0,1\}$.  The product
concretization of $X$ contains $(1,1)$ and therefore safely charges at most
zero.

For $A\subseteq[n]$, let

$$
R_A=\prod_{i=1}^n
\begin{cases}
X_i,&i\in A,\\
Y_i,&i\notin A.
\end{cases}
$$

Every $R_A$ has $\pi_G(R_A)=G$ and $\pi_H(R_A)=H$, while

$$
c_i^*(R_A)=
\begin{cases}
w_i,&i\in A,\\
0,&i\notin A.
\end{cases}
$$

Thus identical marginals hide $2^n$ distinct exact charge vectors.  The
correlation set $A$ itself is an $n$-bit representation, so exponential
semantic multiplicity does not imply exponential physical resources.

### Shared branches and abstract satisfaction

Alternative branches join by union of reachable concrete pairs, preserving
each branch's legality/history correlation.  Projecting the union to separate
marginals and then taking their Cartesian product creates cross-branch pairs
that never existed.  Deduction, propagation, learning, abduction and
quantification may be sound at the model level while still losing this
cost-critical relation.  A reduced product, trace partition or equivalent
relational invariant is necessary for positive precision here; it is not
sufficient for a mixed-calculus lower bound.

Semantic bottom, bounded-proof absence and abstraction indecision remain
separate.  This theorem proves no semantic UNSAT fact.  Conversely, failure of
the marginal domain to prove a positive lower charge is loss of precision,
not evidence that a cheap concrete proof exists.

## Independent computation and resource ledger

The Python producer exhaustively enumerated every $R_A$ through $n=10$:
2,046 correlation masks and 1,398,100 relational states, with 79,913
assertion groups and five malformed-input rejections.  The independent V8
implementation used different code and weights through $n=9$: 1,022 masks,
349,524 states, 27,662 checks and four malformed rejections.  Both found all
$2^n$ exact charge vectors and the zero marginal-only vector at every tested
dimension.

| Artifact / phase | Exact evidence |
|---|---|
| Python producer | 5,691 bytes; SHA-256 `124a1bd8d39b6a9e78d826c86e2828e9933be90d8db5617cbdc754602276ac2b`; 2.962 s shell wall rerun |
| independent V8 | 2,932 bytes; SHA-256 `ede3eaf9d69b65ec3c4859e087de0f02201bb24d8ed96c51009d482769b364fb`; 0.441 s shell wall rerun |
| raw result | 5,217 bytes; SHA-256 `eff4444e1a9c1e1773136e287785fbc17004da4e3b740712d2a85a4796d7dd00` |
| logical work | restricted exact minima above; no historical mixed proof computed |
| evidence bits | explicit scripts and JSON only; discovery/search and GitHub reads are separate |
| peak space | no trustworthy process peak was available because `/usr/bin/time` was absent; sparse in-memory enumeration was used |
| publication work | source/index/head reads, blob construction, lease update and full readback charged separately in receipt |

The ideal proof minimum excludes discovery cost.  An implemented upper-bound
algorithm would have to charge parsing, relation construction, refinement,
lookup, caches, failed paths, output and simultaneous memory.

## Established-family / shortcut ledger

| Family / encoding | Established theorem and model | Mandatory shortcut / remaining transfer |
|---|---|---|
| unary PHP, ordinary CNF | Haken exponential ordinary shared-DAG Resolution lower bound; a strict-3CNF preservation theorem was not used here | Cook ER is the stronger-system control; no all-mixed transfer |
| odd cubic expander Tseitin, four strict3 facets per vertex | exponential ordinary Resolution for appropriate expanders | declared /341 AND3+GF(2) proof has $4h-1$ paid nodes; defeats a mixed exponential claim |
| compact mod-3 adders | project ER2 constructions are upper controls in their declared calculus | native LOCAL-CONVERT/DEF simulation and source entailment remain open |
| Horn/RUP selector [P2-L2-528] | checkpoint choice NP-complete in its policy class | unrestricted original source has a one-record RUP shortcut |

Certified UNSAT, restricted proof hardness and empirical solver difficulty are
not conflated.  No new 3-CNF hard family was invented.

## Tracker decision, status and remaining gap

This is a material dependency refinement of [P2-C3], so [P2-L5-469] is
appended to `proof2.txt`.  `proof1.txt` has no material change.

**Actual advance:** a symbolic and independently checked theorem proving that
the independent marginal product of rule legality and paid history can erase
the greatest cost-sound charge, even while each marginal is exact.

**Verification:** symbolic proofs above; Python and independent V8 finite
replay; mandatory controls and malformed cases included.  No authoritative
historical checker executed.

**Precise remaining gap:** authenticate every historical native transformer
and construct a source/context/provenance/history relational abstraction with
complete goal coverage and cost nonexpansion, then prove a superpolynomial
abstract minimum surviving GF(2), ER, RAT/deletion, LOCAL-CONVERT, nonlinear
and shared-DAG shortcuts.  Separately, prove a noncircular same-calculus B3.
[P2-D1], [P2-C3], [P2-B1], [P2-B2] and P versus NP remain **OPEN**.

Publication/readback status is recorded in the accompanying receipt.
