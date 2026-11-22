# Actual suffix events and checkpoint overlap

21 November 2026, 20:46 PST (America/Los_Angeles). Charged Accounting.
**DYNAMIC-CHECKPOINT-OVERLAP1: PROVED/EXACT restricted accounting lemma.**
Independent adversarial review requested; not yet obtained. No external/kernel verification.
P versus NP remains OPEN.

## Result and source revision

This run instantiates the shared entropy ledger on the actual crossings of the Boolean permutation family, then gives the exact multiplicity correction for combining the newly published all-checkpoint potential bounds. The strongest recovered candidate is CHARGED-UNSAT-PREPAYMENT1 at revision 7ad8794c9a6df14d47c85f9ba4efdc76518c46e5 [1], not the easy table-composition family. The source theorem has internal review only. Its all-checkpoint guarantee does not grant independent budgets at each checkpoint.

The new deliverable is an explicit suffix decoder with conditioned past histories, together with the composition identity
\[
 \sum_i a_i\Psi(\tau_i)=\sum_{t=1}^T m_t d_t,\quad
 m_t=\sum_{i:\tau_i<t}a_i,
\]
where d_t is the actual potential drop at transition t. Thus, if m_t<=1 whenever d_t>0, the left side is at most the same execution's CM_min. Unweighted suffix bounds require their actual overlap factor. This closes the checkpoint-composition accounting step, not the existence of new compulsory post-transport work.

## Model, encoding, quantifiers and falsifiers

Fix a total correct deterministic Boolean compatibility decider A first: one writable finite-alphabet tape, one head moving at most one cell per primitive transition, Q control states, output bit and terminator at the fixed left origin, and no original-source oracle or external clock. It is correct on both labels, including every off-diagonal hybrid.

Use exactly [1, §§3–4] and [2]: r>=3, permutations pi,sigma, source
\[
 \bigwedge_i(\neg X_i\lor Y_{\pi(i)})\land(\bigvee_iX_i)
 \land\bigwedge_i(\neg X_i\lor\neg Y_{\sigma(i)}).
\]
It is UNSAT iff pi=sigma. The proper-3-CNF and adjacent-witness compiler gives n=8r-1,m=10r and w=ceil(log2(8r)). The complete encoding is unary n, gamma(m+1), ordered signed triples, both n-bit local witnesses, and the w-bit release identifier:
\[
 N=3n+2+2\lfloor\log_2(m+1)\rfloor+3m(w+1)+w.
\]
The common physical middle has Delta=6(r-2)(w+1)-1 selected interior boundaries. Logical Horn/dual-Horn parts are not physical tape halves. This is Boolean decision, not symmetric strict C, ordered R, or historical S/Q counting.

For the entropy assertion choose any distribution on the r! diagonal inputs after fixing A,r. Choose a finite deterministic number J of checkpoint policies tau_i(I) in [0,T_A(I)]. They may depend on the actual completed execution. No online premise is needed. For the cumulative assertion use the same good-input set and d parameter as [1]. Quantifier order is fixed A,r,d, then the common good set, then every member and every finite checkpoint list. No one-input-for-all-solvers claim is made.

Falsifiers:
1. A full crossing string fails to identify pi on the valid both-label domain.
2. A suffix decoder silently omits its consumed prefix or uses original source bits.
3. Overlapping suffixes are summed with unit event reuse.
4. A potential reset after erasure is charged without a new correctness-derived injection.

The first two are addressed below. The third is excluded by explicit membership counts. The fourth remains forbidden; a new reset obligation is OPEN.

## Actual conditional decoder

Index obligations j=(i,c), checkpoint i and fixed selected physical cut c.
Let U_j=pi and let B_j=(A,r,c,P_j), where P_j is precisely the ordered crossing-state prefix through transition tau_i, without its END marker. B_j is an analytical observer view, not a free machine copy of input or workspace. Its entire history is conditioned upon, so it cannot be counted again as new entropy. A,r,c are fixed for this obligation, not input-dependent advice.

Let
\[
 E_j(I)=\{t:\tau_i(I)<t\le T_A(I),\ t\text{ crosses cut }c\}.
\]
Pi_j is the sequence of states immediately after these crossings followed by END. Set b=ell=ceil(log2(Q+1)); encode Q states and END in fixed ell-bit blocks. Then
\[
 |\Pi_j|=\ell|E_j|+\ell,\qquad h_j=\ell.
\]
The code is prefix-free, including the empty suffix, because END is not a state. There are no uncharged length fields: the prefix length gives the number already consumed; END supplies suffix termination. The initial side and alternating crossings determine direction. No timestamp is needed for an untimed transcript.

An explicit decoder concatenates P_j with Pi_j without END, enumerates all r! diagonal inputs, simulates the fixed total A to halt on each, extracts the complete crossing string at c, and returns the unique matching permutation. Existence follows from the real source execution. Uniqueness follows from the full-transcript injection: equal strings on distinct diagonals splice to an incorrectly rejected valid SAT hybrid. This is the original-input splicing argument, not the unproved claim that arbitrary processed-state mixtures are reachable.

The decoder therefore satisfies H(U_j|B_j,Pi_j)=0. It does not request virtual residual answers, perform a semantic hash merge, or access the unknown input as an oracle. Enumeration is an untimed coding argument. If implemented, it pays generation of r! encodings, all simulated runs and comparisons, and stored transcript lengths. A direct sequential reference algorithm uses at least the sum of those simulation lengths and their simulation overhead; no polynomial decoder time is asserted. Those simulations are not silently added as compulsory transitions of A. A uses no transcript logger.

A physical logger or an executable replay service would require its own charged storage, writes and scheduling, not the b=ell observer code bound. Similarly, sending an adaptively chosen cut requires its address: a W=ceil(log2(N+1)) field plus any selector header must be added to h_j unless conditioned on, in which case its information is removed from the entropy demand. Here all cuts are predetermined. We never charge random-access addresses at constant cost: the real head movements are the event support. Addresses stored or manipulated by A occupy its charged tape. Adding retained caches or the full configuration to B_j can only reduce the displayed entropy; no positive full-state output entropy is assumed.

## Reuse and the actual time inequality

At a real transition t there is at most one selected cut c(t). Its membership count is
\[
 R_t(I)=\#\{i:\tau_i(I)<t\}
\]
if t crosses a selected cut, and zero otherwise. Define rho as a deterministic upper bound on R_t across this finite input distribution and its real transitions; rho<=J. When no event occurs the numerator below is nonpositive and no division by zero is required.

Conditional coding and the decoder yield
\[
 \sum_{i,c}H(\pi\mid A,r,c,P_{i,c})
 \le \ell\,\mathbb E\sum_t R_t + J\Delta\ell
 \le \ell\rho\,\mathbb E T + J\Delta\ell.
\]
Hence the requested concrete bound is
\[
 \boxed{\mathbb E T\ge
 \frac{\sum_{i,c}H(\pi\mid A,r,c,P_{i,c})-J\Delta\ell}
 {\ell\rho}}\quad(\rho>0).
\]
For a single common checkpoint the crossing sets for distinct cuts are disjoint, so rho=1. This specializes the earlier strict-C relocation ledger to the new Boolean family; that specialization alone is not claimed as a new principle. The extension here explicitly handles multiple adaptive/retrospective checkpoints and integrates their overlap with [1].

Repeating the identical checkpoint J times repeats both demand and framing J times and makes rho=J whenever there is a remaining crossing. The bound is exactly unchanged. If the prefix already identifies pi, its residual entropy is zero. Paid relocation and cached decision can accomplish that; correctness does not require restarting the original comparison.

## Cumulative composition on exactly those runs

Use [1]'s good set, ell as above,
\[
 H=\lfloor\log_2(r!)\rfloor-d-1-W-\ell,\quad
 \Phi_\ell(z)=\sum_{k\ge1}(z-k\ell)_+,
\quad \Psi(t)=\sum_c\Phi_\ell(H-\ell p_c(t)).
\]
Its two splicing injections and direct composite-code count give, at actual crossing k of c,
\[
 d_t:=\Psi(t-1)-\Psi(t)=(H-\ell k)_+
 \le K_{\mathcal U}(C_t\mid A).
\]
At noncrossings d_t=0. Also Psi(T)=0 on this same good set. We use these proved source premises, not an independently certified new good-set theorem.

For nonnegative weights a_i, which may even be selected after observing this run, finite rearrangement gives
\[
 \sum_i a_i\Psi(\tau_i)
 =\sum_i a_i\sum_{t>\tau_i}d_t
 =\sum_t m_t d_t,\quad m_t=\sum_{i:\tau_i<t}a_i.
\]
If m_t<=R on positive-drop events, then
\[
 \sum_i a_i\Psi(\tau_i)\le R\,CM_{\min}
 \le R\lambda_A CM_{\mathrm{phys}}.
\]
The final inequality is the source's faithful configuration-description conversion, not equality of physical and descriptive costs. Noncrossing storage remains charged in both complete cumulative sums.

This is a pointwise alternative to the entropy inequality, so data-dependent weights require no unjustified exchange of weights and expectations. For unweighted lists the exact count R_t governs every positive drop. Do not infer R=1 from the source's statement that one transition crosses one cut: the same cut event belongs to many suffixes.

Disjoint intervals instead give
\[
 \sum_i[\Psi(t_i)-\Psi(t_{i+1})]=\Psi(t_0)-\Psi(t_q).
\]
The terms telescope. They do not each receive a restored initial potential. A claim of fresh potential must prove a new actual obligation, source decoder, and allocation of event capacity.

A minimal arithmetic diagnostic uses ell=2,H=6 and one cut with three crossings, whose drops are 4,2,0. Checkpoints 0 and 1 have potentials 6 and 2. Their sum 8 exceeds total drop 6, while multiplicities 1,2,2 give exactly 8. This is an algebraic counterexample to unit-overlap composition, not a claim that this abstract ledger alone is a legal SAT-machine execution or a counterexample to [1]. The symbolic identity supplies the all-execution result.

## Same-execution cap and complete ledger

Under T<=K N^a, fixed a>=1,K, a contradiction from the time formula requires the residual entropy minus all framing to exceed ell rho K N^a. Multiplying the checkpoint count without changing rho cannot meet a new exponent.

All initialization, parsing/authentication, unsuccessful recognizers, retained input, copies, relocation, cache writes and reads, index bits, conversions, arithmetic, recomputation and final output remain in T and the input-inclusive span s_t. Nonselected events contribute zero to this lower-bound certificate, not zero implementation cost. Physical CM is sum s_t; descriptive CM is sum K(C_t|A), with neither source nor time given free. These are not multiplied by unrelated maxima.

The cap gives S=O(N^a), physical CM=O(N^(2a)), descriptive CM=O(N^(a+1)). The baseline remains quadratic time/cubic CM in its one-tape scope, matched by the authenticated O(N²),O(N),O(N³) family solver. The table-composition control at 400ea6f3890fa613d51bf5f4f7b7e80d7f615e75 has a different layout and only its own polynomial upper bound. No cut injection transfers to it. Count-map circuits O(N^a log N) concern counters and are not decision evidence here.

DISJ/equality sanity PASS with both-label hybrids and cheap matching solver retained. Simultaneous DTISP PASS for the explicit event sums. Deterministic-configuration gate PASS as a scoped injection argument, not state-count hardness. Relativization is a scope check only: extra heads or a nonlocal oracle invalidate this physical proof. No Natural Proofs/algebrization bypass or unrestricted separation is claimed. Affine/Tseitin, private-leaf, forced-domain, complement, renaming, sharing and decision-witness controls remain legal; no representation or proof-system lower bound is imported.

## Recovery, evidence and fresh searches

Recovered AGENTS, CODEX, repository research skill, end-to-end directive and supporting references, current dynamic directive, transport and new prepayment report, applicable T5 §15 definitions, all six handoffs, previous Accounting OUTPUT-FIBER-LOSS1, current Construction and Synthesis reports, original prepayment code/raw, and issue324 including comment7074282428. Prepayment code hash recorded by its evidence is 8795e2438b60b217590c7b2e255221cfd422f8de7cd5a175abde757e4d4fd4d6. Its 318281 assertions are prior evidence, not rerun or independently certified here. This run is a symbolic accounting proof; no new computational result or kernel verification is claimed. A checkout was not available, so repository preflight and LaTeX compilation were not run.

Fresh repository query “checkpoint overlap suffix” recovered Synthesis's pending composition task and an unrelated older syndrome DP, not a completed version of this ledger. Branch search “charged” returned no matching draft branches, not proof that all drafts were searched.

Fresh primary query “Patrascu Demaine information transfer encoding addresses cells logarithmic lower bounds pdf” retrieved the authors' SIAM2006 journal PDF [3]. Re-read §§5.3–5.4 and the covert-transfer discussion: actual update/query intervals supply mandatory outputs; the encoding includes addresses and contents, and another setting must certify negative read/write information. This supports retaining decoder and metadata premises, not transferring dynamic-data-structure lower bounds to offline SAT. The proof above is direct and imports no such lower bound.

Official GitHub connector query '"information transfer" "amortized"' covered anthropics,openai,xai-org,google,google-research,google-deepmind. All returned no hits; Google initially returned429 and succeeded on retry. Web fallback queries combined those exact organization scopes with “amortized information transfer”; hits included unrelated issue discussions, OpenAI math overview/theorem excerpts, and DeepMind tsuite. None supplies an inspected theorem applicable to the present checkpoint ledger; no code or theorem was imported, no candidate commit inspected. Do not treat a search excerpt as a verified mathematical result.

Ownership was checked through domain verification at github.com/anthropics and github.com/openai; corporate link x.ai/news/grok-os to xai-org/grok; opensource.google/documentation/reference/github/where naming google; research.google/resources linking its repository; and deepmind.google/research/publications/122591/ naming google-deepmind/trecvit. These are ownership checks only.

## One next dependency

**DYNAMIC-POST-EXHAUSTION-VIEW1, owner Construction with Accounting; review Bounds and Redteam.** Supply one correctness-derived intermediate view after the existing cut potential has been exhausted, together with its nonzero residual entropy and real event allocation. Synthesis should integrate the overlap identity before composing checkpoint claims. Redteam's concrete target is a proposed reset: run the paid authenticated equality solver, cache its answer, and test whether the alleged new source decoder receives any information not already in its conditioned prefix. Distinguish a false reset claim from the currently unproved existence of any stronger obligation.

Existing roles, schedules, enabled states and manuscript ownership are unchanged.

## References

[1] CHARGED-UNSAT-PREPAYMENT1, internal review only, pinned source:
https://github.com/j15marti/pnp/blob/7ad8794c9a6df14d47c85f9ba4efdc76518c46e5/research/main/Charged_UNSAT_Preprocessing_Tradeoff_2026-11-21.md

[2] CHARGED-UNSAT-TRANSPORT1, same revision:
https://github.com/j15marti/pnp/blob/7ad8794c9a6df14d47c85f9ba4efdc76518c46e5/research/main/Charged_UNSAT_Transport_2026-11-21.md

[3] M. Pătraşcu and E. Demaine, Logarithmic Lower Bounds in the Cell-Probe Model, SIAM J. Comput.35(4),932–963,2006, authors' journal PDF:
https://erikdemaine.org/papers/DynamicConnectivity_SICOMP/paper.pdf

[4] Synthesis DYNAMIC-REACHABLE-SPLICE1:
https://github.com/j15marti/pnp/blob/790875f74755a178e8ad810b67ebd603c10f6e89/research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-21_202200_Reachable_Checkpoint_Splice.md

[5] Accounting T5-OUTPUT-FIBER-LOSS1:
https://github.com/j15marti/pnp/blob/7ad8794c9a6df14d47c85f9ba4efdc76518c46e5/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-21_143800_Output_Fiber_Loss.md
