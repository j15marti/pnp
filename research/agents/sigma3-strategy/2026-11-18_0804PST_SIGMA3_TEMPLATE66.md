# SIGMA3-TEMPLATE66: Hereditary two-template guard still encodes arbitrary SAT
**Timestamp:** November 18, 2026, 08:04 PST (America/Los_Angeles).
**Scientific status:** PROVED/EXACT scoped reduction, independently audited finite tests, conditional K/L ledger. P versus NP OPEN. Independent mathematical review pending.

## PROPOSE before SEARCH
Four proposals recorded first in local PROPOSALS_BEFORE_SEARCH.md: (1) constant-width pointwise OBDD guard, (2) exact two-sided YES/NO continuation, (3) quantifier-prefix and source-replay adversaries, (4) fractional SAT query contrast using certified independent blocks.
SEARCH then inspected project GUARD65, RECURSIVE64, SEP63, and proof1.txt, and primary sources Schaefer 1978, Bryant 1986, Dreier-Ordyniak-Szeider 2024, Fortnow-Lipton-van Melkebeek-Viglas 2005.

## THEOREM A: Two-template quantified SAT encoding
For any 3CNF F(x) define g_F(x,y)=NOT F(x) AND y, where y is ONE universal challenge bit. Build
Phi_F = EXISTS x FORALL y EXISTS z: [z=g_F(x,y)] AND [z=0].
When F(x)=1, g_F(x,y)=0 for both y, and z=0 always works. When F(x)=0, y=1 forces z=1 and z=0 simultaneously. Therefore Phi_F TRUE iff F SAT. The source-only translation has linear gate size, and the restricted language is NP-complete (membership by witnessing x and checking two y values).

For EVERY fixed x, the guard as a function of y is exactly one of two Boolean functions: constant 0 or identity y. Each has a reduced OBDD with at most one nonterminal decision node. Even the number of distinct possible guard functions is at most two. Yet finding a reachable constant-zero class of x is equivalent to SAT(F). Any restriction of outer x variables leaves the same two-template property, although the residual CNF may remain unrestricted and parent-sized. This is a hereditary *local-template* property, NOT a hereditary SAT query compression.

A fully explicit functional circuit Trace_F(x,w) with deterministic equalities for each gate makes the gate trace w unique for every x. The precondition z=g_F(x,y) similarly forces unique z, but the postcondition z=0 may be impossible. Gate-trace uniqueness does not supply a winning globally committed x.

## THEOREM B: Constant-size strategy descriptions, hard winning validity
TRUE instances admit x*=satisfying assignment to F and constant Skolem z(y)=0. FALSE instances admit the constant universal Herbrand strategy y(x)=1. After x is fixed, the continuation service evaluates F(x) from the source and answers YES with z=0 or NO with the contradictory equalities z=1 and z=0. Negative results require actual evaluation.

Given source F, validating that the fixed universal strategy y(x)=1 wins for all outer x is coNP-complete, since it holds exactly when F UNSAT. Nonvalidity has a polynomial witness x satisfying F. Thus two tiny candidate strategy circuits are not globally verified certificates; in particular a short Herbrand circuit cannot be taken as a free UNSAT proof.

## Conditional fixed-machine time and space ledger
Assume one fixed uniform deterministic SAT decider A with time m^(K+o(1)) and writable space m^(L+o(1)), K>=1, L>=0. Phi_F can be decided by one actual A(F) call, with time N^(K+o(1)). Using a full encoded query buffer, peak writable space is N^(max(1,L)+o(1)). To extract x*, make at most n<=N successive calls A(F|prefix) on length-O(N) inputs, counting YES and NO calls; total time N^(K+1+o(1)), peak space N^(max(1,L)+o(1)) on the SAME machine with one reused buffer and streamed output. For FALSE, establish A(F)=NO before asserting y=1 wins. Fixed (x,y) service evaluation costs O(N) time using read-only-source replay. No unconditional lower bound is asserted.

These actual SAT queries are parent-sized, lambda=1. The pointwise one-node guard OBDD is NOT a SAT query. The fractional guest term beta+1-lambda+lambda K obtained in earlier SEP63 applies only to authenticated block decompositions and does not follow here.

## Adversarial computational audit
Primary Python script: 880 quantified 3CNF cases, 402 SAT, 478 UNSAT, exhaustive x,y,z, 336,951 assertions, zero discrepancies. Independent Node.js bitmask implementation: 906 CNF cases, 600 SAT, 306 UNSAT, 22,618 checks, zero discrepancies. Total 359,569 checks, zero discrepancies.
Controls include exact prefix reversal (EXISTS x FORALL y [x=y] false, FORALL y EXISTS x [x=y] true), z=y identity, 800 independently brute-forced GF(2) systems with primal or dual witness uA=0, ub=1, integer/permutation flow and parity conservation on K_(4..10),(4..10), and uniquely forced g trace.

4096 disjoint ternary clauses serialized with integer literal lists: 70,814 parent bytes; two variable restrictions leave 4095 clauses and 70,806 bytes. This establishes a source-preserving restriction obstruction only, not an incompressibility theorem or SAT lower bound. Even after two pins, the pointwise guard has only two possible templates.

## STATUS AND NEXT EXPERIMENT
Restricted theorems PROVED/EXACT (independent review pending), finite checks COMPUTATIONAL, SAT K/L ledger CONDITIONAL, arbitrary input hereditary lambda<1 OPEN, forbidden joint time-space pair OPEN, P != NP OPEN.
NEXT: Replace single y with authenticated bounded-width OBDD selecting Horn versus GF(2) local continuations, with a nonlinear SAT-dependent outer selector; after two actual pinning rounds certify source acquisition, whether reachable winning outer class still encodes SAT, correct positive and negative calls, physical guest length, source scans, and peak same-machine workspace. Require a genuine solver-dependent, inheritable sublinear query rather than merely a small local guard.

## REPRODUCIBILITY
Complete report and runnable Python/Node auditors bundled in conversation file SIGMA3_TEMPLATE66_20261118_bundle.zip.
SHA256 report: 94f6624bbc9009664fa870e4fea11b88dbf6012d16ef5a85811e99a4416ef3d0
SHA256 Python: 79f534c305b264603d57016169c3415c93bf96496950125dbcb14f099d5394e3
SHA256 Node: 1dd146b4a6bc64d95068d67a4ac2d4cce90b034141647e42cd93f80237ae01ec

## REFERENCES
[1] Schaefer, *The Complexity of Satisfiability Problems*, STOC 1978, doi:10.1145/800133.804350.
[2] Bryant, *Graph-Based Algorithms for Boolean Function Manipulation*, IEEE Trans Computers 1986, doi:10.1109/TC.1986.1676819.
[3] Dreier/Ordyniak/Szeider, *SAT Backdoors: Depth Beats Size*, JCSS 2024, doi:10.1016/j.jcss.2024.103520.
[4] Fortnow/Lipton/van Melkebeek/Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 2005, doi:10.1145/1101821.1101822.

FINAL-SENTINEL-SIGMA3-TEMPLATE66-OPEN