# Charging the choice of an observed event

22 November 2026, 03:56:05 PST. PNP Lower Bound Connections.
**DYNAMIC-EVENT-SELECTION-DECODER1**, within DYNAMIC-COMPATIBILITY-OBLIGATION1.
**PROVED/EXACT** conditional coding lemma and restricted counterexample. Independent adversarial review pending. P versus NP **OPEN**.

The new premise under examination is whether any input-dependent subset of actual transitions can be supplied to a decoder at the cost of its read symbols alone. That premise is false. The identities of the selected events can encode the obligation even when all selected symbols are identical. The existing shared entropy inequality remains valid when its record-length premise includes these identities or proves that the decoder can reconstruct them.

The target is prompted by the outstanding earlier-observation dependency at revision c97d245967c8ed3c3c2abae6f1b42978b0ca65ec. The latest Construction family has a polynomial relation evaluator. Discovery now gives a static 2-SAT branch on that family. Neither report claims that arbitrary event selection has constant description cost. This report supplies an explicit check required before a new compulsory-decoder application.

## Quantified coding lemma

Fix a deterministic solver A, a finite input distribution X, and a finite list of obligations U_j(X) defined from the inputs independently of a desired runtime bound. All runs halt in at most L transitions. For each j let B_j be declared side information containing L and the record conventions. Let E_j(X) be a subset of actual transition numbers from 1 through T_A(X), with k_j=|E_j|. Each selected transition contributes a payload from an alphabet of at most 2^b possibilities, encoded in b bits, where b is a positive integer. No input-dependent event address, timestamp, state or other annotation is included in this alphabet without counting its bits.

Assume an exact decoder computes U_j from B_j, the sorted set E_j, and the payload sequence P_j. Assume also that every actual transition belongs to at most ρ of the sets E_j on each input, for a deterministic ρ≥1. Define

s_j = ceil(log2 binom(L,k_j)),
g_j = 2 floor(log2(k_j+1))+1,
h_j = g_j+s_j.

There exists a conditionally prefix-free record Π_j of length h_j+b k_j decoding U_j. Encode k_j+1 using the binary gamma code, the lexicographic rank of E_j among the k_j-element subsets of {1,...,L} in s_j bits, and the sorted payload sequence in b k_j bits. For fixed B_j, the gamma prefix determines the remaining two lengths. Distinct k_j have incomparable gamma prefixes, and for fixed k_j the remaining records have fixed length. The decoder recovers E_j,P_j and invokes the assumed decoder. Hence

H(U_j|B_j) ≤ E|Π_j| = E[h_j]+b E[k_j].

Sum these inequalities and use the pointwise bound sum_j k_j≤ρ T_A(X). This proves

E[T_A(X)] ≥ (sum_j H(U_j|B_j) − sum_j E[h_j])/(bρ).

This is an information code, so enumerating subsets need not be an efficient physical operation. Any claim that the solver constructs this record must separately pay for that construction. For the lower-bound proof, decoder existence suffices, while actual event membership and reuse must still be proved.

If event selection is reconstructible from B_j and an already self-delimiting payload record, the rank field can be omitted by a new decoder proof. An observer's knowledge of E_j is itself information. Moving E_j into B_j changes H(U_j|B_j), often reducing it to zero. A fixed tape alphabet alone does not bound the information in a transition's absolute address or timestamp.

The logical premises about decoding, actual membership and overlap are CONDITIONAL for an arbitrary SAT solver. This theorem proves the coding implication once they hold. It does not derive compulsory U_j from decision correctness.

## Concrete counterexample on the synchronized cycles

Use Construction's exact family with t≥4 a power of two, top word W∈{A,C}^t and bottom word A^t. Let ℓ=log2 t and U be the ℓ-bit encoding of the first ℓ symbols of W, A=0 and C=1. Let W be uniform. Thus H(U)=ℓ. This is an ordinary explicit source substring, defined before choosing any observation.

The per-column joint relation is A={(0,0),(1,1),(1,0)} if W_i=A, and D={(1,0)} if W_i=C. A closed walk exists when W=A^t, via a diagonal. If there is a D step then the walk strictly decreases there and never increases anywhere, making closure impossible. Consequently both labels occur at every t. The fast algorithm is correct on the entire synchronized family, and exhaustive fallback handles all other valid inputs.

Fix one solver A* before t and W. Use the pinned authenticated family evaluator, retaining the input until admission and decision. After computing the answer, store it at origin. Clear the used workspace except for public length metadata and the answer. Prepare a run of t blank cells between two markers. Enter a fixed sweep state and move right over these t cells, reading and rewriting the blank symbol identically at each step. Return to the origin and emit the cached Boolean answer with its terminator. The sweep is an actual part of this legal decision execution. Its length and transition types are independent of W. No other device supplies input or clock information.

Define E(W) to be the one transition at relative sweep position U+1. Every E contains a real event and k=ρ=1. B contains t, generator, distribution, A*, and the relative sweep convention. It excludes W, U and the selected index. All symbol payloads are the same blank, represented by 0 with b=1. Thus the symbol-only record has zero entropy and cannot decode U. Supplying the relative index recovers U exactly. Its fixed-length ℓ-bit code is conditionally prefix-free. The indexed record (index,0) uses ℓ+1 bits. Treating that record as a one-bit record violates the length premise.

Because k=1 and the eligible sweep has publicly known length t, a direct local index code has overhead h=ℓ and no count field is needed. Then H(U|B)−h=0. The selected payload contributes no surviving entropy demand. Equivalently, giving the index freely in B yields H(U|B,E)=0. Neither convention creates compulsory work beyond the already charged execution.

The set is selected mathematically using W. It is not identified by A* as a distinguished transition. This is precisely why it tests the permissive claim about arbitrary input-dependent event sets. A model-enforced observer must either produce its selection information through charged events or have a valid decoder that does not need that information. Correctness alone does not single out this dummy event. Earlier input reads are fully charged and remain possible targets for a different theorem.

For a genuine decision obligation V, take E_V to be the final origin-cache read, Π_V the answer bit and B_V the public protocol. Then b=1,h=0,ρ=1, the identity decoder is valid and the two records are prefix-free. Under the W distribution above H(V|B_V)=h_2(2^(-t))≤1. The obligation and distribution therefore concern both labels. This valid ledger coexists with the invalid substring decoder.

## Model, encoding and full costs

The model is the transport report's finite-alphabet, single writable tape, one-head deterministic machine. Primitive head moves have distance at most one. Input, copies, caches, counters, source, address storage and output reside on the same tape. The origin, head and nonblank support determine charged span s_r. Physical CM is sum_r s_r. Minimum-description CM is separately sum_r K(C_r|A*). No unrestricted machine-model transfer is asserted.

The family has d=8t source names and c=26t proper source clauses. For the canonical adjacent-witness encoding let g=max(3,2 floor((c+1)/2)+1), n0=d+(10c+1)g+2, m0=(20c+4)g, n=n0+m0+3, m=2m0+4 and w=ceil(log2(n+1)). Its full length is
N=3n+2+2 floor(log2(m+1))+3m(w+1)+w=Θ(t² log t).
This counts the unary declaration, clause list, two witness assignments and release identifier. Boolean semantics and the layout are inherited from the pinned compiler proof. No order of semantic constraints is imposed on subsequent computation.

Parsing, canonical regeneration, authentication, failed family candidates, word extraction, paired-word addresses, relation updates, retaining the source, and output fit the inherited O(N³) time and O(N) span on this family. Preparing markers and blank cells, erasing sources and copies, establishing the sweep start, executing and returning from the sweep can conservatively be done in O(N²) additional time and O(N) span. All dependence on t is stored and accessed on tape. Hence A* retains T=O(N³), S=O(N), physical CM=O(N⁴). Independently, the original input and time index describe each deterministic configuration in O(N+log(T+2)) bits, giving minimum-description CM=O(N⁴). General valid nonmatches use the retained formula for exhaustive decision, with bound O(N³+2^n N³). These are symbolic implementations using the pinned authentication tariff.

The external coding of E is neither free access for A* nor an extra physical transition performed by A*. It is information in a proposed proof record. Any executable observer calculating E must pay parsing W and its index computation in its own declared ledger, and cannot silently add that observer to every solver's execution.

Under a fixed cap T≤K N^a, a≥1, use L=ceil(K N^a) in the general lemma. For k=1, selector overhead can be Θ(log L). A positive lower bound requires demand exceeding the full h and bρK N^a comparison on the same input distribution. The ceilings remain S=O(N^a), physical CM=O(N^(2a)), minimum-description CM=O(N^(a+1)), and separately count-map circuit size O(N^a log N). No polynomial exponent is excluded here. The internally reviewed permutation transport theorem retains its matched quadratic-time and cubic-cumulative scope and static ceiling.

## Falsifiers and evidence

Four tests delimit the claim. Supplying the selected index for free invalidates the payload-only capacity. Conditioning on that index removes the alleged new entropy. Selecting the same transition for multiple obligations raises ρ. Claiming that every solver executes the added sweep fails because the sweep is a legal optional routine, used here to refute a universal record inference.

The finite script checks the new selection example at t=4 and t=8, covering 16 and 256 top words. The label totals are 1 SAT and 15 UNSAT, then 1 SAT and 255 UNSAT. U is uniform in each case. There is one payload value, while there are t distinct indexed records. This checks record ambiguity and the both-label subfamily. It does not repeat Construction's whole-family SAT audit, simulate a full tape transition table, or independently validate the canonical compiler.

[Checker](../../../experiments/dynamic_bounds_selector_20261122.py) · [Raw evidence](../../../results/raw/dynamic_bounds_selector_20261122.json)

DISJ/equality sanity PASS as polynomial controls. Simultaneous DTISP PASS for the one fixed execution. Deterministic-configuration accounting PASS for its upper description bound. Relativization, algebrization and Natural Proofs give no unrestricted implication here. Affine/Tseitin, complement, relocation, forced-domain, private-leaf and cached-decision controls remain permitted. The conclusion concerns Boolean decision. No strict T5 counting, symmetric C or ordered R claim is inferred.

## Primary sources, searches and receiving dependency

Fresh literature query was “Clifford Jalsenius information transfer encode addresses contents 2w cell probe convolution”. The Bristol copy of arXiv 1101.0768v4 returned HTTP403, and the arXiv PDF fallback was unavailable. Search excerpts were recorded only as leads.

Read Clifford, Jalsenius and Sach, *Cell-Probe Lower Bounds for Bit Stream Computation*, ESA 2016, §3.1 Lemma 4 and its replay decoder. With w-bit addresses and cell contents, its conditional output entropy is bounded by 2w+2w E[I+G]. The code stores both addresses and contents of transfer cells and two size fields. Its decoder simulates known outside updates and uses encoded values for omitted-interval dependencies. The surrounding model requires answers during online arrivals. This supports charging selection metadata, but its online decoder premise is absent for offline SAT. Our combinatorial subset code is proved independently above. [Primary paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol057-esa2016/LIPIcs.ESA.2016.31/LIPIcs.ESA.2016.31.pdf)

Fresh GitHub searches for `"information transfer" "address"` in anthropics, openai, xai-org, google, google-research and google-deepmind returned no hits in five organizations. Google returned protocol and replay-builder excerpts. They address protocol transfer and pointer loads and supply no compulsory-decoding theorem. Inspected excerpt revisions were google/pebble 4051c5bb97377f1215bbd26094c1a157532c55fe, docs/pulse2/pulse2.md, and google/gapid 15b44454df3a2469ee9ba42cb116d9b50786c7a4, gapis/replay/builder/builder.go. No external code was imported. Official ownership was checked through corporate GitHub profiles and official links. [Anthropic](https://github.com/anthropics) · [OpenAI](https://github.com/openai) · [xAI](https://x.ai/news/grok-os) · [Google](https://opensource.google/documentation/reference/github/where) · [Research](https://research.google/resources/) · [DeepMind](https://github.com/google-deepmind)

Mandatory governance, model and T5 definitions, current handoffs, the latest Bounds report and its preceding decoder theorem, Construction report/code/raw, Discovery's new proof, Accounting's ledger and issue324 were recovered at c97d245967c8ed3c3c2abae6f1b42978b0ca65ec. Root SKILL.md was absent, and the required .codex/skills/pnp-research/SKILL.md was then recovered. A complete checkout was unavailable, so full-checkout preflight and LaTeX compilation were not run. No historical TMR manuscript ownership was assumed.

[Construction and original evidence](https://github.com/j15marti/pnp/blob/6dc52153d4e0c60fa778a44334910057721cd120/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_033149_Synchronized_Cycles.md) · [Discovery bypass](https://github.com/j15marti/pnp/blob/c97d245967c8ed3c3c2abae6f1b42978b0ca65ec/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-22_034845_Mixed_To_Binary.md)

**One next dependency to Accounting and Synthesis.** For the next earlier compulsory observation, give a decoder that locates its events from public side information and charged payloads, or debit the complete selector code. Then prove that the resulting entropy minus overhead is positive after joint preprocessing. Redteam receives the concrete blank-sweep selector as a falsification target. Construction and Discovery retain their polynomial bypasses. A general polynomial algorithm and an unrestricted lower bound both remain OPEN.
