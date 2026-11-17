# CLOCKMASKEDINVERSE22: PSPACE-hard forced-bit inversion with a trivial image language

Date: 2026-11-17 15:33 PST / 2026-11-18 08:33 KST.
Status: PROVED/EXACT for the declared restricted family; independent mathematics review OPEN. P versus NP OPEN.
Named dependency: INVERSION-VERIFIER-SEPARATION22.

## PROPOSE: falsifiable branches

(A) Does recognizing a target image in P imply polynomial-time, or even jointly PH-low, uniform source-preimage-bit extraction?
(B) Does authentic copied provenance prevent cheap alternative source circuits?
(C) Does a full-source, genuinely ordered nonlinear feature force hard image fibers?
(D) Does a near-linear source-to-target compiler plus a low verifier automatically transfer an MCSP time lower bound?

The construction below supplies a precise counterexample to B, C and D, and a PSPACE-completeness barrier to A. It does **not** separate PSPACE from P. Relevant recovered corpus includes LOSSY_PROMISE_CASCADE6, PARTIAL_SAMPLE_WEDGE7, PROMISE_CASCADE_FIXEDPOINT8, K_ELIMINATION_TRANSFER4, CLOCKSAT1, CLOCKFEATURE5, CLOCKSEED9, CLOCKEXCEPT10, CLOCKPARITY12, SOURCEQUERY_SYNTHESIS10, PUBLICSEED_PLOTKIN14, CLOCKHIST18, CLOCKKGRAM19, CLOCKSTREAMPROVENANCE20, CLOCKSTATEINVERSE21 and CANONICAL-WITNESS-TRAP9. Governance: AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md and the November 15 end-to-end directive.

## Authentic source and quotient

For m >= 3 set n=m+3 and N=2^n. The authentic N-bit truth-table source is f=D||a||h, where D has m bits, a is the bit at address m and h has N-m-1 bits. Let V(D) denote TQBF on the standard fully quantified Boolean formula described by D, with malformed descriptors assigned zero. Define the ordered adjacency Q(h)=OR_{i<|h|-1}(h_i AND h_{i+1}). Let

    H_m(f) = (D, b=a XOR V(D), q=Q(h)).

Its output has m+2=n-1 bits, and copied D is real source provenance. This is a fixed clock-independent deterministic map. Standard TQBF is PSPACE-complete [1].

## THEOREM 22.1: trivial existential image, PSPACE-hard universal inversion bit

For every m, image(H_m)={0,1}^{m+2}. To realize any y=(D,b,q), choose a=b XOR V(D), choose h=0^(N-m-1) when q=0, or h=11 0^(N-m-3) when q=1, and copy D. Consequently image membership is a trivial legal-length check in P.

However, for **every** f in H_m^{-1}(D,b,q), the source bit f[m] equals b XOR V(D). Any uniform function that, for every image y and address i, computes the ith bit of *some globally consistent correct* preimage necessarily decides TQBF via the single query i=m,y=(D,0,0). This is PSPACE-hard under polynomial reductions. A canonical inverse-bit function is in PSPACE, so its distinguished-bit decision problem is PSPACE-complete. A polynomial-time uniform inverse would imply P=PSPACE. A fixed-PH inverse would imply PH=PSPACE. Neither follows from P=NP.

This is a search-versus-recognition barrier, not an unconditional P-versus-PSPACE separation or an all-preimages circuit-hardness theorem.

## THEOREM 22.2: supplied-circuit equality PSPACE-complete despite the easy image

Let EQ={(C,y): H_m(TT(C))=y}, with an explicitly given n-input Boolean circuit C and legal y of length m+2. EQ belongs to PSPACE: enumerate source addresses, evaluate C, preserve D, a and adjacency, and evaluate V(D) in polynomial space.

For hardness, construct in poly(m) time an n-input point-indicator DNF C_D whose truth table stores D at the first m positions and zero elsewhere. Then H_m(TT(C_D))=(D,V(D),0). The equality test against (D,1,0) decides TQBF. Thus EQ is PSPACE-complete. This shows why a low existential image verifier cannot be substituted for a low supplied-witness evaluator.

## THEOREM 22.3: low-circuit sections and mixed source MCSP fibers

The witness from theorem 22.1 has at most m+3 one-bits and is realized by a point-indicator DNF of CC <= C(m+3)(n+1)=O(n^2). The choice of bit a may require PSPACE to compute *uniformly* from y, but the per-label circuit exists nonuniformly.

For q=1, fixing the header D, bit a, and initial suffix 11 leaves N-m-3 free source positions. The same target fiber therefore has 2^(N-m-3) truth tables. For 0<beta<gamma<1, the number of n-input functions with circuit size at most N^gamma is <=2^{O(N^gamma log(N+n))}=2^{o(N)}. For sufficiently large m every such fiber contains both a source YES with CC <= N^beta and a source NO with CC > N^gamma. Hence two-sided MCSP promise purity FAILS even though source-bound provenance is authentic, Q is nonlinear/order-sensitive, the compiler is near-linear, and the target image verifier is in P.

## SAME_REALIZATION one-way-input, one-work-tape ledger

The declared *length-aware* model has a charged unary 1^n# parameter preamble followed by exactly N genuine source bits. This is not asserted equivalent to CHMY's headerless input convention. The deterministic compiler parses n and m, copies the genuine D bits, records a, scans h once with a predecessor bit and adjacency flag, and after EOF evaluates V(D) by exhaustive assignment/quantifier-stack processing, with all work-head updates charged. Since D has length m and at most m quantified variables, evaluation costs <= 2^m poly(m)=O(N poly(n)); source scanning and output printing likewise cost <=O(N poly(n)). Peak workspace poly(n); serial output m+2 bits. No outside oracle, second input pass, or uncharged random source probes.

A same-machine MCSP lower-bound transfer still FAILS: promises collide, and the source convention is not pinned to the published headerless model [3].

## Hostile finite evidence

Executable: experiments/meta_lift/2026-11-18_clock_maskedinverse22_audit.py.
Raw: results/raw/meta_lift/2026-11-18_CLOCKMASKEDINVERSE22_raw.json.
Deterministic seed 202611171533. The finite QBF test codec uses two quantifiers plus a four-bit truth-table matrix and a complement bit, not the unrestricted PSPACE-hard QBF encoding. Independent recursive and bottom-up quantified evaluation were checked. Exhaustive 128 descriptors x four (b,q) labels; four tested sources per label, random controls at N=2048,4096,8192. Actual success: 9,128 assertions, 512 output labels, 2,048 source cases, 682 canonical checks, 2,730 forced-bit checks, 512 fixed-witness equality checks, 596 hostile controls, ZERO failures. The initial development test had an incorrect fixed-witness assertion that was corrected prior to the successful audit. The symbolic PSPACE-completeness and counting claims are mathematical consequences of known theorems, not finite test outcomes.

## Gates and one next lemma

DISJ: PASS as a no-go sanity control, no rank-to-circuit claim.
Relativization / algebrization / Natural Proofs: NOT APPLICABLE to an unrestricted separation, since none is claimed.
Simultaneous DTISP: FAIL for a proposed MCSP transfer, due to mixed promises and untransferred input convention.
Deterministic configuration counting: PASS as a consistency check on the declared polynomial-space *upper bound*, not a runtime lower bound.

NEXT: PROMISE-PURE-INVERSION23. Require a fixed c-independent B(D,i), one jointly NP/PH-low image and supplied-witness verifier with a stage-independent exponent under P=NP, BOTH source MCSP promise labels protected from all legal alternative seeds/decoders/cheap sections, and a truly headerless, fully charged one-way-input one-work-tape fusion. Do not choose c>K(c) circularly or infer P=PSPACE from P=NP. P versus NP OPEN.

## Primary references

[1] Stockmeyer LJ, Meyer AR. Word Problems Requiring Exponential Time (Preliminary Report). STOC 1973. https://doi.org/10.1145/800125.804029

[2] Savitch WJ. Relationships Between Nondeterministic and Deterministic Tape Complexities. JCSS 1970;4(2):177-192. https://doi.org/10.1016/S0022-0000(70)80006-X

[3] Cheraghchi M, Hirahara S, Myrisiotis D, Yoshida Y. One-Tape Turing Machine and Branching Program Lower Bounds for MCSP. STACS 2021. https://doi.org/10.4230/LIPIcs.STACS.2021.23

Historical overlap includes CLOCKSTREAMPROVENANCE20 (PSPACE-hard **image** with easy sections), CLOCKSTATEINVERSE21 (conditional PH reachability sections), and CANONICAL-WITNESS-TRAP9 (hard canonical witness need not mean hard best witness). No originality claim for the search/decision phenomenon.
