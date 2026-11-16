# TMR-3/063: certified schedule covers, live-frontier replay, and fully charged node queries

November 15, 2026, 23:47 PST. TMR-3 / PNP Time-Space Tradeoffs, Track B.

**Status:** PROVED/EXACT only as a conditional structural transfer for the declared deterministic, locally headed, read-only-source multitape model. The example is an explicitly described blank-start, work-dependent, two-data-block machine. Independent mathematical review OPEN. Executed tests are COMPUTATIONAL. No arbitrary-TM/HPV compiler, generic Cook-Mertz speedup, SAT lower bound, or P versus NP separation is claimed.

## Selected dependency and falsifiers

**C3-SELECTIVE-CANDIDATES-GENERAL-TRANSFER**, restricted advance: replace /062's all-first-block, exactly-two-candidate graph by a fully specified *public schedule-cover certificate* with up to polynomially many candidates and genuinely revisited, mutable work blocks. Integrate authenticated source -> source-independent candidate generator -> true blank-start block simulation with future-live cache -> FAIL consistency checking -> exact YES/NO output -> charged arbitrary node-bit replay. The model is restricted; the all-machine certified-cover existence remains OPEN.

Quantifiers: For each fixed constant-tape, finite-alphabet, total deterministic locally headed machine M with a read-only locally moving original input head, and each uniformly constructible t(N)=B(N)b(N) (possibly one final partial block), suppose a uniform public schedule family H(N,z,h,j), z in {0,1}^{r(N)}, gives work-tape block IDs at time blocks j=1..B, with: (i) b-block-respecting physical executions; (ii) at least one H_z exactly matching the canonical execution for EVERY valid original-source input x of length N; (iii) uniform source-independent access time tau(N) and auxiliary workspace g(N); and (iv) every z has at most w(N) future-live (tape,block) pairs at every cut. H is an implemented generator premise, not an oracle or guessed true trace. Authentic source parsing takes A(N) time and s_A(N) space. Invalid inputs reject deterministically. These are class promises, not silently inferred from arbitrary programs.

Four prior falsifiers: F1, an incorrect guess might discard information before its mismatch; F2, the public family might fail to contain some authentic data-dependent head trajectory; F3, dictionary scans, repeated H queries, source-head resets, failed attempts or arbitrary node queries might be free; F4, a restricted low-frontier algorithm might be promoted to unrestricted height-sublinear TreeEval or a forbidden DTISP pair.

## Exact conditional schedule-cover transfer

Put C=2^r and define
F_j(z)={(h,a): there exist i<=j<k with H(N,z,h,i)=H(N,z,h,k)=a}, w=max_{z,j}|F_j(z)|.
All of H, r, b, B, and t are length-public and actually constructible. For convenience H_z is checked for legal adjacent movement; a nonconforming candidate returns FAIL without claiming authenticity. The machine may use ordinary input-head movements, charged one physical step at a time. Per time block, each writable head occupies its stated active b-cell block; a move to an adjacent block may occur at the boundary. End-of-run state and both output labels are checked, not merely existence of a surviving certificate.

**Lemma 063A (certified-cover replay).** There exists one uniform deterministic blank-start source-to-output simulator which enumerates all C candidates. For each candidate it starts again from empty work storage, reconstructs only the blocks whose *candidate* next uses lie in the future, and tests every physical boundary transition. It returns FAIL on the first mismatch and accepts the first fully consistent candidate's actual YES/NO bit. No wrong candidate can be accepted. At least one candidate is consistent, so the returned bit equals M(x) for every authentic input.

*Proof.* At the beginning of an interval whose claimed head blocks still match the actual prefix, inductively all live cached blocks and current block buffers equal their authentic contents, and the finite state and source-head position agree. A previously touched block absent from the dictionary has no earlier-to-current use under the candidate: if it is requested now, the candidate would have to contain that future request and it would not have been discarded. First-time blocks are blank because the machine starts blank. Simulate the b genuine local transitions and compare the actual outgoing work-head blocks against the H prediction. A discrepancy returns FAIL at its first occurrence, before any alleged incorrect future access is used. Otherwise update authentic block contents and retain a completed block exactly if a later H lookup lists it. Induct. On a fully matching run every block read is authentic, so its output is M(x). Conversely the guaranteed true H candidate cannot fail. Duplicate encodings of the same trace are harmless, since all consistent candidates output the same deterministic bit. No semantic short-circuit, associativity assumption, or compulsory expensive graph is used.

**Exact query count per candidate:** for each tape and time block, one current H lookup, at most one next-boundary lookup, and at most B-j future lookups. Hence
Q_H^(1) <= p[B+(B-1)+B(B-1)/2] = p(B^2+3B-2)/2.
The same-run total H-query bound is C times this expression. For arbitrary requested graph edges, scan candidate H to reconstruct active block histories and last visits; each such graph-edge request costs at most O(pB tau) time and O(g+r+log B) auxiliary space. It is NOT a free edge oracle.

**Disjoint sequential cost partitions**, for a conventional multi-work-tape implementation using one sequential dictionary and p active b-cell buffers:
- Source authentication once: A(N) time, peak s_A(N).
- Per candidate source-head reset and schedule/counter setup: O(N+r+B log(B+2)) time.
- Per candidate genuine local transitions and output: O(t) time.
- Per candidate sequential dictionary searches, insertions, copying, and final dropping: O(pB(w+p)(b+log(t+2))) time.
- Per candidate H lookups with local parameter formation and scratch reset: O(pB^2(tau+log(t+2))) time.
Thus, with V=N+r+t+pB(w+p)(b+log(t+2))+pB^2(tau+log(t+2)),
T_total = O(A(N)+C V), and
S_peak = O(s_A(N)+r+g+(w+p)(b+log(t+2))+log(N+t+2)).
Every object in this expression lives on the **same realization**. Failed schedules cost full repeated work. Cache contents are ordinary writable tape cells, not a free sketch. The bound is conservative; a direct output shortcut is permitted.

**Lemma 063B (charged adaptive virtual checkpoint bits).** After selecting one fully verified z, retain its r bits. An arbitrary canonical node-content *bit* at time block j and tape h can be obtained by restarting from the blank original source, executing the verified z prefix chronologically to j, and extracting the named active-block bit before evicting it. Additional time per request is at most O(V), and additional workspace at most the replay workspace above plus O(log t) request indices. A requested first-visit source node is regenerated directly from authenticated original input or blank symbols. If a downstream evaluator issues Q adaptive node-bit requests with its own internal work T_E and peak space S_E, the fully charged composed upper ledger is
T <= O(A+(C+Q)V+T_E),  S <= O(s_A+r+g+(w+p)(b+log t)+S_E+ell+log(N+t)),
where ell is the number of bits physically retained for the requested label/buffer. Q and T_E are NOT known to be polynomial for generic nonassociative TreeEval. Height-independent chronological evaluation follows only under bounded frontier and public schedule coverage, not for all computation graphs.

The per-candidate physical time can be polynomial if t,N,tau,B,w are polynomial and r=O(log N). If w=O(1), g,s_A,r=O(log(N+t)) and b>=log t, the displayed restricted space becomes O(b+log t), independent of the graph height B. This is a legitimate restricted sublinear-height *frontier* evaluator even for arbitrary nonassociative finite-block transition functions, not the generic Cook-Mertz improvement sought in Track B. The HPV converter is not certified to produce small r or w.

## Explicit blank-start adaptive and revisiting control

The finite witness reads any binary input x of length N>=1, with EOF authentication, and uses public b=N+5, r=bitlength(N)=ceil(log2(N+1)), t=b(r+2)+1 and B=r+3. Since r<=N and 2^(N+5)>=(N+5)(N+2)+1, b>=ceil(log2 t), satisfying the admissible width. The first b-step block scans the original source and aligns an endpoint clock and DATA head at b-1; a second b-step block returns the source head and clocks. Both have fixed work-block movement. During each of the next r b-step epochs, the first four physical transitions read two genuine STATE cells and the current DATA cell, consume one original source bit, update both STATE cells and write the active DATA cell. All other transitions hold the DATA head until the last endpoint pulse. At that last transition the head moves between cells b-1 and b, or stays, according to the updated state, hence crosses tape blocks only at epoch boundaries. A final paid read outputs a Boolean bit.

The concrete nonlinear local update from old STATE (q0,q1), current DATA bit d and source bit x_j is
q0' = q0 XOR x_j XOR d,  q1' = (q0 AND (NOT q1)) XOR x_j XOR d.
Write q0' into the DATA cell, write both new state bits into genuine STATE cells, select the next DATA block by q1', and output q0' XOR q1' at the end. This machine is adaptive to both genuinely revisited DATA and STATE work cells, not merely a read-only movement string. A public candidate z in {0,1}^r specifies the DATA block after each branch epoch. Its trits are successive differences z_j-z_(j-1), with z_0=0. All other work heads stay in their first block; the complete schedule family is source independent, size C=2^r<=2N. The state tape, clock tape and DATA blocks have at most w<=4 future-live physical blocks across any cut. (A separate read-only input head is charged and is not a mutable work block.) No oracle selects the authentic z; the verifier checks it by source replay. The original instance is easy and may have a direct small-register algorithm. That shortcut is fully legal.

One physical clock half-sweep takes b steps through endpoint holds. The first four actions on a branch interval and the last head crossing fit because b>=6. Every block-head transition is local and the DATA head is always at one of the boundary cells b-1,b. This is an actual fixed locally headed machine specified symbolically; its compiled native transition table and exact bootstrap parser microtrace have not been run. It does not instantiate the unspecified HPV folded-copy compiler.

## Hostile cardinality control: public low-entropy coverage cannot be universal

**Lemma 063C (exact source-independent cover lower bound; restricted).** There is one different fixed total, blank-start, locally headed block-respecting machine U, with read-only original source x of length N, public b=N+5, t=b(N+2)+1, and B=N+3, for which the map x -> complete work-head movement word is injective on all 2^N binary inputs. Consequently, *any source-independent* family covering every U trajectory at that length contains at least 2^N movement words; its binary candidate ID requires r>=N. Thus the low-r structural premise of Lemma 063A is FALSE for this fixed machine if universally quantified over all block-respecting machines.

*Construction and proof.* Authenticate the original input during a b-step initial source scan, align a fresh DATA head at physical cell b-1, return the source head during another b-step epoch, and devote one b-step epoch to each x_j. During that interval, the DATA head either holds if it begins on the current block's rightmost cell, or traverses its b-1 remaining cells to that rightmost cell (if it entered on the leftmost cell at the previous boundary). All this occurs before the final transition of the time block. At the last step, move DATA right one physical cell, into the next block, iff the actual source bit x_j=1; otherwise hold. Thus each movement trit is exactly x_j. The entire process uses a genuine b-cell endpoint clock, local heads, blank initial work tapes and a final paid output step. Since distinct N-bit inputs give distinct movement words, a length-only cover must contain all 2^N words. The exact time t=b(N+2)+1 is polynomial, and b>=ceil(log2 t) for N>=1. An independent local Python enumeration checked all 8,190 distinct words for 1<=N<=12; this finite check is COMPUTATIONAL, the all-N injectivity proof is symbolic.

**Crucial limitation:** This is a lower bound only on *source-INDEPENDENT candidate-set cardinality*. A legitimate source-reading indexer outputs this very movement sequence in O(N polylog N) time and O(log N) writable workspace. The example gives no unconditional resource lower bound and does not prohibit a source-conditioned generator H(x,z,h,j) with its acquisition cost charged. This separates coverage entropy, authentic selection cost and actual decision difficulty. It blocks the naive attempt to apply the polynomial candidate-list condition to all machines, not the restricted theorem.

## Independent computational evidence and exact limits

Two byte-identical executions of the actually published self-contained Node source revision **tmr3-schedule-cover063-js-v1**, seed **202611152338**, completed **237,440 assertions**, **2,296 authenticated sources**, **43,044 paid candidate attempts**, **40,748 FAIL guesses**, **2,296 accepted true traces**, **237,988 public schedule queries**, **9,241 genuine DATA-cell reads (some first visits, some revisits)**, and zero unexpected failures. All source prefixes up to N=10 were exhaustive, supplemented by deterministic PRNG controls through N=64; seven malformed sources were rejected. Both output labels occurred (1,446 zero and 850 one). Source "100" visibly visits the second DATA block and then revisits the first. The model counted at most five simultaneously live full b-cell buffers, including active buffers. It explicitly checked local held steps on small inputs, but it did not compile the complete fixed transition table, reproduce the HPV converter, or execute Cook-Mertz's generic evaluator. The complete native all-step machine and external mathematics review remain OPEN.

Published executable: experiments/tmr/tmr3_schedule_cover063.js.
Immutable raw: results/raw/tmr/2026-11-15_2343_TMR3_SCHEDULE_COVER063_NODE_RAW.json.
Additional independently executed local CPython macro audit: revision tmr3-schedule-cover063-py-v1, seed 202611152337, 502,733 assertions, 2,296 sources, zero failures. This local prototype is supplementary, not confused with the exact published Node artifact.

## Mandatory four-gate table and controls

| Gate | Verdict, exact reason |
|---|---|
| DISJ sanity | PASS restricted: no rank-to-general-work implication. DISJ has a linear unbounded-fan-in depth-two circuit regardless of full cut rank; the theorem assumes a certified schedule family, and permits legal cheap shortcuts. |
| Relativization | NOT APPLICABLE TO A CLASS SEPARATION: none is asserted; the restricted positive simulator does not cross the BGS, algebrization, or Natural Proofs barriers. An NP bridge would require a genuine nonrelativizing step and is OPEN. |
| Simultaneous DTISP | PASS for the declared conditional scheduler/verifier; query generation, failed candidates, caches, source replay and final output are charged on one machine. General arbitrary-M and a polynomial-time height-sublinear TreeEval transfer are OPEN. |
| Configuration counting | PASS only as deterministic total-run upper-bound consistency, T<=2^{O(S+log N)}. No work lower bound or randomized/quantum inference. |

Controls: Horn/2-SAT, affine/Gaussian, treewidth, equality, autarky, products, selectors, padding, auxiliary-variable counting, compact representations, independent direct graph selection, sharing and recomputation remain admissible. The DATA control is particularly simple and admits a direct tiny-state evaluation. There is no field-dependent rank argument, randomized isolation, majority-tie or quantum error-model transfer. /341 remains FAIL as full logical UNSAT authority; /386 remains RESTRICTED.

## Primary references and independent review

[1] Ryan Williams, *Simulating Time With Square-Root Space*, STOC 2025, arXiv:2502.17779v1, especially Section 3.2 (candidate movement words, source graph, FAIL and implicit tree). https://arxiv.org/html/2502.17779v1

[2] James Cook and Ian Mertz, *Tree Evaluation is in Space O(log n log log n)*, SIAM Journal on Computing 2025 (published October 10, 2025), DOI 10.1137/24M1690126. https://doi.org/10.1137/24M1690126

[3] TMR-3/058, /061 and /062 original role reports and living-manuscript proofs; /058 required true source-only graph indices, /061 charged full dense guesses, /062 used exactly two public guesses. The current theorem adds a quantified schedule-family/frontier transfer with adaptive revisits, not a generic circuit lower bound.

**ONE next load-bearing lemma, C3-HPV-COVER-CERTIFICATE:** Pin one actual general block-respecting compiler or an explicitly identified wider natural source-machine class. Either construct a verifiable source-obtainable schedule-cover grammar with both r=O(log t) and w=O(1) for that class, and compose with a genuinely improved bounded-query nonassociative evaluator; or construct a real canonical counterexample to that specific pair of restrictions. The current compiler-independent conditional theorem does not claim every machine satisfies its premises. P versus NP remains OPEN.
