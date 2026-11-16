# TMR-5/WR056 | 2026-11-15 19:48 PST | Bit-PHP collapses under extension (red team, shared W̄_R objective)

Authority: `research/coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md` plus the shared worst-case derivation objective
W̄_R(N) = max_{UNSAT F, |F|≤N} min_{π:F⊢_R⊥} cost_R(π), and Bridge(R): SAT∈P ⇒ W̄_R(N) ≤ poly(N).
Role: Independent Proof Red Team (TMR-5). P versus NP remains **OPEN**. This run does not claim any lower bound.

## Named dependency advanced
Directive priority 4: does a proposed hard family survive resolution, algebraic reasoning, circuit compression, shared DAGs and adaptive switching?
The /055W audit (branch `ccr-1695bd63-4oyies`) named bit-PHP as the test family for R⁻_comb = DAG Res(⊕) + CP.
This run tests the compression and sharing arm that R_comb is supposed to contain.

## Candidate and falsifiers (stated before the search)
CANDIDATE under test: "BPHP^{n+1}_n requires superpolynomial minimum derivation cost in R_comb."
Falsifiers considered:
1. a polynomial refutation in some arm of R_comb with extension or definitional DAG nodes (**found**: Theorem E);
2. a polynomial refutation in an algebraic arm (**KNOWN**: Sum-of-Squares is polynomial, per Dantchev–Galesi–Ghani–Martin, as quoted by Beame–Whitmeyer);
3. a polynomial refutation in the CP arm (**ruled out**: CP needs 2^{Ω(n^{1/4})}, a KNOWN THEOREM);
4. a switching (union) refutation in R⁻_comb (**OPEN**).

## Literature checked this run (primary sources)
- Beame–Whitmeyer, "Multiparty Communication Complexity of Collision-Finding and Cutting Planes Proofs of Concise Pigeonhole Principles", ICALP 2025, LIPIcs 334:21; full version ECCC TR25-057. I read the full text of the introduction. It states:
  - CP size 2^{Ω(n^{1/4})} for general DAG-like CP;
  - tree-like CP size 2^{n^{1−o(1)}};
  - Hrubeš–Pudlák 2^{Ω(n^{1/8})};
  - from Dantchev–Galesi–Ghani–Martin: resolution 2^{Ω(n/log n)}, Res(k) 2^{Ω(n^{1−ε})} for k ≤ log^{1/2−ε} n, and Sherali–Adams 2^{Ω(n/log² n)};
  - "BPHP^m_n has polynomial-sized Sum-of-Squares refutations".
- Braun, arXiv:2609.23015. Search snippets only: it claims DAG Res(⊕) > exp(n/(32768 ℓ²)) for ℓ ≥ 32 and was written with AI assistance. It remains a **CANDIDATE**; I have neither verified the proof nor built the Lean artifact.
- Byramji–Impagliazzo, arXiv:2511.20023: bounded-depth Res(⊕) bounds for bit-PHP.
- Cook 1976 (ER refutation of PHP), Buss 1987 (polynomial Frege PHP) and Beame–Kautz–Sabharwal 2004 (RUP ⇒ trivial resolution) are used as KNOWN.

## Theorem E (PROVED/EXACT; ingredients KNOWN; independent review OPEN)
**Setting.** n = 2^k holes and m = n+1 pigeons. The formula has |⟨F⟩| = C(n+1,2)·n·2k = Θ(n³ log n) literal occurrences.

**Statement.** BPHP^{n+1}_n has an explicit extended-resolution refutation, given as RUP lines plus conservative fresh definitions, with these counts:
- extension variables: n(n+1) + (n+1)n(n−1)/3;
- extension clauses: n(n+1)(k+1) + 4(n+1)n(n−1)/3;
- RUP lines: (n+1)(n−1) + C(n+1,2)·n + Σ_{h=2..n} (h + 3(h−1)·C(h,2)) + 1, which is (3/8)n⁴ + O(n³).

**Size.** Each RUP line expands into a trivial-resolution chain of O(n) steps. The total size is therefore O(n⁵) = O(N^{5/3}), with O(N^{4/3}) lines.

**Proof sketch** (the full proof is in main5 §"Bit pigeonhole collapses under extension"):
- *Stage 1, binary to unary.* Define y_{i,h} ↔ ∧_b [x_{i,b} = h_b].
  - Hole clauses ¬y_{i,h} ∨ ¬y_{i',h} are RUP from the source clause.
  - For each pigeon, 2^k − 2 prefix lemmas are RUP bottom-up. The root lemma is P_i = ∨_h y_{i,h}.
- *Stage 2, Cook's reduction.* Define q_{i,j} ↔ p_{i,j} ∨ (p_{i,h−1} ∧ p_{h,j}).
  - Each pigeon clause is RUP.
  - Each hole clause needs two auxiliary RUP lemmas.
  - Repeat down to h = 1, where the empty clause is RUP.

## Executed evidence (COMPUTATIONAL)
**Code and environment**
- Producer: `experiments/tmr/tmr5_bitphp_er_collapse056.py`, revision `tmr5-bitphp-er-collapse056.v1`, sha256 d867b663…5c1f.
- Checker: `experiments/tmr/tmr5_er_rup_checker056.py`, revision `tmr5-er-rup-checker056.v1`, sha256 bbd6a8b8…4403.
- CPython 3.11.18. Everything is deterministic; no seed is used.

**What the checker verifies, independently of the producer**
- it regenerates BPHP from k with its own indexing and compares the clause multisets;
- every extension variable is fresh, and every extension is conservative (brute force over the variables of the step);
- every added line is RUP;
- every deletion removes a clause that is present;
- the last added line is the empty clause.

**Results.** Each RUP lemma also counts as an implied line in the proof-line total.

| n | F literals | ext vars | RUP lemmas | proof lines | proof literals | trivial-res. steps bound | PASS | check time |
|---|---|---|---|---|---|---|---|---|
| 2 | 12 | 8 | 15 | 35 | 74 | 75 | yes | 0.00 s |
| 4 | 160 | 40 | 140 | 280 | 710 | 1,190 | yes | 0.003 s |
| 8 | 1,728 | 240 | 1,773 | 2,733 | 7,314 | 26,448 | yes | 0.04 s |
| 16 | 17,408 | 1,632 | 26,027 | 32,827 | 88,434 | 701,467 | yes | 0.75 s |
| 32 | 168,960 | 11,968 | 403,095 | 453,079 | 1,215,874 | 20,473,408 | yes | 19.8 s |

**Controls and checks**
- The generated counts equal the closed forms for every n in the table.
- Six corruption controls were each REJECTED, at both n = 2 and n = 4:
  - a dropped lemma;
  - a missing empty clause;
  - a non-fresh extension;
  - a non-conservative extension;
  - a dropped source clause;
  - a strengthened lemma.
- Brute force confirms UNSAT for n = 2 and n = 4.
- Symbolic closed-form counts for k = 6..10 are recorded but were not generated or checked.

**Raw data.** `results/raw/tmr/2026-11-15_1948_TMR5_BITPHP_ER_COLLAPSE_WR056_PY_RAW.json` (sha256 fbeb8ecd…3e60).
- It inlines the full proofs for n = 2 and n = 4.
- The proofs for n = 8..32 are not stored; their sha256 is recorded, and the deterministic producer regenerates them bit-exactly.

**Stage timing.** The first checker stage ran in 0.86 s on a pre-final checker revision. That revision differed only in which file received the corruption controls. The final code was rerun, and its check fields are identical (recorded in the raw JSON). Stage 2 (n = 32) took 21.1 s.

**Not run:** preflight, a LaTeX build (no TeX in the container), a DRAT-trim cross-check and Braun's Lean artifact.

## Consequence (red-team verdict)
Consider any fixed multisign DAG-hypergraph system in which a reduction can name a definitional node and resolve on it, that is, any system that p-simulates ER.
- In such a system, bit-PHP's minimum derivation cost is O(N^{5/3}), even with the free optimal sequence.
- The same family is exponential for resolution, Res(k), Sherali–Adams and CP, and candidate-exponential for DAG Res(⊕).

So "survives circuit compression / shared DAGs" is **FALSIFIED for bit-PHP**. It joins PHP (polynomial in CP and in Frege) and Tseitin (polynomial in GF(2) reasoning and quasipolynomial in CP).

No known family is superpolynomially hard for extended Frege. With Corollary D, a W̄_{R_comb} lower bound with extension included would be exactly such an OPEN result. Without extension, the R⁻_comb question stays OPEN. Novelty is not claimed: the new content is the explicit, machine-checked artifact with exact counts.

## Gates
- DISJ: NOT APPLICABLE.
- Relativization: NOT APPLICABLE; this is an unconditional propositional upper bound and no separation is claimed.
- Algebrization and Natural Proofs: NOT APPLICABLE.
- Simultaneous DTISP: NOT APPLICABLE to proof size. The checker itself runs in O(n⁵) time with O(n³) live clauses.
- Configuration counting: PASS as an upper-bound guard.
- /341 is FAIL as a full UNSAT authority; /386 is RESTRICTED.

## One next lemma
In R⁻_comb (DAG Res(⊕) + CP through a clause interface, with no definitions), decide whether BPHP^{n+1}_n has polynomial refutations. Independently build Braun's Lean artifact before relying on its bound. Any survival claim must name a definition-free system and must address the SoS upper bound.
