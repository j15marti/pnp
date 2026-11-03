# LSPV-4 / PNP Time-Space Resource Auditor: BPHP Stream-Recognition and Proof-Size/Decision-Work Firewall345
**November 2, 2026, 16:43 PST | General CNF-SAT | PROVED/EXACT model-specific lemma; COMPUTATIONAL finite controls; B3 and P versus NP OPEN.**

## Fixed proof system, target and exact obstruction
Keep the existing, preselected binary-premise, unit-inference-weight Rmix341 (RES, local AND3/conversions, binary XOR, charged conservative DEF). Define W_R(F) as the minimum sum of derived-node weights of a sound shared refutation DAG, with FREE choice of the optimal derivation. Define Wbar_R(N)=max W_R(F) over UNSAT source encodings of at most N bits. The primary B3 bridge (SAT in P implies polynomial Wbar_R for this SAME R) and a superpolynomial Wbar_R lower bound remain OPEN. Neither a restricted proof lower bound nor sampled solver time proves them.

**New proved firewall:** there is a uniform total correct general CNF-SAT decider that recognizes the explicit bit-pigeonhole UNSAT family in O(N polylog N) bit time and O(log N) writable space on exactly matching original byte strings, using a streamed source generator. It invokes a correct complete exhaustive fallback for everything else, including well-formed SAT and malformed strings. It does not output a proof in a chosen calculus. This is a family upper bound, NOT all-input SAT tractability.

## Authenticated signed CNF family and repair theorem
For h=2^ell holes and h+1 pigeons, use variables x_(i,b), ell bits per pigeon. For every pair i<j and hole c, include one clause C_(i,j,c) asserting that pigeon i or pigeon j differs in at least one bit from c. There are n=(h+1)ell variables, m=h*binom(h+1,2) clauses of width 2ell and L=2ell*m independently signed occurrences. Serialize as ASCII DIMACS with (i,j,c) increasing and pigeon/bit orders fixed, spaces between decimal signed literals and one '0' terminator per clause. The exact bit length is N(h)=Theta(h^3 ell^2).

**Lemma (known project result, independently checked here):** B_h is UNSAT, and flipping ANY one occurrence sign yields exactly (h-1)! models. Proof: the modified formula can be satisfied only by the unique allowed collision of the designated pigeon pair at the designated hole; the remaining h-1 pigeons biject to the other holes, giving exactly (h-1)! assignments.

**Streaming recognizer theorem:** read the short header; enumerate powers h=2,4,8,... and match n,m against the derived parameters. Using O(log N)-bit counters (i,j,c,b,input index and decimal digits), generate the unique expected bytes and compare them one at a time against read-only input, including sign fields and EOF. A complete match certifies UNSAT by pigeonhole and requires O(N) sequential source-byte comparisons, O(N polylog N) bit operations and O(log N) all-phase writable bits on the recognized family; no full CNF or table is written. For nonmatches, run a separately charged full grammar checker and exhaustive general SAT solver, which ensures total correctness but can take exponential time and linear writable space. This model proof is independent of the Python host implementation, which materializes clauses and is NOT a native FLMV trace.

**Conditional proof-system corollary:** Braun's September 19, 2026 arXiv:2609.23015 *reports* >exp(h/(32768 ell^2)) nodes (including sources) for arbitrary DAG-like Res(XOR) B_h refutations when ell>=32. Subtracting m=poly(h) source nodes leaves superpolynomial derived proof cost in the stated restricted calculus. The fast recognizer therefore contradicts B1 for that R, conditional on the author's theorem and exact calculus/encoding alignment. The author's claimed Lean verification was NOT independently rerun. Crucially this does NOT prove hardness for DEF-enabled Rmix341 or refute worst-case B2/B3.

## Paid finite solver/source atlas
A Python producer, independently written no-import JavaScript verifier, and separate constructive-witness checker were executed. The JS verifier passed **19,515 assertions**, including 172 exhaustively model-counted sign flips on h=2,4; the witness checker validated all 1,728 source-sign repairs on h=8 and 24 representative controls on h=16. All sources have stable SHA256 hashes and exact signed-variable matrices. Eight malformed source encodings rejected.

| h | Variables n | Clauses m | DIMACS bytes | UP-DPLL nodes | Literal inspections | UP-DPLL status |
|---:|---:|---:|---:|---:|---:|---|
| 2 | 3 | 6 | 52 | 3 | 29 | UNSAT |
| 4 | 10 | 40 | 508 | 151 | 15,100 | UNSAT |
| 8 | 27 | 288 | 6,061 | 50,000 | 30,930,878 | UNRESOLVED, 50k cap |
| 16 | 68 | 2,176 | 62,990 | 500 | 2,261,625 | UNRESOLVED, 500 cap |

Exact model counts for h=2,4 are 0 and 0; after one signed flip they are 1 and 6. On all four exact BPHP originals the streamed recognizer compares exactly 52,508,6061,62990 bytes. Different fixed solver policies produce different resource trajectories on the SAME signed original. A capped DPLL trace is not a UNSAT proof or universal lower bound. Host operation counters cannot be transferred into a native FLMV forbidden region.

Hostile paired controls: K4 odd/even Tseitin have 0/8 models and 15/4 UP-DPLL nodes; Horn chain UNSAT/SAT 0/1 models and 1/1 nodes; 2SAT UNSAT/SAT 0/1 models and 3/3 nodes. Eight malformed source encodings rejected. Parity/GF(2), compact circuits, extension definitions, variable renamings, source-copy and streaming alternatives remain required escape controls.

## All-phase resources and bridge firewall
For a materialized-child construction retain s'<=max(rho,eta,lambda,lambda*s), with rho the peak over ALL local phases. An N-bit writable input copy, even transient, has rho>=1; the theoretical streaming recognizer uses only logarithmic writable space on its matched family, but its implemented Python producer does not. Any general fallback incurs separately charged time, source/index/head, parsing, failed tests, cache, output, proof validation and peak writable space.

B1 is pointwise W_R(F)<=p_A(N+T_A(F)). B2 instead uses T_A^wc(N), maximum over ALL strings of length <=N. B3 only asserts SAT in P implies polynomial Wbar_R for preselected R. The exhibited A_stream has potentially exponential worst-case fallback. Hence neither B2 nor B3 is refuted by its fast family. Braun's restricted Res(XOR) theorem does not transfer across a change of R; the fixed combined Rmix341 remains without a superpolynomial lower bound.

## Literature, duplicate audit and next gap
Read shared 12:04 and new 16:00 five-role handoffs, active issue #3, AGENTS.md, CODEX.md, repo pnp-research skill, LSPV-2 BPHP-ATLAS-LOCAL-MACRO345, and LSPV-4 SPACE-CAPPED-PORTFOLIO344. Primary sources searched: Braun 2026 arXiv:2609.23015; Peitl/Szeider IJCAI 2021; Cook/Reckhow JSL 1979; FLMV JACM 2005. Project j15marti/pnp and github.com/openai code searches performed; OpenAI/math returned unrelated SAT formalization resources. LSPV-2 had already proved source clauses' (h-1)! repair property and built exact BPHP sources. **Increment here** is a total correct source-stream recognizer with explicit all-phase workspace proof, coupled with measurements across several fixed solvers. No independent author-Lean replay or native FLMV benchmark was performed.

**Next exact gap:** Establish a growing lower-bound invariant robust to every RES/AND3/XOR/CONVERT/DEF inference of the SAME Rmix341 and independently justify B3. The direct recognizer shows why partial proof models cannot be assumed compulsory. P versus NP remains OPEN.

**Reproducibility:** Full Python producer, no-import Node verifier, independent constructive witness checker, source hashes, raw JSON, source fixtures, LaTeX report and SHA256SUMS reside in the user-facing archive `LSPV4_BPHP_STREAM_TIME_SPACE_ATLAS345_repro.zip`. Repository compact code and public JSON separately reproduce the canonical bytes and independently checked small counts.

**References:** [1] K. Braun, arXiv:2609.23015, September 19, 2026. [2] T. Peitl and S. Szeider, *Finding the Hardest Formulas for Resolution*, IJCAI 2021, https://www.ijcai.org/proceedings/2021/657. [3] S. Cook and R. Reckhow, JSL 44(1), 1979. [4] L. Fortnow et al., JACM 52(6), 2005, DOI 10.1145/1101821.1101822.
