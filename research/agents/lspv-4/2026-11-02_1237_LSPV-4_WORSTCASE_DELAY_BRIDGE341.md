# LSPV-4: WORSTCASE-DELAY-BRIDGE341
**November 2, 2026, 12:37 PST. Status: PROVED/EXACT theorem using Haken's KNOWN resolution lower bound; finite checks COMPUTATIONAL. P versus NP OPEN.**

## Fixed system, target, and one exact falsifier
We use general encoded CNF-SAT and one fixed effective refutationally complete calculus R_res: ordinary DAG resolution, zero-cost explicitly named source clauses, unit cost per *distinct* binary-pivot resolvent, no truth oracle or tailored answer axiom. Free best-derivation choice is granted in W_R(F); optimizer discovery is not charged. Physical source reads, clause records, parent access, proof verification and peak space are different quantities.

Write W_R(F)=minimum number of derived nodes in any sound shared resolution-DAG refutation of UNSAT F; Wbar_R(N)=maximum W_R(F) for valid UNSAT F encoded with at most N **bits**. Let T_A^wc(N)=maximum runtime over **all binary inputs** of length at most N, including malformed inputs. B1 is individual F domination by polynomial(|F|+T_A(F)); B2 uses polynomial(N+T_A^wc(N)); B3 is SAT in P implies polynomial Wbar_R for the SAME fixed R. Universal B2 and B3 are OPEN.

**Theorem (B2_A can hold while B1_A fails).** A fixed uniform total correct SAT decider A_slow can satisfy its *individual* B2 on every N, yet fail its *individual* B1 on an infinite family. Proof:

1. Every non-tautological clause over n appearing variables has one of 3 states for each variable (absent/positive/negative). Exhaustive resolution closure proves every UNSAT CNF, reusing clauses, with at most 3^n distinct derived clauses. Since n<=N bits, **Wbar_R_res(N)<=3^N**.
2. Define A_slow as follows. Recognize the **exact canonical** standard pigeonhole PHP(k+1,k) encoding in polynomial time and return UNSAT on it. On every other input x of length N, perform a genuine 2^N-iteration dummy counter loop, then parse and solve valid CNF by exhaustive assignments; reject malformed inputs. This one fixed algorithm handles SAT, UNSAT and malformed strings. The PHP recognizer is a polynomial syntax check, not a semantic SAT oracle.
3. The malformed input 1^N always takes at least 2^N steps before correct rejection, so T_A^wc(N)>=2^N. Therefore Wbar_R(N)<=3^N<=4^N<=(N+T_A^wc(N))^2. **B2 for this individual A is PROVED**, with p(z)=z^2, not universal B2.
4. Haken's 1985 theorem gives DAG-resolution PHP_k refutation size at least 2^{Omega(k)}. The canonical PHP input length is N_k=O(k^3 log(k+1)), yet A_slow recognizes and rejects PHP_k in poly(N_k) time. Hence no polynomial p dominates W_R(PHP_k) by p(N_k+T_A(PHP_k)): **individual B1 fails**.

This is a worst-case/pointwise quantifier firewall. It does not refute universal B2 or B3. For resolution, because Haken already proves superpolynomial Wbar_R, the material implication B3 for this R is classically equivalent to SAT notin P; merely restating B3 is not a proof. Haken's resolution result does NOT imply a mixed calculus's hardness: LSPV-2 MIXED_TSEITIN_MIN_DAG341 proves exact linear 4h-1 refutations for odd Tseitin on bridgeless cubic graphs under its richer binary-premise XOR calculus.

## Finite independently verified controls
A pure Python producer generated the standard PHP_1,PHP_2,PHP_3 sources. A no-import Node.js checker independently regenerated each source, exhaustively evaluated both original UNSAT and one-positive-literal-flipped SAT neighbors, checked every source clause indispensable, and verified every pivot and parent in a complete resolution DAG. Results:
- PHP_1: 2 variables, 3 clauses, 0 original models, 1 SAT-neighbor model, exhibited 2-node refutation, **exact optimum 2** by indispensable-source binary-arity bound.
- PHP_2: 6 variables, 9 clauses, 0/2 models, exhibited 10-node refutation (upper bound, not optimum).
- PHP_3: 12 variables, 22 clauses, 0/6 models, exhibited 43-node refutation (upper bound, not optimum).
- Eight malformed fixtures rejected; corrupted final-clause proof rejected; independent Node checker passed **8,651 assertion groups**.

For **one declared dense certificate encoding** with m source nodes and q inferences, b=ceil(log2(m+q+1)) parent bits, b_x=ceil(log2(n+2)) pivot bits, and 2n bits per full signed clause, each derived record uses 2n+2b+b_x+2 bits. Exact declared proof streams for the three finite controls are 28/270/1892 bits; retaining signed clauses alone requires 2n(m+q) bits. These are not minimum evidence lengths. A checker must actually read sources/parents, verify signed resolution and bit equality, index its tapes and retain or recompute DAG nodes. A unit logical node is not a universal native-machine step lower bound.

The displayed A_slow's real delay requires an N-bit local counter, so the all-phase local-space exponent rho is at least 1 for that implementation. The corrected materialized-child envelope is s'<=max{rho,eta,lambda,lambda*s}; freeing the N-bit counter before future work does NOT lower rho to 1/2. There is no FLMV transfer.

**Falsifiers:** (F1) DELAY makes single-A B2 vacuous while B1 fails (proved); (F2) remove DELAY and audit an all-input optimized A (open); (F3) change resolution to mixed XOR and test proof shortcut (resolution hardness does not transfer); (F4) replace unit-node q by explicit native proof verification, with dense versus compact records (model-dependent).

## Provenance and references
Read first the 2026-11-02 12:04 five-role worst-case handoff; then issue #3, LSPV-2 mixed-Tseitin-341, LSPV-5 trace-correctness-294, AGENTS.md, CODEX.md, pnp-research skill. Project GitHub queries: 'WORST_CASE_MINIMUM_DERIVATION', 'slowdown Wbar', 'worst case delay B2 PHP' (no direct duplicate found); github.com/openai search 'proof complexity resolution derivation DAG SAT' found no directly relevant code (absence proves nothing). Primary sources: Haken, *The Intractability of Resolution*, Theor. Comp. Sci. 39 (1985), 297–308, doi:10.1016/0304-3975(85)90144-6; Cook/Reckhow, *Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36–50, doi:10.2307/2273702; Ben-Sasson/Wigderson, *Short Proofs Are Narrow*, JACM 48 (2001), 149–169.

Full standalone producer, independent verifier, raw JSON and SHA-256 manifest were prepared in the reproducibility archive shared with the user. Root main.tex was not modified without authenticated current nonempty full-blob reconciliation. Task IDs, schedule and enabled states unchanged. The next bridge is B3 for a PRESELECTED representation-inclusive mixed calculus R; neither such a bridge nor a superpolynomial mixed-calculus Wbar lower bound is established. **P versus NP OPEN.**
