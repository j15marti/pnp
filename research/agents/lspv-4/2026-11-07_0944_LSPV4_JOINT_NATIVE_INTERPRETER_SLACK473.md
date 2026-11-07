# LSPV-4/473 | Joint native-interpreter exponent-slack frontier

**November 7, 2026, 09:44 PST, America/Los_Angeles. Route A, P versus NP OPEN.**
Status: **PROVED/RESTRICTED**, an exact conditional exponent-envelope lemma, and **COMPUTATIONAL**, independent finite numeric checks. Neither a SAT algorithm nor a native FLMV interpreter is supplied.

## IDEA -> SEARCH -> ITERATE, falsifiers

**Idea:** Evaluate *simultaneous* positive polynomial time/space exponent penalties imposed by a native guest interpreter on the formerly proposed tree compiler. This isolates the cost of INDEX/WORK conversion from per-stage construction costs. Falsifiers stated before source review: (F1) primary FLMV Corollary 5.8 differs from the claimed $\beta(c)$; (F2) the fixed points below fail algebraic substitution; (F3) some finite initial exponent pair prevents eventual strict entry despite a strictly positive fixed-point margin; (F4) the recurrence is being used without a legal all-input recursively iterable transformation, paid local phases, or authenticated INDEX metric. F1-F3 rejected in the restricted model; F4 remains OPEN, preventing any P-versus-NP conclusion.

**Primary source:** Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, Corollary 5.8, printed p.18, https://lance.fortnow.com/papers/files/tst.pdf. Also inspected machine definition §2.1 and the 2007 van Melkebeek survey §2.1, https://pages.cs.wisc.edu/~dieter/Papers/sat-lb-survey-fttcs.pdf. The exact INDEX-space convention remains qualified as in peer LSPV-4/472, not silently settled.

**Project prior art:** LSPV-4/343, `research/agents/lspv-4/2026-11-02_1436_LSPV-4_FLMV_MARGIN_OUTPUT_STREAM343.md` (blob `6520d6c1`) established the unperturbed fixed point and separate fanout, child-size, probe margins. `research/main/2026-10-22_1948_MAIN_FLMV_PROBE_MARGIN71.md` (blob `bec92643`) established the half-space critical root and rational safe point. **Those are not new.** The increment here is a simultaneous **per-guest native interpreter** penalty, its exact joint frontier and a uniform finite-entry witness. Read both complete trackers (proof1 initial `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, proof2 initial `af85f01efdb8d86c131cabc063d7c8cf2806c1d3`), current issue #3, governing handoff `c3889a3e`, AGENTS.md `19656af1`, CODEX.md `754999f5`, skill `b8df83a7`, LSPV-2/472 `b9e48f7c`, LSPV-4/472 `977c9f1a`, actual Grok `GROKPROOF/2026-11-07_1220_PROGRESS.md` `2c450bb3`, Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` `9a5b05d6`.

**External source review (exact checked paths/blobs):** `konard/p-vs-np/README.md` `0e0ec77f`, `proofs/complexity/README.md` `7ee9a11e` (separate finite one-tape semantics); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` `18d693ea`, `INDEPENDENT_AUDIT.md` `b30515cc` (acquisition restrictions); `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` `4bb5fd19`; `meelgroup/frat-xor/format.md` `986a21aa` (non-native proof format); `openai/math/README.md` `cc5b0a03` (uneven formalization status). Public web literature search was available, separately branded Google and native FLMV execution were not. No external repository proves a universal reduction.

## Theorem 473.1 (PROVED/RESTRICTED): exact joint *upper-envelope* feasibility

**Assumptions, unproved for general SAT:** For EVERY fixed uniform total correct polynomial SAT decider A with arbitrary finite time/space exponents $(t,s)$, suppose an effective all-input same-FLMV-machine both-label/malformed-aware transformation is recursively applicable and makes $q\le N^{3/5+o(1)}$ sequential SAT calls on $B\le N^{1/2+o(1)}$, with ALL non-guest phases charged within local $N^{11/10+o(1)}$ time and $N^{1/2+o(1)}$ peak space, and the native guest interpreter adds at most $B^{\theta+o(1)}$ multiplicative time and $B^{\omega+o(1)}$ multiplicative **charged guest-space** penalty for constants $\theta,\omega\ge0$. This explicitly requires real source, INDEX, WORK, head, failed-policy, materialization/lazy port, output, reset, cache, ancestor and total simultaneous peak charges; none is being proved here.

Then the charged exponent envelopes are

$$
t_{j+1}\le\max\left(\frac{11}{10},\frac35+\frac{t_j+\theta}{2}\right),
\qquad
s_{j+1}\le\max\left(\frac12,\frac{s_j+\omega}{2}\right).
$$

Their monotone 1/2-contractive maps have unique fixed points

$$
T_*=\frac65+\theta,\qquad S_*=\max\left(\frac12,\omega\right).
$$

With FLMV Corollary 5.8

$$
\beta(c)=\frac12\left(\frac{c+2}{c^2}-c\right),
$$

**these upper envelopes guarantee finite strict FLMV-region entry from every finite initial $(t_0,s_0)$ if and only if**

$$
\boxed{\max(1/2,\omega)<\beta(6/5+\theta).}
$$

The iff concerns **guarantees of this exact envelope**, not existence of other faster SAT methods or stronger FLMV theorems. For sufficiency write $a=(t_0-T_*)_+$, $b=(s_0-S_*)_+$, $m=\beta(T_*)-S_*>0$ and $L=(1+T_*^{-2}+4T_*^{-3})/2$. The monotone half-contractions give $t_j\le T_*+2^{-j}a$ and $s_j\le S_*+2^{-j}b$. Because $\beta'(c)=-(1+c^{-2}+4c^{-3})/2$ and $|\beta'|$ decreases for $c>0$,

$$
\beta(t_j)-s_j\ge m-2^{-j}(La+b).
$$

Any finite $j$ satisfying $2^{-j}(La+b)<m$ gives a strict gap. Conversely, initialize the equality recurrences at their fixed point when $S_*\ge\beta(T_*)$; no strict entry can be forced by these envelopes.

## Sharp *Corollary 5.8 only* interpreter time budget

The half-space boundary $c_{1/2}$ solves $c^3+c^2-c-2=0$, giving $c_{1/2}=1.2055694304005903\ldots$. When $\omega\le1/2$, strict entry via this envelope requires

$$
\boxed{\theta<c_{1/2}-6/5=0.0055694304005903\ldots .}
$$

For the rational safe time overhead $\theta=1/200$, $T_*=241/200$ and $\beta(T_*)=11642479/23232400=0.5011311358\ldots$. Thus $\omega=0.501$ passes while $\omega=0.502$ fails. $\theta=0.006$ fails even when $\omega=0.5$. Polylog interpreter overhead corresponds to $\theta=\omega=0$ **only if actually established for every phase**. A one-time $N^d$ preprocessing cost goes in the separate local exponent, NOT in $\theta$.

## Exact family/control and finite checks

Existing known family: odd-charge Tseitin parity contradictions on simple cubic expander graphs with $H$ vertices, $3H/2$ edge variables and four strict width-three forbidden-assignment clauses at each vertex (total $4H$ clauses, encoded length $\Theta(H\log H)$ for ordinary binary edge IDs). Published exponential ordinary DAG-Resolution lower bound: Urquhart (1987) and Ben-Sasson/Wigderson (2001) with suitable expansion hypotheses. GF(2) sums the charge equations and is a short *algebraic shortcut*: no hardness inference for fixed mixed `R_mix341`, arbitrary SAT machines or B3. No new family constructed.

Independent executable **Python** exact `Fraction` tests (4,000 deterministic trials): 8,000 fixed-point checks, 224,000 envelope checks, 50,816 strict-entry checks and seven exact rational controls. **JavaScript** different deterministic pseudo-random dataset (4,000 trials, 282,816 floating-point assertions, 50,810 strict-entry checks). Both reproduce the same threshold and qualitative rational tests. **The random corpora are intentionally different and are not claimed to match per-instance.** Host-language arithmetic tests, NOT native FLMV machine measurements.

Code: `experiments/arc/lspv4_473_joint_slack.py`, `experiments/arc/lspv4_473_joint_slack_independent.cjs`. Raw: `results/raw/arc/2026-11-07_0944_LSPV4_473_JOINT_SLACK_PYTHON.json`, `results/raw/arc/2026-11-07_0944_LSPV4_473_JOINT_SLACK_JS.json`. Full local reproduction archive retained.

## Limits and next exact obligation

This is **resource-envelope arithmetic**, not an actual implementation: logical node weights and certificate bits are irrelevant to the tested code; parser, failed branches, source/index/head probes, source authentication, guest simulation, resets, output, caches, storage, replay, recomputation, and all-phase peak must be measured before use. Original exact INDEX-space metric and its full native implementation remain OPEN (peer LSPV-4/472). Open chain IDs: **[P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04]**; Route B **[P2-D1], [P2-B1], [P2-B2]** untouched. No change to historical R_mix341 grammar, weights or the five-agent assignment.

**Actual advance:** simultaneous quantified native-interpreter exponent feasibility test, extending established /343 single-factor margins. **Verification:** elementary symbolic proof plus two independent finite arithmetic executables. **Precise gap:** native correct same-machine guest interpreter with measured $\theta=\omega=0$ (or a verified pair inside the frontier), plus the all-input recursively applicable transform. **P versus NP OPEN.**
