# LSPV-2: EXTENSIONAL-COST-NOGO372

November 3, 2026, 15:12 PST. **PROVED/EXACT deductions from earlier theorem 341; COMPUTATIONAL finite controls; independent specialist review pending.** Full mixed-calculus superpolynomial minimum, B1, B2, B3, and P versus NP remain OPEN.

## Fixed model and previously certified hard-family anchor

Keep unchanged Rmix341: zero-cost authenticated original CNF clauses, unit-cost paid distinct nodes of binary-premise shared refutation DAGs, including RES, AND3, binary GF(2) operations, justified LOCAL-CONVERT and paid conservative DEF. The input length N is encoded bits, not the number n of variables. W_R(F) is minimum legal paid-DAG cost and Wbar_R(N) is the worst such minimum for UNSAT source encodings of at most N bits.

The established expander-Tseitin lower bound (Urquhart 1987; Ben-Sasson and Wigderson 2001) asserts existence of c>0, h0 and bounded-degree odd-charge expanding graphs such that, for all h>=h0, every unrestricted shared-DAG **ordinary Resolution** refutation of the corresponding signed local CNF requires at least 2^(c h) proof lines. This is restricted proof-system hardness, not a theorem about every SAT machine. For the cubic version there are n=3h/2 variables, m=4h width-three clauses and N=Theta(h log(h+2)) ASCII DIMACS bits up to the standard byte-to-bit constant. Not every cubic graph is an expander.

The previously certified LSPV-2 MIXED-TSEITIN-MIN-DAG341 theorem proves for every connected simple bridgeless cubic graph G with odd charges that

$$
W_{R_{mix341}}(F_{G,chi})=4h-1.
$$

Its lower bound uses 4h indispensable source clauses and binary-premise ancestry; its upper proof takes three AND3 inferences per vertex and h-1 GF(2) additions. It is a GLOBAL optimum in the fixed mixed calculus, not a bounded search result. For appropriate cubic expanders, Resolution requires exponential size on the very same input for which Rmix341 needs only linear logical nodes. The system-inclusion inequality points W_mix <= W_Resolution, not the reverse.

## Theorem 1: same semantics, divergent exact mixed costs

Take the odd cubic Tseitin F of h vertices, with declared n=3h/2 original variables, and the alternate source H_n consisting of two contradictory units (x1) and (NOT x1) with the same declared n variables. Then

$$
Sol(F)=Sol(H_n)=emptyset,
\qquad W_{R_{mix341}}(F)=4h-1, \qquad W_{R_{mix341}}(H_n)=1.
$$

**Proof.** Summing all odd-charge vertex equations gives 0=1; both sources therefore have no satisfying assignments. The first exact cost is prior theorem 341. One Resolution step on the opposing units produces the empty clause, and neither source is already empty, so the second exact cost is one.

**Corollary.** For any proposed extensional intrinsic quantity I(F)=f(n,Sol(F)) which is a valid lower bound I(F)<=W_R(F) for every UNSAT source, one necessarily has I(F)<=1 throughout this infinite odd cubic Tseitin family. Thus purely truth-set-based information cannot certify a growing source-dependent minimum-DAG cost. With comment-enabled DIMACS, H_n can be padded to exactly the same encoded byte length as F without adding source clauses or paid nodes. No claim of exact-length equality is made under a different comment-free canonical grammar.

This **falsifies a semantics-only representation-invariant cost**, not source-indexed signed-hypergraph/provenance invariants that charge converting between representations.

## Theorem 2: complete semantic canonicalization iff P=NP

For a fixed polynomial-time parseable encoding of general CNF with declared n-variable interface, a **uniform polynomial-time complete semantic canonicalizer** C satisfying C(F)=C(G) if and only if Sol(F)=Sol(G) for all same-n valid inputs exists **if and only if P=NP**.

**Proof, forward.** On input F, compute C(F) and C(H_n) and compare them. Equality is exactly UNSAT. Parse malformed strings separately. This puts SAT in P.

**Proof, reverse.** Under P=NP, CNF equivalence is decidable in P, since inequivalence has an NP witness assignment. For a valid input F of length N, choose the globally shortest, then lexicographically first, valid same-n CNF representing its Boolean function. Such a source exists with length <=N because F itself qualifies. For any candidate length and fixed binary prefix, asking whether some equivalent valid CNF of that length and prefix exists is in NP when equivalence is in P, hence in P. Searching at most N lengths and at most N prefix bits yields the desired canonical form uniformly in polynomial time. Handle malformed inputs with a designated error output.

This is a precise warning against treating complete semantic minimization as free polynomial preprocessing. It does not rule out weaker provenance-sensitive invariants and proves neither side of P versus NP.

## Lemma: fixed uniform algorithm, polynomial on every exact affine block source

One fixed total correct CNF-SAT decider parses arbitrary encoded CNF and handles malformed inputs. It groups proper width-three clauses by their variable supports. If every group contains exactly the four distinct clauses forbidding one XOR parity class, it authenticates each group by eight local truth assignments, compresses active original-variable IDs, and uses Gaussian elimination over GF(2). This decides SAT and UNSAT in polynomial bit time and polynomial peak space on every recognized formula, including all standard odd/even cubic Tseitin sources, independently of graph expansion, variable renaming, clause order and global variable sign flips. Otherwise it uses correct exhaustive SAT search, which may require exponential time. No per-input hardcoding is used.

Therefore the established exponentially Resolution-hard expander Tseitin family is polynomial-time decidable by **one fixed total correct uniform SAT machine**. This is a family-wise transfer failure, not a genuine worst-case B2 failure: the machine's global all-input worst-case time may be exponential. Neither is B3 disproved.

## Falsifiers and controls

F1: Equal satisfying sets force equal W_R. **FALSIFIED/EXACT** by 4h-1 versus one.

F2: Huge declared variable IDs force huge Gaussian matrices. **FALSIFIED/COMPUTATIONAL** by a SAT three-active-variable parity source with declared variable bound 1,000,000,000, handled by active-ID compression.

F3: Renaming, clause reordering or consistent polarity changes evade affine recognition. **FALSIFIED/COMPUTATIONAL** on the four standard cubic graph controls, both labels.

F4: Polynomial complete semantic canonicalization is independent of P versus NP. **OPEN**: Theorem 2 shows this is an equivalent formulation of P=NP, not an assumption.

The dependency-free public JavaScript fixture suite actually ran in the available V8 runtime and passed **90 assertions**: eight odd/even K4, K3,3, cube and Petersen controls, seven malformed sources, valid repeated-literal and tautological clause controls, exact DIMACS comment padding, an enormous declared variable index, and eight evaluations of a different-syntax same-nonempty-function pair. The even controls have 8,16,32,64 satisfying assignments and odd controls zero. The old exact mixed minima 15,23,31,39 are **inherited from 341**, not established by this runner. Its finite exhaustive fallback deliberately caps n<=16, while the mathematical all-input decider has no cutoff.

## Work and space, quantifiers and limitations

A paid logical DAG node is not a machine step. Parsing, source authentication, variable indexing, eight-row local tests, Gaussian bit operations, output and simultaneous matrix storage must be charged. Dense elimination uses polynomial bit work and at most O(N^2) matrix bits for recognized inputs. The compact mixed affine proof has O(h) paid nodes but may use O(h^2) encoded mask/proof bits and bit checking work. The general decider's exhaustive fallback has up to 2^n poly(N) time; no polynomial global all-input time is claimed. Exponentially large representations may be evaluated and charged, but compact affine alternatives must also be allowed. For future recursive FLMV transport, every phase must obey s' <= max{rho,eta,lambda,lambda*s}; temporary N-bit buffers imply rho>=1.

B1 (all A, exists polynomial p_A, all UNSAT F, W_R(F)<=p_A(N+T_A(F))) remains OPEN. B2 (all A, exists polynomial p_A, all N, Wbar_R(N)<=p_A(N+T_A^wc(N))) remains OPEN. The weakest sufficient B3 (SAT in P implies polynomial Wbar_R for the SAME fixed Rmix341) remains OPEN. No swap between max_F min_proof and a per-instance minimum over different deciders is permitted.

## Corpus and independent assessments

Read first the approved five-role directive at commit 4e29ed7646f484707767acb6e63ec5f38afd98a8 and blob 033b54b87b7cbe94912af5cf67daa52859143a07, issue #3, AGENTS.md, CODEX.md, and repository pnp-research skill. Read original theorem 341 (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb), LSPV-2 371, LSPV-1 BIT-WITNESS-SEPARATION372, LSPV-3 BOUNDED-INTERFACE367, LSPV-4 GROK-QUERY-EXPONENT364 and referee 299. Earlier SOURCE-SUCCESSOR-ENDPOINT-EQUIV1 is related but does not supply this exact same-interface W_R cost collision; parity recognition itself was already known, so no new academic novelty is asserted for it.

Actual Grok file GROKPROOF/2026-11-03_2214_PROGRESS.md (blob 59fe73c20473bd6bc20500cf58d75e42519aee88) still marks its charged all-input ARC contraction OPEN. Actual Claude file research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67) concerns a restricted alternation-trading system rather than unrestricted SAT computation or B3. The older Grok query upper-to-lower time inference had already been rejected by LSPV-4 and is not reused. Searches in project history surfaced previous semantic endpoint and parity controls; searches in github.com/openai did not yield an applicable proof checker. Primary literature checked Urquhart 1987, Ben-Sasson and Wigderson 2001, and Cook and Reckhow 1979. The container-backed checkout and preflight failed transiently; actual testing was done in a V8 runtime. No task, rule, title or schedule was changed.

**Next exact gap:** build a source/provenance-sensitive representation invariant that survives compact circuits, GF(2), paid DEF and named internal LOCAL-CONVERT wires, charging intermediate encoding lengths and conversion. Separately establish a valid same-system B3 machine-correctness bridge. P versus NP remains OPEN.

**References.** [1] Urquhart, Hard Examples for Resolution, JACM 34 (1987), 209-219. [2] Ben-Sasson and Wigderson, Short Proofs Are Narrow: Resolution Made Simple, JACM 48 (2001), 149-169. [3] Cook and Reckhow, The Relative Efficiency of Propositional Proof Systems, JSL 44 (1979), 36-50. [4] LSPV-2 MIXED-TSEITIN-MIN-DAG341, 2026-11-02, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb.
