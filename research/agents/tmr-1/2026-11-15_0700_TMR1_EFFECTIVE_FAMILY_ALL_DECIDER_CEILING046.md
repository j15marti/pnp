# TMR-1/046: Effective-family ceiling for all-decider SAT tariffs

**2026-11-15 07:00 PST | TMR-1 PNP Machine Model Lead | EFFECTIVEFAMILY046**

**Status:** PROVED/RESTRICTED symbolic family-recognition and tariff-ceiling theorem, independent mathematical review OPEN. Native finite controls COMPUTATIONAL. An unrestricted SAT lower bound is OPEN. P versus NP remains OPEN.

## 1. Candidate and four falsifiers

**Candidate.** A single, polynomial-time **unary-indexed**, polynomially **correctly labeled**, sufficiently length-honest growing collection of source formulas cannot support a superpolynomial lower-bound potential that is cost-sound simultaneously for **every** fixed total correct deterministic SAT decider on those formulas. A single fixed decider can recognize this family, answer its known labels, and run a complete but potentially exponential solver outside it. Apply this ceiling to BOTH the original UNSAT family and the one-final-sign-bit SAT mutants from TMR-1/045.

Four precise falsifiers/checks: (F1) the supplied generator requires superpolynomial time in its unary index or its index exceeds encoded source length, invalidating the search bound; (F2) a purported label is wrong or two colliding indexed outputs carry inconsistent labels; (F3) the specialized machine is not truly total and correct on **all** proper 3-CNF inputs, including off-family ones; (F4) a proposed universal superpolynomial initial potential is defeated by an actual legal run of the correct specialized decider. Here F1-F3 are discharged by the explicit construction and exhaustive-search fallback. F4 is an **authentic legal shortcut**, not a spurious CEGAR path.

## 2. Recovery, prior art, and nonduplication

Read FIRST governing fusion-Lipschitz directive at `research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md`, SHA `54c9177fc211dfca6c94d89d6ebbf3f3908809d6`. Then read the 2026-11-13 TMR replacement, root `proof1.txt` (28,714 characters, SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`), authentic complete Git blobs `proof2.txt` (1,051,196 characters, SHA `930c5eeddafce656717f28055a7a9a755f44737c`) and `main.tex` (2,545,859 characters, SHA `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34`), issue #3 with current issue and recent comments, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, and all five current TMR handoffs. The ordinary GitHub contents endpoint yields empty strings for the two oversized root blobs; fetching by **Git blob SHA** recovered their actual complete content. No shared edit was made.

Direct prior artifacts: `research/agents/tmr-1/2026-11-15_0606_TMR1_PHYSICAL_LASTBIT_TSEITIN_TARIFF045.md` and `experiments/tmr/tmr1_lastbit_tseitin045.py` define the exact source, last-bit opposite labels, and local-head frontier. LSPV-4/499 already proves **all** original polarity positions SAT-critical; LSPV-4/506 already explains source-bit trace necessity and indexed retrieval. This report does **not** rebrand either polarity sensitivity or ordinary polynomial family recognition as new. The added deliverable is the general **one-family, every-decider tariff impossibility with exact quantifier and hypothesis ledger**, a concrete full correct decider, and its application to the shared machine/proof-transfer dependency map.

Primary contextual paper: J. Maly and M. Müller, *A remark on pseudo proof systems and hard instances of the satisfiability problem*, Mathematical Logic Quarterly 64 (2018), pp. 418-428, DOI https://doi.org/10.1002/malq.201700009. The discussion of hard sequences explicitly distinguishes solver-dependent and universal hard sequences. The result proved here is self-contained and must not be confused with any unproved hard-sequence hypothesis or an implication from the paper.

## 3. General indexed-family theorem

Let `L` be any decidable language with a fixed total correct deterministic decider `E` (possibly exponential). Fix a **finite** variant set `B`. Suppose one fixed deterministic transducer `g`, on input `(1^j,b)`, prints a binary word `x_{j,b}` in time at most `p(j)` for a fixed polynomial `p`, and another fixed polynomial-time algorithm computes the **correct** label `h(j,b)=1_{x_{j,b}\in L}`. Assume the length-honesty condition

$$
|x_{j,b}|\ge j\qquad(j\ge j_0,\ b\in B).
$$

There is **one fixed total correct deterministic decider** `D` for `L` and constants `C,q` such that

$$
\boxed{
\forall j\ge j_0\ \forall b\in B:\quad
T_D(x_{j,b})\le C(|x_{j,b}|+1)^q.
}
$$

**Proof.** For an arbitrary input `x` of length `N`, `D` enumerates `j_0\le j\le N` and the finitely many `b\in B`, generates each `x_{j,b}` and its label, and compares the complete generated word with `x`. On equality it outputs the certified correct label. When no equality occurs, it runs `E(x)`. Every branch halts; every output is correct. Each of the at most `|B|N` generator and comparison tasks runs in polynomial time in `N`, including the literal generation, tape writes, original input rereads, comparisons and indices, because `j\le N`. Thus the recognition portion has polynomial time on an ordinary fixed finite multitape Turing machine with only locally moving heads. On a family word `x_{j,b}`, length honesty ensures `j\le |x_{j,b}|`, so a match is found before the expensive `E` fallback. The machine `D` is fixed, not selected separately at each length. QED.

This is a **sufficient ceiling**, not an equivalence: dropping fast labels or unary-index polynomial printability does not establish a lower bound. No random oracle, advice by length, omitted input scan, or unknown-purpose free step is used.

**Corollary 046.1 (all-decider tariff ceiling).** Suppose a scalar potential `Phi_A` is valid for every authentic transition of every fixed correct total decider `A` in the SAME physical model, and `Phi_A(goal)\le0` for each correct completed goal. For the above `D`, telescoping yields

$$
\boxed{
\Phi_D(C_0(x_{j,b}))\le T_D(x_{j,b})
\le C(|x_{j,b}|+1)^q.
}
$$

Therefore no alleged universal superpolynomial initial lower bound on that **same** family for **all** correct machines can be sound. In particular, it cannot satisfy `forall k forall j0 exists j>=j0 Phi_D(C0(x_j)) > |x_j|^k`. Take `k>q` and large `j`. This proves an actual barrier to that restricted research target. It does not rule out **algorithm-dependent** hard inputs and proves neither P=NP nor P!=NP.

## 4. Exact original sources, measure, and concrete specialization

For every `m>=2` use the TMR-1/045 circular ladder `G_m=C_{2m} square K_2`: `H=4m` cubic vertices, `E=6m` original Boolean edge variables, and `16m` proper width-three clauses. The fixed eight-bit magic, unbounded Elias-gamma counts, and one fixed-width original literal ID followed by one literal-polarity bit give

$$
N_m = 8+\ell_\gamma(6m)+\ell_\gamma(16m)
+48m(\lceil\log_2(6m+1)\rceil+1)
=\Theta(m\log m).
$$

The original `F_m^0` has one odd charge and is UNSAT, since summing all vertex equations produces `0=1`. The `F_m^1` variant flips **only the very final original polarity bit**, remains a valid same-length proper 3-CNF, and is SAT by the vertex-deleted spanning-tree assignment established in TMR-1/045. All source operations are literal, authenticated bit manipulations, never a compressed alternate representation passed off as the original input.

Choose `g(1^m,b)=F_m^b` for `b=0,1`, `h(m,b)=b`. The generator is polynomial time in `m`; `N_m>=m`; both labels have complete elementary proofs. The single `D` compares these sources and uses exhaustive original-3CNF assignment search on nonmatches. It is total and correct on the entire declared proper-3CNF grammar. On these two indexed variants its runtime is polynomial in the **actual original input length**.

This directly falsifies any claimed bound `T_A(F_m^b)>N_m^k` for every correct fixed `A` and arbitrarily large `k` on the unmodified canonical sequence. It does **not** falsify the last-bit physical lower `T_A(F_m^b)>=N_m`, nor a lower bound on ordinary Resolution, nor a different family selected **after** a program is fixed.

## 5. Qualification: complete physical state, terminal predicate and seven-column tariff

A concrete configuration includes `(F,A,G,P,Gamma,D,I,O)` plus the exact machine's finite control, all read-only and writable tape contents, each head position, runtime history, and output status. `F` is immutable and may appear as a mathematical **parameter**, not as a free read oracle for the transition function. The machine has one originally left-positioned read-only original bit head moving at most one cell per genuine cost-one transition; arbitrary work tapes, preprocessing, learning, storage, rereads, caching, recomputation, and simultaneous actions permitted by the fixed finite transition table are included. Each authentic transition costs **one** regardless of how many simultaneous legal tape writes it performs. All natural machine zero-cost SCCs are singleton. An optional zero-cost analytic metadata VIEW must be source-blind and cannot alter the original read frontier.

The completed-goal predicate for an eligible machine requires actual finite HALT with the correct SAT label on the entire encoded 3-CNF domain; malformed inputs are deterministically rejected. For any correct `A`, `F_m^0` and `F_m^1` must induce distinguishable completed traces, so the final sign bit must have been genuinely read on BOTH. This is the TMR-1/045 source-frontier lemma.

For an actual input `F`, let `r` be the maximum original source position authentically **read**, initially `-1`. Define the restricted but globally valid potential component

$$
p_{\rm int}(C)=
\begin{cases}
\max(0,|F|-1-r(C)), &F\in\{F_m^b:m\ge2,b\in\{0,1\}\},\\
0,&\text{all other inputs}.
\end{cases}
$$

All six other obstruction coordinates are zero. The seven-vector is `(p_CNF,p_XOR,p_sep,p_fus,p_Gamma,p_int,p_machine)`. For an authentic physical step, exactly one of the following signed discharge rows applies:

| Complete authentic transition class | Cost | `(CNF,XOR,SEP,FUS,Gamma,INT,MACHINE)` discharge |
| --- | ---: | --- |
| First read of next original frontier bit, **including** simultaneous work/write/HALT | 1 | `(0,0,0,0,0,1,0)` |
| Any other physical transition: local reverse, reread, write, storage, algebra, lookup, recompute, HALT | 1 | `(0,0,0,0,0,0,0)` |
| Optional source-blind, reversible analytic VIEW | 0 | `(0,0,0,0,0,0,0)` |

A forward scan can expose at most one new frontier cell per real step. No second charge is levied for the same simultaneous paid identity. Thus the exact active nonnegative cone is `0<=lambda_INT<=1` and the rational certificate

$$
\lambda=(0,0,0,0,0,1,0),\qquad
\Phi_A(C_{0,m}^b)=N_m,\quad
\Phi_A(goal)=0
$$

is valid for every **correct** physical decider on these two sequences, and zero on other sources. A terminal that reads the last bit and HALTs simultaneously is captured by the **same one paid row**, not counted as an additional terminal step. The corresponding finite machine-readable seven-column matrix is separately published. This certificate is only **linear** and fully compatible with the fixed decider `D` above.

An arbitrary free oracle for `F`, a word-at-a-time indexed port, or an uncharged source semantic projection changes the concrete model and invalidates the above physical frontier tariff. Such operations remain genuine hostile controls, not CEGAR-deleted paths.

## 6. Evidence, replay and status

Native local **CPython standard-library** replay completed `m=2..40`: 78 canonical source members, lengths `N_2=506` through `N_40=17322`, 359 explicit instrumented assertion checks, **zero failures**. The code regenerates both variants, checks unique one-bit mutation, parses every proper original source, verifies polynomial family matching and both known labels, exercises the actual total `decide` function, verifies length monotonicity, and tests both a nonfamily SAT source and a nonfamily UNSAT source through exhaustive fallback plus four malformed controls. No randomized inputs; no seed; one bounded 39-index invocation. Finite outcomes are **COMPUTATIONAL** and do not prove polynomial Turing time independently of the symbolic transducer argument.

- Report: `research/agents/tmr-1/2026-11-15_0700_TMR1_EFFECTIVE_FAMILY_ALL_DECIDER_CEILING046.md`.
- Executed source: `experiments/tmr/tmr1_effective_family046.py`.
- Raw regression: `results/raw/tmr/2026-11-15_0700_TMR1_EFFECTIVEFAMILY046_PY_RAW.json`.
- Machine-readable tariff: `results/raw/tmr/2026-11-15_0700_TMR1_EFFECTIVEFAMILY046_TARIFF_MATRIX.json`.
- Compact role handoff: `research/agents/tmr-1/handoff.md`.

No source-code SHA is asserted until separately read back from `main` after merge.

## 7. Dependency and weakest next lemma

| Dependency | Exact status | Consequence |
| --- | --- | --- |
| TMR-1/045 original odd-charge and final-bit SAT mutant | PROVED/RESTRICTED; independent review OPEN | Opposite-label pair and honest source length |
| This run: unary-indexed correctly labeled family recognizer | PROVED/RESTRICTED; independent review OPEN | One fixed complete SAT decider runs polynomial time on **both** sequences |
| This run: universal-machine superpolynomial potential on that fixed public family | **FALSIFIED** under the theorem's indexing/label hypotheses | Any sound tariff must respect the actual recognizer trace |
| All-correct-machine linear last-bit tariff | PROVED/RESTRICTED | `Phi_0=N_m`, no more |
| TMR-2 multiscale interface ranks | RESTRICTED, easy polynomial shared circuit witnesses | Rank sizes do not become time costs for free |
| Proof-to-machine same-qualified-system simulation | **OPEN** | Proof-system hardness cannot be imported into machine time |
| Algorithm-dependent superpolynomial SAT obstruction | **OPEN** | Needs genuinely new non-recognizable, all-program hardness |
| P versus NP | **OPEN** | No unconditional resolution |

**TMR-2 weakest target:** formulate a nontrivial obstruction with the **correct program-dependent quantifiers**, and reject any static all-program superpoly claim for a polynomially labeled unary-indexed family. **TMR-3:** explicitly charge the recognizing `D` path, including generator arithmetic, all original input comparisons, work storage, and fallback not taken, under the local-head model. **TMR-4:** add a sound shortcut-calibration row: whenever one fixed total correct `D` has polynomial on-family execution, no family-universal tariff may exceed its actual steps; retain the real cheap path during CEGAR. **TMR-5:** independently challenge length honesty, source labeling, complete off-family correctness, and the source-port/zero-VIEW boundary.

Historical `/341`: **FAIL** as logical UNSAT authority on its full accepted language. Historical `/386`: **RESTRICTED** to tested guarded odd-charge fragment. Neither was changed or used as an unrestricted checker.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root `proof1.txt`, `proof2.txt`, and canonical `main.tex` were completely inspected and left untouched. Existing five TMR roles and all Pacific hourly schedules were left unchanged. **P versus NP remains OPEN.**

END_OF_TMR1_REPORT::046::EFFECTIVEFAMILY046::2026-11-15_0700_PST
