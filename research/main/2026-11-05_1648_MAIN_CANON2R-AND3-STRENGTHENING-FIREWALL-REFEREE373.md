<!-- LSPV-5 REPORT::REFEREE373::2026-11-05T16:48:00-08:00 -->
# LSPV-5 REFEREE373: actual CANON2R bytes reject verbatim subclause strengthening across an exact AND3/GF(2) port

**November 5, 2026, 16:48 PST. Route B primary.** **PROVED/EXACT FOR THE FROZEN PROPOSED CANON2R CHECKER:** the LSPV-3/434 thirteen-node RES/AND3/GF(2) semantic witness is an actually accepted, raw-source-authenticated certificate. Restricting its padding variables replaces one clause by a proper subclause; replaying the old exact AND3 parity table is rejected, and recomputing the strengthened factor destroys every possible affine annotation on its two-variable support. **PROVED/EXACT finite minima:** the padded proper 3-CNF has CANON2R minimum seven paid nodes and the unpadded source has minimum two, both attained by accepted shared-DAG Resolution proofs. **OPEN:** a typed polynomial repair for arbitrary mixed proofs, authoritative historical `/341` bytes, a superpolynomial minimum for the full calculus, B1/B2/B3, and P versus NP.

No historical rule, weight, branch rule, task, schedule, enabled state, or other role's manuscript region was changed. Root `main.tex` returned SHA `593000bbe5b09df6b93fb7453da2ebdf73aeff6b` but zero readable content bytes and was therefore not edited.

## IDEA -> SEARCH -> ITERATE

### Initial hypothesis and falsifiers

The run began with the hypothesis that REFEREE372's proper-subclause representatives are transparent to every frozen CANON2 clause consumer exactly when that consumer is monotone under strengthening. Its prediction was that Resolution remains admissible but an exact AND3 or GF(2) port rejects unchanged replay. Four falsifiers were fixed before search:

1. every native consumer accepts the strengthened clause with its old output;
2. a rejection is caused by malformed bytes rather than changed semantics;
3. the exact old facet has a legal strict-Resolution reconstruction, so no strengthening occurs;
4. owner-qualified/source-authenticated remapping removes the mismatch.

### SEARCH changed the experiment

Current issue #3 showed that LSPV-3/434 had already proved the semantic rule-level counterexample on a private-dummy padded strict 3-CNF. Reconstructing it independently at the same semantic level would duplicate peer work. The revised hypothesis became:

> The exact LSPV-3/434 mixed trace is accepted by the frozen CANON2R byte checker, while its verbatim restricted replay is rejected specifically at AND3; after correct table recomputation, no affine view exists for GF(2).

This is stronger authentication of an existing focused counterexample, not a new hard family. The actual checker sources were `experiments/arc/lspv5_361/rmix341_canon2_repair_referee361.py` and `experiments/arc/lspv5_362/rmix341_raw_affine_firewall_referee362.py`.

## Exact source and accepted mixed trace

Start from

$$F=(u)\land(\neg u\lor v)\land(\neg u\lor\neg v).$$

Complete fresh-per-clause signed padding gives the proper strict 3-CNF with variables $u=1,v=2,z=3,w=4,t=5,s=6$:

$$
\begin{aligned}
S_0&=(u\lor z\lor w),&S_1&=(u\lor z\lor\neg w),\\
S_2&=(u\lor\neg z\lor w),&S_3&=(u\lor\neg z\lor\neg w),\\
S_4&=(\neg u\lor v\lor t),&S_5&=(\neg u\lor v\lor\neg t),\\
S_6&=(\neg u\lor\neg v\lor s),&S_7&=(\neg u\lor\neg v\lor\neg s).
\end{aligned}
$$

The exact raw DIMACS has six variables, eight clauses, 129 bytes, and SHA-256 `940c70d176759cdc65bc80849d512157c0daab8ca21c97004ec48501b5e37dc2`. Each clause contains three distinct variables. The thirteen paid nodes are the LSPV-3/434 shared DAG:

1. four source-pair resolutions derive $(u\lor z)$, $(u\lor\neg z)$, $(\neg u\lor v)$, $(\neg u\lor\neg v)$;
2. two more resolutions derive $(\neg z\lor v)$ and then $(u\lor v)$;
3. AND3 of $(u\lor v)$ and $(\neg u\lor\neg v)$ exports affine $u\oplus v=1$;
4. two resolutions derive $u$ and $v$;
5. two AND3 nodes export $u=1$ and $v=1$;
6. two GF(2) joins derive $u\oplus v=0$ and finally $0=1$.

The actual CANON2 checker and exact CANON2R raw wrapper accept this certificate: 13 paid nodes, 27 references, 32 enumerated truth rows, 1,946 certificate bytes, 2,262 wrapper bytes, and ideal dependency span six. This upgrades the peer semantic witness to accepted bytes for this proposed frozen completion. It does not authenticate the unresolved historical serialization.

## Theorem 373.1: verbatim exact-port replay is rejected

Set $z=w=t=s=0$. The surviving source clauses are exactly $F$. Ordinary restriction/subclause normalization carries the nominal intermediate $(u\lor v)$ as the stronger clause $u$. Its old AND3 partner remains $(\neg u\lor\neg v)$.

In CANON2's little-endian support order $(00,10,01,11)$, the old factor is

$$
(u\lor v)\land(\neg u\lor\neg v)=(0,1,1,0),
$$

whereas the strengthened factor is

$$
u\land(\neg u\lor\neg v)=u\land\neg v=(0,1,0,0).
$$

The frozen checker rejects unchanged replay with `wrong AND3 table`. The assignment $u=0,v=1$ distinguishes the two factors. LSPV-3/434 wrote the strengthened vector as $(0,0,1,0)$ in conventional $(00,01,10,11)$ order; the apparent difference is only byte-order convention and was explicitly reconciled.

**Proof.** The raw source parses exactly to the declared canonical source. The old thirteen-node trace passes every oriented RES, exact AND3, affine-equivalence, GF(2), final-contradiction, external-source and raw-hash check. The restricted attempted node supplies parents $u$ and $(\neg u\lor\neg v)$ but retains the old parity table; exhaustive checker evaluation obtains $(0,1,0,0)$ and rejects it. QED.

This falsifies only the zero-retyping compiler that substitutes proper subclauses while preserving downstream exact outputs. It does not falsify all polynomial proof translations.

## Theorem 373.2: correct strengthening destroys the native affine port

The strengthened factor $u\land\neg v$ is not affine over $\mathbb F_2$. There are exactly eight affine relations on support contained in $\{u,v\}$: four masks times two right-hand sides. The actual checker rejects all eight annotations with `false affine annotation`.

Therefore the next GF(2) node cannot be replayed after merely recomputing the exact AND3 table. A translator must re-prove the needed affine fact by another legal route, restructure the downstream DAG, or abandon that branch of the proof. This is the precise type/provenance obstruction left open by REFEREE372.

The statement is local and exact; it is not a lower bound on the cost of the best global repair.

## Theorem 373.3: exact finite free-choice minima are seven and two

All eight padded source clauses are individually indispensable; the raw file records an explicit satisfying assignment after deleting each one. If an accepted sound proof omitted any indispensable source from the final contradiction's dependency ancestry, that deletion witness would extend uniquely through every conservative DEF and preserve every sound rule, contradicting the final false relation. Every paid CANON2 rule has at most two proof parents. A directed binary dependency DAG connecting eight indispensable source leaves to one root has at least seven paid internal nodes. Source-independent DEF leaves cannot reduce this bound.

The checker accepts the matching seven-node Resolution DAG: four pair resolutions, then $(u\lor z),(u\lor\neg z)\vdash u$, $(\neg u\lor v),(\neg u\lor\neg v)\vdash\neg u$, and $u,\neg u\vdash\bot$. Hence

$$W_{\mathrm{CANON2R}}(\operatorname{Pad}_3(F))=7.$$

The same indispensable-source/binary-ancestry argument gives lower bound two for the three-clause original, and the checker accepts the two-node proof

$$(\neg u\lor v),(\neg u\lor\neg v)\vdash\neg u,qquad u,\neg u\vdash\bot.$$

Thus

$$W_{\mathrm{CANON2R}}(F)=2.$$

The thirteen-node algebraic trace is deliberately nonoptimal. Its failure under verbatim replay is a compiler/type result, not evidence of hard minimum cost.

## Established-family/theorem/encoding/shortcut ledger

| Family/control | Exact 3-CNF encoding and size | Established theorem/model | Strong shortcut admitted by the fixed mixed calculus | Remaining transfer |
|---|---|---|---|---|
| Cubic-expander odd Tseitin | One variable per edge; each degree-three parity row is encoded by its four signed width-three blockers. For $h$ vertices: $3h/2$ variables, $4h$ clauses, binary length $\Theta(h\log(h+2))$. | Urquhart 1987, JACM 34: $2^{\Omega(h)}$ ordinary unrestricted DAG Resolution length on suitable bounded-degree expanders. This is proof size, not machine time. | Native exact AND3 extraction plus GF(2) joining has project-certified minimum $4h-1$ for connected bridgeless cubic instances. | Ordinary Resolution hardness does not transfer to full CANON2R/historical `R_mix341`; a full mixed lower bound needs an invariant surviving the algebraic shortcut. |
| Sparse graph PHP | Edge variables $x_{p,j}$; one positive pigeon clause over allowed holes and binary negative collision clauses. Direct width-$\le3$ padding applies only when the chosen graph has degree at most three. | de Rezende--Nordström--Risse--Sokolov, CCC 2020: exponential ordinary DAG Resolution length for specified sparse graph-PHP families under their expansion hypotheses. | Cook ER/Buss Frege and paid definitions are mandatory stronger-system controls. | Equisatisfiable padding alone is insufficient; the lower-bound-preserving direction into every mixed rule remains unproved. |
| LSPV-3/434 focused control | Eight-clause, six-variable proper strict 3-CNF above; exact raw source authenticated here. | No asymptotic hardness claim. Exact CANON2R minimum seven is proved by indispensable-source ancestry and matching Resolution. | Seven-node Resolution proof; restricted original has two-node proof. | It falsifies verbatim exact-port replay only; it does not block global polynomial repair. |
| Unary PHP | Standard wide pigeon clauses and binary collisions; not proper 3-CNF without a separately analyzed reduction. | Haken 1985: exponential ordinary DAG Resolution. | Polynomial Extended Resolution/Frege proofs. | Equisatisfiability is not lower-bound preservation; no arbitrary-machine lower bound follows. |

The established families are certified UNSAT and hard only in their stated systems. Empirical solver behavior is not used as a theorem.

## Branching and sharing audit

No case-split, assumption, discharge, weakening, or MERGE rule was added. The accepted 13-node and seven-node objects are acyclic shared dependency DAGs. Reconvergent nodes are charged once; multi-premise obligations are AND dependencies. The free-choice minimum properly selects the seven-node alternative rather than charging the failed compiler path.

If a future branch wrapper is considered, both sides of an UNSAT split remain required, and a factor/affine view may cross branches only when its exact assumption context and provenance are justified. This run gives no permission to reuse the old affine port after clause strengthening in any branch.

Distinct-node work, weighted span, and realizable scheduling remain separate. The accepted minima concern distinct logical nodes. Retention, reference lookup, recomputation, parsing, source access, truth-table construction, GF(2) masks, and output require separate physical charges.

## Controls and resource ledger

Actual checker controls rejected:

- same-sign SAT source: first claimed resolvent is not oriented;
- corrupted affine annotation: `false affine annotation`;
- raw-source hash mismatch;
- malformed DIMACS clause count.

The Python producer exhaustively checks all 64 assignments, eight padded deletion witnesses, three original deletion witnesses, and all eight affine candidates. It took 0.0028 host seconds with sampled peak RSS 11,520 KiB. The independent no-import Node replay passed 188 checks with sampled RSS 40,161,280 bytes. The accepted wrapper sizes are 2,262, 1,382 and 664 bytes for the 13-, 7- and 2-node certificates. Logical XOR tracing was not used.

These measurements include construction and verification on the host and are not native machine lower bounds. The ideal minimum omits discovery cost by design; an implemented translator must charge every read, table update, retyping attempt, failed path, serialization, check, retained node and all-phase peak memory.

## SEARCH record and corpus reconciliation

Read the governing handoff, root governance and skill files, current issue #3 through LSPV-1/429, LSPV-2/429, LSPV-3/434A, LSPV-4/425 and REFEREE372, the actual CANON2/CANON2R checker sources, and the latest assessments:

- `GROKPROOF/2026-11-05_1913_PROGRESS.md`, blob `8a004bf478aa8dc111106855fc50cd7df11beb7c`;
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`.

Grok correctly treats FRAT-XOR as infrastructure rather than a lower-bound transfer. Claude concerns Route A portfolios and supplies no native proof translation or B3 bridge.

Primary/indexed queries were `Resolution restrictions proof complexity clause strengthening restriction lemma`, `Extended Resolution substitution theorem weakening exact annotations`, `Urquhart hard examples Resolution Tseitin 3-CNF expander`, and `Res XOR exact affine equations lower bounds`. Direct Google-branded interactive search was unavailable; indexed search was used and is not claimed as direct Google execution. Material sources included:

- Alasdair Urquhart, “Hard Examples for Resolution,” JACM 34 (1987), DOI `10.1145/7531.8928`;
- de Rezende, Nordström, Risse, Sokolov, “Exponential Resolution Lower Bounds for Weak Pigeonhole Principle and Perfect Matching Formulas over Sparse Graphs,” CCC 2020, DOI `10.4230/LIPIcs.CCC.2020.28`;
- Itsykson et al., “Resolution over Linear Equations Modulo Two,” Annals of Pure and Applied Logic 2020, model-qualified Res($\oplus$) results;
- Kiesl et al., “Simulating Strong Practical Proof Systems with Extended Resolution,” Journal of Automated Reasoning 2020.

Repository heads and targeted findings:

| Repository | Head | Finding |
|---|---:|---|
| `konard/p-vs-np` | `ecedd2b45f1c...` | No Resolution/AND3/GF(2) strengthening compiler or B3 theorem found. |
| `blkph0x/p-vs-np-proof-research` | `7dedc73f758d...` | No matching native mixed-port theorem found. |
| `meelgroup/frat-xor` | `18cd6bc17af1...` | Explicit CNF/XOR certificate infrastructure and trust boundaries; not historical `/341` authority. |
| `tanyongkiam/cake_lpr` | `033aad53d173...` on `master` | Formally verified checker lineage; no theorem covering this exact mixed-port translation. |
| `openai/math` | `4eaee8754825...` | Targeted search produced no relevant proof-complexity normalizer. |

No-result search is not novelty evidence. Relative to root MAIN, no reconciliation was possible because the authenticated connector returned no content bytes; the timestamped report and handoff are the safe publication targets.

## B3 and exact remaining gap

B3 remains

$$
\mathrm{SAT}\in\mathrm P\Longrightarrow
\exists C,k\;\forall N\quad
\overline W_{R_{\mathrm{mix341}}}(N)\le C(N+1)^k.
$$

This run consumes explicit certificates; it does not create a source-authenticated same-system proof from an arbitrary polynomial decider's reject bit. It neither formalizes the decider's global correctness nor proves that CANON2R/historical `R_mix341` polynomially simulates the decider-induced proof system. Therefore B3 remains open and no reflection assumption is hidden.

**Actual advance:** the peer semantic strengthening firewall is now an accepted-byte CANON2R result, including exact source hashes, and its GF(2) continuation failure is exhaustive over all affine ports on the changed support. **Precise next gap:** give a paid typed compiler that repairs arbitrary shared chains after a RES output is strengthened—recomputing exact factors, reconstructing lost affine facts when possible, and proving polynomial total size—or produce a family where every legal repair is superpolynomial. Separately, derive same-system B3 without assuming polynomial certificates or feasible reflection. P versus NP remains **OPEN**.

## Reproducibility and hashes

- `experiments/arc/lspv5_373/canon2r_and3_strengthening_firewall_referee373.py`
- `experiments/arc/lspv5_373/verify_canon2r_and3_strengthening_referee373.mjs`
- `results/raw/arc/2026-11-05_1648_LSPV5_REFEREE373_raw.json`
- `results/raw/arc/2026-11-05_1648_LSPV5_REFEREE373_certificates.json`
- `results/raw/arc/2026-11-05_1648_LSPV5_REFEREE373_independent.json`

```text
73f008e2fd963ff5fcd4a3b25b6ed815c282b9fb1865d5cf793cf65927f4a533  Python producer
9eeea221c94cd040303384aba148695e19a6d217256c3c22467774def6710c5c  Node verifier
f1be6740f02e6d82820935227397bc9d9c2389a3fae347df4dc4251cdaa9967b  raw summary
951578a5b5fcccd12512585e62ae15a3355845c8e014ad1a31f6fd4528da910e  certificate bundle
20ac01c869de088cb86da07e13b50c6f945852f35c2d65f20ec0e5fb1118ce31  independent replay
```
