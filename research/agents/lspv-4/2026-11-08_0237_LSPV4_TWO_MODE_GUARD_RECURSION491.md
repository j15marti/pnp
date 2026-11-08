# LSPV-4/491: Two-mode guarded same-parser recursion and its resource limits

**2026-11-08 02:37 PST | Route A resource auditor | PROVED/RESTRICTED symbolic + COMPUTATIONAL finite checks | P versus NP OPEN**

Exact nodes: material evidence for [P2-A4]. [P2-A2] and [P2-A5] remain OPEN. Cross-chain [P1-01], [P1-03], [P1-04], and Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. No historical R_mix341 rule or weight is changed.

## IDEA -> SEARCH -> ITERATE: hypothesis and falsifiers

**Initial idea.** The /490 self-iterable pinned guard applied its eight-clause normalizer to EVERY subsequent generation, yielding m_{k+1}=16m_k+4, although all outputs were already proper signed 3CNF. A source-uniform two-mode procedure may use the direct two-clause guard for already-proper inputs and the prior padded eight-clause clause-local normalization for other inputs. The prediction is a same-parser, exact both-label source construction with only m_{k+1}=2m_k+4 after one round, while retaining a constant-position output-bit map for lazy indexed reads.

Four predeclared falsifiers: (F1) direct guard fails the pointwise existential identity; (F2) a guest escapes its own parser or extension wires collide; (F3) empty, unary, duplicate, tautological or malformed originals break the slow branch; (F4) prior project work already contains the stronger all-depth two-mode recurrence. Symbolic work and finite tests reject F1-F3; project search confirms /487, /489, /490 already supply the ingredients, but no prior exact two-mode all-depth recurrence was found in those inspected files. No broader novelty assertion follows.

**Sources actually reviewed.** Both complete root proof trackers; current issue #3 and recent peer comments; November 2 governing five-role handoff; AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md; LSPV-2/487, /488, /489; LSPV-4/489 and /490; GROKPROOF/2026-11-06_2316_PROGRESS.md and Claude ONETAPE-0001. The original FLMV paper (Fortnow, Lipton, van Melkebeek and Viglas, JACM 52, 2005, DOI 10.1145/1101821.1101822) was inspected from its authors' PDF, particularly machine Section 2.1, printed p.4, and Corollary 5.8, printed p.18. Primary established restricted-hardness sources: Urquhart, JACM 34 (1987), DOI 10.1145/7531.8928; Ben-Sasson/Wigderson, JACM 48 (2001), DOI 10.1145/375827.375835.

Actual external files checked: konard/p-vs-np README.md and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 (finite machine P subset NP, not NP subset P); blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and REVIEW_ADDENDUM.md (restricted parity-polytope barriers, no universal proof); MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab; openai/math/README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae. The FRAT-XOR obsolete master branch URL returned 404, so it was not treated as reviewed; earlier Grok and project work already discuss its separate format. General public web search was used, no separate Google-branded client. No external source contains the missing SAT compiler.

## Theorem 491.1, proved only for this source construction

Use the SAME canonical binary width<=3 clause-record grammar as /490: input m clauses, declared n<=3m+3, unary header $1^b0$, b-bit n and m, and m fixed three-slot records with each slot b+2 bits, where $b=\lceil\log_2(128(n+m+3))\rceil$. A malformed input is rejected by the distinct parser/controller.

If every input clause has exactly three distinct nonzero original variables, set Q(F)=F and q=m. Otherwise, for EACH clause independently use exactly eight proper ternary clauses with private auxiliary variables: a tautology gets eight repetitions of a satisfiable fresh ternary clause; an empty clause gets all eight sign patterns on three fresh variables; a unit clause gets four patterns on two fresh auxiliaries repeated twice; a binary gets both signs on one auxiliary repeated four times; a proper ternary gets eight copies of itself. This produces q=8m proper 3-clauses with pointwise existential projection F. No variable-length clause-dependent record index is required, since the *whole source* chooses one of two uniform modes.

For each D_i=(a_i OR b_i OR c_i) in Q(F), introduce a fresh h_i and global z and output

$$
(a_i\lor b_i\lor h_i),\qquad(\neg h_i\lor c_i\lor z).
$$

Add the four proper signed ternary pin clauses

$$
P(z,u,v)=\bigwedge_{\sigma,\tau\in\{-1,+1\}}
(\neg z\lor\sigma u\lor\tau v).
$$

With fresh private IDs and both the local normalizer and guard auxiliaries existentially eliminated,

$$
\exists_{\mathrm{new}} J_Q(F)\iff z\lor F,
\qquad
\exists_{u,v}P(z,u,v)\iff\neg z.
$$

Hence the new source K_2(F)=J_Q(F) AND P satisfies the **pointwise** original-variable projection $\exists_{\mathrm{new}}K_2(F)\iff F$. For all finite k, SAT(K_2^k(F)) iff SAT(F), with no external guard contexts. This is a syntactic/equisatisfiability result, not proof-size preservation or a universal SAT decision algorithm.

Choose normalization auxiliaries above original IDs up to n+3m in slow mode. Let n_B=n (fast) or n+3m (slow), h_i=n_B+i, z=n_B+q+1, u=z+1, v=z+2. The output has n'=n_B+q+3. With n<=3m+3, fast mode has n'<=4m+6<=3(2m+4)+3; slow mode has n'<=14m+6<=3(16m+4)+3. Thus the SAME canonical parser accepts the output, including m=0. The output is always strict proper 3CNF.

The exact clause recurrence is

$$
m_1=\begin{cases}2m_0+4&\text{if F initially proper strict3},\\16m_0+4&\text{otherwise},\end{cases}
$$

and for k>=1,

$$
\boxed{m_k=2^{k-1}(m_1+4)-4}.
$$

For initially proper strict-3 input, $m_k=2^k(m_0+4)-4$. For arbitrary other valid input, $m_k=2^{k-1}(16m_0+8)-4$. This greatly improves /490's recursive 16^k count but **STILL EXPANDS** and does not construct a length-N^{1/2} child.

## Native resource ledger and scope firewall

Original-source parser plus detection of proper-triple mode must inspect every original record, using symbolic O(N polylog N) time and O(log N) counters on the indexed read-only-source model. Both fast and slow output use a UNIFORM fixed number of output clauses per input record, so each virtual child bit can be located by quotient/remainder arithmetic, a constant number of original source-field accesses and O(polylog N) symbolic time/O(log N) WORK+INDEX per fixed layer. At any fixed finite recursion depth, virtual nested translation has O(k log N) symbolic workspace, depth-dependent polylog time per bit, and no materialized child buffer. These are not native transition-by-transition benchmarks.

Full materialization writes Omega(M) output bits and, **if the child is held in WORK to be passed to the guest**, requires Omega(M) high-water workspace even if later freed. The original FLMV input is read-only, the output write-only, and INDEX content erased on indexed access. A lazy guest instead incurs paid INDEX-address rebuilding, all source reads, guest time, simulated head states, code/policy choice, failed policies, parsing, output, intermediate ancestors, retention versus recomputation, shared caches and all-phase peak. None are free. A fixed k-fold lazy input has length Theta_k(N), so simply invoking the unchanged solver A still incurs its original worst-case time exponent: removing physical child copying does not prove t'<=max(11/10,3/5+t/2) or s'<=max(1/2,s/2). The materialization envelope s'<=max(rho,eta,lambda,lambda*s) remains an unfilled compiler obligation, not a theorem derived here.

**Proof model:** no R_mix341 inference node, shared proof-DAG certificate, branch/discharge rule, weighted proof-work optimum or B3 simulation is used. Algebraic and extension-variable shortcuts remain legal whenever admitted by the actual fixed calculus; this source reduction says nothing about hardness against those shortcuts.

**Published hard-family control:** Odd-charge cubic Tseitin contradictions on expanding 3-regular graphs use 4H original proper three-literal signed parity clauses, 3H/2 edge variables, N=Theta(H log H) encoded bits, and established exp(Omega(H)) lower bounds in ORDINARY shared-DAG Resolution on suitable expanders (Urquhart; Ben-Sasson/Wigderson), not in R_mix341 or all algorithms. Fast mode applies immediately, yielding $m_k=2^k(4H+4)-4$. Authenticated GF(2) parity summation provides an efficient algebraic upper-bound control. No Resolution-lower-bound-preserving reduction into the full historical mixed calculus is claimed.

## Executed finite checks and resulting status

The committed JS script experiments/arc/lspv4_491_two_mode_guard.cjs, blob 60de78cc2f315eac684d17ea66bcdc9ea045b01d, was refetched completely and its exact source body executed in V8 with an equivalent strict assertion shim. Results: **111 original inputs; 7 fast and 104 slow; 2,197 assertions; 1,680 explicit local normalization truth-table checks; 35 second-level complete parser roundtrips; five malformed headers rejected; zero failures.** An independently implemented Python fallback passed **1,837 checks over 111 inputs**. Raw JSON results: results/raw/arc/2026-11-08_0237_LSPV4_491_TWO_MODE_GUARD_RAW.json, blob 6e67541e36e5784291ce328dcd406163a02bc5a5. Tests physically materialize sources and are finite correctness checks only. Neither native FLMV instruction-level machine nor original historical R_mix341 verifier was executed.

**Advance:** one-time padded normalization and direct proper-triple guarding reduce source growth from 16^k to 2^k after initialization, with exact same-parser and fixed-record random-access addressing. **Remaining gap:** a *shrinking*, solver-dependent, ALL-INPUT, three-label malformed-aware, recursively iterable transformation on the SAME FLMV machine with charged guest execution, time/space, search/restarts, output and caches. [P2-A2], [P2-A5], B1/B2/B3 and P versus NP remain OPEN.
