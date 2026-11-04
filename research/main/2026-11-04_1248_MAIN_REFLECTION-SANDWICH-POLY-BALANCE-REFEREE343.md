# REFEREE343: reflection sandwich, quantifier correction, and polynomial-balance firewall

**November 4, 2026, 12:48 PST — PNP Independent Proof Red Team.**

**Status.** **PROVED/RESTRICTED:** the exact REF342 transparent reflection family is polynomially short in the unchanged fixed `R_mix341` iff the worst-case minimum `Wbar_Rmix341` is polynomial, with explicit cutoff rescaling. **PROVED/EXACT conditional:** polynomial certificate-bit balance plus `SAT in P` and polynomial `Wbar_R` yields one uniform polynomial-time exact minimum-proof extractor. **PROVED counterexamples:** one short nontransparent family, a lazy exponential source, and constant paid-node/unbounded-payload presentations do not yield B3 or machine bounds. **COMPUTATIONAL:** exhaustive SAT/UNSAT, malformed, parity, prefix-extraction, and packed-payload controls. B1, B2, B3, short mixed reflection, a superpolynomial mixed minimum, unrestricted SAT hardness, and P versus NP remain **OPEN**. No rule, weight, task, status, identity, schedule, or ownership boundary changed.

## 1. IDEA before search

Test whether REF342's transparent source retraction converts B3 into a strictly easier statement, or merely repackages the same missing consequent.

Initial proposed lemma: if the canonical universal reflection CNF `H_(A,N)` has polynomial encoded size and retracts with polynomial overhead to every valid UNSAT source `F` of length at most `N`, then polynomial `R_mix341` proof cost for `H_(A,N)` should be equivalent to polynomial `Wbar_Rmix341`. Falsifiable prediction: the reverse implication fails if the reflection object is implicit/exponential, if malformed or underclocked branches destroy coverage, or if the conclusion is incorrectly strengthened from proof existence to a uniform proof generator.

Four adversarial falsifiers were fixed before search:

1. unrelated short proofs hardcoded separately for each cutoff `N`;
2. the trivial short family `(z) AND (not z)` without family-wide source retraction;
3. an `N`-bit lazy descriptor for an explicit `2^N`-bit CNF;
4. a proof node with one unit of logical cost but an unbounded explicit payload.

## 2. SEARCH and the revision it forced

The abstract equivalence was already proved in
`research/main/2026-11-03_1048_MAIN_REFLECTION-FAMILY-EQUIVALENCE-REFEREE318.md`.
It is not new. REF318 left full-mixed restriction stability open. The actual increment available now is narrower and concrete: REF342 rebuilds the exact transparent evaluator source from `F`, alpha-renames proof-owned variables, and copies every downstream mixed node unchanged. That avoids a general restriction theorem for this one architecture.

Primary sources read:

- A. Haken, *The Intractability of Resolution*, TCS 39 (1985), DOI `10.1016/0304-3975(85)90144-6`.
- Cook--Reckhow, *The Relative Efficiency of Propositional Proof Systems* (1979), and Krajicek's exact Cook--Reckhow survey, <https://www2.karlin.mff.cuni.cz/~krajicek/cr.pdf>.
- J. Krajicek, *A Note on SAT Algorithms and Proof Complexity*, <https://www2.karlin.mff.cuni.cz/~krajicek/sat.pdf>. Its Theorem 2.1 assumes a decent proof system **and polynomial proofs of the algorithm's reflection formulas** before transporting a proof lower bound to rejection time; semantic correctness alone is not enough.
- P. Pudlak, *Reflection principles, propositional proof systems, and theories*, arXiv:2007.14835. It explicitly separates existence of short proofs from automatability.
- Atserias--Muller, *Automating Resolution is NP-Hard*, arXiv:1904.02991, used by LSPV-4/393 to calibrate proof search.

Actual general-web queries were `Krajicek A Note on SAT Algorithms and Proof Complexity D1 D4 PDF`, `Cook Reckhow p-bounded proof system NP coNP theorem primary paper PDF`, `Pudlak reflection principles propositional proof systems p-optimal proof systems arXiv`, and `Resolution automatizability P=NP shortest proof`. Direct branded Google UI was unavailable; general web search was used and this limitation is recorded rather than claiming a Google-specific run.

OpenAI GitHub queries were `SAT proof checker resolution verifier`, `Cook Levin proof system reflection`, and `SAT certificate verification`. They found no applicable `R_mix341` compiler or reflection-shortness theorem. The relevant current OpenAI result actually read was `openai/math/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026`: it claims a deterministic polynomial-space `#k-SAT` algorithm running in `(n+m)^O_k(1) 2^{n/(log n)^{1/2+o(1)}}` and explicitly distinguishes that machine upper bound from restricted regular-Resolution lower bounds. It is subexponential, not polynomial, and supplies no same-system proof simulation.

Current project reviews actually read:

- `GROKPROOF/2026-11-04_1518_PROGRESS.md`, blob `4e2bb9d941295f620a64e078117d29244caf4fba`: the arbitrary-decider, fully charged transformation remains OPEN.
- `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`, blob `79e4d4e7e0e3edff3aba8610852c45534bdde128`;
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`;
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`.

Claude's results concern world bookkeeping, restricted alternation-trading portfolios, and sequential/one-tape access. None supplies short mixed reflection proofs, random-access B3, or a uniform arbitrary-machine transfer.

Current five-role inputs were independently checked at:

- LSPV-1/396, `research/agents/lspv-1/2026-11-04_1100_LSPV-1_IMPLICIT_ROW_VALIDATION_FRONTIER396.md`, blob `0355068b61846e8e83f541e2719b9d2a9d243a8a`;
- LSPV-2/396, `research/agents/lspv-2/2026-11-04_1118_LSPV-2_SOURCE_SECTION_COST_REFLECTION396.tex`, blob `8aeb04e656b83fea41c00f23b73df80048dcd38c`;
- LSPV-3/400, `research/agents/lspv-3/2026-11-04_1124_LSPV-3_QUADRATIC_SHADOW_PORT_CERTIFICATE400.tex`, blob `078ce6de1b356481bfe7c943d5dfb481a6c3a1a6`;
- LSPV-4/393, `research/agents/lspv-4/2026-11-04_1136_LSPV-4_POLY_BALANCE_EXACT_OPTIMIZER393.md`, blob `c9fd526934b2d591522f54c0cd4ea7ee6a26dcfb`.

Their relevant conclusions are respectively: implicit all-row validity can be coNP-complete; Resolution source-section backtranslation may be exponentially costly; compact nonlinear circuit ports defeat auxiliary-free size measures; and proof existence becomes uniformly extractable only after polynomial bit balance is added.

## 3. Exact established lower-bound anchor

For `h+1` pigeons and `h` holes, the explicit unary pigeonhole CNF has variables `x_(i,j)`, pigeon clauses

`P_i = OR_(j=1)^h x_(i,j)`,

and collision clauses

`C_(i,k,j) = (not x_(i,j) OR not x_(k,j))` for `i<k`.

It has `h(h+1)` variables and `(h+1)+h*binom(h+1,2)` clauses. Under explicit ASCII DIMACS with binary-magnitude variable identifiers its encoded length is `N_h=Theta(h^3 log h)`.

Haken's theorem, in the exact model used here, is:

> There exist constants `c>0,h0` such that for every `h>=h0` and every ordinary unrestricted shared-DAG **Resolution** refutation `pi` of the explicit unary `PHP_(h+1)^h`, `pi` has at least `2^(c h)` lines.

The quantifier covers arbitrary legal Resolution pivots and DAG sharing. The system has authentic source clauses and ordinary Resolution only. It does **not** include extension variables, Extended Resolution, `Res(oplus)`, GF(2), circuits, semantic rules, `R_mix341`, or arbitrary SAT machines. In explicit encoded length the strength is `2^Omega((N_h/log N_h)^(1/3))`, only for this proof system and family.

Polynomial Extended-Resolution proofs of PHP are the mandatory escape. Odd expander Tseitin CNFs are likewise ordinary-Resolution hard, but the already certified connected odd cubic sources have a `4h-1`-node authenticated GF(2) proof in fixed `R_mix341`. No restricted lower bound transfers without a polynomial simulation in the correct direction.

## 4. ITERATE: exact reflection sandwich

Fix one uniform total correct clocked polynomial-time SAT decider `A`. It is fixed once; there is no per-`N` machine `A_N`. Let `H_(A,N)` be the canonical explicit REF342 reflection CNF covering all valid formula encodings of length at most `N`, with honest worst-case clock, exact validity gate, rejecting-run evaluator, and satisfaction evaluator. Let

`g_A(N)=|enc(H_(A,N))|`

and let `p_A(N)` be the paid source-retraction overhead. REF342 gives fixed polynomials `g_A,p_A`, independent of the source `F`, cutoff `N`, and selected proof.

Because correctness makes `H_(A,N)` a valid explicit UNSAT CNF and REF342 compiles **every** supplied mixed refutation of it to every valid UNSAT source of length at most `N`,

```
Wbar_R(N)
  <= W_R(H_(A,N)) + p_A(N)
  <= Wbar_R(g_A(N)) + p_A(N).                 (Sandwich)
```

The first inequality minimizes after compilation and then maximizes over `F`. The second merely inserts `H_(A,N)` into the cutoff at its **actual encoded length**. If `W_R(H_(A,N))<=C N^d` and `p_A(N)<=D N^e`, then `Wbar_R(N)=O(N^max(d,e))`. Conversely, if `Wbar_R(M)<=C M^c` and `g_A(N)<=D N^a`, then `W_R(H_(A,N))=O(N^(ac))`.

Therefore, for each fixed honest `A`,

`H_A has polynomial minimum R_mix341 proofs  <=>  Wbar_Rmix341 is polynomial`.

This is a proof-size statement:

`exists C,k  forall N  exists pi_N`.

The minimizing proofs may be unrelated across `N`; that does **not** falsify the theorem because `W` already grants per-instance existential minimization. Substituting those proofs as nonuniform advice into a decider would be invalid, but no proof generator is asserted.

### Exact B3 quantifiers

With the canonical family construction and source compiler available for every fixed qualifying machine,

```
B3
<=> for every fixed A,
    [A is a uniform total correct P-time SAT decider
     -> H_A has polynomial R_mix341 minima].
```

The superficially similar existential statement

`exists A [A is a P-time SAT decider AND H_A is short]`

equals `SAT in P AND Wbar_R polynomial`, not the material implication B3. If `SAT` is not in P, B3 and the universal formulation are vacuously true, while the existential statement is false. The finite truth-table control checked all four cases.

This localizes B3; it does not prove it. Correctness proves that `H_(A,N)` is UNSAT, not that it has short proofs.

### Both labels, malformed strings, and clock

- SAT-side correctness makes the reflection conjunction UNSAT: no valid SAT formula may have a rejecting run and satisfying witness.
- UNSAT-side completeness plus an honest clock is needed to specialize the universal evaluator back to every UNSAT source.
- Malformed strings are excluded by the exact charged validity gate; behavior of `A` on malformed strings is not silently treated as a source theorem.
- If a step-6 rejection is placed behind clock 5, the reflection formula can remain UNSAT while the source-coverage compiler fails. An underclock may also become outright unsound if timeout is encoded as rejection.

## 5. Counterexamples to weakened or physical claims

### 5.1 One short family is not enough

In ordinary Resolution, `H_N=(z) AND (not z)` has a one-node refutation for every `N`, while Haken's PHP family makes `Wbar_Res` superpolynomial. Hence shortness of an arbitrary uniform family says nothing. The required premises are the same explicit CNF grammar, polynomial actual length, cutoff-wide source retraction for every valid UNSAT `F`, and one fixed polynomial overhead independent of `F,N,pi`.

### 5.2 Lazy or exponential representation breaks polynomial rescaling

If an `N`-bit descriptor lazily denotes an explicit CNF of length `M(N)=2^N`, even `Wbar_R(M)<=M^e` yields only

`W_R(H_N)<=2^(eN)`.

Materialization and authentication cost `Omega(2^N)` output time. Calling the descriptor an ordinary CNF of length `N` changes the input/proof model. Exponential intermediate representations remain allowed, but their construction, bytes, access, verification, output, and peak live state must be charged. Compact XOR/circuit alternatives must be checked before claiming an intrinsic blowup.

### 5.3 Paid nodes do not dominate bytes or machine work

REF315's unresolved circuit-valued `LOCAL-CONVERT` syntax admits a two-paid-node skeleton with `2k+1` explicit gate records and `k` independently sensitive constant positions. Exact deterministic validation requires `Omega(k)` bit reads. Thus full `R_mix341` presently lacks a theorem `proof bits <= poly(source bits + paid nodes)`.

Shared logical DAG nodes are counted once, but physical reuse requires identifiers plus storage, retrieval, or recomputation. Streaming can lower peak storage while increasing rereads; it cannot erase bytes or validation. A deliberately delayed solver can take arbitrarily long with the same proof. A shortest logical DAG gives neither discovery time nor an FLMV time/space profile.

## 6. Conditional effective upgrade under polynomial balance

The nonuniform-minimum objection can be repaired, but only with an additional representation theorem.

Let fixed sound complete `R` have:

- `V`: one explicit uniform polynomial-time whole-certificate verifier;
- `PB`: one polynomial `b` such that whenever `W_R(F)<=q`, some cost-at-most-`q` proof has at most `b(|F|+q)` total encoded bits, including every payload and metadata field;
- `PMin`: one polynomial `P0` with `W_R(F)<=P0(|F|)` for every UNSAT `F`.

If `SAT in P`, one uniform polynomial-time algorithm outputs an **exact minimum-paid-cost** `R` refutation for every UNSAT input. For `B=b(N+P0(N))`, the predicate

`exists valid R proof y of <=B bits, cost <=q, extending prefix u`

is in NP. A fixed polynomial SAT decider therefore decides it uniformly. Binary-search the least feasible `q`, then choose each of at most `B` proof bits by prefix feasibility. This uses `O(log P0(N)+B)` polynomial-size queries. SAT inputs get a self-reduced and checked witness; malformed inputs are rejected.

This is LSPV-4/393's elementary conditional theorem, independently replayed here. It does not prove PMin/B3. Its significance is diagnostic: under `SAT in P`, existential shortness plus polynomial bit balance already yields a uniform proof generator. The current blockers are short same-system reflection and authoritative full-`R_mix341` payload normalization, not the granted after-the-fact minimum by itself.

Cook--Reckhow's theorem that **some** p-bounded proof system exists iff `NP=coNP` does not identify that system with fixed `R_mix341`. B3 needs this same fixed calculus.

## 7. Exact finite controls

Producer:
`experiments/arc/lspv5_343/reflection_balance_referee343.py`

Independent verifier:
`experiments/arc/lspv5_343/verify_reflection_balance_referee343.js`

Raw:
`results/raw/arc/2026-11-04_1248_LSPV5_343_REFLECTION_BALANCE.json`

The producer exhaustively checked all 256 CNFs over the eight nonempty non-tautological clauses on two variables:

- 95 SAT inputs had no Resolution refutation;
- 161 UNSAT inputs had exact minimum derived-node distribution `q=1:112`, `q=2:48`, `q=3:1`;
- a 44-bit fixed-width minimum proof was recovered by 7,084 prefix-feasibility queries;
- 644 malformed/corrupted certificate controls were rejected;
- odd/even-zero K4 Tseitin controls had `0/8` models;
- the four-row B3/universal/existential truth table passed;
- a packed-payload control held paid nodes at one while explicit payload grew from `2` to `65,536` bits.

The independent Node verifier passed 52 checks.

SHA-256:

- Python: `4eac88e4a3c50a79203bd211eafed0598cc6ba37bff2cbc03719e1219c978f32`
- Node: `17546e9b016cfe3c5411c9eeaa6e1e211b24973a31db6e9557611d3826aa96c7`
- raw JSON: `dfb3935a8679fd0eaa99bbf71c066389aaa139bc3046dc73b69d9f464465e0e6`

Finite controls certify the implementation and quantifier bookkeeping, not asymptotic proof complexity.

## 8. B1/B2/B3 ledger and next gap

| Claim | Status |
|---|---|
| Haken PHP lower bound | KNOWN, ordinary shared-DAG Resolution only |
| REF342 full-mixed source compiler for exact pin/mux family | PROVED/RESTRICTED |
| Reflection sandwich for that family | PROVED/RESTRICTED |
| One arbitrary short family implies B3 | FALSIFIED |
| Lazy descriptor length may replace explicit cutoff length | FALSIFIED / model type error |
| Polynomial paid nodes imply polynomial bytes/runtime | FALSIFIED for unresolved payload syntax |
| PB + PMin + SAT-in-P gives uniform exact proof extraction | PROVED/CONDITIONAL |
| SAT-in-P gives short `R_mix341` reflection proofs | OPEN; exactly the missing B3 consequent |
| B1, B2, B3 | OPEN |
| Superpolynomial `Wbar_Rmix341` | OPEN |
| P versus NP | OPEN |

The next decisive obligation is not another hard formula. It is either:

1. prove authoritative polynomial certificate-bit normalization for every legal full-`R_mix341` record and then prove short canonical reflection under `SAT in P`; or
2. exhibit a sound full-rule counterexample showing that no such normalization or reflection compiler follows from the present calculus.

Any physical theorem must separately charge explicit/lazy source construction, representation conversion, bit access, update, proof construction, output, verification, shared-DAG scheduling, and peak space. An exponential backtranslation is not evidence of superpolynomial machine hardness.

