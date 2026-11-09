# LSPV-2/522: costed affine may-CEGAR and an exponential guest-search falsifier

**2026-11-09 09:22 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

Proof-chain evidence: proposed new [P2-L2-522] refining [P2-A2], [P2-A4], [P2-A5] without closing them. [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2] all OPEN. This is a separate declared experimental solver, **not** historical R_mix341.

## IDEA, falsifiers and SEARCH

Candidate: source-authenticated affine+clause may-abstraction has a finite CEGAR refinement bound, but the bound does not imply cheap guest search.

Precise falsifiers: (1) corrupting one 3-clause facet preserves a purported exact affine row and falsely excludes models; (2) a failed candidate does not yield a fresh violated original clause; (3) refinement count exceeds the number of omitted clauses; (4) the exponentially slow guest family remains expensive even when the solver is allowed unit propagation. Falsifiers (1)-(3) were rejected in finite controls and proofs; (4) correctly invalidates any *unrestricted* hardness interpretation.

Read the complete current proof1.txt and proof2.txt, issue #3, the 2026-11-09 cost-sound abstract-interpretation handoff, AGENTS.md, CODEX.md, repo skill, actual LSPV-2/521, LSPV-5/462 and /463, LSPV-3/536, MODELBRIDGE-0010, GROKPROOF/2026-11-09_1230_PROGRESS.md and Claude TPORT-0002. MODELBRIDGE-0010 rejects unrestricted static normalization; this work does not revive it.

Primary sources: D'Silva, Haller and Kroening, *Abstract Conflict Driven Learning*, POPL 2013 (https://www.kroening.com/papers/popl2013.pdf); Giacobazzi, Ranzato and Scozzari, *Making Abstract Interpretations Complete*, JACM 2000, DOI 10.1145/333979.333989; Clarke et al., CEGAR, JACM 2003; Urquhart, *Hard Examples for Resolution*, JACM 1987, DOI 10.1145/7531.8928. These methods do not already prove the present solver-specific theorem.

Repository source check: konard/p-vs-np README blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95; blkph0x/p-vs-np-proof-research README f397a7747eaca82df3d754d0a4b4bab1fe10f814; openai/math README cc5b0a03bca6c742f045d683b6647a6f44ef2cae; pysathq/pysat README fefde10b1426a92a21425029892f3f49466bf03c; msoos/cryptominisat README 7636988713ee16802b84fb1cdf688ea8f87da70e; meelgroup/frat-xor README 38a137bca4d4ab6443703d4c31fba5783021c581. CNFgen default README lookup failed. External proof formats do not replace historical R_mix341.

## Exact model and theorem

Parse immutable canonical ASCII source `T3|n|m|c1|...|cm\n` with nonempty width-one, two or three distinct-variable signed clauses, reject malformed/noncanonical sources. For a group of four distinct width-three clauses on identical variable IDs, inspect all eight assignments and extract a parity equation **only** when their conjunction has precisely the four assignments of one parity. Other clauses remain residual original IDs.

With extracted rows E and source-indexed learned clauses J, the abstract model set is

$$
S_J=\{a\in\{0,1\}^n:a\models E\land\bigwedge_{j\in J}C_j\}.
$$

Each extracted equation is an exact original-clause consequence; hence for every J, `Mod(F) subseteq S_J`. Gaussian elimination can establish that E has no solutions. Otherwise a lexicographic exhaustive guest enumerates complete assignments satisfying E and J. Replay against the **original** CNF either authenticates a SAT witness or returns a new violated original source clause ID j. Adding j strictly eliminates the candidate. An empty S_J means UNSAT.

**Theorem (PROVED/RESTRICTED).** For every source valid under this explicitly declared grammar, the specified algorithm is total and SAT/UNSAT correct, and uses at most the number of residual unextracted original clauses as strict refinements. Proof: exact quartet extraction preserves all genuine models; every candidate already satisfies all learned clauses, so a violated clause is new; there are finitely many source clauses; exhaustive guest enumeration is complete; and replayed witnesses satisfy all original clauses.

**Parameterized class-relative negative theorem.** For the valid source family

$$
U_n=\bigwedge_{i=1}^n x_i,
$$

there is no quartet. Lexicographic restart enumeration produces candidates `1^j0^(n-j)` for j=0,...,n, with the last candidate the real SAT witness. It performs exactly

$$
Q(n)=\sum_{j=0}^n(2^n-2^{n-j}+1)=(n-1)2^n+n+2
$$

complete candidate checks, although there are just n refinements. This is a lower bound against **this specific restart-from-zero enumeration guest only**. Unit propagation finds the same witness using O(n) deductions, so this is not a SAT-machine lower bound and not an obstacle to universally allowed learning or preprocessing.

Operations declared: exact affine deduction, lexicographic branch enumeration, source-clause replay, source-indexed refinement/learning, cross-round row and clause sharing. No CDCL implication graph, arbitrary learned resolution clauses, incompatible-context join, free equivalence oracle, general proof-DAG search or native R_mix341 steps are admitted. OR alternatives are tried in order, not conjoined. The model-set overapproximation is not a sound coverage certificate for **all** budget-bounded SAT algorithms.

## Established hard family and controls

For cubic connected G=(V,E), h vertices and 3h/2 edge variables, each vertex charge is encoded by exactly four proper signed 3-clauses forbidding parity-incorrect incident edge assignments. Odd total charge is UNSAT; even charge SAT. For suitable *expander* graphs, Urquhart gives exponential ordinary Resolution refutation size. The original encoding has 4h clauses and Theta(h log h) source bits. This does **not** imply full mixed R_mix341 or arbitrary-algorithm hardness. Exact four-facet extraction plus GF(2) is the mandatory short algebraic control. Finite K4, prism and cube are **not** labeled certified expander-hard.

## Replayable finite evidence and costs

Independently written Python and Node.js checkers agreed on **25 exact original-source SHA-256 fingerprints**, all SAT/UNSAT labels (17 SAT, 8 UNSAT), all 57 refinement steps, row counts and each complete-assignment trial count. Twelve signed 3CNF Tseitin controls, an eight-triple UNSAT core, one SAT proper ternary, a Horn/binary SAT, contradictory units, a corrupted odd-charge K4 quartet restoring SAT, and eight all-positive-unit instances were checked. Python: 237 grouped assertions; JavaScript: 229 assertions; both rejected six malformed packets. The 12-unit case uses **45,070** guest candidate trials; unit propagation requires twelve unit steps.

Explicit experimental counters include original byte size, initial clause reads, quartet validation trials, Gaussian row XORs, candidate checks, replayed clause checks and retained learned literal count. They are semantic operation counts, **not** native FLMV machine timing or complete all-phase peak-space measurements. Source parsing, allocations, index reads, failed policy attempts, caches and simultaneous ancestor state must still be charged before any general time-space claim. Guest evaluation may be exponential despite linear refinements.

## Remaining transfer

[P2-A2], [P2-A4], [P2-A5] OPEN: no all-input solver-dependent `A -> Phi(A)`, no same-machine recursive applicability, and neither fully charged FLMV contraction inequality established. Historical grammar, rule weights and proof minimum obligations unchanged; B1/B2/B3 also OPEN. The next step is to replace the deliberately deficient lex guest with a class including legal unit propagation, conflict learning and shared computation, then prove an overapproximate budgeted transition simulation rather than infer a universal lower bound from this toy guest. P versus NP remains OPEN.
