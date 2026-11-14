# TMR-2/022: exact polarity-edit distance, Walsh-flat UNSAT recognition and independent cube audit

**Date:** November 14, 2026, 08:23 PST (America/Los_Angeles).
**Role:** TMR-2 Information Necessity, j15marti/pnp main.
**New synthesis:** TMR2-SRG22, CANDIDATE/RESTRICTED pending independent TMR-1/TMR-5 review. Complete elementary all-length arguments below.
**Testing:** COMPUTATIONAL (hosted V8), not a machine-model or asymptotic proof.
**P versus NP:** OPEN.

## 1. Input model and the exact robustness theorem

Let F be any explicitly encoded ordered proper 3-CNF with m clause occurrences. Each clause C_i has three **distinct** variable IDs, a fixed ID triple, and three independently editable literal-sign bits. A sign edit changes a polarity bit, not an identifier, clause size, clause ordering, input length or uncharged witness. The full ordinary encoded bit length is L; the editable-sign payload has 3m bits, generally L != 3m. For an assignment a let

$$
v_F(a)=|\{i:C_i(a)=0\}|,
\qquad
d_{\rm sign}(F,\mathrm{SAT})=
\min_{F'\mathrm{\ SAT}}\ d_H(\operatorname{sign}(F),\operatorname{sign}(F')).
$$

**Theorem SRG22-A (exact and all lengths, restricted to same-identifier legal sign edits).**

$$
\boxed{d_{\rm sign}(F,\mathrm{SAT})=\min_{a\in\{0,1\}^n}v_F(a)=m-\operatorname{MAXSAT}(F).}
$$

**Proof.** Fix a. Every clause falsified by a must have at least one of its three sign positions changed before a satisfies that clause, because all unedited literal truth values remain false. Distinct clause occurrences have disjoint sign-coordinate sets, so at least v_F(a) edits are required. Conversely, change exactly one literal polarity in each a-falsified clause; all of those clauses then become true under a, and every previously a-satisfied clause remains unchanged. Thus the cheapest edit producing a formula satisfied by the fixed a costs v_F(a). Minimize over a. This proof applies to arbitrary nonempty CNF clauses, although the next 1/8 statement requires **three distinct variables per clause**. In particular d=0 iff F is SAT; it is an exact Max-3SAT deficit, not a physically compulsory computation by A.

For proper width-three clauses, an independent uniform assignment falsifies each clause with probability 1/8. Linearity of expectation and integrality give

$$
\boxed{0\le d_{\rm sign}(F,\mathrm{SAT})\le\lfloor m/8\rfloor.}
\tag{SRG22-B}
$$

This bound is sharp: the repeated full cube U_r has m=8r and d=r. It does not transfer to clauses having repeated variable IDs. This is an immediate application of the standard 7/8 Max-E3SAT averaging argument, not a claim of new field-level priority.

## 2. Exact Fourier/Walsh saturation criterion

Represent an assignment by x_v=(-1)^{a_v}. For clause i and its variable v let eta_{i,v}=(-1)^{b_{i,v}}, where b_{i,v} is the unique variable bit that falsifies that literal. The clause-falsification indicator is

$$
\mathbf 1[C_i(x)=0]=\frac18\prod_{v\in V_i}(1+\eta_{i,v}x_v).
$$

For a nonempty subset S of at most three variables define the **integer** signed clause moment

$$
M_F(S)=\sum_{i:S\subseteq V_i}\prod_{v\in S}\eta_{i,v}.
$$

Then, exactly on every assignment,

$$
8v_F(x)=m+\sum_{\substack{\emptyset\ne S\subseteq[n]\\|S|\le3}}
   M_F(S)\prod_{v\in S}x_v.
\tag{SRG22-C}
$$

Uniqueness/orthogonality of the Boolean Walsh characters and the average m/8 imply an exact characterization:

$$
\boxed{d_{\rm sign}(F,\mathrm{SAT})=m/8
\ \Longleftrightarrow\
 M_F(S)=0\text{ for all nonempty }S.}
\tag{SRG22-D}
$$

Indeed min v=mean v iff v is constant on all assignments; a multilinear Walsh expansion is constant iff all nonconstant coefficients vanish. If m>0 and all M_F(S) vanish, every assignment violates exactly m/8 clauses. Since the violation count is integral, m is then divisible by 8, m>=8, and **F is UNSAT**.

**Uniform charged recognizer:** On an explicit proper 3-CNF occurrence list, construct the integer dictionary of at most 7m coefficient contributions keyed by sorted variable subsets S, |S|=1,2,3; add each signed integer, and check whether every final nonconstant coefficient is zero. Each key has at most three variable identifiers and each counter has O(log(m+1)) bits. Sorting and merging 7m records (or a balanced dictionary) is deterministic polynomial time and uses polynomial writable workspace on a fixed finite multitape TM, with all source reads, parsing, buffers, comparisons and output charged. On the zero-moment, m>0 branch output UNSAT; on nonzero moments output UNKNOWN and run a correct paid general SAT fallback. This produces a **single fixed total correct general decider with polynomial processing time on the spectral-flat sublanguage**, not a polynomial worst-case general 3-SAT algorithm. A conservative polynomial rather than an unproved sharp machine-level exponent is claimed.

This provides an additional hostile example: large polarity-edit distance does not require an expensive search, because its maximal case has a short deterministically computable *global algebraic invariant*. The same effect holds across arbitrary overlapping variable triples when their signed clause moments cancel; a constant-width E3 signature mask is not the only cheap representation.

## 3. Independent TMR-5/019 and TMR-1/022 audit

For U_r, r repetitions of each of eight three-variable forbidden signatures, every assignment falsifies exactly r clause occurrences, so SRG22-A implies d=r and the Walsh moments all vanish. Every distance-r SAT neighbor chooses one of eight signatures to eliminate and flips exactly one of three sign bits in every one of its r copies. All other signatures remain, so the count is precisely 8*3^r. There are 24 disjoint sensitive r-bit blocks, indexed by (old signature, literal coordinate); every SAT-producing block must edit >=r distinct clause occurrences, hence 24 is also the upper bound 3m/r. For r>=2, no individual sign bit is pivotal. Thus TMR-5/019's **corrected** exact 24-block conclusion is independently supported by an all-r symbolic proof. Its superseded eight-block count remains FALSIFIED/RETIRED, not silently reinstated.

I also independently checked the proof of TMR-1/022's cube sign-certificate claim, retaining its distinct certificate definition. In U_{k,r}, any UNSAT-forcing partial sign observation must fully fix at least one clause occurrence for each of 2^k signatures: otherwise an adversarial completion can omit a signature. Thus C_0=k*2^k. For the nearest SAT neighbor V, if r>=2, every untouched clause can be changed to the missing signature while its previous signature still appears, so a label-forcing SAT certificate must touch all m clauses. One observed bit per clause differing from the missing signature suffices, hence C_1=m. The unrestricted r=1 claim is genuinely false: fully observing the two duplicated clause signatures for k=3 requires only 6 sign bits, with m=8; at most seven distinct signatures can then appear under any completion. These are **restricted symbolic peer-verdicts**, not arbitrary-machine time bounds. I have not independently rerun TMR-1's matching-oracle source.

These two measures must not be conflated: sign-edit distance is a distance from the input to the opposite-label input set; certificates are partial observations that force the same label over *all legal completions*; machine time is the actual computation by a fixed uniform total A. None is a general superpolynomial machine lower bound.

## 4. Actual reproducible executions

**Hosted V8 actual execution, exact published source:** 15,585 proper three-literal formulas, including 12,870 exhaustively enumerated unordered signature multisets for n=3 with m<=8, 2,700 deterministic seeded random n=4,5,6 sources and seven explicitly constructed controls (Horn-like, XOR/parity, auxiliary-lifted 2-SAT, path-like bounded overlap, disjoint products, duplication, variable renaming). Every one of 203,992 complete assignments satisfied the exact integer Walsh identity; 15,585 minimum-violation and zero-coefficient tests passed. U_r for r=1..8 was checked on all eight assignments, with 192 explicit SAT-producing block tests. For r<=3, all 63,471 Hamming neighbors of edit distances 0..r were enumerated; the nearest SAT layer counts were 24,72,216. All **zero assertion failures**. Seed 0x6b8b4567, fixed parameters, published raw JSON and executable source. These source controls are **not** executions of specialized Horn, 2-SAT, GF(2), or bounded-treewidth solvers, nor a physical TM compiler.

Code: experiments/tmr/tmr2_walsh_sign_robustness022.cjs (Git blob b38366925c045f91d3c036849939b606fc707f5c).
Raw: results/raw/tmr/2026-11-14_0820_TMR2_WALSH_SIGN_ROBUSTNESS022_RAW.json (Git blob 984e21330b126d74f1826d061717048f24b58957).
Both publications were fetched by exact path and read back; data agree with the hosted execution. Native Node.js, independent CPython, full repo preflight script and TeX compilation were **not** executed this run. Code and data do not establish an all-machine asymptotic result.

## 5. Original Claude and primary-literature audit

Latest files under research/agents/claude/ were surveyed. The latest directly named standalone Claude reports in that directory date **October 28, 2026** (not November 14). In CLAUDE ONETAPE-0001, crossing-sequence obstructions are explicitly sequential-access and apply even to nondeterministic one-tape computation; no unrestricted SAT processing lower bound follows. CLAUDE TPORT-0001/0002 show a portfolio-size threshold/barrier **inside a specified alternation-trading rule system** with random access and small-space hypotheses. None excludes all polynomial-space deterministic SAT deciders. The Claude DIRECTPRODUCT route also does not establish an all-machine hitting-set or reconstruction bottleneck. These reports are useful as falsification guidance, not as a substitute for a general lower bound.

**Primary literature verified for contextual results, not as origin of SRG22's identity:**

1. R. O'Donnell, *Analysis of Boolean Functions*, Cambridge University Press (2014), DOI 10.1017/CBO9781139814782, for Walsh character orthogonality and unique multilinear expansion.
2. Standard Max-E3SAT random assignment averaging, independently derived above (each proper 3-clause false with probability 1/8); see Purdue CS580 notes on randomized Max-3SAT, 2018, https://www.cs.purdue.edu/homes/jblocki/courses/580_Spring18/Lectures/CS580-Lecture27RandomizedAlgorithms.pdf .
3. L. Fortnow, R. Lipton, D. van Melkebeek, A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, DOI 10.1145/1101821.1101822. It excludes specified simultaneous small-workspace/time pairs, not arbitrary polynomial workspace.
4. Original project reports: research/agents/tmr-5/2026-11-14_0754_TMR5_SIGN_ROBUSTNESS_REDTHEOREM019.md; research/agents/tmr-1/2026-11-14_0816_TMR1_CUBE_CERTIFICATE_COST_BARRIER022.md; research/agents/tmr-2/2026-11-14_0725_TMR2_GENERAL_POLARITY_PIVOTAL_DICHOTOMY021.md; research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex and research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex.

## 6. Transfer gap, statuses and strategic next target

The exact general lower-bound quantifiers are still

$$
\forall A\,\forall k\ge1\,\forall C>0\,\forall L_0\
\exists F\text{ valid}:
 |F|\ge L_0,\qquad T_A(F)>C(|F|+1)^k,
$$

for every single correct fixed finite total deterministic 3-SAT machine A. A may read its whole input repeatedly, retain an arbitrary polynomial workspace, use algebra, cache, share and recompute. SRG22 gives an **easy positive UNSAT recognizer for a maximally robust promise subfamily**, not a lower-bound necessity. Its polynomial-time fallback on all inputs may still be exponential outside the recognizable branch.

**Proved by elementary derivation within the restricted sign model, peer promotion pending:** SRG22-A/B/C/D, corrected U_r distance/count/blocks, and the restricted TMR-1/022 certificate audit.
**COMPUTATIONAL:** finite V8 test counts.
**OPEN:** a compulsory after-acquisition computational cost for every unrestricted uniform SAT decider; any universal superpolynomial Bellman potential; all-polynomial-workspace lower bound; and a general polynomial SAT algorithm.

**Research recommendation:** stop treating large polarity sensitivity, Hamming robustness, assignment count or certificate multiplicity as computational resources. Treat the Walsh-flat family as a regression falsifier. The next candidate must lower-bound **nontrivial processing on an all-input correct machine after a fully charged input acquisition**, permit zero-cost semantic summaries only when physically constructed, and survive cheap Horn/2-SAT/GF(2), bounded-treewidth, products, full-cube, and high-treewidth moment-balanced controls. TMR-5 should red-team any universal lower-bound hypothesis using the new spectral recognizer. TMR-3 should charge its concrete sorting, caching, and read/recompute alternatives. TMR-4 should preserve its actual physical trace under may-abstraction, rather than require the recognizer to enumerate assignments. TMR-1 should enforce the exact all-machine quantifiers. A correct polynomial 3-SAT algorithm remains an equally valid endpoint.

**Corpus/integrity:** Authoritative replacement directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4 read first and rechecked before writes. proof1.txt complete 28,714 chars (06f7ebc8c2283304a0f5200b518c6e48fa41e343); proof2.txt complete 1,051,196 chars via authentic blob (930c5eeddafce656717f28055a7a9a755f44737c), not the empty connector body; canonical main.tex complete 2,542,866 chars via authentic blob (5ec8fffb16ec9a7f262e60321bf5aad172d153d8). AGENTS.md, CODEX.md, repo skill, latest issue #3, all current TMR handoffs including TMR-1/022, original peer evidence and named Claude reports reviewed. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex left unchanged for TMR-5 whole-document synthesis. No scheduled tasks or legacy allocations changed.

**One next target:** determine whether a proposed forced processing cost survives the Walsh-zero recognizer plus original TMR-1/022 legal-input certificate controls, before investigating any unrestricted transfer.

END_OF_REPORT::TMR2::022::2026-11-14_0823_PST
