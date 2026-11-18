# CLOCKTRIANGULAR32 | high original-source degree under a complexity-preserving streaming gauge
**2026-11-18 01:30 America/Los_Angeles. PROVED/EXACT restricted theorem; COMPUTATIONAL controls; independent external review OPEN. P versus NP OPEN.**

## Target, hypotheses, and predeclared falsifiers
Dependency: HIGH-BRANCH-DEGREE-PURE32, following CLOCKADAPTIVEPOLY31. Authentic input is an ordered \(N=2^n\)-bit Boolean truth table, one-way read-only input, one writable work tape. The source promises are \(Y_s=\{f:CC(f)\le s\}\), \(NO_t=\{f:CC(f)>t\}\), with \(0<s\le t<N\). A desirable quotient needs asymmetric short YES-image witnesses and exclusion of **every** legitimate NO preimage, not only a fixed circuit decoder.

Four falsifiable mechanisms were compared before the literature check:
(A) high degree in the original source bits defeats low-degree canonical sections; falsifier: a computable nonlinear bijection with easy inverse on sparse witnesses;
(B) a genuinely ordered, high-degree streaming quotient with short target and no cheap sections; falsifier: explicit easy representatives for every target;
(C) jointly fixed-PH supplied-circuit equality plus a physically legal one-tape stream suffices for purity; falsifier: a massive mixed target fiber;
(D) an invertible preprocessing preserves MCSP labels at the **same** threshold; falsifier: the proved additive circuit-cost slack, which cannot be discarded.

## Theorem 1: TRIANGULAR-GAUGE-COMPLEXITY32
Let \(N=2^n\), \(n\ge2\). Define a triangular bijection \(T_N:\{0,1\}^N\to\{0,1\}^N\) by
\[
z_0=f_0,\qquad z_i=f_i\oplus\prod_{h<i}f_h\quad(1\le i<N).
\]
It and its inverse can each be produced by one deterministic left-to-right stream with a one-bit prefix-AND state. For every \(f\), with \(z=T_N(f)\), there is an absolute constant \(c\) (for an ordinary complete bounded-fan-in Boolean basis) such that
\[
|CC(z)-CC(f)|\le c(n+1).
\]
**Proof.** Triangularity makes inversion exact: on input \(z_i\), recover \(f_0=z_0\) and recursively \(f_i=z_i\oplus\prod_{h<i}f_h\). To bound the random-access *circuit* cost, distinguish \(f_0=0\), when \(z=f\), from \(f_0=1\). In the latter case let \(j\) be the first index \(i\ge1\) with \(f_i=0\), or \(j=N\) if none exists. Then \(z\) equals \(f\) with exactly positions \(1\le i\le j\) flipped (truncate at \(N-1\)). The interval-mask indicator is an \(O(n)\)-gate address comparator with \(j\) nonuniformly hardwired. Thus \(CC(z)\le CC(f)+O(n)\). For the reverse inequality, if \(z_0=0\), \(f=z\). If \(z_0=1\), let \(j\) be the first index \(i\ge1\) with \(z_i=1\), or \(N\) if none exists; the inverse flips exactly \(1\le i\le j\). Thus \(CC(f)\le CC(z)+O(n)\). This is nonuniform *circuit* equivalence, NOT a free uniform search for the interval endpoint. QED.

**Threshold warning.** The map \(T_N\) need not preserve YES/NO at the identical gate threshold \(s\). The proved assertion allows an additive \(O(n)\) budget shift. It preserves a separated gap only after accounting for that shift.

## Theorem 2: DYADIC-HIGHDEGREE-MIXEDFIBER32
For \(r=0,\ldots,n\), let \(i_r=2^r-1\). Define the **lossy** target
\[
H_n(f)=(z_{i_0},z_{i_1},\ldots,z_{i_n}),\quad z=T_N(f).
\]
Then all five statements hold.

1. **Exact source, compression and degree.** \(H_n:\{0,1\}^N\to\{0,1\}^{n+1}\). Its last coordinate has original-source ANF degree \(N-1\). The sum of coordinate ANF degrees is \(2N-n-1\) for \(n\ge2\), outside CLOCKADAPTIVEPOLY31's additive-small-degree regime. The last coordinate is non-unate in every one of the \(N\) source positions and the output is order-sensitive.
2. **Every label attainable, exact fiber mass.** Every \(y\in\{0,1\}^{n+1}\) has exactly \(2^{N-n-1}\) original-source preimages. This follows from bijectivity of \(T_N\) and projection onto \(n+1\) independent transformed coordinates.
3. **Uniform bound on easy representatives.** For any \(y\), define \(z_{i_r}=y_r\) at the checkpoints and \(z_i=0\) elsewhere; put \(g=T_N^{-1}(z)\). Then \(H_n(g)=y\), and \(CC(z)=O(n(n+1))\) by point tests against the \(n+1\) checkpoint addresses. Theorem 1 gives \(CC(g)=O(n^2)\). This is an explicit *existential* section, and in this example it is also uniformly constructible from \(y,n\) in polynomial time as a circuit.
4. **EVERY output label mixed for all sublinear power thresholds.** For any fixed \(0<\beta\le\gamma<1\), put \(s=N^\beta\), \(t=N^\gamma\). For all sufficiently large \(n\), the section in (3) has \(CC(g)\le s\). Standard circuit counting bounds the entire \(CC\le t\) family by \(2^{O(t\log(n+t))}=2^{o(N)}\). But each target fiber has \(2^{N-n-1}\) elements. Hence every target fiber contains a source with \(CC>t\), and
\[
\boxed{H_n(Y_s)=H_n(NO_t)=\{0,1\}^{n+1}.}
\]
This defeats **even separated Gap-MCSP** source promises, not just exact-threshold MCSP, for this explicit quotient.
5. **Fixed-PH equality verifier and charged stream.** For a supplied \(n\)-input circuit \(C\), one can compute \(H_n(TT(C))\) via \(n\) NP prefix-zero-existence queries \(\exists k<i_r:C(k)=0\) and direct evaluations \(C(i_r)\). Thus the joint equality predicate \(E(n,y,C)=[H_n(TT(C))=y]\) lies in uniformly fixed \(P^{NP}\subseteq PH\), polynomial in \(n+|y|+|C|\). The original source-to-target quotient itself is headerless and deterministic: scan true source bits sequentially, maintain prefix AND and an online binary index; at each index \(2^r-1\), retain that transformed bit; check power-of-two input length at EOF and serialize the \(n+1\) recorded bits. A conservative one-way-input/one-work-tape physical implementation takes \(O(N\log^3(N+2))\) steps, \(O(\log(N+2))\) work cells, including counter moves, output storage, EOF and malformed lengths. This is an algorithmic upper-bound ledger, **not** a bit-by-bit Turing-machine simulation executed in the audit.

**Proof of degree/non-unateness.** For \(i\ge1\), \(z_i=f_i\oplus f_0\cdots f_{i-1}\); for \(i\ge2\), degree is exactly \(i\) because the top monomial cannot cancel. The dyadic indices give \(1+1+\sum_{r=2}^{n}(2^r-1)=2N-n-1\). For \(z_{N-1}\), varying the last source bit toggles \(z\) and both monotonic orientations occur across other contexts. For any earlier source bit, hold all other prefix bits at 1 and select the last bit to obtain both orientations. Order sensitivity follows from the distinguished prefix and checkpoint addresses. The remaining claims were proved above. QED.

## Corollary: a general nonlinear-coordinate obstruction
Let \(F\) be *any* original-source-independent target map on transformed \(z=T_N(f)\) with the property that each attainable output has a transformed witness \(z\) of weight at most \(r\). Then \(H=F\circ T_N\) has an original-source representative with \(CC\le O(n(r+1))\) for every attainable label, even though its raw original-source ANF degree may be \(\Theta(N)\). In particular, every low-degree polynomial-feature or adaptive-transcript sparse section from CLOCKADAPTIVEPOLY31 transports through this nonlinear coordinate change; exact fiber *cardinalities* are preserved by bijection. This extension is a corollary of existing project sparse sections, not an independently novel polynomial-method theorem.

## Audit / hostile controls
Executed CPython 3 standard-library script with seed **202611180130**, source SHA256 **32824f61e85ed5fabad9f0623aa0b61bc351dd58e94e75615c1964d7c47a6bf2**. **331,562 assertions; zero failures**. Exhausted all 4, 16, 256, and 65,536 authentic source strings for \(n=1,2,3,4\), respectively. Verified inversion, both interval formulas, online scanner, explicit supplied-circuit truth-table oracle control, every output's exact fiber count, and all 60 canonical sections. Source length \(N=16\) gives 32 output labels and exactly 2,048 sources in each fiber. Checked exact ANF degree/non-unateness for all dyadic coordinates on \(N=8\), an order-sensitive swap, 199 malformed length controls, and larger randomly generated sources through \(N=1024\). The finite verifier enumerates possible prefix-zero witnesses only as a correctness oracle; it does not time a PH oracle or prove the physical one-tape bound experimentally. Raw result SHA256 **b655a85b9d6e21f7fcc7d860f16643c847f177f8f37453f335b5dacea5869b5e**.

## SAME_REALIZATION and proof barriers
The only executed machine being bounded is the authentic sequential quotient compiler, not a derived MCSP decider. Charge \(N\) original bits, count/EOF validation, prefix state, binary increment, checkpoint/output storage, one work-tape head motion and output. Target presentation length \(n+1\) is explicit. For circuit-equality verification, the input is \((1^n,y,C)\); each NP oracle query explicitly includes \(C\) and a binary index. This separate PH-verifier machine is **not** the one-tape compiler. Search for a \(CC\)-minimum source is not assumed or provided. No cascade, selector or promise-pure classifier is constructed.

- **DISJ:** NOT APPLICABLE (no tensor-rank or general circuit lower bound).
- **Relativization:** PASS only for this elementary restricted combinatorial counterexample; unrestricted \(P\) versus \(NP\) OPEN. No purported nonrelativizing step; Natural Proofs/algebrization not bypassed.
- **Simultaneous DTISP:** FAIL as an MCSP transfer because every label is mixed. Compiler upper bound is stated for one physical execution only. No forbidden-region decider is built.
- **Deterministic configuration counting:** PASS as upper-bound sanity: \(O(\log N)\) writable space permits at most \(2^{O(\log N)}\) configurations with the read-only input head, consistent with the claimed \(N\operatorname{polylog}N\) time; not a runtime lower bound.

The authentic map is genuinely lossy, not source-reconstructible after projection. Alternate circuits/decoders are allowed: the canonical sections are precisely legitimate alternative preimages that defeat NO exclusion. This is no inference from degree, entropy, difficult grammar, or certificate complexity to generic circuit hardness. Previous partial-MCSP interpolation, Chevalley-Warning, free-seed, graph, parity, signed-unary, low-degree, monotone, automaton, SLP and q-query controls remain untouched. Historical /341 FAIL and /386 RESTRICTED. The five TMR-owned root manuscripts, retired proof trackers, schedules and peer artifacts are not modified.

## Duplication / references
Recovered 2026-11-15 end-to-end directive, AGENTS.md, CODEX.md and pnp-research skill; clock-gate handoff and original CLOCKADAPTIVEPOLY31, CLOCKRESIDUAL30, CLOCKASYMTRANSFER24; main LOSSY_PROMISE_CASCADE6, PROMISE_CASCADE_FIXEDPOINT8, SOURCEQUERY_SYNTHESIS10 and PUBLICSEED_PLOTKIN14 plus earlier clock reports. Queried repository for triangular gauge/prefix and current TMR handoffs. The sparse-polynomial component is **explicitly credited** to earlier CLOCKADAPTIVEPOLY31/THRES-POLYFIBER10; triangular reversible bit maps are classical (Klimov-Shamir T-function precedent), with this explicit bounded-circuit/gap-purity application a project-scoped construction pending review.

[1] Cheraghchi, Hirahara, Myrisiotis, Yoshida, *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*, STACS 2021, https://doi.org/10.4230/LIPIcs.STACS.2021.23 .
[2] Hirahara, *NP-Hardness of Learning Programs and Partial MCSP*, FOCS 2022, https://doi.org/10.1109/FOCS54457.2022.00095 .
[3] Classical invertible triangular T-functions, Klimov and Shamir (2002/2003), cited here only as precedent, not a theorem used in the proof.
[4] Internal exact inputs: `research/agents/clock-gate/2026-11-18_0035_CLOCKADAPTIVEPOLY31.md`, `research/agents/clock-gate/2026-11-17_2330_CLOCKRESIDUAL30.md`, and `research/main/2026-10-18_LOSSY_PROMISE_CASCADE6.md`.

**ONE NEXT: GAUGE-ROBUST-ASYMMETRIC33.** Propose a YES-image witness-budget compression with universal NO exclusion **after quotienting by every cheap nonuniform complexity-preserving source gauge**, not simply high raw ANF degree, and construct its jointly fixed-PH equality plus a fully charged one-tape source compiler. Do not infer same-threshold purity from additive \(O(n)\) circuit preservation. **P versus NP OPEN.**
