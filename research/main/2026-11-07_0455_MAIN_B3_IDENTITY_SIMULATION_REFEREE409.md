# LSPV-5/409 — exact B3 identity-system boundary and rejecting-trace firewall

**2026-11-07 04:55 PST | Route B independent red team | PROVED/RESTRICTED quantifier theorem; COMPUTATIONAL finite controls | historical R_mix341 B3 and P versus NP remain OPEN**

## IDEA -> SEARCH -> ITERATE

### Initial claim, falsifiers, and revision

Initial hypothesis: SAT in P does not by itself force polynomial minimum work in every preselected sound, complete, effective proof calculus. Predeclared falsifiers:

1. every such fixed calculus is automatically polynomially bounded if SAT is in P;
2. a mandatory source-length-dependent chain necessarily destroys soundness, completeness or effectivity;
3. a locally valid rejecting computation trace alone proves source UNSAT;
4. Cook--Reckhow's existence theorem already quantifies over the historical fixed $R_{\mathrm{mix341}}$.

Tracker review showed that the clock construction is **prior project work**, `[P2-B6]`/LSPV-1/462. It was not repackaged as new. The idea was revised to the exact missing quantifier: construct the decider-indexed identity proof system $Q_A$, distinguish existential weighted-size simulation from uniform $p$-simulation, and prove exactly which statement is B3 and which stronger statement could establish B3 noncircularly.

Falsifiers 1, 2 and 4 are already defeated by Cook--Reckhow's quantifiers plus `[P2-B6]`. Falsifier 3 is defeated by the strict-3CNF trace control below. The new result is Theorem 409.1, not the inherited clock example.

## Required state and search record

Complete current trackers read before work: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and `proof2.txt` blob `58a8386e56822de300912b35ee955c021962d27a`. Exact affected IDs are `[P2-B2]` and new `[P2-L5-409]`; relevant prior IDs are `[P2-B3]`, `[P2-B6]`, `[P2-L1-466]`, `[P2-L1-462]`, `[P2-L5-408]`, `[P2-L1-473]`, and `[P2-L3-472]`.

Also read: governing five-role handoff blob `c3889a3e514ddbd747150dcb68607013a3b2d154`; current issue #3; `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`; `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`; complete project research protocol blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`; current Grok `GROKPROOF/2026-11-07_1119_PROGRESS.md` blob `d87fcb3a12ed115c277f7ffda87ecca0f4072630`; and actual Claude `research/agents/claude/world-ledger/README.md` blob `de75a371ce3143a4495e6892df7fb04794a6b708`.

Newest peer evidence read directly:

- `[P2-L1-473]`, `research/agents/lspv-1/2026-11-07_0422_LSPV1_RANDOM_PEEL_AFFINE_FLOOR473.md`, blob `b62cb5c2b14bf58dfa7ae59647fff5f8df77536b`: a source-local affine peeling floor for the published Resolution-hard random proper-3CNF distribution. It does not exclude full mixed derivations.
- `[P2-L3-472]`, `research/agents/lspv-3/2026-11-07_0438_LSPV3_CORE_CAPACITY_TRANSFER_BARRIER472.md`, blob `8098bae1dfcb57448d08f4e4ebae8af9d0f81fb6`: source-core and antecedent-arity counting alone cannot yield a superpolynomial all-mixed lower bound because the minimum core has at most input-linear many clauses. This is a method ceiling, not an upper bound on actual $W_R$.

Primary source: Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44(1), 1979, Definitions 1.3 and 1.5 and Propositions 1.4 and 1.6. They prove existence of **some** polynomially bounded proof system for a language in NP and prove that a system which $p$-simulates a polynomially bounded system is polynomially bounded. They do not say every preselected proof system is polynomially bounded. The p-optimal proof-system literature was reviewed as a stronger sufficient route; no p-optimality theorem for historical $R_{\mathrm{mix341}}$ was found.

Required repository review was change-aware and unchanged at the relevant pinned files: `konard/p-vs-np` README `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` and proof-status JSON `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research` method index `18d693ea71dfa433370eb7afbebc3106e32f03e5` and audit addendum `6a7cc2f8962d3fcfcfc1778b1d3d8f5dc8d56d70`; FRAT-XOR format `986a21aa92b62f844ef1fce852193142c41b2b1f`; CakeLPR README `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; short-proof README `93d2090dba9739bc4983c65ea639a24e1f5e0fab`; CNFgen README `9fba4e26f2a4cd10444a7226a7a3a7caa1762721`; OpenAI math `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`; Anthropic formal-math `1df53bfc14a022088d1b5757698f692bf79390b4`; and `kbr-/math-research` `7d393e0878b739f7c3d37d6baaf1ff83949d3c53`. None authenticates the missing same-calculus compiler. Google-branded search was unavailable; public primary-source web search was used.

## Established-family ledger and mandatory shortcuts

| Family | Exact encoding and size | Established theorem/model | Known shortcut or control | Remaining transfer |
|---|---|---|---|---|
| Odd-charge cubic-expander Tseitin strict 3-CNF | One variable $x_e$ per edge. At cubic vertex $v$ with edges $e_1,e_2,e_3$ and charge $\chi_v$, include the four clauses $\bigvee_i\ell_{e_i,a_i}$ indexed by assignments $a$ with $a_1\oplus a_2\oplus a_3\ne\chi_v$, where $\ell_{e,0}=x_e$, $\ell_{e,1}=\neg x_e$. For $h$ vertices: $3h/2$ variables, exactly $4h$ proper clauses, indexed length $N=\Theta(h\log h)$. Odd total charge certifies UNSAT. | Urquhart: $2^{\Omega(h)}$ ordinary shared-DAG Resolution size on suitable expanders. This is Resolution-only proof-size hardness. | The four local clauses encode a parity row; declared-semantic AND3/GF(2) gives a $4h-1$ paid-node proof. `[P2-L3-472]` shows source-core/arity capacity alone cannot improve this to superpolynomial work. | Exact historical bytes, weights and all-rule lower-bound survival remain `[P2-D1]`, `[P2-B1]`, `[P2-C3]` OPEN. |
| Chvátal--Szemerédi random proper 3-CNF | Choose $m=cn$ signed proper clauses from the $8\binom n3$ possibilities in the published random model; encoded length $\Theta(n\log n)$ for constant $c$. | For suitable fixed density (the project uses $c=8$), UNSAT and $2^{\Omega(n)}$ ordinary Resolution hardness hold with high probability. This is distributional Resolution proof-size hardness, not an individual certificate. | `[P2-L1-473]` proves every source that is fully eliminable by its source-local affine peeling rule is SAT with full affine rank; therefore an UNSAT hard sample has a nonpeelable remainder. That does not exclude indirect Resolution, definitions, GF(2), branching or other mixed shortcuts. | No all-rule $R_{\mathrm{mix341}}$ transfer or certified individual instance follows. |

Cook Extended Resolution, native affine/Tseitin summation, legal branching and shared-DAG proofs remain mandatory upper-bound controls. Certified UNSAT, restricted proof-size hardness and empirical difficulty are not interchangeable.

## The exact B3 boundary

Fix the historical candidate calculus $R$ before inputs. Assume SAT is in P and fix a uniform total polynomial-time decider $A$ for UNSAT (the complement of SAT). Define the **identity proof system** $Q_A$ by the verifier

$$
V_{Q_A}(F,\pi)=1
\quad\Longleftrightarrow\quad
\pi=\operatorname{encode}(F),\ F\text{ is a valid CNF},\ A(F)=\mathrm{UNSAT}.
$$

Under the assumption that $A$ is correct and polynomial-time, $Q_A$ is a sound, complete, polynomial-time proof system for valid UNSAT CNFs. Every UNSAT source $F$ has the identity proof $\pi=\operatorname{encode}(F)$ of exactly $N=|\operatorname{encode}(F)|$ bits.

Define **polynomial $W$-size simulation** $Q_A\le_W R$ to mean that some fixed polynomial $p$ satisfies

$$
V_{Q_A}(F,\pi)=1
\quad\Longrightarrow\quad
W_R(F)\le p(|\pi|)
$$

for every accepted pair. This definition concerns the minimum historical weighted-node work and does not assume a proof generator.

**Theorem 409.1 (PROVED/RESTRICTED, exact quantifier boundary).** Under SAT in P and correctness of $A$,

$$
\overline W_R(N)\le \operatorname{poly}(N)
\quad\Longleftrightarrow\quad
Q_A\le_W R.
$$

**Proof.** If B3 holds, then every UNSAT $F$ of length $N$ has $W_R(F)\le p(N)$. The only accepted identity proof has $|\pi|=N$, so $Q_A\le_W R$. Conversely, if $Q_A\le_W R$, every UNSAT $F$ has accepted identity proof $\pi=\operatorname{encode}(F)$ and therefore $W_R(F)\le p(N)$. Taking the maximum over valid UNSAT sources of length at most $N$ gives polynomial $\overline W_R(N)$ after replacing $p$ by a monotone polynomial envelope. $\square$

This is an exact diagnostic equivalence, not an independent proof of B3. Asserting $Q_A\le_W R$ without proving it for the fixed native rules merely restates B3.

### Stronger noncircular sufficient condition

Suppose instead there is a uniform polynomial-time compiler $C$ such that every accepted $Q_A$ pair is mapped to explicit bytes of a legal, source-authenticated historical $R$ refutation of the same $F$. Suppose the complete output has polynomial bit length and every historical node has its fixed bounded nonnegative weight. Then the output contains polynomially many paid nodes and has polynomial total weight. Hence B3 follows.

This compiler condition is stronger than existential $W$-size simulation and can be attacked rule-by-rule without assuming B3. It must authenticate source IDs, rules, exported/private wires, definition freshness, assumption scope and final contradiction. A compiler to FRAT-XOR, Extended Resolution, a proposed CANON system, or another checker is not a compiler to historical $R$.

Cook--Reckhow Proposition 1.6 supplies the analogous standard proof-length implication: a system which $p$-simulates a polynomially bounded system is polynomially bounded. A p-optimal $R$ would therefore suffice, but no such theorem is available for historical $R_{\mathrm{mix341}}$. Standard proof-bit length and project weighted-node work also require an explicit translation; one cannot silently identify them.

`[P2-L1-466]` is the complementary direction under extra hypotheses: if native proofs have a polynomial compact-bit bound and a polynomial checker, then B3 plus SAT in P yields a polynomial generator by witness-prefix self-reduction. Those compactness/checker premises remain unproved. The present theorem does not duplicate that result.

## Rejecting-trace firewall

A checker that validates only an input hash, local machine transitions and a final `REJECT` state is not a source-UNSAT proof system uniformly over programs. Let $P_{\mathrm{all-reject}}$ transition immediately from `start` to `reject`. Its trace is locally valid for every source, including satisfiable sources.

Fixing $P=A$ and assuming semantic correctness makes the decider-indexed $Q_A$ sound, but it does not make the trace a native $R$ proof. A B3 bridge still needs the compiler above or an independently checked reflection invariant in the historical calculus. Adding `A rejects F` as an axiom changes the proof system/source unless that rule is historically authenticated.

## Finite construction and independent replay

Artifacts:

- producer `experiments/review/lspv5_409_b3_identity_bridge.py`, SHA-256 `ab6108de7105d554fb1cc5f0d6fc36d9fe4741422e23fa6c095debc8c04747cd`;
- independent Node verifier `experiments/review/verify_lspv5_409_b3_identity_bridge.mjs`, SHA-256 `f354839698c809784054da637b268accb32fa9af798d7540595fb02d4ea0f081`;
- raw `results/raw/review/2026-11-07_0455_LSPV5_B3_IDENTITY409.json`, SHA-256 `92e1325d5e71a9154232a7c6ae703c934cf195d8622cc46934bb52c0461e4124`.

The producer generated the exact signed strict-3CNF Tseitin encodings for K4, K3,3 and the cube, both odd and even charge. It checked clause arity/distinctness, parsed the exact DIMACS bytes, exhaustively counted 0/8, 0/16 and 0/32 models for odd/even pairs, and verified that $Q_A$ accepts exactly the odd UNSAT identity certificates. The same locally valid reject-all trace was accepted for every even-charge satisfiable control, giving a concrete trace-only soundness counterexample.

Nine padded odd-K4 controls retained the original UNSAT core while growing the strict proper 3-CNF source. The inherited `[P2-B6]` clock formula was replayed exactly as prior work: identity proof size $N$ versus forced work $2^N+15+1$. Four finite polynomial comparisons were recorded for each padding size. This validates the quantifier distinction only; the symbolic clock theorem remains credited to LSPV-1/462.

Python producer PASS; independent Node replay 143 checks PASS. Eight negative controls rejected source/proof mismatch, SAT identity proof, malformed source, wrong trace digest, truncated trace, unknown program and forged charge behavior while positively witnessing trace-only unsoundness on SAT.

The first implementation policy attempted exhaustive assignment counting after adding up to 24 irrelevant padding variables and exceeded the 30-second run budget. It was replaced by the proved unchanged-UNSAT-core check; this failed policy is charged and recorded. Construction, parsing, truth tables, hashing, big-integer clock arithmetic, serialization and verification were charged in host resources. Host results are not FLMV or historical-checker measurements.

## Tracker effect and remaining gap

Material change: add `[P2-L5-409]` and a `[P2-B2]` evidence line. `proof1.txt` was reviewed with no material change.

The exact missing noncircular premise is now explicit: a rule-specific, original-source-authenticated compiler from $Q_A$ identity certificates (or another polynomially bounded system) into the **same historical** $R_{\mathrm{mix341}}$, with polynomial explicit output and exact native weights. Existential $W$-simulation is B3 itself; rejecting traces, existence of some short-proof system, completeness, and p-optimality analogies do not supply the compiler.

Still OPEN: `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]`, `[P2-B5]`, full mixed superpolynomial $\overline W_R$, historical accepted trace bytes, and P versus NP.

## Publication/readback status

The role artifacts were published and byte-for-byte read back. Immediately before tracker mutation, the complete concurrent `proof2.txt` head was refetched at blob `9b6bc109edbf76c3cd0f713083443d4f4ae5e2fc`; the two-node delta was merged into that complete content, written with its blob precondition, and fully read back exactly at blob `3c9f4ff78db3c04d75294522ec21c6c8036fec83`. `proof1.txt` remained unchanged.

Issue #3 accepted comment ID `6707265694`; an idempotent full-body update by that ID also succeeded. Bulk issue-comment readback failed with `Transport closed`, so no full-thread readback is claimed. The exact comment body is durably preserved at `research/coordination/outbox/2026-11-07_0455_LSPV5_ISSUE3_409_COMMENT.md`.
