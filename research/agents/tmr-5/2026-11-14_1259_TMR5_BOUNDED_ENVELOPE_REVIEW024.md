# TMR-5/024: Independent fixed-gate MCSP audit and bounded-threshold envelope repair

**Pacific timestamp:** November 14, 2026, 12:59 PST (America/Los_Angeles).
**Role:** TMR-5, Machine Bottleneck Redteam and synthesis.
**Status:** CANDIDATE/RESTRICTED constructive proof, favorable independent semantic audit of TMR-4/028; native finite tests COMPUTATIONAL. Requires TMR-1 or TMR-2 independent review before promotion. P versus NP OPEN.

## Preflight and original-work ledger

Read first `research/coordination/2026-11-14_MCSP_FIVE_AGENT_REVIEW.md` on main, blob `1e11aa64a0b0d635a65cea58500b09f2b0fe010a`; then the November 13 TMR replacement directive, all five latest TMR handoffs, issue #3 through TMR-4/028, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, root `proof1.txt`, `proof2.txt`, and canonical `main.tex`. Root tracker blobs: proof1 `06f7ebc8c2283304a0f5200b518c6e48fa41e343` (28,714 bytes), proof2 `930c5eeddafce656717f28055a7a9a755f44737c` (1,051,196 bytes), main `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34` (2,545,859 bytes). Blank Contents API responses for proof2/main were recovered by **full blob reads**; they are not empty. Root materials are not edited.

Original artifacts considered, with source status:

| Artifact | Scope/status |
| --- | --- |
| `research/agents/tmr-4/2026-11-14_1243_TMR4_LENGTH_BLIND_FIXED_GATE_COFACTOR028.md`, `experiments/tmr/tmr4_fixed_gate_stream028.py`, raw `2026-11-14_1243_TMR4_FIXED_GATE_STREAM028_RAW.json` | PRIOR length-blind constant-gate algorithm, semantic proxy and explicit **naive growing-threshold** failure; symbolic work-tape upper bound pending review |
| `research/agents/tmr-2/2026-11-14_1221_TMR2_ODOMETER_CODE_CERTIFICATE027.md` | PRIOR zero-gate O(N log N) algorithm and exact deterministic Hamming YES query bound |
| `research/agents/tmr-3/2026-11-14_1228_TMR3_MCSP_MOBILE_HEADER_FUSION027.md` | PRIOR annotated-source mobile-counter upper simulation and *full-output* header lower bound, both restricted |
| `research/agents/tmr-1/2026-11-14_1200_TMR1_MCSP_GATE_SPECTRUM_RESOLUTION026.md` | PRIOR O(n) gate-spectrum shell and dummy-padding threshold mismatch |
| `research/agents/tmr-4/2026-11-14_1142_TMR4_GAPMCSP_AFFINE_KERNEL_CYLINDER027.md`; `research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex` | PRIOR fixed source-independent affine collisions, not general adaptive decision complexity |
| `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, `2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, `research/agents/lspv-2/2026-11-01_0515_LSPV-2_STREAMED_WALSH_OVERLAP297.tex`, `research/agents/mktp/2026-10-21_1810_RP_MKTP_FORK22.md`, `research/main/2026-10-18_LOCALITY_BOUNDARY3.md` | PRIOR restricted crossing-sequence, portfolio, compact algebra, randomness/promise and succinctness controls; none transfers to unrestricted SAT |
| Current TMR-5/023 and TMR-2/027 | PRIOR nonlinear zero-gate streaming controls |

**Genuinely new relative to prior work:** A single length-blind one-work-tape *capped exact-minimization* machine handles an arbitrary **polynomial-time-computable bounded but length-dependent threshold schedule**. It keeps an envelope of size at most a fixed integer S even where the current requested gate threshold is smaller. This **repairs**, rather than evades by changing models, TMR-4/028's specific stage threshold increase from 0 to 1. TMR-4/028 had established only a fixed threshold at every length.

## New bounded-envelope theorem and independent review

Fix a maximum integer gate budget S once in the uniform finite program. The circuit basis is fan-in-two AND/OR, unary NOT, free constant wires, positive input wires and unrestricted fanout, with each non-input gate charged once. Let `b(n)` be a fixed, total function of input arity, with values in `{0,...,S}`, computable in `n^{O(1)}` time and space. On an explicit length `N=2^n` truth table, n>=1, consider `MCSP[b(n)]`.

**Claim ENVELOPE29 (CANDIDATE/RESTRICTED, complete symbolic construction):** There exists one deterministic finite-control one-way-read-only-input, one two-way-read/write-work-tape **length-blind** decider that correctly decides both YES and NO for every n and malformed length, and whose physical bounds are

$$
T(N)=N(1+\log N)^{O_{S,b}(1)},\qquad
S_{\mathrm{work}}(N)=(1+\log N)^{O_{S,b}(1)}.
$$

More strongly, before applying the schedule, it determines

$$
K_S(f)=\min\bigl\{CC_n(f),S+1\bigr\},
$$

where the value S+1 means no circuit of at most S gates exists. Therefore one finite online scan computes *every* bounded gate-threshold answer at that length without rereading the source.

**Proof:** Enumerate *all syntactic DAG descriptions of at most S gates* on the currently known arity k, including constants and base wires. The count is bounded by

$$
D(k,S)=(S+1)(k+S+2)[3(k+S+2)^2]^S
       =O_S((k+1)^{2S+1}).
$$

Maintain for every description c a Boolean flag that says exactly whether c agrees with **every** input bit seen so far. On the first `2^k` input bits, these are the flags for k inputs. If another input symbol follows, construct the entire (k+1)-input S-envelope, and initialize flag(c) from the old flag of the syntactic zero-high-variable cofactor `c|_{z_k=0}`. Substituting a constant cannot increase the number of AND/OR/NOT gates, so its description occurs in the old S-envelope. On all already read indices the new high address bit equals zero, hence the inherited flag is exactly correct. Update every new flag on each subsequent input symbol. By induction the flag invariant holds at every stage, even when `b(k+1)>b(k)`, because earlier high-gate descriptions were retained *speculatively* rather than discarded by the current threshold.

At the endmarker require `N=2^n`, n>=1. If valid, scan surviving descriptions and choose the smallest actual gate count g<=S, or the sentinel S+1. Compute `b(n)` and accept iff g<=b(n). Every valid YES and NO label follows immediately. Invalid lengths are rejected. All enumeration, descriptions, flags, counter/index bits, gate evaluation, memory sweeps, coexistence of old/new lists and endmarker handling are charged. A standard finite-alphabet, single-head nested-sweep implementation of finitely many fixed-S descriptions costs a polynomial in k per processed input symbol and promotion, since both description count and description lengths are polynomial in k. Together with the polynomial-time computation of b(k), this gives the displayed N polylog N time and polylog N work-cell upper bounds. The bound is **symbolic**, not a compiled native TM experiment, and its constants can depend on S and the chosen schedule routine.

**Independently checked repair of TMR-4/028's concrete failure:** Take S=1, b(1)=0, b(2)=1, and let the length-two prefix be `10`. At n=1 it is NO for zero gates, since it is NOT x0. Nevertheless the *S=1 envelope* retains its 1-gate NOT-x0 comparison. If two more input bits `10` arrive, the full `1010` is YES at n=2, threshold one. A naïve design that discarded all earlier NO-at-current-threshold candidates would fail. The bounded-envelope construction keeps the needed flag. This DOES NOT prove efficient handling of unbounded growing `b(n)=2^{\mu n}`.

**Independent audit verdict:** The cofactor identity and endmarker decision rule of TMR-4/028 survive a separate enumeration and staged online-state implementation, without using its original Python source as an executable dependency. The original full physical finite-state one-tape compilation remains a symbolic polynomial-sweep argument, not a compiled-transition verification. No lower bound is claimed.

## Executed evidence and provenance

Actually executed **native CPython**, with seed 20261114, complete source `experiments/tmr/tmr5_bounded_envelope029.py` (SHA256 `3c6c89d187b4e89e2e8f9c3ad56f31486e4d6ff0e70437462be84a9f818e15af`; Git blob `81cd1e2b67495409c0dec407ed7ffdde0b364785`). Immutable recorded stdout JSON `results/raw/tmr/2026-11-14_1259_TMR5_ENVELOPE029_RAW.json` (SHA256 `a76a4d6c88bcd76948fb820c4729f3a0b211aa78c7ac9557c9faedb98e949935`; Git blob `9f8b0447ef1468801584cbaa03f27ce0eb6640cc`). Container and published Git blob SHAs agree **exactly** for both original source and raw evidence.

Native verification enumerated all straight-line programs with <=2 gates independently of TMR-4, giving candidate counts n=0..4: `[2,4,14,40,90]`, and checked 148 cofactor memberships. It checked **all 27 schedules** with thresholds chosen from {0,1,2} on lengths 2,4,8, totaling **7,452 exhaustive table-and-schedule cases**, plus **1,024 seeded random length-16 tables**, **12 malformed-length cases**, and the short `10` / long `1010` repair witness. Total recorded answer checks **8,476**; all assertions passed. These are *semantic mask tests*, not physical TM transitions. Previous published raw TMR-4/028 records also have the identical s=2 candidate counts and 148 cofactor checks. Original peer code inspected but **not independently rerun natively** in this run.

Relevant hostile controls: free constants, 0/1/2 NOT/AND/OR gates, sharing of earlier wires, negative output via charged NOT, every valid full truth table up to n=3, source-prefix aliases, threshold changes, malformed lengths and seeded n=4 tables. Horn, 2-SAT, Gaussian-elimination XOR, bounded-treewidth, padding, renaming and alternate SAT representations remain viable unrestricted-machine controls; the present **MCSP** result does not claim hardness on them.

## Exact primary-source magnification matrix and dependency map

Write n for Boolean arity, N=2^n for **explicit MCSP truth-table length**, and L for encoded SAT formula bit length. These are distinct. Original reference [1] was inspected in the publisher's PDF, with page-image verification of pages 23:3 and 23:4.

| Source theorem | Model, measure, size parameter and quantifiers | Verified hypothesis/conclusion, actual gap |
| --- | --- | --- |
| Cheraghchi-Hirahara-Myrisiotis-Yoshida, STACS 2021, **Theorem 1, p. 23:3** [1] | Ordinary exact MCSP[2^(mu1*n)], N-bit complete truth table, **deterministic one-way read-only input plus exactly one two-way work tape**, fixed small universal mu1>0 | If **not** decidable in O(N^1.01) time in this model, then P!=NP. Premise **OPEN**. The new envelope addresses only b(n)<=S, never 2^(mu1*n). |
| Same, **Theorem 2, p. 23:3** [1] | Ordinary MCSP[2^(mu2*n)], **randomized two-sided error** one-way-input one-work-tape, N bits, **distinct larger mu2>mu1** | Unconditional nonmembership in BPTIME1[N^1.99]. It does NOT furnish Theorem 1's smaller-threshold premise. |
| Same, **Theorem 3, p. 23:4** [1] | Ordinary MCSP[2^(mu*n)], every fixed 1/2<mu<1; one-way-input one-tape **randomized oracle machine**, all oracle query lengths N^o(1) | For each such mu some mu'>0 excludes time N^(1+mu'). This is a barrier to that **short-oracle-query** magnification architecture, not to all possible proofs. |
| McKay-Murray-Williams, STOC 2019 [2] | Original streaming/resource-bounded compression paper, underlying CHMY Theorem 1 corollary | No direct reduction asserted here. Bound in [1] used as the precise peer-reviewed implication. |
| Oliveira-Pich-Santhanam, CCC 2019 [3]; Chen et al., 2019/2020 [4] | Gap-MCSP/MKtP approximation/nonuniform circuit and locality-barrier settings, **not** the same ordinary one-tape problem | No variant-to-variant hardness inference or natural-proofs bypass is claimed. |

**Ordered proof routes and explicit retirements:**

1. **Strongest sufficient but OPEN:** Prove the exact CHMY Theorem 1 low-mu deterministic MCSP N^1.01 exclusion (or an exactly charged both-label input-model-preserving implication supplying it). This yields P!=NP. Currently no surviving unrestricted witness.
2. **Conditional threshold-descent route, OPEN:** Start from CHMY's large-mu Theorem 2, supply a *both-label* small-mu mapping with exact integer threshold/promise and fully charged one-way-input one-work-tape reduction. TMR-1/026's gate-spectrum counterexamples retire plain mismatched dummy padding. TMR-3/027 fusion has an **annotated** header and does not close this arrow; its full-output header retention does not constrain one-bit decisions.
3. **Confirmed algorithmic escape for bounded thresholds:** TMR-4/028's fixed-gate algorithm receives favorable independent semantic review; this new ENVELOPE29 permits arbitrary uniformly computable bounded schedules and truncated exact gate minimization. Any hypothesis saying a *mere* fixed threshold increase forces Omega(N) retained information is **FALSIFIED/RETIRED** within the fixed-envelope model. Nothing is inferred for b(n)=N^mu.
4. **Explicitly restricted:** TMR-2/027's Hamming-distance query depth requires nearly all N queries on YES cases, but an adaptive nonlinear single-work-tape computation can still be near-linear. TMR-4/027 affine rank counts describe fixed independent sketches, not all adaptive summaries. TMR-3's full-output transducer frontiers describe transport, not MCSP decision-time hardness.
5. **Other models remain separate:** SAT source length L vs explicit MCSP length N; MKTP, Gap-MCSP, partial/succinct MCSP and approximation-P-uniform magnification have additional hypotheses and no proved all-label cost-sound transfer to ordinary MCSP. Crossing-sequence equality-family and bounded-workspace lower bounds do not exclude all polynomial-time multitape SAT machines.

**Unrestricted-machine gap:** The formal objective remains for every one fixed uniform total correct deterministic multitape 3-SAT decider A, every k>=1,C>0,L0, some formula F of bit length >=L0 with T_A(F)>C(|F|+1)^k. Neither a bounded-gate MCSP upper bound nor a restricted streaming/transducer lower bound reaches that quantified conclusion. All load-bearing arrows toward P!=NP remain OPEN.

## Next target, peer request, and tracker status

**Next target:** TMR-1/TMR-2 independently audit the bounded-schedule flag-preservation and minimum-gate extraction, including the n=1 to n=2 threshold jump. TMR-3 audit the one-physical-work-tape nested-sweep costs and test whether its mobile-counter fusion can avoid the annotated-header obligation without storing the full source. TMR-4 seek a true unbounded growing-budget inherited summary at s=N^mu; TMR-5 attack this transition with fresh counterexamples, not merely flag-count arithmetic.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The exact full proof1/proof2/main.tex were reviewed and left unchanged: this is a restricted positive result requiring another agent's independent review before promotion, not a new P=NP or P!=NP arrow. No roles, tasks, schedules or root manuscripts altered.

## Primary references

[1] M. Cheraghchi, S. Hirahara, D. Myrisiotis, Y. Yoshida. *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP.* STACS 2021, Theorems 1–3, pp. 23:3–23:4. https://doi.org/10.4230/LIPIcs.STACS.2021.23

[2] D. M. McKay, C. D. Murray, R. R. Williams. *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes.* STOC 2019, pp. 1215–1225. https://doi.org/10.1145/3313276.3316396

[3] I. C. Oliveira, J. Pich, R. Santhanam. *Hardness Magnification near State-of-the-Art Lower Bounds.* CCC 2019, Theorems and variants as named in original work. https://doi.org/10.4230/LIPIcs.CCC.2019.27

[4] L. Chen, S. Hirahara, I. C. Oliveira, J. Pich, N. Rajgopal, R. Santhanam. *Beyond Natural Proofs: Hardness Magnification and Locality.* 2019 preprint, arXiv:1911.08297. https://arxiv.org/abs/1911.08297
