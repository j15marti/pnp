# LSPV-2/435: Exact source-bit sensitivity defeats literal footprint sharing on Tseitin 3-CNF

**November 5, 2026, 22:16 PST | Route A primary | PROVED/RESTRICTED and COMPUTATIONAL | Universal FLMV contraction and P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE

**Hypothesis:** LSPV-2/432's sound completed-trace input-read-footprint test can have **zero reuse** on a standard published-hard proof-complexity family even when the family has a simple shared algebraic summary. Unlike an inert full-input scan (LSPV-2/433), the obstacle can be forced by *semantic correctness* of every deterministic solver.

Falsifiers checked: (F1) a one-vertex charge change might not reverse the SAT label; (F2) changing a charge might fail to toggle every sign bit from which a solver could detect the charge; (F3) the graph or encoding might change nonlocally or in length, invalidating same-input-trace induction. All fail for the stipulated connected graph and fixed-width literal layout. Reproducing six exact charge-controlled original 3-CNFs and exhaustive finite graph-domain checks is a validation control, not an asymptotic complexity proof.

## Family, exact 3-CNF, binary encoding

Let $G=(V,E)$ be a fixed connected simple cubic graph with $H$ vertices, $M=3H/2$ edge variables, and sorted incident edges $a_v<b_v<c_v$ for each vertex. For each vertex charge $\chi_v\in\{0,1\}$, insert four proper 3-clauses, in lexicographic order of $(p,q)\in\{0,1\}^2$,

$$
C_{v,p,q}(\chi)=\ell_p(x_{a_v})\lor\ell_q(x_{b_v})\lor\ell_{p\oplus q\oplus1\oplus\chi_v}(x_{c_v}),
\qquad \ell_0(x)=x,\quad \ell_1(x)=\neg x.
$$

The conjunction forbids exactly the local assignments of parity $1\oplus\chi_v$, so enforces the graph's usual XOR constraint $x_{a_v}\oplus x_{b_v}\oplus x_{c_v}=\chi_v$. This is the standard Tseitin source family, not a bespoke hard family. It has exactly $4H$ width-3 clauses, $M$ variables and $N=\Theta(H\log H)$ bits.

The replay's typed source stores 8-bit magic `10100111`, unary $H,M$, sorted edge endpoints in $w$ bits, $4H$ ordered clauses with one sign bit and one $w$-bit edge ID per literal, and terminal `00`; $w=\max(1,\lceil\log_2(H+1)\rceil,\lceil\log_2 M\rceil)$. Its exact length is

$$
N=8+(H+1)+(M+1)+2Mw+12H(w+1)+2.
$$

Graph metadata are identical for each charge vector and do not change the *CNF* clause count. Changing a single vertex's charge flips **exactly four source sign bits**, the third sign in each clause of that vertex. Denote this disjoint four-position set by $D_v$. The header, edge IDs, clause ordering and source length do not change. The test script uses $w=\lfloor\log_2 M\rfloor+1$; this equals the stated uniform width on all three tested graphs.

## Theorem 435.1: necessary read from each charge block (PROVED/RESTRICTED)

Fix a connected cubic graph and this binary encoding. Let $A$ be **any deterministic total all-input correct SAT decider** whose source-dependent machine behavior comes from its indexed/sequential source-bit reads. Let $R_A(x)$ contain every source-bit position read on original input $x=\operatorname{enc}(F_{G,\chi})$, including preprocessing and all guest computations. Then

$$
\forall\chi\;\forall v\in V,\quad R_A(\operatorname{enc}(F_{G,\chi}))\cap D_v\ne\varnothing.
$$

**Proof:** XOR-add all vertex equations. Each edge variable occurs twice and cancels, showing every satisfying assignment requires $\bigoplus_v\chi_v=0$. The mod-2 incidence matrix of connected $G$ has rank $H-1$, so this condition is also sufficient. A single charge flip at vertex $v$ reverses the SAT label. Its encoding $x'$ has the same length and differs from $x$ precisely on $D_v$. If $A$ on $x$ never read a position in $D_v$, induction over its deterministic transitions gives identical runs and outputs on $x$ and $x'$, contradicting all-input correctness. QED.

**Corollary 435.2:** For *any* two distinct charge vectors $\chi\ne\chi'$ on the same graph, the successful LSPV-2/432 reuse condition

$$
x|_{R_A(x)}=x'|_{R_A(x)}
$$

is **false**. Choose a vertex $v$ on which the charges differ. All four bits of $D_v$ flip, and Theorem 435.1 requires at least one of them to have been read. This remains true when the two charge vectors have identical parity and thus equal SAT labels. It is not a lower bound on solver time beyond $H$ source-bit reads, and says nothing about the *peak* retained memory.

## Hard-family qualification and strongest shortcuts

The original published-hard control is **odd-charge Tseitin on a growing family of connected cubic expanders**. Urquhart (JACM 1987) and Ben-Sasson/Wigderson (JACM 2001) give $2^{\Omega(H)}$ ordinary shared-DAG **Resolution** refutation-size lower bounds for suitable expander families. The theorem does NOT apply to all connected cubic graphs, extended Resolution, algebraic reasoning, fixed mixed R_mix341 or arbitrary SAT machines. The current K4, cube and Petersen controls do not form a certified asymptotic expander family. UNSAT for odd total charge is certified by parity independently of any Resolution lower bound.

A one-bit running XOR of the authenticated charge vector provides a small-space, polynomial-time *promise-family* solver; a mixed AND3/GF(2) proof with $4H-1$ paid nodes is already reported in LSPV-2/341 for eligible graphs. These are **legal shortcuts**, not exceptions to hide. An arbitrary 3-CNF decider still needs a validated fallback outside the family, and recognition/validation/conversion costs cannot be assumed free. The present theorem establishes a gap between literal input-read equivalence and algebraic summary equivalence, not an unrestricted time/space lower bound.

## Execution record, independent controls

Executed Python producer: **1,164,000 checks** on complete charge vectors and edge assignments, local XOR clauses, four-bit charge toggles and the representative one-pivotal-bit-per-vertex trace comparison. Executed independently written JavaScript parser/referee: **76,965 checks**. Controls: K4 $(H,M,N)=(4,6,250)$, cube $(8,12,608)$ and Petersen $(10,15,757)$; respectively 16/256/1024 charge vectors with 8/128/512 satisfiable charge vectors. Six original source strings with SHA-256, proper 3-CNF parsing, odd/UNSAT and even/SAT labels, exact edge-assignment reachability, malformed-input rejection and corrupt *promise* rejection were checked. A rejected promise certificate is **not** labeled UNSAT. All experiments are host-language finite tests, NOT native FLMV-machine measurements, and no R_mix341 checker was run.

## Resource and transfer audit

A practical footprint cache separately charges instrumentation, read-position storage, every failed comparison, actual solver calls, source parsing, child source acquisition, index-tape writes/erasure and all peak live work space. The theorem forces $H$ **reads**, not $H$ physical work-tape cells: an algebraic shortcut uses a parity bit and loop counters. Static bytes, logical DAG nodes, critical-path span and materialized machine work are different metrics. No general SAT solver, even with a read-footprint trace, has been shown to generate the needed authenticated children and joins.

The missing ALL-INPUT, recursively iterable same-FLMV-machine transformation for every fixed uniform total polynomial SAT decider remains:

$$
A\mapsto\Phi(A),\qquad
t'\le\max\left\{11/10,3/5+t/2\right\},\quad
s'\le\max\left\{1/2,s/2\right\}.
$$

No exponent extraction, free source splitting, semantic oracle, program-dependent hardcoding or native calculus change has been added. B1/B2/B3 remain separate and OPEN, and P versus NP remains OPEN.

## Research and source record

Read governing five-role refocus, current coordination issue #3, LSPV-2/434 handoff/report, LSPV-4/430 and /431, AGENTS.md, CODEX.md, pnp-research skill, actual `GROKPROOF/2026-11-06_0515_PROGRESS.md` and `research/agents/claude/world-ledger/README.md`. Prior /432 footprint reuse and /433 dead scan erasure are *reused*, not restated as new. LSPV-4/430's separate $\Omega(qM)$ private-witness *certificate checking* lemma is not this theorem about the read set of an arbitrary **correct SAT decider**.

Original code/source references inspected: `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` blob `4bb5fd198f`, `meelgroup/frat-xor/README.md` blob `38a137bca`, `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` blob `1ced21f44a`, `konard/p-vs-np/proofs/complexity/README.md` blob `7ee9a11e` (separate one-tape model) and `scripts/proof_status.json` blob `93b77ed3`, `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea` and `AFFINE_BOUNDARY_PHASE_REPORT.md` blob `3228ffe8` (bounded affine piece arithmetic, no general polynomial piece-count claim). These are not accepted as a solution of P versus NP. Google-branded interactive search unavailable; indexed web search used. Primary literature: [1] Urquhart 1987, DOI 10.1145/7531.8928; [2] Ben-Sasson/Wigderson 2001, DOI 10.1145/375827.375835; [3] Nisan 1991, DOI 10.1137/0220062 (general decision-tree sensitivity context); [4] Fortnow et al. 2005, DOI 10.1145/1101821.1101822. Full primary PDFs were not analyzed in this run. Independent mathematical review is pending.

**Next:** Investigate a charged, source-authenticated **solver-derived semantic summary interface** that preserves sharing across sensitive but algebraically equivalent children, then test on a non-affine established hard family. Prove the child/join generation and all-phase native resources without assuming an oracle. P versus NP OPEN.
