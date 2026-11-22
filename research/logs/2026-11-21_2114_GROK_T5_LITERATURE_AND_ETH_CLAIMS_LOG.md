# Grok research log: strict T5 resource lower bounds

Date: 2026-11-21 21:14 PST

## Searches performed

- Web: strict T5, Tseitin DNNF/DLDD, cumulative memory (Beame-Kornerup), transformers counting, streaming approximate counting.
- GitHub user:j15marti: located pnp repository containing the exhaustive handoff and coordination files.
- GitHub org:openai: math repository with SubexponentialSAT Lean formalization claiming ETH false.
- GitHub anthropics/formal-math: eth/ folder with Lean 4 formalization of 2^{o(n)} algorithm for 3-SAT/#3-SAT.

## Key findings from literature and official repositories

OpenAI (openai/math, preprint dated October 25 2026) and Anthropic (anthropics/formal-math/eth, paper by Claude) both claim deterministic subexponential-time exact counting algorithms for k-CNF formulas, of the form 2^{O(n log log n / sqrt(log n))}. Lean formalizations exist and have been kernel-checked with standard axioms. Independent review by Impagliazzo, Paturi, Williams et al. is ongoing. The algorithms are asymptotic and galactic for practical n; they do not resolve P versus NP. Both labs note that the speedup does not transfer through arbitrary polynomial reductions to all of NP.

Related classical results remain: Beame-Kornerup cumulative memory lower bounds (ICALP 2023 / TOCT 2025) convert many time-space tradeoffs into CM bounds of matching strength for randomized and quantum models. DNNF lower bounds for high-treewidth Tseitin and independent-set predicates (de Colnet-Mengel, Itsykson et al.) are representation-specific. One-tape crossing-sequence quadratic lower bounds are classical (Hartmanis).

## Relevance to the strict T5 program

The handoff correctly forbids using ETH, SETH, or #ETH as premises for unconditional claims. If the ETH refutations hold, they remove one common source of conditional hardness for SAT and counting, but they supply upper bounds, not lower bounds. They do not construct a polynomial-size unrestricted circuit for the encoded count map of high-treewidth instances, nor do they refute the model-specific quadratic time / cubic CM lower bounds for the sparse matching families on single-tape machines.

The encoded-count circuit target C_N (section 17 of the handoff) remains the clean unrestricted route. A subexponential #SAT algorithm implies that the corresponding count map has subexponential circuit size under suitable uniformity, but this is still superpolynomial and does not contradict a polynomial-time cap only if the circuit simulation overhead is controlled; the handoff's transfer already accounts for the log factor.

No new unrestricted superpolynomial lower bound for exact #T5 or #SAT was located. Representation lower bounds and restricted-architecture progress bounds remain the strongest available unconditional statements inside the project.

## Status

Unrestricted superpolynomial exact-counting lower bound: OPEN.
P versus NP: OPEN.
Model-specific single-tape T=Ω(N^{2}), CM=Ω(N^{3}) for matching families: retained as audited project theorems.

## Next concrete task

For the Bounds role: attempt a target-specific lower bound on C_N for a high-treewidth NAND/expander family under the explicit bit encoding, or construct a concrete pseudoentropy pair that is indistinguishable to all circuits of size N^a log N. Check against the affine/Tseitin control (easy counting, hard representation).

This log is an additive research record. It does not promote any theorem.
