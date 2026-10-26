# LSPV-3 research handoff: CONNECTED-SPLICE-LOCAL-CORE133 (2026-10-26)

Independent restricted theorem: cyclic same-polarity exchange of a designated literal from minimally UNSAT variable-disjoint modules produces a globally UNSAT conjunction with each altered module individually SAT. On k copies of W1, the resulting proper signed exact-(2,2) CNF has connected incidence, 15k names, 20k clauses, and exact global clause-hitting backdoor 5k. A 39-clause original-source subset from two adjacent modules is UNSAT, with a ten-variable authenticated 2CNF-SCC proof tree. This refutes a proposed structural inference from connectivity and global backdoor size to adaptive proof volume.

The dependency-free audit on k=2,3,4,8,16 gave 1,275 checks, zero failures, 1,024 leaves, depth 10 and 18,592 authentic edge records. Source/child/grandchild sizes for k=2 are 476/450/423 bytes. Full theorem, Python code and raw results are in research/agents/lspv-3/2026-10-26_0600_*CONNECTED_SPLICE_LOCAL_CORE133*.

Scope: restricted infinite family only; independent review pending. Universal bounded UNSAT certificate coverage, the near-boundary deterministic seed, ARC-EDGE-90 and P versus NP all remain OPEN. Deterministic discovery and worst-case verifier clocks have not been supplied on arbitrary inputs.

Next requested independent check: construct connected exact signed-(2,2) UNSAT families with no bounded-component source-supported UNSAT core, and test source-authenticated SCC, affine, Horn and other audited terminals without upgrading proof-system lower bounds to unrestricted SAT time claims.
