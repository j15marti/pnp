# LSPV-1/509: Connected terminal-essentiality upgrades the shared-DAG inference floor
**2026-11-08 09:00 PST | Route B | PROVED/RESTRICTED finite theorem + COMPUTATIONAL | P versus NP OPEN**

**Affected tracker node:** new [P2-L1-509], strengthening [P2-L1-508] and the multi-root accounting control [P2-F13]. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. Companion Route A [P1-01], [P1-03], [P1-04] remain OPEN.

## IDEA, falsifiers registered before SEARCH
Hypothesis: the [P2-L1-508] generic source-essentiality bound $q\ge (m-r)/(d-1)$ is not sharp for the previously published *three-goal* source-indexed Resolution gadget. If the same original source clause is indispensable for multiple distinct goals, those goals must belong to a single connected component of the joint ancestral proof graph. Test these four falsifiers:

1. At least one claimed individually essential source for a *particular* output is actually dispensable for that output.
2. The indispensable-source overlap graph on the three goals is disconnected, so the generic $r=3$ bound is already sharp.
3. A legal binary, context-free shared-DAG deriving all three outputs using all 16 source leaves can have fewer than $m-1=15$ inference nodes despite weak connectivity.
4. The graph floor is mistakenly interpreted as a complete historical mixed-calculus lower bound or a new asymptotic hardness result.

Falsifiers 1–3 are ruled out by exhaustively checked source-deletion witnesses, a graph-theoretic proof and explicit abstract tightness construction. Falsifier 4 is excluded from the claim.

## SEARCH: actual continuity and external scope
Read live root trackers completely: proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; proof2.txt blob 3568f93dad7b5868ddb7c640de6019b77fba8889 (prepublication). Current issue #3, its recent LSPV-3/504-/505 and LSPV-5/436 comments, the 2026-11-02_1204 five-role handoff, AGENTS.md, CODEX.md, pnp-research SKILL.md, and previous LSPV-1/507-/508 were inspected. Read recovered historical /341 checker-scope referee [P2-L5-413], which authenticates only SOURCE/AND3/XOR in its executable, not unrestricted historical RES/DEF/LOCAL-CONVERT. Current actual Grok file GROKPROOF/2026-11-08_0930_PROGRESS.md and Claude research/agents/claude/world-ledger/README.md were inspected; neither proves B3.

Change-aware required repository review: konard/p-vs-np/scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 (model-scoped Lean claims); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 (restricted methods and explicit caveats); meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f (FRAT/XOR proof format, not historical grammar); tanyongkiam/cake_lpr/README.md blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c (verified checker, not historical grammar). Also reviewed source metadata from openai/math and peer /508 references. Public web queries on Pang 2026, Haken, Cook–Reckhow, and proof-size/reflection were performed, without a separate Google-branded client.

Established hard-family control: a connected odd-charge cubic expander Tseitin source has $h$ vertices, $3h/2$ edge variables, exactly four signed 3-clauses per vertex ($m=4h$), and exponential ordinary shared-DAG Resolution lower bound for standard expander constructions (Urquhart 1987; Ben-Sasson–Wigderson JACM 2001). GF(2) summation makes the same formula easy in algebraic mixed systems. It is therefore an upper-bound/shortcut control, not evidence of mixed hardness. Pang, arXiv:2610.00837v2 (2026), establishes lower bounds in a specified constant-degree polynomial-resolution system, explicitly not an extension-complete proof calculus.

## ITERATE: new connected-overlap lemma
For a sound **context-free** proof DAG with distinct original source leaves $S_1,\dots,S_m$ and $r$ designated goals $Q_1,\dots,Q_r$, define $E_j$ as the set of source clauses individually indispensable for deriving $Q_j$: for each $i\in E_j$, there is a Boolean assignment satisfying every other source clause and falsifying $Q_j$. Every sound derivation of $Q_j$ must use $S_i$ as an ancestor.

Define an undirected graph $H$ on the goal indices, joining $j,k$ when $E_j\cap E_k\ne\varnothing$. Assume $\bigcup_j E_j$ contains all $m$ original source clauses and let $c$ be the number of connected components of $H$. If every paid derived node has at most $d\ge2$ parents, the union of the goal-ancestral sub-DAGs has at most $c$ weak components. Let $q$ denote all distinct derived nodes in this pruned union, counted once, and $e$ its number of premise edges. Then
$$
e\ge m+q-c,\qquad e\le dq,
$$
so
$$
\boxed{q\ge\left\lceil\frac{m-c}{d-1}\right\rceil.}
$$
Any extra derivations outside the goal ancestry only increase total work when weights are nonnegative. This extends the [P2-L1-508] bound with $c\le r$. The proof counts a shared premise or node **once** and does not disallow branching or reconvergence. It does NOT add any inference rule. For weighted work, $W\ge w_{\min}q$ only if each contributing derived inference is paid at least $w_{\min}>0$; no assertion is made about unverified historical weights or free rules.

### Exact source, necessity graph and tightened floor
Use the **same** 16 proper signed three-literal source clauses and same three required outputs as /507-/508, on $(x,y,t,a,p,b,h)$, implementing
$$
a=x\land y,\quad p=y\oplus t,\quad b=x\land p,\quad h=a\oplus b=x\land t.
$$
The goals are $Q_0=(\neg x\lor\neg t\lor h)$, $Q_1=(x\lor\neg h)$ and $Q_2=(t\lor\neg h)$.

The new per-goal indispensable source sets, with zero-based source IDs, are:
$$
E_0=\{2,3,5,7,10,11,13,14\},\\
E_1=\{0,1,8,9,12\},\\
E_2=\{0,1,2,3,4,6,8,9,10,11,12,15\}.
$$
Every source belongs to their union. $E_0\cap E_2=\{2,3,10,11\}$ and $E_1\cap E_2=\{0,1,8,9,12\}$, while $E_0\cap E_1=\varnothing$. Thus $H$ contains edges 0–2 and 1–2 and is connected: $c=1$, not $r=3$.

For **binary ordinary Resolution**, $m=16,d=2,c=1$:
$$
\boxed{15\le q_{\mathrm{Res,three\,goals}}\le19.}
$$
The 19-inference existing legal Resolution upper certificate is /507. The lower bound is against **every** context-free source-authenticated shared binary Resolution DAG for the three simultaneous outputs. It does not prove that the minimum is 15: exact Resolution optimum remains between 15 and 19.

**Tightness of the graph argument, not of Resolution:** An abstract union-of-provenance binary DAG has exactly 15 merge nodes and three different terminal roots with source ancestry sets *exactly* $E_0,E_1,E_2$. Build common clusters $A=\{2,3,10,11\}$ with three merges, $B=\{0,1,8,9,12\}$ with four merges; finish goal 0 by four merges with sources $\{5,7,13,14\}$; let goal 1 be the $B$ cluster; finish goal 2 by four merges joining $A,B,\{4,6,15\}$. Hence 3+4+4+4=15. These abstract merges are **not legal Resolution deductions**, and therefore show only that the connectivity/arity invariant alone cannot force 16 or more.

## Finite controls and resource separation
Independent Python: 487 check groups, all 128 Boolean assignments checked for source semantics, all 16 original clauses tested *separately for each goal*, 25 positive per-goal source-deletion witnesses and 15-node structural closure and connectivity. Separately authored JavaScript: per-goal source witnesses, 128 semantics controls, explicit 15-node binary union DAG and a tautology control. The actual historical R_mix341 checker and producer were NOT run for this macro. No claim of solver runtime or peak-space bound follows from proof-node counts; source/checker parsing, discovery, storage, JSON/trace size, references, verification and publication each require separate actual-machine charging. No source-hardness transfer is claimed.

## Status and next decisive gap
**PROVED/RESTRICTED:** connected terminal-source overlap strengthens the finite three-goal Resolution floor from 13 to 15. **COMPUTATIONAL:** exact deletion witnesses and abstract 15-node control. **OPEN** [P2-D1] historical grammar, [P2-C3] all-native transfer, [P2-B1] superpolynomial worst-case minimum over full mixed rules, and [P2-B2] same-calculus noncircular B3. This linear structural invariant is already saturated by known mixed Tseitin shortcuts and cannot itself establish a superpolynomial all-rule lower bound.

P versus NP OPEN.

Primary references: Cook and Reckhow, Journal of Symbolic Logic 44(1), 1979, 36–50; Ben-Sasson and Wigderson, Journal of the ACM 48(2), 2001, 149–169, DOI 10.1145/375827.375835; Pang, arXiv:2610.00837v2, October 24 2026 (preprint).