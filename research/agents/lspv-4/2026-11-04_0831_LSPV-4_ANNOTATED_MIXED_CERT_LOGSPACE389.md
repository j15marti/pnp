# LSPV-4/389: annotated mixed-proof verifier and circuit-value firewall

**2026-11-04, 08:31 PST.** PNP Time-Space Resource Auditor. **PROVED/EXACT** for explicitly annotated certificate grammar. Prior published CVP P-completeness is **KNOWN**. Finite controls **COMPUTATIONAL**. Full R_mix341 byte-level agreement, B1/B2/B3, P versus NP **OPEN**; specialist review pending.

## IDEA -> SEARCH -> ITERATE

**IDEA (pre-search):** Perhaps every R_mix341 shared-DAG certificate can be checked in deterministic O(log M) workspace directly, even when LOCAL-CONVERT uses an arbitrarily long circuit over at most three original variables. Falsifier: reduce Circuit Value Problem (CVP) to the local conversion.

**SEARCH:** Ladner 1975 established P-completeness of CVP under logspace reductions (DOI 10.1145/990518.990519). Project R_mix341 definition: `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (RES, AND3, XOR, LOCAL-CONVERT, conservative two-input DEF, each unit paid). LSPV-4/379 already observed P-complete gate acquisition, while /384 proved a Resolution-only read-only rescanning checker. Checked the November 2 five-role handoff, issue #3, AGENTS.md, CODEX.md, pnp-research skill, latest LSPV-1/392 and LSPV-2/393. External reviewers: `GROKPROOF/2026-11-04_1518_PROGRESS.md` (blob 4e2bb9d9), Claude ONETAPE-0001 and TPORT-0002. None supplies B3. OpenAI GitHub search `resolution certificate` returned unrelated algebraic geometry and network/TLS matches; no relevant OpenAI SAT implementation was found. LeanSAT's verified LRAT checker is an implementation comparison, not an R_mix341 theorem.

**ITERATE, original idea rejected:** For any fully explicit constant-input Boolean circuit C, let v(C) be its output, take source premise P(x)=x, and proposed gate-circuit target D(x)=x AND v(C). Then:

$$
P\models D\quad\Longleftrightarrow\quad v(C)=1.
$$

The transformation merely copies the circuit and adds x and one AND gate, and is logspace-computable. Thus exact **unannotated** LOCAL-CONVERT implication checking, if it permits unrestricted long AND/OR/NOT gate lists over one original variable, is P-complete. The support-two truth table is small but evaluating its circuit is not known to lie in L. This does NOT prove L != P.

## Revised positive theorem (declared annotated grammar)

Attach to every gate of an explicitly encoded LOCAL-CONVERT or AND3 condition a truth-vector of at most eight bits, one for each assignment to its at most three original variables. For a DEF gate, a four-entry fan-in-two truth table is sufficient. This **read-only evidence annotation** introduces no new premise, rule or paid logical inference node.

Given source+proof+annotation total encoded length M, a fixed uniform indexed read-only-input deterministic checker verifies chronological typed R_mix341 proof records in:

$$
S_{check}(M)=O(\log M),\qquad T_{check}(M)=M^{O(1)}.
$$

A conservative bound for nested rescans is O(M^6) bit steps. With g already encoded bounded-support gates, trace bits add at most 8g+O(g) evidence bits, a linear overhead in explicit gate-list size. The original number of inference nodes q is unchanged.

**Proof:** With O(log M)-bit gate, row, source and node counters, read each claimed gate value and its at-most-two earlier parent values from the immutable annotation, check the fixed Boolean operation, and reject bad parents, cycles, types and values. Induction over gate indices authenticates each row. Check local implication, conjunction and GF(2) annotation by at most eight authenticated assignments. RES pivots and exact resolvents, XOR bitwise masks and RHS, and DEF freshness, chronological dependencies and uniquely extendible two-input relation use indexed rescans and logarithmic counters. Check source grammar, source references, proof dependencies and explicit contradiction. Induction over proof nodes establishes soundness. No unbounded computed gate state must be stored.

**Precise limitation:** This is a normal-form theorem, NOT a verified equivalence to every actual serialized R_mix341 record. A complete byte-level checker for its exact parser and all permitted syntaxes is outstanding. An unannotated circuit still encodes CVP. Finding/outputting trace data is not free, and can use Theta(g) writable bits. If a proof is materialized in an N-sized writable buffer, all-phase rho >= 1, even if later freed; low-space verification of a pre-supplied read-only certificate does not repair that. Exponentially long proofs remain legal but entail actual exponential evidence/output cost. This theorem provides neither a machine-time lower bound nor an algorithm-to-proof transfer.

## Falsifiers, exact tests, resource ledger

1. Constant original-variable support automatically implies logspace unannotated evaluation: invalid reasoning by CVP P-completeness.
2. Wrong trace or references accepted as a free oracle: 800 one-bit-corrupted traces and 2400 malformed records rejected by Python.
3. Independent implementation misses corruption: 160 corrupted and 160 malformed records rejected by no-import Node reviewer.
4. Labels/parity forgotten: 8 SAT+8 UNSAT source controls, source RES/AND3/XOR/DEF controls, odd K4 Tseitin 0 models and even K4 8.

Python deterministic seed 389: 800 valid circuits, 4810 assertions, 80 CVP-to-LOCAL-CONVERT controls (39 YES/41 NO), 600 source-implication controls. Independent JavaScript: 602 checks. Host process space is NOT an indexed-TM-space measurement.

Let N be source bits, P explicit proof bits, M=N+P+O(g) annotated bits. Checking has O(log M) writable space by a formal rescan algorithm; producing a proof, generating the annotations, outputting M bits, checking correctness of an arbitrary decider, and all simultaneously live buffers have **separate** costs. Source-arity and shortest proof node count are not physical machine running time.

## Established hard family and bridge status

Haken (1985): for the *standard unary PHP(h+1,h)* explicit signed-index CNF, N_h=Theta(h^3 log h) bits, there exist c>0,h0 such that for all h>=h0 **every ordinary shared-DAG Resolution refutation** has at least 2^(ch) lines. This is NOT a lower bound for Extended Resolution, GF(2), R_mix341 or all SAT machines. Cook (1976) constructs polynomial Extended Resolution proofs. No existing hard examples were regenerated.

B1: for each uniform total correct A, W_R(F) <= p_A(N+T_A(F)) for all UNSAT F. B2: Wbar_R(N) <= p_A(N+T_A^wc(N)), where worst-case runtime is over **all** strings <=N. B3 (weakest sufficient): SAT in P implies Wbar_Rmix341(N) polynomial. B1 => B2 => B3; none proved, and no superpolynomial R_mix341 lower bound is known.

**NEXT:** independently formalize every byte-level node grammar and show sound, cost-preserving trace-annotation normalization for all authentic R_mix341 certificates. Even this does not imply B3 or P != NP.

References: [1] Ladner, SIGACT News 7(1):18-20 (1975). [2] Haken, Theoretical Computer Science 39:297-308 (1985). [3] Cook, SIGACT News 8(4):28-32 (1976). [4] Buss, JSL 52(4):916-927 (1987). [5] leanprover/leansat verified LRAT implementation.
