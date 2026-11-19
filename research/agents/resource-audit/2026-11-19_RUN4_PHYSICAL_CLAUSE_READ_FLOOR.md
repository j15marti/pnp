# Resource bounds run 4: physical-clause inspection and one-sided promise firewall

2026-11-19. P vs NP remains **OPEN**. **PROVED (elementary model-specific):** every physical record of any clause-critical UNSAT strict-T5 input must be accessed by a deterministic fully sound deciding or certified-refuting computation. **VERIFIED:** 167 independent original-C one-slot SAT mutations.

## Main theorem

Let F=(c_0,...,c_{m-1}) be a physically clause-minimal UNSAT strict-C source with m>=2, represented as m independently addressable fixed-width records of triples of distinct named variables. Let A be any uniform deterministic decision algorithm correct on all legal sources with this record format, or any combined UNSAT-certificate construction/verification computation that is sound even on SAT sources. All source accesses made by preprocessing, construction, source hashing and checking are charged.

**Then A must query every physical record on input F.**

For each i, choose j != i and form F_i by replacing record c_i with a duplicate of retained c_j. Because F is clause-critical, F\{c_i} has a witness w_i. That same w_i satisfies F_i, which remains a legal strict-C source of identical size, differing at exactly the i-th record. An algorithm that does not query i on F has exactly the same full transcript on F_i, by induction on its adaptive source queries. It therefore wrongly accepts an UNSAT claim on SAT F_i. Thus >=m distinct clause-record reads are necessary. This is an Omega(m) **source-access floor**, not a superlinear runtime lower bound, not an Omega(total source bits) bound, and not a universal statement about noncritical sources. A supposedly free trusted hash/source identity is outside this model: its generation/authentication must be charged.

## Reproducible finite audit

The canonical original predicate uses R(a,b) iff (b-a) mod5 in {1,3} and accepts C=30 of 125 triples; 125/125 independent consecutive-triple checks matched. Exhaustive six-variable evaluation of the native 4-C equality motif found exactly **20** SAT assignments, four per equal terminal pair, and **zero** with unequal terminals.

A new standalone audit independently checked the original-C witnesses in conversation archive `T5C_Native_Equality_Chain_Redteam_20261119.zip`, for sources k=1,8,32 with (n,m)=(7,5),(42,33),(162,129). For every one of **167** physical clause slots it verified all retained clauses true and deleted clause false, then produced a same-length SAT variant replacing just that slot by a second clause, and reverified the same full witness. At least **17,755** original-C source-position evaluations passed. No seed or probabilistic step.

Source archive SHA256 `ee3204648f8318fc0ff7d864923ae9f3f731136d7c3b90417285664135dfd94c`.

## Exact promise/polarity and path ledger

A uniform, sound UNSAT specialist which, on *every UNSAT legal input*, completes source reading, certificate output and independently sound verification within a known T(L) time and S(L) writable-space bound yields a deterministic **full** SAT decider by clocking T(L): output UNSAT iff a valid proof appears; otherwise SAT. Correctness requires no free UNSAT/SAT polarity bit. Dual statement holds for a uniformly SAT-complete sound witness specialist, reversing the timeout result. If both such specialists exist, dovetailing works without the clocks, charging both. For a k(L)-bit supplied nondeterministic path, deterministic exhaustive simulation may require 2^k attempts. Universal branches must all be considered or replaced by an independently verifiable symbolic proof. An existentially chosen block j(z) for one shared z is not a forall-z refutation.

Full scan for <=N^.195 rows, <=N^.65 blocks, per-child encoded length <=N^.35 and complete local cost p^a gives N^(.845+.35a), requiring **a<=97/70** for N^1.33. If each child actually needs k=beta log2 p path bits enumerated, effective bound is a+beta<=97/70. Full source reread for every row-block N^1.845; once per row N^1.195. Holding N^.65 arbitrary clause offsets as writable O(logN)-bit entries exceeds N^.5 bits. Bounding only private variable names does not bound encoded child clause length.

## Published bound and proof firewall

Buss-Williams, *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds*, Computational Complexity 24 (2015), 533-600, Figures 8.2/8.3 report SAT not in DTISP(n^1.34070,n^0.5) with a computer-aided 44-round/406-triple refutation **in the defined deterministic random-access input-bit-length model**: https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf . Fortnow, Lipton, van Melkebeek, Viglas, JACM 52 (2005), 835-865, https://doi.org/10.1145/1101821.1101822 separately distinguish deterministic from co-nondeterministic bounds. Williams, *Inductive Time-Space Lower Bounds for SAT*, 2006, https://doi.org/10.1007/s00037-007-0221-1.

For reduction length L=n^(1+delta+o(1)), a strict-C T=L^1.33 and S=L^.5 decider yields SAT T=n^(1.33(1+delta)+o(1)) and S=n^(.5(1+delta)+o(1)); direct comparison against the published half-space point needs delta=0. Exact machine simulation, source-local clause access, all-input correctness and full reduction cost must still be discharged. This numerical point does NOT imply P != NP.

**OPEN:** all-input low-row uniform obstruction-cover compiler with source-certified selection, full recursion accounting, and a theorem addressing arbitrary polynomial-time SAT algorithms.

## Artifacts

Reproducibility package: `T5C_Resource_PhysicalClause_ReadFloor_20261119.zip`, SHA256 `63773605bd697519f3981eab981577e2ab26b5cb20b308091523f12a751e84fd`. It contains `audit_clause_probe.py`, `results.json`, complete `changed_slot_witness_ledger.json`, `REPORT.md`, `HANDOFF.md`, and `SHA256SUMS`.