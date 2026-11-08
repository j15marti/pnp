# LSPV-5/427 | Completion-robust native-core Tseitin exclusion

**November 7, 2026, 22:53 PST | Independent red team, Route B primary.**  
**Status:** PROVED/RESTRICTED theorem synthesis + COMPUTATIONAL exact-checker replay. **P versus NP OPEN.**

Affected exact tracker IDs: [P2-B12], [P2-D1], [P2-C3]. Dependencies [P2-B1] and noncircular B3 [P2-B2] remain OPEN. This report does not change the historical grammar, weights, agent allocation, identities, schedules, enabled states, or `main.tex`.

## IDEA and falsifiers stated before search

Hypothesis: the accepted SOURCE/AND3/XOR derivations plus [P2-B12]'s indispensable-source/binary-ancestry identity exclude simple bridgeless cubic odd-Tseitin as a superpolynomial witness in **every** sound source-explicit, unit-paid, at-most-binary completion retaining those core rules, even if the completion adds RES, DEF, LOCAL-CONVERT, branching, sharing, or other legal binary rules.

Falsifiers were: (F1) a rebalanced packet fails the exact recovered `/341` verifier or changes node cost; (F2) $4h-1$ work or $\lceil\log_2(4h)\rceil$ ideal depth fails on a fixture; (F3) the conclusion needs a non-native split/discharge/weakening rule or unsound source provenance; (F4) `proof2.txt` already records this exact accepted-byte/quantified synthesis.

## SEARCH: exact continuity and sources

Both complete root trackers were read before work: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and `proof2.txt` blob `5f88d535e3453a987cac863f5132156e38748e81`. Current head at the read was `3d98fee292efd5f239573e2bf7e8fa51661d5010`. The historical five-role handoff was read at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, path `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, blob `033b54b87b7cbe94912af5cf67daa52859143a07`. Current `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, issue #3 page 13 including comments `6718362584` and `6718372212`, Grok `GROKPROOF/2026-11-06_2316_PROGRESS.md` blob `a20fb8b3640d7574faf238a4a83a021bb0984808`, and Claude's actual world-ledger README/blob `de75a371ce3143a4495e6892df7fb04794a6b708` and report/blob `79e4d4e7e0e3edff3aba8610852c45534bdde128` were read. The ledger is classification context, not proof.

Peer artifacts read in full included LSPV-1/496 `research/agents/lspv-1/2026-11-07_2200_LSPV1_ONEHOT_BIT_ENCODING_TRANSFER496.md` blob `d6c56ef88750ea3733d496c97adaf499925d2a76`; LSPV-3/491 `research/agents/lspv-3/2026-11-07_2224_LSPV3_BALANCED_HISTORICAL_CHECKER_REPLAY491.md` blob `c9b7b445c2774f363b852531e3ad08cfe77574f3`; LSPV-4/487 blob `86c431e06250b1c5cceda129df0a420cd3578f13`; and the LSPV-5 interactive report/handoff blobs `265ea4da9067f4e99ba6ab0678a54b76fe6e4f06` / `2cbe57a80fbad141a9b16a4a1855393afeeab7ab`.

Primary-web queries were: `Haken 1985 pigeonhole principle resolution lower bound paper PDF`; `Cook 1976 feasible constructive proofs extended resolution pigeonhole principle polynomial proof PDF`; `Pang 2026 degree size relation resolution over polynomials arXiv 2610.00837 theorem 7.2`; and `Ben-Sasson Impagliazzo Wigderson near optimal separation tree-like general resolution Tseitin 3-CNF PDF`. Direct Google UI was unavailable; the configured web-search service located the primary/author-hosted records. Haken proves exponential ordinary-Resolution length for PHP, while the same abstract explicitly notes polynomial Extended-Resolution proofs. Cook's 1976 paper is the short-ER PHP control. Pang's arXiv:2610.00837v2 supplies an opposite-characteristic restricted proof-system lower bound only. Ben-Sasson--Impagliazzo--Wigderson separates tree-like from general Resolution and therefore reinforces the need to minimize over shared DAGs.

Required repository delta review:

- `konard/p-vs-np` remains pinned at `ecedd2b45f1c524d85c00b2da27a9c140025550c`; README blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` limits its checked theorem to $P\subseteq NP$ in a finite-machine model and does not close the converse.
- `blkph0x/p-vs-np-proof-research` remains pinned at `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` and peer-audit response blob `f5ed2f0b8d8a018a9f87587c25e29441e055019d` explicitly preserve finite/promise scope and the OPEN general problem.
- `meelgroup/frat-xor` remains at `18cd6bc17af10a9891c10a846ce966166f9fe0dc`; `format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f` authenticates original clause/XOR identifiers and native XOR additions in a distinct format. This is an upper-bound/control format, not historical R_mix341 authority.
- `peitl/short-proof` remains at `2c524cfceecf68b56f51d23f6b63255b502856d3`; README blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab` optimizes Resolution/Q-resolution only, so its finite minima do not quantify over the mixed calculus.
- `openai/math` remains at `4eaee87548250b2682affda7d05d947c05554bae`; its README blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` expressly describes mixed verification stages and raw research artifacts, not a P-versus-NP result.
- `anthropics/formal-math` remains at `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. Its `eth/README.md` blob `0b3dcf4a858ff802b3275fc5999ffb134c74de60`, `MainResults.lean` blob `1c62a550fa1e4cbec65bb7112f92ad67589afddc`, and `Solution.lean` blob `176892178e49792ae41368c13bb4973bae035b29` claim a subexponential 3-SAT/#3-SAT result and ETH failure in a specified formal model. Even taken at face value, subexponential is not polynomial, gives no native R_mix341 refutation translation, and does not supply B3.

No repository claim was promoted beyond its stated model. No claimed P-versus-NP solution was found or inferred.

## ITERATE: exact encoding, accepted proof, and theorem

For a connected simple cubic graph $G=(V,E)$ with $h=|V|$, assign one Boolean variable $x_e$ per edge, so $|E|=3h/2$. Choose vertex charges $c_v\in\{0,1\}$ with odd total parity. At each vertex, the four width-three clauses forbid exactly the four incident-edge assignments whose parity differs from $c_v$. Thus the source $B_h$ is an exact signed strict 3-CNF with $3h/2$ variables, $4h$ clauses, and canonical indexed length $N=\Theta(h\log h)$. Connectedness plus odd total charge proves UNSAT; the published deletion witnesses prove every one of the $4h$ clauses individually indispensable on the bridgeless fixtures.

The new executable `experiments/review/lspv5_427_completion_robust_tseitin_audit.py` independently reconstructs a balanced two-level AND3 tree for each vertex and a balanced XOR tree across vertices, then submits the complete packet to the recovered `/341` verifier. Fresh run: 30,714 checks PASS; all seven malformed controls and five corrupted-proof controls reject. Work remains $4h-1$. Ideal depth changes K4 $6\to4$, K3,3 $8\to5$, cube $10\to5$, Petersen $12\to6$, prism6 $14\to6$, prism16 $34\to7$. The bridged fixture has a legal 39-node proof but only 36 essential clauses, so no exact-minimum claim is made for it.

**Completion-robust theorem (restricted assumptions explicit).** Let $R'$ be any sound, source-explicit, acyclic proof calculus in which original clauses are free, every paid node costs one, every paid node cites at most two antecedents, and the accepted SOURCE/AND3/XOR derivations remain legal. For a bridgeless $B_h$, every sound contradiction ancestry must include all $4h$ indispensable source clauses: omitting clause $C$ would yield the same contradiction from satisfiable $B_h\setminus\{C\}$. Any connected acyclic ancestry with $4h$ source leaves and binary paid nodes has at least $4h-1$ paid nodes. The accepted balanced core proof has exactly $4h-1$. Therefore

$$W_{R'}(B_h)=4h-1,$$

and its minimum possible ideal binary-fanin depth is $\lceil\log_2(4h)\rceil$. Adding legal binary rules, branching encodings, auxiliary definitions, or shared lemmas cannot make this family hard; it can only supply alternative proofs, and the ancestry lower bound prevents a sub-$4h-1$ proof under the stated source-explicit/unit/binary assumptions.

This is [P2-B12]'s general identity plus [P2-L3-491]'s historical accepted-subgrammar evidence, now joined explicitly. It is not authentication of the missing RES/DEF/LOCAL-CONVERT/branch byte grammar [P2-D1]. It falsifies only a proposed same-source polynomial-output normalization into a target (such as ordinary Resolution on expander Tseitin) that has superpolynomial target proof size: the accepted linear native proof cannot map with polynomial output size to such a target proof. It does not preclude exponential translation, a different source encoding, or a different hard family. Hence [P2-C3] remains OPEN rather than proved or refuted globally.

## Family / theorem / encoding / known-method / remaining-transfer ledger

| Family | Exact encoding and size | Established theorem/model | Legal shortcut/control used | Remaining transfer |
|---|---|---|---|---|
| Cubic odd Tseitin $B_h$ | one edge bit; four signed strict 3-clauses per vertex; $3h/2$ vars, $4h$ clauses, $N=\Theta(h\log h)$ | ordinary Resolution hard on suitable expanders; exact $4h-1$ only in source-explicit unit-paid binary-parent calculus | accepted AND3 per vertex + GF(2) XOR; balanced shared DAG | family excluded from [P2-B1]; full grammar [P2-D1] still OPEN |
| Haken PHP | standard wide pigeon clauses + binary collision clauses; not native 3-CNF | $2^{\Omega(n)}$ ordinary Resolution | Cook polynomial Extended Resolution | any 3-CNF reduction needs proved lower-bound preservation; full mixed shortcut audit OPEN |
| Pang one-hot cubic Tseitin | 3 edge-state vars and 7 clauses per vertex; $7h$ clauses | conditional on Pang v2, exponential opposite-characteristic $\operatorname{Res}(PC_1/\mathbb F_p)$ | LSPV-1/496 derives bit clauses with linear prefix; native GF(2) still short on bit source | no full R_mix341 lower bound; source encodings not identical |
| Random proper 3-CNF | $n$ variables, $m=cn$ proper signed ternary clauses | exponential ordinary Resolution w.h.p. in published model | RES/DEF/algebra/branch controls remain legal | need invariant covering every native rule; current candidate direction |

Certified UNSAT, proof-size hardness in a named restricted system, and empirical solver difficulty are kept distinct throughout.

## Resource ledger

The logical certificate has $4h-1$ paid nodes and depth $\lceil\log_2(4h)\rceil$ on the six bridgeless fixtures. The replay parses 197,514 source bytes, reconstructs and serializes a balanced packet, invokes the exact preserved JavaScript verifier, and records 30,714 checks. Construction and verification are linear in explicit packet size apart from JSON/string overhead; output evidence is explicit. The execution retains source packet, rebuilt packet, parsed objects and verifier output simultaneously, so this is an offline validation run, not an FLMV same-machine space claim. Search, repository reads, failed first invocation without the required packet argument, serialization, subprocess startup, and output capture were charged as actual workflow phases; none enters ideal $W_R$.

## Revision and status

F1--F3 were not triggered. F4 **was** triggered only partly: [P2-B12] already proves the abstract work/span theorem and [P2-L3-491] already records accepted historical checker semantics, so neither is re-claimed. The material new tracker fact is their explicit completion-robust synthesis plus the current independently executable replay and exact artifact hashes. The revised claim is therefore a family exclusion/normalization countercontrol, not a new lower bound.

Actual advance: accepted native-core evidence is now attached to a quantified theorem that survives every sound source-explicit unit-paid binary completion retaining the core derivations. Precise remaining gap: an established nonaffine 3-CNF family with a lower-bound invariant covering **all** historical native shortcuts, plus the independent noncircular same-calculus B3 arrow. [P2-B1], [P2-B2], [P2-D1], and global [P2-C3] remain OPEN. **P versus NP remains OPEN.**

