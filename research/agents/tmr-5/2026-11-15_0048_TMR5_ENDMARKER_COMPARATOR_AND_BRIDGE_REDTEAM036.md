# TMR-5/036 | COMPARATOR075: explicit fused-halt comparator, endmarker convention attack, and worst-case-bridge red team

**2026-11-15 00:48 PST | Independent Proof Red Team | America/Los_Angeles**

**Status summary.** (i) TMR-4/040 ENDMARKER074-A survives at its stated scope (PASS/RESTRICTED). (ii) The fused (1,1) halt row is *physically reachable*: an explicit finite transition table realizes it, and this is now COMPUTATIONAL, with m=3..12 executed. (iii) NEW PROVED/EXACT: the "+1" endmarker unit depends entirely on the total-language malformed-input convention. Under the promise convention, a correct comparator accepts in exactly N steps without ever inspecting the endmarker. (iv) NEW red-team lemma on the scheduled worst-case objective. For every fixed system R with a known unconditional superpolynomial lower bound (e.g. Resolution), the bridge SAT∈P ⇒ W̄_R(N)≤poly(N) is *logically equivalent* to SAT∉P. It is a reformulation, not a weaker target. That lemma uses only KNOWN THEOREMS. **P versus NP remains OPEN.**

## 1. Candidate and falsifiers fixed before work

Candidate: build the hardcoded comparator that TMR-4/040 §5 asserted, executing its transition table rather than describing it. Then attack whether the fused endmarker-scan-plus-accept row, and the extra unit it carries, are robust facts about SAT computation.

Falsifiers:
- (F1) No finite deterministic table attains T=N+1 with a single (1,1) final row.
- (F2) The comparator is incorrect on some off-target input, so it is not a total correct decider for fixed m.
- (F3) The extra unit survives a change of input convention.
- (F4) The scheduled bridge is strictly weaker than P≠NP for the systems in which the corpus has hard families.

Results: F1 and F2 do not occur. F3 occurs: the unit does not survive. F4 occurs for every R with known lower bounds.

## 2. Exact machine and executed comparator

Tape: `< x_0 ... x_{N-1} >` with one read-only head starting on x_0. The model is scan-before-move with unit cost per transition, and halting is a transition that consumes the scan of the current cell. This is exactly the TMR-4/040 convention. The source family is F_m^± from the TMR-3/039 encoder, ported line by line into Python. The port reproduces N_m=(24m+1)(b_m+1)+8m+1 and the final-bit pair for every m tested.

Program A_m (fixed m), with explicit states ('C',i) for i=0..N plus REW:
- In ('C',i) with i<N, on scanning target[i], go to ('C',i+1) and move right.
- In ('C',N), on scanning `>`, HALT-ACCEPT. This is the fused row.
- On any mismatch, rewind to `<` and enter a total fallback: the strict TMR-3 grammar parser plus an independent complete DPLL. The fallback's physical cost is **not** modelled, so it is ABSTRACT. Only its label is used. This is legitimate because TMR-4's claim concerns only the match path, and any total correct decider may serve as the fallback.

The table has (N+1)·3+3 rows (1,176 at m=3; 6,366 at m=12).

Executed results (`experiments/tmr/tmr5_comparator075.py`; chunked one m per invocation, each run under 6 s):

| m | N | T on F_m^+ (total conv.) | final row | T on F_m^+ (promise conv.) |
|---:|---:|---:|---|---:|
| 3 | 390 | 391 | (1,1) | 390 |
| 6 | 919 | 920 | (1,1) | 919 |
| 9 | 1375 | 1376 | (1,1) | 1375 |
| 12 | 2120 | 2121 | (1,1) | 2120 |

All m=3..12 give the same pattern. Every earlier row is (1,0). The unit-unit tariff λ_int+λ_mach=2 is violated at exactly one step, the fused final step. This independently confirms TMR-4's cone λ_int+λ_mach≤1 and its claim that unit-unit weighting FAILS.

Hostile battery (11,823 inputs in total): every single-bit flip of F_m^+, F_m^-, the extensions x0, x1 and x00, truncations, the empty string, "0", and a left shift. A_m agreed with the independent reference on every input and left the match path on every x≠F_m^+. Of the flips, 9,952 remain valid proper 3-CNF; 9,942 of them are SAT, the 10 UNSAT cases being exactly F_m^- (one per m). Most of the source neighbourhood is therefore *satisfiable*. The UNSAT witness is isolated, which is consistent with the cheap-recognizer controls.

Total: 23,806 assertions, zero failures. Raw data: `results/raw/tmr/2026-11-15_0048_TMR5_COMPARATOR075_RAW.json`.

## 3. NEW PROVED/EXACT: the endmarker unit is a convention artifact

**Proposition C075-A.** Fix m, and let A'_m be A_m with the single change that ('C',N−1), on scanning target[N−1], halts and accepts.
1. A'_m is correct on every *valid* encoding. The grammar is prefix-free, so the only valid string with prefix F_m^+ is F_m^+ itself.
2. A'_m accepts F_m^+ in exactly N transitions and never inspects cell N.
3. A'_m errs exactly on the strict extensions F_m^+·w with w≠ε. These are malformed, so their Boolean SAT label is NO only under the total convention.

*Proof.* The prefix-free property follows from the unary-header parser: the header fixes the total length. On a valid x≠F_m^+, there is a first mismatch index <N. The machine therefore falls back before the halting state and inherits the fallback's correctness. On F_m^+·w the run is identical to the run on F_m^+ through step N. QED.

Executed: A'_m had T=N and frontier r=N−1 on F_m^+ for every m tested. It was wrong on exactly the 3 extension controls per m and correct on every other hostile input.

**Consequence.** ENDMARKER074-A's bound T≥N+1 is correct, but its margin over TMR-3/039's T≥N comes only from requiring correctness on malformed suffixes. The same margin disappears in any of three variants: if the halt-state entry is not charged as a transition, if inputs come with a length header given for free, or if the problem is a promise problem. No variant changes the asymptotics. The physical-ingress coordinate carries at most N+1 units, which by TMR5-O1 (/001) is the maximum of any observation-only potential. This ingress line is therefore saturated. No further work on endmarker, last-bit or frontier tariffs can raise the initial potential above linear.

## 4. Red team on the scheduled worst-case objective W̄_R(N)

The scheduled prompt asks for the "weakest sufficient bridge" SAT∈P ⇒ W̄_R(N)≤poly(N), where W̄_R(N) = max over UNSAT F with |F|≤N of min over R-refutations π of cost_R(π).

**(a) The free-strategy principle is sound only inside a fixed R.** Minimizing over derivations π for a fixed proof system R is legitimate, and W̄_R is then exactly R's proof-complexity function in the Cook–Reckhow (1979) sense. Charging no search cost is standard and correct.

If the minimization instead ranges over *algorithms* per instance, it collapses. Section 2 exhibits it: for each fixed valid F, the hardcoded comparator gives min_A T_A(F) ≤ N+1, and the same table with a reject halt does this for UNSAT F as well. So max over F of min over A of T_A(F) ≤ N+1 under the total convention. This is exactly the order-of-quantifiers trap that TMR-4/040 §5 notes for one source. Any machine-side version of the objective must keep the quantifier order ∃A ∀F, never ∀F ∃A.

**(b) Lemma B036 (reformulation; status: follows from KNOWN THEOREMS).** Let R be any fixed proof system for which W̄_R(N) ≥ N^{ω(1)} is unconditionally known. Then

  [SAT∈P ⇒ W̄_R(N) ≤ poly(N)]  ⟺  SAT∉P.

*Proof.* The right-hand side of the implication is unconditionally false, so the implication is true exactly when its premise is false. QED.

Instances: Resolution, by Haken (1985) and the Ben-Sasson–Wigderson (2001) expander Tseitin bounds already used in TMR-1/036. The same holds for every system with a known superpolynomial lower bound, including bounded-depth Frege, Polynomial Calculus and Cutting Planes.

For such R, "proving the bridge" *is* proving P≠NP. It is a ledger "equivalent of P≠NP" row, not a weaker target. TMR-1/036 already falsified the *pointwise* machine-to-Resolution simulation. Lemma B036 adds that the *conditional* bridge is no easier.

**(c) The remaining option is a strong R, and there the bridge is not the obstacle.**
- If the bridge's R may depend on the hypothetical algorithm, it is trivial and useless. Given a poly-time SAT decider A, the system "proof of F = 1^{p(|F|)}, verifier runs A" is p-bounded. Equally, by Krajíček–Pudlák (1989), E=NE gives a p-optimal system, and P=NP implies E=NE by padding.
- For a *fixed explicit* R_T (Frege or Extended Resolution augmented with T-proofs, as in the Krajíček–Pudlák P_T construction), the bridge holds whenever T proves the hypothetical algorithm correct. A run of length t on F translates into a poly(t)-size R_T proof.

So for strong R the bridge is cheap, modulo T-provable correctness. The hard part is the superpolynomial lower bound for that strong R, which is open even for Frege. The two requirements pull in opposite directions:
- lower bounds are known only for weak R, and there the bridge is ⟺ P≠NP;
- the bridge is easy only for strong R, and there no lower-bound technique exists.

This is the classical Cook-program tension. It is recorded as a structural barrier on this objective, not a new theorem.

**Transfer classification.** The proof-complexity material in (b) and (c) is an EXACT OBJECT/THEOREM TRANSFER. The PQ ledger items are FAILED TRANSFERS for this ingress question: there is no algebraic structure to exploit.

## 5. Corpus, duplication and contradiction audit

**CORPUS REVIEWED:** fusion-Lipschitz directive; TMR-4/040 (full), with its JS and raw data cited; TMR-3/039 (full) and its encoder `experiments/tmr/tmr3_lastsat073.js`, which this run ports; TMR-1/036 (bridge distortion); the codex 2026-11-11 SAT-polynomial audit and transfer-recovery reports, which define W_R and the clocked/p-optimal system; the TMR-5 handoff history including /001 TMR5-O1; and AGENTS.md. Root proof1/proof2 and full main.tex were **not** re-read in full this run (local checkout only, time-boxed). No tracker or main.tex edit is made.

**DUPLICATION:**
- The fused-row cone duplicates TMR-4/040 and is confirmed, not new.
- The trivial p-bounded system for a known algorithm is in codex /1331 §"p-optimal".
- New here: the executed transition table and hostile battery, Proposition C075-A, and Lemma B036's explicit "bridge ⟺ P≠NP for lower-bounded R" classification together with the strong-R/weak-R tension applied to the scheduled objective.

**CONTRADICTIONS:** none found. TMR-4's "per-source optimum exactly N+1" is consistent with this run.

**STALE OR OVERSTATED CLAIMS FOUND:**
- Any reading of ENDMARKER074's +1 as convention-independent is overstated. TMR-4 did list "free endmarker lookahead" as model-changing, but it did not note that the promise convention removes the endmarker inspection while keeping correctness on all valid encodings.

**ADOPTED / REJECTED / RETIRED:**
- Adopted: TMR-4/040 at its scope.
- Retired: further ingress or frontier tariffs as a route to superlinear potential, since these are saturated at ≤N+1.
- Retired: "Weakest sufficient bridge" for Resolution-strength R as a target distinct from P≠NP.

**Limits:** the fallback cost is abstract; one input head; no LaTeX compile; no native multitape compiler; literature summaries checked via secondary sources (arXiv 2304.14702 and the Köbler–Messner–Torán citation chain) rather than the 1989 original.

## 6. References

- S. Cook, R. Reckhow, *The relative efficiency of propositional proof systems*, JSL 44(1) 1979, doi:10.2307/2273702.
- J. Krajíček, P. Pudlák, *Propositional proof systems, the consistency of first order theories and the complexity of computations*, JSL 54(3) 1989, 1063–1079, doi:10.2307/2274765.
- J. Köbler, J. Messner, J. Torán, *Optimal proof systems imply complete sets for promise classes*, Inf. Comput. 184 (2003).
- A. Haken, *The intractability of resolution*, TCS 39 (1985).
- E. Ben-Sasson, A. Wigderson, JACM 48(2) 2001, doi:10.1145/375827.375835.
- Secondary survey of the KP/KMT conditions: https://arxiv.org/pdf/2304.14702 .

## 7. Next targets

- TMR-1: add Lemma B036 to the transfer ledger, and pick a candidate R for which neither a lower bound nor a ⟺P≠NP collapse is known (Res(lin)? bounded-depth Frege with parity gates?).
- TMR-2: supply a family hard for a *strong* system, or show the hostile cheap paths defeat it.
- TMR-4: stop refining ingress, and combine an observer with a nonlocal fusion-safe obstruction.
- TMR-5 next: attack whichever nonlinear initial potential appears first.

**TRACKERS: not fully re-read this run; NO MATERIAL CHANGE claimed.** Root main.tex unchanged. Schedules unchanged. **P versus NP remains OPEN.**

END_OF_REPORT::TMR5::036::2026-11-15_0048_PST
