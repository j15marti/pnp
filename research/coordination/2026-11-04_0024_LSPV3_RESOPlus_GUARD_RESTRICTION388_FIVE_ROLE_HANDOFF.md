# LSPV-3/388 | Five-role handoff | November 4, 2026, 00:24 PST

**PROVED/EXACT within published Res(oplus); CONDITIONAL on Braun 2026 numerical hard-family premise; COMPUTATIONAL finite checks; OPEN for full fixed R_mix341, B1/B2/B3, and P versus NP.** No agent identity, schedule, enabled state, proof-system grammar or prior result changed.

## Incremental proved theorem and model

Let P_oplus be the fixed published Res(oplus) calculus: DAG derivations of disjunctions of affine GF(2) equations, with complementary-affine resolution on ANY affine pivot and one-premise semantic weakening, no extension axioms. Count distinct source and inference DAG nodes once. For every UNSAT linear-clause formula F and fresh t, G_t(F) = { (t=0) OR C : C in F } and H_t(F)= G_t(F) union {(t=1)} satisfy

$$
S_\oplus(F\vdash\bot)=S_\oplus(G_t(F)\vdash(t=0)),
\qquad
S_\oplus(F)\le S_\oplus(H_t(F))\le S_\oplus(F)+2.
$$

**Key proof:** Guard-lift each original DAG node. Reverse *every arbitrary* guarded unit proof by restricting t=1. An affine pivot using t becomes an affine data pivot; if it becomes a constant, one source-authenticated semantic weakening replaces the step. Semantic weakening remains sound under restriction. Shared DAG nodes remain shared. G_t(F) itself is SAT at t=0, and H_t(F) UNSAT exactly when F is. This extends previous guarded-Resolution / paid AND2 work to the exact Res(oplus) grammar and explicitly permits mixed t-pivots. Not a novel unconditional Res(oplus) lower bound; literature originality not established.

**Published hard anchor:** Braun, arXiv:2609.23015 (2026-09-19, preprint not externally reviewed). For ell>=32, n=2^ell, bit-PHP CNF has (n+1)ell variables, n*binom(n+1,2) width-2ell clauses. All unrestricted DAG-like Res(oplus) refutations have > exp(n/(32768 ell^2)) nodes under published theorem. Literal occurrence length Theta(n^3 ell), full signed-binary-variable-ID bits N=Theta(n^3 ell^2). This encoding distinction was already recognized in LSPV-1/370. Our guarded-unit and guarded-UNSAT corollaries inherit *only this restricted proof-system* bound, not unrestricted SAT time nor fixed mixed calculus hardness.

## Falsifiers and tested controls

F1: guard-dependent pivot breaks restriction. Rejected in exact grammar; constant pivot uses one semantic weakening. F2: cofactor breaks entailment. Rejected. F3: paid gates, LOCAL-CONVERT and compact macros are handled by the theorem. **Not established: these change the grammar.** F4: guarded-unit hardness means G_t(F) is decision-hard. **FALSIFIED: t=0 satisfies it.** Same-source SAT and UNSAT controls, corrupted inference and malformed atom rejection were tested.

Original exhaustive local-rule JS passed **29,439** assertions; independently written bitset verifier passed **29,429**. Both counted 9,583 affine resolution cases, 4,191 cofactor semantic entailment cases, 591 guard-lifted entailments, and 4,107 guard-lifted data resolutions. Original producer also rejected 9 corrupt/malformed cases. Finite checks do NOT certify all-size proof minima or recheck Braun's Lean code. No new hard examples or optimization search were performed.

## Artifacts, exact readback blobs

- Formal: research/agents/lspv-3/2026-11-04_0024_LSPV-3_RESOPlus_GUARD_RESTRICTION388.tex ; blob 84a6ea82e1109e6530c5d9d4351b2cb81576e106
- Producer: experiments/arc/lspv3_388_guard_resxor_audit.js ; blob b877a9f01cf6fb59e864f06ebe4ec4e8bebc29e7
- Independent: experiments/arc/lspv3_388_independent_bitset.js ; blob fcca8b2999f506305c7bc41af4d0586158a62a8e
- Raw: results/raw/arc/2026-11-04_0024_LSPV3_RESOPlus_GUARD_TRANSPORT388_raw.json ; blob 040158ba4e14ff55d3ddfadaf32a0141d7bf4d94
- Independent raw: results/raw/arc/2026-11-04_0024_LSPV3_RESOPlus_GUARD_TRANSPORT388_independent.json ; blob 750d87c6ef224d1408d8a3a64d178fa2d20fad63

## Duplication, peer review and folder audit

The November 2 12:04 refocus (commit 4e29ed7646f484707767acb6e63ec5f38afd98a8), issue #3, AGENTS.md, CODEX.md, the pnp-research skill, and root main.tex blob e874de13 were read. Relevant peers: LSPV-1/370 (fdc2bb0c) already records Braun N-bit measure and Itsykson-Sokolov common-disjunct closure; LSPV-2/381 (f67c91fa) covers t-dependent paid AND2; LSPV-3/385/386/387 cover guarded ER, 3-wire local implication and affine guard nonclosure; LSPV-4/379 (16939bba) P-complete conditional gate evaluation; LSPV-5/331 (6b602a0c) explicitly refutes arbitrary cost-equivalence under representation padding.

Grok directory located **GROKPROOF/**; inspected GROKPROOF/2026-11-04_0720_PROGRESS.md (blob 06304e87), universal all-input charged FLMV transformation remains OPEN. Claude directory located **research/agents/claude/**; inspected 2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727) and 2026-09-30_CLAUDE-0266_review.tex (blob 694c1c81), restricted alternation trading and independent spectral metric critique, neither B3. Peers should check current Grok and Claude folder changes themselves, without using their assessments as authority. Public github.com/openai proof-checking search yielded no relevant original R_mix341 grammar implementation.

## Specialized next requests

LSPV-1: check quantifier discipline and B3 nonimplication. LSPV-2: audit actual LOCAL-CONVERT and GF(2) record types, not hypothetical semantic rules. LSPV-3: seek one legal mixed-rule counterexample to guard cofactor transport in full R_mix341. LSPV-4: charge proof evidence bytes, cofactor computation and all-phase peak memory. LSPV-5: independently referee constant-pivot degeneration, paid source costs, and representation padding. No scheduler or agent mutations.

**Next barrier:** a source-identical, polynomial-cost lift/restrict translator for every fixed R_mix341 operator. The present result does not supply it, nor B1, B2, B3, superpolynomial Wbar_R or P versus NP.
