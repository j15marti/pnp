# LSPV-1/443: SAT-preserving syntactic Tseitin transform erases ordinary Resolution hardness
**2026-11-06 03:00 PST | Route B lead | PROVED/RESTRICTED construction, COMPUTATIONAL finite tests; full mixed bounds, B1/B2/B3, P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE
Hypothesis: a uniform, both-label-preserving, malformed-aware **all-input** map can turn a published Resolution-hard proper 3-CNF family into short strict-Resolution instances, falsifying the inference that polynomial-size SAT equivalence alone preserves proof hardness. This is a focused transfer falsifier, not a new hard candidate.

Falsifiers established before search: (F1) signed original Tseitin clauses do not uniquely expose graph and charges syntactically; (F2) SAT/UNSAT or malformed/nonfamily handling fails; (F3) target strictly oriented Resolution certificates need hidden XOR, weakening or unpaid logical nodes; (F4) result duplicates earlier work or is mistakenly promoted to mixed hardness, B3 or FLMV.

Reviewed governing five-role handoff, current issue #3, original /341 rule specification, /436, /440, /442, latest REFEREE383, actual Grok and Claude research files, primary literature, and the required external repositories. Revision: LSPV-1/436 already proved a **lower-bound-preserving signed-literal** projection for guarded Tseitin; REFEREE383 independently reproduced its legal original-coordinate mixed shortcut at $12h+2$ nodes. The present construction deliberately is **not** lower-bound preserving. The parity recognizer and circuit propagation are standard techniques, not claimed novel.

## Exact established family, theorem, encoding and shortcut ledger
**Odd cubic expander Tseitin:** Let $G=(V,E)$ be connected simple cubic with $h$ even vertices, $3h/2$ edge variables, and one local equation $\bigoplus_{e\ni v}x_e=\chi_v$ per vertex. Encode each by exactly four signed proper three-clauses excluding the wrong-parity triples. Thus $m=4h$ and binary indexed length $\Theta(h\log(h+2))$. It is UNSAT when $\bigoplus_v\chi_v=1$. For **suitable expander sequences**, Urquhart 1987 and Ben-Sasson/Wigderson 2001 establish $2^{\Omega(h)}$ **ordinary unrestricted shared-DAG Resolution** refutation-size lower bounds. Not an all-machine lower bound. The known historical semantic AND3/GF(2) /341 proof has **exact $4h-1$ minimum nodes** on bridgeless cubic graphs, so this family already fails as a full-mixed hardness candidate.

**Guarded strict 3CNF /436:** Add fresh $g,u,v$ and private $y_i$, replacing each base $C_i=(a_i\vee b_i\vee c_i)$ by $(g\vee a_i\vee y_i)\wedge(\neg y_i\vee b_i\vee c_i)$ plus the four $(\neg g\vee u^{s}\vee v^{t})$ clauses. Has $8h+4$ proper ternary clauses, $11h/2+3$ variables, and a proved **ordinary Resolution lower-bound-preserving literal projection**, not equisatisfiability alone. REFEREE383 confirms an already known source-authenticated **historical rule-level** RES/AND3/XOR refutation with $8h+3\le W_{mix341}\le12h+2$ and depth $\le5+\lceil\log_2 h\rceil$, without fresh-wire AND3, DEF, LOCAL or new rules. Historical accepted-byte checker still unavailable. The guarded family's exact full mixed optimum remains unknown.

**Haken/Cook/Braun controls:** Unary PHP is hard in ordinary Resolution but has polynomial Extended-Resolution shortcuts; bit-PHP Res(XOR) claims depend on a different proof system and encoding. Any 3CNF lower-bound transfer requires proof-specific simulation; equisatisfiability is not enough.

## Theorem 443.1: total both-label syntactic transformation
For every valid ASCII DIMACS CNF source, in deterministic polynomial time recognize **exactly** the cubic Tseitin syntax: group the four different proper width-3 clauses per support triple, check all four prohibited assignments have common parity, each edge variable occurs in exactly two triples, and the induced incidence graph is simple, connected and cubic. Recover the charge vector $\chi$ without a SAT oracle. If valid but not recognized, output the **unchanged source CNF**; for malformed encoding, return a separate malformed status, not a fabricated SAT answer. On recognized source, set $h$ charge bits $c_i=\chi_i$, compute $h-1$ two-input XOR gates $t_1=c_1\oplus c_2$ and $t_i=t_{i-1}\oplus c_{i+1}$, and force $t_{h-1}=0$. Encode each XOR by the four canonical proper ternary blocking clauses. Pad each of the $h+1$ input/output units by the four sign combinations of two new private variables.

The resulting proper 3CNF $H_3(\chi)$ has precisely **$8h$ clauses**, **$4h+1$ variables**, and $\Theta(h\log(h+2))$ bit length. Connected GF(2) incidence equations are satisfiable iff the total charge parity is even. Hence $F_{G,\chi}$ is SAT iff $H_3(\chi)$ is SAT. Identity on every other valid input preserves both labels for **all** valid CNFs. This is a uniform syntactic reduction, not a general SAT algorithm and not a same-machine FLMV shrinking-child transformation.

## Theorem 443.2: a short strict Resolution DAG
Every one of the $h+1$ padded units is recovered from its four original target clauses in **three** correctly oriented binary-Resolution steps. Each of the $h-1$ XOR gate outputs follows from the two known input units and an original defining clause in **two** Resolution steps. Odd charge yields a final outgoing positive unit opposite the fixed negative unit, resolved once to false. Exactly
$$
3(h+1)+2(h-1)+1=\boxed{5h+2}
$$
**distinct paid oriented Resolution inferences** suffice. No native XOR inference, weakening, extension, assumption-discharge, proof-search oracle, omitted AND premise or fake free source is used. This is a constructive **upper bound, not a global minimum**.

On suitable **original odd cubic expander** sources, the published ordinary Resolution lower bound is exponential in $h$, whereas the transformed target has $O(h)$ ordinary Resolution work and $O(h\log h)$ source bits. Thus there is a uniform all-input polynomial SAT-preserving transformation **without** polynomial lower-bound preservation of Resolution proof complexity. This is exactly why any purported transfer to the stronger historical mixed calculus must prove the reverse simulation direction, not merely equisatisfiability.

## Finite verification, resource and hostile-control ledger
Standard-library Python producer generated original signed K4, K3,3, cube and prism6 Tseitin sources for odd/even total charge and exhaustively checked their SAT labels through 18 edge variables. Independent Node verifier rebuilt target original clauses and checked all oriented-pivot proof nodes, topological IDs and empty-root proof. **Eight packets, 1,015 independent assertions and seven rejected hostile certificate mutations**. The Python total syntax recognizer passed **28 tests** covering graph cases, arbitrary clause orders, multiple charge choices, valid nonfamily identity, and six malformed controls.

| source | $h$ | original clauses | target clauses | exhibited odd strict RES |
| --- | ---: | ---: | ---: | ---: |
| K4 | 4 | 16 | 32 | 22 |
| K3,3 | 6 | 24 | 48 | 32 |
| cube | 8 | 32 | 64 | 42 |
| prism6 | 12 | 48 | 96 | 62 |

These small graphs are correctness controls, not certified asymptotic expander-hard examples. Full source-bound proof packet, original-byte controls, independent checker, malformed and corrupt controls and SHA checksums are in the downloadable local reproducibility archive; the compact GitHub checker is only supplementary.

Physical resources are **distinct** from ideal logical work. Source/index/head reads, parsing, clause grouping, graph verification, canonical sorting, constructing output, discovering/choosing policy, materializing all source and proof bits, reference access, checking, caching, failed policies, serialization and simultaneous peak memory must be charged. An explicit certificate requires $O(h\log h)$ bits with compact IDs, and this syntactic family transformer runs in polynomial time/space; no fixed-model FLMV exponents follow. Measured host phases: Python producer 5.68s / 96,524 KiB RSS; independent Node verifier 0.16s / 29,688 KiB; recognizer 1.09s / 96,140 KiB before two added controls. No all-phase simultaneous peak was measured. The ideal work excludes proof-search choice intentionally, actual implemented upper bounds do not.

## Sources and prior-corpus verification
Project sources actually read: historical handoff 4e29ed76, current issue #3, AGENTS.md SHA 19656af1, CODEX.md SHA 754999f5, project SKILL SHA b8df83a7, original /341 SHA c87acd11, /436 SHA 2c72bdf3, /440, /442, latest REFEREE383 SHA d15f283, Grok 2026-11-06 09:20 UTC SHA 6b32bc3, Claude 2026-10-28 ONETAPE SHA 9a5b05d. Required external method files read: konard/p-vs-np scripts/proof_status.json SHA 93b77ed3, blkph0x/p-vs-np-proof-research METHOD_INDEX.md SHA 18d693ea, meelgroup/frat-xor format.md SHA 986a21aa, tanyongkiam/cake_lpr README SHA e94f45e9, peitl/short-proof README SHA 93d2090. No source authenticates historical byte grammar, B3, or universal mixed hardness. Primary literature: Urquhart, JACM 1987 DOI 10.1145/7531.8928; Ben-Sasson/Wigderson, JACM 2001 DOI 10.1145/375827.375835; Cook/Reckhow, JSL 1979 DOI 10.2307/2273702; Cook 1976 ER pigeonhole. Direct Google-branded search was unavailable. Full project preflight could not execute without checkout; authenticated remote project instructions were read.

Root main.tex fetched with valid blob SHA but **zero readable content bytes**, so no ownership-unsafe edit. No titles, schedules, agent count, role allocation, old files, native rules or inference weights modified.

## Exact remaining OPEN transfer
Find a genuine superpolynomial minimum $\overline W_{R_{\mathrm{mix341}}}(N)$ surviving **all native mixed legal rules, shared DAGs and shortcuts**, and independently prove the noncircular SAME-fixed-calculus B3:
$$
\mathrm{SAT}\in P\quad\Longrightarrow\quad\overline W_{R_{\mathrm{mix341}}}(N)=N^{O(1)}.
$$
B1, B2, B3, and P versus NP remain **OPEN**.
