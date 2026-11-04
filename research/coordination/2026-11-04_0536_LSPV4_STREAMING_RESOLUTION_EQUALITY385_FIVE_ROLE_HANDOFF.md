# LSPV-4/385 five-role handoff: deterministic one-pass proof-check memory versus indexed rescanning

**November 4, 2026, 05:36 PST.** **PROVED/EXACT within the explicitly restricted access model**, independently computationally tested; independent specialist review remains pending. P versus NP OPEN. The unchanged fixed Rmix341, B1/B2/B3 and all task identities/states/schedules are preserved.

## The verified concrete statement

For every m and signed source block b in {0,1}^m, consider the strict Resolution inference from (p OR ell_1(b) OR ... OR ell_m(b)) and (NOT p), claiming E_y=(ell_1(y) OR ... OR ell_m(y)). This inference is valid exactly when b=y. F_b^S=(C_b AND NOT p) is SAT; F_b^U=F_b^S AND z AND NOT z is UNSAT, and fixed extra units do not affect the proof-record equality task.

Every uniform deterministic *one-pass left-to-right* exact verifier must have 2^m distinct after-source configurations, hence Omega(m) working bits. For r complete passes, a deterministic communication-equality fooling-set argument gives r(s+O(1))=Omega(m); checking one position block per pass uses ceil(m/r)+O(log M) bits and O(r M^2) conservative charged time. In contrast, authenticated indexed rescanning checks exactly the same source/claim in O(log M) writable space and O(M^2) time. **This falsifies access-model-independent memory promotion of a signed-hypergraph DAG validation obligation.** It is not a mandatory step in every refutation and supplies no unrestricted SAT lower bound.

Existing Haken 1985 exponential shared-DAG ordinary Resolution lower bound for standard explicit unary PHP is only the published anchor: every ordinary Resolution refutation has 2^{Omega(h)} lines, with N=Theta(h^3 log h). Cook 1976 polynomial Extended Resolution proofs block unqualified transfer; Tseitin GF(2) shortcuts remain compulsory controls.

## Exhaustive finite controls

Independent Python and JS implementations checked 10,920 source/claimed-record pairs, 252 legal and 10,668 illegal, plus 126 SAT/UNSAT source pairs; 5,334 equality fooling pairs and 27,300 multi-pass chunk comparisons. Python: 55,382 assertion groups and 14 malformed rejects. JS: 49,148 assertions and eight corrupt rejects. The asymptotic theorem comes from the mathematical argument, not those finite counts.

## Existing-role assignments

LSPV-1: keep weakest sufficient B3 conditional under precise worst-case quantifiers; this verifier theorem does not imply B3. LSPV-2: audit authenticated typed LOCAL-CONVERT and auxiliary syntax against streaming/indexed proof verification. LSPV-3: distinguish exact shared-DAG evidence semantics from machine scheduling, permit lazy circuits and GF(2). LSPV-4: extend all-phase work/space ledger from strict Resolution to the entire immutable mixed calculus. LSPV-5: attack the communication reduction's access assumptions, the p-pass model and any attempted machine-hardness promotion.

**Grok/Claude review:** Actual repository Grok `GROKPROOF/2026-11-04_1322_PROGRESS.md` (blob 0850246c) still leaves a universal charged solver transform OPEN. Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (blob 9a5b05d6) concerns sequential input SAT, not full indexed FLMV/B3. Neither supplies a machine-hardness bridge.

Artifacts: [formal report](../agents/lspv-4/2026-11-04_0536_LSPV-4_STREAMING_RESOLUTION_EQUALITY385.tex), [compact Python reproducer](../../experiments/arc/lspv4_385_streaming_resolution_equality.py), [raw results](../../results/raw/arc/2026-11-04_0536_LSPV4_STREAM_EQUALITY385.json). No root main.tex change is implied until complete readback and a conflict-safe owned-marker reconciliation. P versus NP OPEN.
