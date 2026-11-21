# PNP Independent Counterexamples: T5-CIRCUIT-CM-RECON1
Pacific timestamp: 2026-11-21 08:14 PST (America/Los_Angeles).
Role: charged-redteam. Independent baseline audit; no TMR manuscript ownership acquired.

## 1. Target, source pin, and result
Target ONE named lemma: T5-CIRCUIT-CM-RECON1, the unrestricted encoded-count circuit to self-contained cumulative-description bridge in Sections 17–18 of research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md, commit 10d2ccb2062c3efd4b4f03873eaa88822edf732f, file blob a886f3387a8676b9cc86afbf3bebf22630109d49.

Status: **PROVED/EXACT for the reconstructed distinct-configuration and same-run implication; CONDITIONAL on the separately stated time-to-circuit simulation interface.** That interface is a known published theorem, whose author-hosted abstract was retrieved; the full publisher text returned HTTP 403, so this run is not a fresh full-paper audit. No counterexample to the scoped bridge was found. Two stronger, explicitly unclaimed variants are FALSIFIED/RETIRED below. No unrestricted counting or decision lower bound is established.

Independent-review status: this is an independent reconstruction of the published baseline, not independent certification of the whole handoff. The new proof and tests have not received a second external review.

At recovery, issue #324 contained only the assignment-publication comment. The new charged-bounds directory and charged-redteam/handoff.md returned 404. Hence there was no newly posted mathematical peer report to reconstruct. Rather than invent one, this run selects the strongest relevant cross-model claim in the pinned baseline. Its original source, *Circuit size, entropy, time, space, and cumulative memory* (Library libfile_f758560558688191921972d8783f20a5), was read through its Sections 1–5, including the exact proof of equations (5)–(8). This explicitly scopes the deviation from “new peer report”: baseline audit now; new peer audit when one is published.

The complete current 141,084-byte handoff, including all appended programs, was read in successive text windows. AGENTS.md, CODEX.md, the current assignment directive, .codex/skills/pnp-research/SKILL.md, and the compatible older manuscript directive were read. Repository search and a branch-list page were inspected; this was not an exhaustive audit of every historic branch. Prior charged work is secondary and supplies no premise here. The first role-specific repository handoff is created, not a replacement of a peer file.

## 2. Exact claim and falsifiers
For every fixed deterministic, correct, halting strict-C exact counter A in the sole-tape model below, let X_N be the nonempty set of valid N-bit encodings, T=T_A(N)=max_x t_A(x), and
M_min=max_x sum_{t=1}^{t_A(x)} K_U(C_t(x)|A).
The universal decoder U and program A are fixed, independent of N. Let C_N be minimum fan-in-two AND/OR/NOT noninput gate count for the padded exact count map on all X_N, with arbitrary invalid-input behavior.

Given the simulation premise C_N <= c_A (N+T) log_2(N+T+2), there is a constant d_A with
C_N <= d_A [1 + N log_2(N+2) + M_min].
When T>=N and grows, C_N=O_A(M_min). If C_N>=L(N) and either T>=N or L=omega(N log N), then T=Omega_A(L/log(L+2)) and M_min=Omega_A(L). If faithful physical encoding costs O_A(s_t+1), also M_phys=Omega_A(L), up to the harmless actual-time additive term.

A proposed cap is fixed before inputs: T<=K N^a, a>=1, K and a independent of N. The statement does not provide L. It does not assert a pointwise circuit lower bound on each input or combine two different solvers.

Four attempted falsifiers:
1. A halting legal run revisits a FULL configuration, invalidating injectivity.
2. Code reuse with a fixed decoder gives two distinct configurations the same description.
3. Circuit simulation needs sum_t max_x s_t while the proof silently uses max_x sum_t s_t.
4. Clock, input oracle, omitted addresses, or post-halt padding supplies hidden state and invalidates the distinctness argument.

## 3. T5 and encoding audit
C is symmetric on Z_5, permitting the unordered triples 012,123,234,340,401 and their permutations (30 ordered tuples). Strict clauses use three distinct variable names, no literal signs, constants or relation tags. This is not historical S/Q. Ordered R means its first value beats exactly one of the other two under i beats i+1,i+3 mod 5; it has 40 tuples. Conversion C(x,y,z)=R(x,y,z) AND R(y,x,z) is a distinct, explicitly size-changing operation, not used in this audit.

Input encoding is 1^n 0 gamma(m+1) followed by m triples of w=ceil(log_2(n+1))-bit identifiers:
N=n+1+2 floor(log_2(m+1))+1+3mw.
Unary n ensures n<=N and O(N) padded output bits. Identifiers and locations are charged. Count output is exact, not a Boolean satisfiability bit. An exact count circuit may yield a decision circuit by testing positivity; a lower bound for count circuits does not reverse this implication.

A uses one finite-alphabet read/write tape and one head, fixed finite control, input/work/output on that tape, canonical output at the left origin, no separate input oracle or free time-dependent behavior. C_t includes tape contents and position/support, control and head, stored addresses and every continuation-relevant datum. The actual post-transition times 1,...,t_A(x), including the final state once, are charged.

## 4. Independent proof reconstruction
Fix an input x and actual halting time t. If C_i=C_j for i<j<=t and neither is a terminal state, deterministic continuation from both states is identical. Iterating the intervening segment gives an endless cycle, contradicting halting. A terminal state cannot occur earlier in an actual run. Hence the t charged post-transition configurations are pairwise distinct.

Choose one shortest U-program for each C_i conditional on fixed A. Equal programs have equal output, so those descriptions are injective. No efficient procedure for finding them is assumed. The t shortest binary strings have total length
g(t)=r t-2^(r+1)+r+2, r=floor(log_2(t+1)).
Counting all strings of lengths below r and then the required strings of length r proves this expression. Thus g(t)=t log_2 t-O(t); with prefix-free programs Kraft/Jensen gives sum_i lengths>=t log_2 t.

Choose x* attaining T on the finite nonempty valid domain X_N. The SINGLE execution on x* therefore has description CM at least g(T). Consequently M_min>=g(T). No peak-space lower bound is multiplied by a time bound, and no maximum is pushed inside a sum.

For T sufficiently large, T log(T+2)=O(1+g(T)). Splitting N+T according to which term is larger gives
(N+T) log(N+T+2)=O(N log(N+2)+T log(T+2)).
Combine this with the simulation premise and M_min>=g(T). For T>=N, the input term is absorbed by T log T. A faithful physical state encoding, with a fixed decoder and self-delimiting framing, has description length O_A(s_t+1); summing on any one run and maximizing yields M_min=O_A(M_phys+T). With normal positive per-step physical charge, T is absorbed.

If C_N>=L and L dominates N log N, the input term is absorbed. Inverting u log(u+2) gives the time consequence. This does not invert a time lower bound into a circuit lower bound. The final lower bounds use the same fixed solver; x* witnesses sufficient description CM even if another input attains M_min.

This validates the scoped mathematical implication, not the existence of a hard count map. Small input regimes are covered by an additive 1; empty X_N is excluded or assigned circuit cost zero by convention.

## 5. Small boundary counterexamples and smallest safe statement
**Post-halt padding.** A deterministic transition from start to halt has one actual transition. A circuit simulation may stutter on that terminal state for 16 layers. There is one distinct poststate, not 16. For arbitrary padding H the repeated fixed state has total description cost H*K(c|A)=O_A(H), not H log H. This falsifies replacement of actual T by an arbitrary simulation cap in the injective-description argument. It is NOT a counterexample to Section 18, which uses actual worst-case runtime. Strict T5 even permits n=m=0, encoding 01, exact count 1; a total correct counter can recognize this constant case and otherwise enumerate. Padding its halted simulation does not add real computational work.

**Maximum/sum swap.** Three storage profiles (9,1,1), (1,9,1), (1,1,9) have worst-run sum 11 and summed layer maxima 27. These are accounting arrays, not claimed T5 runs or an in-model counterexample. They refute the algebraic equality sometimes used in a tableau shortcut. The selected bridge never uses that equality.

**Omitted state.** A head scanning a run of identical symbols can have repeated control/scanned-symbol projections while its positions differ. Erasing the head location is not a faithful configuration code. Likewise making t free to the decoder is a different measure. These are hypothesis-boundary attacks, not valid counterexamples to full-state injectivity.

Smallest safe statement: use actual halting configurations of one fixed solver with a fixed input-charged decoder, retain N log N unless T>=N or the lower-demand term dominates it, and leave the all-input circuit simulation as an explicit external premise. No stronger claim is needed for the cap comparison.

## 6. Controls tied to this claim
- Relocation: complete states include the relocated head and support; actual configurations remain distinct. Old-cut-only CM is not this M_min. The cubic old-cut ceiling does not falsify the all-time bridge.
- Affine/Tseitin and private-leaf trees: their cheap scalar algorithms are allowed. The bridge cannot import their hard witness representations as C_N. They attack the missing lower-demand premise, not injectivity.
- Complement, sharing and renaming: legitimate algorithms/circuits remain permitted; no DLDD/DNNF compilation is used. A global renaming does not remove physical identity needed to decode a state.
- Forced domains: easy exact counts remain easy. Raw graph width is absent from both sides of the audited inequality.
- Decision-witness packing: no factorial decision diagonal is assumed. The theorem is about count-map circuits; decision consequences require their own lower bound.
- Full-state entropy: H(output|complete state)=0 is compatible with distinct states and large accumulated description lengths. Shannon remaining uncertainty is not used as work.

## 7. Same-execution resource ledger
Parsing, invalid-input handling, source authentication, algorithm discovery, failed attempts, representation changes, adaptive switches, queries, real accesses, address manipulation, cache lookup, retained copies, recomputation and output are inside t_A(x) whenever performed. The proof grants no free instance-specific advice, code, oracle, or residual service. A fixed program contributes only a program-dependent constant; repeated execution still costs transitions. There is no requirement to construct the simulation circuit during A's run. Circuit existence is nonuniform; finding it is not claimed free in a uniform algorithm.

Under T<=K N^a with the stated input convention:
S=O(N^a), physical CM=O(N^(2a)), M_min=O(N^(a+1)), C_N=O(N^a log N).
The descriptive ceiling follows by describing input plus step index and replaying A, which need not be fast. It is not a physical-space simulation. The existing matching Omega(N^3) CM fits below, for example, the a=3 ceilings; no excluded polynomial family follows. One fixed exponent excluded would not exclude every exponent.

Peak physical space counts simultaneous buffers and retained state; CM sums that full charge over actual time. Multiple accounts are not added as independent demands. The original-space tableau and sharp-size simulation are alternative circuits; no simultaneous best width/size assertion is made.

## 8. New evidence, not repetition
New runner: experiments/t5_redteam_cm_recon1_20261121.py. Raw data: results/raw/t5_redteam_cm_recon1_20261121.json.
It exhausts EVERY deterministic successor function on q nonterminal states plus one halt, q=1,...,5, from every start. There are 41,592 runs: 14,831 halt and 26,761 enter loops. Independent bounded replay confirms distinct poststates on each halting run and no late halting after a repeat. It also records the padding and max/sum controls.

These abstract finite systems test the exact deterministic-transition premise, beyond the proposer's T5 matching family. They are not physical T5 runtime simulations or complexity lower bounds. The proof in Section 4 is universal; finite tests are COMPUTATIONAL only. The earlier 1..100 code-length arithmetic suite was not rerun. No wall-clock or output-entropy argument is used.

No local git checkout exists; repository preflight, solver suite and LaTeX compilation were not run. Connected reads recovered current state. No manuscript was claimed or edited. Full-paper Pippenger–Fischer verification was unavailable (HTTP 403); author-repository abstract and bibliographic theorem statement were read. Publication readback checks are performed separately.

## 9. Sources and gates
Pinned baseline: https://github.com/j15marti/pnp/blob/10d2ccb2062c3efd4b4f03873eaa88822edf732f/research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md
Original peer evidence: https://chatgpt.com/library?file_id=libfile_f758560558688191921972d8783f20a5&account_id=personal
Pippenger and Fischer, Relations Among Complexity Measures, JACM 26(2), 361–381 (1979), DOI 10.1145/322123.322138: https://scholarship.claremont.edu/hmc_fac_pub/597/ . Author-hosted abstract states the O(t log t) combinational-network simulation. A fan-in bounded basis and output normalization are explicit premises of the use here; this run does not independently verify all details from the blocked full paper.

DISJ sanity: PASS as a scope audit; no communication lower bound transferred to general counting.
Relativization: NOT APPLICABLE to a claimed separation; this is a deterministic simulation/accounting implication and identifies no nonrelativizing hardness step.
Simultaneous DTISP: PASS for accounting, OPEN for any stronger lower demand. No new forbidden region reached.
Deterministic configurations: PROVED/EXACT under full-state, no-clock, actual-run hypotheses.
Natural Proofs/algebrization: NOT APPLICABLE to this lemma; no constructive/largeness circuit lower bound is proposed.

## 10. One next dependency
Receiving roles: Bounds (encoded-count circuit route) and Synthesis.
Supply a target-specific, independently justified lower bound L(N) for the unrestricted encoded strict-C count map that exceeds the chosen N^a log N ceiling, or a fully specified pseudoentropy premise giving it. Keep the simulation premise and same-run proof above as the transfer edge; do not relabel this audit as progress on L(N). A new peer report with a concrete alternative bridge should become the next Redteam target.
P versus NP remains OPEN.
