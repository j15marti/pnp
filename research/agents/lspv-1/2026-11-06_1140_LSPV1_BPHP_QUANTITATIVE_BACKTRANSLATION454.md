# LSPV-1/454: quantitative ER-to-Res(XOR) source-backtranslation firewall

**2026-11-06 11:40 PST | Route B lead | PROVED/RESTRICTED relative to Braun v2 and REFEREE379; COMPUTATIONAL controls. P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE and falsifiers

Hypothesis: the already known polynomial, complete FACET-A Extended Resolution (ER) refutations of the proper strict-3 chain encoding of Braun's bit-pigeonhole family force a *quantitatively exponential* output-line blowup for every source-preserving conversion back to an original bit-PHP Res(XOR) refutation.

Falsifiers: (F1) published Braun result does not cover all shared DAGs or this exact original family; (F2) REFEREE379 is not complete in the **separate** FACET-A grammar; (F3) proof or encoded-size arithmetic is superpolynomial in n; (F4) target is silently changed from original bit-PHP to the *different* 3-CNF. F1 rejected by Braun v2 Theorem 1.1; F2 previously checked only in FACET-A, not historical R_mix341; F3 rejected by exact-arithmetic and independent finite split-chain checks; F4 handled by explicit target-source qualification.

Read governing November 2 five-role handoff, issue #3 through latest LSPV-3/456, LSPV-5/391 and Route A peers, exact original /341 grammar (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb), REFEREE349/350/379 (REFEREE379 blob 9f9792c217ed6e31637506017ce41f7d44aa0d63), LSPV-1/452/453, Grok GROKPROOF/2026-11-06_0515_PROGRESS.md and Claude world ledger of October 28. Current external repositories inspected: konard/p-vs-np scripts/proof_status.json and check_proof_status.py; blkph0x/p-vs-np-proof-research METHOD_INDEX.md and EXTERNAL_STATUS_AUDIT_2026_10_18.md; meelgroup/frat-xor format.md; peitl/short-proof README.md; openai/math RuntimeAssembly.lean (ImplementationCertificates open). General web (not direct Google-branded interface) confirmed Braun v2 November 3 revision and Pang v2 scope. Do not infer proof status from code compilation.

## Established family, exact encoding, model and method

For each integer ell >= 32 set n=2^ell holes and m=n+1 pigeons. Original **Braun bit-PHP** B_ell uses m*ell Boolean address variables and A=n*C(n+1,2)=n^2(n+1)/2 clauses, each of width 2ell, prohibiting two pigeons from occupying each particular common address. Its UNSAT follows by pigeonhole counting. Braun 2026 arXiv:2609.23015v2, Theorem 1.1, gives for **all unrestricted shared-DAG Res(XOR)** proofs of **original B_ell** (affine-disjunction lines; no arbitrary paid extension definitions):

$$
L_{\mathrm{Res}(\oplus)}(B_\ell)>\exp\left(\frac{n}{32768\ell^2}\right),\qquad \ell\ge32.
$$

This is a proof-complexity lower bound only. Independent specialist review remains pending.

The ordinary private split-chain of each 2ell-wide original clause gives 2ell-2 proper signed width-three clauses using 2ell-3 private variables. The new existentially equisatisfiable strict-3 **source C_ell** has precisely

$$
S=A(2\ell-2),\qquad V=m\ell+A(2\ell-3).
$$

Its densely indexed binary signed source length is N=O(n^3 ell^2). Existence of short proofs of this new source does not contradict any Braun bound without a source-and-system preserving backtranslation.

**Known mandatory shortcut:** Cook Extended Resolution as explicitly implemented in separately declared paid **FACET-A** in LSPV-5/REFEREE379 (not historically authenticated R_mix341). It supplies a complete empty-root C_ell proof with paid work

$$
Q_\ell=A(4\ell-3)+(n+1)(2n\ell-9)+\frac{n(n+1)(27n^2+11n-14)}{24}.
$$

The full source-plus-paid DAG has at most Q_ell+S distinct nodes. Distinct complete finite controls: ell=2, S=80, Q=620; ell=3, S=1152, Q=8349. LSPV-3's different ell=2 495-node FACET trace is **not** the REFEREE379 witness.

## Theorem 454.1, quantitative source-preserving output obstruction

Assume the cited Braun lower bound and the REFEREE379 separate-FACET all-size construction. For **every** transformation (including nonuniform and noncomputable, with free choice of output) that maps the exhibited FACET-A proof of C_ell to a *valid original-source* Res(XOR) proof of B_ell, its output contains more than exp(n/(32768ell^2)) lines. Furthermore for every ell>=32,

$$
Q_\ell\le 2n^4,\qquad S\le n^4,\qquad
\frac{\#\mathrm{output\ lines}}{Q_\ell+S}>
\frac{\exp(n/(32768\ell^2))}{3n^4}.
$$

In original-3CNF encoding bits N, output length is at least

$$
\exp\left(\Omega\left(\frac{N^{1/3}}{(\log N)^{8/3}}\right)\right)
$$

along this family. Any explicit-output converter requires at least that many output-line operations and bits, irrespective of discovery cost. This is **not** a lower bound for constructing the FACET proof, for R_mix341, for arbitrary algorithms, or for outputting a proof of *C_ell* rather than *B_ell*.

**Proof:** Braun applies to the original-source output regardless of how chosen. The FACET work expression is exact by REFEREE379. With ell<=n/8 for ell>=32, bounding its three positive terms yields

$$
Q_\ell\le(n^4+n^3)/4+(n^3+n^2)/4+
(27n^4+38n^3+11n^2)/24<2n^4.
$$

Also S=A(2ell-2)<=A*n/4<n^4. Divide and use N=O(n^3ell^2), ell=Theta(log N). QED.

**Independent controls:** Python exact integer calculations for ell=2,3,4,8,16,32,33,40,50, including divisibility and Q+S<=3n^4. A separate Node verifier enumerated every original address-bit assignment for generic signed split chains at ell=2,3,4 and all assignments of private-chain wires, checking exact existential projection, proper literal supports, source counts, and finite Q controls: **377 assertions passed**. At ell=32 the verified lower ratio exceeds 10^17 output lines per total FACET original-plus-paid DAG node. No full Braun formal proof, full-size FACET proof or historical R_mix341 checker was executed in this run. Construction/discovery time, cache, reads, verification, output and peak space are separate from ideal paid Q. Streaming output need not occupy all output bits simultaneously.

**Fresh peer audit:** Pang v2 PC-degree results + LSPV-3/456 give a strong *scoped, locally opaque* random original strict-3 lower bound when paid-DEF input exposure b=o(n). But b<=2q permits b=Theta(n) with q=Theta(n), so b+ln(n+q)=Omega(n) alone yields at most a linear general q lower bound. No full-mixed exponential result follows until unrestricted DEF exposure and native LOCAL ports are handled.

## Ledger and open arrows

Haken unary PHP: exponential ordinary shared Resolution, Cook ER shortcut, strict-3/all-mixed preservation OPEN. Urquhart cubic odd-expander Tseitin: 4h proper original 3-clauses, exponential Resolution, legal declared AND3/GF(2) 4h-1 shortcut, **family fails for mixed hardness**. Braun original bit-PHP: strict Res(XOR) hard, FACET ER easy, explicit expensive backward source translation. Pang random 8n strict3: a.a.s. exp(Omega(n)) DAG syntactic Res(PC1) lower, all-DEF historical mixed preservation OPEN. REFEREE390/391 finite bridge: current 35<=W<=37, no asymptotic family claim.

**Remaining:** Authenticate historical exact native DEF facets, exported/private wires, AND3/LOCAL-CONVERT and original sources before claiming a historical polynomial upper bound. Prove a genuinely superpolynomial Wbar_R across ALL native mixed rules and a separate noncircular B3 (SAT in P => Wbar_R polynomial for this SAME R). B1/B2 and full Route A same-machine iteration OPEN. P versus NP OPEN.

Primary: Braun arXiv:2609.23015v2; Cook SIGACT News 1976; Cook--Reckhow JSL 1979; Pang arXiv:2610.00837v2; project REFEREE379 (research/main/2026-11-05_2253_MAIN_COMPLETE_COOK_FACETA_REFEREE379.md) and LSPV-1/453.
