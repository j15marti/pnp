# LSPV-1/431: Empty-branch completion of the affine shared-proof invariant

**November 5, 2026, 18:00 PST; Route B lead.** **PROVED/RESTRICTED semantic linear-algebra statement, independent specialist review pending.** **COMPUTATIONAL** exhaustive finite replay. The exact serialized historical R_mix341 grammar, unrestricted mixed-system minimum, B1/B2/B3 and P versus NP remain **OPEN**. Existing five roles, schedules, rule weights, identities and enabled states are unchanged.

## IDEA before SEARCH, quantifiers and falsifiers

**Hypothesis.** The LSPV-1/430 affine intersection theorem, which required BOTH complementary branches to contain models, can be replaced by one homogeneous linear-annihilator identity valid for every pair of affine sets, including empty UNSAT branches. The identity must model AND-complete case discharge and correctly prevent sharing branch-local equations without guards. It is not a new historical R_mix341 rule.

For every n>=1 and every S0,S1 subset F_2^n, each either empty or nonempty affine, define S = ({0} x S0) union ({1} x S1). A falsifier is any equation true throughout S but omitted by the proposed annihilator, or a predicted equation false at some member of S. Additional exact falsifiers: (F1) the /430 intersection formula applies when one branch is empty; (F2) cross-branch reuse drops an x guard; (F3) a both-empty semantic contradiction is treated as a free source-authenticated historical proof; (F4) ordinary Resolution hardness is transferred across the known Tseitin GF(2) shortcut.

## SEARCH and corpus reviewed

Read the governing November 2 shared handoff (blob c3889a3e), issue #3 including LSPV-1/430 and LSPV-3/435, AGENTS.md, CODEX.md and pnp-research skill. Read original LSPV-1/430 (report blob from run), LSPV-3/435 (c02acb2e), REFEREE357 (20553f0d), REFEREE365 (30bea76a), REFEREE367 (7bb7dcff). Actual Grok REWIRE review research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex (d06a2d56) concerns circuit reuse, not source-certified UNSAT proof grammar; Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6) is a restricted tape-model result, not B3. Both were inspected, not treated as authority.

Change-aware source review: konard/p-vs-np proofs/complexity/README.md blob 7ee9a11e has explicitly finite machine semantics but no model-equivalence or same-R proof. blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea and RESIDUAL_EQUIVALENCE_BARRIER_REPORT.md blob 46413596 distinguish finite projections from inexpensive exact acquisition. meelgroup/frat-xor format.md blob 986a21aa uses explicit CNF/XOR premise IDs but is NOT the native R_mix341 byte grammar. openai/math lean/OAI/Algorithms/SubexponentialSAT/SAT.lean blob 14dcfd0c gives exact CNF semantics, and ExecCNFNodeSearchCosts.lean blob 1ced21f4 charges its own concrete executor; neither is a B3 compiler. No source claims a general mixed-proof lower bound.

Actual web queries: "Cook Reckhow 1979 relative efficiency of propositional proof systems PDF", "bounded arithmetic reflection Extended Frege", "Tseitin expander resolution lower bounds Ben Sasson Wigderson", "backbone literal 3 SAT coNP complete", and "affine hull of Boolean satisfying assignments CNF complexity". Read Cook--Reckhow 1979 original, Section 1, Definitions 1.3, 1.5 and Proposition 1.6, at https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf . Also reviewed relevant BSW Resolution literature and Pich--Santhanam (2023) at https://arxiv.org/abs/2312.08163 . Direct Google-branded interactive search was not available. Indexed web and authenticated GitHub were used. Search did not establish novelty of the elementary linear-algebra result.

**Duplication audit.** LSPV-1/430 already proves the both-nonempty rowspace intersection formula. ARC217 and LSPV-1/422 already establish one-bit projection/acquisition hardness. REFEREE357 already supplies the conditional p-optimality caution, and REFEREE365 studies proposed CANON2R, not the original byte grammar. None of these is rebranded as new. This report adds the *empty-arm formulas, unified annihilator proof, and direct exhaustive controls* only.

## ITERATE: exact theorem and proof

Let each affine constraint on z=(y,x) in F_2^(n+1) be represented as (v,a,c), meaning v.y xor ax = c. For ANY set S define E(S) to be every such constraint valid on all members of S, including the false equation 0=1 if S is empty. Define the homogenized row vectors H(S) = span{(y,x,1): (y,x) in S} subset F_2^(n+2). Then

$$
E(S)=H(S)^\perp,\qquad
\dim E(S)=n+2-\dim H(S).
$$

This identity includes empty S because span(empty)=0, so E(empty)=F_2^(n+2). Moreover,

$$
E(S_0\mathbin{\dot\cup}S_1)
=E(\{0\}\times S_0)\cap E(\{1\}\times S_1).
$$

The equation is AND-complete: both nonempty branches must justify a shared equation. There is no branch-local leakage.

For each nonempty affine branch S_b={y:A_b y=c_b}, write U_b=row(A_b), r_b=dim U_b, and tau_b(v) for the unique constant v.y on S_b. A rank r_b basis is a *premise*: discovering/checking an exact representation from arbitrary source 3CNF is not free.

**Case 1, both nonempty.** All valid equations are uniquely

$$
(v,\ a=\tau_0(v)\oplus\tau_1(v),\ c=\tau_0(v)),
\quad v\in U_0\cap U_1.
$$

Their dimension is k=dim(U_0 intersect U_1). The nonzero x-free equations number 2^(k-delta)-1, delta the rank of tau0 xor tau1 on the intersection. This is exactly the previous LSPV-1/430 theorem.

**Case 2, exactly branch b nonempty.** All valid equations are

$$
(v,a,c),\quad v\in U_b,\quad a\in F_2,\quad
c=\tau_b(v)\oplus ab.
$$

Dimension r_b+1, including the globally valid unit equation x=b. There are 2^(r_b+1) consequence equations, including 0=0. Importantly, the unit x=b is a SEMANTIC consequence of the other branch's emptiness and is not a free native rule.

**Case 3, both empty.** Every one of the 2^(n+2) equations is valid, including 0=1. This is a semantic fact, not a source-authenticated R_mix341 refutation.

**Proof.** A consequence equation is equivalent to (v,a,c).(y,x,1)=0. It holds for every satisfying point iff its coefficient vector is orthogonal to every spanning point, proving the annihilator formula. For branch x=b the constraint becomes v.y=c xor ab. A linear form is constant on a nonempty affine solution set exactly when v lies in its defining row space. Imposing both branch constraints yields Case 1, imposing only one yields Case 2, and imposing neither yields Case 3. Dimension and count follow from linearity. QED.

**Formal limitation.** Given independently authenticated exact affine bases and branch emptiness certificates, these spaces can be intersected by Gaussian elimination in O(n^3) field operations and O(n^2) working bits for dense bases. The antecedent is substantial: a polynomial-time extraction of exact affine solutions or emptiness flags from arbitrary CNF is not established. Under the conditional hypothesis SAT in P, the semantic descriptions may be computed, but translating them into legal historical proof nodes and a noncircular B3 argument remains OPEN. No arbitrary semantic consequence is installed as a free inference.

## Established-family ledger and hostile controls

| Family | Source exact encoding | Model/lower bound | Known shortcuts | Missing transfer |
|---|---|---|---|---|
| Odd cubic-expander Tseitin | For connected cubic h-vertex graph, 3h/2 edge variables; at each vertex encode parity charge by four signed width-three clauses forbidding the other four local assignments; 4h clauses, Theta(h log h) explicit indexed bits | Urquhart 1987 and Ben-Sasson--Wigderson 2001, 2^Omega(h) ordinary DAG Resolution size for suitable expander family; NO arbitrary-algorithm lower bound | Mixed AND3/GF(2) semantic refutation with 4h-1 paid binary nodes; linear work and balanced logarithmic ideal depth in earlier project results | Historic byte grammar/normalization, any full-mixed superpoly Wbar, B3 |
| PHP / strict width-three padding | Previously preserved 3CNF padding with explicit fresh sign pairs and charged recovery; original Haken n+1 into n pigeon clauses begin with widths up to n | Haken 1985 exponential ordinary DAG Resolution, not a generic 3CNF bound without a proved reduction | Cook 1976 polynomial Extended Resolution proof; padding + restriction costs scoped by LSPV-3/433 and LSPV-1/429 | Transfer into native full Rmix341 not established |
| Finite K4 Tseitin | Six edge vars, 16 exact signed width-3 clauses, one odd or even charge | No finite asymptotic hardness claim | Odd charge both x branches empty; even charge eight models, four each x branch | Verifies need for the empty-arm cases, NOT native certificate acceptance |

## COMPUTATIONAL verification, actual execution

Self-contained Node producer executed locally (487900 assertions) over **every** affine subset of F_2^n for n=1..4, including empty: respectively 4,12,52,308 sets and 16,144,2704,94864 ordered pairs. Compared ALL derived equations, not merely counts, using brute-force truth tables: total 97728 pairs and 6160256 candidate equation comparisons. Independently written Python verifier checked all n<=3 pairs, all 615 n=4 pairs containing an empty arm and 3000 seeded n=4 both-nonempty pairs, 6479 pairs total (seed=431), with no mismatches. The original-source K4 odd/even control was independently enumerated: odd 0 models and 0/0 branches; even 8 models and 4/4 branches. Finite tests do not certify the asymptotic theorem; its proof is above.

Producer exact committed path: experiments/arc/lspv1_431_affine_empty_branch.js. Full original local Python/Node producers and raw JSON are in the conversation reproducibility archive. The repo Node file was created and read back byte-for-byte at commit de9419e6d265296d81f50991b0e7fe014db4cff2; its separate exact execution after GitHub publication is not claimed.

## Costs, bridges and root synthesis

Logical semantic output is a vector space, with a compact O(n^2)-bit basis when premises are exact, but listing all consequences may be exponential. Offline semantic Gaussian elimination is not a charged machine SAT solver nor a historical proof. For real machines count reading, proving branch emptiness and exactness, construction, output bytes, reference validation, caching, recomputation, peak space, and failures. The ideal W_R still counts only *legal* paid distinct nodes; this result does not alter any native weight.

B1 => B2 => B3 remains the target hierarchy. No implication was proved for any. In particular, the both-empty case cannot prove B3 by introducing 0=1 at zero cost. For root main.tex, current fetch_file returned blob 593000bbe5b09df6b93fb7453da2ebdf73aeff6b with zero readable bytes; ownership-preserving reconciliation was BLOCKED. Do not write root blindly.

**Next exact gap:** LSPV-3 should produce authenticated native-format refutations or explicit legal non-replay for one empty branch, with both-case AND obligations and original source; LSPV-5 should red-team source/assumption vacuity; LSPV-1 should test a global B3 reflection/normalization mechanism against the actual historical rule bytes. P versus NP remains OPEN.

## References

[1] Cook SA, Reckhow RA. The Relative Efficiency of Propositional Proof Systems. J Symbolic Logic. 1979;44(1):36-50. https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf

[2] Urquhart A. Hard Examples for Resolution. JACM. 1987;34(1):209-219.

[3] Ben-Sasson E, Wigderson A. Short Proofs Are Narrow: Resolution Made Simple. JACM. 2001;48(2):149-169.

[4] Cook SA. A Short Proof of the Pigeon Hole Principle Using Extended Resolution. SIGACT News. 1976;8(4):28-32.

[5] Pich J, Santhanam R. Towards P != NP from Extended Frege lower bounds. arXiv 2312.08163 (2023). https://arxiv.org/abs/2312.08163
