# END-TO-END-SIGN-ACQUISITION-REFEREE329

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 3, 2026, 21:48 PST**

**Status:** PROVED/EXACT tight randomized canonical-source acquisition theorem; PROVED/EXACT counterexample to arbitrary supplied-representation invariance; COMPUTATIONAL finite controls. B1, B2, B3, a superpolynomial lower bound for fixed `R_mix341`, unrestricted SAT hardness and P versus NP remain OPEN. No task, schedule, state, identity, ownership boundary, calculus rule or weight was changed.

## Outcome first

There is one robust end-to-end invariant on the established sign-sensitive minimally-UNSAT families, but it is deliberately modest. If an explicit canonical source has `L` independent occurrence-sign fields, the center is UNSAT, every single-sign neighbor is SAT, and one paid physical probe exposes at most `kappa` sensitive fields, then every one fixed adaptive randomized all-input SAT pipeline with worst-case error `epsilon < 1/2` satisfies

`E[probes on the UNSAT center] >= (1-2 epsilon)L/kappa`.

This survives arbitrary adaptive preprocessing, compact circuits, GF(2), auxiliary definitions, shared DAGs, caching, lazy access, rereads and early stopping **when every original-source access across the whole pipeline is charged**. The coefficient is exact.

The stronger representation-independent candidate fails. Under the invertible linear recoding

`y_1 = x_1 xor ... xor x_L`, and `y_j = x_j` for `j >= 2`,

the star label is exposed by one supplied coordinate. Computing or validating this recoding from the canonical source still pays the source-acquisition lower bound; receiving it as trusted input changes the grammar/model. Thus the surviving theorem is end-to-end and source-relative, not an intrinsic invariant of an abstract signed hypergraph under arbitrary supplied encodings.

It is only linear, gives no linear writable-space bound, and supplies none of B1/B2/B3. This is a concrete proved theorem and a concrete counterexample, not P != NP.

## Established hard-family anchor: exact model and strength

Haken's 1985 lower bound is for the standard unary pigeonhole CNF `PHP(h+1,h)` in **ordinary unrestricted shared-DAG Resolution**. The explicit formula has:

- variables `p_{i,j}` for `h+1` pigeons and `h` holes: `h(h+1)` variables;
- `h+1` pigeon clauses of width `h`;
- `h * binom(h+1,2)` binary collision clauses;
- `L = h(h+1)^2 = Theta(h^3)` independently serialized literal-occurrence signs;
- explicit signed DIMACS length `N = Theta(h^3 log h)` under ordinary binary/ASCII variable identifiers.

For all sufficiently large `h`, every ordinary Resolution refutation has at least `2^(c h)` lines for some constant `c>0`. The quantifier is over every Resolution refutation of every sufficiently large member of this fixed family. It is not an Extended Resolution, Res(XOR), `R_mix341`, semantic-proof or arbitrary-machine SAT lower bound. [Haken 1985](https://doi.org/10.1016/0304-3975(85)90144-6).

Standard unary PHP is clause-minimally UNSAT. Deleting a pigeon clause permits leaving that pigeon unassigned while matching the others. Deleting one collision clause permits exactly its pigeon pair to share that hole while the remaining pigeons occupy distinct holes. Therefore the sign-star lemma below applies. Importantly, the present acquisition theorem uses only this minimality, not Haken's exponential Resolution lower bound.

Mandatory controls remain:

- Extended Resolution/Frege can abbreviate and bypass the ordinary-Resolution lower bound;
- odd cubic Tseitin CNFs can be Resolution-hard yet have linear authenticated GF(2) refutations in `R_mix341`;
- LSPV-3/383 gives a signed-profile family with exponential monotone-circuit complexity but a uniform polynomial-time matching algorithm.

No exponential-overhead backtranslation is used as evidence of machine hardness.

## Lemma 1: authenticated sign star

Let `F = AND_j C_j` be clause-minimally UNSAT. Use a fixed injective binary source grammar in which every ordered literal occurrence has its own sign field, separate from its variable identifier and all structural fields. Let `L` be the number of occurrences.

For every occurrence `i` in clause `C_j`, minimality supplies an assignment `a_j` satisfying `F \ {C_j}`. Because `F` is UNSAT, `a_j` falsifies every literal of `C_j`. Flipping sign `i` makes that one literal true while preserving every other clause, so the same-length neighbor `F^(i)` is SAT.

The source-rooted semantic certificate may share one deletion witness `a_j` across all occurrence mutations in clause `C_j`. It must also contain or reference a sound refutation of the center; deletion witnesses alone do not prove the center UNSAT. Mutation records must authenticate exact byte/field equality except for one named sign. Malformed IDs, multiple changes, shared sign fields, invalid witnesses and invalid refutations are rejected.

Variable-length textual minus signs are not literal one-bit neighbors without normalization. The theorem is stated for the fixed direct binary grammar, not for arbitrary serializations.

## Lemma 2: tight adaptive randomized end-to-end acquisition

Fix one classical randomized, total, uniform algorithm `A`, correct on all valid SAT and UNSAT encodings and malformed strings. Its preprocessing, compilers, representation switches, solver and checker are one charged pipeline. Couple its runs on `F` and `F^(i)` with the same infinite random tape.

Let the center SAT-error be at most `alpha`, and leaf `i`'s UNSAT-error be at most `beta_i`. Let `Q_i` be the event that the complete center execution reveals source sign `i`. Until `i` is revealed, the two coupled transcripts and future adaptive choices are identical. If `i` is never revealed, the outputs agree. With `U,U_i` the two UNSAT-output indicators,

`|U-U_i| <= 1[Q_i]`.

Therefore

`Pr_F[Q_i] >= E|U-U_i| >= |E U - E U_i| >= 1-alpha-beta_i`.

Summing gives the exact general form

`E[distinct sensitive signs read] >= sum_i max(0,1-alpha-beta_i)`.

For two-sided error at most `epsilon < 1/2`, this is `(1-2 epsilon)L`. For a probe that reveals at most `kappa` sensitive fields, linearity and packing give

`E[probes] >= (1-2 epsilon)L/kappa`.

For a fixed word partition, if `J` words contain at least one sensitive sign, the stronger bound is `(1-2 epsilon)J`, hence at least `(1-2 epsilon)ceil(L/w)` when a word holds at most `w` signs. Zero-error/Las Vegas gives `L/kappa`; one-sided error gives `(1-epsilon)L/kappa`.

### Exact tightness

Choose one uniform exact total SAT decider `D` that deliberately scans the whole canonical input before deciding. Run `D` with probability `1-alpha-beta`, output SAT blindly with probability `alpha`, and output UNSAT blindly with probability `beta`. This is one uniform globally correct randomized decider with the declared per-input errors and expected center acquisition exactly `(1-alpha-beta)L` signs (or the corresponding occupied-word count). The exact branch may be exponentially slow, so this proves tightness only for acquisition, not total SAT time.

Worst-case per-input correctness is essential. Under the uniform distribution on the `L+1` star points, the zero-query algorithm that always outputs SAT errs only with average probability `1/(L+1)`. An UNSAT-only promise likewise admits a zero-query hardcoded answer. Both-label, per-input correctness creates the bound.

## Lemma 3: arbitrary supplied recoding destroys coordinate invariance

For `x in {0,1}^L`, define an invertible GF(2) change of basis by

`y_1 = xor_i x_i`, `y_j=x_j` for `j>=2`.

The inverse is `x_1 = xor_i y_i`, `x_j=y_j` for `j>=2`. Relative to the central codeword, every one-coordinate flip in `x` toggles `y_1`; hence the star label is decidable from the first supplied recoded bit. Deterministic query cost is one, not `L`.

More generally, if recoded neighbor `i` differs from the center on target-coordinate set `D_i`, coupling forces only `Pr[query intersects D_i] >= 1-2epsilon`. The generic invariant is a hitting/cover quantity of the `D_i`, which arbitrary invertible coding can reduce to one. A compact fixed-graph Tseitin grammar similarly exposes only `h` charge bits rather than `12h` expanded occurrence signs; Gray coordinates can change the relevant coordinate count and layout.

This does not evade the end-to-end theorem. Producing or validating `y_1` from the explicit source must acquire every pivotal source sign. A free trusted syndrome, digest, preprocessed cache or parity oracle is extra advice/model power. An untrusted digest cannot be accepted without source authentication on both labels.

Consequently:

- internal exact representations are harmless when source reads are charged;
- a solver handed only an already-compiled object has no raw-source query lower bound;
- a lazy conversion postpones but does not erase first authentication;
- extension variables and compact circuits compute derived values but do not assert a trusted value;
- a short generator seed invalidates independent-coordinate premises and must be analyzed in seed coordinates.

## Physical cost ledger

The theorem charges source acquisition across all phases. It does not identify ideal derivation nodes with native runtime.

| Cost | What is proved or required |
|---|---|
| Source bit/field access | Exact expected lower bound above |
| Word access | Exact fixed-partition bound, or `L(1-2epsilon)/kappa` for bounded exposure |
| Intermediate encoded length | Must be counted; exponential objects are allowed at actual length |
| Construction/conversion | Must include all source reads and emitted bits |
| Update/cache/reread | First authentication is unavoidable; repeats and recomputation are separately charged |
| Verification/output | Not bounded by logical node count; must be serialized and checked |
| Peak writable space | No linear lower bound follows; streaming can use `O(w+log L)` bits plus solver state |
| Offline XOR trace | Diagnostic only unless the solver pays to acquire and compute it |

For ordinary word size `w=Theta(log N)`, the PHP consequence is at most a near-linear `Omega(N/log^2 N)`-scale word-access floor under the stated encoding conventions, and the bit-field statement is `Omega(L)=Omega(N/log h)`. Exact constants depend on field layout. In every case the result is polynomially bounded by the input length.

## Four falsifiers and verdicts

1. **Internal compact representation beats acquisition.** FALSIFIED when canonical-source reads across construction and solving are charged; GF(2), circuits and laziness are downstream of the same transcript.
2. **The sign count is invariant under arbitrary supplied encodings.** FALSE. The invertible parity-coordinate encoding makes the supplied-star query cost one.
3. **Linear acquisition implies linear writable space.** FALSE. A streaming scan can use `O(w+log L)` writable bits, paying time/rereads instead.
4. **The acquisition floor proves B1/B2/B3 or P != NP.** FALSE. It is a lower bound on machine access, whereas B1/B2/B3 require an upper simulation of `W_R` by machine time; reversing the inequality is invalid.

Additional firewall: clause minimality is necessary. `(x) AND (not x) AND (y)` remains UNSAT when the `y` sign is flipped. Average-error guarantees are also insufficient, as the zero-query star distribution example shows.

## B1/B2/B3 classification

For the same fixed `R_mix341`:

- **B1** asks, for every one fixed uniform total correct exact SAT decider `A`, for a polynomial upper simulation `W_R(F) <= p_A(|F|+T_A(F))` on every UNSAT `F`.
- **B2** asks `Wbar_R(N) <= p_A(N+T_A^wc(N))` for all `N`.
- **B3** asks `SAT in P => Wbar_R(N)` polynomial for this same fixed calculus.

All remain OPEN. The theorem gives a lower bound on `T_A(F)` and no proof-producing translation. Its randomized formulation also does not silently replace the exact deterministic quantifiers in B1--B3; a randomized bridge would need its own expected/worst-coin time definition and simulation theorem. A fast algorithm for this recognizable family would not settle worst-case B2/B3.

Horn chains and odd Tseitin formulas show why the measures are separate: both can have maximal local sign sensitivity and short mixed proofs. Conversely, Haken's PHP Resolution lower bound supplies no arbitrary-machine lower bound without a polynomial-overhead simulation into Resolution, which is not available.

## Literature, project, Grok and Claude review

The coupling is an elementary classical randomized-query argument, not a novelty claim. Related primary sources include Yao's minimax principle ([FOCS 1977](https://doi.org/10.1109/SFCS.1977.24)), Nisan's decision-tree results, and Jain--Zhang's influence/query-elimination framework ([Theory of Computing 2011](https://doi.org/10.4086/toc.2011.v007a010)). None is used to inflate the scoped theorem.

Direct predecessors actually read:

- LSPV-4/347, `research/agents/lspv-4/2026-11-02_1836_LSPV-4_RANDOMIZED_CERTIFICATE_SENSITIVITY347.tex`, blob `86ee1b9a7a1a559307bc7be00ef29d0db79c2e77`: same-certificate randomized-verifier sensitivity. REFEREE329 extends the coupling to one actual end-to-end decider pipeline and proves exact acquisition tightness.
- LSPV-3/377, `research/agents/lspv-3/2026-11-03_1551_LSPV-3_SIGNED_INPUT_QUERY377.tex`, blob `66e7817366e8d6039d8dedd1aebb954a7872ec58`: deterministic all-stage signed-input conservation.
- LSPV-2/373, `research/coordination/2026-11-03_1612_LSPV2_SYNDROME_COORDINATE_COLLAPSE373_FIVE_ROLE_HANDOFF.md`, blob `0f5f3999...`: supplied syndrome coordinates collapse query depth, while construction reads the source.
- LSPV-4/374, `research/coordination/2026-11-03_1836_LSPV4_RANDOMIZED_SAT_LATE_INDEX374_HANDOFF.md`, blob `47fd3896d64a6ca23e231a3815a702643ced89d6`: one-pass INDEX-space route is defeated by rereads.

Current five-role handoffs read:

- LSPV-1/379: `research/coordination/2026-11-03_2100_LSPV1_MULTIWIRE_EXTENSIONAL_QUOTIENT379_FIVE_ROLE_HANDOFF.md`, blob `6c52aaf76954079b1b8a8106ce9dc0fdc3ca2cef`;
- LSPV-2/379: `research/coordination/2026-11-03_2112_LSPV2_PAID_TERNARY_BANK379_FIVE_ROLE_HANDOFF.md`, blob `0ce12435c61d6165b2df1c860a7a0acf1b36b6f6`;
- LSPV-3/383: `research/coordination/2026-11-03_2124_LSPV3_MONOTONE_MATCHING_SIGN_PROFILE383_FIVE_ROLE_HANDOFF.md`, blob `808d798d0bc111af39b869ae7b3a94c72aeb8354`;
- LSPV-4/377: `research/coordination/2026-11-03_2136_LSPV4_CUT3_BANK_EXTRACTION377_HANDOFF.md`, blob `894d139c89d7ba408a338d12daf520a186b57062`.

Current Grok `GROKPROOF/2026-11-04_0513_PROGRESS.md`, blob `085e27e9984a46697556125c37beb18d4eea7113`, explicitly leaves the universal fully charged all-input transformation OPEN. Claude files actually read were `research/agents/claude/2026-09-30_CLAUDE-0266_review.tex` (`694c1c8169d9a193397b94e6ee572c476e639a94`), `2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex` (`95c2649b29ae7efac79e9400effffd2c3bdeb2fc`), `2026-10-28_1452_CLAUDE_TPORT-0002.tex` (`1f9fc727d3e2b009cba7afec2a93beb62959dd67`) and `2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (`9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`). They respectively warn against representation-invariant influence claims and prove only restricted direct-product/portfolio/sequential-tape statements. None supplies B1, B2 or B3.

Scoped `github.com/openai` searches found no relevant randomized decision-tree/SAT-query implementation; absence is not novelty evidence.

## Finite replay

The producer checked nine Horn-chain centers (`m=2..10`) and all 90 sign-flip neighbors; three unary PHP centers (`h=1..3`) and all 70 sign-flip neighbors; exact parity recoding/inversion; tight randomized mixtures for five errors and five lengths; packed-probe arithmetic; eight malformed records; and K4 odd/even both-label controls (`0/8` models). It made **445 assertions**. A separately written Node verifier made **72 assertions**. The replay used 9,216 KiB peak RSS and about 0.50 seconds on the recorded host; these are experimental upper costs, not lower bounds.

Artifacts:

- `experiments/arc/lspv5_329/end_to_end_sign_acquisition_referee329.py`
- `experiments/arc/lspv5_329/verify_end_to_end_sign_acquisition_referee329.js`
- `results/raw/arc/lspv5_329/end_to_end_sign_acquisition_referee329.json`

## Exact next gap

The raw-coordinate count cannot be promoted to an invariant of arbitrary supplied representations. The next viable target is a **source-authenticated** invariant stronger than linear acquisition, or a direct B3 simulation theorem for fixed `R_mix341`, with polynomially bounded proof serialization and checker overhead. Any proposal must survive compact parity bases, total conservative definitions, private/shared circuits, lazy access, rereads, streaming and direct family recognition. Until such a theorem is proved, this run establishes an exact linear firewall and its exact representation limit—nothing superpolynomial.

P versus NP remains **OPEN**.
