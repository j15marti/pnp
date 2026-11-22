# Circular-anchor obligations after paid aggregation

22 November 2026, 07:46 PST. PNP Charged Accounting.
DYNAMIC-ANCHOR-DECODER1 within DYNAMIC-COMPATIBILITY-OBLIGATION1.

PROVED/EXACT for the fixed protocol and the explicit two-source decoder counterexample below. COMPUTATIONAL for the eight-source fiber classification. The complete physical upper tariff remains conditional on the inherited compiler authentication implementation. Independent review requested. P versus NP OPEN.

## Revision and scope

Construction's circular-occurrence report, source and raw evidence were read at commit 5ed5f9f1a66e50ecf517d1382a2a3de3651781a5. The [report](https://github.com/j15marti/pnp/blob/5ed5f9f1a66e50ecf517d1382a2a3de3651781a5/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_073529_Circular_Occurrences.md) supplies the source and compiler. Latest Accounting matching-cache report, Bounds first-read handoff, Redteam pivotal-read handoff, Synthesis compiled-support handoff and issue324 were recovered. The new question concerns three alternative anchors of one overlapping exact-cover instance. Earlier work treated independent matching components and is preserved.

Fix one uniform deterministic globally correct SAT solver A before the input. It operates on one finite-alphabet writable tape with a single unit-moving read-before-write head and origin output. On an exactly authenticated canonical image, it recognizes the circular-occurrence source and tries anchors in increasing name order, using the shared arc table. It may stop at the first successful anchor. On failed recognition it uses exhaustive SAT on the retained original. It then writes the decision D at the origin, clears every other used cell, returns to the origin and enters a common READY state. A reads D and produces the fixed terminated decision output. Clearing and the return are paid preprocessing. This normalization is a legal implementation choice and suffices for an existence counterexample to a universal obligation.

The source consists of positive exact-one triples. For each of the three variables x_j in row zero, let V_j mean that a satisfying assignment exists with x_j true. This is a semantic definition independent of A and of the desired bound. D=OR_j V_j. The tested implication is that decision correctness forces the READY suffix to decode all V_j from its charged observations and public size/protocol information.

Four falsifiers are two inputs with the same normalized suffix and different V, a hidden input-dependent address or timestamp, free access to retained source, and assigning one actual read to several demands while claiming reuse one.

## Explicit falsification

Use five ordered rows on five names. Write 012 for the exact-one equation x0+x1+x2=1.

F = (012,012,012,034,134).
G = (012,012,012,034,234).

All five names occur, every row has three distinct names, and each name occupies one circular interval in this order. In F, the last two equations force x0=x1. The first equation over Boolean values forces x0=x1=0 and x2=1. The remaining equation requires x3+x4=1. Thus V(F)=001. In G, the last two equations force x0=x2, so the first forces x0=x2=0,x1=1, again with x3+x4=1. Thus V(G)=010. Both inputs are SAT. Their compiler parameter counts and encoded lengths agree because m=v=5.

After paid normalization, the complete configurations of A on F and G coincide. The state is READY, the head is at the origin, only the decision bit remains, and all other cells are blank. Every future transition therefore coincides. Public side information B consists of A, the fixed compiler, m=v=5, the prior and protocol, excluding source identity and absolute entry time. No decoder of (B, any record of this suffix) recovers V on both inputs. This proves the implication false even if every suffix transition is recorded. It does not refute a proposed decoder that uses paid earlier events.

The two-source uniform prior has H(V|B)=1 and D=1 surely. The eight-source computational extension realizes every vector in {0,1}^3 with the same m,v and first row. Under its uniform prior H(V|B)=3, Pr(D=1)=7/8, and H(V|B,D)=(7/8)log2(7). The seven-way SAT fiber needs at least three fixed-width additional bits for exact identification. Variable-length prefix advice conditioned on D has average length at least (7/8)log2(7). Such advice must come from charged events or be declared as side information. The missing decoder is already established by the analytic pair, independently of these finite counts.

## Valid actual-event ledger

For the normalized solver and any distribution on admitted images, define the single obligation U=D. B is the public protocol and any public size parameters, without the sampled source, cache bit or absolute preprocessing time. E is exactly the first actual transition after entry to READY. Its address is the origin and its state is fixed. Pi is the observed binary cache symbol. The conditional codebook is a subset of {0,1}, hence prefix-free. The identity decoder recovers U. Capacity b=1, overhead h=0 and maximum reuse rho=1 hold pointwise. The origin tag and output convention are fixed and contain no sampled information.

Consequently H(D|B) <= E[|Pi|] = E[|E|] = 1 <= E[T_suffix]. This is precisely the shared inequality with one obligation. Under the eight-source prior it gives E[T_suffix] >= h2(1/8), approximately 0.5435644432. The payload count is exactly one, with later output transitions charged separately. Three duplicates of the obligation U=D with this same event have rho=3, cancelling the threefold numerator. Changing U_j to V_j breaks decoding, as shown above.

This deliberately limited suffix decoder receives no retained source because A erased it before READY. If a different solver retains source, include its storage in the physical ledger and charge actual accesses. If the decoder instead receives source or complete observed preprocessing history freely, V and D become determined and their ordinary conditional entropy is zero. Neither convention makes earlier acquisition free or proves the computational cost of forming V.

## Complete cost audit

Put s=v+m. Construction uses t=5v+6m, r=3m, d=8t,c=26t+4r, g=max(3,2 floor((c+1)/2)+1), n0=d+(10c+1)g+2,m0=(20c+4)g,n=n0+m0+3,M=2m0+4. With w=ceil(log2(n+1)),

N=3n+2+2 floor(log2(M+1))+3M(w+1)+w=Theta(s^2 log(s+1)).

Fields include unary n, gamma clause count, signed identifier triples, both n-bit witnesses and the release identifier. All equal-size examples above have the same headers and field lengths. The counterexample does not assume disjoint physical edit supports.

| Phase on the same admitted execution | Work and retained representation |
|---|---|
| Parse, inverse, regenerate and compare | Inherited O(N^4) sole-tape time and O(N) span, original retained for failed-guard fallback |
| Dense incidence construction | mv bits, source rows and O(log s)-bit names/counters, bounded scans and initialization |
| Arc detection | Check every column, cyclic seam and full columns, O(s^2 log^2(s+2)) indexed bit operations |
| At most three anchor trials | At most 3mv edge examinations and O(m) reachability flags reused between trials, O(s^2 log^2(s+2)) indexed bit operations |
| Cache, relocation, clearing and return | O(N^2) conservative physical time, O(N) span, one cached bit survives |
| READY and output | O(1) transitions and live span after clearing |
| Failed recognition | Bounded work above followed by exact exhaustive SAT, O(N^4+2^n N^3) conservative time, O(N) span |

Since s^2 log^2(s+2)=O(N^2), even the conservative O(N^2) physical simulation charge per indexed bit operation fits O(N^4). Address arithmetic, table accesses, failed anchors and clearing are included. The three trials multiply a polynomial bound by at most three. They share one incidence table and one reachability workspace.

Thus the new source-solving phase preserves the published restricted O(N^4) time, O(N) span tariff. Full-image authentication remains an inherited symbolic implementation premise, independently unexecuted here. For that implementation, summing actual per-step span gives CM_phys=O(N^5). Separately, input plus transition index describes each deterministic configuration in O(N+log(T+2)) bits, giving CM_min=O(N^5). This is an upper description bound and does not identify information content with allocated storage. At READY the normalized live configuration has O(1) physical size and description, so its suffix cumulative costs are O(1). A convention charging maximum-ever-visited span would instead retain O(N) suffix physical charge and must be labeled separately.

For a fixed cap T<=KN^a, the entropy numerator must exceed b rho K N^a on the same inputs. Here it is at most one. General cap ceilings remain S=O(N^a), CM_phys=O(N^(2a)), CM_min=O(N^(a+1)), with count-map circuit size O(N^a log N) as a separate counting statement. No fixed polynomial cap is excluded. The original permutation control retains its internally reviewed single-tape quadratic/cubic bounds.

## Verification and searches

[Checker](../../../experiments/dynamic_accounting_anchor_fibers_20261122.py) and [raw evidence](../../../results/raw/dynamic_accounting_anchor_fibers_20261122.json). Python3, deterministic, no sampling. The new test varies the four tail rows over all 10,000 lists of triples on five names with row zero fixed to012. It admits 2,022 sources with all five names present and circular supports. For each admitted source, all32 assignments independently determine each anchor bit and agree with gap reachability. Eight representatives and their fibers are retained. This tests richer anchor semantics than the prior decision-only four-row experiment. The initial four-row test lacked the000 vector when all five names were required, so the dimension was increased to five rows before defining the eight-source prior. No full compiled image, native tape execution, kernel build or checkout preflight was run. Selected-file recovery supplied the governance documents, transport model and applicable T5 sections15,18,20.

Fresh literature query was "conditional prefix free entropy information transfer cell probe addresses Patrascu Demaine". Clifford, Jalsenius and Sach, *Time bounds for streaming problems*, Theory of Computing15(2),2019, version of record, sections2–3 and Lemma3.1 were read. For their online cell-probe setting with w-bit addresses, the conditional entropy of required output symbols is at most w+2w times expected information-transfer size. Their encoding charges cardinality, addresses and contents and supplies a simulation decoder. Future updates are unavailable when each answer is due. This supplies an accounting checklist. The present offline decision protocol does not require three intermediate anchor outputs, so that online premise does not transfer. [Primary PDF](https://research-information.bris.ac.uk/ws/portalfiles/portal/218447978/v015a002.pdf)

Fresh GitHub code search used org:ORG "exact cover" separately in anthropics, openai, xai-org, google, google-research and google-deepmind. Counts were32,158,0,34,0,4. Anthropic initially rate-limited and succeeded on retry. First-page results included unrelated Lean statements and Rust/rendering text. DeepMind's FormalConjectures/ErdosProblems/947.lean was inspected at2207c54d0dbe960de591d280f997b195bf3f6e28, blob60b927c9d2f361f2e87fd0a9ec9542f62a4e09b3. It concerns exact congruence coverings with distinct moduli and contains a sorry with an external proof link. Its scope does not provide the required offline decision decoder. No external code or kernel build was executed. OpenAI math search hits were at4eaee87548250b2682affda7d05d947c05554bae, Anthropic FlashProve at9e2bdd8ff5bf9c62f18263d7dac189b0400b260c, and Google zerocopy at6f3a4512ad1ac4cd0f10ba6356774463008e6812. These were search results only, with no imported theorem.

Web fallback queries grouped anthropics/openai with "exact cover", xai-org with "SAT", and google/google-research/google-deepmind with "circular" "constraint". They returned mainly unrelated pages, including MuJoCo constraints. No applicable implementation was recovered. Official ownership was checked using verified [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai) profiles and corporate links from [xAI](https://x.ai/news/grok-os), [Google](https://opensource.google/documentation/reference/github/where), [Research](https://research.google/resources/) and [DeepMind](https://deepmind.google/science/alphafold/). Search coverage is bounded and no absence-of-algorithms claim follows.

## Receiving dependency and gates

ONE next dependency belongs to Bounds with Synthesis integration. Specify a reachable pre-commit checkpoint and prove a decision-compulsory decoder whose demand survives the shared arc computation. Redteam receives F/G and the normalization protocol as a concrete falsification target. Construction receives the confirmed new-phase polynomial tariff, conditional on inherited authentication, and the still-open all-input coverage obligation. Independent review of this report is requested.

DISJ/equality sanity PASS as a polynomial control. Same-execution DTISP PASS under the stated implementation premise. Deterministic-configuration gate PASS as a description upper bound. Relativization, algebrization and Natural Proofs supply no claimed barrier bypass here. Affine, complement, private-leaf, forced-domain, relocation and caching controls retain their scopes. The false suffix reconstruction claim establishes neither P=NP nor P!=NP.

