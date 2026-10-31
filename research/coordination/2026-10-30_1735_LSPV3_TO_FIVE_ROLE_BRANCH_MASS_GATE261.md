# LSPV-3 ARC-BRANCH-MASS-GATE261: source-authenticated split-tree coverage

**2026-10-30 17:35 America/Los_Angeles.** Integrated adaptive residual-SAT / arbitrary-A ARC / actual FLMV program. Historical tasks, enabled or paused states, hourly offsets, and role ownership unchanged. P versus NP OPEN.

## Proven restricted invariant, not an arbitrary-algorithm lower bound

For a proper signed exact-(2+,2-) source with n variables, m=4n/3 original clauses, partial original-variable assignment rho of depth t, and s_j(rho) number of satisfied source occurrences, the exact eliminated-clause count is D(rho)=2t-Omega(rho), Omega=sum_j max(0,s_j-1). This refines previously verified LSPV-3 signed overlap; do not claim novelty for the elementary equality.

For a **complete source-preserving binary direct-cofactor search** whose leaves P are authenticated refuted cubes, leaves S have all ORIGINAL clauses satisfied, and leaves E output exact residual ordinary SAT formulas of at most r original clauses, let t*=ceil((m-r)/2). Every E leaf has depth at least t*. Binary cylinder mass satisfies

mu(P)+mu(S)+mu(E)=1, and mu(E)<=|E|*2^(-t*).

On UNSAT F, mu(S)=0. Thus polynomially many power-short emitted residuals must be accompanied by certificates covering nearly all assignment mass **within this explicit architecture**. This is a specialization of Kraft equality to DPLL cubes plus old signed-overlap accounting. Each UP-assigned literal must have its inconsistent alternative charged as a P sibling, or the partition equality is invalid. The theorem says nothing about arbitrary algorithms, noncofactor children, source-retaining joint access, dynamic structure switching, or FLMV lower bounds.

## Falsifiers and independently verified controls

1. **Free propagation falsely reduces search mass.** Minimal F=(x) under UP would appear to retain only a half-cube unless the x=0 refuted sibling is recorded. Rejected.
2. **Small number of emitted children implies target physical length.** Rejected. W1 UNSAT and SWAP6 SAT are n=15,m=20, physically N=368 bits, target floor(sqrt(N))=19 bits, but exact cutoff8 direct-cofactor child strings are 86--117 bits. No ARC stage.
3. **Hard-looking source structure forces arbitrary algorithm hardness.** Rejected. The connected 21-variable strict22 orbit formula has a directly constructible satisfying assignment, despite locally nonshrinking pivots.
4. **Finite policy gain implies universal contraction.** Rejected by policy sensitivity and fully charged work.

At cutoff eight ORIGINAL residual clauses, first-variable full partition has W1 UNSAT 14 emitted children, selected 101381 events, SWAP6 SAT 18 emitted children, selected 110741 events. Max-incidence full partition has W1 3 emitted / 66362 events, SWAP6 11 emitted / 71159 events, but still physically too large. Min-incidence gives 99 and 87 emitted children respectively, exceeding N^(3/5) finite cap about 34. Every experiment has source-indexed S/U extremes, their inversions, SS/SU/US/UU pair modes, coherent 0^n/1^n and flip trails as adversarial controls, not an oracle.

Same source complete decision-only runs (selected instrumented events, UP-DPLL / first / max / min):
- W1 UNSAT: 108528 / 93127 / 59725 / 400069;
- SWAP6 SAT: 54656 / 46360 / 16982 / 62822;
- renamed W1 UNSAT: 131812 / 105425 / 49485 / 310423;
- renamed SWAP6 SAT: 20666 / 15621 / 15531 / 6170.

These counts include source scans, policy selection, status updates, source-proof checking, guest DPLL calls and physically emitted child writes for the declared selected-operation model. They are NOT full interpreter instructions or native FLMV simultaneous time/space. Independent full Boolean partition verifier checks n<=15; orbit21 relies on symbolic leaves and explicit witness. No production CDCL result. Every correct SAT witness is checked against the original source; UNSAT relies on complete binary partition and authenticated original-source conflicts.

## Publication and corpus reconciliation

Verified GitHub:
- formal report: `research/agents/lspv-3/2026-10-30_1735_LSPV-3_ARC_BRANCH_MASS_GATE261.tex` (blob `b7ddb4b443d9b35fbc702c853ec36aa5c31ce1d2`);
- producer: `experiments/arc/2026-10-30_1735_LSPV-3_ARC_BRANCH_MASS_GATE261.py` (blob `fc9962e7e80eb1727a54a1798e2bbe01afca778a`);
- independent verifier, decision and policy executables and their separate verifiers co-published in `experiments/arc/` with matching date and run tag;
- compact summaries and checksum manifest: `results/summaries/arc/` with same run tag.

Complete verified ZIP and 2.8MB raw JSON in persistent Library `/P-vs-NP/2026-10-30_1735_LSPV-3_ARC_BRANCH_MASS_GATE261_COMPLETE.zip`, library ID `libfile_3a4151ae43848191a22db3d1daa061fc`, SHA256 `1a803b957d3ff5a3d6f9c27d7557a25d5407532d1b900e1be002b07a04f77f96`. PDF and individual code also uploaded. Root `main.tex` reconciled ONLY in `% BEGIN/END LSPV-3 OWNED` region: commit `7545636cfcea53be68e837f9cf142f39e8b37fb1`, readback blob `9b8cdf8fbd65982ac8b9ad8df97437f3af7e3de1`; no outsider bytes changed.

Prior-work audit: user 09:48 governance and CONTRACT1, AFFINE-SMALLBIAS-DESCENT-GATE2 (only affine MCSP), CONSTRUCTION-STRENGTHEN17, ARC-LINEAR22-SATURATION1, SIL/M22, LSPV-3 signed-overlap258 and recursive replay260, LSPV-5 reusable-boundary228. FLMV JACM 2005 forbidden strict c=241/200,d=11642479/23232400. Classical DPLL branching/cylinder counting is known. No claim of an unconditional ARC compiler or P!=NP.

## Role-specific next target

LSPV-1: referee mass proof and specify which universal candidate architecture would actually be forced to use source-preserving cofactors; do not transfer this restriction without a theorem.

LSPV-2: implement one genuine **noncofactor** certified child or source-accessible implicit child on the same original SAT source; record exact physical bit size, local random-access addressing and both-label correctness.

LSPV-3: adaptive mixed representation parameter controller with cached probes/Horn/Krom/XOR and complete fallback; measure policy acquisition and derivation cost, not offline oracle selection.

LSPV-4: carry these emitted-bit counts and retained Python/full-tree workspace through exact native FLMV simulation including guest heads, subroutine tape storage and ancestor states; no uncharged source access.

LSPV-5: independently verify root/role boundaries, mass accounting, easy orbit controls, and whether any theorem truly covers all algorithms.

**One open arrow:** a uniform hereditary source-authenticated A->Phi(A) stage producing at most N^(3/5) exact ordinary SAT children of <=N^(1/2) physical bits with local <=N^(11/10) time, <=N^(1/2) simultaneous workspace, and universal arbitrary-guest compatibility in one FLMV model. None constructed.
