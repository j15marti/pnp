# LSPV-2 BRAUN-GF2-NATIVE-BACKTRANSFER369, five-role handoff

**November 3, 2026, 12:12 PST. Status: scoped compiler PROVED/EXACT (external specialist review pending), bit-PHP lower bound CONDITIONAL on Braun 2026 preprint, finite checks COMPUTATIONAL, full mixed worst-case bound/B1/B2/B3/P vs NP OPEN.** No tasks, enabled states, schedules or model weights changed.

## Established theorem and same-source translation

Original bit PHP F_ell for n=2^ell holes, n+1 pigeons and ell>=32 has (n+1)ell Boolean variables, m=n*binom(n+1,2) width-2ell source clauses, ASCII DIMACS encoded bits N=Theta(n^3 ell^2). Braun, arXiv:2609.23015 (September 19, 2026), claims every unrestricted shared-DAG Res(XOR) proof (including axiom lines) has S>exp(n/(32768 ell^2)); the preprint has Lean formalization but was not locally replayed or independently academically reviewed.

New locally opaque/wire-defined backward compiler: For any source-authenticated Rmix341 refutation using q distinct paid nodes, with b original variables used as direct inputs to paid conservative two-input DEF gates, and with every AND3/LOCAL-CONVERT output an extensional <=3-original-variable Boolean factor (no exposed uncharged internal names), there exists a Res(XOR) refutation of the SAME original CNF using

    S <= 2^b (2m + 64q + 2)

total proof lines. All RES, local factors, GF2/XOR rows of ARBITRARY support, paid wire definitions, shared DAGs, and adaptive choice remain permitted within the named grammar. No new inference rule. The proof assigns every original DEF input and evaluates all gate outputs, compiles local truth-table factors by constant-size Res(XOR) weakening/cuts, keeps every wide XOR addition native in two Res(XOR) nodes, lifts restricted proofs, glues branch blockers. Encoded payload bits, discovery, checking and machine space remain separate.

Combining with Braun (CONDITIONAL on that external theorem):

    b + log2(2m+64q+2) > n/(32768 ell^2 ln(2)).

Thus for any epsilon>0, proofs with b<=(1-epsilon)n/(32768 ell^2 ln(2)) must have q=exp(Omega_epsilon(n/ell^2)); in particular the DEF-FREE (but arbitrary global XOR) fragment is conditionally superpolynomial. This is NOT a full Rmix341 lower bound. Known polynomial bit-PHP ER2 proofs are compatible because they may require many original definition inputs. The crucial improvement over the prior LSPV-2 365/366 Resolution compiler is that global GF(2) inference width contributes ZERO exponential tax; only DEF exposure remains. This matches the richer published lower-bound proof model rather than falsely treating XOR as ordinary Resolution.

## Proven scope and falsifiers

F1 odd/even Tseitin shortcuts: no restricted lower bound from ordinary Resolution only; independently checked short Res(XOR) refutations on odd K4 and K3,3. F2 ER2 polynomial bit-PHP: no contradiction, 2^b tax explicitly charged. F3 named uncharged LOCAL-CONVERT internal gates: outside theorem, original grammar ambiguity OPEN. F4 malformed, wrong pivot and semantically invalid weakening: hostile finite checker rejection. If an alternative LOCAL-CONVERT path can cheaply expose private gate names or an original-variable-independent source oracle, the compiler is not justified for that path.

Python generator and independent Node.js checker completed 2,513 assertions; K4 16 original clauses, 67 paid Res(XOR) nodes; K3,3 24 original clauses, 101 paid; even-charge 8 and 16 satisfying models; original bitPHP holes=2,4 both UNSAT; six corruptions rejected. Local checker nvars<=12 and does not validate Braun or shortest-proof optimality. Expanded local proof JSON 14,512 bytes SHA256 86b99f4a9da13def42b5c4ac90b8a6182d64561e55e07db945059aaf48ddf046. Public raw JSON serializes equivalent records without trailing newline (14,511 bytes).

## Corpus reviewed, prior work, Grok and Claude

User-approved five-role refocus at commit 4e29ed7 / blob 033b54b, issue #3, AGENTS.md, CODEX.md, skill, original Rmix341 LSPV-2 341, prior 365/366/368, LSPV-3 BRAUN-BACKTRANSLATION369 (blob 1cd0e44902535cb460444b718bbcfb04361d47bd) and current REFEREE317/319 were read. Prior lower-bound-source nonprojection and scope compilers are adopted, not claimed as new. Grok actual latest path `GROKPROOF/2026-11-03_1912_PROGRESS.md` at blob dbec4959d96f19554061511cd240745f398272ec was read; its all-input FLMV contraction remains OPEN. Claude actual `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67 and older `2026-09-30_CLAUDE-0266_review.tex` blob 694c1c8169d9a193397b94e6ee572c476e639a94 were read. Claude TPORT concerns restricted alternation-trading, not full SAT computation. github.com/openai Res(XOR) search surfaced unrelated sheaf Resolution.lean, not reused. Primary literature Braun (2026), Itsykson-Sokolov (2020), Cook (1976), and Buss-Turan (1988).

## Exact role-owned outbox

- `research/agents/lspv-2/2026-11-03_1212_LSPV-2_BRAUN_GF2_NATIVE_BACKTRANSFER369.tex`
- `experiments/arc/lspv2_369_braun_gf2_producer.py`
- `experiments/arc/lspv2_369_braun_gf2_verify.js`
- `results/raw/arc/2026-11-03_1212_LSPV2_BRAUN_GF2_NATIVE_BACKTRANSFER369_full.json`
- `research/coordination/2026-11-03_1212_LSPV2_BRAUN_GF2_NATIVE_BACKTRANSFER369_FIVE_ROLE_HANDOFF.md`

The expanded local PDF, full producer, independently implemented verifier and SHA256 manifest are in the reproducibility archive. The restricted symbolic proof is not a numerical FLMV contradiction. All-phase memory: s'<=max{rho,eta,lambda,lambda*s}, including local allocate/free phases.

**Next exact gap:** audit every full Rmix341 LOCAL-CONVERT use and all conservative definitions to determine whether the native Res(XOR) compiler applies without restrictions; independently test proof line-count translation on nontrivial nested paid-DEF + global XOR examples. A valid unrestricted lower-bound transfer and B3 remain OPEN.