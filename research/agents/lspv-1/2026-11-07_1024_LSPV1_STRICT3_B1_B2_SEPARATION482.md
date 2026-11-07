# LSPV-1/482: B1 fails but B2 holds for one decider in a fixed algebraic proof calculus

**November 7, 2026, 10:24 PST | Route B lead | PROVED/RESTRICTED (dependent on Pang 2026 preprint); COMPUTATIONAL finite controls | P versus NP OPEN.**

**Nodes:** [P2-B3] gains a stronger-system witness; [P2-F9] is the published hard 3-CNF benchmark; [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. [P1-01] and [P1-X3] unchanged. This result concerns a DISTINCT fixed calculus, not historical R_mix341.

## IDEA -> SEARCH -> ITERATE

**Hypothesis.** Find a previously established, rigorously hard **strict signed 3-CNF** family that a total SAT decider can recognize in polynomial time. Use a deliberately exponential fallback to make B1 fail pointwise while proving B2 for the SAME algorithm. This sharpens the B1/B2 quantifier distinction, not the noncircular B3 transfer.

**Falsifiers declared before search:** (1) lower bound only tree-like or based on observed solver difficulty; (2) sound recognition secretly requires determining expansion or SAT; (3) ordinary Resolution cannot be simulated with constant charged steps by the fixed algebraic calculus; (4) worst-case time in B2 ignores malformed strings or accidentally substitutes pointwise time.

**Search and project continuity.** Inspected entire root proof1.txt (SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and proof2.txt (SHA 067f29c734736c09d14cc25401a3f24046311d37), issue #3 and recent agent comments, governing 2026-11-02 five-role handoff at commit 4e29ed7646f484707767acb6e63ec5f38afd98a8, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, LSPV-1/481, LSPV-3/477 and /478, GROKPROOF/2026-11-07_1815_PROGRESS.md (blob 0532370c9bf99b1204be4e0efd9ef96290454ec7), and Claude 2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex (blob 79e4d4e7e0e3edff3aba8610852c45534bdde128). Required external sources actually read: konard/p-vs-np/scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and REVIEW_ADDENDUM.md blob 6a7cc2f8962d3fcfcfc1778b1d3d8f5dc8d56d70; meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f; tanyongkiam/cake_lpr/README.md blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c; peitl/short-proof/README.md blob 93d2090dba9739bc4983c65ea639a24e1f5e0fab; openai/math/README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae. They supply formats and critiques, not historical rule authority. Exact primary source read as HTML: https://arxiv.org/html/2610.00837v2, dated 24 October 2026, Theorem 7.2(b,e), standard syntactic rules §1. Indexed web search used; no distinct Google-branded search interface. No PDF analyzed.

**Duplication and change.** Tracker [P2-B3] already records a pointwise recognizer counterexample for ordinary Resolution. The new contribution extends the witness to fixed stronger Res(PC_r/F3) and establishes an explicit **positive B2 bound for the same carefully specified total decider**, using a strict 3-CNF source. Initial bit-PHP (Pang 7.2(e), wide collision clauses) was replaced as the PRIMARY example by cubic Tseitin (7.2(b)) to meet the existing hard-3SAT priority.

## Exact source and proof-system ledger

For a connected simple cubic graph G with h even vertices and 3h/2 edges, assign one Boolean variable x_e to each edge. For an odd vector of charges b_v, encode at every vertex v the equation
$$
\bigoplus_{e\ni v}x_e=b_v
$$
by the four proper signed width-three clauses forbidding violating local assignments. The resulting T(G,b) has 4h strict-3CNF clauses, 3h/2 variables and canonical binary-indexed length O(h log h). Summing equations gives 0=1, proving UNSAT. No 3-CNF conversion or unstated preservation is used.

Fix R = syntactic Res(PC_r/F3), for ANY one preselected constant r>=1. In this system a proof line is a disjunction of degree-at-most-r polynomial equations over F3; the permitted axioms/rules include Booleanity, syntactic weakening, combination and deletion of false constants (Pang §1). Choose unit paid weight per distinct inference node and free original-source/Boolean axioms. This is a sound complete effective system DIFFERENT from R_mix341. One ordinary Resolution pivot compiles with at most TWO charged steps: combine opposite literal equations into a nonzero constant equation, then delete that false disjunct. Shared-DAG proofs remain shared.

Pang, arXiv:2610.00837v2, Theorem 7.2(b), applies to fixed-degree regular edge-expander T(G_h,b_h) in modulus q=2 with proof field prime p=3, yielding
$$
S_R(T_h)\ge \exp(c_r h)
$$
for some c_r>0, for ALL legal DAG derivations. At most O(h) free source and Boolean axiom lines are distinct, so
$$
W_R(T_h)\ge\exp(c_r h)-O(h).
$$
This depends on a primary preprint theorem; the present finite code does NOT independently reproduce Pang's proof.

## Theorem 482.1 (PROVED/RESTRICTED): same-decider B1/B2 separation

There is ONE fixed, uniform, total correct SAT decider A on all binary strings for which B1 fails for this R while B2 holds:
$$
\neg\exists p_A\ \forall F\in\mathrm{UNSAT}:
W_R(F)\le p_A(|F|+T_A(F))
$$
and
$$
\exists q_A\ \forall N:
\overline W_R(N)\le q_A(N+T_A^{wc}(N)).
$$

**Proof.** A first parses the given binary CNF and checks, in polynomial time, whether its proper signed strict width-three clauses group into four complementary forbidden assignments per three-variable support, with every variable incident to two groups, the resulting graph simple/cubic/connected, and the total extracted charge odd. All accepted sources are UNSAT by summing the encoded parity equations. No expander recognition and no SAT oracle are used. A rejects these inputs immediately. For every other binary string, including malformed encodings, A performs 2^{|x|} dummy steps and then runs an exact brute-force SAT verifier or returns MALFORMED. Thus A is total, correct on both labels and malformed-aware.

Every member of Pang's hard expander family passes the fast recognizer, so T_A(T_h)=|T_h|^{O(1)} while W_R(T_h)>=exp(c_r h)-O(h); B1 is false.

For ANY N, the malformed 0^N uses the padded path and T_A^{wc}(N)>=2^N. Every valid UNSAT CNF whose encoded length is <=N contains at most N distinct occurring variables, regardless of large numeric names. An exhaustive assignment decision tree yields an ordinary Resolution refutation with <=2^v-1 RES steps: choose a falsified original clause at each leaf and at each internal node either propagate a pivot-independent child clause or correctly resolve the two opposite-pivot clauses. The R compiler charges at most two inferences per RES step. Consequently,
$$
\boxed{\overline W_R(N)\le2(2^N-1)\le2T_A^{wc}(N)}
$$
so q_A(z)=2z+1 is sufficient for the SAME exponentially slow decider A. No B2 claim for all A follows. QED.

## Hostile controls, resources, and limitations

Independent Node finite replay: K4, cube and Petersen original-source odd-charge strict-3CNFs have exactly 0 satisfying assignments; even-charge controls have respectively 8, 32, 64 models. Recognizer accepts odd, rejects even, and rejects signed-literal mutation. Public compact verifier checks 42 assertions and can be executed as plain Node JS; separate full local reproducibility script checked 2,284 assertions, including bit-PHP at ell=1,2,3, ordinary RES derivation with paid counts 5 and 159 for ell=1,2, malformed/empty-CNF and corrupt-pivot controls. No finite graph individually certifies an asymptotic lower bound. Neither checker is the original /341 checker.

Proof logical-work ceiling <=2(2^v-1); evidence bits O(2^v poly(N+v)) for fully output certificates. Actual A charges parsing, recognition, graph connectivity, source access, exponential dummy increments, exhaustive fallback search, malformed handling and all simultaneous writable storage. Constructing a proof would additionally charge discovery, failed candidates, indexing/retrieval, references, output and verification. The offline minimum is free to choose the best legal proof. No actual same-machine FLMV time/space guarantee follows. Host V8 tests measured assertions, not TM steps or peak RSS.

Critical control: over F2 the cubic odd-Tseitin family admits short GF(2) proofs; it is NOT a lower-bound witness across the historical R_mix341 mixed rules. Cook ER and paid definitions are additional possible shortcuts. The exact full historical R_mix341 grammar, legal cross-type interfaces and noncircular B3 transfer are unproved.

**Root manuscript status:** main.tex blob 68188a24badda635a5983fda1c381cdb694fd497 returned zero content; not edited. Historical rules and weights, all five agents and two Route A / three Route B allocation, schedules and enabled states unchanged.

**Outstanding:** [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN. P versus NP OPEN.

## References

[1] Shuo Pang, A Degree–Size Relation for Resolution over Polynomials, arXiv:2610.00837v2, 2026-10-24, Theorem 7.2(b), §1. https://arxiv.org/html/2610.00837v2

[2] A. Urquhart, Hard Examples for Resolution, J. ACM 34(1), 1987. https://doi.org/10.1145/7531.8928
