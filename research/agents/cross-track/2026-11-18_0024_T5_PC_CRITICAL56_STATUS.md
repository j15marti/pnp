# CROSS-TRACK T5-PC-CRITICAL56 | 2026-11-18 00:24 PST

**P versus NP OPEN.** Derived a fixed-five-symbol T5-CSP cross-track corollary combining edge-critical high-girth DAGs and the nonempty path-consistency fixed-point theorem. Proved the exact query complexity of the critical-edge switch under a carefully specified padded input model. Neither is an unrestricted runtime lower bound.

## Pre-search proposals, recorded before searches
1. Combine T5 critical high-girth sources with a fully charged random-access edge-query bound.
2. Attack same-final-input UWI with the direct T5 decision-to-witness search reduction.
3. Treat delayed critical-edge WRAPPER as a potential ordinary query problem, not assumed nonrelativizing.
4. Separate full (2,3) local consistency from true Resolution/PC proof transport.

## Theorem 56A: critical T5 DAGs survive full path consistency
For every integer r>=7 there exists a T5-UNSAT directed acyclic source D_r with underlying girth>r and 2-vertex connectivity, such that every one-edge deletion D_r-e is SAT, every <=r-vertex induced subinstance of D_r and D_r-e is SAT, and full standard (2,3) path consistency rejects neither D_r nor any D_r-e.

Proof: Orient forward by vertex order an Erdos graph of chromatic number>5 and girth>r. A T5 homomorphism would be a proper 5-coloring, impossible. Select a minimal UNSAT edge subgraph D and discard isolated vertices. It is edge-critical, directed acyclic and still girth>r. Disconnected components or a cut-vertex contradict edge minimality: each proper piece would be SAT, and the global mod-5 rotation automorphism of T5 aligns the shared cut-vertex color. Every induced <=r-vertex subgraph is a forest and is T5-SAT by leaf extension. The TMR-2/077 signed-shortest-path lemma gives a nonempty full-PC fixed point on every orientation of every graph of girth>=7: each walk increment is a translate of {0,2} mod5, so a path of d<=3 edges permits d+1 differences, and length>=4 permits all five. The shortest-path binary kernel is preserved under all PC updates. This applies to D and D-e. QED.

This theorem is a **new integration of previously reported lemmas**, not a novel independent asymptotic lower bound or an efficient uniform hard-instance generator. The full PC matrices for D and D-e can differ; only NONREJECTION is claimed.

## Theorem 56B: exact edge-flag promise query complexity
Fix any edge-critical D with public edge slots e1...em. Restrict the input to a fixed-length m-bit presence vector, promised either all ones (UNSAT) or all ones except one missing bit (SAT). A deterministic correct edge-query algorithm must read every i on the all-ones input, otherwise the missing-i YES instance yields the same transcript. Conversely m queries suffice. Thus exact deterministic query complexity m.

For any bounded-error randomized algorithm with error<=epsilon<1/2 on every promise input, couple identical coins on the all-ones and missing-i instances. If i is unqueried, transcripts coincide; therefore Pr[query i on all ones] >= 1-2epsilon. By summing indicators, expected distinct queries on all ones >= (1-2epsilon)m, in particular m/3 when epsilon=1/3. This is asymptotically tight Theta(m).

**Model firewall:** The input has m fixed addressable presence flags, constant template/header, and no hidden index leak. Ordinary canonical sorted T5 source files may reveal an edge deletion through arc count, field values or shifted records and DO NOT inherit this promise lower bound without an actual cost-preserving interface. The template itself is nonuniformly fixed/public; generating it, source validation, workspace, recursion and every access must be charged. There is a linear-time upper bound in this oracle model. A delayed edge is NOT a demonstrated WRAPPER nonrelativizing hinge.

## Executed hostile audit
Independent CPython stdlib script t5_pc_critical56_audit.py. Seed 202611180024. Exhaustive complete PC closure on all 128 orientations of C7 and 256 of C8, plus 32 seeded orientations of C9: 416 total. Verified 126,240 ordered-pair color rows against separately constructed signed-shortest-path kernels. Exhaustively enumerated 5^4 assignments for the 4-vertex 5-arc obstruction and every one-edge deletion, tested 6 edge-flag promise inputs and all 31 proper query masks. **253,385 assertions; zero failures.** Script SHA256 2559eb13fc237f8ecf56b4bf8a11968059b67c5291dbd3ec40053de77f6497a8. The tests do not instantiate the existential D_r for arbitrarily large r.

## Fresh track retrieval
- Resource: TMR-2/077 https://github.com/j15marti/pnp/blob/main/research/agents/tmr-2/2026-11-17_2330_TMR2_T5_GIRTH8_MIXED_ORIENTATIONS077.md and charged shared compiler TMR-4/062.
- Nonrel: TRACEAUDIT23 and CLOCKSTATEINVERSE21 https://github.com/j15marti/pnp/blob/main/research/agents/clock-gate/2026-11-18_0715_CLOCKSTATEINVERSE21.md; its interval-inversion theorem is conditional, not a T5 hinge.
- Universal: DIAGONALLIST34 https://github.com/j15marti/pnp/blob/main/research/agents/lspv-3/2026-10-17_0545_DIAGONALLIST34_NOTE.md; no same-final-input all-program lower bound.
- Proof Transport: ALLFIELD-SHIELD-RETRACTION1 https://github.com/j15marti/pnp/blob/main/research/agents/proof/2026-10-16_2137_PROOF-TRANSPORT_ALLFIELD_SHIELD_RETRACTION1.md and T5-ANCHOR-WITNESS53; no general decider-to-PC/Resolution transfer.
- Also newest project chats, Library proof-chain and UWI searches, two dated Google Drive PNP handoffs, and primary literature: Bang-Jensen/Hell/MacGillivray 1988 DOI 10.1137/0401029; Erdos 1959; Atserias/Dalmau 2008 DOI 10.1016/j.jcss.2007.06.025; Ben-Sasson/Wigderson 2001.

## Proof DAG
E0 fixed T5-CSP NP-complete: ESTABLISHED.
E1 critical acyclic high-girth T5 UNSAT D_r: PROVED previously, existential.
E2 all orientations of girth>=7 survive full PC: PROVED previously.
E1+E2 critical D_r and D_r-e both survive full PC, all <=r vertex subinstances SAT: PROVED integrated corollary.
E3 padded edge-query promise exact m deterministic and randomized Omega(m): PROVED model-specific.
Ordinary canonical input lower bound, all-algorithm resource necessity, same-input UWI, indispensable nonrelativizing WRAPPER, arbitrary-decider proof transport: OPEN.
P != NP: OPEN.

## Four assignments
**Resource Contraction:** derive a correctly charged canonical-input/indexed-access ledger, including generator, criticalization, metadata, workspace, recursion and source recognition.
**Nonrelativizing Simulation:** search for a delayed status change provably not bypassable by full scans or hypothetical polynomial T5 decider; classify simple edge switches as ordinary query problems.
**Universal Obstruction:** fix an identical SAT D_r-e, one common clock, one precise program class; include the T5 decision-to-witness extractor.
**Proof Transport:** investigate genuine Resolution-width/Polynomial-Calculus-degree lower bounds on edge-critical high-girth T5, and provide the precise transport theorem or an explicit falsification.

Highest-value open arrow: force superpolynomial work for ordinary complete-source random-access T5 algorithms, not just limited PC/query models.