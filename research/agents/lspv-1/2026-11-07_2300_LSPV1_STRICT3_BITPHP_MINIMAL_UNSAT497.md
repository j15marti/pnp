# LSPV-1/497 | Strict proper-3CNF bit-PHP is clause-minimal: a legal binary-work floor, not superpolynomial hardness
**November 7, 2026, 23:00 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**Affected proof-chain node [P2-F3].** Dependencies [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. Relevant existing [P2-B12] is an earlier *generic* indispensable-source/fanin counting argument: the general combinatorial lemma is NOT new. This result supplies an explicit all-size clause-by-clause minimal-unsatisfiability application to the standard strict-3CNF bit-PHP splitter family, with a paid binary-inference floor and independently replayed deletion witnesses.

## IDEA and falsifiers (precommitted)
Hypothesis: the familiar private-chain strict proper-3CNF expansion of the established bit pigeonhole family is **minimally UNSAT**: removing *any single generated source clause* admits an explicit satisfying assignment. Consequently a source-explicit, sound, conservative-auxiliary, unit-paid, at-most-binary refutation DAG has at least S-1 paid inference nodes for S source clauses, even with arbitrary shared reasoning. This floor is only polynomial and is NOT a claim of [P2-B1].

Four falsifiers: (F1) a pair-hole collision source is redundant in the original bit PHP; (F2) one splitter-link clause is redundant after existentially quantifying its private helpers; (F3) a deletion witness for one link violates an unrelated collision constraint; (F4) sharing or reconvergence invalidates the generic at-most-binary DAG ancestry lower bound. F1-F3 are ruled out by a symbolic witness and independent finite replay; F4 is ruled out by the elementary connected-graph edge count, under the expressly stated arity and cost assumptions.

## SEARCH and continuity
Read BOTH complete live root trackers at start, proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b (18,553 characters) and proof2.txt blob 4c5ef09a141053c89e1304d2ca4a705b322c99d7 (337,180 characters). Read the November 2 five-role handoff, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, issue #3 and latest comments, LSPV-1/496, LSPV-3/491, LSPV-5/427, Grok's actual GROKPROOF/2026-11-08_0320_PROGRESS.md, and Claude's actual research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex. Reviewed required external repo actual files konard/p-vs-np/scripts/proof_status.json (blob 93b77ed3d8fe456f81c690035f45f07910a247f2) and blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (blob 18d693ea71dfa433370eb7afbebc3106e32f03e5) plus its RESIDUAL_EQUIVALENCE_BARRIER_REPORT.md. They provide no general lower-bound transfer.

Primary literature search: Kamil Braun, *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv:2609.23015v2, revised 2026-11-03, proves > exp(n/(32768 ell^2)) nodes in ALL DAG-like Res(XOR) proofs of the ORIGINAL bit-PHP for n=2^ell and ell>=32. Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (2026-10-24), Thm. 7.2(e), claims the stronger exp(Omega(n)) lower bound in Res(PC1/F2) for the original bit-PHP; these are restricted proof systems and Pang is a preprint. Checked Haken 1985 ordinary-Resolution PHP and Cook 1976 Extended-Resolution PHP as required contrasting controls. Project's prior [P2-F3], LSPV-1/480, LSPV-1/453/457 already describe the bit-PHP source, size counts and an **external, distinct extension-variable short-proof control**. This iteration does not claim to invent the family or establish source-hardness preservation into the split encoding. Indexed web search was available, but a separate branded Google interface and independent formal Lean proof replay were not used.

## Exact original family and strict 3-CNF encoding
Set n=2^ell, ell>=2, with pigeons i=0,...,n and holes a=0,...,n-1. Original Boolean variables x_{i,k} encode the kth bit of the hole of pigeon i, for k=0,...,ell-1.

For each unordered pigeon pair i<j and hole a, define the width 2ell collision clause

$$
C_{i,j,a}=\bigvee_{k=0}^{\ell-1} [x_{i,k}\ne a_k]\ \vee\
\bigvee_{k=0}^{\ell-1} [x_{j,k}\ne a_k].
$$

The bracket is the positive literal x if a_k=0 and negative literal not x if a_k=1. It excludes precisely the event that BOTH pigeons i,j occupy a. Original clause count

$$
A=n\binom{n+1}{2}=\frac{n^2(n+1)}2.
$$

Use a fresh set of w-3=2ell-3 private variables z_1,...,z_{w-3} for EACH original width-w clause C=(L_1 vee ... vee L_w). Replace it by the w-2 signed proper width-three clauses

$$
(L_1\vee L_2\vee z_1),\quad
(\neg z_{r-1}\vee L_{r+1}\vee z_r)\quad (2\le r\le w-3),\quad
(\neg z_{w-3}\vee L_{w-1}\vee L_w).
$$

Call the resulting formula H_ell. It is **equisatisfiable** with the original bit-PHP by the standard existential splitter; all 3-clause literals have three distinct variable IDs. Exact counts:

$$
S=A(2\ell-2),\qquad
V=(n+1)\ell+A(2\ell-3).
$$

With ordinary binary variable-ID serialization the encoded input length is Theta(n^3 ell^2), since ell=log_2 n. No claim of a proof-size-preserving simulation of Res(XOR) is made in either direction.

## THEOREM 497.1 (all sizes): H_ell is minimally UNSAT
The pigeonhole principle makes H_ell UNSAT: n+1 binary labels lie among n holes, so some pair collides; the splitter preserves satisfiability.

Take any selected splitter clause indexed by (i,j,a,r), where r is its position in the private chain. Construct a base assignment setting pigeons i,j to hole a and assigning the remaining n-1 pigeons injectively to all other n-1 holes. Exactly one original collision clause C_{i,j,a} is false; every other original collision clause is true.

For each SAT original collision clause D with literals L_1,...,L_w, set its private z_t to 1 precisely when the first t+2 literals of D are all false. This is an extension satisfying every clause in D's private chain. For the selected all-false original clause, let its private z_t equal 1 BEFORE the chosen break and 0 AT and AFTER it (if the first link is removed, all z_t=0; if the last is removed, all z_t=1). Exactly the selected chain clause is falsified, while every other chain clause holds. Hence the formula after deleting this ONE 3-CNF clause is satisfiable. Because the clause was arbitrary, H_ell is minimally UNSAT. QED.

This proves the claim for all ell>=2 without enumerating exponentially many truth assignments. It does **not** assert that every assignment or every resolution path is expensive.

## COROLLARY 497.2: charged source-ancestry floor in a QUALIFIED binary system
Let R' be a sound, complete or incomplete, source-explicit refutation calculus on H_ell with the following extra qualifications: every inference node has at most TWO immediate proof premises; all non-source auxiliary axioms are conservative and cannot make an originally SAT source unsatisfiable; every inference node costs at least one unit; and the final contradiction's directed ancestry contains every necessary source premise. A proof omitting any one source clause would refute a SAT formula and violate soundness/conservativity, so all S distinct clauses must occur in the contradiction ancestry.

Let a be the number of paid inference nodes. The underlying undirected ancestry graph is connected with at least S+a vertices, thus at least S+a-1 edges, but each inference has indegree at most two, thus at most 2a edges. It follows that

$$
\boxed{W_{R'}(H_\ell)\ge S-1=A(2\ell-2)-1.}
$$

Sharing, reconvergence, legal affine deductions and optimal after-the-fact choice do NOT evade the source/fanin counting argument; source-implicit mass imports, uncharged multivariate rule calls, higher-arity joins, and zero-weight nodes are explicitly outside this corollary. Under minimum positive inference weight w_min replace S-1 by w_min(S-1). This is only an **Omega(N/log N) source-length-scale floor**, not a superpolynomial lower bound. No full historical R_mix341 grammar/weight conclusion is asserted.

The bound does NOT imply that any proposed system has proofs *attaining* S-1. It is a lower bound, not an exact value of W_R'. Its semantics are independent of the certificate search cost. Distinguish logical node work from bit serialization and actual time/space.

## ITERATE and reproducibility
Independent Python and separately implemented JavaScript constructions **executed**, each creating the original bit-PHP and every signed 3-CNF clause, then for **every** deleted source clause constructing an explicit total satisfying assignment of all remaining clauses and verifying that exactly the indexed target clause fails. Both report:
- ell=2, n=4: 40 long clauses, 80 strict-three clauses, 50 variables, 80 exact deletion witnesses; binary unit-work floor 79.
- ell=3, n=8: 288 long clauses, 1152 strict-three clauses, 891 variables, 1152 exact deletion witnesses; binary unit-work floor 1151.

These are exhaustive over **source-clause deletions**, NOT an exhaustive search over arbitrary proof DAGs or all Boolean assignments. The Python program additionally checks original clause uniqueness. No R_mix341 historical native checker, Res(XOR) checker, or Lean formalization was executed. Python timing: 0.004 seconds / 0.841 seconds for ell=2 / ell=3; JS runtime separately executed with identical structural outcomes. Dedicated code and machine-readable raw results are published. Hostile controls were different deleted links including first, internal and last, proper-three-variable tests, and exact falsified-clause indexes.

Work/space disclosure: the finite programs explicitly materialize O(S) source clauses and up to O(V) assignment bits per witness, then rescan O(S) clauses for each of S deletions, giving O(S^2) time times literal evaluation overhead and O(S+V) live storage excluding output. This is *verification expense*, not the proof-DAG minimum. Constructing a single witness is polynomial in V+S. The general symbolic proof does not require running the enumerator. A fully implemented actual SAT decider would separately charge input reads, source authentication, all search and all-phase live memory.

## Interpretation and exact remaining gap
The **original** bit-PHP has a published unrestricted shared-DAG Res(XOR) lower bound (Braun, strengthened in Pang). The **split strict-3CNF** H_ell is now explicitly proven *minimally UNSAT*, which yields a robust **linear-in-source-count** work floor in qualified binary calculi. Minimal unsatisfiability alone CANNOT inherit Braun/Pang's exponential bound. Conversely, Cook's polynomial Extended-Resolution pigeonhole proofs and the project's FACET-A shortcut controls show why paid extension definitions are dangerous for any naive universal invariant. To transfer the original lower bound, the actual missing direction is a polynomial simulation converting every short FULL historical mixed proof of H_ell into a legal original-source Res(XOR) proof, including all native definitions, GF(2), Resolution, LOCAL-CONVERT, branching/assumptions, and sharing. No such simulation exists in this report; it may be false. All candidate upper shortcuts must remain admissible in R_mix341 if historically legal.

Ledger: Original BPHP, source A=n^2(n+1)/2 width-2ell clauses, Braun/Pang unconditional/research-preprint restricted Res(XOR) DAG bounds, no mixed transfer. Split H_ell, S=A(2ell-2) strict proper 3CNF clauses, all-size minimal UNSAT proven, binary unit-paid W>=S-1 under stated rule qualifications, full mixed W UNKNOWN. Hall/ER extensions remain polynomial upper controls in different calculi; no historical native definition acceptance authenticated.

**Tracker status:** new explicit evidence concerns [P2-F3] only. [P2-D1] historical grammar, [P2-C3] unrestricted transfer, [P2-B1] superpolynomial all-mixed bound and [P2-B2] noncircular B3 remain OPEN. No P=NP/P!=NP proof; keep the 2 Route A / 3 Route B allocation and all tasks unchanged. Root main.tex not edited: complete safe ownership-region read was unavailable and unauthorized replacement would be unsafe.

## Sources and artifacts
1. Braun, K. (2026), *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv:2609.23015v2, original bit PHP, no DAG depth/regularity restriction.
2. Pang, S. (2026), *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, Theorem 7.2(e), fixed Res(PC1/F2), restricted original-source bit-PHP.
3. Cook, S. (1976), *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*. Distinct proof-system upper control.
4. Project [P2-F3], LSPV-1/480 and /453-/457, LSPV-5/427, LSPV-3/491. No novelty claim for standard splitter, PHP source or generic fanin ancestry lemma.
5. experiments/arc/lspv1_497_bphp_minimal_unsat.js and results/raw/arc/2026-11-07_2300_LSPV1_497_BPHP_MINIMAL_RAW.json; independent Python available as a conversation artifact.

**Actual advance:** rigorous per-source-clause deletion witnesses for all sizes in the proper signed-3CNF bit-PHP family and their sharp *necessary* binary-source-ancestry floor. **No unqualified historical mixed work or B3 advance. P versus NP OPEN.**
