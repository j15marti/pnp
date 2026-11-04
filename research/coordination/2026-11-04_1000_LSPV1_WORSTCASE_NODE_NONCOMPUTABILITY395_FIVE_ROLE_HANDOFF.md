# LSPV-1/395 five-role handoff: uncomputable *worst-case* minimum node profile
November 4, 2026, 10:00 PST (America/Los_Angeles). LSPV-1 owns formal $W_R/\overline W_R$ and B1/B2/B3 quantifiers. No task, state, schedule or rule mutations. P versus NP OPEN.

## IDEA -> SEARCH -> ITERATE
**IDEA:** strengthen LSPV-1/385's pointwise uncomputable node-minimum example to a *worst-case profile*, and falsify the assumption that a uniform polynomial paid-node upper bound makes $\overline W(N)$ computable. Prediction: a single fixed, sound, complete, polynomial-time-checkable proof system can have a globally linear node-count upper bound but an uncomputable exact worst-case profile.

**SEARCH:** Reviewed verified November 2 refocus (commit 4e29ed7/blob 033b54b), issue #3 including newest 808 comments, AGENTS.md (19656af1), CODEX.md (754999f5), project skill (b8df83a7), original Rmix341 grammar (c87acd11), LSPV-1/385, LSPV-1/394, LSPV-5/REFEREE334, LSPV-2/351, LSPV-3/392, LSPV-4/390, and real Grok/Claude files. Primary literature: Cook--Reckhow JSL 1979, Haken TCS 1985, Cook SIGACT 1976, Lacerda arXiv:1406.1808. Queries included 'worst-case minimum uncomputable', 'Wbar uncomputable', 'proof system minimum certificate halting', 'Cook Reckhow polynomial verification', 'Haken pigeonhole resolution', and OpenAI GitHub 'ExecCNFNodeSearchCorrectness', 'ExecCNFNodeSearchCosts'. Actual openai/math source files blobs 1eb3d29c and 1ced21f4 were read; they do not provide a SAT-to-mixed-R compiler. Direct Google interface unavailable; general web search and GitHub authenticated search used.

**ITERATE:** The initial fallback chain might have been dominated by other UNSAT formulas when maximizing over *all* CNFs. Repaired the construction with a one-node, fully checked PACK rule for every **non-special** source, and only FAST/SLOW proofs for a syntactically recognizable series of contradictory special sources. The proof avoids hidden SAT oracles: the packed full Resolution payload is independently replayed, and the FAST halting trace is locally verified.

## PROVED/EXACT metatheorem, specialist review pending
For canonical signed source $S_n=(x_1)\wedge(\neg x_1)\wedge\bigwedge_{j=2}^{n+1}(x_j\vee\neg x_j)$, define a fixed *artificial* proof calculus $P^\dagger$:
- Generic UNSAT (not a syntactic $S_n$): one PACK node encloses an authentic full ordinary-Resolution refutation.
- Special $S_n$: one FAST node iff an explicit universal-machine halting tableau on input $n$ is verified; otherwise n+2-stage SLOW chain always works.
- Only those proof kinds are admissible on the corresponding source. All full certificates are polynomial-time checkable in actual serialized length.
Thus $W_{P^\dagger}(S_n)=1$ for halting $n$, $n+2$ for nonhalting $n$, and other UNSAT formulas have $W=1$. At strictly increasing canonical lengths $N_n=|E(S_n)|$:
$$
\overline W_{P^\dagger}(N_n)
 =\max(\{1\}\cup\{j+2:j\le n, U(j)\uparrow\});
\quad U(n)\uparrow\iff\overline W_{P^\dagger}(N_n)=n+2.
$$
Yet for **every** N, $\overline W_{P^\dagger}(N)\le N+2$. Therefore the exact worst-case node profile is noncomputable despite a known linear node upper bound and polynomial-time **full evidence** checking. This is a deliberately pathological proof system, **not** the unchanged $R_{\mathrm{mix341}}$. The former permits gigantic hidden PACK/HALT evidence and is not a permissible node/blocking transformation for the latter. It neither refutes nor supplies B1/B2/B3 for the real R. Indeed the fake calculus has trivial B1/B2/B3 by its linear node bound.

## Both-label, malformed, controls and full physical cost
Local deterministic Python finite producer: 196 assertions, 20 toy sources $S_1..S_{20}$; separate Node verifier: 255 checks. Six toy halting and fourteen nonhalting indices; prefix maximum 22. Invalid sources, wrong Resolution pivot/output, malformed/shortened/permuted slow chains, forged FAST trace, and forbidden PACK on a special source rejected. The finite machine halts iff $n$ divisible by 3, **NOT a universal halting test**. Universal theorem is symbolic. All payload bytes, construction, source/index access, checking, and peak space remain charged in physical computational models, even if their wrapper consumes one artificial logical node.

## Published exact outbox and readback
- Formal report: `research/agents/lspv-1/2026-11-04_1000_LSPV-1_WORSTCASE_NODE_PROFILE_NONCOMPUTABILITY395.tex`, blob `cf2e5b4aef465ac94381d22db44fade3a14db62a`.
- Python producer: `experiments/arc/lspv1_395_profile_producer.py`, blob `0a3d868820a5dbcc4faefb65b18539155a0e30cd`.
- Independent JS verifier: `experiments/arc/lspv1_395_independent_verify.js`, blob `32d993d965310ffeab19bce99922c7b4f18aede3`.
- Raw finite record: `results/raw/arc/2026-11-04_1000_LSPV1_WORSTCASE_NODE_NONCOMPUTABILITY395.json`, blob `ff5986f37e46d200901ee67a6d6d23dc4b4ff49f`.
All four published files fetched with nonempty correct content and full readback. Local producer/verifier programs were executed as logically equivalent scripts, not claimed as byte-identical to the GitHub readback executables. Root main.tex reconciliation status reported separately.

## Role-targeted next steps
LSPV-1: Return to authentic Rmix341 LOCAL-CONVERT and prove or falsify a computable all-proof node-to-bit bound b(N,q). This countermodel proves that merely showing $\overline W(N)\le \mathrm{poly}(N)$ is insufficient for exact-minimum computability; it is no progress on the main hardness target.
LSPV-2: Pin the full original grammar and private/public wire rules; no added PACK/FAST step.
LSPV-3: Test whether source-authentication and shared-DAG conditions exclude all macro payload hiding.
LSPV-4: Explicit paid parsing, proof output, tableau length, and checker time/space; keep all-phase $\rho$.
LSPV-5: Audit source-special-case legitimacy and the nonhalting iff prefix-max step; confirm no B3 sleight of hand.
Historical Grok `GROKPROOF/2026-11-04_1518_PROGRESS.md` blob 4e2bb9d9 and Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob 9a5b05d6 were read. Neither has a B3 bridge. Fixed Rmix341, all five roles, existing hourly times and activation state unchanged.
