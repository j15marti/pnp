# REFEREE378: strict-3 bit-PHP decoder, exact work/span audit, and the FACET-A firewall

**November 5, 2026, 21:53 PST. LSPV-5 Independent Proof Red Team, Route B.**

**Status. PROVED/EXACT, RESTRICTED to the separately declared FACET-A grammar:** the LSPV-3/439 bit-PHP-to-unary-PHP prefix compiler lifts to a proper strict-3-CNF source with exact paid distinct-node work

$$
W_{\mathrm{pre}}=
M(4\ell-3)+(n+1)(2n\ell-9),
\qquad
n=2^\ell,\quad M=n\binom{n+1}{2},
$$

and exact critical-path span

$$
\operatorname{span}_{\mathrm{pre}}=\max\{n-1,\,4\ell-3\}.
$$

The work includes every Resolution node needed to reconstruct each original width-$2\ell$ bit-PHP clause from its strict-3 chain. **COMPUTATIONAL:** independently generated FACET-A trace bytes for $\ell=2,3$ were accepted by a separately authored checker with 27,858 assertions and seven hostile rejections. **OPEN:** this is not an authoritative historical $R_{\mathrm{mix341}}$ trace, it stops at the unary-PHP premises rather than the empty clause, the published Res($\oplus$) lower bound has no strict-3 lower-bound transfer, and B3 remains open. P versus NP remains **OPEN**.

## IDEA -> SEARCH -> ITERATE

### Initial hypothesis and falsifiers

The initial hypothesis was that the proposed “wide GF(2) row or exponentially many branch contexts” dichotomy remained incomplete because a linear chain of paid binary extension gates could summarize boundary parity. Falsifiers were:

1. historical DEF cannot express XOR or expose facets usable by Resolution;
2. original-source component clauses cannot derive the summary without an already-wide GF(2) row;
3. every extension encoding necessarily expands to exponential evidence;
4. current LSPV-1/3 work already contains and correctly scopes this extension escape.

Search found falsifier 4: LSPV-3/439 already constructs a stronger shared binary-extension decoder for Braun's bit pigeonhole formulas. The parity-summary proposal was therefore dropped as duplicated.

### Revised target

The revised target was an independent, falsifiable cost audit of /439: regenerate its declared FACET-A proof from **proper strict-3 source bytes**, verify every oriented Resolution step and owner-qualified facet, and determine exact union work and longest dependency path. Revised falsifiers were:

1. standard clause splitting does not reconstruct each original width-$2\ell$ clause in exactly $2\ell-3$ paid Resolution nodes;
2. /439's $D+R$ count omits a required definition, prefix implication, at-least-one expansion, or collision step;
3. the explicit DAG has greater span than the claimed formula because apparently parallel prefix work is actually sequential;
4. extension outputs are not globally fresh relative to the strict-3 source variable bound.

All four were rejected in the declared FACET-A model after fixing the producer's DIMACS header to end at the **source** maximum variable rather than the later DEF outputs. That correction is scientifically material: a header including future DEF outputs would destroy the intended freshness claim.

## Search, continuity, and exact sources

Read the governing five-role handoff at historical commit 4e29ed7646f484707767acb6e63ec5f38afd98a8; current issue #3 through LSPV-4/430; LSPV-1/434; LSPV-3/438 and /439 report, code, raw and handoff; historical /341; REFEREE377; actual research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex; and actual research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex.

Primary sources inspected:

- Kamil Braun, *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv:2609.23015, revised October 22, 2026, Theorem 1.1. For $\ell\ge32$, $n=2^\ell$, every unrestricted DAG-like Res($\oplus$) refutation has more than $\exp(n/(32768\ell^2))$ lines. The model permits arbitrary affine pivots and semantic weakening, but **not extension axioms**.
- Stephen Cook, *A short proof of the pigeon hole principle using extended resolution*, SIGACT News 8(4), 1976. This is the mandatory ER shortcut control.
- Buss, *Quasipolynomial Size Proofs of the Propositional Pigeonhole Principle*, TCS 576 (2015), which recalls the Cook--Reckhow polynomial extended-Frege PHP proof and distinguishes Frege from extension reasoning.
- Urquhart, *Hard Examples for Resolution*, JACM 34 (1987): exponential ordinary-Resolution lower bounds for expander Tseitin clauses, with a width-three variant, not mixed-calculus or all-machine hardness.

Indexed queries included “Braun exponential lower bound bit pigeonhole principle resolution over parities arXiv 2609.23015 Theorem 1.1”, “Cook Reckhow extended resolution polynomial pigeonhole principle proof primary paper”, “Buss polynomial size proofs propositional pigeonhole principle extended Frege primary”, and “Urquhart hard examples resolution strict three literal clauses Tseitin expander”. Direct Google-branded access was unavailable; indexed search was used.

Change-aware GitHub heads and relevant files:

- konard/p-vs-np ecedd2b45f1c524d85c00b2da27a9c140025550c, proofs/experiments/np_subset_p_proof_attempt.md: explicitly leaves polynomial SAT-machine time open.
- blkph0x/p-vs-np-proof-research 7dedc73f758dfbdc072e7aa29dfc08505761ebd5, PROOF_PORTFOLIO_BRIDGE_REPORT.md: bounded proof-DAG relation projection, no universal interface theorem.
- meelgroup/frat-xor 18cd6bc17af10a9891c10a846ce966166f9fe0dc, format.md: typed clause/XOR identifiers for XLRUP, not historical /341 selectors.
- tanyongkiam/cake_lpr 033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2, README.md: verified LPR checking and explicit heap/stack limits, not an extension-proof producer.
- peitl/short-proof 2c524cfceecf68b56f51d23f6b63255b502856d3, README.md: exact bounded shortest ordinary-Resolution search, not an all-rule minimum.
- openai/math 4eaee87548250b2682affda7d05d947c05554bae, lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean: same-execution cost accounting, not B3 or a mixed proof-system transfer.
- anthropics/formal-math 16a5ce41304fcdaea4e0be7c132e1c361dc26da5, eth/README.md, eth/MainResults.lean, eth/Solution.lean, and eth/proof/PaperIndex.lean: claims a formally checked $2^{o(n)}$ 3-SAT/#3-SAT algorithm and ETH failure in its stated Mathlib machine model. The inspected theorem is subexponential, not polynomial, and supplies no same-$R_{\mathrm{mix341}}$ proof-size implication. This run did not build or independently kernel-check that large development and does not rely on it.

Repository text and passing checkers are evidence about declared artifacts, not proof of P versus NP.

## Established-family ledger

| Family | Exact encoding and size | Published theorem/model | Strong shortcut control | Missing transfer |
| --- | --- | --- | --- | --- |
| Cubic-expander odd Tseitin | One edge variable; four proper signed width-three blockers per cubic vertex. $3h/2$ variables, $4h$ clauses, $N=\Theta(h\log h)$ indexed bits. | Urquhart/Ben-Sasson--Wigderson: $2^{\Omega(h)}$ ordinary unrestricted shared-DAG Resolution length on suitable expanders. | Historical semantic AND3/GF(2) proof has exact $4h-1$ nodes. | Ordinary Resolution hardness does not survive the legal mixed shortcut. |
| Braun bit-PHP | $m=n+1$, $n=2^\ell$ holes; $m\ell$ bit variables; $M=n\binom m2$ clauses of width $2\ell$. | Braun Theorem 1.1: $>\exp(n/(32768\ell^2))$ lines for DAG-like Res($\oplus$), $\ell\ge32$, no extension axioms. | Shared prefix definitions decode unary PHP premises; Cook-style extension proof is a polynomial upper-bound control in an extension calculus. | Source is not 3-CNF. No lower-bound-preserving strict-3 or historical-/341 transfer. |
| Haken/Cook unary PHP | Standard at-least-one clauses have width $n$; binary collision clauses. | Exponential ordinary Resolution; polynomial ER/extended-Frege proofs. | Cook's extension construction is the mandatory countercontrol. | Equisatisfiable strict-3 splitting alone proves no lower-bound direction. |

Certified UNSAT, a lower bound in a named proof system, and empirical solver difficulty remain distinct.

## Exact source and declared FACET-A grammar

For pigeon $i\in[m]$, bit position $t\in[\ell]$, and hole address $a\in\{0,1\}^{\ell}$, let $[b_{it}\ne a_t]$ be the mismatch literal. The original Braun clause for $i<j$ and $a$ is

$$
C_{ij,a}=\bigvee_{t=1}^{\ell}[b_{it}\ne a_t]\ \vee\
\bigvee_{t=1}^{\ell}[b_{jt}\ne a_t].
$$

There are $M=n\binom{n+1}{2}$ such clauses. Each has $2\ell$ pairwise distinct literals.

Replace every width-$2\ell$ clause $(l_1\vee\cdots\vee l_{2\ell})$ by its private strict-3 chain

$$
(l_1\vee l_2\vee z_1),\
(\neg z_1\vee l_3\vee z_2),\ldots,\
(\neg z_{2\ell-3}\vee l_{2\ell-1}\vee l_{2\ell}).
$$

This uses $2\ell-2$ proper strict-three clauses and $2\ell-3$ fresh source variables per original clause. Sequential Resolution reconstructs the original clause in exactly $2\ell-3$ paid nodes. Thus

$$
V_{\mathrm{src}}=(n+1)\ell+M(2\ell-3),\qquad
C_{\mathrm{src}}=M(2\ell-2),\qquad
Q=M(2\ell-3).
$$

The separate FACET-A378-v1 grammar permits:

1. free authenticated strict-3 source clauses;
2. one unit-paid globally fresh signed-AND2 owner $z=A\land B$, with individually addressable owner-qualified facets $(\neg z\vee A)$, $(\neg z\vee B)$, and $(z\vee\neg A\vee\neg B)$;
3. one unit-paid correctly oriented binary Resolution node;
4. no free split, weakening, semantic oracle, or tailored answer axiom.

This is a precise proposed completion, not authenticated historical syntax.

## Reconstructed prefix decoder and exact work

For each pigeon and every prefix $p$ of length $d\ge2$, introduce

$$
y_{i,p}=y_{i,p^-}\land[b_{id}=p_d].
$$

Length-one prefixes are signed source-bit literals. The paid definition count is

$$
D=(n+1)\sum_{d=2}^{\ell}2^d=(n+1)(2n-4).
$$

For every prefix gate derive $\neg y_{i,p}\vee[b_{it}=p_t]$. Immediate inputs use owner facets; inherited bits use one Resolution through the parent. The paid inherited-implication count is

$$
I=(n+1)\sum_{d=3}^{\ell}2^d(d-1)
=(n+1)\,2n(\ell-2).
$$

For each pigeon, child third facets yield parent bridges. Two length-one bridges resolve on the first bit; each deeper frontier prefix costs one bridge and one expansion. The exact at-least-one count is

$$
A=(n+1)(2n-5).
$$

Finally, resolve each reconstructed $C_{ij,a}$ against its $2\ell$ authenticated leaf implications to obtain $\neg y_{i,a}\vee\neg y_{j,a}$, costing

$$
B=2\ell M.
$$

Consequently /439's wide-source compiler has exact work

$$
D+I+A+B=2\ell M+(n+1)(2n\ell-9),
$$

matching 195 and 2079 nodes at $\ell=2,3$. The strict-3 lift adds $Q$, giving

$$
\boxed{
W_{\mathrm{pre}}=Q+D+I+A+B
=M(4\ell-3)+(n+1)(2n\ell-9).
}
$$

This counts the union of distinct DAG nodes once. It excludes free sources, optimizer discovery, and any later unary-PHP refutation.

## Exact critical-path span

Give sources depth zero, a definition one plus its parent-owner depth, and Resolution one plus the maximum antecedent depth. Independent pigeons, addresses, pairs, prefix gates, and source chains run in parallel.

- A strict-3 chain reconstructs its wide clause at depth $2\ell-3$.
- Leaf implications have depth at most $\ell$.
- Cancelling $2\ell$ mismatch literals puts each collision output at depth $4\ell-3$.
- The two length-one bridges and root have depth three. Sequential frontier expansion performs $n-4$ dependent replacements, putting each at-least-one output at depth $n-1$.

Hence

$$
\boxed{\operatorname{span}_{\mathrm{pre}}=\max\{n-1,4\ell-3\}.}
$$

Thus $W_{\mathrm{pre}}=\Theta(n^3\ell)$ while span is $\Theta(n)$. This is not a small-space theorem. A materialized verifier may retain all clauses and owners; streaming/recomputation must separately charge lookup, output, cache misses, and peak state.

## Strict-3 direction and proof status

The chain proves only the **upper-bound lifting direction**:

$$
\text{a FACET-A/ER proof from the wide source}
\Longrightarrow
\text{a polynomial FACET-A proof from the strict-3 source}.
$$

It does not prove that a short proof of the strict-3 source back-translates to Res($\oplus$). The chain variables are new resources, and Braun explicitly excludes extension axioms. Therefore the published lower bound is not transferred.

The emitted traces stop after producing all unary PHP axioms. Cook's polynomial ER/extended-Frege PHP proof is a literature upper-bound control, but this run did not emit its complete suffix in FACET-A bytes. No complete empty-clause certificate or historical mixed upper bound is claimed.

## Reproducibility and adversarial controls

The producer emitted complete compact-JSON traces for $\ell=2,3$, including exact DIMACS, strict-3 sources, fresh definitions, owner facets, every source reconstruction, every prefix implication, and all unary outputs.

| $\ell$ | strict-3 clauses | source vars / final vars | source RES | DEF | other RES | total work | span | serialized trace bytes |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 80 | 50 / 70 | 40 | 20 | 175 | 235 | 5 | 31,707 |
| 3 | 1,152 | 891 / 999 | 864 | 108 | 1,971 | 2,943 | 9 | 424,165 |

Independent Node replay checked source headers/hashes, unique IDs, freshness beyond the source bound, facets, ownership, oriented pivots, exact resolvents, non-tautology, output clauses, union work, and longest paths. It executed **27,858 assertions** and rejected seven mutations: wrong pivot, nonfresh DEF, corrupt facet, duplicate ID, omitted at-least-one obligation, bad source hash, and malformed DIMACS header.

SAT controls used $n$ pigeons in $n$ holes at $\ell=2,3,4$ with the explicit distinct-address assignment. The UNSAT bit-PHP theorem is pigeonhole counting; these finite traces certify only the compiler prefix.

Physical observations from the first corrected run: 0.273 host seconds and 2,432,158 Python tracemalloc peak bytes. Timing and allocator observations are excluded from the persisted certificate. Two consecutive post-fix producer/replay runs yielded an identical 456,531-byte raw file and identical verifier summary. Artifact SHA-256 values:

- producer c60e580534df10a60b0de28ebcaeb9def0912cab39102fd23255a9b581cd911c;
- independent verifier 59a25236e535b08a8f045e8975c86d75619abf626306316a42f3cceba0e3e7d1;
- raw traces 6ad7d7f5d51105975903971d46985818ffe2bbb702fc252d617305f3981f7412.

The JSON stores every resolvent. A compact certificate could omit result clauses and recompute them; that changes evidence bits and verifier time, not logical work.

## Final status and precise remaining gap

- **PROVED/EXACT, RESTRICTED FACET-A:** exact strict-3 pre-PHP work $M(4\ell-3)+(n+1)(2n\ell-9)$ and span $\max\{n-1,4\ell-3\}$.
- **COMPUTATIONAL:** two complete declared-grammar traces, 27,858 assertions, seven hostile rejections, and both-label controls.
- **CORRECTED DURING AUDIT:** DIMACS source headers now stop before later DEF outputs, preserving genuine global freshness.
- **NOT PROVED:** Braun's lower bound for the strict-3 transform; historical /341 acceptance; a complete FACET-A empty-clause proof; superpolynomial full-mixed work; B1/B2/B3.
- **OPEN:** authenticate historical owner/facet/export bytes and then either replay this decoder plus a fully paid Cook suffix in the same fixed calculus, or exhibit a legal rejection. For lower bounds, find an invariant surviving extension, GF(2), Resolution, LOCAL, sharing, and optimal proof choice. P versus NP remains OPEN.

The immediate red-team demand on LSPV-3/439 is precise: its polynomial upper-bound idea survives the strict-3 source charge, but only in FACET-A and only through the unary premises. Historical facet selection and the complete paid ER suffix remain the two unclosed links.
