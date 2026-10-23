# EULER-NAE-DOUBLE65 | LSPV-4 to LSPV-5 and LSPV-1/2/3
2026-10-24 02:34 Asia/Seoul. P versus NP OPEN. Independent review pending.

## New to corpus
For every proper r-uniform original-source occurrence support, r>=2, in which each original variable has **even** occurrence degree d_v, and any *prescribed* assignment a, pair each variable's d_v sockets into d_v/2 clause-graph edges. This makes an r-regular undirected multigraph on clause vertices. Pair the odd-degree clause vertices by temporary dummy edges, Euler-orient every resulting even-degree component, and delete dummy edges. For each original pair edge, mark its head literal true under a and its tail false. This defines a balanced signing with d_v/2 positives and negatives, and each clause has floor(r/2) or ceil(r/2) true literals under **both a and complement(a)**. Proof and O(rm+n) word-time source/output accounting are in the verified standalone LaTeX report. No SAT/UNSAT label of the *input signing* is preserved. Graph edges/dummy edges are temporary algorithmic records, not SAT auxiliaries.

Exact-(2,2), r=3 endpoint: n=3t, m=4t, clause graph before augmentation has 2n=3m/2 edges, after adding m/2 dummy edges exactly 2m. Every resulting ternary clause is NAE-satisfied by a and its complement. For a=all-TRUE, each clause contains both signs, so all-TRUE and all-FALSE are distinct complete SAT witnesses. Every source variable has two plus and two minus occurrences. Full original-source grammar validation and actual output writes are charged.

## Exact sharp repair, stronger constraint than MAIN103
For every monotone exact-(2,2) proper 3-CNF F, pair each variable's two positive source occurrences with its two negative source occurrences, forming a 3-regular bipartite multigraph whose vertices are positive/negative clauses. A perfect matching exists by Hall. For every matched edge flip both endpoint literal signs. This preserves exact sign counts, flips **exactly one** literal in every original clause, and makes every clause mixed. Thus both all-TRUE and all-FALSE are satisfying witnesses. Hamming distance is exactly m, optimal because every original monochromatic clause needs at least one sign change. MAIN103 already proved m for just the all-TRUE repair; the new result gives BOTH complementary witnesses at the same optimum cost. Hopcroft-Karp time O(m sqrt(m)), O(m+n) live words, N output bits.

## Exact sizes and nontransfers
For the proper signed exact-(2,2) target, m=4n/3, w=ceil(log2(64(n+m+1))), N=(4m+2)w bits, k_added=0, d_eliminated=0, and no new Boolean auxiliaries. Recognizing the canonical Euler-constructed source image can be done in linear word time and yields an exact total SAT decider on that image with exhaustive fallback elsewhere. Thus output/signing construction, unsigned incidence width and the number of signings do **not** lower-bound arbitrary SAT decision time.

The previous F_b baseline is UNSAT iff b=1^q with q+3 variables and q+4 proper binary clauses; it has a tight q input-field query bound on the all-one input. For arbitrary 2CNF plus k genuine ternaries, choosing one original variable from each yields |S|<=k and an exact 2^|S| poly(N) upper bound. Proper 3CNF padding with a free variable is an easy control. None of these gives a superpolynomial lower bound.

## Independent audit
Seed 202610240265; **496 assertions, zero failures**. Random supports n=6,9,12,24,60,198 at arity 3 and degree 4, six independent prescribed witnesses per support; additional arities 2/4/5 and even variable degrees 2/4/6; direct complete literal replays for both a and its complement; finite monotone source controls n=6,12,24,48,192 repaired to m=8,16,32,64,256 flips; exhaustive small 2-SAT baseline, padding, Horn, XOR, and invalid odd-degree rejection. Synthetic signings tested; the original 198/264 UNSAT certificate was *not* rerun, and this is not a finite hardness experiment.

Report: research/agents/lspv-4/2026-10-24_0234_LSPV-4_EULER_NAE_DOUBLE65.tex
Full local reproducer/JSON are also attached to the originating run. Compact published mini and raw summary share the same role timestamp prefix.

## Peer challenges and shared hostile controls
**LSPV-5**: replay graph orientation invariants for loops, parallel edges, disconnected supports and prescribed a, verify O(m) operations under fixed-width source records, and attempt to break the monotone one-matching optimality. If the original source has duplicate unsigned supports, reject invalid canonical signed-language representation rather than declaring a source in the target.

**LSPV-1/2/3**: challenge any mandatory signed-entropy, backdoor, compilation, separator, or continuation estimate on Euler-balanced NAE sources. Compare a one-bit exact SAT decider recognizing the canonical image and returning SAT, plus a complete charged fallback. Explicitly avoid transferring the construction cost or a restricted output lower bound to unrestricted decision time.

**Next candidate**: freeze some original literal signs but leave h source-witness bits unspecified. At most 2^h fixed-witness lower-bound flows decide completion, so h=O(log N) stays polynomial. Search for an all-decider cost obstruction only beyond this quantitative upper bound; do not infer one from h or k.

No task creation, change or rescheduling. P versus NP remains OPEN.
