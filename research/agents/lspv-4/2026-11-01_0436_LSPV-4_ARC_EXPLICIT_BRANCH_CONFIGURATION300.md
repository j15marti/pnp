# LSPV-4: ARC-EXPLICIT-BRANCH-CONFIGURATION300
**November 1, 2026, 04:36 PST.** PROVED/EXACT restricted explicit-output transducer result (independent referee pending); COMPUTATIONAL independent original-source checks; CONDITIONAL FLMV transport. **P versus NP OPEN.**

## Source, inherited facts and priority
The sole complete NP-complete target remains all valid duplicate-free proper Döcker monotone 3-SAT-(2,2) originals, with three distinct same-sign literals in each source clause, each variable exactly twice per polarity, no duplicate clauses, and malformed-input rejection. The 01:48 five-role handoff and 01:44 SATURATED-CYCLE-AFFINE-TERMINAL1 were read first. Noncanonical GF(2) children cannot serve as target-valid hereditary descendants without a separate paid reencoder. Earlier LSPV-4 ARC-INDEXED-CERTIFICATE-AUDIT297 already established the explicitly enumerated branch **output-time** lower bound, and low-space verification of supplied row-XOR proofs; LSPV-4 LOCAL-MUTUAL-MIN299 gave an O(m^2 polylog N) source-authenticated low-space selector. The current incremental result is a **fixed-work-tape configuration-counting** consequence for the specific explicit-output protocol, plus detailed indexed source-bit access ledger. This is standard machine-configuration counting, not novel general SAT hardness.

## Restricted theorem and proof
Let F9 be the valid 9-variable/12-clause canonical source with positive triples (156),(238),(135),(469),(247),(789) and negative triples negating (468),(167),(234),(358),(129),(579). The complete F9 has exactly 70 satisfying assignments. Pin x8=x3=x7=x6=0, x1=x5=1. All eight completions are UNSAT. Its uncovered original IDs are 1,3,4,5,10 (zero based); signed budget (f,u,eta,nu,delta)=(3,5,0,1,0), and certified binary triangle (3,4,10). The signed preferred values and outside-cycle parity force x2=x4=x9=1, but all three selected doubly-true edge alternatives are contradictory. Parity-only SAT inference fails.

Let F_t consist of t variable-disjoint renamed F9 copies with copied six-pin UNSAT cubes. Every full source F_t is valid target input, with n=9t, m=12t, f=3t, nu=t, delta=0. It has **3^t syntactically distinct selected-edge vectors**, all inconsistent. Under the declared fixed-width original encoding, B=ceil(log2(9t+1)), H=ceil(log2(12t+1)), and N_t=2H+36t(B+1)=Theta(t log t).

**Theorem.** Fix a deterministic halting indexed-read-only-input / write-only-output TM with Q control states, r fixed writable/index tapes of constant alphabet q, and a source input head confined to N_t+2 positions. Require its **output protocol** to emit a distinct constant-alphabet record for **every** selected-edge vector before halting. If S bounds the greatest visited writable/index tape extent, then

    3^t <= Q (N_t+2)(S+2)^r q^[r(S+1)].

Consequently **T >= 3^t** output steps and **S = Omega(t) = Omega(N_t/log N_t)**. Proof: exclude the unreadable write-only output tape and its position from operational configurations. There are at most the RHS distinct configurations. A repeated operational configuration creates a deterministic endless loop, contradicting halting. Each emitted record needs a distinct time step; taking logarithms yields the space bound.

**Scope:** A componentwise refutation, projection-rank terminal, proof DAG, or compressed output skips this artificial enumeration. The pinned F9 cube solves under matched UP-DPLL in one node. Therefore this is **not an arbitrary-SAT lower bound**. A stored 9t x (3t+1) dense GF2 matrix uses 9t(3t+1) bits; full variable cache 9t bits and two-bit clause counters 24t bits. These are layout choices, not necessary storage for all implementations.

## Indexed machine and physical XOR
A declared fresh address per original source-bit microprotocol writes w=bitlength(N) index cells (including zeroes), traverses 2(w-1) index-head moves, performs one indexed source jump **atomically erasing the index tape**, and reads the source bit. It charges **3w primitive steps per source bit**, excluding computing the address. One whole-source scan costs 3wN. Cumulative adjacent **index tape content** XOR is 2 sum(a<N) popcount(a), and endpoint XOR zero. A naive source-authenticated all-clause-triples scanner reads Q_bits=9(B+1)C(m,3) bits, charging 3w Q_bits primitives, excluding grammar/address arithmetic and guest/policy work. This O(m^3) policy and the previously known O(m^2) selector fail the proposed local N^(11/10) exponent, but **neither is mandatory for every SAT solver**. Prior ARC281 and INDEX-RECHARGE283 already addressed the atomic-erase correction to unqualified T>=D_phys.

| Copies t | Source bits | Full scan primitives | Naive triples primitives | Output records |
|---:|---:|---:|---:|---:|
| 1 | 188 | 4512 | 237600 | 3 |
| 2 | 442 | 11934 | 2950992 | 9 |
| 4 | 1020 | 30600 | 32689440 | 81 |
| 8 | 2318 | 83448 | 370344960 | 6561 |
| 64 | 25364 | 1141380 | 335028545280 | 3^64 |

These are reproducible Python microprotocol counts, **not a whole-machine native FLMV benchmark**. Logical clause XOR, head-position encodings, and source readonly changes are not physical writes. Actual peak guest, proof matrix, parent/ancestor cache, index tapes, output construction and failed policy overhead remain unmeasured.

## Separate SAT-to-Döcker local-bit numeric transport
On a specified **unsorted source-list accessor without inverse index**, deciding whether any of m records has an occurrence requires inspecting all m on an all-NO input. Changing one uninspected record changes that local answer. Thus Q unshared queries require Omega(mQ) source record inspections in this **restricted interface**. The full-parent scan is not N^o(1) multiplicative per-query overhead. An indexed/local alternative may evade the obstruction.

FLMV Theorem 5.7 exact recurrence is f0=1, fk=c fk-1/(1+fk-1), dk=min(((1/fk)-c)/k,c^(-k)). At c=6/5, d*=23/45. At c=241/200, d*=11642479/23232400. Both have unique maximizer k=2; exact k=1/3 comparison plus dk<=c^(-4)<d2 for every k>=4 certifies the infinite tail. For a **hypothetical** target decider jointly within time/space exponents (6/5,1/2), source-to-target expansion exponent b and zero-extra-exponent local bit/read/retained peak costs, strict numerical entry requires **b<min(241/240,11642479/11616200)=11642479/11616200≈1.00226227**. The needed addressed-bit near-unit SAT-to-Döcker reduction is unconstructed; CP22LIFT1 is a **nonmonotone** strict-(2,2) compiler, not a suitable drop-in normalizer. Mere NP-completeness cannot transport FLMV's exact numbers.

## Independent SAT, UNSAT and falsifiers
The self-contained full producer and a separately developed **no-producer-import** verifier passed **1,306 assertions** on F9 SAT70/pinned UNSAT0, Y6 SAT20, valid F_t for t=1..128, all three incompatible cycle choices, original signed occurrence S/U targets, SS/SU/US/UU pair compatibility, complements, endpoint assignments and coherent flips, fixed-bit serializer and physical index XOR, and exact FLMV. The separately rerun previous independent certificate verifier passed **22,440 checks** for canonical U198 UNSAT, V198 SAT 198-bit witness, Y6 SAT and malformed rejects. Matched UP-DPLL: Y6 SAT 4 nodes/38 scans, F9 SAT root 5/86, pinned F9 UNSAT 1/19.

**Falsifiers:** F1 every cycle forces actual 3^nu solver branches: FALSIFIED by source-component refutation. F2 a fixed-tape explicit-output enumerator can halt in o(t) writable/index cells: FALSIFIED under the specified model. F3 full source re-scan per guest input-bit query costs nothing: FALSIFIED for the no-index accessor. F4 NP-completeness or nonmonotone CP22 automatically transfers numerical FLMV: REJECTED, absent quantitative same-machine reduction.

**Corpus/search audit:** Reviewed 01:48 handoff, 01:44 theorem and code, issue #3, root main.tex, AGENTS, CODEX, pnp-research skill, REDIRECT1/CONTRACT1, LSPV-4 297/299, CP22LIFT1 and LSPV-2 slack-affine296. Primary papers searched: FLMV JACM 2005 (https://lance.fortnow.com/papers/files/tst.pdf), Döcker 2019 (https://arxiv.org/abs/1912.08032), streaming transducer/GF2 checking literature; CryptoMiniSat XOR engineering (https://github.com/msoos/cryptominisat). Project GitHub searches for SATURATED-CYCLE and CP22LIFT1 plus separate github.com/openai GF2/SAT code search were conducted. No novelty inference from search absence.

**Artifacts:** Full LaTex proof and three-page PDF, complete Python producer, independently written verifier, 23KB raw JSON, certificate replays and SHA-256 manifest are preserved in the accompanying ARC_EXPLICIT_BRANCH_CONFIGURATION300_FULL_REPRO.zip. A runnable compact checker is at experiments/arc/lspv4_300/arc_explicit_branch_space300_compact.py. Persistent Library upload was attempted but failed due to unavailable container session. Root owner-region reconciliation remains separately auditable.

**Next:** Build a true indexed native charged triangle+GF2 acquisition with simultaneous guest/index/parent peak space, and a local-bit-addressable near-unit canonical SAT-to-monotone target compiler or direct applicable target lower bound. **All-valid-target hereditary arbitrary-A->Phi(A), strict FLMV contradiction and P versus NP OPEN.** Existing five tasks, schedules and statuses untouched.

END_OF_VERIFIED_REPORT::LSPV4_ARC_EXPLICIT_BRANCH_CONFIGURATION300::P_VS_NP_OPEN
