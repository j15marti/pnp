# TMR-3/039: LASTSAT073, opposite-SAT-label final-bit tariff

**2026-11-15 00:28 PST | PNP Time-Space Tradeoffs | America/Los_Angeles**

**Scientific status:** PROVED/RESTRICTED for the exact binary 3-CNF encoding and every correct total finite-alphabet, locally moving deterministic multitape SAT decider in the stated model. Independent mathematical/physical-machine review OPEN. Finite V8 tests COMPUTATIONAL. The new theorem gives a **linear**, not superpolynomial, physical-time bound. P versus NP remains OPEN.

## 1. One candidate and four preselected falsifiers

**Candidate:** Repair TMR-3/038's last-byte **macro-certificate-language** indistinguishability argument by building a pair of valid proper 3-CNF formulas with **opposite SAT labels**, identical in every bit except the final source bit. Prove a valid source-ingress tariff for arbitrary correct SAT machines, and then test whether the family itself has a polynomial-time recognizer.

Preselected falsifiers were: (F1) the final-sign mutation changes only macro-language acceptance, not SAT; (F2) a mutated formula is malformed or an earlier bit differs; (F3) authentic local heads, rereads, caching or sharing read the final source bit without traversing the input; (F4) a fixed correct machine recognizes the pair in polynomial time, disqualifying its use as a superpolynomial witness. F1 and F2 are ruled out by exact construction and finite tests; F3 is excluded by the declared **physical** model only; F4 is a genuine polynomial-time hostile control.

## 2. Qualified state, source grammar and encoded family

A machine A is one fixed finite-alphabet deterministic total multitape program, with one read-only source tape, any fixed finite number of writable tapes and heads initially at their respective left positions. A physical step reads the scanned symbols, changes control, writes or erases work/output cells and moves each head by at most one position; its sequential cost is exactly one. Every correct program must classify all valid encoded 3-CNF formulas and malformed strings, not only the chosen examples. Additional fixed read-only copies with **left-starting, locally moving heads** do not alter the ingress proof. Random access, uncharged prepositioned heads and input-oracle access are different models.

The fixed general **proper 3-CNF input grammar** is a unary bit-width field 1^b 0, a unary clause-count field 1^M 0, then exactly 3M literal records. A literal record is a b-bit nonzero unsigned variable identifier and a single sign bit (0 positive, 1 negative). Each clause has exactly three pairwise distinct IDs. There are no trailing bits. The parser treats malformed source encodings as invalid, under the machine's declared total convention. The grammar admits arbitrary proper width-three CNFs, not only the family below.

For each integer m>=3, let G_m be the cubic prism graph C_m square K_2, with H=2m vertices and E=3m uniquely numbered edges. Associate Boolean variable x_e with edge e. At a vertex v having distinct incident edges a,b,c, the **complete four-clause encoding** of x_a XOR x_b XOR x_c = b_v forbids all four triples with opposite parity. Use charge b_v=0 at H-1 vertices and charge b_v=1 at the last vertex. Order all H four-clause blocks by vertex, and order the last odd block with the all-positive clause (x_a OR x_b OR x_c) **last**. Call this proper source F_m^-.

Construct F_m^+ by changing only the final literal x_c in the final clause to NOT x_c. No other literal or source field changes. Both are syntactically valid proper three-CNF formulas with M=4H=8m clauses. Take b_m=ceil(log_2(3m+1)); their **bit** encoding lengths are exactly

$$
N_m=(24m+1)(b_m+1)+8m+1=\Theta(m\log m).
$$

The formula counts the unary width header (b_m+1), unary clause-count header (8m+1), and 24m literal records of (b_m+1) bits. The first N_m-1 bits of the two valid encoded formulas are identical, while the last polarity bit is 0 in F_m^- and 1 in F_m^+. The source length N_m is distinct from H, E, literal records, semantic assignments, evidence bytes and any proof-DAG event count.

**Exact symbolic SAT-label proof (PROVED/RESTRICTED):** Every full parity block is equivalent to its three-variable XOR equation. In F_m^- the XOR of all H equations has left side zero because each graph edge occurs in precisely two vertex equations; the right side is one because precisely one vertex charge is odd. Hence 0=1 and F_m^- is UNSAT. In F_m^+, the **all-zero assignment** satisfies every even-charge block, the three unmodified final odd-charge clauses, and the changed last clause containing NOT x_c. Hence F_m^+ is SAT. Both remain proper 3-CNF and have Hamming distance exactly one **input bit**.

No expansion or Resolution lower-bound assumption enters this proof. Ben-Sasson and Wigderson [1] provide relevant original Tseitin/Resolution context, not a logical premise of LASTSAT073.

## 3. All-correct-machine theorem, precise transition bound

**Theorem LASTSAT073-A.** For every single fixed correct total deterministic locally moving multitape 3-SAT decider A, and **every** m>=3, both its F_m^- and F_m^+ runs read original input cell N_m-1 and have actual physical transition counts

$$
T_A(F_m^-)\ge N_m,\qquad T_A(F_m^+)\ge N_m.
$$

**Proof.** Until the first inspection of the final input cell, the two runs encounter identical input symbols. Starting from identical control, blank work tapes, input-head locations and source prefix, determinism forces identical program state, work tapes, head movements and requested input positions. If one run halted before reading the final cell, the other would halt with the same answer, contradicting the two proven opposite labels and A's correctness on both. Therefore neither run can halt before accessing this last cell. A head initially at input cell zero, moving at most one cell per transition, cannot read cell N_m-1 before the N_m-th transition, with the symbol scanned before the move. The argument allows arbitrary polynomial or larger work space, adaptive rereads, compressed representations, shared computation, caching and recomputation. With any fixed number of left-initialized local input heads, the maximum frontier obeys the same unit step bound. QED.

This theorem covers arbitrary correct machines **within the stated physical input model**, rather than only a macro certificate verifier. It establishes no superpolynomial lower bound. Its quantifier pattern is intentionally stronger than needed for the linear family property, but is not the all-exponent 3-SAT lower bound being sought. No source-length or word-RAM access theorem is silently imported.

## 4. Complete local tariff slice, zero closure and goal

For either original source in this pair, let r(C) be the maximum original input index that A has **actually inspected**, starting at -1. Use the reduced-product physical-obstruction vector in the shared seven-column order

$$
p(C)=(0,0,0,0,0,\max(0,N_m-1-r(C)),\mathbf 1[\text{not halted}]).
$$

Every **actual** finite-alphabet machine step, including a pure read, output, head movement, cache update, physical storage, recomputation, control switch, halt or their simultaneous fusion, costs w=1. There are no zero-price physical transitions, so the exact zero-cost SCC quotient and directed cl0 closure are both the identity. An unknown machine instruction is not declared illegal: all genuine standard TM transitions satisfy the locality inequality.

All input heads move locally, hence r(C')-r(C)<=1 and the interface component can decrease by at most one on every step. Theorem LASTSAT073-A independently establishes that on the **correct terminal runs of this two-formula family** the rightmost input cell has been read. Thus both interface and machine obstruction components are zero at the goal. The exact valid rational seven-column tariff certificate is

$$
\lambda=(0,0,0,0,0,1,0),\qquad
\lambda^\top(p(C)-p(C'))\le1=w(C,C').
$$

The initial potential equals N_m and the final potential is zero. Telescoping therefore certifies T_A(F_m^\pm)>=N_m. The machine-readable matrix includes first-time input reads, rereads, pure work/cache/recomputation, multiple left-started heads, fused input/work/output operations and terminal transitions. A hypothetical legal read-and-halt may discharge interface and machine flags simultaneously; independently charging both flags at full weight would violate a **conservative** complete local row. We claim **only** the displayed feasible witness, not an exact optimal two-coordinate cone for the restricted reachable correct-program state set.

**Physical ledger:** one transition is one sequential elapsed step, even when many conceptual views/caches or proof obligations change together. Logical inference events, evidence bits, messages, work-space visited cells, proof span, input bits, and output are separate measures. With a fixed number of work-heads, at most O(T+1) writable cells can first be visited in T actual transitions on the same run; no time-space mixing across different A or different inputs. Every source reread, definition, allocation, address movement, conversion, proof serialization and output is already accounted for as its genuine physical step, not an extra arbitrary abstract charge.

## 5. A real cheap correct algorithm closes the superpolynomial-family route

**Theorem LASTSAT073-B (POLYNOMIAL FAMILY CONTROL).** There is one fixed total correct uniform deterministic multitape SAT machine D, with exponential fallback outside the family, that runs in at most O((N_m+1)^6) transitions and visits at most O((N_m+1)^2) work cells on **both** F_m^- and F_m^+.

**Construction/proof.** Parse and fully validate the general source grammar, including endmarker. From clause count M and index width b, test whether M=8m and b=ceil(log2(3m+1)) for some integer m>=3. Generate the canonical prism graph, full four-clause blocks, and the two expected bitstrings deterministically; compare the **complete source** to the two candidates. On an exact negative match reject (UNSAT), on an exact positive match accept (SAT), using the already proven labels. On every other valid 3-CNF use exhaustive assignment search, and classify malformed encodings under the explicit total parser. The full program is fixed across m and all binary input lengths. Correctness is all-input, because unmatched valid formulas are solved by exhaustive search rather than guessed from the special family.

On matched sources, all generated tables, counters, indices, string comparisons, and recorded bitstrings have size O(N_m) and can be implemented by a fixed number of finite-alphabet tapes. Even naive nested scanning and binary counter operations use a polynomial number of primitive transitions; O((N_m+1)^6) time and O((N_m+1)^2) visited writable cells are conservative bounds, not empirical compiled-machine timings. Every source bit and endmarker is actually read; there is no free parser or nonuniform advice. The fallback may be exponential off-family. This proves the family cannot supply a superpolynomial initial potential valid for **every** correct SAT machine, although every correct local-input A still pays the linear ingress cost. QED.

Hostile controls are explicit: F_m^- is fully affine/Tseitin and has a short parity contradiction; F_m^+ has a known all-zero witness. Gaussian elimination, Horn and Krom/2-SAT checks, bounded-treewidth dynamic programming, autarky, source preprocessing, extension variables, learning, renaming, padding, cache sharing, compact circuits and arbitrary alternate representations remain legal. None can make the initial last-bit locality floor superlinear; a true random-access machine requires separate model charges. The old /341 full checker remains FAIL and /386 remains RESTRICTED.

## 6. Prior results, exact execution, qualification and status

**Read FIRST:** research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md (blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6), then November 13 TMR replacement; full proof1.txt (blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343), complete proof2.txt via authentic blob 930c5eeddafce656717f28055a7a9a755f44737c and main.tex via blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 (GitHub contents calls returned blank for the two large files), AGENTS.md, CODEX.md, project pnp skill, latest issue #3, and all five TMR handoffs. Original TMR-3/038 report/code/raw/matrix, TMR-1/037 AUTHXOR source, TMR-3/036 affine recognizer, TMR-3/037 serialization, TMR-1/039 guarded interface, TMR-2/039 EQUALJ, TMR-4/039 MODEJOIN and TMR-5/035 MODEALT were inspected. Historical Lipschitz failure controls retained. No conflicting peer theorem is promoted into general machine time.

**New versus earlier work:** TMR-3/038 used a final-byte mutation that changed acceptance in a *restricted macro-certificate language*, without proving opposite SAT labels. The newly constructed proper 3-CNF last-bit pair has **opposite SAT labels**, upgrading the locality lower bound to every correct all-input SAT decider in the standard local-head model. The fully charged polynomial **family recognizer** simultaneously falsifies any superpolynomial extrapolation from this ingress obstruction.

**Exact native V8 execution:** experiments/tmr/tmr3_lastsat073.js. The tested function is serialized byte-identically to published source, with a Node console wrapper not independently re-executed. Raw machine-readable output: results/raw/tmr/2026-11-15_0028_TMR3_LASTSAT073_V8_RAW.json. Full seven-column tariff matrix: results/raw/tmr/2026-11-15_0028_TMR3_LASTSAT073_TARIFF_MATRIX.json. Deterministic tests: m=3,...,14, 33,659 assertions and 33,062 physical tariff edge templates, **zero failures**; complete small SAT assignment enumeration m=3,4,5; exact decoder roundtrips, source parity authentication, all-zero SAT witnesses, malformed strings, source tampering, and uniform pair-recognizer controls. These are **COMPUTATIONAL**, not a compiled physical Turing-machine replay. The all-m assertions are separate symbolic proofs above.

**Dependency status:** original physical local-head locality PASS; opposite-label parity construction PROVED/RESTRICTED, peer review OPEN; rational one-column tariff PROVED/RESTRICTED, peer review OPEN; superpolynomial extrapolation for this family FAIL via polynomial D; a dynamic nonaffine fusion-safe all-machine potential OPEN; same-system nonlinear multiscale family OPEN; P versus NP OPEN.

**Peer requests:** TMR-1 check exact CNF grammar and uniform quantifiers; TMR-2 verify all-zero witness and counterfactual labels; TMR-4 import this first-read ingress matrix to a physical all-step LP without assuming a fused-halt row reachable; TMR-5 independently compile/attack the family recognizer and check nonlocal-access model changes. Next TMR-3 target is a nonaffine dynamic family where a **nonlinear** obstruction survives compact algebra, shared work and arbitrary polynomial workspace, beyond the inherently linear input-head diameter.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither proof tracker nor canonical root main.tex changed. Five existing schedules untouched. P versus NP remains OPEN.

## Reference

[1] E. Ben-Sasson and A. Wigderson, "Short Proofs Are Narrow: Resolution Made Simple," Journal of the ACM 48(2):149-169 (2001). https://doi.org/10.1145/375827.375835. Original published Resolution results apply to proof size and width, not arbitrary SAT-machine transition lower bounds.
