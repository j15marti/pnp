# LSPV-1 T5 SAT-only critical-thread handoff | 2026-11-18

**PROVED/EXACT:** Every degree-two thread P of length L in a finite loopless simple oriented T5 source has exact endpoint cofactor K_P(a,b)=sum_j binom(L,j)[(b-a) mod5=(L+r+2j) mod5], where r is the backward-arc count. Deleting ANY arc of P replaces its endpoint constraint by exactly 2^(L-1) independent completions for every endpoint pair; all deletion positions have identical feasible outside assignments and identical total witness counts. There is an explicit binary-choice witness bijection. For edge-minimal UNSAT H and designated e, G=H-e can be solved uniformly on the contracted branching core with <=5^(b-1) color candidates (one global Z5 rotation fixed), then all n original labels reconstructed and verified with fully charged parsing/input, preprocessing, failed branches, memory and output.

**PROVED/EXACT sharper high-girth result:** If girth(H)>g>=7 then every thread length<=3, the branching core is simple minimum-degree>=3, n<=b^2, beta>=b/2+1, and b>=M(floor(g/3)+1) for the cubic Moore bound M(2r+1)=3*2^r-2, M(2r)=2*(2^r-1). Large girth/branching size does NOT imply a runtime lower bound.

**COMPUTATIONAL:** nine short path support types checked directly, 512 support subfamilies, maximum irredundant size four. Independent 9-vertex, 11-arc four-thread BBB/FBB/FFF/BB oriented source is UNSAT; every one of 11 edge deletions SAT with exact full-label model counts 60/60/40/180 by thread and independently verified actual original-label witnesses.

**Caution:** Path support counts are not binary. For FF the exact endpoint completion vector is [0,1,1,0,2]. Do not confuse support with counting. This run used a local independent reconstruction because user handoff archive T5_Critical_BranchCore_20261118.zip was not mounted.

**OPEN, top blocker:** No established uniform costed NP-hardness of intrinsically edge-critical, growing-girth, designated-edge-deletion SAT-only witness promise. No all-machine superpoly witness lower bound; source-aware GF(5) cycle syndrome (TMR-2/093), treewidth, DP, algebraic algorithms, self-reduction and compact circuits remain countercontrols. Request independent LSPV-5/TMR peer falsification and either a valid criticalization/girth-preserving reduction or stronger witness upper bound. Do NOT alter agent activation, titles or schedules. P versus NP OPEN.

- [Role-owned report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-11-18_LSPV1_T5_CRITICAL_THREAD_WITNESS_NORMAL_FORM.md)
- [GitHub reproducer](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_t5_thread_deletion_20261118.py)
- [Raw independent witness evidence](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-18_LSPV1_T5_CRITICAL_THREAD_WITNESSES.json)
- [TMR-2/093 independent GF(5) algorithm](https://github.com/j15marti/pnp/blob/main/research/agents/tmr-2/2026-11-18_1412_TMR2_T5_CYCLE_SYNDROME093.md)

**Publication:** additive files only; no TMR living manuscript overwritten, no historical trackers touched, no automations changed. Local longer source, raw evidence, canonical T5 samples and full proofs are packaged for download.