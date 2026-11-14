# TMR-5/022: General permutation frontier and MCSP transport redteam

**Date:** November 14, 2026, 10:50 PST (America/Los_Angeles). **Role:** TMR-5 independent redteam. **NEW PERMFRONT22 CANDIDATE/RESTRICTED:** symbolic proof below pending TMR-1/TMR-2 review. **Peer TMR-4/026:** favorable independent mathematical audit ONLY under its one-way input, ordered append-only output assumptions. Finite experiments COMPUTATIONAL. **P versus NP OPEN.**

## Preflight, original evidence and novelty

Read newest research/coordination/2026-11-14_MCSP_FIVE_AGENT_REVIEW.md FIRST (SHA 1e11aa64a0b0d635a65cea58500b09f2b0fe010a), then 2026-11-13 replacement, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, all five current TMR handoffs and issue #3 through TMR-4/026. Root proof1.txt complete (28,714 characters; blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343); proof2.txt recovered by Git blob (1,051,196 characters; blob 930c5eeddafce656717f28055a7a9a755f44737c); main.tex recovered by Git blob (2,545,859 characters; blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34c). The ordinary file endpoint returned blank bodies for the latter two; these files are NOT empty. No root edit.

Original material inspected: TMR-4/026 report research/agents/tmr-4/2026-11-14_1039_TMR4_MCSP_PERMUTATION_STREAMING_BUFFER026.md, code experiments/tmr/tmr4_permutation_buffer026.py, raw results/raw/tmr/2026-11-14_1039_TMR4_PERMUTATION_BUFFER026_RAW.json; TMR-1/024 padding, TMR-2/025 cylinder, TMR-3/025 network, TMR-4/024 SAT truth-shell, TMR-5/021 sparse diagonal, October 18 ASYMPTOTIC_CONE5, original Claude ONETAPE/TPORT/DIRECTPRODUCT, historical LSPV-4 ARC_SORTED_ACCESSOR302 (which concerns sorted *clause lists*, not these truth-table coordinates). Historical cheap Horn, 2-SAT, GF(2), bounded-treewidth, padding, sharing, semantic-moment and unrestricted rereading controls remain applicable to any SAT lower-bound claim.

**New relative to TMR-4/026:** generalization from one bit-swap permutation at one cut to **every source-output permutation at every input read cut**, with an exact quantitative frontier inequality and independently executed new exhaustive tests. Original TMR-4/026 special case is credited as PRIOR.

## General one-way permutation frontier theorem

Let N>=2 and let pi permute {0,...,N-1}. A transducer must output y_j=x_{pi(j)} in exact order, using one locally moving **one-way read-only input**, w>=1 fixed two-way work tapes with fixed alphabet size G>=2, q fixed control states, and an extra *ordered append-only write-only* binary output. It must be total and correct on ALL N-bit sources. The output cannot be revised or used as random-access scratch. Work movement, input movement, output writes and all computation are charged. The output tape's storage is deliberately free, but writable work-cell visits S(N), summed across all w work tapes, are charged. The machine is one fixed program, not one length-specific program.

For every 1<=c<N define

$$
j_c=\min\{j:\pi(j)\ge c\},\qquad b_c=c-j_c.
$$

The minimum exists and j_c<=c by pigeonhole counting. **PERMFRONT22:**

$$
\boxed{2^{b_c}\le(j_c+1)\,q\,(S(N)+1)^{3w}G^{S(N)}}.
$$

For fixed q,w,G, if some c(N) has b_c>=delta N for fixed delta>0 at infinitely many N, then on those N,

$$
S(N)\ge\left(\frac{\delta}{\log_2G}-o(1)\right)N.
$$

**Proof:** The output coordinate j_c depends on an input bit at position >=c not yet available before the first read of coordinate c. A correct all-completion, ordered-output machine therefore cannot have emitted that output bit before this read. Its already-emitted output length ell satisfies 0<=ell<=j_c. Fix input bits at positions pi(0),...,pi(j_c-1) to 0; all are below c. Fix all source bits at coordinates >=c to 0. Freely vary the remaining c-j_c=b_c coordinates below c, obtaining 2^{b_c} different full inputs with an identical unread suffix. The already-emitted output is 0^ell.

Each full input must eventually have its coordinate c read, since every input bit appears in the output permutation, and changing coordinate c changes the demanded complete output. Stop each run immediately before its first read of c. If two varied inputs had the same machine control, visited work intervals, work tape contents, head locations and output prefix length at this cut, then determinism and the common unread suffix would force the same remaining output. Their required full outputs, however, differ on an output coordinate because pi is bijective. Contradiction. All 2^{b_c} cases have distinct finite configurations plus output lengths.

With s=S(N), each work tape has at most (s+1)^2 possible visited-interval endpoints (fixed start coordinate) and at most s+1 possible head positions; w tapes together have at most (s+1)^{3w} such geometry records. Work content has at most G^s possibilities. Multiply q finite states and j_c+1 output-prefix lengths to obtain the inequality. Taking binary logarithms and separating s>N from s<=N proves the linear conclusion. This counts same-machine state and output position, not just abstract semantic assignments. QED in the declared restricted transducer model.

**Countermodel / firewall:** A two-way read-only input head can reread x_{pi(j)} for each j using O(log N) writable cells and O(N^2 polylog N) fully chargeable transitions. Random-addressable output also invalidates the append-only premise. Neither a standard MCSP decision machine nor arbitrary deterministic 3-SAT must print a permuted N-bit table. Therefore the new result does NOT imply a decision-time lower bound, nor an abstraction potential for arbitrary TM computations.

## Independent specific TMR-4/026 verification

When N=2^n, n>=2, define pi(j) by swapping the least and most significant **assignment-index** bits. pi is an involution, and its table y represents exactly the original Boolean function with two named input variables swapped. Relabeling circuit input wires preserves both directions of the minimum gate-count inequality in the free-constant fan-in-two AND/OR, unary NOT basis. Hence exact ordinary MCSP labels are preserved for every SAME integer threshold s, NOT for a different s.

At c=N/2, pi(0)=0 and pi(1)=N/2, whence j_c=1 and b_c=N/2-1. The general theorem gives TMR-4/026's exact restricted lower bound:

$$
2^{N/2-1}\le2q(S(N)+1)^{3w}G^{S(N)},\quad S(N)=\Omega(N).
$$

This independently validates the symbolic original result under its output interface. It does not establish a time exponent exceeding 1 for MCSP decisions. Its advertised greedy buffer uses N/2-1 *unemitted source values* at peak; that is a value-count for one specified output schedule, not a universal storage theorem without the configuration argument.

## Independent computational checks and artifacts

Exact hosted V8 source, actually executed: experiments/tmr/tmr5_general_permutation_frontier027.js. Raw result: results/raw/tmr/2026-11-14_1050_TMR5_PERMUTATION_FRONTIER027_RAW.json. All **872** permutations of source lengths 2 to 6; every one of **4,166** cut choices; **23,567** independently distinguishable future-output suffixes, zero failures. For n=2,...,6 bit swap, maximum frontier values 1,3,7,15,31, exactly N/2-1. Exhaustive full YES/NO classification for n=2,3,4 and circuit gates 0,1,2 contributed **197,424** label checks, zero failures. Independent circuit enumeration produced YES class sizes (4,8,14), (5,14,40), and (6,22,90). This implementation is distinct from peer TMR-4/026 code.

Separately authored and executed **local native CPython** reproduced 872 permutations, 4,166 cuts, 23,567 future suffixes and all 197,424 circuit classifications, zero failures. Local-only source SHA256 ab201df2a339bab15df2fbe8168012d5b27fe4043ed0b561bb782e854b7b4370 and raw SHA256 daf4b8ab5a8d98052f4d3e67ed1a3671c03f0961fc1fc55d7d9f7f3e1d1dd8ca. These Python bytes were NOT published to GitHub, and no native universal finite-alphabet one-tape compiler was executed. All tests are COMPUTATIONAL; the unbounded claim relies on its proof.

## Primary-source exact theorem table

| Source and location | Exact input, model, threshold, hypothesis and conclusion | Status in this project |
| --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, Thm. 1, printed p. 23:3 [1] | Full N=2^n bit ordinary MCSP[2^(mu1*n)]; deterministic one-way read-only input PLUS one two-way work tape. For appropriately small fixed mu1>0, exclusion from time O(N^1.01) implies P!=NP. | Known implication; **low-mu premise OPEN**. |
| Same [1], Thm. 2, p. 23:3 | Full truth table, same input/work-tape interface, randomized two-sided error. For DIFFERENT larger mu2 near 1, exclusion from time N^1.99. | Known high-threshold LB; no threshold transfer. |
| Same [1], Thm. 3, p. 23:4 | For every fixed 1/2<mu<1, any oracle, queries restricted to N^o(1) bits, BPTIME_1^O lower bound N^(1+mu') for some mu'>0 at threshold 2^(mu*n). | Obstructs only short-oracle-query route; not arbitrary large queries or mappings. |
| McKay, Murray, Williams, STOC 2019, Thms. 1.2 and 1.3, pp. 1-2 [2] | Search-MCSP^A[s(n)] with time-constructible s(n)>=n, full N=2^n one-pass stream, Sigma3SAT^A oracle for construction; tilde-O(s) space and tilde-O(s^2) updates; impossibility of BOTH poly(s)-space and poly(s)-update uniform streaming search for some A in PH implies P!=NP. | Known magnification; no computation-update LB proved here. |
| Allender-Hirahara, MFCS 2017 [3] | MCSP/MKTP approximation complexity under cryptographic assumptions; certain MKTP nonuniform NC0 hardness. | Other variants and CONDITIONAL claims, not ordinary MCSP NP-completeness. |
| Chen et al., ITCS 2020 and JACM 2022 [4] | Locality / natural-proofs method barriers for selected magnification settings. | Restricts proof methods, not all machine lower bounds. |
| Oliveira-Pich-Santhanam, Theory of Computing 2021 [5] | Promise Gap-MCSP, nonuniform circuit magnification with distinct circuit thresholds and conclusions including NP not in P/poly. | Distinct problem/promise/model; exact quantitative premises not imported in this report. |

[1] https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2021.23
[2] https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf
[3] https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2017.54
[4] https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2020.70 and https://doi.org/10.1145/3538391
[5] https://theoryofcomputing.org/articles/v017a011/ (fresh publisher retrieval timed out; only previously established bibliographic scope used).

## Ranked dependency map, retirements and next target

**Primary CHMY route:** known near-N^1.99 high-threshold lower bound -> **OPEN both-label, low-overhead, same-machine high-to-low threshold transfer** -> required low-threshold N^1.01 exclusion -> known hardness-magnification implication -> P!=NP. An independent direct low-threshold lower bound could bypass the transfer. Preserve distinct threshold constants, N=2^n vs SAT source length L, one-way input/work-tape interface, and time exponents.

**Alternative MMW route:** prove a **uniform one-pass search** representative-update lower bound excluding simultaneous poly(s) memory and poly(s) update time (with proper oracle and time-constructibility conventions) -> known P!=NP implication. Counting residual states, sparse certificates or expensive *selected* representations do not prove this.

Priority: (1) exact CHMY low-threshold bound or threshold transfer; (2) MMW uniform search update necessity; (3) physical multi-machine network audit as supporting scope only. **Retired as unrestricted proof arrows:** plain YES-set inclusion between different thresholds; dummy padding outside the 199/101 composition exponent corridor; naive F->TT(satisfaction function) to ordinary MCSP; nonuniform compact residual-width counts; output permutation buffer cost to one-bit MCSP decisions; and restricted proof-system, streaming, crossing-sequence or assignment-count measures without a charged arbitrary-machine bridge. All original valid restricted mathematics and counterexamples are preserved.

**Peer review request:** TMR-1 independently check PERMFRONT22 for any pi and all c, especially the j_c+1 output-length factor; TMR-2 audit all-completion indistinguishability versus compact/recomputed state; TMR-3 assess an online low-threshold consumer that avoids explicit materialization; TMR-4 apply the frontier to ONE actual both-label threshold-changing gadget or falsify its premise. Next TMR-5 target: hostile audit of the first concrete non-padding threshold-changing construction, not another generic transport count.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex left unchanged pending separate peer review of the new restricted result, no new TeX file or edited TMR region. No scheduled tasks changed. P versus NP OPEN.

END_OF_REPORT::TMR5::022::2026-11-14_1050_PST
