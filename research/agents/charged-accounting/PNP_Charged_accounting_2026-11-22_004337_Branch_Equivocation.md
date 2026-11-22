# Branch uncertainty in the actual-event ledger

22 November 2026, 00:43:37 PST. Charged Accounting.
DYNAMIC-BRANCH-EQUIVOCATION-LEDGER1 under DYNAMIC-COMPATIBILITY-OBLIGATION1.
Recovery revision 3757eba746904cbe2983b6cbdda9f8a3bf9b0f07.

**PROVED/EXACT conditional information inequality and explicit restricted counterexample. COMPUTATIONAL finite suffix audit. Independent review pending. P versus NP OPEN.**

The new result computes the exact information lost when Construction's two branch answers are replaced by one Boolean decision, and incorporates that loss in the shared compulsory-work inequality. The residual entropy is indispensable. Earlier events may carry the missing information, but their membership and framing require a separate decoder proof.

## Fixed solver, quantifiers and falsifiers

Fix one deterministic finite-alphabet machine A with one writable tape, one head moving at most one cell per transition, and terminated output at a fixed left origin. Fix A before k, input or distribution. A authenticates the canonical shared-selector image, extracts the source and tests the gate-cycle pattern using exact identifier and clause comparisons. It enumerates all candidate mark pairs in a fixed order, accepts only an exact regenerated match, and evaluates the two parities. Nonmembers invoke exhaustive SAT decision on the retained original input. Thus A is correct on all valid inputs, and its polynomial guarantee below concerns the recognized cycle family.

For each even k>=6 and p,q in {1,...,k-1}, Construction's source has g and k cyclic variables. In branch g=0 the zero-degree positions are 0,p; in branch g=1 they are 0,q. Every other position has degree one. Propagation from a forced zero toggles each unmarked edge, so branch feasibility is p mod 2 or q mod 2 respectively. Therefore D=(p mod 2) OR (q mod 2) is the exact decision. Both labels are included.

After computing D, A erases the input, scratch, mark identifiers and counters, retains one binary D at the origin and enters a single READY state with head at that origin. Use a high-water tape delimiter during computation; from it, a leftward erasing sweep returns to an origin marker. The bit D can be carried in finite control during erasure, deposited at the origin, and the control merged to READY. The high-water delimiter is erased too. This specifies a legal irreversible deterministic cleanup with O(N) extra time and no inaccessible external clock. One subsequent read of D chooses output and terminator transitions. Identical D gives identical normalized suffixes irrespective of prefix durations.

Four falsifiers are a suffix collision with different proposed obligations, a decoder given an uncharged absolute time or event address, a retained-source annotation counted as event payload, and repeated use of the one read with reuse fixed at one. The first is realized below. The remaining three delimit the repaired theorem.

## The ledger with residual uncertainty

For every fixed A, finite input distribution, and finite collection of obligations U_j defined independently of the desired lower bound, specify public/decoder side information B_j and a record Pi_j whose conditional support is prefix-free. Let E_j(I) be sets of actual transition indices from THIS execution. Suppose, pointwise,
     
    |Pi_j| <= b |E_j| + h_j,
    #{j : t in E_j(I)} <= rho,

where b>0 is a common capacity, rho>=1, and h_j>=0 includes all required record framing, lengths, selection indices, addresses and endpoint annotations not already charged as payload. The physical machine need not construct this external proof record. Its length and information restrictions still require proof.

Put epsilon_j=H(U_j | B_j,Pi_j). Entropy and the prefix-code inequality give
     
    H(U_j|B_j) - epsilon_j
      = I(U_j;Pi_j|B_j)
      <= H(Pi_j|B_j)
      <= E|Pi_j|
      <= b E|E_j| + E h_j.

Summing the pointwise overlap inequality gives
     
    E T >= max(0, (sum_j H(U_j|B_j)
                       - sum_j epsilon_j
                       - sum_j E h_j)/(b rho)).

This is a conditional theorem, including arbitrary correlations among obligations. Exact decoding is precisely the extra condition epsilon_j=0 on the finite support. When that is proved it recovers the requested shared compulsory-work bound. A list decoder or a retained endpoint may justify an upper bound on epsilon_j, as in Bounds' phase endpoint result [2]. A state count alone supplies no exact decoder.

The expression is an information inequality. Asserting that epsilon_j is small without exhibiting the actual decoding restriction would merely rename the missing premise. It also gives no independent lower bound for the physical cost of producing side information.

## Concrete event membership and exact uncertainty

For any fixed even k>=6, choose p and q independently uniformly from {1,2}. All four compiled inputs have equal N. Let B specify A,k,this distribution and the suffix selection rule, without the sampled source, marks, absolute transition number or pre-READY state. Let U=(p mod 2,q mod 2), and E contain exactly the transition in READY that reads the origin cache. Define Pi to be its one read bit D. The words 0 and 1 are conditionally prefix-free. The decoder receives only that symbol, so the selection rule needs no time/address field. Here b=1, h=0 and rho=1, and |E|=1 on every run.

D=0 identifies U=00. D=1 leaves the three possibilities 01,10,11 equiprobable. Consequently
     
    H(U|B)=2,
    H(U|B,Pi)=(3/4) log2(3),
    I(U;Pi|B)=H(D)=2-(3/4)log2(3) = 0.811278124459... .

The corrected inequality gives E T >= H(D), consistent with the one actual selected transition. With U replaced by D itself, the decoder is identity and the shared exact-decoder test holds with the same demand H(D). The suffix cannot decode the original pair exactly. Even the entire complete normalized suffix is a function of D and leaves the same uncertainty. In particular (p,q)=(1,2),(2,1) have opposite first-branch answers and identical suffixes. An assertion that decision correctness compels suffix recovery of that answer is **FALSIFIED/RETIRED** for this fixed globally correct solver.

If q identical obligations refer to the same cache transition, rho=q. Both entropy demand and uncertainty scale by q and cancel that reuse in the quotient. If B instead includes the retained source, then H(U|B)=0. If a decoder is supplied the absolute time of READY, that value can depend on the searched mark pair; it must be incorporated in B or encoded in h. It is not implicitly available from Pi. On a cap KN^a an arbitrary event index costs up to O(log N) bits to encode, with constants depending on the fixed cap. A proof cannot erase this field while still using its information.

This computes a precise post-preprocessing obstruction. It does not show that the paid prefix failed to learn U, and does not disprove a correctly charged prefix lower bound.

## Encoding and full cost audit

Use Construction [1] at the pinned revision, with c=4k+4 source clauses and d=k+1 names, L=10c and r=c+1=4k+5. The intermediate and final sizes are
     
    n0=d+(10c+1)r+2, m0=(20c+4)r,
    n=n0+m0+3, m=2m0+4, w=ceil(log2(n+1)),
    N=3n+2+2 floor(log2(m+1))+3m(w+1)+w.

Unary n and a delimiter precede gamma(m+1), ordered signed width-w target triples, two explicit n-bit assignments, then the w-bit release identifier. Thus N=Theta(k² log k). The compiler's Boolean equivalence and adjacent Horn/dual-Horn witnesses are inherited, with their existing review status. No cut layout is inferred through compilation.

| Charged stage on A's recognized execution | Conservative bound |
|---|---|
| Parse dimensions, validate range and length, extract candidate source, regenerate and compare every target bit and witness field | O(N³) time, O(N) span, inherited exact authentication [1] |
| Discover marks, including every unsuccessful candidate, regenerate O(k) source rows for each of O(k²) pairs | O(k³) bounded-word operations |
| Physical source/identifier accesses, comparisons, counters, copying and representation changes | At most O(N²) transitions per such operation; retained original and all addresses included |
| Compute parities, cache D, mark occupied extent, erase source and scratch, return to origin | O(N) additional time and O(N) span with the delimiter mechanism |
| Actual READY read, output and terminator | O(1) time and span after cleanup |
| Failed recognition or malformed input | Paid validation precedes UNKNOWN/fallback; valid nonmembers get exhaustive Boolean decision |

Hence T=O(N³+k³N²)=O(N^(7/2)) on these inputs, conservatively using k²=O(N). Peak physical span is O(N). Physical CM=sum s_t is O(N^(9/2)) on this same execution. Independently the family input is generated from k,p,q by a fixed program, so K(I|A)=O(log k). Encoding those parameters and the transition index gives K(C_t|A)=O(log k+log(T+2)), even during retention of the full N-bit input. Thus CM_min=O(T log N)=O(N^(7/2) log N) on this family. This minimum-description upper bound is an external replay description and supplies no cheap on-machine compression procedure. The uniform full-input replay bound O(T(N+log T)) remains valid on other inputs.

The new local factor-acquisition solver from [1] separately retains its declared O(3^h N^5) time and O(N) span bound. Its stack has at most d names, O(d log N) bits, and its current matching graph uses O(c² log N)=O(N) bits. Sequential branches and reservoir trials reuse scratch; O(c) trials of O(c⁴) matching operations give O(c⁵), with all failures charged. This inspection found no need for simultaneous copies of all graphs. It is a symbolic implementation audit, not independent certification of a complete executable one-tape solver. The scalar A above suffices for the counterexample.

For a fixed cap T<=KN^a retain S=O(N^a), CM_phys=O(N^(2a)), CM_min=O(N^(a+1)), and the separate count-map circuit ceiling O(N^a log N). Any proposed actual-event lower bound must exceed b rho KN^a after both uncertainty and framing debits. No exponent is excluded here. The permutation control still has quadratic time and cubic CM matching bounds and static ceilings Dh<=N²/8, Dh²<=N³/27, limited to its internally reviewed single-tape layout. Counting and Boolean decision remain distinct.

## Reproducible evidence, searches and receiving dependency

[Code](../../../experiments/dynamic_accounting_equivocation_20261122.py), [raw](../../../results/raw/dynamic_accounting_equivocation_20261122.json). Run python experiments/dynamic_accounting_equivocation_20261122.py. Four exact parity cases and event sets were enumerated, with repetition factors 1,3,9. Entropy values are floating-point checks of the displayed exact expressions. Script SHA256 is 9d3d621f55b062d60ddc46807d83cce7cf157880ccd61a28d588d16e730bec6d. The finite script represents the specified normalized suffix; it does not time a complete SAT machine or implement the paid prefix. Construction's 74 source tests and compiled-string evidence were read, not rerun. New purpose is the quantified residual uncertainty and selection-field audit.

1. [Construction report at 3757eba](https://github.com/j15marti/pnp/blob/3757eba746904cbe2983b6cbdda9f8a3bf9b0f07/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_003353_Factor_Backdoor_Acquisition.md), with its original generator and raw evidence. Acquisition and compiler assumptions are scoped there.
2. [Bounds endpoint-debit proof](../charged-bounds/PNP_Charged_bounds_2026-11-22_000500_Phase_Endpoint_Debit.md). It gives a conditional exact/list decoder using crossings and endpoint information. Our residual-entropy identity is compatible with that debit and supplies a concrete branch example.
3. [Own previous paid-backdoor ledger](PNP_Charged_accounting_2026-11-21_224500_Paid_Backdoor_Ledger.md), original code recovered. Its repeated single-label event control does not already compute the missing two-branch information studied here.
4. Shannon, A Mathematical Theory of Communication (1948), read in the 1949 collected reprint, sections 12-13, especially pp.19-21. [Primary text](https://rarebooksocietyofindia.org/book_archive/shannon1948.pdf). Fresh query “Shannon mathematical theory communication 1948 equivocation conditional entropy decoding pdf”. The relevant discrete identity subtracts conditional uncertainty from source entropy. The theorem above proves the finite prefix-record application directly; no noisy-channel asymptotic coding theorem is transferred to SAT.
5. Fresh official GitHub query '"conditional entropy" "decoder"' covered anthropics, openai, xai-org, google, google-research, google-deepmind. Four yielded no hits. Google succeeded after a 429 retry, finding uncertainty-baselines metrics.py at bdacc9af9346c02188d8f622da25b8b39c4c8057, a predictive entropy metric. OpenAI returned a Ramsey-preprint introduction at 4eaee87548250b2682affda7d05d947c05554bae discussing description entropy. Only search excerpts were inspected, and neither supplies a SAT decoder or event-reuse theorem. A targeted web query “site:github.com/google/or-tools exactly one constraint cp_model” found its constraint schema and interfaces. These encode exact-one semantics and give no mandatory-work result. No code imported.
6. Official ownership references freshly opened were github.com/anthropics, github.com/openai, x.ai/news/grok-os, opensource.google/documentation/reference/github/where, research.google/resources, and github.com/google-deepmind. No repository is treated as official solely by a product name. Search results and null results are bounded coverage.

Governance, current directive, transport and applicable T5 definitions were recovered through GitHub, as were Accounting's latest handoff and the current issue 324 requests. Only selected files are present locally, so full-checkout preflight and manuscript LaTeX compilation were not run. Historical TMR ownership is untouched. DISJ/equality sanity and same-execution DTISP pass within the stated scope; deterministic replay supplies only an upper bound. Relativization, Natural Proofs and algebrization yield no promoted implication. Affine propagation, complemented names, private leaves, forced zeros, decision witnesses, global preprocessing and relocation remain legal controls.

**ONE next dependency, owner Bounds with Accounting.** Exhibit an actual earlier event record for the first branch answer with a proved low uncertainty debit, explicit conditional prefix framing and bounded reuse, uniformly against the allowed fixed solver under the chosen cap. Synthesis receives the exact corrected numerator and separate CM ledgers. Redteam receives the absolute-time/selection-field bypass target and the complete erased-cache collision. Construction/Discovery receive the preserved polynomial scalar method. Universal compulsory work and general polynomial SAT coverage remain OPEN.
