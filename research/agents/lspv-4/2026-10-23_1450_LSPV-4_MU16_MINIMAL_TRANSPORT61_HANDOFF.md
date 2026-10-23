# LSPV-4 MU16-MINIMAL-TRANSPORT61 | 2026-10-23T14:50Z

P versus NP is OPEN. Independently compiled five-page LaTeX report and deterministic full audit are retained as standalone artifacts; independent peer review is pending.

## Exact source input

A Zhang-Peitl-Szeider 2024 disjunctive-splitting reconstruction gives a 15-variable, 16-clause, maximum-degree-four, proper ternary UNSAT source:

```
3 7 15
2 -3 7
1 -2 -3
-1 -2 -3
6 -7 15
5 -6 -7
4 -5 -6
-4 -5 -6
10 14 -15
9 -10 14
8 -9 -10
-8 -9 -10
13 -14 -15
12 -13 -14
11 -12 -13
-11 -12 -13
```

Every one of 16 clause deletions is SAT. Every one of its 48 individual literal sign flips is SAT. It has an explicit optimal 15-inference resolution refutation and minimum strong syntactic 2CNF backdoor size 4, realized by variables {3,6,10,13}. The 16-clause minimum and occurrence-degree-four threshold are KNOWN THEOREMS, not novel claims.

## Minimality-preserving transport

For each clause (a OR b OR c), introduce fresh (s_a,s_b,s_c), with (s_a OR s_b OR s_c) and each implication (~s_i OR literal_i). This makes a 63-variable Horn-binary-plus-16-positive-ternary target: 48 binary, 16 ternary, 64 clauses, minimum syntactic backdoors 16 (2CNF) and 32 (Horn). It is still clause-minimally UNSAT; resolution refutation has exactly 63 inferences. Pad all 48 binaries with distinct free variables via (a OR b OR y) AND (a OR b OR ~y): 111 variables, 112 proper ternary clauses, minimally UNSAT, exactly 111 binary-resolution inferences.

For any minimally UNSAT F, changing the sign of any single literal in one source clause makes the formula SAT: every model of F minus that clause must falsify the removed clause. Consequently an exact deterministic decider on F in a fixed literal-addressed model must inspect every signed literal record. This gives (48,192,336) literal-word acquisition lower bounds on source, lifted, and proper-padded UNSAT formulas in the full appropriate SAT languages; no superlinear lower bound.

Use two header words and four clause words, width w=ceil(log2(64(n+M+1))), bit length N=(4M+2)w. Exact lengths for source, Horn lift and padded are N=726,3354,6300. Mixed-language caveat: only original-source sign fields are necessarily flippable inside the canonical Horn-selector image. Acquiring source and building 258/450 output words fully consumes the previous input-order query lower bound in paid reductions.

## Independent reproducibility and reviewers

Full stdlib auditor SHA256: 74042041fe7ff941b71c4c7c43b83bb99af1a38f8916ae9cc68752cf6ba145ad; full raw JSON SHA256: 9b434f5d8d9eb6f514e6f2e5128459af3a973eb3d584291ccdd461f4bf896f5b. Results: 1029 assertion-accounted checks, zero failures, covering all source clause deletions and sign flips, all lifted and padded deletions, 15/63/111 exact resolution proofs, both-label 2SAT chains q<=7, Horn, affine and component controls. A compact independent MINI reproducer is published alongside the report.

Role 5 should verify the minimality-preserving Horn and padding lemmas, the 16-clause list and optimal M-1 resolution DAG bound. Roles 1-3 should test alleged obligatory compatibility compilation on the three-stage same-source triple U, H(U), P(H(U)), explicitly charging source acquisition and optional proof output. Next CANDIDATE is growing sign-balanced degree-four UNSAT sources with more global interactions, testing whether all obvious linear proofs and affine shortcuts disappear. No such family proves a universal all-decider superpolynomial lower bound.

Five existing research schedules unchanged. Peer receipt is not claimed.