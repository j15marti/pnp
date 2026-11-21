# Synthesis: full-multiplier normalization with source-dependent shifts
2026-11-21 10:28 PST, America/Los_Angeles.

## Claim, status and scope
**T5-VARIABLE-MULTIPLIER-BUDGET1 — PROVED/EXACT interface; hardness consequence CONDITIONAL.** On Construction's split graph image, even when graph parameters vary at a fixed encoded length N, the multiplier exponent is recoverable from the header:
E(x)=(3m(x)-n(x))/14.
Uniform bounded-fanin circuits convert between raw count and full-multiplier quotient with O(N log(N+2)) gates, including header extraction. Fixed-parameter slices need only O(N) gates. Conditional Shannon and average conditional min-entropy are preserved by the exact, source-dependent bijection. No target-specific indistinguishability premise is proved.

This is a new interface extension of the prior /10 result, not another test of its constant divisor. It makes explicit the cost when E is not fixed for the entire distribution. The O(N log N) bound is an upper bound; no matching lower bound or necessity of the logarithm is asserted.

Review: symbolic reconstruction and finite arithmetic tests by this assistant, external independent review pending. Redteam's latest audit explicitly used the same continuous assistant session; it must not be promoted to external independent review. Independent adversarial review of this new interface is requested through issue #324.

ONE next dependency: **T5-FULL-MULTIPLIER-PAIR1**, owner Bounds, Redteam review, Synthesis tracking. Supply an actual core-quotient fake with independently proved cap-facing indistinguishability. Passing every known multiplier test is not sufficient.

## Exact quantifiers and model
Let Gamma_N be the union, over all simple graph parameters v,e whose Construction image has length N, of the valid images B_G=D(H_G). Every x has
n=55+18v+11e, m=65+20v+13e, E=10+3v+2e,
and F_N(x)=10*2^E Q(x), with Q(x)=Z_C(H_G)/10 an integer, including zero.

For EVERY distribution X supported on Gamma_N and EVERY jointly distributed integer V with
0<=V<=floor(5^{n(X)}/(10*2^{E(X)})),
put Ztilde=10*2^{E(X)}V. Use ell=3N zero-padded output bits. The circuit basis is fan-in-two AND/OR and unary NOT, constants, arbitrary depth, sharing and fanout; noninput gates are charged. Exact-output circuits may behave arbitrarily off Gamma_N. No efficient sampler for X,V or Q is assumed.

There is a universal delta_N=O(N log(N+2)) such that, for B>=delta_N,
Adv_{B-delta_N}((X,Q),(X,V)) <= Adv_B((X,F_N(X)),(X,Ztilde)),
and conversely with raw and quotient pairs exchanged. Exact-output complexities on the SAME Gamma_N differ by at most delta_N. A circuit correct on all valid N-bit strict-C inputs restricts to this domain.

Separately fix one correct total deterministic counter A and fixed K>0,a>=1, independently of X, on the baseline sole-read/write-tape model, and suppose T_A(N)<=KN^a. All input/output, head/control and stored address information is charged. Circuit conversion is not an equal-time tape wrapper.

C is the symmetric relation containing all permutations of 012,123,234,340,401 over Z5. Clause names are distinct and start with full domains. Ordered R is different; neither R nor historical S/Q replaces C. The input remains
1^n 0 gamma(m+1), followed by m triples of one-based w-bit IDs,
w=ceil(log2(n+1)), N=n+2+2floor(log2(m+1))+3mw.
The present result is exclusively about counting outputs; positivity is preserved but its hardness is not established.

Four falsifiers:
1. A genuine graph image violates E=(3m-n)/14 or the exact multiplier.
2. A promised conversion collides, overflows, or loses conditional entropy.
3. Parsing a variable header or selecting a shift is silently treated as free fixed wiring.
4. Residue support is promoted into indistinguishability, or a count demand into a decision demand.

## Proof and reproducible circuit recipe
Subtract n from 3m:
3m-n=140+42v+28e=14E.
Thus no graph recovery or equality-component enumeration is needed to obtain E on this PROMISED image. The formula is not valid for every bounded-occurrence strict-C formula or every general equality split D(F). The promise is indispensable.

Here is a uniform header-extraction circuit construction at fixed N. Compute prefix-ANDs of input bits and sum them using binary adders to find the initial unary run n; the prefix gates and O(log N)-bit additions use O(N log N) gates. Use stages of conditional shifts by powers of two to move the suffix after n+1 to a fixed boundary. Compute its initial zero run l similarly. A second shift brings the gamma payload to the boundary. On valid inputs m<=N, so its l+1 value bits fit L=ceil(log2(N+1)) bits. Take the first L bits (zero pad beyond the source) and shift right by L-(l+1) to recover m+1. Subtract one. Malformed strings can return a default value; no image recognizer is asserted. Compute 3m-n and divide by the constant 14 on O(log N)-bit words. A fixed-remainder scan implements constant division with linear gates in word width.

For a w-bit word, a conditional shift by 2^j selects, at each position, either its old bit or the appropriately displaced bit (zero outside the word). A selector is two ANDs and one OR, with a shared NOT for its control. At most ceil(log2(w+1)) stages handle any 0<=E<=w, using O(w log(w+1)) gates. Induction on stages proves the displacement is the sum of the selected powers. Fixed E instead uses wires/zeros.

Divide a raw word by ten using the prior fixed-remainder scan, then right-shift by E. In the other direction left-shift V by E and multiply by ten using two constant shifts and a ripple adder. Because 10*2^E V<=5^n<2^{3N}, no promised value overflows. On the support, division and multiplication are exact mutual inverses. Their combined gate cost, including header parsing, is delta_N. All recipes are uniform in N; finding a hard count circuit remains a different problem.

For fixed x, multiplying V by the positive integer 10*2^{E(x)} merely relabels its conditional probability vector. Consequently H(V|X)=H(Ztilde|X), and
-log E_x max_v Pr[V=v|x] = -log E_x max_z Pr[Ztilde=z|x].
Unconditional entropy need not be preserved by a source-dependent relabeling. Conditioning on the same full X is essential. Flooring arbitrary off-lattice fake values is not injective and is outside the claim.

Composing a distinguisher with either converter proves both advantage inequalities with additive gate loss. Composing exact-output circuits proves the complexity comparisons. No theorem about witness representations is used.

If average conditional min-entropy of V is at least k and (X,Q),(X,V) are (B,epsilon)-indistinguishable with epsilon<1-2^{-k}, an exact Q circuit plus an O(ell)-gate equality comparator distinguishes with advantage at least 1-2^{-k}. Therefore
C_Q(Gamma_N)>B-O(N),
C_F(Gamma_N)>B-delta_N-O(N).
This implication is CONDITIONAL on an independently proved pair. The sufficient asymptotic demand B=omega(N^a log N) still exceeds both conversion loss and A's count-circuit ceiling, but no such B is supplied here. The graph-core quotient is a weighted color count, not unweighted #3COL.

## Reconciliation and dependency graph
All sources were recovered at main 55805b5b8f8d6a453ddebb029a74b71de5252d07; originating revisions below retain their model and review qualifications.

| Role/revision | Established or falsified statement | Remaining consequence |
|---|---|---|
| Construction 8ae69ba65b79af7d3da945293eacb7bbf1ebe2d1 | PROVED/EXACT peer: equality interface 2[U=V], max occurrence5, Z(D(F))=2^E Z(F); graph images preserve SAT iff3COL. General N'=O(N log N), graph N_B=Theta(N_H). External review pending. | No compulsory decision work; equality contraction legal. |
| Accounting 9f6787be1c19431c5848f0cc44f8e3ccd4b4a75c | FALSIFIED/RETIRED external random orientations as compulsory decoded information; full deterministic trace remains independent. Exact decoder/reuse inequality is conditional on actual services. | Actual core service above brKN^a plus selector overhead remains OPEN. |
| Discovery 3168128105d8f040f41f8a49da8d6f0deffb9112 | PROVED/EXACT restricted: M records, global group order g, expansion O(gM), closed defect O(gM^2); dihedral under fixed a gives N^{a+1},N^{2a+1}. | General scalar coverage OPEN; these node bounds are not CM. |
| Redteam 55805b5b8f8d6a453ddebb029a74b71de5252d07 | Reconstruction supports full-context memoization; weaker caches/composition/scopes fail. 181352 finite comparisons. Explicitly same-session, not external review. | Scope-context optimization and external review pending. |
| Bounds 12726183d307127ed4e07103f2eec9324dae7cc9 | FALSIFIED/RETIRED Y+10R: raw low-bit OR distinguishes; 37-bit fake at N6059 defeated by36 gates. | Full-multiplier-supported pair still OPEN. |
| Prior Synthesis d18f513e02a053db9d30ee7172ee516834c152d3 | Exact /10 normalization with O(N) loss; support+entropy alone fails. | Extended here to source-dependent full multiplier with explicit parsing/shift budget. |

Strongest new construction advance is the full-domain occurrence-five reduction with both decision labels, under its proved gadget premises; strongest new restricted simulation is depth-independent small-global-group expansion. Neither is an unrestricted lower bound. The earlier Omega(N/log N) parity count-map demand remains below the cap ceilings. No independent external review is newly claimed.

Dependency graph (arrows require the premises above):
- equality reduction -> exact full multiplier -> this paid normalization -> CONDITIONAL count demand;
- OPEN quotient indistinguishability -> that same count demand -> baseline same-solver simulation comparison;
- witness lower bound -> small-group typed expansion -> OPEN all-scalar coverage;
- decision-sensitive graph reduction -> OPEN compulsory decision progress.
These branches are not added or multiplied.

## Complete same-execution ledger and controls
Under the same A,N,K,a retain S=O(N^a), physical CM=O(N^{2a}), minimum-description CM=O(N^{a+1}), count gates O(N^a log N). Input length N_B is not source N_H or graph-list length. No exponent is excluded.

Parsing/authentication: header extraction is charged above; recognizing actual graph-image membership is NOT supplied and is unnecessary for a promised distribution comparator. Any operational solver using the shortcut must authenticate its source or use a sound fallback, with UNKNOWN distinct from UNSAT.
Discovery/failed work/adaptation: fixed conversion recipe supplies no count oracle or free sampler; actual failed candidates and switches remain in A's work.
Representation/accesses: O(N log N) gates have wire IDs and serialized descriptions O(N log^2 N) bits. Circuit wiring does not grant random-access tape operations.
Storage/sharing/recomputation: shared gates counted once; actual caches, source, maps, arithmetic buffers, retained output and address bits count simultaneously; discarded records must be recomputed or reread.
A direct scan implementation of the arithmetic/header wrapper uses conservatively O(N^3) sole-tape time and O(N) span (repeated scans suffice); its own physical CM is O(N^4). This is not A's CM and is not a measured Python runtime. Composing with A preserves polynomiality, not the same numeric exponent below3. Description CM remains the separate replay bound.
Output: ell padded bits plus terminator, exact carries and zero tests charged. A one-bit distinguisher is not a SAT solver. No overlapping demands combined.

Renaming preserves the numeric count/header lengths but does not grant invariant source-bit geometry. Relocation does not force revisits of original cuts. Affine/Tseitin, private-leaf trees, forced-domain, matching, caching, complement and global algebra retain cheap paths; full multiplier removal is itself such a path. Complemented relations require their own support check. Full-state entropy of the actual deterministic answer remains zero. Decision-witness constraints remain untouched; Q>0 iffF>0 does not transfer a full-value lower bound to positivity.

DISJ: NOT APPLICABLE, no communication direct sum. Relativization: OPEN for unrestricted separation, no nonrelativizing step. Simultaneous DTISP: PASS for distinct execution ledgers, OPEN for cap violation. Deterministic configurations: PASS as bookkeeping, not lower-demand evidence. Natural Proofs/algebrization: no barrier bypass.

## New evidence, searches and recovery
Code experiments/t5_synthesis_variable_multiplier1_20261121.py; raw results/raw/t5_synthesis_variable_multiplier1_20261121.json. Run Python3 with assertions and redirect stdout to the raw path. COMPUTATIONAL:63488 staged left/right shift checks,93 graph-parameter header cases and372 arithmetic roundtrips. Headers are synthetic, not asserted complete valid T5 inputs. No new full count, circuit minimization or tape benchmark. These tests address variable shifts/header recovery, not the completed fixed-/10 experiment. Raw contains every parameter row and the code SHA256.

Recovered original Bounds code/raw (blobs edb6c74a3abc9039b4ef75d22b617f00df0f7c69 and b12b4c15d685c4dff97307f5d078959a7b56cd7d) and Accounting raw5485b96a17bc8278548554beba8efafde2f7857f. Their same-length SAT/UNSAT example has n211,m243,E37,N6059 and counts9411819533762560/0; normalized values6848/0. These are reused source results, not independently recounted.

Fresh literature queries: “Vadhan Zheng pseudoentropy conditional polynomial alphabet 2013”; “site:github.com/google/xls barrel shifter dynamic bit slice”. Read [Vadhan–Zheng, March8,2013, ECCC revision3](https://salil.seas.harvard.edu/sites/g/files/omnuum4266/files/salil/files/eccc2013.pdf), Definitions2.6,2.8–2.9 and Theorem1.3's explicit polynomial-alphabet limitation. No sampling equivalence imported for the exponential count alphabet. Our bounded-gate converter is proved directly, with no external circuit theorem.

Fresh connector query “barrel shifter variable shift circuit” under anthropics,openai,xai-org,google-research,google-deepmind: no matches except google-research/google-research/numbert/model/vocab.txt at87e25a5ba04d2c4cf0108f0cec96d648fe2b945a, an irrelevant vocabulary snippet. Web fallbacks for each organization with “barrel shifter” or “variable shift circuit” returned third-party hardware projects, not official target results. Google XLS documentation appeared as a lead, not a pinned source inspection or imported theorem. No exhaustive absence claim. Ownership is grounded in the verified corporate-domain and official cross-link evidence recovered earlier in this continuous session: [Anthropic](https://github.com/anthropics), [OpenAI](https://github.com/openai), [xAI](https://x.ai/open-source), [Google Research](https://research.google/pubs/implicit-rate-constrained-optimization-of-non-decomposable-objectives/), [DeepMind](https://deepmind.google/blog/open-sourcing-mujoco/). Product names or off-owner fallback hits are not ownership verification.

Current full baseline/assignment/AGENTS/CODEX/research instructions were fetched again; hashes match the complete prior continuous-session reading. Baseline blob a886f3387a8676b9cc86afbf3bebf22630109d49 is not recertified. Latest own report and all six handoffs, peer reports/relevant original evidence and issue324 recovered. No checkout exists; preflight/LaTeX not run. No TMR manuscript or schedule/identity/enabled-state change.

Review request to Redteam: independently verify header extraction at gamma boundaries, source-specific exponent identity, support/no-overflow, conditional entropy and budget directions. The next mathematical dependency remains Bounds' T5-FULL-MULTIPLIER-PAIR1. **P versus NP remains OPEN.**
