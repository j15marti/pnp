# Bounds: the zero-output atom limits average-min pseudoentropy
2026-11-21 10:59 PST, America/Los_Angeles.

**T5-ZERO-ATOM-MINENTROPY1 — PROVED/EXACT**, elementary target-specific obstruction; external independent review pending. For any distribution on valid encoded T5 instances with UNSAT probability p0, a 3N-gate test implies
Adv_B >= max(0,p0-2^(-k))
whenever a fake has average conditional min-entropy at least k and B>=3N. Thus (B,epsilon)-indistinguishability requires k<=-log2(p0-epsilon) when p0>epsilon. This holds even after imposing the full construction multiplier. It needs no SAT solver or quotient converter.

**FALSIFIED/RETIRED:** the concrete balanced, full-multiplier-supported fake below as an indistinguishable high-min-entropy pair. This does not retire all full-multiplier pairs, the one-bit target, or conditional Shannon pseudoentropy. **COMPUTATIONAL:** 8160 explicitly enumerated fake values and1125 exact probability-table checks passed; finite evidence is separate from the proof.

ONE next dependency: **T5-SAT-SLICE-PAIR1**, Bounds owner, Redteam review and Synthesis tracking. Construct a positive-output full-multiplier pair on a specified satisfiable-input distribution and prove its indistinguishability at the cap-facing circuit budget, or give an explicit small distinguisher. Removing the zero atom is necessary for growing average-min entropy, not evidence of hardness. Efficient conditioning/sampling is not assumed for free. This remains a counting path, not a decision separation.

## Quantifiers, circuit class and exact source
For EVERY N, EVERY distribution X on valid strict-C encodings of exactly N bits, and EVERY jointly distributed integer Ztilde in the per-input alphabet 0..5^{n(X)}, set Y=F_N(X), p0=Pr[Y=0]. Use ell=3N output bits with leading zeros. Define
g=E_x max_z Pr[Ztilde=z|X=x],
Hbar_inf(Ztilde|X)=-log2(g).
This is average conditional min-entropy, not the expectation of pointwise min-entropies.

Circuits have fan-in-two AND/OR, unary NOT, constants, arbitrary depth, fanout and DAG sharing; count noninput gates. Adv_B is the supremum absolute acceptance-probability difference for size-at-most-B circuits on the pair (X,z). Our circuit is uniformly constructible from N and ignores X. No sampling oracle is supplied to it.

Fix separately one total correct deterministic strict-C counter A and constants K>0,a>=1 independent of the input, under T_A(N)<=K N^a in the handoff's fixed-alphabet sole-tape model. All input/output, control/head and stored address information is charged. This lemma constrains a proposed pseudoentropy premise; it does not refute A's cap.

C comprises all permutations of012,123,234,340,401 over Z5,30 tuples. Ordered R means the first value beats exactly one of the other two, with i beating i+1 and i+3 modulo5; it has40 tuples and is not C. The conversion C(x,y,z)=R(x,y,z) AND R(y,x,z) changes clause count and is not performed here. No historical S/Q substitution.

The exact input is 1^n0 gamma(m+1) and m triples of one-based w-bit IDs, w=ceil(log2(n+1)):
N=n+2+2floor(log2(m+1))+3mw.
Since n<=N, 5^n<2^(3N), so the output padding suffices.

Four falsifiers:
1. The output atom test requires solving X or exceeds ell gates in the declared circuit basis.
2. Average conditional guessing probability is smaller than the fake's marginal zero probability.
3. The concrete fake violates the actual output alphabet or the full multiplier support.
4. The min-entropy ceiling is asserted for Shannon entropy, for p0<=epsilon, or as a decision lower bound.

## Proof and exact budget
Let D_0(x,z)=[z=0]. OR all ell bits with ell-1 binary OR gates and negate once. Thus size(D_0)=ell. Its true acceptance is p0 and fake acceptance q0=Pr[Ztilde=0]. For every x,
max_z Pr[Ztilde=z|x]>=Pr[Ztilde=0|x].
Averaging gives g>=q0. If Hbar_inf>=k then g<=2^-k, so
Adv_B>=|p0-q0|>=p0-q0>=p0-2^-k.
The nonnegative maximum gives the displayed statement.

Conversely, indistinguishability with epsilon implies q0>=p0-epsilon. If this is positive, g>=p0-epsilon and Hbar_inf<=-log2(p0-epsilon). For p0=1/2 and epsilon=o(1), the ceiling is1+o(1) bits. For example k>=2 forces advantage at least1/4. This DOES NOT rule out k=1 on a balanced distribution, nor even constant larger k on a sufficiently SAT-biased distribution. On all-SAT support p0=0, the bound is vacuous.

No input recognizer, hardwired exact-count solver, source-dependent variable shift or comparison with A is used. The distinguisher sees an output supplied as part of a pair, not an oracle answer it must obtain itself. It does not decide whether a given X is UNSAT. Calling it a fast SAT algorithm would reverse this interface.

The obstruction applies to all fake distributions on the declared alphabet, including correlated fakes. It is not merely an attack on independent noise. More generally a constant output atom can be tested by an equality circuit, but only zero is needed here. The result concerns the encoded count map's distribution, never a fixed-instance witness representation.

## Concrete full-multiplier pair on the new decision-sensitive image
Use Construction's NEW unweighted graph image B*_G=D(J_G), not the older weighted H_G. Its exact interface, at c5d8802644abe2caef15ef67153fa76ab8da1152, is
F_N(B*_G)=M #3COL(G), M=10*2^E,
E=10+9v+12e, n=55+48v+63e, m=65+58v+77e.
All target occurrences are at most five. This reduction's proof/evidence is a premise for the example, not independently recertified by this run. The general zero-atom lemma does not depend on it.

For every r>=0, let G_S=K2,3 plus r isolates, G_U=K4 plus r+1 isolates. Both have v=5+r,e=6. Use the published canonical clause generator/splitter, then the encoding above. Let X_r be uniform on these two valid N_r-bit images. Their labeled coloring counts are30*3^r and0: K2,3 has24 colorings with equal colors on its two-vertex side and6 with different colors; K4 has none. Isolates multiply counts by3. Thus p0=1/2.

Put k=v. Independently choose R uniform on {0,...,2^v-1} and define
Ztilde=M*6R.
For either input this has exactly2^v distinct equally likely values. Both H(Ztilde|X) and Hbar_inf(Ztilde|X) equal v, whereas the deterministic true answer has both entropies zero. Every fake is divisible by the FULL multiplier M and also by6M, so this is not the retired Y+10R low-bit experiment. The factor6 is consistent with the color-permutation symmetry of the nonempty edge-containing graph cores; it is not claimed to characterize possible counts.

The alphabet check is explicit. For v>=5,6*2^v<=3^v, so Ztilde<M*3^v. With e=6, E=82+9v and n=433+48v. Then
M*3^v=10*2^(82+9v)*3^v<2^(86+11v)<2^n<5^n.
No overflow, modular wrapping or discarded carries occurs. The true and fake outputs use exactly the same ell=3N padding.

D_0 accepts true pairs with probability1/2 and fake pairs with probability2^-v. Its advantage is exactly1/2-2^-v. At r=0, n673,m817,E127,N25203, k5, the advantage is15/32 using75609 gates. For increasing r, N is Theta(v log v); the fake entropy grows but this uniformly constructible O(N)-gate test defeats it. No need to parse E or divide by M.

The graph-pair generator is uniform; its T5 construction is polynomial with paid encoding expansion. The fake sampler uses v fair bits, shifts and constant multiplication on O(N)-bit words. This supplies no hard sampling premise. The pair is an explicit failed candidate, not a proposed hard input distribution.

## Entropy scope: why matching zero mass does not settle the route
A useful control preserves the decision label pointwise: on the UNSAT input output zero; on the SAT input output M*6R with R uniform on {1,...,2^v}. The same alphabet bound holds. D_0 then has zero advantage, while
H(Ztilde|X)=v/2,
Hbar_inf(Ztilde|X)=-log2(1/2+2^(-v-1))<1.
Thus large conditional Shannon entropy can coexist with a fixed zero atom. Neither matching zero mass nor the Shannon gap establishes indistinguishability; the two-input distribution is easy and other comparators can distinguish it. This control prevents an incorrect Shannon version of the lemma.

The existing exact-solver equality implication remains CONDITIONAL: an independently established (B,epsilon) pair with average-min entropy k and epsilon<1-2^-k would force C_F>B-O(N). For a fixed cap exponent a, B must be large enough to exceed the O_A(N^a log N) simulation ceiling plus comparator loss. No such pair is supplied. This run identifies an impossible combination of p0,k,epsilon before that expensive proof attempt.

## Reproducibility and original evidence
Code: experiments/t5_bounds_zero_atom1_20261121.py.
Raw: results/raw/t5_bounds_zero_atom1_20261121.json.
Run:
```
python experiments/t5_bounds_zero_atom1_20261121.py > results/raw/t5_bounds_zero_atom1_20261121.json
```
Code SHA256:0d8bd7bc0823c50c0779da1e674f79ad7252da1dda77c364922d254f5a6d2676.

The runner counts the two five-vertex graph cores directly over their243 labeled color assignments each. This small check is newly needed to instantiate the distribution, not a new whole-reduction audit. It then enumerates fake supports for r0..7 (8160 values), checks multiplier/alphabet/exact zero advantages and records n,m,N,E. It also exhaustively checks1125 two-input, three-output probability tables with quarter-grid probabilities and five input biases. Exact fractions are used; no seed or floating entropy estimate. The proof covers all N/r; these finite tables do not.

Original Construction generator was read in full, blob/source at c5d8802644abe2caef15ef67153fa76ab8da1152; original raw blob194d2bf5127715b9cf8c4b45f9ec0e8b9793b7b0 identifies its76-case local/reduction evidence and code SHA256 d0c1437cca6a8b1de2230514168eccb2f362a5c0434fee28630ec8521eb5e866. Expanded T5 assignments are NOT re-enumerated here. Fake values need only lie in the declared count alphabet, not be realized as counts of another T5 input.

## Complete resource ledger and controls
| Item | Charged treatment |
|---|---|
| Source parsing/authentication | X distribution is explicitly generated from valid images. An operational solver recognizing a shortcut must pay authentication; the output-only test needs no source recognition. Reading input in A's model remains charged. |
| Discovery/failed candidates | The rejected pair and all deployed recognition/search work are separate from solving F_N. No free count oracle, advice discovery or certificate. |
| Representation changes/adaptation | Full multiplier and output bits retained; no quotient conversion is charged because none is used by D_0. A's mode switches and alternate algebra remain legal and paid. |
| Queries/accesses/addresses | D_0 reads ell supplied bits, with ell gates. Circuit wire IDs require O(N log N) serialized bits. Tape traversal is not free random access. No virtual residual queries or forced original cuts. |
| Storage/sharing | OR reduction shares no duplicated demand. A's source, output, cache, buffers and physical addresses count together; actual shared storage is counted once. |
| Recomputation/output | Rebuilding discarded data costs work; exact fake arithmetic retains all carries. The test writes one output bit; A must write its complete exact count and terminator. |
| Uniform implementations | D_0 has a simple uniform gate generator; a sequential scan of the pair uses O(N) time and O(N) input-charged span, hence O(N^2) physical CM for THAT test. This is not A's execution. |
| Sampling/reduction | Use Construction's paid polynomial source-to-target generator; the simple fake sampler is polynomial. Input length is N_r, not v or graph-list length. |

For the same fixed A,N,K,a, retain S=O(N^a), physical CM=O(N^(2a)), minimum-description CM=O(N^(a+1)), count-map circuit size O(N^a log N). No lower demand exceeds these ceilings; no exponent is defeated. Fake entropy is not compulsory solver information.

Full-state entropy obstruction remains intact. Relocation and caching do not change zero output; no revisit is forced. Affine/Tseitin, private-leaf trees, matching cycles and forced domains remain legal cheap paths; the theorem does not infer hardness from width, state count or witness size. Renaming preserves exact count; complement changes zero mass and must be analyzed as its own count map. Decision-witness requirements are not inferred from color/frame multiplicity. SAT, UNSAT and UNKNOWN remain distinct. Hashes authenticate evidence bytes, not semantic merges.

DISJ: NOT APPLICABLE, no communication claim. Relativization: no nonrelativizing step; unrestricted transfer OPEN. Simultaneous DTISP: PASS for separate ledgers, no compulsory violation. Deterministic configurations: PASS for scope, no runtime lower bound from state counts. Natural Proofs/algebrization: no unrestricted lower-bound or barrier-bypass claim.

## Recovery, literature and official repository searches
Current base1274ba70556d11dcea569a65b728ba256f5f6f07. Freshly fetched complete current handoff, assignment, AGENTS,CODEX and research instructions; blobs match the prior complete continuous-session recovery (handoff a886f3387a8676b9cc86afbf3bebf22630109d49, SHA256 c9a3a0f362c72dfad7548b0cd44723853f105dcdc6a4f9ea5fef4559d3bb2a33). The baseline is not independently certified. Revisited exact C/R, encoding and sections16–19. Recovered Bounds10:01 report/handoff9cbefb89a5e94388e8bd6d9c234f89a538129cbc, Construction10:35 full proof/generator/raw, Synthesis10:28 full multiplier interface, and issue324 through Discovery comment7067611902. Discovery's typed simulation is not a premise here. Bounded repository search “zero atom min entropy” returned historical unrelated results, not this named lemma; no novelty claim.

Fresh literature queries: “average conditional min entropy guessing probability Dodis Ostrovsky Reyzin Smith fuzzy extractors”; “Vadhan Zheng2013 conditional pseudoentropy polynomial alphabet”.
Read [Vadhan–Zheng, March8,2013, ECCC revision3](https://salil.seas.harvard.edu/sites/g/files/omnuum4266/files/salil/files/eccc2013.pdf), Definitions2.6 and2.8–2.9 and polynomial-alphabet qualification. Its conditional definition there is Shannon entropy. Its sampling characterization cannot be imported for the exponentially large full-count range. Our min-entropy obstruction is proved directly, not attributed to a Shannon theorem.
Read the authors' [Dodis–Reyzin–Smith, Fuzzy Extractors survey, April9,2008, section2.1](https://courses.csail.mit.edu/6.857/2009/handouts/DodisReyzinSmith-FuzzyExtractors.pdf) for the explicit average guessing-probability definition. It is an author survey, not a newly checked extractor theorem; no extractor or chain-rule theorem is used.

Fresh connected GitHub query “conditional min entropy guessing probability” under anthropics,openai,xai-org,google,google-research,google-deepmind. Anthropic returned an irrelevant [eval question dataset](https://github.com/anthropics/evals/blob/84fcc677e52e1902d696c32cd1a6b663e70d3993/advanced-ai-risk/lm_generated_evals/self-awareness-training-nn-architecture.jsonl), commit84fcc677e52e1902d696c32cd1a6b663e70d3993. Google Research returned [numbert vocabulary](https://github.com/google-research/google-research/blob/87e25a5ba04d2c4cf0108f0cec96d648fe2b945a/numbert/model/vocab.txt), commit87e25a5ba04d2c4cf0108f0cec96d648fe2b945a. OpenAI,xAI,Google returned none. DeepMind initially returned429, then retry returned [code-verification deviations](https://github.com/google-deepmind/code-verification/blob/8c8d371f1962ac73435c8eb148678991f5c3470d/Computational/docs/DEVIATIONS.md), commit8c8d371f1962ac73435c8eb148678991f5c3470d; its cryptographic modeling snippets do not supply this count-map claim. These are snippet screens, not full-file/kernel audits.

Web fallbacks: site:github.com/openai “min entropy”; site:github.com/xai-org “entropy”; site:github.com/google-deepmind “conditional entropy”; site:github.com/google “min entropy”; site:github.com/anthropics “conditional min entropy”; site:github.com/google-research “conditional min entropy”. Returned xAI [sandbox entropy-device path](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-sandbox/src/paths.rs), DeepMind [quantum-capacity formalization issue](https://github.com/google-deepmind/formal-conjectures/issues/3417), and unrelated third-party repositories. None proves this finite classical counting lemma. No exhaustive absence claim, code import or formal build.

Official ownership is grounded in checks already recovered in this continuous session, not product-name inference: [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai) corporate-domain verification; [xAI corporate links](https://x.ai/open-source); [Google Research corporate link](https://research.google/pubs/implicit-rate-constrained-optimization-of-non-decomposable-objectives/); [DeepMind corporate repository link](https://deepmind.google/blog/open-sourcing-mujoco/); [Google OR-Tools](https://developers.google.com/optimization). Prior search logs prevented redundant deep review of unrelated claims.

## Publication and review
Publish only Bounds report/handoff plus uniquely named code/raw. No local repository checkout; preflight and LaTeX not run. No TMR ownership, manuscript, schedules or enabled states changed. This is the same continuous assistant session; external independent adversarial review remains pending.

Redteam/Synthesis: check the average-versus-pointwise min-entropy definition, zero-test budget, positive p0-epsilon condition, full-multiplier alphabet, and the explicit non-exclusion of one bit or Shannon pseudoentropy. The smallest correction to the failed strategy is to match output atoms and respect k<=-log2(p0-epsilon), or change the source distribution with its own paid/specified sampling model. Neither correction supplies indistinguishability.

Next dependency T5-SAT-SLICE-PAIR1 as above. **P versus NP remains OPEN.**
