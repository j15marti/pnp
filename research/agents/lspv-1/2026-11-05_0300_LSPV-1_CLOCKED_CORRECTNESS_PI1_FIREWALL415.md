# LSPV-1/415: Global rejection soundness of clocked SAT programs is Pi^0_1-complete

**November 5, 2026, 03:00 PST | PNP General SAT Lower-Bound Lead.** **PROVED/EXACT** for a specifically declared program-index language (independent specialist review pending); **COMPUTATIONAL** for finite mock-clock controls; **FALSIFIED/RETIRED** universal automatic recognition of rejection soundness; **OPEN** fixed R_mix341 B1/B2/B3, byte grammar, all-consumer source-authenticated normalization, superpolynomial mixed cost, and P versus NP.

## IDEA, hypotheses, falsifiers (before search)

Test whether a universal construction under hypothetical SAT in P can inspect the source code of *any syntactically polynomial-clocked* decider, prove that its UNSAT outputs are sound, and emit native mixed refutations from rejecting traces. Prediction: a polynomial clock does not make global one-sided soundness decidable. F1: the reduction loses the common polynomial clock; F2: the exceptional input is invalid or UNSAT; F3: fallback fails the required all-input control; F4: exhaustive finite testing suffices. The first three are ruled out by the construction, and F4 fails by quantifier order. We explicitly **do not** claim this falsifies B3.

## Fixed calculus and scope

The original rule specification is `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, Git blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`: free exact indexed signed DIMACS clauses, unit-cost binary RES, local support-three AND3 with only globally exact GF(2) annotation, binary GF(2) row XOR, unary LOCAL-CONVERT by constant-support implication, paid fresh two-input conservative DEF. Every derived DAG node has indegree <=2. This report changes no grammar or weights. The historical byte-parser and DEF-facet/exported-wire selectors remain unspecified. `W_R(F)` is the smallest paid-node UNSAT refutation cost, and `Wbar_R(N)` the maximum for authentic UNSAT source encodings up to N bits. The B3 goal is SAT in P => Wbar_R(N) <= C(N+1)^k for fixed C,k, **not proved here**.

## Theorem 1: exact one-sided index complexity

Let `ClockP` be a decidable effective program syntax whose interpreters halt under an explicitly enforced polynomial clock; one fixed degree suffices for the reduction. Outputs are SAT/UNSAT/MALFORMED. Let

$$
RS=\{\langle P\rangle : \forall F,w\;[ValidCNF(F)\land Eval(F,w)\Rightarrow P(F)\ne UNSAT]\}.
$$

Then **RS is Pi^0_1-complete under computable many-one reductions**, even on a uniformly generated, commonly polynomial-clocked subclass.

*Proof.* Failing RS is c.e.: enumerate finite (F,w); check parsing, the complete assignment, and the clocked P(F) output. For hardness reduce NONHALT of an arbitrary blank-input Turing machine M_e. Let U_n be the canonical authentic signed DIMACS encoding of the n positive unit clauses (x_1),...,(x_n), of size Theta(n log(n+2)). Its all-ones assignment satisfies it. Effectively compile e to one fixed clocked program C_e: parse and reject malformed inputs, recognize *exact* U_n, simulate M_e for at most n steps there, return UNSAT if it halts and SAT otherwise, and return SAT on all other valid CNFs. A bounded universal simulation, canonical comparison and parsing have one fixed polynomial exponent in the input/source length, with e-dependent constant permitted. Thus

$$
e\in NONHALT\quad\Longleftrightarrow\quad C_e\in RS.
$$

This is a specialization of classical coHALT completeness, not an original undecidability theorem. The reduction's NO cases deliberately contain **incorrect** programs, and therefore cannot serve as B1, B2 or B3 counterexamples.

## Theorem 2: exact full-correctness index complexity, conditional on SAT in P

Assume a fixed externally correct total P-time general CNF decider A, handling SAT, UNSAT and MALFORMED. Modify C_e to use A on non-U_n inputs. On U_n return UNSAT iff M_e halts in <=n steps and SAT otherwise. Call this B_e. If e never halts, B_e agrees extensionally with A on **every** binary input. If e halts, B_e falsely rejects a true SAT U_n. For one sufficiently large **fixed** syntactic clock degree d (depending on A, not e), all B_e lie in ClockP_d, and

$$
CORR_d=\{\langle B\rangle: B\text{ correctly classifies all CNF and malformed inputs under its degree-d clock}\}
$$

is **Pi^0_1-complete**. Membership: a wrong classification on one finite binary string is decidably checkable using exhaustive truth-table SAT, and programs are clocked. Hardness: the NONHALT reduction above. Without SAT in P no such full-correctness P-class is asserted.

*Corollary.* Under SAT in P, a sound recursively enumerable proof theory cannot prove global correctness for **every** correct ClockP_d program: a complete such effective enumeration would make this non-c.e. Pi^0_1-complete index set c.e. This does not prohibit proving soundness for **some one** particularly structured P-time SAT decider, as in LSPV-1/357's conditional bounded-arithmetic theorem. It does not preclude B3 by another route.

## IDEA -> SEARCH -> ITERATE and duplication firewall

Read the Nov-2 12:04 governing handoff, issue #3 through REFEREE359, `AGENTS.md`, `CODEX.md`, pnp-research skill, original /341 and /384, LSPV-1/357 and /414, peer LSPV-2/413, LSPV-3/418, LSPV-4/409, LSPV-5/REFEREE320,357,359. Actual Grok `GROKPROOF/2026-11-05_1218_PROGRESS.md` and Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` and `2026-10-28_1452_CLAUDE_TPORT-0002.tex` were inspected. Their FLMV and sequential-memory results are restricted and do not transfer to B3. OpenAI GitHub queried `CookLevin`, `ExecCNFNodeSearchCosts`; full `openai/math` Lean files were read (blobs `1e23a159`, `1ced21f4`), and neither formalizes a same-R correctness/refutation compiler.

General-web searches: `Pi1 halting complement arithmetical hierarchy`, `Rice index set correctness polynomial time programs`, `Cook Reckhow proof systems`, `Pudlak reflection principles`, `Haken PHP Resolution`, `Raz Tzameret Res linear equations`. Direct Google-branded interactive search was unavailable, so web-engine and authenticated GitHub search were used. Prior LSPV-1/357 already constructed an unprovably correct Godelian wrapper; REFEREE320 already proved finite-prefix indistinguishability. These results are credited. This run adds the precise Pi^0_1 classification and fixed-clock quantifiers instead of repeating the prior broad obstruction.

Established hard controls are unchanged: Haken (1985) bounds **ordinary shared-DAG Resolution** on explicit PHP, not full mixed or machines; Cook (1976) ER PHP and native GF(2) odd Tseitin are bypasses; Raz and Tzameret Res(linear equations) bounds concern their specific grammar.

## ITERATE, verification, physical and epistemic costs

Mock tests, **not** a HALT oracle: Python script exhaustively checks 256 signed two-variable clause-subset CNFs (95 SAT, 161 UNSAT), 216 HALT_AT(t)/LOOP canonical U_n runs for n=1..24, and seven malformed controls. Producer: 560 assertion groups. No-import independent Node verifier: 1,175 checks, reconstructs SAT labels independently. Full raw locally SHA-256 `56f770e57f434e1301e30681c1e83ff08529017bc21d6d09fde0786102d1bcf8`. Full producer/independent verifier/raw are local conversation artifacts; GitHub contains a compact reproducer and the machine-readable summary. Testing finite mock clocks does not establish coHALT, which follows from the symbolic proof above.

The wrapper parses/compares original source bits and simulates at most n steps of M_e with polynomial input reads, time, working memory, output and fixed-program storage. Conditional B_e additionally pays all costs of A. No R proof is emitted; no claim about mixed minimum size, optimizer discovery, encoded proof bytes, proof checking, FLMV or arbitrary SAT machine hardness follows. All five role identities/schedules/enabled states remain unchanged.

## Next precise missing link

Only a **one-decider** theorem could still salvage this B3 route: derive, rather than assume, a globally sound P-time general SAT decider with a formal rejection-soundness proof translatable to paid original-source R_mix341 refutations. In parallel, freeze a normative byte parser and fully charge DEF selector, LOCAL exported-port, AND3 and GF(2) consumers. Same-system B1/B2/B3 and P versus NP remain **OPEN**.

## Numbered references

[1] Stanford Encyclopedia of Philosophy, *Recursive Functions* (arithmetical hierarchy), https://plato.stanford.edu/entries/recursive-functions/ .

[2] Cook SA, Reckhow RA. *The Relative Efficiency of Propositional Proof Systems*. J Symb Log. 1979;44:36-50. https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf .

[3] Pudlak P. *Reflection Principles, Propositional Proof Systems, and Theories*. https://arxiv.org/abs/2007.14835 .

[4] Haken A. *The Intractability of Resolution*. TCS 1985;39:297-308.

[5] Raz R, Tzameret I. *Resolution Over Linear Equations and Multilinear Proofs*. APAL 2008.
