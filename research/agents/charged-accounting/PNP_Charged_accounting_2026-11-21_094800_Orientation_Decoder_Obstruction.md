# Accounting: auxiliary orientation is not an actual decoding obligation
2026-11-21 09:48 PST, America/Los_Angeles.

## Claim, quantifiers, outcome
**T5-ORIENTATION-OBLIGATION1: FALSIFIED/RETIRED** as a proposed compulsory demand. This is a candidate tested here, not a claim attributed to Construction. **PROVED/EXACT**: the decoder obstruction below. Independent adversarial review pending.

Fix any correct total deterministic strict-C decision solver or exact counter A in the handoff's input-charged sole-tape model; fix K>0,a>=1 and, conditionally, T_A(N)<=KN^a. Fix any satisfiable source F, its occurrence-split image X=D(F), and a satisfying source assignment w. Construction supplies E=3m-u independent two-way auxiliary frame extensions of w. Let U be their uniformly independently sampled E-bit orientation vector. U is sampled externally and is NOT part of X. For every record Pi obtained as a deterministic function of A's actual trace, including adaptive event indices, addresses, cached state and arbitrary relocation, and every side information B determined by X,w, that trace, and fixed parameters:
```
H(U | B,Pi)=E,    I(U;Pi | B)=0.
```
Thus no exact decoder d(B,Pi)=U exists when E>0, even with unlimited computation and the whole trace. Every deterministic guess succeeds with probability exactly 2^-E. Proof: X and w are fixed; the trace and every such record are independent of U. Conditioning on them leaves the uniform orientation distribution unchanged. The same reasoning applies conditional on each sampled X,w if U is sampled independently afterward.

This falsifies assigning one compulsory dynamic bit per auxiliary orientation. It does not falsify the reduction, the count multiplier, or possible obligations involving the actual graph core. Counting separation alone is not decision separation; P versus NP remains OPEN.

Falsifiers: (1) encode U into the actual input or supply its randomness to the solver, which changes the experiment; (2) show a genuine required service that exposes the externally requested U, rather than merely some witness; (3) reconstruct U from identical actual traces without additional information; (4) find a canonical fixed orientation that fails to lift a satisfying source assignment. The first two are changes of premise, not counterexamples to the independence theorem.

## Recovery, exact model and source
Recovered the current baseline, assignment, AGENTS.md, CODEX.md and repository research instructions, plus the full current Accounting report/handoff and original timing experiment code/raw. The handoff blob is a886f3387a8676b9cc86afbf3bebf22630109d49; its model-specific claims are not independently certified by recovery. The entire handoff, including appended programs, was available in the continuous workspace; current full contents were retrieved and the target sections reread. Existing Accounting handoff blob b59851f7ec0e4b14e320f78cf053c203f7d2bddc.

Source revision: [Construction 09:32](https://github.com/j15marti/pnp/blob/8ae69ba65b79af7d3da945293eacb7bbf1ebe2d1/research/agents/charged-construction/PNP_Charged_construction_2026-11-21_093200_Full_Domain_Equality_Split.md), generator and raw evidence at the same commit. Current issue324 was read through comment7066621150. That report explicitly permits equality contraction. The present test supplies a concrete failed decoder on its new bounded-occurrence family; it does not repeat the prior timing experiment or Construction's full gadget suite.

C allows all permutations of 012,123,234,340,401. Names within a clause are distinct; domains start as Z5. Ordered R is distinct and unused. Exact encoding is unary n followed by gamma(m+1) and 3m one-based IDs of width ceil(log2(n+1)):
N=n+2+2floor(log2(m+1))+3m ceil(log2(n+1)).
No S/Q substitution.

Construction's Q(U,V) comprises a five-variable frame b0=U plus C(b4,V,b1), with four fresh auxiliaries. For fixed U=V=s its two extensions are bi=s+i and bi=s-i modulo5. Each occurrence path enforces equality. D(F) has n'=n+15m-5u,m'=19m-6u and count2^E Z(F). These semantic identities, rather than hash equality, support the audit.

## Smallest local obstruction and both-label control
With two source clauses C(x0,x1,x2),C(x0,x3,x4), n=5,m=2,u=5,E=1. This minimizes m for a positive link count and then n' for two clauses with E>0. The split image has n'=10,m'=8,N'=114. Its full clause list (zero-based IDs) is:
```
(0,1,2),(3,4,5),(0,6,7),(6,7,8),
(7,8,9),(8,9,0),(9,0,6),(9,3,6).
```
Two valid witnesses projecting to the same source witness are
(0,1,2,0,1,2,1,2,3,4) and (0,1,2,0,1,2,4,3,2,1).
A solver sees exactly the same input regardless of which witness an external experiment samples. Its trace cannot identify that sample. This is an exact finite counterexample to the proposed decoder, without claiming an optimal solver runtime.

For the decision-sensitive graph family, use v=5,e=6 and either K2,3 or K4 plus one isolate. Original H_G has n=26,m=21,N_H=351. Both split images have n'=211,m'=243,E=37,N_B=6059, degree at most5. K2,3 has30 proper three-colorings, strict-C source count68480, and target count9411819533762560; K4+isolate is UNSAT with both counts0.

A uniform two-input distribution therefore contains both decision labels at one exact encoded length. Conditional on the SAT input and a fixed valid projected witness, all37 orientation bits remain independent of the solver trace. On UNSAT define U=bottom. Then H(U|X,trace)=37/2 for the mixture. This does not demand that a witness exist on UNSAT. The universal obstruction already holds on the SAT member.

Choosing every orientation positive gives a valid canonical lift; its orientation entropy is zero. Uniform sampling instead requires fresh random bits. An independent sampler may generate a valid random witness, but cannot recover an independently specified external sample. Supplying that sample in B makes the purported demand zero. Supplying it through a paid input/randomness channel changes the task from scalar decision/counting to sampling or transmission.

## Correct accounting and cap comparison
For actual obligations U_j,B_j, selected actual event indices I_j, q_j=|I_j|, b-bit payloads P_j and extra metadata Z_j, exact decoding is a prerequisite:
```
H(U_j|B_j,I_j,P_j,Z_j)=0.
H(U_j|B_j) <= H(I_j|B_j)+H(Z_j|B_j,I_j)+b E q_j.
sum_j H(U_j|B_j) <= sum_j [H(I_j|B_j)+H(Z_j|B_j,I_j)] + br E T.
```
The first inequality follows from exact reconstruction and the entropy chain rule; the second requires pathwise event reuse at most r. Decoder computation is not automatically an event of A: any claimed implemented service must pay its reads, computation and output. Explicit indices/addresses normally cost O(log(N+T)) bits per event under the cap; selectors cannot depend on unobserved U for free.

For the orientation candidate one may take a single joint obligation with B=(X,w), I all actual transitions, and P their complete fixed-alphabet transition descriptions. Then q=T,r=1; the entire trace still does not decode U. Including recorded absolute addresses and times does not repair independence. No finite b or overhead makes the exact-reconstruction premise true. Substituting E into the entropy-transfer inequality is therefore invalid.

A corrected demand for actual graph information would have to exceed
brKN^a plus all selector/header entropy on the SAME distribution and run. None is supplied. Moreover E=O(N), so even a real E-bit service alone would not defeat every polynomial cap. Keep S=O(N^a), physical CM=O(N^(2a)), descriptive CM=O(N^(a+1)), and count-map gates=O(N^a log N) distinct. N_B=6059 and N_H=351 are not interchangeable resource inputs.

## Resource ledger and controls
| Item | Charge/status |
|---|---|
| Parsing and source authentication | Read actual unary/gamma/ID fields; validate strict syntax and exact graph/gadget structure. Hashes only check file integrity. |
| Discovery/failed candidates | Fixed orientation candidate tested; a general recognizer's failed matches and fallback must be paid. No free graph/equality oracle. |
| Representation change | Occurrence maps, equality contraction and source reconstruction are physical operations; Construction gives a conservative O(U^4)-time,O(U)-space scan compiler with U=N_H+N_B+2. This is an upper envelope, not solver timing. |
| Access and addresses | Actual tape moves charged. Any stored trace carries values, indices, framing and addresses. No free original-input oracle or clock. |
| Retention/sharing/recomputation | Input, map and live output count simultaneously. Cached contraction may be shared once; rereads and regenerated maps cost again. |
| Decoder | No decoder exists for independent U. An external sampler's E random bits cannot be credited as solver-produced information. |
| Witness output if requested | Explicit lift has O(n') color entries; construction and checking cost paid, conservatively within O(U^4),S O(U),physical CM O(U^5) for a scan implementation given the source witness. Finding that witness is not included or asserted easy. |
| Scalar output | Decision bit or exact binary count only; no mandatory witness/orientation output. |
| Description CM | Original input/time not free; separate reconstructible-configuration bound O(T(N+log T)), not physical residency. |
| Tests | Python semantic checks, no instrumented sole-tape trace or all expanded assignments. |

Relocation cannot correlate a deterministic trace with independent randomness. Full-state entropy of the actual answer remains zero. Renaming and reflection preserve the lift semantics; both were checked. Complement and caching are legal shortcuts, not excluded. Equality contraction leaves the original core; private-leaf trees, matching cycles, affine/Tseitin and forced-domain sources retain their cheap algorithms. Witness multiplicity cannot be converted into a decision witness-packing claim.

DISJ: NOT APPLICABLE, no communication lower bound imported. Relativization: PASS for independence obstruction, no nonrelativizing separation claimed. Simultaneous DTISP: PASS for scope, no mixed-execution demand; unrestricted lower-bound gate OPEN. Deterministic configurations: PASS, whole trace remains a function of input; state count is not work. Natural Proofs/algebrization: no circuit-hardness theorem or barrier bypass asserted.

## Evidence and fresh sources
Run:
```sh
python experiments/t5_accounting_orientation1_20261121.py > results/raw/t5_accounting_orientation1_20261121.json
```
Code SHA256 ffec525899c8dab9e1397033b7c5dc637c279810bc69e1a844049f35ade71eff.
Pinned dependency experiments/t5_construction_occurrence5_20261121.py, SHA256 830f2bf2a15a6282017701f527c6cea082a4d83360865aefd3a593a089b37cfb at8ae69ba.
COMPUTATIONAL: all3^5 color assignments on each of the two graphs;256 distinct first-eight-bit lifts plus37 single-coordinate flips; canonical witness, reflection and renaming checks; exact encoding round trips; the two minimal witnesses. Full expanded counts are derived by the proven multiplier and private-leaf sum, not brute force. No random seed. Executed stage0.18 seconds, not a complexity benchmark.

Fresh literature query: “Patrascu Demaine information transfer entropy cell probe queries lower bounds”. Read [Pătraşcu–Demaine, SICOMP2006 author PDF](https://erikdemaine.org/papers/DynamicConnectivity_SICOMP/paper.pdf), introduction and section5.4 encoding argument, with section6 contrast. Their record uses addresses and contents of cells read in the query interval and written in the update interval; actual required operations permit reconstruction. This supplies no compulsory residual-query service for a static T5 counter. No cell-probe exponent is transferred to the sole-tape model. The obstruction above is proved directly.

Fresh official GitHub searches, query “SAT witness sampling” with each org:
- anthropics: claude-cookbooks/misc/sampling_past_max_tokens.ipynb at8ad5de647d4f0f50c95d74aabc8aa20a3f70cdd3; returned story/sampling fragments are unrelated.
- openai: math/preprints/Perfect-completeness-for-2-to-1-games-September-23-2026/build/03-sampling.tex at4eaee87548250b2682affda7d05d947c05554bae; finite-game witness choices are not an actual T5 solver service. Snippets only; no theorem imported.
- xai-org: no returned matches in this bounded query.
- google-research: google-research/numbert/model/vocab.txt at87e25a5ba04d2c4cf0108f0cec96d648fe2b945a; vocabulary coincidence rejected.
- google-deepmind: code-verification/Computational/docs/DEVIATIONS.md at8c8d371f1962ac73435c8eb148678991f5c3470d; sampling/verification fragments concern other specifications, not this obligation.

Web fallback queries “site:github.com/anthropics witness sampling entropy” and corresponding OpenAI query returned no applicable strict-C theorem. These searches are not exhaustive absence claims. Official ownership checks from this continuous session: verified corporate domains on [anthropics](https://github.com/anthropics) and [openai](https://github.com/openai); [xAI official link](https://x.ai/open-source); [Google Research official repository link](https://research.google/pubs/implicit-rate-constrained-optimization-of-non-decomposable-objectives/); [DeepMind official repository link](https://deepmind.google/blog/open-sourcing-mujoco/). Ownership is not theorem verification. No external kernel or repository build was run.

## Next dependency and publication scope
ONE next dependency: **T5-CORE-SERVICE1**, owner Accounting, Redteam review, Synthesis tracking. Supply a source-dependent graph-core variable and an actual service/decoder compulsory for every fixed correct solver after equality contraction, with all source/cache side information and bounded reuse. Independent witness randomness is excluded. The broader T5-BOUNDED-3COL-DYNAMIC1 remains OPEN.

No TMR manuscript edits, schedules or enabled-state changes. No checkout/preflight/LaTeX build. Current-head-protected publication and exact readback are required; independent review has not occurred.
