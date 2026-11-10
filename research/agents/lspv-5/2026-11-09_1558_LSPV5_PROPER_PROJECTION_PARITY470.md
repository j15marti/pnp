# LSPV-5/470: all proper projections still erase a cost-critical legality/history correlation

**November 9, 2026, 15:58 PST | Route B independent red team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

Material tracker node: **[P2-L5-470]**, refining [P2-L5-469] and the open transformer obligation [P2-C3]. The historical accepted-byte grammar [P2-D1], full mixed superpolynomial minimum [P2-B1], noncircular same-calculus B3 [P2-B2], Route A and P versus NP remain OPEN.

## Claim card and IDEA

- **Target:** falsify the repair “retain every pairwise, or even every proper-coordinate, correlation between simultaneous rule legality and paid history.”
- **Quantifiers:** for every $m\ge1$, there exist two concrete relations on $m$ premise bits and one paid-history bit with identical projections on every proper coordinate subset but different guarded cost minima.
- **Model:** finite collecting semantics over complete relational states; a positive first-use weight $w$; AND guard requiring every premise bit. This is an analysis-layer control, not a replacement calculus.
- **SAME_REALIZATION:** premise legality and paid history refer to the same candidate application in the same state; the charge is computed after imposing the same all-premises guard.
- **Weakest material theorem:** show that every abstraction factoring only through all proper projections must use zero as its greatest universally safe charge on at least one abstract value.

Falsifiers fixed before search were: (F1) some proper projection distinguishes the two relations; (F2) the all-premises guard leaves both histories possible within either relation; (F3) a positive uniform charge can be safe for every concretization of the common abstract value; (F4) the required full relation itself forces exponential representation, proof work or runtime. F1--F3 are disproved below. F4 is positively falsified: one parity equation represents the relation.

## SEARCH and continuity

Read complete root trackers `proof1.txt` (blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`) and `proof2.txt` (startup blob `54aadf0ca552bcbe7d6eec78b8cb2fb82dc6a255`), current issue #3 through LSPV-2/530, the November 9 abstract-interpretation handoff, the November 2 five-role refocus, AGENTS.md, CODEX.md, the repository research protocol and red-team mode. Actual peers reviewed: LSPV-1/547's source-specific $(q,b)$ budget invariant, LSPV-2/530's output-free RUP-CDCL conflict abstraction, LSPV-3/543's exact binary-gate CNF facets, LSPV-5/469, `GROKPROOF/2026-11-09_2015_PROGRESS.md`, and Claude's world/trace-partitioning ledgers. LSPV-1/547 and LSPV-2/530 are valid only in their stated restricted systems; neither supplies the all-native relation used here.

Primary sources were read for their exact scope: Cousot--Cousot (POPL 1977) gives sound approximation/fixpoint machinery; D'Silva--Haller--Kroening (POPL 2013) treats the bottom-everywhere problem for completely additive reductive functions on powerset lattices and combines overapproximate greatest-fixed-point with underapproximate least-fixed-point reasoning; their Abstract Satisfaction paper (POPL 2014) models sets of models and deduction, abduction and quantification transformers; Giacobazzi--Ranzato--Scozzari (JACM 2000) distinguishes pointwise and fixpoint completeness and does not guarantee least complete fixpoint refinements for arbitrary monotone operators. None states a mixed-proof lower bound, a native cost theorem or B3.

Change-aware repository reads included both required sources: `konard/p-vs-np` at head `ecedd2b45f1c524d85c00b2da27a9c140025550c` (`scripts/proof_status.json`: scoped Lean theorem list, not a P-vs-NP resolution) and `blkph0x/p-vs-np-proof-research` at head `7dedc73f758df3f8325c57a7bd7f1271730cb151` (`METHOD_INDEX.md`: explicitly scoped finite/family claims). Also inspected `meelgroup/frat-xor` head `18cd6bc17af10a9891c10a846ce966166f9fe0dc` (external provisional XOR/FRAT format), CakeML/LPR, short-proof, DRAT-trim, CryptoMiniSat, CNFgen's Tseitin generator, ABC, mockturtle, `openai/math` head `4eaee87548250b2682affda7d05d947c05554bae`, and `anthropics/formal-math` head `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. Targeted OpenAI GitHub search returned no relevant native mixed-calculus theorem. A standalone Google-branded interface was unavailable; primary web search and direct original pages/PDFs were used.

## Concrete and abstract domains

Fix $m\ge1$ and positive weight $w$. Let

$$
\Omega_m=\{0,1\}^{m+1},\qquad x=(p_1,\ldots,p_m,h).
$$

The bits $p_i$ mean that each required premise/facet/context check for one candidate native application is legal; $h=1$ means its positive-weight owner is already in the global paid-history set. The **concrete domain** is $C_m=(\mathcal P(\Omega_m),\subseteq)$ with collecting union as join. Define the all-premises guard $g(x)=\bigwedge_i p_i$ and concrete safe first-use charge

$$
c^*(R)=\min\{w(1-h):x\in R,\ g(x)=1\},
$$

when the guarded set is nonempty.

The proposed **proper-projection abstract domain** is

$$
A_m=\prod_{S\subsetneq[m+1]}\mathcal P(\{0,1\}^{S}),
$$

ordered componentwise by inclusion. Abstraction and concretization are

$$
\alpha(R)=(\pi_S(R))_{S\subsetneq[m+1]},\qquad
\gamma(a)=\{R\subseteq\Omega_m:\forall S\subsetneq[m+1],\pi_S(R)\subseteq a_S\}.
$$

This is a MAY overapproximation: $R\in\gamma(\alpha(R))$. A guard transformer intersects the concrete relation with $g$; the best sound abstract guard is $\alpha(R\cap g)$ only when the full $R$ is available. Any transformer that factors solely through $\alpha(R)$ must be uniform over all relations with the same abstract value. Its greatest safe lower charge is therefore at most the minimum concrete charge over those relations. This explicitly fixes the approximation direction required for a cost lower bound: the abstract charge may not exceed the concrete first-use charge.

For an actual native rule, the $p_i$ must include **every** authenticated parent, signed pivot/facet, source/provenance and context obligation; $h$ must use the calculus's global paid owner. Resolution, AND3, GF(2), DEF-facet and LOCAL-CONVERT transformers remain OPEN until their historical accepted-byte semantics are authenticated. Case split/discharge is not silently added.

## Theorem 470.1: all proper projections are insufficient

For $q\in\{0,1\}$ define

$$
R_q=\{x\in\Omega_m:p_1\oplus\cdots\oplus p_m\oplus h=q\}.
$$

**PROVED/RESTRICTED.** For every proper coordinate subset $S\subsetneq[m+1]$,

$$
\pi_S(R_0)=\pi_S(R_1)=\{0,1\}^{S}.
$$

Nevertheless, under $p_1=\cdots=p_m=1$ each $R_q$ contains exactly one state and

$$
h=q\oplus(m\bmod2).
$$

Thus $\{c^*(R_0),c^*(R_1)\}=\{0,w\}$. Consequently every deterministic cost transformer depending only on the common all-proper-projection value and sound for both relations must return at most zero; nonnegativity forces zero.

**Proof.** If $S$ omits at least one coordinate, any assignment on $S$ extends to each parity by choosing an omitted bit to satisfy the target parity; with $r$ omitted coordinates there are exactly $2^{r-1}$ extensions in each relation. This proves the projection identity. Setting all premise bits to one leaves the displayed parity equation for $h$, so the histories and charges are opposite. A uniform sound abstract charge must be no greater than the smaller guarded concrete charge, namely zero. QED.

The $m=2$ instance directly defeats a pairwise-projection repair for a two-parent Resolution-like action:

$$
R_0=\{000,011,101,110\},\qquad R_1=\{001,010,100,111\}.
$$

Every one- and two-coordinate projection is the corresponding full cube, but the guard $p_1=p_2=1$ selects `110` versus `111`, changing charge $w$ versus $0$.

## Joins, shared DAGs, and abstract satisfaction

The collecting join $R_0\cup R_1=\Omega_m$ permits both guarded histories and therefore has safe charge zero. This is the expected polarity of a MAY join; choosing the more favorable branch would be unsound. In a real shared proof DAG, the relation must remain keyed to immutable paid-owner identity and compatible assumption context, with reconvergent histories charged once. An AND hyperedge needs all premises; OR alternatives select one legal derivation. This theorem concerns one guarded application and does not license summing branch minima or leaking a branch-local lemma.

Abstract satisfaction's deduction/abduction/quantification operations can express refinement of such relations, and ACDCL can synthesize learned transformers under its lattice hypotheses. But solver correctness does not supply the missing native relation, a lower bound on its abstract distance, or a same-R B3 bridge. A nonempty overapproximation after guarding is inconclusive; bottom in a sound model overapproximation is semantic UNSAT evidence, not automatically absence of a cheap native refutation.

## ITERATE: controls and revised conclusion

Python exhaustively checked every proper projection for $1\le m\le9$: 4,162 assertion groups, 2,035 projection comparisons, 173,050 individual extension-count checks and five malformed rejections. Independent Node code used a separately written bit enumeration for $1\le m\le8$: 2,073 checks, 1,012 projection comparisons and four malformed rejections. Both confirm the binary witness and union charge. These finite runs validate the implementation; Theorem 470.1 is symbolic.

Mandatory controls revise the scope sharply:

- **Tseitin/GF(2):** the full missing correlation is exactly one parity equation, so Gaussian/affine representation is a compact repair and an adversarial shortcut, not evidence of unavoidable explosion.
- **ER/PHP:** a paid extension owner may package a high-order relation compactly; projection count cannot be converted to proof size without a native simulation/lower-bound theorem. LSPV-1/547 remains a conditional `/369` result on wide bit-PHP only.
- **Compact mod-3 adders:** the Boolean parity witness does not cover modular-3 or nonlinear transformers. They must be included separately; omitting them invalidates all-native coverage.
- **Shared DAG/reconvergence:** collecting union can erase the parity class and force zero charge. Exact native joins may retain a compact tag; count-once work must not be double-counted.
- **Horn/2SAT/tiny cores/renaming/padding:** the theorem is representation-invariant under coordinate renaming but proves no formula hardness and must not make these easy controls costly.
- **DEAD/COPY/DELAY/INTERP/RECOMP and semantic/algebraic oracles:** none is forced to instantiate this abstraction. The arbitrary-algorithm transfer is OPEN.

The revised repair is not “enumerate the full relation.” It is: retain a sufficient **relational invariant** tying every simultaneous native guard to the paid owner/history, represented symbolically when possible, and prove rule-by-rule that its transformer is cost-nonexpanding. Domain cardinality and explicit projection count do not establish representation, verification, proof or runtime cost.

## Family and bridge ledger

| Family/control | Original encoding and established model | Applicable method/shortcut | Remaining transfer |
|---|---|---|---|
| Cubic expander Tseitin | Native proper signed 3-CNF, $n=3h/2$, $m=4h$, general DAG Resolution lower bound in the cited family scope | Gaussian/GF(2), native /341 AND3/GF(2) control | Resolution hardness does not cover full mixed R_mix341 |
| Haken PHP | Standard PHP CNF, exponential ordinary Resolution size | Cook ER/definitions are mandatory shortcut controls | Need precise source encoding and all-native normalization; no all-algorithm conclusion |
| Braun bit-PHP | Original wide width-$2\ell$ signed clauses; published Res(XOR) lower bound, used conditionally in /547 | `/369` exposure compiler and source-specific $(q,b)$ invariant | No strict-3CNF preservation or full historical grammar coverage |
| Compact mod-3 adders | Established compact adder encodings as nonlinear/algebraic control | Extension variables and modular reasoning | Current parity theorem supplies no transformer or lower bound |

For B1/B2/B3: Theorem 470.1 only narrows [P2-C3]. It proves neither a superpolynomial abstract minimum nor concrete [P2-B1]. It says nothing that makes `SAT in P => polynomial Wbar_Rmix341` noncircular, so [P2-B2]/B3 remains OPEN.

## Resource, trust and publication ledger

Logical test states and projections were generated exhaustively only within the stated finite ranges. Python executor wall was 28.300971597 s; Node executor wall was 0.017947378 s. `/usr/bin/time` was unavailable, so peak RSS is unknown. Source parsing, enumeration, projection construction, validation and output are charged in these observed executions; neither is an FLMV machine schedule. The symbolic parity representation uses $O(m)$ written bits and one equation; discovery cost is irrelevant to ideal proof minimum but would be charged in an implemented algorithm.

The authoritative historical checker was not available/executed; no accepted trace bytes or native cost were claimed. Local preflight found no repository-root `main.tex`, AGENTS.md, CODEX.md or skill files in scratch despite exiting zero with errors; complete GitHub reads were used. The ordinary GitHub file API returned zero readable bytes for the 1.84 MB `main.tex`; therefore it will be edited only if the authenticated full blob can be fetched and outside-marker equality verified. No partial response will be overwritten.

## Actual advance, verification, publication status, precise gap

**Actual advance:** a symbolic theorem strictly strengthens /469: not merely separate marginals, but the complete collection of *all proper-coordinate correlations* can erase a cost-critical all-premises/history fact. A full or equivalently sufficient symbolic relation is necessary for exact positive charging.

**Verification:** complete proof above; two independent exhaustive implementations and malformed controls. **Status:** PROVED/RESTRICTED + COMPUTATIONAL, not a native-rule theorem.

**Publication status at report drafting:** report, code, raw and handoff prepared for conflict-safe publication and complete readback; final receipt records the resulting commit or exact blocker.

**Precise remaining gap:** authenticate every historical R_mix341 native rule and build a symbolic relational abstraction covering original source, context discharge, full shared-DAG reconvergence, all guards, paid owners and every GF(2)/DEF/LOCAL-CONVERT/nonlinear shortcut with abstract cost no greater than concrete cost; then prove a superpolynomial abstract minimum. Separately prove noncircular same-R B3. P versus NP remains OPEN.

## References

Patrick Cousot and Radhia Cousot, *Abstract Interpretation*, POPL 1977, https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml . Vijay D'Silva, Leopold Haller and Daniel Kroening, *Abstract Conflict Driven Learning*, POPL 2013, https://www.kroening.com/papers/popl2013.pdf ; *Abstract Satisfaction*, POPL 2014, https://www.kroening.com/papers/popl2014.pdf . Roberto Giacobazzi, Francesco Ranzato and Francesca Scozzari, *Making Abstract Interpretations Complete*, JACM 47(2), 2000, https://www.sci.unich.it/~scozzari/paper/JACM00.pdf .

## End-of-run status

**Actual advance:** Theorem 470.1 proves that even the complete family of all proper-coordinate projections can erase a cost-critical all-premises/history correlation; the binary instance rules out pairwise projection as a general repair. **Verification:** symbolic proof plus two independent exhaustive programs, with the exact finite ranges and limitations above. **Publication status:** this report, code, raw summary and handoff are the exact outbox; GitHub commit, tracker, issue and readback identifiers are recorded in the companion publication receipt. **Precise remaining gap:** authenticate every native historical rule and construct a symbolically relational, cost-nonexpanding all-rule transformer that preserves source, context, shared owners and nonlinear shortcuts; then prove a superpolynomial abstract minimum and separately a noncircular same-R B3. P versus NP remains OPEN.
