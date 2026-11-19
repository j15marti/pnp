# LSPV-2: Exact-one T5 source-aware circuits and critical-deletion batching
Date: 2026-11-18, America/Los_Angeles. Owner: LSPV-2 SAT-CIRCUIT REDUCTION BUILDER, Route A.
**PROVED/RESTRICTED + COMPUTATIONALLY VERIFIED. P versus NP OPEN.**

## Candidate and falsifiers
Build one source-authenticated fan-in-two AND/OR/NOT DAG for Q(h,u,v)=R(h,u) XOR R(h,v), with five one-hot color pins per named variable, reused directed comparison gates, and an eight-bit deleted-clause selector for the 283-variable, 236-clause intrinsically critical source. Attempt to falsify: (1) all-125-table correctness or malformed one-hot rejection; (2) per-head parity forest equivalence; (3) wrong-deletion acceptance; (4) gains disappearing when physical netlist/CNF bytes and actual witness checks are counted.

## PROVED: parity-forest normalization
For a fixed first variable h, let w_h(v)=R(h,v), where a tie is a nonwin. Each Q(h,u,v) says w_h(u) XOR w_h(v)=1. An odd cycle in the graph of tail-pairs proves UNSAT. If all head-specific graphs are bipartite, retaining any spanning forest per head preserves **the Boolean truth of the whole Q formula for every actual five-letter assignment**, not just SAT-equivalence: omitted edge equations follow by XOR along forest paths. Consequently a clause-minimal UNSAT Q formula that passes per-head parity has **a forest at every head**. If a minimal source has any odd head-cycle, the source consists exactly of such a cycle.

Independent four-variable 2^12 enumeration: 1,976 SAT, 2,120 UNSAT, 76 inclusion-minimal UNSAT, four odd-cycle minimal instances, 72 parity-feasible forest minimal instances. The 283-variable critical fixture has 236 private heads and no parity redundancy. Its 47-vertex graph has 236 edges and zero triangles, yet is six-chromatic by its Mycielski source construction. Parity, forest and simple K6-clique tests cannot decide it.

## PROVED: source-aware Boolean and CNF interface
For each variable v create five Boolean color bits with an exact-one check. Define t[v,a]=x[v,a+1] OR x[v,a+3] (indices mod 5) and W[h,v]=OR_a(x[h,a] AND t[v,a]). This computes the specified directed tournament including R(a,a)=false. Q=W[h,u] XOR W[h,v] uses the explicit four-gate (a OR b) AND NOT(a AND b); old P=W[h,u] AND W[h,v] uses one gate. The complete output ANDs original constraints with exact-one validation. Tseitin encoding charges 3 clauses per AND/OR, 2 per NOT and 1 positive output unit, with each internal gate uniquely determined by inputs. This is a SAT **candidate verifier**, not a witness-generation algorithm.

For original clauses C_0..C_235 and eight-bit index e, compute s_i=[e=i] and V(e)=OR_{i<236}s_i. Output ONEHOT(colors) AND V(e) AND AND_i(s_i OR Q(C_i,colors)). For each valid index e, this is exactly the truth of H minus source clause e; all 20 invalid indices 236..255 reject. The true source is retained and no answer-status bits are admitted.

## COMPUTATIONAL: gate counts and real materialization
| Source | Naive Q gates | Shared Q gates | Shared old P gates | Shared Q depth |
| --- | ---: | ---: | ---: | ---: |
| One clause, 3 variables | 93 | 83 | 80 | 10 |
| Five-clause parity-feasible UNSAT | 282 | 184 | 169 | 12 |
| Critical fixture, 283 variables/236 clauses | 14,958 | 10,473 | 9,765 | 17 |
| Critical deletion, 235 retained clauses | 14,915 | 10,450 | 9,745 | 17 |

All 125 value triples and all 32,768 raw one-hot pin patterns were independently checked for the one-clause Q/P circuits: 60 Q successes, 20 disjoint P successes, and 32,643 malformed patterns rejected by each. A broader 25-source grid comprised 14,877 assignment-by-variant tests with zero mismatches; input scopes/seeds and raw data are in the reproducibility archive.

| Resource | 236-way shared circuit | All 236 separate source-deletion circuits |
| --- | ---: | ---: |
| Gate records | **11,236** | **2,466,200** |
| Actual materialized DIMACS bytes | **480,887** | **104,252,286** |

The shared circuit has 5,898 AND, 3,962 OR, 1,376 NOT gates, depth 18, 1,423 input pins including eight selector bits, 32,333 functional Tseitin clauses, and 569 max simultaneously live intermediate values under an explicit last-use replay model. Physical CNF size saving is **216.79-fold**. All 236 individual CNFs were actually emitted and measured to temporary files, not extrapolated. The batch build took 0.084 s, its CNF emission 0.016 s and replay of all positive/wrong/out-of-range controls 0.856 s; these are finite Python timings, not asymptotic bounds. Independent replay accepted 236 supplied deletion witnesses, rejected 236 wrong-deletion selectors and 20 invalid indices, and checked all 32,333 clauses of the batched DIMACS under one true witness. The source fixture SHA-256 is f119902fbdbc6f9d9fce407287ccda75878849e0b9c627845d689beb934fcb12.

## Resource and proof-chain limits
The zipped original experiment evidence was 327,824 bytes; the raw fixture was 151,017 bytes; the batched JSON netlist was 196,992 bytes. The 569 last-use gate values exclude 1,423 pinned input bits, the read-only netlist, source acquisition and actual Python RSS. Verification of all 236 complete witnesses requires repeated input reads and circuit evaluations; *constructing* 236 witnesses requires outputting at least 66,788 five-valued symbols and still needs a correct search method. These witnesses came from the supplied experimental archive, not from the compiler. Sound per-head parity rejection is a one-sided UNSAT specialist: return UNSAT only with a checked odd-cycle certificate; otherwise UNKNOWN. It does not cover arbitrary CNF, all z-rows, or the proposed n^1.33 time/square-root-space specialist. A supplied favorable nondeterministic path is not deterministic search or a source-bound UNSAT certificate. Published SAT RAM time-space exclusions are model-specific and do not transfer to these gate counts.

Full exact original source, executable compilers, independent replayers, 236 individual CNF byte logs, serialized batched netlist and CNF, all raw results, and SHA-256 manifest are in **LSPV2_T5_Q_EXACT_ONE_BATCH_CIRCUITS_20261118.zip**, generated in the originating conversation. No automation state, tracker or root main.tex was modified.

References: Original user-supplied **T5_Exact_One_Experiments_2026-11-18.zip**; Garey, Johnson, Stockmeyer (1976), https://doi.org/10.1016/0304-3975(76)90059-1; Mycielski (1955), https://doi.org/10.4064/cm-3-2-161-162; FLMV (2005), https://doi.org/10.1145/1101821.1101822; Williams (2006), https://doi.org/10.1007/s00037-007-0221-1.