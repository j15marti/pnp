# LSPV-4/499 | Critical polarity-bit SAT sensitivity on original Resolution-hard Tseitin sources
**2026-11-08 10:47 PST | Route A resource auditor | PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

**Tracker:** proposed [P2-L4-499] strengthens the scope of [P2-L4-498], and informs [P2-A4]; [P2-A2] and [P2-A5] remain OPEN. Cross-route [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. No changes to historical R_mix341 rules/weights, role allocation, schedules or enabled state.

## IDEA -> SEARCH -> ITERATE
**Initial falsifiable hypothesis:** the already-authenticated *odd-charge diagonal* of LSPV-2/495, which is UNSAT and ordinary-Resolution-hard on an expanding graph, differs from a SAT instance by flipping ANY one original sign-bit occurrence. This may turn LSPV-4/498's specialized **membership** probe floor into a lower bound for actual general **SAT-vs-UNSAT decision** on valid proper 3-CNF inputs. It would remain only near-linear and would not yield the universal FLMV contradiction.

Predeclared falsifiers: F1, some original clause is not essential; F2, a sign-bit flip is malformed or creates an illegal/duplicate clause; F3, the fixed local wrong-parity pattern does not extend to a satisfying assignment for the remaining graph; F4, an adaptive randomized correct-on-all-inputs algorithm distinguishes all single-sign mutants while querying o(H) positions on the UNSAT diagonal.

**SEARCH:** Recovered the entirety of root proof1.txt and proof2.txt, latest issue #3 comments (including peer LSPV-2/498), governing 2026-11-02 five-role refocus, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, LSPV-4/497-/498, peer LSPV-2/493 and /495-/498, actual GROKPROOF/2026-11-08_1130_PROGRESS.md (blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70), Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67), and the current source files in the external corpus. **Important duplication caught:** LSPV-2/493 already establishes clause essentiality, relying on LSPV-4/488. This report does NOT claim that fact as new. The refined output is its direct general-SAT input-query implication, explicitly distinct from specialized family recognition.

Exact external repository reads (Git blobs): konard/p-vs-np README.md 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 (only finite-machine P subset NP); blkph0x/p-vs-np-proof-research METHOD_INDEX.md 18d693ea71dfa433370eb7afbebc3106e32f03e5 (scoped claims); MassimoLauria/cnfgen cnfgen/families/tseitin.py 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (original parity generator); meelgroup/frat-xor format.md 986a21aa92b62f844ef1fce852193142c41b2b1f (different XOR proof grammar); openai/math README.md cc5b0a03bca6c742f045d683b6647a6f44ef2cae (nonuniform formalization scope); pysathq/pysat README.rst fefde10b1426a92a21425029892f3f49466bf03c (solver framework). Primary literature: Urquhart (JACM 1987) and Ben-Sasson/Wigderson (JACM 2001) for ordinary Resolution; Viola/Wigderson, *Local Expanders* (Computational Complexity 2018) for an explicit infinite cubic bipartite Ramanujan family; FLMV (JACM 2005) for a DIFFERENT machine/time-space theorem. The ECCC public abstract was consulted for Local Expanders; no full PDF proof was independently checked. No separately authenticated Google-branded search. No third-party repository proves the missing universal contraction.

## Exact source/theorem/model/known shortcut/remaining-transfer ledger
Let G=(V,E) be a connected SIMPLE cubic bipartite graph, H=|V| even, with fixed odd-total charge vector chi. The *original* Tseitin source uses one propositional edge variable per edge and, for each vertex v, its four distinct proper 3-clauses that forbid the four 3-bit patterns whose XOR is not chi_v. Thus there are 4H original clauses and 12H signed-literal records. With the existing LSPV-2/495 fixed fields (magic 11100011, unary H and 2H, sign bit plus W-bit variable ID in every signed literal, trailer 10),

$$
W=\lceil\log_2(2H+1)\rceil,\qquad N=3H+12+12H(W+1).
$$

For the diagonal a=b of LSPV-2/495, every original matching pair denotes the SAME Boolean variable, and the source is simply the classical odd-charge Tseitin contradiction after a variable bijection. On the **specific explicit expanding family** from peer LSPV-2/498, the published ordinary shared-DAG Resolution lower bound transfers under the bijective renaming, of size 2^{Omega(H)}. This is NOT a lower bound for all mixed R_mix341 rules, Extended Resolution, GF(2), or arbitrary SAT machines. Known shortest-route upper controls are GF(2) parity summation, extension variables, ordinary solvers with algebraic preprocessing, and LSPV-4/497 + LSPV-2/498 native-indexed family recognizers; no shortcut is disallowed.

## Theorem 499.1: every original polarity bit is SAT-critical (PROVED/RESTRICTED)
Let F be the above odd-charge ORIGINAL 4H-clause source. For every clause C and each of its three literal occurrences, flip just the corresponding polarity bit in F's binary source, yielding F^(C,i). Then:

$$
F\in\mathrm{UNSAT},\quad F^{(C,i)}\in\mathrm{SAT},\quad
F^{(C,i)}\text{ is still a proper duplicate-free 3-CNF of the same }N\text{ bits}.
$$

**Proof.** In a connected 3-regular bipartite graph, no edge is a bridge: a component separated by a bridge would require 3(|L'|-|R'|)=+/-1, impossible. A degree-three bridgeless connected graph has no cut vertex, because some component of G-v would attach through only one incident edge, a bridge. Fix any v and any one of its four wrong-parity local patterns z. Since G-v is connected, the remaining vertex-edge incidence equations have rank H-2 and are consistent after fixing the three v-incident edges to z. The only global residual consistency condition is XOR_{u != v}chi_u = XOR(z), and both sides equal chi_v XOR 1 by odd total charge and the definition of z. An assignment therefore satisfies every vertex parity except v, where it realizes exactly z. It falsifies precisely the unique clause C_{v,z} among the four at v. Consequently F\{C_{v,z}} has a witness. Flipping any one sign of C_{v,z} changes its only forbidden local pattern by one bit, making the same witness satisfy the flipped clause as well. All untouched clauses stay satisfied. Variable IDs and the width-three structure are unmodified. The flipped sign pattern has the opposite parity and thus cannot duplicate any of the remaining three clauses at that vertex; other vertices have different incident-edge supports because G is simple and cubic. QED.

**Corollary 499.2: genuine SAT bit-probe lower bound.** Let A be an adaptive randomized decision algorithm that is correct with worst-case error at most epsilon<1/2 on *every valid proper 3-CNF*, in the exact declared bit-source grammar, and let Q_A(F) count distinct queried INPUT bit positions on the above original UNSAT F. For each of the 12H polarity positions i, couple A's random coins on F and SAT-mutant F^i. The outputs can differ only if i is queried along the run on F. Since their correct labels differ,

$$
\Pr[i\text{ read on }F]\ \ge\ 1-2\varepsilon.
$$

Summing these 12H disjoint query events gives:

$$
\boxed{\mathbb E[Q_A(F)]\ge(1-2\varepsilon)\,12H
=\Omega(N/\log N).}
$$

For exact deterministic or zero-error randomized correctness, all 12H positions must be queried on F (in every halting random run that is correct on both compared inputs). At epsilon=1/3, the bound is 4H distinct expected queries. This is a source-bit **decision** lower bound, not merely source-family membership authentication. It holds for the actual UNSAT diagonal when the decider's domain includes its SAT neighbors. It does not claim Omega(N) or polynomial exponent greater than one for SAT.

**Machine qualification:** One indexed input-bit query costs at least one physical operation in any ordinary explicit-source bit-probe implementation. Deriving precise FLMV machine time for an arbitrary input encoding or simulator requires independently paid representation conversion, INDEX/head, guest-interpreter and all-input obligations; the present theorem is ONLY for the declared fixed-field source and access model.

## COMPUTATIONAL original-source controls
A newly written Python source+GF(2) witness constructor independently authenticated the FIRST odd diagonal bits against peer LSPV-2/495 SHA-256 on K3,3, Q3 and Heawood: K33 5dc81af61477fdf2e4f9e3c72135ce0489dea80c6873868f6d0bd6d9ef882ef8, Q3 80b0e7b161e48d81f4b477770a162130f325a87b95fbe739864d7046b2f3a7a1, HEAWOOD 2c098df7e943ad86450c3929ff0d9325f93935cabbde59cdc1ba7d9c839630c0. All 72+96+168=336 single sign-flip mutants retained proper strict 3-CNF and had independently constructed full SAT assignments. Python reports 2,361 weighted check credits (not an exact count of Python assert-call executions). A separately implemented Node.js fixed-grammar parser checked all 336 source-bit mutations, exact logical clause changes and every supplied witness with 105,313 assertions; an additional self-contained JS brute SAT implementation checked all 168 sign mutants on K3,3 and Q3 with 374 assertions. All tests PASS; zero failures. A hostile header-bit mutation fails grammar. Original odd-charge unsatisfiability was checked by GF(2) inconsistent-rank certificate, NOT by a native R_mix341 checker. The exact Python/JS/witness reproducer is available as a conversation archive; GitHub standalone code and summary are also published.

## Resource ledger and limitations
**Lower bound:** distinct source-bit probes >=(1-2epsilon)12H in expectation; each probe includes an indexed read at cost >=1. No nontrivial WORK high-water lower bound is inferred. **Experiment:** the Python witness-generation stage uses host-language integer arithmetic, input construction O(H log H) bits, GF(2) equation assembly and Gaussian elimination (crude O(H^3) arithmetic operations and O(H^2) bits, excluding host overhead), 336 independent witnesses and 40,404 bytes of explicit verification evidence for the three tested graphs. JavaScript parsing and witness checking likewise use ordinary host memory, NOT native indexed FLMV high-water accounting. **Compiler context:** a hypothetical solver-dependent transformation can generate and trust its own children; the bit-probe bound on independently supplied adversarial SOURCE inputs does not charge reauthentication of compiler-owned children. No general source contraction, worst-case machine-time exponent >1, noncircular B3, or all-rule mixed-calculus lower bound follows.

**ITERATE:** F1 was already discharged by peer LSPV-2/493; F2/F3 were discharged by the explicit GF(2) witness and independent valid-source tests; F4 is excluded by the coin-coupling proof within its declared input-query model. The genuine new distinction relative to /498 is testing SAT versus UNSAT on **syntactically valid** formulas, rather than exact membership in one patterned source family. The gap stays OPEN: [P2-A2] uniform all-input solver-dependent transformation and [P2-A5] fully charged recursive same-machine applicability. Existing five agents, allocations, historical rule weights and statuses remain unchanged.

### References
[1] Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), 209-219, doi:10.1145/7531.8928.
[2] Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM 48 (2001), 149-169, doi:10.1145/375827.375835.
[3] Viola and Wigderson, *Local Expanders*, Computational Complexity 27 (2018), 225-244, https://eccc.weizmann.ac.il/report/2016/129/ (public abstract, no PDF proof replay).
[4] Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005), 835-865, doi:10.1145/1101821.1101822.
[5] j15marti/pnp, peer LSPV-2/493 original-clause essentiality, /495 exact binary source, /498 locally explicit expanding generator, and LSPV-4/498 authentication bound.
