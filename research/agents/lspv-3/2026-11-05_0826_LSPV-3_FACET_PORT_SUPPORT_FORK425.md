# LSPV-3/425 | GF(2) gate-port reification and exact support-typing fork

**November 5, 2026, 08:26 PST | PNP Hypergraph & Proof Certificates | task 6ad6f05603248191abb281a5b43b3fc2.**

**Status: PROVED/CONDITIONAL for a specified facet-addressable completion; COMPUTATIONAL finite controls; historical native grammar, complete normalization, B3 and P versus NP OPEN.** No arbitrary-machine hardness claim.

## IDEA before search

Hypothesis H425: a derived high-width GF(2) equation can be reified as a conservative chain of paid two-input XOR-gate definitions with linear additional paid cost, **if** (i) the four clauses of each paid DEF are independently addressable as owner-labelled premises; (ii) AND3 counts the three literal identifiers of a gate condition, including paid auxiliaries, rather than unfolded original-variable source cones; (iii) GF(2) accepts rows with these auxiliaries; (iv) the public output may be referenced. Falsifiers were failure of any of these four exact grammar permissions. None is assumed native merely from /341's prose.

## SEARCH, provenance and relevant findings

Read governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (blob c3889a3e514ddbd747150dcb68607013a3b2d154), the original research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb), AGENTS.md, CODEX.md and research skill, issue #3 through REFEREE364 and LSPV-2/419, and LSPV-3/424. Reviewed actual Grok GROKPROOF/2026-11-05_1218_PROGRESS.md (blob d3183283d6869f92617c0c758c9d31d1a201c32f) and Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67); neither resolves this fixed calculus or B3.

New repositories: konard/p-vs-np README (blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95), scripts/proof_status.json (blob 93b77ed3d8fe456f81c690035f45f07910a247f2), proofs/complexity/README.md: its P-subset-NP verification concerns its finite-machine model, not a native proof compiler. blkph0x/p-vs-np-proof-research README (blob f397a7747eaca82df3d754d0a4b4bab1fe10f814), METHOD_INDEX.md (blob 18d693ea71dfa433370eb7afbebc3106e32f03e5), affine_projection_recognition_lab/AFFINE_HULL_METHOD.md and resolution_width_lab/PHP_WIDTH_REPORT.md (blob f650bfe14e07392e32c6aba0898ae11acd5ecca4): its affine hull can overapproximate the projected relation and its PHP exact-width proof remains ordinary Resolution. Neither establishes B3.

External formats reviewed: meelgroup/frat-xor/format.md (blob 986a21aa92b62f844ef1fce852193142c41b2) explicitly distinguishes clause and XOR IDs; tanyongkiam/cake_lpr/README.md (blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c) describes a source-DIMACS-bound checker's trust chain; peitl/short-proof/README.md (blob 93d2090dba9739bc4983c65ea639a24e1f5e0fab) optimizes ordinary Resolution, not the mixed system. Relevant primary sources: Haken 1985 TCS 39:297–308 (ordinary Resolution PHP only); Raz–Tzameret APAL 155:194–224 (2008, DOI 10.1016/j.apal.2008.04.001, specified Res(linear) fragments); Gocht–Nordström AAAI 2021 DOI 10.1609/aaai.v35i5.16494 (explicit parity proof logging). Indexed web queries targeted these papers and XOR proof formats. Direct Google-branded search was unavailable; container GitHub DNS failed, so authenticated connector reads and standalone local tests were used.

## ITERATE: precise conditional theorem

Define a hypothetical completion $R^+_{\mathrm{facet}}$ with these **extra interpretations, not declared native**: each paid 2-input XOR DEF emits four individually addressable defining-clause facets under its single paid owner; each facet is available as a named AND3 premise; the three-literal gate support, including auxiliary outputs, satisfies AND3's width bound; each exact 3-variable XOR factor may carry a GF(2) annotation including auxiliaries; GF(2) can combine these rows; ownership edges and fresh output checks are obligatory. All paid weights remain one.

**Lemma 425A (PROVED/CONDITIONAL):** Given an already derived, original-source-authenticated row

$$
r:\quad\bigoplus_{i=1}^n x_i=b,\qquad n\ge2,
$$

with distinct original variables, $R^+_{\mathrm{facet}}$ derives a fresh paid gate-output affine unit $z_n=b$ with exactly $5(n-1)$ **additional** paid inferences, and original-source projection is unchanged.

Define $z_2=x_1\oplus x_2$ and $z_k=z_{k-1}\oplus x_k$ for $3\le k\le n$, using $n-1$ conservative paid two-input DEF nodes. For each $z=a\oplus c$, the four facets exclude exactly the four triples $(u,v,1\oplus u\oplus v)$, so three AND3 conjunctions yield the exact factor $a\oplus c\oplus z=0$, with a checked GF(2) annotation. Summing the $n-1$ annotated gate rows uses $n-2$ XOR inferences and gives $\bigoplus_{i=1}^n x_i\oplus z_n=0$. One more GF(2) inference with $r$ gives $z_n=b$. Cost:

$$
(n-1)\mathrm{DEF}+3(n-1)\mathrm{AND3}+(n-1)\mathrm{GF2}=5(n-1).
$$

Topological induction proves unique extension of every original assignment across the DEF DAG; the operation preserves original source bytes, and owner-labelled facets preserve checkable syntactic provenance **under the stipulated augmented rules**.

**Lemma 425B (PROVED/RESTRICTED typing fork):** Each gate condition mentions exactly three literal identifiers $\{a,c,z\}$, but its *original input cone* is $\{x_1,\ldots,x_k\}$ at gate $k$. Thus literal-support <=3 holds for every gate; original-source-cone-support <=3 **first fails at $k=4$**. This is a precise counterexample to treating these two support disciplines as interchangeable. A third notion, essential support of the gate identity after imposing its defining relation, is zero; substituting that semantic tautology for rule provenance is not justified.

This is NOT a legal native counterexample, because /341 does not settle the facet reference, auxiliary row, output export or support-counting conventions. In particular, the result does not assert that all alternative compilers fail under source-cone support.

## Original-source tests, resources and controls

Use strict raw DIMACS with two separately indexed positive unit clauses $(x_i)$ for each $i$. It is SAT with exactly one original-variable model. $n$ paid AND3 steps lift units to $x_i=1$; $n-1$ GF(2) steps build the high-width authenticated row with $b=n\bmod2$. Adding the conditional reifier gives $q=(2n-1)+5(n-1)=7n-6$ paid nodes, an **upper witness**, not a minimum or refutation.

| Original variables $n$ | Paid nodes $q$ | Full explicit JSON bytes | Final gate source-cone width |
|---:|---:|---:|---:|
| 2 | 8 | 946 | 2 |
| 4 | 22 | 2,343 | 4 |
| 8 | 50 | 5,264 | 8 |
| 16 | 106 | 11,397 | 16 |
| 32 | 218 | 25,060 | 32 |
| 64 | 442 | 57,328 | 64 |

A locally executed full JS proof producer/typed checker passed **5,476** assertions/checks across $n=2,3,4,5,6,8,16,32,64$, rejecting eight forged source/facet/owner/row/DAG variants. An independently written Python semantic audit checked **1,048 gate-facet assignments**, **380 explicit small-source assignments**, and four negative facet controls. A separate GitHub-published JS auditor, replayed from connector readback in a V8 isolate, passed **1,740** checks. These are different implementations of a *conditional* grammar, not executions of the authoritative native checker.

With source encoded length $N$, preexisting evidence $E$ and $n$ input literals, explicit sparse evidence of the reifier uses at most $O(n^2(N+\log(n+2)))$ additional bits under canonical decimal IDs, including huge numerical source identifiers. Parsing, source-byte binding, eight-truth-row checks, GF(2) cancellation, output and verification are polynomial in $N+E+n$. Eager full-proof peak space is bounded by stored evidence; streaming/recomputation need their own schedule. The count of paid nodes is not physical runtime. No global proof search or unrestricted SAT lower bound is asserted.

## Next exact missing arrows

Authenticate the historical accepted-byte specification of DEF facets, auxiliary rows, AND3 support, exported gate outputs and LOCAL-CONVERT consumers. Replay this construction in that checker if permitted, or record the **exact** native rejection and repair using already legal steps. Extend or refute full original-source polynomial normalization for every consumer. Separately settle the noncircular same-$R$ B3 implication; neither this conditional proof nor correctness of a SAT decider supplies it. No other specialist manuscript region or root main.tex was edited; all original schedules and weights are unchanged.
