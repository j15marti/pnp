# TMR-1/059: An exact padding barrier for the NP-level promotion of C1f

Date: November 15, 2026, 20:06 PST (America/Los_Angeles). Owner: TMR-1 / PNP Machine Model Lead. Governing directive: `research/coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md` (main blob `8451d955f6cd5397de0895f8ebb46e30818842c3`). Compatible scientific scope: SAT compression and circuits. P versus NP **OPEN**.

## Candidate before source review; falsifiers

**C1g-EXP-PADDING-NP-GATE.** Can the specific C1f conditional higher-class witness `W ∈ E^NP`, with infinitely-often general-circuit lower bound `Ω(n sqrt(log n))`, be padded to a language in NP while inheriting a *superpolynomial* circuit lower bound? Exact quantifiers: for every deterministic oracle machine witnessing `W∈E^NP` with time `2^{a n}`, every fixed integer `c≥1`, and every circuit family for the padded function, study the input-length map `M=2^{c n}`, its direction of circuit restriction and its complexity under the **hypothesis P=NP**. No hypothesis on actual circuit complexity of W beyond C1f's conditional lower bound is added.

Predeclared hostile falsifiers: (i) a correct-direction restriction that preserves an `M^{ω(1)}` bound despite `n=Θ(log M)`; (ii) an unconditional NP membership certificate for this exact padded E^NP language with charged oracle answers; (iii) a circuit-size upper bound for n-bit truth tables exceeding the proposed padding lower-bound ceiling; (iv) a nontrivial alternative **non-padding** NP-level theorem (out of scope and not ruled out here).

## Source-authenticated integration point

The pinned Anthropic source `anthropics/formal-math` at `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`, `eth/MainResults.lean` blob `1c62a550fa1e4cbec65bb7112f92ad67589afddc`, asserts its exact count bound for one fixed finite-alphabet machine. `eth/Solution.lean` blob `176892178e49792ae41368c13bb4973bae035b29` supplies the formal theorem term. The pinned upstream CI acceptance is documented in TMR-1/057; a *new* independent local Lean kernel rebuild was unavailable in this run.

Jahanjou--Miles--Viola, *Local Reductions*, revision 3 (April 2014), Theorem 1, uses a clause-index decoder `D:{0,1}^ell→{0,1}^{3v+3}` produced in `poly(n,log T)`, with constant output-bit locality for `T≥2^n`. Its Corollary 2 target is `E^NP`, not NP. TMR-1/056 independently builds the binary oracle witness `W∈E^NP` and the conditional mildly superlinear lower bound. TMR-5/054 already proved the authentic-address zero-violation guard; **this run does not duplicate it**. The new dependency is *only* the attempted higher-class-to-NP padding arrow C1g.

## Theorem C1g (PROVED/EXACT, restricted to exponential padding and circuit restriction)

Let `W ⊆ {0,1}^*` be any language, let `c≥1` be fixed and define the exact exponential-padding language

```
P_c(W) = { x 1 0^(2^(c|x|)-|x|-1) : x∈W, |x|≥1 }.
```

Use `SIZE(f_n)` for fan-in-two circuit gate complexity excluding source-input gates, permitting hardwired constants.

**(a) Correct-direction restriction.** For `M=2^{cn}` and every `M`-input circuit `A_M` computing the padded predicate on all `M`-bit strings, hardwire the last `M-n` inputs to the unique delimiter and zero suffix. The remaining `n`-input circuit computes `W_n`. Hence

```
SIZE(P_c(W)_M) >= SIZE(W_n) - O(1).
```

This arrow is lower-bound transfer from the original `n`-bit function to its *much longer* padded version at a sparse sequence of lengths; it cannot be reversed to infer a stronger original bound.

**(b) Ceiling on what this method alone can infer.** Every Boolean `n`-bit function has a standard DNF fan-in-two circuit with at most `O(n 2^n)` noninput gates: at most `2^n` minterms of up to `n` literals, then a binary OR tree. Therefore `SIZE(W_n)≤O(n2^n)` for every W, whether or not it is computable. At `M=2^{cn}` this equals `O(M^{1/c} log M)`. In particular, no lower bound transferred **only by applying (a) to a lower bound on `SIZE(W_n)`** can prove `M^{ω(1)}) circuit complexity for the padded language. This is a limitation of that proof rule, **not** an upper bound on `SIZE(P_c(W)_M)` itself and not a theorem against arbitrary NP-level methods.

If `SIZE(W_n)≥η n sqrt(log_2 n)` for infinitely many n, then (a) supplies **only**

```
SIZE(P_c(W)_(2^(cn))) >= Ω(log M sqrt(log log M))
```

along the associated sparse padded lengths. The comparison is quantitative: this is sublinear in M, far below a superpolynomial lower bound.

**(c) Under P=NP the padded E^NP witness is in P.** More explicitly, suppose `W∈DTIME^{NP}(2^{a n})` for fixed a. Assume `P=NP`, and fix the resulting polynomial-time oracle decider with time at most `L^b+O(1)` on oracle queries of L bits. The original oracle machine makes at most `2^{a n}` queries, none longer than `2^{a n}`; replacing all calls on the **same deterministic realization** gives `T_W(n)≤2^{a(b+1)n+O(1)}`. Let `ρ=a(b+1)/c`. A fixed locally headed multitape machine for the padded language scans/authenticates the entire M-bit source, finds the final delimiter, checks `M=2^{cn}`, runs the above oracle-free decider on x and emits one bit. Conservative identical-run resource bounds are

```
T_pad(M)=O(M^3 + M^ρ),   S_peak,pad(M)=O(M + M^ρ)
```

on all words (invalid words reject), with constants depending only on the fixed machines and c. This proves `P_c(W)∈P⊆NP⊆P/poly` under P=NP, **not** `P≠NP`. Without the additional P=NP assumption, the direct argument does *not* establish that the padded `E^NP` language is even in NP.

## Precise implication ledger

`C1a` authenticated circuit bits → `C1b` parsimonious Tseitin wires → `C1c` all-input totalizer → `C1d` pinned low-first `encInput` → `C1e` pinned counting theorem (CONDITIONAL; upstream kernel evidence, no local replay) and standard physical simulation (PROVED/EXACT fixed-machine restricted) → `C1f` JMV binary oracle witness / higher-class circuit bound (CONDITIONAL and independent review OPEN). The proposed further arrow `C1f→NP superpolynomial` *via exponential padding and the simple restriction inequality* **FAILS** by Theorem C1g(b), independently of the authenticity of the earlier counting theorem. Any NP-level promotion needs a genuinely new nonpadding, nonrelativizing implication and cannot assume the hierarchy contradiction itself.

## Same-realization and four mandatory gates

**DISJ sanity: PASS restricted.** No inference from rank; DISJ has full static cut rank and a linear-size circuit. Horn, 2-SAT, affine/Gaussian, bounded treewidth, equality, products, autarkies, padding, selectors, unique solutions and compact shared shortcuts remain legal.

**Relativization: PASS for the scoped elementary padding calculation; OPEN for NP promotion.** A fully relativizing P-vs-NP separation is blocked. An actual NP-level theorem requires a specified nonrelativizing ingredient with algebrization/Natural Proofs audit.

**Simultaneous DTISP: PASS for the conditional padded deterministic upper execution in part (c), but NOT APPLICABLE to a forbidden FLMV pair.** The same process charges full M-bit validation, all oracle substitutions, access, buffers, output, and its single-run peak writable memory. No time-space impossibility or lower bound on unrestricted SAT is claimed.

**Configuration counting: PASS as a one-way upper-bound sanity check.** For total deterministic read-only-source physical machines, `T≤2^{O(S+log M)}`; this is not a work lower bound and cannot be applied to a randomized or quantum algorithm without a separate argument.

Historical /341 is FAIL as unrestricted UNSAT logical authority; /386 remains RESTRICTED. All unknown operations MAY; compact alternatives admissible.

## Reproduction and source status

This is a **symbolic proof** (parts a-c). No finite empirical tests, LaTeX compilation, independent Lean/lake/nanoda rebuild, `#print axioms` replay or local PNP preflight were performed. The container has no repository checkout or Lean/lake installation; git DNS access is unavailable. Exact repository sources, five handoffs, peer manuscript sections, issue #3 and active directives were read via the connected GitHub interface. Existing source evidence under TMR-1/057–058 is not claimed to have been reexecuted.

**ONE next load-bearing lemma (unchanged):** Independently rebuild pinned Lean v4.33.1 / Mathlib at the exact `eth` revision, run `#print axioms MainResults.mainTheorem` and `#print axioms MainResults.ethIsFalse`, then verify the proof-term and physical-machine interpretation. C1g has closed only the *padding-based NP target candidate*.

Primary sources:
1. Anthropic, `eth/MainResults.lean` and `eth/Solution.lean`, commit `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. https://github.com/anthropics/formal-math/tree/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth
2. Jahanjou, Miles, Viola, *Local Reductions*, ECCC TR13-099 rev. 3, April 4, 2014, Theorem 1, Corollary 2. https://eccc.weizmann.ac.il/report/2013/099/
3. TMR-1/056, /057 and /058, their GitHub blobs and TMR-5/054 address-domain counterexample on `j15marti/pnp/main`.

Independent mathematical review: OPEN. Proof status: C1g PROVED/EXACT RESTRICTED; unrestricted P versus NP OPEN.
