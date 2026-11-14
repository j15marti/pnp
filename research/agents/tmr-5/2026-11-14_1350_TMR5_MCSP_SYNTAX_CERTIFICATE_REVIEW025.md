# TMR-5/025: MCSP orientation-certificate barrier and syntax-aware falsifier

**2026-11-14 13:50 PST (America/Los_Angeles).** Owner: TMR-5 Machine Bottleneck Redteam. New elementary results: **PROVED/RESTRICTED**, independent TMR-1/TMR-4 review requested. Native finite tests: **COMPUTATIONAL**. P versus NP: **OPEN**.

## What is genuinely new

Compared with TMR-4/029's earlier adaptive source-independent evaluation-oracle locality theorem, this run establishes a **polynomial-output certificate-orientation implication** for a hypothetical reverse-label SAT-to-MCSP reduction, and an independent **syntax-aware, equal-source-length countermodel** to transferring oracle-query lower bounds to arbitrary syntactic reducers. A separate native Python program independently verifies the exact balanced cyclic OR locality frontier; it does not execute the TMR-4 code. The complexity-class implication is elementary and not claimed novel to the field.

## Prior-work ledger and complete source-state review

The current 2026-11-14 MCSP directive (research/coordination/2026-11-14_MCSP_FIVE_AGENT_REVIEW.md, SHA 1e11aa64a0b0d635a65cea58500b09f2b0fe010a) was read FIRST, then the 2026-11-13 TMR replacement directive. The entire root proof1.txt (28,714 characters, blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343), proof2.txt (1,051,196 characters, blob 930c5eeddafce656717f28055a7a9a755f44737c), and main.tex (2,545,859 characters, blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34) were obtained and checked; the latter two required complete Git blob readback because Contents API returned blank bodies. AGENTS.md, CODEX.md, the pnp-research skill, all five latest TMR handoffs, and issue #3 through the newest TMR-4/029 were reviewed.

Relevant ORIGINAL inputs, with prior statuses preserved:

| Original path | Prior result and scope |
| --- | --- |
| research/agents/tmr-4/2026-11-14_1336_TMR4_ORACLE_LOCALITY_GAP_MASK029.md; experiments/tmr/tmr4_oracle_gap029.py and its raw JSON | Adaptive black-box locality $Nq$ theorem; source syntax and globally shared preprocessing excluded, restricted |
| research/agents/tmr-1/2026-11-14_1307_TMR1_MCSP_GROWING_THRESHOLD_ENUMERATION027.md; original Python/raw | Unbounded but slowly growing $s=\Theta(n/\log n)$ one-work-tape *upper* bound; not small positive power $s=N^\mu$ |
| research/agents/tmr-2/2026-11-14_1322_TMR2_GROWING_MCSP_PERIODIC_CODE028.md; original Python/raw | Full-query but cheap periodic YES subclass; not an MCSP both-label decider |
| research/agents/tmr-3/2026-11-14_1327_TMR3_MCSP_RAWSCAN_HEADER_BOUND028.md; original Python/raw | Single-head raw-cache compiler and distinct upfront-header model; symbolic restricted |
| research/agents/tmr-5/2026-11-14_1259_TMR5_BOUNDED_ENVELOPE_REVIEW024.md; original Python/raw | Fixed cap and bounded varying threshold cofactor envelope, restricted |
| research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex; research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex; research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex | Historical affine, one-tape, and portfolio controls; none supplies unrestricted SAT hardness |

Other historical Walsh/moment, signed/hypergraph and checker/normalizer accepted-path failures were retained; no real counterexamples were deleted.

## Verified primary-source theorem matrix

| Original paper and theorem | Exact premise and conclusion |
| --- | --- |
| Cheraghchi, Hirahara, Myrisiotis and Yoshida, STACS 2021, [publisher PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol187-stacs2021/LIPIcs.STACS.2021.23/LIPIcs.STACS.2021.23.pdf), **Thm 1, p.23:3** | Ordinary exact MCSP threshold $2^{\mu_1 n}=N^{\mu_1}$ for some sufficiently small constant $\mu_1>0$, full $N=2^n$ truth table, deterministic one-way read-only input plus one two-way work tape. Nonmembership in $DTIME_1[N^{1.01}]$ implies $P\ne NP$. Hypothesis **OPEN**. |
| Same source **Thm 2, p.23:3** | At a different larger $\mu_2$, randomized two-sided-error one-way-input one-work-tape nonmembership in $BPTIME_1[N^{1.99}]$ is proved. It cannot replace the small threshold in Thm 1. |
| McKay, Murray and Williams, STOC 2019, [original paper](https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf), **Thms 1.2-1.3, p.2** | Search-MCSP with oracle gates, full $N=2^n$ input, $s(n)\ge n$, one-pass streaming with $\Sigma_3SAT^A$ small queries, $\widetilde O(s)$ space, $\widetilde O(s^2)$ update; conditional no-poly$(s)$ streamer for some $A\in PH$ implies $P\ne NP$. This is not ordinary exact decision MCSP. |

Keep source SAT encoded bit length $L$, source variable count $v$, target Boolean arity $n$ and target explicit truth-table length $N=2^n$ separate. No ETH/SETH, oracle advice, ordinary MCSP NP-completeness, or Gap/partial/MKTP equivalence is assumed.

## Theorem CERT-ORIENT30: polynomial-output label reversal

Let $R$ be a single **uniform deterministic polynomial-time total** map taking every 3CNF $F$, encoded in $L$ bits, to a **fully output** target truth table $R(F)$ of length $N(F)=2^{n(F)}\le L^c$. Assume the target gate threshold $s(n(F))\le N(F)^d$ is computable in polynomial time, with fixed constants $c,d$. Let $CC_n$ count AND/OR/NOT gates with free constants, inputs and fanout. Suppose **for every valid $F$**:

$$
F\in3UNSAT\implies CC_{n(F)}(R(F))\le s(n(F)),
$$

$$
F\in3SAT\implies CC_{n(F)}(R(F))>s(n(F)).
$$

Then **$NP=coNP$**.

*Proof.* On any 3UNSAT input, produce all $N\le\mathrm{poly}(L)$ target bits, nondeterministically guess a size-$s$ circuit, and exhaustively compare its outputs against the table on all $N$ assignments. The certificate description and verification take $\mathrm{poly}(N+s+n)=\mathrm{poly}(L)$ time. Both-label preservation yields a valid NP verifier for the coNP-complete language 3UNSAT, hence $coNP\subseteq NP$, and by complementation equality follows. QED.

This extends to a Gap-MCSP Hamming promise with the same easy small-circuit YES set and SAT mapping to **promised far-NO**, because far-NO implies not YES. If the target MCSP slice itself lies in P, the same hypothetical $R$ implies **$P=NP$** by direct composition; in particular ordinary $MCSP[0]\in P$ by checking constants and input projections.

**Status:** an exact restricted **conditional implication** from a hypothetical polynomial-output reversal, not proof that such a reduction is impossible, not $P\ne NP$, and not a claim about nonuniform source-advice mappings. A forward orientation SAT to MCSP YES would instead establish MCSP NP-hardness, which is not known in general.

TMR-4/029's original $h_F(x,u,w)=F(x)\land u\land w$ maps UNSAT to the zero-gate YES label and SAT to ordinary zero-gate NO. But its *complete* output length is **$N=2^{v+2}$**, exponential in $v$ and potentially superpolynomial in $L$. On a unique-witness source the table has one 1, normalized distance $1/N$ from zero, so it is not promised far-NO for $\eta>1/N$. Dummy padding preserves this relative distance. Thus there is no conflict with CERT-ORIENT30.

## Construction SYNTAX30: syntax defeats an overgeneralized oracle bound

For every $v\ge3$, $a\in\{0,1\}^v$, and variable $i$, choose $j=i+1\bmod v$ and $k=i+2\bmod v$. Let $B_i^b$ contain **all four proper three-distinct-variable clauses**

$$
(\ell_i^b\vee\ell_j^p\vee\ell_k^q)\quad(p,q\in\{0,1\}),
$$

where $\ell_i^b=x_i$ for $b=1$ and $\neg x_i$ for $b=0$. Their conjunction is exactly the unit constraint $x_i=b$. Set $B_a=\bigwedge_iB_i^{a_i}$ and

$$
F_a^+=B_a\land B_0^{a_0},\qquad F_a^-=B_a\land B_0^{1-a_0}.
$$

Both have **$4(v+1)$ proper 3CNF clauses**, identical encoded bit length (fixed-width signed literals), and the same variables. The positive source has unique satisfying assignment $a$, while the negative source is UNSAT. Repeated clauses in the positive source are permitted and counted.

On this **promised family only**, comparing the sign of the first literal in the first forcing block with that in the final block decides the source label without any evaluation-oracle query. A uniform source-syntax-aware transformation maps negative sources to the complete two-input zero table $0000$ and positive sources to XOR table $0110$. In the zero-gate target, allowed YES tables are $0000$, $1111$, $0011$, $0101$; $0110$ is at distance **2/4=1/2** from every one. Hence for any $\eta\le1/2$ this syntax-aware map preserves both promised Hamming-gap labels, with **zero evaluation-oracle calls**.

This is a concrete **FALSIFICATION** of extrapolating TMR-4/029's $q\ge\eta 2^v$ bound beyond its **source-independent evaluation-oracle** model. It does not falsify that actual theorem or furnish a general 3SAT-to-MCSP reduction. The family is a cheap recognizable promise language, and $N=4$ is a deliberate control.

## Independent native experiment and mathematical replay

In the actual source-independent oracle model, the all-zero response path for each output coordinate contains at most $q$ distinct queried assignments. Every singleton at an unqueried assignment produces that same path. Summing changing positions over all singletons yields $\sum_a d_H(y(f_a),y(0))\le Nq$. The balanced cyclic OR of $q$ queries per target bit attains equality for reference distance when $N$ is a multiple of $2^v$, but does **not** certify far distance from *every* small circuit.

**Executed native CPython** source experiments/tmr/tmr5_syntax_certificate030.py (SHA256 e4ebfbd97bd2251d5fa998de7c37e0455bcc54f065d384b32d818ab38f481bc0), exact stdout results/raw/tmr/2026-11-14_1350_TMR5_SYNTAX_CERT030_RAW.json (SHA256 f3bf6be2972b1a09e6ef7d1dc25742238a04e01b10395ca704ed9abbd3e1a6cb). **1,094** grouped assertions, zero failures: 120 SAT and 120 UNSAT proper formulas across $v=3,4,5,6$, exhaustive assignment correctness, equal-length checks, direct $h_F$ truth-table weight checks, target distance, and all $q\le2^v$ cyclic controls for $v=1,\dots,5$. No random seed, no oracle, no physical-TM compiler. Finite results are **COMPUTATIONAL**; symbolic proofs above are separate. This code was independently authored and executed, not a replay of the peer's Python script.

## Ranked integrated dependency and retirement map

| Rank | Route | Weakest still-OPEN arrow |
| --- | --- | --- |
| 1 | CHMY low-$\mu$ one-work-tape lower bound $\Rightarrow P\ne NP$ | Prove ordinary *full-table* $MCSP[N^{\mu_1}]\notin DTIME_1[N^{1.01}]$ at exact **small** threshold |
| 2 | CHMY proved high-$\mu_2$ bound to low-$\mu_1$ | Fully charged both-label, threshold- and model-preserving transfer with admissible exponent |
| 3 | Source syntax SAT composition to MCSP or Gap-MCSP | Polynomial $L\mapsto N$ explicit-output, correct-promise reduction; label reversal also triggers the NP=coNP certificate barrier |
| 4 | One-tape streaming, crossing sequences, networks, certificate/query capacity | Model-preserving lower bound for the **one-bit** decision problem and then arbitrary uniform SAT deciders; full-output transport alone is insufficient |
| 5 | Fixed/bounded/slowly growing MCSP upper bounds | A both-label full-MCSP algorithm or lower-bound obstruction at $s=N^\mu$, not merely fixed gates or periodic YES subclasses |

**Retired as purported general proof arrows:** source-independent oracle-query lower bounds applied to source syntax; exponential $h_F$ treated as a polynomial-size truth-table reduction; Hamming promise NO treated as ordinary NO; high-$\mu_2$ CHMY lower bound substituted at low $\mu_1$; compulsory input/output transport inferred from a one-bit decider. These retirements apply to the **specified attempted deductions**, not to every possible reduction technique. Natural-proofs, relativization and locality barriers were kept as model-specific warnings.

The unrestricted target still requires, for each *fixed total correct uniform deterministic multitape 3SAT decider* $A$, every integer $k\ge1$, $C>0$ and $L_0$, a valid $F$ with $|F|\ge L_0$ and $T_A(F)>C(|F|+1)^k$. All load-bearing arrows remain OPEN.

## Governance and exact next target

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical root main.tex remains untouched: the new TMR-5 lemma needs independent peer review before manuscript promotion. Historical material and original code/raw evidence preserved. No task, schedule or agent identity altered.

**Peer requests:** TMR-1 verify the coNP-to-NP certificate argument and reduction quantifiers; TMR-4 check the proper 3CNF four-clause forcing and zero-query syntax bypass; TMR-2 verify the zero-oracle-path double count; TMR-3 verify the $L$-to-$N$ full-materialization charge. **Next target:** build or falsify a genuinely syntax-aware, polynomial-output, both-label reduction at exactly the CHMY small-$\mu$ threshold, checking orientation before attempting any time lower-bound transfer.
