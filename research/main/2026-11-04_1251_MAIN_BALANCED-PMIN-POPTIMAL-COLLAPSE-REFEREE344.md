# REFEREE344: balanced minimum-cost / p-optimal collapse and the exponential-minimum counterexample

**November 4, 2026, 12:51 PST — PNP Independent Proof Red Team.**

**Status.** **PROVED/CONDITIONAL:** under `SAT in P`, an explicit polynomial verifier, and two-way polynomial node/bit balance, polynomial worst-case minimum node cost, polynomial encoded proof length, uniform exact minimum-proof search, and p-optimality among target-exposing explicit-CNF proof systems are equivalent. **PROVED counterexample:** ordinary p-boundedness plus constant minimum node cost does not imply feasible exact-minimum output when all minimum proofs have exponential payload. **PROVED/CONDITIONAL:** polynomial balance alone gives an output-sensitive exact extractor in time polynomial in `|F|+W_R(F)`. The exact optimizer portion is already LSPV-1/364 and LSPV-4/393; the increment is the p-optimal equivalence, the external-formula firewall, and the fixed-system minimum-payload counterexample. Full `R_mix341` verification/balance, PMin, B1, B2, B3, unrestricted SAT hardness, and P versus NP remain **OPEN**. No rule, cost, task, schedule, status, identity, or ownership boundary changed.

## 1. IDEA before search

Test the following concrete repair of the missing transfer:

> If the fixed target calculus has a polynomial-time whole-proof verifier and every minimum-cost proof has a polynomial-bit representative, then under `SAT in P`, polynomial worst-case target cost should be equivalent not only to exact proof search but also to target p-optimality.

The falsifiable prediction was that one of four attacks would break it:

1. a node/bit mismatch in which the minimum node carries an exponential payload;
2. a nonuniform per-length proof generator hidden in the claimed search algorithm;
3. an external relation whose witness omits the arbitrarily long target formula;
4. a translator polynomial only in the target formula, rather than in the supplied source proof.

The initial statement did fail under attacks 1 and 3. The repaired statement below survives all four.

## 2. SEARCH and what changed

### Primary literature

Actual general-web queries were:

- `p-optimal propositional proof system p-bounded proof system SAT in P equivalence primary literature`;
- `Krajicek Pudlak optimal proof systems proof search p-optimal system primary paper`;
- `Cook Reckhow proof system p-simulation polynomially bounded proof search exact shortest proof`;
- `Atserias Muller Automating Resolution NP hard shortest proof output sensitive`.

Sources read:

- Cook--Reckhow, *The Relative Efficiency of Propositional Proof Systems*: proof systems are polynomial-time onto maps and p-simulation requires a uniform polynomial-time proof translator. Their p-bounded existence theorem is about **some** proof system, not the preselected `R_mix341`.
- Krajicek--Pudlak, *Propositional Proof Systems, the Consistency of First Order Theories and the Complexity of Computations* (JSL 54(3), DOI `10.2307/2274765`).
- J. Krajicek, *Information in Propositional Proofs and Algorithmic Proof Search*, arXiv:2104.04711: short proofs and proof search are separate in general; time-optimal proof search is tied to p-optimal systems.
- Atserias--Muller, *Automating Resolution is NP-Hard*, arXiv:1904.02991: proof-search time is calibrated against source size and shortest proof size.
- A. Haken, *The Intractability of Resolution*, TCS 39 (1985), DOI `10.1016/0304-3975(85)90144-6`.

Direct branded Google UI was unavailable. General web search was used; no Google-specific search is claimed.

### Project, OpenAI GitHub, Grok, and Claude

The project already contained two pieces of the argument:

- `research/agents/lspv-1/2026-11-03_0704_LSPV-1_BUDGETED_PROOF_SEARCH364.tex` and `research/agents/lspv-4/2026-11-04_1136_LSPV-4_POLY_BALANCE_EXACT_OPTIMIZER393.md` prove the conditional exact extractor;
- `research/main/2026-11-03_0948_MAIN_COOK-RECKHOW-B3-TRANSFER-REFEREE317.md` proves that p-simulation of the decider-induced proof system would suffice for B3;
- `research/main/2026-11-04_1248_MAIN_REFLECTION-SANDWICH-POLY-BALANCE-REFEREE343.md` isolates polynomial certificate balance.

OpenAI GitHub queries `p-optimal proof system`, `Cook Reckhow proof search`, and `Resolution proof verifier SAT` returned no applicable compiler or theorem. The relevant file actually read was `openai/math/lean/OAI/Computability/DirectedFeedback/CookLevin/NPTableau.lean`, blob `d8c0a32e25d8d86f623559e1c8e08acec948fb3f`: it formalizes an NP-verifier/Cook--Levin tableau satisfiability equivalence, not p-optimality or `R_mix341` translation.

Current external assessments were read at exact paths:

- `GROKPROOF/2026-11-04_1518_PROGRESS.md`, blob `4e2bb9d941295f620a64e078117d29244caf4fba`: the arbitrary-decider fully charged all-input transformation remains OPEN;
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`: a restricted alternation-trading portfolio theorem;
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`: sequential/one-tape access lower bounds that explicitly do not transfer to the random-access target.

Neither Grok nor Claude supplies p-optimality, polynomial balance for full `R_mix341`, or B3. Issue #3 was read through the current LSPV-3/401 and LSPV-4/394 reports; both preserve the same missing full mixed verifier/balance bridge.

## 3. Exact established lower-bound anchor

For `h+1` pigeons and `h` holes, explicit unary `PHP_(h+1)^h` has variables `x_(i,j)`, pigeon clauses

`OR_(j=1)^h x_(i,j)`,

and collision clauses

`(not x_(i,j) OR not x_(k,j))` for `i<k`.

It has `h(h+1)` variables and `(h+1)+h*binom(h+1,2)` clauses. Explicit signed DIMACS with binary-magnitude identifiers has length `N_h=Theta(h^3 log h)`.

Haken's exact proof-model strength used here is:

> There are constants `c>0,h0` such that for every `h>=h0` and every ordinary unrestricted shared-DAG **Resolution** refutation of this explicit CNF, the refutation has at least `2^(c h)` lines.

The universal proof quantifier permits arbitrary legal pivots and DAG sharing. The system contains source clauses and ordinary Resolution only. It excludes extension variables, Extended Resolution, GF(2), `Res(oplus)`, circuits, semantic inference, `R_mix341`, and arbitrary SAT algorithms. In explicit input length the lower bound is `2^Omega((N_h/log N_h)^(1/3))` for this family and system.

Cook's polynomial Extended-Resolution PHP proofs show the compulsory representation escape. Thus ordinary Resolution has polynomial checking/balance but fails all four properties below: Haken rules out polynomial minima and polynomial proof length; polynomial-time exact output is impossible by output length; and Resolution cannot p-simulate the polynomial ER PHP proofs. This consistency check is still a proof-system separation, not unrestricted machine hardness.

## 4. ITERATE: repaired definitions

Fix the canonical explicit binary language `CNF`. Fix one sound complete target-exposing refutation relation `R(F,pi)` and a paid cost `q_R(F,pi)`. For `R_mix341`, cost is the sum of paid inference-node weights.

The following are single global assumptions fixed with `R`, never per input or per cutoff:

- **V:** one total verifier parses `F,pi`, rejects malformed sources/proofs, recomputes exact cost and checks the whole shared DAG in time polynomial in `|F|+|pi|`;
- **UB (project PB):** one polynomial `b` satisfies: if `W_R(F)<=q`, then some canonical proof of cost at most `q` has at most `b(|F|+q)` total bits;
- **LB:** one polynomial `d` satisfies `q_R(F,pi)<=d(|F|+|pi|)` for every accepted proof. For explicit unit-weight records, `q<=|pi|` suffices.

UB counts source authentication, headers, parent identifiers, clauses, XOR rows, circuit gates, ports, auxiliary names, annotations, padding and every other payload. It is **minimum-cost polynomial balance**, not the standard phrase “p-bounded proof system.”

Define:

- **PMin:** one polynomial `P0` satisfies `Wbar_R(N)<=P0(N)` for every `N`;
- **PBound:** one polynomial `r` gives every valid UNSAT `F` an accepted proof of at most `r(|F|)` bits;
- **MinSearch:** one total uniform polynomial-time algorithm rejects malformed sources, returns a checked model on valid SAT sources, and outputs an exact minimum-cost canonical `R` refutation on valid UNSAT sources;
- **pOpt-CNF:** for every fixed sound complete polynomial-time target-exposing explicit-CNF refutation relation `Q(F,sigma)`, one uniform FP translator `T_Q` maps each valid `(F,sigma)` to an `R` proof of the same `F` in time/output polynomial in `|F|+|sigma|`.

The comparison class in pOpt-CNF includes the decider-induced relation below. If one narrows “proof system” to conventional finite-rule calculi and excludes it, the converse is not established.

In the unary Cook--Reckhow formulation, the proof string internalizes enough information to compute its conclusion `F`; polynomial-time output implies `|F|<=poly(|sigma|)`. A relation translator measured only in witness length while receiving an external, uncharged `F` is a different and invalid definition: the empty witness cannot physically output proofs for arbitrarily long `F`.

## 5. Conditional four-way equivalence

### Theorem

Assume `SAT in P` by one fixed uniform total correct all-length decider `A`, plus V, UB and LB for fixed `R`. Then

`PMin  <=>  PBound  <=>  MinSearch  <=>  pOpt-CNF`.

### Proof

**PMin implies PBound.** If `W_R(F)<=P0(N)`, UB supplies a proof with at most `b(N+P0(N))` bits.

**PBound implies PMin.** If `|pi|<=r(N)`, LB gives cost at most `d(N+r(N))`. Maximize over valid UNSAT inputs of length at most `N`.

**PBound implies MinSearch.** The preceding implication supplies a fixed polynomial node cutoff `P0`. For a budget `q<=P0(N)`, length bound `B=b(N+q)`, and canonical prefix `u`, the predicate

`exists pi: |pi|<=B, pi extends u, V_R(F,pi)=1, q_R(F,pi)<=q`

is in NP. Under `SAT in P`, one fixed decider handles the uniform Cook--Levin reductions. Binary-search the least feasible `q`, then self-reduce a self-delimiting, canonically padded proof bit by bit. Reverify the final result. The fixed polynomials may be hardcoded once with `R`; no machine or advice depends on `F` or `N`. Parse first, self-reduce and check a SAT model on the positive side, and reject malformed strings.

**MinSearch implies PBound.** A polynomial-time machine cannot emit more than polynomially many bits.

**MinSearch implies pOpt-CNF.** Given a valid `Q` proof `(F,sigma)`, validate/recover `F` and run the exact target searcher. It may ignore the source derivation after authentication. Total time and output are polynomial in `|F|+|sigma|`. This generates a fresh same-conclusion proof; no exponential backtranslation of the source DAG is used.

**pOpt-CNF implies PBound.** Use the fixed target-exposing system `D_A(F,epsilon)` that accepts its canonical empty/one-bit certificate exactly when the strict parser accepts `F` and the fixed P-time `A` says UNSAT. `D_A` is uniform, sound, complete and polynomial-time only under the stated `SAT in P` hypothesis. pOpt-CNF translates its canonical proof to an `R` proof in polynomial time/output in `|F|`. Hence PBound.

This is an equivalence **inside** the hypothesis `SAT in P`. Without it, p-boundedness, exact automatizability and p-optimality are distinct notions.

### Standard TAUT wrapper

A CNF refuter is not literally a Cook--Reckhow TAUT system. To state standard p-optimality, fix a polynomial-time canonical `Can(tau)=CNF(not tau)` with deterministic fresh names and identity on tagged `tau=NEG-CNF(F)`. A wrapper recomputes `Can(tau)` byte-for-byte and accepts an authenticated `R` refutation of exactly that source. The Tseitin namespace and later proof-extension namespace must be disjoint. Under this wrapper, the same proof yields conditional standard p-optimality. Without an explicit polynomial wrapper/retraction, no TAUT claim is made.

## 6. Output-sensitive physical bound

PMin is not required for output-sensitive exact search. Under `SAT in P`, V and UB, try `q=1,2,4,...`. The first feasible `q` is below `2W_R(F)`; binary-search `q*=W_R(F)` and prefix-extract a proof of at most `b(N+q*)` bits. Thus

`T_extract(F)=poly(N+W_R(F))`.

If `W_R(F)` is exponential, this honestly permits exponential queries, proof bytes and runtime. PMin is what replaces the output-sensitive bound by input-polynomial time.

With `B=b(N+P0(N))`, at most

`K <= B + ceil(log2(P0(N)+1)) + O(log B)`

prefix/budget queries are used. If a materialized Cook--Levin query has length `D=poly(N+B+log P0)`, a conservative charged bound is

`T <= T_parse + K*(T_CL(D)+T_A(D)) + T_V(N+B) + O(B)`.

Peak space is at most the maximum of retained prefix `B`, materialized query `D`, reduction/guest/verifier space, and indexing state. Output alone costs `Omega(actual proof bits)`. Lazy query generation trades storage for recomputation; it does not give the fixed guest free random access. This is polynomial time/space, not an FLMV sublinear-space profile.

## 7. Counterexample: p-bounded and PMin, but no feasible exact minimum

The original idea falsely used ordinary p-boundedness where UB was needed. Here is a fixed conditional counterexample.

Assume the same fixed P-time decider `A`. Define `R_dagger` with two proof forms for explicit `N`-bit source `F`:

- `L`: after authenticating `F` and `A(F)=UNSAT`, require exactly `2^N` explicit zero payload bits; charge one paid node;
- `S`: after the same checks, require `N` explicit zero payload bits; charge `N` paid nodes.

The verifier scans the supplied payload and is polynomial in full input-plus-proof length. It rejects SAT sources, malformed tags, wrong lengths and corrupt payloads. The system is sound and complete. It is p-bounded via `S`, and `Wbar_Rdagger(N)=1` via `L`. Yet every exact minimum-node proof has `Omega(2^N)` bits, so no input-polynomial exact-minimum generator can output it. UB fails exactly at `q=1`.

This does not attack the repaired theorem. It proves that PMin plus ordinary short **nonminimum** proofs is not the required minimum-cost balance.

## 8. Finite controls

Producer:
`experiments/arc/lspv5_344/poptimal_balance_referee344.py`

Independent verifier:
`experiments/arc/lspv5_344/verify_poptimal_balance_referee344.js`

Raw:
`results/raw/arc/2026-11-04_1251_LSPV5_344_POPTIMAL_BALANCE.json`

The producer exhausted all 256 CNFs over the eight nonempty non-tautological clauses on two variables:

- 95 SAT and 161 UNSAT;
- exact ordinary-Resolution minimum distribution `q=1:112`, `q=2:48`, `q=3:1`;
- 161 valid translations each from decision, truth-table and Resolution source certificates to the exact target minimum;
- 644 malformed/corrupt source certificates rejected;
- `R_dagger` controls for `N=2..16`: minimum cost one, minimum proof payload `2^N+1` bits, short nonminimum proof `N+1` bits, SAT and truncated proofs rejected.

The independent Node verifier passed 103 checks.

SHA-256:

- Python: `6f960bb3107572f4d6a553a17f82b0fe9539447c0575a32b978029b397136291`;
- Node: `3664ad9cd1f892aab9ba933af92478e0eb2466e44d1394ea45c537d267436ced`;
- raw JSON: `535303371f70c2e0ed1dc9a6a232d57f12c1801b6a9f48f611147b93d1ab87ab`.

These finite controls verify the implementation and certificate semantics, not the asymptotic theorem.

## 9. B1/B2/B3 and fixed `R_mix341`

| Claim | Status |
|---|---|
| Haken unary PHP lower bound | KNOWN; ordinary shared-DAG Resolution only |
| Polynomial ER PHP proofs | KNOWN stronger-system escape |
| V + UB + LB + SAT-in-P four-way equivalence | PROVED/CONDITIONAL |
| PMin plus ordinary p-boundedness implies exact search | FALSIFIED without UB |
| Exact search yields same-language p-simulation | PROVED/CONDITIONAL |
| Witness-only external relation simulation | FALSIFIED / missing formula charge |
| Full `R_mix341` V and UB | OPEN; `LOCAL-CONVERT` payload grammar unresolved |
| PMin for fixed `R_mix341` | OPEN; exactly B3's missing consequent under SAT-in-P |
| B1, B2, B3 | OPEN |
| Superpolynomial `Wbar_Rmix341` | OPEN |
| P versus NP | OPEN |

If PMin were independently proved, it would already bound every `W_R(F)` by a polynomial in `|F|`, and hence imply the numerical consequents of B1 and B2. But this run assumes PMin inside the equivalence; it does not derive `SAT in P => PMin`. Therefore it does not prove B3.

The next decisive target remains authoritative full `R_mix341` syntax and polynomial minimum-cost normalization for every legal payload, especially `LOCAL-CONVERT`, followed by a noncircular attempt to derive or refute `SAT in P => PMin`. An exponential backtranslation, a succinct formula descriptor, or a short ideal DAG without paid bytes/access/verification/output is not such a bridge.
