# TMR-4/023: exact cubic-moment streaming congruence and a minimal SAT/UNSAT erasure falsifier

**Date:** November 14, 2026, 08:36 PST (America/Los_Angeles). **Role:** TMR-4, new Cost-Sound Abstraction agent. **Project:** j15marti/pnp, main after merge. **New result:** TMR4-MC23, CANDIDATE/RESTRICTED, pending independent TMR-2/TMR-5 review. **Executed evidence:** COMPUTATIONAL. **P versus NP:** OPEN.

## 1. One sharply scoped new result

The latest TMR-2/022 establishes a signed Walsh expansion of the number of violated proper 3-CNF clauses and a polynomial recognizer for the zero-nonconstant-moment case. The user-directed Claude/TMR synthesis asks for an actual source-bound compositional summary, rather than another sensitivity parameter. This report answers the following **restricted** question exactly: can an ordered proper 3-CNF clause stream be reduced to a polynomial-length canonical state which is sufficient for **all future clause continuations and the final SAT/UNSAT label**?

**Yes, if all degree-three signed moments are retained. No, if only degrees zero through two are retained.** The failure has a minimal eight-clause opposite-label witness using three variables. The exact repair is a polynomially constructible canonical sparse moment table. The reduction is a semantic congruence for a **specified clause-streaming compiler**, not a program-independent abstraction of arbitrary 3-SAT Turing-machine executions and not a polynomial-time SAT decision algorithm.

The original prior contribution is TMR-2/022's exact Walsh identity and spectral-flat recognizer. The new contribution here is (i) its all-continuations congruence formulation, (ii) the explicit **minimum-size** opposite-label degree-two quotient collision, (iii) a physically chargeable canonical streaming compiler and its limited all-transition replay guarantee, and (iv) the unrestricted-machine failure/repair boundary.

## 2. Source model, full encoding, and coefficient definition

Fix a finite total deterministic multitape machine over a finite alphabet, a local two-way read-only input head, and finitely many ordinary locally moving writable work heads. Time counts every transition. Space counts all visited writable cells, indices, temporary records, buffers, sorting scratch and output. A standard explicit binary encoding contains the variable identifiers, three distinct identifiers in each clause, their literal signs, clause delimiters and headers; let **L denote all input bits**, not three times the clause count. There are m occurrences. The paper-level sign-stream cube with only three fixed identifiers has a shorter special encoding used solely for the minimal witness.

Each proper clause C has distinct variable IDs V(C) of cardinality three. Let b_C(v) be the Boolean bit that makes the literal on v **false**, and put eta_C(v)=(-1)^{b_C(v)}. Write x_v=(-1)^{a_v} for a complete assignment a. Define, including the clause count separately,

$$
M_F(S)=\sum_{\substack{C\in F\\S\subseteq V(C)}}\prod_{v\in S}\eta_C(v)
\qquad(1\le |S|\le3).
$$

All these integer moments are bounded in magnitude by m. The complete summary is H_3(F)=(m,{M_F(S)}_{1<=|S|<=3}), with zero entries omitted. Its truncation H_2 retains only |S|<=2. For fixed variable-ID universe both include the total number of processed occurrences.

The elementary per-clause identity is

$$
8\mathbf{1}[C(a)=0]=\prod_{v\in V(C)}(1+\eta_C(v)x_v).
$$

Expanding and summing clauses gives, **for every Boolean assignment**,

$$
8v_F(a)=m+\sum_{1\le |S|\le3}M_F(S)\prod_{v\in S}x_v.
\tag{MC23-1}
$$

Thus H_3 determines the entire violated-clause function, not merely the one-bit SAT label.

## 3. Complete continuation-congruence theorem

**Theorem MC23-A (restricted exact factor).** For any two proper 3-CNF clause-occurrence sequences P and Q on the same declared variable universe, if H_3(P)=H_3(Q), then for every proper suffix R on that universe and every assignment a,

$$
v_{P\mathbin{\|}R}(a)=v_{Q\mathbin{\|}R}(a).
\tag{MC23-2}
$$

Consequently, the two completed formulas have exactly the same satisfying assignments, SAT/UNSAT label, model count, and minimum violated-clause count. The result holds for arbitrary overlaps, repeated clauses, reordered clauses, Horn and XOR patterns, and syntactic sharing of variables.

**Proof.** Every clause makes precisely the same additive contribution (1,seven signed moments) to H_3 regardless of what clauses preceded it. Hence H_3(P||R)=H_3(P)+H_3(R)=H_3(Q)+H_3(R)=H_3(Q||R). Apply MC23-1 pointwise to every a. The SAT condition is v(a)=0 for at least one a, so the SAT/UNSAT statement follows. This proof establishes a congruence of the abstract **append-clause** semantics. It does NOT assert that an arbitrary SAT machine computes H_3 or ignores the original prefix.

The summary has at most 7m nonzero signed contributions before merging. Each key contains at most three original variable identifiers; each counter needs O(log(m+1)) bits. A deterministic fixed finite multitape compiler can read the explicit source, emit these contributions to a writable tape, sort them by binary key with a standard charged merge-sort or comparison method, add equal keys, and write a canonical sorted table. Every source read, key copy, comparison, counter update and temporary buffer costs real steps and writable space. The number of intermediate records and their total bit length are polynomial in L. In particular O(L^2) bits of work are sufficient by storing at most 7m records with complete ID strings and O(log(m+1))-bit signed coefficients (m<=O(L)); any chosen straightforward multitape sort gives polynomial time. No unit-cost unbounded integers or free lookup construction is used.

The full table is a **polynomial-length exact semantic representation**; deciding whether its polynomial is zero at some Boolean point still requires solving the same satisfiability problem. Generating a compact expression is not a charged minimization or a separation.

## 4. Exact minimal degree-two failure and repair

Let U be the eight-clause three-variable formula containing exactly one clause C_s falsified at each assignment signature s in {0,1}^3. Then

$$
v_U(a)=1\quad\text{for every }a,\qquad U\text{ is UNSAT}.
$$

Let V contain two copies of each clause C_s for s of even parity, namely s in {000,011,101,110}, and no other clauses. Then

$$
v_V(a)=1+\chi_{\{1,2,3\}}(a),
\quad
\chi_{\{1,2,3\}}(a)=(-1)^{a_1+a_2+a_3}.
$$

Thus V has four satisfying assignments (the four odd-parity assignments) and U has none. Yet the two source streams have the same eight-clause count and

$$
H_2(U)=H_2(V)=(m=8,\ M(S)=0\text{ for }1\le|S|\le2).
$$

This follows because the signed parity-even four-point subset has vanishing Walsh coefficients of degrees one and two. At degree three they differ:

$$
M_U(\{1,2,3\})=0,\qquad
M_V(\{1,2,3\})=8.
\tag{MC23-3}
$$

It is the **smallest possible opposite-label collision by clause count** in the three-fixed-variable proper-clause language: an UNSAT formula on these variables must contain all eight forbidden signatures, so needs at least eight clause occurrences. No length-minimality is claimed across arbitrary variable-ID encodings or different alphabets.

**FALSIFIED candidate:** truncate the moment abstraction to degrees at most two, merge equal summaries, and assign a unique SAT/UNSAT terminal label. MC23-3 gives two equal abstract states with opposite true terminal labels, so unique-label terminal preservation is impossible. The error cannot be called a spurious path without source-specific replay. A sound may-abstraction must retain **both** permitted terminal outcomes from that merged state, causing the shortest abstract decision-path potential to reflect the cheap outcome. Restoring cubic moments repairs this *particular* terminal conflation, not arbitrary TM transition simulation.

This witness also separates the source label from a low-degree numerical proxy: complete Walsh moments record exact violation counts, while low-degree moments alone lose a parity distinction.

## 5. Physical transition charges and the precise all-transition scope

An implementation can maintain the sorted canonical moment dictionary **after every parsed clause** rather than merely sorting once at the end. Specify the following one fixed finite compiler B:

1. Parse the fixed-width or self-delimiting 3-CNF source and validate records, with MALFORMED as a separate terminal.
2. On each valid clause, physically read its three IDs/signs, construct its seven signed moment contributions, update the sorted work-tape dictionary, and home the work heads to a canonical position. Each actual head movement, tape write, comparison, temporary record and sort is charged.
3. After the final record, B may use its table for an exact **paid** exhaustive Boolean-assignment evaluation and return SAT or UNSAT. It never treats semantic minimization as an abstract free instruction. The total decision stage is generally exponential.

For this **particular B**, restrict to valid source streams having the same fixed-width record length and an identical unread suffix R, with a checkpoint immediately after finishing the same number j of clauses. By canonicalization, if H_3(P)=H_3(Q), then the work-tape contents, work-head positions and control at these checkpoints can be identical. B is specifically constructed never to reread the consumed prefix. Therefore equal unread suffixes yield identical input symbols at every subsequent primitive transition, and induction on the deterministic transition relation gives **one-to-one replay of every subsequent concrete physical step**, all remaining tape/head updates, both terminal labels, and exact *future* transition cost. A finite all-step simulation follows because each control/tape state, and not just each logical clause append, is synchronized. No off-head field access is supplied for free.

Past spent time and peak visited work cells may nevertheless differ between prefixes: those historical charges remain attached to the respective concrete runs, or must be retained as an explicit charged ledger if an abstract state is meant to preserve cumulative T and S. The theorem does **not** assert equality of whole-run cost merely from equal H_3. Source-bound arbitrary A can reread the earlier prefix, inspect input order, or branch on an irrelevant sign and insert paid delays before solving. Hence H_3 by itself is NOT an exact or even output-deterministic transition quotient for arbitrary A.

For the valid-input scanning phase of B, let p be the source bit position already traversed, with right end at L, and set Phi=L-p; set Phi=0 after the right end is reached. Since B reads every source bit with a local head and no physical transition advances by more than one, **every reachable scanning microstep** satisfies

$$
\Phi(c)\le1+\Phi(c'),
$$

and internal post-scan steps satisfy the same inequality with Phi=0; SAT/UNSAT terminal states have Phi=0. Thus the source-bound potential yields a rigorous **linear** initial bound L for B. It is not superpolynomial. Malformed early-rejection paths are not part of this valid-source potential assertion. A different correct solver need not perform B's canonical compilation.

More generally, for an arbitrary correct total decider A, the universally safe MAY abstraction maps each legal concrete transition to an abstract path of no greater cost, beginning with its bound concrete source x and preserving the observed SAT/UNSAT/MALFORMED terminal state. One can always retain the full physical configuration and use a unit-cost identity edge. To erase source or work history, a finite coverage certificate is needed; adding a low-degree moment summary without one does not satisfy the all-transition relation. For any candidate potential the Bellman inequalities must hold on **all** retained MAY edges, and its initial superpolynomial growth must be proved independently. The existence of an identity abstraction alone is a tautological simulation theorem, not progress toward that growth requirement.

## 6. Executed independent tests and hostile controls

Two implementations were independently authored and actually executed. A native CPython script, locally preserved as tmr4_moment023.py, checked 608 formulas, 29,896 full degree-three Walsh/truth-table assignment equalities, 26,032 equal-summary continuation equalities, and 36,183 clause-moment contributions with no assertion failure. Its exact program and complete raw JSON are local-only, not yet an authoritative GitHub source. It included U,V,Horn,XOR,duplication, 2-SAT auxiliary lifting, disjoint products and seeded random 3..7-variable formulas.

**AUTHORITATIVE published hosted-V8 version** has its exact executed function text in experiments/tmr/tmr4_moment_congruence023.cjs. It verified 507 formulas (500 SAT, 7 UNSAT), 24,928 assignment equalities, 22,448 continuation equalities, 27,741 signed clause contributions, 40 maximum nonzero moment keys, and zero failures. This JS test uses exact machine-size integer arithmetic in its small fixtures and a seeded high-bit recurrence; it is NOT a native OS Node run, not the actual machine B, and not an arbitrary TM compiler. The matching file results/raw/tmr/2026-11-14_0836_TMR4_MOMENT_CONGRUENCE023_RAW.json contains the actual V8 result. The two executable implementations differ in fixture counts and are not being misrepresented as byte-identical replay.

The finite verification is COMPUTATIONAL. The all-length moment identities and the eight-clause counterexample have explicit symbolic proofs above. No assertion that exhaustive tests cover all arbitrary machines, all inputs, or superpolynomial asymptotics is made.

## 7. Dependencies, barriers, and next target

**Existing source:** TMR-2/022, research/agents/tmr-2/2026-11-14_0823_TMR2_MAXSAT_WALSH_SIGN_ROBUSTNESS022.md and its original executed source/raw, establishes the Walsh coefficient identity and a flat-spectrum UNSAT recognizer. TMR-5/019, corrected sign-robustness, and TMR-1/022 certificate result show why sensitivity and input certificates are not machine-time bounds. TMR-4/022's authenticated moving-tape-head factor is a restricted all-transition predecessor, not a universal checker. The user-directed November 14 synthesis makes symbolic composition a high priority. Historical R_mix341 checker/normalizer failures remain evidence of the need for actual source and transition authentication, but do not apply as an arbitrary-machine theorem and were not reinspected exhaustively here.

**Primary references inspected:** R. O'Donnell, Analysis of Boolean Functions, Chapter 1, Cambridge UP 2014, https://doi.org/10.1017/CBO9781139814782.002 (Walsh orthogonality); P. Cousot and R. Cousot, Abstract Interpretation, POPL 1977, https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml (simulation consistency, not complexity separation); R. Ryan Williams, Simulating Time with Square-Root Space, STOC 2025, https://doi.org/10.1145/3717823.3718225 (arbitrary-machine space simulation via implicit Tree Evaluation, without an unconditional polynomial-time shortcut).

**Barriers:** The moment representation is polynomial in encoded source length and exactly sufficient for the clause-stream continuation semantics. It is not a program-independent operational sufficient statistic: an arbitrary decider may inspect source order, reread, use alternate encodings, share operations, cache, recompute, or use polynomial work space. Computing H_3 is optional, not necessary. The last operation of testing min_a v_F(a)=0 is general SAT. No exact cost-sound compression of all unrestricted arbitrary-machine traces, and no superpolynomial Bellman potential, was derived. Randomized/deterministic circuit-natural-proofs and relativization/algebrization barriers do not themselves refute the present elementary construction, which claims no general circuit lower bound.

**Quantifier target still OPEN:**

$$
\forall A\ \forall k\ge1\ \forall C>0\ \forall L_0\
\exists F\text{ valid}:\quad |F|\ge L_0,\
T_A(F)>C(|F|+1)^k.
$$

Here A is one fixed correct total deterministic multitape machine serving all lengths; T and S are charged for the SAME A and source. No fixed superlinear exponent or small-space restriction closes this. An algorithm with general polynomial worst-case time would be a legitimate alternative outcome.

**ONE NEXT TARGET for TMR-5/TMR-2:** audit the MC23-A all-continuation statement and the minimal H_2 opposite-label collision, then ask whether the actual Williams/Cook-Mertz block-composition evaluator permits a polynomial-size, physically computable *complete* sufficient statistic under its true extension and access semantics. Test any proposed projection with a U/V parity collision; do not conflate clause-level semantic congruence with a polynomial-time minimization algorithm or unrestricted machine simulation.

**Integrity:** directive 47459817e66dccf1f3079e6c724c0fd2643e7bc4 first; proof1 fully read SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343 (28,714 characters); proof2 recovered via authentic blob SHA 930c5eeddafce656717f28055a7a9a755f44737c (1,051,196 characters); canonical main via blob SHA 5ec8fffb16ec9a7f262e60321bf5aad172d153d8 (2,542,866 characters). Instructions, newest TMR handoffs, latest issue #3, relevant original reports/code/raw and primary source model descriptions inspected. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** TMR-5 owns the canonical root main.tex synthesis; no root modification is attempted. No schedules or legacy identities were changed.

END_OF_REPORT::TMR4::023::2026-11-14_0836_PST
