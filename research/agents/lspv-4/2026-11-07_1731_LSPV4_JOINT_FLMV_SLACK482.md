# LSPV-4/482 | Joint four-parameter FLMV exponent-slack audit

**November 7, 2026, 17:31 PST | Route A resource auditor | PROVED/RESTRICTED arithmetic + COMPUTATIONAL finite checks. P versus NP OPEN.**

**Nodes:** restricted evidence for [P2-A4]. [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN. Existing five roles, two Route A / three Route B, all tasks, schedules, weights and historical R_mix341 untouched.

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis:** LSPV-4/480 calculated admissible *individual* overhead in child-call exponent a, child-size exponent lambda, local-time exponent rho and all-phase-space exponent eta. One cannot consume those thresholds independently when all four physical expenses increase simultaneously. Derive the exact equal additive exponent tariff delta allowed by the original FLMV strict inequality.

**Four falsifiers:** (F1) even arbitrarily small positive common overhead destroys the 1/90 gap; (F2) the fixed-point branch switches from a/(1-lambda) to rho; (F3) for arbitrarily high fixed initial polynomial exponents there is no finite strict entry despite positive limiting margin; (F4) this recurrence bound is mistaken for a fully charged physical compiler.

**READ AND SEARCH:** Both root trackers, issue #3 (current), governing five-role handoff, current peer LSPV-2/480 direct-guest padding (report blob 456801ac78c32d53f2eb0b7beda5aea848f932b3), LSPV-4/480 individual slack and /481 finite entry, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, actual GROKPROOF/2026-11-06_2316_PROGRESS.md (blob a20fb8b3640d7574faf238a4a83a021bb0984808), Claude world ledger 2026-10-28_0924 (blob 79e4d4e7e0e3edff3aba8610852c45534bdde128). Original FLMV author PDF Section 2.1 and Cor. 5.8, https://lance.fortnow.com/papers/files/tst.pdf (the corollary is formally phrased for NTIME[n], with SAT connected by the paper's quasi-linear reductions). External authentic source files checked: konard/p-vs-np TOOLS_AND_METHODOLOGIES.md blob b3f5ceb025a75360d1956f4bb0ab6ae702761283, blkph0x/p-vs-np-proof-research INDEPENDENT_AUDIT.md blob b30515cced93d8911a6415555ee9ec1444502d93, meelgroup/frat-xor format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f, MassimoLauria/cnfgen cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab, openai/math lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean blob 1ced21f44ad49370d1b812e862c03c3a91d7f836. Generic web search available; direct Google-branded search not available. No inspected repository supplies the universal contraction. Prior art /480 and /481 is retained, not claimed as new.

## Theorem 482.1: sharp common four-parameter tariff

Fix a common additive overhead $0\le\delta\le1/100$ and let

$$
a=3/5+\delta,\quad\lambda=1/2+\delta,\quad
\rho=11/10+\delta,\quad\eta=1/2+\delta.
$$

Consider the equality **upper envelope**, with arbitrary fixed finite $t_0\ge1,s_0\ge0$:

$$
t_{j+1}=\max\{\rho,a+\lambda t_j\},
\qquad
s_{j+1}=\max\{\eta,\lambda s_j\}.
$$

On the stated interval $a/(1-\lambda)>\rho$. Its fixed point is therefore

$$
c_\delta=\frac{3/5+\delta}{1/2-\delta},
\qquad s_\infty=\eta.
$$

With the exact published FLMV threshold $\beta(c)=((c+2)/c^2-c)/2$, the **simultaneous** margin is

$$
G(\delta)=\beta(c_\delta)-\eta
=\frac{1000\delta^4+200\delta^3+510\delta^2-1765\delta+2}
{20(1-2\delta)(5\delta+3)^2}.
$$

Its numerator has derivative $4000\delta^3+600\delta^2+1020\delta-1765<0$ on $[0,1/100]$, positive value at zero, and negative value at $1/100$. Hence it has exactly one root

$$
\boxed{\delta_*=0.00113351590406104969293425767706074158\ldots}.
$$

**PROVED/RESTRICTED:** The equality upper-envelope recurrence eventually enters $s<\beta(t)$ for every finite initial pair if and only if $0\le\delta<\delta_*$. If actual machine exponents merely obey the corresponding recurrence inequalities, $\delta<\delta_*$ remains *sufficient* for guaranteed finite entry. If $\delta\ge\delta_*$, the equality fixed-point trajectory defeats that generic upper-envelope guarantee; a physically better algorithm may still enter. No all-machine impossibility follows.

## Theorem 482.2: explicit finite iteration

Let $D_t=(t_0-c_\delta)_+$, $D_s=(s_0-\eta)_+$, $L=433/216$ and $A=LD_t+D_s$. Because

$$
\beta'(c)=-1/2-1/(2c^2)-2/c^3,\qquad
|\beta'(c)|\le433/216\ \text{for}\ c\ge6/5,
$$

the recurrence upper envelope obeys

$$
\boxed{\beta(t_j)-s_j\ge G(\delta)-\lambda^j A}.
$$

Any finite $j$ satisfying $\lambda^j A\le G(\delta)/2$ guarantees the strict margin $G(\delta)/2$. Selection of such a *fixed finite* depth can be noncomputable from the hypothetical solver code, conditional on a separately proved **effective, universally recursively applicable** transformer. This is an arithmetic refinement of /481, not an exponent-extraction algorithm.

## Quantitative decisions

| Common delta | c_delta | eta | G(delta) | Universal envelope finite entry |
|---:|---:|---:|---:|---|
| 0 | 1.200000000 | 0.500000 | 0.011111111 | YES |
| 1/10000 | 1.200440088 | 0.500100 | 0.010129234 | YES |
| 1/1000 | 1.204408818 | 0.501000 | 0.001306653 | YES |
| 1/900 | 1.204899777 | 0.501111 | 0.000219225 | YES |
| 1/800 | 1.205513784 | 0.501250 | -0.001139512 | NO generic guarantee |

**ITERATE:** F1, F2 and F3 refuted within the declared exact recurrence. F4 is the central still-open physical obligation. A simultaneous $N^{0.002}$ exponent loss cannot be silently absorbed by this four-way envelope; genuinely subpolynomial losses $N^{o(1)}$ can be absorbed into some fixed positive delta below the threshold, for each fixed finite composition, ONLY after their all-input same-machine accounting and recursive closure are proved.

## Source-hardness and shortcut controls

Signed cubic graph Tseitin formulas have four exact proper 3-clauses per vertex, $3H/2$ edge variables and length $N=\Theta(H\log H)$. On genuine cubic-expander families there are exponential **ordinary DAG Resolution** refutation lower bounds under the published expansion assumptions, while GF(2) charge summation solves the formulas efficiently. Therefore hardness in ordinary Resolution cannot be transferred to fixed mixed R_mix341 or arbitrary machines. The small original signed K4 family below is a model-count regression control, NOT a certified asymptotically hard example. No new 3-SAT family is proposed.

## Verification and full resource qualification

Independent exact-rational Python: 1,204 initial pairs, 110,966 conservative counted inequalities, max needed depth 33, lowest measured strict gap 0.0006606911, all PASS. Separately written independent JavaScript with different seed: 1,204 pairs, 145,386 assertions, max depth 33, minimum gap 0.000676435, all PASS. Both agree on quartic threshold and rational sign controls. Original signed K4 3-CNF: all 16 charge masks, 16 original ternary clauses each, every one of 64 edge assignments per mask; eight charge configurations SAT (8 models each), eight UNSAT. Full code/raw and independent exact-rational source available in the run's reproducibility archive; JavaScript source and compact raw published in repository.

This is **only arithmetic**. The physically required terms remain all input/index/head reads, malformed parsing, source authentication, preprocessing, policy search and failures, child length and materialization or lazy bit ports, guest TIME/WORK/INDEX simulation, simultaneous ancestor/child memory, cache, references, JOIN/OR reductions, output, conversions, replay and recomputation. No native FLMV machine instruction implementation ran. No historical R_mix341 proof, inference-node count, proof evidence bits or B1/B2/B3 implication was produced. These resources were not measured, not assumed zero. The fixed-point test is necessary to audit candidate upper bounds, not a construction of a universal solver contraction.

**Actual advance:** exact *joint* overhead threshold, strict finite-entry certificate, independent finite tests. **Publication:** dated report, code, raw and five-role handoff. **Remaining gap:** [P2-A2] effective same-FLMV-machine all-input recursively iterable contraction, and [P2-A4] fully charged physical realization remain OPEN; [P2-A5] contradiction conditional. Route B remains OPEN. **P versus NP OPEN.**
