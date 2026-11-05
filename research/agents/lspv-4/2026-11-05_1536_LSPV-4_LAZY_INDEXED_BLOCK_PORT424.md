# LSPV-4/424 | Lazy indexed SAT-child source port and hereditary failure
**2026-11-05 15:36 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | universal FLMV bridge OPEN; P versus NP OPEN.**

## IDEA, falsifiers, SEARCH, iteration
Initial proposed repair of LSPV-2/428: when a sound source decomposition supplies genuinely short locally addressable CNF children, run any fixed indexed guest SAT decider directly on *virtual read-only child input*, avoiding eager materialization. Falsifiers: (F1) arbitrary indexed guest jumps and index-tape erasures fail to simulate; (F2) separate SAT child labels are conjoined despite shared variables; (F3) hidden N-bit preprocessing, source authentication, address/caching overhead; (F4) produced children do not satisfy the required recursive decomposition grammar. For the explicit disjoint-block class F1-F3 have a paid repair and F4 fails: the construction is NOT a universal recursively iterable FLMV transform.

Actual repository sources: 2026-11-02 12:04 five-role handoff (blob c3889a3e), current issue #3 and newest peers, LSPV-2/428 (fd2b8d6d), LSPV-4/423, AGENTS.md, CODEX.md, pnp-research skill, actual GROKPROOF/2026-11-05_1218_PROGRESS.md (d3183283), actual Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6). Prior LSPV-1/147 already supplied a conditional lazy-access simulation, so the general principle is **not novel**. The new work is the explicit original-source block implementation, indexed read/erase instrumentation and failed hereditary-closure test. Primary literature: FLMV JACM 2005 DOI 10.1145/1101821.1101822 (full PDF §2.1 and page 4 inspected), Urquhart JACM 1987 DOI 10.1145/7531.8928, Ben-Sasson/Wigderson JACM 2001 DOI 10.1145/375827.375835, Pippenger/Fischer JACM 1979 DOI 10.1145/322123.322138. Authenticated sources: konard/p-vs-np proofs/complexity/README.md (finite one-tape model, *not* FLMV); blkph0x/p-vs-np-proof-research METHOD_INDEX.md and affine_projection_recognition_lab/AFFINE_HULL_METHOD.md (affine hull not exact arbitrary projection); openai/math lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (particular program, no arbitrary-A theorem); meelgroup/frat-xor README. Direct Google-branded access unavailable; indexed web and GitHub searches used.

## Component lemma: physical indexed virtual guest
Fix a parent source of bit length N and suppose a previously *proved and charged* reduction produces q<=N^(a+o(1)) children each of encoded length L<=N^(lambda+o(1)), and an exact Boolean combination of child SAT/UNSAT labels. Require: total local setup/validation/combination time <=N^(d+o(1)); all-phase local peak <=N^(rho+o(1)), retained ancestors <=N^(eta+o(1)); each child-input bit f(F,i,j) is retrievable in polylog(N) work and polylog(N) simultaneous scratch on the parent indexed read-only tape, with every source and index access charged. Then for any fixed uniform total indexed guest A of time O(L^(t+o(1))) and writable space O(L^(s+o(1))), a sequential virtual-input simulator obeys

$$
t'\le\max\{d,a+\lambda t\},\qquad
s'\le\max\{\rho,\eta,\lambda s\}.
$$

The implementation keeps guest work/index tapes physical, stores its virtual input position in O(log N) bits, and reconstructs each demanded child bit by paid index writes, original input reads, erased index words and returns to guest control; this includes nonsequential guest reads. No child input is materialized and no free SAT/equivalence oracle is introduced. The *eager materialization* contract instead needs s'<=max(rho,eta,lambda,lambda*s). This positive theorem is CONDITIONAL on the original source decomposition and is not the open all-input transformation.

## Source-authenticated hard-family test and exact dimensions
For a connected cubic graph G_h on h even vertices, each vertex parity constraint yields four proper 3CNF clauses, so a component has 4h clauses and 3h/2 edge variables. Odd charge is UNSAT, even charge SAT. Suitable cubic *expander* instances have 2^Omega(h) ordinary DAG Resolution lower bounds (Urquhart and width-size follow-ups), whereas a mixed AND3/GF(2) refutation of the odd component has 4h-1 paid nodes in the scope of previous fixed-calculus /341. Neither is an arbitrary-machine lower bound.

Make r=h contiguous components on disjoint edge-variable intervals, each with 4h clauses. Canonical bit encoding: CNF3 magic, self-delimiting Elias-gamma positive variable and clause counts and literal width, reserved zero bit; each signed literal uses 1+w bits where w=ceil(log2(3h²/2+1)). Parent and child headers H_p,H_c are O(log h), and

$$
N=H_p+12h^2(1+w),\qquad q=h,\qquad L=H_c+12h(1+w).
$$

Hence q,L are each N^(1/2+o(1)), with original source validator O(N polylog N) time and O(log N) peak scratch. Body bit j of child i is exactly original bit H_p+i*12h(1+w)+(j-H_c). The wrapper's correct final answer is AND of its children's SAT labels because variable sets are disjoint. That is true for *every* CNF in the stated syntactically recognized block class, not only Tseitin. An out-of-class but well-formed CNF must not be rejected as UNSAT.

If one block is a certified odd cubic-expander Tseitin and other blocks SAT, restricting other variables to satisfying witnesses converts any ordinary Resolution proof of the whole formula to a no-larger Resolution proof of the hard block. Thus ordinary Resolution hardness 2^Omega(h)=2^Omega(sqrt(N/log N)) is preserved in this particular 3CNF packaging. This does NOT transfer any lower bound to full mixed R or SAT machines. No strongly explicit expander generator was assumed for input-bit access: the compiler reads the original literal stream.

**OPEN / F4 failure:** Each child has only 4h clauses and therefore does not belong to the input block grammar requiring 4h² clauses. Thus the successful port is not recursively iterable; an unchanged-guest fallback would recover the /417 obstruction.

## Machine resource ledger and finite checks
The FLMV 2005 indexed read-only input has an erased index tape on each indexed jump. Each virtual read pays O(log²N) address arithmetic, O(logN) writes/erasures, original source-bit access and guest input-state update. Repeated accesses pay repeatedly; fully caching q bodies needs Theta(N) writable space. Class validation scans all input (not an uncharged proof hash). Sequential children contribute sum of guest times, not parallel critical-path max. Peak guest plus live parent and accessor is bounded separately from output. Logical inference-node work is not being inferred from this wrapper.

| Finite graph | Parent N bits | q | Child L bits | Source body reads | Physical index-word bit writes AND erases | Host scratch-register proxy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| K4 | 1212 | 4 | 344 | 1152 | 10988 each | 78 |
| Cube | 6212 | 8 | 830 | 6144 | 72216 each | 92 |
| Petersen | 10872 | 10 | 1146 | 10800 | 135448 each | 99 |

COMPUTATIONAL: independently executed Python original-source producer **58,869** checks and separately implemented no-import JavaScript checker **58,765** assertions on nine full originals (all-even SAT, one-odd UNSAT, all-odd UNSAT per graph). Every virtual bit inspected in nonsequential interleaved and reversed order; child truth checked by exhaustive variable assignments (6,12,15 edge variables), malformed/truncated/corrupted original encodings rejected, and valid but out-of-class cross-block variable mutation rejected by class recognition only. Every child fails hereditary membership. Host operation counters are NOT native FLMV runtimes.

## Corpus reconciliation and open arrow
No alteration to root main.tex: authenticated root retrieval returned blob 593000bb... but **zero bytes**, so overwriting would be unsafe. No changes to existing five task identities, schedules, enabled states, native R_mix341 rules or other specialists' manuscripts. The general lazy-access idea predates this run (LSPV-1/147); the new exact serial implementation is only a restricted positive control. The actual missing theorem remains an all-input, malformed-aware, recursively iterable, semantically sound constructor of q short locally addressable children for every correct SAT decider, with all preprocessing/failed policies/guest access and simultaneous memory charged. B3 is separate and OPEN. P versus NP OPEN.
