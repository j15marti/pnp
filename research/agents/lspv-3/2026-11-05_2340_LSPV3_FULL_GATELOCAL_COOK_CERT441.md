# LSPV-3/441: Complete strict-3 bit-PHP Cook refutation compiled to declared GATE-LOCAL

**2026-11-05 23:40 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL. Historical R_mix341 native grammar, all-rule normalization, B3, and P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE

**Hypothesis.** If a unit-paid two-input conservative DEF owner can itself be used as a three-wire exact LOCAL-CONVERT antecedent, the **complete** LSPV-5/REFEREE379 source-authenticated FACET-A bit-pigeonhole refutation can be compiled into paid GATE-LOCAL without changing any Resolution step, source identity, dependency, or empty conclusion.

**Falsifiers:** an invalid three-variable facet implication; incorrect Resolution orientation or missing AND premise; an unowned/private wire or lost source ancestor; duplicate paid facet or unexpected span explosion. A fifth *unresolved* falsifier is that the historical native checker rejects DEF owners as LOCAL input. The first four were tested and rejected within the stated declared grammar, **not** under an authenticated historical checker.

The starting point is existing, not newly generated hardness: Braun bit-PHP (arXiv:2609.23015, updated 2026-10-22) has an exponential lower bound for unrestricted DAG-like Res($\oplus$) for $\ell\ge32$, with **no extension axioms**. Its $n=2^\ell$, $m=n+1$ source has $M=n\binom{m}{2}$ collision clauses of width $2\ell$. Each private chain has $2\ell-2$ proper strict-3 clauses, giving $S=M(2\ell-2)$ strict-3 sources and $V=m\ell+M(2\ell-3)$ variables. Reconstructing the original collision clauses by $2\ell-3$ Resolution steps is an upper simulation, NOT a Res($\oplus$) lower-bound transfer.

**The new independent advance is proofwise composition with the complete LSPV-5/379 Cook suffix**, not rediscovery of /440's gate-local facet lemma or Cook's ER proof. The known odd-cubic Tseitin /341 mixed GF(2) proof and Cook/Buss PHP proofs remain mandatory shortcut controls.

## Formal theorem, declared grammar only

Take the *complete* source-authenticated FACET-A/379 shared proof DAG with $D$ globally fresh nondegenerate signed two-input AND definitions and $R$ correctly oriented binary RES nodes. Replace each owner facet of $z=a\land b$,

$$
(\neg z\lor a),\quad (\neg z\lor b),\quad (z\lor\neg a\lor\neg b),
$$

by one fresh **unit-paid** LOCAL from the exact owner relation. Each is checked by all eight assignments to the three underlying variables. Acyclic owner dependencies, all original source edges and all subsequent Resolution pivots are preserved; a repeated facet reference points to the same paid LOCAL, not a duplicate derivation. This proof has no branch assumptions, splitting or discharge. For the actual /379 trace all three facets of every owner are needed in the final backward slice, yielding exact *exhibited* cost $R+4D$, **not a proven global minimum**.

For $n=2^\ell$, $m=n+1$, and $M=n\binom{m}{2}$,

$$
D=m(2n-4)+\frac{2(n-1)n(n+1)}3,
$$

$$
W_{FA}^{\rm exhib}=M(4\ell-3)+m(2n\ell-9)+\frac{n(n+1)(27n^2+11n-14)}{24},
$$

$$
\boxed{W_{GL}^{\rm exhib}=W_{FA}^{\rm exhib}+3D
=W_{FA}^{\rm exhib}+2(n+1)(n^2+2n-6)=O(n^4).}
$$

**Span lemma:** In this typed architecture, DEF may depend only on earlier DEF owners, never on a Resolution result, and LOCAL facets are consumed by RES. Any source-to-root dependency path thus acquires **at most one** added LOCAL layer. It follows that $\mathrm{span}_{FA}\le\mathrm{span}_{GL}\le\mathrm{span}_{FA}+1$ for unit-latency unlimited-processor span. This does NOT extend to an arbitrary historical mixed DAG.

## Actual independent full-trace verification

Read upstream **full raw peer certificate**, not just its prose summary: `results/raw/review/2026-11-05_2253_LSPV5_FULL_COOK_FACETA379.json`, blob `cbf6b243d3697cc775801ac26a052b0622d3e9ef`, 741,690 bytes. An independent JS/V8 validator reconstructed every DEF facet, verified gate implication on eight assignments, replayed **every correctly oriented Resolution step**, and walked backwards from the exact empty-clause root to verify all original sources and charged nodes. No added node was double-counted.

| $\ell$ | Strict-3 sources | Old FACET-A paid | DEF | Paid LOCAL added | New GATE-LOCAL paid | Span old -> new | Backward-slice vertices | Independent checks |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 80 | 620 | 60 | 180 | **800** | 19 -> **20** | 880 | 2,921 |
| 3 | 1,152 | 8,349 | 444 | 1,332 | **9,681** | 53 -> **54** | 10,833 | 33,604 |

All three facets per owner are reachable. Source hashes reported by the upstream trace: `13361aa6164d76373ac8d4b4b6935f05257bb99266441f3405cfeecb653da6a6` and `27f97b3a3c906b2858769ad9e9d691dfd95002852c5f99febf01e21f11c3bd9d`.

An **independent local executable compiler** (complete source in the separately retained reproducibility archive) also built and replayed a genuine ten-clause proper strict-3 UNSAT control: one DEF, three paid LOCAL, thirteen paid RES, **17 total paid nodes**, all ten original clauses in the final ancestry and all three DEF facets used. It rejected **8/8 hostile file modifications**: source hash, pivot sign, degenerate or nonfresh DEF, illegal facet index, omitted AND premise, duplicate node ID and false last step. The local compiler was run on that control; it was **not run on the full peer raw file**, which was read and checked inside the connected GitHub environment. Do not conflate the two test executions.

## Resource and source authenticity ledger

The logical minimum excludes discovery cost by design. An implemented translation instead must pay full acquisition/index/head read, JSON parsing, source and defining-owner authentication, construction of each LOCAL, 8-row checks, all RES references and byte serialization, output/hash and verification, caches, recomputation and all-phase simultaneous peak. The original trace is 741,690 bytes, not zero-space metadata. A materialized compiler has $O(B_{in}+B_{out})$ simultaneous state before host-runtime overhead. Unit logical nodes do not make identifier, SHA, port checking, or affine-mask bit manipulation free. The standalone ten-clause test emitted 2,292 bytes in 0.00384 host seconds at observed RSS 28,033,024 bytes (Linux, Node 22.16.0); these are neither formal asymptotics nor FLMV same-machine bounds.

Reviewed governing five-role handoff, issue #3, /341 original calculus (blob `c87acd11`), /440 (blob `1e4340bc`), /379 report (blob `9f9792c2`), and actual Grok REWIRE (blob `d06a2d56`) and Claude ONETAPE (blob `9a5b05d6`) files. External review included `konard/p-vs-np/proofs/experiments/np_subset_p_proof_attempt.md` (`f07e4821`), `blkph0x/p-vs-np-proof-research/PROOF_PORTFOLIO_BRIDGE_REPORT.md` (`22215cec`), `meelgroup/frat-xor/format.md` (`986a21aa`), `tanyongkiam/cake_lpr/README.md` (`e94f45e9`, final release 2026-11-01), `peitl/short-proof/README.md` (`93d2090d`) and OpenAI math's `ExecCNFNodeSearchCosts.lean`. These prove neither the historical owner-selector syntax nor B3. Indexed web and connected GitHub search were used; direct Google-branded search and local raw GitHub network download were unavailable.

**Remaining:** an authoritative historical byte grammar for paid DEF owner/LOCAL input, facet selectors, private/exported ports, plus proofwise normalization for arbitrary AND3/GF(2)/branching shared DAGs and noncircular same-R B3. The result is an **upper-bound shortcut** conditional on declared GATE-LOCAL; it neither transfers Braun's Res($\oplus$) lower bound nor proves superpolynomial $\overline W_{R_{mix341}}$ or P vs NP.

**References:** Braun (2026), arXiv:2609.23015; Cook (1976), SIGACT News 8(4), DOI 10.1145/1008335.1008338; Buss (1987), JSL 52:916-927.