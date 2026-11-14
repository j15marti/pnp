# TMR-1/025: Exact approximation-gap invariance under MCSP dummy padding; new uniform magnification theorem comparison

**Date:** November 14, 2026, 11:10 PST (America/Los_Angeles). **Owner:** TMR-1 Machine Model Lead. **Status:** APPROXPAD25 **PROVED/RESTRICTED elementary argument, independent TMR-2/TMR-5 review pending**; finite checks COMPUTATIONAL. Neither P=NP nor P!=NP is established. No agent or schedule changes.

## 1. Genuinely new relative to prior project work

TMR-1/024 proved exact gate-minimum equality for ignored-variable padding in the fan-in-two AND/OR and unary-NOT basis, with free constants and input wires. It analyzed explicit-output exponent loss for ordinary MCSP and warned about matching *integer* thresholds. The older October 18 ASYMPTOTIC_CONE5 already analyzed why padding does not automatically amplify a useful lower-bound slope. TMR-4/026 and TMR-5/022 subsequently proved resource lower bounds for *permutation* transducers under one-way input plus append-only output. The October 18 MAGRED_STREAM_NO10 showed a sampled threshold construction could mislabel original YES inputs.

**New here:** a complete **normalized Hamming distance identity**, simultaneously for *every* source truth table, *every* circuit threshold and *every* number of ignored inputs. This extends the prior exact YES/NO identity to the precisely defined **approximation promise** used by a verified 2025 uniform magnification paper. A one-spike adversarial input independently falsifies transferring arbitrary ordinary-MCSP NO instances to approximation-MCSP NO promises. These are not new general MCSP time lower bounds.

A further primary-source addition, not mentioned in the five most recent TMR handoffs nor canonical main.tex: Atserias and Müller, *Simple general magnification of circuit lower bounds*, arXiv:2503.24061v2 (June 2025), Theorems 11 and 27. Its uniform magnification conclusion is **P != NP^(oplus P)**, not the required **P != NP**. Its premise is a **P-uniform circuit-size** lower bound for an **approximate promise** problem, not CHMY's **one-work-tape time** lower bound for **ordinary decision** MCSP. We must not import one into the other.

## 2. Exact definitions and theorem ledger

Set the circuit arity to n, its explicit truth-table length N=2^n, the circuit-size threshold to an integer s, and the 3-SAT source bit length separately to L. Let C(n,s) be the set of Boolean functions on n inputs with fan-in-two AND/OR gates, unary NOT, arbitrary fan-out, free named input wires and constants, and at most s gates. Define

$$
\Delta_{n,s}(f)=\min_{g\in C(n,s)}\frac{d_H(\mathrm{TT}(f),\mathrm{TT}(g))}{2^n}.
$$

Define the ignored-input extension E_t(f)(x,z)=f(x), with t>=1 new inputs, truth-table size M=2^{n+t}=2^t N. This is *not* a SAT formula reduction, and it is not a succinct MCSP instance.

For a gap parameter eta in (0,1], the promise problem eta-MCSP[s] has YES instances with Delta=0 and NO instances with Delta>=eta; cases with 0<Delta<eta are **outside the promise**.

| Primary source and theorem | Problem and exact input measure | Model and stated conditional conclusion | Firewall |
| --- | --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, Thm 1, pp. 23:3-4 | Ordinary fixed-threshold MCSP[2^(mu_1 n)], N=2^n, small fixed mu_1 | Excluding deterministic one-way-input/one-work-tape O(N^1.01) implies P != NP | Required low-threshold exclusion remains OPEN |
| Same paper, Thms 2-3, pp. 23:3-4 | Ordinary MCSP at a *different* larger threshold mu_2; Thm 3 mu>1/2 and N^o(1)-length oracle queries | Randomized two-sided-error one-way-input/one-work-tape N^1.99 lower bound for Thm 2; short-oracle restrictions for Thm 3 | Cannot switch thresholds or input access |
| McKay, Murray, Williams, STOC 2019, Thms 1.2-1.3 | Search-MCSP with optional A-oracle gates, N-bit full stream, s(n)>=n | Appropriate simultaneous poly(s)-space AND poly(s)-update exclusion in the specified uniform streaming search model implies P != NP | Neither ordinary decision lower bounds nor a space-only argument suffice |
| Atserias, Müller, arXiv:2503.24061v2, Thm 27, p. 17 (Thm 11, p. 6) | N^(-epsilon)-MCSP[sigma] promise, sigma(n)<=2^(gamma n), where N=2^n | For all delta,epsilon>0, there is gamma>0: excluding P-uniform-SIZE[N^(1+epsilon+delta)] implies **P != NP^(oplus P)** | This is a uniform **circuit** lower-bound hypothesis, different promise, and a different separation |
| Atserias, Müller, Thm 9, p. 5 | N^(-epsilon)-Q for a 2^(N^o(1))-sparse NP language Q | Certain nonuniform formula/probabilistic-formula bounds imply NP not subset NC1 | Not a deterministic one-tape bound or direct P != NP |

Sources: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2021.23 ; https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf ; https://arxiv.org/pdf/2503.24061 (v2, 21 June 2025). Theorem 27's P-uniformity constructs circuit families in polynomial time in their truth-table input length N, not finite Turing-machine source-time bounds. The paper also studies sparse problems and formulas; no variant swap is made here. In particular, P != NP^(oplus P) does not by itself imply P != NP.

## 3. NEW APPROXPAD25 exact Hamming-gap theorem

**Statement.** For every n>=1, t>=0, s>=0, and Boolean function f:{0,1}^n -> {0,1},

$$
\boxed{\Delta_{n+t,s}(E_t f)=\Delta_{n,s}(f).}
$$

The equality holds in the specified gate basis with free constants and for every input f, not merely YES sources or random functions.

**Proof, upper bound.** Choose any optimal n-input g with CC(g)<=s. Ignoring z gives E_t g with the same gate count. Every original assignment is repeated 2^t times, so

$$
d_H(E_t f,E_t g)=2^t\,d_H(f,g).
$$

Dividing by M gives Delta_{n+t,s}(E_t f)<=Delta_{n,s}(f).

**Proof, lower bound.** Choose *any* (n+t)-input h with CC(h)<=s. For each z in {0,1}^t, restrict the t new inputs to that constant assignment. Simplifying the resulting AND/OR/NOT circuit produces an n-input h_z with CC(h_z)<=s, because free constants exist and gate count cannot increase under restriction. Therefore

$$
\frac{d_H(E_t f,h)}{M}
 =2^{-t}\sum_{z\in\{0,1\}^t}
       \frac{d_H(f,h_z)}{N}
 \ge\Delta_{n,s}(f).
$$

Minimizing over h proves the reverse inequality. QED.

**Corollary 1 (exact promise transfer, identical integer s).** At any *fixed* eta, E_t is an exact YES/NO-preserving map from eta-MCSP_n[s] to eta-MCSP_(n+t)[s]. For length-varying eta_N=N^(-epsilon), epsilon>0, an eta_N-promised NO source maps to an eta_M-promised NO target, because eta_M<=eta_N. The reverse implication is not automatic.

**Corollary 2 (explicit-output cost).** If the reduction actually materializes the full M-bit truth table in a standard locally moving finite-alphabet output model, it costs Omega(M) output operations, regardless of the algebraic identity. For threshold exponents mu_h>mu_l, keeping s=floor(2^(mu_h n))=floor(2^(mu_l(n+t))) typically requires M=N^rho with rho≈mu_h/mu_l, subject to exact floor/rounding alignment. Consequently the quantitative generic N^1.99 composition corridor from TMR-1/024 still applies; the promise identity does *not* cure output explosion. A succinct circuit or re-readable output oracle is a different problem and requires its own charged simulation.

**Counterexample (ordinary NO need not satisfy an approximation NO promise).** For n=3, s=0, let f be 1 at exactly one of eight assignments and 0 elsewhere. In this basis, CC(f)>0 so f is ordinary MCSP[0] NO; however Delta_{3,0}(f)=1/8<1/4. Hence it is neither YES nor promised NO for (1/4)-MCSP[0]. This explicitly defeats the inference 'known hard ordinary-MCSP NO instances are automatically hard promise-MCSP NO instances'. The example itself is a *label gap*, not a lower bound on decision time.

## 4. Executed finite evidence and hostile controls

Exact native CPython executed experiments/tmr/tmr1_approx_padding025.py. It enumerated complete truth-table classes of circuits with 0,1,2 gates, on n=2,3 and padded arities 3,4, including input/constant outputs and both output labels. It checked **816 individual source truth tables at six (n,s) parameter settings** against the target optimum and verified that padded minimum Hamming distance equals *twice* source minimum distance. All 816 ordinary YES/NO labels also agree. It counted 40, 76 and 131 ordinary NO sources at n=3 and s=0,1,2 that fail the 1/4-far NO promise, respectively, and checked the one-spike counterexample. Zero failed assertions. Original raw: results/raw/tmr/2026-11-14_1103_TMR1_APPROXPAD025_RAW.json. These experiments are FINITE COMPUTATIONAL controls, not an asymptotic proof and not a machine compiler. The mathematical proof above covers arbitrary n,t,s.

Hostile algorithms remain allowed: source rereading when available; compact factorization; Gaussian elimination on XOR/Tseitin encodings; Horn/2-SAT/low-treewidth methods; products and sharing; cache or recompute; variable renaming and alternative gates. No mandatory assignment enumeration or proof-system certificate has been imposed.

## 5. Exact remaining gap and next peer target

**CHMY route OPEN:** Need ordinary small-threshold MCSP outside deterministic one-way-input/one-work-tape O(N^1.01), or a both-label, low-cost high-threshold to low-threshold transfer with precise circuit-threshold floors and a matching machine simulation. APPROXPAD25 leaves high-threshold bounds in the wrong parameter regime and does not supply such a lower bound.

**Atserias-Müller route OPEN:** Need a P-uniform circuit-size lower bound for *approximation-promise* MCSP at the theorem's gamma, epsilon and delta parameters. CHMY's ordinary decision one-tape lower bound is not this premise. Even obtaining the new paper's stated magnification conclusion P != NP^(oplus P) would not by itself settle P vs NP. An additional valid implication would be required.

**Single next target:** TMR-2 and TMR-5 independently check the restriction/average equality and promise direction, then test one candidate strong-enough *uniform circuit* lower-bound transfer without replacing the promise by ordinary MCSP. TMR-3 must charge explicit truth-table expansion and any P-uniform-circuit-to-one-tape simulator. TMR-4 should examine whether a non-padding, source-sensitive mapping respects both the circuit threshold and the Hamming-distance NO gap. TMR-1 will keep CHMY the primary P!=NP chain while recording the 2025 uniform result as a separate optional route.

## 6. Provenance and integrity

Read newest November 14 MCSP directive FIRST (Git blob 1e11aa64a0b0d635a65cea58500b09f2b0fe010a), November 13 TMR role replacement (47459817e66dccf1d07...), all five TMR handoffs, issue #3, AGENTS.md, CODEX.md, pnp-research skill, full proof1.txt (28,714 chars; 06f7ebc8c2283304a0f5200b518c6e48fa41e343), authentic full proof2.txt via Git blob (1,051,196 chars; 930c5eeddafce656717f28055a7a9a755f44737c), and full main.tex via Git blob (2,545,859 chars; 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34). Inspected original TMR-1/024, TMR-2/025, TMR-3/025, TMR-4/026, TMR-5/022 reports, October ASYMPTOTIC_CONE5, THRES_ENTROPY1, MAGRED_STREAM_NO10, and original Claude ONETAPE and DIRECTPRODUCT reports. Consulted primary CHMY, MMW and Atserias-Müller PDFs (including original page renderings). The exact new paper was not found in the latest five role handoffs or canonical manuscript; this is a scoped novelty finding, not a complete corpus-wide absence theorem.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No root proof1/proof2 or canonical main.tex edits are warranted while the P!=NP arrow remains OPEN; TMR-5 owns manuscript synthesis. No tasks, roles, titles or schedules modified. Independent proof review is OPEN; P vs NP is OPEN.

END_OF_REPORT::TMR1::025::2026-11-14_1110_PST
