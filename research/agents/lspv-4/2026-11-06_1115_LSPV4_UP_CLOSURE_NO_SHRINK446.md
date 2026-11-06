# LSPV-4/446 | UP no-shrink on known Resolution-hard Tseitin 3-CNF
**2026-11-06 11:15 PST | Route A primary | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE: precise falsifiers
Hypothesis: native unit propagation (UP) after any logarithmic edge-variable branch on odd-charge cubic Tseitin 3-CNF still leaves source-scale children. Four falsifiers fixed first: (F1) more than 2k additional forced variables from k initial decisions; (F2) a cubic vertex forces more than one new variable; (F3) all assignments UP-close despite source Resolution width exceeding k+3; (F4) this architecture's obstruction applies to all algorithms, GF(2), ER or virtual-port input. F1/F2 are refuted by incidence proof and finite tests, F3 by width-lifting, and F4 is *false* outside this restricted architecture.

Historical predecessors: LSPV-4/437 (matching restrictions), /438 (giant components), /445 (sequential acquisition); LSPV-2/447-449 (algebraic shortcut and topology edits). New focus is full UP for *arbitrary* chosen k edge variables, not just matching or raw restriction.

## Exact published hard family and encoding
Let $G=(V,E)$ be simple cubic, $H=|V|$, $M=3H/2$. For incident edge IDs $a<b<c$ at vertex $v$, charge $\chi_v$ and $p,q\in\{0,1\}$, the four original proper strict signed 3-CNF clauses are
$$
C_{v,p,q}=\ell_p(x_a)\vee\ell_q(x_b)\vee\ell_{p\oplus q\oplus1\oplus\chi_v}(x_c),\qquad
\ell_0(x)=x,\quad\ell_1(x)=\neg x.
$$
This *exactly* encodes the local XOR equation. There are 4H clauses, 12H signed literal occurrences and M original edge variables. With fixed-width variable IDs of $w=\lceil\log_2(M+1)\rceil$ bits, source literal body is $12H(w+1)$ bits plus $O(H)$ boundaries, $N=\Theta(H\log H)$. Source graph authentication is separately charged.

On *growing odd-charge cubic constant-expander families* satisfying the published graph-expansion assumptions, standard shared-DAG **ordinary Resolution** requires minimum width $W_{\mathrm{Res}}(F_H)=\Omega(H)$ and exponential proof size (Urquhart 1987; Ben-Sasson/Wigderson 2001). This does NOT transfer to historical mixed $R_{\mathrm{mix341}}$, Res(XOR), Cook Extended Resolution or unrestricted SAT algorithms. Authenticated componentwise GF(2) parity is a polynomial shortcut; finite small graphs below are not certified asymptotic expanders.

## Lemma 446.1: schedule-independent UP forcing bound (PROVED/RESTRICTED)
Let $G$ be any simple $\Delta$-regular graph, $\Delta\ge3$, with exact parity-blocking width-$\Delta$ CNF at each vertex. Fix any k distinct edge variables. Ordinary original-clause UP, stopped upon conflict or at a fixed point, makes t additional distinct forced edge assignments. Then
$$
(\Delta-2)t\le 2k,\qquad t\le\lfloor 2k/(\Delta-2)\rfloor.
$$
**Proof:** A vertex can force a new edge only once its other $\Delta-1$ incident edges are fixed, and then all $\Delta$ are fixed. It cannot be the triggering vertex of a second *new* assignment. The t forces have t distinct triggering vertices, accounting for $\Delta t$ fixed incidences. Each of the k+t fixed edges has at most two endpoints, so $\Delta t\le2(k+t)$. Rearrange. The argument applies to *every* legal propagation schedule even when a conflicting branch stops early. QED.

For cubic graphs $t\le 2k$. The $k+t\le3k$ assigned edges touch at most $6k$ vertices. **At any UP-open fixed point**, at least $4\max(0,H-6k)$ original signed three-literal clauses remain *literally unchanged*. When $k=o(H)$, the ordinary explicit residual serialization is $\Omega(H\log H)=\Omega(N)$ bits. Restriction $\Delta\ge3$ is essential: one fixed edge on a consistent degree-two parity cycle may propagate around the entire cycle.

## Lemma 446.2: width guarantees an open branch (PROVED/RESTRICTED)
For UNSAT source CNF F with source width at most $w_0$, choose any k distinct variables. If UP contradicted on every full assignment $\alpha$ to those variables, its branch-local unit refutation can be lifted to a derivation of the k-literal decision-conflict clause $D_\alpha$ from the *original source*, with width $\le k+w_0$. Do this for all $2^k$ branches, pairing and resolving complementary conflict clauses until empty, discharging **all AND cases**. Resolution with admissible weakening can be normalized to ordinary Resolution without width increase. Thus
$$
W_{\mathrm{Res}}(F)>k+w_0
\ \Longrightarrow\
 \exists\alpha\in\{0,1\}^k:\mathrm{UP}(F|_\alpha)\text{ is open}.
$$
On the published odd-charge cubic expander sequence, $W_{\mathrm{Res}}=\Omega(H)$. For $k=\lceil(3/5)\log_2N\rceil$, eventually $W_{\mathrm{Res}}>k+3$, so **at least one** UP-open branch retains $4(H-6k)=\Theta(H)$ unchanged ternary clauses, with ordinary length $\Omega(N)$. This does **not** imply all $2^k$ branches survive or $\Omega(2^kN)$ total materialization.

## Restricted compiler obstruction and cost audit
The **specific** compiler that (i) selects k original edge variables, (ii) applies UP on only original parity clauses, (iii) writes every open full ordinary CNF child to a **writable work tape**, then (iv) calls an unchanged guest on that child, must physically allocate $\Omega(N)$ work positions on some input. Its local peak exponent $\rho\ge1$, violating proposed $s'\le\max(1/2,s/2)$ when $s<2$. Materializing solely to a write-only output charges $\Omega(N)$ output operations, not work-tape space by itself. Virtual indexed source ports may avoid work allocation but do not automatically shrink the guest's $N$-bit logical input or its runtime. Algebraic shortcuts remain valid and can circumvent this particular architecture.

A fully charged compiler must separately account for malformed parsing, source and graph authentication, failed policy search, source/index/head reads and erasure, UP passes, child materialization or every virtual-read calculation, conversion, output, guest execution, ancestor/child simultaneous buffers, caches, reference/retrieval costs, branching joins and recomputation. Those phases are absent in this finite experiment, **not free** in the universal target. Preserve $s'\le\max(\rho,\eta,\lambda,\lambda s)$, and required $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$ on **one same FLMV indexed random-access machine**. Conditional numerical FLMV margin at $(6/5,1/2)$ remains $1/90$; the universally iterable all-input transformation is OPEN.

## Independent computational controls and correction
Original strict signed 3-CNF producer on K4, cube, Petersen, Heawood, both SAT even-charge and UNSAT odd-charge: all distinct edge subsets/assignments at $k\le3$ (K4 $k\le4$): **36,272** cases, **35,496 open**, **776 conflicting**. Every case checked t<=2k, untouched original clauses; 3,652 SHA-256 source-hashed raw samples, malformed signed-facet rejection, small exhaustive SAT controls and degree-two eight-cycle countercontrol. Independent Node graph-parity implementation checked all 36,272 and 3,652 sampled original-source SHA-256 hashes, **82,187 assertions PASS**.

**Hostile schedule correction:** Original-clause scan and vertex-driven UP counted respectively **26,800** and **26,544** total force events. On a contradictory K4 branch with decisions on edges (1,2,4,5)=(0,0,0,1), one legal schedule forces edge 3 then discovers conflict while another discovers conflict first. Final outcomes agree and *open* fixed-point assignment states agree. Counts before *conflict* are schedule-dependent; the theorem's t<=2k is not. These host-language finite tests are not native FLMV time-space executions or certificates of asymptotic hardness.

## Source continuity and publication scope
Read governing Nov-2 handoff, current issue #3, AGENTS.md SHA 19656af1, CODEX.md SHA 754999f5, research skill SHA b8df83a7; actual LSPV-4/437, /438, /445; LSPV-2/447-/449 and handoffs; Grok file GROKPROOF/2026-11-06_1617_PROGRESS.md SHA b931933c and Claude file research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex SHA 9a5b05d6. Both requested external repositories inspected: konard/p-vs-np scripts/proof_status.json SHA 93b77ed3, DETAILED_SOLUTION_PLAN.md SHA 19450e38; blkph0x/p-vs-np-proof-research METHOD_INDEX.md SHA 18d693ea, INDEPENDENT_AUDIT.md SHA b30515cc, tseitin_expander_lab/README.md SHA 58ba565b. Additional code: CNFgen tseitin.py SHA 4bb5fd19, FRAT-XOR README SHA 38a137bc, openai/math README SHA cc5b0a03. No external checkout/build, Lean execution or separate Google-branded search. Root main.tex SHA ab900e0e665f5fba2dc88d38e6931c9000f08da7 returned **zero readable bytes** and was not edited. Exactly five research tasks, schedules, ownership and historical native weights unchanged.

Primary references: Urquhart, *Hard Examples for Resolution*, JACM 34(1) (1987), DOI 10.1145/7531.8928; Ben-Sasson/Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, JACM 48(2) (2001), DOI 10.1145/375827.375835; FLMV, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6) (2005), DOI 10.1145/1101821.1101822.

**Advance:** schedule-independent 2k UP forcing bound + width-open branch + specific writable-child compiler obstruction. **Verification:** elementary proofs, separate finite implementations, hostile countercontrols; independent mathematical peer review pending. **OPEN:** universal recursively iterable same-machine SAT contraction, mixed-calculus $W_{\mathrm{mix341}}$ lower bound and B3. **P versus NP OPEN.**
