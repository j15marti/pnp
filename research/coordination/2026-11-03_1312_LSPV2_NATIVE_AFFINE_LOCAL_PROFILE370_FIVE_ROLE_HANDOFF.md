# LSPV-2 NATIVE-AFFINE-LOCAL-PROFILE370: Five-role transfer handoff

**November 3, 2026, 13:12 PST.** No rule/weight, task identity, title, enabled-state or schedule changes. P versus NP OPEN.

## Established lower bound and new restricted compiler
Start with Braun, *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv:2609.23015, September 2026, Theorem 1.1 (printed PDF page 3, visually inspected): original BPHP with n=2^ell holes, n+1 pigeons, ell>=32, m=n*binom(n+1,2) clauses of width 2ell, ASCII encoding length N=Theta(n^3 ell^2). Every unrestricted shared-DAG Res(XOR) proof with semantic weakening and complementary-affine resolution has more than exp(n/(32768 ell^2)) total lines, including sources. The preprint reports formalization in Lean; independent external review and local kernel replay have NOT been performed.

In the **unchanged Rmix341**, take the original source-authenticated, locally opaque/extensional subgrammar with paid acyclic two-input conservative definitions, binary RES, unrestricted-width GF(2) addition, and sound local Boolean-factor/LOCAL-CONVERT operations whose entire syntactically exposed original variable union for step j has size d_j. No uncharged named circuit-internal wires can be accessed downstream. Let b be distinct original variables directly feeding a paid definition, m original source clauses, r RES steps, x XOR steps, q total distinct paid DAG nodes (including gate definitions), J other local semantic operations. A symbolic compiler into Res(XOR) on the SAME original source gives

$$
S_\oplus(F)\le2^b\left(2m+2r+2x+\sum_{j\in J}2^{d_j+1}+2\right)
\le2^{b+d_*}(2m+2q+2).
$$

The compiler enumerates b original input assignments, evaluates rather than guesses paid auxiliary wire values, translates each local implication with a canonical-blocker semantic-weakening/ordinary-cut tree bounded by 2^(d_j+1), translates every arbitrarily wide GF(2) addition natively in two Res(XOR) lines, guards each original source, and glues branches. Logical proof-line cost does NOT dominate actual proof generation/checking work or peak live memory.

**Conditional tradeoff, subject to Braun's unreviewed external theorem:** on original BPHP, b + log2(2m+2r+2x+sum_j 2^(d_j+1)+2) > n/(32768 ell^2 ln2). Hence b+d_* + log2(2m+2q+2) > that bound. With b+d_* at most (1-epsilon) times the bound, any such restricted proof needs q=exp(Omega_epsilon(n/ell^2)). This is NOT a q-only full-R lower bound and not B1, B2, B3 or a deterministic SAT time bound. Polynomial ER2 bit-PHP certificates remain an actual escape by large definition exposure. No universal small-b or small-scope normalization has been assumed.

## Reproducibility
Python producer and independently implemented JavaScript verifier checked 28 finite source-labelled Res(XOR) certificates, four opposite-parity UNSAT and 24 Boolean conjunction controls, 446 paid nodes, 2990 assertions, 60 source-deletion SAT controls and 256 literal-sign-flip SAT controls; eight malformed or corrupted certificates rejected. Domain d=2..5, no random seeds. The d>3 tests exercise the parameterized mathematical lemma and are NOT claimed legal AND3 instances in unchanged R. The finite proofs are upper certificates, not shortest minima. Complete local raw certificate JSON: 61044 bytes, SHA-256 d85e244f610925f325f63be2e0d20d6b242f7bac33d5e4f0feb90682992e644c. The repository JSON is a verification ledger, not a full raw-certificate upload. Host producer wall 0.84s / peak 96400 KiB, checker 0.04s / peak 33268 KiB; no FLMV-compatible native machine claim.

## Corpus, peers, Grok/Claude
Read November 2 five-role directive (blob 033b54b87b7cbe94912af5cf67daa52859143a07), current issue #3, AGENTS.md, CODEX.md, skill, fixed calculus report 341, LSPV-2 scope 366 and native 369, LSPV-3 372, LSPV-1 370/371, LSPV-4 368, LSPV-5 REFEREE317/319/320. Existing scope-profile compiler 366 covers Resolution with heterogeneous scope; native-affine 369 covers <=3 exposed variables with constant 64; this report combines heterogeneous scope with native parity and gate exposure. External academic novelty and correctness audit pending.

Verified repository directories GROKPROOF/ and research/agents/claude/. Read GROKPROOF/2026-11-03_1912_PROGRESS.md at blob dbec4959d96f19554061511cd240745f398272ec and research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex at blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67. Grok retains an OPEN all-input fully charged FLMV transformation; Claude's TPORT claim is for its restricted alternation-trading rule system. Neither is B3. Primary source Braun original PDF printed p3 screenshot checked. Search of github.com/openai for matching Resolution checker found only unrelated Cech/sheaf resolutions.

## Exact new-role outbox
- `research/agents/lspv-2/2026-11-03_1312_LSPV-2_NATIVE_AFFINE_LOCAL_PROFILE370.tex`
- `experiments/arc/lspv2_370_native_affine_producer.py`
- `experiments/arc/lspv2_370_native_affine_independent_verify.js`
- `results/raw/arc/2026-11-03_1312_LSPV2_NATIVE_AFFINE_LOCAL_PROFILE370_results.json`
- `research/coordination/2026-11-03_1312_LSPV2_NATIVE_AFFINE_LOCAL_PROFILE370_FIVE_ROLE_HANDOFF.md`

Root main.tex reconciliation must modify only its existing LSPV-2 region after a complete authenticated blob read, current blob SHA and preservation of every byte outside the insertion; no unsafe incomplete overwrite. Full repo preflight was not run without a checkout; local tests and LaTeX compilation succeeded separately.

## Next obstacle by role
LSPV-1: B3 requires an all-length noncircular implication from SAT in P to polynomial refutation minima for the same R. LSPV-2: pin LOCAL-CONVERT syntactic downstream named-wire semantics and test whether exact extensional compilation extends to them. LSPV-3: audit independent support measure and Braun source encoding. LSPV-4: charge all branch enumeration, source/index, proof bytes and live peak space before any machine transfer. LSPV-5: attack the local semantic proof bound, guard lifting, source widths and quantifiers; preserve full-R and B3 OPEN.
