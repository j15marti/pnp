# TMR-3/062: P-complete authentic-graph selection with exactly two public candidates

November 15, 2026, 22:54 PST. Owner TMR-3 / PNP Time-Space Tradeoffs, Track B.

**Status:** PROVED/EXACT for the declared TMR-3/060 fixed-machine block-respecting family and a restricted virtual simulator; external independent mathematical review OPEN. Finite evidence COMPUTATIONAL. Generic nonassociative Tree Evaluation, unrestricted SAT lower bounds, and P versus NP remain OPEN.

## Selected connected dependency, quantifiers, and falsifiers

Named dependency: **C3-SELECTIVE-CANDIDATES-AND-COMPACT-STATE**, restricted to the existing authenticated CVP-marker machine M* from /060. Prove or falsify whether an authentic graph-edge bit that is P-complete already forces many candidate graphs, an expensive full-word representation, or expensive serial guessing.

For the ONE fixed total blank-start local multitape M* of /060 and every valid one-hot circuit x of length N=2n^2+3n+1, a uniform source-INDEPENDENT length-only machine produces exactly two possible complete block-movement words g_0(N),g_1(N), one of which is authentic. Both graphs occur at each admissible n. The authentic selection bit is f(x), P-complete by Ladner's CVP theorem plus the /055 dual-rail logspace compiler. A separately specified single deterministic virtual simulator checks both complete candidates against the actual source execution with a full charged time/space ledger; it never receives f(x) as an oracle.

Four falsifiers explicitly audited: (F1) an A or clock head might secretly enter another tape block; (F2) the public final query j or the position of the conditional boundary crossing could depend on f; (F3) false candidates could produce Boolean answers if intermediate movement labels or original input accesses are not verified; (F4) writing out candidate words or storing physical b-cell clock tapes could be falsely charged as free in a supposed small-space simulator. Also, a P-complete selector must NOT be promoted into many-guess or all-machine hardness.

## Primary source and exact prior construction

Williams, *Simulating Time With Square-Root Space*, arXiv:2502.17779v1, Section 3.2, defines m_(h,i) in {-1,0,1} for the movement of tape h between time blocks i and i+1. Claims 3.4/3.5 compute graph edges efficiently **given** the candidate word; the paper enumerates such words and returns FAIL when any locally checked movement is wrong. This is a space simulation, not a polynomial-time bound. /060 proves one actual block-respecting M* with b=N+d, exact t=C b^3+3b+1, final time-block B=C b^2+4, where C is a fixed sufficiently large even integer and d is a fixed large integer. Every head stays in tape block 1 except for MARK's final answer-dependent possible crossing. The /060 authentic first-visit edge is present iff f(x)=1. See PR #196 and /060 report; its native A clock-completion microcode remains independently uncompiled.

## New two-graph lemma

Let p be the fixed number of actual heads in M*, h_* the MARK head, and B=C(N+d)^2+4. For c in {0,1} define the COMPLETE movement word of pB trits by

    g_c(h,i)=c   if h=h_* and i=B-1,
             0   otherwise.

Here movement at time-block boundary i describes the transition to time block i+1; the final unused terminal entry is zero. In the graph induced by g_c, every head accesses block 1 in every block except MARK, whose block at i=B is 1+c.

**Theorem (exact two-graph support).** For every valid source x, its authentic complete block-movement word is g_(f(x)). For every n>=1 the set of such words over length N=2n^2+3n+1 has cardinality exactly two, not merely at most two. Furthermore the source-independent bit provider (N,c,h,i) -> g_c(h,i) runs in O(log N) writable space and polynomial-in-log N bit time after a charged O(N) length scan, and can stream each full word using O(pB polylog N) time, O(log N) writable space, and a write-only output channel. An implementation that retains the entire word instead pays Theta(pB) bits.

**Proof.** /060's original source head, finite A work and counter heads, and three clock heads all remain inside their first b-cell tape block in every time block. MARK stays at zero until a final b-step sweep, reaches cell b-1 after the first b-1 sweep steps, and makes the unique possible move from b-1 to b at absolute time Cb^3+3b, exactly the boundary between blocks B-1 and B. That move occurs iff f(x)=1. Thus no other block-index transition is possible and the displayed g_(f(x)) is exact. For each n, a source with all constant-zero gates has f=0 and a source with all constant-one gates has f=1, yielding both distinct words at the SAME N. Computing B and checking (h,i) against (h_*,B-1) uses O(log N)-bit counters and fixed-degree arithmetic. Full streaming repeatedly emits the requested trit; it does not materialize pB trits. QED.

The exact two-graph theorem is a **falsifier of the proposed implication** “P-complete authentic edge selection requires superpolynomially many candidate movement words.” Authentic selection of which candidate is correct remains P-complete. This does NOT imply a generic efficient verifier or an L=P collapse.

## A complete restricted input-to-output verifier and virtual provider

On each authentic original binary source x, run c=0 and then c=1. For each candidate:

1. Authenticate the entire source in the actual one-hot grammar, marking invalid sources with f=0 without trusting a malformed header.
2. Simulate A from blank work tapes, preserving its real VALUE cells and read-only-input accesses; in parallel, represent the three originally b-cell clock tapes **symbolically** by O(log b)-bit head positions, directions and fixed endpoint symbols (every other clock cell is blank). Represent the unwritten MARK tape by its head position and blank-symbol rule. Step the entire fixed M* clock epoch, alignment, sweep and final read with paid binary arithmetic.
3. At every time-block boundary check every true head-block movement against g_c using its on-demand trit provider; return FAIL on the first discrepancy. Only the matching candidate returns the actual Boolean output f(x). Restart and replay for the second candidate when needed.
4. If the authentic candidate passes, return its Boolean output. No guessed graph, tape, checkpoint, or output bit is used as an unverified oracle.

The verifier's actual chronological evaluation corresponds to a SPECIAL restricted computation-graph chain with one possible source edge. It is **not** a generic Cook-Mertz implementation or an improved evaluator for arbitrary nonassociative height B. The legal source-aware shortcut of computing f directly also remains available.

**Same-realization ledger.** Let t=Cb^3+3b+1=Theta(N^3), B=Cb^2+4=Theta(N^2), n=Theta(sqrt N) on valid sources, p fixed. Each candidate checks at most p(B-1) real boundary trits, so Q_move<=2pB for both. An additional independently requested canonical checkpoint BIT at a chosen (h,i,cell) may be supplied by replaying the actual source and virtual machine from blank up to that time, in T_bit=O(t polylog(N+2)) time and S_bit=O(n+log(N+2)) space. For q arbitrary bit requests, such replay costs O(qt polylog N), not zero; the chronological verifier needs no extra arbitrary replay. Charging length acquisition, invalid-input guard, repeated A evaluation, source scans, checking EVERY claimed boundary, all head/address counters, symbolic clock decoding, FAIL switching, retained A VALUE state, and output, ONE deterministic virtual simulator has

    T_total = O(2t polylog(N+2) + 2pB polylog(N+2)),
    S_peak = O(n+log(N+2))     (valid source),

with invalid-source parser using O(log N) additional workspace. There is no b-cell clock tape stored in the simulator, because the exact two-endpoint tape contents are computed from the fixed clock program, not silently treated as physical preloaded checkpoints. If a generic evaluator insists on materializing b-bit node labels, the b-bit buffer MUST be added, and this restricted small-space bound does not transfer.

## Four mandatory gates and controls

| Gate | Verdict |
|---|---|
| DISJ sanity | PASS restricted. No cut-rank or semantic-mass lower bound is inferred; DISJ's small depth-two circuit, Horn, 2-SAT, affine/Gaussian, treewidth, equality, product, selector, unique-solution and compact/shared shortcuts remain legal. |
| Relativization | NOT APPLICABLE WITH REASON to an unrestricted separation. Only a fixed-language exact construction and conditional L=P implication are stated; an NP-level nonrelativizing step is OPEN. No algebrization or Natural Proofs claim is made. |
| Simultaneous DTISP | PASS for the declared virtual simulator, with two paid replays and peak n+log N bits on the SAME execution. Generic nonassociative Tree Evaluation, arbitrary machine transfer, and a strict FLMV contradiction remain OPEN. |
| Configuration counting | PASS as a deterministic halting-run upper-bound consistency check only. Polynomial T with S=Theta(sqrt N) is compatible with 2^O(S+log N). No runtime lower bound or randomized/quantum extension. |

Local field/basis rank, DISJ, Valiant-Vazirani randomness, majority ties and quantum error models play no role in this construction; they remain guards on any attempted external transfer. /341 FAIL full UNSAT authority; /386 RESTRICTED.

## Executed evidence and limitations

Actually executed CPython 3 standard-library revision **tmr3-two-candidate062-short-v1**, seed **202611152254**, twice with byte-identical raw JSON. The final exact published script passed **16,247 assertions**, testing **900** authentic one-hot circuits, **1,807** malformed controls, both outputs and two candidate labels, public block/index arithmetic and matching/mismatching candidate behavior, with **zero failures**. An earlier longer audit also ran successfully (17,737 assertions), but the published short revision is the authoritative self-contained evidence. The Python script is under experiments/tmr/tmr3_two_candidate062_short.py and raw results under results/raw/tmr/2026-11-15_2254_TMR3_TWO_CANDIDATE062_SHORT_RAW.json. Finite evidence is COMPUTATIONAL and does not execute the complete native A transition table, the folded-copy HPV converter, or Cook-Mertz; the symbolic compiler and virtual clock space analysis remain subject to independent review. The finite test chooses C=4,d=64 for labels, **not** a certified deadline for a native compiled A; the theorem uses sufficiently large fixed C,d.

Preflight: no local Git checkout (external GitHub DNS resolution failed), so repo preflight not executed. Connected GitHub fetch/readback is used for publication. Historical proof trackers and peer manuscripts are untouched.

## One next load-bearing lemma

**C3-SELECTIVE-CANDIDATES-GENERAL-TRANSFER:** Pin a concrete general block-respecting compiler and specify a structural, SOURCE-CHECKABLE certificate that its authentic movement word lies in a polynomial-cardinality, O(log t)-addressable candidate family; give a same-run polynomial-time FAIL verifier or a proof that a nominated certificate scheme cannot meet both time and space. The present exact two-candidate result works only because all ordinary heads are confined to one block, and it does not solve generic work-dependent Tree Evaluation.

## References

[1] R. R. Williams, *Simulating Time With Square-Root Space*, STOC 2025, arXiv:2502.17779v1, Section 3.2, https://arxiv.org/html/2502.17779v1 .
[2] R. E. Ladner, *The Circuit Value Problem Is Log Space Complete for P*, SIGACT News 7(1), 1975, https://doi.org/10.1145/990518.990519 .
[3] J. Hopcroft, W. Paul, L. Valiant, *On Time Versus Space*, JACM 24, 1977, https://doi.org/10.1145/322003.322015 .
[4] TMR-3/060, *Admissible-block graph hardness and the conversion-preservation distinction*, original report in research/agents/tmr-3/2026-11-15_2030_TMR3_ADMISSIBLE_BLOCK_GRAPH060.md.
