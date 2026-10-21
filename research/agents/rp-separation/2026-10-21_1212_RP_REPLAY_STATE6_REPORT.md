# RP-REPLAY-STATE6: A polynomial replay-footprint theorem and a source-compatible SAT witness countermodel

**Date:** October 21, 2026, 12:12 Asia/Seoul investigative slot (report assembled during the same run).  
**Scope:** P versus RP exclusively.  
**Class statuses:** **P != RP OPEN; P = RP OPEN; P != NP OPEN.**

## 1. Claim and source-order protocol

Four distinct falsifiable proposals were written to `PROPOSALS_PREREGISTERED.md` before this run's fresh primary-paper searches: limited persistent-address graph reachability; persistent versus independently refreshed CNF witness evaluation; a source-accurate completion-time hash normal form; and a unique-witness dense-amplification counterexample. The first two are implemented and checked here. They constitute a restricted theorem and its hostile boundary, not an unrestricted class separation. The third remains only partially analyzed; the fourth is tested as a density control.

I directly fetched the **original** GitHub sources `AGENTS.md` (partly output-truncated), `COMPLETIONCUT1/README.md`, `completion_cut_audit.py`, `RANDOMSTOP10_theorem.txt`, `RP_BOOLEAN_QUOTIENT5_theorem.md`, and the 11:48 synthesis handoff and main report. I also read original 2026-09-24 REDTEAM-0004 and 2026-09-28 SIM-4-0006 Google Docs and three recent P-vs-RP peer handoffs. The cumulative `COVERAGE_LEDGER6.json` carries inherited records marked as inherited, as well as new direct inspection and the remaining inaccessible/unread portions. This is a **partial** historical reconstruction, not an exhaustive review of the project's GitHub, Drive, ChatGPT or archival Files.

## 2. Exact verifier and tape model

An ordinary RP verifier is a fixed uniform deterministic machine given a source input x of length N and an independent uniformly random read-only tape r in {0,1}^{m(N)}, with m(N) polynomial. It halts within T(N) polynomial steps on **every** tape. For the language L it recognizes,

\[
 x\notin L\implies \forall r\ R(x,r)=0,\qquad
 x\in L\implies \Pr_{r}[R(x,r)=1]\ge\tfrac12.
\]

Read-after-read of a given random-tape address MUST return the same bit. A random-access tape is not the same object as a sequential stream that emits an independent fresh bit at every request.

We count every source read, replay, tape address, program operation, input-head position, work-tape content, clock value and deterministic configuration. No uncharged advice, true random oracle, snapshot side table, source pointer, or external hash-hardness assumption is permitted.

## 3. ESTABLISHED restricted theorem: Polynomial replay footprint

**Theorem (bounded persistent-address support).** Fix a uniform verifier R with a known polynomial clock T(N), polynomial random-tape length m(N), and at most C(N)=N^{O(1)} deterministic configurations on input x of length N, excluding values of the random tape. Assume a uniformly polynomial-time procedure outputs an explicit list S_x of q(N) tape addresses satisfying:

1. On **every** execution path of R(x,r), any address outside S_x is requested at most once along that path.
2. Addresses in S_x may be requested arbitrarily many times, in any adaptive order.
3. q(N) <= c log_2 N for a constant c depending on the fixed R.

Then the language recognized by R under the RP one-sided-error definition is in deterministic P. A deterministic accepting tape can also be recovered on YES inputs.

**Construction.** Build a finite directed configuration graph. A vertex is `(time, ordinary-configuration, a)` where `a in {?,0,1}^{S_x}` records each persistent tape address as unobserved, previously observed 0, or previously observed 1. At a random read of address j:

- If j in S_x and a(j) is known, follow only the remembered value.
- If j in S_x and a(j)=?, branch on 0 and 1, recording the result.
- If j not in S_x, branch on a fresh 0 and 1 without retaining either bit.

All deterministic transitions are those of the original machine. Accept if and only if an accepting vertex is reachable from the start vertex.

**Soundness of graph reduction.** Every actual fixed-tape execution maps to a directed graph path. Conversely, given any accepting graph path, assign every persistent address the value recorded in `a`. Assign each nonpersistent address the value requested on its unique occurrence along this path. The premise guarantees no such nonpersistent address occurs twice. Extend arbitrarily to unread addresses. The resulting single fixed tape reproduces the entire graph path under the original verifier, proving genuine acceptance. The merging of finite machine configurations does not create false paths, because a hypothetical first repeated nonpersistent-address read on a spliced path would itself be an executable prefix under a consistent tape, contradicting the stated access discipline.

**Explicit resource bound.** There are at most

\[
 (T(N)+1)C(N)3^{q(N)}
\]

vertices, each of outdegree at most two. Enumerating reachable vertices takes

\[
 \operatorname{poly}(N)+(T(N)+1)C(N)3^{q(N)}\operatorname{poly}(N)
\]

time and at most the same polynomial order of live graph/storage space. The final polynomial includes reads from x, machine-description processing, source rereads needed for transitions, list construction and optional backpointer reconstruction. The random tape has **no runtime external randomness** in this deterministic graph simulation; accepting tape output uses at most m(N) bits. As q(N)=O(log N), `3^q=N^{O(1)}`. An RP NO input has no accepting tape, so the graph rejects. An RP YES input has at least one accepting tape, so the graph accepts. No exact probability computation is needed.

**Qualifications.** This is a standard configuration-graph/NL-to-P type argument with an explicit bounded-replay extension. It assumes the program has polynomial **configuration width**, not merely polynomial running time. The set S_x is required to be explicit and computable; asserting that only a few addresses will be repeated *after observing a particular random run* is not enough. No uniform polynomial running-time exponent across arbitrary machine descriptions is claimed.

## 4. ESTABLISHED hostile boundary: CNF global compatibility needs persistent values

Define a uniform random-access assignment checker W(F,r): parse a Boolean CNF formula F with n declared variables; for every literal occurrence x_j or not-x_j, read the **same fixed** random-tape bit r_j, and accept exactly when every clause is satisfied. W runs in polynomial time, uses O(log N) working bits for indices, scanning and a clause-success flag, and accesses n independent fair tape bits. Its acceptance density is exactly

\[
 \Pr_r[W(F,r)=1]=\frac{\#SAT(F)}{2^n}.
\]

Thus exact acceptance counting for this fixed source-readable logspace machine is #SAT-hard, a known counting-complexity phenomenon [6]. In contrast, **language membership** for the same verifier is not shown to be in RP: a uniquely satisfiable F has success only 2^{-n}, below RP's 1/2 guarantee.

A bona fide RP verifier recognizing a *trivial language* can retain the same hard counting behavior: let

\[
 E(F,b,r)=[F\text{ is well formed}]\land [b=1\ \lor\ W(F,r)=1].
\]

Malformed inputs reject on **every** tape. All valid formulas accept with probability

\[
 \Pr[E(F,b,r)=1]=\tfrac12+\frac{\#SAT(F)}{2^{n+1}}\ge\tfrac12.
\]

It uses n+1 unbiased bits, polynomial worst-case time, O(log N) work space for parsed proper CNF, source rereads charged, and zero advice. Its language is exactly the easily decidable syntax language of well-formed CNF formulas. Recovering its **exact** acceptance probability is nevertheless #SAT-hard. This is the precise language-bypass guard: a #P-hard property of one verifier need not make its recognized language hard for **any** deterministic decider.

### Replacing repeated reads by fresh bits breaks one-sided soundness

For n=3, consider all eight proper three-variable clauses, one for each choice of literal signs. Their conjunction F_8 is UNSAT and **minimally** so: removing any one clause leaves exactly one satisfying assignment.

Persistent assignment reads yield

\[
 \Pr[W(F_8,r)=1]=0.
\]

If every literal occurrence is instead replaced by an independent fresh random bit, each three-literal clause is satisfied with probability 7/8, independently across eight clauses. The altered evaluator accepts F_8 with probability

\[
 \boxed{(7/8)^8=5,764,801/16,777,216\approx0.343609>0.}
\]

Thus the altered evaluator **fails RP's all-random-tapes NO soundness**. This is not a change in runtime cost only; it changes the Boolean relation and loses globally compatible assignments. On the seven-clause uniquely satisfiable subfamily, the persistent success rate is 1/8, while fresh-per-literal success is `(7/8)^7`.

The exact threshold between the theorem and this counterexample is not a proven hierarchy boundary: here the set of recurrent assignment addresses has size n, whereas the positive theorem assumes at most O(log N) explicitly identified recurrent addresses. The counterexample does not establish an RP-versus-P lower bound.

## 5. Genuine candidate RP language: Arithmetic-circuit NONIDENTITY

The most concrete surviving *language*, already present in the prior :12 investigation, is arithmetic-circuit formal **NONIDENTITY**. Its uniform RP algorithm is fully specified here to avoid a hidden sampling loophole.

Encode an arithmetic circuit C over F_p with s gates and v<=s+1 variables, and prime p written in binary. Let D<=2^s be a known syntactic upper bound on its total degree. For this **restricted ordinary language** require that p is prime and p>8D, rejecting all malformed or invalid-domain inputs deterministically (AKS tests primality in polynomial time [7]). The YES inputs are circuits whose formal polynomial over F_p is not identically zero. The NO inputs are formally zero circuits and all invalid encodings.

Choose l=ceil(log_2 p) random bits per tentative field element and reject integers >=p. This succeeds with probability >1/2 on each attempt, and conditional on success the accepted residue is exactly uniform in F_p. For each variable try h=ceil(log_2(8 max(1,v))) independent attempts, rejecting the entire run if any variable runs out. The probability of successfully sampling all v independent field elements is at least 7/8. Conditional on that event, Schwartz-Zippel bounds the probability that the nonzero circuit evaluates to zero by D/p<1/8 [8]. Therefore the all-input YES acceptance probability is at least

\[
 (7/8)(7/8)=49/64>1/2.
\]

A formally zero circuit evaluates to zero on every field point and rejects every random tape. The coin budget is bounded *a priori* by `v*h*l=poly(input length)`, and arithmetic circuit evaluation plus validation is polynomial-time with no advice, randomness oracle, or indefinite rejection sampling. This proves NONIDENTITY is in RP in this model, **not** that it lies outside P.

The historic CNF clause-product polynomial cannot reduce SAT to this language: every proper clause polynomial is nonzero in the formal polynomial ring, so the full product is nonzero even for **UNSAT** CNFs. The eight-clause UNSAT cube has product value 208 modulo 257 at (2,2,2), as the original `RP_BOOLEAN_QUOTIENT5` theorem records and this audit independently checks. Substituting the field PIT membership algorithm for a Boolean SAT decider therefore fails soundness, not merely quantitative resource accounting.

## 6. Executable verification

`rp_replay6_audit.py` was run locally after its final edit. `RP_REPLAY6_raw.json` is the untouched standard-library output of this run.

| Control | Actual result |
| --- | ---: |
| Assertion-accounted checks | **14,880** |
| Failures | **0** |
| Exhaustive three-variable proper-3CNF clause subsets | **256** |
| Exhaustive 4-variable, 3-clause cases with repetition | **5,984** |
| Unique UNSAT full-cube formulas | 1 |
| Deletions from minimal-UNSAT cube independently tested | 8 |
| Persistent sample acceptance probability on full cube | **0** |
| Fresh-per-literal sample acceptance probability on full cube | **5,764,801/16,777,216** |
| Finite-field UNSAT clause-product at (2,2,2), modulo 257 | **208** |
| Field PIT for X^2-X at p=257 | 255/257 nonzeros |

All tested CNF labels agreed between exhaustive assignment enumeration and the bounded-replay state-propagation algorithm. These are finite implementation controls, **not** asymptotic lower-bound evidence. The complete symbolic proof is in sections 3 and 4.

## 7. Transfer audit and status

| Arrow | Scope and status | Exact obstruction |
| --- | --- | --- |
| poly configurations + q=O(log N) recurrent addresses -> deterministic reachability | **ESTABLISHED** | Strong model restriction; does not cover arbitrary RP |
| consistent Boolean assignment reads -> CNF witness checking | **ESTABLISHED** | YES probability can be 2^{-n} |
| independently refreshing repeated CNF variables -> valid RP SAT test | **FALSIFIED / RETIRED** | Minimally UNSAT cube accepts with positive probability |
| formal field polynomial nonidentity -> RP language | **ESTABLISHED** | Class membership only |
| SAT -> formal clause-product nonidentity with soundness | **FALSIFIED / RETIRED** | Boolean UNSAT can be formally NONZERO |
| source/trace or exact acceptance-count difficulty -> language lower bound | **OPEN; implication invalid without transfer** | Valid-CNF language is in P despite #P-hard exact density |
| some explicit L in RP -> L not in any deterministic polynomial time | **OPEN** | No all-deterministic machine lower bound |
| P = RP for all verifiers | **OPEN** | Arbitrary polynomial-time machines need not have polynomial configuration graphs or bounded replay |

The strongest new *necessary condition for a WRAPPER-based separation* is now: a proposed hard RP language cannot be realized solely by a fixed polynomial-width controller, independent one-off randomness, and a uniformly described O(log N) recurrent-address set. Otherwise graph reachability provides a deterministic polynomial-time bypass. It would have to violate at least one of these restricted hypotheses, and then separately exclude **every** alternative deterministic polynomial-time decider for the same language.

## 8. Next highest-value original-source test

Audit the **generalized** prime-lineage/completion-time WRAPPER's exact random-address trace, not just the three-stage toy. Instrument: (i) the number of distinct addresses that may recur over *all* paths (not just one sampled path), (ii) whether `r_i` replays or resamples, (iii) the complete nonrandom configuration count including counters, hash buffers and prime products, (iv) deterministic bypass by classifying SAT independently of transcript, and (v) exact one-sided guarantee on both source labels. If recurrent-address support is O(log N) and configurations polynomial, apply the theorem before making a new hardness claim. Otherwise test the first condition that fails, rather than declaring entropy itself a deterministic lower bound.

**Synchronization:** A local, source-checkable package is prepared. GitHub/Drive publication and independent peer readback must be recorded separately; report them as PENDING_SYNC unless independently verified. No root manuscript, peer task, or hourly schedules are changed by this investigation.

## References

[1] J. Gill, *Computational Complexity of Probabilistic Turing Machines*, SIAM J. Comput. 6 (1977), DOI 10.1137/0206049.  
[2] L. Adleman, *Two Theorems on Random Polynomial Time*, FOCS (1978), DOI 10.1109/SFCS.1978.37.  
[3] L. G. Valiant and V. V. Vazirani, *NP Is as Easy as Detecting Unique Solutions*, Theor. Comput. Sci. 47 (1986), 85-93, DOI 10.1016/0304-3975(86)90135-0.  
[4] N. Nisan and A. Wigderson, *Hardness vs. Randomness*, JCSS 49 (1994), 149-167, DOI 10.1016/S0022-0000(05)80043-1.  
[5] N. Nisan, *Pseudorandom Generators for Space-Bounded Computation*, Combinatorica 12 (1992), 449-461, DOI 10.1007/BF01305237.  
[6] L. G. Valiant, *The Complexity of Enumeration and Reliability Problems*, SIAM J. Comput. 8 (1979), 410-421, DOI 10.1137/0208032.  
[7] M. Agrawal, N. Kayal, N. Saxena, *PRIMES Is in P*, Ann. Math. 160 (2004), 781-793, DOI 10.4007/annals.2004.160.781.  
[8] J. T. Schwartz, *Fast Probabilistic Algorithms for Verification of Polynomial Identities*, JACM 27 (1980), 701-717, DOI 10.1145/322217.322225.  
[9] V. Kabanets, R. Impagliazzo, *Derandomizing Polynomial Identity Tests Means Proving Circuit Lower Bounds*, Comput. Complex. 13 (2004), 1-46, DOI 10.1007/S00037-004-0182-6.  
[10] Prior project original: `RP_BOOLEAN_QUOTIENT5_theorem.md`, verified GitHub current `https://github.com/j15marti/pnp/blob/main/research/review/outbox/rp-separation/2026-10-21_1112_RP_BOOLEAN_QUOTIENT5_theorem.md`.

**FINAL_VERIFICATION_SENTINEL::RP_REPLAY_STATE6::P_VS_RP_OPEN::P_VS_NP_OPEN**