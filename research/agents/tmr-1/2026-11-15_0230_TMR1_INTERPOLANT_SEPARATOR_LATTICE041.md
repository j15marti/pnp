# TMR-1/041: Unique interpolants, disjoint-NP separator lattice and the general-circuit transfer gate

**2026-11-15 02:30 PST (America/Los_Angeles).** Role TMR-1, PNP Machine Model Lead. Governing fusion-Lipschitz directive: `research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md`, blob `54c9177fc211dfca6c94d89d6ebbf3f3908809d6`.

**Status:** PROVED/RESTRICTED (self-contained algebraic/projection theorems and exact model qualification), independent peer mathematical review OPEN. The exhaustive small-CNF audit is COMPUTATIONAL. No superpolynomial lower bound, no SAT-machine transfer and no P-versus-NP conclusion.

## 1. Candidate and falsifiers fixed before source and corpus checks

**Claim to delimit:** A fusion/interpolation lower-bound program that obtains a *unique* Craig separator from uniform polynomial-size CNF pairs is already investigating a language in NP intersect coNP. If its fusion measure upper-simulates unrestricted shared-fanout AND/NOT circuit gates at polynomial overhead, then an unconditional superpolynomial initial separator potential requires a superpolynomial **general Boolean circuit** lower bound for such a language, not merely ordinary Resolution hardness or large semantic rank.

Preselected falsifiers: (F1) A and B individually SAT and jointly UNSAT may still leave exponentially many valid separators rather than a unique one. (F2) A unique nonaffine or exponentially high communication-rank separator may have a linear or polynomial general Boolean circuit. (F3) Free intersection/complement or shared fanout omitted from a monotone-only/branching fusion cost can give a legal cheap circuit. (F4) A machine-to-proof or proof-to-interpolant bridge may change model, input, uniformity, source-length measure, or cost; a short native proof may not be constructible by a proposed SAT decider.

The current theorem is a **barrier and model classification**, not a proof of a lower bound. Original relevant peers: TMR-1/040 `research/agents/tmr-1/2026-11-15_0104_TMR1_CIRCUIT_GUARD_ADDITIVE_FIREWALL040.md` (blob `720ecf3b73fab83b073fadd4bb16f17076388c1d`), TMR-5/037 `research/agents/tmr-5/2026-11-15_0143_TMR5_NAE_RANK_GUARD_COMPOSITION037.md` (blob `7bb9e3bc27c011943d665f67d2ce077c78f694b6`), TMR-2/041, TMR-4/041 and the original October Lipschitz audit LEAD-0029.

## 2. Exact projection lattice: new project classification (PROVED/RESTRICTED)

Let `X` be n shared Boolean bits, `Y` and `Z` disjoint private variables, and `A(X,Y)`, `B(X,Z)` be source-authenticated CNFs. Define the projections

$$
U=\{x:\exists y\ A(x,y)\},\qquad
V=\{x:\exists z\ B(x,z)\},\qquad
\Omega=\{0,1\}^{n}.
$$

Suppose `A AND B` is UNSAT, equivalently `U intersection V` is empty. A Boolean Craig interpolant `I(X)` is exactly a Boolean function satisfying

$$
U\subseteq I^{-1}(1)\subseteq\Omega\setminus V.
$$

In particular, the **pointwise least interpolant** is `1_U`, the greatest is `1_{Omega minus V}`, and the exact number of Boolean interpolant truth tables is

$$
\boxed{2^{|\Omega\setminus(U\cup V)|}.}
$$

Consequently, a **unique Boolean interpolant exists if and only if** `U union V = Omega`; then it is `1_U=1_{Omega minus V}`. Both sides individually satisfiable means only `U,V nonempty`, **not** complementary. This theorem concerns extensional Boolean interpolants; circuit/syntax representations of the same function are not unique.

**Proof:** For each shared assignment x in U, A entails I=1. For each x in V, B entails I=0. At the remaining x, no implication restricts I, and every independent 0/1 choice is valid. This proves the lattice interval, extremal elements and count. QED.

**Smallest explicit hostile control:** On three shared bits, let U contain only 000 and V only 001. Encode each exact projection by a proper 3-CNF forbidding the other seven assignments. Both sources are separately SAT and jointly UNSAT, yet the six unrestricted shared assignments yield exactly `2^6=64` interpolants. Unique-separator claims that check only both-side SAT and joint UNSAT are false.

## 3. Exact uniform complexity classification (PROVED/RESTRICTED)

Suppose for each n the two formulas are constructible deterministically from `1^n` in polynomial time, each is of bit length polynomial in n, and every private witness is of polynomial length. If their projections cover all n-bit x, then the language

$$
L=\{x:\exists y\ A_{|x|}(x,y)\}
$$

lies in **NP intersect coNP**. Its YES certificate is y for A, and its NO certificate is z for B. The latter is sound and complete only because the shared projections are *complementary*, not merely disjoint.

**Conversely**, every language L in NP intersect coNP admits such a polynomial-time constructible complementary pair of 3-CNF verifier encodings (with private witness and auxiliary gate wires), by polynomial-size verifier circuits and local Tseitin constraints. Under a fixed input representation, the projection onto the n public bits agrees with the original YES/NO verifier, and the unique interpolant is precisely L restricted to n-bit inputs. This is an extensional representation theorem, not a claim of efficient proof discovery or a lower bound.

**Critical special case:** If a polynomial-size **uniform complementary** CNF pair had the general 3-SAT YES language as its unique interpolant, its B witness would place UNSAT in NP, and hence imply NP=coNP. No such unrestricted SAT/UNSAT witness pair is assumed or constructed. A noncomplementary disjoint NP pair does not supply all NO witnesses.

If the pair exists only nonuniformly, the immediate classification is with **nonuniform advice**, not an unqualified NP intersect coNP assertion. Uniform constructibility is an explicit hypothesis here.

## 4. Circuit route and conditional implication strength (PROVED/RESTRICTED implication)

Let `C_{AND,NOT}(f_n)` count minimum nonuniform **shared-DAG** Boolean gates in an unrestricted fan-in-two AND/NOT basis (constants and input wires available). Such circuits can be simulated using intersection and complement gates on represented Boolean signals without duplicating shared subgraphs. If an intended fusion complexity `rho(f_n)` satisfies the independently **proved** bridge

$$
\rho(f_n)\le \operatorname{poly}(n,C_{AND,NOT}(f_n))
$$

for every function in the selected source/interpolant class, then a superpolynomial lower bound on `rho` for an explicit uniform complementary CNF-pair family of polynomial bit length implies a superpolynomial **general circuit** lower bound on its NP intersect coNP interpolant. In particular it implies

$$
\boxed{NP\not\subseteq P/poly,}
$$

which is strictly a stronger conclusion than merely `P != NP` (the implication is one-way, not an equivalence).

**Proof of implication:** If NP were a subset of P/poly, the particular uniformly NP language U would have polynomial-size circuits. By the postulated fusion upper simulation, its unique separator would have polynomial fusion cost, contradicting the superpolynomial lower bound. QED. This does *not* assert that the fusion upper simulation has been proved for the historical fusion grammar.

The same argument works for a disjoint pair without coverage if the proposed obstruction lower-bounds **every** separator: the NP language U itself always supplies a separating Boolean function. A lower bound on one arbitrarily selected separator does not suffice.

**Weakest independent SAT-in-P gate:** Suppose a fixed total SAT decider runs in polynomial time on every encoded 3-CNF. Given any uniform polynomial-size disjoint pair, substitute an n-bit x into the A side, construct the resulting polynomial-length SAT instance, and run that decider. Its answer is `1_U(x)`, a valid separator. Standard time-unrolling of a fixed finite multitape machine produces a polynomial-size nonuniform AND/NOT circuit for each n (or a uniform circuit generator with polynomial overhead). This is an **algorithm-to-separator-circuit** transfer only. It is not a polynomial-cost compiler from an arbitrary SAT machine into **ordinary Resolution**, nor a lower bound.

The direction of the circuit comparison is indispensable. An abstract fusion measure that forbids NOT, sharing, Gaussian compression, or compact extensions **may be exponentially larger** than general circuit size even for easy functions. Such a restricted measure cannot be used for the nonuniform conclusion without its own exact cost-sound machine bridge.

## 5. Qualified circuit laboratory and all-step tariff

**Model C-SEP (RESTRICTED, not a physical SAT decider):** An immutable source pair (A,B) defines a disjoint projection pair. A state records the source, available public input bits/constants, a complete shared AND/NOT DAG of computed wires, and a selected output wire or open-goal flag. Legal zero-price operations are input-wire reference, reusing an existing wire, switching which already available output is considered, and NOP; these never create a new Boolean function. The only paid primitive is APPEND a legal AND or NOT gate using extant signals, with cost one. A terminal goal is reached when an available wire semantically separates U and V. The semantic goal predicate is an *external mathematical property*, not a free effective SAT oracle. Arbitrary sharing/fanout, circuit shortcuts and both labels are legal. Unknown additional operations are MAY if this lab is ever used to approximate a richer machine.

Let `R(C)` be the **minimum number of additional paid gates** required to reach a valid terminal separator from state C. It is finite because U is a finite Boolean function and ordinary AND/NOT circuits can represent it. Any zero-cost transition C->C' has `R(C')<=R(C)`; if reversible it is equality. Any paid APPEND step has `0<=R(C)-R(C')<=1` (the upper bound follows by prepending the performed gate to an optimal continuation). Goals have R=0. Therefore the seven-column obstruction vector `p=(0,0,0,0,0,0,R)`, with `lambda_machine=1`, is an exact all-step tariff certificate, but its initial value is **by definition the minimum circuit complexity of a separator**. It is not an independent superpolynomial gap theorem. Source construction, authentication, optimal-circuit search and physical gate evaluation are NOT paid by this laboratory and cannot be transferred to an actual SAT machine for free.

**Exact tariff rows:** zero reference/NOP: Delta=(0,0,0,0,0,0,0), w=0; paid APPEND: Delta=(0,0,0,0,0,0,d), 0<=d<=1, w=1; zero terminal selection: Delta=0 because R=0 already. The abstract zero-cost SCC quotient identifies mutually reversible pointer/NOP changes, while directed free output selection is retained. Every legal transition obeys lambda.Delta<=w; completed goals have Phi=0. The cross-model all-machine transfer remains **OPEN**.

## 6. Explicit growing family and compact hostile controls

For n>=3, take `P_n(x)=NAE_n(x)`, true exactly when not all n input bits are equal. Use

$$
A_n(x)= (x_1\vee\cdots\vee x_n)\wedge(\neg x_1\vee\cdots\vee\neg x_n),
$$

and B with private bit s imposing equality of every x_i to s:

$$
B_n(x,s)=\bigwedge_{i=1}^{n}
((\neg s\vee x_i)\wedge(s\vee\neg x_i)).
$$

Both sides are SAT; their projections partition all shared x; the unique interpolant is NAE_n. Replacing the two wide A clauses by source-authenticated standard gate-Tseitin clauses gives polynomial-size CNF of width at most three with private wires, still with exact projection. Both sides have encoded length `O(n log n)` after ordinary indexed serialization. NAE_n has an `O(n)` AND/NOT circuit using two OR trees plus one AND; sharing and negation are allowed. It is a nonaffine/somewhat nontrivial separator, not a hard separator. The source itself is handled polynomially by direct evaluation, Horn/2-SAT or equality propagation as appropriate. Affine and private-leaf Q_k controls from TMR-2/040/041 have already independently supplied further cheap examples.

The other control is PARITY3: four proper-3CNF clauses on each side yield complementary parity projections, while Gaussian elimination or a small XOR/AND/NOT circuit evaluates the unique interpolant. Do not count truth-table rank or non-Schaefer status as required machine work.

## 7. Actual V8 execution and exact evidence

`experiments/tmr/tmr1_separator_lattice083.js` contains the **exact V8-executed audit function** serialized from the successfully evaluated function. `results/raw/tmr/2026-11-15_0230_TMR1_SEPLAT083_V8_RAW.json` is the original result. No native Node process or physical SAT-machine program was executed.

For n=3 shared bits, each of the 256 Boolean functions is represented exactly by a proper 3-CNF forbidding all other complete assignments; the script verifies its whole truth table. Across all `3^8=6,561` disjoint projection pairs, it explicitly checks **1,679,616 possible candidate separators**. The unique-pair count is `2^8=256`; among `6,050` pairs with each source SAT, `254` have a unique separator. The total number of valid separator tables over all pairs is `4^8=65,536`. All 19,948 assertions passed, with zero failures. PARITY3 and NAE3 opposite-projection source controls passed. Finite evidence is COMPUTATIONAL only; the general theorems above are symbolic proofs.

## 8. Dependency ranking and precise gaps

| Arrow | Verdict | Exact reason |
|---|---|---|
| Disjoint CNF projections -> separator lattice/count | PROVED/RESTRICTED | Direct finite-set proof; independent review OPEN |
| Uniform complementary polynomial CNFs -> unique NP intersect coNP separator | PROVED/RESTRICTED | Two polynomial witness verifiers; construction via Cook-Levin/Tseitin |
| Uniform general SAT YES/NO complementary pair | OPEN / implies NP=coNP | Requires short witnesses for arbitrary UNSAT |
| General circuit cost upper-bounds fusion cost with full sharing/NOT | OPEN for project's intended fusion grammar | Exact C-SEP equivalence only in qualified AND/NOT lab |
| Superpolynomial general-fusion separator lower bound -> NP not in P/poly | CONDITIONAL | Requires prior arrow and uniform complementary source family |
| Native Resolution hard -> arbitrary SAT-machine hard | FAIL as unqualified transfer | TMR-1/036 and /037 affine shortcut |
| Fusion-safe multiscale superpolynomial initial potential for all machines | OPEN | No unconditional general-machine obstruction provided |
| Historical /341 full logical UNSAT checker | FAIL | Retain source SAT counterexample, no relabel |
| Historical /386 | RESTRICTED | Tested guarded odd-charge fragment only |
| P versus NP | OPEN | No all-machine time lower bound or uniform polynomial solver |

**Genuinely new relative to /040 and TMR-5/037:** The exact separator lattice and uniqueness iff coverage theorem, uniform NP intersect coNP characterization of unique-CNF interpolants (both directions), the stronger NP not in P/poly implication threshold for a circuit-faithful fusion route, the SAT-as-unique-interpolant NP=coNP gate, an explicit qualified circuit-APPEND tariff and exhaustive proper-3CNF projection-pair audit. These results do not independently prove circuit lower bounds or improve the already established Resolution-hard source bounds.

**Next weakest lemma and peers:** TMR-2 should supply a candidate uniform nonaffine disjoint NP pair whose *minimum over ALL valid separators*, not just one chosen interface, survives compact arbitrary circuit and preprocessing controls. TMR-3/4 should precisely decide whether a proposed fusion operator grammar simulates unrestricted shared AND/NOT circuits with polynomial overhead and charge all physical interface-construction costs. TMR-5 should audit the NP intersect coNP uniformity and the conditional NP not in P/poly conclusion, and replay the 64-separator nonunique control. If the fusion model excludes cheap negation or sharing, record it as a restricted proof-model lower bound rather than a general-machine theorem.

## References, original source and scope

[1] J. Krajicek, "Interpolation Theorems, Lower Bounds for Proof Systems, and Independence Results for Bounded Arithmetic", *J. Symbolic Logic* 62(2):457-486 (1997), DOI https://doi.org/10.2307/2275541 . Primary journal abstract https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/abs/interpolation-theorems-lower-bounds-for-proof-systems-and-independence-results-for-bounded-arithmetic/F12076ADD221B77416830DFB41475A95 . This paper supplies proof-system-specific **feasible interpolation** upper bounds, NOT a converse lower bound from native proof hardness.

[2] A. Razborov, "On Provably Disjoint NP-Pairs", BRICS Report Series RS-94-36, November 1994, https://www.brics.dk/RS/94/36/index.html . Supports the disjoint-NP-pair context; the elementary lattice/classification statements here are proved independently.

[3] S. Cook, "The Complexity of Theorem-Proving Procedures", STOC 1971, pp.151-158, https://doi.org/10.1145/800157.805047 . NP verifier-to-SAT encoding; no proof-system lower-bound preservation imported.

[4] E. Ben-Sasson and A. Wigderson, "Short Proofs Are Narrow: Resolution Made Simple", JACM 48(2):149-169 (2001), https://doi.org/10.1145/375827.375835 . Historical exponential Resolution lower bounds are model-scoped and not used to prove the new lattice/classification theorem.

**Preflight:** Read fusion directive first, then TMR replacement directive, root proof1 full SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`, root proof2 authentic full Git blob SHA `930c5eeddafce656717f28055a7a9a755f44737c`, root main.tex authentic full Git blob SHA `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34`, issue #3 and latest comments, AGENTS.md, CODEX.md, repository skill and mode guidance, all five latest TMR handoffs, and materially relevant original TMR/LEAD reports. Empty GitHub contents bodies for the huge proof2/main files were NOT interpreted as blank files. TMR-5 owns root manuscript synthesis. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No agent/task changes.
