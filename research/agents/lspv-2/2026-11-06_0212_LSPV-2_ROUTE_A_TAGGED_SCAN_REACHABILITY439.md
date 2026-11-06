# LSPV-2/439 | Conditional undecidability of an all-length scan-reachability audit
**November 6, 2026 02:12 PST. Route A primary. PROVED/RESTRICTED conditional theorem; COMPUTATIONAL finite controls. Universal FLMV contraction OPEN.**

## IDEA -> SEARCH -> ITERATE and falsifiers
Hypothesis: while LSPV-2/433 safely removes *syntactically authenticated* dead private scans, no total exact static analyzer can determine for every correctly implemented polynomial-time SAT decider whether a designated scan executes on **any input length**. Falsifiers: (F1) nonhalting source machine causes a non-total decider; (F2) bounded simulation loses polynomial runtime; (F3) the output changes, making this merely Rice's extensional theorem; (F4) the result wrongly excludes all beneficial optimization. Bounded $n$-step simulation resolves F1/F2. The output is identical to the guest's, resolving F3; F4 limits the conclusion rather than strengthening it.

## Theorem 439.1 (CONDITIONAL, complete proof)
**Assume SAT is in P**, so a fixed uniform total polynomial-time decider $A_0$ handles the project's binary CNF SAT/UNSAT/malformed conventions correctly on every binary string. For any blank-input Turing machine $M$, effectively construct $A_M$ as follows on $x$ of length $n$:
1. Simulate $M$ on blank input for at most $n$ transitions, stopping early on a simulated halt.
2. If and only if a simulated halt occurred, execute a specially **tagged, private** full-input scan of $x$; the scan has no guest-visible side effects.
3. Restore the guest entry configuration and call $A_0(x)$, returning its answer.

Every $A_M$ is total and uniformly polynomial-time: bounded $n$-step simulation requires $O(n^2)$ time and $O(n)$ tape on a fixed ordinary indexed machine under a conservative implementation, the optional scan requires $O(n)$ time, and $A_0$ is polynomial. All answers, including malformed-input handling, exactly equal $A_0(x)$.

If $M$ halts after $h$ transitions, the tagged scan occurs whenever $|x|\ge h$. If $M$ never halts it never occurs. Thus
$$
\exists x\;[\operatorname{TAGGEDSCAN}\text{ executed in }A_M(x)]
\quad\Longleftrightarrow\quad M\text{ halts on blank input}.
$$
Any total computable exact analyzer of this all-length tagged-reachability property for the promised family of total polynomial correct SAT deciders would decide the halting problem. Contradiction. The property is enumerable but not decidable under that promise. This is a classical **intensional program-reachability** reduction, not an invocation of Rice's theorem for semantic input/output properties.

**Important falsification of an overclaim:** The tagged scan is known syntactically to be semantically dead and can be erased without deciding reachability. Hence this theorem does NOT prohibit generic erasure of this tag, solver-dependent shortcuts, or a universal $A\mapsto\Phi(A)$ transformation. It only prohibits an exact all-length reachability preflight if that particular test is demanded by a proposed compiler. The theorem is conditional on the P=NP hypothesis, not evidence that SAT in P is true.

## Established hard-family ledger and controls
Use the published *cubic-graph Tseitin* original signed proper 3-CNF on connected $G_H=(V,E)$, $H$ vertices, $m=3H/2$ edge variables. At each vertex with ordered incident edge IDs $a_v<b_v<c_v$, encode four original 3-clauses:
$$
C_{v,p,r}(\chi)=\ell_p(x_{a_v})\vee\ell_r(x_{b_v})\vee\ell_{p\oplus r\oplus1\oplus\chi_v}(x_{c_v}),\quad(p,r)\in\{0,1\}^2,\quad\ell_0(x)=x,\ell_1(x)=\neg x.
$$
Exactly $4H$ source clauses and $m$ original variables. The finite test bit encoding uses unary $m$ and $4H$ in the header, then $12H$ $(w+1)$-bit signed literal fields, $w=\lfloor\log_2m\rfloor+1$, $N=\Theta(H\log H)$. For connected $G_H$, SAT iff $\bigoplus_v\chi_v=0$. Suitable *growing cubic-expander* odd Tseitin instances have $2^{\Omega(H)}$ **ordinary shared-DAG Resolution** size lower bounds, per Urquhart 1987 and Ben-Sasson/Wigderson 2001. These are restricted proof-size bounds, not arbitrary SAT time lower bounds and not bounds for full historical $R_{\mathrm{mix341}}$. The permitted GF(2) parity shortcut is a mandatory upper control. Finite K4/cube/Petersen instances are semantic fixtures, not growing-family hardness certificates. This fixed width-three family needs no reduction from wider CNF.

## Executed finite controls
A Python producer created six original source encodings, K4/cube/Petersen with both odd UNSAT and even SAT charges, six malformed and 48 short binary controls. It ran four bounded-control machines: HALT_0, HALT_5, HALT_20 and a syntactically verified infinite right-moving LOOP. Across 60 inputs and 240 traces, 123 tagged scans occurred; 754 producer assertions passed. An independently implemented Node.js checker rebuilt the original Tseitin clauses and hashes, used separate exhaustive SAT evaluation on small instances, checked all traces and exposed five corrupted controls: **1,449 checks PASS**. The first draft of its Petersen fixture used a different edge numbering; exact byte matching caught it and the verifier was corrected before the passing run. A **standalone** Node.js compact replay passed 423 assertions on 32 inputs/128 traces. The exhaustive fixture decider is NOT polynomial in general and no native FLMV timings or high-water space were measured.

## Resource and transfer audit
An actual $A_M$ charges the bounded simulation's $O(n^2)$ work, its $O(n)$ writable high-water, every executed input scan and index/head cost, guest computation and output. Its construction is *not* the sought contraction. A trace-reachability test cannot be assumed free or decidable on all lengths. No source-only splitter, semantic oracle, recursively shorter SAT children, both-label join, or iterated same-machine proof is supplied. Results from LSPV-2/432-438 and LSPV-4/435 remain valid at their original restricted scope; proof-DAG branching/shared assumptions and native R_mix341 rules/weights are unchanged.

## Source recovery and literature
Read GitHub governing five-role handoff at historical commit 4e29ed7646f484707767acb6e63ec5f38afd98a8 (blob 033b54b8), issue #3 through 1,039 comments, AGENTS.md 19656af1, CODEX.md 754999f5, skill b8df83a7; LSPV-2/438 df2d5570; LSPV-4/435 87759faa; Grok root GROKPROOF/2026-11-06_0515_PROGRESS.md 93f9202; Claude research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex b7150bb. Required external source checks: konard/p-vs-np/proofs/complexity/README.md 7ee9a11 (finite one-tape model differs from FLMV); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md 18d693e and AFFINE_DECOMPOSITION_NEXT_REVIEW.md (potentially exponentially many affine terms); MassimoLauria/cnfgen/cnfgen/families/tseitin.py 4bb5fd1; meelgroup/frat-xor/README.md 38a137b; openai/math/README.md cc5b0a0. Literature: FLMV JACM 2005 DOI 10.1145/1101821.1101822; Ben-Sasson/Wigderson JACM 2001 DOI 10.1145/375827.375835; Urquhart 1987 DOI 10.1145/7531.8928; Bennett 1989 DOI 10.1137/0218053. Browser web search used; Google-branded search unavailable. Root main.tex existed but fetch returned **zero bytes**; left unchanged to prevent overwrite.

**Status:** restricted conditional computability barrier and finite controls established; independent peer theorem review pending. **OPEN:** for EVERY correct uniform polynomial SAT decider, fully charged original-source-authenticated recursively iterable all-input same-machine FLMV contraction with $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$; noncircular same-calculus B3; P versus NP.
