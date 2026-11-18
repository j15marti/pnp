# T5-BOUNDARY-PROMISE49 | 2026-11-17 17:25 PST

STATUS: Restricted exact NP-completeness theorem for **extracting a constant-size two-terminal T5 SAT-support relation**. Finite audit PASS. External mathematical review OPEN. P versus NP OPEN.

PRE-SEARCH INTEGRATIONS: (1) T5 boundary compression and fully charged resource contraction; (2) delayed terminal labels as potential WRAPPER nonrelativizing operation; (3) same-final-input witness lifting/projection; (4) one-hot Resolution clause transport. Proposals committed before targeted source search.

LATEST SOURCES READ: Resource TMR-2/071 exact two-palette adaptive read-once NROBP lower bound (source SAT trivial YES; earlier /070 girth correction); TMR-4/069-070 MDD compiler and triple obstruction falsifier (Library); Nonrelativizing Clock Gate CLOCKWITNESSPH23 latest conditional joint PH verifier to inverse (historical TRACEAUDIT23); Universal Obstruction DIAGONALLIST34 and T5-TOGGLE-CERT48 same-input controls; Proof Transport SEMDEG-FIREWALL1 and PC22-ORCLOSURE38 restricted calculus-specific transport. Targeted GitHub recent commits, project chats, Google Drive, Library and primary literature (Bang-Jensen/Hell/MacGillivray 1988; Razgon NROBPs; Cook-Reckhow 1979) reviewed.

EXACT CONSTRUCTION: Let G=(V,E), n>=1, with c weak connected components and representatives r_1,...,r_c. Preserve G entirely; add two terminal vertices a,b, an all-forward private four-edge path a -> r_i for every component i, and a private four-edge path b -> r_1. Each path uses three new internal vertices. Thus H(G) is connected with n+2+3(c+1) vertices and |E|+4(c+1) arcs, and is constructed with polynomial source scanning/serialization overhead. T5 relation R(x,y) means (y-x) mod 5 in {1,3}. Four-edge transfer A^4 has first row (4,4,1,6,1), so EVERY fixed endpoint-color pair extends along each path.

THEOREM: For the 5x5 Boolean terminal-support table S_H(alpha,beta), S_H(G)=J_5 (all ones) iff G is SAT, and S_H(G)=0_5 iff G is UNSAT. Any coloring of H restricts to G; if G has witness g, independently extend each four-edge path for every fixed alpha,beta. Therefore computing one fixed support entry and deciding if the entire table is full are NP-complete even on the connected, promised all-or-nothing image. Emptiness is coNP-complete. The table is a constant 25-bit representation, but recognizing which table applies is as hard as unrestricted T5-SAT. This does NOT prove superpolynomial runtime or P != NP.

EXACT COUNT: For fixed alpha,beta the number of H extensions equals sum over g in Sol(G) of [product_i A^4(alpha,g(r_i))] times A^4(beta,g(r_1)). Counting needs its own charged algorithm.

HOSTILE CONTROLS: Replacing four-edge paths by one-edge paths breaks full support (G one isolated vertex; alpha=0,beta=1). Delayed terminal colors do not change SAT status and are not a nonrelativizing hinge. Every SAT H witness projects to a SAT G witness, and conversely any SAT G witness lifts to every terminal pair with charged path extension. Under one-hot CNF, G's original clauses are a subset of H's, so any Resolution refutation of G replays verbatim on H; the reverse proof-system transfer and any arbitrary-decider-to-proof map remain OPEN. No uncharged table discovery or recursive access is assumed.

AUDIT: Executed stdlib Python independent transfer-matrix-vs-literal path check; 187 source graphs, 81 SAT and 106 UNSAT; 25 table entries per graph; 125 independent direct whole-graph DFS endpoint counts; short-path, opposite arc, loop and disconnected controls. 5,582 final assertions, ZERO failures. An initial DFS harness self-loop omission was found by adversarial testing, fixed, and the entire final suite rerun. Script SHA256 0112f1ca99879e5a8cd8ee50e8502d09bba71c85186e233c280a3c5d58ca4d92; results SHA256 93f1875e79186454c93c471c7e0e88a5c7d216f6bec952c812ce1938114b35fa. Local full report and executable bundle generated and ZIP-verified.

DAG: ESTABLISHED T5 fixed-template CSP NP-completeness. PROVED H(G) two-terminal all-or-none exact support, connectedness, size ledger, NP/coNP classifications, one-way trivial Resolution inclusion. FALSIFIED uncharged inference small semantic support -> cheap extraction. IMPORTED restricted TMR-2/071 representation lower bound. OPEN: arbitrary all-input resource contraction, correctness-forced WRAPPER hinge, same-input UWI over all eligible programs, general decider-to-hard-proof transport, P vs NP.

NEXT FOUR TASKS:
RESOURCE: source-accounted graph boundary extractor with discovery, caching, recursion and output, adversarially checked on mixed T5 sources and source-aware shortcuts.
NONREL: construct a SAT-status-changing delayed source operation not equivalent to a post-release port-color query, with precomputation/direct-oracle controls.
UNIVERSAL: fix exactly one final satisfiable H, common clock and eligible portfolio; test projection/lifting and quantifier swaps.
PROOF: investigate reverse H-refutation -> G-refutation for specified T5 one-hot calculus with step/width accounting, not only forward axiom inclusion.

HIGHEST-VALUE OPEN ARROW: Uniform cheap, fully charged semantic-boundary extraction beyond supplied bounded-width decompositions; arbitrary two-port extraction already embeds NP-complete SAT, so a low-width output is no evidence of efficient discovery.

Previous run: https://github.com/j15marti/pnp/blob/main/research/agents/cross-track/2026-11-17_1624_T5_TOGGLE_CERT48_STATUS.md
References: https://doi.org/10.1137/0401029 ; https://arxiv.org/abs/1411.0264 ; https://doi.org/10.2307/2273702

END_T5_BOUNDARY_PROMISE49.