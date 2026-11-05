# CLAUDE / BRIDGE-DICHOTOMY-0001 — the conditional bridge is necessary, and equivalent to P≠NP wherever a lower bound is known
2026-11-05. P versus NP remains OPEN. Role: General SAT Lower-Bound Lead (worst-case W̄_R, weakest sufficient bridge).

## Corpus reviewed
Survey of the repo tree and last commits (LSPV-1/412, LSPV-3/415, LSPV-2/411); LSPV-1/395 handoff (W̄ can be noncomputable even with a linear node bound); LSPV-1/412 (RUP→native-Resolution bridge, restricted B1); grep hits for reflection reports 353 and 405; Claude ONETAPE-0001. No file states the dichotomy below in this exact form (grep for "bridge is equivalent" / "vacuous" found only unrelated hits), but it is elementary and may be folklore; novelty is NOT claimed.

## Setting
R: a fixed sound, complete propositional proof system with a polynomial-time verifier. W̄_R(N) as in the directive. Bridge(R) := (SAT∈P ⟹ ∃k W̄_R(N) ≤ N^k+k). Lower(R) := W̄_R superpolynomial.

## Theorem 1 (PROVED/EXACT, elementary)
(a) Bridge(R) ⟺ (SAT∉P) ∨ (W̄_R polynomially bounded).
(b) Lower(R) ∧ Bridge(R) ⟹ SAT∉P (the intended use), and Bridge(R) is *necessary* for the strategy: if SAT∈P and Lower(R) held, Bridge(R) would be false.
(c) If Lower(R) is a known theorem (Resolution — Haken 1985; cutting planes; bounded-depth Frege), then Bridge(R) ⟺ SAT∉P ⟺ P≠NP, *unconditionally*. So a proof of the bridge for such R is a proof of P≠NP; the bridge is not a weaker, separately provable step there.
Proof: (a) is propositional logic on "A→B ≡ ¬A∨B". (b) modus ponens / contrapositive. (c) substitute the known truth of Lower(R) into (a): "W̄_R poly" is false, leaving ¬(SAT∈P). ∎

## Corollary (non-circularity criterion)
A bridge proof is informative only for an R whose polynomial-boundedness is OPEN (Frege, Extended Frege, stronger). For such R the bridge ⟺ (P≠NP ∨ R poly-bounded); proving it requires, assuming only that some poly-time A decides SAT, *short R-proofs of every UNSAT instance*. Known routes: (i) R proves "A is correct" in a short uniform way (reflection; the gap is that true correctness of an unknown A need not be R-provable — cf. corpus reports 353, 405); (ii) R is, by definition, enriched with A's verifier (artificial system; trivially poly-bounded under SAT∈P but then Lower(R) is the same unknown). Hence the "weakest sufficient bridge" and the lower bound for a strong R are *jointly* at least as hard as the Cook–Reckhow program NP≠coNP-for-all-systems; the directive's strategy does not escape it.

## Clarification of free strategy search (consistent with the directive)
W̄_R is a min over derivations, so charging nothing for finding the optimal π is legitimate for a lower bound on executing π. Atserias–Müller (Resolution is NP-hard to automate) concerns finding π, not its existence; it neither helps nor harms the bridge. LSPV-1/395 shows exact W̄ can be uncomputable, so this free-knowledge convention is a *definition*, not an algorithmic step.

## Literature check (this run)
- Pitassi/Atserias-Müller/… line: automatability of Resolution NP-hard; no non-trivial system known (quasi)poly automatable (background, via search summary).
- arXiv:2506.16956 "The Proof Analysis Problem" (revised May 2026; not read in full, only search summary): poly-time extraction of a satisfying assignment from short Resolution refutations of Ref(φ) ("φ has a short Resolution refutation"); Proof Analysis for EF NP-complete; for systems simulating EF, weak automatability ⟺ automatability on formulas stating Resolution lower bounds. CANDIDATE clue: Ref(φ)-type formulas are natural hard-instance families for EF-class R; whether they give a superpolynomial W̄_R is unknown. Needs reading before use.
- No found result resolves optimal proof systems or EF lower bounds.

## Status
PROVED/EXACT: Theorem 1 (elementary). CANDIDATE: use Ref(φ) families as test instances for the red-team role. OPEN: Lower(R) for any R with OPEN poly-boundedness; Bridge for such R. No claim toward P vs NP.

## Next steps per role
Lead: state precisely which R-reflection principle suffices for Bridge(R) (uniform over all poly-time A, not a fixed A). Builder/Auditor: none needed — Theorem 1 is system-independent. Red team: look for a flaw in (c) via R whose lower bound is proved only for a *restricted* formula class, so Bridge(R) is equivalent to P≠NP only for the restricted-family version.
