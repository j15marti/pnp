# TMR-1/053: The quantitative loglog-density tariff for local witness circuits

**November 15, 2026, 13:57 PST | TMR-1 / PNP Machine Model Lead | Track C**

**Status:** New restricted compiler lemma PROVED/EXACT; new conditional quantitative transfer PROVED/RESTRICTED, independent mathematical review OPEN. Finite V8 verification COMPUTATIONAL. OpenAI/Anthropic #SAT results are pinned SOURCE CLAIMS, not independently kernel-replayed in this run. P versus NP OPEN.

## 1. Candidate and four falsifiers

**Candidate LDT053:** For fixed beta in {0,1,2}, assume one uniform deterministic algorithm decides every width<=3 CNF with V variables and m<=5V clauses in V^b 2^[A V (log_2 log_2 V)^beta / sqrt(log_2 V)] bit operations, for fixed positive A,b. Combine the constant-locality Jahanjou-Miles-Viola reduction, a shared circuit-to-CNF checker, and nondeterministic hierarchy to derive an infinitely-often lower bound Omega(N sqrt(log N)/(loglog N)^beta) on *general* fan-in-two circuits for one E^NP language. It is not an NP circuit lower bound.

Precommitted falsifiers: (F1) inserting the beta>0 solver into an uncorrected s=Theta(n sqrt(log n)) witness circuit gives exponent Theta(n(loglog n)^beta), no 2^(n/2) contradiction; (F2) violating formal AllOccur, clause-list NoDup, m<=5V, or n>=4 invalidates the claimed Anthropic transfer; (F3) an arbitrary poly(n)-gate clause decoder, rather than O(n) constant-locality decoder, can dominate the witness budget; (F4) claiming an NP conclusion or P!=NP from an E^NP hierarchy contradiction is a class mismatch.

## 2. All-occurring, duplicate-free functional CNF normalization: PROVED/RESTRICTED

Let C have q>=1 named input wires, G distinct shared, fan-in-two gates with arbitrary Boolean truth tables, and one output. For each gate z=f(a,b) add one z variable and four width-3 clauses indexed by (u,v) in {0,1}^2:

    (a != u) OR (b != v) OR (z = f(u,v)).

For every predecessor assignment exactly one of the four clauses forces z; the rest are satisfied. This remains true if a and b are the same wire, f is constant, gates share outputs, or some inputs are unused. Pin the final circuit output with one unit clause. The provisional formula has V=q+G variables and <=4G+1 clauses, and exactly one auxiliary assignment for each accepted original input. For each variable absent from every clause insert the tautology (x OR NOT x OR x), and remove duplicate *ordered clause lists* if any. These operations do not affect satisfiability or counting, make every variable occur, and preserve uniqueness of the gate extension.

The final H satisfies m<=4G+1+V<=5V (because q>=1), AllOccur, IsKCNF 3, and NoDup of the outer clause list. It is width-at-most-three, not necessarily strict proper 3CNF. This matches the actual Anthropic MainResults.lean predicates, which permit opposing or repeated literals **within** a clause. It takes O((q+G)log(q+G)) encoding bits and polynomial sequential construction time, with shared gates counted once. No witness or original-input enumeration is required.

The published deterministic JS checker exercises 16 binary gate functions, 96 seeded shared-DAG instances, repeated gate inputs, XOR, constants, omitted inputs, full extension enumeration and each exact input predicate. **112 circuits; 13,552 source-plus-auxiliary assignment checks; 2,136 assertions; 0 failures; 125 necessary tautologies.** Revision TMR1_LOGLOG_DENSITY053_v1, seed 20261115. These finite experiments are COMPUTATIONAL, while the preceding clause argument is symbolic.

## 3. Conditional theorem and proof: LDT053

**Theorem.** Assuming the specified density-five single-machine decision bound, the Jahanjou-Miles-Viola constant-locality reduction, and the unary nondeterministic exponential-time hierarchy, there exist one L in E^NP, c>0 and infinitely many N such that its minimum unrestricted shared fan-in-two noninput-gate circuit size exceeds

    c*N*sqrt(log_2 N)/(log_2 log_2 N)^beta.

**Proof.** Choose an appropriate unary H in NTIME(2^n) but not NTIME(2^(n/2)). At time T=2^n poly(n), the local reduction yields a succinct 3CNF phi_n with q=n+O(log n) clause-address bits and O(n) decoder output bits. Each output bit depends on at most a constant w index bits. Evaluate addresses of Hamming weight <=w to recover the support and truth table for every decoder output; the O(n) local outputs therefore have a uniform O(n 2^w)=O(n) binary-gate decoder, constructed in polynomial time.

Pad variable labels to dn bits for a fixed integer d. Define W(i), for |i|=dn, to be bit i of the lexicographically first satisfying assignment to phi_n (or zero if none). Produce the explicit 2^q clauses and make at most 2^(dn) NP prefix-extension queries, each on a formula of length 2^O(n). This computes W in 2^O(n)=2^O(|i|) time with an NP oracle, so W belongs to E^NP.

Assume for contradiction that, for every sufficiently large n, W at length dn admits a circuit of at most

    s_n=floor(eta*n*floor(sqrt(floor(log_2 n)))/
              max(1,floor(log_2 floor(log_2 n)))^beta)

gates, where rational eta is positive and 3A eta<1/2 (for example eta<1/(12A)). On unary 1^n, nondeterministically guess such a circuit, evaluate three copies on the three decoded variable labels, and construct a checker accepting an address iff the indexed clause is violated. Its number of gates is G<=3s_n+kappa*n, q=n+O(log n) inputs, and the normalization above gives

    V_n=3s_n+O(n), m_n<=5V_n.

If phi_n is satisfiable, the true W circuit makes the checker UNSAT; if phi_n is UNSAT, *every* candidate assignment circuit violates some clause. Accept exactly when the uniform SAT decider declares this checker UNSAT. The nondeterministic decider is correct for H.

For fixed beta, s_n=(eta+o(1))n sqrt(log_2 n)/(log_2 log_2 n)^beta. Hence V_n=(3eta+o(1))n sqrt(log_2 n)/(log_2 log_2 n)^beta, log_2 V_n~log_2 n, and log_2 log_2 V_n~log_2 log_2 n. The solver's bit-time exponent satisfies

    b log_2 V_n + A V_n(log_2 log_2 V_n)^beta/sqrt(log_2 V_n)
      = (3A eta+o(1))*n < n/2.

Guessing, local-decoder preparation, circuit encoding, wire access and CNF construction cost poly(n+s_n), absorbed within 2^(n/2). This contradicts the unary nondeterministic time hierarchy. Thus W requires >s_n gates infinitely often; with N=dn, any c<eta/d works asymptotically. QED, conditional on the stated sources.

**Sharp loglog tariff within this architecture:** Keeping s_n=eta n sqrt(log n) when beta>0 yields time exponent (3A eta+o(1))*n*(loglog n)^beta, not a fixed 2^((1/2-delta)n) hierarchy saving. The correction factor (loglog n)^beta in s_n is essential to *this particular proof*, not a universal lower bound on better methods.

## 4. Quantitative source dependency ledger (exactly pinned)

| Source | Actual scoped assertion | Consequence and guard |
|---|---|---|
| OpenAI October-25 manuscript, openai/math commit 42907c9e999cc00d6abe7a50bfc1023250edd1b9; build/main_full_version.tex and build/quantitative-circuits.tex | Claimed fixed-density m<=DV #SAT/3SAT time poly(V) 2^[O(V/sqrt(log V))], polynomial space; its corollary already states E^NP nonuniform gate lower bound Omega(N sqrt(log N)) infinitely often | beta=0, **manuscript source claim**, not re-proved independently as an underlying #SAT algorithm |
| OpenAI lean/docs/378.md at same commit | Lean scope explicitly reports poly(bit-length) 2^[O(V (loglog V)^2/sqrt(log V))], polynomial visited cells; sharper density manuscript bound separately labeled | beta=2 yields conditional Omega(N sqrt(log N)/(loglog N)^2); do NOT promote Lean scope to beta=0 |
| Anthropic formal-math commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5; eth/MainResults.lean and eth/Solution.lean | One finite-stack TM, all k>=1, V>=4, m>=2, outer NoDup, AllOccur; machine steps <=2^[C min(km/sqrt(log m), k^2 V loglog V/sqrt(log V))]. Solution.lean states proof terms for MainTheorem. | With k=3 and m<=5V, <=2^[15 C V/sqrt(log V)]; beta=0 is supported by the *stated* theorem, subject to full kernel replay, source-input conversion, and finite-stack-to-multitape charge. MainResults.lean alone defines propositions, not proofs. No polyspace implication from this time statement alone |
| Jahanjou-Miles-Viola, ECCC TR13-099 rev3, 2014 | Clause-index q=n+O(log n), constant-locality outputs at exponential T | O(n) decoder-gate tax, necessary for 3s+O(n) |
| Williams algorithmic method; Bathie-Williams 2024 | Established NEXP/ACC, E^NP, or restricted depth/formula lower bound conclusions at stated scopes | Here the target is E^NP general circuits; neither NP nor P!=NP |

The beta=0 loglog-free quantitative *premise* is stronger than the OpenAI Lean scope, but Anthropic's m-sensitive formal theorem has an independently stated beta=0 route on dense formulas satisfying its special input restrictions. The new normalization lemma explicitly discharges those input restrictions. Full Lean build and standard-machine transfer are still independently unverified in this run.

## 5. Same-realization resource ledger

| Stage on the one nondeterministic H execution | Paid sequential time | Writable storage |
|---|---|---|
| Read 1^n, construct constant-junta clause decoder | poly(n), including support discovery | poly(n) |
| Guess W circuit and wire indices, keep shared gates | O((s+n)log(s+n)) | O((s+n)log(s+n)) |
| Build clause-violation circuit and unique-extension CNF; dedup and tautologies | poly(n+s), m<=5V, input bits O(V log V) | poly(n+s) |
| Call the uniform deterministic decision/count-positive solver; negate its SAT result | <=poly(V) 2^[A V(loglog V)^beta/sqrt(log V)] | Source-specific: OpenAI manuscript/Lean claim poly(V); Anthropic time statement alone only guarantees <=time |
| Output H result | O(1) after solver | O(1) additional |

No separate machines are spliced into a forbidden time-space region. The NP oracle computes the **definition of the E^NP witness language W**, not an uncharged oracle on H's hypothesized fast execution. Gate construction, variable labels, canonical encoding, source access, nonuniform-circuit guessing, and all copies are paid. A multi-processor span bound is never substituted for sequential runtime. No DTISP(N^(1+gamma),N^sigma) contradiction is established.

## 6. Mandatory four gates

| Gate | Status and reason |
|---|---|
| DISJ sanity | **PASS restricted.** DISJ_k has full 2^k cut rank but an O(k) circuit; our CNF has O(k) gate variables and we infer no hardness from rank. Unique-witness, XOR/affine, dummy input, shared gates and constants remain cheap controls. |
| Relativization | **PASS restricted; OPEN unrestricted.** Ordinary local reductions, uniform #SAT premise and a nondeterministic hierarchy support a conditional E^NP statement, not a fully relativizing P!=NP argument. A nonrelativizing NP-level step, algebrization and Natural Proofs audits are OPEN. |
| Simultaneous DTISP | **NOT APPLICABLE WITH REASON.** This is a charged hierarchy *time* contradiction, not a claim to put one execution in a strict FLMV time+sublinear-space forbidden box. Same H execution is accounted; no strict workspace exponent certified. |
| Configuration counting | **PASS upper-bound control.** For deterministic total read-only-input machines, T<=2^O(S+log N) is an upper bound, never the claimed work lower bound. Not extrapolated to probabilistic/quantum execution. |

/341 remains FAIL as full logical UNSAT authority; /386 remains RESTRICTED. No inference from truth-table mass, padded bytes, static cut rank, entropy or prescribed DAG costs.

## 7. Corpus, reproducibility, remaining dependency

Read the newest SAT-compression directive FIRST (blob 7b8804dc7587abc5134055b5b0d16a143055ca5a), root proof1.txt (full SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), AGENTS.md, CODEX.md, research skill, five handoffs, issue #3 with latest comments and the original TMR-1/052, TMR-5/049, TMR-4/053 reports/code/results. proof2.txt SHA 930c5eeddafce656717f28055a7a9a755f44737 and main.tex SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 returned empty connector bodies; not touched. Native repo clone failed DNS; full preflight/Lean build unavailable. Published JS executed with exact raw JSON in hosted V8, no standalone Node test. Numeric log-size diagnostics are finite examples, not proof of asymptotics.

**Artifacts:** research/agents/tmr-1/2026-11-15_1357_TMR1_LOGLOG_DENSITY_WITNESS_TRANSFER053.md; experiments/tmr/tmr1_loglog_density053.js; results/raw/tmr/2026-11-15_1357_TMR1_LOGLOG_DENSITY053_V8_RAW.json; updated handoff.md.

**One next lemma:** Independently replay Anthropic's pinned kernel theorem and certify all source-encoding, tautological coverage and finite-stack-to-multitape costs in one hierarchy-decider realization. Separately compare the weaker OpenAI beta=2 Lean scope without substituting the unverified manuscript beta=0 bound. TMR-5 independent verification and TMR-3 same-system resource review requested; A/B results cannot be imported as arbitrary-circuit transfer.

**TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.** All five TMR identities/schedules remain unchanged. **P versus NP remains OPEN.**

### Sources

1. OpenAI, pinned October-25 paper and quantitative appendix: https://github.com/openai/math/blob/42907c9e999cc00d6abe7a50bfc1023250edd1b9/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/quantitative-circuits.tex
2. OpenAI Lean scope: https://github.com/openai/math/blob/42907c9e999cc00d6abe7a50bfc1023250edd1b9/lean/docs/378.md
3. Anthropic MainResults and Solution: https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth/MainResults.lean
4. Jahanjou, Miles, Viola, Local Reductions (ECCC 2013/099, rev. 2014): https://eccc.weizmann.ac.il/report/2013/099/
5. Williams, Non-Uniform ACC Circuit Lower Bounds: https://people.csail.mit.edu/rrw/acc-lbs-journal-final.pdf
6. Bathie, Williams, Towards Stronger Depth Lower Bounds (ITCS 2024): https://doi.org/10.4230/LIPIcs.ITCS.2024.10

END_OF_VERIFIED_REPORT::TMR1::053
