# LSPV-2/415: Four-paid-node SAT-to-contradiction counterexample in proposed CANON1 checker

**November 5, 2026, 04:12 PST. Role: LSPV-2 SAT-Circuit Reduction Builder.**  
**Status: FALSIFIED/RETIRED for the unchecked soundness assertion of `Rmix341-CANON1` in REFEREE360. PROVED/EXACT by inspection of its published executable rule branches and an explicit Boolean countermodel; independently checked finite replay is COMPUTATIONAL.** The unchanged original semantic `R_mix341` is **not** refuted or modified. B1/B2/B3 and P versus NP remain **OPEN**.

## IDEA, hypothesis and falsifiers (before searches)

REFEREE360 newly proposed a fixed-facet byte grammar. The falsifiable hypothesis was: if a paid two-input DEF gate uses the **same antecedent variable twice**, the four fixed defining clauses may contain **both signs of the same RES pivot**, and its checker may silently erase both signs instead of checking one complement on each opposite parent. Prediction: a satisfiable authentic source can be falsely certified UNSAT in four paid nodes. Additional falsifiers were (i) fresh distinct DEF inputs, (ii) repairing premise clause normalization while preserving legal repeated-input gates, and (iii) exact native rule authorization as distinct from proposed CANON1 bytes.

## SEARCH (actual accesses, not just snippets)

Read first governing five-role handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`; issue #3 through REFEREE360 (03:48 PST), `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`; original `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11...`), /384 grammar addendum, LSPV-2/414 plus SAT-miter addendum, LSPV-3/420, LSPV-4/411, and full REFEREE360 report and its checker `experiments/arc/lspv5_360/rmix341_canon1_referee360.py` (blob `67ecd99a2071ef4ffd5552655a90cb91fcb08fb9`). Also read actual `GROKPROOF/2026-11-05_1218_PROGRESS.md` (blob `d3183283`) and Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (blob `9a5b05d6`) and `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (blob `1f9fc727`). Neither provides the omitted DEF-premise tautology invariant.

Indexed web queries: `Cook Reckhow 1979 relative efficiency propositional proof systems definition polynomial verifier`, `resolution tautological clauses cannot resolve tautological premise elimination both literals pivot proof checker`, `Haken 1985 intractability of resolution pigeonhole principle extended resolution Cook 1976`, `certifying parity reasoning efficiently pseudo Boolean Gocht Nordstrom paper 2021`. Read primary Cambridge Cook--Reckhow, publisher Haken 1985, and AAAI Gocht--Nordström entries. Direct Google-branded search was unavailable; used general indexed web instead. Authenticated GitHub search query `ExecCNFNodeSearchCosts` in `github.com/openai` found `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean`; read its complete 7,306-character blob `1ced21f44ad49370d1b812e862c03c3a91d7f836`. That Lean program charges concrete traces and storage but has no CANON1 proof checker/repair or B3 p-simulation.

## ITERATE: explicit accepted invalid certificate

Take the **SAT** original source `{"nvars":1,"clauses":[[1]]}`, i.e. `F=(x)`. A valid model is `x=1`. Pay one fresh DEF `z=f(x,x)` with `f(a,b)=a` and 4-bit truth table `[0,1,0,1]`. The unique conservative extension is `z=x=1`.

The proposed four fixed DEF facets, indexed exactly as the checker generates them, are:
```
facet 0: [ 1, 1,-2]      (x OR x OR not z)
facet 1: [ 1,-1,-2]      (x OR not x OR not z)  TAUTOLOGY
facet 2: [ 1,-1, 2]      (x OR not x OR z)      TAUTOLOGY
facet 3: [-1,-1, 2]      (not x OR not x OR z)
```
The purported proof DAG is:
```
node 0 DEF  var=2 inputs=[1,1] truth=[0,1,0,1]
node 1 RES  facet=(node 0, facet 1), source=(x), pivot=1 => (-z)
node 2 RES  facet=(node 0, facet 2), source=(x), pivot=1 => (z)
node 3 RES  node1 (-z), node2 (z), pivot=2 => EMPTY CLAUSE
final node 3, empty clause
```
All four nodes have unit weight. The full exact `Rmix341-CANON1` JSON witness, including original-source SHA-256 `99dc3cc7aaa4c4237ca3167e6f3d6f2c8de57df6c7cc31de2450e328029a422a`, is 615 canonical ASCII bytes. The original source object uses 27 canonical ASCII bytes. Satisfying assignment `x=z=1` makes derived `(-z)` **false** even though its facet and original source clause are true, exposing the first unsound step.

The published Python checker **permits** this without any speculative operation:
- `def_facets` (lines 132-140) constructs the tautological facets with repeated inputs, then `Checker.run` lines 281-291 stores each as a clause without `norm_clause`.
- DEF inputs (lines 284-288) need only be earlier positive IDs; no distinctness test.
- RES (lines 210-223) accepts complementary pivot **presence somewhere across parents**, deletes **all occurrences of abs(pivot)** from both clauses, and only checks the resulting clause for tautology. It never requires non-tautological parent facets. All declared outputs `[-2]`, `[2]`, `[]` match its computed `want`; the final empty clause passes lines 295-298.
- The two RES parent references are the newly authorized exact `{"node":0,"view":"clause","facet":1}` and `facet:2`; no free LOCAL wire/export, GF(2) semantic oracle, or uncharged gate was used.

**This is a concrete accepted-byte counterexample to the REFEREE360 proposed checker, not a legal derivation in sound mathematical Resolution.** Sound Resolution from a tautological parent cannot erase both its pivot polarities by treating them as one resolvable literal. Therefore the REFEREE360 unconditional checker-soundness claim is false **for the published implementation**, pending a patch.

## Repair preserving the semantic paid-DEF calculus

For each DEF, normalize its four truth-table forbidding clauses *as relations*: collapse duplicate literals; if both signs of a variable occur in a generated facet, it is a tautology and **must not be exported as a selectable clause premise**. Equivalently validate every RES parent with the same clause invariant as source/resolvent clauses. A conservative, alternative syntactic restriction is `inputs[0]!=inputs[1]`, but this unnecessarily excludes otherwise valid repeated-input gates and is not a faithful semantic normalization. For the witness, retain only the two consistent rows `(x OR not z)`, `(not x OR z)`; they exactly encode `z=x`. A new frozen byte grammar needs to say how omitted facet indices are treated. Proof cost of this DEF remains one. The unsound trace is then rejected at node 1.

This **repairs the specific pivot-tautology defect only**; the entire CANON1 implementation still requires independent full-rule fuzzing, negative controls and a formal checker audit. The original `/341` does not prescribe a unique byte parser, so the repaired CANON1 is a proposed completion, not an authoritative recovered historical syntax.

## Reproducible computational challenge

A separate no-import JavaScript producer reimplements **only** the identified published DEF/RES code branches and generates the exact JSON proof, checking acceptance under the vulnerable algorithm and rejection after the canonical-parent repair. A separately written Python semantic verifier evaluates all four (x,z) assignments, verifies conservativity and demonstrates the nonentailed intermediate clause. It exhaustively tests all **16** two-input gate truth tables when inputs are aliased, finding **8** tables where inconsistent off-diagonal rows allow opposite false unit clauses, and all 16 functions with **distinct** inputs yield valid three-variable facets. Python: **99** independent semantic assertions. JS: all assertions pass. These are narrow faithful branch/semantic replays, **not** execution of the original 473-line REFEREE360 Python file, which could not be downloaded to the container through direct raw GitHub DNS. The connector did fetch and expose the exact published source and blob, allowing the static code-path conclusion.

## Cost/quantifier status and B3

Fixed original semantic `R_mix341` still has original-free source clauses, charged binary RES/AND3/GF(2)/LOCAL/DEF nodes and conservative fresh definitions; no semantic change has been made. For this hostile proposed-CANON1 witness, logical **q=4**, semantic source `N=27` canonical JSON bytes (distinct from DIMACS N), supplied canonical proof `E=615` bytes; full acquisition, hash, parse, index/reference, truth-table, output, checking, storage and temporary buffers are physical costs distinct from q. The forged proof is tiny; its defect is **logical soundness**, not a resource gap. The output file read and checker use at least Omega(E) bit/byte acquisition in an explicit stream, and buffered peak memory is O(E); no measured machine time/space assertion is made.

The original hard-family control remains Haken's exponential **ordinary Resolution** pigeonhole lower bound (polynomial-size usual encodings, all ordinary refutations, proof length); Cook's Extended Resolution PHP and /341 affine odd-Tseitin proof are shortcut controls. The broken CANON1 proof system cannot be used to infer `Wbar_Rmix341` anything. No inference from accepted certificates to UNSAT is permitted until this and any other soundness bugs are repaired. Even once repaired, the noncircular same-fixed-calculus B3 implication `SAT in P => polynomial Wbar_Rmix341` still lacks a uniform p-simulation/reflection compiler. B1, B2, B3, any mixed superpolynomial minimum, and P versus NP remain **OPEN**.

**Next shortest decisive step:** LSPV-5 patch CANON1 clause normalization and add this exact SAT regression, independent red-team retest; LSPV-2 audit **all** normalized DEF facet-to-RES consumers and then attempt a real native consumer-preserving GF(2)/AND3/LOCAL translation. Do not alter historical /341 calculus or any other role's manuscript region. Repository root `main.tex` returned an existing SHA but an empty body through authenticated retrieval; no unsafe overwrite performed.

### References
[1] Cook & Reckhow, JSL 44 (1979), 36-50, https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/abs/relative-efficiency-of-propositional-proof-systems/218048250981F835B4B2A4080205A0BA

[2] Haken, *The Intractability of Resolution*, TCS 39 (1985), 297-308, DOI 10.1016/0304-3975(85)90144-6.

[3] Gocht & Nordström, *Certifying Parity Reasoning Efficiently Using Pseudo-Boolean Proofs*, AAAI 35 (2021), 3768-3777, DOI 10.1609/aaai.v35i5.16494.

% LSPV-2 REPORT::415::2026-11-05 04:12 PST
% END_OF_VERIFIED_REPORT::LSPV-2::415
