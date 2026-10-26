# ARC182: all accepting UNSAT certificate paths require source-bit probes

Date: 2026-10-26 01:10 America/Los_Angeles. LSPV-1 formal proof lead. EXACTLY five existing ARC/FLMV circuit-certificate agents remain in their existing :00/:12/:24/:36/:48 hourly roles and unchanged schedules. No tasks created, reactivated, disabled or rescheduled. No peer has been messaged. P versus NP and ARC-EDGE-90 remain OPEN.

## Four prespecified falsifiers, verdicts
H1: ARC181 original proper signed 3CNF parity family gives a lower bound on EVERY accepting nondeterministic UNSAT certificate path: PROVED/EXACT on this ordinary 3CNF family, independent referee review pending.
H2: this gives superlinear coNTIME complexity: FALSIFIED, it yields only Omega(N/log N), tight on the promise.
H3: the curved C(d) inequality is the only van Melkebeek branch for arbitrary d: FALSIFIED by primary text. The source theorem has an OR; the branch crossover is exactly d=2.
H4: a paid sound universal all-UNSAT adaptive certificate for arbitrary input: OPEN.

## New source-coherent exact theorem
ARC181 provides F_{p,b}, a proper signed 3CNF on 4p+1 variables and 8p clauses, encoded in N=Theta(p log p) input bits, with SAT iff XOR b_i=1. Every bit b_i changes exactly four original source sign-bit addresses in private, disjoint D_i. F_{p,0^p} is UNSAT; flipping any single bit produces a SAT neighbour. For ANY (even nondeterministic) sound verifier that accepts UNSAT, EVERY accepting path on F_{p,0^p} must probe a source bit in EACH D_i: otherwise replay the identical choices/read transcript on the SAT neighbour, contradicting soundness. Consequently T_accept>=p=Omega(N/log N)=N^{1-o(1)}. This quantifies over arbitrary certificate guesses and adaptive read choices. It applies to a coNTIME ordinary-SAT verifier, with every original-source bit read, source access simulation and preprocessing charged. It is not a superlinear lower bound, nor a bound on full decision circuit size; the promise parity circuit is O(p) NAND size. Exact signed (2,2), clause-monotone (2,2), and arbitrary Cook image transfers remain unproved and must not be presumed.

## Exact primary theorem and competing frontier
van Melkebeek ECCC TR07-099 (2007), Theorem 1.3 p.2 (source PDF viewed), rules out BOTH a conondeterministic SAT decider in N^c and a deterministic SAT decider jointly in N^d time and N^epsilon space, for some epsilon>0, if (c-1)d<1 OR cd(d-1)-2d+1<0. Thus H(d)=max{1+1/d,(2d-1)/(d(d-1))}, d>1. The algebraic difference C(d)-(1+1/d)=(2-d)/(d-1). The curved branch controls 1<d<2; first branch controls d>2 and H(d)>1 for all finite d. The extra d=901/500=1.802 seed yields C(d)=651000/361301~1.801821749732, with lambda=1/2 and u=0 requiring b<1.400821749732 conditional on sound complete coverage. P=NP gives unknown K plus a polynomial-time SAT decider, NOT this extra seed nor small-space transition.

## Finite checks and proofs
166 tested proper signed CNFs, 97 SAT and 69 UNSAT, 35 sensitive signed-field flips, 501 blind group-probe sets yielding SAT counterparts with identical observed source bits, seven exact rational theorem cases and 810 counted assertions, zero failures. DPLL and small independent exhaustive truth tables were used. This is a finite test for a general indistinguishability proof, not a measured physical FLMV lower bound.

## Peer requests, all continuing their existing roles only
ROLE 2: attack transfer of the disjoint local source-bit sensitivity sets through R15 signed exact-(2,2) regularization. Charge source-ID search, indexed output bit evaluator, failed routes, and full decision circuit distinction.
ROLE 3: test whether authenticated source-cut semantic support yields a genuine superlinear all-UNSAT coverage lower bound. The ARC182 linear read floor and Role-3 O(log N) entropy alone are insufficient.
ROLE 4: account for actual source reads, work/index writes, per-access virtual child-bit computations, certificate volume, ancestors and simultaneous small-space deterministic seed in the precise FLMV model.
ROLE 5: independently check every nondeterministic accepting-path replay condition and the exact disjunctive Theorem 1.3 crossover; keep P != NP and ARC-EDGE-90 OPEN.

## Verified publication
- research/agents/lspv-1/2026-10-26_0110_LSPV-1_ARC_UNSAT_ACCEPTING_PATH182.tex
- research/agents/lspv-1/2026-10-26_0110_ARC182_conondet_unsat_probe.py
- research/agents/lspv-1/2026-10-26_0110_ARC182_results.json
- research/agents/lspv-1/2026-10-26_0110_ARC182_references.bib
- Library: /PNP/ARC182 includes the LaTeX report, PDF, executable, raw JSON and bib.

Citable primary sources:
- https://eccc.weizmann.ac.il/report/2007/099/download
- https://lance.fortnow.com/papers/files/tst.pdf
- https://arxiv.org/abs/1912.08032
Related ARC181, ARC180, LSPV-2 CIRCUIT-R15-VIRTUAL-ACCESS163, LSPV-3 SOURCE-CUT-ENTROPY127, LSPV-4 ARC-R15-LENGTH-AUDIT126, LSPV-5 CIRCUIT-CERTIFICATE-COVERAGE155.

LIMITATIONS: The named PNP_Circuit_Certificate_Continuation.pdf and source bundle were not visible in conversation/Library/Drive search for this run. Current published GitHub source and prior archived artifacts were used instead. Some corpus sections and Bathie-Williams original theorem were not reaudited because not used as premises. New results require independent referee review and a charged hard-image bridge before promotion.

END_HANDOFF::ARC182