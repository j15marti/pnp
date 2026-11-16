# TMR-1/059 v2: unconditional polynomial-circuit upper bound for exponential padding

November 15, 2026, 20:12 PST. TMR-1 / PNP Machine Model Lead. This is a **strict strengthening and explicit correction of the scoped emphasis** of TMR-1/059 at `2026-11-15_2006_TMR1_EXP_PADDING_NP_GATE059.md`. Its existing proofs remain valid, but it needlessly stopped at a limitation on a particular lower-bound transfer rule. The stronger upper construction below rules out *any superpolynomial unrestricted circuit lower bound on this exact padded language*, even if the base language is undecidable. No claims are made about other nonpadding NP-level constructions.

## Candidate and falsifiers (pre-source check)

For every language W, integer c≥1 and input length M=2^(cn), the **actual padded language itself**, not just its inherited lower-bound certificate, has O(M log M) fan-in-two nonuniform circuit size. Three falsifiers: (1) ambiguous delimiter or multiple n corresponding to one M; (2) uncharged nonuniform advice dependence that is incorrectly presented as a uniform algorithm; (3) output-family sizes M not of form 2^(cn) inadvertently accepting inputs. All three are explicitly handled. Source and model scope: arbitrary f_n, deterministic Boolean fan-in-two circuits, all M-bit inputs, counting noninput gates, NOT an asserted uniform circuit compiler.

## Theorem C1g+ (PROVED/EXACT restricted; independent review OPEN)

For every language W⊆{0,1}* and fixed integer c≥1 define

```
P_c(W)={x 1 0^(2^(c|x|)-|x|-1): x∈W, |x|>=1}.
```

Then for **every length M**, `SIZE(P_c(W)_M)≤O(M log(M+2))` in unrestricted nonuniform fan-in-two Boolean circuits, with the hidden constant depending on c but not W or M. In particular, `P_c(W) ∈ P/poly` **unconditionally**, even if W is undecidable. Thus no valid circuit lower bound `M^ω(1)` for this padded language is possible. This is an upper-bound construction, not a P=NP conclusion.

**Proof.** If M is not equal to 2^(cn) for any integer n≥1, the length-M characteristic function is identically zero and has a constant-size circuit. Otherwise n=(log_2 M)/c is uniquely determined. Build an M-input circuit as follows. Let `Z` be the AND of the delimiter bit in position n+1 and the negations of all M−n−1 trailing positions. It has O(M) fan-in-two gates, including any input negations. Let `F_n` be a DNF circuit for the arbitrary n-bit function `W_n`, using a shared set of n input negations, at most 2^n minterms with ≤n literals each, and a balanced OR tree: at most O(n2^n) gates. Output `Z AND F_n(x_1,...,x_n)`. The output equals the padded predicate **for every M-bit input**, not only for words already known to have a valid suffix. Gate count is

```
G(M) <= O(M+n2^n) = O(M + (log M) M^(1/c)) = O(M log M)   (c>=1).
```

For nonuniform circuits, the at most 2^n-bit truth table of W_n may be hardwired separately at each length; no uniform discovery procedure is claimed. Such advice has length 2^n=M^(1/c), itself polynomial in the padded length. Thus the construction is valid even for noncomputable W.

The previously proved correct-direction restriction is also valid: fixing the authentic padding suffix of any padded circuit yields a circuit for W_n. Hence `SIZE(P_c(W)_M)≥SIZE(W_n)-O(1)`, but the **actual universal upper bound** just proved rules out any stronger unrestricted superpolynomial lower bound on the padded family. The conditional C1f `Ω(n√log n)` lower bound still translates only to `Ω(log M√loglog M)` on its sparse lengths. These facts are mutually consistent.

## Conditional uniformity lemma (unchanged from /059)

If W∈E^NP is computed in time 2^(an) with NP queries and **if P=NP** gives an oracle decider of degree b, substitute at most 2^(an) calls of length ≤2^(an). An ordinary machine runs in time ≤2^(a(b+1)n+O(1)). For M=2^(cn), a padded-input verifier reads and validates every source bit and computes W, with one-run conservative `T=O(M^3+M^(a(b+1)/c))`, `S_peak=O(M+M^(a(b+1)/c))`. Thus `P_c(W)∈P` under P=NP, whereas P/poly membership needs **no** P=NP assumption. The two claims must not be conflated. Without P=NP no uniform P or NP membership is implied by this proof.

## Integration and gates

The C1a input→C1b count-preserving gate compiler→C1c promise totalizer→C1d formal `encInput`→C1e pinned formal #SAT and physical TM (conditional/unrebuilt source)→C1f JMV and binary hierarchy (`E^NP` conditional mild i.o. LB) chain is unchanged. The proposed C1g exponential-padding route to an NP **superpolynomial** circuit lower bound is now **FALSIFIED outright by an explicit polynomial-size padded circuit**, not just blocked by an inadequate lower-bound transfer rule. The circuit is fully general, includes all input accesses as actual wires, shares negations, checks padding for both labels, and never assumes a uniform construction or free advice acquisition. The statement does not disprove nonpadding NP-level hypotheses.

Four gates: DISJ **PASS** (the upper construction explicitly admits compact circuits despite high rank); relativization **PASS for upper construction, OPEN for any NP separation** (BGS/algebrization/Natural Proofs remain); simultaneous DTISP **NOT APPLICABLE to nonuniform upper circuit size**, with separate conditional uniform source-checking machine's time and peak space explicitly matched; deterministic configuration counting **NOT APPLICABLE to circuit gate counting**, with total deterministic physical-run upper sanity retained if the conditional machine is used. /341 FAIL full UNSAT logical authority; /386 RESTRICTED. All Horn/2SAT/affine/treewidth, equality/autarky/product, auxiliary, selector, unique-solution, field effects and compact alternatives legal.

Status PROVED/EXACT RESTRICTED, external independent mathematical review OPEN. No empirical execution was required for the elementary symbolic construction; no new code/raw data, Lean kernel build, `#print axioms`, LaTeX compilation or PNP checkout preflight occurred. The older /059 report is retained verbatim for provenance and correctly described its weaker method-specific bound.

**ONE next load-bearing source dependency:** independent Lean v4.33.1 pinned rebuild plus transitive axiom audit of `MainResults.mainTheorem` and `MainResults.ethIsFalse`, then verify C1e fixed finite-stack/physical-bit semantics. P versus NP OPEN.

Sources: Anthropic pinned `eth/MainResults.lean`, `eth/Solution.lean`, `CountedRoute/Main.lean`, `Wrap/Main.lean`, commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5; Jahanjou--Miles--Viola *Local Reductions*, ECCC TR13-099 rev.3 (2014), Theorem 1 and Corollary 2, https://eccc.weizmann.ac.il/report/2013/099/ . DNF truth-table circuit upper is proved independently here.
