# TMR-5/099: paid two-polarity correct-path firewall and native T5 switching control

Date: 2026-11-18 (America/Los_Angeles). Role: TMR-5 independent machine red team. This is a standalone, source-aware audit; no other agent identities, files, schedules, enabled states, or peer manuscripts are to be changed. **P versus NP remains OPEN.**

## Propose / literature / new result
Candidate to test: a universal SAT/UNSAT specialist has a short externally supplied "correct path" of `k(n)` bits, with worst-path charged RAM time `n^(1.33+o(1))` and live space `n^(.5+o(1))`. The candidate **fails** if every possible accepting path is source-checked and sound, every input has a valid path, and `k(n)` is too small. This follows from complete branch enumeration, and yields a quantitative **advice-bit barrier**. A supplied **unverified** correct polarity bit does not satisfy the premise.

Primary literature checked: FLMV, JACM 2005, Theorems 5.7 and 6.4, [DOI](https://doi.org/10.1145/1101821.1101822), [author PDF](https://lance.fortnow.com/papers/files/tst.pdf); Buss and Williams, *Computational Complexity* 24 (2015), Figure 8.2 and its quantified DTISP model, [journal manuscript](https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf); Diehl, van Melkebeek, Williams, *Journal of Combinatorial Optimization* 22 (2011), 325-338, [DOI](https://doi.org/10.1007/s10878-009-9286-x). The earlier 2004 FLMV manuscript's front-matter description of "nondeterministic SAT" must not override the actual Theorem 6.4's **coNTISP** inclusion or the corrected JACM abstract. It does *not* exclude an ordinary nondeterministic SAT witness verifier.

## Exact quantified row/block interface
Let `Z` be an explicit or uniformly enumerable set of at most `R=n^(.195+o(1))` shared assignments. Let `F(z,y)=AND_{i=1}^B F_i(z,y_i)`, with `B<=n^(.65+o(1))`, disjoint private `y_i`, authenticated residual size `m<=n^(.35+o(1))`. Then

    SAT(F) <=> EXISTS z IN Z FOR ALL i EXISTS y_i: F_i(z,y_i).
    UNSAT(F) <=> FOR ALL z IN Z EXISTS i FOR ALL y_i: NOT F_i(z,y_i).

The bad-block index `i` may depend on `z`. An UNSAT declaration must check every represented row, and *each negative local assertion* must be independently source-proven. A SAT declaration requires one source-valid shared row plus privately valid assignments for **all** blocks. A child SAT witness cannot certify a child UNSAT result. A procedure that accepts one favorable path without checking the failing universal branches is a nondeterministic/advice procedure, **not** a deterministic specialist.

A deterministic partial NO specialist must output a source-bound proof or UNKNOWN, with NO always correct. If it emits NO on **every** UNSAT arbitrary CNF while remaining sound, then mapping UNKNOWN to SAT produces a **total deterministic** SAT decision procedure within its own time and space bounds. Thus that property cannot be invoked as an uncharged "one-sided" escape.

## Theorem 099.1: paid complete-path enumeration and advice-bit floor
Fix one uniform machine `V`. On input `x` of actual binary encoded length `n`, and an optional binary path `p` of length at most `k(n)`, it returns SAT, UNSAT, or UNKNOWN. Suppose:
1. **Wrong-path soundness:** every SAT or UNSAT output is *correct for that source input*, on every path, even deliberately wrong ones.
2. **Completeness:** every input has at least one path that returns SAT or UNSAT.
3. The entire run on **every path** costs at most `T(n)` time and `S(n)` peak live workspace, charging source parsing, program use, local checking, failures, verification, child calls of either polarity, certificate access/replay, all output writing, and materialization. No free decision oracle, source-dependent program, or free path selector is permitted.
4. If `p` is provided on a read-only external tape, deterministic enumeration **copies its bits into counted workspace** before replay. No free access to a correct answer bit persists.

Enumerate all at most `2^(k(n)+1)` possible paths, replay `V` from the authenticated source, and return the first non-UNKNOWN answer. Soundness makes the first answer correct, completeness guarantees an answer. Resource bound:

    T_det(n) = O(2^k(n) [T(n)+poly(n+k(n))])
    S_det(n) = O(S(n)+k(n)+log n+streaming buffers).

For a path certificate only available as a stream, account for its position and re-reading; if the verifier requests random access to `p`, storing `k` bits makes that access paid. The simple upper bound holds for a fixed standard random-access RAM with input-copy overhead at most `O(n+k)`; this overhead is subsumed by `T(n)>=n` in the current target.

Buss-Williams (2015) Figure 8.2 explicitly excludes `SAT in DTISP(n^1.34070, n^.5)` for the defined random-access model, with `n^o(1)` exponent slack. Use the conservative interior point `c_0=1.34060`. Consequently, assuming `T=n^(1.33+o(1))`, `S=n^(.5+o(1))`, all-input correctness and a valid near-linear source encoding, **it is impossible** for `k(n) <= (0.01060-delta) log_2(n)` for all sufficiently large n, for any fixed `delta>0`. Otherwise enumeration gives deterministic time `n^(1.34060-delta+o(1))` and space `n^(.5+o(1))`, a contradiction.

This is an **all-input, model-conditional, small-advice firewall**, *not* a general lower bound on witness search. It does not apply to a correct path of length `Omega(log n)` with a larger constant, an unverified oracle-selected answer bit, a nonuniform advice scheme, an unchecked wrong path, a one-input or fixed-girth family, or a strategy whose full charged adaptive/alternating tree is not covered by `k(n)`.

**Single-polarity corollary:** an everywhere sound SAT/UNKNOWN verifier that accepts every SAT formula, or a sound UNSAT/UNKNOWN verifier that accepts every UNSAT formula, can likewise be deterministically enumerated and complemented if needed. Neither yields an all-input `1.33/.5` algorithm with subthreshold `k`. This statement does not prohibit an ordinary nondeterministic verifier with an `Omega(n)`-bit witness.

## Theorem 099.2: exact native T5 dynamic selector
Let `R(a,b) <=> (b-a) mod 5 in {1,3}`. Take terminals `u=0,v=1`, private vertices `a=2,b=3,c=4`. Define block zero by arcs `u->a->v` and `u->b<-v`. Define block one by `u<-c<-v`. The blocks share only `u,v`; their private vertices are disjoint. The graph is a simple orientation of `K_(2,3)` with 5 vertices and 6 arcs.

Let `delta=x_v-x_u mod 5`. The two native length-two path supports of block zero are `{1,2,4}` and `{0,2,3}`, so block zero has private solutions **iff** `delta=2`. Block one's support is `{1,3,4}`. Thus both blocks cannot be satisfied simultaneously, but **neither block is UNSAT for all shared assignments**. The exact winning bad-block schedule is:

    delta=0     : both 0 and 1 are bad
    delta=2     : only block 1 is bad
    delta=1,3,4 : only block 0 is bad

Every residue has five simultaneous color rotations. Any alleged fixed single bad-block proof for all shared assignments fails on an explicit row. The whole graph has zero T5 homomorphisms; deleting each arc yields respectively `10,10,40,40,10,10` homomorphisms. Hence it is an **intrinsically edge-critical UNSAT** native T5 obstruction, not an unrelated hard source with an attached gadget.

A further source-aware algorithmic escape: if a connected T5 block has only **one** shared boundary vertex, its private feasibility is independent of the shared vertex's absolute color, by the five global rotations. For `r` boundary vertices, feasibility depends only on `r-1` relative residues, so at most `5^(r-1)` distinct boundary orbits exist. This is an *upper bound on interface profiles*, not a lower bound on algorithmic work. The native two-terminal obstruction shows that the `r=2` case already allows row-dependent selection.

## Source literature: precise polarity/model exclusions
**Deterministic SAT decision:** Buss-Williams (2015) Figure 8.2 provides `c=1.34070` at `space=n^.5`. For `space=n^o(1)`, the alternation-trading endpoint is `c<2 cos(pi/7)=1.801937...`. Both require the stated deterministic random-access machine and an all-input SAT decision guarantee; they do not transfer automatically to arbitrary encodings, T5, or critical-deletion witness search.

**Nondeterministic UNSAT acceptance / co-nondeterministic SAT:** FLMV Theorem 6.4 proves `NTIME[n] not subset coNTISP(n^c,o(n^d))` where `d=min((1/g_k-c)/k,c^(-2k))`, `g_0=1,` `g_k=c^2 g_(k-1)/(1+c g_(k-1))`. The same transfer to coSAT certificates assumes a valid efficient SAT-completeness reduction. At `c=1.33`, the optimized **FLMV** cutoff is `d=0.08929991057...` (`k=3`). This excludes sufficiently *smaller* simultaneous space exponents, **not** space exponent `.5`. Diehl-van Melkebeek-Williams improves the subpolynomial-space time endpoint to `c<cube_root(4)=1.5874...`, still not a `.5`-space exclusion.

**Deterministic SAT, older exact FLMV tradeoff:** Theorem 5.7 uses `f_0=1,` `f_k=c f_(k-1)/(1+f_(k-1))`, `d=min((1/f_k-c)/k,c^(-k))`. At `c=1.33`, optimum `d=0.27910422645...` (`k=3`), weaker at `space=.5` than Buss-Williams.

**Nondeterministic SAT witness acceptance:** an existential verifier is not the coNTISP machine of Theorem 6.4. A freely supplied read-only, random-access assignment tape permits near-linear-time/polylog-workspace *verification* of an explicit CNF witness; its length, generation, access and output have not thereby been paid in a solver. Ordinary nondeterministic guesses in a RAM do not automatically confer a free random-access read-only witness tape. For UNSAT, a general polynomially checkable certificate system that is complete for all CNFs would imply `NP=coNP`; such a certificate system cannot be assumed.

**Proof/representation lower bounds:** OBDD widths, read-once or resolution proof sizes, communication, information-counting, fixed treewidth, and source-unaware recursion are not lower bounds for an unrestricted witness-finding RAM. Adaptive variable order, affine Z5 path transfer, quotienting, DAG sharing, and direct source-aware algorithms remain valid escapes.

## Supplied layout and recurrence: conditional, no hidden seed
Prior cross-track synthesis 72 independently obtained the charged upper-bound envelope
`T_new<=n^(1.195+o(1))+n^(.845+o(1)) T_seed(n^(.35+o(1)))` and `S_new<=n^(.35+o(1))+S_seed(n^(.35+o(1)))` for a *supplied authenticated* row/block layout, **not** arbitrary CNF. For seed `T_seed(m)=m^(t+o(1)),S_seed(m)=m^(s+o(1))`, a one-step `1.33/.5` target requires `t<=97/70=1.385714...`, `s<=10/7=1.428571...`. A merely polynomial-time hypothetical seed gives no such guarantee. The often quoted iteration toward the fixed point `t=1.30` requires an actually constructed hereditary **arbitrary-child** splitter and paid recursion, precisely the missing all-input theorem.

For SAT witness extraction, traditional variable bit-pinning across all `B*m=n^(1+o(1))` private bits performs `n^(1+o(1))` child calls; re-materializing each `n^.35` child costs `n^(1.35+o(1))` just to emit queries. This falsifies a naive `1.33` **implementation claim**, not the existence of optimized reusable witness reconstruction. On native T5 critical deletion controls, exact transfer/dynamic programming already defeats generic lower-bound proxies.

## Independent reproducibility and status
Native exhaustive checker (no SAT oracle) tested all 25 endpoint assignments and 5 rotations of each, explicit private-variable enumerations, 200 independent length/path-count recurrences, all six deletions and their witnesses, a separate Boolean 2-block switch, and 100 levels of rational FLMV recurrences. Total **606 assertions/checks, zero failures**. Raw SHA-256: `7323d98b688f322a3611b003616def66c9524a2e1cc83cb958e5bcc5579ac529`. Exact local executable and raw JSON packaged separately; published manuscript/report code is not itself a machine-time benchmark.

**PROVED:** row/block quantifier equivalence; deterministic enumeration theorem and conditional small-advice barrier; native T5 two-boundary changing-selector obstruction; one-boundary Z5 rotation collapse; finite exact criticality.
**CONDITIONAL:** fast split recurrence on supplied authenticated layout; witness-saving by stronger seed; all-input forbidden-target implication if full soundness, uniformity, charged resources and small `k` are established.
**FALSIFIED:** free correct polarity is a sound deterministic decider; there exists a single globally bad block for the native switching graph; a `k=o(log n)` complete verified two-polarity route at target `1.33/.5` on arbitrary CNFs; treating coNTISP lower bounds as nondeterministic SAT witness bounds.
**OPEN:** an all-input hereditary seed-dependent CNF splitter; polynomial-time source-preserving reduction to intrinsically critical high-girth SAT-deletion witness search; arbitrary-machine superpolynomial SAT witness lower bound; P versus NP.

**Next blocker:** supply a formally checkable correct-path witness/NO-verifier with the *full* charged strategy depth, source binding and wrong-path soundness for **every** arbitrary input, then run the enumeration firewall before making any unrestricted machine-time claim. Do not infer this from an individual hard critical graph, path OR gadget, or a free oracle-polarity label.
