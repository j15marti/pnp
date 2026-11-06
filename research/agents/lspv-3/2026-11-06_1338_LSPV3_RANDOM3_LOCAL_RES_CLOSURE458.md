# LSPV-3/458: first- and second-generation local inference scarcity on an established hard random strict-3-CNF family

**2026-11-06 13:38 PST | Route B, LSPV-3 primary | PROVED/RESTRICTED combinatorial theorem; COMPUTATIONAL reproducibility.** P versus NP OPEN. The original historical R_mix341 grammar and weights, all tasks, five roles and 2 Route A / 3 Route B allocation are unchanged. This report makes **no** superpolynomial lower-bound claim for the full mixed calculus.

## 1. IDEA, four falsifiers, SEARCH, and revision

**Hypothesis:** On the already established random proper strict-3-CNF family at density 8, a cheap original-source-only local-compression pipeline has very few opportunities. In particular, direct native AND3 of *distinct* source clauses should disappear asymptotically and strict native Resolution restricted to clauses of width at most three should stop after its first generation asymptotically almost surely.

Predeclared falsifiers: (F1) pairs of raw source clauses sharing all three variable labels persist with non-vanishing probability; (F2) width-3 direct RES pairs occur linearly rather than a bounded number on average; (F3) second-generation width-at-most-three RES can occur with non-vanishing probability as n grows; (F4) oppositely signed shared literals are accidentally counted as legal strict non-tautological RES.

**Revision after literature and search:** F2 cautions against claiming there are *zero* immediate RES shortcuts: the exact mean tends to 288, not zero. There are many legal shallow shortcuts at moderate sizes. The defensible result is asymptotically **zero second-generation** bounded-width RES with failure probability O(1/n), while a constant expected number of first-generation width-3 RES lines survives. F1, F3 and F4 are rejected by the counting proof under the stated grammar. This is elementary random-hypergraph counting, **not an asserted new published proof-complexity theorem**. It is a precise local shortcut filter, not full mixed hardness.

## 2. Existing source/theorem/encoding/known-method/transfer ledger

**Primary existing hard family.** Let n>=4, m=8n. Independently sample each indexed clause with replacement from the 8*binom(n,3) proper signed width-three clauses on n ambient variable labels, with three *distinct* labels and signs chosen independently and uniformly. Preserve all m original clause indices, including duplicates. The resulting source is already exact strict 3-CNF; no gadget or equisatisfiability-only reduction is used. Decimal DIMACS occupies O(n log(n+2)) encoded bits.

**Published lower bounds.** Chvatal and Szemeredi (JACM 35, 1988, pp. 759-768) established exponential ordinary DAG-Resolution size on an appropriate random 3-CNF model. Pang's arXiv:2610.00837v2 (24 Oct 2026), Theorem 7.2(a), proves for fixed prime p, integer r>=1, fixed width w>=3 and density Delta>=2^w that F~F(n,w,Delta*n) needs exp(Omega_{p,r}(n)) size in DAG Res(PC_r/F_p), asymptotically almost surely. In particular Delta=8,w=3 applies here. The proof model has syntactic algebraic rules and **does not include unrestricted paid fresh DEF or all historical LOCAL-CONVERT**. The theorem is a recent preprint, not described as peer-reviewed or all-algorithm hardness. Earlier project LSPV-3/442, /456 and /457 already studied the source-core bounds, degree/definition exposure and shortcuts for this exact family; those claims are not reintroduced as new.

**Required shortcut controls.** The fixed R_mix341 explicitly contains strict native RES, AND3 on up to three original variables, XOR, LOCAL-CONVERT and paid conservative two-input DEF. The present theorem constrains only native RES when every intermediate clause retains width <=3, and raw-source-to-raw-source AND3. Wide RES intermediates, AND3 self-references, later derived factors, private gates, algebraic elimination, full branching, learned lemmas, reconvergence and extended-Resolution-style Cook shortcuts remain legal candidates at their historical costs. Cubic odd-Tseitin expander sources have four clauses per identical triple and admit linear paid AND3/XOR refutations; thus their behavior is **not** evidence that this random family has the same immediate raw-to-raw shortcut. Haken PHP ordinary Resolution hardness likewise cannot be carried over to a mixed ER-capable calculus.

**Remaining transfer:** Neither Pang's restricted proof-size theorem nor the local scarcity result gives a superpolynomial minimum over *all* historical mixed DAGs. Original-source authentication, native exported/private DEF ports, bit normalization and a noncircular B3 are still OPEN.

## 3. Exact probabilities

Write

$$
C=\binom n3,\qquad m=8n.
$$

Two independently sampled *supports* are identical with probability 1/C. For supports sharing exactly two variables, the probability is 3(n-3)/C. Given exactly two shared labels, strict oriented RES yields one non-tautological width-three resolvent **if and only if** precisely one shared literal has opposite signs and the other has identical signs, probability 1/2.

Define

$$
p=\frac{3(n-3)}{2C}.
$$

This is the probability that two independent source clauses admit a strict non-tautological width-three resolvent. Equal supports can instead yield a width-two resolvent if their signs disagree in precisely one of three coordinates, conditional probability 3/8. The probability of a strict resolvent of width at most three is therefore

$$
q=p+\frac{3}{8C}.
$$

The resulting width-three signed resolvent, conditioned on the p event, is uniform over all signed three-label clauses by permutation and independent sign-flip symmetry.

Let Y count distinct-index raw source pairs with identical supports, and Z the pairs yielding a valid width-three first RES node. Linearity of expectation gives

$$
\mathbb E Y=\frac{\binom m2}{C},
\qquad
\mathbb E Z=\binom m2 p.
$$

Consequently

$$
\mathbb E Y\sim\frac{192}{n},
\qquad
\mathbb E Z\longrightarrow 288.
$$

Thus Markov gives Pr(Y>0)<=EY=O(1/n). On Y=0, no two *distinct* original source clauses can directly enter AND3 within combined support three, and every successful strict width-at-most-three RES between distinct originals has width exactly three.

## 4. Second-generation theorem, including shared branches

**Theorem 458.1 (PROVED/RESTRICTED).** With probability 1-O(1/n), the complete source-authenticated strict Resolution closure of the random formula when **every derived clause is restricted to width at most three** has no clause requiring two or more RES inference steps. Its non-source lines are solely first-generation width-three resolvents of two original source clauses. This is true even for shared DAGs that reuse any prior line. It does not assert that the complete unrestricted Resolution or mixed calculus has no short proof.

To bound every possible second step, introduce these counted events:

- A: two different first-generation width-three resolvents share an original source clause;
- B: one first-generation width-three resolvent and a *third distinct* original source clause admit a valid strict width-at-most-three RES step;
- D: two first-generation width-three resolvents constructed from four distinct sources admit a valid strict width-at-most-three RES step.

Independent sampling, conditioned-uniform first resolvents, and the symmetry calculation above yield the exact expectation bounds for the numbers of indicated patterns:

$$
E_A=m\binom{m-1}{2}p^2.
$$

$$
E_B=\binom m2(m-2)pq.
$$

$$
E_D=3\binom m4 p^2q.
$$

Every one is O(1/n) except E_D=O(1/n^2). The factor 3 in E_D counts the three partitions of four distinct indexed clauses into two unordered source pairs.

A first-generation non-tautological resolvent cannot strictly resolve against one of its own two parent clauses: each surviving literal from either parent has the same sign it had there. Two resolvents obtained from an identical original pair are identical when Y=0, hence cannot strictly resolve against each other. Every remaining second-generation possibility is covered by A, B, or D, even under DAG sharing and arbitrary legal optimal choice. Therefore

$$
\Pr(\mathrm{second\ bounded\ RES\ step})
\le
\mathbb EY+E_A+E_B+E_D
=O(1/n).
$$

This proves Theorem 458.1. No branching/split/weakening/discharge rule has been added. AND3, XOR, LOCAL and DEF are *outside* the second-generation theorem. In particular the proof does not bar source clause self-conjunction into a factor, a width-four RES intermediate later reduced to width three, or cross-representation reuse.

## 5. Independent execution and hostile controls

An original Python 3.13 source producer sampled 12 instances at n=128,512,2048,8192 and seeds 11,23,37. It enumerated every raw-support pair via pair-indexed buckets, checked actual literal polarities and non-tautological strict RES, and enumerated source-to-first and first-to-first second steps. All 12 observed totals agree with the formulas' scales and the expected decline in second-step opportunities; finite outcomes **are not** the asymptotic proof.

| n | seeds | first-generation width-three RES counts | source-pair support duplicates | second first+third counts |
|---:|---|---|---|---|
| 128 | 11,23,37 | 278,272,293 | 1,3,1 | 154,123,162 |
| 512 | 11,23,37 | 308,291,268 | 0,0,1 | 64,56,39 |
| 2048 | 11,23,37 | 288,267,264 | 0,0,0 | 12,7,4 |
| 8192 | 11,23,37 | 284,282,284 | 0,0,0 | 1,2,1 |

A separate, independently written Node.js *naive all-pairs* checker (not using Python's inverted support index) replayed the exact n=128 seed=11 source. It confirmed all eight separately recorded numerical fields, source SHA256 e2910d4d9e421cddab26ce7cdba4d2e9e3a43ea32ee71faf4f5b5e1c7cb0809d, and thirteen checks including deliberate illicit-pivot controls. Python controls additionally rejected four malformed strict-three clauses, checked a SAT instance, an UNSAT instance, and eight deletion SAT witnesses, plus explicit same-support and legal two-step counterexample formulas. These are validation controls, **not candidate new hard families**.

Original combined producer wall time 2.288 s and maximum Linux process RSS 163692 KiB; Node check was separately run successfully. Python full raw SHA256 8beaddeeb17e67d9fca287400c0ae52d4c9b6849455393de48aaa147cdefd870. The smaller GitHub reproducibility script and machine-readable summary reproduce key counts; the conversation ZIP contains the full original Python producer, full 19 KiB raw, independent Node checker, fixed source fixture, report, and SHA256 manifest. These measurements exclude network/GitHub lookup, publication and checker compilation. No authoritative historical R_mix341 accepted-byte parser was run.

## 6. Corpus, search and publication audit

Read the governing November 2 handoff, latest user November 5 allocation, original R_mix341 LSPV-2/341 (blob c87acd11), LSPV-3/448, /449, /453, /456, /457, LSPV-5 REFEREE393 and issue #3 (1107 comments before this update). Actual Grok file GROKPROOF/2026-11-06_1617_PROGRESS.md (blob b931933c), Claude TPORT-0001 (blob b7150bb) reviewed for separate-method critiques. Required external pinned files: konard/p-vs-np scripts/proof_status.json blob 93b77ed3; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea; meelgroup/frat-xor README.md blob 38a137bc; peitl/short-proof README.md blob 93d2090d; openai/math README.md blob cc5b0a0; anthropics/formal-math README.md blob 1df53bf. None is authority for historical native R_mix341 ports. Primary search and open: Pang arXiv HTML v2, especially Theorem 7.2(a) and rule syntax in Section 1; Chvatal-Szemeredi original JACM metadata. Direct branded Google interface was not available; web search worked. No claim of exhaustive literature novelty.

Root main.tex blob a1aecc4f was returned with *zero readable content* for an explicit range request, so there was no safe region-preserving update. The dedicated five-role handoff carries any necessary synthesis. No other role's files or tasks were edited.

**Next exact transfer target:** Can one prove that any mixed paid proof of the published random strict-3 family must spend a quantitatively large paid cost before opening *nonlocal* width-four, algebraic, or paid-DEF shortcuts? The theorem above stops precisely at that representation-changing step and is not a global invariant. B3 and P versus NP remain OPEN.

### References

1. V. Chvatal and E. Szemeredi, "Many hard examples for resolution," J. ACM 35(4), 759-768 (1988), DOI 10.1145/48014.48016.
2. S. Pang, "A Degree-Size Relation for Resolution over Polynomials," arXiv:2610.00837v2, October 24, 2026, Theorems 1.1 and 7.2(a). https://arxiv.org/html/2610.00837v2
3. LSPV-2/341, original R_mix341 declaration, j15marti/pnp research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex.
