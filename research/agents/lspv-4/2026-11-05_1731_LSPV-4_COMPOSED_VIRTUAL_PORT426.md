# LSPV-4/426: Source-authenticated nested virtual CNF ports

**November 5, 2026, 17:31 PST. Route A. PROVED/RESTRICTED conditional composition lemma; COMPUTATIONAL finite controls; all-input FLMV contraction OPEN; P versus NP OPEN.**

## IDEA, four falsifiers, SEARCH, ITERATE

**Hypothesis before search:** Even though obtaining a cheap virtual child bit is not automatic, the composition of O(log log N) already certified locally addressable child-bit generators with polylogarithmic parent-query fanout is inexpensive in both indexed-machine time and all-phase peak space. Falsifiers: (F1) a polynomial number of root probes arises from O(log log N) such levels, (F2) the source/index/head stack exceeds N^1/2 even with no caching, (F3) source-authenticated nested renumbering changes SAT labels or smuggles branch-local hypotheses, (F4) a small child descriptor is confused with cheap bit acquisition.

F1 and F2 are ruled out **under explicit generator assumptions**, F3 passes finite source-disjoint Tseitin controls, and F4 is a real counterexample to an *unconditional* interpretation, already supplied by LSPV-2/429's opaque checkpoint query adversary. No all-input generator is derived.

## Theorem: charged composition

Fix one uniform fixed-tape indexed random-access machine; immutable root encoding X0 of N bits; and a chain X0,...,XD with D <= C log_2 log_2 N. Each already proved correct, source-authenticated local child-bit port Gi computes any bit of Xi+1 by <= b(N)=K(1+log_2 N)^r bit queries to Xi, <= b other *native* operations including source/index/head reads, address writing/erasure, arithmetic, output and context access, and <= b live scratch/descriptor bits. Dependencies are acyclic and contexts are faithfully retained. No SAT oracle, hidden child materialization or unverified intermediate lemma is permitted.

Sequentially recomputing parent bits on demand yields

$$
Q_i \le b^i,\qquad T_i = O(b^{i+1}),\qquad S_i=O(ib).
$$

**Proof.** Q0=1, Qi<=b Q(i-1). Ti<=b T(i-1)+b, giving O(b^(i+1)). A depth-first schedule retains only one frame of <=b bits per active ancestor, so S<=ib. The fixed-tape implementation includes address-index erasure on indexed jumps and logarithmic source addressing in b. For D=O(log log N), log(TD)=O((log log N)^2)=o(log N), and SD is polylogarithmic. Simulating a guest input read with this port charges the guest's original address/index operation as well as every virtual-port operation, while preserving guest work/index state and adding only polylog scratch. This proves *composition* of effective ports, not their existence for arbitrary CNF inputs. QED.

A port requiring polynomially many opaque successor probes (LSPV-2/429) violates the hypothesis. Depth Omega(log N) can also cause superpolynomial port costs. Neither case is covered.

## Existing certified hard family and finite tests

Odd-charge Tseitin on a connected cubic expander: 3h/2 edge variables; four proper signed 3-clauses per vertex, totaling 4h clauses and N=Theta(h log h) binary encoded bits. Urquhart (JACM 1987) and Ben-Sasson–Wigderson (JACM 2001) establish 2^Omega(h) ordinary shared-DAG Resolution lower bounds on suitable expanding graph families, **not** SAT-machine lower bounds. The previously authenticated fixed mixed Rmix341 AND3/GF(2) shortcut has 4h-1 paid logical nodes on specified bridgeless odd-charge cubic sources. In a disjoint product with all other components SAT, the ordinary Resolution bound of one hard component survives restriction of other variables, but not transfer to all mixed rules.

Our finite host-language exact bit-port tests use genuine K4 and cube parity CNFs, not certified asymptotically hard expanders. There are B=4 or 16 disjoint components, SAT controls with all even charges and UNSAT controls with exactly one odd charge. A bit-level source port selects contiguous groups, reencodes each smaller CNF with locally renumbered variable identifiers and source-authenticates every expected byte. Nesting terminates at individual components. The actual code uses a bounded fixed 88-bit header only for finite experiments; it is *not* claimed to be an all-size FLMV encoding.

| Source | Root bits | First-level child bits | Levels |
|---|---:|---:|---:|
| K4 x 4 | 1240 | 568 | 2 |
| K4 x 16 | 6232 | 1240 | 3 |
| Cube x 4 | 2776 | 1240 | 2 |
| Cube x 16 | 13912 | 2776 | 3 |

Both SAT and UNSAT versions pass. Expanded Python producer: **6109 checks**, 8 raw rows, **2598508** source-bit reads across all probes and a maximum 168-bit host-level live-address proxy. Independently implemented JS reviewer: **638 checks**, rebuilding complete original clauses and source SHA-256, verifying each recursive group and exhausting K4/cube block assignments. One initial independent reviewer assumption that a SAT middle block must have odd charge failed; the verifier was corrected to use the declared source charges. The tests include malformed and one-bit-corrupt source controls. These are host proxy counts, NOT physical FLMV-machine timings.

## Search and source checks

Read project five-role handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (blob c3889a3e), issue #3, AGENTS.md 19656af1, CODEX.md 754999f5, pnp-research skill b8df83a7, LSPV-2/429 7a1be16, LSPV-2/430 7e9045f, LSPV-4/424 and /425, actual GROKPROOF/2026-11-05_1913_PROGRESS.md 8a004bf4 and Claude research/agents/claude/tport/README.md d1290822. LSPV-4/424 already established the one-level conditional simulator, so that result is not claimed as new. Current LSPV-2/430 is a bit-oracle extensionality lemma, not a solver-dependent contraction.

Primary literature: Fortnow, Lipton, van Melkebeek, Viglas, JACM 52 (2005) 835-865, DOI 10.1145/1101821.1101822, actual PDF https://lance.fortnow.com/papers/files/tst.pdf, section 2.1 indexed machine and section 3 locally computed SAT reduction bits, with visual inspection of page 4. Explicitly searched indexed web for FLMV SAT indexed machine and bit-local reductions. Direct Google-branded search was unavailable. Actual GitHub files read: konard/p-vs-np README.md (0e0ec77), SOLUTION_STRATEGIES.md (62f5955); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693e), PROOF_PORTFOLIO_BRIDGE_REPORT.md (22215ce); openai/math lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (1ced21f); meelgroup/frat-xor format.md (986a21a). None asserts the missing universal recursive contractor.

## Physical ledger, qualification, next gap

Distinct logical inference DAG nodes, critical-path span, proof-selection cost and actual scheduled machine time/space remain separate. The conditional simulation pays guest input-index writes, source-index reads/erasure, recursive address frames, arithmetic, re-reads/recomputation and output. The experiment's proxy omits a physical-machine implementation of full source parsing and compiler-policy search; these remain separate all-phase rho costs. Caching a port answer requires additional physical peak space. For materialized children retain the established bound s'<=max(rho,eta,lambda,lambda*s).

**OPEN:** find effective, source-authenticated, label-preserving, AND/OR-complete, malformed-aware child generators for *all* CNF inputs of arbitrary uniform correct polynomial SAT deciders, with worst-case local time <=N^(11/10+o(1)), child number <=N^(3/5+o(1)), child length <=N^(1/2+o(1)), all-phase peak <=N^(1/2+o(1)), recursively on the SAME indexed machine. In particular prove the cheap input-bit port assumption, not just a compact descriptor. Route B B1/B2/B3 remains separate and OPEN; P versus NP OPEN.

Root main.tex SHA 593000bb was returned with zero readable characters via authenticated fetch, so no unsafe overwrite. No task/schedule/status/rule/weight was changed. Expanded producer and exact raw records are preserved in the local reproducibility archive.