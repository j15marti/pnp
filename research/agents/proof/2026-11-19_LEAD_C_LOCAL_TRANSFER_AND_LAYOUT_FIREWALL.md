# Strict-C proof lead: local transfer and layout firewall
2026-11-19, America/Los_Angeles. P versus NP remains OPEN. Labels: PROVED (model-specific/structural); COMPUTATIONAL (finite tests); CONDITIONAL (promise transfer); FALSIFIED (automatic layout).

## Single strongest resource-preserving bridge
Prior repository report `research/agents/proof/2026-11-19_LOCAL3COL_C_SOURCE_ACCESS_RESOURCE_FIREWALL.md` supplies a source-local fixed-width indexed 3-SAT to strict-C compiler, with exactly 15+9v+39m named variables and 10+7v+31m strict-C clauses. Its per-clause index uses O(1) original literal reads and O(log(v+m)) work bits; Boolean SAT witnesses extend to complete C assignments, which project back. Source is strict directed-cycle T5, R(a,b) iff (b-a) mod5 in {1,3}, C triangle 30/125; not historical Q/P/S.

**Missing literature gate:** Williams, *Inductive Time-Space Lower Bounds for SAT and Related Problems* (2006), Theorem 2.1 and Corollary 2.3, explicitly establish NQL completeness of SAT with each reduction output bit locally computable in polylog time and log work space, and list 3-SAT among efficient targets. The locally indexed 3SAT->C compiler composes with this. A random-access C input bit can be generated on demand, retaining the original source as read-only input and O(log n) extra work bits, without materializing the C instance. Encoded C length is n^{1+o(1)} under fixed-width or standard local indexed bit encodings.

Buss and Williams, *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds* (2015), Figures 8.2/8.3, provide a deterministic random-access SAT refutation at DTISP(n^1.34070,n^.5), using 44 search rounds/406 intermediate triples. Therefore a uniform total unrestricted strict-C algorithm using N^1.33+o(1) time and N^.5+o(1) writable space in this model, including all source access and verification, would contradict the established lower bound. This is NOT a P != NP proof and does not transfer to critical/growing-girth promises.

**One-sided clocking lemma (PROVED):** For deterministic A with never-false UNSAT output and guaranteed correct UNSAT output for *every* UNSAT input by a known uniform bound T(N), simulate A for T(N) steps and return SAT when it fails to refute. This is a total decider. The dual holds for sound SAT-witness specialists guaranteed on all SAT inputs. All verification and any required clock are charged. Wrong paths and supplied advice are not free.

## New structural falsifier: unrestricted C does not automatically fit small shared-row blocks
For every k>=6 form G_k=K_{k,k} plus a K6 among six left-side vertices. Give each graph edge {u,v} a fresh private head h_e and strict-C clause C(h_e,u,v). This is UNSAT (forces proper five-coloring of K6), has 2k+k²+15 C variables and k²+15 strict C clauses, all with three distinct variable names. It is not clause-critical and has an easy K6 certificate.

Let z be ANY s<k fixed C variables. The remaining bipartite endpoints stay connected; at least 2(k-s) endpoints and (k-s)^2-s surviving private heads are in one private component. Thus the largest private component is >=2(k-s)+(k-s)^2-s. For s=O(log k) this is Omega(k²)=Omega(N/log N), where explicit source N=Theta(k²log k) bits. If every shared assignment is an explicitly listed row, 5^s<=N^.195 forces s<=.195 log_5 N. The required max N^.35-private-size decomposition is therefore impossible for these unrestricted sources by simply assigning each original clause to a private block. This does not exclude paid symbolic aggregation, alternate encodings, or a restricted promise.

## New executed controls
Fresh standard-library script seed 2026111902. Exhaustive 125 C value triples (30 accepted) and 25 private-head projection pairs; independent indexed/direct compilers matched 35,747 edges across 240 new small 3-CNFs. Of those, 232 Boolean-SAT cases had full verified C witnesses covering 34,395 original strict-C checks; eight Boolean-UNSAT cases were not independently C-DFS refuted. Structural test: 1,200 seeded z subsets of sizes 0..3 for k=8,12,16; all private components passed the proven lower bound. Largest private component minima for k=8 by s=0/1/2/3 were 95/94/92/91, for k=12 183/182/180/179, for k=16 303/302/300/299. Executed script SHA256 73c3a5cec63fd90a93a0a65c84deb33eeff0891f71666f8f332cf4869c401b63, JSON SHA256 c2acd7e291434a173aafb3b9d1c0a0b5bb4facc31bb7e398be78ace0e5ac70a8. Python tracemalloc peak 145,852 bytes is NOT a formal RAM space bound. Independent prior script SHA256 95dde7d7a82743a54b1d7b70bd12043ea7dbb55dfd816648ad0c73d37473145d checked locally.

## Resource ledger and next blocker
For explicit R<=N^.195 rows, B<=N^.65 blocks, child size <=N^.35, full sequential calls with local m^a child time cost N^.845+.35a, plus source generation/materialization potentially N^1.195, all failed calls, read-only vs writable buffers, replay, verification, complete output. N^1.33 requires a<=97/70; local space m^s requires s<=10/7 before other live workspace. An unspecified polynomial SAT seed does not imply these exponents.

CONDITIONAL: if any restricted critical/girth C family were a locally encoded near-linear complete target for arbitrary 3SAT, the source-local lower bound could transfer, but NO such compiler is established. OPEN: a paid total grammar reduction and symbolic UNSAT obstruction covers for all z. Independent peer review pending. No agent schedule, enabled state, or manuscript ownership changed.

Sources:
1. Williams (2006), https://www.cs.cmu.edu/~ryanw/sat-journal-final.pdf; DOI 10.1007/s00037-007-0221-1.
2. Buss & Williams (2015), https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf; DOI 10.1007/s00037-015-0104-9.
3. User Library t5_strict_research.pdf, pages 1-3, read this run; confirms C/S relation discipline and nonparsimonious gadget limits.
4. Full source, ledger, raw outcomes, hash manifest in current-run package T5C_Proof_Lead_Local_Transfer_Firewall_20261119.zip; script not committed here.
