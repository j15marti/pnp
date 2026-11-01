# LSPV-4 ALLINPUT-YES-GRAMMAR-WORK-FLOOR308
**2026-11-01, 10:36 PST. PROVED/EXACT restricted source-encoding YES-side deterministic bit-query theorem; KNOWN recurrence; independently checked computation; P versus NP OPEN. External referee pending.**

## Exact obstruction and decision-only priority
The user explicitly removed any obligation to reconstruct stored pin values, assignment states, lost source bits, or a unique transcript. The previous CUBEKEY306 bound on an injective recoverable key is not a decision-work lower bound; DECISION-WORK-ONLY307 established only a tight linear pin-query promise. The present theorem applies to **EVERY valid SAT original of the ONE complete canonical language**, but only under a declared explicit source grammar. It does not lower-bound the work of all SAT algorithms beyond bit reads.

## Theorem: Every clause-polarity bit must be queried on a YES input
Encode valid duplicate-free proper Döcker Monotone 3-SAT-(2,2) originals with Elias-gamma integers n,m and exactly m records, each a one-bit whole-clause polarity followed by three fixed-width unsigned variable IDs of width w=ceil(log2(n+1)); reject all malformed strings. Exact grammar requires three distinct same-sign literals in every original clause, no duplicate clauses, and **exactly** two positive and two negative occurrences per variable. Thus m=4n/3 and
[
N=|gamma(n)|+|gamma(m)|+m(1+3lceillog_2(n+1)ceil)=Theta(nlog n).
]
**Exact claim:** For EVERY correctly encoded SAT instance F, EVERY uniform deterministic decider that accepts F and rejects malformed strings must query all m distinct original clause-polarity input bits on F. Therefore **T(F)>=m=Omega(N/log N)** native read-only-source observations, regardless of adaptive policy, semantic compression, source rereads or key representation.

**Proof:** Flip only the polarity bit of clause j while keeping IDs/header/length fixed. Every original variable in that clause changes one of its two appearances from its old sign to the opposite sign, so its required (2,2) quota fails. The changed string is malformed and must be rejected. If the actual accepting run does not read polarity bit j, the original and mutated strings produce identical bit observations, deterministic transitions, and accepting output, contradiction. The argument holds for every j, with no recovery of any variable assignments. It is the standard decision-tree certificate adversary, here explicitly scoped to the canonical signed-quota grammar.

**Limitations:** Not a lower bound on writable space or superpolynomial SAT runtime. Grammars with different sign layouts or a prevalidated valid-input promise need a fresh proof. On an UNSAT original the same malformed neighbors are also rejected, so no analogous NO-side bound follows from this adversary. In a three-sign-bits-per-clause encoding, all 3m sign positions are separately pivotal on YES sources, but this is a distinct encoding.

## Independently checked canonical and opposing-label controls
The valid original F9 has 9 variables, 12 monotone signed triples and **70 global satisfying assignments**. Coherent pin states P=(x1,x2,x3,x4,x8)=(1,0,1,0,0) and Q=(1,1,0,0,0) on this **same** original have respectively **1 and 0 satisfying completions**, independently exhausted. A measured, specified UP-DPLL baseline processes one node on each: P 75 literal checks/4 forced units, Q 46 literal checks/3 forced units/1 falsified original-clause leaf. Unpinned F9 takes 5 nodes/209 literal checks. Full 16-completion enumeration on the two pin states takes 183 versus 196 literal checks. These literal checks are NOT native FLMV steps.

The independent no-producer-import checker made **8,467 assertions**: all F9 264 original SS/SU/US/UU clause-pair modes, all 6,144 complement clause identities, six other malformed originals, and **1,908 independent one-sign-bit malformed mutations** over connected canonical SAT originals G_t with t=1,2,4,8,16,128. For each G_t it reconstructed and checked a full original SAT witness using a repeated F9 witness with x5=0; the cyclic F9 x5 occurrence splice preserves exact quotas, distinctness and connectedness.

| t | Canonical encoded bits N | Critical YES input polarity probes m | One declared serial indexed-source protocol components |
|---:|---:|---:|---:|
|1|170|12|235|
|2|402|24|510|
|4|934|48|1192|
|8|2138|96|2781|
|16|4830|192|6134|
|128|52266|1536|60163|

For G128's concrete *serial indexed-read* protocol: 1,536 source reads, 11,011 index-cell set writes, 46,080 index-head moves, 1,536 indexed jumps and 22,022 cumulative index-content XOR; endpoint index XOR=0, peak input-index addressed cells=16. This serial implementation is not a proved lower bound on arbitrary index-head overhead, nor a complete native FLMV SAT benchmark. FLMV indexed jumps atomically erase their index tape; do **not** use the invalid local k-cell Hamming bound for such jumps. Prior ARC-AMORTIZED-INDEX282 already establishes the relevant global recharge correction, not newly claimed here.

## Known, explicitly credited A-independent polynomial closure
The October 7 project BOUND-MATCH1 already recovered the standard recurrence: If there exists one uniform **A-INDEPENDENT** all-input, both-label-correct, malformed-rejecting target-valid hereditary decomposition with all nonrecursive native work <=O(N^alpha), <=O(N^gamma) evaluated child calls, each child length <=O(N^lambda), for 0<lambda<1, including paid grammar/discovery/failed policies/bit access/guest/output/proofs and a correct terminal, then
[
T(N)=N^{max{alpha,gamma/(1-lambda)}+o(1)}.
]
Proof: recursion depth O(log log N), at depth i the aggregate cost exponent is gamma/(1-lambda)+lambda^i(alpha-gamma/(1-lambda))+o(1), whose maximum is max(alpha,gamma/(1-lambda)). Thus such an unconditional controller already yields P=NP for the established NP-complete target. Under (alpha,gamma,lambda)=(11/10,3/5,1/2) the conditional exponent is **6/5**. A symbolic exact integer worklist with N=2^(5*2^q), q=2..9, confirms effective exponents 1.18073549 through 1.19989638, approaching 1.2. This is not an actual SAT controller, and is not new mathematical proof of all-input shrinkage.

**Quantifier firewall:** Under a hypothetical P=NP, A-dependent semantic compression can first run a correct arbitrary decider A and then emit either of two fixed YES/NO canonical instances. Its children are constant size, but acquiring their correct labels costs T_A(N); no work contraction follows. A mere one-bit final answer is not free decision work. Ordinary Shannon branching only reduces one variable and can still require 2^n leaves. A fixed-depth or favorable-policy existence claim does not prove an all-input quantitative algorithm.

## FLMV exact strict boundary
Independently read primary FLMV §2.1 and Theorem 5.7, including page images. Recomputed f_0=1, f_(k+1)=c*f_k/(1+f_k) and d_k(c)=min((1/f_k-c)/k,c^(-k)), with exact rational arithmetic. At c=6/5, d_*=23/45; at c=241/200, d_*=11642479/23232400. At both c, k=2 dominates k=1,3 strictly, and every k>=4 satisfies d_k<=c^(-4)<d_2. The theorem's forbidden space is **o(N^d)**, not a closed O(N^d) boundary.

To transport a hypothetical target algorithm (time,space)=(N^(6/5+o(1)),N^(1/2+o(1))) to ordinary SAT at c=241/200 requires a fully charged **same-machine**, arbitrary-bit-addressable SAT-to-Döcker normalizer, with output length exponent b and per-guest-step access exponent rho satisfying (6/5)b+rho<241/200 and b/2<11642479/23232400, plus separate setup/peak-space checks. Even at rho=0, b<11642479/11616200≈1.00226227. The normalizer and universal arbitrary-A->Phi(A) contractor remain unconstructed. NP-completeness alone does not transport the numeric FLMV box.

## Four falsifiers
F1: 'YES can skip an independent clause-polarity bit because global quotas determine it.' **FALSIFIED** for the declared encoding via equal-length malformed one-bit flips.
F2: 'The same one-bit malformed flip establishes an UNSAT-input read floor.' **INVALID inference**, since both source and mutant reject.
F3: 'Recoverable syntactic state cardinality or short final output lower-bounds decision work.' **FALSIFIED as a general inference**, as shown by prior two-state transfer and the paid constant-child compressor.
F4: 'Any decreasing-state recursive controller yields polynomial total work.' **FALSIFIED** by exhaustive ordinary Shannon search; a proven power shrink and fully charged polynomial fanout would suffice, but is OPEN.

## Charged recurrence and open problem
For actual executable state z:
[
W_D(z)le C_{m grammar/source/index/head}+sum_{pi	ext{ attempted}}C_{m discover/select/switch/failed}(z,pi)+C_{m GE/matroid/proof/cache/replay}(z)+sum_{yinmathrm{evaluatedSucc}(z)}(C_{m child/output/bit/guest}(z,y)+W_D(y)).
]
Peak space is the maximum **simultaneous** live original-dependent writable/index/head, retained ancestors, matrices, proof DAG, cache, translators, child materialization and guest DELAY/COPY/RECOMP state. Lazy virtual XOR and full-state offline tracing are not free computation.

The remaining target is either a *computably found*, fully charged polynomial-total-work controller correct for **ALL valid** canonical originals (which gives P=NP), or a genuinely arbitrary-decider power-short ARC contraction plus a separate strict numerical SAT-to-Döcker same-machine transfer (which could support P!=NP). No new universal computational hardness is proved by the YES grammar-probe floor.

## Literature/project preflight and publication
Read first the verified 01:48 integrated handoff and 01:44 affine-terminal proof; then latest LSPV-1 PAID-BRANCH-ENTROPY307, LSPV-2 MULTIPIN-SIGNED-FLUX306 and TRANSFER305, LSPV-3 GATE304, LSPV-4 306/307/INDEX282, LSPV-5 REFEREE269, decision-only five-role scope, issue #3 and governance/AGENTS/CODEX/pnp-research. Primary web queries covered FLMV 5.7 and indexed model, Döcker monotone 2,2, Nisan decision-tree sensitivity, recursive power-short closure. GitHub project queries covered state-key, recurrence, sign-bit grammar and index erasure; github.com/openai/math searches covered SAT self-reduction and encoded worklist programs. Prior BOUND-MATCH1 and ARC-AMORTIZED-INDEX282 were identified and credited; no novelty inferred from search misses.

Primary: Fortnow et al., JACM 52 (2005), https://doi.org/10.1145/1101821.1101822 ; Döcker, arXiv:1912.08032 ; Nisan, SIAM J. Comput. 20(6), 1991, DOI:10.1137/0220062. Prior project BOUND-MATCH1: https://github.com/j15marti/pnp/blob/main/research/agents/lead/2026-10-07_1610_BOUND_MATCH1.tex .

Producer, independent verifier, *full raw JSON*, execution log and checksum manifest are in the separately produced reproducibility ZIP; the repository receives a compact standalone checker and summary. **Root main.tex reconciliation PENDING**: current GitHub connector fetch returned zero content despite a nonempty SHA for the >1 MB root after a documented earlier oversized-write incident, so no unsafe root write was attempted. Exactly five task identities, schedules, enabled states and role boundaries remain unchanged.

**P versus NP remains OPEN.**
END_OF_VERIFIED_REPORT::LSPV4::ALLINPUT_YES_GRAMMAR_WORK_FLOOR308::OPEN
