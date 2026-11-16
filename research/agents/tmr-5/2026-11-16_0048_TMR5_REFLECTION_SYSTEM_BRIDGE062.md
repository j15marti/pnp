# TMR-5/062 | 2026-11-16 00:48 PST | A fixed reflection system for which the derivation-cost bridge is provable, and the exact gap that remains

Role: TMR-5 / PNP Machine Bottleneck Redteam, acting as "Independent Proof Red Team" for the scheduled
worst-case derivation-cost directive. P versus NP remains **OPEN**. Retired trackers, historical root
main files, peer manuscripts, identities and schedules are untouched.

## 0. Repository state and reconciliation

Base: origin/main `a29605c5`. Two divergent unmerged TMR-5 lineages existed:
`origin/ccr-1695bd63-lh9sf9` (/057 bridge, /058, /059, /060 black-box collapse; no PR) and
`origin/tmr5-20261115-2125-pinned-kernel-retry058` (draft PR #199: /058, /059, a second /060 on the
C1g padding ceiling, /061 conditional quadratic count). Both were merged into branch
`ccr-1695bd63-873tr6`. The two main5 conflict hunks were resolved by keeping both sides in full
(bridge section followed by the /061 and C1g sections). Both conflicting handoffs are archived
byte-exact:

* `archive/handoff_pre_2026-11-16_0048_branch060bridge.md`, blob `0a1cdcb15a28f7ec84a329cdd1d6b8a546513171`
* `archive/handoff_pre_2026-11-16_0048_branch061.md`, blob `48eb6e9973ece1fe2fd576d7c72c93369a5732ee`

Both blobs equal the branch originals (checked with `git hash-object` and `git rev-parse`).

Duplicate check: /057 proved Theorem A (known L(R) gives B(R) <=> SAT not in P) and recorded
Theorem B (for R >= EF, B(R) <=> a correct algorithm has short R-proofs of soundness). /057 also
remarked that B(R) is known for an *optimal* R, whose existence is OPEN. /060 proved Theorem C (no
black-box proof of B(R)). This run does not repeat them. It replaces the hypothetical optimal system
with an explicit fixed system, proves the bridge for a precisely named and very large algorithm
class, and isolates the exact residual premise.

## 1. Named dependency, candidate and falsifiers

Dependency: **BRIDGE-B(R), choice of R.** The directive asks for "a fixed, sufficiently powerful
logical system" for which `SAT in P => W_R(N) <= poly(N)` can be proved. Theorem A rules out every R
with a known lower bound. Theorem B reduces EF to feasible provability. The question left open is
whether any explicit fixed R makes the bridge provable, and what it would then cost.

Candidate, stated before the literature check: for a sound theory T (for example ZFC), the
Krajíček–Pudlák-style reflection system P_T makes the bridge provable for every SAT algorithm whose
*soundness* (only) is T-provable. The remaining gap is then exactly a provability statement. That gap
cannot be closed by any single fixed T.

Falsifiers stated in advance:

1. P_T is not a Cook–Reckhow system, because its verifier runs in time that grows with the proof
   rather than in one polynomial, or because it is unsound.
2. The restricted bridge contradicts Theorem C, which would mean a hidden black-box step.
3. The gap is illusory: every correct polynomial-time SAT algorithm has T-provable soundness for some
   fixed T.
4. The gap is closable by a single stronger fixed theory.

## 2. The system P_T

Let T be a theory with a polynomial-time recognizable axiom set. T contains IΣ1, so it formalizes
Turing machines and Gödel's second theorem applies. T is Π⁰₁-sound, meaning every Π⁰₁ theorem of T is
true. ZFC is assumed Π⁰₁-sound.

For a deterministic multitape machine code M and an integer k let `Sound(M,k)` be the Π⁰₁ sentence

    for every CNF G: if M on input <G> halts within |<G>|^k + k steps with output 0,
    then no assignment satisfies G.

A **P_T-refutation** of a CNF F is one of two things:

* (a) an ordinary resolution refutation, which keeps P_T complete; or
* (b) a tuple `pi = (<M>, k, sigma, 1^t)`, where sigma is a T-proof of `Sound(M,k)` and
  `t = |<F>|^k + k`.

The verifier `V_T(F, pi)` handles case (b) in four steps. It rebuilds the sentence `Sound(M,k)` from
`<M>` and k, in time poly(|M| + log k). It checks sigma as a T-proof of that sentence, in time
poly(|sigma|), which works because the axioms are polynomial-time recognizable. It checks the padding
length. Finally it simulates M on F with a universal clocked machine for t steps, in time
O(|M| · t log t), and accepts iff the output is 0.

**Lemma 1 (Cook–Reckhow, PROVED).** V_T runs in time poly(|F| + |pi|) for one fixed polynomial. It
is sound, and P_T is complete.

*Proof.* Every term in the running time is polynomial in |pi|, because t ≤ |pi| and |M|, |sigma| ≤ |pi|.
Soundness: if V_T accepts in case (b), then T proves `Sound(M,k)`. That sentence is Π⁰₁, so it is
true, and M's output 0 on F within the clock certifies that F is unsatisfiable. Case (a) is sound
because resolution is sound. Completeness comes from (a). ∎

Falsifier 1 is refuted. The padding `1^t` is what makes one polynomial suffice. Without it the
verifier time would be |F|^k with k read from the proof, which is not Cook–Reckhow. This is the
standard Krajíček–Pudlák device.

## 3. Theorem D (PROVED/EXACT, elementary; independent review OPEN)

Define the algorithm class

    K_T = { (M,k) : M outputs 0 within |<G>|^k + k steps on every unsatisfiable G,
                    and T proves Sound(M,k) }.

Only the soundness direction must be T-provable. Completeness on UNSAT inputs and the running time
need only be *true*. The SAT side of the decision is irrelevant here, because refutations concern
UNSAT inputs only.

**(i) Restricted bridge with explicit cost.** If (M,k) is in K_T, then for all N

    W_{P_T}(N) ≤ |<M>| + O(log k) + |sigma_M| + N^k + k = N^k + c_M,

where c_M is a constant that depends only on M and its T-proof. The verification time is
O(c_M · N^k log N).

*Proof.* For every UNSAT F with |<F>| ≤ N, the tuple (b) built from M is accepted. ∎

No discovery is charged, exactly as the directive allows. The constant c_M may be astronomically
large. It is still a constant.

**(ii) The full bridge, reduced to one premise.** Define

    BR_T :  SAT in P  =>  K_T is nonempty.

Then BR_T implies B(P_T). Hence

    BR_T  and  L(P_T)  =>  P ≠ NP,

where L(P_T) means W_{P_T}(N) ≥ N^{ω(1)}.

**(iii) Exactly what L(P_T) says.** By (i), L(P_T) implies that K_T is empty. In the generalised
form with appended Q-proofs, W_{P_T} ≤ poly holds if some fixed T-provably-sound, polynomially
bounded checker Q exists. The converse is not claimed, because the certified Q may vary with N.
Here "L" is read as "not polynomially bounded", and the infinitely-often versus almost-everywhere
distinction is kept explicit. L(P_T) implies L(EF), and
therefore L(Frege), L(AC0[2]-Frege) and L(Res(⊕)). The reason is that P_T p-simulates every proof
system whose soundness T proves via a polynomial-time checker. That includes EF, Frege, Res(⊕) and
CP: in each case M takes the proof as part of the input, so the class definition is applied to the
system's checker. That generalisation is a one-line change, with sigma proving soundness of a checker
Q and a Q-proof w appended. Without BR_T, L(P_T) yields only the *metamathematical* statement "T does
not prove any explicit polynomial-time UNSAT decider sound". That is not P ≠ NP.

**(iv) Gödel control: K_T depends on the code, not the language. PROVED.** Assume SAT is decided in
polynomial time by some A with (A,k) in K_T. Define M_T. On input G, it sets ℓ = ⌊log₂|<G>|⌋. It
searches every string of length ≤ ℓ for a T-proof of 0=1, which takes 2^ℓ · poly(ℓ) = poly(|G|) steps.
If it finds one it outputs 0. Otherwise it outputs A(G).

Since T is consistent, M_T computes exactly the function A computes, within a clock k' = k + 2.
Suppose T proved `Sound(M_T, k')`. Work inside T. If p were a T-proof of 0=1 of length ℓ, then
M_T(G) = 0 on the satisfiable padded formula G = (x₁) ∧ (x₁ ∨ x₂) ∧ … of length ≥ 2^ℓ. That contradicts
soundness. So T ⊢ Con(T), which is impossible by Gödel II. Hence (M_T, k') is not in K_T, although it
is a correct polynomial-time decider whenever A is.

So falsifier 3 is refuted *in its strong form*. For every fixed T there are correct polynomial-time
SAT algorithms whose soundness T cannot prove. This does **not** show that K_T is empty when SAT is in
P. In the scenario above A itself is in K_T. BR_T asks only that *some* correct code be T-provable.

**(v) No single fixed theory closes the gap. PROVED in the following exact form.** For every
consistent recursively axiomatized T as above, M_T is in K_{T + Con(T)} \ K_T. Consider the scenario
"SAT is in P, but every correct polynomial-time decider is like M_T, with soundness unprovable in T".
No known theorem refutes it. In that scenario L(P_T) is true and P ≠ NP is false. Therefore:

* any proof of `L(P_T) => P ≠ NP` must prove BR_T or a substitute. BR_T is a genuinely
  metamathematical premise.
* falsifier 4 is refuted. Replacing T by T' = T + Con(T) only moves the gap, because M_{T'} escapes
  T'.

**(vi) Consistency with Theorem C (falsifier 2).** The proof of (i) uses the oracle-free code of M
and a T-proof about that code. Relative to an oracle O, an algorithm in P^O has no oracle-free code,
and P_T does not simulate oracle-backed systems. So (i) is white-box, and the relativized statement
B^O(P_T) gets no support from it. Theorem C(iii) does not apply, because no L(P_T) is known.
Theorem C(i) still says that B^TQBF(P_T) would give W_{P_T} ≤ poly. No contradiction.

## 4. Consequences for the five-agent plan (ranked)

1. **For the General SAT Lower-Bound Lead (priority 1, weakest sufficient bridge).** The strongest
   *provable* version of the bridge is Theorem D(i) for R = P_ZFC. Its class K_ZFC contains every SAT
   algorithm whose soundness ZFC proves, which covers every algorithm a human could certify. The
   full unconditional bridge is equivalent, for this R, to BR_ZFC. Any priority-1 claim must name
   BR_T as an explicit premise, or restrict its conclusion to K_T.
2. **For the Hypergraph & Proof Certificates agent (priority 4, survival across reasoning methods).**
   A hard family for P_T must be hard for EF. As of the February 2026 literature (Section 6), general
   superpolynomial lower bounds are open even for Res(⊕), which sits far below EF. Candidate families
   should therefore be graded by the weakest system known to refute them in polynomial size. Tseitin
   falls to Res(⊕) and GF(2) elimination. PHP falls to CP, and to counting. Random 3-CNF at constant
   density has no known polynomial refutation in any system: it is the standing candidate, with no
   proof.
3. **For the SAT-Circuit Reduction Builder (fixed combined inference system).** P_T is not a
   local-rule DAG system. Inside the multisign-hypergraph framework, P_T-strength is reached only by
   adding *reflection hyperedges*. Each such hyperedge is an axiom RFN_Q: "a Q-proof of φ implies φ",
   and EF + RFN_Q p-simulates Q. A fixed local-rule system without reflection is at most a fixed
   system Q₀ for which BR-type premises fail in the sense of (iv)–(v).
4. **The free optimal sequence concession (directive item 2) remains sound.** In P_T it makes the
   minimum cost N^k + c_M, a polynomial that is dominated by padding. All hardness then sits in
   whether a certified code exists, not in executing a derivation.

## 5. Four gates

* DISJ sanity: PASS. No static invariant is used as a work bound.
* Relativization: Theorem D(i) is white-box and non-relativizing (Section 3(vi)). The full bridge
  still FAILs for black-box proofs, by Theorem C.
* Algebrization: FAIL for algebrizing proofs of the full bridge, by Theorem C(v).
* Natural Proofs: any L(P_T) implies L(EF) and inherits the proof-complexity-generator barriers
  (OPEN).
* Simultaneous DTISP: NOT APPLICABLE, because no simulation is claimed.
* Deterministic configuration counting: PASS only as an upper-bound guard.
* /341 FAIL as full UNSAT authority. /386 RESTRICTED.

## 6. Literature check this run (clues)

Web search, 2026-11-16.

* Krajíček–Pudlák, JSL 54(3):1063–1079 (1989). An optimal proof system exists iff a "fast
  consistency prover" exists, namely a theory with short proofs of the finite consistency statements
  of every polynomial-time axiomatized theory. Seen through the abstract of Joosten, NDJFL 48(3)
  (2007), arXiv 2004.05431. **Clue:** BR_T is closely related to this. If T were a fast consistency
  prover, the M_T obstruction would shrink from unprovability to proof length. That suggests a
  length-sensitive version of BR_T as the natural repair target. This is OPEN and unverified, and
  the full KP paper was not read.
* Res(⊕) status. ECCC 2025/116 (Efremenko–Gryaznov) and ECCC 2026/018 both state that general
  superpolynomial Res(⊕) size lower bounds are open. ECCC 2026/018 calls Res(⊕) the weakest
  subsystem of AC0[2]-Frege without them. There are restricted results: depth o(n²/log⁴ n) in ECCC
  2026/018, nearly quadratic depth in arXiv 2507.23008, and bounded-depth bit-PHP in arXiv
  2511.20023. Only abstracts and search summaries were read.
* arXiv 2304.00610 ("Ruling out short proofs of unprovable sentences is hard") appeared in the
  results and is unread. It is plausibly relevant to the length-sensitive BR_T.

## 7. Validation actually run

This is a pen-and-paper proof checked by hand. No new code, no preflight script, no LaTeX build
(pdflatex is unavailable), and no Lean or nanoda. Git checks of the merge and archive blobs were
executed. The /057 Python control was not rerun.

## 8. One next lemma

Length-sensitive BR_T, for the General SAT Lower-Bound Lead with TMR-1. Either prove or refute:
"if SAT is in P via any A, then there are k and a T-proof of `Sound(M,k)` for some M computing the
same function as A within a polynomial clock". Alternatively, show that this statement implies a
fast-consistency-prover property for T, which would make it at least as hard as the open existence
of optimal proof systems. Section 3(iv) shows that the code-level version fails. Only the
function-level version is open.

## References

Cook, Reckhow, JSL 44 (1979). Cook, STOC 1975. Krajíček, Pudlák, JSL 54 (1989). Joosten, NDJFL 48
(2007). Krajíček, *Proof Complexity*, CUP 2019. Gödel 1931; Hilbert–Bernays derivability conditions.
Efremenko, Gryaznov, ECCC TR25-116. ECCC TR26-018. Bhattacharya, Chattopadhyay, arXiv 2507.23008.
Byramji, Impagliazzo, arXiv 2511.20023. TMR-5/057 and /060 reports in this directory.
