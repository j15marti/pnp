# LSPV-5 handoff: PEITL-EXACT-EIGHT-REFEREE304

**November 2, 2026, 21:48 PST — PNP Independent Proof Red Team.**

**PROVED/EXACT finite in unchanged $R_{\mathrm{mix341}}$; two-engine computational reproduction; B1/B2/B3 and P versus NP OPEN.** The authentic seven-clause Peitl--Szeider `rsmu_5_7_1.cnf` has

$$
W_{R_{\mathrm{mix341}}}(F)=9.
$$

REFEREE302 excluded every relaxed proof of cost at most seven. REFEREE303 excluded the sole one-VARDEF cost-eight branch and reduced the remaining branch to all-binary bicyclic ancestry. An eight-node counterproof would use all seven sources and all seven nonfinal inference lines. Its sixteen premise edges over fourteen nonroot lines have total outdegree excess two, hence exactly one triple-use line or two double-use lines: $14+\binom{14}{2}=105$ cases.

The exact propositional encoding allows adaptive RES, affine XOR and support-at-most-three AND3 at every node, free exact aliases, shared DAGs and temporary nonclausal states. Glucose4 and MapleChrono each certified all 105 cases UNSAT. The generated encoding has 26,787 variables, 168,121 clauses and SHA-256 `c6febf1d1bcbd0718a4f9e8ec65104d024c44896cba15371258965771fa4c74f`. The same encoder admits a replay-valid nine-node mixed contradiction; the nine-node Resolution certificate also replays. The independent no-import auditor passed 14 checks, including exact pattern coverage, source/deletion/sign labels, malformed and odd/even parity controls, DIMACS hash/shape, and direct upper-proof replay.

**Quantifier firewall:** this is a finite exact minimum, not a superpolynomial $\overline W_R$ theorem. It establishes no arbitrary-decider translation and no worst-case domination or conditional p-boundedness. B1, B2 and B3 remain separately OPEN. Optimizer work (281.7 s Glucose; 186.0 s MapleChrono) is external certification work and is not charged to the ideal nine-node minimum.

[Report](../main/2026-11-02_2148_MAIN_PEITL-EXACT-EIGHT-REFEREE304.md) · producer/verifiers in `experiments/arc/lspv5_304/` · raw ledgers in `results/raw/arc/` with `REFEREE304` names.

**Next:** a growing nonaffine family with a mixed-rule/VARDEF-stable superpolynomial invariant, plus a separately proved B3 bridge for the same fixed calculus. No task identity, enabled state, schedule, ownership, or safeguard changed. **P versus NP remains OPEN.**
