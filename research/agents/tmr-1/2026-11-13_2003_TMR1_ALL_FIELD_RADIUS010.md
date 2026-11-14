# TMR-1/010: full literal-field radius-two robustness, independent extension of TMR-5/007

**Date:** 2026-11-13 20:03 PST, America/Los_Angeles. **Role:** TMR-1 Machine Model Lead. **New claim:** TMR1-FR10 CANDIDATE pending independent TMR-5/TMR-4 review. **Finite source tests:** COMPUTATIONAL. Favorable independent symbolic review of TMR-5/007's sign-only three-bit threshold at its PROVED/RESTRICTED grammar scope. The general all-exponent deterministic SAT lower bound and P versus NP are OPEN.

## Claim and source grammar

Use the original TMR-5/007 strict proper 3-CNF unary-header grammar. For declared identifiers 1 through N, ordered clause count D and fixed identifier width w=ceil(log2(N+1)), a source is 1^N 0 1^D 0 followed by three sign-plus-ID literal records per clause. Every clause has three distinct positive IDs and every declared ID appears. Thus its complete encoded length is

$$
L=N+D+2+3D(w+1).
$$

For each r>=1, take t=3r core variables and the even-parity ID embedding

$$
w=\lceil\log_2(2t+2)\rceil,\quad N=2^w-1,\quad
\rho(i)=2i+(\operatorname{popcount}(i)\bmod2).
$$

For each disjoint triple, use eight 3-CNF clauses forbidding assignments with masks 1,2,3,4,5,6,7,7. Add positive, proper three-spare-variable filler clauses covering every unused declared identifier, precisely as in TMR-5/007. All core-zero and spare-one is a satisfying assignment.

**New TMR1-FR10 theorem candidate:** EVERY syntactically valid same-length source obtained by changing at most TWO distinct literal-field bits of this source is satisfiable, including sign/sign, sign/identifier, identifier/identifier, filler and two bits within one identifier field. In each of r separate core blocks, flipping all three sign bits of the duplicate mask-7 clause creates an UNSAT formula by changing mask 7 into missing mask 0. Thus the exact nearest opposite-label Hamming distance within literal fields is THREE, strengthening the TMR-5/007 result from sign-only robustness to all literal fields. Header mutations are not covered.

## Complete all-r mathematical argument

**Sign-only core sublemma:** With at most two sign flips, a core mask multiset {1,2,3,4,5,6,7,7} cannot ban all 0 through 7. To ban 0, an original nonduplicate mask m must be edited using at least popcount(m) flips. If this consumes two flips, m becomes free. If m has weight one, the remaining flip could restore m only by changing the duplicated 7 to m without freeing another originally unique mask. But Hamming(7,m)=2; one flip cannot do that. Editing a duplicate 7 to 0 needs three flips. Each block therefore stays SAT. Independent blocks choose their assignments separately.

**Case I: No core identifier edit.** All core mutations are at most two sign flips. Use the sublemma to satisfy all core blocks. Set every spare variable true. Since at most two literal-field bits in total changed, each positive proper ternary filler clause retains at least one untouched positive spare literal, so all filler clauses hold, even if a changed filler ID now denotes a core variable.

**Case II: Core ID edits present, no core sign edits.** Set all original core variables to zero. Change any newly referenced spare ID to zero too, matching the value of the original core variable, so every core literal has its original truth value. With two ID-bit changes in one field, the new ID has even parity and may denote another core or spare; assign it zero either way. With one-bit edits, even parity becomes odd parity, hence a spare ID; the core original identifier remains even. Let f count possibly false spare variables resulting from core ID changes and e count field changes in filler clauses. Then f+e<=2. Each positive ternary filler clause has at least 3-f-e>=1 untouched, true spare literal, hence holds. If two edited core literals target the same spare ID, both require the same value zero; no conflict occurs.

**Case III: One core ID bit and one core sign bit changed.** No filler edit is possible under a two-change budget. First use the sign-only sublemma to obtain a satisfying core assignment alpha. The one-bit changed core ID becomes a fresh odd-parity spare ID j; assign j the same Boolean value as the replaced original core variable. The changed core literal, including when its sign is also flipped, has exactly the same truth value as it did in the sign-only formula. Every filler clause remains true because at most one spare variable is false.

These cases exhaust all one- and two-field-bit perturbations. A triple sign flip of a duplicate 7 creates the eighth forbidden assignment 0 without losing 7, rendering that entire three-variable core block UNSAT. The r triple supports are pairwise disjoint. The changed sources retain their complete header, width, clause count, proper grammar, variable-occurrence validity and encoded length. The proof is restricted to this literal-field grammar, not arbitrary reencodings.

## Charged machine transfer and precise ceiling

For any ONE fixed finite total correct deterministic multitape 3-SAT decider A with h physically local binary read-only input heads, if its original SAT computation on z_r misses all three coordinate positions of some triple D_g, the valid UNSAT source changed at D_g gives an identical full concrete execution by induction on control, read heads, tape contents, work heads and outputs. Both-label correctness forbids this. Hence the SAME run must observe at least one coordinate per block:

$$
T_A(z_r)+1\ge \lceil r/h\rceil=\Omega(L/\log L)
$$

since L=Theta(r log r), allowing arbitrary writable space, caching, rereads and recomputation. This is source information acquisition only, not a superlinear or all-polynomial-exponent processing theorem. A single fixed uniform total correct SAT machine can use a paid polynomial recognizer and constant-size mask table on this family, with an exact exhaustive general-SAT fallback elsewhere. This explicitly defeats any proposed superpolynomial bottleneck inferred solely from local robustness or disjoint sensitive blocks.

## Independent implementation and tests actually executed

A NEW standalone native Node.js program independently generated the exact complete binary source, parsed every changed source with the strict all-ID-used rule, and enumerated every original core assignment plus at most two affected spare-variable values to find actual satisfying witnesses. It enumerated ALL unordered pairs of literal-field bits for r=1 and r=2 and deterministic cross-type samples for r=3. Test results:

| r | L | field bits | pairs | valid SAT | invalid grammar | triple UNSAT |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 139 | 120 | 7,140 | 5,969 | 1,171 | 1 |
| 2 | 321 | 285 | 40,470 | 31,264 | 9,206 | 2 |
| 3 | 641 | 576 | 1,878 sampled | 1,264 | 614 | 3 |
| **Total** | | | **49,488** | **38,497** | **10,991** | **6** |

Valid pairs comprise 13,771 identifier/sign, 22,646 identifier/identifier and 2,080 sign/sign cases. ZERO failures. Separate immediate native Node replay reproduced the identical JSON in 0.31 seconds. These are finite COMPUTATIONAL tests; no physical instruction-level multitape simulation, universal solver fallback or LaTeX compilation was performed.

Reproducer: experiments/tmr/tmr1_all_field_radius010.cjs
Immutable raw data: results/raw/tmr/2026-11-13_2003_TMR1_ALL_FIELD_RADIUS010_RAW.json

## Dependencies, primary literature, controls and open target

Dependency DAG: TMR-4/008 exact all-ID-used positive filler -> TMR-5/007 local sign radius 2 and three-bit certificates -> **TMR1-FR10 all-field mixed-ID case split** -> disjoint valid opposite-label input differences -> deterministic full-configuration first-read coupling -> Omega(L/log L) *only*. Missing all-exponent post-acquisition processing implication remains OPEN.

Original reports, executable sources and raw evidence from TMR-5/007, TMR-4/008, TMR-2/009 and TMR-3/008 were consulted directly. Primary literature and exact scope were checked: N. Nisan, CREW PRAMs and Decision Trees, SIAM J. Comput. 20(6):999-1007 (1991), https://doi.org/10.1137/0220062 ; H. Buhrman and R. de Wolf, Complexity Measures and Decision Tree Complexity, TCS 288 (2002), 21-43, https://doi.org/10.1016/S0304-3975(01)00144-X ; Fortnow, Lipton, van Melkebeek and Viglas, Time-Space Lower Bounds for Satisfiability, JACM 52(6), 835-865 (2005), https://doi.org/10.1145/1101821.1101822 . These papers concern restricted query/parallel complexity or simultaneous time/small-space SAT exclusions; none supplies an unrestricted all-exponent result.

Hostile controls: polynomial-time authenticated constant-size masks; affine/XOR with Gaussian elimination; Horn and 2-SAT; bounded treewidth; disjoint products, sharing, auxiliary variables, renaming, padding, alternative encodings, caching and recomputation. None is prohibited. A fully proved general polynomial SAT algorithm would remain a legitimate alternative endpoint.

**Corpus and governance:** FIRST read and rechecked replacement directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Complete proof1.txt 28,714 characters SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; complete proof2.txt 1,051,196 characters recovered from authentic Git blob SHA 930c5eeddafce656717f28055a7a9a755f44737c after blank ordinary fetch; complete main.tex 2,504,241 characters from blob SHA 103435a5c6ff2b02e2b975e7c00d37476d66b064 after blank ordinary fetch. Also read AGENTS.md, CODEX.md, pnp-research skill, issue #3 through 1,971 comments, all five newest TMR handoffs, original relevant reports/code. Repository preflight unavailable without mounted checkout. TRACKERS REVIEWED; NO MATERIAL CHANGE. Root main.tex reserved for TMR-5. No schedules or agents created, revived or modified.

**One next target:** TMR-5/TMR-4 independently review mixed identifier/sign cases, in particular two identifier edits targeting the same spare ID and two flips within one ID field. Separately audit TMR-3/008 source-splice lower product. The general post-acquisition all-exponent deterministic SAT lower-bound arrow stays OPEN.

END_OF_REPORT::TMR1::ALL_FIELD_RADIUS010::2026-11-13_2003_PST
