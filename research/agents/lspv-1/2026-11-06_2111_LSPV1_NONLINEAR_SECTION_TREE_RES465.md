# LSPV-1/465 | Nonlinear Skolem-section decision-tree transfer for shared-DAG Resolution

**November 6, 2026, 21:11 PST (America/Los_Angeles) | Route B lead | PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

**Trackers reviewed:** main `proof1.txt` blob `e417a1a376d3347e6ef8f6915307005f5fa40972`, `proof2.txt` blob `d3f6779c030a17e920fdba9302915169aae161d7` at initial research read; prepublication tracker head must be refreshed. Exact IDs: [P2-B1], [P2-B2], [P2-B7], [P2-B8], [P2-C1], [P2-C3], [P2-F2], [P2-F8], [P2-D1]; [P1-01], [P1-03], [P1-X3]. New restricted evidence candidate: [P2-B9]. No other load-bearing node is closed.

## IDEA -> falsifiers -> SEARCH -> ITERATE

**Hypothesis:** The disjoint/literal-alias preservation results of LSPV-1/463-464 can be generalized quantitatively to nonlinear conservative auxiliary clauses if ONE globally coherent partial-assignment decision tree makes all auxiliary clauses identically true at its leaves. Prediction: plain unrestricted shared-DAG Resolution has at most linear-in-leaf-count backtranslation overhead into original-source Resolution.

**Four advance falsifiers:** (1) a leaf auxiliary clause remains non-tautological after its promised assignment; (2) restriction increases distinct Resolution inferences or imports an auxiliary source; (3) discharging both cases requires a non-native SPLIT/WEAKEN/DISCHARGE step or illegitimate branch-local reuse; (4) full reconvergence duplicates an ancestor beyond the explicit L-fold allowance, invalidates the claimed bit/work bound, or changes SAT status. The symbolic proof addresses all four; finite controls additionally test (1)-(3), source provenance, exact RES pivots and acyclicity. The L-fold bound intentionally *permits* copies and is not a promised same-machine optimizer.

**Prior work and actual sources inspected:** Governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, current issue #3 and its latest peer comments, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, LSPV-1/463-464, LSPV-3/463 (single-split native RES discharge), LSPV-3/464 (FRAT-XOR arity mismatch), LSPV-4/457 and LSPV-5/401, `GROKPROOF/2026-11-06_2316_PROGRESS.md` and `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`; issue #3 also disclosed newer Claude WORSTCASE-LOG note on a separate branch, not treated as a main-branch theorem. Searched GitHub project for "Skolem decision tree Resolution conservative", "decision-tree section", "branch leaf source projection", "resolution proof by cases"; no matching theorem with these precise quantifiers was found, but this is an elementary synthesis of classical Resolution restriction and the existing LSPV-3/463 branch-discharge lemma, **not a novelty claim**.

**External targeted source reads:** `konard/p-vs-np/README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` and `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2` (finite machine P subset NP, not general solution); `blkph0x/p-vs-np-proof-research/README.md` blob `f397a7747eaca82df3d754d0a4b4bab1fe10f814` and `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` (restricted methods); `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f` (external XOR grammar); `tanyongkiam/cake_lpr/README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c` (verified LPR checker); `peitl/short-proof/README.md` blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab` (exact RES optimizer, not run here); `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` (mixed verification status). Public web research checked Chvátal-Szemerédi (JACM 1988 DOI 10.1145/48014.48016), Cook Extended Resolution PHP history, Resolution restriction/proof-by-cases and recent Res(XOR) tradeoffs. Google-specific search interface was not used. Direct GitHub via connector; no shell-network Git. No exact historical native R_mix341 accepted-byte checker executed.

## Theorem 465.1 (source-only Resolution under nonlinear section decision trees)

Let F(X) be **any UNSAT CNF** of original variables and G(X,Y) any conservative CNF over disjoint fresh auxiliary variables Y. Let T be a finite full binary decision tree querying ORIGINAL variables X, without repeated query on any root-leaf path, with L leaves. Every leaf ell specifies its path's partial assignment alpha_ell and a FIXED assignment b_ell to ALL Y such that **every individual clause of G restricted by alpha_ell and b_ell is a tautology on the remaining original variables**. This is a uniform, total, all-X sectional condition; it does not let an oracle choose Y only for satisfying assignments of F.

Let S_Res(H) be the minimum number of DISTINCT paid oriented binary Resolution inference nodes in a source-authenticated shared-DAG refutation of H. Source clauses are free, all added G clauses are even granted as source clauses for this stronger upper-control model; NO extension, GF(2), LOCAL, SPLIT, weakening, semantic oracle or discharge rule exists. Then

$$
\boxed{S_{\mathrm{Res}}(F)\le L\bigl(S_{\mathrm{Res}}(F\land G)+1\bigr)-1.}
$$

Equivalently,

$$
\boxed{S_{\mathrm{Res}}(F\land G)\ge
\frac{S_{\mathrm{Res}}(F)+1}{L}-1.}
$$

**Proof.** Take any fixed source-authenticated shared Resolution refutation pi of F and G with s paid nodes. For each leaf ell, set X according to alpha_ell and Y according to b_ell. Every G source simplifies to TOP because of the per-clause tautology premise. Standard Resolution restriction replaces an inference by at most one correctly oriented Resolution inference or bypasses a parent; it never adds inference nodes and preserves sharing within the leaf. This yields an F|alpha_ell refutation with <=s paid nodes. Lift it to F sources: every surviving original source C has only literals FALSE under alpha_ell on assigned variables, so retaining the original C and replaying each unassigned-variable pivot gives an F-derived clause D_ell contained in the blocking clause B(alpha_ell), with at most s paid inferences. No axiom of G appears after restriction; no weakening or new case rule is used.

Join the two child derivations at an internal node splitting original variable x. If one child's conclusion omits the literal FALSE on its x branch, use that legal existing clause (already contained in the parent context's blocking clause). Otherwise the two child conclusions contain x and not-x respectively; one ordinary oriented Resolution inference on x yields a subclause of the parent blocking clause. This is exactly an AND obligation, not a free logical OR choice. Process bottom-up to derive the empty clause at root. There are L leaves and L-1 internal nodes, so counting all leaf proof copies and one paid RES per actual internal join gives <=Ls+(L-1) paid distinct nodes. Sharing can only reduce this union count. Minimize s over all refutations of F and G to obtain the result. QED.

**Concrete parameterization:** if the section values are determined by at most d original bits (joint support), T may query those d bits completely, so L<=2^d. This is a COROLLARY, not an assumption that an optimal decision tree can be acquired cheaply. The bound permits nonlinear AND/OR circuits and shared circuit computations as proof alternatives; d and L are properties of a specified section, not an all-input hardness invariant.

## Published-family consequence and controls

**Published hard source [P2-F8].** Chvátal-Szemerédi, *Many hard examples for resolution*, JACM 35(4) (1988), 759-768, DOI 10.1145/48014.48016. Take n original variables and m=6n independently uniform proper signed width-3 indexed clauses: each clause uses three DISTINCT original variables and independent polarity bits; duplicates between indexed source clauses are permitted. Since 6/8>=0.7, the theorem supplies epsilon>0 such that with probability 1-o(1) the formula is UNSAT and every unrestricted ordinary shared-DAG Resolution proof requires >=(1+epsilon)^n proof clauses. Therefore paid RES nodes satisfy S_Res(F_n)>=(1+epsilon)^n-6n (modulo the source-count convention). If G_n has a qualifying total Skolem-section decision tree with L_n=2^{o(n)} leaves, then the above theorem gives

$$
S_{\mathrm{Res}}(F_n\land G_n)
\ge \frac{(1+\varepsilon)^n-6n+1}{L_n}-1
=\exp(\Omega(n)).
$$

The original indexed binary encoding occupies N=Theta(n log n) bits. The bound therefore is superpolynomial in N for ordinary Resolution with these **restricted auxiliaries**, not in an unrestricted mixed system. It is a lower-bound-preserving 3-CNF source statement, not a claim about a random SAMPLE's certified individual proof hardness. The construction of G is distinct from the random source selection.

**Finite original signed proper 3-CNF control [P2-F2].** Odd K4 Tseitin with four vertices, six edge variables, four width-3 forbidden-parity clauses per vertex, 16 original clauses; odd-charge source has 0/64 satisfying assignments and even-charge control has 8/64. Add a strictly proper-3-CNF five-clause conservative gadget defining x7=x1 AND x2 via two padded binary facets using fresh x8,x9: (-7,1,8),(-7,1,-8),(-7,2,9),(-7,2,-9),(7,-1,-2). Its exact total section has a minimum three-leaf tree: if x1=0 assign (x7,x8,x9)=(0,0,0); if x1=1 and x2=0 assign (0,0,0); if x1=x2=1 assign (1,0,0). All five clauses simplify to TOP at every leaf, including on all assignments to the remaining unqueried originals. AND depends essentially on both original bits, so a two-leaf decision tree is impossible. Source-only DP Resolution builds an original F refutation with 31 paid inferences, depth 6. Three restricted-leaf derivations have generated inference counts 15,7,7; literal conclusions x1, (not x1 OR x2), (not x1 OR not x2); two genuinely legal RES joins on x2 then x1 yield a **complete 31-paid-node, 16-original-source, span-6 refutation**. This reproduces a finite certificate, NOT the exact minimum, and has no new asymptotic hardness certification.

**Known shortcut countercontrols:** Haken PHP exponential ordinary Resolution vs Cook polynomial Extended Resolution with paid nonlinear extension definitions (different calculus); expander odd Tseitin exponential ordinary Resolution vs source-anchored compact mixed GF(2) refutations (project declared semantic model). Hence the theorem **does not** prove an invariant under ALL historical R_mix341 rules or B3. A full R minimum may take an OR-alternative short proof not reproduced by the Resolution-only restriction.

## Executed tests and complete resource scope

Python producer generates original indexed source, signed-line SHA-256 `f5cdf17bdae46655aa8b480af5bfaa34bb5b430b18cf7a1e31691dbdab8b5909`, and a source-only proof certificate with exact parent IDs and pivots. 502 Python assertions PASS including SAT/UNSAT, full nonlinear gadget truth table with both padding bits, all leaves, source ancestry, no illegal rule, 5 invalid mutation rejections; 0.74s wall, 96,776 KiB peak RSS on test host. Independent Node.js verifier checks a published certificate with 1,182 assertions PASS, 960 section-clause tests, 5 invalid mutations rejected, 31 paid nodes and depth 6; 0.03s wall, ~26,356 KiB peak RSS. A separate fully standalone Node.js producer/checker passes 1,123 assertions and produces the same 31-node result, rejection of 5 corruptions. These are finite COMPUTATIONAL controls, NOT native mixed accepted-byte validation.

Explicit certificate file 9,331 UTF-8 bytes; Python script 10,505 bytes; independent verifier 5,342 bytes; standalone JS 4,507 bytes; raw summary 2,047 bytes. Logical paid nodes, explicit proof bits, reconstruction time, source parsing, memory allocation, verification, cache and output are distinct. The ideal S_Res minimum excludes discovery cost intentionally. A physical algorithm constructing this proof incurs every actual stage and does not inherit a small SAT-decider runtime from the bound. Work/depth minima need not be co-optimizable, and the finite 31/6 pair is just one witness. No FLMV exponents are deduced.

The repository-root `main.tex` blob `68188a24badda635a5983fda1c381cdb694fd497` again returned zero content for requested line-range read; no unsafe editing occurred. The skill preflight script could not execute as a real repository preflight because no local checkout and direct shell-network Git (DNS) was available. All five existing roles, IDs, titles, schedules and enabled states remain untouched; no historical rule or weight changed.

## Next exact open implication

[P2-B9] is a restricted **positive** quantitative transfer for short-section nonlinear AUXILIARY padding in ordinary Resolution. To advance [P2-B1] and [P2-C3], first authenticate the historical native R_mix341 grammar, then test whether its paid GF(2), AND3, LOCAL-CONVERT and conservative definition rules admit any analogous source retraction without excluding known shortcuts. A fully general bound for every legal rule is not supplied. The independent [P2-B2] noncircular SAT-in-P -> same-R polynomial-work transfer remains OPEN; the theorem does not supply reflection/correctness proofs of arbitrary deciders.

**Actual advance:** A proved L-leaf quantitative backtranslation for nonlinear conservative section gadgets, with source-only branching/reconvergence finite controls and an explicit published strictly-3CNF exponential-hardness corollary in Resolution only. **Verification:** local symbolic argument and independently executed finite controls; GitHub status requires separate write/readback. **Remaining gap:** historical full mixed-calculus normalization/lower bound and noncircular B3. P versus NP OPEN.

## Sources
1. V. Chvátal and E. Szemerédi, *Many hard examples for resolution*, JACM 35(4) (1988), 759-768, DOI 10.1145/48014.48016.
2. A. Haken, *The intractability of resolution*, Theoretical Computer Science 39 (1985), 297-308.
3. S. A. Cook, *A short proof of the pigeon hole principle using extended resolution*, SIGACT News 8(4) (1976), 28-32.
4. LSPV-3/463 `research/agents/lspv-3/2026-11-06_1919_LSPV3_NATIVE_RES_BRANCH_DISCHARGE463.md`, for the one-split source-only RES rule; independently reconstructed here.
5. `proof2.txt` [P2-F8], [P2-F2], [P2-B8] and corresponding original source reports.
