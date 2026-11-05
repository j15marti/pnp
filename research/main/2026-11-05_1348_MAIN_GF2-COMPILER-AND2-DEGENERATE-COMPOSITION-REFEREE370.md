<!-- LSPV-5 REPORT::REFEREE370::2026-11-05T13:48:00-08:00 -->
# LSPV-5 REFEREE370: strict GF(2) compiler confirmed; degenerate signed-AND2 elimination is repairable but native facet bytes remain unspecified

**November 5, 2026, 13:48 PST. Route B primary.** **PROVED/EXACT, RESTRICTED:** LSPV-1/425's strict GF(2)-row compiler is correct, including zero-variable rows, and the earlier `/371` signed-AND2 extension-elimination theorem can be extended without a worse asymptotic factor to equal or complementary signed inputs **at the semantic clause level**. **COMPUTATIONAL:** independent Python and Node implementations exhaust the finite controls below. **OPEN:** whether such degenerate gates are legal accepted historical `R_mix341` bytes, because `/341` does not specify positional repeated/tautological defining facets; the full native LOCAL-CONVERT/exported-wire/AND3/GF(2)/DEF normalizer, any superpolynomial full-mixed minimum, B1/B2/B3, and P versus NP.

No historical rule, weight, task, schedule, enabled state, or other role's manuscript region is changed.

## IDEA fixed before SEARCH

The initial hypothesis was that the new LSPV-1/425 row compiler might fail because its output blocker tree uses non-strict weakening or creates nonpivot complementary literals. The current peer report already stated a sharper $2^{|S\cap T|}-1$ construction, so the red-team target was revised before implementation:

> **Revised hypothesis.** `/371`'s definition-elimination step does not actually require its two signed AND inputs to name distinct literals. If the exact three-facet AND relation is interpreted extensionally, equal inputs $a=b$ and complementary inputs $a=\neg b$ can be eliminated with no larger local Resolution overhead. The prediction is falsified by any legal transformed inference that requires weakening, any nonpivot complementary pair, any surviving defining facet, or any authoritative native byte rule rejecting the required normalized facet representation.

Four falsifiers were fixed:

1. an assignment falsifying the XOR-sum row falsifies both or neither parent row;
2. an intersection-tree merge creates a nonpivot complement or needs a clause not derivable by strict Resolution;
3. equal/complementary signed AND inputs defeat the local `/371` substitution simulation;
4. semantic elimination is incorrectly promoted to an accepted-byte theorem, full-native normalization, or B3.

Falsifiers 1--3 did not occur. Falsifier 4 remains decisive: the historical serialization gap blocks promotion.

## SEARCH record and established-family ledger

### Authenticated project state

Read the governing five-role handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` (current blob `c3889a3e...`), issue #3 through LSPV-4/422, `AGENTS.md`, `CODEX.md`, the complete repository `pnp-research` protocol and red-team mode, and the following load-bearing artifacts:

- historical calculus: `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`;
- distinct-input extension eliminator: `research/agents/lspv-1/2026-11-03_1306_LSPV-1_HAKEN_EXTENSION_BUDGET371.tex`, blob `816da1eb...`;
- strict row compiler: `research/agents/lspv-1/2026-11-05_1312_LSPV-1_GF2_STRICT_ROW_COMPILER425.md`, blob `7a1fcfe7...`;
- LSPV-3/430 graph-PHP essentiality and LSPV-4/421--422 as peer controls;
- actual Grok assessment `GROKPROOF/2026-11-05_1913_PROGRESS.md`, blob `8a004bf4...`;
- actual Claude assessment `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`, blob `79e4d4e7...`.

Grok correctly treats FRAT-XOR/checker work as certificate infrastructure, not a B3 theorem. The Claude ledger warns that statements equivalent to P versus NP are reformulations, not progress. Neither supplies the missing native facet grammar or reflection compiler.

The root `main.tex` fetch authenticated blob `1b8a7d9a...` but returned zero readable document characters. Whole-document reconciliation could not be done safely and root was not overwritten. The repository preflight script was not available in the scratch filesystem; its governing source and checklists were read from GitHub instead.

### Primary literature and queries

Indexed web queries included:

- `primary paper extended resolution extension rule Cook Reckhow proof systems substitution elimination definitions`;
- `primary paper resolution proofs closure under substitutions proof complexity`;
- `primary paper parity resolution Res XOR lower bounds Tseitin formulas`;
- `Urquhart 1987 hard examples resolution Tseitin expander JACM primary`;
- `Ben-Sasson Wigderson short proofs are narrow resolution Tseitin expander primary PDF`;
- `Cook 1976 polynomial extended resolution pigeonhole principle primary`.

Direct Google-branded interactive search was unavailable; indexed web search was used and this is not described as a direct Google search. Material sources read or checked were Cook--Reckhow's proof-system paper, Haken's 1985 Resolution lower bound, Urquhart's 1987 expander/Tseitin construction, Ben-Sasson--Wigderson's 2001 width-size paper, Cook's 1976 ER PHP shortcut, and the current Res($\oplus$) literature. Exact links:

- Cook--Reckhow, *The Relative Efficiency of Propositional Proof Systems*: <https://www.cs.utoronto.ca/~sacook/homepage/cook_reckhow.pdf>
- Haken, *The Intractability of Resolution*: <https://doi.org/10.1016/0304-3975(85)90144-6>
- Urquhart, *Hard Examples for Resolution*: <https://dblp.uni-trier.de/rec/journals/jacm/Urquhart87.html>
- Ben-Sasson--Wigderson, *Short Proofs Are Narrow*: <https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf>
- Part--Tzameret, *Resolution over Linear Equations Modulo Two*: <https://doi.org/10.1016/j.apal.2019.102722>
- Efremenko--Garlík--Itsykson, *Lower Bounds for Regular Resolution over Parities*: <https://doi.org/10.1137/24M1696640>

The exact model qualification matters: Haken concerns ordinary Resolution PHP; Urquhart and Ben-Sasson--Wigderson give ordinary shared-DAG Resolution hardness for appropriate Tseitin/expander encodings; the cited Res($\oplus$) lower bounds are for named restricted systems such as regular Res($\oplus$), not arbitrary DAG-like Res($\oplus$), full `R_mix341`, or all SAT machines.

### Required repository review

Change-aware heads were unchanged from the previous run:

| Repository | Pinned head | Finding for this claim |
|---|---:|---|
| `konard/p-vs-np` | `ecedd2b45f1c...` | README/manifest explicitly limits results to stated formal models; targeted extension-substitution search returned none. |
| `blkph0x/p-vs-np-proof-research` | `7dedc73f758d...` | Contains scoped certificate and relaxation work; no fixed-`R_mix341` facet grammar or B3 bridge. |
| `meelgroup/frat-xor` | `18cd6bc17af1...` | Elaborates FRAT-XOR to XLRUP and a verified checker; relevant trust discipline, not the historical calculus or a minimum lower bound. |
| `peitl/short-proof` | `2c524cfceecf...` | Finds shortest proofs in declared Resolution systems; no mixed-rule normalizer. |
| `openai/math` | `4eaee8754825...` | Targeted proof-complexity query returned no relevant implementation; broad lexical hits were unrelated mathematics. |

Actual repository queries were `extended resolution substitution definition variable repeated inputs`, `extended resolution substitution definition variable checker`, `resolution proof extension variable substitution`, `xor resolution proof checker substitution`, and `resolution proof extension variable`. A no-result search was recorded as no result, not novelty evidence.

### Concise family/theorem/shortcut ledger

| Family | Exact 3-CNF encoding and size | Established theorem/model | Known legal shortcut in fixed mixed calculus | Remaining transfer |
|---|---|---|---|---|
| Odd cubic-expander Tseitin | One edge variable per edge; each degree-3 parity row becomes its four width-3 assignment blockers. For $h$ vertices: $3h/2$ variables, $4h$ clauses, explicit DIMACS $N=\Theta(h\log(h+2))$. | For appropriate constant-expanders, ordinary unrestricted shared-DAG Resolution requires $2^{\Omega(h)}$ size (Urquhart; also width-size treatment by Ben-Sasson--Wigderson). This is proof-system hardness only. | Historical `/341` admits the authenticated AND3/GF(2) proof with exactly $3h+(h-1)=4h-1$ paid nodes on bridgeless cubic instances. | This family is not hard for full `R_mix341`. `/425` yields only a restricted tradeoff when mixed shortcuts are bounded. No B3 follows. |
| PHP control | Haken's standard PHP CNF is not width-3; no lower-bound-preserving 3-CNF conversion is assumed here. | Exponential ordinary Resolution lower bound. | Cook's extension-variable proof is polynomial in ER. | Equisatisfiable 3-CNF conversion alone cannot transport Haken's lower bound. It remains a mandatory shortcut/control, not the selected exact 3-CNF family. |

## ITERATE I: exact strict GF(2) blocker lemma

Let rows be

$$
\bigoplus_{i\in S}x_i=b_S,
\qquad
\bigoplus_{i\in T}x_i=b_T.
$$

Write $I=S\cap T$, $D=S\triangle T$, and $t=|I|$. Fix an assignment $\tau$ to $D$ that falsifies the XOR-sum row on $D$. For every assignment $u$ to $I$, exactly one parent row is false: the XOR of the two parent truth values is the false output equation, and the $I$ variables cancel. Take the canonical blocking clause of that false parent row.

Pair the leaves that differ only on the last variable of $I$. The two false-parent identities swap, so the clauses contain complementary pivot literals. Their nonintersection supports are $S\setminus T$ and $T\setminus S$, hence no nonpivot complementary pair is created. One strict Resolution step eliminates the pivot. Continue over all $t$ intersection variables. The tree has exactly $2^t-1$ internal strict Resolution steps when $t>0$ and yields the target blocker; for $t=0$ the selected parent blocker is already a subclause. If a parent is the false zero-variable row, its empty blocker is a subclause of every target; a true zero-variable row contributes no blocker and the other row supplies the result.

Therefore every canonical output blocker has a strict Resolution subclause in at most $2^t-1$ steps. Summing over all output blockers gives the `/425` $2^{|S\cup T|}\le 2^{2b}$ bound. This proof is original-source compatible only when the parent representatives themselves retain their complete source ancestry, exactly as repaired in `/425`.

**Status:** PROVED/EXACT for the declared strict clause compiler. This neither lowers native GF(2) unit weights nor backtranslates an unrestricted proof with unbounded row width polynomially.

## ITERATE II: degenerate signed-AND2 input repair

Consider the three standard clauses for $z\leftrightarrow(a\land b)$, with signed literal inputs $a,b$. `/371` proves the global gate-elimination theorem when the two signed named inputs are distinct. Two omitted semantic cases are harmless:

### Equal inputs $a=b$

The definition is $z\leftrightarrow a$. Substitute $a$ for $z$ throughout the proof and normalize duplicate or tautological literals. A Resolution step on $z$ becomes one strict Resolution step on $a$; steps on any other pivot commute with substitution, except that a tautological image is discarded and the other premise is already a subclause of the transformed conclusion. The defining facets normalize to tautologies or duplicates. Thus each old line still has a strict subclause representative and no larger local factor is needed.

### Complementary inputs $a=\neg b$

The definition is $z\leftrightarrow 0$. A clause $z\lor C$ becomes $C$, while $\neg z\lor D$ becomes a tautology. For a $z$-pivot inference from these two clauses, $C$ itself is a subclause of the transformed target $C\lor D$, so no Resolution step is needed. Other pivots commute; if a premise becomes tautological, the surviving premise is already a subclause of the target. All three defining facets become tautologies.

Hence, **conditional on a grammar that accepts the exact extensional signed-AND2 relation with repeated/tautological positional facets**, the `/371` $64^d$ gate-elimination factor remains valid when inputs are equal or complementary. Shared-DAG reasoning is preserved: transform each paid definition owner and each derived node once, cache the representative by owner, and retain every original dependency reference. No branch-local conclusion is reused and no ASSUME/MERGE/case-discharge rule is added.

The condition is load-bearing. Historical `/341` says only “fresh variable as a two-input Boolean gate with all defining relations attributed to that same charged node.” It does not settle whether equal signed occurrences are legal, whether three positional facets must remain distinct records, or how tautological facets are encoded and referenced. The semantic repair is therefore **not** an authoritative accepted-byte trace and cannot authenticate native grammar by itself.

## Exact computation and hostile controls

Python independently exhausted every ordered pair of 64 GF(2) rows on five variables:

- 4,096 ordered row pairs;
- 15,552 output blockers;
- 18,062 constructed strict Resolution steps;
- maximum $t=5$ and maximum 31 steps, exactly $2^5-1$;
- 9,788 exact target blockers and 5,764 proper subclause outputs.

It then enumerated all 1,372 valid strict Resolution inference shapes over four variables and all 16 ordered signed-input pairs from $\{x_1,\neg x_1,x_2,\neg x_2\}$:

- 5,488 inferences for equal inputs, 5,488 for complementary inputs, 10,976 for distinct inputs;
- 19,432 transformed target-clause obligations across the two degenerate classes and 10,472 for distinct inputs;
- maximum local strict-Resolution depth 1 for each degenerate class and 2 for distinct inputs;
- all 48 positional definition-facet checks vanished as tautologies after substitution;
- corrupt nonpivot complement, self-input/output collision, and forged target controls were rejected.

The no-import Node verifier reimplemented both constructions and passed **473,809 assertions**, reproducing every principal count. The computation is exhaustive only for the declared finite domains; the proofs above supply the general restricted lemmas.

Resource ledger on the host run:

| Phase | Time | Peak/live memory observation | Logical proof meaning |
|---|---:|---:|---|
| Python producer/auditor | 0.622 s | `ru_maxrss` 10,880 KiB | Offline exhaustive diagnostic and artifact construction. |
| Independent Node replay | 0.405 s | sampled RSS 60,997,632 bytes | Offline independent replay, not native proof execution. |

Input parsing, enumeration, closure construction, hashing, output serialization and independent replay are charged physical work. There was no logical XOR-state diagnostic. These measurements do not convert unit proof nodes to Turing-machine steps, do not include proof search for arbitrary instances, and do not satisfy an FLMV same-machine transfer.

## Branching/shared-DAG and B3 audit

The user-requested AND/OR branching minimum does not alter the result. Historical `R_mix341` has no authenticated ASSUME/MERGE/discharge rule, so this run does not add one. Within its unbranched shared DAG, every transformed node is emitted once and references are shared; there is no double counting. If a future branch extension is proposed, both child contradictions are AND obligations and a lemma may cross branches only after its assumptions are legally discharged. Nothing in the present substitution proof supplies that discharge.

The B3 implication remains

$$
\mathrm{SAT}\in\mathrm P
\Longrightarrow
\exists C,k\;\forall N\quad \overline W_{R_{\mathrm{mix341}}}(N)\le C(N+1)^k.
$$

This run supplies no noncircular route from a polynomial decider to an original-source native refutation. Cook--Reckhow gives a polynomially bounded proof system under the relevant collapse, not polynomial boundedness of this preselected historical calculus. A verified checker establishes sound acceptance of supplied certificates, not their polynomial existence. Exponential Resolution backtranslation when $d$ or $b$ grows cannot support B3. Thus B1, B2, and B3 are all OPEN.

## Status and precise next gap

- **KNOWN THEOREM:** ordinary shared-DAG Resolution hardness of suitable exact width-3 odd Tseitin expander CNFs.
- **PROVED/EXACT, RESTRICTED:** the `/425` intersection compiler and the semantic equal/complementary-input extension of `/371`.
- **COMPUTATIONAL:** the two independent exhaustive finite audits and corrupt controls.
- **FALSIFIED/RETIRED:** “distinct signed inputs are mathematically necessary for the `/371` elimination bound.”
- **OPEN:** whether degenerate gates are legal historical accepted bytes; complete native rule-by-rule normalization; a superpolynomial minimum across every legal mixed rule; B1/B2/B3; P versus NP.

The next load-bearing test is not another formula. It is to recover or explicitly freeze the historical `DEF` facet/reference byte convention and then replay one equal-input and one complementary-input certificate through that authoritative checker. If the checker requires distinct non-tautological facets, the degenerate case is illegal rather than a normalization counterexample; if it accepts positional tautological facets, the semantic repair above should be instantiated as exact bytes and composed with `/425`.

## Reproducibility

- `experiments/arc/lspv5_370/gf2_and2_composition_referee370.py`
- `experiments/arc/lspv5_370/verify_gf2_and2_composition_referee370.mjs`
- `results/raw/arc/2026-11-05_1348_LSPV5_REFEREE370_raw.json`
- `results/raw/arc/2026-11-05_1348_LSPV5_REFEREE370_independent.json`

SHA-256 values at publication preparation:

```text
43c868c5aa7e6296d8f2f32f220a1c7f8de1571c2146efa6d7f5632bda474d1a  Python
32f0435d237781fabbf0a9732b40938aa9cc83e6a8335dc697e15a4f7e142d13  Node
b219d1dbc9824030024bbc32b3812ebea3ba1566ff48794853717a2defe3cd42  raw
350e27f21a3694d60a842898c8d0ebb0bb87658eea96808d7138eb1e8369bcc7  independent
```

P versus NP remains OPEN.
