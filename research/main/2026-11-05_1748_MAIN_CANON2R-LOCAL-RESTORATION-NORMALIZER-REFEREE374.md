<!-- LSPV-5 REPORT::REFEREE374::2026-11-05T17:48:00-08:00 -->
# LSPV-5 REFEREE374: frozen CANON2R admits a linear whole-proof signed-AND normalization

**November 5, 2026, 17:48 PST. Route B primary.** **PROVED/EXACT for the proposed frozen CANON2/CANON2R completion:** every accepted proof with arbitrary binary `DEF` tags has a same-raw-source accepted proof using only signed-AND `DEF` tags and at most eleven times as many paid nodes. **COMPUTATIONAL:** the new translation interfaces passed 1,363 exact CANON2R wrapper certificates; the LSPV-3/435 eleven-node shared-LOCAL trace is accepted as actual CANON2R bytes. **OPEN:** the historical `/341` serialization is not uniquely specified by the printed semantic rules; no superpolynomial lower bound for the complete mixed calculus and no noncircular B3 bridge is proved. P versus NP remains OPEN.

No historical rule, weight, schedule, task, role allocation, or proof-system hardness claim is changed. The theorem is checker-relative and does not silently promote CANON2R to historical authority.

## IDEA -> SEARCH -> ITERATE

### Initial hypothesis and falsifiers

Before search, the proposed repair was:

> Whenever a translated clause is a proper subclause of the old clause immediately before an exact `AND3` or `LOCAL` consumer, one paid `LOCAL` implication restores the exact old clause. Thus REFEREE372's DEF-facet subclauses may suffice for a polynomial whole-proof normalization, despite REFEREE373's failure of verbatim replay.

Four falsifiers were fixed:

1. an old exact consumer has support larger than three or contains an auxiliary at the restoration boundary;
2. a proper subclause does not imply the old clause under the checker's actual truth convention;
3. a lost affine port cannot be re-exported after restoration;
4. repeated DEF inputs, tautological facets, shared reconvergence, or branch-local assumptions break the constant expansion.

### Search changed the claim

Current issue #3 showed that LSPV-3/435 had already independently proposed the two-paid-node semantic repair, so this run does not claim that idea as new. LSPV-3/435 explicitly left two tasks open: actual CANON2R byte acceptance and a polynomial global translation. Those became this run's precise targets.

The search also exposed a real missing case in the first formulation: REFEREE372 exhaustively serialized distinct DEF inputs, but the checker permits repeated inputs and tautological defining facets. The experiment was expanded to all 16 truth tags and all four ordered input patterns `(1,1),(1,2),(2,1),(2,2)`. This evidence changed the final theorem from a distinct-input statement to the full binary-DEF grammar accepted by the frozen checker.

## Exact frozen grammar used

The authoritative executable object for this theorem is the already published proposed completion:

- `experiments/arc/lspv5_361/rmix341_canon2_repair_referee361.py`;
- `experiments/arc/lspv5_362/rmix341_raw_affine_firewall_referee362.py`.

Its relevant rules are:

- `RES`: an explicitly oriented strict resolvent of two referenced clause views;
- `AND3`: the exact conjunction of two clause/factor views whose combined support contains at most three original variables; an affine annotation is accepted only when all rows agree exactly;
- `LOCAL`: a one-parent implication to a clause or factor, verified on all rows of a combined support of at most three original variables;
- `GF2`: exact XOR addition of two affine views;
- `DEF`: one globally fresh sequential output, two earlier input IDs, one four-bit truth tag, and four owner-qualified defining facets;
- CANON2R: exact external raw DIMACS bytes, canonical base64, raw SHA-256, and equality of parsed source with the embedded source.

The checker contains no case-split, discharge, weakening, context, private-wire, or selector record. Extra context payloads are rejected. This theorem adds none.

## Lemma 374.1: exact bounded restoration

Let $D\subseteq C$ be canonical clauses over at most three original variables. Then $D\Rightarrow C$, including empty and tautological cases, so one native `LOCAL` node restores the exact view $C$ from a reference to $D$.

More generally, if factor relation $G$ is a subrelation of a factor $F$ and their combined original support has size at most three, `LOCAL(G,F)` is legal. If $F$ is affine, one self-`AND3(F,F)` re-exports its exact affine annotation. These are paid nodes, not free weakening or an equivalence oracle.

**Proof.** Clause truth is monotone under literal-set inclusion. Factor inclusion is exactly the rowwise implication checked by `LOCAL`. Self-conjunction preserves every row of $F$, after which the checker independently compares the proposed affine row on all assignments. QED.

The actual checker accepted all 729 pairs $D\subseteq C$ over the six signed literals on three variables, including complementary literal pairs. It also accepted all 634 pairs $G\subseteq F$ where $F$ ranges over every affine relation on every subset of three original variables and $G$ ranges over every subrelation of $F$.

## Lemma 374.2: Resolution survives strengthening

Suppose an old oriented inference resolves $C_1\ni x$ and $C_2\ni\neg x$ to

$$C=(C_1\setminus\{x\})\cup(C_2\setminus\{\neg x\}).$$

Let translated clause references denote $D_i\subseteq C_i$.

- If $x\in D_1$ and $\neg x\in D_2$, their oriented resolvent is a subclause of $C$.
- If $x\notin D_1$, reuse $D_1$, since $D_1\subseteq C_1\setminus\{x\}\subseteq C$.
- Otherwise $\neg x\notin D_2$, and reuse $D_2$.

Thus an old Resolution node needs at most one translated `RES` node and never needs unlicensed weakening. Tautological parents do not invalidate the set inclusion argument. The finite control exhaustively checked 236,196 parent/representative combinations over three variables; the proof above is symbolic and has no width restriction.

## Theorem 374.3: whole-proof signed-AND normalization

Let $\pi$ be any accepted frozen CANON2R refutation of an externally fixed raw source. Let

$$q=d+r+a+\ell+g$$

be its paid-node count, partitioned into arbitrary binary `DEF`, `RES`, `AND3`, `LOCAL`, and `GF2` nodes. There is an effectively constructible CANON2R refutation $N(\pi)$ of the **identical raw source bytes** such that:

1. every `DEF` truth tag in $N(\pi)$ is a signed two-input AND tag;
2. all references remain owner-qualified, globally fresh, acyclic, and source-authenticated;
3. every old clause view is represented by a subclause after the global auxiliary renaming, while every old factor and affine view used at a mixed boundary is represented exactly;
4. the paid-node bound is

$$|N(\pi)|\le 11d+r+3a+2\ell+g\le 11q.$$

The output evidence has polynomial bit length and the translator runs in polynomial time in the explicit input proof length.

### Proof

Process old nodes in topological order and maintain a global map from old auxiliary IDs to the final outputs of their replacement networks.

**Source clauses.** Preserve the original CANON2R raw bytes, parsed source, and clause IDs exactly. Source clause views are exact.

**DEF.** REFEREE372 gives, for each of the 16 four-bit tags, a replacement with at most three signed-AND definitions and a strict-Resolution subclause representative for each of four old facets, with at most two Resolution ancestors per facet. This run additionally serializes every ordered equality pattern of the two inputs. All 64 old/replacement gate pairs and all 256 facets are accepted; 200 representatives are exact and 56 are proper subclauses. Alpha-renaming covers arbitrary earlier input IDs and nested definitions. The union bound is at most $3+4\cdot2=11$ paid nodes per old owner. A compiled owner is emitted once and shared by all reconvergent references.

**RES.** Apply Lemma 374.2, emitting at most one new Resolution node or reusing one pivot-free representative.

**AND3.** The old inference's legality implies that the union of its parent supports has at most three original variables. A factor parent is exact by induction. For each clause parent represented by $D\subseteq C$, emit one paid `LOCAL(D,C)`. The restoration is legal because $C$ itself contains only the original variables admitted by the old `AND3`. Replay the old `AND3` with its exact factor and, when present, exact affine annotation. This costs at most three nodes.

**LOCAL.** Factor and affine parents are exact by induction. If the parent is a clause representative $D\subseteq C$, first restore $C$ with one paid `LOCAL`; the old node's own support check already guarantees legality. Then replay the old `LOCAL` exactly. This costs at most two nodes and produces an exact output view.

**GF2.** Both affine parents are exact, so replay the same XOR sum in one node.

**Final view.** If the old final view is an empty clause, its representative is a subclause of the empty clause and is therefore empty. Final affine/factor contradictions are exact by induction. Thus the translated document is a refutation.

All templates and facet witnesses are finite constant lookup data. A single scan maintains the variable/reference map and emits $O(q)$ records. IDs and references take $O(\log(N+q))$ bits, and raw-source copy/hash verification is polynomial in the original source length. This proves effective polynomial translation for the frozen completion. QED.

## Actual accepted shared-DAG port repair

LSPV-3/435's padded source has eight original proper 3-clauses on six variables. The accepted trace uses:

| Rule | Count |
|---|---:|
| RES | 5 |
| AND3 | 3 |
| LOCAL | 2 |
| GF2 | 1 |
| Total | 11 |

The first shared factor is $u\land v$. Two separate paid LOCAL outputs restore $(u\lor v)$ and $(u\lor\neg v)$. The following exact AND3 nodes export respectively $u\oplus v=1$ and $u\oplus v=0$, and one GF2 node gives $0=1$. The frozen CANON2R wrapper accepted 11 distinct paid nodes, span 6, 21 references, 28 checked truth rows, 1,634 CANON2 bytes, 1,950 wrapper bytes, and the exact raw-source hash `efb4b5540b448b019b8360b86c6fb6173dd8e5fade92f07eaa7ad1e6f73658ae`.

This independently confirms LSPV-3/435's semantic repair at the proposed byte level. It is not a new optimum: the same padded source already has an exact seven-node Resolution refutation.

## Hostile controls and branching/shared-DAG audit

The actual checker rejected:

- the reversed invalid factor implication;
- a false affine RHS;
- an auxiliary-containing LOCAL boundary;
- an extra branch-context payload;
- a forged raw hash;
- a malformed clause count;
- an alleged refutation of a SAT same-sign source.

CANON2R has no native split/discharge rule. Therefore Theorem 374.3 is a theorem about its existing acyclic inference DAG, not about a silently extended branching calculus. If an external calculus later adds contexts $\Gamma\vdash C$, the translation may be applied inside a fixed context, but a lemma can be shared only when every assumption in its ancestry is available. Both children of an UNSAT split remain AND obligations; this report does not discharge either branch or leak a local conclusion across incompatible contexts.

Distinct logical nodes are charged once under the frozen weights. Critical-path span and a realizable storage/recomputation schedule are separate. The ideal minimum grants free best-proof selection; the implemented translator still pays parsing, template lookup, maps, source reads, hashing, output construction, certificate verification, and storage.

## Established-family and missing-transfer ledger

| Family/control | Exact encoding and size | Published/model-qualified result | Strong legal shortcut | Remaining transfer |
|---|---|---|---|---|
| Cubic-expander odd Tseitin 3-CNF | One variable per edge. Each degree-3 parity row is encoded by its four width-3 blocking clauses. For $h$ vertices: $3h/2$ variables, $4h$ proper 3-clauses, binary length $\Theta(h\log(h+2))$. | Urquhart (JACM 1987) and the Ben-Sasson--Wigderson width method give $2^{\Omega(h)}$ ordinary shared-DAG Resolution size on suitable bounded-degree expanders. This is proof-system hardness, not machine hardness. | Historical semantic $R_{mix341}$ has the source-authenticated AND3/GF(2) proof of exact minimum $4h-1$ on connected bridgeless cubic odd sources (LSPV-2/341). | **Family failure for full mixed hardness.** Resolution hardness does not transfer through a system containing the affine shortcut. |
| Sparse graph PHP / perfect matching | Graph PHP uses pigeon clauses on graph neighborhoods plus binary collision clauses; the exact source width depends on the chosen degree. | de Rezende--Nordstrom--Risse--Sokolov, CCC 2020, prove exponential ordinary Resolution length for specified sparse-expander formulas. | ER/Frege extension reasoning is a mandatory upper-bound control. | If the source is not already exact 3-CNF, equisatisfiability is insufficient; a lower-bound-preserving 3-CNF simulation direction and encoded-size overhead are required. No transfer to full CANON2R is proved. |
| Unary PHP | Standard wide pigeon clauses and binary collision clauses. | Haken (TCS 1985) proves exponential ordinary DAG Resolution length. | Cook's Extended Resolution has polynomial PHP proofs; shared extension variables defeat a Resolution-only inference. | Not a 3-CNF family as stated. No full mixed-system lower bound or all-algorithm SAT lower bound follows. |

The first family is the primary exact 3-CNF control for this run. Its known affine shortcut is evidence about the true mixed minimum and is included, not excluded.

## B3 audit

The required bridge remains

$$\mathrm{SAT}\in\mathrm P\Longrightarrow\exists C,k\ \forall N:\quad
\overline W_{R_{mix341}}(N)\le C(N+1)^k.$$

Theorem 374.3 is a **proof-to-proof** simulation internal to frozen CANON2R. It does not construct a CANON2R proof from a rejecting trace of an arbitrary polynomial SAT decider. Under `SAT in P`, the standard Cook--Reckhow argument yields some polynomially bounded proof system whose verifier can use the decider, but identifying that system with the preselected CANON2R requires a polynomial simulation or feasible correctness/reflection proof. That is precisely the missing arrow; assuming it would be circular. Completeness of Resolution, checker acceptance, and the existence of a finite normalizer do not fill it.

Thus B1, B2, B3, a superpolynomial full-mixed $\overline W$, and P versus NP all remain OPEN.

## SEARCH record and source limitations

Project materials actually read:

- historical five-role handoff at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`;
- current issue #3 through LSPV-4/426 and LSPV-3/435;
- `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11...`;
- REFEREE371--373 reports, checkers, raw data, and accepted certificates;
- `research/agents/lspv-3/2026-11-05_1731_LSPV3_NATIVE_LOCAL_PORT_REPAIR435_GITHUB.md`, blob `c02acb2...`;
- `GROKPROOF/2026-11-05_1913_PROGRESS.md`, blob `8a004bf4...`;
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727...`.

Grok reports no B1/B2/B3 closure and treats FRAT-XOR as certificate infrastructure only. Claude's TPORT theorem concerns a restricted alternation-trading portfolio model and supplies no CANON2R reflection theorem.

Actual indexed-web queries included:

- `graph pigeonhole principle resolution lower bound 3-CNF de Rezende Nordstrom Risse Sokolov CCC 2020`;
- `Cook Reckhow 1979 relative efficiency propositional proof systems polynomially bounded P NP`;
- `Haken intractability of resolution pigeonhole principle 1985`;
- `Res XOR Tseitin lower bounds proof complexity`.

Primary documents read included de Rezende et al., CCC 2020, DOI `10.4230/LIPIcs.CCC.2020.28`, and Cook--Reckhow, JSL 1979. Current Res($\oplus$) sources found only restricted depth/regular/tree-like lower bounds, not a full mixed-CANON2R lower bound. Direct Google-branded interactive search was unavailable; indexed web search was used and is not represented as direct Google execution.

Change-aware repository review:

| Repository | Head checked | Finding |
|---|---:|---|
| `konard/p-vs-np` | `ecedd2b45f1c...` | No change from prior pin and no CANON2R normalizer/B3 theorem found. |
| `blkph0x/p-vs-np-proof-research` | `7dedc73f758d...` | Residual-equivalence reports explicitly remain scoped barriers; no same-system proof compiler. |
| `meelgroup/frat-xor` | `18cd6bc17af1...` | Explicit clause/XOR IDs and binary XLRUP semantics; useful checker control, not historical `/341` authority. |
| `tanyongkiam/cake_lpr` | `033aad53d173...` | Proof-checker engineering, not a minimum-proof/B3 transfer. |
| `openai/math` | `4eaee8754825...` | `ExecCNFNodeSearchCosts.lean` charges a particular search program; it does not formalize arbitrary-decider correctness or CANON2R simulation. |

No-result searches are limitations, not novelty claims.

## Corpus reconciliation

**CORPUS REVIEWED.** Governing handoff, issue #3, historical `/341`, REFEREE371--373, peer /435, relevant LSPV-1/3/4 issue updates, actual Grok/Claude, frozen checker sources, cited raw/certificate artifacts, primary proof-complexity papers, and required external repositories.

**DUPLICATION / CONTRADICTION AUDIT.** The semantic LOCAL repair is prior LSPV-3/435 and is not rebranded. REFEREE373's claim that verbatim strengthening is invalid remains correct; this theorem pays explicit restoration nodes. No contradiction exists. REFEREE372's distinct-input evidence was incomplete for repeated inputs; the new 64-gate audit repairs that finite coverage gap.

**WHAT CHANGED RELATIVE TO ROOT MAIN.** The frozen CANON2R whole-proof normalization arrow may be marked proved with linear factor 11, but historical grammar authentication and B3 remain open. Authenticated root `main.tex` fetch returned zero readable characters at blob `593000bbe5b09df6b93fb7453da2ebdf73aeff6b`; an overwrite would violate the safe-readback rule, so root reconciliation is explicitly pending rather than claimed.

**ADOPTED / REJECTED / RETIRED.** Adopted REFEREE372's finite signed-AND compilation and LSPV-3/435's paid LOCAL repair. Rejected verbatim mixed replay, free weakening, auxiliary LOCAL ports, cross-branch reuse, and any inference from internal normalization to B3. No established theorem was retired.

## Reproducibility and physical ledger

Artifacts:

- `experiments/arc/lspv5_374/canon2r_local_restoration_normalizer_referee374.py`;
- `experiments/arc/lspv5_374/verify_canon2r_local_restoration_referee374.mjs`;
- `results/raw/arc/2026-11-05_1748_LSPV5_REFEREE374_raw.json`;
- `results/raw/arc/2026-11-05_1748_LSPV5_REFEREE374_certificates.json`;
- `results/raw/arc/2026-11-05_1748_LSPV5_REFEREE374_independent.json`;
- four chunk files for ordered DEF input patterns.

The distinct-input chunks took 14.76 s and 14.83 s; repeated-input chunks took 0.52 s and 0.50 s. The final producer pass took 0.26 s with sampled peak RSS 13,176 KiB. The independent no-import Node verifier passed 5,905 assertions with sampled RSS about 45.5 MB. These are host measurements, not logical weights or native Turing-machine bounds.

Charged phases include construction, exhaustive enumeration, strict parsing, source hashing, serialization, checker replay, independent verification, and output. Any implemented general translator additionally pays proof input reads, owner/reference maps, renamed-ID encoding, output writing, lookup storage, verification, and all-phase peak space. Logical XOR tracing was not used.

```text
63873d601a8081e92f17ec643fba98abc0399314d3fd7049b71aa52b3f04f269  Python producer
f3e32a94781b594bf2413b9bd01ac168fc7518b4585e2912bde79b58cacecc77  Node verifier
42c1bc04e0ddfa6da392262f7596b7202ac1ff289e413367cc403c4cfc9bed15  raw summary
4ab7697a435c9d95cd4162d861d9b291d03abb5186f6d4523b467815723bafed  certificate bundle
8315b5cf8bda021589dae0123363a3a2906f39406a6e9749d2f6ca7e10cfc62b  independent replay
```

**Actual advance:** the REFEREE373 mixed-consumer obstruction is repaired globally, with an explicit linear factor, for the frozen proposed CANON2R grammar—including repeated inputs and reconvergent shared owners. **Precise remaining gaps:** authenticate the historical `/341` exported-wire/LOCAL/facet serialization rather than substituting CANON2R, and prove a noncircular polynomial simulation from a `SAT in P` decider-induced proof system into that same fixed calculus. P versus NP remains OPEN.

<!-- END_OF_VERIFIED_REPORT::LSPV-5::REFEREE374 -->
