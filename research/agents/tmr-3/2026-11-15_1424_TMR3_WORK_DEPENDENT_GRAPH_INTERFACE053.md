# TMR-3/053: Work-dependent computation graphs and an exact checkpoint sketch/probe tariff

**2026-11-15 14:24 PST | PNP Time-Space Tradeoffs | Track B | WORKCHECK053**

**Status:** **PROVED/EXACT only for the qualified checkpoint-service and binary-probe model, independent mathematical review OPEN**. Finite verification **COMPUTATIONAL**. The unrestricted Tree Evaluation, SAT-machine and P-versus-NP arrows remain **OPEN**.

## 1. Candidate, quantifiers and falsifiers stated before source review

**Candidate:** Extend TMR-3/052's source-indexed graph-selection investigation to **head movements determined by previously written work-tape data**, rather than immutable source bits. For every k and every binary k-bit *legal checkpoint content* z, construct one fixed physical service with graph-movement record z. For every uniform deterministic selector required to output this entire record on **all those checkpoint states**, prove that its retained checkpoint-dependent s-bit sketch plus q binary checkpoint-data probes must satisfy **s+q >= k**. This is an interface-information theorem, not a lower bound on arbitrary algorithms' total runtime.

Four falsifiers: (F1) the original input is identical across the checkpoint states, so source-only selection cannot decide the record without information flow; (F2) authentic work-bit probes, source replay or retained sketches are legal and may avoid any proposed impossibility, provided fully charged; (F3) the checkpoint configurations are NOT all canonical blank-tape runs on one fixed input, so their multiplicity cannot imply a hard-input family; (F4) the physically preloaded checkpoint already uses k writable cells, and abstracting those cells away without a sound virtual-node interface would falsify the resource ledger.

## 2. Primary source and previous corpus

Williams [1, Section 3.2] defines graph edge relations using a guessed per-block movement word, encodes the guess in O(B) bits, computes its block indices/edges in O(log t) *additional* space **given that guess**, and checks the guess by propagating FAIL through the Tree Evaluation node functions. His general construction enumerates possible guesses; it does not assert free access to the authentic graph record. The Cook-Mertz evaluator is restated as using O(d b + h log(db)) space [1,2], with height h=O(t/b).

TMR-3/050 shows the graph-retaining architecture bottleneck, /051 the physical exhaustive-enumeration bottleneck, and /052 a source-dependent family X_b(z) where *actual original-source bits* regenerate the graph with O(log N) auxiliary space at O(N) per local-source query. This /053 test is deliberately different: the graph labels live in checkpoint **work cells** not in the common original input. It does **not** contradict /052's authentic source-only shortcut on its own family.

Governing main directive SHA: 7b8804dc7587abc5134055b5b0d16a143055ca5a. Consulted root proof1 (SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), root proof2 (SHA 930c5eeddafce656717f28055a7a755f44737c), main.tex (SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34), AGENTS.md, CODEX.md, research skill, all five current TMR handoffs, issue #3, and original TMR-3/052 draft PR #152. Oversized proof2/main bodies were returned empty and cannot be claimed fully recovered. Local git clone/preflight failed DNS. No root writes.

## 3. Genuine fixed finite-control TM suffix

There are exactly two locally headed writable tapes, DATA and MOVE, alphabet {0,1,#,blank}, and one fixed finite-control transition rule independent of k,z. The original immutable input is the **same empty word** for every experiment. This is an explicitly **preloaded checkpoint suffix**, not a standard blank-work-tape computation.

The DATA tape holds z_1...z_k# starting at cell 0, with its head at 0; the MOVE tape is blank, head 0. In the READ state, one actual paid transition reading z_i advances DATA one cell right and advances MOVE right iff z_i=1 (otherwise MOVE stays). Reading # executes a paid HALT. Consequently

    m_i=z_i,  DATA_head_after_i=i,
    MOVE_head_after_i=sum_{j=1}^i z_j,  T_suffix=k+1.

At block width one, m_i is the *authentic* 0/1 block displacement of MOVE during time block i. Thus the fixed service realizes **2^k** distinct genuine graph-movement words, all while the immutable original input stays fixed. This is a local block-respecting service, but no claim is made that it reproduces every detail of Williams's original M-to-M' compiler.

**Smallest counterexample:** k=1, DATA[0]=0 versus DATA[0]=1, with the same immutable source, control and both head starting positions. A source-only, zero-advice and zero-work-probe selector must emit the same first movement label for both, and is wrong on one.

## 4. Exact binary checkpoint sketch/probe theorem

**Theorem 053-A.** Fix k>=1. A uniform deterministic all-checkpoint selector has (i) a public algorithm and the fixed original source; (ii) an initial preprocessor allowed to see the checkpoint and retain **one fixed-length s-bit sketch register** a(z) that includes all checkpoint-dependent advice/control/addresses; (iii) at most q adaptive *binary-symbol* work-checkpoint probes, whose next addresses may depend on a(z) and preceding replies; and (iv) no other checkpoint-dependent information channel. It must output the full correct k-label movement record for every z∈{0,1}^k. Then

    s + q >= k.

**Proof.** There are at most 2^s possible sketches. For a fixed sketch, the deterministic adaptive binary decision tree of depth at most q has at most 2^q leaves. Query addresses and final output are deterministic functions of the sketch and returned answers, so they do not convey extra information. The total number of distinct outputs is at most 2^(s+q). All 2^k different authentic records z are required. Therefore 2^(s+q) >= 2^k and s+q>=k. QED.

**Tightness:** retain z_1...z_s (with acquisition/writes charged), probe z_{s+1}...z_k (with actual cell access/address/time charged), and output the concatenation. The information inequality holds at equality q=k-s. A source-only q=0 all-context selector needs at least k bits of retained checkpoint-dependent sketch, whereas s=0 allows q=k work probes. The latter is a *legal cheap-space route* for a selector that has actual access to the checkpoint data, not a free graph oracle.

The count is information in a local service interface; it does not give any lower bound when a selector is permitted an uncharged giant advice tape, uncharged preprocessing, arbitrary oracle for work contents, or when only the one canonical state reached by a complete machine is required.

## 5. Same-realization time/space/evidence tariff and cube-root diagnostic

| Item | Charged resource |
|:--|:--|
| Genuine suffix | k+1 paid transitions, k DATA reads, k physical MOVE displacement labels, one endmarker/HALT |
| Visited writable space, one actual suffix | DATA k+1 cells, MOVE 1+sum_i z_i cells; this already costs Omega(k) total physically retained checkpoint space |
| Selector preprocessing | Sketch s bits plus real acquisition work, writable registers, scans and copies |
| Virtual work-data interface | q binary work-cell probes, head/index/address operations and any recursive reconstruction work |
| Output | k movement labels; stream output paid, and any rereadable output storage counts toward memory |
| Tree Evaluation | All Q separate evaluator queries, live node values, implicit graph/edge generation, arithmetic, conversions, recomputation, caching and failures counted on the SAME machine |
| Network | Sequential total work and aggregate live writable memory, not span/per-processor space |

If k=B=Theta(T^(2/3)), an **all-context** selector claiming s=O(sqrt B), q=0 contradicts s+q>=B. But allowing q=B correct work-cell probes evades that information obstruction. Whether the virtual Tree Evaluation environment can provide all such probes efficiently, with whole-machine space ~O(T^(1/3)), remains **OPEN**. This is not a general lower bound for every actual run. Preloading the k cells is already an Omega(k)-space implementation, so one may not combine that implementation with the auxiliary sketch's small memory and claim a cube-root-space whole machine.

## 6. Four required gates and hostile controls

| Gate | Status |
|:--|:--|
| DISJ sanity | **PASS**. No inference from assignment-cut rank to circuit or SAT-machine hardness. Horn, DISJ, 2-SAT, affine/Gaussian, equality, unique-solution, bounded-treewidth and compact-input controls are not declared hard. |
| Relativization | **NOT APPLICABLE WITH REASON** to unrestricted separation, none claimed. The explicit probe-bound remains a bounded-interface statement; any claimed nonrelativizing P-vs-NP arrow is OPEN. Algebrization/Natural Proofs not invoked. |
| Simultaneous DTISP | **PASS** for this ONE suffix's actual T=k+1 and visited writable space. **OPEN** for a complete matched SAT/FLMV time-space realization and for the hypothesized improved evaluator. |
| Configuration counting | **PASS** as an ordinary deterministic halting-run upper bound only; it supplies no lower bound on work here. Randomized/quantum runtimes are not inferred. |

Cheap graph access via caching, retained state, probes, source replay, real algebra, adaptive switching, path sharing or recomputation is permitted. No false all-SAT lower bound is inferred from 2^k graph words. Historical /341 remains FAIL as full UNSAT authority; /386 remains RESTRICTED.

## 7. Reproducibility and next proof obligation

CPython source revision **tmr3-work-checkpoint053.v1**, seed **none**, executed twice with byte-identical raw JSON. **336,030 assertions, zero failures; 8,190 exhaustive checkpoint states k=1..12; 98,304 s/q split cases**. Physical head-position/transition/visited-cell equalities and exact trace injectivity were independently checked by exhaustive enumeration. These finite tests are **COMPUTATIONAL**. The universal s+q>=k lemma has a separate full symbolic proof; no exhaustive enumeration of all selectors is claimed.

New paths:
- research/agents/tmr-3/2026-11-15_1424_TMR3_WORK_DEPENDENT_GRAPH_INTERFACE053.md
- experiments/tmr/tmr3_work_checkpoint053.py
- results/raw/tmr/2026-11-15_1424_TMR3_WORK_CHECKPOINT053_PY_RAW.json
- research/agents/tmr-3/runs/2026-11-15_1424/handoff.md

**TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.** Root proof trackers, main.tex and the canonical old historical handoff unchanged. Five scheduled agents unchanged. P versus NP OPEN.

**Next lemma:** Construct or falsify an exact virtual-node checkpoint bit-access interface for arbitrary work-dependent graph movements, and audit its *number of queries Q*, sequential cost per query and aggregate live space under a genuinely new height-sublinear Tree Evaluation evaluator. Do not convert the authenticated /052 source-specific shortcut into a free all-state oracle.

### References

[1] R. Ryan Williams, *Simulating Time With Square-Root Space*, STOC 2025, arXiv:2502.17779v1, Sections 2–3. https://arxiv.org/html/2502.17779

[2] J. Cook and I. Mertz, *Tree Evaluation Is in Space O(log n log log n)*, STOC 2024, Theorem 7, restated in Williams [1]. https://doi.org/10.1145/3618260.3649664
