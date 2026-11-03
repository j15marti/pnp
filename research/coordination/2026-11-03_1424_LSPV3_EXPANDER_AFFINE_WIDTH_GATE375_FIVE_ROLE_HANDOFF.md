# LSPV-3 EXPANDER-AFFINE-WIDTH-GATE375: Five-role handoff

**2026-11-03 14:24 PST, America/Los_Angeles.** Existing task 6ad6f05603248191abb281a5b43b3fc2 and all five established schedules, enabled states, ownership boundaries, and the fixed Rmix341 grammar remain unchanged. P versus NP OPEN.

## Published hard theorem and new scoped lemma

Urquhart (JACM 1987) and Ben-Sasson--Wigderson (JACM 2001) establish exponential unrestricted shared-DAG ordinary Resolution size on odd Tseitin 3CNFs from bounded-degree expanders. For cubic h-vertex G, the source formula has n=3h/2 edge variables, m=4h original clauses, encoded signed ASCII DIMACS N=Theta(h log h) bits. Ordinary Resolution requires 2^Omega(h) lines. The **same sources** have previously proved exact unit-node minimum W_Rmix341=4h-1 under source-authenticated AND3 extraction plus GF(2) addition, so this is not full mixed hardness.

**PROVED/EXACT, scoped to the pure-XOR phase (specialist review pending):** Let beta(G)=min_{empty != S != V} |delta(S)|/min(|S|,h-|S|). Every binary shared-DAG XOR refutation of the h authentic vertex equations R_v: XOR_{e incident v} x_e=b_v, with odd total charge and root 0=1, has an **intermediate** affine equation containing at least beta(G)h/3 distinct original edge variables. The minimum number of charged XOR steps is nevertheless exactly h-1. In any constant-expansion cubic family, optimal XOR derivations have Theta(h) logical nodes while *every* XOR derivation has maximum row width Theta(h)=Theta(N/log N). DAG sharing, cancellation, redundant recomputation and hindsight-minimal choices do not escape the bound.

**Proof spine:** Connected graph incidence B has left kernel span(1_h). Odd charge makes augmented [B|b] full row rank h, so each derived affine row has a unique vector of h source-row coefficients. The root 0=1 has coefficient 1_h. In any root-ancestor topological order, take the first node whose coefficient support exceeds h/3; both parents have support <=h/3, hence its support S satisfies h/3<|S|<=2h/3. Its nonzero edge coefficients equal the boundary delta(S), so expansion forces width >=beta h/3. Any proper subset of h source rows is consistent, yielding binary-arity minimum h-1, attained by a balanced XOR tree.

## Falsification controls and machine-cost firewall

F1: sharing/cancellation avoids balanced coefficient support: **falsified by topological proof**. F2: balanced coefficient support is always narrow in edge variables: **false for expanders**, with path negative control. F3: zero-width root invalidates intermediate width: **false**. F4: this width bound automatically holds for every mixed RES/AND3/DEF/LOCAL-CONVERT proof: **OPEN and not claimed**.

Python producer independently implemented JS checker completed **8,936 assertions**, rejected **10 malformed/corrupt fixtures**, inspected three XOR-DAG styles per five graphs, all finite edge cuts, original signed source clauses, local parity truth tables, 120 same-source deletion SAT witnesses, 360 literal-sign repairs, even-charge SAT models and exhaustive odd/ even counts on small cases. Fixed graphs (h,m,beta,minimum balanced boundary,N bits): K4 (4,16,2,4,1304); K3,3 (6,24,5/3,4,1912); cube (8,32,1,4,2720); prism6 (12,48,2/3,4,4320); path8 (8,14,1/4,1,832). The path is noncubic and a negative expansion control, not a 4h-1 minimum claim. No new formula family was generated beyond established graph controls.

Logical node count, maximum affine row support, full encoded proof evidence, proof search and native verification/peak memory remain different measurements. One wide XOR row can be a single paid *logical* node, so the width theorem does not imply a superlinear W_Rmix341 lower bound or Turing-machine time. Continue fully charged all-phase rho with s'<=max{rho,eta,lambda,lambda*s} before any FLMV claim.

## Corpus and external assessments

Read the latest priority refocus at commit 4e29ed7646f484707767acb6e63ec5f38afd98a8 / blob 033b54b87b7cbe94912af5cf67daa52859143a07, issue #3, AGENTS.md, CODEX.md, repository skill, root main blob 6fc51c87, original LSPV-2 341 (c87acd11), LSPV-3 373/374, and current peer LSPV-1 372, LSPV-2 370/368, LSPV-4 368/369, and LSPV-5 321. Credit prior full mixed minimum and depth; do not rediscover them.

Real paths were listed and files read: GROKPROOF/2026-11-03_2214_PROGRESS.md (59fe73c2), research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex (d06a2d56), research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex (b7150bb9), and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6). Grok's all-input charged FLMV contraction is OPEN; REWIRE concerns circuit optimization; Claude's alternation-trading and one-tape conclusions are model-restricted. Neither supplies full mixed hardness or B3.

Literature: Urquhart 1987 DOI 10.1145/7531.8928; Ben-Sasson--Wigderson 2001 DOI 10.1145/375827.375835; Cook--Reckhow 1979. Searches included expander Tseitin proof lower bounds, row support XOR, the repository's existing affine width and LOCAL-CONVERT work, and github.com/openai for a parity verifier (no relevant connected result). The pure-XOR bound may be a known cutwidth-style observation; no claim of external novelty is made.

## Published artifacts and boundaries

Formal report: `research/agents/lspv-3/2026-11-03_1424_LSPV-3_EXPANDER_AFFINE_WIDTH_GATE375.tex`

Public standalone recomputation: `experiments/arc/lspv3_375_expander_cut_compact.js`

Public raw summary: `results/raw/arc/2026-11-03_1424_LSPV3_EXPANDER_AFFINE_WIDTH_GATE375_public.json`

Complete local reproducibility archive includes full Python producer, independent no-import JS verifier, full 39,453-byte raw witness/DAG fixture SHA-256 e34d80629298baf77d2a0f556a63559840183c0cc0cc7105820d8db760d867ac, and check ledger. The public compact checker is not the full verifier. Root main.tex reconciliation will use full-blob SHA current-head conditional update, preserving content outside the LSPV-3 ownership markers.

**Next exact missing arrow:** Extend/falsify the support-cut constraint under every permitted Rmix341 inference, especially conservative circuits and named LOCAL-CONVERT interfaces, or establish a polynomial same-source backtranslation with proper direction. Independently B3 remains SAT in P implies polynomial Wbar_Rmix341 for this same fixed R; B1/B2/B3 and superpolynomial Wbar_R are OPEN. P versus NP OPEN.

**Role allocation:** LSPV-1 B3/reflection; LSPV-2 test mixed-rule circumvention, typed circuits and paid definitions; LSPV-3 source-width invariant boundary and escape profile; LSPV-4 bit-evidence/work/peak-space auditing; LSPV-5 falsify hidden width-to-cost reversal or unsound backtranslation. No task mutation.