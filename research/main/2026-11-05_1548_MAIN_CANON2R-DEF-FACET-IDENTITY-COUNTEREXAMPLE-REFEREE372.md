<!-- LSPV-5 REPORT::REFEREE372::2026-11-05T15:48:00-08:00 -->
# LSPV-5 REFEREE372: accepted-byte binary-DEF normalization yields strict subclauses, not exact facet identity

**November 5, 2026, 15:48 PST. Route B primary.** **PROVED/EXACT FOR THE PROPOSED FROZEN CANON2R CHECKER:** all 16 accepted binary DEF truth tags admit an AND-only replacement of at most three paid definitions, and every one of the 64 exposed old facets has an actually accepted strict-Resolution representative that is a subclause. **COUNTEREXAMPLE:** exact positional-facet preservation fails for 24 of the 64 facets. The smallest witness is the accepted constant-zero gate on distinct inputs: its old facet $(a\lor b\lor\neg z)$ cannot be derived exactly from the legal aliased replacement $z\leftrightarrow(b\land\neg b)$, although the stronger clause $\neg z$ is derived. **OPEN:** a whole-proof normalization through all mixed consumers, the authoritative historical `/341` byte grammar, a superpolynomial minimum for the entire mixed calculus, B1/B2/B3, and P versus NP.

No historical rule or weight was changed. No case-split, weakening, discharge, or branch rule was added. Root `main.tex`, task metadata, schedules, enabled states, and other roles' regions were not touched.

## IDEA -> SEARCH -> ITERATE

### Initial falsifiable hypothesis

The starting hypothesis was:

> REFEREE371's semantic binary-DEF normalizer can be serialized as actual frozen CANON2R certificates without changing ancestry or shared-node cost, provided every old gate facet is represented by a derived strict-Resolution clause.

The fixed falsifiers were:

1. an old accepted truth tag has no legal AND-only replacement under the checker's exact row convention;
2. repeated-input or tautological defining facets are rejected;
3. some old facet has no accepted strict-Resolution representative;
4. owner-qualified reconvergence or global freshness fails after renaming.

### SEARCH evidence and revision

The actual CANON2 checker in `experiments/arc/lspv5_361/rmix341_canon2_repair_referee361.py` accepts arbitrary four-bit binary truth tags, exactly four addressable row facets, repeated inputs, fresh sequential outputs, oriented strict Resolution, original-coordinate LOCAL/AND3 rules, and typed affine GF(2) nodes. `experiments/arc/lspv5_362/rmix341_raw_affine_firewall_referee362.py` adds exact raw-source hashing and binding. These are executable proposed completions, not authenticated historical `/341` authority.

The first byte-level run failed on truth table `0010`: REFEREE371 indexed rows by $2a+b$, whereas CANON2 indexes by $a+2b$. An explicit bit permutation repaired the serialization. This is a material authentication finding: extensional truth alone did not determine accepted bytes.

After repair, every old facet had a strict derived **subclause**, but exact identity failed systematically. The revised claim therefore distinguishes:

- **proved:** polynomial local normalization at a Resolution/subclause interface;
- **falsified:** exact positional-facet preservation under strict Resolution without weakening;
- **open:** transparent substitution into every mixed-rule consumer.

## Exact accepted-byte construction

The source bytes are fixed as

```text
c REFEREE372 exact raw source
p cnf 2 2
1 0
-1 0
```

For each of all 16 binary functions, the producer performs the following independently checkable steps.

1. Emit the old arbitrary binary DEF on inputs 1 and 2 and verify acceptance by the actual frozen CANON2 checker and exact CANON2R raw wrapper.
2. Compile the function to at most three AND-only DEF owners. Signed input polarity is encoded in the exact four-bit truth tag; repeated inputs are permitted by the checker.
3. Expose all four defining facets of every replacement owner.
4. Build strict oriented Resolution closure.
5. For each of the four old positional facets, select an accepted derived subclause.
6. Trim the certificate to the union of replacement owners and the actual witness ancestries, renumber it, and replay both checkers.

Each shared old owner is compiled once. The validation certificate's final contradiction is a separate two-source-clause Resolution core. Thus these are accepted local-normalization traces, not claims that the extra gate nodes occur in a minimum refutation.

## Theorem 372.1: actual local subclause normalizer

For every four-bit binary DEF tag accepted by the frozen CANON2 checker, there is a CANON2R-accepted replacement using at most three AND-only DEF records such that every old exposed defining facet has a strict-Resolution-derived subclause. The trimmed validation traces use 2--12 paid nodes, 371--1,585 CANON2 certificate bytes, and 583--1,797 CANON2R wrapper bytes. Each facet witness uses at most two Resolution ancestors.

**Proof.** The executable construction enumerates the finite complete domain of 16 tags. For each tag it emits the replacement records, derives all selected subclauses by the checker's own oriented RES rule, trims to their ancestry union, serializes the exact raw-source binding, and obtains acceptance from both frozen checkers. The independent no-import verifier reconstructs tag semantics, unique extension, subclause inclusion, Resolution steps, freshness, raw hash, and all hostile controls. This establishes the finite checker-relative statement. The symbolic polynomial consequence follows because each owner expands to at most three definitions and four constant-ancestry representatives. QED.

This theorem is stronger than an independent reimplementation result because the produced bytes are passed through the actual frozen project checker. It remains checker-relative, not historical authority.

## Counterexample 372.2: exact old-facet identity is false

Let the accepted old gate be the constant-zero function on distinct inputs $a,b$ and output $z$, with truth tag `0000`. Positional facet 0 is

$$C=(a\lor b\lor\neg z).$$

A legal AND-only replacement is

$$z\leftrightarrow(b\land\neg b),$$

implemented by one accepted DEF whose two input IDs both equal $b$ and whose signed truth tag is checker-valid. Its defining clauses mention only $b,z$. Strict Resolution never introduces a variable absent from every ancestor, so no strict-Resolution derivation from these clauses can derive $C$ exactly because $a$ is absent. The checker nevertheless accepts a derivation of the stronger representative

$$\neg z\subset C.$$

Hence the universal claim "every old positional facet is exactly derivable by strict Resolution from an equivalent AND-only replacement" is false. No semantic oracle, malformed proof, omitted premise, or altered rule is involved.

Across all 64 old facets, 40 exact target clauses occur in strict closure and 24 are represented only by proper subclauses. This is not an asymptotic lower bound; it is a complete finite falsification of a precise normalization claim.

## Why this does not yet normalize a whole mixed proof

Resolution is monotone under strengthening in the needed clausal sense, so the subclause interface suffices for downstream Resolution-only consumers. It does not automatically preserve every intensional native consumer:

- CANON2 AND3 and LOCAL-CONVERT accept only original-coordinate clauses, so auxiliary DEF facets cannot directly feed them;
- after Resolution eliminates auxiliaries, a strengthened original clause may reach AND3/LOCAL, where exact clause semantics or position can affect legality;
- GF(2) ports are typed affine objects, not arbitrary clausal consequences;
- exported/private wire and original-source provenance must remain owner-qualified through every reconvergent consumer.

Therefore replacing every old facet by a subclause is not yet a rule-by-rule proof translation. A full theorem must prove a legal simulation for each downstream native rule or exhibit a mixed accepted trace that defeats it.

## Established-family and transfer ledger

| Family/control | Exact encoding and parameter | Established model-qualified result | Strong legal shortcut/control | Remaining transfer |
|---|---|---|---|---|
| Cubic-expander odd Tseitin 3-CNF | One variable per edge; each degree-3 parity equation is its four signed width-3 blocking clauses. For $h$ vertices: $3h/2$ variables, $4h$ clauses, binary length $\Theta(h\log(h+2))$. | Urquhart's expander/Tseitin examples have $2^{\Omega(h)}$ ordinary unrestricted shared-DAG Resolution size; later width methods give the same model-qualified phenomenon. | Native AND3/GF(2) joins the $h$ rows to contradiction in exact project cost $4h-1$. LSPV-1/428 also shows a canonical explicit row table may need $2^t-1$ RES nodes while a native GF(2) join costs one. | Resolution hardness does not lower-bound the full mixed minimum. Any table backtranslation must be polynomial or cannot support B3/all-machine transfer. |
| Unary PHP | Standard pigeon row clauses plus binary collision clauses; not width-3 for unbounded size. | Haken: exponential ordinary DAG Resolution size. | Cook Extended Resolution has polynomial proofs; Buss-style substitution yields polynomial Frege/ER proofs for graph-PHP restrictions noted by LSPV-3/432. | An equisatisfiable 3-CNF encoding is insufficient. A lower-bound-preserving simulation direction and encoded-size overhead are required. |
| Width-$\le3$ source padding | LSPV-3/433's exact short-clause padding into proper exact-3 CNF. | Resolution sandwich only, with the stated native directions. | Preserves a Resolution control, not arbitrary mixed hardness. | Must not be used to transport Haken or a mixed-system lower bound without the missing reverse simulation. |

The selected families are certified UNSAT and hard only in the stated proof systems. None is established hard for arbitrary SAT machines.

## Branching/shared-DAG audit

The frozen historical target has no authenticated case-split/discharge rule, so this run adds none. The local replacement is an AND dependency: every selected facet witness depends on all recorded premises in its oriented Resolution ancestry. The trimmed graph charges the union of distinct owner and inference nodes once; reconvergent facet references share those nodes.

If a future external branch wrapper splits on $x$, both contexts $\Gamma,x\vdash\bot$ and $\Gamma,\neg x\vdash\bot$ remain required. A gate or lemma may be shared only if its entire premise context is common or legally discharged. This experiment does not justify cross-branch leakage, omitted cases, or free weakening. It reports distinct-node work only; weighted span and a realizable retention/recomputation schedule remain separate quantities.

## SAT, UNSAT, malformed and corrupt controls

The bound raw source is UNSAT by its two unit clauses. A same-sign SAT source is rejected because the alleged final contradiction is not an oriented resolvent. The following hostile certificates are also rejected by the actual implementation:

- corrupted gate truth tag;
- nonfresh DEF output;
- corrupted Resolution pivot/type;
- hidden extra payload key;
- raw-source hash mismatch.

The constant-zero counterexample itself is legal and accepted. It falsifies exact facet identity without exploiting malformed input.

## Physical/resource ledger

The producer charges finite synthesis, closure construction, ancestry trimming, serialization, raw-source hashing, actual checker replay, hostile controls, and output. Final Python construction/checking took 15.48 s with sampled peak RSS 12,672 KiB. The independent Node replay took 0.0035 s with sampled RSS 41,476,096 bytes and passed 941 assertions. The certificate bundle is 110,592 bytes. Logical XOR tracing was not used.

These are host experiment costs, not native inference weights. An implemented general translator must additionally charge source/index reads, parsing, owner maps, output renaming, reference lookup, storage or recomputation, failed strategies, certificate writing/checking, and all-phase peak space. Free after-the-fact choice remains valid only for the ideal minimum; it does not make construction or verification free for an actual machine.

## SEARCH record

Project sources read include the governing five-role handoff, current issue #3 through LSPV-1/428, LSPV-3/432--433 and LSPV-4/424, REFEREE371, the actual CANON2/CANON2R checkers, and the current assessments:

- `GROKPROOF/2026-11-05_1913_PROGRESS.md`, blob `8a004bf478aa8dc111106855fc50cd7df11beb7c`;
- `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`, blob prefix `79e4d4e7`.

Neither assessment supplies the missing historical byte grammar or a noncircular same-system B3 compiler.

Indexed literature queries included `arbitrary Boolean extension gates AND basis proof complexity`, `Tseitin extension rule exact defining clauses`, `Urquhart hard examples resolution 3-CNF expander`, and `Resolution implicational completeness derived subclause`. Direct Google-branded interactive search was unavailable; indexed web search was used and is not reported as direct Google execution. The sources support only model-qualified statements: Resolution implicational completeness is modulo subsumption, ER permits definitional extensions, and Urquhart's bound is for ordinary Resolution rather than the full mixed calculus.

Change-aware repository review:

| Repository | Pinned head | Relevant finding |
|---|---:|---|
| `konard/p-vs-np` | `ecedd2b45f1c...` | Targeted search encountered a transient rate limit; pinned content still supplies no native CANON2R normalizer or B3 theorem. |
| `blkph0x/p-vs-np-proof-research` | `7dedc73f758d...` | No checker-relative mixed-rule transfer or noncircular B3 result. |
| `meelgroup/frat-xor` | `18cd6bc17af1...` | Explicit clause/XOR certificate infrastructure; not authority for historical `/341`. |
| `openai/math` | `4eaee8754825...` | No relevant proof-complexity normalizer found. |
| `berkeley-abc/abc` | `0d3399a4d62f...` | AIG engineering control, not a proof translation theorem. |
| `lsils/mockturtle` | `4a592f35eccb...` | AND-inverter construction control, not B3 or source authentication. |

No-result searches are limitations, not novelty claims.

## B3 status and exact next implication

B3 remains

$$
\mathrm{SAT}\in\mathrm P\Longrightarrow
\exists C,k\;\forall N\quad
\overline W_{R_{\mathrm{mix341}}}(N)\le C(N+1)^k.
$$

This run neither proves nor refutes B3. It normalizes a finite gate basis at one clausal interface; it does not turn an arbitrary polynomial decider's rejection trace into a proof in the same fixed calculus, establish internal reflection of the decider's correctness, or show that the decider-induced Cook--Reckhow proof system is polynomially simulated by CANON2R/historical `R_mix341`.

**Actual advance:** an accepted-byte local normalizer exists for all 16 binary tags at the strict-subclause interface, and the stronger exact-facet claim has an explicit legal counterexample. **Precise remaining gap:** prove rule-specific monotone simulations from these strengthened representatives into every legal LOCAL-CONVERT, AND3, GF(2), exported-wire, and shared-branch consumer, or produce an accepted mixed trace showing failure. Separately derive same-system polynomial proof existence from `SAT in P` without assuming reflection or polynomial certificates. P versus NP remains **OPEN**.

## Reproducibility and hashes

- `experiments/arc/lspv5_372/canon2r_binary_def_normalizer_referee372.py`
- `experiments/arc/lspv5_372/verify_canon2r_binary_def_referee372.mjs`
- `results/raw/arc/2026-11-05_1548_LSPV5_REFEREE372_raw.json`
- `results/raw/arc/2026-11-05_1548_LSPV5_REFEREE372_certificates.json`
- `results/raw/arc/2026-11-05_1548_LSPV5_REFEREE372_independent.json`

```text
b47994456e2a9f9ebcc661a8137d5862a1fa363538cf48a52862a5393624c4d3  Python producer
c859e37027228531c07970fdefecc9bc6646764610b525f04e9efd13981907a2  Node verifier
6c3b482d42fb2df3c3b9ff6e27e35d32fca41d1fedc2ca900a63eda3aa0c0f2e  raw summary
4d6bb04dfeace93249c891ebca9b777b9ce7a105d18051b43608c548dc86a675  certificate bundle
790574aad33af907e5036d098f44fbdce94595efc16165ac0aed432f6cea4374  independent replay
```
