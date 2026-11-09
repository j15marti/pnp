# LSPV-2/523: source-authenticated budget abstraction and the RUP macro/micro barrier

**November 9, 2026, 10:12 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

Affected tracker node [P2-L2-523] refines still-open [P2-A2], [P2-A4], [P2-A5]. This is NOT the historical R_mix341 calculus. The source partition lower-bound invariant is reused from LSPV-3/536, not claimed as a novel general lower bound.

## IDEA, falsifiers, and exact separate calculi

Candidate: a budgeted negative-proof abstraction that treats one RUP record as one paid binary Resolution node excludes a genuine legal shortcut, and thus violates cost-sound overapproximation. Falsifiers: (1) a shared Resolution refutation uses fewer than n nodes; (2) an original Horn-chain clause is dispensable; (3) the RUP checker rejects the empty clause; (4) the one-merge abstract transformer drops a legal Resolution transition. Mathematical proof plus two independent implementations reject (1)-(4) in the declared model.

For n>=1 define the Horn chain

$$
H_n=(x_1)\land\bigwedge_{i=1}^{n-1}(\neg x_i\lor x_{i+1})\land(\neg x_n).
$$

It has m=n+1 source clauses and a canonical indexed signed width-1..3 ASCII encoding of N=Theta(n log(n+2)) bits. MICRO-RES is a separate experimental calculus with free original premises, explicitly oriented two-parent Resolution nodes of cost one, a full shared/reconvergent proof DAG, global reuse paid once, source IDs/hashes and no unproved case discharge or free learning. Branch/UP/CDCL search operations cannot assert a globally learned clause without a legal paid Resolution derivation. MACRO-RUP is a DISTINCT sound proof-record system where a RUP empty-clause addition is charged one record and accepted only if unit propagation on the original source yields conflict. Its checker still costs time, memory, source reads and verification. Neither system changes historical R_mix341.

## PROVED/RESTRICTED exact theorem and may-simulation

$$
W_{\mathrm{MICRO}}(H_n)=n,\qquad W_{\mathrm{MACRO}}(H_n)\le 1.
$$

Every source clause is indispensable: removing the positive unit admits all false; removing the negative unit admits all true; deleting implication i admits x_j=1 for j<=i and x_j=0 otherwise. Every sound refutation must therefore depend on all m source leaves. If its undirected ancestor DAG has q binary paid nodes, connectivity gives at most 2q parent edges among m+q vertices, so 2q>=m+q-1 and q>=m-1=n. The n consecutive oriented resolutions of x1 through the implications and the final negative unit attain n. Sharing cannot invalidate this counting argument.

An abstract MICRO state retains its source-dependency-component partition and global paid count q. Initially there are m singleton components. A concrete two-parent inference connects at most two components; abstractly allowing any such merge at cost 1 is a sound may overapproximation. A global contradiction must contain every indispensable source, hence its partition has one component. The invariant

$$
\kappa+q\ge m
$$

proves abstract goal nonreachability at every budget B<n without running a proof-search heuristic. It is a cost-sound restricted negative certificate. Branch scheduling and lemma references stutter, but globally reused learned conclusions require paid source-authenticated derivations.

A coarse one-cost LEARN_EMPTY abstract goal is **spurious for MICRO** when n>1: exact MICRO replay rejects the absent legal one-node Resolution derivation. CEGAR repairs the rule tag and paid provenance. In contrast, one RUP_ADD(empty) is **genuine in MACRO**, since original-source unit propagation reaches conflict; it cannot be refined away. A purported one-cost projection of MACRO-RUP into the MICRO one-merge abstraction would exclude this genuine budget-one goal for n>1, so is unsound. This is a parameterized *cost-model transfer obstruction*, not a general SAT computational lower bound.

## Source-authenticated controls and accounting

Python: 357 grouped assertions; independently implemented Node.js: 262. Both replayed n=1..16, all source-deletion satisfying witnesses, 16 original signed K4 3-CNF Tseitin charge patterns, and 32 matching original-source SHA-256 values. Both rejected seven malformed sources and seven corrupted proof variants. At n=16, 103 source bytes, 17 source clauses, 16 MICRO nodes, 1 MACRO addition record, 17 RUP source-clause scans and 16 UP assignments. The full independent scripts, raw data and expanded mathematical report are included in the separately delivered reproducibility archive. This is no native FLMV timing/peak-space result.

Explicit MICRO certificate descriptions need Theta(n log n) bits in this indexed trace. One MACRO proof record is O(1) payload apart from source binding; its tested checker parses the whole source and does n+1 clause reads and n assignments. Acquisition, parsing, source/index reads, construction, failed branches, validation, caches, references, output and simultaneous writable space must be charged for *actual* solver time/space. The source-dependency invariant only counts paid MICRO inference nodes. It does not bound alternative span or guest space.

## Hard-family and literature controls

The established hardness baseline is odd-charge Tseitin 3-CNF on suitable cubic expander graphs: h vertex charges, 3h/2 edge variables, four original signed clauses per vertex parity, 4h total clauses, N=Theta(h log h) bits. Urquhart (JACM 1987, DOI 10.1145/7531.8928) gives exponential bounds in ordinary Resolution on appropriate expanders, not for the complete mixed R_mix341 calculus or arbitrary SAT algorithms. Four-facet source authentication and GF(2) elimination remain a legal easy algebraic control. The 16 K4 cases tested here are finite controls, not certified asymptotic hard instances. H_n is elementary Horn UNSAT; it is a focused falsifier, not a hard SAT candidate.

Recovered both root trackers, issue #3, Nov 9 abstract-interpretation handoff, AGENTS.md, CODEX.md, repository skill, LSPV-2/522, peers LSPV-1/539, LSPV-3/537, LSPV-4/522, LSPV-5/464, historical MODELBRIDGE-0010, Grok Nov 9 1230 and Claude TPORT-0002. Primary research consulted: D'Silva/Haller/Kroening POPL 2013 ACDCL, DOI 10.1145/2429069.2429087; Giacobazzi/Ranzato/Scozzari JACM 2000 complete shells, DOI 10.1145/333979.333989; Clarke et al. JACM 2003 CEGAR, DOI 10.1145/876638.876643; Ben-Sasson/Wigderson JACM 2001, DOI 10.1145/375827.375835. These papers do not prove this experiment-specific result.

Change-aware actual files: konard/p-vs-np README blob 0e0ec77f and proof_status.json 93b77ed3; blkph0x/p-vs-np-proof-research METHOD_INDEX 18d693ea; meelgroup/frat-xor format.md 986a21aa; MassimoLauria/cnfgen Tseitin source 4bb5fd19; openai/math README cc5b0a03. PySAT README retrieval returned 404; do not count as reviewed.

**Remaining:** [P2-A2], [P2-A4], [P2-A5] OPEN. No universal uniform all-input (SAT/UNSAT/malformed) exponent-oblivious recursively iterable solver transformation, no fully charged same-machine t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2), and no safe guest peak-space bound. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. Future test: authenticated CDCL learning/backjumping plus algebraic and RUP shortcuts under one explicit physical costed transition model. **P versus NP OPEN.**
