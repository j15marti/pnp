# RP-TRACE-FOURIER4: explicit finite-field spectral hitting sets and a sharp bounded-norm boundary

**Research date:** 2026-10-21 10:36 Asia/Seoul. **Scope:** P versus RP alone. **Status:** ESTABLISHED for the stated restricted RP subfamilies; RETIRED as a purported universal derandomization; P=RP OPEN; P!=RP OPEN; P!=NP OPEN. The original small-bias primitives are published mathematics, not new results. This project run supplies a fully explicit construction, resource ledger, a hereditary Fourier-norm proof, and an adversarial test.

## 1. Preregistered approaches

The four approaches were written to `00_PRELITERATURE_PROPOSALS.md` *before the targeted primary-literature lookup*: (1) explicit finite-field epsilon-biased trace hitting sets for polynomial-Fourier-L1 acceptance; (2) approximate conditional expectations against prior exact-prefix NP-hardness; (3) an RP self-attack against the very same public trace set; (4) a literal Fourier audit of the real six-bit COMPLETIONCUT1 SAT-answer function, including hard high-norm acceptance patterns with small state. See the original dated file for full falsifiers.

## 2. Definitions and theorem (ESTABLISHED, restricted)

Let `R(x,r)` be a deterministic polynomial-time evaluation of an RP verifier given all `m=m(|x|)<=poly(|x|)` independent fair tape bits `r` explicitly. Define `f_x(r)=R(x,r)`, so **NO** instances obey `f_x≡0` and **YES** instances obey `E_U f_x>=1/2`. The source-verifier's time bound is `T_R(n)=poly(n)` and workspace `S_R(n)=poly(n)`; source tape random access is simulated by providing the full tape to R, with all reads charged inside `T_R`.

For `S⊆[m]`, let

`chi_S(r)=(-1)^(XOR_{i∈S} r_i)`,

`hat(f_x)(S)=2^(-m) * sum_r f_x(r) chi_S(r)`, and

`||f_x||_A = sum_{S⊆[m]} |hat(f_x)(S)|`.

**THEOREM (TRACE-FOURIER4).** Fix an RP verifier R and a declared polynomial `B(n)>=1` such that for every input x, `||f_x||_A <= B(|x|)`. Then its language is in P by a deterministic, uniform, total procedure with **no advice, no SAT oracle and no unproved pseudorandomness assumption**. It evaluates R only on an explicitly enumerated polynomial-size trace set, preserving both labels exactly. It can also output an accepting random tape for each YES input, but does not need to solve conditional SAT prefix extension.

**Construction.** Let `q=2^k` be the least power of two satisfying `q>=8mB(n)` (for `m=0`, run R directly). Find an irreducible degree-k binary polynomial by deterministic exhaustive search over at most q candidates; this is polynomial in n because q is polynomial in n. Work in the resulting field `F_q`. For each pair `(a,z)∈F_q²`, set

`H_{m,q}(a,z)_i = Tr_{F_q/F_2}(a z^i)` for `i=0,...,m-1`, with `z^0=1` even if `z=0`.

The deterministic decider enumerates all q² seeds and accepts if any execution `R(x,H_{m,q}(a,z))` accepts. The enumerable set may contain repetitions; seeds, not distinct resulting tapes, are the charged resource. Uniform q and polynomial representation search are critical. The construction is a simple, explicit instance of the classical small-bias strategy of Naor--Naor and Alon--Goldreich--Hastad--Peralta, and is **not claimed as a novel result of general derandomization**.

**Proof of exact bias.** For any nonempty S, the polynomial `P_S(Z)=sum_{i∈S} Z^i` is not identically zero and has degree at most m-1<q. Its character bias equals

`E_{a,z} (-1)^{sum_{i∈S} H(a,z)_i}`
`= E_z E_a (-1)^{Tr(a P_S(z))}`
`= Pr_z[P_S(z)=0] <= (m-1)/q`.

The conditional `a` average is exactly 0 for nonzero P_S(z), since trace multiplication is a nontrivial F2-linear functional of a. This identity also shows the bias is nonnegative. Thus for any Boolean f,

`|E_H f - E_U f| <= ((m-1)/q) * sum_{S≠∅}|hat f(S)|`
`<= (m-1)/q * ||f||_A <= 1/8`.

On a YES instance `E_H f>=3/8`, so at least one seed accepts. On a NO instance all seeds reject. This yields an exact P decision procedure, not a randomized estimate. There is no error in the final deterministic output.

**Resource ledger.** `k=O(log(m B))`, `q²=O(m²B(n)²)` seeds, `2k` seed-index bits. Polynomial search for irreducibility takes `q poly(k)` bit operations using Rabin's polynomial criterion. For each seed, generate m tape bits by repeated field multiplication and trace in `m poly(k)` bit operations, then execute the original verifier with input x and random tape. Conservative deterministic total time:

`O(q poly(k) + q² [m poly(k) + T_R(n) + n])`;

peak workspace:

`O(m + S_R(n) + n + poly(k))`.

A literal single-work-tape implementation may incur further polynomial simulation overhead; no **CHMY one-work-tape bound**, sublinear-space resource point or tight exponent is asserted. No original-source pointer, oracle, entropy source, stored exponential table, nonuniform circuit advice, or hidden generator proof is assumed.

**Uniformity boundary.** The exponent of `B(n)` may be hardwired as part of a particular machine's restricted-class proof. Deriving a correct B from the code of every arbitrary RP machine is NOT established. The theorem is `RP_{poly-Fourier-L1} ⊆ P`, not `RP ⊆ P`.

## 3. HEREDITARY conditional-expectation witness theorem (ESTABLISHED under same B)

Fixing any prefix of f's coin input cannot increase its Fourier L1 norm: terms `hat f(T)` and `(-1)^b hat f(T∪{i})` merge into one coefficient and the triangle inequality proves `||f|_{r_i=b}||_A<=||f||_A`. Repetition preserves `<=B`. Hence the same trace construction uniformly approximates **every conditioned suffix's** acceptance probability with absolute error bounded by `B(ell-1)/q`.

Choose q at least `8m²B` and at each of the m bit positions evaluate both conditioned-suffix expectations over the trace distribution. Select the bit with larger approximate expectation. Let `µ(u)` be the true conditional acceptance probability of a partial prefix. If each estimated child µ differs from the true child by at most δ=`1/(8m)`, then

`µ(next selected prefix) >= µ(current prefix) - 2δ`.

Starting from `µ(empty)>=1/2`, after m steps the final acceptance bit is at least `1/2-2m/(8m)=1/4>0`. As that final bit is 0 or 1, it equals 1. NO instances accept on no tape and remain rejected by any chosen tape. Thus the restricted algorithm can **construct** a successful seed uniformly in polynomial time. The extra deterministic cost is `2m q²` original-verifier evaluations with `q=O(m²B)` and polynomial field operations. For each fixed x, R itself is run on fully supplied real tapes; there is no oracle for probability or for SAT.

**Relation to the :12 PREFIX-DENSITY3 result.** The 2026-10-21 10:12 agent showed exact strictly optimal first-coin selection can be NP-complete for an RP verifier recognizing a P-language. That theorem does **not** falsify polynomial-additive-approximation prefix selection. The counts of the two prefixes differ by just one or a few assignments out of an exponential denominator, so exact rank ordering can encode SAT while any sufficiently accurate additive approximation need not distinguish those cases. What is missing for unrestricted RP is a deterministic polynomial-time suffix-probability approximator or a bound on its total Fourier mass. No assertion that :12's unrestricted verifier has such a bound is made.

## 4. Exact high-norm RP falsifier (ESTABLISHED)

The spectral hypothesis is not automatic even for a *quadratic-time, two-state-at-pair-boundaries* RP verifier.

For `m=2h`, define `Q_m(r)=XOR_{j=0}^{h-1} (r_{2j} AND r_{2j+1})` and `f_m(r)=1` iff `Q_m(r)=0`. The language can be `L={x : XOR_i x_i=1}`, decidable in linear time, by defining `R(x,r)=parity(x) AND f_m(r)`. On NO inputs, all random tapes reject. On YES inputs,

`Pr[f_m=1]=1/2+2^(-h-1)`.

Thus it satisfies RP's one-sided error with polynomially many coins. The verifier processes pairs of bits, retaining one parity state at two-bit boundaries (width two there, and at most four states while holding the first bit of each pair), and needs O(m+n) time, O(log m) index storage or a constant controller plus the normal input scan. Each local gate is low degree and requires no crypto or external randomness.

For `g_m(r)=(-1)^Q_m(r)`, Fourier multiplicativity across h disjoint pairs implies **every** Fourier coefficient has magnitude `2^{-h}` (each 2-bit factor has four Fourier coefficients of magnitude 1/2). Since `f_m=(1+g_m)/2`, its spectral L1 norm is exactly

`||f_m||_A = 1/2 + 2^{h-1} = 1/2+2^{m/2-1}`.

This is EXPONENTIAL. Therefore the missing claim `poly-time RP ⇒ polynomial Fourier L1 norm` is **FALSIFIED**, even for a constant-width ordered streaming verifier (two states at pair boundaries, at most four when bits arrive individually). This family has F2 ANF degree two, so the preceding *low-degree* derandomizer still works. The two structural restrictions are different and neither is universal.

Conversely, OR of m coin bits has algebraic normal form degree m, yet exact Fourier L1 norm `2-2^{1-m}<2`, so TRACE-FOURIER4 covers an unbounded-degree family. This is a bona fide extension of the project's previously tested low-degree *criterion*, although the OR language has an obvious deterministic bypass.

## 5. Public-set self-attack and universal quantifier control (ESTABLISHED)

The specific `H_{m,q}` must NOT be proposed as a hitting set for every RP machine. There is a uniform polynomial-time RP verifier for the P language `odd parity(x)` that, on its YES inputs, rejects exactly those random tapes that occur in the publicly enumerable `H_{m,q}` and accepts all remaining tapes. For any sufficiently large m with `|H_{m,q}|<2^{m-1}`, YES acceptance is >1/2. Its membership test recomputes the entire q²-seed set and compares the random tape; its cost is polynomial (but does not preserve small workspace). Every H seed is rejected. On NO x it rejects every tape. The language remains trivially in P. Theorem TRACE-FOURIER4 is not contradicted because this self-attacking acceptance function necessarily has larger Fourier norm than its stated bound.

An explicit certificate is `E_U f - E_H f = Pr_U[r not in H]`; Fourier small-bias yields `||f||_A >= Pr_U[r not in H] / epsilon`. In the tested m=16,q=64 case, the set has 587 distinct tapes among 65,536, and the self-attack accepts 64,949/65,536 >1/2, while rejecting all 4,096 seed pairs. The checked spectral norm indeed obeys this required lower bound. This is a focused hostile test of the actual trace construction, not an unrelated public-hitting-set example.

The :12 investigator's stronger 10:12 diagonalization concerns an *arbitrary*, source-code-aware, total P-time **explicit-list constructor with a common declared polynomial clock**, and refutes that stronger interface using recursion-theorem self-reference. TRACE-FOURIER4 does not use that discredited universal interface: its correctness is promised only for the bounded-spectral-norm class, and its generated list does not inspect the RP verifier code.

## 6. Original WRAPPER inspection and computational results

The original `experiments/review/completion_cut_audit.py` was fetched directly from GitHub (SHA `239dc90e90cc78a9b77c1264fd79a59dc0390326`, partial first-130-line inspection), along with `experiments/wrapped_dag/wrapper_as_sat_prime_lineage_toy.py` (SHA `95abeb9447a71b4ef6cb523e58adace6da6c808f`). The original completion-controller's terminal **SAT answer**, distinct from SHA state, is the function `f(r)=1 XOR (r1 AND r2 AND r3)` on six independently sampled random bits. Exact full truth-table evaluation gives acceptance `56/64=7/8`; exact Fourier norm `||f||_A=7/4`. This verifier does **not** create a hard language: its output labels belong to a fixed toy model and deterministic bypasses exist. The trace-family enumerator hits its acceptance set as expected. The low norm is only for this concrete six-bit controller and does not transfer to arbitrary unbounded wrappers.

The original prime-lineage script uses a fixed satisfiable base `x1 AND x2`; its distinct prime/hashing histories preserve SAT. It supplies neither a hard RP language nor a universal source of polynomial spectral bounds.

**Finite program test:** `rp_trace_fourier_audit.py`, standard Python, no third-party libraries, ran to completion and produced **1,334,343 assertion-accounted checks, zero failures**. It exhaustively checked every nonempty parity subset for m=2..8, compared the Walsh bias against a completely independent finite-field polynomial-root count, checked the exact trace distribution and irreducible polynomials, verified OR and quadratic spectral identities for even m≤8, computed COMPLETIONCUT1 Fourier norm, tested the actual public trace set self-attack at m=16, and verified a 4-coin hereditary approximate-prefix greedy witness by 524,288 charged verifier evaluations. Runtime of this reference implementation was 7.808 seconds in the recorded run. Tests confirm finite code only; infinite theorems follow from the field/root/triangle proofs above.

## 7. Historical coverage and sharing state

Cumulative ledger: `COVERAGE_LEDGER_SPECTRAL4.json`, **140 individually identified source records**, of which 121 are inherited from the :12 10:12 inventory and **19** were independently indexed or inspected in this run. Inherited records are NOT represented as having been reread here. Fresh direct reads include `AGENTS.md`, `main5.tex` index (partial), original COMPLETIONCUT1 Python (partial), original prime-lineage Python (partial), recent :12 source-filled Google Docs, previous :36 handoff, 09:48 synthesis original LaTex, and research STATUS partial. Current/archival Drive Living Logs and MAIN were located but not comprehensively inspected. The returned 10:36 Drive HITSET-VERIFY3 document was empty; title metadata alone cannot certify its body. Complete October 20 RP/coRP conversations, most huge WRAPPER/AVOID archives, full original Adleman 1978 text and long Drive MAIN remain in the UNSEEN ledger. No exhaustive-corpus representation is made.

**Sharing:** If GitHub accepts complete `.tex`, `.py` and `.json` publication, report precise commit SHAs and readback matches; otherwise retain the local package and label `PENDING_SYNC`. A successful write does not prove the :12/:48 agents read it.

## 8. Status and next decisive falsifier

**ESTABLISHED:** The trace generator is `(m-1)/q`-biased, and every RP verifier with a known polynomial bound on the COMPLETE acceptance function's Fourier spectral L1 norm has a deterministic polynomial-time membership decider and a constructive accepting random tape on YES inputs. The conditional expectation construction is hereditary. This rests on known published small-bias mathematics and the elementary proofs shown here.

**FALSIFIED/RETIRED:** Polynomial-time RP verifiers do not necessarily have polynomial Fourier L1 norm. The explicit quadratic-phase constant-width verifier has norm `1/2+2^{m/2-1}` and a trivial deterministic parity-language bypass. The unrestricted use of this construction to infer P=RP is invalid.

**CONDITIONAL/OPEN:** Derandomize every ordinary RP machine by proving an all-input Fourier bound or a different source-checkable class-covering property. There is no such verified implication. Similarly no language is exhibited in RP outside deterministic P. P versus RP OPEN; P versus NP OPEN.

**Next strongest mathematical test:** Search the archived generalized completion-time controller for a uniformly bounded spectral norm theorem that survives *input length growth, arbitrary adaptive coin access, and acceptance conditioning*, rather than measuring just one toy's low norm. Explicitly try the quadratic-phase constant-width controller as a hostile input and a long XOR composition of independent stages. Any proposed spectral invariant must survive this construction and include the true source-reader/workspace cost. Otherwise abandon this restricted route rather than announcing universal equality.

## Numbered primary references

[1] Naor J, Naor M. Small-Bias Probability Spaces: Efficient Constructions and Applications. SIAM J Comput. 1993;22(4):838-856. https://doi.org/10.1137/0222053

[2] Alon N, Goldreich O, Håstad J, Peralta R. Simple Constructions of Almost k-wise Independent Random Variables. Random Structures & Algorithms. 1992;3(3):289-304. https://doi.org/10.1002/rsa.3240030308

[3] Nisan N, Wigderson A. Hardness vs Randomness. J Comput Syst Sci. 1994;49(2):149-167. https://www.math.ias.edu/~avi/PUBLICATIONS/MYPAPERS/NOAM/HARDNESS/final.pdf

[4] Impagliazzo R, Wigderson A. P = BPP if E Requires Exponential Circuits. STOC 1997:220-229. https://doi.org/10.1145/258533.258590

[5] Kabanets V, Impagliazzo R. Derandomizing Polynomial Identity Tests Means Proving Circuit Lower Bounds. Computational Complexity. 2004;13:1-46. https://www2.cs.sfu.ca/~kabanets/Research/poly.html

[6] Adleman LM. Two Theorems on Random Polynomial Time. FOCS 1978:75-83. https://doi.org/10.1109/SFCS.1978.37

[7] Valiant LG, Vazirani VV. NP Is as Easy as Detecting Unique Solutions. Theor Comput Sci. 1986;47:85-93. https://doi.org/10.1016/0304-3975(86)90135-0