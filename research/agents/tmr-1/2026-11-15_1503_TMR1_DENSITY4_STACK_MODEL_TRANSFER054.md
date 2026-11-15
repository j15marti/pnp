# TMR-1/054: Density-four exact-count CNF compiler and physical stack-model transfer

**2026-11-15 15:03 PST | PNP Machine Model Lead | Track C | user-governing SAT compression directive main blob 7b8804dc7587abc5134055b5b0d16a143055ca5a.**

**Status:** Compiler PROVED/EXACT restricted to explicitly encoded shared fan-in-two circuits (independent mathematical review OPEN); standard-machine simulation PROVED/RESTRICTED conditional on precisely stated finite-stack machine semantics; numerical finite checks COMPUTATIONAL. Anthropic October 2026 mathematical MainTheorem treated as a pinned FORMAL SOURCE CLAIM, not kernel replayed here. NP-level transfer and P versus NP remain OPEN.

## 1. Candidate, model, and four falsifiers

**D4-054.** For every explicitly given DAG C with q>=1 named Boolean input bits and G>=0 ordered distinct, shared binary-truth-table gates, with arbitrary predecessor reuse, including constant functions and dead gates, one designated output, and V=q+G>=4, construct in polynomial bit time a *count-preserving unique-extension* width-at-most-three CNF H on V variables. It satisfies the actual Anthropic predicates AllOccur, outer-list NoDup, k=3, V>=4, m>=2, and crucially **m<=4V**, improving the previous TMR-1/053 tariff m<=5V. It has a precisely known bit length under Anthropic's `encInput`, and admits an explicitly charged physical standard multitape simulation of the finite-stack algorithm without asserting a small-space bound.

Falsifiers: **F1** repeated gate predecessors, constants, dead outputs or shared fan-out create zero or multiple satisfying auxiliary extensions; **F2** marking only original unused inputs misses any declared CNF variable, or dedup destroys a constraint; **F3** a clause/header/padding interpretation fails the exact pinned Lean `encInput`, including low-bit-first slots or ordered-list NoDup; **F4** a finite-stack operation hides nonconstant physical work, or preprocessing/arithmetic/input length erases the claimed asymptotic exponent.

The computational input is the entire explicitly written shared gate DAG; gate identities are charged once, all q inputs and G named gate outputs contribute to V. This is not a compiler from arbitrary SAT input to O(n) variables when G=n^4.

## 2. Symbolic proof: m<=4V and exact count

For each gate z=f(a,b), a and b may even be the **same** predecessor, emit exactly four clauses indexed by u,v in {0,1}:

`(a != u) OR (b != v) OR (z = f(u,v))`.

Here the first two literals are true precisely when predecessor bits disagree with the indexed pair. For a fixed predecessor valuation, the matching (u,v) clause forces z=f(a,b); every other clause is true. This remains valid for a=b because contradictory-index clauses become tautologies and the matching-index clause still forces z. Induction in topological order gives exactly one gate-vector for every original input assignment. Pin the designated output by a positive unit. Thus each source input has exactly one satisfying extension iff C outputs 1, otherwise none. The total #SAT counts are equal.

Every gate-output variable appears in its own four clauses. Every original input appearing as a gate predecessor appears in its corresponding clauses, and an original input used directly as the designated output appears in the unit. Let u<=q be the count of **remaining unused original** inputs. Add for each one the tautological *ordered list* (x, not x, x); unlike pinning, this does not multiply the number of extensions because x was already an original free input. Remove only exact duplicate **outer clause lists** (permitted by the Lean statement). The above constraints remain equivalent. All V variables now occur, width<=3, and NoDup holds.

There are at most `m<=4G+1+u<=4G+1+q<=4(q+G)=4V`, since q>=1 and 1<=3q. There are at least two clauses whenever V>=4: if G=0 the output unit and the other q-1 input tautologies already give m=q>=4; if G>=1 a gate contributes at least one syntactically distinct clause plus an independently distinct positive output unit. For source circuit input length L_C=O(V log V), an ordinary deterministic compiler can enumerate clauses and deduplicate by pairwise comparison in time O(V^2 log V) with O(V log V) storage (a more conservative O(V^3) bit time is also valid). Clauses from the same gate may be syntactically tautological, but are legal and may not be silently deleted if that would remove an input occurrence.

**IMPORTANT scope:** `IsKCNF 3` in pinned Anthropic MainResults.lean permits zero-, one-, two-, or three-literal clauses, repeated/opposite literals within a clause, and distinguishes differently ordered lists. This is not a strictly proper exactly-three CNF compiler. TMR-5/049's count-only normalizer is a different construction and cannot be treated as a fast compiler.

## 3. Exact source bit length and TM model

At k=3, `encInput 3 H` is: three ones, zero; V ones, zero; then for every clause exactly three padded slots. A slot value is 0 for absent, `2i+1` for negative variable i, or `2i+2` for positive; each slot is represented LOWEST BIT FIRST using `w(V)=floor(log2(2V))+1` bits. Thus its *exact* total length is

`B(V,m)=V+5+3m w(V)<=V+5+12V w(V)=O(V log V).`

This includes repeated symbols, padding, unary headers, source scanning, clause ordering, and original variable names. Explicit deterministic encoding and reading cost polynomial bit time; the numerical verifier performs the inverse parser on each generated test.

Pinned Anthropic `MainResults.lean` (commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5; blob 1c62a550fa1e4cbec65bb7112f92ad67589afddc) declares one `Turing.FinTM2` with a fixed finite set of stacks and finite alphabets, and one constant C for all k/formulas. One fixed program block executes boundedly many push/pop/top operations in one formal step. **Given these precise semantics**, a conventional deterministic multitape TM has one writable tape per simulated stack with its head at the logical stack top, plus constant control. Each formal push, pop and read uses O(1) genuine tape actions; preparing the input in correct stack order and writing the answer uses O(B^2) conservatively. Therefore a T-step formal execution on an encoded input of B bits transfers to **one** conventional multitape execution with paid

`T_standard=O(T+B^2)` and `S_standard=O(T+B)` writable cells.

S_standard is an *upper bound*, not a claim of polynomial space. Finite stack alphabet symbols and fixed control count at constant-factor bit cost. This standard simulation is a mathematical model lemma, NOT an independent Lean build or validation of the formal source theorem.

For m<=4V and AllOccur, the latter implies V<=3m, hence log2 m>=log2(V/3). At k=3 the first arm of pinned Anthropic's `timeMin` is

`expM=3m/sqrt(log2 m)<=12V/sqrt(log2(V/3))=(12+o(1))V/sqrt(log2 V).`

For all sufficiently large V, polynomial compilation, input preparation, and the one machine's output cost are absorbed in the same exponent. **Conditional on the correctness of the pinned proof**, the fully charged conventional uniform #Circuit-SAT algorithm for explicitly provided q-input G-gate circuits has

`T_C(q,G)=2^{(12C+o(1))(q+G)/sqrt(log2(q+G))}`

with a polynomial preprocessing tax, and a conservative peak storage bound O(T_C+V log V). The formula is a *size-V* guarantee, not a `2^{o(q)}` algorithm when G grows polynomially above q.

This makes explicit the coefficient reduction from the prior source tariff 15C under density five to 12C under density four. It does not improve the exponent's order, and the constant C is neither extracted nor numerically estimated from Lean.

## 4. Quantitative hierarchy target and the missing NP-level bridge

Applying the existing TMR-1/053 Jahanjou-Miles-Viola constant-local clause reduction, one candidate witness circuit with s gates is instantiated three times plus O(n) decoder gates, yielding V=3s+O(n). Under the density-four Anthropic first-arm source premise, at s=eta n sqrt(log n) the solver's exponent is asymptotically `36C eta n`. Choosing `0<eta<1/(72C)` leaves strictly less than n/2 in the exponent, and the prior conditional nondeterministic hierarchy argument yields the same **E^NP**, infinitely-often general gate lower bound Omega(N sqrt(log N)). Previous density-five coefficient would have been 45C eta rather than 36C eta. Every uniform source construction, three copies, wire name, clause, stack alphabet and input-bit conversion is paid as above. The source-locality theorem and hierarchy step themselves are inherited and not independently re-proved here.

**No NP-level conclusion:** The witness language is explicitly E^NP, not NP. Williams's NEXP circuit conclusion and Bathie-Williams's E^NP formula conclusion also cannot be recast as NP. Under P=NP, an E^NP or NEXP lower bound need not contradict anything. An NP-level circuit lower bound strong enough to imply P!=NP requires a new justified nonrelativizing ingredient. No claimed `DTISP` forbidden region is used here.

## 5. Four mandatory gates

| Gate | Status | Exact reason |
|---|---|---|
| DISJ sanity | **PASS** | The compiler handles compact DISJ circuits, retains their O(q) gate count, and infers no hardness from their full 2^k cut rank. Horn, XOR/affine, constants, dead/shared gates, input padding and no-gate controls are included in finite tests. |
| Relativization | **PASS restricted / OPEN unrestricted** | Syntactic CNF and stack simulation can relativize, but neither implies P!=NP. A nonrelativizing NP-level separation is NOT constructed; algebrization/Natural Proofs remain future audits. |
| Simultaneous DTISP | **NOT APPLICABLE to hierarchy transfer; OPEN for proposed FLMV use** | A single charged algorithm has the time above but only S<=O(T+B); no forbidden simultaneous strict time-and-sublinear-space pair is claimed. |
| Configuration counting | **PASS upper-bound guard** | The fixed deterministic total read-only-input standard TM satisfies T<=2^{O(s+log B)}; the inequality is never inverted into an algorithmic work lower bound. |

An OPEN load-bearing NP-level or DTISP bridge prohibits unrestricted promotion. /341 remains FAIL as full logical UNSAT authority, /386 remains RESTRICTED.

## 6. Reproducibility and provenance

Hosted V8 executed `TMR1_DENSITY4_STACK054_v1`, xorshift32 seed 20261115, with **426 circuits, 10 directed hostile controls, 8160 original assignments, 47888 complete input-plus-gate assignments, 24229 assertions, zero failures**. Tests cover all 16 binary Boolean truth tables with all 16 pairs of input predecessor indices; 160 seeded shared circuit instances; dead gates, repeated variables, constants, XOR, NAND, AND, and a compact DISJ2. Each test checks exact count, per-input unique extension, all original inputs and auxiliary vars occurring, outer list NoDup, density four, encoder exact bit length, and inverse parser. Finite status COMPUTATIONAL, NOT a test of asymptotic lower bounds or Lean kernel.

Code: `experiments/tmr/tmr1_density4_stack054.js`.
Raw: `results/raw/tmr/2026-11-15_1503_TMR1_DENSITY4_STACK054_V8_RAW.json`.
Run: `node experiments/tmr/tmr1_density4_stack054.js`.
Source revision: `TMR1_DENSITY4_STACK054_v1`, seed 20261115.

**Primary source:** Anthropic pinned MainResults.lean and Solution.lean at commit `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`, plus OpenAI math October-25 manuscript and documented weaker Lean scope (TMR-1/053). Jahanjou-Miles-Viola local 3SAT reduction [https://eccc.weizmann.ac.il/report/2013/099/] and 2014 Harvard theory seminar [https://toc.seas.harvard.edu/seminar14-15]. Prior originals: TMR-1/053 report, code SHA 08f0ee435bdb7f28dcee5d5a05210e67ed3bf13a, raw SHA 05d9c9d938230225ccff8ec6728b022a88e3ad8e; TMR-5/049 scalar-count collision; TMR-4/053 restricted adaptive switch BP.

**Repository reconciliation:** governing directive read first. proof1.txt full blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt blob 930c5eeddafce656717f28055a7a9a755f44737c and main.tex blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 returned empty bodies from connector. AGENTS.md, CODEX.md, pnp-research skill, TMR 1-5 current handoffs and issue #3 reviewed. Full local repo preflight and Lean build not run. No existing root or other-agent files edited. **TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.**

**Next weakest lemma:** independent pinned Lean kernel build of the density-sensitive MainTheorem with a source-order TM2->multitape conversion at actual executable/encoding level; or a real same-machine compression for G=q^4 that beats the V=q+G tax without losing uniformity or counting.

**P versus NP remains OPEN.**
