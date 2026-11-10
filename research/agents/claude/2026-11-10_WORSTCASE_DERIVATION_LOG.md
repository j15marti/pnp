# Worst-case derivation-cost program: living log (CANDIDATE/OPEN)

Run 2026-11-10 (scheduled). P vs NP remains **OPEN**. Nothing below proves a lower bound.
Shared target: W_R(N) = max over UNSAT F, |F|<=N, of min over derivations pi of F in R of cost_R(pi).
Strategy discovery is not charged (this is proof *size*, i.e. the Cook-Reckhow measure).

## Corpus note
No file named as the "shared worst-case directive" exists in the repo; this log is its anchor.
Related earlier work: research/agents/lspv-1/*WORSTCASE* (MUS worst-case quotient 350, core barrier 335,
node-profile noncomputability 395), GROKPROOF/ (living status), world-ledger/ (rows L13, L34-L40).

## Results this run
**R1 (KNOWN THEOREM, Cook-Reckhow 1979).** There is a sound, complete, poly-time-verifiable R with
W_R(N) <= poly(N) iff NP = coNP. So "free choice of optimal derivation" is exactly the Cook-Reckhow program;
the (size, space, sign-multiplicity) cost refinement only adds coordinates, never removes the NP vs coNP content.

**R2 (PROVED/EXACT, definitional).** Bridge(R): "SAT in P => W_R <= poly" is equivalent to "P = NP => R is
polynomially bounded". Consequences:
* For any R with a proven superpolynomial W_R (resolution, tree/DAG, cutting planes, bounded-depth Frege, PC with
  suitable degree...) Bridge(R) is **equivalent to SAT not in P**. So the bridge is as hard as P != NP for those R and
  gives no leverage there. The bridge has content only for R beyond all known lower bounds (Frege / EF-strength).
* SAT in P => NP = coNP, so a poly-bounded system Q exists; Bridge(R) follows if R is optimal (Krajicek-Pudlak), and
  optimal systems are known only under NE = coNE (p-optimal under E = NE). Existence is open and not settled by
  relativizing proofs (oracle results in the literature).

**R3 (KNOWN, conditional route).** If a poly-time M decides SAT and PV proves M sound (provably correct algorithm),
then EF has poly-size refutations (Cook PV translation). The quantifier gap for the bridge is therefore exactly:
*arbitrary* M, whose correctness need not be provable in the fixed system. This is the Levin-search / unprovable-
correctness obstruction; it is the precise missing transfer theorem. Candidate narrowing: restrict the hypothesis to
"SAT in P via an algorithm with feasibly provable correctness" and show the multisign-DAG measure matches EF size (CANDIDATE).

**R4 (design constraint).** A multisign DAG hypergraph cost must be shown polynomially equivalent to a known
system (resolution/EF/Frege) before any lower bound is meaningful; otherwise W_R is for a nonstandard R whose
simulation relation to Q (the hypothetical poly system) is unknown, and Bridge(R) is unsupported.

## Role tasks (next runs)
1. Lead: fix R = multisign DAG calculus; prove p-simulation of (or by) Frege/EF, or exhibit separation.
2. Reduction builder: certified shortest-derivation DAGs for small N (exhaustive, <=30 s chunks).
3. Hard families: test Tseitin/PHP/random k-CNF; each is known hard for resolution only, so survival against EF is the real test.
4. Resource auditor: peak memory via pebbling; resolution size-space tradeoffs (Ben-Sasson; Nordstrom survey) as baseline.
5. Red team: attack R2/R3, look for R where Bridge(R) is provable without optimality.

## Literature check (this run)
* Optimal/p-optimal systems still open; NE=coNE => optimal, E=NE => p-optimal; oracle barriers: https://arxiv.org/pdf/2304.14702
* "The Proof Analysis Problem" (2025) ties analyzable optimal-system conjectures to NP vs coNP / P vs NP (unverified preprint): https://arxiv.org/pdf/2506.16956
* Resolution size-space separations via pebbling formulas: https://lmcs.episciences.org/1111 ; Nullstellensatz size-degree = reversible pebbling: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2019.18
No literature found closing the bridge for any system above known lower bounds. Status: OPEN.
