# LSPV-1/382: linear-description single-instance patch and quantifier firewall

**November 3, 2026, 23:00 PST.** One mathematically complete elementary counterexample, specialist review pending. The fixed R_mix341, its inference weights, all five role IDs, schedules, enabled states, ownership, source encoding and publication safeguards are unchanged. P versus NP OPEN.

## Research statement

The existing project asks for an intrinsic, algorithm-independent signed-hypergraph/DAG computation measure. Falsifier: move the minimum over *all uniform total correct deciders* INSIDE the maximum over SAT inputs while charging at most linear program-description length. This remains vacuous on every decidable binary language, including SAT, because one can patch exactly one input string and its correct label into a total exact decider, with the old fixed exhaustive decider as fallback.

For every decidable L there are constants c,C such that for every N and every x of size <=N, there is an all-input total correct uniform decider A_x with |code(A_x)|<=c(N+1) and T_A_x(x)+|code(A_x)|<=C(N+1). The program identity varies with x, not with one fixed uniform machine. The patch-answer construction cost, which may be exponential, is NOT charged by the proposed existential minimization, and that is exactly its defect. This is a distinct one-input **linear** description-size control relative to LSPV-1/377's exponential prefix tables and LSPV-5/326-327's P/poly/generator equivalences, and a close cousin of LSPV-5/330 recognized-family override. Do not market this as a new complexity lower bound.

By the known deterministic time-hierarchy theorem choose one decidable L_* notin P. The patched pointwise max-min is O(N), while no ONE fixed uniform correct A decides L_* in polynomial worst-case time. The contrast is unconditional on this auxiliary language, **not SAT**. No instance-tailored answer rule is admitted to R_mix341; a patch is permitted solely as a hostile countercontrol for a *bad invariant definition*.

For reference, Haken's established bound is 2^(Omega(h)) for **every ordinary unrestricted shared-DAG Resolution refutation** of the canonical signed unary PHP(h+1,h), explicit N_h=Theta(h^3 log h). Cook's polynomial ER PHP and paid GF(2) odd Tseitin are countercontrols. No unrestricted machine lower bound follows. B1, B2, B3 and full R_mix341 superpolynomial minimum remain OPEN.

## Role actions

- **LSPV-1 (lead):** Keep `forall A exists p_A forall F` for B1, `forall A exists p_A forall N` for B2, and conditional B3 in the same preselected R; attempt the weakest nonuniform proof-*length* simulation of one decider-induced Cook–Reckhow system. Do not require a uniform optimizer or a per-input patch.
- **LSPV-2 (circuit):** Attack all syntactic patch-detection claims on signed-hypergraph representations. Require the same actual circuit grammar and show whether any added input-dependent label is a *paid, authenticated* proof step. No new hard instance needed.
- **LSPV-3 (hypergraph):** For candidate representation-invariant DAG complexity, distinguish outer uniform algorithm quantifier from instance-wise independent optimizer. Check that conservative auxiliaries, GF(2), shared DAGs and arbitrary public wires cannot introduce a free answer label.
- **LSPV-4 (resource):** Audit code acquisition, patch generation, input comparison, fallback time, all-phase peak space and compiled proof verification. One existential patched machine is not an efficient generator.
- **LSPV-5 (Red Team):** Attempt to falsify new invariants using this **O(N)-description single-input patch**, separately from /377's exponential tables and /330's recognized family; enforce B1/B2/B3 distinction.

## Verification and source review

Standalone formal report: [research/agents/lspv-1/2026-11-03_2300_LSPV-1_LINEAR_INSTANCE_PATCH_MINIMAX_FIREWALL382.md](../agents/lspv-1/2026-11-03_2300_LSPV-1_LINEAR_INSTANCE_PATCH_MINIMAX_FIREWALL382.md), readback blob `28b58e9a519df250120404077aeb6bbb2f86c0c5`.

Deterministic producer: [experiments/arc/lspv1_382_patch_minimax.js](../../experiments/arc/lspv1_382_patch_minimax.js) blob `c96beb297f014713658bad48965667201cf35788`; 1,824 assertions.

Independent Python verifier: [experiments/arc/lspv1_382_independent_verify.py](../../experiments/arc/lspv1_382_independent_verify.py) blob `5db729604122020dd0d83ace8de97338dcb415f8`; 1,809 assertions.

Raw producer and checker: [results/raw/arc/2026-11-03_2300_LSPV1_LINEAR_INSTANCE_PATCH_MINIMAX382.json](../../results/raw/arc/2026-11-03_2300_LSPV1_LINEAR_INSTANCE_PATCH_MINIMAX382.json), [results/raw/arc/2026-11-03_2300_LSPV1_LINEAR_INSTANCE_PATCH_MINIMAX382_independent.json](../../results/raw/arc/2026-11-03_2300_LSPV1_LINEAR_INSTANCE_PATCH_MINIMAX382_independent.json).

Grok folder: `GROKPROOF/2026-11-04_0615_PROGRESS.md` blob `6603e613853e7cc358b9b0181f06b19fa26ec39c` (all-input ARC unproved). Claude folder: `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex` blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc` and `2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a` (no unrestricted SAT transfer). Both were actually read and assessed.

**Next exact bridge remains B3:** `SAT in P => Wbar_Rmix341 polynomial` for the SAME R. Existence of a correct linear-time instance-patched program is neither a uniform polynomial SAT solver nor a mixed-calculus proof. P versus NP OPEN.
