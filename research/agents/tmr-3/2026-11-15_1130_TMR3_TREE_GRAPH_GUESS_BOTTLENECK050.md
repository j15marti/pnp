# TMR-3/050: Graph-Guess Retention Barrier for Sub-Square-Root Tree Evaluation

**2026-11-15 11:30 PST | TMR-3 / PNP Time-Space Tradeoffs | Track B | PROVED/RESTRICTED protocol lemma (peer review OPEN), COMPUTATIONAL finite checks | P versus NP OPEN.**

## 1. Candidate and falsifiers

**Candidate.** Merely replacing Cook–Mertz Tree Evaluation by a hypothetical constant-arity evaluator using \(\widetilde O(b+h^\alpha)\) space for \(\alpha<1\) cannot break square-root space **within the existing Williams full-graph-materialization protocol**, because separately charged graph guesses and full tree-node addresses can still require \(\Theta(h)\) writable bits.

Falsifiers: (F1) compute the correct graph lazily from original source, invalidating any representation-independent \(\Omega(h)\) claim; (F2) stream tree addresses instead of materializing length-\(h\) paths; (F3) reuse memory, hence do not sum two lower bounds unless their live storage is proved disjoint; (F4) an evaluator may take exponential time, so space-only bounds cannot enter simultaneous time-space exclusions.

This is a precise **implementation** barrier, not a lower bound on all simulators or SAT algorithms.

## 2. Source-verified baseline and duplication

Williams, *Simulating Time With Square-Root Space* (2025), Section 3.2 pp. 10–13, reduces a time-\(T\), fixed-number-of-tapes computation to an implicitly defined constant-arity tree of height \(B=\Theta(T/b)\). Each of \(pB\) block-boundary head-motion symbols is in \(\{-1,0,+1\}\). The proof explicitly enumerates putative computation graphs \(G'\), retains the \(O(B)\)-bit candidate during evaluation, and uses \(O(B)\) space to identify nodes and their paths. Each local block function costs \(O(b)\) time and space. Theorem 2.2 restates Cook–Mertz's space bound \(O(db+h\log(db))\). Williams derives \(O(b+(T/b)\log b)\). **Section 3.3 already states that even LOGSPACE Tree Evaluation would leave \(O(b+T/b)\) in this graph-guessing reduction.** The present note makes this protocol distinction explicit, gives an exact integer floor and a compact-input hostile control. It does not claim independent novelty for Williams's observation.

Primary source: https://arxiv.org/pdf/2502.17779 (arXiv v1); Cook–Mertz, STOC 2024, https://doi.org/10.1145/3618260.3649664 .

Project originals checked: 2026-11-15 compression directive (SHA 7b8804dc...), current TMR-1..5 handoffs, TMR-3/049, the direct-request Allender draft PR #140, TMR-3/023's compact OR extension, LSPV-4 SOURCELDEGATE2's exponential tree unfolding and LSPV-5 adaptive-RAM firewall. Root proof1 fully retrieved (SHA 06f7ebc8...); proof2 (930c5eedd...) and main.tex (6ac34c5dc...) returned SHAs but empty bodies through the connector. AGENTS.md, CODEX.md, repository research skill, issue #3 reviewed. Full repository checkout/preflight unavailable. No shared root edits.

## 3. Exact protocol theorem

**EGA-B (explicit-graph/address/block) protocol.** Fix constant \(p\ge1\). A sequential finite-alphabet machine groups \(T\) source steps into \(B=\lceil T/b\rceil\) blocks, \(1\le b\le T\). It must (i) materialize one **complete candidate** of \(pB\) ternary head-motion symbols in counted writable cells while invoking its implicit evaluator and (ii) materialize one complete \(b\)-bit block-value register in counted writable cells at some stage. Storage may be reused. Count the maximum distinct writable bits/cells of the single execution, including graph choice and buffers; original input is immutable read-only.

**Theorem A (restricted).** Every EGA-B execution has
\[
S_{\rm EGA}(T,b)\ge \max\{b,\lceil T/b\rceil\}
\]
in the binary-cell convention. Consequently
\[
\boxed{\min_{1\le b\le T}\max\{b,\lceil T/b\rceil\}=\lceil\sqrt T\rceil.}
\]
Changing Tree Evaluation alone does not remove this protocol bound.

**Proof.** The block register occupies \(b\) cells. The candidate domain has \(3^{pB}\) distinct syntactic words, requiring a fixed-length injective binary representation of at least \(\lceil pB\log_2 3\rceil\ge B\) cells; the declared protocol requires the complete word. Reuse implies a **maximum**, not a sum: \(S\ge\max(b,B)\). Since \(b\lceil T/b\rceil\ge T\), its maximum squared is at least \(T\), and the integer maximum is at least \(\lceil\sqrt T\rceil\). Choosing \(b=\lceil\sqrt T\rceil\) gives \(\lceil T/b\rceil\le b\), meeting the minimum of the two-register resource expression. This does not assert the complete Williams simulation reaches this bound without logarithms. QED.

**Theorem B (separate full-path interface).** An API that must simultaneously emit a complete fixed-length injective identifier for any of the \(d^B\) leaves of a complete \(d\)-ary height-\(B\) tree (\(d\ge2\)) requires at least \(\lceil B\log_2d\rceil\) writable output bits for some leaf, by pigeonhole counting. This does not cover streamed addresses, read-only head positions, compressed shared DAGs, or all Williams implicit trees.

**Smallest falsifier to universal extrapolation.** For \(B=1\), full ternary graph-choice encoding already needs two binary bits. For arbitrary \(B\), a fixed machine can follow \(2^B\) different valid right/stay block-head schedules specified by \(B\) read-only input directives; the correct schedule can then be generated **from that input** without retaining \(B\) writable bits. Hence the large number of possible head histories is not intrinsic memory hardness. The result concerns the full-guess materialization contract.

## 4. Combined exponent budget

Let a hypothetical evaluator use \(\widetilde O(b+B^\alpha)\) writable space; let true graph generation, address generation and other charges use respectively \(\widetilde O(b+B^\beta)\), \(\widetilde O(b+B^\zeta)\), and \(\widetilde O(b+B^\omega)\). Only after proving all these simultaneous upper bounds may one write
\[
S_{\rm sim}=\widetilde O(b+(T/b)^\mu),\qquad
\mu=\max\{\alpha,\beta,\zeta,\omega\}.
\]
The optimum exponent for this **upper-bound template** is \(\rho=\mu/(1+\mu)\), taking \(b=T^\rho\). It is not an algorithm by itself.

For full-graph EGA-B, \(\beta=1\), and Theorem A blocks sub-square-root space regardless of \(\alpha<1\). The cube-root target \(\rho=1/3\) requires \(\alpha,\beta,\zeta,\omega\le1/2\), so graph generation and path addressing need a new interface **in addition** to an improved evaluator.

Example: \(T=2^{18}=262144\), \(b=64\), \(B=4096\). A miraculous \(b+\sqrt B=128\)-cell evaluator still encounters a full graph-description obligation of at least 4096 cells. The existing protocol's optimal two-register floor is 512 at \(b=B=512\), before logs.

## 5. Same-realization time, work, and space ledger

| Resource | Exact charge / restriction |
|---|---|
| Graph choice | \(pB\) ternary labels, counted writable storage, reusable |
| Candidate alternatives | At most \(3^{pB}\); **not** a proof each input tries all |
| Node addressing | Source uses \(O(B)\) generator space; full-path lower bound is separate/restricted |
| Local block evaluation | Williams gives \(O(b)\) space/time per call; EGA-B requires a physical \(b\)-bit register |
| Input and control | Source rereads, head indices, counters, buffers, output and failed guesses charged |
| Tree Evaluation | Hypothetical space improvement; actual sequential time unspecified, possibly exponential |
| Entire simulation | Work across every call and guess, **not** parallel span |
| Peak storage | Count-once distinct writable cells; never add independent maxima |

Williams proves a space simulation, not a polynomial-time simulation with the same time-space pair. Neither implicit-tree size nor the \(3^{pB}\) candidate count is an unconditional runtime lower bound against SAT.

## 6. Mandatory four gates

| Gate | Status |
|---|---|
| DISJ sanity | **PASS**. No rank-based bound. Easy DISJ, Horn, affine, 2-SAT, compact-algebra shortcuts are allowed outside EGA-B. |
| Relativization | **NOT APPLICABLE TO SEPARATION**. Counting/explicit-buffer lemma relativizes, but no separation. Nonrelativizing step OPEN; algebrization/Natural Proofs not invoked. |
| Simultaneous DTISP | **OPEN**. Storage is matched to one physical protocol; compatible polynomial sequential time and an SAT compiler absent. |
| Configuration counting | **PASS as consistency only**. Deterministic complete configurations give runtime **upper** bound \(2^{O(S+\log N)}\), not a lower bound. |

## 7. Finite audit and next target

Standalone Python source: experiments/tmr/tmr3_graphguess_address050.py; separate raw JSON: results/raw/tmr/2026-11-15_1130_TMR3_GRAPHGUESS050_PY_RAW.json. Standard library, exact integers, no random seed. Executed twice in approximately one second each; byte-identical output. **722,196 assertions, zero failures**, covering \(1\le T\le1200\), \(1\le b\le T\), ternary address capacities through \(B=17\), explicit binary move histories through \(B=10\), read-only streaming controls, and four cube-root parameter examples. Finite checks are COMPUTATIONAL. No native Williams machine or improved evaluator constructed.

**Next lemma:** design a uniform lazy graph/path interface for all adaptive work-tape histories with counted graph/address space \(\widetilde O(b+B^{1/2})\), exact source authenticity and charged sequential generator time, or falsify it on an adaptive schedule. This must be coupled to a genuinely improved Tree Evaluation algorithm.

**TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.** Root main/proof2 complete contents unavailable through connector, no shared writes. All five schedules unchanged. /341 full logical authority FAIL, /386 RESTRICTED. P versus NP OPEN.
