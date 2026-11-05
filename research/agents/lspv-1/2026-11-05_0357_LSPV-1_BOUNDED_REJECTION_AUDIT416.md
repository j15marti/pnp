# LSPV-1/416: A polynomial witness for failure of SAT self-reduction, but no native UNSAT certificate
**November 5, 2026, 03:57 PST.** P versus NP remains OPEN. **PROVED/EXACT (elementary finite-prefix theorem; independent specialist review pending)**, **COMPUTATIONAL** small controls, **CONDITIONAL** under SAT in P for semantic auditing, and **OPEN** B1/B2/B3 for the unchanged R_mix341.

## IDEA and exact falsifiers
Can polynomial-time SAT classifier A be audited on the *entire restriction tree of one source F* without presupposing a formal proof of A's correctness? Predictions: every root error has a polynomial-size local recurrence/leaf counterexample; constant-NO makes detecting such a counterexample NP-hard, despite satisfying every interior recurrence; a semantic negative SAT answer to the audit does NOT constitute a legal R_mix341 proof. An additional falsifier is the existence of a root-correct classifier that violates a descendant, which does occur.

## Theorem 416.1 (PROVED/EXACT)
Fix ANY total deterministic polynomial-time binary classifier A on valid signed CNFs, whether correct or incorrect. For valid source F with m actually occurring original variables, let G_alpha be F restricted by prefix alpha of the ordered original variables, 0<=|alpha|<=m. The clause and header records are reserialized, with O(|F|) bits each. Define BAD_A(F) iff there exists a prefix alpha such that:
* at an interior prefix, A(G_alpha) != A(G_alpha0) OR A(G_alpha1);
* at a full leaf, A(G_alpha) differs from direct evaluation of F on alpha.

Every witness has O(|F|) bits and verification runs in polynomial time, with at most three A calls. **BAD_A(F) is empty if and only if A is correct on ALL restrictions of this one F.** Proof: exact leaf values plus backward induction using the standard SAT self-reduction identity. An incorrect root entails a bad prefix. The converse does not hold: a root-correct A can be wrong elsewhere in the restriction tree.

## Theorem 416.2 (PROVED/EXACT, sharp countercontrol)
For the fixed constant-time classifier A0(G)=UNSAT on every valid G, all interior recurrence checks pass automatically. A leaf differs exactly when the corresponding full assignment satisfies F. Hence
```
  BAD_A0(F) iff F is SAT.
```
Thus deciding whether there exists a bad local witness for this ONE fixed trivial A is NP-complete by the identity reduction from SAT. This is an NP-completeness classification, **not** an unconditional superpolynomial runtime lower bound. A0 is intentionally incorrect, not a counterexample to B1/B2/B3.

## Theorem 416.3 (CONDITIONAL, semantic only)
For any fixed polynomially clocked A, BAD_A is in NP. A uniform Cook-Levin compiler makes a CNF M_A,F with polynomially many encoded bits such that SAT(M_A,F) iff BAD_A(F). If SAT is in P, a polynomial-time decider can check this audit and, when it succeeds, SAT self-reduction can extract and locally verify the bad prefix. This does not assume a formal proof of A's correctness. A negative answer is merely another SAT-decider answer, **not** an original-source-authenticated refutation in R_mix341; replacing an R inference by this answer would introduce the prohibited semantic SAT oracle. No polynomial source-to-R translation, native grammar resolution, or B3 implication follows.

## Tests and falsification
The full local producer and independent no-import JS checker evaluated all 256 subsets of eight signed non-tautological unit/binary clauses over two original variables, 95 SAT and 161 UNSAT, under six classifiers. Root errors / bad-audit counts: exact 0/0; constant NO 95/95; constant YES 161/255; empty-clause-only 161/183; clause-count parity 129/253; one poisoned positive unit 1/1. **Zero** incorrect root answers escaped the full audit. A root-correct but bad-descendant example occurred 94 times under constant YES, falsifying equivalence of root correctness and an empty BAD set. Seven malformed DIMACS controls were rejected by independent Python/JS parsers, and a valid source was accepted. JavaScript checker: 48 summary assertions and all 1,536 source/classifier combinations reconstructed; zero mismatches. Finite checks are not asymptotic proofs. Code/raw are in conversation artifacts; compact GitHub reproducer/summary are linked in the handoff.

## Scope, literature and physical cost
The fixed original /341 calculus has free original indexed clauses; paid unit-node binary RES, support<=3 AND3, GF(2) row addition, constant-support LOCAL-CONVERT, and conservative paid two-input DEF. No extra rule is adopted. The exact native DEF/public-port selector bytes remain unratified. Parsing, source/index reads, residual construction, Cook-Levin miter compilation, guest A calls, output, and all simultaneously allocated storage are charged for semantic algorithm upper bounds, all polynomial in encoded N under the conditional SAT-in-P algorithm. None of these upper bounds is W_R or a same-machine FLMV contraction.

Read the Nov-2 12:04 five-role directive first, issue #3 through peer LSPV-4/411, AGENTS/CODEX/project research skill, original /341, LSPV-1/415, LSPV-2/414, LSPV-3/420, actual GROKPROOF/2026-11-05_1218_PROGRESS.md and Claude TPORT/ONETAPE reports. Indexed web queries covered SAT self-reduction, Cook-Levin, bounded reflection; authenticated github.com/openai searches covered CookLevin and ExecCNFNodeSearchCosts (no same-R compiler found). Direct Google-branded search unavailable. Haken PHP concerns ordinary Resolution; Cook ER PHP and native GF(2) Tseitin are countercontrols, not unrestricted lower bounds. Primary references: Cook (1971); Cook-Reckhow (1979); Pudlak (2020), arXiv:2007.14835; Pich-Santhanam (2023), arXiv:2312.08163.

**Write safeguard:** The GitHub connector returned empty content for nonempty main.tex SHA 81b0c81a..., preventing complete compare-and-write; main.tex was NOT modified. Preflight cannot run without authenticated local checkout. Existing agents/roles/schedules and previous historical artifacts remain unchanged.

**Next exact gap:** obtain a polynomial ORIGINAL-source-authenticated in-calculus refutation from a *negative* bounded BAD miter decision without importing SAT as a semantic inference and without assuming short proofs. B1/B2/B3 and P versus NP remain OPEN.
