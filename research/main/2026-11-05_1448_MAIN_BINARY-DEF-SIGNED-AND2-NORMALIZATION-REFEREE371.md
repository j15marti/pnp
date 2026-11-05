<!-- LSPV-5 REPORT::REFEREE371::2026-11-05T14:48:00-08:00 -->
# LSPV-5 REFEREE371: every semantic binary DEF has a constant signed-AND2 normal form, including projected defining facets

**November 5, 2026, 14:48 PST. Route B primary.** **PROVED/EXACT, RESTRICTED:** every conservative two-input Boolean definition in the semantic `/341` model can be replaced, once per shared owner, by at most three globally fresh signed-AND2 definitions. Every non-tautological defining clause over the old two inputs and output is derivable from the replacement by a constant-size strict-Resolution sub-DAG. This gives a polynomial original-source clausal-interface normalization and a new restricted extension/GF(2) escape-budget composition. **COMPUTATIONAL:** independent Python and Node implementations exhaust all 16 binary functions, all projected clause facets, and 9,216 depth-two signed/reconvergent networks. **OPEN:** the historical accepted-byte grammar for DEF facets, private/exported wires, LOCAL-CONVERT, AND3 and GF(2); normalization of every intensional native consumer; a superpolynomial minimum for the full fixed calculus; B1/B2/B3; P versus NP.

No rule, weight, role, task, schedule, enabled state, or other role's manuscript region was changed.

## IDEA fixed before SEARCH, then revised

The initial hypothesis was that the unresolved historical `/341` grammar could be falsified by two sound serializers that disagree about repeated-input or tautological DEF facets. Its prediction was: absent an overlooked distinctness clause or authoritative checker, both serializers would satisfy the extensional prose but disagree on accepted bytes. Four falsifiers were fixed:

1. historical `/341` actually specifies positional facet multiplicity or forbids repeated signed inputs;
2. an authoritative checker selects one byte language;
3. one serializer is semantically unsound or not a unique conservative extension;
4. the ambiguity disappears once every exported wire and source-provenance reference is explicit.

SEARCH confirmed the ambiguity but also showed that CANON2 and REFEREE370 already recorded it. Repeating the ambiguity would not advance the transfer. The revised falsifiable claim was stronger and constructive:

> Every arbitrary native two-input Boolean DEF can be compiled to at most three shared signed-AND2 owners, and every old clausal facet can be reconstructed by strict Resolution with constant overhead. A counterexample is any binary truth table, signed/repeated/reconvergent consumer, or old projected facet for which the construction is not a unique conservative extension or has no strict-Resolution subclause.

The first implementation exposed a further missing obligation: remapping only the exported output wire does **not** translate a proof that directly names an old defining-clause slot. The experiment and theorem were revised to reconstruct every projected old facet. A first corrupt-control design also failed because it merely renamed an output truth-function tag while preserving semantics; it was replaced by an actual last-gate polarity corruption and the harness now aborts if any hostile control is accepted.

## Authenticated historical model and exact scope

The load-bearing source is `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. Its DEF prose says: at unit cost introduce one fresh variable as a two-input Boolean gate; all defining relations belong to that same charged node; every valuation of previous variables extends uniquely; later uses reference the charged owner. It does **not** define accepted bytes for gate tags, repeated signed occurrences, positional tautological facets, clause selectors, private wires, or exported-wire typing.

This theorem uses the resulting **semantic clausal interface**:

- a DEF owner denotes a binary truth function of two signed input wires and one globally fresh positive output;
- later gate consumers may use either polarity of that output;
- a clausal-facet consumer may name any clause over the two inputs and output that is valid for the graph of the function;
- a tautological old facet is bypassed by the usual strict-subclause invariant;
- every owner is compiled once in topological order and every consumer reference is remapped to its final output owner.

It is not an accepted-byte theorem and does not silently choose CANON1, CANON2 or CANON2R.

## Theorem 371.1: three signed-AND2 definitions suffice

Let $f:\{0,1\}^2\to\{0,1\}$ be arbitrary. A signed-AND2 owner has the form

$$
z\leftrightarrow(\ell_1\land\ell_2),
$$

where each $\ell_i$ is either polarity of an original input or an earlier fresh wire; repeated and complementary inputs are allowed at the semantic level. Then $f(a,b)$ is the positive output of a network of at most three such owners.

**Proof.** The following constructions cover all 16 truth tables. Constants, literals and the four minterms require at most two signed inputs to one AND owner. AND/negated-input variants require one owner. OR/NOR and implication variants are obtained by De Morgan using one minterm owner followed by the repeated-input negation idiom $w\leftrightarrow(\neg z\land\neg z)$. XOR is

$$
u\leftrightarrow(a\land b),\qquad
v\leftrightarrow(\neg a\land\neg b),\qquad
z\leftrightarrow(\neg u\land\neg v),
$$

and XNOR uses the two unequal minterms followed by the same NOR construction. These are all binary functions. Every introduced output is globally fresh and is uniquely fixed by prior wires, so the network is a conservative unique extension. QED.

The executable breadth-first synthesis independently found 9 functions needing one owner in its copy-inclusive basis, 5 needing two and XOR/XNOR needing three. The lower-bound part of those finite minima is only a computational audit; the written theorem needs only the explicit at-most-three constructions.

## Theorem 371.2: old clausal facets have constant strict-Resolution reconstructions

Instantiate the standard three clauses of every replacement owner

$$
(\neg z\lor\ell_1),\qquad(\neg z\lor\ell_2),\qquad
(z\lor\neg\ell_1\lor\neg\ell_2),
$$

normalizing duplicate and tautological literals extensionally. The complete replacement network has at most five named variables: $a,b$ and at most three fresh wires. Let $C(a,b,z)$ be any non-tautological old defining clause valid for $z=f(a,b)$. Then the replacement CNF entails $C$. By implicational completeness of Resolution, its strict Resolution closure contains a subclause of $C$. There are at most $3^5=243$ distinct non-tautological clauses (including the empty clause) on five variables, so materializing the entire closure uses fewer than 243 distinct strict Resolution nodes. Tautological old slots need no reconstruction: under the strict-subclause invariant, any inference using one is either tautological or is represented by a subclause already justified by the other premise. Thus one old DEF owner, all its clausal slots and its exported output can be replaced with a fixed constant number of paid nodes, with complete original ancestry retained.

The finite audit sharpens the generic constant. Across all functions there were 98 valid nonempty projected implicates; the largest complete closure had 108 clauses, and every projected implicate had a strict derived subclause using at most two Resolution nodes. Fifty-six targets were represented by proper subclauses. These sharper constants are COMPUTATIONAL; the symbolic polynomial theorem uses the safe 243-clause bound.

## Corollary 371.3: shared-DAG cost and the established-family transfer

Process an original semantic proof in topological order. Compile each arbitrary binary DEF owner once; cache its final fresh output and the derived representatives of any exposed clausal slots; remap all downstream polarities and references. Reconvergent consumers share this compiled owner. No branch is duplicated, no branch-local lemma leaks, and no ASSUME/MERGE/discharge rule is added.

If the original proof has $q$ paid nodes and $d$ arbitrary binary DEF owners, the normalized proof has at most $d'\le3d$ signed-AND2 owners and, using the deliberately loose full-closure bound,

$$
q_*\le q-d+3d+243d=q+245d\le246q.
$$

Compose this with LSPV-1/371's signed-AND2 elimination and LSPV-1/425's strict GF(2) row compiler in the declared normalized $X(K)$ fragment. For the established cubic-expander odd-Tseitin 3-CNF family,

$$
L_{\rm Res}(F_h)
\le 64^{3d}\left(4h+4C_K(q_*+1)2^{2b}+1\right),
$$

and hence

$$
\boxed{18d+2b+\log_2(4h+q+245d+2)\ge \alpha h-O_K(1).}
$$

This is a **restricted escape-budget tradeoff**, not a lower bound on $q$ alone. The actual full historical calculus already has the $4h-1$ AND3/GF(2) proof of this family, so odd Tseitin cannot witness superpolynomial full-mixed $\overline W_R$.

## Established family/theorem/encoding/shortcut ledger

| Family | Exact encoding and size | Published theorem/model | Strong known shortcut/control | Remaining transfer |
|---|---|---|---|---|
| Cubic-expander odd Tseitin | One variable per edge; each degree-3 parity row is its four proper signed width-3 blockers. $h$ vertices, $3h/2$ variables, $4h$ clauses, DIMACS $N=\Theta(h\log(h+2))$. | Urquhart 1987 and the Ben-Sasson--Wigderson width treatment yield $2^{\Omega(h)}$ ordinary unrestricted shared-DAG Resolution size for appropriate expanders. | Historical `/341` AND3/GF(2) refutation has exact cost $4h-1$ on connected bridgeless cubic sources. | Resolution hardness does not transfer to the full mixed calculus. Corollary 371.3 covers only normalized bounded-width/definition budgets. |
| Unary PHP | Standard row clauses plus binary collision clauses; $N=\Theta(h^3\log(h+2))$ in the project encoding; not 3-CNF for unbounded $h$. | Haken 1985: exponential ordinary shared-DAG Resolution size. | Cook 1976: polynomial Extended-Resolution proofs. | Equisatisfiable 3-CNF conversion alone gives no lower-bound-preserving direction. LSPV-1/427 gives only an explicit reverse-output firewall for a different original BPHP/Res(XOR) target. |
| Path graph-PHP control | $2h+1$ clauses of width at most two, $N=\Theta(h\log h)$. | LSPV-3/431 proves exact mixed minimum $2h$ and a legal Resolution chain. | The chain itself; it is a restriction of complete PHP. | Demonstrates that source restriction and individual essentiality do not transport Haken hardness. |

The selected hard family is certified UNSAT and Resolution-hard in its stated proof model. None of these facts is an arbitrary SAT-machine lower bound.

## Branching/shared proof-DAG audit

Historical `R_mix341` has no authenticated case-split/discharge/weakening rules. This run does not add them. In a future declared branch wrapper, a compiled definition owner may be shared only in a context where all its premises are available. Both children of an UNSAT split are AND obligations, and a branch-local conclusion may cross branches only after legal discharge. The present normalizer is context-preserving: it compiles one owner inside the same context and remaps only consumers whose dependency path already reaches that owner.

Logical distinct-node work, weighted critical-path depth, and realizable schedules remain separate. The normalizer proves a work upper bound; it does not prove an optimal span or small peak space. Retaining all compiled facets can use more memory than recomputing them; either schedule must separately charge references, storage, retrieval and recomputation.

## Exact computation, hostile controls and physical ledger

The Python producer and independent no-import Node verifier each synthesized all 16 functions without importing one another. Results:

- 64 abstract truth-table checks;
- 164 unique-extension and defining-facet checks;
- 98 projected old-facet implicates, with maximum closure 108 clauses and maximum two-node strict-Resolution witness;
- 9,216 arbitrary depth-two networks whose second gate uses signed, repeated or reconvergent inputs from $\{a,b,z\}$;
- 36,864 nested valuation checks;
- SAT control $(a\lor b)$ retained exactly three projected models; UNSAT control $(a)\land(\neg a)$ retained zero;
- empty template, corrupt XOR polarity, short truth table and nonfresh-output controls rejected;
- independent Node replay passed 37,059 assertions.

Final host measurements: Python construction/search 0.336 s with `ru_maxrss` 10,752 KiB; Node replay 0.049 s with sampled RSS 53,043,200 bytes. These include enumeration, parsing, closure construction, output and checking on the host. They are offline diagnostics, not native proof steps or an FLMV machine. Proof discovery is intentionally excluded from the ideal minimum but must be charged for an implemented normalizer, together with source reads, allocation, serialization, verification, retained caches and all-phase peak memory. Logical XOR tracing was not used.

## SEARCH record, repositories and peer assessment

Read the governing five-role handoff, issue #3 through LSPV-1/427, LSPV-3/431 and LSPV-4/423, historical `/341`, LSPV-1/371 and `/425`, REFEREE370, AGENTS/CODEX governance, and the actual current assessments:

- `GROKPROOF/2026-11-05_1913_PROGRESS.md`, blob `8a004bf478aa8dc111106855fc50cd7df11beb7c`;
- `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`, blob `79e4d4e7...`.

Grok treats FRAT-XOR as certificate infrastructure, not B3. Claude's world ledger labels equivalences as reformulations rather than separation proofs. Neither supplies historical native bytes or a decider-to-same-system compiler. LSPV-1/427 (blob `108fa9ef...`) correctly proves only a reverse explicit-output no-go into original BPHP Res(XOR); LSPV-3/431 (blob `10f63cc1...`) correctly exhibits the restriction-direction firewall.

Indexed literature queries were `primary extended resolution arbitrary extension rule conjunction gates signed literals functional completeness proof complexity`, `Tseitin extension rule two input Boolean gate conjunction normal form extended resolution primary`, `Urquhart hard examples resolution cubic Tseitin expander exact CNF primary`, and `resolution over linear equations modulo two DAG lower bound current primary`. Direct Google-branded interactive search was unavailable; indexed web search was used and is not claimed as direct Google execution. Primary sources checked included Urquhart 1987 (DOI 10.1145/7531.8928), Cook's ER work, standard ER definitions, and current Res($\oplus$) papers. Current lower bounds found are model-qualified; in particular regular/tree-like restrictions cannot be promoted to full DAG extension-enabled `R_mix341`.

Change-aware repository heads and findings:

| Repository | Head | Finding |
|---|---:|---|
| `konard/p-vs-np` | `ecedd2b45f1c...` | No native mixed-calculus normalizer or B3 theorem. |
| `blkph0x/p-vs-np-proof-research` | `7dedc73f758d...` | Scoped certificate/Resolution material only. |
| `meelgroup/frat-xor` | `18cd6bc17af1...` | Useful explicit clause/XOR proof format and checker discipline; not historical `/341`. |
| `openai/math` | `4eaee8754825...` | Targeted proof-complexity search found no relevant normalizer. |
| `berkeley-abc/abc` | `0d3399a4d62f...` | Circuit tooling; no theorem establishing the required source-authenticated proof translation. |
| `lsils/mockturtle` | `4a592f35eccb...` | AIG AND-inverter networks corroborate the engineering basis choice, not the mathematical transfer. |

No-result searches are recorded only as limitations, not novelty evidence.

## B3 audit and exact remaining gap

B3 remains

$$
\mathrm{SAT}\in\mathrm P\Longrightarrow
\exists C,k\;\forall N\quad
\overline W_{R_{\mathrm{mix341}}}(N)\le C(N+1)^k.
$$

The present compiler relates one semantic DEF basis to a signed-AND2 fragment. It does not turn a rejecting polynomial-time machine trace into a source-authenticated proof, prove the machine's global correctness inside the calculus, or show polynomial proofs of the decider-induced Cook--Reckhow system. Cook--Reckhow gives some polynomially bounded proof system under the relevant collapse, not polynomial boundedness of this preselected one. Thus the result neither proves nor refutes B3.

**Actual advance:** arbitrary binary DEF tags are no longer a semantic obstruction at the clausal interface; they cost only a constant-factor shared normalization and triple the signed-AND2 definition budget. **Precise next gap:** authenticate exact historical bytes and prove that every native LOCAL-CONVERT/exported-wire/AND3/GF(2) consumer accepts this remapping, or exhibit an accepted trace whose intensional slot/type behavior defeats it. Independently derive same-system proof existence from bare SAT in P without assuming reflection or polynomial certificates. P versus NP remains **OPEN**.

## Reproducibility and hashes

- `experiments/arc/lspv5_371/boolean_def_to_signed_and_referee371.py`
- `experiments/arc/lspv5_371/verify_boolean_def_to_signed_and_referee371.mjs`
- `results/raw/arc/2026-11-05_1448_LSPV5_REFEREE371_raw.json`
- `results/raw/arc/2026-11-05_1448_LSPV5_REFEREE371_independent.json`

```text
0e2b3d848707768e971c88d49f5216945dd0cd0b3b6ebeb5d0f9c745403414b7  Python
75e93279e156984ab8ed753fe9dde4462797b1c161646ed8cd8f03abd421287d  Node
ddef999effa31d76203d5ba2f88d1ec512479436401ee1f6866740b08068f3b3  raw
c5ca9c56bb82b41bd0b24a9c8dc2c36b2500e2de2f7442dcf1eb5b85ae37687c  independent
```
