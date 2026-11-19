# Claude lane: audit of the "Dual Proof Attempts" Google Doc against primary sources | 2026-11-19 09:48 PST

Lane: Claude scheduled routine (research/agents/claude/). This is not a TMR-1..5 run. No TMR manuscript, handoff, retired tracker (proof*.txt) or historical main*.tex was read for writing or modified. Repository base d55630ca024a4af03e8451ee77f4ddf757927393. P versus NP remains OPEN. Nothing here promotes any theorem.

## Source reviewed

Google Doc 1b2SYjJJJVjMwap-5wURTFbUMn212lwFnYhq2k5Sqdds, "Dual Proof Attempts for P = NP and P != NP" (about 62.6 kB of text, fetched 2026-11-19 through the Drive connector). Read coverage: sections 1, 2.1, 2.2, the 3.2 diagnosis, 3.3 and 4 were read in full. The section 2.3 (IPS synthesis), 3.1 (GCT) and 3.2 construction bodies were only skimmed. No claim about those parts is made here.

The doc is a literature survey that frames each attempt as "construction, then exact breakdown". It contains no new lower bound for SAT. Its value to this repo is that it contains checkable claims. Four of them were checked.

## Candidate and falsifiers (stated before search)

Candidate (from doc 2.2): "For exact contraction of the 3-SAT tensor network, the minimal bond dimension along any contraction order is lower-bounded by 2^Omega(tw(G)), where G is the incidence graph."

Falsifiers that were set up in advance:
1. A family with tw(G) = Theta(n) whose exact contraction has polynomial (or constant) bond dimension.
2. Instances where the cut-rank depends on the field (GF(2) versus Q).
3. Instances where the cut-rank is far below 2^(cut) even though tw is high.

## Findings

### F1. Doc 2.2 graph-only tensor-network lower bound: FALSIFIED as stated (PROVED/EXACT, elementary; not independently reviewed)

The construction works for every graph H on n vertices. Take any monotone 3-CNF whose primal graph is H, so tw(primal) = tw(H), which can be Theta(n) for expanders. Then add the unit clauses (x_i) for all i.

Contract in this order. First absorb each unit-clause tensor into its variable copy tensor. Each copy tensor then becomes the product vector e_1 tensored over its legs. After that, every intermediate tensor in any contraction order is a tensor product of e_1 and/or scalar factors, so every bond has dimension 1. Equivalently, the solution indicator is a point function, and its matricization has rank 1 across every bipartition.

So exact contraction with maximum bond dimension 1 exists while tw = Theta(n). No lower bound that depends only on the graph can hold.

The correct and known statement depends on the function. At a cut of a contraction tree, an exact environment-aware bond has dimension at least the rank of the full function's matricization across that cut. Without environment compression, the bond is at least the rank of the sub-network tensor. Treewidth bounds the contraction cost from above (Markov-Shi), not from below.

The doc qualifies the claim with "hard instances". That restricts the claim but does not repair it: deciding which instances need large rank is exactly the open question. This matches the repo guard "no unrestricted runtime claim from rank".

Computational illustration (COMPUTATIONAL, finite, n = 14): experiments/claude/tn_rank_vs_treewidth.py, blob 22c7a0fb04e16db57236cc3558c18e78d7cb02f4. Seed 20261119, cut seed 7. Raw output: results/raw/claude/2026-11-19_0948_TN_RANK_VS_TREEWIDTH_RAW.json, blob cfe13bcd47fa928321ea914f0401075292ea4780. Runtime 1.9 s. The run used exact subset-DP treewidth and six balanced 7|7 cuts. Ranks were computed over GF(2) and modulo 2^61-1, plus an exact Fraction rank on cut 0.

| Instance | Models | Exact primal tw | Cut ranks (GF2 = mod p) | Cut cap |
|---|---|---|---|---|
| random 3CNF, m = 42 | 40 | 8 | 9, 7, 8, 7, 8, 7 | 128 |
| monotone core + all units (point) | 1 | 8 | 1 on every cut | 128 |
| 10 parity triples (affine) | 16 | 4 | 2, 2, 2, 4, 4, 2 | 128 |
| random 3CNF, m = 64 (UNSAT) | 0 | 11 | 0 on every cut | 128 |

On these instances, GF(2) and mod-p ranks agree, and the exact Q rank matches on cut 0. Field dependence was therefore not exhibited (falsifier 2 was not triggered). Cut-rank is far below 2^tw in every row. These are finite tests, not asymptotics. The unit-forced and affine rows are known easy-family controls (unique-solution rank one, affine). They are recorded only because they kill the doc's stated arrow.

### F2. Doc 3.3 "strongest explicit lower bound (3 + 1/86)n": OUTDATED (KNOWN THEOREM, source verified)

Find, Golovnev, Hirsch and Kulikov (FOCS 2016) proved (3 + 1/86)n - o(n). This was improved to 3.1n - o(n) for affine dispersers by Jiatu Li and Tianqi Yang, STOC 2022 (ECCC TR21-023, DOI 10.1145/3519935.3520010).

### F3. Doc 3.3 attribution and conclusion of the 2n magnification threshold: CORRECTED (KNOWN THEOREM, abstract verified)

The doc attributes the 2n + O(n/log log n) threshold to Chen-Jin-Williams STOC 2020 and its "CCC 2022 refinements". Chen, Jin and Williams' STOC 2020 paper (ECCC TR20-065) is about formulas at the n^2 threshold. The 2n gate threshold is from Lijie Chen, Jiatu Li and Tianqi Yang, "Extremely Efficient Constructions of Hash Functions, with Applications to Hardness Magnification and PRFs", CCC 2022, LIPIcs 234:23.

The exact conclusion in that paper is NTIME[2^n] not in SIZE[2^(n^(1/5))] and NP not in SIZE[n^k] for all k. The hypothesis is that an n^alpha(n)-sparse NP language with alpha(n) <= log n / log log n lacks probabilistic circuits of 2n + O(n/log log n) gates. This conclusion implies the doc's weaker "NEXP not in P/poly", so the doc understates rather than misstates it.

The unconditional O(n)-sparse language in P requiring probabilistic circuits of size at least 2n - 2 is confirmed.

### F4. Doc 3.3 "no local argument can ever cross the threshold": OVERSTATED

The locality barrier (Chen, Hirahara, Oliveira, Pich, Rajgopal, Santhanam, ITCS 2020) is a heuristic meta-observation about known techniques. It is not a theorem ruling out all local arguments. Atserias and Muller (arXiv 2503.24061, v2 June 2025) give distinguisher-based magnification that, in their words, "seems to sidestep the localization barrier", with thresholds they state are sharp.

## Corpus search: OpenAI and Google GitHub organizations

These ran through `gh api search/repositories`, restricted to user:openai, user:google and user:google-deepmind. The queries were "sat", "sat solver", "theorem proving" and "or-tools".

The only relevant hit is google/or-tools, which includes the CP-SAT solver: an engineering solver with no lower-bound content. The openai searches returned 0 results. google-deepmind returned only cartesian-frames (HOL), which is not relevant. The GitHub search API reaches only default branches, and these queries were narrow. Absence of results is not evidence of absence. No new SAT lower-bound idea was found in these organizations' repositories.

## Four gates (for F1's corrected statement: TN bond >= function cut-rank)

- DISJ sanity: PASS. Rank of the DISJ matrix is 2^n, consistent.
- Relativization: NOT APPLICABLE. This is a statement about a fixed representation model, not about machines.
- Simultaneous DTISP: NOT APPLICABLE. No machine time-space claim is made.
- Deterministic configuration counting: NOT APPLICABLE, for the same reason.
- Natural Proofs: cut-rank is constructive and large over random functions, so it cannot alone yield P/poly lower bounds. It is consistent only as a restricted-model measure.

## Integration point

This is relevant to Track A (TMR-2 rank/tensor invariants) and TMR-4 (compiler to tensor representation). It supplies a primary-source-corrected statement and a minimal source-level falsifier for the doc's IB arrow. For TMR-2 and TMR-4 to use it, it should go through issue #3 and their handoffs as a suggestion, not as an edit to their manuscripts.

Known restricted-model analogue for follow-up: Bova, Capelli, Mengel and Slivovsky (IJCAI 2016) give communication-complexity lower bounds for (d-)DNNF compilations of explicit CNFs. Only the abstract was checked; the exact CNF families and theorem statements are NOT yet source-verified.

## One next lemma

Determine whether an explicit polynomial-size 3-CNF family F_n has full-function cut-rank 2^Omega(n) across every balanced cut of every contraction tree over Q (and over GF(2)). The approach would be to source-verify the Bova et al. families, or the OBDD/structured-d-DNNF lower bounds for CNFs. That would give an unconditional lower bound for exact environment-aware tree tensor-network contraction of SAT. It would remain a restricted-model bound, with no general runtime consequence.
