# LSPV-5/428 | Distinct-support affine extraction after Resolution

**November 7, 2026, 23:59 PST | Independent red team, Route B primary.**  
**Status:** PROVED/RESTRICTED finite structural lemma + COMPUTATIONAL exact replay. **P versus NP OPEN.**

Affected exact tracker IDs: `[P2-B13]`, `[P2-C3]`, `[P2-D1]`, and new evidence node `[P2-L5-428]`. `[P2-B1]`, `[P2-B2]`, and full historical grammar authentication remain OPEN. No grammar, weight, role, title, schedule, enabled state, allocation, or `main.tex` byte was changed.

## IDEA and falsifiers stated before search

Hypothesis: `[P2-B13]`'s valid four-original-source theorem cannot be promoted to a bounded-ancestry rule saying that pairwise-distinct unsigned source supports prevent affine extraction after ordinary Resolution. Prediction: a constant proper signed 3-CNF with every source support distinct has an exact nonconstant affine projection and admits explicit oriented Resolution derivations of both CNF facets.

Falsifiers were: (F1) exhaustive projection finds a model with $x=y$ or no model with $x\ne y$; (F2) any claimed resolvent has a bad orientation, absent pivot, tautology, missing AND premise, or cross-branch reuse; (F3) the extraction needs a non-native rule or only semantic equality; (F4) the exact support-distinct gadget and restricted floor were already present in trackers or peer artifacts.

## SEARCH: continuity, literature, and repositories

Both complete root trackers were read before work. At head `a402ca92b602e0725e67fe60fa3391410423950a`, `proof1.txt` was blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and `proof2.txt` was blob `ad652f69558e3f87a6fcef02d2f9ba61e11117f7`; both were refetched complete and unchanged at prepublication head `a504d8d15772db18aed178cdaa4982dabb043764`. The historical five-role handoff was read at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, path `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, blob `033b54b87b7cbe94912af5cf67daa52859143a07`. Current `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`, `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, `.codex/skills/pnp-research/SKILL.md` blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`, and issue #3 page 13 through comment `6718833962` were read.

Actual peer files read included LSPV-1/497 `research/agents/lspv-1/2026-11-07_2300_LSPV1_STRICT3_BITPHP_MINIMAL_UNSAT497.md` blob `5a0a809c739afec8d763765290177c0c9c758d5e`; LSPV-2/486 `research/agents/lspv-2/2026-11-07_2321_LSPV2_POSTSTEP_EXPONENT_SLACK486.md` blob `fafa6b73936f696bb3869799547a980db708c508`; LSPV-3/492 final report blob `f968a33b76709501ad2ee29d52f942bd3bf8b64a`; and the newly arriving LSPV-4/488 `research/agents/lspv-4/2026-11-07_2336_LSPV4_MULTIPASS_TSEITIN_SAT_FRONTIER488.md` blob `68db71e082bb0a69e2ddafee7be2d0ff35ede13f`. The latter is a restricted fixed-order sequential multipass SAT bound and does not supply Route B's mixed lower bound. Grok was first read at `GROKPROOF/2026-11-06_2316_PROGRESS.md`, then refetched at the actual latest path `GROKPROOF/2026-11-08_0320_PROGRESS.md`, blob `72edb3140d8ed798d0905a827f85d3428728e396`; Claude's actual world-ledger README/report blobs were `de75a371ce3143a4495e6892df7fb04794a6b708` and `79e4d4e7e0e3edff3aba8610852c45534bdde128`. No guessed path or chat summary was substituted.

Primary-literature queries were `Chvatal Szemeredi many hard examples resolution random 3-CNF JACM 1988 theorem PDF`; `Ben-Sasson Wigderson short proofs are narrow resolution random 3-CNF width lower bound PDF`; `Alekhnovich Razborov lower bounds polynomial calculus random 3-CNF PDF`; and `random 3-CNF resolution affine XOR preprocessing Gaussian elimination proof complexity primary paper`. Direct Google UI was unavailable; the configured primary-web search located the paper/author records. Chvatal--Szemeredi gives exponential ordinary Resolution complexity with high probability for its fixed-density random $k$-CNF model under stated parameter conditions. Ben-Sasson--Wigderson supplies size--width relations for Resolution, not a mixed-calculus theorem. Alekhnovich--Razborov gives degree lower bounds for random $k$-CNFs in specified Polynomial Calculus settings, including characteristic restrictions; it does not cover all R_mix341 rules.

Required repository delta review:

- `konard/p-vs-np` remains pinned at `ecedd2b45f1c524d85c00b2da27a9c140025550c`; README blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` remains educational/model-scoped, not a proof of the converse inclusion.
- `blkph0x/p-vs-np-proof-research` remains pinned at `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` and audit-response blob `f5ed2f0b8d8a018a9f87587c25e29441e055019d` expressly retain finite/family scope.
- `meelgroup/frat-xor` remains at `18cd6bc17af10a9891c10a846ce966166f9fe0dc`; `format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f` is a different proof format with explicit XOR operations and does not authenticate historical R_mix341 conversion bytes.
- `peitl/short-proof` remains at `2c524cfceecf68b56f51d23f6b63255b502856d3`; README blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab` optimizes Resolution/Q-resolution only.
- `MassimoLauria/cnfgen` remains at `24e633bdbed0d0998493bee99c42faf480c7dc96`; `cnfgen/families/randomformulas.py` blob `b00a885122b82dc4d134b95b69d847da53740f05` samples proper width-$k$ clauses without signed-clause repetition. It supplies reproducible instances, not lower-bound certificates.
- `msoos/cryptominisat` remains at `ed61e2170ab8d86a69c7cd99ae09059414fa0e0a`. The attempted root `README.markdown` path returned 404 and was logged. Actual `src/gaussian.cpp` blob `7b9d200c1c1d8e344ce0c3109bfc92806a14359b` and `python/README.md` blob `214382938447c4e4c918f963d1c69751018db766` confirm implemented XOR/Gaussian shortcuts; this is an upper-bound control, not a proof-system lower bound.
- `openai/math` remains at `4eaee87548250b2682affda7d05d947c05554bae`, README blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`; `anthropics/formal-math` remains at `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`, `eth/README.md` blob `0b3dcf4a858ff802b3275fc5999ffb134c74de60`. Neither repository supplies the same-calculus B3 implication.

## ITERATE: exact source, native RES DAG, and proofs

Use variables $x=1,y=2,a=3,b=4,c=5,d=6,e=7,f=8,g=9,h=10,i=11,j=12$. The twelve proper source clauses are

$$
\begin{aligned}
C_1&=(x\lor\neg a\lor b),&C_2&=(x\lor\neg b\lor c),&C_3&=(x\lor\neg c\lor\neg a),\\
C_4&=(y\lor a\lor d),&C_5&=(y\lor\neg d\lor e),&C_6&=(y\lor\neg e\lor a),\\
D_1&=(\neg x\lor\neg f\lor g),&D_2&=(\neg x\lor\neg g\lor h),&D_3&=(\neg x\lor\neg h\lor\neg f),\\
D_4&=(\neg y\lor f\lor i),&D_5&=(\neg y\lor\neg i\lor j),&D_6&=(\neg y\lor\neg j\lor f).
\end{aligned}
$$

All twelve unsigned triples are different. Under $x=y=0$, the $C$ half is the unsatisfiable implication pair $a\to b\to c\to\neg a$ and $\neg a\to d\to e\to a$. If either $x=1$ or $y=1$, one guarded half disappears and the other has a model. The $D$ half is the sign-complemented copy, excluding $x=y=1$. Consequently the exact projection is

$$\exists a\ldots j\;F(x,y,a,ldots,j)\quad\Longleftrightarrow\quad x\oplus y=1.$$

The native ordinary-Resolution DAG has no branch contexts and no extra rule:

$$
\begin{array}{lll}
R_1=\operatorname{Res}_b(C_1,C_2)=(x\lor\neg a\lor c),&&R_2=\operatorname{Res}_c(R_1,C_3)=(x\lor\neg a),\\
R_3=\operatorname{Res}_d(C_4,C_5)=(y\lor a\lor e),&&R_4=\operatorname{Res}_e(R_3,C_6)=(y\lor a),\\
R_5=\operatorname{Res}_a(R_4,R_2)=(x\lor y),&&\\
S_1=\operatorname{Res}_g(D_1,D_2)=(\neg x\lor\neg f\lor h),&&S_2=\operatorname{Res}_h(S_1,D_3)=(\neg x\lor\neg f),\\
S_3=\operatorname{Res}_i(D_4,D_5)=(\neg y\lor f\lor j),&&S_4=\operatorname{Res}_j(S_3,D_6)=(\neg y\lor f),\\
S_5=\operatorname{Res}_f(S_4,S_2)=(\neg x\lor\neg y).&&
\end{array}
$$

Every pivot is oppositely oriented and every resolvent is non-tautological. The union contains ten distinct paid RES nodes; there is no double-counted shared subproof and no omitted AND case. These two derived facets are semantically the row $x\oplus y=1$, but converting that pair to a historical native GF(2) row is **not claimed**: `[P2-D1]` still requires exact LOCAL-CONVERT authentication.

**Restricted six-clause floor.** A proper binary CNF with pairwise-distinct unsigned supports that is UNSAT needs at least six clauses. Any UNSAT formula contains a minimally UNSAT subformula; the standard deficiency lemma gives $m\ge n+1$, so a counterexample with $m\le5$ uses at most four variables. Exhaustive enumeration of every signed clause choice on each simple support for $2\le n\le4$, $m\le5$, checked 11,656 formulas and found zero UNSAT. The six-clause $C$ core at $x=y=0$ witnesses equality. This floor is for simple-support proper 2-CNF cores only; it is not a minimum theorem for every 3-CNF affine gadget or every mixed proof.

Exact Python replay enumerated all $2^{12}=4096$ assignments: projection model counts were $(00,01,10,11)=(0,144,144,0)$. Removing any one of the twelve source clauses admits a forbidden equal-guard assignment, so all twelve sources are individually essential for this affine implication. Three malformed Resolution controls reject. An independent V8 implementation made 4,134 checks, reproduced the projection and trace, checked twelve deletions, and rejected all three corrupt traces.

## Family / theorem / encoding / known-method / remaining-transfer ledger

| Family/control | Exact encoding and size | Theorem/model | Known legal method used | Remaining transfer |
|---|---|---|---|---|
| Chvatal--Szemeredi random proper 3-CNF | $n$ variables, $m=cn$ distinct signed proper ternary clauses, indexed $N=\Theta(n\log n)$ | exponential ordinary shared-DAG Resolution with high probability in the published parameter regime | arbitrary ordinary RES; CNFgen reproduces the sampling model | no invariant covering DEF/LOCAL-CONVERT/GF(2)/branches/shared mixed DAG; `[P2-B1]` OPEN |
| LSPV-5/428 focused control | twelve listed clauses, 12 variables, 177-byte DIMACS | exact XOR projection; ten-node ordinary RES derivation; not a hardness family | oriented RES only | historical conversion of derived facets remains `[P2-D1]` OPEN |
| Cubic odd Tseitin | four strict ternaries per vertex, $4h$ clauses | ordinary Resolution hard on suitable expanders, but accepted mixed affine proofs are linear | AND3 + GF(2) shortcut | excluded as full mixed-hard family by `[P2-L5-427]` |
| Haken PHP | wide pigeon/occupancy clauses; not native 3-CNF | exponential ordinary Resolution | Cook Extended-Resolution shortcut | any 3-CNF transfer needs lower-bound preservation, not equisatisfiability |

Certified satisfiability projection, restricted proof-size hardness, and empirical solver behavior are not conflated.

## Resource ledger

Logical work is exactly ten distinct RES nodes; the source has twelve explicit clauses. The Python artifact is 8,422 bytes, independent V8 artifact 2,861 bytes, DIMACS 177 bytes, primary JSON 5,454 bytes before the final timing-field fluctuation, and independent JSON 318 bytes before timing-field fluctuation. The final Python run used 10,112 KiB maximum resident set before serialization and 0.126 seconds before serialization; the independent V8 run reported 50,909,184 RSS bytes and 0.071 seconds. Python performed 4,096 full projections, twelve deletion searches, 11,656 small-CNF exhaustive tests, ten RES checks, and three corrupt controls. V8 independently performed 4,134 checks.

Construction/search, tracker and peer reads, primary-web queries, repository reads, the failed CryptoMiniSat README path, one rejected first Python trace caused by a deliberately strict orientation check and then corrected by swapping parent order, parsing, hashing, serialization, publication, and readback are charged workflow phases. None is hidden inside ideal $W_R$. The run retains formulae, assignments, source/index data, results, and output simultaneously and makes no FLMV same-machine resource claim.

Final artifact SHA-256 values before publication: Python `77eec3d009696fd0138e33d24fe8098b03e49343c879b784426d0a1b2b82f4bf`; V8 `a5abe653d098a3db7a18ca9d6d2915fff5b561ebe874909bed37ed12be829e15`; DIMACS `e3c9c8c607f1f5fa1e1a2d6a2cbefe3edc10f2744b02ddb5d1e21b43443a2b7b`; primary JSON `8b12305184fa4ff211a6c96d4c6f1628c6b193a01c6003b1e4e9e41d79e17544`; V8 JSON `17ae79439d70714bce809dd84af5798d49901bbcad3c80b8b4b7feab9aa70dea`.

## Revision and status

F1--F3 were not triggered. F4 was partly triggered: `[P2-L5-410]` already proves on a larger split-Tseitin control that source-support uniqueness does not survive arbitrary RES as a hardness invariant. That earlier result is preserved and not rebranded. The new advance is the much smaller exact affine-projection witness plus the sharp six-clause simple-support 2-CNF floor and independent deletion controls.

Revised claim: `[P2-B13]` remains correct at exactly four original source clauses; it cannot be extrapolated into a general support-collision necessity once ordinary RES ancestry grows. The result is a shortcut control and evidence update, not a full-family failure, not a B1/B2 proof, and not B3. Precise remaining gap: an invariant and authenticated checker semantics covering every historical R_mix341 rule on an established hard 3-CNF family, plus an independent noncircular `SAT in P => polynomial Wbar_R` bridge for the same fixed calculus. **P versus NP remains OPEN.**
