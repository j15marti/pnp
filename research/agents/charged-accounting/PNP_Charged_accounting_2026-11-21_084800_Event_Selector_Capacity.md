# Accounting: adaptive event indices are part of the record
Pacific timestamp: 2026-11-21 08:48 PST (America/Los_Angeles).
Role: charged-accounting. Named lemma: **T5-EVENT-SELECTOR1**.

## Target and outcome
**PROVED/EXACT:** the selector-aware conditional-entropy inequality below. **FALSIFIED/RETIRED:** reconstructing a value from adaptively indexed events while charging only their payload bits and omitting the indices/timing needed by the decoder. **COMPUTATIONAL:** 126 strict-C control inputs and their finite tape-phase traces, including relocated copies, pass. **OPEN:** any compulsory superpolynomial information demand for arbitrary strict-T5 solvers.

The original handoff and original entropy note ALREADY charge timing/address/termination metadata. This is a concrete refinement and falsifier of an unclaimed stronger simplification, not a counterexample to their stated transfer theorem. It does not violate the coarser bound b r T on the entire long execution: the failed step is the proposed small record charge b|E_j|.

Independent-review status: elementary proof and executable falsifier supplied; external adversarial review requested, not received. No unrestricted separation is promoted.

## Exact quantifiers and corrected inequality
Fix one correct total deterministic solver A, one explicit N-bit input distribution, and one actual halting run per sampled input X. Use the handoff's sole read/write tape, fixed finite alphabet/control, charged input, complete head/location/storage state and no external clock. Fix K,a independent of input and assume, when making cap comparisons, T_A(N)<=K N^a.

For each j in a fixed finite obligation set, let:
- U_j be the proposed information to reconstruct;
- B_j be ALL side information actually granted to its decoder;
- I_j be the ordered subset of actual transition indices selected for this record, with q_j=|I_j|;
- P_j be their required payloads, each from an alphabet of size at most 2^b;
- Pi_j=(I_j,P_j), with a fixed actual decoder satisfying H(U_j|B_j,I_j,P_j)=0.

If each physical transition belongs to at most r selected sets on every run, then
```
H(U_j|B_j) <= H(I_j|B_j) + b E[q_j],
sum_j H(U_j|B_j) <= sum_j H(I_j|B_j) + b r E[T].
```
Additional metadata Z_j not included in I_j/P_j contributes H(Z_j|B_j,I_j), or is included in a separately charged prefix-free header. B_j is not permission to supply free input or cache access to a real computation.

Proof: exact reconstruction implies H(U_j|B_j)<=H(I_j,P_j|B_j). Apply the chain rule. Conditional on B_j,I_j, q_j is known and P_j has at most 2^(b q_j) possibilities, so its conditional entropy is at most b E[q_j]. Sum, and use the pathwise overlap bound sum_j q_j<=rT. No independent-demand or independent-event assumption is used.

For L=floor(K N^a), with N and the cap known to the decoder,
```
H(I_j|B_j) <= H(q_j|B_j) + E[log2 binom(L,q_j)]
           <= log2(L+1) + E[log2 binom(L,q_j)].
```
The count q can be encoded in ceil(log2(L+1)) bits, followed by the rank of its subset in ceil(log2 binom(L,q)) bits. Fixed q framing then determines the payload length, producing a prefix-free record. This is an existence/capacity bound; uniform rank computation or physical trace collection must be charged if an algorithm uses them. A simpler explicit list pays O((q_j+1)log(L+1)) bits.

If I_j is already determined by B_j, the selector entropy is zero. Otherwise omitting it requires a separate decoder argument; adaptive selection by itself does not make it free.

To exclude the fixed cap using these records, one must prove, on the SAME distribution and solver,
```
sum_j H(U_j|B_j) - sum_j H(I_j|B_j)
 - other charged header overhead > b r K N^a.
```
No such compulsory net demand is established here. Under a polynomial cap, explicit timing/address indices normally add O(log N) bits per event; treating b as a universal constant can be invalid.

Four falsifiers:
1. Show the displayed decoder reconstructs U without the selector indices although identical payloads arise for different U.
2. Find a valid bounded-alphabet payload violating the chain-rule bound with all actual indices and side information included.
3. Reuse one event in arbitrarily many obligations while retaining r=1.
4. Grant input/cache/clock/address data to the decoder without including it in B, P, I or a paid header.

## Recovery and exact source revision
Recovery pin: 358200a519d8cd27b33a02a12bb1b6b7db24a825. The complete current handoff was fetched unchanged from the fully read baseline at 10d2ccb2062c3efd4b4f03873eaa88822edf732f, blob a886f3387a8676b9cc86afbf3bebf22630109d49. Current assignment directive, AGENTS.md, CODEX.md and repository research instructions were fetched unchanged. The new accounting handoff returned 404.

The latest saved [Accounting 07:41 raw-module report](https://chatgpt.com/library?file_id=libfile_2a46fd98b9d48191866bd26527671e42&account_id=personal) was located by prefix search; its actual parser, source-index correction and charged service ledger were recovered in the continuous work. Its selector-ID bug is about source/query lengths, not this temporal event-selector issue. The old parser suite is not repeated.

Relevant current peers: [Construction 08:39](https://github.com/j15marti/pnp/blob/358200a519d8cd27b33a02a12bb1b6b7db24a825/research/agents/charged-construction/PNP_Charged_construction_2026-11-21_083900_Three_Color_Private_Leaves.md) supplies an exact graph-three-color projected interface and weighted count, but no compulsory computation; [Synthesis 08:28](https://github.com/j15marti/pnp/blob/c4b8923cb7437f2794fa0da3181be3795dd2e35b/research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-21_082800_Terminal_Defect.md) retains terminal extension costs; Redteam 4b84b9c preserves actual-run rather than padded-time accounting. Their actual reports and evidence were recovered. Issue #324 through the verified Construction comment 7065872266 was read.

Original evidence [Entropy and Unrestricted Counting](https://chatgpt.com/library?file_id=libfile_b0573d581d088191ac5f98340866246a&account_id=personal), Section 6, lines 249–337, was read. Its Theorem 2 explicitly includes timing and addresses in h_j. The handoff §15 has the same safeguard. The new experiment tests a specific way that overhead can be forgotten; it is not a rerun of the matching or affine tests.

## A legal strict-C timing control
C has unordered allowed triples 012,123,234,340,401 and all permutations; there are 30 satisfying ordered tuples. Clauses use three distinct names and no constants/signs. Ordered R (40 tuples, first value beats exactly one other) is not used; no historical S/Q result is substituted.

For h>=1 let m=2^h and let U be uniform on {0,...,m-1}. Declare exactly three variables x_0,x_1,x_2. Encode the h bits of U by choosing, for each of the first h clauses, either
```
0: C(x_0,x_1,x_2)
1: C(x_1,x_0,x_2).
```
Every remaining clause is C(x_0,x_1,x_2). All these explicit inputs have the identical relation and count 30. Clause order/argument order is permitted by the handoff encoding, even though C is symmetric. With w=2, the exact original encoded length is
```
N=3+1+2 floor(log2(m+1))+1+6m = 6m+2h+5.
```
There is no succinct-padding assumption: every clause is written and read.

A single fixed correct counter recognizes this exact syntax by full parsing, extracts U, then prepares a unary extent of length U+1 on its writable tape. It executes the fixed phase below and returns 30. On other valid inputs it uses a complete enumeration fallback. It is therefore a correct total solver, but NO global polynomial bound is claimed for that fallback.

The phase has constant alphabet and states START, RIGHT, BACK, DONE. It begins at a marked origin; an end marker is U+1 cells to the right. START writes a start symbol and emits label 0. RIGHT moves until the end marker, then BACK returns to the start symbol. The final transition writes the finish symbol and emits label 1. Time is merely the observer's count of real transitions, never an input to the machine's transition function. Preparation and later count output are part of the surrounding solver.

The two labeled events are at phase indices
```
I=(1,2U+4);     P=(0,1);     gap=2U+3.
```
Take B=N (equivalently h on this family), one obligation, q=2, b=1 and r=1. The actual decoder is U=(gap-3)/2. Thus
```
H(U|B)=h,   H(I|B)=h,   H(P|B)=0.
```
Charging only the two one-bit labels would claim h<=2, false already at h=3,m=8,N=59. A fixed-h encoding of the observed gap uses h bits because it has exactly 2^h possibilities. If the timing is omitted altogether, no decoder from (B,P) exists. Those are the two honest alternatives.

This is a counterexample to payload-only LOCAL record capacity. The run takes many more than two transitions; its full-time bound is not contradicted. Nor is the count output carrying h bits: every answer is 30. This deliberately unnecessary work shows that reconstructibility of a trace statistic is not proof that every solver must expose that statistic.

The finite phase is a real constant-state tape transition system on a prepared segment. It does not model the preparatory parser as one free transition. A full implementation pays O(N^2) time and O(N) simultaneous total storage to recognize the source, build the unary extent, position the head, execute the phase and output 30 using straightforward scans. Short code does not remove those costs.

For a proposed GLOBAL polynomial cap, there is an additional quantifier caveat. No globally polynomial total counter is exhibited. If a hypothetical correct A has cap exponent a>=2, a wrapper that uses this recognized control branch and otherwise A has time O(N^2)+O_A(T_A(N))=O_A(N^a), with a changed fixed constant. Thus a global-cap assumption does not justify omitting event metadata. This statement does not preserve an a<2 cap or a prescribed numerical K, and does not assert the hypothetical A exists.

## Relocation, actual collection and sharing
The tested relocated phase starts at absolute position 2N. Its end marker is at 2N+U+1. The two event labels and inter-event gap are unchanged; each trace position shifts by exactly 2N. Moving and preparing there costs real work. No original input-cut visits are forced. Full configurations still include head location, unary extent, source and control.

The transcript is an external mathematical observation of the actual phase. A real implementation collecting timestamps must scan the relevant execution/trace, maintain a counter and emit indices. The experiment does not grant A a free stored clock or assume a missing transcript already exists. If a lower-bound proposal requires such a stored record rather than an external transcript, it must first prove that the solver supplies it or that a valid charged decoder can construct it. Otherwise the proposed obligation fails before applying entropy.

Here there is one record so r=1. Duplicating its demand J times uses the same two transitions J times and requires r>=J. It cannot amplify work while retaining r=1. For general adaptive selectors the proof above needs the pathwise overlap bound, not merely an average number of different task names.

If the decoder already has the source bytes, U is determined and H(U|B)=0. The same is true if B includes a cache containing U. H(output|complete deterministic state)=0 throughout. Moving information between B and the record changes the demand and cannot be used to count the same information twice.

## Resource ledger and cap comparison
| Resource/stage | Charge and scope |
|---|---|
| Parsing/source authentication | Full source scan; identify n,m, check all actual clauses and canonical tail. No semantic hash merge. |
| Discovery/failures | One fixed recognizer and phase; failed recognition leads to the separately charged fallback, not UNSAT. |
| Representation change | Extract h input bits and build the actual unary extent; O(U) spatial distance is real, not an unbounded integer instruction. |
| Access/addresses | Tape moves are primitive steps; encoded event positions need O(log T) bits when retained. Relocated addresses remain charged. |
| Recursion/caches/sharing | No recursive phase; fallback state is separate. Any retained caller/source/output data contributes simultaneously. Duplicate obligations require their real reuse factor. |
| Recompute | Regeneration of extent, source or transcript costs again. |
| Output | Count 30 and any exported transcript must be written. Constant count length does not make long metadata free. |
| Physical peak/CM on controls | O(N) total storage and O(N^2) wrapper time give conservative O(N^3) physical CM; not a lower bound. |
| Descriptive CM | Keep K_U(C_t|A), with no free input/time, separate. Small descriptions do not supply a fast physical simulation. |
| Research tests | Python source semantics and finite tape-phase transitions; not end-to-end one-tape compiler timing or heap measurements. |

For fixed cap T<=K N^a retain S O(N^a), physical CM O(N^(2a)), descriptive CM O(N^(a+1)), count-map circuits O(N^a log N). No combination of this control's entropy and another solver's time/space is used. Excluding one exponent is not exclusion of all polynomials; counting hardness alone is not decision hardness.

The all-SAT control is intentionally not a proposed hard decision family. The new Construction three-color image still lacks compulsory U_j and actual decoders. This audit prevents assigning constant capacity to sparse selected records that use uncharged timing; it does not provide the missing obligations.

## Reproducible finite evidence
Code: experiments/t5_accounting_event_selector1_20261121.py.
Raw: results/raw/t5_accounting_event_selector1_20261121.json.
Reproduce: python experiments/t5_accounting_event_selector1_20261121.py.
Code SHA-256: 99f64df3ec319153b0ac558076acb784a0a8d103e52a6acc4ac8c1aa4ff3ae13.
Raw SHA-256: e5241d93d741935396b523b54725db3a63ba599edffcfa3e102ea9ad4bc492d8.

All 126 U values for h=1,...,6 were tested. On each source, 125 five-valued assignments were checked: 15,750 assignment evaluations, all counts 30. Every phase's actual transition count and event-index decoder agreed. Relocation preserved labels/gaps and translated each head position by 2N. Payload entropy is exactly zero; index entropy and U entropy are h because their finite maps are injective. Payload-only capacity fails for h=3,4,5,6. No random seed or asymptotic extrapolation. The universal coding statement is proved by the chain rule.

## Gates, sources and one next dependency
Affine/Tseitin, private-leaf trees and forced-domain controls remain legitimate cheap algorithms; no witness-state count is used. Complement/renaming/caching are not excluded. Decision-witness packing is not invoked. DISJ gate: no communication problem imported. Relativization: the coding identity alone supplies no nonrelativizing hardness. Simultaneous DTISP: same-run costs retained, no new forbidden region. Deterministic configurations: observer timing is not a free machine clock. Natural Proofs/algebrization: no general circuit lower bound proposed.

[Baseline §15](https://github.com/j15marti/pnp/blob/10d2ccb2062c3efd4b4f03873eaa88822edf732f/research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md) and [original entropy §6](https://chatgpt.com/library?file_id=libfile_b0573d581d088191ac5f98340866246a&account_id=personal) retain their explicit metadata premise.
John Duchi, [Lecture Notes on Statistics and Information Theory](https://web.stanford.edu/class/stats311/lecture-notes.pdf), December 6, 2023, Chapter 2, chain-rule derivation on page 17 was read as foundational context. The selector-aware inequality is derived explicitly here; no external unrestricted lower-bound theorem is imported.

**ONE next dependency, owner Accounting, review Redteam:** T5-3COL-DYNAMIC1 remains OPEN. For one declared distribution on Construction's graph-color image, exhibit obligatory U_j with side information including actual retained source/cache state and either B-determined selectors or fully charged selector descriptions. Prove bounded reuse and a net demand exceeding b r K N^a; if the decoder needs unavailable virtual answers or free timing, retire it. Synthesis should treat this report as a capacity correction/control, not positive lower-demand progress.

No checkout/preflight/LaTeX build; no TMR manuscript ownership or edits. Owned report, code, raw data and handoff are published with current-head protection and exact readback. P versus NP remains OPEN.
