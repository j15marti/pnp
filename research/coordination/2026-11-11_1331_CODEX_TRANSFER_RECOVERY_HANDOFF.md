# Recovered transfers and quantified work amplification

Date: 11 November 2026, 13:31 PST
Mode: synthesis / reconstruction
Status: **P versus NP remains open.**

## Target and result

The user requested a search of prior work for a transfer theorem supporting the previous conditional contradiction, with polynomial, quasipolynomial, and general superpolynomial assumptions.

The strongest recovered unconditional computation bridge is the October 13 minimum verified-witness benchmark $H$. Its description budget is $b_0+\lfloor\log_2(N+2)\rfloor$ and its outputs are independently verified SAT witnesses.

For every fixed correct SAT decider $A$, with constants $K,D$ fixed by the encoding, universal machine, and verification allowance,

$$
\overline H(N)\le C_A(N+T_A(KN)+2)^D.
$$

Here $T_A$ is global worst-case time, since witness self-reduction queries other formulas. Conversely an explicit upper bound $h$ for $\overline H$ gives uniform SAT time polynomial in $N+h(N)$ by enumerating the $O(N)$ admitted programs. Thus polynomial boundedness and each fixed QP log-degree transfer in both directions. This does not establish a lower bound on $H$.

The report distinguishes a numerical growth envelope from a decision-time class. No algorithm for computing optimum proof or witness cost is asserted.

## New quantitative development

Assume a satisfiable sequence with $s_j=|F_j|+2\to\infty$ and

$$
s_{j+1}\le A s_j^a,\qquad
H_{j+1}\ge H_j^b s_j^c/B,
$$

where $a>1,c>0$ and all constants are fixed.

| Case | Forced lower bound for $\overline H(N)$ |
|---|---|
| $b<a$ | The recurrence alone permits a fixed polynomial exponent |
| $b=a$ | $N^{\Omega(\log\log N)}$ |
| $b>a$ | $2^{\Omega((\log N)^{\log_a b})}$ |

The last two also lower-bound every SAT algorithm at the same scale. They hold for all sufficiently large envelope lengths: the predecessor of the first crossing of $N$ has size in $((N/A)^{1/a},N]$.

A fixed log-power $p>1$ excludes QP upper bounds with exponent less than $p$, not the full QP union.

## Correction to the old wire multiplier and the sharper target

A work **multiplier** is not a work **power**.

With $s_{j+1}\le C s_j$ and $W_{j+1}\ge\mu W_j$ for fixed $C,\mu>1$, only the polynomial scale $s_j^{\log_C\mu}$ is forced. Fourfold work per size doubling gives quadratic growth. The accumulated constant $C$ cannot be discarded by saying that a size exponent tends to one.

A growing multiplier is sufficient. If the actual benchmark satisfies

$$
s_{j+1}\le Cs_j,\qquad
H_{j+1}\ge H_js_j^c/B,\qquad C>1,\ c>0,
$$

then

$$
\log H_j\ge\frac{c}{2\log C}(\log s_j)^2-O(\log s_j).
$$

This follows by summing the last $\Theta(\log s_j)$ work increments and using $\log s_{j-k}\ge\log s_j-k\log C$.

Every SAT algorithm would then require $2^{\Omega((\log N)^2)}$ time, while a sufficiently large QP upper bound could remain consistent. The amplification premise is still OPEN.

## Replay obstruction

The earlier note already proves that a fixed polynomial formula transformation with polynomial witness extension, iterated from one fixed witnessed seed with polynomial total generation work, has polynomial $H$ along its orbit. One short program hardcodes the seed and replays the construction.

Such an orbit cannot satisfy critical power amplification or the growing multiplier above. The seed's initial difficulty does not help because its one fixed witness can be embedded in the replay program. A formula generator without a witness extender is not ruled out.

## Recovered fixed-system alternative

LSPV-1/336 defines the sound unary-clock proof system $Q_A$ for each fixed externally correct total decider $A$:

$$
L_{Q_A}(F)\le O_A(|F|+\mathrm{time}_A(F)+1)
\quad(F\text{ UNSAT}).
$$

If the same fixed target $R$ size-simulates these proof systems with overhead $G_A$, then

$$
W_R(N)\le G_A(O_A(N+T_A^-(N)+2)).
$$

Only size simulation is needed for minimum cost. Cost must be polynomially bounded by encoded proof length, or simulated directly. Every system and solver in this comparison uses the same source language.

Polynomial size optimality gives the common logarithmic exponent $r=1$. Algorithm-dependent polynomial degrees become coefficients after logarithms. The needed optimality or clock-only simulation is not proved for the preselected mixed calculus.

A weaker sufficient target also works. For one common $0<\theta<1$, suppose

$$
G_A(s)\le2^{2^{C_A(\log(s+2))^\theta}},
\qquad W_R(N)\ge2^{\kappa N^\alpha}.
$$

Then

$$
T_A^-(N)\ge2^{\Omega_A((\log N)^{1/\theta})}.
$$

At $\theta=1/2$ this again gives the squared-log lower scale. Both simulation and same-system hardness remain OPEN.

An available P or QP clock valid on all UNSAT inputs can be completed to a global P or QP algorithm by returning SAT on timeout. This does not apply to a selected family.

## Reflection and literature scope

LSPV-1/361 proves a restricted $E$ reflection-family equivalence for one fixed polynomial SAT solver. Its polynomial inequalities preserve every fixed QP log-degree. It does not automatically extend to the full mixed calculus.

For a larger solver clock, the report explicitly redefines the reflection CNFs and their proof envelope, requires the clock to bound all relevant negative instances, and charges the larger encoding. Under solver degree $a$ and reflection-proof degree $b$, the forward global proof bound has degree $\max(a,b)$; reverse direct substitution can have degree $ab$.

The primary-literature audit supplies a narrower witnessing target, but no unconditional reflection upper bound. Details are in the report.

## Provenance correction

The uploaded PC22_ALLFIELD1 and CP22LIFT1 reports do not use the same compiler despite the latter's attribution. The former uses transparent padding with variable bound $576m$; the latter uses a selector construction with $72m$. Their source families differ. Do not compose them by label.

Restricted PC/PCR and CP transfers do not establish $H$ amplification or all-solver clock simulation. The separate proposed CP repair is not promoted here without exact gadget derivations.

## Reconciliation and validation

Reviewed current root main.tex at blob 106ae16da087794611989ac1d3f5a9ad6a1a5173, governance, both proof trackers, the November 9 coordination state, the previous November 11 Codex report, actual historical clock/reflection reports, and the uploaded note/PDFs.

Three temporary agents independently reviewed the archive, attachments, and rate calculations. Their final review fixes were incorporated: the verification allowance is included in the fixed exponent, general program budgets and clocks are effective, exceptional small inputs have finite work, numerical envelope notation is separate, and reflection language/clock scope is explicit.

The work is symbolic, not a proof-assistant check. Local preflight and report hygiene checks apply only to the partial snapshot. No root ownership region, existing timestamped report, tracker status, automation, or schedule is changed.

**TRACKERS REVIEWED; NO MATERIAL CHANGE** to a load-bearing OPEN status. The report strengthens the quantitative ledger and corrects source composability without closing a hardness premise.

## Single next target

Prove or falsify one explicit construction satisfying

$$
s_{j+1}\le Cs_j,\qquad H(F_{j+1})\ge H(F_j)s_j^c/B
$$

for fixed $C>1,c>0,B\ge1$, for the actual bounded-description witness benchmark. The quantifier must cover every admitted witness program and survive fixed-seed replay. A structural rank or proof-size inequality is insufficient without transfer to this computational measure.

## Artifacts

- research/agents/codex/2026-11-11_1331_TRANSFER_RECOVERY_AND_RATE_AMPLIFICATION.tex
- research/agents/codex/2026-11-11_1331_TRANSFER_RECOVERY_AND_RATE_AMPLIFICATION_refs.bib
- research/coordination/2026-11-11_1331_CODEX_TRANSFER_RECOVERY_HANDOFF.md
