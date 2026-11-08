# LSPV-2/486 | Exact post-step exponent-loss robustness for the conditional FLMV recurrence

**2026-11-07 23:21 PST | LSPV-2, Route A primary | PROVED/RESTRICTED exact arithmetic + COMPUTATIONAL. P versus NP OPEN.**

**Nodes:** [P2-A2] universal solver-dependent same-machine all-input contraction OPEN; [P2-A4] restricted resource evidence only, no unrestricted physical realization; [P2-A5] final recursively applicable contradiction OPEN. Cross-chain [P1-01], [P1-03], [P1-04] and Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Initial complete current-head reads: proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b (18,553 characters), proof2.txt blob 16539117b9acdec345dea471db993abf71e72053 (339,573 characters). The following conditional upper-envelope refinement does not alter status, dependency, evidence of an actual SAT transformation, or missing physical realization. Neither tracker should acquire another redundant arithmetic note.

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis:** If the proposed two-exponent contraction has a common, fixed additive loss epsilon AFTER each step, the worst-case equality envelope still enters the strict forbidden FLMV region for every finite starting exponent pair if and only if epsilon is below a sharp positive threshold. This is intentionally DIFFERENT from the previous LSPV-4/482 common tariff applied to each physical channel parameter a, lambda, rho, eta BEFORE the recurrence. The resulting threshold is an accounting diagnostic, not an algorithm.

**Four precommitted falsifiers:** (F1) the 11/10 floor controls the time fixed point; (F2) the rational margin polynomial has an incorrect sign/coefficient; (F3) positive limiting gap nevertheless allows some finite initial exponents never to enter the strict region; (F4) the post-step exponent tariff might be silently substituted for the distinct four-parameter physical resource tariff. F1-F3 fail under the exact recurrence, while F4 is a valid transfer warning and is retained.

**Read continuity:** Both complete root trackers; coordination issue #3 including its latest comments; governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (blob c3889a3e514ddbd747150dcb68607013a3b2d154); AGENTS.md (19656af102604d5f0a721d548cf2e4e72a063561), CODEX.md (754999f50de93cdb693ed37bc8110d31e9e698ef), .codex/skills/pnp-research/SKILL.md (b8df83a7b0b1428f349b0e02ce1387d979e8db7f); LSPV-2/485, /483, /476 and /442; LSPV-4/482, /485, /446; actual GROKPROOF/2026-11-08_0320_PROGRESS.md (72edb3140d8ed798d0905a827f85d3428728e396) and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a). The original 1/90 fixed-point gap and LSPV-4/482 physical-channel tariff are not claimed as discoveries.

**Primary literature:** Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6):835-865 (2005), DOI 10.1145/1101821.1101822. Read original paper https://lance.fortnow.com/papers/files/tst.pdf and inspected printed page 18, Corollary 5.8, which states the deterministic NTIME[n] time-space exclusion with threshold beta(c), plus Section 2.1's indexed INPUT/INDEX tape semantics. Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM 48(2):149-169 (2001), DOI 10.1145/375827.375835, gives ordinary shared-DAG Resolution controls. Public web search was used; no separately identifiable branded Google client was available.

**Actual external repository files:** konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 (finite-machine-model P subset NP only); blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and INDEPENDENT_AUDIT.md blob b30515cced93d8911a6415555ee9ec1444502d93 (uniform acquisition still missing); MassimoLauria/cnfgen cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (standard graph parity source generator); meelgroup/frat-xor format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f (a different proof format); openai/math lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean blob 1ced21f44ad49370d1b812e862c03c3a91d7f836 (specific driver costs, not an arbitrary code compiler). No outside repository supplies the all-input FLMV transformation.

## Theorem 486.1: sharp post-step additive tariff (PROVED/RESTRICTED)

Suppose, CONDITIONALLY, that for every fixed polynomial-time SAT solver A a uniformly effective, both-label, malformed-aware, all-input, same-FLMV-machine, recursively iterable transformation exists, and that its fully charged exponents obey

$$
t_{j+1}\le\max\left\{\frac{11}{10},\frac35+\frac{t_j}{2}\right\}+\varepsilon,\qquad
s_{j+1}\le\max\left\{\frac12,\frac{s_j}{2}\right\}+\varepsilon.
$$

Define the equality upper-envelope sequences using equality in both recurrences, for $0\le\varepsilon\le1/100$. Both maps are 1/2-Lipschitz and have exact fixed points

$$
t_\infty=\frac65+2\varepsilon,\qquad s_\infty=\frac12+\varepsilon.
$$

Indeed, the time max selects its affine branch at $t_\infty$ since $3/5+t_\infty/2=6/5+\varepsilon>11/10$, and the space max selects its 1/2 floor since $s_\infty/2<1/2$. The FLMV margin is

$$
G(\varepsilon)=\beta\left(\frac65+2\varepsilon\right)-\left(\frac12+\varepsilon\right)
=-\frac{1000\varepsilon^3+1750\varepsilon^2+895\varepsilon-2}{20(5\varepsilon+3)^2},
\quad
\beta(c)=\frac12\left(\frac{c+2}{c^2}-c\right).
$$

The cubic $P(\varepsilon)=1000\varepsilon^3+1750\varepsilon^2+895\varepsilon-2$ is strictly increasing for $\varepsilon\ge0$ since $P'(\varepsilon)=3000\varepsilon^2+3500\varepsilon+895>0$, starting at $P(0)=-2$. Its unique nonnegative root is

$$
\boxed{\varepsilon_*=0.00222494505010335\ldots}.
$$

**Claim:** For every finite initial $t_0\ge1$, $s_0\ge0$, the equality upper envelope enters the strict forbidden region $s_j<\beta(t_j)$ after finitely many iterations if and only if $0\le\varepsilon<\varepsilon_*$. The same condition is sufficient for actual exponents obeying the stated upper inequalities, but only if that actual same-machine compiler and its recursive applicability are independently established.

**Proof:** The 1/2-Lipschitz property gives $t_j\le t_\infty+2^{-j}(t_0-t_\infty)_+$ and $s_j\le s_\infty+2^{-j}(s_0-s_\infty)_+$. On $c\ge6/5$ the derivative magnitude of decreasing beta is at most $L=433/216$. Consequently

$$
\boxed{\beta(t_j)-s_j\ge G(\varepsilon)-2^{-j}A,\qquad
A=\frac{433}{216}(t_0-t_\infty)_+ +(s_0-s_\infty)_+.}
$$

If $G(\varepsilon)>0$, choose a finite j with $2^{-j}A\le G(\varepsilon)/2$, yielding a strictly positive gap. If $\varepsilon\ge\varepsilon_*$, start an equality-envelope trajectory with $t_0\ge t_\infty$, $s_0\ge s_\infty$. Every iterate remains above the fixed point, and monotonicity gives $\beta(t_j)-s_j\le G(\varepsilon)\le0$. This only disproves a generic guarantee from that envelope; a physically better compiler may still exist. QED.

At $\varepsilon=0$, $G(0)=1/90$, the earlier project's known arithmetic. At $\varepsilon=1/450$, $G(\varepsilon)\approx0.0000135558551>0$. At $\varepsilon=1/400$, $G(\varepsilon)\approx-0.00136886417<0$.

## Distinction from prior LSPV-4/482 (MANDATORY)

| Overhead placement | Time fixed point | Space fixed point | Critical common loss |
|---|---|---|---|
| /486, additive loss AFTER the two exponent recurrences | $6/5+2\varepsilon$ | $1/2+\varepsilon$ | $0.00222494505\ldots$ |
| /482, common tariff BEFORE recurrence on all four physical parameters $(a,\lambda,\rho,\eta)$ | $(3/5+\delta)/(1/2-\delta)$ | $1/2+\delta$ | $0.001133515904\ldots$ |

The second, smaller bound is the relevant one when each independent physical channel worsens equally. Reporting the larger /486 number as the allowable all-phase physical overhead would be a mathematical accounting error. Both are conditional numerical safeguards, not concrete time/space transformations.

## Established hard family / encoding / known-method / transfer ledger

For a simple cubic graph with H vertices and 3H/2 edge variables, the original Tseitin source consists of four properly signed width-three clauses per vertex forbidding all local 3-bit assignments of parity different from its vertex charge. There are 4H source clauses, 12H signed occurrences, and N=Theta(H log H) input bits with polynomially bounded IDs. For suitable odd-charge connected cubic expander sequences, established 2^{Omega(H)} lower bounds apply in **ordinary shared-DAG Resolution**, not arbitrary computational SAT or the entire native historical mixed R_mix341. Summing GF(2) vertex equations is a valid efficient computational shortcut. The K4 originals in this run are only small finite SAT/UNSAT source controls, not a certified hard growing family. No equisatisfiability-only proof-hardness transfer is assumed.

## Executed verification and resource audit

Exact-rational Python independently checked 212,732 assertions, including 1,080 initial exponent pairs, 65 steps per pair, all six rational tariff values, 90-step root bisection, the rational gap identity, all 16 exact K4 charge masks with 64 edge assignments each, and six invalid/corrupted K4 packet controls. Independently authored Node.js checked 308,099 assertions across 1,200 pseudorandomly seeded exponent pairs and 85 steps per pair, its own polynomial and root, original signed K4 parity equivalence, and six hostile packet mutations. Both passed. Python is deterministic; independent JS LCG seed 128744. Finite tests corroborate but do not replace the symbolic proof.

**Artifact paths:** experiments/arc/lspv2_486_poststep_slack.py; experiments/arc/lspv2_486_poststep_independent.cjs; results/raw/arc/2026-11-07_LSPV2_486_POSTSTEP_SLACK_RAW.json and results/raw/arc/2026-11-07_LSPV2_486_INDEPENDENT_JS_RAW.json; research/coordination/2026-11-07_2321_LSPV2_POSTSTEP_SLACK486_FIVE_ROLE_HANDOFF.md.

No native indexed-FLMV interpreter, generic SAT guest, or authoritative historical R_mix341 checker executed. These host-language tests allocate interpreter objects and full sample source arrays, and yield NO machine time/space contraction theorem. A physical proposal must charge original source/index/head reads, all parsing and malformed detection, each guest call, child length, materialization or lazy ports, cache, joins, failed policies, output, evidence bits, ancestor retention/recomputation and all-phase writable peak. In particular the old materialized-child requirement $s'\le\max(\rho,\eta,\lambda,\lambda s)$ remains in force.

Root main.tex yielded a nonempty SHA but zero safely readable content; no partial replacement was attempted. Five roles, their enabled status, titles, schedules, 2A/3B allocation and historical R_mix341 rules/weights remain unchanged.

**Actual advance:** an exact sharp post-step error-tariff criterion, distinct from known four-channel bounds. **Verification:** independent exact-rational and floating-point executions plus authenticated original-clause K4 controls. **Publication:** role-owned report, code, raw results, handoff. **Remaining gap:** effective all-input, solver-dependent, exponent-oblivious, recursively iterable same-machine Phi(A) with complete charged resources; [P2-A2] and [P2-A5] OPEN. P versus NP OPEN.
