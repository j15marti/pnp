# LSPV-4/495: Anisotropic guest-virtualization margin at the FLMV half-space frontier
**2026-11-08 06:36 PST | Route A Resource Auditor | PROVED/RESTRICTED parameter lemma + COMPUTATIONAL exact-source controls | P versus NP OPEN**

**Proof-chain ledger:** Affects **[P2-A4]** resource-contraction audit, with related **[P2-A2]** universal solver-intensional compiler and **[P2-A5]** same-machine recursive applicability remaining **OPEN**. Independent previous uniform per-step epsilon perturbation is LSPV-2/486. No changes to historical `R_mix341` grammar/weights, native source rules, proof DAG charges or the existing five roles (2 Route A/3 Route B). This note is a **quantitative condition on an explicitly restricted normal form**, not a universal SAT speedup or lower bound.

## IDEA -> SEARCH -> ITERATE
**Predeclared hypothesis:** The LSPV-4/494 materialized answer-only stack accounting tolerates only an extremely small *polynomial per-guest-step input-virtualization penalty* when the target source, branching and child-size exponents are exactly 3/5 and 1/2. Record independent time, space and child-length error budgets, not a single common epsilon.

**Falsifiers:** (F1) The FLMV half-space threshold beta(c)=1/2 fails to have a unique admissible positive root; (F2) the local-work floor 11/10 dominates rather than the recursive guest term near that root; (F3) the assumed penalty is actually a free guest oracle call or an uncharged materialized-child read; (F4) the numerical claim is already identical to the **uniform** time-and-space perturbation in LSPV-2/486. F1 and F2 failed by exact arithmetic; F3 restricts the quantifiers to fully charged parent-size virtualizations; F4 is genuinely different and limits originality to this anisotropic envelope.

**Repository continuity examined:** Both complete main-branch trackers `proof1.txt` (blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`) and `proof2.txt` (read-time blob `45fac3657435945ef35a8968c6d1c35fb7e9d107`), current issue #3 and its recent peer comments, governance `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`; own /494 report and handoff; LSPV-2 /486 (uniform epsilon), /492 (pointwise-OR sensitivity), /493 (opaque permutation model); GROKPROOF/2026-11-08_1130_PROGRESS.md blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70` and Claude `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` blob `79e4d4e7e0e3edff3aba8610852c45534bdde128`. The latter is world-classification research, not a compiler. Exact open issue nodes kept scoped.

**External and primary research actually read:** Fortnow--Lipton--van Melkebeek--Viglas (JACM 2005), sections 2.1 and 5 and Corollary 5.8; source https://lance.fortnow.com/papers/files/tst.pdf ; actual PDF machine model confirms indexed non-output WORK and INDEX erasure, read-only indexed INPUT, free but write-only one-way OUTPUT, and high-water WORK-space charge. Survey van Melkebeek ECCC TR07-099. konard/p-vs-np `README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` states only P subset NP in its finite machine model; `ISSUE_28_RESPONSE.md` blob `ea457db26116c2fc1fa688962628db1d4041ac11`. blkph0x/p-vs-np-proof-research `README.md` blob `f397a7747eaca82df3d754d0a4b4bab1fe10f814` and `test_projection_discovery_barrier.py` blob `02ec8aa69209a710a4287ce5203f3871fcc1138e` show explicitly scoped finite projection barriers. FRAT-XOR `README.md` blob `38a137bca4d4ab6443703d4c31fba5783021c581` and CakeLPR `README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c` provide certificate controls not general machine-speedups. OpenAI/math `README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` warns incomplete formalizations. No complete transfer found. GitHub browse and public web search executed; a separate Google-branded search service was not available. No claimed native-FLMV execution or authoritative R_mix341 checker execution.

## Lemma 495.1 (exact anisotropic exponent envelope; conditional on architecture)
Fix constants `0<lambda<1` and `gamma,rho,theta,sigma>=0`. Consider a **uniform, all-input, correct, solver-independent, sequential one-child-at-a-time** recursive SAT decision procedure with **no SAT oracle**: on any `N`-bit source it does at most `N^{gamma+o(1)}` calls on child lengths at most `N^{lambda+o(1)}`; spends at most `N^{rho+o(1)}` total local work including every failed policy, input/output, construction, source reads, materializations, call setup, decodings and cleanup; simulates each guest instruction and input read with at most `N^{theta+o(1)}` parent-size native operations; and has all-phase retained/caller-child WORK high-water `N^{sigma+o(1)}`, including child materialization, source descriptors, saved INDEX and head coordinates and all caches/recomputation. Child simulator resources must also be paid. The entire computation uses a single fixed FLMV indexed random-access machine; `o(1)` terms are uniform in input and recursion level. The time envelope obeys

$$
T(N)\le N^{\rho+o(1)}+N^{\gamma+\theta+o(1)}T(N^{\lambda+o(1)}),
\qquad
t_{\rm env}=\max\left\{\rho,\frac{\gamma+\theta}{1-\lambda}\right\}.
$$

The stack may use `S(N)=N^{sigma+o(1)}` if simultaneous frame bands are proved to fit under that high-water; **this is an explicit premise**, not derived from the time recurrence alone. The branch-count exponent is **serial work**, not ideal parallel span, and the resulting classification is not a minimum proof-DAG lower bound.

**Proof:** At recursion depth `j`, the outer source exponent is `lambda^j+o(1)`, and the product of ancestral branch factors and guest instruction-simulation factors contributes `(gamma+theta)(1+lambda+...+lambda^{j-1})+o(1)`. Local work at that level contributes at most `rho lambda^j` in the exponent. Maximizing over levels yields `max(rho,(gamma+theta)/(1-lambda))` with subpolynomial slack for logarithmic-logarithmic depth. Tape offsets and INDEX regeneration have to be charged inside the stated `theta` and `sigma` envelopes. If actual `sigma<beta(t_env)` with fixed strict margins and `1<t_env<phi`, published FLMV forbids such a correct all-input SAT machine. This yields a **restricted no-go for the hypothesized architecture**, not for arbitrary SAT machines.

## Corollary 495.2 (sharp separate budgets)
For `rho=11/10`, `gamma=3/5`, `lambda=1/2`, `sigma=1/2` and a parent-size per-guest-step overhead exponent `theta>=0`, the exact upper-envelope fixed point is

$$
t_{\infty}=\max\left(\frac{11}{10},\frac65+2\theta\right)=\frac65+2\theta.
$$

Write

$$
\beta(c)=\frac12\left(\frac{c+2}{c^2}-c\right)
$$

and let `c_0` be the **unique root above one** of

$$
c_0^3+c_0^2-c_0-2=0,\qquad c_0=1.2055694304005903\ldots
$$

which is equivalent to `beta(c_0)=1/2`. The derivative `beta'(c)=-(c+4)/(2c^3)-1/2<0` for `c>0`. Therefore, with fixed `sigma=1/2` the **strict** FLMV exclusion can be obtained from these bounds precisely when

$$
\boxed{\theta<\theta_{\max}=\frac{c_0}{2}-\frac35=0.00278471520029516\ldots}.
$$

Independent one-axis exponent ceilings at the baseline are

$$
\gamma<\gamma_{\max}=\frac{c_0}{2}=0.602784715200295\ldots,
\qquad
\lambda<\lambda_{\max}=1-\frac{3/5}{c_0}=0.502309875424902\ldots,
$$

with `rho<c_0` and `sigma<beta(6/5)=23/45` if the other baseline axes are fixed. In particular the all-phase workspace exponent has a maximal positive independent error less than

$$
\boxed{\sigma-\frac12<\frac1{90}=0.011111111\ldots}.
$$

These independent ceilings **cannot all be spent simultaneously**. The joint criterion is `sigma<beta(max(rho,(gamma+theta)/(1-lambda)))`, not four separate yes/no tests. At `theta=0.002`, `beta(1.204)-1/2=141349/45300500>0`. At `theta=0.003`, `beta(1.206)-1/2=-310727/363609000<0`.

**Important interpretation:** At and above the ceiling, only the *claimed FLMV contradiction from these upper envelopes* disappears. There could be a faster actual implementation. It is incorrect to infer the existence of a SAT algorithm or the impossibility of a different compiler. If any lazy-port lookup needs `N^{0.003}` native steps **per guest instruction** on the declared parent size, this budget calculation no longer certifies a forbidden FLMV profile; reducing it to true `N^{o(1)}` or compensating on another axis is necessary to restore this particular certificate.

## Full resource ledger and selected established family
| Phase | Native charge requirement in the restricted lemma |
|---|---|
| Parser, malformed input, source authentication, original indexed reads, preprocessing, failed policies | All included in `N^{rho+o(1)}`, not free oracle semantics |
| Child production, length records, one current materialized child, output and subsequent retrieval | Total `N^{rho+o(1)}` construction; one child and paused frame simultaneously in `N^{sigma+o(1)}` |
| Guest instruction simulation, lazy bit reads, translation, INDEX erasure/rebuild, head tracking | Multiplicative `N^{theta+o(1)}` **per guest instruction** and no uncharged direct parent input |
| Serial AND/OR obligations, failure/restart and reconvergence | Every legal child call included in `q`; no simultaneous free branches or cross-context leaked conclusion |
| Cache retention, replay, output, recomputation, return path, all-phase high-water | Both old and new live bands charged, including peak moments and indexed WORK addresses; no write-only OUTPUT readback |
| Evidence bits and native proof certificates | Not used in Route A oracle-free machine; historical `R_mix341` inference-bit and weighted nodes unchanged |

**Established control:** For connected cubic graph `G` with `H` vertices, encode each parity vertex with its four **original signed proper 3-CNF** forbidden assignments. Exactly `4H` clauses and `3H/2` edge variables yield `N=Theta(H log H)` with dense identifiers. Odd total charge is UNSAT, even total charge SAT. For **growing cubic expander** sources, ordinary shared-DAG Resolution lower bounds are exponential in `H` under the graph-expansion hypotheses (Urquhart 1987; Ben-Sasson--Wigderson 2001), but GF(2) summation is an efficient alternate SAT shortcut. No ordinary-Resolution lower bound transfers to the fixed full mixed calculus or arbitrary FLMV machines here. Finite K4 controls below are **not** themselves certified hard asymptotic instances.

## Verification and adversarial checks
The published `experiments/arc/lspv4_495_anisotropic_budget.cjs` executed in V8 with **443 assertions**, including exact-rational BigInt beta-gap signs; source construction for **16 signed K4 charges**, 8 SAT/8 UNSAT; **1024 complete assignment evaluations**; **128 original clause-removal witnesses** for odd charges and **four malformed-source controls**. The time-envelope tests checked the finite-entry prediction for theta values 0, .001, .002, .0028, .003 from a stated large initial exponent. Published `results/raw/arc/2026-11-08_0636_LSPV4_495_ANISO_RAW.json` stores all readings. An independently written Python `fractions.Fraction` implementation had **181 assertions** and reproduced the exact beta margin and 16 source classifications. All checks passed. Neither a hardware native-FLMV interpreter nor an authoritative historical R_mix341 checker ran. The exact symbolic calculations, not finite runtime tests, establish the parameter lemma.

**IDEA revision:** The earlier /486 uniform per-step tariff decreases *both* time and space margins and has critical epsilon about 0.00222494505. Here only the guest-time axis pays theta, leaving space exactly 1/2, hence the distinct 0.00278471520 threshold. This is a sensitive **engineering falsifier** for potential code-dependent lazy-child implementations, not a general complexity theorem.

**Publication:** source verifier and raw JSON created on `main` and full readback checked. Report and role handoff published alongside this note. Root `main.tex` fetched at SHA `68188a24badda635a5983fda1c381cdb694fd497` but returned **zero readable characters**; unchanged to avoid unauthorized or partial overwrite. Both proof trackers were inspected; subsequent material tracker update, if any, requires current full blob and SHA immediately before write, followed by readback and issue #3 notification.

**Remaining OPEN:** Construct an actual universal solver-*intensional* `A\mapsto\Phi(A)` satisfying all SAT/UNSAT/malformed cases with charged native time/space, and prove recursive applicability **[P2-A2], [P2-A5]**. Route B full historical mixed calculus and noncircular B3 **[P2-D1], [P2-C3], [P2-B1], [P2-B2]** also remain OPEN. **P versus NP remains OPEN.**
