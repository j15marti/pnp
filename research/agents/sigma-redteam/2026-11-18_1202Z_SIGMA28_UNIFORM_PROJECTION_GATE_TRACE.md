# SIGMA REDTEAM28: Uniform-projection and gate-trace quantifier firewall

**UTC:** 2026-11-18 12:02. **Status:** PROVED/EXACT restricted coNP-completeness and trace-prefix facts; COMPUTATIONAL finite audit; all-input Circuit-SAT resource contraction OPEN; P versus NP OPEN.

## PROPOSE and SEARCH
Four adversarial controls: (1) universal intersection of trivial singleton relations supplied by a succinct circuit; (2) early gate-trace witness and illegally late global x placement; (3) separate gate-local witness challenges; (4) padded/delayed hypothetical solvers, input decoding and maximum work-address accounting.

Direct repository reads: `sigma-primary/2026-11-18_0303PST_SIGMA_PATHCUT_1.md`, `sigma3-strategy/2026-11-18_0626KST_SIGMA3_FIBER56.md`, `sigma-redteam/2026-11-18_0957Z_SIGMA27_JOIN_TREE_QUANTIFIER_FIREWALL.md`, recent commits. Primary literature: Yannakakis, *Algorithms for Acyclic Database Schemes* (VLDB 1981), https://www.vldb.org/dblp/db/conf/vldb/Yannakakis81.html ; Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability* (JACM 2005), https://doi.org/10.1145/1101821.1101822 ; Bova et al., *Knowledge Compilation Meets Communication Complexity* (IJCAI 2016), https://ijcai.org/proceedings/2016/147 ; Amarilli et al., *Connecting Knowledge Compilation Classes and Width Parameters* (2018), https://arxiv.org/abs/1811.02944.

## Exact restricted theorem A: one-bit global interface with coNP-complete uniform projection
Take an ordinary Boolean circuit H(y), and for each universal y let the projected outer-witness relation P_y={H(y)}. Every *fixed-y* CSP contains a single unary relation with a trivial join tree and a one-bit witness. Yet

`intersection_y P_y != empty iff H is a constant Boolean function`.

This succinct-input decision is **coNP-complete**. Nonconstancy has an NP certificate y,y' with distinct H outputs. Given any CNF F(u), form H_F(b,u)=b AND F(u). The value at b=0 is always zero; H_F is constant iff F is UNSAT, giving a uniform linear-size reduction from UNSAT. Equivalently the exact trace QBF `exists x forall y exists t [TRACE_H(y,t) AND x=output(t)]` is coNP-complete on this syntactic subfamily. This is the classical UNSAT reduction applied to a compiler interface, not a new complexity separation.

**Critical scope:** P_y is a succinctly indexed family. Explicitly materializing all P_y already has exponential size in |y|. The circuit evaluating H may have large gate-factor width, even though each conditioned unary relation has width one. This provides no unconditional lower bound for arbitrary source-readable SAT.

## Exact restricted theorem B: trace placement and global commitment
The following give the same Boolean answer for each H:
1. Sigma1 expanded: `exists x, (t_y for all y) AND_y [TRACE(y,t_y) AND x=output(t_y)]`.
2. Sigma2 succinct: `exists x forall y [x=H(y)]`.
3. Sigma3 exact: `exists x forall y exists t [TRACE(y,t) AND x=output(t)]`.
The Sigma1 expansion is generally exponential; equivalence of truth values is not a complexity reduction.

Early placement `exists x,t forall y [...]` is UNSOUND: H(y)=y0 AND NOT(y0) outputs zero identically, yet its internal NOT trace changes with y, so no fixed t works. Moving the global x after y (`forall y exists x,t [...]`) is also UNSOUND: x(y)=H(y) is a compact adaptive Skolem response and makes every total H true, including nonconstant H with false original QBF.

Separately challenged gate constraints with independently refreshed intermediate wires also fail: H(y0)=NOT(NOT(y0)) is nonconstant, but an independent local response can assign the internal NOT output differently in the output-gate challenge and make fixed x=0 appear valid.

## Executed finite audit
Primary Python standard-library seed 202611181148: **29,537 assertions, zero failures**. All 256 three-input truth functions; 240 small gate circuits with *every possible gate trace* exhaustively quantified; 800 random gate DAGs including 440 whose output functions are non-affine; 506 incorrect acceptances by separately refreshed gate traces on false-source random DAGs; 1,500 CNFs in the anchored H_F reduction (969 SAT/531 UNSAT); all 501 black-box one-spike controls for y widths 2 to 8; equivalent double-NOT encodings on every exhaustive and random circuit; 2/2 early-trace false negatives for constant DNF outputs and 254/254 illegal-late-x false positives for nonconstant truth functions.

Independent Python auditor with a different seed: **5,114 assertions, zero failures**, 256 truth functions, 1,200 independent CNF guards and 501 oracle spike pairs. Primary deterministic rerun yielded byte-identical output. No asymptotic lower bound is inferred from finite tests.

## Black-box oracle boundary
With H(0)=0 known and H available only through oracle queries, a deterministic exact constancy tester requires all 2^m-1 nonzero queries in the worst case: an all-zero oracle and an oracle with one spike at an unqueried address have identical transcripts. A compiler reading the circuit source need not obey this oracle-only lower bound. No relativizing conclusion about P versus NP follows.

## Triple time / space / RAM resource audit
The latest restricted PATHCUT-1 recurrence at its stated parameters is
`K' <= max(1.04,0.58,0.56+K/2), L' <= max(0.5,L/2)`.
Its time fixed point is **K=1.12**; strictly contracting ONLY for K>1.12. K=1.10 gives K'=1.11, an increase. The earlier AUTOENC recurrence `max(1.08,0.58+K/2)` has fixed point **1.16**.

For an explicit source expansion N=n^1.01, delayed A_3 and N^.04 additional guest decoding, the PATHCUT guest schedule costs exponent `1.01*(.56+1.5+.04)=2.121`, not the nominal 2.06. A **reached** full-parent A_3 call costs n^3.03. These refute those implementations' omitted-cost bounds, not all conceivable implementations.

R<=T for number of distinct RAM addresses is tautological. A six-operation trace [0,1,2,1,2^30,0] touches four distinct locations while reaching maximum work address 2^30. This is not a substitute for the FLMV machine's work-address space measure.

**Still OPEN:** Uniform source-to-guest and bit-index encoding, negative answers, quantified strategy and trace provenance, source-certified joins over all y, parent-scale obligations, simultaneous time/space model transfer, maximum live memory, and hereditary recursive closure. These are required before any unrestricted SAT time-space contradiction. No P!=NP proof is claimed.

## Reproducibility and handoff
Complete local bundle: `SIGMA_REDTEAM28_PACKAGE.zip` (REPORT.md, HANDOFF.md, README.txt, audit.py, independent.py, results.json, independent_results.json, SHA256SUMS.txt), ZIP SHA256 `736ce793adb1220177434ef56a6a0e44f29f57370057afe185efcece1e2a5286`; ZIP integrity and all seven file hashes checked. Primary script SHA256 `17276ec1ca1ee5e91c07ffe86066a51e5e55b90c3795a893abdf9b7561b8fb3f`; independent SHA256 `7f6f12c1f30df3a90afca06645dfc05aa4a53b346980054aa5a9234343439553`; raw results SHA256 `9adc81e68171a3e8eec4f85cd4e32d842b8fe4ca610e0787a7de0e7c5d6def2d`.

**Next mandatory tests:** H_F(b,u)=b AND F(u) even with singleton P_y; constant-output nonconstant internal traces; a NOT-NOT chain with separately challenged gate values; equivalent encodings and physical source-indexed serialization. Preserve one global x across every challenge, one consistent t(y) per challenge, true guest/decoder costs and hereditary closure. Restricted exact results stand; general contraction and P vs NP remain OPEN.

VERIFICATION_SENTINEL_SIGMA28_UNIFORM_PROJECTION_20261118_1202Z
