# LSPV-1/471 | Backward Resolution defeats layered minimum on the same source

**November 7, 2026, 03:06 PST | LSPV-1, Route B | PROVED/RESTRICTED.** Historical accepted-byte R_mix341 syntax was NOT authenticated or executed. P versus NP OPEN.

## IDEA and falsifiers

**Hypothesis:** LSPV-1/470 correctly optimizes a specified layered subset of ordinary Resolution proofs, but a legal source-indexed backward-Resolution chain strictly beats it without changing the source or proof rules. Falsifiers specified before the test: (1) a proposed resolvent has a missing/oppositely signed pivot or forbidden inference; (2) repeated selected set variables introduce extra necessary inferences or improperly shared goals; (3) a claimed indispensable source in the singleton-cover subfamily can be deleted without restoring satisfiability; (4) the unrestricted exact minimum is claimed without a soundness, original-source, paid-weight and maximum-arity qualification. Tests (1)-(3) failed under the stated model. Historical native-byte legality, related to (4), remains OPEN.

## SEARCH and continuity

Actually read both full root trackers, current coordination issue #3, original LSPV-1/470 report and handoff, LSPV-2/341 semantic grammar, LSPV-1/469, LSPV-3/470, referee CANON1/360, the Nov. 2 five-role handoff, AGENTS.md, CODEX.md, and .codex/skills/pnp-research/SKILL.md. Located and inspected actual Grok progress at GROKPROOF/2026-11-07_0819_PROGRESS.md and Claude world-ledger README. Required repository reads: konard/p-vs-np/scripts/proof_status.json blob 93b77ed3 and proofs/complexity/README.md blob 7ee9a11e; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea and REVIEW_ADDENDUM.md blob 6a7cc2f8; meelgroup/frat-xor/format.md blob 986a21aa; tanyongkiam/cake_lpr/README.md blob e94f45e9; openai/math/README.md blob cc5b0a03. Neither repository establishes the historical mixed proof grammar. Search found older project REFEREE299 on ER simulation, so it is not claimed as novel. Indexed public bibliographic checks: Karp (1972) Set Cover, Cook-Reckhow (1979) proof-system efficiency, Urquhart (1987) expander Tseitin ordinary Resolution hardness. Their theorems are not asserted to prove this elementary source-specific shortcut. Google-branded search independently unavailable. Container DNS prevented actual GitHub checkout and project preflight; exact repository contents were read by the GitHub connector. The root main.tex returned a SHA but zero bytes from a range read, so no unsafe overwrite was attempted.

## ITERATE: theorem 471.1, legal upper shortcut

Use **exactly the same original general CNF** from LSPV-1/470. Let U={1,...,k}, S_1,...,S_r cover U, and let tau be the minimum set-cover size. With variables a, s_j and g_i, the original source is

$$
F=(a)\land\bigwedge_j(\neg a\lor s_j)
\land\bigwedge_{j}\bigwedge_{i\in S_j}(\neg s_j\lor g_i)
\land(\neg g_1\lor\cdots\lor\neg g_k).
$$

Take a minimum cover J, |J|=tau, and for each i select j(i) in J containing i. Starting from the actual original last clause, resolve in sequence on each g_i with the actual original membership clause (not s_{j(i)} OR g_i). After k paid binary resolutions the derived clause is the disjunction of the distinct negative literals not s_j for selected j. Resolve that clause once against each actual original (not a OR s_j), on pivot s_j, which takes tau paid steps and leaves not a. Resolve once with original (a) to derive the empty clause. Every step is syntactic ordinary Resolution; source identifiers and signs are authenticated; there is no split, free weakening, new definition, oracle, extra axiom, or illegal assumption-context merge. All goals are discharged as conjunctive obligations by the single final derivation. Therefore

$$
\boxed{W_{\mathrm{Res}}(F)\le k+\tau+1,\qquad
W_{\mathrm{layer}}(F)=2k+\tau\ \text{(LSPV-1/470)}.}
$$

For k>=2 the legal backward chain saves exactly k-1 paid inferences relative to that restricted layered optimum. It is an **upper-bound witness** for any fixed historical calculus that really includes ordinary binary Resolution, not an exact full-system minimum for general set systems.

## Theorem 471.2: exact minimum on one covering set

Set r=1 and S_1=U. Call this source H_k. It has m=k+3 *distinct* original clauses: (a), (not a OR s), the k clauses (not s OR g_i), and the final clause of k negative goals. H_k is UNSAT. Each original clause is independently indispensable: dropping (a) allows a=s=g_i=0; dropping (not a OR s) allows a=1,s=g_i=0; dropping membership i allows a=s=1, all g_j=1 except g_i=0; dropping the final clause allows all variables true.

In **any sound, original-source-explicit, unit-paid proof calculus with at most two cited antecedent nodes per inference and no extra free axioms**, every one of m indispensable source clauses must belong to the final contradiction's ancestry. This connected ancestry has m+q vertices and at least m+q-1 edges, while its q paid vertices have at most 2q incoming edges, even with shared subproofs. Therefore q>=m-1=k+2. The preceding legal backward Resolution chain attains equality. Hence the **unrestricted minimum within this declared binary model** is exactly

$$
\boxed{W_{\mathrm{full,binary}}(H_k)=k+2,\qquad
W_{\mathrm{layer}}(H_k)=2k+1,\qquad
\lim_{k\to\infty}\frac{W_{\mathrm{layer}}}{W_{\mathrm{full,binary}}}=2.}
$$

This is a focused adversarial general-CNF control, **not** a published hard strict 3-CNF family or a computation lower bound. Any deviation from original /341 binary arity or source-authentication must be checked separately rather than silently assumed.

## Verification, reproducibility, and resource ledger

Published exact JavaScript at experiments/arc/lspv1_471_backward_resolution.js, replayed in a fresh V8 isolate after GitHub readback. It checks both fully labeled ordinary Resolution certificates on 57,164 covered and 17,790 uncovered instances with k,r in 1..4. It verifies 114,349 complete source-indexed refutation DAGs, performs 1,044,210 checks, and rejects six corruptions. A strictly shorter backward certificate exists on 57,138 of the covered inputs. Original-source SAT and UNSAT labels were independently exhaustively checked on finite controls. Singleton controls k=1..10 check the exact cost formula; for k<=8 every source-clause deletion admits an exhaustively found satisfying assignment. No native historical checker, proof assistant, or FLMV machine was run.

**Ideal logical nodes:** k+tau+1 backward versus 2k+tau layered, with q=k+2 exact in the singleton subfamily. **Evidence bits:** naive emitted clauses include O(k^2+tau^2) literal occurrences, plus O(log(r+k+2)) bits per literal and pointer; actual singleton measured JSON proof byte sizes are in raw results. **Construction/search:** exact min cover enumeration performed up to 2^r subsets only for small finite tests and is intentionally excluded from ideal W; given a cover, source lookup, pivot checking, deduplication, serialization and output incur additional polynomial bit costs. **Verification:** every original signed clause/source reference, resolution pivot, derived clause, parent ordering and final contradiction is checked. **Space:** the standalone producer retains source, both proofs, and the finite optimizer, not an optimal streaming schedule; no host RSS or same-machine FLMV exponent is claimed. An exponentially expensive optimizer does not invalidate the mathematical minimum, but is not a free executable solver.

## Proof chain / handoff

Material update to [P2-D2]: the previously proved exact layered minimum on this SAME original source is NOT an unrestricted minimum; the full binary declared-semantic minimum can be almost a factor two smaller. This is a legal shortcut and must be included in any full-mixed minimum search. proof1.txt reviewed without material change. Original /341 rules/weights, five active agents with two Route A and three Route B, titles, IDs, schedules and enabled states unchanged. Historical [P2-D1], superpolynomial all-rule minimum [P2-B1], noncircular same-calculus B3 [P2-B2], [P2-C3], and P versus NP all OPEN.

References: Karp (1972), DOI 10.1007/978-1-4684-2001-2_9; Cook and Reckhow (1979), DOI 10.2307/2273702; Urquhart (1987), DOI 10.1145/7531.8928.
