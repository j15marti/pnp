# TMR-4/008: unbounded zero-singleton SAT sources with disjoint two-bit UNSAT certificates

**Run and report:** 2026-11-13 19:36 PST (America/Los_Angeles). **Owner:** NEW TMR-4 Cost-Sound Abstraction, \`j15marti/pnp\`, branch \`main\`. **Status:** CANDIDATE, pending independent TMR-5 mathematical review. Executed finite source audits are COMPUTATIONAL. The unrestricted 3-SAT time lower bound and P versus NP remain **OPEN**.

## 1. New increment, exact scope, and falsification target

The prior TMR-4/007 certificate-prefix abstraction uses arbitrary opposite-label input-difference sets, including a 268-bit SAT source with two disjoint *large* UNSAT difference sets and no sensitive individual literal-field bit. This report supplies an **unbounded, explicit, strict proper 3-CNF family** with:

1. **Every syntactically legal one-bit flip in any literal-sign or literal-identifier field preserves SAT**, even with the strict rule that every declared variable must occur. The claim intentionally does not cover header-bit flips or malformed encodings.
2. For every integer \`r >= 1\`, there are **r pairwise disjoint two-position difference sets**. Flipping *both* bits of one such pair yields a valid, same-length UNSAT source.
3. Every correct total fixed uniform deterministic machine with at most \`q\` physical original-input-bit observations per transition must acquire at least one position from each pair on the SAT source: \`T_A(x_r) >= ceil(r/q)\`. This is a noncircular, program-independent instantiation of the all-transition MAY observation potential. The source length satisfies \`L_r=Theta(r log r)\`; the bound is \`Omega(L_r/log L_r)\`, **not superpolynomial**.

This is stronger than the finite two-certificate example in /007 as a *certificate-size witness*, and shows that singleton sensitivity can miss an unbounded compulsory distinction while the exact observation abstraction remains valid. It does not close the post-acquisition processing gap.

## 2. Exact grammar and construction

Use \`1^N 0 1^M 0\` followed by \`M\` ordered clauses, each containing three distinct signed positive variable IDs, with one polarity bit and \`w=max(1,ceil(log2 N))\` bits per variable ID. All declared IDs \`1..N\` must occur. The complete encoded length is

$$
L=N+M+2+3M(w+1).
$$

Fix \`r >= 1\`, let \`t=3r\`, \`w=ceil(log2(2t+2))\`, \`N=2^w-1\`. Encode the \`t\` core variables by distinct even-Hamming-parity identifiers

$$
\rho(i)=2i+(\operatorname{popcount}(i)\bmod 2),\quad i=1,\ldots,3r.
$$

Each individual bit flip of a core ID has odd parity, so it maps to a *spare* dummy ID, not another used core ID. Let \`U\` be the other \`N-t\` declared IDs. Add \`K=ceil(|U|/3)\` all-positive proper three-dummy clauses that cover all of \`U\`: group dummy IDs in consecutive triples, and complete a last group of one or two by distinct earlier dummy IDs. Every dummy appears, and every filler clause remains satisfied when any *one* dummy variable is set false and all others true.

For each block \`g=0,...,r-1\` use the three independent core variables \`a_g,b_g,c_g\`. For \`m in {0,...,7}\`, let \`C_g(m)\` be the proper 3-clause which is FALSE exactly when the three local variable bits equal the binary digits of \`m\`; thus the polarity of literal \`j\` is negative precisely when bit \`j\` of \`m\` is 1. The block contains **eight** clauses with masks

$$
1,\ 2,\ 3,\ 4,\ 5,\ 6,\ 7,\ 3.
$$

All blocks use disjoint core variables. The complete formula \`x_r\` contains \`8r+K\` clauses. Setting every core variable to 0 and all dummies to 1 satisfies the complete formula; no chosen core block bans mask 0, and filler clauses are positive.

### All valid one-bit literal-field mutations preserve SAT

- **Original core clause polarity.** If one of the two mask-3 duplicates is changed by one polarity bit, its new forbidden mask is 2 or 1, never 0; the all-zero assignment remains SAT. If one of the unique masks 1..7 is changed into a nonzero mask, all-zero remains SAT. If the changed unique mask becomes 0, the formerly banned old mask is now unbanned; setting only that block's core variables to the old mask and all other core variables to 0 satisfies every core clause. Filler clauses remain satisfied by all dummies true. These cases exhaust all original core sign-field flips.
- **Original core identifier bit.** An even-parity ID becomes a spare odd-parity dummy ID. Keep all core variables 0; give the newly referenced dummy whichever Boolean value makes its modified literal true; set every other dummy to 1. The rest of that clause was already true or is rescued by this literal. The filler still holds because two other dummy literals remain true in each filler triple. Each original core variable occurs eight times, so its replacement in one literal cannot make the old declared ID unused.
- **Filler literal polarity or identifier.** Keep all cores 0 and all dummies 1. The other two positive dummy literals in the changed filler clause remain true. This applies whenever the modified clause is syntactically valid (nonzero in-range ID, three distinct IDs and all declared IDs occurring). Invalid mutations are not treated as opposite-label source neighbors.

Thus every valid one-bit change to any literal-field bit keeps SAT. No claim about legal header changes is required.

### Disjoint two-bit opposite-label certificates

In each block \`g\`, change the two polarity bits for \`a_g\` and \`b_g\` in its second mask-3 clause to 0. The duplicate mask 3 becomes mask 0, while the first mask-3 clause remains. That block now contains all eight possible three-variable forbidden tuples \`0..7\`, so it is UNSAT independently of every other clause and every dummy value. The mutated complete formula is still proper, parses under the same \`N,M,w,L\`, and every declared variable still occurs. Let \`D_g\` be the pair of changed encoded bit positions. The pairs are distinct and mutually disjoint.

Consequently the difference-set hypergraph \`mathcal D={D_0,...,D_{r-1}}\` has exact hitting number

$$
\tau(\mathcal D)=r.
$$

These are actual opposite-label, same-length inputs, not oracle-given or merely hypothetical assignments.

## 3. Exact charged abstraction and machine implication

Fix **any** one finite total correct deterministic multitape SAT machine \`A\` serving all binary lengths, with fixed program, finite alphabets, one or more physically charged read-only input heads, complete writable tapes, stack/index/buffer/caches and fixed \`q>=1\` original-bit observations possible per transition. A read or reread costs its physical transition. An input-indexed instruction is not added for free: if another model is used, its maximum observations per charged physical transition must be justified separately.

Augment concrete histories with ghost set \`V\` of original encoded positions ever read. Ghost history is not free working memory available to A. The MAY abstraction has mask states \`star_V\`, cost-one edges that reveal up to \`q\` new positions, cost-zero stutters preserving V, and cost-zero edges to **both** SAT/UNSAT goals only when V meets every D_g. Relate the complete concrete program/configuration/history to the abstract mask; the concrete side retains the true finite-control, both tape alphabets and contents, input contents, all heads and writable memory. Every physical step maps to an abstract path of cost <=1: one reveal edge, or a zero-cost stutter, followed by an appropriate zero-cost terminal edge if the physical machine halts.

The last edge is valid: if A halted on \`x_r\` without reading either position in some \`D_g\`, the source \`y_g\` obtained by changing precisely those two bits would produce the **identical entire deterministic execution**, including every adaptive input location, all writable work and the terminal label. Since \`x_r\` is SAT and \`y_g\` UNSAT, that contradicts correct total decisions. Thus any actual terminal has hit all \`D_g\` and connects to its true goal. Both label outcomes are represented by the general MAY graph; the semantic coupling is applied separately to each concrete source.

Let

$$
\tau(V)=\min\{|W|: W\subseteq [L]\setminus V,\ (V\cup W)\cap D_g\neq\varnothing\ \text{for all }g\},
\qquad
\Phi(\star_V)=\left\lceil\frac{\tau(V)}q\right\rceil,\quad
\Phi(g_{\rm SAT})=\Phi(g_{\rm UNSAT})=0.
$$

For every cost-one reveal edge \`V -> V union R\`, \`|R|<=q\`, one has \`tau(V)<=|R|+tau(V union R)\`, so

$$
\Phi(\star_V)\le 1+\Phi(\star_{V\cup R}).
$$

Cost-zero stutters preserve Phi; terminal edges have tau=0, so obey the edge inequality. **Every edge** satisfies \`Phi(a)<=cost(a,b)+Phi(b)\`. Telescoping through the represented complete physical execution yields

$$
\boxed{\Phi(\star_{\varnothing})=\lceil r/q\rceil\le T_A(x_r).}
$$

The abstract shortest decision path equals \`ceil(r/q)\`: no path can hit r disjoint pairs with fewer observed positions, and reading one position per pair in batches of size q realizes that cost. The prior TMR-4/007 exact-prefix extension also applies if a separately executed \`B\`-transition prefix and its actually read positions \`V_B\` are supplied; no double count is allowed.

**No superpolynomial premise:** \`N<12r+3\`, \`K<=3r+1\`, \`M<=11r+1\`, \`w=Theta(log r)\`, and \`L=Theta(r log r)\`. Therefore \`r=Omega(L/log L)\`. Among the \`L\` bits, \`Q=24r(w+1)\` original core literal-field bits are all individually *insensitive* to the SAT label, and

$$
\liminf_{r\to\infty}Q/L\ge 8/11.
$$

The exact source-encoding costs and fully charged arbitrary workspace are respected. The lower bound is only a source-observation necessity, bounded by \`L\`.

## 4. Hostile controls, computational audit and non-transfer

**EXECUTED in hosted V8 (re-run from published GitHub source after readback):** ten deterministic source sizes \`r=1,2,3,4,5,6,8,10,12,16\`; 1,977 single-polarity SAT-neighbor checks; 9,968 valid one-bit ID SAT-neighbor checks; 2,185 ID-bit mutations rejected as invalid by a full grammar parser; 67 independent two-polarity UNSAT block certificates; zero failed assertions. Each parsed legal neighbor is accompanied by an explicit satisfying assignment. Every UNSAT certificate contains all 8 forbidden local tuples, which is an exact mathematical contradiction. At \`r=16\`: \`N=127, M=155, w=7, L=4004, Q=3072\`, certificate count 16 and Q/L approximately 0.7672. The executable also validates exact serialized length, dummy coverage, proper triples, nonzero IDs, all-declared-ID use, and pair disjointness. Raw data includes a per-size ledger. The independent native OS Node script at \`/mnt/data/tmr4_zero_sensitivity_disjoint_pairs008.cjs\` separately completed 12 sizes, 2,439 sign SAT checks, 12,272 valid ID SAT checks, 83 disjoint certificate blocks and zero failures; **this separate local script is not claimed to be published**.

**ANALYTIC hostile controls:** Input rereading, cache/recompute, speculative preprocessing and multiple heads are not forbidden by the MAY graph; already-read positions are never charged again. The complete source can be copied and recognized in polynomial time on a fixed physical multitape program. In particular, a **fixed correct total** decider can authenticate the described independent 8-clause mask-block grammar and positive dummy filler, check each block's eight forbidden-mask table, and invoke a fully charged exhaustive general-SAT fallback if authentication fails. On the authenticated sources and two-bit neighbors its runtime is polynomial in L (a conservative \`O(L^c)\` for some fixed c suffices), so this family cannot establish superpolynomial processing. This is a symbolic construction, **not executed as a physical Turing-machine transition table**.

**NOT EXECUTED this run:** physical TM transition-level replay, a general fallback solver, LaTeX compilation, standalone native Node replay of *the exact published hosted-V8 executable*, and specific Horn, 2-SAT, Gaussian-elimination, bounded-treewidth, variable-renaming or auxiliary-variable stress suites. These remain eligible solver techniques, not excluded cases. Finite source audits do not prove an asymptotic lower bound; the all-r statement rests on the elementary symbolic proof.

**Historical checker scope:** Original LSPV-5/511 accepted a support *string* where a checker expected an array. This remains a real accepted path of its specific historical proof grammar, not a spurious path to delete. The current theorem is about physical source-reading ghosts, not the /341 checker, and draws no native-checker lower-bound transfer.

## 5. Independent literature and provenance

[1] H. Buhrman and R. de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, Theoretical Computer Science 288 (2002), 21-43, original author manuscript: https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf . Certificate complexity/block sensitivity is the conceptual precedent; this report supplies its own proof and does **not** transfer an unbounded-query decision-tree lower bound to physical SAT execution.

[2] P. Cousot and R. Cousot, *Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints*, POPL (1977), pp. 238-252, author source: https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml . The present MAY abstraction deliberately overapproximates possible outcomes and underestimates physical charges.

[3] N. Nisan, *CREW PRAMs and Decision Trees*, SIAM J. Comput. 20(6) (1991), pp. 999-1007, DOI https://doi.org/10.1137/0220062 . Its model is CREW PRAM, not a general deterministic SAT multitape machine; no machine-model lower-bound transfer is asserted.

**Original project sources reviewed:** TMR-4/007 \`research/agents/tmr-4/2026-11-13_1840_TMR4_CERTIFICATE_PREFIX_ABSTRACTION007.md\`, /006 \`research/agents/tmr-4/2026-11-13_1737_TMR4_PREFIX_SENSITIVITY_PRODUCT006.md\`, /003 deferred-final-symbol falsifier, five TMR handoffs, original LSPV-5/511 support-string duck-typing handoff, both root proof trackers, root main.tex, AGENTS.md, CODEX.md, repository skill and latest issue #3. The historical LSPV directives are superseded by the unchanged 2026-11-13 12:49 PST TMR replacement directive.

## 6. Publication and next dependency

Verified GitHub source: \`experiments/tmr/tmr4_zero_singleton_pairs008.cjs\`, Git blob \`fa86967d21a79ee42d3036280dd06b9071e2fc32\`. Raw per-size evidence: \`results/raw/tmr/2026-11-13_1936_TMR4_ZERO_SINGLETON_PAIRS008_RAW.json\`, blob \`1f3b8bed7547a9f518435d471cc407b07bedd6ed\`. These two were read back and the source was re-executed from the readback body with identical counts.

**TRACKERS REVIEWED; NO MATERIAL CHANGE:** \`proof1.txt\` complete 28,714 characters SHA \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`; \`proof2.txt\` complete 1,051,196-character Git blob SHA \`930c5eeddafce656717f28055a7a9a755f44737c\` (ordinary contents endpoint returned empty). Root main.tex full authenticated blob 2,502,146 characters SHA \`62c0c400a5eddfbdbdfa06fbabcf7bcee8b753be\`. No proof tracker, canonical main.tex region, or schedules were modified.

**ONE NEXT TARGET:** TMR-5 independently check the strict all-used parser, \`r\` disjoint 2-bit UNSAT certificates and every-edge potential; then seek an unavoidable processing cost not capped by source information, surviving the authenticated polynomial block-mask recognizer and arbitrary polynomial workspace. **All unrestricted load-bearing implications remain OPEN.**

END_OF_REPORT::TMR4::ZERO_SINGLETON_DISJOINT_PAIRS008::2026-11-13_1936_PST
