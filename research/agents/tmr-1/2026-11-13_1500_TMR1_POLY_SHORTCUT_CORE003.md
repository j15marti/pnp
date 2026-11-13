# TMR-1 / 003: uniform fast-path firewall against recognizable hard UNSAT families

**Date:** 2026-11-13 approximately 15:00 PST (America/Los_Angeles).  
**Role:** TMR-1, Machine Model Lead, under the authoritative five-TMR replacement directive.  
**Status:** CANDIDATE symbolic theorem pending TMR-5 independent review; finite tests COMPUTATIONAL; unrestricted superpolynomial SAT lower bound OPEN; P versus NP OPEN.

## 1. Target, model, and falsifiers

**Target.** Determine whether an explicit, easily generated infinite family of UNSAT 3-CNFs with growing primal treewidth can independently establish hard inputs for **every** fixed correct deterministic 3-SAT decider. The answer is NO if that family is polynomial-time recognizable and its labels are efficiently computable on the recognized promise.

Falsifiers checked: (i) the fast path accidentally rejects a satisfiable instance; (ii) the syntactic gadget recognition requires exponential subgraph isomorphism; (iii) its correctness depends on a particular variable naming, literal order or clause order; (iv) clause removal leaves the core UNSAT; (v) the wrapper is confused with a general polynomial SAT algorithm; (vi) high treewidth or input size is silently treated as a runtime lower bound.

**Model.** One fixed, total, deterministic, finite-alphabet, fixed-multitape program acts on all binary lengths. There is one read-only sequential input head, finitely many work tapes, counted head transitions and visited writable cells. Parsing, searching, temporary hash/sorted records, counter and address bits, fallback enumeration and output all count. Indexed implementations, if used, require charged polynomial multitape simulation. The explicit strict-proper 3-CNF source format has header `1^N 0 1^M 0`, each of the 3M literals then represented as a sign bit and `w=max(1,ceil(log2 N))` variable-ID bits. Thus

$$
L=N+M+2+3M(1+w).
$$

All invalid source strings are rejected; every valid satisfiable source is accepted. The fallback is an ordinary exhaustive SAT decider, not an oracle or an uncharged certificate. No fixed-polynomial runtime is claimed off the designated promise.

## 2. Polynomial shortcut theorem

**Theorem TMR1-PF3, symbolic proof, CANDIDATE pending review.** Let `D` be any total decidable binary decision language (in particular, fixed-encoded 3-SAT). Suppose a set `K` is recognizable in deterministic polynomial time and there is a deterministic polynomial-time algorithm giving the correct `D` label for **every x in K**. Then there is **one fixed, total, correct deterministic decider** `B_K` for `D` and a fixed polynomial `p_K` such that

$$
\forall x\in K,\qquad T_{B_K}(x)\le p_K(|x|).
$$

More generally, a polynomial-time total *partial classifier* `Q(x) in {YES, NO, UNKNOWN}` whose decisive answers are always sound can be prepended to any total `D` decider. Its non-UNKNOWN domain is uniformly easy for the resulting single total decider.

**Proof.** Fix a polynomial-time recognizer `R_K`, a polynomial-time promise labeler `C_K`, and a total correct decidable fallback `A_0`. Hardwire these **three finite programs once**, independent of the input length. On input `x`, compute `R_K(x)`. If positive, run `C_K(x)` and return its correct answer. Otherwise run `A_0(x)` to completion. All input, work tapes, simulation and final output are paid. The program is total and correct on both branches, and for every `x in K` it finishes within a polynomial depending on `R_K, C_K` but not on `x` or its length. A standard polynomially charged fixed-multitape simulation preserves the claim. This constructs a competing algorithm, so a claimed superpolynomial lower bound on **every correct algorithm on this same K** is false. QED at the specified scope.

**Corollary.** Any polynomial-time recognizable infinite family of UNSAT 3-CNF instances admits a correct uniform complete SAT decider that rejects **every family member** in polynomial time. Consequently a universal lower-bound candidate of form

$$
\forall A\ \forall k,C,L_0\ \exists F\in K:\ |F|\ge L_0
\ \wedge\ T_A(F)>C(|F|+1)^k
$$

cannot hold for such a `K`. A proof may still use a family with hard-to-recognize membership, or a fixed family on which its SAT labels are not polynomially decidable. An algorithm-dependent hard-input selection is also admissible. These escape routes remain OPEN.

This is a routine but often overlooked **complexity-core firewall**, not an unconditional separation or a new claim of priority. Lynch's 1975 complexity-core result is conditional on the language not being in P; it produces an infinite recursive core, not a polynomial-time recognized monochromatic family. It therefore does **not** contradict this shortcut theorem.

## 3. A connected, strict 3-CNF, unbounded-treewidth falsifier

For every `n>=3`, use original variables `x_1,...,x_n` and four auxiliaries `u,v,p,q`. Form `H_n` from **all positive triples** `(x_i or x_j or x_k)` for distinct `i<j<k`. Add these eight proper 3-literal clauses:

$$
G_+=\bigwedge_{s,t\in\{-1,+1\}}(x_1\lor s u\lor t v),
\qquad
G_-=\bigwedge_{s,t\in\{-1,+1\}}(\neg x_1\lor s p\lor t q).
$$

Let `F_n=H_n AND G_+ AND G_-`.

**UNSAT.** If `x_1=0`, the four `G_+` clauses demand all four sign combinations over `u,v`; no assignment can satisfy all. Thus `G_+` forces `x_1=1`. Similarly `G_-` forces `x_1=0`. The pair contradicts. `H_n` cannot restore satisfiability.

**High primal width and connectivity.** Every two distinct original variables share a triple in `H_n`, so the primal graph contains a clique `K_n`, with treewidth at least `n-1`. All four auxiliaries are adjacent to `x_1` via the gadgets, so the primal graph is connected. The formulas are strict and proper: all clauses have three different variables, no within-clause tautologies, no unit clauses. `N=n+4, M=binom(n,3)+8`, and `L=Theta(n^3 log n)`.

**Polynomial recognizer.** Parse the actual signed triples; for a pivot variable `z` test whether some pair `u,v` realizes all four clauses `(z or +/-u or +/-v)` and whether some (possibly different) pair realizes all four `(not z or +/-p or +/-q)`. If both are present, reject as UNSAT immediately. A canonical sorted-clause set and enumeration of `O(N^3)` pivot/pair candidates makes this polynomial-time in `L`, without trusting a supplied decomposition or a hidden oracle. The test is invariant under variable renaming, clause order, within-clause literal order, and global sign flips. It never outputs false UNSAT: the eight certified clauses logically contradict.

**Deletion control.** Deleting **any one** of the eight contradictory clauses from `F_n` makes the resulting formula satisfiable. When a positive forcing clause is removed, take `x_1=0`, set `u,v` to falsify only that missing clause, and set `x_2,...,x_n=1`. For deletion from the negative quartet, take `x_1=1`, choose `p,q` similarly and set remaining original variables true. Thus the small core is not an accidental tautology or malformed source.

**Scope:** Connected high-primal-treewidth UNSAT instances are an effective adversarial control against **structural-width alone** as a universal time lower bound. This does not prove bounded-width decomposition useless, nor show that an arbitrary difficult-looking 3-SAT formula is easy, nor exclude some other all-input bottleneck.

## 4. Exact machine/quantifier firewall and dependency DAG

The project's unrestricted target remains

$$
\forall A\in\mathrm{Dec}_{3SAT}\ \forall k\ge1\ \forall C>0\ \forall L_0\ 
\exists F\text{ valid},\quad |F|\ge L_0\ \land\ 
T_A(F)>C(|F|+1)^k.
$$

TMR1-PF3 makes the following candidate route **FALSIFIED/RESTRICTED**:

`explicit P-recognizable all-UNSAT high-width family` -> `every complete SAT decider requires superpolynomial time on that family`.

It does **not** disprove the unrestricted target. A viable next arrow must quantify over all correct fixed programs and show a *computed* globally decisive distinction that cannot be bypassed by a polynomial-time recognizable shortcut, arbitrary nonuniform-**free** representation, algebraic elimination, streaming, memory caching or paid recomputation. It may select instances dependent on `A,k,C,L0`.

TMR-2: seek a necessity measure beyond already-readable bits and recognizable shortcut cores. TMR-3: test any same-machine tradeoff against the one fixed fast-path wrapper, including its fallback and parsing costs. TMR-4: abstract actual fast-path transitions as real legal paths, with no may-edge deletion. TMR-5: independently verify the syntactic eight-clause implication, polynomial recognizer, and the quantifier-level impossibility statement.

The earlier TMR-1/002 conversion `S<=b(T+1)` still only converts suitably strong joint lower bounds; TMR-2/002's easy one-sweep equality family and TMR-4/003's speculative final-bit algorithm remain valid temporal falsifiers at their respective scopes. Nothing here supplies a superpolynomial lower bound.

## 5. Reproducibility, controls, and publication

**Executed:** One self-contained deterministic JavaScript V8 run, 273 assertion groups, zero failures. Exhaustive brute-force semantic checks for `n=3..8`, 30 renamed/permuted/sign-flipped UNSAT controls, 48 single-gadget-clause deletion SAT controls, plus complete strict binary serialization/parser checks. Additional large `n=12,20,35,50` accepted original encodings had `M=228,1148,6553,19608`, reaching `L=431432` bits and clique-width lower bound 49. Exhaustive assignment enumeration is used **only as an independent small test**, never as a lower-bound premise. The source code uses a deliberately bounded enumerator for finite checks; the mathematically defined complete fallback is unbounded and total.

Executable source: `experiments/tmr/tmr1_poly_shortcut_core003.cjs`, verified blob `93dd19216e51d8da27105945f972996aee585981`.  
Immutable raw: `results/raw/tmr/2026-11-13_1500_TMR1_SHORTCUT_CORE003_RAW.json`, verified blob `8f4ca4975e2a1d3aa725b2570fedb3dc7ea8d111`.

All 273 checks were performed in the tool's V8 runtime by invoking the same named functions embedded in the published script. **Not executed:** native Node CLI, a physical Turing-machine simulator, root LaTeX compilation, repository-wide preflight, or a full polynomial-time recognizer implemented as a physical multitape TM. The latter is a symbolic construction from a polynomial finite parser/enumeration.

Corpus actually reviewed: latest authoritative replacement directive FIRST; full root proof1.txt; recovered full nonempty 1,051,196-character proof2.txt using original Git blob SHA 930c5eeddafce656717f28055a7a9a755f44737c; root main.tex 2,485,460 chars recovered by original blob, including all five owner markers; issue #3 latest TMR-2/002, TMR-3/002, TMR-4/003; AGENTS.md, CODEX.md, pnp-research skill; all five TMR latest handoffs; original TMR-3/002 and TMR-4/003 reports; historical project restricted original-source and expander decomposition failures (P1-S3 and P2-D1 reports as referenced by verified trackers). No old LSPV schedule or proof-system obligation was revived.

**Tracker/main decision:** No P1/P2 all-input proof node changed; **TRACKERS REVIEWED; NO MATERIAL CHANGE**. Root main.tex not edited, because this is a new symbolic claim pending TMR-5 review; new TMR-1 ownership region exists but old history is preserved. All prior claims retain their exact status. P versus NP OPEN.

## 6. Primary literature and historical scope

[1] N. Lynch, "On Reducibility to Complex or Sparse Sets," *Journal of the ACM* 22(3), 1975, 341-345. Primary author-hosted PDF, section 3, Lemma 1: https://groups.csail.mit.edu/tds/papers/Lynch/jacm75.pdf . Lynch's existence theorem is conditioned on the language being outside P; it does not assert a polynomial-time recognizable easy family is inherently hard.

[2] L. Fortnow, R. Lipton, D. van Melkebeek and A. Viglas, "Time-Space Lower Bounds for Satisfiability," *JACM* 52(6), 2005, 835-865, https://doi.org/10.1145/1101821.1101822 . SAT time-space bounds under exact restricted hypotheses, not arbitrary-space separation.

[3] TMR-1/001 and /002, TMR-2/002, TMR-3/002, TMR-4/003, TMR-5/001, and root proof1.txt/proof2.txt are the project-specific prior corpus. The easy-core shortcut is elementary; no originality is asserted.

**One next target:** test whether a proposed machine-global processing potential admits a fast-path wrapper on a sound, polynomial-time recognized subset, or whether its proof genuinely rules out all such shortcuts while including every real computation.
