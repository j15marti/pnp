# LSPV-4 ALLINPUT-FULL-PAYLOAD-VALID-NEIGHBOR310
**2026-11-01 11:36 PST, America/Los_Angeles.** PROVED/EXACT *restricted deterministic source-query* lemmas under an explicitly declared binary grammar; COMPUTATIONAL independent original SAT/UNSAT and bit-flip controls; known FLMV Theorem 5.7; universal P-vs-NP spine OPEN. External mathematical review pending.

## Exact obstruction, prior work, falsifiers
The new goal is generalized SAT/UNSAT **decision work** rather than recovery of assignments or injective syntactic pin keys. CUBEKEY306's 84^t count applies only to its lossless key. YES-GRAMMAR308 proves an m-bit *clause-sign* source floor on accepting valid canonical originals. This run strengthens it to **every literal-ID bit**, establishes a nearly full source-read floor for every accepted target input in the declared grammar, and independently reconstructs a VALID-only opposite-label two-bit neighbor control. The U/V valid-input direct-sum principle was already proved in project ARC-PROBE-DIRECT-SUM286 and VALID-STATE285; no novelty claimed for the generic adversary.

F1: valid YES inputs may skip an ID bit once clause signs/quotas are available. **FALSIFIED.** F2: malformed neighbors force the same reads on UNSAT inputs. **INVALID**, because both outcomes reject. F3: valid-input promise makes all source probes avoidable. **FALSIFIED on U198/V198 direct sum**, but the lower bound is just linear in components. F4: full input read implies superlinear computation/linear writable space. **INVALID**, sequential reading is O(N) and source inspection is distinct from solving.

## Theorem 310A, every payload bit pivotal on SAT
The target is ALL proper duplicate-free monotone 3-SAT-(2,2) originals, clausewise 3 distinct same-sign names, exactly two occurrences of each sign per variable, malformed rejected. The declared binary input grammar is

E(F)=gamma(n) gamma(m) product_{j=1}^m [sign(C_j), bin_w(v_j1),bin_w(v_j2),bin_w(v_j3)],
w=ceil(log2(n+1)), m=4n/3,

where gamma is Elias-gamma encoding, and the three variable IDs are positive unsigned w-bit numbers.

**Exact quantified statement.** For EVERY valid **SAT** original F and EVERY deterministic exact SAT decider D that rejects malformed strings, the accepting run on E(F) queries *every* signed literal-payload bit:

    Q_D(E(F)) >= m(1+3w)
              = |E(F)| - |gamma(n)| - |gamma(m)|
              = N-O(log N).

**Proof.** Flip one arbitrary signed-literal-payload bit while fixing the gamma header and all other cells. If it is the clause polarity, each of the clause's three variables loses one occurrence of its former sign and gains an occurrence of the other; the 2P/2N quota fails. If it is one of the w ID bits, its original name x changes to a distinct integer y. If y=0 or y>n, grammar fails; otherwise x loses one signed occurrence and y gains one, so both exact sign quotas fail. Either way the one-bit mutant is **malformed**. If D skips that bit on its accepting native computation, it has the same observed input transcript and therefore the same deterministic strategy, index/work/head/guest execution and accepting output on the malformed neighbor, contradiction. Apply independently to each of the m(1+3w) bits. QED.

**Scope firewall:** The theorem is for a specified binary grammar, acceptance/YES, and correct rejection of malformed strings. On UNSAT input F, its one-bit malformed neighbors share the NO label, so this proof gives no UNSAT-side read floor. On a prevalidated-valid promise, the mutated strings are outside the promise. It is a **linear input-observation lower bound, not a superlinear time bound, workspace bound, mandatory pin recovery or arbitrary-machine P!=NP proof**. Read-only input scans can be sequential; repeatedly building a log N indexed address for each bit is an avoidable implementation-specific overhead.

## Theorem 310B, independently reconstructed VALID source-neighbor pair and direct sum
The original authenticated canonical U198 consists of 198 variables and 264 clauses, UNSAT with six 32-variable modules and 64 boundary assignments. Let V198 be obtained by swapping the third positive variable ID of zero-based original clauses **2 and 44**, exchanging 197 and 196. Both remain valid complete-language originals. A full published 198-bit witness was freshly checked against each V clause, while an independently programmed U refutation checked **all 64** boundary cubes: 16 direct original-clause contradictions, 48 refuted with 152 private-module DPLL calls (10,709 nodes with an independent clause-based branching policy). Another producer ordering used 711,932 nodes. Both labels are certified.

In the SAME gamma+fixed-ID binary grammar at n=198,m=264,w=8,

    |E(U198)|=|E(V198)|=6632,
    d_H(E(U198),E(V198))=2,
    differing physical bit cells (zero-based) = {106,1156}.

This is the smallest possible nonzero **payload** Hamming distance between different valid originals sharing the same n,m header: every one-bit payload mutation is invalid by Theorem 310A's quota argument (which does not require satisfiability for the invalid-neighbor fact). This U/V pair attains the minimum and has **opposite** SAT labels.

For any integer t>=1, let S_t be t variable-disjoint renamed copies of V198 and let N_{t,i} replace copy i by U198. All are valid canonical originals, S_t is SAT, N_{t,i} is UNSAT. Rename offsets are multiples of 198, so 196+198i and 197+198i still differ in one least-significant ID bit, and each D_i={b:E(S_t)_b != E(N_{t,i})_b} consists of **two** bit positions within block i. D_i are pairwise disjoint. For **every deterministic exact decider correct on all valid canonical originals**, even when malformed inputs are not supplied, its accepting computation on S_t must read a bit in each D_i or it would incorrectly accept the valid UNSAT N_{t,i}. Thus

    Q_D(S_t) >= t = Omega(N_t/log N_t),
    N_t=|gamma(198t)|+|gamma(264t)|
        +264t*(1+3 ceil(log2(198t+1))).

Under the much stronger *promised* per-block U/V alphabet, checking one predesignated discriminating bit per block attains t queries; all membership/authentication/discovery costs are separately paid. These originals are disconnected, easy AND-decomposable controls; this cannot imply superpolynomial SAT hardness. The source-adversary/direct-sum method is previously known in ARC-PROBE-DIRECT-SUM286; the source bit positions and alternative swap are an independently reproduced refinement.

## Independent source and bit-level checks
A producer with a standalone source parser and a separate no-producer-import verifier were executed. Producer: **28,337 assertions and 21,900 one-bit source mutations** (the G128 sample is 256 because every bit is already covered by the symbolic proof). Independent small-original verifier: **8,725 assertions and 8,700 same-source mutations**. Independent U198/V198 verifier: **13,332 assertions including all 13,200 U/V payload mutations, 64 UNSAT boundary conditions, 152 module calls, and the 198-bit SAT witness**. Both independent verifiers use their own source reconstitution and grammar-checking logic.

| Original | status | N bits | header bits | all payload bits | tested flips |
|---|---|---:|---:|---:|---:|
| Y6 | SAT, 20 models | 92 | 12 | 80 | 80 |
| F9 | SAT, 70 models | 170 | 14 | 156 | 156 |
| G2 | SAT | 402 | 18 | 384 | 384 |
| G4 | SAT | 934 | 22 | 912 | 912 |
| G8 | SAT | 2138 | 26 | 2112 | 2112 |
| G16 | SAT | 4830 | 30 | 4800 | 4800 |
| G128 | SAT | 52266 | 42 | 52224 | 256 sample |
| U198 | UNSAT | 6632 | 32 | 6600 | 6600 |
| V198 | SAT | 6632 | 32 | 6600 | 6600 |

On the SAME valid F9 original, coherent partial pins (x1,x2,x3,x4,x8)=(1,0,1,0,0) yield exactly **one** SAT completion, versus (1,1,0,0,0) yielding zero. All 264 original clause-pair SS/SU/US/UU modes and 6,144 complement clause identities were checked. U198/V198 signed quotas, original clauses, full YES witness and complete NO refutation were separately checked. U198's malformed one-bit mutants do **not** imply obligatory reads on a NO run.

## FLMV exact model and full work ledger
Original FLMV §2.1 uses **a binary read-only input tape**, index tapes for jumps that are atomically erased, writable work tapes, and a one-way write-only output tape. Input and output capacity do not count toward writable space; indexes/heads, all live cache/matrix/proof/guest state must still be charged. A distinct source-bit observation costs at least one native read step. A serial input-head scan can read N bits in O(N) source/head steps; a naively repeated indexed-jump scanner may charge O(N log N) native index/header work. The latter overhead is NOT a universal lower bound. Existing ARC-AMORTIZED-INDEX282 controls atomic index erasure. d_logic and checkpoint XOR are OFFLINE unless traced by the SAT machine.

For adaptive controller node z, the correct fully charged recursive upper accounting is

W_D(z) <= C_grammar/source/index/head(z)
         + sum_{attempted policies pi} C_discover/select/switch/failed(z,pi)
         + C_GE/matroid/proof/cache/replay(z)
         + sum_{y evaluated successor}(C_encode/output/bit/guest(z,y)+W_D(y)).

Peak space is the maximum simultaneous retained ancestor/work/index/head, child translators, live guest A, proof/GE, caches, output buffers and policy state. Free-variable count gives finite fallback only, possibly 2^Theta(n); signed delta can increase. Neither a paid all-input polynomial aggregate-work controller nor an arbitrary-decider power-short hereditary target-valid A->Phi(A) is proved.

Exact-rational FLMV Theorem 5.7 audit: d*(6/5)=23/45, d*(241/200)=11642479/23232400. Unique maximizing k=2 at both c and k>=4 strictly excluded by c^-4<d_2. The theorem forbids a **little-o** space range, not an equal closed boundary. For hypothetical target exponents (6/5,1/2) numerical SAT transfer requires a fully charged same-machine SAT-to-Döcker reduction with output exponent b and guest-access overhead rho:

    (6/5)b+rho < 241/200,
    b/2 < 11642479/23232400,
    so b < 11642479/11616200 ~= 1.00226227 even at rho=0,

plus setup, output-bit accessor, source/index/head and peak workspace checks. NP-completeness alone does not supply this quantitative reduction; neither a valid addressable near-linear normalizer nor universal ARC contractor has been constructed.

## Preflight, source and duplication audit
Read FIRST the verified 01:48 integrated handoff SHA fcb07fb4612055ad476155da47643c5d4d687c74 and 01:44 saturated-cycle theorem SHA 3c05146b10ffd597f922f395c967dd4b2dd89875; then AGENTS, CODEX, pnp-research skill, REDIRECT1, CONTRACT1, active issue #3, LSPV-1 CONTINUATION308, LSPV-2 SEMANTIC-QUOTIENT310, LSPV-3 GATE308, LSPV-4 GRAMMAR308/ORDERED309, LSPV-5 REFEREE270, and original U198 source/witness. Duplicated known work: ARC-PROBE-DIRECT-SUM286, VALID-STATE285, ARC-AMORTIZED-INDEX282 and YES-GRAMMAR308. No duplicate-free novelty inferred from search absence.

Web literature queries: "FLMV 2005 indexed read-only input model Theorem 5.7 PDF"; "Döcker monotone 3-SAT-(2,2) 2019"; "boolean matrix semiring SAT bounded-interface DP"; "locally bit-addressable SAT reduction." Primary: Fortnow et al., JACM 52(6), 2005, https://lance.fortnow.com/papers/files/tst.pdf (PDF p.4 visually checked), and Döcker, arXiv:1912.08032. Decision-tree pivotal-bit method is classical (Nisan, SIAM J. Comput., 1991). Separate project GitHub searches: "literal ID bit grammar floor", "every literal identifier bit malformed neighbor", "U198 V198 two bit Hamming distance", "U198 V198 direct sum bit probes", "amortized index erasure physical XOR". github.com/openai searches: "time space lower bounds model tape index erase", "proof complexity semantic compression", "branching program SAT". No generalized hardness inferred from no search matches.

**Reproducibility:** full 9-file ZIP with expanded markdown report, producer, two independent no-import verifiers, signed U198 public fixture, original-source raw JSON, exact boundary proof outcomes and SHA-256 manifest available in this run's conversation sandbox. GitHub compact reproducer, role-owned report, machine-readable summary and five-role handoff are published separately with GitHub readback.

**Root main.tex:** reconciliation of LSPV-4's own marker remains pending because the >1 MB root has returned empty connector content despite a nonempty blob in recent audits, and an unsafe overwrite is prohibited. No task identity/status/schedule changed. **P versus NP OPEN.**

END_OF_VERIFIED_REPORT::LSPV4::FULL_PAYLOAD_VALID_NEIGHBOR310::P_VS_NP_OPEN
