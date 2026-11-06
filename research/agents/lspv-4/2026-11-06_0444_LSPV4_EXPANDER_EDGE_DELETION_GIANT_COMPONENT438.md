# LSPV-4/438 | Expander giant-core persistence under logarithmic SAT branching

**2026-11-06 04:44 PST. Route A primary. PROVED/RESTRICTED structural result; COMPUTATIONAL finite controls. Universal FLMV contraction and P versus NP OPEN.**

## IDEA, falsifiers, correction
Hypothesis: LSPV-4/437's failure of literal-preserving branching to produce small SAT children should persist when the selected edge variables are **arbitrary, possibly adjacent**, if the published 3-CNF source is an odd-charge cubic Tseitin formula on an edge expander. Four falsifiers: F1 removing \(k\) edges separates balanced components; F2 untouched source clauses change under restriction; F3 a known GF(2) shortcut defeats claims of genuine SAT computation hardness; F4 guest-size calculations omit supplied source bytes, and any source authentication or connectivity execution cost. F1 and F2 are ruled out in the restricted theorem below; F3 is affirmed and retained as the strongest legal upper control; F4 requires explicit resource restrictions.

## Published family and encoding
Let \(G=(V,E)\) be a connected simple cubic graph with \(H=|V|\) even and \(M=3H/2\). Each edge has an input bit \(x_e\); each vertex has charge \(\chi_v\). With incident edge IDs \(a_v<b_v<c_v\), \(\ell_0(x)=x\), and \(\ell_1(x)=\neg x\), use exactly the four strict 3-CNF clauses per vertex

$$
C_{v,p,r}(\chi)=\ell_p(x_{a_v})\lor\ell_r(x_{b_v})\lor\ell_{p\oplus r\oplus1\oplus\chi_v}(x_{c_v}),\quad p,r\in\{0,1\}.
$$

These assert \(x_{a_v}\oplus x_{b_v}\oplus x_{c_v}=\chi_v\). There are \(4H\) original clauses and \(12H\) source literal occurrences. When \(G\) is connected, odd total charge is UNSAT and even charge SAT, by binary incidence rank \(H-1\). This family is already strict 3-CNF, without a 3-CNF conversion. On **suitable growing cubic expander graphs**, odd-charge Tseitin contradictions have \(2^{\Omega(H)}\) proof-size lower bounds against **ordinary unrestricted shared-DAG Resolution** [1,2], not arbitrary machines, ER, or full historical \(R_{\mathrm{mix341}}\).

The audited input packet contains an 8-bit marker, unary \(H\), unary \(M\), \(H\) charge bits, \(3H\) ordered incidence IDs of width \(w=\lfloor\log_2 M\rfloor+1\), and all \(12H\) original signed literals with \(w+1\) bits each. Its **charged** bit length is

$$
N=8+(H+1)+(M+1)+H+3Hw+12H(w+1)=\Theta(H\log H).
$$

This packet has *supplied metadata*, not an uncharged oracle for arbitrary raw CNF. The original strict CNF literal body alone has \(12H(w+1)\) bits. LSPV-2/441 separately establishes a standard-\(L\) source-only canonical-family recognizer, but does not prove a native FLMV \(N^{11/10}\) time bound.

## Theorem 438.1, giant core for ANY \(k\) edge deletions (PROVED/RESTRICTED)
Assume a lower edge-expansion constant \(h>0\): \(|\delta_G(S)|\ge h|S|\) for each nonempty \(S\subseteq V\), \(|S|\le H/2\). Delete **any** set \(D\) of \(k<hH/3\) edges. The graph \(G-D\) contains a **unique** component \(C_{\mathrm{big}}\) with more than \(H/2\) vertices and

$$
|V\setminus C_{\mathrm{big}}|\le k/h,\qquad |C_{\mathrm{big}}|\ge H-k/h.
$$

*Proof.* If all components had size at most \(H/2\), their union could be partitioned to give a union \(S\) of whole components with \(H/3\le |S|\le2H/3\): add components until crossing \(H/3\); if the last one overshoots \(2H/3\), that component alone lies between \(H/3\) and \(H/2\). All original edges crossing this union are in \(D\), hence at most \(k\). Applying expansion to the smaller of \(S,V\setminus S\) yields at least \(hH/3>k\), contradiction. Thus there is a unique component larger than \(H/2\). For its complement \(T\), \(|T|\le H/2\) and \(\delta_G(T)\subseteq D\), so \(h|T|\le k\). QED.

For a fixed family with \(h\ge h_0>0\) and \(k=\lceil(3/5)\log_2N\rceil\), eventually \(k<h_0H/3\), so EVERY such deletion leaves \(H-O(\log N)\) vertices in one component. Edge choices may be adaptive or adjacent; neither matching nor an artificial branch-choice restriction is required. In particular, at most \(2k\) vertices in the giant component can be incident to fixed edges. Thus at least \(H-k/h-2k\) giant-component vertices retain all four original 3-clauses, giving at least \(4(H-k/h-2k)\) unchanged ternary clauses **inside the unique giant component**, prior to further propagation.

## Theorem 438.2, exact original signed-clause restriction (PROVED/RESTRICTED)
For any partial edge assignment, let \(r_v\) be the number of assigned incident edges at \(v\). Before any further propagation, the four source clauses at vertex \(v\) leave **exactly**: when \(r_v=0\), four ternary clauses; when \(r_v=1\), two binary clauses; when \(r_v=2\), one unit clause; when \(r_v=3\), either one empty clause or none. This follows from restricting the parity equation, whose remaining forbidden rows number \(2^{(3-r_v)-1}\) for \(r_v<3\).

At most \(2k\) vertices meet the selected edges. Therefore every restricted source has at least

$$
4(H-2k)
$$

**unchanged original ternary clauses**. This holds for arbitrary edge selection **before** additional unit propagation or algebraic preprocessing. Adjacent choices can create units and propagate; the old matching result LSPV-4/437 is the special case \(r_v\le1\) with exactly \(4(H-2k)\) ternary and \(4k\) binary clauses and no units. The remaining graph-component core and unchanged source clauses both have \(\Omega(N)\) explicit original-literal encoding size for \(k=O(\log N)\). This falsifies the proposed \(N^{1/2}\) guest-size premise for **direct restriction plus graph component splitting**, NOT for every legal algorithm.

## Strongest legal shortcut and proof-DAG qualification
For assigned edges \(D\) with bits \(\alpha_e\), define \(\chi'_v=\chi_v\oplus\bigoplus_{e\in D,\ v\in e}\alpha_e\). The residual parity system is satisfiable exactly when each component of \(G-D\) has even \(\chi'\) parity. Every fixed edge contributes to two vertex charges, so \(\bigoplus_v\chi'_v=\bigoplus_v\chi_v\). Thus *every branch of an odd-charge original formula remains UNSAT*, and a suitably authenticated GF(2) algorithm can decide without enumerating any branches. This is an **upper-bound control** and prevents any all-algorithm-hardness inference. The native historical \(R_{\mathrm{mix341}}\) proof and paid GF(2) certification need their own authenticated rule derivations. No split/discharge/weakening rule is inserted; when a legal split is used, UNSAT requires every case, shared inference nodes are paid once, and contextual assumptions cannot leak.

## Charged resource consequences
For \(q=2^k=\Theta(N^{3/5})\), literal-preserving *explicit* children each contain \(\Omega(N)\) original source bits, so printing \(q\) children costs \(\Omega(qN)=\Omega(N^{8/5})\) bit outputs. One complete work-tape-resident child has \(\Omega(N)\) peak physical workspace. Lazy read-only sharing can avoid copies but cannot call the guest on an actual \(N^{1/2}\)-bit CNF without a separate correct shrink compiler. A straightforward sequential guest simulation yields an **upper bound** of \(O(qN^t)\) if the guest is \(O(N^t)\), NOT \(O(qN^{t/2})\); it is not a runtime lower bound on this recognizable family.

Source parsing and external metadata, source/index/head reads, failed decomposition policies, descriptor acquisition, guest fallback, cache references, recomputation, component detection, output, and simultaneous peak high-water must all be charged. LSPV-2/440 proves a near-linear checker only when an annotation is ALREADY supplied; LSPV-2/441 source-only logspace uses Reingold with unspecified polynomial time exponent. The host finite checker uses linear-memory DSU and is **not** an FLMV execution. Logical shared proof-DAG minimum, parallel critical depth, and realizable machine time/space schedules are separate. The conditional desired recurrence remains \(t'\le\max(11/10,3/5+t/2)\) and \(s'\le\max(1/2,s/2)\), with the previously established conditional FLMV gap \(1/90\) at \((6/5,1/2)\). The universally applicable transformation is OPEN.

## Reproducibility and external review
Python producer independently generated exact signed 3-CNF and examined all edge deletions of size \(k\le3\), all branch assignments, both parity charges, and exact finite edge expansion. Finite family controls: K4 \(H=4,h=2,N=252\); cube \(H=8,h=1,N=614\); Petersen \(H=10,h=1,N=765\); Heawood \(H=14,h=1,N=1277\). Total **35,792** residual branch/charge records, **2,239** giant-claim checks. A separate Node.js implementation reconstructed all records and source hashes and passed **201,895 assertions**. Hostile changed signed source literal had a different SHA-256. Full raw JSON SHA-256: \`2fa26ffcc4e8213c34ca0ae00b4b6c5be0cedfad956d060586663be3362a3df0\`. These finite graphs are NOT certified growing hard expanders. No native FLMV trace.

Actual reviewed project: 2026-11-02 governing handoff; issue #3; AGENTS.md; CODEX.md; pnp-research skill; LSPV-4/437 blob \`8e200b44\`; LSPV-2/440 \`d04f60c6\`, /441 \`1ca86432\`; Grok 2026-11-06 12:20 UTC \`5c4fbf8f\`; Claude TPORT \`b7150bb9\`. External GitHub paths: \`konard/p-vs-np/proofs/complexity/README.md\` \`7ee9a11e\` (distinct one-tape model), \`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md\` \`18d693ea\` (model-specific results), \`MassimoLauria/cnfgen/cnfgen/families/tseitin.py\` \`4bb5fd19\`, \`meelgroup/frat-xor/README.md\` \`38a137bc\`, \`openai/math/README.md\` \`cc5b0a03\`. Indexed web and GitHub searches ran; Google-branded search and native FLMV execution were unavailable.

References: [1] Urquhart, *Hard Examples for Resolution*, JACM 34(1):209-219 (1987), DOI 10.1145/7531.8928. [2] Ben-Sasson & Wigderson, *Short Proofs Are Narrow*, JACM 48(2):149-169 (2001), DOI 10.1145/375827.375835. [3] Reingold, *Undirected Connectivity in Log-Space*, JACM 55(4) (2008), DOI 10.1145/1391289.1391291. [4] FLMV, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6):835-865 (2005), DOI 10.1145/1101821.1101822.

**Advance:** generalizes LSPV-4/437 from matching branches to any \(O(\log N)\) edge-variable restrictions under a certified expansion premise for direct component-splitting. **Verification:** complete combinatorial proof, independently recomputed finite controls, no native machine trace. **Remaining:** genuine shrinking, recursively iterable all-input same-machine transformation with fully charged costs; Route B all-rule mixed minimum and noncircular B3. **P versus NP OPEN.**
