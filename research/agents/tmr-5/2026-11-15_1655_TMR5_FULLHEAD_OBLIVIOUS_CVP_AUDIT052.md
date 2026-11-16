# TMR-5/052 | All-head-oblivious authenticated circuit-value replay

**2026-11-15 16:55 PST | TMR-5 / PNP Machine Bottleneck Redteam | Tracks B/A/C independent verification.**

## Candidate, quantifiers and falsifiers, stated before source replay

Named dependency **C3-VALUE-PROVIDER** in the TMR-3/055 stacked draft PR #169 (its base PR #164 is separately unmerged): Is a *public movement trajectory* enough to answer an authentic canonical mutable work-bit request cheaply?

For **every** integer n>=1 and **every** well-formed source of n topologically ordered binary AND/OR/CONST gates, construct **one fixed deterministic locally headed multitape machine** with blank initial work tapes, exact output equal to the designated circuit value, and a public complete movement schedule for both original-source INPUT and revisited VALUE heads. Source lengths and per-head itineraries depend only on n, not the gate table, operand choices or computed bits. Extend to remaining scratch heads by explicitly fixed-width, padded counter scans. Test a uniform logspace reduction of general CVP. This is a **restricted source-service theorem**, not a lower bound.

Falsifiers: (F1) source encoding excludes a legal gate or requires an uncharged lookup; (F2) either head moves according to operand bits; (F3) the global schedule has unpadded data-dependent microtimes or hidden writable source copies; (F4) the P-completeness reduction fails logspace, or a conditional L=P conclusion is incorrectly treated as a proved separation.

## Independent source-to-output construction and exact tariffs

Use the TMR-3/055 authentic source domain: unary `1^n0`, then for each gate j=0,...,n-1 a two-bit opcode and two n-bit one-hot operand masks. Constants use zero masks. Nonconstants select exactly one predecessor index < j per mask. Both operands may coincide; fan-out and reconvergence are legal. Output is gate n-1. Total source bits:

```
N = (n+1)+n(2+2n) = 2n^2+3n+1.
```

A total parser scans every field, validates length, legal opcodes, zero constant masks, one-hot masks and earlier-gate conditions; it flags failures instead of early-exiting on well-formed inputs. It does not store the entire circuit. A dedicated VALUE tape contains n genuine cells, initially blank/zero. For each gate j:

1. INPUT starts at left end, advances to record j, reads the two op bits, and subsequently advances through the 2n mask bits; its movements are independent of mask contents.
2. VALUE starts at cell zero, sweeps all n cells concurrently with mask A and captures a single bit A, rewinds to zero, then sweeps all n cells concurrently with mask B and captures bit B.
3. VALUE moves from cell n-1 to j, writes f(A,B) (or the constant), returns to zero, while INPUT rewinds to its left boundary. The last computed gate bit is placed in the output cell.

The induction on j establishes that every previously written VALUE cell contains precisely its actual circuit gate's Boolean value. Constant-false/true sources demonstrate that identical two-head itineraries may yield opposite answers.

The **exact authentic physical movement ledger** (including full input scan and rewind during authentication) is:

```
INPUT head moves:  2N + 2n(n+1)(n+2)
VALUE head moves:  4n(n-1)
VALUE cell reads:  2n^2
VALUE cell writes: n
```

Derivation: the input head's stage-j round trip goes from position zero to record-end `n+1+(j+1)(2+2n)` and back. Sum these 2*record-end movements over all j, plus 2N authentication movements. VALUE performs 3 complete (n-1)-length sweeps and a seek from n-1 to j followed by a return from j to zero, giving exactly 4(n-1) per gate. Output is one bit. Shared source wire identities are read afresh, never duplicated as mandatory DAG work. A separate source table is not preloaded.

Gate functions and one-hot captures operate on fixed-size finite-control bits. All source-symbol operations and binary counters/addresses can be padded to a predetermined O(log(n+2))-step schedule, including comparison and increment by full-width scans. All loops have public limits (n,j,i). This yields a **uniform fixed-machine bit-level implementation** with global head positions scheduled solely by n on well-formed words, **T=O(n^3 log(n+2))** and **peak S=O(n+log(n+2))** on the SAME execution. Exact *native* microtransition schedules and counter-tape padding are reasoned symbolically, NOT executed by the Python checker. The instrumented Python checks actual INPUT and VALUE macro-head itineraries only, and is not a native low-space runtime measurement.

## Complexity consequence and exact nonconsequence

General topologically ordered CVP is P-complete under logspace many-one reductions [1]. The standard dual-rail translation sends each original gate to two monotone AND/OR gates encoding its value and complement: NOT swaps the two rails via two legal AND(z,z) copies, while constants and AND/OR gates use monotone copies. Append one final AND(z,z) output gate. Every original size-g program becomes a well-formed monotone n=2g+1 gate program. A uniform O(log g)-space output transducer writes its unary header, opcodes and n-bit masks using public counters and rereads the original gate table. The output length is 2n^2+3n+1=O(g^2). The last VALUE bit equals the original circuit value. Thus **the authenticated canonical terminal-work-bit language is P-complete even though the entire multihead trajectory can be public**.

Hence **if a uniform exact polynomial-time, O(log N)-space provider answered this canonical terminal work bit on all valid sources, then L=P**. Conversely L=P would put this P-complete bit language in logspace. This is a conditional equivalence of resource classes, **NOT** a proof of L!=P, not a superlogarithmic unconditional lower bound, and not an impossibility of a provider using O(T^(1/3)) space. Source movement alone contains no unavoidable work lower bound.

This strengthens TMR-3/055's stated VALUE-only public movement property to a **full-head, fixed-padding public movement existence proof** for the *same authenticated service*, rather than modifying the source problem, moving to preloaded checkpoints, or claiming a generic Tree Evaluation result. It closes the named graph-label-to-work-value inference by a restricted, correct-direction P-completeness reduction. More general canonical mutable checkpoint-bit providers with arbitrary adaptive Q and a genuinely improved nonassociative evaluator remain OPEN.

## Independent executable replay and verification limitations

**Originals:** TMR-3/055 draft report blob `afa0019069b8719368957e796c0381eec2748c5d`, executed code blob `1dd318a057f72b81c42a080b15833bf9dd2c3344`, raw blob `8661dd4688684a1313ef69b7ac0346fd6c945e52` on PR #169 (not merged); merged TMR-5/051 source-head theorem; main TMR-1/055, TMR-2/055 and pending TMR-4/056 handoff reviewed. Historical /341 remains FAIL as a full UNSAT authority, /386 RESTRICTED. Retired root text proof trackers were not read or edited.

**Independent local CPython 3.13.5 execution:** `experiments/tmr/tmr5_fullhead_cvp052.py`, code revision `tmr5-fullhead-cvp052.v1`, seed 20261115, 432 n=1..12 monotone inputs, 380 general AND/OR/NOT dual-rail reductions up to 21 compiled gates, eight malformed strings, all original intermediate gate values and output bits, exact paid head movements, equal input/value schedule digests across same-n sources, opposing constant controls. **191,000 assertions, zero failures.** Exact local Git blob for source `624b1816cb905a24ee368d9e23f90cfd4cc94324`; raw JSON local SHA256 `001a1bc8e11a6a9a940840fbcb7e68fb6d32954b786ebc4b183af43b3ff81c9e`. Stage is a macro interpreter, not native TM microcode; P-completeness follows the symbolic reduction and known theorem, not finite tests. Python script runtime completed within the 30-second stage target. No repository checkout or preflight (connector-only access), full test suite, Lean kernel or LaTeX build executed. External independent mathematical review OPEN.

## Four mandatory gates

| Gate | Verdict | Exact reason |
|---|---|---|
| DISJ sanity | PASS (restricted) | The result imposes no runtime or circuit lower bound on DISJ or any easy family. Compact interleavings, Horn/2SAT, Gaussian, bounded-treewidth, equality, autarkies, padding, selectors, count normalizers and cached circuits remain legal. |
| Relativization | NOT APPLICABLE WITH REASON | No P-vs-NP separation is claimed. P-completeness/conditional L=P cannot be promoted to a nonrelativizing separation. Algebrization/Natural Proofs unrestricted bridges remain OPEN. |
| Simultaneous DTISP | PASS (restricted implementation); OPEN unrestricted | The same source-authentic machine admits the specified T and peak S with all access paid. There is no forbidden-region pair or generic compressed TreeEval simulation. |
| Configuration counting | PASS (upper-bound safeguard) | Fixed deterministic total read-only-input machines obey T<=2^O(S+log N). This is not a work lower bound and has no automatic randomized/quantum extension. |

## Ranked end-to-end dependencies

| Rank | Pipeline | Scoped finding | First unclosed dependency |
|---|---|---|---|
| 1 | TMR-3 C3-VALUE-PROVIDER | PASS independent source-to-output, stronger public-head theorem | A canonical arbitrary revisited-work-bit provider with adaptive Q plus a genuinely improved nonassociative TreeEval evaluator and same-run T/S |
| 2 | TMR-1 C1-SOURCE->SOLVER->HIERARCHY | PASS restricted parser/unique-aux CNF and promise totalizer, CONDITIONAL counting | Actual pinned Lean transitive kernel build and original E^NP hierarchy chain, no NP bridge |
| 3 | TMR-4 D4-COMPILER | PASS restricted read-once register, pending supplied-live-frontier PR | Uniform schedule finder and transfer to arbitrary shared circuits without exponential blowup |
| 4 | TMR-2 D2-COUNT | PASS restricted authenticated graph and weighted future-count quotient | Constructible efficient future signature for genuinely connected nontrivial family, arbitrary counting hardness OPEN |

**One next target:** source-authenticated canonical work-bit access for an explicit nonassociative Tree Evaluation family with legal repeated writes, adaptive queries Q, charged physical source/work heads, and a single complete provider-plus-evaluator T/S ledger. No NP-level hierarchy contradiction, SAT lower bound or P-versus-NP result has been established.

### Primary references

1. R. E. Ladner, *The Circuit Value Problem Is Log Space Complete for P*, SIGACT News 7(1), 18-20 (1975). https://doi.org/10.1145/990518.990519
2. L. M. Goldschlager, *The Monotone and Planar Circuit Value Problems Are Log Space Complete for P*, SIGACT News 9(2), 25-29 (1977). https://doi.org/10.1145/1008354.1008356
3. N. Pippenger and M. J. Fischer, *Relations Among Complexity Measures*, JACM 26, 361-381 (1979). https://doi.org/10.1145/322123.322138. This is prior art for oblivious simulations, not a new general result here.
4. R. Greenlaw, H. Hoover and W. Ruzzo, *Limits to Parallel Computation*, Oxford (1995), Chapter 6. https://academic.oup.com/book/41695/chapter-abstract/353938389
