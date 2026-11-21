# Information that may disappear after exact aggregation

21 November 2026, 14:38 PST, America/Los_Angeles. Charged Accounting. Recovery head 2303eb12b08af4eaaf5e0a94e4097eb1599c835f.

**T5-OUTPUT-FIBER-LOSS1. PROVED/EXACT obstruction to compulsory source reconstruction after aggregation. Independent review pending.** For every fixed deterministic total strict-C counter A there is a fixed total counter A_clean that returns the same answer and reaches a normalized prehalt configuration depending only on that answer. For a finite encoded-input distribution, let U be a source label, Y the answer, B that checkpoint, and Pi the entire subsequent physical trace without an external absolute timestamp. Then
    H(U | B,Pi) = H(U | Y).
In particular the balanced DISJ fixed-weight complement distribution has H(U|Y)=log2 binom(k,floor(k/2)). A post-aggregation decoder for U is impossible for k≥2, even with unlimited decoding computation. The proposed universal obligation that this source identity must still be recovered is **FALSIFIED/RETIRED**. The whole-run crossing obligations retain their original scope.

The corrected accounting rule is
    Σ_j [H(U_j|B_j) − H(U_j|B_j,Pi_j)]
    ≤ br E[T_suffix] + Σ_j E[h_j].
Its left side measures information supplied by real records. A source entropy term alone becomes a demand only after a reconstruction theorem sets the residual term to zero. One next dependency, Accounting with Redteam review, is a checkpoint-local decoder for an observable required by a still-unanswered service, with source, retained state, event support and bounded reuse specified. On the present static DISJ family, a positive post-aggregation source-identity demand is unavailable. P versus NP remains OPEN.

The named result addresses the direct evaluator in Construction [1]. This report does not independently certify that report's entire polynomial bound. Its general normalization proof applies even to exhaustive counting. The polynomial-orbit consequence uses Construction's explicit evaluator and its proved width argument, under independent review.

## Exact model and input

Fix one finite-state deterministic one-head read/write tape machine, fixed alphabet, no original-source oracle or independent clock, and canonical binary output with terminator at the fixed left origin. Input, work, output and stored addresses are charged on this tape. The same physical realization supplies time, peak storage and CM. State equality includes tape values, head and control, including all continuation-relevant markers. Historical visited-span accounting may continue charging erased cells and is treated separately from the current configuration.

C is the symmetric relation containing all permutations of 012,123,234,340,401 on Z5, with distinct variable names in each row and full initial domains. R is the ordered relation with first color beating exactly one other under i beating i+1,i+3. This report uses C. No substitution of R or historical S/Q is made.

Use the full generator image(k,a,b) of Construction [2]. The predicate on k Boolean x requires (A_i OR x_i) AND B_i=0 for every i. It is satisfiable iff A and B are disjoint, in which case its strict-C split count is 10·2^(E+k−|B|), with E=98+282k. The complete ledger is
    n_J=25+66k, m_J=41+116k,
    n=515+1476k, m=629+1808k,
    w=ceil(log2(n+1)),
    N=n+2+2 floor(log2(m+1))+3mw.
The input is the actual unary-n/gamma-(m+1)/fixed-width triple list of N bits.

Let U be a uniform k-bit mask of weight floor(k/2), and X=I(complement U,U), at fixed k. The count Y=10·2^(98+282k+ceil(k/2)) is constant. There are P=binom(k,floor(k/2)) distinct source strings. Cross inputs are still in the correctness domain and include UNSAT cases. Separate exact decision machines can use the same normalization with Y equal to their answer bit. This is not a counting-to-decision lower-bound inference.

## Normalization and the failed decoder

Simulate A with a marked finite work interval. When A has computed the output, save it on a protected track, move it to the left origin, erase all input/work tracks except the output, erase the interval marks, return the head to the origin and enter one fixed prehalt state. The next transition enters a fixed halt state. A fixed finite number of tracks is encoded in a finite alphabet. Marked sweeps and bit-by-bit copies implement the procedure on the single tape.

If the simulated execution has time t and input-inclusive occupied span s=O(N+t), the simulation has constant-factor overhead plus a conservative O(s²) cleanup and O(s) space. Every source read, copy, erased cell, head movement, index, and output bit is included. No efficient algorithm is needed to decide whether two source instances have equal counts. Each count is computed first. Across inputs with the same answer the resulting full current configurations are identical; their arrival times may differ. This does not repeat a configuration within one halting execution. A model exposing an external clock would require a different statement.

Because B contains only the normalized output and fixed machine state, B is an injective computable function of Y. Pi is a deterministic fixed-length continuation from B. Therefore conditioning on (B,Pi) is exactly conditioning on Y. On the distribution above, B and Pi are constant and
    H(U|B)=H(U|B,Pi)=log2 P,
    I(U;Pi|B)=0.
Any deterministic proposed decoder produces the same mask for all P inputs and succeeds with probability at most 1/P. Independent decoder randomness cannot improve that bound. The smallest nontrivial example is k=2, masks U=01 and U=10. Both counts equal 10·2^663. Both normalized states coincide while the source labels differ.

The actual output decoder reads the binary word up to its terminator. Its bit operations and scans are paid if executed as part of an algorithm. Conditional on B its answer uncertainty is zero. There is no source-label decoder, regardless of overhead allowance. Giving a decoder the original source, a prior crossing transcript, or the pre-erasure cache changes B and accounts for past information. Requiring that every earlier cut be revisited cannot recover information that the solver has legally discarded.

This strengthens the previous relocation counterexample [3] at a distinct checkpoint. That report retained paired masks after relocating them and showed that no further original-cut crossings were necessary. Here the paired masks themselves have been consumed and erased. The source becomes unrecoverable from the entire future. No claim is made that the expensive earlier phase was avoidable.

## Conditional entropy and event capacity

For arbitrary finite U_j,B_j and a conditionally prefix-free physical record Pi_j, chain rule gives
    H(U_j|B_j) − H(U_j|B_j,Pi_j)
    = I(U_j;Pi_j|B_j) ≤ H(Pi_j|B_j) ≤ E|Pi_j|.
Suppose Pi_j is supported on actual suffix event set E_j and
    |Pi_j| ≤ b|E_j|+h_j,
with at most r memberships per real transition on each run. Summation gives the displayed inequality. No independence assumption between U_j is used.

An admissible record includes read/written symbols, real addresses, state or event identity where needed, lengths and termination. Under a fixed cap KN^a with a≥1 and fixed K,a, address and time-index fields fit O(log(N+2)) bits, so b=O_A,K,a(log(N+2)) is a safe per-transition record budget for explicitly indexed events. Encoding the number of records with a self-delimiting integer contributes h_j=O(log(T+2)); extra headers or retained-state encodings are also charged. Free original reads or unrecorded interval choices invalidate that bound. A global fixed padding convention is another option, with all padding charged.

For the concrete obstruction take j=1, U_1=U, B_1=B, E_1 the one halt transition, Pi_1 its full record, r=1. It is the same record on every sampled input. The residual term exactly cancels the proposed log2 P demand. For any collection with valid exact decoders, a cap contradiction would require
    Σ_j H(U_j|B_j) − Σ_j E[h_j] > brKN^a.
Without exact reconstruction, replace each entropy by its conditional mutual information above. Replicating one record across many obligations requires the corresponding reuse factor. Arbitrary shared computation and caches remain legal.

The general cap ceilings remain S=O(N^a), physical CM=O(N^(2a)), minimum-description CM=O(N^(a+1)), count-map circuit size O(N^a log N). The normalization of a generic cap machine may raise its time exponent to 2a; it is not a refutation preserving every proposed a. On Construction's orbit evaluator, the reported O(N^20) time and O(N³) storage absorb O(N⁶) cleanup, retaining O(N^20) time, O(N³) peak, O(N^23) physical CM and O(N^21) minimum-description CM. Constants and implementation overhead are independent of k. These bounds are loose and inherit the peer evaluator's scope. They do not exclude any additional exponent.

## Falsifiers and finite evidence

1. A continuation-relevant residue, clock, address, or marker distinguishing normalized inputs would invalidate state equality. The proof explicitly erases each such field and excludes an external clock.
2. Opposite exact outputs reaching the same normalized state would violate correctness. The SAT/UNSAT control retains different outputs.
3. A correct decoder for two distinct labels from identical (B,Pi) would falsify the information argument.
4. A charge omitting the pre-checkpoint computation or charging one shared record repeatedly with r=1 would invalidate a proposed whole-run consequence.

The new executable uses the recovered width evaluator on all fixed-weight complement pairs at k=2,3, then performs explicit one-cell erase-and-move cleanup on a represented tape. Five counts were exact. Two inputs merged at k=2 and three at k=3. Entropies were respectively 1 and log2 3 bits before and after the constant suffix, with zero information supplied by that suffix. Two same-length controls have opposite labels and distinct normalized output states. The script compares complete state strings for equality; hashes are evidence fingerprints only. It records exact cleanup transition counts and reserved-span CM. Counter runtime, source parsing, and staging are not simulated as TM transitions by the Python script; their polynomial ledger is the mathematical construction above. Finite results are COMPUTATIONAL. This experiment is new because it examines information loss after aggregation, beyond the earlier retained-mask checkpoint.

The source and its dependencies are pinned by SHA-256 in the raw evidence. Reproduce with
    python experiments/t5_accounting_output_fiber_20261121.py
The full algorithm can use exact enumeration on UNKNOWN. Failed structural recognition never becomes UNSAT.

The DISJ gate passes with valid hybrids. The simultaneous DTISP gate applies to one normalized solver and the stated polynomial overhead. Deterministic-configuration counting passes because merging is across different executions. Relativization supplies no separation here. Affine/Tseitin, private-leaf trees, forced domains and complement are compatible with normalization whenever a correct scalar evaluator is provided. Renaming is allowed by the peer orbit evaluator. Decision-witness packing is respected because no claim reconstructs all witnesses. Full-state output entropy remains zero. The result does not promote restricted width or witness bounds into unrestricted lower bounds.

## Sources and search record

Startup recovered the current main handoff, assignment, AGENTS.md, CODEX.md, research skill, Accounting handoff and report, Construction report/code/raw and issue324. No full checkout was present, so repository preflight was unavailable. Main source revisions were read through GitHub. Existing manuscript ownership remains with the assigned owners.

[1] Construction, T5-DISJ-ORBIT-WIDTH1, revision2303eb12b08af4eaaf5e0a94e4097eb1599c835f.
https://github.com/j15marti/pnp/blob/2303eb12b08af4eaaf5e0a94e4097eb1599c835f/research/agents/charged-construction/PNP_Charged_construction_2026-11-21_143200_Disjoint_Orbit_Width.md

[2] Construction, balanced DISJ generator and its original proof, revision27e01b7746b30af30f9de413263ea1e8cebd8362.
https://github.com/j15marti/pnp/blob/27e01b7746b30af30f9de413263ea1e8cebd8362/experiments/t5_construction_disjoint_cut_20261121.py

[3] Accounting, T5-DISJ-RESIDUAL-SERVICE1, revision8dc5f151662803d335872ed09423df0b0f00deea.
https://github.com/j15marti/pnp/blob/8dc5f151662803d335872ed09423df0b0f00deea/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-21_133800_Disjointness_After_Relocation.md

[4] Fresh query “Patrascu Demaine logarithmic lower bounds cell probe information transfer encoding memory cells 2004 pdf”. Read the authors' journal-version PDF, SIAM J. Comput.35(4),2006, §5.3. The decoder encodes addresses and contents of cells written in the earlier interval and probed in the later interval, reconstructing required partial-sum query answers with stipulated side information. Its dynamic query specification supplies an obligation absent from our final scalar source recovery. No dynamic-data-structure lower bound is imported.
https://people.csail.mit.edu/mip/papers/loglb/loglb.pdf

[5] Fresh query “Shannon 1948 mathematical theory communication conditional entropy information lost deterministic function pdf”. Read conditional entropy and equivocation sections of the 1948 original. The chain rule above is proved directly; lost source information is retained in the residual entropy term.
https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf

[6] Fresh GitHub query '"conditional entropy" "decoder"' under anthropics,openai,xai-org,google,google-research,google-deepmind. No hits for Anthropic,xAI,Google Research,DeepMind. OpenAI math at4eaee87548250b2682affda7d05d947c05554bae returned Ramsey-description and Thorp-sweep excerpts, unrelated to compulsory static-count source reconstruction. Google uncertainty-baselines atbdacc9af9346c02188d8f622da25b8b39c4c8057 returned language-model metrics in baselines/t5/data/metrics.py; its T5 name is unrelated to this relation. Search excerpts only were inspected. No theorem or code was imported. Web fallback queries paired Anthropic/OpenAI with “information theory entropy”, and xAI/Google/Google Research/DeepMind with “information transfer entropy”; unrelated nonofficial repositories were excluded. Official-owner checks revisited github.com/anthropics, github.com/openai, github.com/google and corporate links at x.ai/news/grok-os, research.google/resources/, deepmind.google/research/publications/122591/. A repository search for OUTPUT-FIBER-LOSS returned no prior result. The searches supply background and rejection records; the proof is the direct argument above.

[Executable](../../../experiments/t5_accounting_output_fiber_20261121.py) and [raw evidence](../../../results/raw/t5_accounting_output_fiber_20261121.json). Independent adversarial review requested from Redteam for normalization, missing-clock assumptions and the residual entropy term.
