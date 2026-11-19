# CLAUDE DOCAUDIT-0001 — review of "P vs. NP Proof Attempts" (Google Doc) + external-repo survey

Date: 2026-11-19 (scheduled hourly Claude routine). Base revision: `2582d7b4974248a2041599e67c73a2efee516ff2`.
Ownership: additive Claude report only. No TMR manuscript, handoff, retired tracker (proof*.txt) or historical root file was edited.
**P versus NP remains OPEN.** Nothing here is a lower bound for SAT; the main result is a falsification of one claimed obstruction.

## 0. What was read

Source: Google Doc `1b2SYjJJJVjMwap-5wURTFbUMn212lwFnYhq2k5Sqdds`, title "P vs. NP Proof Attempts" (62,596 chars as exported via the Drive connector on 2026-11-19).
Read: all section headings; §1, §2.1, §2.2, §3.3 and §4 in full; §2.3, §3.1, §3.2 through the first 1,500 characters of each paragraph plus the IPS table. **Disclosure:** the tails of a few long paragraphs in §2.3/§3.1/§3.2 and the "Works cited" list were not read.

## 1. Candidate, falsifiers, dependency

Doc claim (Attempt IB, "Diagnosis"): *"the space complexity and minimal exact bond dimension along any contraction order are lower-bounded by 2^{Ω(tw(G))}, where tw(G) is the treewidth of the 3-SAT incidence graph."*

Dependency advanced: the doc's Attempt IB obstruction is the load-bearing arrow "high incidence treewidth ⇒ exact tensor-network #SAT contraction is exponential". Falsifiers considered: (F1) a high-treewidth family with rank-1 exact compressed contraction; (F2) contraction value ≠ #SAT; (F3) the treewidth bound being only an upper bound. F1 holds (below); F2 checked negative; F3 handled by using a rigorous minor-min-width lower bound.

## 2. Result — FALSIFIED (claim), PROVED/EXACT (counterexample), not independently reviewed

**Proposition.** Let H be any bipartite variable–clause incidence graph with clause degree 3. Let Φ_H⁺ be the 3-CNF with incidence graph H whose literals are all positive, conjoined with the unit clauses (x_i) for every i. Then (a) tw(inc(Φ_H⁺)) ≥ tw(H); (b) #SAT(Φ_H⁺) = 1; (c) there is a contraction order in which, with exact (δ = 0) SVD compression after each step, every intermediate tensor has matricization rank 1 across every bipartition of its open legs, and the total work is linear in the size of the network.

*Proof.* (a) inc(Φ_H⁺) is H plus one pendant vertex per variable; H is a subgraph, and treewidth is subgraph-monotone. (b) The units force x = 1ⁿ, which satisfies every all-positive clause. (c) Contract each unit vector e₁ into its variable's copy tensor δ_d first: δ_d · e₁ = e₁^{⊗(d−1)}, a product tensor, which exact SVD splits into d−1 rank-1 vectors. Each clause tensor OR₃ then meets three copies of e₁ and contracts to OR₃(1,1,1) = 1. Every intermediate is a product tensor, so all bond dimensions are 1. ∎

Choosing H with tw(H) = Ω(n) (e.g. bounded-degree bipartite expanders — KNOWN THEOREM that expanders have linear treewidth; primary-source re-check for the random (6,3)-biregular model OPEN) gives a uniform family with tw = Ω(n) and polynomial-time exact compressed contraction. So the doc's "any contraction order" lower bound is false as stated. What survives is the KNOWN THEOREM that *uncompressed* contraction along an order has cost exponential in that order's width (Markov–Shi 2008, SIAM J. Comput. 38(3)), i.e. an upper-bound/cost statement about one algorithm without compression — not a lower bound on compressed contraction, and certainly not on SAT.

Corrected statement (CANDIDATE, OPEN): the right obstruction is a *function-level* parameter — the minimum over contraction trees of the maximum exact rank of the partial-contraction tensors — which can be far below 2^{tw}. Any lower bound proved for it is a rank argument for one structured algorithm family and, per AGENTS.md, gives no unrestricted runtime claim. It must also pass the unit/autarky/Horn/2-SAT/affine/treewidth easy-family controls; the family above is exactly a unit-propagation control.

### Executed evidence — COMPUTATIONAL (finite, not asymptotic)

`tn_rank_falsifier.py` (sha256 `0c50d160…7ac29`), seed 20261119, Python 3.11.18, numpy 2.4.6, elapsed 17.4 s. Raw output `tn_rank_falsifier_results.json` (sha256 `6144a911…d3767`). Random (6,3)-biregular incidence graphs, m = 2n, dense numpy tensors, exact SVD peeling of rank-1 legs, greedy minimum-open-legs pairing.

| n | m | MMW tw lower bound (with units) | unit-first: Z, max rank, max open legs | control (no units): Z = brute #SAT? max balanced rank |
|---|---|---|---|---|
| 6 | 12 | 5 | 1.000, 1, 1 | 34 = 34, rank 6, 13 legs |
| 9 | 18 | 5 | 1.000, 1, 1 | 156 = 156, rank 13, 16 legs |
| 12 | 24 | 5 | 1.000, 1, 1 | 918 = 918, rank 14, 16 legs |
| 15 | 30 | 6 | 1.000, 1, 1 | exceeded 16-leg cap (17) |
| 18 | 36 | 7 | 1.000, 1, 1 | exceeded 16-leg cap (18) |
| 30 | 60 | 8 | 1.000, 1, 1 | not run |
| 60 | 120 | 11 | 1.000, 1, 1 | not run |
| 90 | 180 | 13 | 1.000, 1, 1 | not run |

The unit-first Z equals the brute-force count 1 for n ≤ 18 (floating error < 1e-13). The MMW values are rigorous treewidth lower bounds for these specific instances (Gogate–Dechter 2004 minor-min-width), growing with n; they are not an asymptotic proof. The control only shows that this greedy order does not compress the no-unit formulas; it is not a lower bound for any order.

### Four gates

DISJ sanity, relativization, simultaneous DTISP, deterministic configuration counting: all NOT APPLICABLE — this is a falsification of a claimed obstruction for one algorithm family, not a lower-bound candidate. No complexity-class consequence is asserted.

## 3. Other corrections to the doc (literature, not re-derived)

| Doc statement | Correction | Status |
|---|---|---|
| §2.3: Bürgisser — VP = VNP over a finite field gives P = NP "unconditionally" | Bürgisser's transfer gives *non-uniform* collapses (e.g. NP ⊆ P/poly, hence PH collapse), not uniform P = NP. Over ℂ the GRH-conditional transfer is also non-uniform. | KNOWN THEOREM; page-level source check OPEN |
| §2.3 title: NP = coNP ∧ VP = VNP ⇒ P = NP | No such implication is known; neither hypothesis, nor both together, is known to give uniform P = NP. | Logical correction |
| §3.3: the strongest explicit circuit lower bound is (3 + 1/86)n − o(n) | Superseded: Li & Yang, "3.1n − o(n) circuit lower bounds for explicit functions", STOC 2022. | KNOWN THEOREM |
| §3.3: Locality Barrier | Due to Chen, Hirahara, Oliveira, Pich, Rajgopal & Santhanam, "Beyond natural proofs: hardness magnification and locality", ITCS 2020 / JACM 2022. The doc's version (one polylog-fan-in oracle gate after the kernel) matches that paper's idea. | Attribution |
| §3.3: an explicit O(n)-sparse language in P needs 2n − 2 probabilistic gates; magnification threshold 2n + O(n/log log n) | Plausibly from Chen–Jin–Williams, "Sharp threshold results for computational complexity", STOC 2020; the exact constants were not verified. | Source check OPEN |
| §2.1: "Basis collapse for k = 2, 3, 4 and general domains" | Cai–Lu's basis-collapse results concern bases of higher dimension over the Boolean domain; the doc's "domain size k" wording is likely garbled. | Source check OPEN |
| §2.2: obstruction = 2^{Ω(tw)} for any contraction order | FALSIFIED above. | PROVED/EXACT counterexample |

## 4. External repositories (OpenAI / Google)

Searched with `gh api search/code` (default branches) and public shallow clones.

| Repository / path | Revision | Relevance |
|---|---|---|
| `openai/math` `lean/OAI/Algorithms/SubexponentialSAT/*` (≈50 Lean files, incl. `Separation.lean`, `SpectralRank.lean`, `Sunflower.lean`) | default branch | Already audited heavily in this repo (396 local files reference it, e.g. lspv-5 and TMR reports). No new action. |
| `google-deepmind/formal-conjectures` `FormalConjectures/Millennium/PvsNP.lean` | file sha256 `c99c8930…878df` | States `P_ne_NP : P ≠ NP := by sorry` (category "research open"), plus NP ≠ coNP and P = BPP. `P_subset_NP` cites an external formal proof. Possible pinned formal target statement for TMR-1's source-verification track; its `P`/`NP` definitions were not inspected. |
| `google-deepmind/alphaevolve_repository_of_problems` | `8f447457` | 68 problem pages whose text is rendered client-side (not inspected); experiment notebooks are combinatorial/analytic constructions (difference bases, Kakeya, Erdős–Gyárfás, …). No SAT lower-bound content found. |
| `google-deepmind/alphaevolve_results` | `4226acbf` | Single notebook of mathematical constructions; no SAT/complexity lower-bound content found. |

Code-search queries for MAX-CUT gadgets, proof complexity and circuit complexity in google/google-deepmind returned nothing.

## 5. One next load-bearing lemma

State and test the function-level contraction-rank parameter ρ(Φ) = min over contraction trees of the max exact intermediate rank, and find a *unit/autarky/Horn/affine-closed* 3-CNF family where ρ is provably 2^{Ω(n)} — e.g. via Raz-style or Nisan-style rank bounds on partial-contraction tensors. The scope is restricted to tensor-network algorithms, the status is OPEN, and the result would not be a SAT lower bound.
