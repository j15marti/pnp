# A charged reduction inequality from the encoded T5 count map

Prepared 21 November 2026, 15:03:40 PST, America/Los_Angeles. Role: PNP Lower Bound Connections. Recovery head: 2f50f80fbd579bdc04ca0fbf24626ee63a20897e.

## Claim, outcome, and integration point

**T5-PAYLOAD-SUPPORT1. PROVED/EXACT for symmetric strict C, the specified explicit encoding, and acyclic fan-in-two Boolean circuits. Internal adversarial mathematical review completed; external independent review pending.** For every integer w>=3, n=2^w-1, and m>=2, there is one valid N-bit input x* at which flipping any of its L=3mw clause-data bits gives another valid input and changes the same binary exact-count output bit. Therefore every circuit computing the encoded-input count map F_N has at least L-1 noninput gates. Every deterministic bit-query exact counter must inspect all L data bits on the execution on x*. If a reducer's output alone suffices for exact downstream evaluation, that reducer itself must inspect all those bits.

For m=n, the bound is

    C_N >= 3nw-1 = N-n-2w-3 = Omega(N).

The statement is along this explicitly specified length sequence. It is stronger in asymptotic order than this role's previous Omega(N/log N) encoded-map support bound, although the two constructions use different length sequences. The underlying input-dependence principle is elementary and not claimed as historically novel.

**No contradiction with polynomial time is obtained.** The lower bound is linear, and the small promise family used to prove it has an O(N)-gate count circuit and a uniformly discoverable polynomial-time exact evaluator. All sensitivity witnesses are SAT, so this run proves no decision-map lower bound. It does not replace the previously established model-specific transport bounds.

This run follows the user's request to try the reduction-factor approach. It advances one load-bearing dependency: an independently justified demand on the combined reducer and evaluator of F_N. The resulting exact inequality is

    size(R_N) + size(E_N) >= 3mw-1

whenever E_N(x,R_N(x))=F_N(x) on every valid length-N input. The stronger superpolynomial demand needed to exclude all fixed time caps remains OPEN. The count-map route is selected; no pseudoentropy claim is made.

Four concrete falsifiers were fixed for this target:

1. A one-bit change produces an invalid ID, a repeated name inside a clause, or a changed header/length.
2. The two true counts do not differ at one common output coordinate.
3. Shared circuit gates or the valid-input promise permit a correct circuit to omit a purportedly essential data bit.
4. The argument is applied to an input class forbidding repeated clauses or unused declared names, to ordered R, or to a model with unbounded-fan-in/unit-cost unbounded-word operations.

The construction and proof rule out the first three under the declared model. The fourth records genuine scope boundaries.

## 1. Exact model, domain, quantifiers, and proposed cap

C is the symmetric ternary relation on {0,1,2,3,4} containing all permutations of 012,123,234,340,401. It has 30 ordered satisfying tuples. Every clause uses three distinct variable names, and every declared variable initially has the full five-color domain. Repeated clauses and declared unused variables are permitted [1]. There are no literal signs or input constants. Ordered R has 40 tuples and distinguishes its first coordinate; it is not substituted here. Historical S/Q claims are not used.

The input is

    1^n 0 gamma(m+1) followed by m triples of one-based w-bit IDs,
    w=ceil(log2(n+1)),
    N=n+2+2 floor(log2(m+1))+3mw.

F_N maps every valid length-N encoding to its exact satisfying-assignment count, padded to ell=3N binary output bits. The range on instances declaring n variables is contained in {0,...,5^n}; ell bits suffice since n<N and 5^n<2^(3N). Invalid strings impose no requirement on the circuit. The output bit indexed 2 from the least significant end has weight four.

Circuits are acyclic with binary AND/OR, unary NOT, charged constant nodes, arbitrary sharing and fanout, and no depth restriction. The lower bound also holds for any fixed basis with fan-in at most two. Circuit size counts noninput gates, not physical wire lengths. Each length may have its own nonuniform circuit. The lower-bound construction and the promise evaluator are uniform across w,m.

For resource comparisons fix ONE deterministic total exact counter A correct on all valid strict-C inputs, and fix K>0 and a>=1 independent of the input. The proposed cap is T_A(N)<=K N^a in the handoff's fixed-alphabet, one-head read/write tape model, with input, work, and output on the same tape. The gate conclusion quantifies over every correct circuit at the stated lengths. The input-reading conclusion quantifies over every correct deterministic bit-query computation on the SAME x*. The proof does not select a different difficult execution for each bit.

Define P_(w,m) as x* together with every one-bit clause-data neighbor of x*. These are L+1 distinct valid encodings. A concrete input distribution, if desired, is uniform on this set. The theorem is pointwise and needs no distributional hardness assumption. On this promise the count range has exactly the two values derived below.

## 2. A single baseline with every data bit sensitive

Let every one of the m clauses have one-based IDs (3,5,6). In w-bit binary, these have Hamming weight two, and each pair has Hamming distance two. With a zero-based clause API, the corresponding names would be (2,4,5); the new executable uses one-based IDs throughout.

Flipping any single bit in any occurrence of one of these IDs produces a fourth ID:

- It is nonzero because the original ID has two one-bits.
- It differs from each of 3,5,6 because their pairwise Hamming distances are two.
- It is at most 2^w-1=n because it is still a w-bit word.

Consequently each data-bit flip changes exactly one ID in exactly one clause, preserves strict syntax and the exact header and length, and introduces one previously unused name. Since m>=2, at least one unchanged copy of the original clause remains.

For colors a,b define t(a,b) as the number of c with C(a,b,c). Directly from C,

| a\b | 0 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|
| 0 | 0 | 2 | 1 | 1 | 2 |
| 1 | 2 | 0 | 2 | 1 | 1 |
| 2 | 1 | 2 | 0 | 2 | 1 |
| 3 | 1 | 1 | 2 | 0 | 2 |
| 4 | 2 | 1 | 1 | 2 | 0 |

There are ten ordered color pairs with t=2, ten with t=1, and five with t=0. Hence

    sum_(a,b) t(a,b) = 30,
    sum_(a,b) t(a,b)^2 = 50.

The original instance is one constraint repeated, with n-3 unused variables, so

    Z0 = F_N(x*) = 30 * 5^(n-3).

After any data-bit flip there are two distinct constraints sharing two variables. Once the common colors are fixed, their two remaining colors can be chosen independently. Thus, for EVERY data position i,

    Z1 = F_N(x* xor e_i)
       = 50 * 5^(n-4)
       = 10 * 5^(n-3).

Both are positive. Since 5^s modulo 8 is either 1 or 5,

    Z0 mod 8 = 6,    Z1 mod 8 = 2.

Therefore count output bit 2 is one on x* and zero on every one-bit data neighbor. This proves full data-bit sensitivity at a single actual encoded instance. This is not a claim about assignments to one fixed formula.

## 3. Circuit size and same-execution reduction cost

If a data input bit has no path to output bit 2, changing only that bit cannot alter the output. The valid pair x*,x* xor e_i contradicts correctness. Thus all L=3mw data inputs are ancestors of the same output.

Let that output cone have g noninput gates and l distinct input nodes. Its underlying graph is connected, so it has at least g+l-1 edges. Fan-in at most two gives at most 2g edges. Therefore l<=g+1. Since l>=L, g>=L-1. Constants and unary gates can only make this edge budget less generous. Arbitrary sharing is already allowed by the graph argument. Input negations cannot evade essential dependence. The same elementary bound appears in the fan-in discussion of Riedel and Bruck [5]; the proof here is supplied in full and does not import their cyclic-circuit model.

With m=n=2^w-1, floor(log2(m+1))=w, so

    N=n+2+2w+3nw,
    C_N >= N-n-2w-3.

The ratio of this lower bound to N tends to one as w grows. No assertion for every sufficiently large exact length is made.

For a deterministic bit-query counter, suppose its run on x* does not read position i. Coupling it with the valid one-bit neighbor gives identical states and future actions until termination, since every observed bit agrees. It would return the same count on both inputs. Thus all L positions must be observed on x*. On a machine whose transition observes at most b original bits, the corresponding requirement is at least ceil(L/b) observation transitions. A constant-size alphabet containing a fixed number of bits changes only constants. Word machines must charge word width; one word access is not automatically one bit access.

Now let a deterministic reduction R emit a summary S(x), and let an exact evaluator depend only on that summary. If R omits bit i on x*, then S(x*)=S(x* xor e_i), contradicting exact decoding. Hence R itself must inspect all L bits. If the evaluator can reread the original input, the correct conclusion concerns the UNION of reducer and evaluator reads on that execution. There is no separate second L-bit charge.

At the circuit level, let R_N have p gates and E_N have e gates, and permit E_N to receive the original x as well as R_N(x). If

    E_N(x,R_N(x)) = F_N(x)

on all valid length-N inputs, composition gives a correct count circuit with at most p+e gates. Therefore

    p+e >= L-1,    p >= max(0,L-1-e).

This is the proved cost-of-reduction inequality. A description of the residual using few variables does not remove evaluation gates or input accesses. Shared work is charged once in the composed DAG; it is not charged anew for each nominal reduction.

For an explicitly enumerated residual, suppose there are B=2^r nonnegative ell-bit terms, each produced by a size-v Boolean circuit from the summary, original input, and an r-bit index. Each term must include any multiplicity weights and their actual arithmetic. Assume their sum is exactly F_N(x) on every valid input. Unrolling all B indices and adding their outputs gives

    C_N <= p + B*v + 9*ell*(B-1) + 2.

A ripple full adder uses at most nine AND/OR/NOT gates per bit when the two XOR computations share their AND term with the carry; global constants cost at most two extra gates. Modular ell-bit addition is exact on the valid domain because all terms are nonnegative and the final sum is less than 2^ell. Thus a necessary comparison for this declared architecture is

    p + B*v + 9*ell*(B-1) + 2 >= 3mw-1.

This uses an upper construction for the evaluator against an independent lower bound. It does not claim that every solver enumerates B terms or that this upper construction is optimal.

Because the independent lower bound concerns count bit 2, there is a sharper necessary inequality. Let v_3 be the size of the term circuit's cone feeding its lowest three output bits. Adding only these bits modulo eight suffices to compute count bit 2. The three-bit adder costs at most 27 gates, so

    p + B*v_3 + 27*(B-1) + 2 >= 3mw-1,
    p >= max(0,3mw-3-B*v_3-27*(B-1)).

Here v_3<=v. This is the strongest reduction-cost inequality established in this run. It still has only a linear right-hand side. In particular, it cannot rule out a polynomial reducer that computes the entire answer and leaves a constant-size residual.

## 4. What the user's factor equation does and does not require

For a fixed solver on input x, partition its actual execution into paid reduction work P(x), processed terminal candidates of individual costs v_j(x), and other disjoint work H(x). The exact identity is

    T(x) = P(x) + H(x) + sum_(j=1)^B v_j(x).

P includes discovery and failed attempts. If each processed item costs at least v_min>0, then the cap implies

    B <= (K*N^a-P-H)/v_min.

Using an upper verification bound V instead gives T<=P+H+B*V, a sufficient budget calculation. The previous conversational equality T=P+B*V was too strong if V meant only an upper bound. Early-exit decision algorithms need only process their actual candidates, not all surviving candidates after a satisfying witness is found.

If successful sound reductions change positive candidate counts by factors r_i, then

    B_t = 2^k / product_i r_i,
    sum_i log2(r_i) >= k-b*log2(N)

is necessary for the specified terminal enumeration budget B_t<=N^b. If each step reduces by at most four, it requires at least ceil(max(0,k-b*log2(N))/2) successful steps. This is O(k), and O(N^d) work per step remains polynomial when k=O(N). It is not a contradiction.

Conditioning on two Boolean variables, by itself, creates FOUR residual instances. After t such levels, without pruning or shared evaluation,

    4^t * 2^(k-2t) = 2^k.

For k=15 and t=6, the eight assignments per leaf are multiplied by 4096 leaves, still 32768 assignments in total. Actual pruning, sound aggregation, or reuse is needed to save work. This corrects the earlier illustrative six-step calculation: it had assumed genuine removal of choices, not ordinary branching.

The strict-T5 full domain has 5^n assignments. Conditioning on two T5 variables creates 25 branches, and 25^t*5^(n-2t)=5^n. The Boolean calculation applies only to an explicitly established Boolean core.

For decision, if unrestricted polynomial-time computation is allowed inside the reducer, a reduction to a constant-size instance is equivalent to polynomial solvability: a hypothetical polynomial decider can compute the answer and output a fixed valid YES or NO representative. In the other direction, polynomial reduction to O(log N) residual variables with polynomial encoded length permits polynomial enumeration. This equivalence does not prove either side for SAT.

Exact counting needs weighted summaries or another exact decoder. An unweighted residual with O(log N) Boolean variables cannot have more than polynomially many models, whereas even easy T5 instances can have exponentially large counts. For example m disjoint clauses have 30^m models, computable by a product with O(m)-bit output. The format restriction is not a runtime lower bound. A general exact summary could be the answer itself; proving that every such summary is expensive would already require an independent counting lower bound.

Finally, minimizing over a different reducer for each input is not a uniform algorithm. Such a minimum can choose a program that hardcodes that input's answer and uses a correct fallback elsewhere. The required no-polynomial-time quantifiers are

    for every fixed correct A, every a,K,N0,
    there is a valid x with |x|>=N0 and T_A(x)>K*|x|^a.

Arbitrarily large violations suffice. One need not prove violation at every sufficiently large length.

## 5. A legitimate compact evaluator and the absence of a contradiction

On P_(w,m), the count only selects between Z0 and Z1. Check whether the payload equals the known baseline. This takes O(L) fan-in-two gates, and the selected full count uses shared selector/complement/constant wires. The two count constants are computable uniformly by repeated multiplication by five with O(n)-bit integers. Thus this promise has an O(N)-gate count circuit, despite every data bit being essential at x*.

A uniform partial algorithm parses the actual input, verifies n=2^w-1, w>=3, m>=2, regenerates the exact baseline, and counts differing bits. It returns Z0 for distance zero and Z1 for distance one, and UNKNOWN otherwise. The new code implements this algorithm. Exact byte comparison supplies authentication; hash equality is not used for admission. A general total exact solver can use this shortcut and fall back to exhaustive counting on UNKNOWN. The fallback has no polynomial guarantee outside the promise.

The shortcut can be implemented with O(N) physical storage and a deliberately conservative O(N^3) sole-tape time envelope: repeated scans cover parsing, counters, regeneration, and exact comparisons; repeated multiplication by the fixed constant five uses O(n)-bit integers; conversion and the complete binary output are included. Its physical CM is then O(N^4), and its input-charged minimum-description CM is O(N^4) by replay. These are upper envelopes for one implementation, not measured Python TM timings.

For the same fixed target solver under T<=K N^a, the inherited ceilings remain:

| Resource | Cap ceiling |
|---|---:|
| Peak physical storage | O(N^a) |
| Physical CM | O(N^(2a)) |
| Input-charged minimum-description CM | O(N^(a+1)) |
| Encoded-input count circuit | O(N^a log N) |

The Pippenger-Fischer forward simulation, with the handoff's input/output normalization, supplies the circuit ceiling [1,6]. A linear circuit lower bound fits below that ceiling for every a>=1. A bound omega(N^a log N) at infinitely many valid lengths would refute that fixed cap through the simulation. Excluding all polynomial-time counters requires defeating every fixed a. A counting contradiction alone would not establish a decision P-versus-NP separation.

The new same-execution bit-read lower bound is Omega(N) when m=n. It does not create an additional superlinear CM charge or compulsory retained information. Original input cells are charged by the stated space convention; working memory can still be small. The baseline is uniformly describable with O(log N) bits, so no high input-entropy or high Kolmogorov-complexity claim is made.

## 6. Resource ledger, controls, and gates

| Item | Charge and limitation |
|---|---|
| Input acquisition and source authentication | Every header and identifier belongs to N; the shortcut uses complete parsing and exact comparison. The proved sensitive-bit demand applies on x* even if its pattern is easy to recognize. |
| Reduction discovery and failed candidates | Included in P for a real solver. A circuit existence result does not supply free uniform discovery. The shortcut tries one explicit family; failed admission is paid before fallback. |
| Representation changes and adaptive switching | Every emitted byte, remapping, intermediate circuit, and selected representation is paid. The composition theorem permits arbitrary legal representations and raw-input access. |
| Queries, accesses, and addresses | Original bit observations are compulsory only as proved. Indexed tape accesses incur physical travel. No virtual residual queries are forced. Stored addresses use their full bits. |
| Sharing and recomputation | Distinct gates count once; repeated physical evaluations cost their actual transitions. Cache entries are charged while retained. No tree occurrence is automatically a new DAG operation. |
| Storage | Live input, counters, buffer copies, weights, and output occupy physical cells. Reading all data does not imply retaining all inferred facts. |
| Output | Exact count has O(N) binary bits. Large numeric value does not force unary output. B summands require actual weight arithmetic; an unweighted model-preserving kernel has a different specification. |
| CM | Sum the actual occupied state or the specified input-charged description at each transition. Do not multiply independent worst cases or add overlapping demands. |
| Research experiment | Generic finite counting enumerates used colors and multiplies the exact unused-variable factor; full all-name enumeration independently cross-checks the smallest class. This verifier work is not a lower bound on A. |

DISJ sanity: PASS as a scope control. The recovered canonical DISJ count circuit remains O(N), and the newer permuted-orbit evaluator [3] is a legal compact shortcut. None is contradicted by an Omega(N) support demand.

Relativization: no separation claimed. The unread-bit coupling applies to machines whose only access to the original bytes is through the declared bit interface. An oracle receiving the entire source in a free query would violate that interface; writing an ordinary query is itself charged. No nonrelativizing hardness theorem is supplied.

Simultaneous DTISP: PASS for the stated comparisons. The bit observations all belong to one run on x*. The partial evaluator's time, space, and CM refer to one implementation. They are not combined with another solver's optimal resource use.

Deterministic configuration counting: NOT USED as a lower bound. Halting computations and replay-based descriptive ceilings retain the handoff conventions. Full-state conditional output entropy remains zero and supplies no remaining-work measure.

Affine/Tseitin, complement, private-leaf trees, forced domains, and algebraic/cached evaluators remain permitted. No lower bound for a fixed witness relation is imported. The count-sensitive neighbors are all SAT, so no decision-witness packing argument is invoked. Renaming and slot permutations preserve semantics, while arbitrary byte changes do not; the construction uses a genuine new variable, not a global renaming. Relocation cannot erase a byte before its relevant information has been read, but it can prevent any claimed second service across old cuts.

Algebrization and Natural Proofs: no barrier bypass is asserted. The support measure has at most N input positions and therefore cannot itself give a superpolynomial bound. A stronger interaction measure needs its own theorem covering all shared gates.

## 7. Reproducible evidence and internal review

New executable: experiments/t5_bounds_payload_support_20261121.py.

Immutable raw evidence: results/raw/t5_bounds_payload_support_20261121.json.

    python experiments/t5_bounds_payload_support_20261121.py > /tmp/t5-payload-support.json
    cmp /tmp/t5-payload-support.json results/raw/t5_bounds_payload_support_20261121.json

The script uses Python's standard library, exact integers, no random seed, and explicit checks that are not disabled by python -O. It tests all 2190 data-bit positions across nine (n,m) parameter choices. Every generated pair is fully encoded and decoded, differs at exactly the intended original bit, has the claimed exact count, and changes output bit 2. The generic used-variable enumerator does not know the 30/50 identity. Nineteen full five-color enumerations over all seven declared names independently check the baseline and all neighbors at n=7,m=2.

| n | m | N | Sensitive data bits | Proved gate floor |
|---|---:|---:|---:|---:|
| 7 | 2 | 29 | 18 | 17 |
| 7 | 7 | 78 | 63 | 62 |
| 15 | 2 | 43 | 24 | 23 |
| 15 | 15 | 205 | 180 | 179 |
| 31 | 2 | 65 | 30 | 29 |
| 31 | 31 | 508 | 465 | 464 |
| 63 | 2 | 103 | 36 | 35 |
| 63 | 63 | 1211 | 1134 | 1133 |
| 15 | 20 | 265 | 240 | 239 |

The last row is a FIVE-valued strict-C instance, not the user's earlier 15-variable Boolean example. Its counts are 7,324,218,750 before a flip and 2,441,406,250 afterward.

Controls verify that m=1 does not have this sensitivity, C-slot permutations preserve the count, invalid zero IDs are rejected, and a valid two-bit alteration is returned as UNKNOWN despite having an independently computed positive count of 4500. An unrelated four-name strict-C UNSAT instance validates the counter's zero case with one additional full enumeration of 625 assignments. The figure of nineteen full enumerations refers specifically to the sensitivity family. The Boolean 15-variable branch table checks the bookkeeping identity, not a SAT lower bound.

The final code's SHA-256 is embedded in the raw file. All baseline encodings, changed positions, replacement IDs, counts, and mutant SHA-256 hashes are preserved. Hashes identify artifacts only. Finite observations are COMPUTATIONAL evidence; the all-w,m theorem is established by the symbolic proof above.

An internal reviewer independently derived the pair-fiber table, attacked partial-domain correctness and DAG sharing, and improved the initial per-slot baselines to the single (3,5,6) baseline. The reviewer also inspected the final code and raw evidence without repeating the experiment, confirmed their hash agreement, checked the parser and UNKNOWN guard, and sharpened the summation inequality to three-bit modular addition. This is internal review in the same research session, not external certification or a formal kernel proof.

The complete handoff, current assignment, AGENTS.md, CODEX.md, PNP skill and compatible governance were recovered. Own latest report, code and raw results [2], every current role handoff, issue #324, and the relevant new Redteam/Synthesis/Construction original sources and evidence were read. Construction's new direct evaluation closes the alternative left open by Synthesis; neither report is used as a premise of the new sensitivity proof. The older generic prefix-sensitivity report [4] was checked for overlap; it already explains unread-bit coupling and why observed bits cannot be charged twice. This run contributes the explicit strict-C count-map instance, simultaneous sensitivity of every ID bit, and its reduction/evaluator inequality.

Repository searches for essential/count/payload, 3mw/circuit, sensitivity/strict/count, and payload/support/bit found related historical interface results, but no duplicate of this encoded strict-C construction. A branch-name search for charged returned none; the first 100 branch records were also inspected. This is bounded pending-branch coverage, not an exhaustive review of the repository's many archival branches. No complete checkout was available, so repository preflight and LaTeX compilation were not run. No TMR manuscript or another role's file was edited.

## 8. Fresh literature and official-repository search record

The fresh searches targeted charged reduction discovery, exact counting versus decision-preserving elimination, kernelization barriers, and fan-in input dependence. Primary results were read at the hypotheses indicated below.

| Primary source | Exact scope and disposition |
|---|---|
| Darwiche and Marquis, JAIR 17 (2002), Definition 3.1 [7] | Succinctness compares existence of polynomial-size equivalent representations without requiring polynomial-time acquisition. Model-counting operations apply to declared target languages. Supports the acquisition/evaluation distinction; no unrestricted F_N lower bound imported. |
| Fortnow and Santhanam, author manuscript dated 19 March 2010, Theorem 1.2 [8] | OR-SAT compression from lists of formulas is excluded under NP not contained in coNP/poly. The input regime and unproved assumption prevent use as an unconditional T5 contradiction. |
| Dell and van Melkebeek, JACM 61(4), Article 23 (July 2014), Theorem 1 and reduction discussion [9] | Under coNP not contained in NP/poly, excludes O(n^(d-epsilon)) communication for n-variable d-SAT in its oracle model. This is a conditional parameterized compression bound, not a superpolynomial runtime theorem in N. |
| Riedel and Bruck, Cyclic Boolean Circuits, preprint dated 3 December 2009, Section 3.1 Claim 2 [5] | The acyclic fan-in leaf bound is compatible with the present one-output cone. Their separate cyclic-circuit semantics are not imported. |
| Pippenger and Fischer, JACM 26(2) (1979) [6] | The author repository abstract states the forward O(T log T) combinational-network simulation of one-dimensional-tape computation. The exact input/output normalization remains the current handoff's dependency, not a fresh independent certification. Both requested khoury and ccs.neu.edu PDF URLs returned 403. The full proof was unavailable in this run. No reverse inference from tape time to circuit demand is used. |

Fresh literature queries were:

- Fortnow Santhanam infeasibility instance compression succinct PCP NP coNP poly pdf
- Darwiche Marquis knowledge compilation map succinctness model counting polytime pdf
- SAT polynomial kernel number variables compression lower bounds Dell van Melkebeek sparsification pdf
- Boolean circuit fan in two essential variables size lower bound input dependence
- exact model counting variable elimination sharing circuit size lower bounds knowledge compilation
- Pippenger Fischer Relations Among Complexity Measures pdf 1979

The IJCAI 2024 primary abstract Compilation and Fast Model Counting beyond CNF [10] was also inspected. Its distinction between compilation and direct counting reinforces the scope guard; no theorem from its full proof is imported.

Connected GitHub search queried SAT presolve model counting compression separately under anthropics, openai, xai-org, google, google-research and google-deepmind. Follow-ups were SAT solver under Anthropic and xAI, SAT circuit under OpenAI, constraint satisfaction and sat solver under Google Research, constraint satisfaction under DeepMind, and 2-SAT solver example within jraph. Web fallback used site:github.com/<owner> SAT solver for xAI, Research, and DeepMind.

Official ownership was checked through verified organization domains for Anthropic and OpenAI, xAI's corporate grok-os release link, Google's OR-Tools installation documentation, the Google Research resources page, and DeepMind's corporate publication link. Ownership proves provenance, not correctness of the code.

| Official source inspected | Commit and relevance |
|---|---|
| anthropics/mockturtle, lib/bill/bill/sat/solver/abc/Solver.h | 852605f5ad0f8f4c90b6e1dc8cabff11e0a3c75e. Vendored Glucose/MiniSat-derived code has conflict/propagation budgets and a three-valued limited solve. No new Anthropic theorem or polynomial guarantee inferred. |
| openai/math, lean/OAI/Algorithms/SubexponentialSAT/PackedSAT.lean | 4eaee87548250b2682affda7d05d947c05554bae. Semantic counting/decision pipeline separates correctness and leaf-call counts from machine runtime; noncomputable constructions and possibly overlapping decision leaves prevent importing a paid exact-count algorithm. Imports and kernel were not fully audited. |
| google/or-tools, ortools/sat/sat_parameters.proto | 4782dbd0aa85621c8115cf33de1574a2e6757004. Bounded variable elimination checks occurrence products and representation growth; feasible-solution-preserving presolve differs from ordinary decision presolve. This concretely motivates charging reduction cost and count multiplicities. |
| google-research/google-research, smug_saliency/masking.py | 87e25a5ba04d2c4cf0108f0cec96d648fe2b945a. Z3-backed saliency application with timeout and SAT/UNSAT/UNKNOWN handling. No lower-bound theorem. |
| google-deepmind/jraph, jraph/examples/sat.py | 51f5990104f7374492f8f3ea1cbc47feb411c69c. Learned 2-SAT example on finite training/test sizes; no all-input exact algorithm or lower bound. |
| xai-org | No relevant result in the bounded searches. Broad SAT solver hits at 2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8 were saturating/UI-layout false positives. No xAI file was deeply reviewed. |

One xAI search returned HTTP 429 and succeeded on a later retry with no relevant matches. Connected jraph search missed the example located by web fallback and fetched directly. An initial Dell URL without the author-home tilde was inaccessible; the correct author URL succeeded. External source code was inspected but not executed. No theorem prover kernel was run. These searches identify relevant methods and barriers; empirical code is not evidence of unrestricted asymptotic hardness.

## 9. One next dependency

**T5-SHARED-INTERACTION1, Bounds with Redteam review:** define a two-block interaction measure on the actual encoded count map, then prove or falsify a bound on its decrease under ONE shared fan-in-two gate, including arbitrary fanout and cached algebra. The initial demand must be independently proved and exceed the input-support ceiling; counting pairs of sensitive bits is not sufficient without the per-gate bound. This is the next test, not an established theorem or a claim that the present easy family is hard.

P versus NP, unrestricted superpolynomial exact-counting bounds, and the separate decision lower-bound bridge remain OPEN.

## References

[1] [Current handoff at recovery head](https://github.com/j15marti/pnp/blob/2f50f80fbd579bdc04ca0fbf24626ee63a20897e/research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md), especially Sections 3-6 and 16-21; blob a886f3387a8676b9cc86afbf3bebf22630109d49. Baseline scope is retained, not independently recertified.

[2] [Bounds, T5-DISJ-COUNT-CIRCUIT1](https://github.com/j15marti/pnp/blob/a8459529ba2511d359418bf7ac9b96d802f31ffc/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-21_135900_Disjoint_Encoded_Count_Circuit.md). Its original code and raw evidence were recovered without repeating its completed experiment.

[3] [Construction, T5-DISJ-ORBIT-WIDTH1](https://github.com/j15marti/pnp/blob/2303eb12b08af4eaaf5e0a94e4097eb1599c835f/research/agents/charged-construction/PNP_Charged_construction_2026-11-21_143200_Disjoint_Orbit_Width.md); [Synthesis, orbit certificate](https://github.com/j15marti/pnp/blob/ecdeffc5cc65913ed74bed05ba1cfb53ca329f02/research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-21_141900_Orbit_Certificate_Gap.md); [Redteam, canonical admission](https://github.com/j15marti/pnp/blob/960c4be768d6e9667b9d27db2ef36b3602dc54a3/research/agents/charged-redteam/PNP_Charged_redteam_2026-11-21_140800_Canonical_Admission_Audit.md). These retain their external-review qualifications.

[4] [TMR-4/006, exact-prefix and residual-sensitivity product](https://github.com/j15marti/pnp/blob/2f50f80fbd579bdc04ca0fbf24626ee63a20897e/research/agents/tmr-4/2026-11-13_1737_TMR4_PREFIX_SENSITIVITY_PRODUCT006.md). Generic coupling and no-double-charge precedent, with its original candidate status preserved.

[5] Riedel MD, Bruck J. [Cyclic Boolean Circuits](https://www.paradise.caltech.edu/papers/etr099.pdf). Author preprint, 3 December 2009, Section 3.1.

[6] Pippenger N, Fischer MJ. Relations Among Complexity Measures. JACM 26(2):361-381, 1979. [Author repository and abstract](https://scholarship.claremont.edu/hmc_fac_pub/597/), [attempted paper copy, unavailable with HTTP 403](https://www.ccs.neu.edu/home/viola/classes/papers/PippengerF-Oblivious.pdf).

[7] Darwiche A, Marquis P. [A Knowledge Compilation Map](https://www.cs.cmu.edu/afs/cs.cmu.edu/project/jair/pub/volume17/darwiche02a.pdf). JAIR 17:229-264, 2002.

[8] Fortnow L, Santhanam R. [Infeasibility of Instance Compression and Succinct PCPs for NP](https://lance.fortnow.com/papers/files/compress.pdf). Author version dated 19 March 2010; JCSS 77(1), 2011.

[9] Dell H, van Melkebeek D. [Satisfiability Allows No Nontrivial Sparsification Unless The Polynomial-Time Hierarchy Collapses](https://pages.cs.wisc.edu/~dieter/Papers/sparsification-jacm.pdf). JACM 61(4), Article 23, 2014.

[10] de Colnet A, Szeider S, Zhang T. [Compilation and Fast Model Counting beyond CNF](https://ijcai.org/proceedings/2024/367). IJCAI 2024:3315-3323. Abstract-level scope check only.

[11] Official sources: [Anthropic verified organization](https://github.com/anthropics/), [OpenAI verified organization](https://github.com/openai), [xAI corporate link](https://x.ai/news/grok-os), [Google OR-Tools corporate installation page](https://developers.google.com/optimization/install/python/source_linux), [Google Research resources](https://research.google/resources/), [DeepMind corporate repository link](https://deepmind.google/research/publications/122591/).

[12] Inspected code: [Anthropic vendored solver](https://github.com/anthropics/mockturtle/blob/852605f5ad0f8f4c90b6e1dc8cabff11e0a3c75e/lib/bill/bill/sat/solver/abc/Solver.h), [OpenAI PackedSAT](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/lean/OAI/Algorithms/SubexponentialSAT/PackedSAT.lean), [Google OR-Tools parameters](https://github.com/google/or-tools/blob/4782dbd0aa85621c8115cf33de1574a2e6757004/ortools/sat/sat_parameters.proto), [Google Research SMT application](https://github.com/google-research/google-research/blob/87e25a5ba04d2c4cf0108f0cec96d648fe2b945a/smug_saliency/masking.py), [DeepMind Jraph example](https://github.com/google-deepmind/jraph/blob/51f5990104f7374492f8f3ea1cbc47feb411c69c/jraph/examples/sat.py).
