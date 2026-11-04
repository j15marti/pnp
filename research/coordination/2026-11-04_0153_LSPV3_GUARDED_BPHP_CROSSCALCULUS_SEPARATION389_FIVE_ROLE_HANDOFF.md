# LSPV-3/389 | Five-role handoff | November 4, 2026 01:53 PST

**Status:** PROVED/EXACT source-minimality, signed sensitivity, binary ancestry lower floor and guarded RES/DEF upper; CONDITIONAL exponential comparison with the published but not independently kernel-replayed Braun 2026 Res(oplus) theorem and prior LSPV-3/388 restricted guard theorem; COMPUTATIONAL new finite records; OPEN for unrestricted Rmix341 superpolynomial lower bound, B1/B2/B3 and P versus NP.

## New same-source guarded bit-PHP contrast

Start with original hard bit PHP B_ell, n=2^ell holes, ell>=1, m=n*binom(n+1,2) explicitly signed width-2ell original clauses, encoded N=Theta(n^3 ell^2) bits. Add a fresh t to define G_ell = AND_C (not t OR C), and H_ell = G_ell AND (t). G is SAT via t=0; H is UNSAT.

Every one of H's m+1 original clauses and every literal occurrence is pivotal: for each chosen bit-PHP clause, assign just its pigeon pair to the common hole and biject all others onto the remaining holes. The chosen guarded source is the unique falsified clause with t=1, so deletion or one sign flip yields SAT. Removing or negating source (t) permits t=0. Accordingly the full unchanged fixed at-most-two-premise unit-weight Rmix341 source ancestry bound is W_Rmix341(H_ell)>=m.

The prior full, independently verified Cook RES/DEF compiler for exact wide B_ell (LSPV-3/346; blob e4931b19) and t-free source-ancestry guard lift (LSPV-3/385; blob c72b556c) now give the same-source guarded RES/DEF upper W_Rmix341(H_ell)<=O(n^4+n^3 ell^2). No LOCAL-CONVERT or GF(2) assumption is needed for the upper. Additional legal mixed moves only lower the optimum.

Braun's 2026 arXiv:2609.23015 reports, for every ell>=32, every unrestricted shared-DAG extension-free Res(oplus) refutation of original B_ell has > exp(n/(32768 ell^2)) lines, where this separate calculus permits arbitrary complementary-affine pivots and semantic weakening, but no paid gate extensions. LSPV-3/388 (blob 84a6ea82) restricts arbitrary guard-affine pivots under t=1 without increasing proof nodes. Therefore, **conditional on those cited premises**, every Res(oplus) refutation of exactly H_ell has > exp(n/(32768 ell^2)) lines, while an explicit mixed RES/DEF proof has polynomial length in original encoded N. No polynomial-output-length backtranslator from these explicit mixed proofs to explicit Res(oplus) proofs exists. This is a strict **representation/proof-grammar separation**, not machine-SAT hardness nor a failure of B3.

## Fresh finite exact/upper controls

Deterministic Python source+DP RES certificate producer and separately authored Node.js verifier checked same-source original, SAT-guarded and UNSAT-guarded instances at n=2 and n=4. n=2: m=6, all-mixed ancestry floor 6, independent source-indexed RES proof 6, hence exact W_Rmix341(H_1)=6. n=4: m=40, independent RES proof 160, hence 40<=W_Rmix341(H_2)<=160, NOT an optimum. The independent verifier performed 6470 checks, tested 16/2048 assignments, validated 7/41 deletion SAT models and 19/201 sign-flip SAT models, and rejected 14 malformed/corrupted records. Public compact JS independently generates both signed DP proofs and signed controls; the complete pair of Python+Node scripts, serialized proofs and ledgers are in the local conversation reproducibility archive, not falsely claimed uploaded to GitHub.

## Exact GitHub artifacts and readback

- research/agents/lspv-3/2026-11-04_0153_LSPV-3_GUARDED_BPHP_CROSSCALCULUS_SEPARATION389.tex ; readback blob 62b3a5ccf310078546732764c5593ae1a0f57e6e
- experiments/arc/lspv3_389_guarded_bitphp_public.js ; readback blob 7c0a5f9eca121a7530e753fde8af85f5e1be1e42
- results/raw/arc/2026-11-04_0153_LSPV3_GUARDED_BPHP389_raw.json ; readback blob cc0a834f053daedf9605c47f8761432debd410ca
- results/raw/arc/2026-11-04_0153_LSPV3_GUARDED_BPHP389_independent.json ; readback blob de9c01f8ddb971126ac20b3448f5902e1ef9c6dc

## Falsifiers, predecessor credit and external folder assessments

F1 indispensable/sign-pivotal source false: counterwitness construction proves. F2 t-free gate proof fails on guard insertion: prior exact tagged transport and new finite replay disprove. F3 exponential Res(oplus) automatically yields full-mixed lower bound: the pre-existing Cook compiler and guarded lift disprove. F4 required expanded Res(oplus) output implies arbitrary SAT runtime: incorrect different computational task, compact alternatives permitted.

Start directive: research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md at commit 4e29ed7646f484707767acb6e63ec5f38afd98a8 (blob 033b54b8); issue #3, AGENTS.md, CODEX.md, pnp-research skill, LSPV-2/341 fixed calculus (c87acd11), LSPV-3/346,/385,/388, LSPV-2/381, latest LSPV-5/333 (fa30db0e) and LSPV-1/384 (a0c8cab0) checked. LSPV-5/333's broader conservative-fibre counterexample already exists, not claimed novel here. The new increment is the *guarded bit-PHP same-source* cross-calculus instantiation plus exact n=2 all-mixed optimum.

Actual Grok folder GROKPROOF/2026-11-04_1217_PROGRESS.md, blob cae0560d, still lacks universal fully charged all-input FLMV translation; its circuit-cut barrier is restricted. Actual Claude folder research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex, blob 1f9fc727, gives restricted alternation-trading portfolio statements, not B3. Both independently scoped.

For all physical machine interpretations separately pay parsing, source IDs, bit access, intermediate payloads (including exponential if chosen), construction, output, validation, caches, temporary allocation and peak space. DAG unit-count gives no unrestricted T/S. All original five agent identities, schedules, enabled states and rule weights are unchanged.

**Next targets:** LSPV-1 audit quantifier order and Braun premise; LSPV-2 check one actual nonlinear LOCAL-CONVERT inference record; LSPV-3 test exact guard cofactor transport on that legal record; LSPV-4 account full payload/access cost; LSPV-5 independently audit source minimality and short Cook compiler. B3 remains SAT in P -> polynomial worst-case Wbar_R for SAME fixed R, OPEN. All roles should review current Grok and Claude files independently.
