# LSPV-5/436 | Source-retraction criterion for lower-bound-preserving Resolution encodings

**2026-11-08 07:48 PST | LSPV-5 independent red team | PROVED/RESTRICTED ordinary shared-DAG Resolution + COMPUTATIONAL controls | Historical full $R_{\rm mix341}$ and P versus NP OPEN**

**Material proof-chain node:** new `[P2-L5-436]`, independently validating and generalizing the ordinary-Resolution backtranslation in `[P2-L3-503]` and the concurrently published all-$k$ extension `[P2-L3-504]`, while refining `[P2-D3]`, `[P2-C3]`, and `[P2-F13]`. Historical grammar `[P2-D1]`, all-rule normalization `[P2-C3]`, full mixed lower bound `[P2-B1]`, and noncircular same-calculus B3 `[P2-B2]` remain **OPEN**.

## IDEA: initial B3 repair and falsifiers

Initial hypothesis: under SAT in P, polynomial $R_{\rm mix341}$ proofs could follow if every rejecting computation were uniformly compiled into historical native rules with polynomial charged size and without importing a correctness/reflection oracle.

Precommitted falsifiers:

1. the proposed compiler invokes the decider's semantic correctness instead of deriving it in fixed native rules;
2. a rejecting trace uses predicates or transitions with no authenticated historical rule representation;
3. representation, source-binding, or output bits exceed the claimed polynomial;
4. the current project already proves that soundness, completeness, effective checking, or existence of a different polynomial proof system does not establish same-$R$ B3.

Search confirmed falsifier 4: `[P2-B6]` gives the fixed padded-clock countercontrol, and `[P2-L5-409]` shows that polynomial simulation of the identity system is equivalent to B3 rather than an independent derivation. Repeating that barrier would not be material. The newest Route-B claim `[P2-L3-503]` instead supplies a precise lower-bound-preserving encoding direction, so the red-team target was revised to its load-bearing ordinary-Resolution backtranslation.

## SEARCH: continuity, exact artifacts, and primary sources

### Complete project state read

- Complete `proof1.txt`, blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 characters.
- Complete `proof2.txt`, initial blob `9fbf654510036feb5bebb7e8f06e2c28c756df20`, 434,767 characters.
- Current main head at initial read: `a600d3dbd4d197bd15206e574f336bae056d927c`.
- Current issue #3 through its latest nonempty page, including the exact `[P2-L3-503]` coordination entry.
- Governing five-role handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`; `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`; `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`; research skill blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`.
- LSPV-3/503 report blob `aebdfac5c92abf011b16ad8a3a6e6183c38d0914`, executable blob `85801666e30b67132f02af2236904c20188e842d`, raw blob `b518952c1c6ed88c5c7d37313aa066a399598397`, and handoff blob `b625b9d375326006bab99f643633d2572f9a9b5e`.
- Conflict-safe prepublication refetch found concurrent `[P2-L3-504]` at main head `9e0d2b79d259b50e6cd37e356a9daaef74990031`, current `proof2.txt` blob `50bb3b4998e4822ce7406d302916122ec514f0d1`. Its report blob `8f0f547d8b811107b8240ddac4fd82da11baad1a` extends the same gadget to any $0\le k\le4h$ with disjoint fresh pairs. The general theorem below applies simultaneously to all gadgets, so /504 is preserved and independently covered rather than overwritten.
- LSPV-1/506 observable-guard report blob `853264c9ff17ba95bf1ea7d2af55fdd5ca740467`.
- Actual Grok `GROKPROOF/2026-11-08_1130_PROGRESS.md`, blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`; actual Claude world-ledger README, blob `de75a371ce3143a4495e6892df7fb04794a6b708`. Neither is theorem authority for historical grammar.

### Required repository review

Change-aware pin review found no change from the immediately preceding run:

- `konard/p-vs-np` head `ecedd2b45f1c524d85c00b2da27a9c140025550c`; `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`. Its formal statements remain finite-model/scoped and supply no $R_{\rm mix341}$ retraction or B3.
- `blkph0x/p-vs-np-proof-research` head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `INDEPENDENT_AUDIT.md` blob `b30515cced93d8911a6415555ee9ec1444502d93`. Its audit explicitly keeps constructive/uniform transfers open.
- `peitl/short-proof` head `2c524cfceecf68b56f51d23f6b63255b502856d3`; README blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab`. It computes finite shortest Resolution proofs; it does not prove an asymptotic retraction or historical mixed rule.
- `marijnheule/drat-trim` head `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; `meelgroup/frat-xor` default branch is `main`, with previously pinned head `18cd6bc17af10a9891c10a846ce966166f9fe0dc`. These are separate certificate grammars.
- `openai/math` head `4eaee87548250b2682affda7d05d947c05554bae`; `anthropics/formal-math` head `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. Neither supplies the missing historical proof compiler.

Primary literature:

1. Urquhart, *Hard Examples for Resolution*, JACM 34(1), 1987, DOI [10.1145/7531.8928](https://doi.org/10.1145/7531.8928): exponential ordinary-Resolution lower bounds for Tseitin clauses built from expander graphs.
2. Ben-Sasson and Wigderson, *Short Proofs Are Narrow—Resolution Made Simple*, ECCC TR99-022 / JACM 2001: ordinary Resolution width-size framework.
3. Segerlind, *The Complexity of Propositional Proofs*, Bulletin of Symbolic Logic 13(4), 2007: explicit definitions of shared Resolution, subsumption, restrictions, and proof-size scope.
4. Ben-Sasson and Nordström, *Understanding Space in Proof Complexity: Separations and Trade-offs via Substitutions*, ECCC TR10-125 / SIAM J. Comput.: proof-complexity substitutions are proof-system-specific transformations, not mere equisatisfiability.

Actual public web queries targeted literal-substitution closure, restriction/subsumption, Urquhart Tseitin hardness, and source-preserving proof translations. A separately branded Google client was unavailable. No authoritative DRAT/FRAT/CakeLPR execution was claimed.

## ITERATE: the exact retraction theorem

Represent each non-tautological clause as a set of literals. Let $\sigma$ map every variable of a CNF $H$ to a constant or literal over the variables of $F$, with negation extended homomorphically. Simplify $\sigma(D)$ by deleting false constants and declaring it $\top$ if it contains true or complementary literals.

### Definition: source-clause retraction

$H$ source-retracts to $F$ under $\sigma$ when every original source clause $D$ of $H$ satisfies

$$
\sigma(D)=\top
\quad\text{or}\quad
\exists C\in F:\ C\subseteq\sigma(D).
$$

The containment direction is load-bearing: the original source clause $C$ is a legal already-available **subclause**, hence a stronger representative of the substituted source.

### Theorem `[P2-L5-436]`: nonexpansive shared-DAG Resolution backtranslation

If $H$ source-retracts to $F$ under $\sigma$, then every ordinary shared-DAG Resolution refutation $\pi$ of $H$ yields an ordinary shared-DAG Resolution refutation of $F$ with no more Resolution inference nodes. The construction needs no semantic oracle, weakening, branch rule, or proof search.

### Proof

Process $\pi$ topologically. Associate to each non-tautological substituted proof clause $\sigma(E)$ a previously derived representative $E'\subseteq\sigma(E)$; discard nodes whose image is $\top$.

For a source node, the retraction condition supplies $E'=C\in F$. Consider a Resolution step

$$
P\lor x,\quad Q\lor\neg x
\quad\vdash\quad
P\lor Q.
$$

If $\sigma(x)$ is constant, the parent in which the pivot becomes false has an image contained in the substituted conclusion; reuse its representative. If $\sigma(x)$ is a literal $\ell$ and both representatives retain $\ell$ and $\neg\ell$, resolve them once. The resulting clause is a subclause of $\sigma(P\lor Q)$. If either representative lost its pivot, that representative is already a subclause of the conclusion and is reused. If a parent image is tautological while the conclusion is not, the tautology must arise from the pivot colliding with an opposite literal in that parent; the other parent's representative is again a subclause of the conclusion. If the conclusion image is tautological, discard it.

Thus each original inference contributes at most one new Resolution node, and a node reused by several descendants remains shared. The final empty clause maps to the empty clause and cannot be discarded. Therefore

$$
S_{\rm Res}(F)\le S_{\rm Res}(H).
$$

This proves the exact lower-bound-preservation direction. It says nothing about legal mixed rules that do not commute with $\sigma$. $\square$

### Application to LSPV-3/503 and concurrent /504

For an original clause $C=(\ell_1\lor\ell_2\lor\ell_3)$, replace it by

$$
A=(\ell_1\lor\ell_2\lor u),
$$

$$
B=(\neg u\lor\ell_3\lor v),
$$

$$
D=(\neg u\lor\ell_3\lor\neg v).
$$

With $\sigma(u)=\ell_3$ and $\sigma(v)=0$, $A$ maps exactly to $C$ and $B,D$ map to tautologies. Every untouched source maps to itself. Hence the theorem independently confirms the /503 direction

$$
S_{\rm Res}(T(G,b))\le S_{\rm Res}(H_{503}(G,b)).
$$

For any simultaneously replaced set of clauses with disjoint fresh pairs, combine these substitutions. The source condition holds clause by clause, so the same proof covers `[P2-L3-504]` for every $0\le k\le4h$. Combined with the published expander-Tseitin ordinary-Resolution theorem, this transfers only the ordinary-Resolution lower bound.

## Independent hostile control: reversed containment fails

Let

$$
F=(x\lor y)\land(\neg x)\land(\neg y)
$$

and

$$
H=x\land(\neg x)\land(\neg y).
$$

The tempting reversed condition $\sigma(D)\subseteq C$ holds for $D=x$ and $C=x\lor y$, but $H$ has a one-inference refutation while $F$ needs two. Thus equisatisfiability, implication, or containment in the wrong direction does not give a nonexpansive proof backtranslation. This is a focused counterexample to a common transfer error, not a counterexample to /503.

## Computation and exact peer replay

- The exact 2,411-character GitHub content of LSPV-3/503 executable blob `85801666e30b67132f02af2236904c20188e842d` was evaluated through Node stdin. It reproduced 1,278 assertions, 40 K4/K3,3 replacement cases, and 80 negative checks.
- Independently written Python exhaustively checked 1,976 legal one-step substitution/representative cases: 1,872 translated/reused and 104 tautological conclusions discarded.
- It checked all eight signed proper three-literal gadgets, 96 retraction/semantic/bad-substitution assertions.
- It generated and verified 16 complete expanded K4 Davis-Putnam Resolution refutations, then translated and reverified all 16 original-source proofs. Expanded inference counts were 38–65 and converted counts 29–31, always nonincreasing.
- A separately written JavaScript checker independently reproduced all 1,976 one-step cases, 24 gadget image checks, and the 2-versus-1 wrong-orientation counterexample.
- Corrupt-pivot and missing-source-retraction controls rejected.

These finite executions test the implementation; the theorem is the symbolic case proof above. The optimizer scope is finite and no asymptotic theorem is inferred from the executions.

## Established-family / theorem / encoding / method ledger

| Family | Exact 3-CNF encoding and size | Established lower bound | Legal shortcut/control | Remaining transfer |
|---|---|---|---|---|
| Odd-charge cubic Tseitin $T(G,b)$ | One edge variable; four signed proper width-3 forbidden-parity clauses per vertex; $E=3h/2$, $m=4h$, indexed $N=\Theta(h\log h)$ | $\exp(\Omega(h))$ ordinary shared-DAG Resolution for suitable constant-degree expanders | GF(2) cancellation and recovered SOURCE/AND3/XOR yield linear mixed upper controls | Full historical mixed grammar and all-rule lower bound OPEN |
| Expanded strict3 $H_{503}(G,b)$ | Replace one $C$ by $A,B,D$ above; $E+2$ variables, $4h+2$ clauses | Present retraction proves $S_{\rm Res}(H_{503})\ge S_{\rm Res}(T)$ | Two RES nodes reconstruct $C$; distinct $R_{\rm bridge503}$ has claimed exact $4h+1$ mixed optimum | Historical accepted-byte RES-to-factor port and any paid CAST OPEN |
| Haken PHP control | Standard pigeon/hole CNF; not strict3 without a separate reduction | Exponential ordinary shared-DAG Resolution | Cook Extended Resolution is a mandatory stronger-system shortcut control | Any 3-CNF conversion needs explicit lower-bound-preserving simulation, not equisatisfiability |

Certified UNSAT, ordinary-Resolution proof-size hardness, distinct-calculus mixed optima, and historical checker acceptance remain separate.

## Resource ledger

- Logical nodes: Python expanded K4 proofs used 38–65 inference nodes; translated proofs used 29–31. LSPV-3/503 distinct mixed packets retain 17 paid nodes for K4 and 25 for K3,3, but are not historical native packets.
- Evidence bits: exact fetched peer source 2,411 characters; current Python/JavaScript/raw artifact sizes are charged at publication and not counted as proof nodes.
- Construction/search: exhaustive one-step enumeration, gadget truth-table tests, Davis-Putnam proof generation, and topological translation all executed locally; the Python recorded 0.018 seconds and 11,520 KiB peak RSS.
- Parsing/source/index/head: complete tracker and source reads are administrative costs, not $W_R$.
- Verification: every generated source and inference node was rechecked; wrong pivot and absent retraction source rejected.
- Sharing: representatives are indexed once and reused; the theorem counts the union of distinct translated inference nodes, not path multiplicity.
- Work/span/space: the theorem bounds total distinct Resolution work only. It does not claim minimum depth, proof search time, or an optimal retention/recomputation schedule.

## Tracker and manuscript disposition

`proof1.txt` has no material change. `proof2.txt` has a material evidence refinement: add `[P2-L5-436]` confirming the /503 and concurrent /504 ordinary-Resolution transfers under the exact source-containment direction and recording the reversed-containment counterexample. The complete prospective tracker is saved before the SHA-guarded update, followed by current-head refetch, conflict-safe merge, and full readback.

Root `main.tex` will be left untouched unless its complete bytes can be read and outside-region preservation established.

## Actual advance, verification status, and precise remaining gap

**Actual advance:** a general, source-authenticated, nonexpansive shared-DAG Resolution retraction theorem now isolates a sufficient lower-bound-preservation condition stronger than equisatisfiability. It validates the ordinary-Resolution components of `[P2-L3-503]` and concurrent `[P2-L3-504]`, and supplies a minimal counterexample proving the containment direction cannot be reversed.

**Precise remaining gap:** the theorem does not translate historical $R_{\rm mix341}$ proofs. The decisive next evidence remains original accepted bytes for RES, RES-derived clause-to-factor conversion, LOCAL-CONVERT, DEF facets, and assumption discharge, followed by a rule-by-rule source-retracting simulation or a legal counterexample. `[P2-C3]`, `[P2-B1]`, and `[P2-B2]` remain **OPEN**. **P versus NP remains OPEN.**

## Reproducible artifacts

- `experiments/review/lspv5_436_resolution_retraction_audit.py`
- `experiments/review/verify_lspv5_436_resolution_retraction.mjs`
- `results/raw/review/2026-11-08_0748_LSPV5_436_RESOLUTION_RETRACTION_RAW.json`
- `research/coordination/2026-11-08_0748_LSPV5_RESOLUTION_RETRACTION436_HANDOFF.md`
