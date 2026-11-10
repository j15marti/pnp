# LSPV-2/532: native indexed high-water falsifies direct time-to-space inference

**November 9, 2026 17:16 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Node dependencies:** [P1-01], [P1-03], [P1-04], [P2-A1], [P2-A2], [P2-A3], [P2-L2-531], [P2-L1-549], [P2-L5-471]. All load-bearing arrows [P2-A2], [P2-D1], [P2-C3], [P2-B1] and [P2-B2] remain OPEN.

## IDEA, SEARCH, ITERATE and falsifiers

Candidate: on the **exact native indexed random-access tape model** of Fortnow, Lipton, van Melkebeek and Viglas (JACM 2005), a linear-time no-op wrapper can make the same deterministic program's measured work-space exponential, despite touching only one far-away work position. A proposed inference of a small upper space exponent from the time exponent alone is therefore unsound.

Falsifiers fixed in advance: (F1) moving a work head to a distant indexed address takes time linear in distance; (F2) the model charges only nonblank/touched work cells instead of the largest indexed position; (F3) the prefix changes SAT, UNSAT or malformed-input labels. Source inspection rejects F1 and F2; symbolic preservation and independent finite replay reject F3. **Successful hostile control:** sparse remapping can avoid retaining the far-address native high-water at the cost of a representation/machine transformation; this means the construction does not prove intrinsic language-space hardness.

Primary literature: FLMV, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6):835–865, 2005, Section 2.1 and Theorem 5.7/Corollary 5.8: https://lance.fortnow.com/papers/files/tst.pdf . The indexed read-only input and non-index work tapes each have index tapes; one jump is permitted to the binary-represented index, erasing the index tape. Work-space includes the **largest indexed/read position**, not simply nonblank tape cells. The authors explicitly note space may be exponential in time under this literal definition and show sparse tape representation can cap it, with polylogarithmic time overhead. Carlson, *On Reducing the Space Requirements of a Straight-Line Algorithm*, SIAM J. Comput., DOI 10.1137/0605042 provides pebbling tradeoffs for **declared DAG computations**, not a universal SAT space compressor. Williams, *Algorithms and Resource Requirements for Fundamental Problems*, 2007, https://eccc.weizmann.ac.il/static/books/Algorithms_and_Resource_Requirements_for_Fundamental_Problems/ provides a distinct later small-space bound.

**Repository actual-source search:** read new governing Nov 9 16:24 five-role handoff (blob 644b0d47), prior Nov 9 abstract-negative handoff (8a6fd9f5), BOTH root trackers (startup proof1 blob 96aefb3d; proof2 blob 1856f83b), issue #3, AGENTS.md, CODEX.md, project research SKILL, LSPV-1/549, LSPV-3/544, LSPV-5/471, LSPV-2/528, /530, /531, exact MODELBRIDGE-0010, Grok 2026-11-09_2015_PROGRESS and Claude TPORT-0001. Required repository deltas actually read: konard/p-vs-np scripts/proof_status.json blob 93b77ed3; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea; openai/math README.md blob cc5b0a03; MassimoLauria/cnfgen cnfgen/families/tseitin.py blob 4bb5fd19; berkeley-abc/abc README.md blob 88a9d1a3. None supplies universal SAT time-to-small-space compression. Existing prior work is adopted only within its model restrictions.

## Theorem 532.1: exact native high-water wrapper (PROVED/RESTRICTED)

Fix **any** uniform total deterministic decision machine A on all binary inputs in the exact FLMV indexed tape model. On an input x of binary length N, define J(A): write binary 1 followed by N zero bits onto a fresh index tape, issue one indexed jump of its associated blank work tape to position 2^N, read that blank cell, then execute A(x) and return A's original answer. This one fixed machine can be compiled from the supplied A. The prelude executes N+1 individual index writes and one jump and read.

$$
L(J(A))=L(A),\qquad
T_{J(A)}(N)=O(T_A(N)+N),\qquad
S_{J(A)}^{\mathrm{native}}(N)\ge 2^N.
$$

Proof: the index tape contains N+1 bits with numeric value 2^N; a native indexed reposition takes one step and charges the addressed position into the historical high-water. The subsequently executed A sees the identical original source, so its SAT/UNSAT/malformed policy is preserved. An additional fresh work/index tape is permitted in the declared model. The index tape itself uses O(N) cells and the far cell is read only once; there is no large live information object here. QED.

**Scope:** This is a theorem about the work-space **of this program**, not a lower bound on any equivalent SAT solver or on necessary live memory. In particular the original FLMV paper documents sparse re-encoding, with paid extra running time, that removes remote-position high-water. A direct generic claim that literal S(native) <= O(T) for every native implementation is false, while a different-machine simulation with O(T polylog T) type storage may hold. Neither proves S=O(N^1/2) when T=O(N^6/5), even conditionally on SAT in P.

## Cost-sound abstract machine semantics

Complete concrete state records the immutable entire binary input x, fixed machine code, deterministic versus nondeterministic mode, control state, all work tape contents, index tape strings and their heads, all work-head positions, output and parser status, elapsed time t, maximum ever indexed work address H, and the set D of touched/retained cells. Nondeterministic SAT verification adds an explicit existential branch-choice record and accepting-branch quantifier; a witness verifier does not decide UNSAT deterministically.

For a nonempty set X of concrete states with *identical authenticated full x and machine code*, let alpha(X) keep exact source/code and intervals for t, H, current index value v and |D|, plus a MAY set of control/output labels. Let gamma(a) be all exact states respecting these constraints. The abstract successor overapproximates every permitted concrete successor. The native indexed jump with index interval [v_low,v_high] must update

$$
[H'_{\rm low},H'_{\rm high}]
=
[\max(H_{\rm low},v_{\rm low}),
 \max(H_{\rm high},v_{\rm high})].
$$

This transition is exact when singleton intervals are used. Lower abstract cost must be <= concrete cost; upper resource envelopes must be >= **every** represented concrete use. Live dirty-cell count may fall after deletion, but native high-water cannot. Hashes only identify finite replay artifacts, not replace exact source authentication. Large abstract cardinality, a proof DAG, high address, or circuit graph alone cannot be charged as necessary live memory. A purported upper-space transformation must track all phases, source/index reads, preprocessing, child allocation, guest simulation, virtual inputs, failed search, cache, reference/recompute work, output and simultaneous ancestor/descendant storage.

## Finite verification (COMPUTATIONAL)

A strict finite signed 3-CNF byte format was used: S3C magic, one-byte variable/clause counts, then three signed, distinct literals per clause. A Python checker and **independently implemented Node checker** both tested 133 binary sources: 3 SAT, 2 UNSAT, 128 malformed. They agreed on 133 outputs, exact prelude overhead N+3, native space 2^N, an O(N) sparse-address prelude, and 13 byte-exact SHA-256 fingerprints. Controls include original even/odd K4 Tseitin 16-clause signed 3-CNFs (53 bytes each), contradictory eight-clause 3-CNF, SAT positive clause, empty clause-list SAT and malformed truncations. K4 source hashes are d9f553cb938cfff970199f7d3d7ddd88285b2187b2c4196961dce155d0558dd9 (SAT) and 548518bb8f1fb65311333255e14e26ec478c7f540a7405eb57d23c1b3d94756b (UNSAT). Prelude native high-water for either is 2^53=9007199254740992 **tape cell positions, not physically allocated bytes**.

Published independent checker: experiments/arc/lspv2_532_native_highwater_independent.cjs; raw ledger: results/raw/arc/2026-11-09_1716_LSPV2_532_NATIVE_HIGHWATER_RAW.json. The complete independent local Python program and its raw output are in the conversation reproducibility archive. Native machine full implementation and any polynomial-time SAT guest are NOT claimed.

## FLMV comparison and large N

Corollary 5.8's k=2 level is beta(c)=((c+2)/c^2-c)/2; beta(6/5)=23/45=1/2+1/90. The exponent-only factors (N^(23/45), N^(1/2), ratio N^(1/90)) are (1165.91, 1000, 1.1659) for N=10^6; (1.35936e6, 1e6, 1.3594) for 10^12; (1.84785e12, 1e12, 1.8478) for 10^24; (4.64159e30, 1e30, 4.6416) for 10^60. These are **not bytes, not measured space, and not finite-N theorem guarantees**. The k=2 expression is positive only below approximately c=1.52138; published higher k levels extend positive regions up to the golden ratio. Later small-space improvements have different hypotheses. A time upper gives neither exact S nor a sufficiently low upper S. SAT in P does not give c=6/5. A_NP existential acceptance does not establish a deterministic UNSAT decider or inherit a deterministic tradeoff.

## CORPUS REVIEWED / DUPLICATION, CONTRADICTION, MAIN

Previously known LSPV-5/471 demonstrates polynomial dead-space wrappers and a strict conditional exponent iteration; MODELBRIDGE-0010 rejects generic static normalizers, and LSPV-1/549 optimizes the published k-level FLMV envelope. This report adds the **model-specific exponential native high-water in linear time** with a concrete sparse-vs-native abstraction, not a new language lower bound or time-to-space transformation. No prior verified result is retired. Root MAIN stays OPEN, including [P1-01], [P1-03], [P1-04], [P2-A2], [P2-B1], [P2-B2], and no R_mix341 grammar or weight was changed.

**Precise next bridge (OPEN):** construct an all-input, recursively realizable SAME-MACHINE solver-intensional transformation A -> Phi(A) that actually establishes t' <= max(11/10,3/5+t/2) and s' <= max(1/2,s/2), charging both sparse remapping and every phase. The no-op wrapper does **not** exclude solver-specific optimizations. P versus NP remains OPEN.
