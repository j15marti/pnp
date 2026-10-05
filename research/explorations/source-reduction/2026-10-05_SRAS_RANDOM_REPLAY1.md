# SRAS-RANDOM-REPLAY1 — Freshness, Replay Closure, and Universal Response Evaluators

**Date:** 2026-10-05  
**Repository:** `j15marti/pnp`  
**Global status:** **OPEN. P versus NP remains open.**

This note integrates the earlier random-bitstream / CRS-PPC / HEC / authenticated-replay work into the Source-Reduction Accounting System (SRAS).

Canonical predecessors:
- `research/explorations/random-challenge/2026-10-01_CRS-PPC-SAT1.md`
- `research/explorations/random-challenge/2026-10-01_CRS-PPC_BEST-THEOREMS.md`
- `research/explorations/random-challenge/2026-10-02_1008_LSPV5_ACR1.tex`
- `research/explorations/random-challenge/2026-10-02_1018_LSPV5_SBACR1.tex`
- `research/explorations/random-challenge/2026-10-02_1031_LSPV5_EVACR1.tex`
- `research/explorations/random-challenge/2026-10-01_VSC-HEC_SHIFT1.md`
- `research/agents/lspv-4/2026-10-01_1149_LSPV-4_REREAD1.tex`
- `research/agents/lspv-4/2026-10-01_1446_LSPV-4_RANDCLOSE1.tex`
- `research/agents/lspv-4/2026-10-02_0449_LSPV-4_TRACECLOSE1.tex`

---

## 1. Exact surviving facts from the random-stream program

### CRS-FRESH1 — Fresh Snapshot Lemma

**Status: PROVED/EXACT.**

Let

\[
G=(R_1,R_2,\ldots)
\]

be an IID fair-bit source with natural filtration \(\mathcal F_t\). If \(\tau\) is an \(\mathcal F_t\)-stopping time and future bits have not been exposed, then for every \(b\ge1\),

\[
\boxed{
(R_{\tau+1},\ldots,R_{\tau+b})
\mid \mathcal F_\tau
\sim U(\{0,1\}^b).
}
\]

Thus the next challenge block is genuinely fresh relative to the entire causal past.

---

### CRS-TIME1 — Timing-Sensitivity Lemma

**Status: PROVED/EXACT under the declared blind-source/common-prefix hypotheses.**

Suppose two deterministic solvers have the same causal prefix but different charged completion times before the next \(b\)-bit capture. Then the next captured windows begin at distinct offsets. For IID bits,

\[
\boxed{
\Pr[B^{A}_{i+1}=B^{A'}_{i+1}]
=
2^{-b},
}
\]

including overlapping windows at distinct offsets. Equality forces periodicity of the corresponding IID block.

Hence

\[
\boxed{
\Pr[B^{A}_{i+1}\ne B^{A'}_{i+1}]
=
1-2^{-b}.
}
\]

This proves that runtime differences normally induce different future random transcripts.

---

### CRS-TRANSCRIPT1 — Transcript determinacy

**Status: PROVED/EXACT.**

For fixed deterministic solver \(A\), controller \(C\), input \(x\), and source realization \(G\), the causal transcript is uniquely determined.

Therefore the random-stream construction supplies a rigorous SAME_REALIZATION / provenance object.

---

## 2. Why the exact facts do not yet imply SAT hardness

### Solver-relative transcript obstruction

The timing-sensitive transcript depends on the chosen solver:

\[
(x,G)\mapsto \mathcal T_A(x,G).
\]

Therefore exact timed transcript reproduction is not automatically a solver-independent language property.

The three obvious repairs have known problems:

1. **solver-relative game:** a faster solver is judged on its own different transcript;
2. **reference-solver transcript:** the problem becomes simulation of the reference solver;
3. **external schedule:** the problem becomes a genuinely online/interactive task.

Thus

\[
\boxed{
\text{timing-sensitive provenance}
\not\Rightarrow
\text{static SAT lower bound}.
}
\]

---

### Constant-rate entropy ceiling

If the external source emits \(O(1)\) fresh bits per charged machine step, then elapsed time \(T\) exposes only \(O(T)\) fresh entropy.

Hence true randomness cannot generate a superlinear time lower bound merely by information counting.

Injecting \(K\) truly independent random bits requires accounting for those \(K\) bits. Encoding exponentially many fresh bits literally changes the actual input/resource scale; replacing them by a short seed introduces a computational-hardness assumption.

---

### RANDCLOSE1

**Status: PROVED/EXACT closure under the counterfactual.**

A uniform bounded-error polynomial-depth static computation using polynomial deterministic work, polynomially many adaptive NP queries, and polynomially many fresh random bits lies in

\[
\mathrm{BPP}^{NP}.
\]

Under \(P=NP\),

\[
\mathrm{BPP}^{NP}
=
\mathrm{BPP}
\subseteq
\Sigma_2^P\cap\Pi_2^P
=
P.
\]

Therefore

\[
\boxed{
P=NP
\Longrightarrow
\mathrm{BPP}^{NP}=P
}
\]

for the declared polynomial computation.

Fresh randomness plus polynomial causal depth is therefore **FALSIFIED/RETIRED** as a standalone static-SAT hardness mechanism.

---

# 3. Replay results

## ACR-REALIZED1 — Realized-path replay closure

**Status: PROVED/EXACT.**

If a realized authenticated replay transcript has polynomial length and its validity relation is polynomially balanced and lies in fixed PH, then under \(P=NP\) a valid transcript is selectable in FP by PH-PROV-CLOSE1.

If the replay transcript is a deterministic polynomial execution trace plus a polynomial authenticator, TRACECLOSE1 applies directly.

Therefore

\[
\boxed{
\text{polynomial replay}
+
\text{polynomial authentication}
\not\Rightarrow
\text{superpolynomial resource}.
}
\]

---

## ACR-CONG1 — Semantic continuation congruence

**Status: PROVED/EXACT.**

If legality of the next step depends only on the current extensional Boolean state, then semantically equivalent histories have identical legal semantic continuations.

Therefore provenance matters only if legality is independently defined on a richer source realization.

This is the correct role of SAME_REALIZATION.

---

## ACRTREE1 — Explicit strategy-tree growth is not representation-independent

**Status: COMPUTATIONAL hostile control illustrating an exact representation warning.**

A depth-\(d\) binary challenge tree contains \(2^d-1\) explicit nonterminal histories, while the tested complete response strategy is represented by \(d\) source bits plus a polynomial evaluator.

At \(d=20\), the explicit tree has \(1,048,575\) nodes while the source representation has only 20 bits.

Therefore explicit challenge-tree size is not a valid unrestricted complexity resource.

---

# 4. The strongest positive replay result: SBACR1

SBACR1 committed one exact Boolean-grid source word \(w\) and considered legal future SU05/Hadamard slice challenges \(s\). Let

\[
B_s(w)
\]

be the canonical reduced binary basis of the challenged slice and

\[
\Sigma(w)=(B_s(w))_s
\]

the complete response signature.

### Finite source-bound retention theorem

**Status: PROVED/EXACT in the finite no-reread model.**

If future challenge \(s\) may be arbitrary and no new \(w\)-dependent information enters after commitment, then distinct complete signatures cannot share one retained state:

\[
\boxed{
s_{\rm state}
\ge
\left\lceil
\log_2|\{\Sigma(w):w\in W\}|
\right\rceil.
}
\]

### Computational battery

All nonconstant source words were exhaustively enumerated for

\[
(p,h,m)
=
(17,4,4),
(29,5,5),
(37,6,6),
(43,7,7),
(53,8,8),
(67,9,9).
\]

The response signature was injective in every tested family:

\[
14/14,\;
30/30,\;
62/62,\;
126/126,\;
254/254,\;
510/510.
\]

Fixed-order source separation occurred after only

\[
4,\;7,\;6,\;4,\;4,\;5
\]

slice challenges respectively.

This is a real structural fact about the tested source-bound response system: a small collection of legal challenges can identify the committed source realization.

### But the reread attack is exact

The same response can be recomputed by

\[
w
\to
\text{interpolation}
\to
\text{orbit evaluation}
\to
\text{binary labels}
\to
B_s(w),
\]

all in polynomial time in the explicit parameters.

Hence

\[
\boxed{
\text{injective response signature}
\not\Rightarrow
\text{expensive reacquisition}.
}
\]

The committed source itself is a succinct representation of the complete response strategy.

---

# 5. EVACR1 and the history-quotient obstruction

## EVACR-COMP1 — Compositional evolution collapses to a succinct quotient

**Status: PROVED/EXACT.**

Suppose legal restriction operators satisfy

\[
R_{r_2}(R_{r_1}(X))
=
R_{r_1\circ r_2}(X)
\]

and the composed restriction has a polynomial-size canonical representation \(q(H)\).

Then a challenge history

\[
H=(r_1,\ldots,r_d)
\]

need not be stored as an explicit tree. The realized descendant is simply

\[
X_H=R_{q(H)}(X).
\]

If \(q(H)\) is polynomially updatable and \(R_q(X)\) is polynomially computable from the static source, costs compose rather than multiply.

Therefore ordinary evolving restrictions do not justify

\[
T(n,d)\ge n^c T(n,d-1).
\]

---

# 6. New SRAS abstraction: universal response evaluator

The earlier random/replay work points to a sharper object than provenance.

Let \(R\) be a committed source realization and \(U\) the legal challenge universe. Define the required response map

\[
\Phi_R:U\to Y.
\]

A **universal response evaluator** is an algorithm \(E\) such that

\[
\boxed{
E(R,u)=\Phi_R(u)
\qquad
\forall u\in U.
}
\]

The key resources are:

\[
|R|,
\qquad
|E|,
\qquad
T_E(R,u),
\qquad
S_E(R,u).
\]

The evaluator may also use a canonical polynomial-size evolving state \(q(H)\).

---

## Theorem FRESH-EVAL1 — Freshness does not amplify a compact evaluator

**Status: PROVED/EXACT.**

Suppose:

1. \(R\) has polynomial length;
2. legal challenges \(u_1,\ldots,u_T\) arrive adaptively, including from an IID post-stopping-time random source;
3. \(T(n)\) is polynomial;
4. there is a deterministic polynomial-time universal evaluator
   \[
   E(R,h_{<i},u_i)
   \]
   returning the exact required response at each round, where the maintained history quotient \(h_{<i}\) has polynomial size and is polynomially updatable.

Then the complete realized response process runs in deterministic polynomial total time after the challenges are revealed.

### Proof

Store \(R\) and the polynomial-size current quotient. At round \(i\), wait for the challenge \(u_i\), evaluate \(E(R,h_{<i},u_i)\), update the quotient, and continue. Polynomially many polynomial-time rounds remain polynomial. Freshness prevents preprediction of \(u_i\), but does not obstruct post-revelation evaluation. \(\square\)

### Consequence

\[
\boxed{
\text{unpredictable challenge}
+
\text{source-bound SAME\_REALIZATION}
\not\Rightarrow
\text{expensive response}.
}
\]

A random-stream lower-bound route must prove that no polynomial universal response evaluator exists, or prove a quantitative tradeoff on every such evaluator.

---

# 7. Source entropy ceiling

## Lemma SIG-ENTROPY1

**Status: PROVED/EXACT.**

For a finite committed source family \(W\), any complete response signature

\[
\Sigma:W\to Y^U
\]

satisfies

\[
|\Sigma(W)|\le |W|.
\]

Hence

\[
\boxed{
\log_2|\Sigma(W)|
\le
\log_2|W|.
}
\]

If the committed source has \(h\) explicit bits, pure response-signature information cannot exceed \(h\) bits.

Thus repeated challenges cannot manufacture more independent source information than the committed source contains.

SBACR1 reaches this ceiling on its tested nonconstant word families because the complete signature is injective.

This is a positive structural property, but not a runtime lower bound.

---

# 8. New SRAS classification for random/replay systems

The relevant state is

\[
\mathcal A_t
=
(\text{source authority},
\text{challenge filtration},
\text{response evaluator},
\text{history quotient},
\text{recovery authority},
\text{fate}).
\]

For each future-relevant response obligation, classify it as:

1. **PRECOMPUTED:** encoded before challenge revelation;
2. **EVALUABLE:** generated after challenge from a retained/re-readable source by a compact evaluator;
3. **REACQUIRED:** regenerated by replay/reread/recomputation;
4. **EXTERNAL:** supplied by genuinely new information;
5. **HARD-EVAL:** no sufficiently cheap evaluator is available.

The first three are forms of GLOBAL AUTHORITY in static SAT. Only HARD-EVAL is a candidate lower-bound branch.

Freshness is recorded separately:

\[
\mathrm{Fresh}(u_i\mid \mathcal F_{\tau_i})=1.
\]

It blocks PRECOMPUTED challenge-specific answers, but does not block EVALUABLE or REACQUIRED answers.

---

# 9. Replay attack taxonomy

The previous documents identify four replay attacks that every future construction must survive.

### Replay A — deterministic rerun

If

\[
R=S(x)
\]

for deterministic polynomial-time \(S\), then discard-and-rerun costs polynomial time.

### Replay B — transcript regeneration

If a demanded object is a polynomial-time functional of a polynomial execution transcript, TRACECLOSE1 makes it polynomially regenerable.

### Replay C — PH replacement

If a valid replacement realization is polynomially balanced and fixed-PH verifiable, then under \(P=NP\) PH-PROV-CLOSE1 selects a valid realization in FP, including unique or lexicographically canonical realizations.

### Replay D — compositional quotient

If challenge histories compose into a polynomial-size canonical quotient, EVACR1 lets the algorithm retain the quotient and evaluate only the realized branch.

A surviving replay-hardness theorem must defeat all four.

---

# 10. What the random stream can still contribute

The random stream is not useless. It gives an exact way to guarantee that challenge selection is not a function of the prior solver state.

This can be useful for a **no-sharing/direct-product test**:

- commit the source/representation before seeing the next fresh challenge;
- draw challenge \(u_i\) independently after a stopping time;
- require a SAME_REALIZATION response;
- ask whether one globally reusable evaluator can service all such fresh challenges.

If a cheap evaluator exists, FRESH-EVAL1 closes the route.

If not, the missing theorem becomes precise:

\[
\boxed{
\text{fresh source-bound challenge family}
\Longrightarrow
\text{superpolynomial universal-response evaluation cost}
}
\]

for the selected hard 3-SAT family and every ordinary computation model under consideration.

This is stronger and cleaner than a claim about replay authentication or transcript size.

---

# 11. Candidate Random-Source Evaluation Barrier

## Candidate RSEB1

**Status: OPEN / load-bearing candidate.**

There exists an infinite 3-SAT-derived family of committed source objects \(R_n\) and legal challenge universes \(U_n\) such that:

1. challenges can be sampled fresh after source commitment;
2. responses are intrinsic to the same source realization;
3. no polynomial-size/polytime universal evaluator \(E(R_n,u)\) computes all exact responses;
4. no polynomial-size history quotient or preprocessing structure restores such an evaluator;
5. static reread, deterministic replay, memoization, pointer jumping, INTERP, RECOMP, semantic oracles, and algebraic oracles do not supply an equivalent cheap evaluator;
6. the response obligation is forced by every hypothetical polynomial-time exact SAT decider through a model-preserving compiler.

If the evaluator lower bound is merely superpolynomial, that is enough for a \(P\ne NP\) contradiction once the compiler is proved.

No clause of RSEB1 is currently established at unrestricted SAT scope.

---

# 12. Relativization interpretation

Fresh randomness is not itself nonrelativizing. RANDCLOSE1 and the generic replay closures relativize.

However, RSEB1 suggests where a nonrelativizing hinge would have to live:

\[
\boxed{
\text{ordinary source implementation}
\not\equiv
\text{opaque semantic/oracle evaluator}.
}
\]

A valid proof must use implementation/source structure essential to ordinary computation while explicitly failing when the evaluator is replaced by an oracle.

Merely appending source tags, commitments, hashes, or authenticated replay does not achieve this.

---

# 13. Practical consequence for SRAS/CSE

The earlier LOCALIZE / SUMMARIZE / REACQUIRE classification should be refined for static random/replay constructions:

\[
\boxed{
\mathrm{CONTRACT}
\;\vee\;
\mathrm{UNIVERSAL\ EVALUATOR}
\;\vee\;
\mathrm{EXTERNAL}.
}
\]

Reread, replay, preprocessing, memoization, and compact retained summaries are all implementation variants of UNIVERSAL EVALUATOR / GLOBAL AUTHORITY.

Therefore the most useful next attack is not another provenance layer. It is:

\[
\boxed{
\text{prove or falsify a universal-response evaluator barrier}
}
\]

on the low-degree externally mediated clean-core 3-SAT family or another source-matched hard family.

---

# 14. Strict ledger

## PROVED/EXACT
- stopping-time freshness;
- timing-sensitive transcript divergence under blind-source hypotheses;
- transcript determinacy for fixed solver/source;
- realized-path replay closure;
- semantic continuation congruence;
- compositional history-quotient collapse;
- deterministic reread/replay closure;
- RANDCLOSE1 under \(P=NP\);
- FRESH-EVAL1;
- SIG-ENTROPY1.

## COMPUTATIONAL
- CRS-PPC timing experiments;
- ACRTREE1 strategy-compression control;
- SBACR1 injective complete response signatures for \(h=4,\ldots,9\);
- small distinguishing challenge depths \(4,7,6,4,4,5\);
- finite shift/pebbling controls.

## FALSIFIED/RETIRED AS GENERIC HINGES
- random freshness alone;
- solver-relative timed transcript divergence;
- replay authentication alone;
- explicit strategy-tree size;
- response-signature diversity alone;
- ordinary evolving restrictions;
- repeated shift/affine histories;
- no-reread storage lower bound under unrestricted static rereading;
- polynomial random causal depth as static hardness.

## OPEN
- source-matched no-succinct-evaluator theorem;
- representation-independent no-sharing/direct-product theorem;
- static-SAT compiler forcing the response obligation;
- superpolynomial evaluator or reacquisition cost;
- nonrelativizing/nonalgebrizing hinge.

---

## Final assessment

The earlier random-digit/random-bitstream work produced a useful exact resource:

\[
\boxed{\text{freshness after a stopping time}.}
\]

The replay work produced a useful exact guard:

\[
\boxed{\text{same-realization provenance does not prevent cheap replay}.}
\]

Their synthesis shifts the target from “cannot predict the challenge” to

\[
\boxed{
\text{cannot cheaply evaluate the correct response after the challenge}
}
\]

even with the committed source, polynomial preprocessing, replay, and every legitimate reusable representation available.

That is the strongest surviving random/replay contribution to the current SRAS/CSE program.