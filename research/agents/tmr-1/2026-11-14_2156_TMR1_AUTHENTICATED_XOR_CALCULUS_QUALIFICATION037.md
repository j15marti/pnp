# TMR-1/037: Exact source-bound XOR proof price and sound total-calculus qualification

**2026-11-14 21:56 PST | AUTHXOR061 | PNP Machine Model Lead**

**Status: PROVED/RESTRICTED, peer mathematical review OPEN.** Tests COMPUTATIONAL. No unrestricted SAT time lower bound or P-versus-NP proof.

## Candidate and pre-registered falsifiers

**Candidate:** TMR-1/036's native ordinary-Resolution transfer obstruction is calculus-specific. Define a different fully source-authenticated calculus with XOR equations and independently qualify a sound, complete tagged calculus for all CNFs in its declared proper-three-CNF grammar. Establish an **exact** price theorem for connected odd-charge Tseitin instead of importing the exponentially larger ordinary-Resolution lower bound.

Falsifiers fixed before source search: (1) incomplete parity block falsely authenticated as an XOR equation; (2) source-ID magnitude causes exponential bitset allocation; (3) SAT input yields an accepted contradiction or some mandatory vertex source is skipped; (4) one abstract proof-rule cost is silently treated as one actual finite-alphabet Turing-machine transition or an unrestricted SAT lower bound.

Previous LSPV/MAIN work, TMR-1/036, and TMR-3/036 already established expander-Tseitin Resolution hardness, polynomial-time authenticated Gaussian elimination and a machine-to-Resolution model-transfer no-go. These are not claimed as new. **New here:** a distinct globally sound and complete disjoint proof authority, an exact shared-DAG 2H proof-price theorem for its XOR mode, and two independent executed checker controls.

## Exact sources and input measures

[1] Ben-Sasson and Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, JACM 48(2), 2001, Definition 4.1, Lemma 4.2, Theorem 4.4 and Corollary 4.5, printed pp.155-156, https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf . A connected cubic **edge expander** with H vertices and odd charge has a proper 3-CNF Tseitin contradiction with 4H original clauses and 3H/2 edge variables. Its **ordinary shared-DAG Resolution** proof size is $2^{\Omega(H)}$. The published bound does not encompass XOR inference. The original PDF was checked by page screenshot.

[2] Laitinen, Junttila and Niemela, *Conflict-Driven XOR-Clause Learning* (2014), introduction pp.1-2, https://arxiv.org/pdf/1407.6571 . This primary source distinguishes polynomial GF(2) elimination from expensive parity CNF reasoning and motivates a different proof authority. No specialized theorem from this paper is required in our new counting proof. Original PDF checked by page screenshot.

[3] Original repository reports: TMR-1/036 source-authenticated Tseitin Resolution transfer, TMR-3/036 arbitrary-incidence XOR3 fast-path and dense-ID repair, TMR-2/036 nonlinear minimax tariff, TMR-4/037 paid Bellman envelope, TMR-5/032 asymmetric fusion falsifier and original LEAD-0029 October Lipschitz audit.

Let H be graph vertices, E=3H/2 edge variables and L the **encoded original CNF bit length**. Under the standard graph vertex/edge numbering, L is Theta(H log(H+2)) for the signed literal-ID grammar. It is not the MCSP full truth-table length N=2^n. Rule-step price is not physical machine time.

## Qualified systems and grammar

For a connected **simple cubic graph** G, each vertex v has three edge variables and one parity equation

$$
\bigoplus_{e\ni v}x_e=b_v.
$$

Its exact original 3-CNF source group comprises the **four distinct** three-literal clauses excluding the violating local assignments. The source parser derives this group from the actual clause bytes, not supplied graph, charge, advice or external oracle. The authenticated subset grammar requires the same three distinct variable IDs within each group, precisely four complementary sign patterns for one parity, and no missing or extraneous clause. Ordinary non-XOR proper three-CNFs remain valid in the RES mode of the new total authority.

Define **Q-XOR3** as a fixed source-bound shared-DAG proof calculus. Its configurations include immutable input, authenticated grouped clauses, derived row DAG, source-provenance ledger, paid-event history and a terminal goal flag. Complete legal native transitions are:

1. SOURCE(i), proof price 1: append equation authenticated by the complete four-clause source group i.
2. ADD(j,k), proof price 1: append GF(2) sum of two existing lines; their earlier proof work remains shared and counted once.
3. HALT(j), proof price 1: legal only if existing line j is the explicit zero-equals-one contradiction.

Zero-cost closure is identity; Q-XOR3 has **no native free rule**. Unknown operations outside this specifically qualified proof calculus remain MAY in general SAT machines.

Define a separate **Q-TOTAL-XOR-RES**, the *disjoint tagged union* of Q-XOR3 and ordinary Resolution. A proof selects either XOR mode above, or RES mode with original-clause SOURCE, complementary-pivot RESOLVE and empty-clause HALT, each price 1. Cross-mode inference is forbidden. On **all encoded proper 3-CNFs in its declared canonical grammar**, RES mode is sound and refutationally complete by the standard Resolution completeness theorem; no polynomial bound on its proof length is asserted. XOR mode is also sound on the authenticated subclass. Therefore Q-TOTAL-XOR-RES is sound and complete for UNSAT over **this entire declared ordinary proper-three-CNF input language**, with separate tags. It is a NEW authority. It does not repair or relabel /341 (FAIL on its full accepted language) or /386 (RESTRICTED).

## Theorem AUTHXOR061-A: exact shared-DAG cost

For **every connected simple cubic graph** on H vertices, with odd total vertex charge, the exact minimum Q-XOR3 proof cost is

$$
\boxed{\overline W_{\mathrm{Q-XOR3}}(F_G)=H+(H-1)+1=2H.}
$$

**Upper bound.** SOURCE all H vertex equations, use H-1 sequential ADD operations to sum them, and HALT on zero-equals-one. Each edge occurs at two vertices and cancels; odd total charge yields one. Exactly 2H paid nodes.

**Lower bound with arbitrary DAG sharing.** Label each derived equation by the vector of its original SOURCE-row provenance over GF(2). The left kernel of a connected graph's vertex-edge incidence matrix consists precisely of zero and the all-ones vector. Indeed, to eliminate an edge (u,v), its two vertex source coefficients must satisfy z_u xor z_v=0; connectedness makes z constant. The zero provenance has zero right-hand side. Therefore a final equation zero-equals-one must have the all-ones provenance and includes **each of H distinct vertex SOURCE nodes** in its transitive dependency DAG.

Let s be the number of SOURCE nodes in that transitive DAG and a its binary ADD nodes. We have s>=H. The undirected operand graph of all nodes contributing to the contradiction is connected. It contains s+a vertices and 2a incoming operand arcs, counting multiplicity, so 2a>=s+a-1. Thus a>=s-1>=H-1. One paid HALT is unavoidable. The total is at least H+(H-1)+1=2H. This already allows sharing, repeated reads and arbitrary reconvergence. QED.

**Theorem AUTHXOR061-B.** If an authenticated complete three-XOR CNF has m source groups and its GF(2) system is inconsistent, an inconsistent subset of at most m source equations exists, as witnessed by elimination. SOURCE that subset, ADD it, then HALT. A valid Q-XOR3 proof of price at most 2m exists. Conversely a satisfiable authenticated group system cannot yield an accepted contradiction because SOURCE and ADD preserve truth under any satisfying assignment. Thus Q-XOR3 is sound and complete **only on its authenticated XOR3 domain**.

**Theorem AUTHXOR061-C.** The globally sound/complete Q-TOTAL-XOR-RES has proofs of price at most 2H on the standard cubic expander Tseitin family, even though ordinary Resolution requires $2^{\Omega(H)}$ lines by [1]. Merely strengthening a proof system into a sound/complete source-bound authority does **not** transfer the Resolution lower bound. Exact 2H is asserted for the XOR-only mode, **not** as a lower bound on the disjoint union.

## Authentic tariff rows and machine-transfer limitations

Six fully specified native rule rows appear in the separate machine-readable tariff JSON: XOR SOURCE/ADD/HALT and RES SOURCE/RESOLVE/HALT, all proof price 1, with no native zero-cost transitions. These are **proof-rule tariffs**, not a seven-component all-machine discharge matrix. Arbitrary physical Turing machines may parse, compute rows, share, recompute, cache, read input and process several logical obligations within one transition. The proposed general lambda vector and every genuine machine transition remain OPEN.

The conditional telescoping implication is valid only **within the same system**: if Phi(C)-Phi(C')<=w(C,C') for every authentic transition and every completed goal has Phi<=0, then every completed path has cost at least Phi(C0). But on this particular family, any valid Q-XOR3 initial potential is bounded by the genuine cheap 2H proof. In an actual fixed total SAT machine, the source authentication and Gaussian elimination have polynomial bit costs (TMR-3/036); no constant-price abstract rule is called a unit-cost TM transition.

The independent family bridge,

$$
\mathrm{SAT}\in\mathrm P
\Longrightarrow
\exists C,d,H_0\ \forall H\ge H_0:
\overline W_R(F_H)\le C(L_H+1)^d,
$$

holds on this special Tseitin family for Q-TOTAL-XOR-RES **without even assuming SAT in P**, so the family cannot yield P != NP with that proof calculus. The corresponding universal machine-to-native-Resolution bridge was falsified in TMR-1/036. For an unknown hard nonaffine family or arbitrary correct SAT deciders the bridge and superpolynomial initial potential remain OPEN.

## Actual independent tests and hostile controls

**Exactly published and executed V8 source**: experiments/tmr/tmr1_authxor061_native.js. **Exact native execution output**: results/raw/tmr/2026-11-14_2156_TMR1_AUTHXOR061_V8_RAW.json. V8 completed **22,624 assertions, zero failures**. It authenticated all four-clause source truth tables on 10 odd/even cubic-prism instances H=6,8,10,12,14, independently built and checked GF(2) refutations and exact 2H proof prices, checked all subsets for the connected-kernel condition when H<=12, and brute-forced small source CNFs. It verified a non-XOR all-eight-clauses contradiction with a disjoint ordinary Resolution 8-SOURCE/7-RESOLVE/1-HALT certificate.

The local original native CPython implementation also ran **11,784 assertions, zero failures**; it separately exercised sparse source IDs above $2^{115}$ and strict ASCII parsing. That code is not claimed byte-identical to the published V8 source and its local stdout is not the published V8 raw. The V8 source operates on normalized proper clause arrays, not a native physical tape. The finite prism graphs are **not claimed to be expanders**. Exact 2H for any connected cubic graph rests on the proof, not finite experiments.

**Smallest grammar falsifier tested:** three of four parity-zero clauses plus all four opposite-parity clauses on one variable triple form a **satisfiable seven-clause CNF**. A careless incomplete-block XOR extractor would unsoundly infer both parities. The authenticator rejects it. Even-charge graph instances have satisfying assignments. Invalid source indices, premature HALT and cross-mode inference are rejected. All-eight-clauses ordinary contradiction is rejected by the XOR authenticator but accepted by the RES verifier. Shared ADDs remain legal and are included in the exact lower-bound graph argument.

## Dependency map and peer assignment

| Arrow | Status | Action |
| --- | --- | --- |
| Full source XOR-block meaning and Q-XOR3 soundness | PROVED/RESTRICTED | Peer audit exact grammar |
| Shared-DAG exact 2H price on connected odd cubic graphs | PROVED/RESTRICTED | TMR-4/TMR-5 review |
| Disjoint Q-TOTAL-XOR-RES globally sound/complete within declared proper-three-CNF grammar | PROVED/RESTRICTED | Verify mode separation |
| Ordinary cubic-expander Resolution exponential size | KNOWN THEOREM | Do not import to affine calculus |
| Native Resolution lower bound transfers after XOR extension | FALSIFIED/RETIRED on family | Explicit cheap 2H derivation |
| Full arbitrary-machine rule tariff and fusion multiscale gap | OPEN | TMR-2/3/4 |
| Same fixed total SAT decider general transfer | OPEN | TMR-1/TMR-5 independent gate |

**Next:** TMR-2 seek nonlinear residual after the exact affine quotient; TMR-3 cost physical tape/source and message movements; TMR-4 audit shared-DAG 2H and source authentication; TMR-5 challenge malformed controls and cross-mode scope. TMR-1 should next qualify a nonaffine source-bound transition system and seek an actual new same-machine transfer arrow, not simply rename P != NP.

**Recovery and publication:** Controlling fusion directive SHA 54c9177fc211dfca6c94d89d6ebbf3f3908809d6 read FIRST, then 2026-11-13 replacement, full proof1, proof2 authentic Git blob 930c5eeddafce656717f28055a7a9a755f44737c (1,051,196 chars), root main.tex Git blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 (2,545,859 chars), AGENTS/CODEX/research skill, five current TMR handoffs, issue #3 through TMR-4/037, and relevant original reports. The local container lacked the repository checkout, so repository preflight.py was not executed; authentic remote file/blob preflight was performed. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex unchanged under TMR-5 ownership. Five schedules untouched. /341 FAIL and /386 RESTRICTED preserved. P versus NP OPEN.

END_OF_REPORT::TMR1::037::2026-11-14_2156_PST
