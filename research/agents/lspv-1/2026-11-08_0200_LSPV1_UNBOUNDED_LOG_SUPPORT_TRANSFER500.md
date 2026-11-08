# LSPV-1/500 | Unbounded logarithmic-support nonlinear feedback lower bound

**2026-11-08 02:00 PST | Route B | PROVED/RESTRICTED under published preprint theorem; COMPUTATIONAL finite syntactic controls; P versus NP OPEN.**

Node **[P2-L1-500]**, building on **[P2-L1-499]** and **[P2-L1-498]**. Historical **[P2-D1]**, all-rule transfer **[P2-C3]**, unrestricted minimum **[P2-B1]**, and same-calculus noncircular B3 **[P2-B2]** remain OPEN. Companion **[P1-00]**, **[P1-01]**, **[P1-03]**, **[P1-04]** remain unchanged.

## IDEA: hypothesis and falsifiers (before search)

Hypothesis: Result 499's bounded-support simulation has a uniform quantitative overhead O((b+1)2^b), not merely a constant for fixed b. Let b=b(n) be one fixed computable function of ORIGINAL variable count. The exp(Omega(n)) known random-3CNF proof lower bound survives whenever b(n)=o(n), and the same distinct calculus is polynomial-checkable if b(n)=O(log n).

Precise falsifiers: **F1** Pang Fact 7.1 secretly requires fixed t; **F2** canonical CNF bundles or resolution of eliminated variables require more than 2^{O(b)} target nodes; **F3** a purportedly legal LOCAL node can cite an unsupported global row, paid fresh definition or undischarged branch; **F4** Pang's theorem is not about the same original signed proper random 3-CNF and syntactic characteristic-two degree-one rules. F1 and F2 are refuted by exact source theorem/proof and construction below; F3 is a mandatory exclusion defining this distinct calculus; F4 was checked against the primary theorem but not independently reproved.

## SEARCH: exact sources, corpus and assumptions

Both complete root trackers fetched at initial inspection, proof1.txt SHA **96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b** (18,553 characters), proof2.txt SHA **86fb4253c55c9b2353cdd1b2f2325637e54abd23** (366,477 characters). Main-branch tracker heads must be refetched immediately before any actual update. Also read current issue #3 (1,312 comments), governing November 2 five-role handoff (blob c3889a3e514ddbd747150dcb68607013a3b2d154), AGENTS.md, CODEX.md, and .codex/skills/pnp-research/SKILL.md. Prior LSPV-1/499 report blob **3dbf42d6d79d0ea439d3a131e69480886ca4b10c**, LSPV-5/429 audit **38869202422774f11683e4e905e1605ad60f3f9d**, LSPV-3/495 one-hot shortcut **41176223e63396aade776171a848b127f3536187** read. Grok GROKPROOF/2026-11-08_0930_PROGRESS.md blob **e3e8c9657e0f2b2e0751752135cf2558e28183cf**, Claude research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex blob **95c2649b29ae7efac79e9400effffd2c3bdeb2fc** read as critical context, not unrestricted proofs.

Primary source: Shuo Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, October 24, 2026; https://arxiv.org/html/2610.00837v2 . Section 1 lists exact syntactic Res(PC_r/F_p) rules; Fact 7.1 gives O(t 2^t) derivation for *variable* t; Theorem 7.2(a) gives exp(Omega(n)) DAG-size for independent-with-replacement signed proper fixed-width random CNF of density Delta>=2^w. Our instance is w=3, Delta=8, n variables, 8n clauses, fixed p=2,r=1. The theorem is a cited preprint result, not a locally independently verified formal proof. Queries included Pang Fact 7.1 growing support, Pang random proper 3CNF Theorem 7.2, proof-system reflection Cook Reckhow and Extended Frege simulation. No separate Google-branded search or Lean kernel replay.

Required external repository content was inspected: konard/p-vs-np/scripts/proof_status.json blob **93b77ed3d8fe456f81c690035f45f07910a247f2** (shared finite-model/assumption manifests, no P-vs-NP conclusion); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob **18d693ea71dfa433370eb7afbebc3106e32f03e5** (restricted/conditional methods); meelgroup/frat-xor/format.md blob **986a21aa92b62f844ef1fce852193142c41b2b1f** (external XLRUP format, not historical grammar). These pinned blobs match the prior /499 checks. Root main.tex was not overwritten or partially edited.

## FORMALIZE: fixed calculus with growing support

Fix ONCE a computable function b(n), with 3<=b(n)<=n for n>=3, independently of any individual SAT source. The separate sound complete fixed calculus R_local-feedback[b] is Result 499's original-source-indexed unit-weight system except a LOCAL step may inspect the union of supports of its named antecedents and proposed conclusion on at most b(n) ORIGINAL variables, rather than a constant b. It permits ordinary unrestricted Resolution, unrestricted global GF(2) addition of existing affine rows, and local semantic conversions between ordinary clauses, affine rows and arbitrary explicitly tabulated Boolean factors. Local rules may be interleaved, branched by legal alternatives and shared/reconverged within an acyclic proof DAG, but NO fresh variables, nonlocal Boolean factors, branch assumptions or discharge rules. A LOCAL implication is checked by exhaustive truth tables, not a free oracle. For b(n)=ceil(log2(n+2)) capped at n, the LOCAL checker is polynomial-time in the explicit input and proof size.

**Theorem 500.1 (uniform quantitative same-source simulation):**

For each such fixed function b, every q-inference legal DAG refutation of an m-clause CNF F on n original variables yields a syntactic degree-one characteristic-two Res(PC_1/F_2) refutation from the SAME ORIGINAL clauses with

$$
S_{\mathrm{Res}(\mathrm{PC}_1/\mathbb F_2)}(F)
\le C(n+m+q+1)(b(n)+1)2^{b(n)}
$$

for an absolute constant C independent of n, F, q and the values b(n).

**Proof.** An ordinary clause becomes a native disjunction of literal equations, and an affine row becomes its native unit equation. A factor with support I is represented by at most 2^{|I|} canonical exclusion clauses, one for each falsifying complete assignment to I. Source clauses and each bundle are derived just once and shared. Ordinary RES is simulated by a native linear combination plus false-constant deletion, and XOR by one native linear combination. At a sound LOCAL inference let U be the union of supports, |U|<=b. For each assignment alpha to U falsifying the output, some NAMED antecedent is false. A false parent clause or factor supplies its canonical exclusion clause, weakened to full D_alpha. A false parent affine row supplies D_alpha by its equation, Boolean tautologies, O(b) syntactic weakening/linear-combination/false deletion, as established constructively in LSPV-1/499. For output support J subseteq U, eliminate the U\J bits by ordinary binary Resolution in a complete assignment tree, at most 2^{|U|}-2^{|J|} steps. These yield exactly the canonical exclusion bundle for an output factor or the unique falsification clause for a clausal output. For an affine output, Pang's explicit Fact 7.1 compiles the canonical CNF into its unit equation in O((b+1)2^b) syntactic target steps. Hence each LOCAL input node contributes O((b+1)2^b) distinct target nodes. Source axioms cost O(m+n) and all shared subproofs are reused without double-counting. This proves the stated size bound. No target inference is an unrestricted semantic rule and all contexts are empty. QED.

**Corollary 500.2 (sublinear locality lower bound, published preprint premise).**

Pang's target bound on the original proper signed F_n with 8n independently sampled clauses is S(F_n)>=exp(kappa n) with probability 1-o(1), for some kappa>0. Thus, if a SINGLE FIXED b(n)=o(n),

$$
W_{R_{\mathrm{local-feedback}[b]}}(F_n)
\ge \frac{e^{\kappa n}}{C(b(n)+1)2^{b(n)}}-O(n)
=e^{\kappa n-o(n)}=e^{\Omega(n)}.
$$

In an explicit signed-index source encoding N=Theta(n log n), the resulting restricted worst-case bound is exp(Omega(N/log N)) along an unbounded N sequence. This extends /499 from CONSTANT b to **unbounded** b(n)=ceil(log2(n+2)) with polynomial-time LOCAL checking, and indeed to every fixed sublinear computable b(n) with mere effective (not necessarily polynomial) checking. It does NOT establish historic all-rule hardness, computational SAT hardness or any consequence for P versus NP.

## ITERATE: independent computational controls

Independent Python /mnt/data/lspv1_500_growing_locality_audit.py: 96 factor-conversion cases for support n=2..5, 1,612 assertions checking weakened premises and actual binary resolvents, four sampled proper 3-CNF 8n-clause formulas at n=6,8,10,12 independently exhaustively certified UNSAT, and deliberate corrupted implication rejected. Independently authored GitHub JavaScript experiments/arc/lspv1_500_growing_locality.cjs (blob **a252e13c1e26a8a790c989749db1d1b4bfb16973**) checks 96 cases, 912 assertions, max extra macro steps 6,14,14,21 for supports 2,3,4,5; all four small sampled 8n-clause signed 3-CNF are UNSAT by enumeration; corrupt implication rejected. Results stored in results/raw/arc/2026-11-08_0200_LSPV1_GROWING_LOCALITY_RAW.json (blob **63c977b5b04c044c6eeec988db560872002fe01c**). The first JavaScript trial used a low-bit-biased LCG and was corrected to xorshift32 before report publication; commit history retains the correction. These are finite **COMPUTATIONAL** controls only; neither the historical checker nor Pang's asymptotic proof was executed.

**Resource ledger:** logical source work q distinct inference nodes with perfect free optimum selection; translated nodes O((n+m+q)(b+1)2^b); each truth-table factor O(2^b) data bits; full bundle O(b2^b log(n+q+2)) explicit variable/line-identifier bits. LOCAL validation may enumerate 2^b assignments and scan recorded premises, costing O(q2^b poly(b+proof record length)) for each LOCAL node in the worst case, polynomial in n+certificate size when b=O(log n). Actual translation charges parsing, antecedent reads, source binding, generated targets, checking, indexing, reference storage and output; the ideal minimum excludes discovery by design. A full retained proof DAG may use O(q b2^b polylog(n+q)) bits simultaneous storage; recomputation may save storage but raises time. Paid proof work, weighted critical-path span and physical time/peak-space schedules must not be conflated.

**Boundary:** paid fresh definitions, arbitrarily nonlocal AND3/LOCAL-CONVERT, any extra Boolean circuit factoring, case splitting with assumption discharge and other historic R_mix341 rules are NOT simulated; these shortcuts must not be prohibited when evaluating its TRUE unrestricted minimum. The separate B3 bridge remains entirely open. Four exact unclosed IDs: [P2-D1], [P2-C3], [P2-B1], [P2-B2]. P versus NP remains OPEN.
