# TMR-1/050: A parsimonious circuit-to-3CNF wire-tax and the exact algorithm-to-lower-bound missing gate

**2026-11-15 11:03 PST | PNP Machine Model Lead | CIRCUITWIRE050**

**Status.** The Tseitin counting/size lemma below is **PROVED/RESTRICTED** (elementary symbolic proof, independent mathematical review OPEN). The finite exhaustive test is **COMPUTATIONAL**. The October 2026 manuscript statements are **SOURCE-PINNED CLAIMS/FORMALIZATION SCOPE**, not independently rebuilt in this run. Their consequences are **CONDITIONAL on those source theorems**. Williams and Bathie-Williams results are **KNOWN THEOREMS** at the cited scope. Unrestricted Circuit-SAT algorithm and NP-level lower-bound transfer **OPEN**. P versus NP **OPEN**.

## 1. Predeclared candidate and falsifiers

**Candidate.** Translate ANY topologically ordered shared fan-in-two AND/OR/NOT circuit C with n input variables and g>=1 gate identities to a width-at-most-three CNF F_C. Prove the exact #SAT bijection and charge every new wire variable, clause, bit and computation. Substitute the pinned October 2026 #kSAT theorem statements, then test whether their resulting Circuit-SAT algorithm satisfies the all-polynomial-size hypothesis of the Williams algorithm-to-lower-bound theorem. It does not, under this ordinary compiler.

**Falsifiers and controls, specified before source investigation.** (F1) DISJ_k has rank 2^k but an O(k)-gate circuit; any resulting claim that it needs superpolynomial circuits is false. (F2) A g=n^2 shared-gate circuit becomes a CNF with n+g variables under this compiler; a bound subexponential in n+g is not necessarily better than 2^n. (F3) An unconstrained auxiliary variable doubles an exact count; nonfunctional "equisatisfiable" conversions do not preserve #SAT. (F4) Unfolding shared DAGs into formulas can be exponentially costly; do not identify general circuits with tree formulas.

## 2. Corpus, provenance and pinned primary statements

**Authoritative directive first:** research/coordination/2026-11-15_SAT_COMPRESSION_CIRCUITS_FIVE_AGENT_REFOCUS.md, blob SHA 7b8804dc7587abc5134055b5b0d16a143055ca5a. Its Track C supersedes Allender-first, fusion-first and MCSP-first priorities. Read proof1.txt (28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), recovered COMPLETE proof2.txt from authentic blob (1,051,196 characters, SHA 930c5eeddafce656717f28055a7a9a755f44737c), and COMPLETE main.tex from authentic blob (2,545,859 characters, SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34); also AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, current TMR-1..5 handoffs and recent issue #3 entries. Compared the prior TMR-1/049 unique-extension lemma and TMR-5/046 all-balanced-cut Horn expander falsifier; neither supplies the present source-specific circuit encoding/time-budget theorem. Project search found related historical parsimonious Tseitin encodings; this run does NOT claim invention of the standard compiler.

**[1] OpenAI manuscript pinned revision:** openai/math commit 4eaee87548250b2682affda7d05d947c05554bae; manuscript build/main_full_version.tex blob f7af85e623b58e0ca9f4b9416916d442defa963a. For fixed k, the manuscript asserts exact #kSAT in time poly_k(n,m) 2^{O_k(n loglog n/sqrt(log n))}; when m<=Dn for fixed D, it asserts poly(n,m) 2^{O(n/sqrt(log n))}, polynomial space. Its *Lean scope document*, lean/docs/378.md blob 223bbe187394bffca8a2c7ba1656538bfba26e3b, states a formally checked WEAKER poly(L) 2^{O_k(n (loglog n)^2/sqrt(log n))} with polynomial total tape cells visited. ComparatorChallenges/SubexponentialSAT.lean blob a8d5ff3a3e80323675b1f2d1ea611560b783e9ca specifies the Boolean-CNF representation, canonical encoding and counted tape steps. We inspected statements; we did not rebuild Lean or independently certify paper-to-formalization equivalence.

**[2] Anthropic formalization pinned revision:** anthropics/formal-math commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5; eth/MainResults.lean blob 1c62a550fa1e4cbec65bb7112f92ad67589afddc; eth/README.md blob 0b3dcf4a858ff802b3275fc5999ffb134c74de60; eth/Challenge.lean blob 6297ab1398884550253bdd1475704729d02ce89b. The *defined target statement* MainTheorem uses ONE finite-alphabet multi-stack deterministic machine and ONE C for ALL k>=1, n>=4, m>=2, duplicate-free clauses of width <=k and EVERY variable occurring. Exact count output, time <=2^{C min(km/sqrt(lg m), k^2 n lg lg n/sqrt(lg n))}, binary lg. The README reports Lean build and standard axioms; this run did not independently build it. **MainTheorem itself does not assert polynomial space**, unlike the OpenAI Lean scope. The original paper's sharper prose and a claimed build must be kept distinct from the audited statement.

**[3] Williams framework at exact scope:** Vyas and Williams, Theory of Computing Systems 67 (2023), Theorem 1 (informal formulation of Williams 2010/2014): for a suitable circuit class closed under AND, projections and composition, SAT for ALL n^k-size circuits in O(2^n/n^k) for EVERY k implies NEXP lacks polynomial-size circuits of that class. For general fan-in-two Boolean circuits this target is NEXP not contained in P/poly, NOT an NP lower bound. Source: https://link.springer.com/article/10.1007/s00224-022-10106-8 .

**[4] Bathie and Williams:** ITCS 2024, doi:10.4230/LIPIcs.ITCS.2024.10. Their example assumes #SAT on DeMorgan FORMULAS of size n^{2+2epsilon} in 2^{n-n^{1-epsilon} log^k n} and concludes some function in E^NP requires >n^{3+epsilon}-size formulas. This is a formula theorem with a different size regime and E^NP witness class, not an NP-level conclusion. Source: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2024.10 .

## 3. New scoped lemma: fully functional parsimonious wire gate conversion

**Theorem TMR1-050-A (PROVED/RESTRICTED).** Let C be ANY explicitly given n-input, g>=1 gate, topologically ordered, fan-in <=2 AND/OR/NOT circuit; gate outputs may be shared or unused. Its output is the last gate (otherwise first append an identity gate and charge it). There is a uniform deterministic gate-by-gate compiler producing a set CNF F_C on V=n+g declared variables, with m<=3g+n+1 DISTINCT clauses, every clause length <=3, every declared variable occurring, and the following exact equality:
\[
\#F_C=\#\{x\in\{0,1\}^n:C(x)=1\}.
\]
The output has O((n+g) log(n+g)) bits. A word-RAM implementation with O(log(n+g))-bit words and sorting/deduplication performs O((n+g) log(n+g)) word operations; a conservative bit-TM implementation takes poly(n+g) time and O((n+g) log(n+g)) materialized-output/workspace bits. Total serialized CNF bit length L=O((n+g) log(n+g)), plus any representation-dependent fixed parsing overhead. Exactly one satisfying assignment to each internal gate vector extends each input x, whether or not C(x) is accepted.

**Construction.** Assign wire variable z_j to each gate and use the following clauses, where u,v are positive wire IDs (input or earlier gate):
- z=u AND v: (not z OR u), (not z OR v), (z OR not u OR not v).
- z=u OR v: (z OR not u), (z OR not v), (not z OR u OR v).
- z=NOT u: (not z OR not u), (z OR u).
Conjoin a unit clause z_g. Remove duplicate clauses. For an input x_i absent from every generated clause, add the tautology (x_i OR not x_i). These tautologies make all original variables occur without changing the assignment count. The number of clauses is <=3g+1+n, and each auxiliary z_j occurs in its own defining clauses, so all V variables occur. If g>=1, the gate equivalences plus the output clause give m>=2 after deduplication. By induction over gate order each x has precisely one vector z satisfying all equivalences; imposing z_g=1 gives a unique extension iff C(x)=1. No unconstrained auxiliary witness is ever introduced. Duplicates are removed because Anthropic's IsKCNF requires CNF.Nodup. The gate input may be shared repeatedly; each distinct gate identity is allocated ONCE. This proves the theorem.

**Encoded input measure.** Under Anthropic's explicit encoding, k=3 is unary followed by V in unary and 3 literal slots per clause of B=floor(lg(2V))+1 bits, so L_A=4+(V+1)+3m B=O(V log V). The n original source variables and V counted variables are NOT interchangeable. Output length is V+1 bits, of which the high V-n bits are zero by uniqueness. The interface must read and convert those bits; it is counted in the polynomial front/end cost.

## 4. Proven resource transfer, conditional on the pinned source algorithm

Let m<=3g+n+1, V=n+g, k=3. Applying Anthropic MainTheorem to this genuine valid encoding after materializing F_C gives one algorithm for exact #Circuit-SAT with:
\[
T_{\rm AN}(n,g)\le\operatorname{poly}(n+g)+
2^{C\min\{3m/\sqrt{\lg m},\;9V\,\lg\lg V/\sqrt{\lg V}\}},
\qquad S_{\rm AN}(n,g)\le T_{\rm AN}(n,g)+O(V\log V).
\]
The displayed S bound is only the trivial deterministic machine time-to-space bound, NOT a polynomial-space certification from that Lean theorem. For each fixed 0<=alpha<1/2, if g<=n(lg n)^alpha, then m,V=O(n(lg n)^alpha) and the FIRST exponent is O(n(lg n)^{alpha-1/2})=o(n). Thus, *conditional on the formalized counting statement*, this exact compiler gives a UNIFORM 2^{o(n)} #Circuit-SAT algorithm for fan-in-two general circuits with <=n(lg n)^alpha gates. It includes all sharing in that gate range, and it excludes arbitrary polynomial g=n^k, k>1. The result is a transfer of an upper bound, not an unconditional circuit lower bound.

The OpenAI formalized WEAKER scope (source [1]) independently gives, for the same CNF encoding, T=poly(V)2^{O(V(lg lg V)^2/sqrt(lg V))} and S=poly(V). It also gives 2^{o(n)} for all fixed alpha<1/2 (but for a more general growing g its sufficient condition is g=o(n sqrt(lg n)/(lg lg n)^2)). This uses the documented Lean scope, NOT the unformalized sparse-clause improvement. The manuscript's faster sparse m<=4V assertion would instead yield poly(V)2^{O(V/sqrt(log V))} with polynomial space, subject to its source-status caveat.

**Wire-tax falsifier.** For g=n^2 in the *same specified compiler*, V=n+n^2 and m=O(n^2). Both source formulas yield only a generic upper bound of the form 2^{O(n^2/sqrt(log n))} (up to loglog factors), which is NOT certified to be o(2^n). This does not prove a lower bound on the actual algorithm; it proves the cited upper bound plus this compiler does NOT meet the input-n Williams premise. Padding the number of COUNTED CNF variables is not a legitimate way to reinterpret n in the target circuit theorem.

**Exact conditional missing bridge.** To use the general-circuit Williams theorem, for every integer k>0 we need an all-input correct uniform Circuit-SAT procedure on n ORIGINAL input variables and g<=n^k gates satisfying T_k(n)<=O(2^n/n^k), after counting construction, wire/auxiliary handling and all bit operations. One sufficient new ingredient would be a UNIFORM parsimonious compiler with polynomial-time construction and V(n,n^k)=o(n sqrt(log n)/(loglog n)^2) counted variables for each k, plus at most polynomial(n) serialized length; then the published weaker OpenAI Lean statement would yield T_k(n)=2^{o(n)}, hence the needed time savings. Such a compiler is **OPEN**; nothing here says it exists. It cannot be inferred by deleting functional gate witnesses, and it must still compute correct exact counts. The actual *weakest resource inequality* is log_2 T_compile(n,n^k)+E_source(V,m,L)<=n-k lg n-O(1), uniformly for every k, where E_source includes the source theorem exponent, encoded-input length overhead, count output, arithmetic and all calls. There is no matching inequality for the ordinary V=n+g compiler when g=n^2.

## 5. Four mandatory gates and same-realization ledger

| Gate | Status | Audit |
| --- | --- | --- |
| 1. DISJ sanity | **PASS** for this scoped upper-bound lemma | DISJ_k has rank 2^k across its x/y cut, but an O(k)-gate shared circuit and an O(k)-gate Tseitin CNF. The experiment checks DISJ_1..3, with exactly 3^k satisfying inputs. NO static-rank lower bound asserted. TMR-5/046 additionally falsifies even all-balanced-cut rank on easy Horn expander CNFs. |
| 2. Relativization | **PASS** for compiler/count bijection; **OPEN** for unrestricted separation | This purely syntactic bijection can relativize; it claims no P-vs-NP separation. The possible nonrelativizing step in a Williams-style separation would require an actual algorithm for all circuits of the hypothesized nonuniform class with its gate semantics; arbitrary oracle gates cannot simply be expanded into the ordinary compiler. Oracle treatment, algebrization and Natural Proofs implications require separate checks. |
| 3. Simultaneous DTISP | **NOT APPLICABLE** to the Williams circuit implication; **OPEN** for FLMV/Allender reuse | Same materialized converter+counter is used for time and space bookkeeping. OpenAI Lean scope provides polynomial total visited cells, Anthropic MainTheorem by itself provides no polynomial-space conclusion. Neither places one machine inside a forbidden near-linear/sublinear-space DTISP rectangle, and no network span/per-processor substitution is made. |
| 4. Deterministic configuration count | **PASS** as a consistency control | For a total deterministic read-only-input s-space decider on N input bits, T<=2^{O(s+log N)} (for s>=log N, 2^{O(s)}). It is an UPPER bound, not a work lower bound; the actual counting machines are not claimed to violate it. The preprocessor has materialized O(V log V) writable bits; the standard tape-input model can instead account for these as source encodings, with all costs included. |

**Same-realization cost ledger.** (1) Read n input IDs, g gate records and references. (2) Allocate and identify each of g globally shared paid output wires once. (3) Materialize <=3g+n+1 unique width<=3 clauses, with sorting/deduplication, O(V log V) serialized bits and valid AllOccur/Nodup representation. (4) Invoke ONE exact #3SAT machine on V, not n, counted variables, including input access and its true stack/tape steps. (5) Decode V+1 output bits and return the n-input #CircuitSAT count. Materialization alone costs Omega(V) bit operations and Omega(V) writable bits for this explicitly chosen implementation; a different virtual query implementation requires its own charge. There is no claim that every solver must perform this prescribed conversion. Source variables, auxiliary variables, formula length, arithmetic/bit widths and workspace are all distinguished.

## 6. Independent executable evidence and hostile examples

Standalone exact V8 verifier: experiments/tmr/tmr1_tseitin_wiretax050.js. Raw output: results/raw/tmr/2026-11-15_1103_TMR1_TSEITIN_WIRETAX050_V8_RAW.json. Deterministic xorshift32 seed 0x0502026, exact 484 distinct test invocations (480 deterministic pseudo-random AND/OR/NOT circuits with 2..4 original inputs and 1..5 gate identities, DISJ_1..3, one XOR2 composition), **72,528 auxiliary-inclusive assignments enumerated and 3,393 assertions, zero failures**. All formula counts equal the circuit counts, including unused inputs and shared gate dependencies; m bounds, all-occurring vars, duplicate-free clauses and encoding lengths checked. Numerical scale table in raw uses coefficient 1 ONLY to visualize exponent sizes, not the unknown paper constant or an actual SAT execution. No performance claim comes from this finite test.

**Historical guards:** /341 **FAIL** on full accepted language as logical UNSAT authority; /386 **RESTRICTED** guarded odd-charge fragment. Easy Horn, 2-SAT, affine/Gaussian, equality, bounded treewidth, padding, unique-output tensor rank one, compact algebra, arbitrary adaptive solving, caching, rereading and recomputation remain valid cheap controls. DISJ falsifies raw rank as cost. The TMR-5/046 expander/Horn all-balanced-cut result is a sharper additional control. No invented CEGAR exclusion.

## 7. Dependency ledger and next lemma

| Arrow | Status | Required |
| --- | --- | --- |
| Shared circuit -> correct parsimonious width<=3 CNF, V=n+g | **PROVED/RESTRICTED** | Exact symbolic construction; finite COMPUTATIONAL check |
| Pin manuscript/Lean result and separate their complexity scopes | **VERIFIED SOURCE STATEMENTS** | Commits and blob SHAs above; independent Lean rebuild NOT performed |
| Source counting algorithm -> uniform subexp counting for g<=n log^alpha n, alpha<1/2 | **CONDITIONAL** on cited source theorem | Fully charged converter and count output; proper source preconditions |
| Ordinary compiler -> n^k-size Circuit-SAT satisfying Williams for every k | **FAIL / FALSIFIED AS A CLAIM ABOUT THIS BOUND** | g=n^2 wire tax already prevents certification |
| Stronger count-preserving compiler or direct poly-size Circuit-SAT savings | **OPEN** | Uniformity, all k, actual time and bit costs |
| Williams theorem -> NEXP not in P/poly upon all-k premise | **KNOWN THEOREM** | NEXP target, not NP |
| Bathie-Williams formula savings -> an E^NP formula lower bound | **KNOWN THEOREM, HYPOTHESIS NOT MET HERE** | DeMorgan formula class and n^{2+2epsilon} size |
| Any NP-level unrestricted circuit lower bound or P!=NP | **OPEN** | Explicit new nonrelativizing proof bridge |

**One next lemma for TMR-2/3/4/5:** either construct and verify a uniform size-n^k, original-n-input exact Circuit-SAT compressor whose fully charged CNF variable count and machine time pass the above Williams inequality FOR EVERY k, or prove a precise restricted-model obstruction to that compiler without claiming one for arbitrary circuits. TMR-2 should test dynamic multi-cut decompositions with DISJ/Horn controls; TMR-3 must couple compression discovery and actual evaluator time/space; TMR-4 must account for sharing and wire identities under any alternative encoding; TMR-5 should reproduce the source-scope/encoding count and challenge any NP-target promotion.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No edits to root proof1.txt, proof2.txt, main.tex, no new agents or schedule mutations. P versus NP remains OPEN.

## Sources

[1] https://github.com/openai/math/tree/4eaee87548250b2682affda7d05d947c05554bae/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026 ; https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/lean/docs/378.md

[2] https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth/MainResults.lean

[3] https://link.springer.com/article/10.1007/s00224-022-10106-8

[4] https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2024.10
