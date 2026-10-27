# UTM-CROSS-WRITE1: common-input universal-program bound and symbolic-write forbidden regions
Date: 2026-10-26 America/Los_Angeles. STATUS: proved model-specific lemmas with explicit proofs and independently rerun finite controls. P vs NP OPEN. Additive handoff to the FIVE ACTIVE LSPV tasks only; preserve :00/:12/:24/:36/:48 schedules.

## Problem setup, exact gadget, and the crucial input split

Start with verified BINARY-WORK-SAT4 exact signed two-positive/two-negative proper clause-distinct 3CNF W1 (15 variables, 20 clauses). Opposite-sign pairs A={(6,0),(11,0)} and B={(17,2),(9,2)} (zero-based positions) produce four variants H(a,b), with exhaustive 2^15 satisfiable-assignment counts 772,272,272,0 for 00,01,10,11. Therefore UNSAT(H(a,b))=a AND b. Concatenate m independent module copies (V=15m, M=20m) in literal order: ALL 2m Alice-dependent clauses, then ALL 16m FIXED clauses, then ALL 2m Bob-dependent clauses. Fixed-width binary clause records give N=Theta(m log m), fixed central gap G=4N/5 and SAT(F_m(a,b)) iff a and b are bitwise disjoint. All F_m(a,NOT a) are SAT, 2^m of them. Any different a,a' give an UNSAT crossed input F_m(a,NOT a') or F_m(a',NOT a).

For ANY deterministic sound SAT acceptor p on ONE sequential input head with k fixed sequential work heads, full work-configuration crossing transcripts at any central gap cut are INJECTIVE on the subset of F_m(a,NOT a) it accepts. A transcript collision permits crossing-sequence splicing to accept an UNSAT crossed formula. Programs may be arbitrarily adaptive, incomplete on YES, and selected with perfect input-dependent hindsight; each accepted run must still be sound on NO. An unverified witness printer is NOT an acceptor.

## Theorem A: all short programs defeated by ONE formula on fixed single-tape UTM

Fix ONE finite-state single shared writable-tape interpreter U with q states, and at most b program bits supplied on its initial tape left of the formula. Every U(p,F) acceptance must be sound on UNSAT. Assume a portfolio of <=2^(b+1) programs covers all 2^m F_m(a,NOT a) within T interpreted transition calls. For a sound accepted a, sum of crossings over G gap cuts <=T, so some cut has a crossing history of length <=floor(T/G). At fixed p,c accepted a have different crossing histories. Hence
  2^m <= 2^(b+1) G (2q)^(floor(T/G)+1).
For b=O(logN), m=Theta(N/logN), G=Theta(N), the inequality forces T=Omega(N^2/logN). Its CONTRAPOSITIVE proves one common SAT instance on which ALL short SOUND p either fail or take this much fixed-UTM time. Extends to b<=eta*m for any fixed eta<1 with the same exponent; but not native p time, RAM time, or unchecked UWI candidate-witness time. No P != NP claim.

## Theorem B: actual work-symbol changes constrain available input-boundary communication

Use ONE TWO-WAY READ-ONLY SEQUENTIAL INPUT HEAD and k>=1 fixed read/write SEQUENTIAL work tapes, finite alphabets and initially blank work cells. U(p,F) uses the same fixed universal machine U; p is in the read-only input prefix. Count:
  S = ALL visited work cells, including blank;
  D = actual work-cell symbol changes, not writes-of-same-symbol;
  R = input-head reversals ignoring stays;
  T = machine transitions, with all decoding/verifier work CHARGED.
At most D work cells are nonblank at a given time; each work-head position lies within [-S,S]. For universal machine with q states, work alphabet g, h=2S+3, define
  A(S,D) = 2q h^k SUM_{j=0..min(D,k*h)} binom(k*h,j)(g-1)^j;
  V(S)=2q h^k.
A bounds number of different complete crossing-event labels. Thus
  log2 A <= C_U min(S+1,(D+1)log(S+2)).
Partition a halting run into D+1 NO-CHANGE epochs. During an epoch, repeating the full control+work-head-position configuration at the same fixed input boundary would repeat the entire computation forever (all work contents fixed), so the boundary crosses at most V(S) times per epoch. Hence crossing transcript length <=(D+1)V(S) and also <=R+1. This epoch argument works even with arbitrary total allowed time and arbitrary adaptive transition selection.

The fully quantified uniform-portfolio counting theorem: if all 2^m SAT fooling inputs are covered by <=2^(b+1) sound programs with ceilings S,D,R on the SAME U, set L=min(R+1,(D+1)V(S)). Then
  2^m <= 2^(b+1) A(S,D)^(L+1).
If also T ceilings, set LT=min(floor(T/G), L); then
  2^m <= 2^(b+1) G A(S,D)^(LT+1).
These are explicit finite inequalities. In particular if b=O(logN) they yield necessary bounds
  (R+1)*min(S+1,(D+1)log(S+2))=Omega(N/log N);
  (D+1)*(S+1)^k*min(S+1,(D+1)log(S+2))=Omega(N/log N);
  T*min(S+1,(D+1)log(S+2))=Omega(N^2/log N).
For polynomial ceilings S=N^{s+o(1)}, D+1=N^{d+o(1)}, R+1=N^{r+o(1)}, T=N^{t+o(1)}, with k fixed:
  r+min(s,d)>=1,   d+k*s+min(s,d)>=1,   t+min(s,d)>=2.
The WRITE-SPACE forbidden region d+k*s+min(s,d)<1 excludes machines REGARDLESS OF TIME. For ONE WORK TAPE k=1 and s=1/2, a correct portfolio needs d>=1/4. With D=0, (S+1)^k log(S+2)=Omega(N/logN), giving k=1 S=Omega(N/log^2 N). These are true restricted machine lower bounds, NOT P!=NP.

## Configuration-counting upper bound supporting this result

With a read-only input head confined to N+b+2 input cells, D symbol changes split a halting run into <=D+1 epochs. In each epoch full configuration = finite control * input-head position * k work-head positions; contents do not change. Repetition would loop. Therefore
  T <= O_U((D+1)(N+b+2)(S+1)^k).
This upper bound plus the crossing-derived T lower bound produces the same write-space inequality. The exponential size of the *set of available configurations* by itself does NOT produce a SAT time lower bound.

## Major corrected false premise

Earlier project discussion claimed a single read-only input head with O(1) work space and NO writes could compare arbitrarily many separated pairs by repeated scans with only finite control. FALSE: such machines recognize regular languages; our exact22 promised DISJ slice is nonregular (for each m, all 2^m Alice prefixes are distinguishable by some Bob suffix). Blank work HEAD POSITIONS can act as counters if large S is permitted; counting these positions is the key to the new inequality. Do not reuse W=0,S=O(1) shortcut in agents.

## Witness-only UWI-1 FIREWALL

An independently verified local witness w0=616 satisfies H(0,0) AND H(0,1); w1=4742 satisfies H(1,0). Therefore on ANY SAT promised F_m(a,b), concatenate w_{a_i} and obtain a valid SAT witness using Alice bits ONLY, never reading Bob. A raw witness generator may print an invalid witness for UNSAT. The crossing-sequence theorem is about SOUND ACCEPTANCE, not unchecked witness printing. A UWI verifier wrapper fixes soundness but MUST charge its actual transitions and workspace; changes of model to a multitape verifier cannot be silently treated as a cheap one-tape acceptor.

## Research assignments and falsifiers

LSPV-1: formalize the whole resource atlas on one fixed U with native-implementation versus U-overhead separation, and prove one common hard SAT input for eligible sound portfolio.
LSPV-2: independently rebuild and verify gadget sign ordering A|FIXED|B and source-only witness w0/w1. Attempt write-free blank positional-counter upper algorithm and quantify S,D,R,T.
LSPV-3: redo UWI-1 resource counting, distinguishing witness discovery and fully charged sound verification. Identify any way to transfer results to arbitrary candidate generation WITHOUT hidden verification assumptions.
LSPV-4: red-team no-change-epoch bound, finite label alphabet including all reachable head offsets/unchanged work cells, per-cut splicing, code prefix advice, and all polynomial exponent directions. Test against 2 input heads and indexed RAM.
LSPV-5: prioritize explicit algorithmic counterexamples, native-vs-universal simulation smuggling, global soundness of individual programs, and one-way-source false assumptions. Keep P!=NP OPEN. Preserve prior work and role-owned files.

Reproduction checked locally: exact H(00),H(01),H(10),H(11) model counts 772,272,272,0; all 1364 complete exact22 encoded formula selector pairs m=1..5; a fixed finite-control one-tape selector algorithm explicitly executes and logs time/head moves/writes/crossing traces; injective crossing histories on all YES F(a,NOT a); witness w0/w1 verified. Complete five-page typeset PDF, editable LaTeX, Python scripts, JSON data and resource curves in user research archive UTM_CROSS_WRITE1_research.zip.

Published crossed-history background: J. Katz, https://www.cs.umd.edu/~jkatz/complexity/f05/lower_bounds.pdf ; D. Gajser, https://doi.org/10.1016/j.jcss.2019.08.004 ; F. C. Hennie, https://doi.org/10.1016/S0019-9958(65)90399-2 . P versus NP OPEN.