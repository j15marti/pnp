# TMR-5/021: MCSP magnification redteam, exact two-state uniformization counterexample

**Pacific time:** 2026-11-14 09:53 PST (America/Los_Angeles). **Role:** TMR-5 Machine Bottleneck Redteam and synthesis. **Status:** new diagonal theorem PROVED/RESTRICTED by complete elementary argument, independent peer review requested; finite tests COMPUTATIONAL. **P versus NP:** OPEN. No task or schedule changes.

## 1. Preflight, original ledger, and provenance

Read the latest authoritative `research/coordination/2026-11-14_MCSP_FIVE_AGENT_REVIEW.md` FIRST (Git blob `1e11aa64a0b0d635a65cea58500b09f2b0fe010a`, rechecked before writes), followed by the 2026-11-13 TMR replacement, root `AGENTS.md`, `CODEX.md`, repository research skill, both root proof trackers, complete canonical `main.tex`, latest issue #3 comments, and all five role handoffs. The contents API returned SHA but empty bodies for `proof2.txt` and `main.tex`; authentic `fetch_blob` recovered **1,051,196** and **2,545,859** UTF-8 characters respectively. No empty body was treated as an empty stored file. Root `proof1.txt` was fully fetched (28,714 characters).

Original relevant ledger:

| Artifact | Original location | Verified scope and status |
| --- | --- | --- |
| TMR-1/023 parameter shell | `research/agents/tmr-1/2026-11-14_0908_TMR1_MCSP_PARAMETER_SHELL023.md` | CANDIDATE/RESTRICTED counting proof: distinct MCSP circuit thresholds define distinct languages; not a decision-time lower bound or a no-reduction theorem. |
| TMR-2/024 residual width | `research/agents/tmr-2/2026-11-14_0927_TMR2_MCSP_RESIDUAL_WIDTH024.md`, `experiments/tmr/tmr2_sparse_residual024.py` | CANDIDATE/RESTRICTED: at most M+1 exact residuals for a length-N language with M accepted words; nonuniform state bound, not a uniform transition compiler. Independently audited and sharpened here. |
| TMR-3/024 processor network | `research/agents/tmr-3/2026-11-14_0936_TMR3_MCSP_FIXED_NETWORK_SERIALIZATION024.md`, `experiments/tmr/tmr3_mcsp_network024.py` | CANDIDATE/RESTRICTED: fixed p, shared one-way source, R-round network serializes in O_p(R²); derived exponent .995 is weaker than mandatory R≥N source ingestion. No polynomial-p or unrestricted multitape bridge. |
| TMR-4/023 moment compiler | `research/agents/tmr-4/2026-11-14_0836_TMR4_MOMENT_CONGRUENCE_AND_QUOTIENT_COUNTEREXAMPLE023.md` | CANDIDATE/RESTRICTED exact semantic continuation; does not implement general machine transitions or a truth-table reduction to MCSP. New MCSP role artifact not yet present in reviewed handoff. |
| TMR-5/020 algebraic cancellation | `research/agents/tmr-5/2026-11-14_0858_TMR5_GF4_CANCELLATION_MOMENT_TRACE020.md` | CANDIDATE/RESTRICTED SAT/UNSAT same-field-point collision and equal moment/different physical-runtime counterexample. |
| Prior threshold analysis | `research/main/2026-10-18_ASYMPTOTIC_CONE5.md`, `research/agents/chmy-threshold/2026-10-21_0612_CHMY_BRIDGE33_HANDOFF.md` | CONDITIONAL exponent/parameter descent; identifies simple padding slope loss and small-parameter gap, no unconditional descent. |
| Claude original | `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex`, and `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex` | Restricted sequential-input/crossing and prescribed alternation-trading frameworks, no general SAT bridge. |
| Historical controls | `research/agents/threshold-descent/2026-10-20_1700_MCSP_SPARSE_TEMPLATE_KT_FIREWALL1.md`, `research/agents/magnification-redteam/2026-10-18_1919_MAGRED_STREAM_NO10.md`, `research/agents/tmr-2/2026-11-14_0823_TMR2_MAXSAT_WALSH_SIGN_ROBUSTNESS022.md` | Compact representations and genuine failed YES preservation under selected sampling; not removable by declaring real counterexamples spurious. |

Additional original TMR code/raw inspected via peer handoffs and reports. No native replay of peer source is claimed. This run uses an independently authored native CPython check for the exact residual assertion, not a wrapper around peer code.

## 2. Primary source theorem matrix and exact mismatch

Let N=2^n be a full truth-table input, n its Boolean input arity, and L an independent encoded SAT formula size. MCSP[s(n)] means ordinary EXACT decision over N-bit truth tables, with circuit size threshold s(n), not search-MCSP or a promise problem.

| Original source, pinpoint | Model, input, thresholds, quantifier and conclusion |
| --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, Theorem 1, printed p. 23:3 | For some **small fixed** mu1>0, **if** ordinary MCSP[2^(mu1 n)] is not in deterministic one-way read-only input plus one two-way work-tape TIME O(N^1.01), **then** P != NP. Uniform, both-label decision; conditional magnification. |
| Same, Theorem 2, printed p. 23:3 | For **some different mu2 close to one**, ordinary MCSP[2^(mu2 n)] is not in bounded-two-sided-error randomized one-way-input one-work-tape TIME O(N^1.99). Unconditional, but mu2>mu1. Does **not** satisfy Theorem 1's small-threshold hypothesis. |
| Same, Theorem 3, printed p. 23:4 | For every fixed 1/2<mu<1, an arbitrary-oracle one-work-tape machine with only N^o(1)-length oracle queries still suffers N^(1+mu') lower bound for some mu'>0. It forbids the proposed short-query magnification method at high threshold, not every conceivable higher-threshold magnification argument. |
| Same, Theorems 4-5, printed pp. 23:4-5 | MKTP has deterministic/nondeterministic/parity branching-program bounds (including Omega(N²/log²N) for deterministic and Omega(N^1.5/logN) for nondeterministic/parity); MCSP BP size N^(1.5-o(1)) in stated nondeterministic/co-nondeterministic/parity models. Different input representation/model from a uniform multitape decision-time bound. |
| McKay, Murray, Williams, STOC 2019, Theorem 1.2, printed p. 3 | On an explicit N=2^n truth table, **search-MCSP^A[s(n)]**, with A oracle gates, has a one-pass streaming procedure with Sigma3SAT^A oracle calls of length tilde-O(s), tilde-O(s) space, tilde-O(s²) update time; s(n)>=n time-constructible. Not an unconditional ordinary decision upper bound without oracle-cost replacement. |
| McKay, Murray, Williams, STOC 2019, Theorem 1.3, printed p. 3 | If for some time-constructible s>=n and A in PH **search-MCSP^A[s]** lacks polynomial-in-s space and update-time streaming algorithm, P != NP. Conclusion conditional, search/oracle formulation retained. |
| Chen et al., ITCS 2020, abstract and locality-barrier result | Certain magnification approaches admit small fan-in oracle algorithms, and corresponding lower-bound methods can extend to those oracles. This is a proof-method limitation, not an impossibility of P != NP. |
| Oliveira, Pich, Santhanam, Theory of Computing 17 (2021), article 11 | Gap-MCSP/MKtP have distinct YES/NO size thresholds and nonuniform hardness-magnification consequences; exact threshold and model must be rechecked before applying them. No transfer from ordinary one-work-tape decision has been established here. |

Primary URLs: STACS DOI https://doi.org/10.4230/LIPIcs.STACS.2021.23 ; original MMW STOC https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf ; Chen et al. https://doi.org/10.4230/LIPIcs.ITCS.2020.70 ; OPS https://doi.org/10.4086/toc.2021.v017a011 . We directly examined STACS's printed Theorems 1-5 and MMW's Theorems 1.2-1.3; OPS finer theorem variants are not invoked as premises of a new result.

## 3. NEW result: TWO-STATE-DIAGONAL-025

**Theorem (PROVED/RESTRICTED, independent review requested).** There exists a **decidable**, fully uniform language D over binary strings satisfying:

1. For every input length N>=1, D contains **exactly one** accepted N-bit word.
2. At **every cut**, D's length-N slice has at most **two** exact right-residual languages. Thus an exact deterministic *nonuniform* length-N ordered read-once branching program has width at most two and size O(N), preserving both labels.
3. Nevertheless, D is **not in P**, so no fixed finite uniform deterministic polynomial-time machine can compute all its slices.

**Proof.** Effectively enumerate every pair (M_i,k_i) consisting of a deterministic Turing machine and a positive integer clock exponent; duplicates are harmless and each pair occurs at some index i. For each N>=1 let j=nu_2(N), the exponent of the largest power of two dividing N. Define a unary predicate H on 1^N by simulating M_j on 1^N for N^(k_j) steps and outputting the **complement** of its acceptance bit; an over-clock or malformed computation is treated as nonacceptance. This definition always halts because the simulation clock is finite, so H is decidable by one uniform algorithm.

If H were decided by a fixed polynomial-time M in at most C N^k steps, choose j indexing (M,k+1). Infinitely many arbitrarily large N satisfy nu_2(N)=j, and for all sufficiently large such N, C N^k <= N^(k+1). On each of these lengths, the defining algorithm contradicts M's output. Hence H is not in P.

Let b_N=H(1^N), and define D intersect {0,1}^N to contain precisely the constant word b_N^N. D is decidable: compute b_N and compare each of the N input bits with b_N. If D were in P, H would be in P by evaluating D on 1^N (which is accepted iff b_N=1), a contradiction. For any fixed N and prefix cut d, a prefix matching b_N^d has a singleton accepted suffix {b_N^(N-d)}; every other prefix has the empty suffix set. Therefore exact width is <=2, with a match/dead deterministic transition automaton. Both terminal labels are exact. QED.

**Interpretation:** Theorem 2 falsifies any proposed inference **small exact prefix width => efficiently uniformizable residual updates** even when the entire language is decidable and has a single YES word per length. Its per-length transition rule needs nonuniform knowledge of b_N; the theorem does NOT establish any actual lower bound for MCSP, which is a specific uniform decidable language. It strengthens the scope firewall in TMR-2/024 by providing an unconditional *decidable*, rather than merely unknown or uncomputable, counterexample to uniformization from width alone.

## 4. Independent computation

**Exactly executed locally in native CPython 3:** `experiments/tmr/tmr5_mcsp_uniformization025.py` (the 3,018-byte published source had Git blob SHA `bd417d4869c7f3d5cc6adc4164ac840b6b9bef41`, identical to the natively executed local `git hash-object`). The exact all-YES-set residual verifier enumerated **65,812 languages** for word lengths N=1..4, checked **1,969,768** two-bit successor relations and all size upper bounds, with zero assertion failures. The maximum width over all languages at N<=4 was 4. A separate 128-length toy diagonal controller verified disagreement with its selected toy algorithm and eight length-N singleton width-two controls; it does not instantiate the infinite universal construction or demonstrate asymptotic complexity. Original CPython stdout JSON was normalized on publication; all numeric fields are preserved.

**Limits:** Finite verification is COMPUTATIONAL. The theorem itself follows from the explicit diagonal proof; the toy diagonal is not being substituted for that proof. There is no native execution of arbitrary full MCSP or of other roles' complete tests in this run.

## 5. Integrated implication graph and hostile route retirements

```text
CHMY known: MCSP[N^mu2], large mu2, no one-work-tape N^1.99
    |
    | MISSING: threshold-descent keeping exact YES+NO labels,
    |           same N and one-work-tape interface, charged time
    v
CHMY required: MCSP[N^mu1], small mu1, no N^1.01
    |   [conditional CHMY Theorem 1]
    v
P != NP  [OPEN]

TMR-2: sparse YES set -> small nonuniform residual width
    |   X (TWO-STATE-DIAGONAL-025 disproves generic uniformization)
    v
poly-time uniform MCSP streaming updates [OPEN]

TMR-3: fixed p, one-way stream, R rounds
    |   O_p(R²) serialization
    v
one-work-tape bound -> only R not O(N^0.995)
    |   X (already weaker than R >= N source scan)
    v
unrestricted multitape SAT lower bound [OPEN]

TMR-4: SAT description / Walsh moments -> explicit MCSP table
    |   X (N=2^n writing cost, no free expansion;
    |      different source and target languages)
    v
charged, both-label, promise-preserving reduction [OPEN]
```

**Rank by the weakest unresolved arrow, not theoretical ambition:**

1. **High priority:** Build or refute one explicit *exact same-variant* threshold-descent map for ordinary MCSP, with both-label preservation and a fully charged one-way-input, one-work-tape compiler. Show precisely which size threshold is reduced and retain the hardest-instance length range. Historical ASYMPTOTIC_CONE5 already retires ordinary padding as slope amplification, so do not relabel it a new route.
2. **Medium priority:** Directly prove the *small-threshold* streaming/search-MCSP resource lower bound needed by MMW Theorem 1.3. A width or entropy bound is insufficient by TWO-STATE-DIAGONAL-025; the real target is uniform representative-update complexity in the oracle/search model.
3. **Conditional exploratory:** New cost-sound direct SAT-to-MCSP reductions only if source length L, truth-table length N, circuit thresholds, promises and finite-work-tape simulation are fixed explicitly.
4. **Retire as primary paths:** Fixed-p quadratic serialization (after exponent division it gives less than mandatory scan), unlabeled semantic multiplicity, nonuniform residual width, uncharged full truth-table expansion, conflating MKTP/Gap-MCSP with ordinary MCSP, and simply moving the one-tape exponent across different circuit-size thresholds. Preserve all their valid restricted evidence.

### Exact remaining general-machine gap

Even a valid lower bound `MCSP[N^mu]` outside one-work-tape TIME N^1.01 is not itself a lower bound on arbitrary multitape 3-SAT; the chain depends on the **conditional** hardness-magnification implication for the exact small threshold. No fixed correct 3-SAT decider's arbitrary polynomial-time exponent has been excluded. The required all-exponent quantified statement over one A and valid F remains OPEN.

## 6. Next action and peer review

**Concrete next target:** TMR-1 should extract the precise admissible mu1 from the original MMW/CHMY simulation and its one-tape source/query charges; TMR-3 should derive a model-exact threshold transfer budget, and TMR-4 should design a both-label truth-table threshold gadget or a decisive counterexample. **Peer request:** TMR-2 independently verify TWO-STATE-DIAGONAL-025's uniform decidability and non-P diagonal indices, and TMR-1 inspect quantifiers. No general MCSP lower bound follows from the two-state result.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both complete root trackers recovered; no new premise justifies promoting the P=NP or P!=NP chain. Canonical `main.tex` should receive only a scoped CANDIDATE/RESTRICTED synthesis notice after independent peer review, not a theorem promotion; no authorized shared proof-status change was made here. No task was created, disabled, revived or modified.
