# LOCALSHIELD1 T5 mixed-fiber shield audit (2026-11-19)

**Mission:** fixed five-symbol tournament CSP, $R(a,b)\iff(b-a)\bmod5\in\{1,3\}$, SAT-only witnesses for $G=H-e$ with intrinsically edge-minimal UNSAT $H$, connected, increasing *underlying undirected* girth. **P versus NP remains OPEN.** No unrestricted lower bound or critical-promise NP-hardness is claimed.

## Exact theorem LS-MIX1: expansion-based shielding is deletion-robust, not edge-critical

Let $D=(V,E)$ be any loopless oriented source. Let $A$ have $N\ge5$ vertices and a binary relation $Q\subseteq A^2$, and set $k=\lceil N/5\rceil$ and
$$
 h_5(Q)=\min_{U,W\subseteq A:\ |U|,|W|\ge k}|Q\cap(U\times W)|.
$$
Form an $N$-fiber lift $L$ with blocks $V_u=\{u\}\times A$. For each original arc $e=(u,v)$, use **explicit** bijections $\alpha_{e,u}:A\to V_u$ and $\alpha_{e,v}:A\to V_v$, inserting precisely the $q=|Q|$ arcs $\alpha_{e,u}(a)\to\alpha_{e,v}(b)$ for $(a,b)\in Q$. The blocks remain disjoint; no edge gadget is appended to an unrelated source.

**PROVED:** For every deletion set $F\subseteq E(L)$ with $|F|<h_5(Q)$,
$$
 L-F\longrightarrow T_5\quad\Longleftrightarrow\quad D\longrightarrow T_5.
$$
**Proof:** A $D\to T_5$ witness lifts by the block projection $\pi(u,a)=u$, regardless of $F$. Conversely let $\varphi:L-F\to T_5$. On each block $V_u$, choose a most frequent $\varphi$-color $c_u$; at least $k$ vertices have this color. For any original arc $e=(u,v)$, the inverse images under its two edge-specific bijections of these monochromatic block subsets are $U,W\subseteq A$ with $|U|,|W|\ge k$. They contain at least $h_5(Q)$ distinct $Q$-arcs. Since $|F|<h_5(Q)$, at least one corresponding lifted arc survives, proving $R(c_u,c_v)$. Thus $u\mapsto c_u$ satisfies every original constraint. QED.

**Consequences (PROVED):**
1. If $D$ is UNSAT and $h_5(Q)\ge2$, deleting *any single arc* of $L$ leaves an UNSAT instance. In fact at least $h_5(Q)$ arc deletions are needed before $L$ could become SAT. **A redundant fiber shield of this type cannot itself be an edge-minimal UNSAT $H$**. This is an exact obstruction to the proposed criticalization route, not a general obstruction to high-girth critical graphs.
2. Fiber-majority decoding translates any valid lifted witness into an original witness. It is source-aware: the projection, per-edge bijections, source records, and all incurred accesses must be accounted for. Recognition/extraction cannot be treated as free advice.
3. For an $\varepsilon$-expander relation $Q$, $|Q(U,W)|\ge |Q|(|U||W|/N^2-\varepsilon)$. Thus $h_5(Q)\ge\lceil(1/25-\varepsilon)|Q|\rceil$ (with the integer/boundary convention adjusted for strict inequalities). For fixed girth and $\varepsilon<1/25$, Kun's deterministic twisted-product construction provides high **incidence/undirected** girth and preserves T5 SAT status, with sufficiently large $Q$ ensuring deletion robustness. This imports Kun's theorem for fixed girth; it is **not** a uniform growing-girth or critical-promise hardness theorem. The proof of LS-MIX1 does not assume any girth.

**Status of criticalization:** Any edge-minimal UNSAT subgraph pruned from $L$ must discard at least $h_5(Q)-1$ lifted arcs (because every smaller deletion leaves UNSAT); pruning may lose the majority-decoding invariant and selecting a critical core may require nonpolynomial decisions. It is **OPEN** whether a polynomial-time, witness-preserving *intrinsically critical* shield exists without external hard attachments.

## Exact theorem LS-PATH2: long path shields erase every terminal constraint

Traverse an arbitrary oriented path of length \(\ell\). A forward-traversed arc permits increment \(\{1,3\}=1+2\{0,1\}\) in \(\mathbb F_5\); a backward-traversed arc permits \(\{2,4\}=2+2\{0,1\}\). If \(b_i\in\{1,2\}\) records the traversal direction, the exact set of endpoint differences is
$$
 \Delta_\ell=\left\{\sum_{i=1}^\ell b_i+2j\pmod5 :j=0,\dots,\ell\right\},
 \qquad |\Delta_\ell|=\min(5,\ell+1).
$$
All values in the set are constructive: choose exactly (j) arcs' larger increments. **PROVED:** for \(\ell\ge4\) every pair of endpoint colors extends over the path, for every arc orientation. Replacing each source arc by a private path of length at least four therefore produces an instance with a direct linear-time witness generator (assign original vertices zero and fill each path). It cannot preserve T5-SAT decision difficulty or witness difficulty. Paths of length 2 or 3 admit respectively three or four endpoint differences and cannot individually realize the two-valued original relation. This falsifies a naive high-girth shield by long subdivisions, not all branched or expander shields.

## Finite independent algorithmic checks

Reproducer: `experiments/localshield1_t5_mixedfiber_20261119.py` (Python standard library; exhaustive tests and a separate AC3+DFS solver). On the fixed T5 relation:
- Enumerating all \(3^6=729\) loopless labeled orientations on four vertices yields **48 edge-minimal UNSAT** sources (each with five arcs). One chosen $D$ has arcs `[(0,2),(0,3),(1,2),(3,1),(3,2)]`. Its five edge-deletion witnesses are `[(0,1,4,3),(0,0,3,2),(0,1,1,3),(0,0,1,3),(0,2,3,1)]`. Each is independently verified, and its rotations provide five distinct witnesses.
- Exhaustive orientation-sign transfer sets for paths of lengths 1..6 verify sizes 2,3,4,5,5,5 respectively.
- Base $A=\{0,\dots,5\}$, $Q=\{(a,b):a\ne b\}$: $q=30$, $k=2$, exhaustive all qualifying subset pairs give $h_5(Q)=2$. Identity-bijection lift of the above critical $D$ has **24 vertices / 150 arcs**; an independent domain-propagation-and-backtracking solver certifies all 150 one-arc-deleted lifts UNSAT, with 900 total DFS nodes and zero failures. The concrete base has short cycles and **does not** test high undirected girth.
- These finite computations corroborate but do not establish the general LS-MIX1 theorem; the mathematical proof above does.

## Full accounting, quantifiers, and adversarial checks

Let $n=|V(D)|,m=|E(D)|,q=|Q|$. Fully materialized output costs (nN) vertices and (mq) arcs, with source and arc endpoints stored at \(\Theta$(nN+mq)\log(nN)$\) bits, plus up to \(O$mN\log N$\) bits for explicit edge-specific permutations, depending on encoding. Construction must read $D$, generate $Q$, compute and validate the twists (including actual girth), and emit the entire output. Witness verifier must read the complete instance/answer, not only the majority projection; the projected source answer costs \(\Theta$n\log5$\) bits. An annotated reduction can extract majorities in \(O(nN+m)\) additional operations after loading the charged records, plus conventional verification. For fixed \(g\), Kun's construction is polynomial, but a bound uniform in a growing \(g$n$\) is not obtained here.

**FALSIFIED:** four-or-more subdivisions preserve T5 edge constraints; an expander-backed lift with $h_5\ge2$ is intrinsically edge-critical merely because its source is.

**PROVED:** deletion-resilience/majority-decoding theorem; exact oriented-path transfer; explicit 4-vertex critical controls.

**CONDITIONAL:** availability of a fixed-undirected-girth deterministic twisted lift follows from Kun's cited construction, not from our finite base test; high-girth edge-critical witness hardness would require a new source-aware reduction and a valid quantifier bridge.

**OPEN:** polynomial uniform intrinsically critical SAT-only witness-search reduction; growing-girth hardness; any representation-independent worst-case superpolynomial lower bound. **P versus NP OPEN.**

## Literature / independent audit boundary

1. Gábor Kun, *Constraints, MMSNP and expander relational structures*, Combinatorica (2013), Theorem 2, Lemma 14. https://arxiv.org/abs/0706.1701 . Kun's relational girth uses incidence cycles, suited to the requested undirected girth.
2. P. Mark Kayll and Michael Morris, *On colouring oriented graphs of large girth* (2023), Theorem 1.1. https://arxiv.org/abs/2307.09461 . **Caution:** its Section 2 explicitly defines girth using *directed* cycles, so it must not be silently used as an undirected-girth source, and its main lift is probabilistic/nonconstructive.
3. Cranston, Li, Su, Wang, Wei, *Orientations of 10-Edge-Connected Planar Multigraphs and Applications* (Mar 2026), https://arxiv.org/abs/2603.24292 . The planar high-girth corollary concerns some five-vertex tournament, **not explicitly the fixed $T_5$**. No fixed-T5 impossibility is inferred from it.

The source literature and repository predecessor `research/agents/cross-track/2026-11-17_2332_T5_CRITICAL_GIRTH55_STATUS.md` were read. This report is a **self-audited mathematical argument with finite independent-algorithm checks**, not an independent external referee audit. Next blocker: find a polynomial uniform criticalization preserving *source witness decoding* despite the necessary loss of the $h_5\ge2$ fiber-mixing margin; attempt source-aware DP/treewidth and compact transfer-circuit counteralgorithms first.
