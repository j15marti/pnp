# Bounds: split-family quotient noise leaks through raw output bits
2026-11-21 10:01 PST, America/Los_Angeles.
Named lemma **T5-SPLIT-QUOTIENT-RESIDUE1**.
**PROVED/EXACT** explicit distinguishing bound; **FALSIFIED/RETIRED** the additive quotient-noise pseudoentropy candidate below. Independent adversarial review pending. Unrestricted count lower bounds and P versus NP remain OPEN.

## Exact candidate and quantifiers
For every feasible pair v,e of nonnegative graph parameters, let Gamma_(v,e) consist of the explicit strict-C images B_G=D(H_G) of all simple v-vertex,e-edge graphs, using Construction's fixed generator. Put
E=10+3v+2e,
n=55+18v+11e,
m=65+20v+13e,
N=n+2+2floor(log2(m+1))+3m ceil(log2(n+1)).
Every member has this exact N. Let X have ANY distribution supported on Gamma_(v,e). Define Y=F_N(X)=Z_C(X), and Q=Y/10. For every integer1<=k<=E, independently sample R uniformly from {0,...,2^k-1}, and define
V=Q+R,   Ytilde=10V=Y+10R.
This is a concrete quotient-space fake, supported on multiples of ten in the original output alphabet. Both conditional Shannon entropy H(Ytilde|X) and average conditional min-entropy are exactly k; the true conditional entropy is zero. Efficient sampling of X or Ytilde is not assumed and is not supplied to a solver for free.

Use padded ell=3N binary output bits, indexed from0 at the least significant bit. The circuit class is arbitrary-depth, nonuniform fan-in-two AND/OR and unary NOT, constants and unrestricted fanout/sharing, charging noninput gates. For every integer budget B>=0,
```
Adv_B((X,Y),(X,Ytilde)) >= 1 - 2^(-min(k,B+1)).
```
At B=k-1 this equals total variation1-2^-k. In particular, one raw output wire (bit1), **zero noninput gates**, gives advantage1/2. If a convention charges the output buffer, add one gate. The circuits are also uniformly constructible, and do not inspect or solve X.

Fix separately any correct total deterministic sole-tape counter A and constants K>0,a>=1 independent of X, under the hypothetical cap T_A(N)<=KN^a. The displayed pair already fails epsilon-indistinguishability for epsilon<1/2 at the smallest circuit budget. It cannot supply the premise needed to contradict A's O_A(N^a log N) count-circuit ceiling. This is a failed candidate, not a new lower bound.

Four falsifiers:
1. A generator image whose true count is not divisible by10*2^E.
2. A fake outside0..5^n, a conditional probability collision, or unequal R multiplicities.
3. The specified output-bit OR test has a different acceptance probability after binary carries.
4. Noise restricted to multiples of2^E defeats this test; the report must not generalize failure to all quotient-supported fakes.

## Recovery, exact definitions and source evidence
Current head3168128105d8f040f41f8a49da8d6f0deffb9112. Retrieved current full baseline handoff, assignment, AGENTS.md, CODEX.md and repository research instructions, unchanged from their complete contents in this continuous workspace. Baseline blob a886f3387a8676b9cc86afbf3bebf22630109d49; the handoff's own models and review limitations remain in force. Publishing it was not independent certification.

Read the full latest [Bounds orbit report](https://github.com/j15marti/pnp/blob/3168128105d8f040f41f8a49da8d6f0deffb9112/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-21_091146_Orbit_Pseudoentropy.md), current handoff e3cb75aa647e32543c180ae63dfbcb639c18f803, and [Synthesis quotient-budget report](https://github.com/j15marti/pnp/blob/d18f513e02a053db9d30ee7172ee516834c152d3/research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-21_092400_Quotient_Budget_Bridge.md). They leave a lattice-supported pseudoentropy pair OPEN. The present pair satisfies the old mod10 filter and has a positive entropy gap, but fails an additional source-specific filter.

Original construction: [09:32 report and generator](https://github.com/j15marti/pnp/blob/8ae69ba65b79af7d3da945293eacb7bbf1ebe2d1/research/agents/charged-construction/PNP_Charged_construction_2026-11-21_093200_Full_Domain_Equality_Split.md). The exact equality-extension multiplier is2^E; the source H_G has a free ten-frame symmetry. Current [Accounting report](https://github.com/j15marti/pnp/blob/9f6787be1c19431c5848f0cc44f8e3ccd4b4a75c/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-21_094800_Orientation_Decoder_Obstruction.md), code and raw data provide an equal-length both-label control. Issue324 was read through Discovery comment7066859935. Discovery's small-group representation theorem is not a premise for this encoded-count result.

C is symmetric on Z5 with allowed unordered triples012,123,234,340,401 and all six permutations. Every clause has distinct names; no primitive signs, equality or constants. Ordered R has different semantics; it is not substituted. The input uses unary n, Elias gamma(m+1) and one-based fixed-width IDs, exactly as above. Historical S/Q results play no role.

## Proof
Construction gives Z_C(B_G)=2^E Z_C(H_G). H_G has at least the five anchor clauses. The ten color maps z -> s+/-z mod5 act freely on satisfying assignments: a nonidentity rotation has no fixed color; a reflection fixes only one color, whereas every satisfying clause uses three distinct colors. Thus10 divides Z_C(H_G), including zero. Therefore Y is divisible by10*2^E=5*2^(E+1).

For a fixed X, addition of the independent R and multiplication by10 are injective on its2^k possible values; every fake value has conditional probability2^-k. Both entropy notions are k. To check the alphabet rather than assuming it, let n_H=5+3v+e. Then n=n_H+5E,n_H>=5,E>=10, and
```
Ytilde < 2^E(5^n_H+10)
        < 2^(E+1)*5^n_H
        <= 5^(n_H+5E)=5^n.
```
Nonnegativity is immediate. Dividing by10 places V in0..floor(5^n/10). No modular wraparound or truncating count arithmetic is used.

For any1<=r<=k, define D_r(x,z) as the OR of raw bits1,...,r of z. True Y has all these bits zero. Every fake is even, and
(Ytilde/2) mod2^r = 5R mod2^r,
because Y/2 is divisible by2^E and r<=E. R mod2^r is uniform, and5 is invertible modulo2^r. Thus these r bits are jointly uniform; D_r accepts with probability1-2^-r. It uses r-1 OR gates, or zero gates for r=1. The fake's only overlap with the true value at each input is R=0, with probability2^-k, so the statistical distance is1-2^-k, attained by D_k. This proves the budget inequality and its tight endpoint.

No division-by-ten circuit is needed for this RAW count distinguisher. Merely examining the already supplied pair component is enough. This is stronger for this candidate than applying Synthesis's general O(N)-gate quotient converter.

The smallest corrected support requirement is: a fake on these images that hopes to be indistinguishable must avoid leaking mass into the forbidden low E bits of z/2. Full support on multiples of10*2^E passes this particular filter. For example Y+10*2^E R has zero advantage for every D_r with r<=E, when the resulting values stay in the alphabet. Its indistinguishability against other tests is NOT established. Dividing out the known multiplier is a normalization, not new hardness.

## Concrete both-label distribution and computational evidence
Take X uniformly on the two Construction images of K2,3 and K4 plus an isolate. Both have v=5,e=6,E=37,n=211,m=243,N=6059. H_G has n_H=26,m_H=21,N_H=351; these lengths are kept distinct. The true counts, recovered from Accounting's exact graph/source evidence, are9411819533762560 (SAT) and0 (UNSAT). Their quotient-by-ten values are941181953376256 and0.

For k=37 the fake has37 conditional entropy bits and passes mod10. Its raw output bit1 still gives advantage1/2, while36 OR gates give137438953471/137438953472. This includes both decision labels; it does not prove that deciding positivity is hard. The fake distribution is allowed to contain positive values when X is UNSAT; an actual exact-count solver must not.

Reproduce:
```sh
python experiments/t5_bounds_split_residue1_20261121.py > results/raw/t5_bounds_split_residue1_20261121.json
```
Code SHA2569036d0d3ab18ed77014558cb692b8d5be6648ede7b12c2a4cf91d3739864f82d.
Input evidence results/raw/t5_accounting_orientation1_20261121.json at9f6787be, SHA256529ac88423dcafccea48c735485bcf9e4283aff4a0dd0785d4b4d77e8519f4b9. It contains full original target clauses/encodings. Counts are explicitly reused, not independently re-enumerated here.

COMPUTATIONAL: enumerate16380 fake values across both sources and k=1..12; check all r=1..k, giving156 exact rational advantage rows, raw bit positions, gate counts, alphabet and mod10 assertions. The k37 row is the symbolic formula, not enumeration of2^37 values. No seed, no physical solver benchmark. This experiment tests the new construction multiplier and raw-bit distinguishing budget, not the old mod10 or parity experiment.

## Complete resource ledger and cap-facing consequence
| Component | Charge and scope |
|---|---|
| Pair/input source | X is an explicitly encoded valid input; Ytilde is the supplied second component of the distinguishing experiment. Computing F_N to define/sample it is not claimed free or efficient. |
| Source authentication | The theorem is distribution-promised. D_r intentionally ignores X; it need not recognize the entire image. Building or validating source instances elsewhere reads all actual syntax and pays Construction's compiler costs. |
| Distinguisher discovery | Fixed formula and fixed bit positions from r; uniform circuit generator O(r log(ell+1)) bit output for wire labels. No source-dependent advice or search. |
| Circuit evaluation | r-1 fan-in-two OR gates, r input wires, one output, arbitrary sharing allowed. Bit0 is deliberately skipped. |
| Physical access | A tape implementation on the supplied pair must move to the output coordinates, costing up to O(N+ell), plus r reads and label output; circuit wires do not imply free tape random access. Input-charged S O(N+ell), conservative physical CM O((N+ell)^2) for this separate scan execution. |
| Queries/failed candidates | No count queries in D_r; no runtime trial candidates or adaptive modes. |
| Representation/arithmetic | No physical quotient conversion in D_r. The distribution's mathematical addition/multiplication is not an algorithm for A. |
| Storage/sharing/recompute | Scan accumulator is one bit plus position/control; retained original pair is charged. No materialized witness relation, cache or repeated residual service. |
| Output | One distinguish bit, not an exact count or decision certificate. Pair values remain full padded binary words. |
| Descriptive CM | Separate replay bound O(T(L+log T)) with L the actual pair length; not identified with the solver's physical CM or with output entropy. |

For fixed A,K,a on ORIGINAL X length N, retain S_A=O(N^a), physical CM_A=O(N^(2a)), minimum-description CM_A=O(N^(a+1)), and count-map circuits O_A(N^a log N). No demand exceeds these ceilings. The distinguishing input has length N+ell, not a silently changed solver input regime.

Synthesis's implication “adequate entropy plus (B,epsilon)-indistinguishability implies count-circuit demand>B-O(N)” remains CONDITIONAL and correct under its stated hypotheses. This candidate fails its indistinguishability premise already for B=0 and epsilon<1/2 (under the stated gate convention). A rejected fake says nothing about the existence of other successful fakes. It excludes no fixed polynomial exponent and supplies no decision P-versus-NP separation.

## Controls and scientific gates
The support theorem is algebraic and source-specific, not witness-width or state-count based. Shared variables and both labels are explicitly covered. Relocation, renaming, caching and recomputation do not change numeric divisibility; no source-bit restriction invariant is presumed under renaming. Affine/Tseitin, matching cycles, private-leaf trees and forced-domain formulas retain legitimate cheap evaluators after splitting; the test remains valid wherever the same known multiplier applies. Complementing a predicate changes its count by a scoped subtraction; do not assume the resulting value remains in Gamma without verifying its encoding. Native complement is not forbidden. Full-state output entropy remains zero; the fake's entropy is not actual computation.

DISJ: NOT APPLICABLE, no direct-sum claim. Relativization: no nonrelativizing lower bound; unrestricted bridge OPEN. Simultaneous DTISP: PASS for separation of executions/measures; no mixed tradeoff. Deterministic configurations: PASS, no state-count runtime inference. Natural Proofs/algebrization: no general circuit lower-bound claim. SAT/UNSAT are exact for the two sources; unproved indistinguishability remains UNKNOWN/OPEN, not a positive result.

## Fresh primary literature and official repository searches
Queries: “Vadhan Zheng pseudoentropy conditional deterministic function output range”; “site:github.com/anthropics pseudoentropy”; corresponding OpenAI query; connector org searches “pseudorandom entropy counting” under xai-org,google-research,google-deepmind and “pseudoentropy pseudorandom” under anthropics,openai.

Read [Vadhan–Zheng full version](https://salil.seas.harvard.edu/sites/g/files/omnuum4266/files/salil/files/eccc2013.pdf), March8,2013, ECCC TR11-141 revision3, Definitions1.1/1.2 and Theorem1.3 with its alphabet qualification. Conditional pseudoentropy requires both indistinguishability and conditional entropy. The sampling equivalence's polynomial-alphabet restriction is not applicable automatically to exponentially ranged counts; the paper also describes a distinct nonuniform large-range measure formulation, not imported here. This run uses a direct explicit circuit, with no cryptographic or hardness premise.

Bounded official-repository results:
- Anthropic and OpenAI connector queries returned no matches for the exact pseudoentropy query. Web fallback returned OpenAI math overview entropy entries and reinforcement-learning entropy code, none an applicable strict-C pseudoentropy construction. These are not exhaustive absence claims.
- xai-org and google-deepmind query returned no matches.
- google-research returned google-research/anthea/anthea-eval.js at87e25a5ba04d2c4cf0108f0cec96d648fe2b945a: random-seed warmup/entropy comments in evaluation tooling, not a complexity theorem. Snippet screened and rejected; no code imported.
Official ownership checks retained from this continuous session: corporate-domain verification on [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai), official [xAI repository link](https://x.ai/open-source), [Google Research link](https://research.google/pubs/implicit-rate-constrained-optimization-of-non-decomposable-objectives/) and [DeepMind link](https://deepmind.google/blog/open-sourcing-mujoco/). No product-name-only repository was treated as official. No external kernel/repository build or unverifiable headline theorem used. Prior logs prevented redundant deep review; searches were fresh and task-specific.

## Next dependency
ONE next dependency **T5-FULL-MULTIPLIER-PAIR1**, owner Bounds, Redteam review, Synthesis tracking: normalize away10*2^E on this image and specify a fake for the remaining graph count quotient with independently proved distinguishing budget beyond the fixed cap, or produce an explicit falsifier. No free choice of a hard count distribution and no inference from entropy alone.

No TMR manuscript edits, schedule/enabled-state changes, local checkout/preflight or LaTeX build. Symbolic theorem and computational evidence remain separate. P versus NP OPEN.
