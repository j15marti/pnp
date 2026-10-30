# AFFINE-SMALLBIAS-DESCENT-GATE2

Run started: 2026-10-30 09:19 America/Los_Angeles. Requested continuation of the MCSP/MKTP threshold-descent investigation.

**Status:** PROVED/EXACT restricted mathematical implication, with the proof below and independent red-team review PENDING. Executed finite tests are COMPUTATIONAL. P versus NP remains OPEN. No arbitrary-SAT runtime lower bound, standard-model SAT-to-ordinary-MKTP reduction, or ARC contractor is claimed.

## 1. Result and change from the preceding report

The preceding MULTIPORT-PAIRWISE-BUDGET-GATE1 report left a critical masking-depth band and a possible near-threshold baseline escape. A source-distribution argument eliminates both for the stated modified-source construction. It also yields a broader theorem:

For fixed 0 < nu < mu < 1, no input-independent randomized affine transformation of a complete N-bit truth table can preserve both labels from source MCSP[N^mu] to target MCSP[N^nu], with polynomially bounded target truth-table length and worst-case error bounded away from 1/2.

Here N^nu is the **absolute target circuit threshold measured relative to source length**, not necessarily a power of target length. At equal lengths, nu is the earlier beta. With M=N^(a+o(1)) and target threshold M^beta, the obstruction applies when a beta < mu. This distinction prevents falsely ruling out ordinary ignored-variable padding, which keeps the absolute circuit threshold unchanged.

The theorem concerns transformations affine in the N source truth-table **bits**. It does not assert that arbitrary SAT algorithms, nonlinear reductions, or source-dependent encoders are affine.

## 2. Proposed tests and recovered clues

Four mechanisms were examined in order:

1. Repeat a small source truth table across ignored variables to increase the number of exposed source degrees of freedom. This suggested a stronger YES-side attack than a sparse-support family.
2. Replace that block argument by the earlier LOW-SIZE-HALFDISTANCE9 construction: small-circuit, k-wise independent source functions. This gives a simpler exact mask-fooling lemma and eliminates every masking depth without any concentration hypothesis.
3. Use the actual CHMY local small-bias primitive, Theorem 33, to replace diagonal masks by arbitrary affine linear maps. The relevant comparison is the image of an easy source distribution versus the image of a uniform source, NOT a longer uniform target.
4. Break possible overgeneralizations using nonlinear source-dependent membership, pairwise-only source independence, reused mask layers, rank-zero maps, and length-expanding padding with unchanged numeric threshold.

The useful earlier clue was therefore constructive pseudorandomness of **easy source truth tables**, not a lower bound on the baseline H_z. The new proof does not need the repeated-block occupancy argument, so no experimental or theorem claim is made for that abandoned intermediate calculation.

## 3. Exact model and quantifiers

Fix a finite complete fan-in-two Boolean circuit basis with free input wires and constants. Changing the basis changes only absolute constants. Let N=2^n. Let M=M(N)=2^m be at most N^a for a fixed a>0. Put

- s_N = floor(N^mu), the source circuit threshold;
- u_N <= N^nu, the target circuit threshold, with fixed 0<nu<mu<1;
- Y_{L,v} = the length-L truth tables having circuit complexity at most v.

For each N, let Z be an arbitrary distribution independent of the source x. After Z=z is fixed, let

    R_z(x) = A_z x XOR b_z,

where A_z is an M-by-N binary matrix and b_z is an M-bit vector. Matrix, offset, seed length, and preparation time may be arbitrary. They may be nonuniform in N. The only structural restriction is that they do not depend on x.

A proposed label-preserving randomized many-one transformation requires

    x in Y_{N,s_N}       => Pr_Z[R_Z(x) in Y_{M,u_N}] >= 1-e_N,
    x not in Y_{N,s_N}   => Pr_Z[R_Z(x) in Y_{M,u_N}] <= e_N.

The theorem proves e_N >= 1/2-o(1), so in particular e_N<=1/3 is impossible eventually. The source counterexample is fixed before Z is sampled. No source-after-seed quantifier swap occurs.

## 4. Lemma A: bounded independence fools masked small-set membership

Let D be an exact k-wise independent distribution on N bits. Fix a bit mask q and offset h, both independent of x, and a set C of at most B output strings. Then

    |Pr_{x~D}[h XOR (q AND x) in C]
       - Pr_{x~U_N}[h XOR (q AND x) in C]| <= B*2^(-k).

If the mask has at most k active coordinates, the two entire output distributions are identical.

**Proof.** With r<=k active coordinates, exact k-wise independence makes their distribution fully uniform, proving equality. With r>k, select any k active coordinates. For each fixed candidate output y, membership in the event that the full output equals y fixes those k input bits, so its probability under D is at most 2^(-k). The same bound holds under U_N. Each acceptance probability is therefore between zero and B*2^(-k), and their absolute difference is at most B*2^(-k). Average the bound over any source-independent randomness in (h,q). QED.

**Easy source distribution.** For any fixed rho with nu<rho<mu, choose k=ceil(N^rho). Over GF(2^n), choose a random polynomial of degree below k and output one fixed nonzero F_2-linear functional of its evaluation at each field point. Vandermonde invertibility gives exact k-wise independence. Hardwiring the coefficients and evaluating by Horner's rule with schoolbook field arithmetic uses O(k n^2)=N^(rho+o(1)) gates. Thus every support truth table belongs to source YES for sufficiently large N. This is the same elementary source construction underlying LOW-SIZE-HALFDISTANCE9; CHMY Theorem 31 provides a sharper locality bound [1, project P2].

This alone handles the proposed same-length CHMY additive-insertion maps, with no assumption on the distribution of their masks or baseline.

## 5. Lemma B: small bias fools affine preimages of a small set

Define character bias explicitly: D on N bits is epsilon-biased when

    |E_{x~D} (-1)^(v dot x)| <= epsilon

for every nonzero binary vector v. Let A be any M-by-N binary matrix, b any offset, and C any set of at most B M-bit strings. Then

    |Pr_D[Ax XOR b in C] - Pr_{U_N}[Ax XOR b in C]| <= B epsilon.       (1)

This holds for singular, rectangular, and full-rank matrices and for arbitrary source-independent mixtures (A_Z,b_Z,C_Z) with |C_Z|<=B.

**Proof.** Fix y. If Ax=y XOR b is inconsistent, both point probabilities are zero. Otherwise choose r=rank(A) independent equations Lx=c defining the same fiber. Their indicator is

    1[Lx=c] = 2^(-r) sum_{v in F_2^r} (-1)^(v dot c) (-1)^((L^T v) dot x).

The v=0 term is the same under D and U_N. Since L has independent rows, L^T v is nonzero whenever v is nonzero. Every remaining character expectation has absolute value at most epsilon. The point-probability difference is therefore at most (1-2^(-r)) epsilon <= epsilon. Summing over at most B accepted output points proves (1). The r=0 case is exact equality. Conditioning on and then averaging over Z proves the randomized version. QED.

**Important comparison.** The reference distribution is R_Z(U_N), not U_M. No surjectivity, target uniformity, or affine-dimension expansion is assumed.

## 6. Actual CHMY source construction, not a black-box surrogate

CHMY Theorem 33 and its proof give a local epsilon-biased distribution whose every N-bit output has an ordinary circuit of size

    O-tilde(log(N/epsilon))*log N.                                  (2)

Their explicit primitive uses a,b uniform in GF(2^d), with output coordinate j=1,...,N equal to the binary inner product of a^j and b. For a nonempty parity of coordinates, averaging over b gives zero unless the nonzero polynomial sum_{j in S} a^j vanishes. It has degree at most N, hence at most N roots when 2^d>N. Therefore the character bias is at most N/2^d. This direct derivation avoids any convention-dependent factor of two in the term 'bias'. The published near-linear field-multiplication circuit bound yields (2) after hardwiring a^(2^i), exactly as in Theorem 33 [1].

Choose rho strictly between nu and mu and epsilon_N=2^(-ceil(N^rho)). Then every output has circuit size N^(rho+o(1))<N^mu. Thus D_N is supported entirely on source YES while retaining the exponentially small bias required by Lemma B.

This construction is used as an adversarial **source ensemble**. It is not inserted as a free oracle or as a purported efficient SAT-to-MKTP constructor. Efficient acquisition of an adversarial example is not needed to refute an all-input semantic guarantee.

## 7. Theorem: affine threshold descent fails

Let B_N=|Y_{M,u_N}| and eta_N=|Y_{N,s_N}|/2^N. Circuit-description counting yields

    log_2 B_N = O(u_N log(m+u_N+2)) = N^(nu+o(1)),
    eta_N <= 2^(O(N^mu log N)-N) = o(1).

For the source distribution D_N above, Lemma B gives acceptance probabilities p_D,p_U satisfying

    |p_D-p_U| <= B_N epsilon_N = o(1).                              (3)

If worst-case error is at most e_N, completeness on every support point of D_N gives p_D>=1-e_N. Uniform input is source NO except on a fraction eta_N, so soundness gives

    p_U <= e_N+(1-e_N)eta_N.

Combining these with (3) gives the quantitative bound

    e_N >= (1-eta_N-B_N epsilon_N)/(2-eta_N) = 1/2-o(1).             (4)

This proves the theorem. The argument also excludes the reversed polarity by reversing the acceptance inequalities. No time lower bound for an unrestricted machine follows. QED.

## 8. Application to the critical band

For additive insertions of the same source at ports J, subtracting the original and modified recurrences gives, for every full seed,

    Phi_z(f) = H_z XOR (Q_J(z) AND f),
    Q_J(z) = XOR_{j in J} AND_{i>j} T_i(z).

This is an affine map with A_z=diag(Q_J(z)). Hence Lemma A or the broader theorem applies at every masking depth. It covers the previously open t=(mu-beta)log_2 N+o(log N) band, as well as baseline circuit-size saturation. The proof does not require independent layers, almost-two-wise mask marginals, a bound on CC(H_z), or fixed ports across random seeds. Ports may depend on source-independent randomness; once the seed is fixed, the map must still be affine in f.

**Precisely retired:** same-length, source-independent additive source injection, and more generally affine truth-table preprocessing, as an all-input bounded-error reduction from threshold N^mu to N^beta with beta<mu.

**Not retired:** the original CHMY generator and lower bound, genuinely nonlinear source transformations, source-dependent selection, nonlinear semantic quotients, general SAT-to-MKTP reductions, or the separate ARC contractor target. Source-dependent matrices are not exempt when the resulting map is still affine; it is the final function of x that matters.

The former Theorem 38 width concern remains a correct caution about using an upper bound as a lower bound, but it is no longer load-bearing for this negative result. We changed the proof method rather than resolving the baseline's unknown minimum circuit complexity.

## 9. Executed finite audit and hostile controls

File: `affine_smallbias_gate_audit.py`. Executed in this run, Python standard library. Deterministic exhaustive components plus 2,000 seeded multiport examples, seed 202610300919. Exact raw output is `affine_smallbias_gate_raw.json`.

- Actual power/inner-product primitive: all 256, 1,024 and 4,096 seed pairs in GF(16), GF(32), GF(64), giving 4-, 8-, and 16-bit outputs.
- 65,805 nonzero Fourier-character checks; 274 independent polynomial-root identities; 109 nonzero field-element inverse checks.
- All 4,096 binary 3-by-4 matrices and all eight offsets, giving 32,768 affine maps and 262,144 exact singleton inequalities.
- All 256 accepting subsets of the 3-bit output universe for each linear matrix: 1,048,576 exact set-probability inequalities. Offset translation was separately checked 32,768 times. We do not count unexecuted set/offset Cartesian products as experiments.
- 4,096 exact bounded-independence mask checks.
- 512,000 direct multiport recurrence checks, covering every 8-bit source for each of 2,000 seeded full recurrences. Direct recurrence and suffix-product formula are independently implemented.
- Zero failed assertions. Runtime recorded in the raw file, approximately 0.84 seconds in this environment; not a model-matched complexity bound.

A nonlinear indicator of membership in the 16-bit primitive's 586-element image has distinguishing advantage 32475/32768, despite maximum character bias 1/4. This is an intentional counterexample to extending Lemma B to nonlinear maps. Pairwise-independent even-parity sources also fail to fool an unrestricted parity query, showing why pairwise independence alone cannot replace small bias. Reused layers can cancel the effective mask, but such cancellation does not evade the new semantic theorem. Sixteen exhaustive same-threshold padding checks confirm that unchanged absolute threshold is outside the strict-shrink hypothesis.

Code SHA256: `a3cf902f1dd06c14af887b3a0753f26e5e0ce7ba32471262f07862055a01c007`.

Finite tests validate the probability identities. They do not measure minimum general circuit size for large inputs, prove the asymptotic claim without the argument above, or validate the original PRG's entire security theorem.

## 10. Corpus and duplication audit

Fresh original sources read: MULTIPORT-PAIRWISE-BUDGET-GATE1 (2026-10-30 08:41); LOW-SIZE-HALFDISTANCE9 / MAGRED-DISTANCE-OVERLAP9 (2026-10-18); AFFINE-DUAL-STREAM-OBSTRUCTION35 (2026-10-21); current AGENTS.md and CODEX.md prefixes; repository research skill. Targeted searches covered repeated-table masking, affine/small-bias threshold transport, and prior critical-window arguments. This was a targeted review, not a byte-for-byte audit of the entire repository.

Adopted: small-circuit k-wise source ensemble; source/seed quantifier discipline; actual CHMY local small-bias generator; ordinary circuit counting. The old dual-stream result concerned expansion M>N+d and a nonuniform parity tester. The present statement needs no dimension expansion and compares target-label probabilities rather than claiming a target uniformity test. The bounded-independence lemma applies directly to the masking candidate; the affine result broadens it with an additional primary-source ingredient. No claim of literature-wide novelty is made for the elementary Fourier argument.

What changed: the previous report's critical-band escape is eliminated for the declared affine-source preprocessing family. Its moment and budget lemmas remain valid but are no longer the limiting diagnostic for this family. Independent review is pending before synthesis promotion.

Root `main.tex`, ownership regions, automation prompts, schedules, and team activation were not modified. Current AGENTS.md contains later global allocation notes; this user-requested scoped continuation does not overwrite those notes or claim that the global scheduler was changed.

## 11. Model, barrier, and resource boundaries

The impossibility is semantic for a restricted family, even granting unlimited computation to choose its source-independent matrices and offsets. Thus there is no hidden one-tape speedup to charge in this negative result. A surviving constructive reduction must still charge source reads, output length, seed preparation, tape motion, replay, retained states, error and both labels. A high matrix rank or a large image is not an arbitrary runtime lower bound.

The Fourier argument is algebraic and relativizing at its probability level. It establishes no nonrelativizing P-versus-NP separation and no constructive large property yielding a general circuit lower bound. COMPACT-HISTORY20's single compact time-indexed witness remains OPEN; explicit affine fast-forward is still a valid hostile control.

MMW Theorem 4.2 supplies its ordinary-MKTP streamer after a valid target exists [2]. OPS's exact Gap-MCSP promise and nonuniform model remain distinct [3]. Ilango's proof-of-work reduction remains random-oracle-relative, with unrelativized hash instantiation only a candidate [4]. None supplies the missing standard-model deterministic SAT-to-ordinary-MKTP R_k here.

## 12. Single next constructive test

For a proposed nonlinear or input-adaptive replacement, write its exact output-bit predicate R_z(f)[i] and first test its target-YES probabilities on the explicit easy distributions D_N and on U_N. It must create a constant acceptance gap while preserving all source YES inputs, not merely distinguish the generator's image. An example separating D_N from U_N alone is not a valid MCSP reduction. Then account for the complete one-way-input/one-work-tape implementation and target threshold.

This is a test obligation for a new construction, not an assertion that such a construction exists or that it has been scheduled.

## References

[1] Cheraghchi, Hirahara, Myrisiotis, Yoshida. One-Tape Turing Machine and Branching Program Lower Bounds for MCSP. ECCC TR20-103 revision 1, Theorems 31 and 33, Lemma 32, Definition 36, Theorems 37-38, Corollary 39. Primary PDF, inspected including screenshots of printed pp. 16-17: https://eccc.weizmann.ac.il/report/2020/103/revision/1/download/ . STACS 2021 DOI: 10.4230/LIPIcs.STACS.2021.23.

[2] McKay, Murray, Williams. Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes. STOC 2019, Theorem 4.2, printed p. 8: https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf .

[3] Oliveira, Pich, Santhanam. Hardness Magnification Near State-of-the-Art Lower Bounds. Theory of Computing 17(11), 2021: https://www.theoryofcomputing.org/articles/v017a011/ .

[4] Ilango. SAT Reduces to the Minimum Circuit Size Problem with a Random Oracle. ECCC TR23-165 revision 1 (2025); SIAM Journal on Computing 55(3), 2026, DOI 10.1137/24M1652568: https://eccc.weizmann.ac.il/report/2023/165/ .

[P1] `research/agents/threshold-descent/2026-10-30_0841_ROUTE1_MULTIPORT_PAIRWISE_BUDGET_GATE1.md`.
[P2] `research/agents/magnification-redteam/2026-10-18_1909_MAGRED_DISTANCE_OVERLAP9.md`.
[P3] `research/main/2026-10-21_0748_MAIN_AFFINE_DUAL_STREAM_OBSTRUCTION35.tex`.

END_OF_VERIFIED_REPORT::ROUTE1::AFFINE_SMALLBIAS_DESCENT_GATE2::P_VS_NP_OPEN
