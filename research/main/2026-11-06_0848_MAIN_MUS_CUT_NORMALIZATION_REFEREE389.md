# LSPV-5/REFEREE389: minimally-unsatisfiable cut normalization closes the interleaved pure-Resolution floor

**November 6, 2026, 08:48 PST | Route B independent red team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

This report preserves the fixed historical $R_{\mathrm{mix341}}$ rules and weights. It adds no split, discharge, weakening, or case rule. The main theorem is about the strict pure-Resolution subgrammar. Its bridge application excludes every pure-Resolution 35-node tree, including interleaved trees; it does **not** exclude a 35-node mixed AND3/XOR/RES tree, any 36-node class, or prove an asymptotic mixed lower bound or B3.

## 1. IDEA -> SEARCH -> ITERATE

**Initial hypothesis.** For a split formula $L(X,b)\wedge R(Y,b)$ with $X\cap Y=\varnothing$, both sides satisfiable, and $b$ the only shared variable, every strict source-once Resolution refutation can be normalized into an $L\vdash b$ tree, an $R\vdash\neg b$ tree, and one final RES.

Falsifiers were: (i) an interleaved mixed-private clause that cannot be commuted without source copying; (ii) a small split CNF with a global read-once refutation but no full-source side-unit derivation; (iii) interpolation preserving only semantics, not clause-once structure; or (iv) failure of the authenticated bridge split assumptions.

**Search outcome.** Feasible/Craig interpolation gives a formula over the shared variables but does not supply the claimed source-once unit proofs. Iwama--Miyano establishes the incompleteness and NP-completeness of read-once Resolution, not this normalization. Falsifier (ii) succeeds with five 2-CNF sources when no minimality hypothesis is imposed.

**Revised claim.** The 36-clause bridge core is minimally unsatisfiable (MUS), and MUS is exactly the missing repair. The theorem below proves the normalization under this hypothesis. Together with REFEREE388's exact side closures, it excludes the remaining interleaved pure-Resolution 35-node class.

## 2. A minimal counterexample to the unrestricted claim

Let the only shared variable be $b$, with private variables $x$ and $y$:

$$
L=(b\lor\neg x)\wedge(b\lor x),
$$

$$
R=(\neg y)\wedge(\neg b)\wedge(\neg b\lor y).
$$

$L$ is satisfiable and forces $b$; $R$ is satisfiable and forces $\neg b$. All five sources occur once in the strict interleaved refutation

$$
(b\lor\neg x), (\neg b\lor y)\vdash(\neg x\lor y),
$$

$$
(\neg x\lor y),(b\lor x)\vdash(b\lor y),
$$

$$
(b\lor y),(\neg b)\vdash y,
\qquad y,(\neg y)\vdash\bot.
$$

But the three right sources have no strict full-source Resolution-tree outcome at all, hence no full-source derivation of $\neg b$. The formula is not MUS: deletion model counts in source order are $(1,1,0,0,0)$. This is a legal focused counterexample to the unrestricted structural statement, not a candidate hard family.

## 3. MUS one-cut normalization theorem

### Theorem 389.1 (PROVED/RESTRICTED)

Let $L$ and $R$ be finite CNFs with

$$
\operatorname{Var}(L)\subseteq X\cup\{b\},\qquad
\operatorname{Var}(R)\subseteq Y\cup\{b\},\qquad X\cap Y=\varnothing.
$$

Assume $L$ and $R$ are satisfiable and $F=L\cup R$ is minimally unsatisfiable. In strict oriented binary Resolution, $F$ has a source-once refutation if and only if, after possibly exchanging signs, there are source-once derivations using every local source exactly once

$$
L\vdash b,qquad R\vdash\neg b,
$$

followed by one final RES. No weakening, source copying, split, discharge, or semantic oracle is used.

### Proof

Because private assignments combine, the nonempty sets of bridge values realized by $L$ and $R$ are disjoint. Hence, after exchanging signs, $L\models b$ and $R\models\neg b$.

**Polarity forced by minimality.** No clause of $L$ contains $\neg b$. If $C\in L$ contained $\neg b$, then at $b=0$ it would be satisfied automatically. Since $L\models b$, $(L\setminus\{C\})|_{b=0}$ would remain unsatisfiable. At $b=1$, $R$ is unsatisfiable. Thus $F\setminus\{C\}$ would still be unsatisfiable, contradicting minimality. Symmetrically, no clause of $R$ contains $b$.

Moreover, $L|_{b=0}$ is minimally unsatisfiable. It is unsatisfiable because $L\models b$. For each $C\in L$, a model of $F\setminus\{C\}$ exists by minimality; it must have $b=0$ because it satisfies $R$, and therefore witnesses satisfiability of $(L\setminus\{C\})|_{b=0}$. The symmetric statement holds for $R|_{b=1}$.

Now take a strict source-once refutation tree $T$ of $F$, and choose a model of $R$, necessarily with $b=0$. Restrict $T$ by that bridge value and the model's $Y$-assignment. Every $R$ source becomes true. Normalize the restricted tree bottom-up: a true node is virtual; a surviving source keeps its restricted clause; at a RES node, strictly resolve the two surviving representatives when their pivot remains, and otherwise retain the stronger surviving representative. Removing literals cannot create a second complementary pivot. The result is a strict source-once refutation from a subset of the sources of $L|_{b=0}$.

Since $L|_{b=0}$ is minimally unsatisfiable, no source can be omitted. Thus the normalized tree uses every restricted $L$ source exactly once. Lift its leaves back to the original $L$ clauses and replay the same private-variable pivots. Every lifted clause is either its restricted clause $C$ or $C\lor b$; there is no $\neg b$ anywhere, so every pivot remains unique and legal. At least one source contains $b$, since a satisfiable formula independent of $b$ cannot force $b$. Therefore the lifted root is the unit $b$. This gives the required full-source $L\vdash b$ tree. The proof for $R\vdash\neg b$ is symmetric. The converse is the displayed final resolution. $\square$

The MUS hypothesis is load-bearing, as the five-source counterexample proves. Craig interpolation alone would not establish the source-once conclusion.

## 4. Application to the authenticated bridge source

The established bridge source has 15 variables and 40 strict width-three clauses, raw DIMACS SHA-256 `4f8a7e613ace4f67cd0b62204cdda2a4d8072047bd55a70da23da282e3537b18`. Its unique essential 36-clause core is indexed by

`0..15,17,18,20..36,39`.

The left 18 sources are `0..15,17,18`; the right 18 are `20..36,39`. Independent exhaustive checks give:

- the 36-clause core has zero models;
- every one-clause deletion is satisfiable, with 16 or 32 models;
- the two variable sets intersect exactly in variable 15;
- each side has 1,024 models;
- the left forces $x_{15}$ and contains no $\neg x_{15}$;
- the right forces $\neg x_{15}$ and contains no $x_{15}$.

REFEREE386 proved that 35 paid binary nodes at the ancestry floor require a 36-source full binary source-once tree. REFEREE388 then exhaustively proved that neither full-source side-unit tree exists. Per side it checked 1,126,097,195 clause pairs, found 154,950,040 legal pre-dedup resolvents, and ended with 1,888 full-source outcomes, excluding the target unit. A separate base-3 implementation with a 43,046,721-entry strict-resolution table reproduced the result.

Theorem 389.1 now removes the earlier qualification "canonical side join": any interleaved global pure-Resolution source-once tree would normalize to exactly the two impossible side-unit trees. Therefore

$$
W_{\mathrm{RES}}(F_{\mathrm{bridge}})\ge 36
$$

under the project's paid-node convention. This is a restricted finite lower bound. The full historical mixed interval remains

$$
35\le W_{R_{\mathrm{mix341}}}(F_{\mathrm{bridge}})\le37.
$$

A 35-node AND3/XOR/RES tree may still exist. The theorem does not constrain the three 36-node topology classes.

## 5. Established-family and shortcut ledger

| Family | Exact encoding / parameter | Established theorem and model | Known legal shortcut/control | Remaining transfer |
|---|---|---|---|---|
| Cubic odd Tseitin | One edge variable; four signed width-three forbidden-parity clauses per cubic vertex; $3h/2$ variables, $4h$ clauses, $\Theta(h\log h)$ indexed bits | Urquhart and Ben-Sasson--Wigderson: exponential ordinary shared-DAG Resolution size for suitable expanders | Historical AND3 derives each vertex row and GF(2) XOR combines rows in $4h-1$ paid nodes | Ordinary Resolution hardness does not survive the fixed mixed rules |
| Classical PHP | Standard pigeon/hole CNF, not native strict 3-CNF | Haken: exponential ordinary Resolution | Cook Extended Resolution has polynomial proofs | No authenticated lower-bound-preserving strict-3-CNF reduction into all of $R_{\mathrm{mix341}}$ |
| Braun bit-PHP | $n=2^\ell$; source clauses have width $2\ell$ | Exponential unrestricted DAG Res(XOR) lower bound under the paper's separated low-degree criterion | Conservative extensions remain an external mandatory control | Width-to-3-CNF backtranslation and historical DEF/LOCAL simulation remain OPEN |
| Finite bridge control | 15 variables; 40 strict 3-clauses; 36-clause MUS core | This run: pure-RES 35-node class impossible | Existing 37-node proof uses 28 AND3, 6 XOR, 2 LOCAL, 1 RES | Mixed 35 and all 36 classes remain OPEN |

Certified UNSAT, restricted proof-size hardness, and empirical solver difficulty are distinct. This report proves a finite restricted proof-size statement only for the bridge control.

## 6. Independent computation and hostile controls

The producer exhaustively rechecked all $2^{15}$ assignments for the bridge core and each of its 36 deletions. It found zero core models; each deletion had 16 or 32. It rechecked the two 1,024-model sides, exact cut variable, forced bridge signs, and absence of wrong-polarity bridge literals. It authenticated the prior REFEREE388 raw and independent-verification records by exact SHA-256.

An independently written Node verifier rebuilt the five-source proof, enforced exactly one complementary pivot and non-tautological resolvents, checked all five source IDs once, recomputed both side closures, confirmed nonminimality, and separately re-enumerated the bridge core/deletions/sides. It passed 119 grouped assertions and rejected five hostile proof-tree mutations: forged root, out-of-range source, corrupted internal clause, missing premise, and duplicated source.

Additional non-load-bearing finite searches found no MUS counterexample among all 77 minimally $b$-entailing width-at-most-three clause sets over two private variables, and none among 36 paired weakenings of a known six-clause minimal-unsatisfiable non-ROR formula. These finite absences are controls only; Theorem 389.1 rests on the symbolic proof.

## 7. Resource and provenance ledger

| Phase | Charged result |
|---|---|
| Five-source search | 220 semantic side pairs before the first counterexample; 0.133 s, 8,960 KiB RSS |
| Small MUS search | 26 candidate clauses, 77 minimal-entailment sets; 5.265 s, 9,728 KiB RSS |
| Non-ROR MUS gadget control | 36 global pairs; 2.188 s, 10,496 KiB RSS |
| Bridge premise producer | Core/deletion/side enumeration, parsing and hashes; 4.564 s, 10,752 KiB RSS |
| Independent verifier | 119 checks and five mutation rejects; 0.070 s, 50,360 KiB RSS |
| Reused exact closure | REFEREE388 producer 16.975 s / 34,608 KiB; independent verifier 29.571 s / 118,528 KiB; imported by exact hashes, not rerun here |
| Evidence bits | Four new raw JSON records, master summary, verification record, source code, report, handoff, outbox |
| Search and reads | Current head/issue, governing handoff, original grammar/addendum, peers LSPV-1/451 and LSPV-3/453, Grok and Claude files, primary literature, required repository deltas |
| Publication | Git-object creation, root merge, issue comment and full readback are separately charged after this report |
| Simultaneous peak | 50,360 KiB in this run's executed checks; 118,528 KiB including reused REFEREE388 execution; connector memory is unmeasured |

No logical minimum includes discovery cost. The implemented upper/checking work includes enumeration, failed hypotheses, parsing, hashing, serialization, verification and output. No native FLMV time/space inference is made.

Artifact SHA-256 values before publication:

- master result: `07f451e8c58fd2c4c91a853400fce0afcbf6a69c4887c5bee6b298c93e9b847f`;
- independent verification: `26148ed013553751c06eda3c06141bf930f82518216c5cd16a3dd9784c36bf82`;
- producer: `43d83f3a168c37e5b03f428db0a907f1975dedba74a33e26641dd1a14cdb0bcd`;
- independent verifier: `e471c6c62df2e0d733b8bcc442ac95919e085c1ab945122276c3807418c14d91`.

## 8. Search/repository log and limitations

Read current issue #3 through LSPV-3/453; governing five-role handoff; AGENTS.md, CODEX.md and the repository skill; original `/341` rules and LOCAL addendum; REFEREE386--388; LSPV-1/451; LSPV-3/453; LSPV-4/442; actual `GROKPROOF/2026-11-06_1617_PROGRESS.md`; and actual Claude TPORT-0002 and ONETAPE-0001. LSPV-3/453's native-Resolution treewidth serialization is a useful upper-bound control but not B3, while LSPV-4/442's expander/UP result is explicitly restricted Route-A evidence and retains the algebraic-shortcut objection. The scratch workspace is a partial artifact checkout: the mandated local preflight ran but reported missing root `main.tex`, AGENTS.md, CODEX.md and skill from its inferred local repository root. Their complete current GitHub bytes were read separately; the preflight limitation is not disguised as success.

Required repository heads were change-checked: `konard/p-vs-np` `ecedd2b45...`, `blkph0x/p-vs-np-proof-research` `7dedc73f...`, `meelgroup/frat-xor` `18cd6bc1...`, `tanyongkiam/cake_lpr` `033aad53...`, and `peitl/short-proof` `2c524cfc...` were unchanged. `openai/math` was at `4eaee875...`; `ExecCNFNodeSearchCosts.lean` remained blob `1ced21f4...` and models a different concrete SAT execution, not a proof compiler. FRAT-XOR has explicit clause/XOR provenance in a different format; CakeLPR verifies LPR; short-proof optimizes ordinary Resolution. None authenticates the historical mixed grammar or proves B3. The two requested P-vs-NP repositories contain hypotheses/status artifacts, not this normalization theorem or a P-vs-NP solution.

Primary indexed search covered Iwama--Miyano read-once Resolution, Craig/feasible interpolation, Urquhart, Ben-Sasson--Wigderson, and Haken. Direct Google-branded search was unavailable. No authoritative historical accepted-byte checker was located or executed.

## 9. B3 verdict, advance, and precise remaining gap

Theorem 389.1 is a proof-structure theorem inside pure Resolution. It neither constructs $R_{\mathrm{mix341}}$ proofs from arbitrary SAT decider traces nor formalizes correctness/reflection for arbitrary deciders. LSPV-1/451's NP-hard minimum-XOR optimization also does not imply superpolynomial minimum size. B1, B2 and B3 remain OPEN.

**Actual advance:** every pure-Resolution 35-node bridge refutation is excluded, including arbitrary interleaving across the one-variable cut. The unrestricted normalization conjecture was simultaneously falsified by a minimal five-source non-MUS counterexample and repaired with an exact load-bearing MUS hypothesis.

**Precise remaining gap:** construct or exclude a legal 35-node mixed AND3/XOR/RES tree, then analyze the three 36-node topology classes under the exact historical grammar. Separately, transfer an established asymptotic lower bound through every legal mixed shortcut and prove a noncircular same-system B3 bridge. P versus NP remains **OPEN**.

## Artifacts

- `experiments/review/lspv5_389_split_ror_counterexample.py`
- `experiments/review/lspv5_389_split_ror_mus_search.py`
- `experiments/review/lspv5_389_mus_gadget_search.py`
- `experiments/review/lspv5_389_bridge_mus_normalization.py`
- `experiments/review/lspv5_389_independent_verify.mjs`
- `results/raw/review/2026-11-06_0848_LSPV5_SPLIT_ROR_COUNTEREXAMPLE389.json`
- `results/raw/review/2026-11-06_0848_LSPV5_SPLIT_ROR_MUS389_s5.json`
- `results/raw/review/2026-11-06_0848_LSPV5_SPLIT_ROR_MUS389_w3_s6.json`
- `results/raw/review/2026-11-06_0848_LSPV5_SPLIT_ROR_MUS_GADGET389.json`
- `results/raw/review/2026-11-06_0848_LSPV5_BRIDGE_MUS_NORMALIZATION389.json`
- `results/raw/review/2026-11-06_0848_LSPV5_BRIDGE_MUS_NORMALIZATION389_verification.json`
- `research/coordination/2026-11-06_0848_LSPV5_MUS_CUT_NORMALIZATION389_HANDOFF.md`
- `research/agents/lspv-5/outbox/2026-11-06_0848_LSPV5_ROOT_INSERT389.tex`
