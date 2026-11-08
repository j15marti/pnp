# LSPV-5/434 | Context lifting for auxiliary GF(2), with a metric-separation countercontrol

**2026-11-08 05:49 PST | LSPV-5 independent red team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

Material node **[P2-L5-434]** composes **[P2-L1-503]** with the explicit assumption-context and two-branch discharge discipline of **[P2-L5-433]**. It also reconciles **[P2-L3-500]**: direct original variables must enter the support bound for a translation to ordinary canonical CNF, but they need not enter the exponential cone parameter when the target keeps a wide original affine atom native in syntactic $Res(PC_1/\mathbb F_2)$. This is a theorem about a distinct declared calculus. Historical **[P2-D1]**, full mixed transfer **[P2-C3]**, superpolynomial mixed minimum **[P2-B1]**, and noncircular B3 **[P2-B2]** remain OPEN.

## IDEA -> SEARCH -> ITERATE

Initial hypothesis: an auxiliary-bearing GF(2) inference can be compiled under branch contexts only if its support measure includes every directly occurring original variable as well as all original ancestors of extension wires.

Predeclared falsifiers were: substituted GF(2) addition becomes unsound; an auxiliary-only metric undercharges a high-width affine row; parent bundles cannot derive the child bundle in $O((b+1)2^b)$ nodes; or a branch-local conclusion crosses to the opposite branch without discharge.

**Search found a necessary distinction, falsifying part of the initial hypothesis.** LSPV-1/503 translates each extension-bearing row to disjunctions that retain all direct original affine variables in one native equation. Its exponential parameter $b$ therefore need count only complete original ancestors of extension wires in both premises. LSPV-3/500 translates the same kind of predicate all the way to ordinary original clauses, so its support $U_E$ correctly includes both direct originals and wire ancestors. The two metrics answer different target questions and must not be merged.

The revised claim is the common-context lifting theorem below. The /503 and /500 published programs were independently replayed before construction: /503 JS blob `8b98a7bbafe5eb58a6edcd6b46f2b68c13d5dac2` passed 4,096 ordered pairs and 393,216 projection comparisons; /500 JS blob `80cbda28c0d007000615f60f0780626776ff2eca` reproduced the four-node source proof and rejected seven corruptions, while its independent Python blob `03f399524468dfd1890b94f2baf4d56b8d805fba` reproduced the exact branch witnesses. These are proposed-system checks, not historical checker executions.

## SEARCH continuity and source log

Complete root trackers were read at main head `c03a43f98dc041a9250a815d55269681f27c3dc8`: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 bytes; `proof2.txt` blob `cf42e531eff0573aa2d2474e8cfd724061e0e173`, 410,825 bytes. Exact reviewed nodes include [P1-00], [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2], [P2-L1-502], [P2-L1-503], [P2-L3-500], [P2-L5-432], and [P2-L5-433]. During the run main advanced to `f11ad4dae3401fb5e163b7dc0fcaf3b3785576e4`; both trackers were refetched (`proof2.txt` blob `a5a6d7a06f5017398f295f7d9ca784b4ab35a4ce`, 413,469 bytes), and the new **[P2-L3-501]** report/handoff/code/raw were read. /501 proves a factor-island obstruction only for a distinct SOURCE/AND3/XOR fragment and expressly leaves historical RES/DEF/LOCAL interfaces open; it neither duplicates nor contradicts the contextual GF(2) composition here. Current issue #3 metadata was read; bulk comment retrieval failed through the connector, so no claim of full comment-body review is made. Current peer state was recovered from exact main-branch reports and tracker entries.

Read the November 2 governing handoff at historical blob `033b54b87b7cbe94912af5cf67daa52859143a07`, current AGENTS.md, CODEX.md, repository research skill, LSPV-2/341 historical prose blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`, the recovered native-core audit, LSPV-1/503, LSPV-3/500, prior LSPV-5/433, actual Grok progress, and Claude one-tape/portfolio assessments. The recovered /341 checker is authoritative only for its SOURCE/AND3/XOR sublanguage; it has no authenticated context/discharge or new extension-bearing GF(2) trace. It was therefore not relabelled a full historical checker.

Primary literature searches actually issued covered Pang's degree-size theorem and random 3-CNF application, syntactic resolution over linear equations, Ben-Sasson--Wigderson resolution width, and Cook's ER PHP shortcut. Pang arXiv:2610.00837v2 lines 18-38 give the exact syntactic $Res(PC_r/\mathbb F_p)$ rules and DAG node-size measure; Section 7.1 defines $\mathcal F(n,w,\Delta n)$ as independent uniform proper signed width-$w$ clauses with repetitions, and Theorem 7.2(a) gives $\exp(\Omega(n))$ size for fixed $w\ge3,\Delta\ge2^w$. This is preprint-level proof-size hardness in the named system, not arbitrary-machine hardness. Raz--Tzameret and the 2020 $Res(\oplus)$ paper provide rule/model controls; Ben-Sasson--Wigderson remains ordinary Resolution only; Cook ER remains the mandatory PHP shortcut. No Google-branded search client was available.

Required repository delta review: `konard/p-vs-np` head `ecedd2b45f1c524d85c00b2da27a9c140025550c`, proof-status blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research` head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, method index `18d693ea71dfa433370eb7afbebc3106e32f03e5`, audit `b30515cced93d8911a6415555ee9ec1444502d93`. Both remain model-scoped hypothesis/control sources, not P/NP authority. Rotating exact reads included FRAT-XOR format `986a21aa92b62f844ef1fce852193142c41b2b1f`, cake_lpr `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`, CakeML README `8215ddfa23ab8d2254cb475b10689e1d4f92a6ec`, short-proof `93d2090dba9739bc4983c65ea639a24e1f5e0fab`, openai/math `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`, deprecated LeanSAT `afc8a7c67599bd9653c831026571a6b0823ec05f`, and Anthropic ETH README `0b3dcf4a858ff802b3275fc5999ffb134c74de60`, Challenge `6297ab1398884550253bdd1475704729d02ce89b`, Solution `176892178e49792ae41368c13bb4973bae035b29`, comparator `85f16dc55e511335729e668917308b375f0f6036`. The ETH artifact explicitly confines its two `sorry` statements to Challenge and permits `propext`, `Classical.choice`, `Quot.sound`; no independent local build was done, and even its claimed subexponential algorithm would not prove same-calculus B3.

## Theorem 434.1: common-context lift (PROVED/RESTRICTED)

Fix original variables $X$, globally fresh acyclic conservative Boolean definitions $Z$, and the exact syntactic target rules of Pang's $Res(PC_1/\mathbb F_2)$. A source judgement is $\Gamma\vdash E$, where $\Gamma$ is a consistent set of original literals. Definitions are global; no branch-scoped definition may be shared.

For an extension-bearing affine equation $E$, let $S(E)$ be the complete transitive original-ancestor union of its extension variables. The /503 translation $\mathcal T(E)$ enumerates assignments only to $S(E)$ and leaves direct original variables outside $S(E)$ inside one affine atom. For a context, prepend to every translated line the guard

$$
G_\Gamma=\bigvee_{\ell\in\Gamma}\neg\ell.
$$

For every legal same-context extension-bearing GF(2) addition $E_1,E_2\to E_3$, put $V=S(E_1)\cup S(E_2)$ and $b=|V|$. The /503 derivation of $\mathcal T(E_3)$ from the two parent bundles can be lifted line-by-line by adjoining the common disjunct $G_\Gamma$. A target axiom is lifted by one paid weakening. Binary linear combination duplicates the guard, after which paid contraction restores one copy. Weakening, contraction and false-constant deletion remain legal under a common disjunct. When an ancestor variable cancels from extension support but remains as a direct original coefficient, the /503 two-case restoration uses both Boolean values and the target Boolean axiom; the common context guard is carried unchanged. Hence the node overhead remains $O((b+1)2^b)$, up to a fixed constant per target step. Context/reference bits add $O(|\Gamma|)$ per emitted line but do not create $2^{|\Gamma|}$ branches.

For discharge, suppose both $\Gamma\cup\{x\}\vdash E$ and $\Gamma\cup\{\neg x\}\vdash E$ are present. Corresponding target lines have the form

$$
G_\Gamma\vee(x=0)\vee D,
\qquad
G_\Gamma\vee(x=1)\vee D.
$$

Linear combination of the displayed guard equations yields the false constant $0=1$; false deletion and contraction derive $G_\Gamma\vee D$. Thus discharge is an AND hyperedge: both branches are necessary, while an alternative complete proof remains an OR choice. A shared global definition is translated once; any branch-local definition or premise is incompatible with the sibling and cannot be referenced across the join.

Therefore the /503 restricted compiler and /433 context discipline compose. With the prior restricted components, the same size-versus-cone form is retained:

$$
S_{Res(PC_1/\mathbb F_2)}(F)
\le K(n+1)(m+n+q+1)(b+1)2^b,
$$

where $q$ is the union of distinct paid nodes and $b$ charges both GF(2) parents' complete extension-wire ancestor union. This theorem does not supply historical entrance rules, historical split/discharge bytes, or a polynomial bound when $b=\Theta(n)$.

## Metric-separation countercontrol

Let $z=r\oplus x$ be one paid global gate and consider

$$
z\oplus u_1\oplus\cdots\oplus u_{12}=0.
$$

The /503 target needs only four specialized affine lines, one for each assignment to the two ancestors $r,x$; the twelve $u_i$ remain in the affine atom. Both independent programs exhaustively checked all $2^{14}=16{,}384$ original assignments. In contrast, complete ordinary canonical CNF has support 14 and 8,192 falsifying-assignment clauses. Thus the initial proposal to force direct originals into every exponential cone bound is false for the affine target, while /500 is correct to charge them for an ordinary-clause target. Evidence bits still contain all twelve identifiers; they are not free.

## Exact finite source-authenticated control

Use original variables $r,x$ and the four-clause source

$$
(\neg r\vee x)\wedge(\neg r\vee\neg x)\wedge
(r\vee x)\wedge(r\vee\neg x).
$$

It is UNSAT, and deleting any one clause yields a SAT witness. One global gate $z=r\oplus x$ is shared. Under context $r$, two source-authenticated LOCAL nodes derive $z=0$ and $z=1$, and one GF(2) addition derives false. Under context $\neg r$, the symmetric two LOCAL nodes and one addition derive false. A binary discharge consumes both branch contradictions. The trace has eight paid nodes: one shared DEF, four LOCAL, two GF(2) additions and one discharge; maximum extension ancestor cone two. Its canonical serialization is 737 bytes, SHA-256 `893753b9e9876912c850660c5d4a8835c38ad56b1b0a130438a6b50abbbb47e6`.

The compiled original-only target is exactly three correctly oriented Resolution nodes deriving $\neg r$, $r$, then the empty clause. Independent Python and JavaScript implementations agree on all semantic counts and reject the same eight mutations: missing branch, cross-branch reuse, branch-scoped definition, wrong GF(2) RHS, wrong LOCAL row, missing source parent, wrong discharge pivot and source-sign mutation. Python also rejects five malformed source strings. This easy 2-CNF is a focused scope/control witness, not a hard family and not an accepted historical packet.

## Established family / theorem / shortcut / remaining-transfer ledger

| Family | Exact source | Published theorem/model | Known legal shortcut/control | Remaining transfer |
|---|---|---|---|---|
| Pang random proper 3-CNF | $\mathcal F(n,3,8n)$: $8n$ independent draws from $8\binom n3$, repeats allowed; indexed $N=\Theta(n\log n)$ | Pang Theorem 7.2(a), preprint: $e^{\Omega(n)}$ shared-DAG syntactic $Res(PC_r/\mathbb F_p)$ size | Full target syntax/sharing allowed; no extension variables in the theorem | Authenticate every historical rule; broad-cone short proofs remain possible |
| Expander odd Tseitin | Four proper 3-clauses per cubic vertex; $N=\Theta(h\log h)$ | Ben-Sasson--Wigderson/Urquhart ordinary Resolution only | Historical SOURCE/AND3/GF(2) core has a $4h-1$ proof | Retired as full mixed-hard witness when core retained |
| PHP | Preserve each published encoding; no new 3-CNF preservation claim | Haken ordinary Resolution lower bound | Cook ER and modern DRAT polynomial auxiliary proofs | Equisatisfiability alone does not transfer hardness |

## Work, span, evidence and machine boundary

Logical work counts the union of distinct paid nodes once. Both discharge branches are included; the global definition is shared once. Ideal span is one plus the maximum branch span, not their sum. Actual generation pays source/index reads, context and gate ancestry propagation, $2^b$ case construction, direct affine identifier reads, target-rule emission, failed attempts, references, serialization, verification, output and readback. A materialized translator has output-scale peak space; streaming trades retention for recomputation and retrieval. The executed Python control reported 47,625,505 ns and 9,728 KiB maximum RSS, but host measurements establish no FLMV exponent. Proof selection remains free only in the mathematical minimum.

## Publication and exact remaining gap

Artifacts: this report; `experiments/review/lspv5_434_context_auxxor_redteam.py`; `experiments/review/verify_lspv5_434_context_auxxor.mjs`; `results/raw/review/2026-11-08_0549_LSPV5_434_CONTEXT_AUXXOR_RAW.json`; `research/coordination/2026-11-08_0549_LSPV5_CONTEXT_AUXXOR_HANDOFF434.md`.

**Actual advance:** the /503 extension-bearing GF(2) compiler survives explicit contexts, AND discharge and shared global definitions, while a 12-direct-variable control proves that /503's affine cone metric and /500's ordinary-clause support metric must remain distinct. **Verification:** peer replay, symbolic target-rule proof, two independent finite implementations, exact trace hash and hostile controls. **Precise remaining gap:** authenticate original historical extension-bearing GF(2), LOCAL/DEF facets and split/discharge bytes; then prove a complete all-rule normalization without a linear-cone escape and prove noncircular same-system B3. P versus NP remains OPEN.

## Primary sources

1. Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, Sections 1 and 7, https://arxiv.org/html/2610.00837v2.
2. Ran Raz and Iddo Tzameret, *Resolution over Linear Equations and Multilinear Proofs*, APAL 155(3), 2008, ECCC TR07-078.
3. Eli Ben-Sasson and Avi Wigderson, *Short Proofs Are Narrow—Resolution Made Simple*, JACM 48(2), 2001.
4. Stephen Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4), 1976.
