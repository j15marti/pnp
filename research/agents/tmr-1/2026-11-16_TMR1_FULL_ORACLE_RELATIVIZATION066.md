# TMR-1/066: fully relativized exact counting and the missing oracle-gate compiler

Date: November 16, 2026 PST. Owner: TMR-1 / PNP Machine Model Lead. Track C. Named dependency: C1h-FULL-ORACLE-RELATIVIZATION. Scientific status: PROVED/EXACT RESTRICTED, via standard PSPACE completeness; external independent mathematical review OPEN. P versus NP OPEN.

## Candidate, precise model, quantifiers and falsifiers

Candidate: purely relativizing reasoning from uniform polynomial-time exact circuit counting to a P-versus-NP separation is invalid, even when the circuit class and counting premise are correctly relativized.

Quantifier prefix:
\[
\exists A\,\exists U^A\,\exists d\ge1\,\forall z\in\{0,1\}^*:
\quad U^A(z)=
\begin{cases}
\#C_z^A,&z\text{ authentic A-circuit source},\\
\mathrm{INVALID},&\text{otherwise}.
\end{cases}
\]
Here one total deterministic oracle machine U^A has polynomial total oracle time and polynomial simultaneous writable space, while P^A=NP^A.

Falsifiers identified before the primary-source audit: (F1) the genuine oracle-gate count-threshold language might not be in PSPACE; (F2) its TQBF reduction might require exponential question length; (F3) P^TQBF and NP^TQBF might not both be PSPACE; (F4) the ordinary Boolean Tseitin compiler might already translate arbitrary oracle gates to ordinary CNF at polynomial cost. F1--F3 are discharged, while F4 is precisely isolated as a strong missing premise below.

## Authentic input-to-count circuit model

Fix A=TQBF, the PSPACE-complete set of true closed quantified Boolean formulas; malformed oracle queries are NO. Define one explicit prefix-parseable *oracle-circuit* source grammar, C1a^A, distinct from the ordinary Boolean C1a grammar. The source starts with unary 1^q 0, 1^G 0 for q>=1 and G>=1, then topologically ordered gate records. Boolean records encode two earlier predecessor IDs and a complete four-bit truth table. Oracle records encode unary 1^m 0 and m earlier predecessor IDs, allowing m=0. The m predecessor bits are evaluated and concatenated into the **actual materialized TQBF query word** at that gate. A final output index selects the circuit result. All indices have a common fixed width max(1,ceil(log_2(q+G))). Complete lengths, opcode tags, every predecessor relation, every query length, output and absence of trailing junk are authenticated before accepting an input. All invalid sources yield INVALID.

Let N denote the entire encoded source bit length. Then q+G=O(N) and m<=N on every authentic source. Arbitrary fan-out, shared earlier gates, repeated query bits and adaptive dependence through earlier Boolean and oracle outputs are permitted. Every true assignment to the q *original* Boolean inputs counts once:
\[
\#C_z^A=\sum_{x\in\{0,1\}^q} C_z^A(x),
\qquad 0\le\#C_z^A\le2^q.
\]
No query has a free provenance, no pretrained table is supplied, and no input-dependent advice exists.

## Theorem 1: exact FP^TQBF counting on the same oracle execution

For A=TQBF, one uniform total deterministic oracle machine outputs the exact count for every authentic C1a^A source and rejects malformed sources. For a sufficiently large fixed integer d:
\[
Q_A\le q+1,\qquad
T_{\rm total}=O((q+1)(N+q+1)^d),\qquad
S_{\rm peak}=O((N+q+1)^d).
\]
These are simultaneous costs of the SAME complete oracle-machine execution, with each completed TQBF oracle answer charged one unit only in the declared oracle model.

Proof. For a given original assignment, evaluate the source gates in topological order. Every TQBF query has at most N bits and TQBF itself lies in PSPACE. Therefore, an ordinary no-oracle deterministic polynomial-space machine can compute each individual oracle-gate bit and reuse every shared gate result; the entire source evaluation uses polynomial space. Enumerate all 2^q original assignments and maintain a q+1-bit counter. Hence the ordinary count-threshold predicate
\[
L_{\ge}^A=\{(z,h):z\text{ authentic and }\#C_z^A\ge h\},
\quad 0\le h\le2^q
\]
lies in ordinary unrelativized PSPACE **for the chosen fixed A=TQBF**. Its explicit input length is O(N+q), since h occupies q+1 bits.

By the standard uniform polynomial-time many-one completeness of TQBF for PSPACE, one fixed polynomial-time map R writes a complete QBF query representing L_ge^A(z,h). The total query length and actual writing time are each O((N+q+1)^d), for fixed sufficiently large d. One deterministic oracle machine authenticates the actual N-bit source, then uses binary search on 0,...,2^q, requiring at most q+1 adaptive threshold oracle calls. Each call materializes R(z,h) on the actual query tape. All unsuccessful thresholds, source rereads, reusable buffers, gate wires, query symbols, head motion, arithmetic, output and invalid rejection are included. At most one query buffer is live at a time, so the stated time and peak writable space belong to the same complete execution. An oracle answer is NOT an ordinary no-oracle polynomial-time computation. QED.

Because TQBF is PSPACE-complete, PSPACE subseteq P^A. Simulating each polynomial-length TQBF query in polynomial space and using Savitch gives NP^A subseteq NPSPACE=PSPACE. Therefore
\[
\boxed{P^A=NP^A=PSPACE,\qquad\#CIRCUIT^A\in FP^A.}
\]
This is the **fully relativized** countermodel. The earlier /065 ordinary-#CNF oracle example alone did not explicitly model A-gates in the input, so by itself was insufficient to certify full syntactic relativization.

## Theorem 2: exact missing compiler premise

Suppose a single uniform polynomial-time procedure K translates every authentic C1a^A TQBF-oracle circuit into an ordinary Boolean 3CNF K(z) of polynomial encoded length with
\[
(\exists x\ C_z^A(x)=1)\iff K(z)\in SAT.
\]
Then PSPACE subseteq NP, hence PSPACE=NP.

Proof. Given any closed QBF psi of length m, build a legal C1a^A source with one dummy original Boolean input, O(m) constant Boolean gates whose fixed output bits spell psi, and one final oracle gate querying the entire fixed word psi. Source length O(m log(m+2)); its original-input accepting count is 2 if psi is true and 0 otherwise. The hypothetical polynomial-time K maps this source to an ordinary polynomial-length 3CNF satisfiable exactly when psi is true, providing TQBF <=_m^p SAT. By completeness, PSPACE subseteq NP, and the reverse inclusion is standard. QED.

This is a conditional implication, NOT proof that K cannot exist: NP versus PSPACE remains OPEN. It establishes the exact missing interface in any attempt to extend the user's ordinary functional Tseitin C1b compiler to arbitrary oracle gates. Four-row constant Boolean truth tables do not implement a TQBF membership operation. Anthropic's pinned MainTheorem counts **ordinary** 3CNFs, not formulas containing oracle predicates. No polynomial-cost ordinary-CNF compiler for such oracle gates was furnished or claimed.

## Integration point and hierarchy consequence

The unrelativized chain retains its separate scope: authentic binary shared Boolean-DAG source -> C1b parsimonious CNF -> repaired C1c four-density normalizer -> exact C1d low-first formal input -> pinned fixed finite-stack counting theorem (upstream kernel evidence, **independent local replay OPEN**) -> C1e same-execution conventional multitape implementation -> exact count -> charged Jahanjou--Miles--Viola vector clause decoder and coherent 2^v-variable-name witness -> binary nondeterministic hierarchy -> **CONDITIONAL mildly superlinear infinitely-often general-circuit lower bound for E^NP**. The new TQBF-oracle countermodel is a *separate* correctly relativized source-to-output chain; it does not replace any of those stages or yield an unrestricted result.

A claimed NP-level implication requires an identified genuinely nonrelativizing premise with explicit encoding, quantifier, bit-time and model semantics. Neither P!=NP nor NP superpolynomial circuit lower bounds follow. Algebrization and Natural Proofs audits remain OPEN for any actual future NP arrow.

## Mandatory gates and controls

DISJ sanity: **PASS restricted**. DISJ_k has compact 2CNF / linear circuit representations and exactly 3^k satisfying assignments in its independent-pair model. No rank-to-hard-work inference.

Relativization: **FAIL** for the intended purely relativizing NP-promotion inference, now with authentic A-gate circuit inputs. New nonrelativizing premise OPEN, with algebrization/Natural Proofs safeguards retained.

Simultaneous DTISP: **PASS for stated same-run oracle time and peak writable space; NOT APPLICABLE to FLMV forbidden pair**. Oracle-internal computation is explicitly outside the physical time count and cannot be inserted into a standard no-oracle forbidden region.

Deterministic configuration counting: **PASS, upper-bound safeguard only**, with all query-tape cells and heads included. It states an upper bound of 2^{O(S+log N)} for fixed halting deterministic oracle machines, not a necessary-work lower bound or randomized/quantum assertion.

Horn/dual-Horn/2SAT, affine/Gaussian, treewidth, equality, autarkies, independent products, padding/auxiliaries, selectors, unique-solution rank-one, local basis and field effects, alternative compact algorithms, sharing, caches and recomputation remain legal. Majority ties and quantum amplitudes are NOT APPLICABLE to this deterministic exact countermodel. /341 remains FAIL full UNSAT authority; /386 RESTRICTED.

## Evidence, restrictions and ONE next dependency

Sources: Jahanjou, Miles and Viola, *Local reductions*, March 2014, Theorem 1 and Corollaries 2/3 (https://www.khoury.northeastern.edu/home/viola/papers/explicit.pdf); pinned Anthropic formal-math MainResults.lean and Solution.lean at commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5 (https://github.com/anthropics/formal-math/tree/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth); University of Wisconsin CS710 complexity lecture 06 (https://pages.cs.wisc.edu/~dieter/Courses/2011f-CS710/Scribes/PDF/lecture06.pdf); Baker, Gill, Solovay (1975); Savitch (1970); existing TMR-1/065 dated original report.

This is a **symbolic standard-theorem-based construction**, not a newly run numerical experiment, source microtrace or native TQBF evaluator. No executable or immutable raw test file is claimed for /066. PNP checkout is unavailable because direct GitHub DNS resolution failed; therefore the updated repository preflight was NOT executed. Lean, Lake and Cargo are absent locally. No independent pinned Lean/nanoda build, per-theorem axioms replay, physical no-oracle verification, or complete LaTeX build was executed. Upstream CI remains evidence of its own run only. External mathematical peer review OPEN.

**ONE next load-bearing lemma:** independently build Anthropic's exact pinned Lean 4.33.1 and Mathlib dependencies, inspect transitive axioms and execute both Lean and nanoda kernel checks, then audit fixed FinTM2 input/stack/output physical semantics. P versus NP remains OPEN.
