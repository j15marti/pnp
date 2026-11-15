# TMR-5/032: Asymmetric fusion shortcut, directed zero closure, and a length-uniform dual collapse

**2026-11-14 20:48 PST (America/Los_Angeles)** | **ASYMFUS057** | TMR-5 Machine Bottleneck Redteam

**Scientific status:** PROVED/RESTRICTED for the exactly qualified finite-alphabet AND-obligation transition system and the all-\(n\) symbolic parameter family; native exact-rational checks are COMPUTATIONAL. Independent mathematical peer review remains OPEN. Neither SAT nor a Turing-machine lower bound is claimed. **P versus NP remains OPEN.**

## 1. Candidate and falsifiers

**Candidate:** Independently reproduce the directed-zero scalar-closure / tariff analysis in TMR-4/036, then add a more selective compact fusion operation that is available from **only one** of two incompatible zero-cost normal forms. Determine the exact tariff cone, including weights that may depend on length, and ask whether the old linear initial potential survives.

**Hostile controls:** (F1) zero-cost U-to-R or U-to-L conversion violates scalar monotonicity; (F2) the new paid fusion discharges more than its price under the old weights; (F3) a genuine cheap route to the goal is incorrectly removed because it uses free normalization first; (F4) a broader FUSE_ALL or free-goal operation, or a transition to a different proof/machine model, invalidates the claimed cost. All genuine cheap paths are retained.

**New relative to TMR-4/036:** Its FUSE_ALL shortcut is available from every nonterminal state. ASYMFUS057 tests an **asymmetric** extension, available only from \(R^n\), and derives both the length-dependent exact cone and the collapse of every length-independent initial scalar tariff to zero. This is not a novelty claim about the abstract-interpretation literature.

## 2. Complete qualified protocol

For fixed \(n\ge1\), state \((z,t)\) has \(z\in\{U,L,R,D\}^n\) and redundant tag \(t\in\{0,1\}\). Each of the \(n\) positions is a separate required AND obligation; \(D\) denotes discharged. Both \((D^n,0)\) and \((D^n,1)\) are complete goals. Exactly the following concrete rules exist:

| Rule | Guard and action | Paid cost |
| --- | --- | ---: |
| TAG | Flip redundant tag | 0 |
| CHOOSE_L / CHOOSE_R | Replace any U by L or R, respectively | 0 |
| DISCHARGE | Replace one L or R by D | 1 |
| NOP | Paid no-op at a nonterminal state | 1 |
| **FUSE_R** (new) | Only when \(z=R^n\), replace all of \(z\) with \(D^n\) | **1** |

The protocol has no other transitions. In particular, neither L-to-R conversion nor FUSE_R from an arbitrary partially discharged state is legal. This is a **qualified source-free inference-price laboratory**, not a sound/complete SAT calculus or a physical Turing machine. Introducing FUSE_R changes the baseline protocol, and its native one-unit price is an **assumption defining the laboratory**, not a claim of a free or one-step SAT inference.

The zero-cost SCCs are the two tag values for each \(z\); all \(U\to L/R\) paths are directed between SCCs. The complete directed closure must include choices at every U position. It must not identify L and R or delete a reachable R-only shortcut.

## 3. Exact scalar closure and complete tariff theorem

Let the only nonzero raw vector components be

$$
p_\Gamma(z)=2|\{j:z_j\in\{U,R\}\}|,\qquad
p_{\mathrm{int}}(z)=2|\{j:z_j\in\{U,L\}\}|.
$$

Fix nonnegative rational weights \(g=\lambda_\Gamma\), \(i=\lambda_{\mathrm{int}}\), with all other directive-vector coordinates zero. For the genuine zero closure \(Z_0(z)\),

$$
h_{g,i}(z)=\min_{y\in Z_0(z)}[g\,p_\Gamma(y)+i\,p_{\mathrm{int}}(y)].
$$

A direct product-of-zero-choices calculation gives

$$
\boxed{h_{g,i}(z)=
2\min(g,i)\#U(z)+2i\#L(z)+2g\#R(z).}
$$

This is the pointwise greatest zero-edge-nondecreasing scalar minorant of the raw weighted vector, using the exact finite-graph lemma of TMR-4/036. Its value on every completed goal is zero. Every actual zero step obeys \(h(C)\le h(C')\).

**NEW ASYMFUS057 theorem (PROVED/RESTRICTED).** In the new R-only-fusion protocol for each fixed \(n\), the complete set of admissible nonnegative tariff weights is

$$
\boxed{0\le g\le\frac{1}{2n},\qquad 0\le i\le\frac12.}
$$

The other five weights, whose components vanish, may be any nonnegative values.

**Necessity.** A single L-to-D paid discharge changes \(h\) by \(2i\), so \(i\le1/2\). The new paid edge \(R^n\to D^n\) changes \(h\) by \(2ng\), forcing \(g\le1/(2n)\). A single R-to-D discharge is then automatically admissible, since \(2g\le1\).

**Sufficiency.** TAG leaves \(h\) unchanged. CHOOSE_L/CHOOSE_R cannot decrease \(h\), by its directed-minimum definition. Every single paid discharge changes \(h\) by exactly \(2g\) or \(2i\), both at most 1, and NOP changes it by 0. FUSE_R changes it by \(2ng\le1\). No other legal rules exist. All paid inequalities, zero inequalities and completed goals are therefore covered. Telescoping bounds every complete concrete path.

The exact optimal initial potential (with **length-dependent weights allowed**) is

$$
\max_{g,i\text{ feasible}} h_{g,i}(U^n)
=\max 2n\min(g,i)=\boxed{1},
$$

attained by \(g=1/(2n)\), \(i=1/2\). This matches a real optimal path

$$
U^n\xrightarrow{0}R^n\xrightarrow{1}D^n.
$$

**Stronger length-uniform collapse.** If one fixed pair \((g,i)\) must work for **all** \(n\), the inequalities \(2ng\le1\) for unbounded \(n\) force \(g=0\). Consequently \(h_{g,i}(U^n)=0\) for every \(n\), even though its true minimum work is one. Allowing length-dependent tariff weights repairs this loss to a tight bound of one, but cannot produce a growing, much less superpolynomial, initial gap.

### Smallest concrete falsifier

At \(n=2\), the original baseline weights \(g=i=1/2\) give \(h(RR)=2\), yet the genuine \(R R\to D D\) FUSE_R edge costs one. The real path

$$
(UU,0)\xrightarrow{0}(RU,0)\xrightarrow{0}(RR,0)
\xrightarrow{1}(DD,0)
$$

finishes both obligations with one paid operation. Thus the original baseline tariff fails by one unit, and this is the smallest \(n\) with strictly more than one unit of old discharge. For \(n=3\), the old weights discharge 3 at price 1. These are **real** paths, not spurious paths for CEGAR to prune.

A mixed already-L state can remain genuinely more expensive: from \(L^n\), no free route reaches \(R^n\); \(n\) individual discharges are still required. The asymmetry therefore cannot be replaced by a fictitious FUSE_ALL edge on every state.

## 4. Independent native execution and negative controls

I implemented the transition graph independently, including each tag SCC, directed zero reachability, the exact rational scalar minimum, every concrete edge, goal checks, and shortest paid work using Dijkstra. This is a separate native CPython reimplementation, **not** execution of TMR-4's original script and not a compiled TM.

**Actual execution:** 17,331 checks, 16,776 distinct edge verifications, 16 model/length combinations, zero failures. For each \(n=1,2,3,4\), I ran the original base protocol, R-only fusion, the peer's FUSE_ALL control, and free-goal oracle control; I exhaustively compared every legal edge against the proposed certificate and checked an exact rational grid of candidate weights against the predicted cones.

| \(n=3\) model | States | Directed edges | Initial potential | Shortest paid completion |
| --- | ---: | ---: | ---: | ---: |
| Base | 128 | 638 | 3 | 3 |
| **R-only fusion** | 128 | 640 | **1** | **1** |
| FUSE_ALL | 128 | 764 | 1 | 1 |
| Free goal | 128 | 764 | 0 | 0 |

All 16-case raw records are preserved. The source and raw stdout Git blobs are byte-identical to the executed local files:
- \`experiments/tmr/tmr5_asymmetric_fusion057.py\` blob \`1d31142a687f3abb49fd03dd2d3e518daed4bed4\`.
- \`results/raw/tmr/2026-11-14_2048_TMR5_ASYMFUS057_NATIVE_RAW.json\` blob \`e8604806dbe0f3193a08980abdae011f5dbff9b3\`.

Finite checks are **COMPUTATIONAL**; the exact all-\(n\) conclusion rests on the enumerated legal-rule schema and direct algebra.

## 5. Source/peer ledger and ranked dependency map

| Evidence / implication | Independent verdict |
| --- | --- |
| TMR-4/036, \`research/agents/tmr-4/2026-11-14_2039_TMR4_SCALAR_DIRECTED_ZERO_CLOSURE036.md\`: greatest directed-zero scalar minorant and baseline n-unit laboratory | **PASS/RESTRICTED**, independently regenerated |
| TMR-4/036: uniform weights survive FUSE_ALL | **FAIL**, peer already correctly retired this; R-only is a strictly weaker new shortcut |
| TMR-3/035, \`research/agents/tmr-3/2026-11-14_2026_TMR3_COMPACT_IMPLICIT_FANOUT_TARIFF035.md\`: implicit aliases can share work | **RESTRICTED**; inspected original code/raw, not independently rerun in this work; this experiment agrees with fusion-as-MAY discipline |
| TMR-2/035, \`research/agents/tmr-2/2026-11-14_2023_TMR2_AFFINE_FUSION_QUERY_QUOTIENT035.md\`: affine source-coordinate tariff | **RESTRICTED** and separate query-only model; duplicate work must not be charged twice |
| Authenticated physical SAT-machine transition costs and complete conservative MAY behavior | **OPEN** |
| Sound complete proof calculus and proof-to-interpolant fusion transformer preserving shared DAG cost | **OPEN** |
| Fusion-safe superpolynomial initial potential on a growing SAT family | **OPEN** |
| Same-system transfer from every polynomial SAT decider to this exact proof resource | **OPEN** |
| P versus NP | **OPEN** |

Project primary originals consulted: the November 14 governing fusion directive (blob \`54c9177fc211dfca6c94d89d6ebbf3f3908809d6\`), November 13 machine replacement, all five current handoffs, \`AGENTS.md\`, \`CODEX.md\`, the research skill, both proof trackers, canonical \`main.tex\`, issue #3, LEAD-0029 Lipschitz squeeze, LSPV-3/615's authentic /341 false acceptance, and LSPV-1/572's restricted /386 normalizer. **/341 remains FAIL** as a full UNSAT authority and **/386 remains RESTRICTED**. No historical checker is imported into this model.

External primary scope references (no hardness theorem imported): Cousot and Cousot, *Abstract Interpretation*, POPL 1977, pp.238-252, DOI https://doi.org/10.1145/512950.512973; Fortnow et al., *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, DOI https://doi.org/10.1145/1101821.1101822. The former motivates abstract collecting semantics; the latter concerns a different random-access SAT-machine model. Neither establishes the laboratory cost assignment or a P/NP implication.

**Next peer repair:** TMR-4 should verify the R-only symbolic cone and all-length fixed-weight degeneration; TMR-3 must determine whether any real native proof rule can fuse several obligations at the claimed physical price; TMR-2 should canonicalize cross-normal-form identities so an initial potential survives every cheap affine/circuit normal form. The weakest load-bearing arrow is still a genuine, model-matched **superpolynomial** initial potential with a valid all-step transfer to arbitrary SAT deciders, not the finite zero-closure algebra.

**Publication/preflight:** full \`proof1.txt\` SHA \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`; full \`proof2.txt\` recovered via Git blob \`930c5eeddafce656717f28055a7a9a755f44737c\` (1,051,196 characters); full \`main.tex\` recovered via Git blob \`6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34\` (2,545,859 characters). The normal Contents API returned blank for the last two, so blob retrieval was used. Governing directive was rechecked before write. No material root tracker or main manuscript change is justified. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Five existing schedules unchanged.

END_OF_REPORT::TMR5::032::ASYMFUS057::2026-11-14_2048_PST
