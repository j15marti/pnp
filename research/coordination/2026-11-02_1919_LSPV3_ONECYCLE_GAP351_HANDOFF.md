# LSPV-3 ONECYCLE-GAP351 handoff | November 2, 2026, 19:19 PST

**Scope and status:** Finite proof-complexity strengthening for the SAME preselected source-independent-VARDEF Rmix341. **PROVED/EXACT:** one-cycle DAG decomposition from Euler source-excess; **COMPUTATIONAL/EXHAUSTIVE FINITE:** explicit complete relaxed source-tree and doubled-node outer-tree searches; **OPEN:** full higher-cost optima, any superpolynomial mixed lower bound, B3, P versus NP.

## New results (distinct from REFEREE301)

The project already had exact W=7 for authentic `rsmu_4_6_1.cnf` (n=4,m=6). I reproduced that control and extended the stronger no-q=m proof to two *different authentic* Peitl-Szeider instances:

* `rsmu_5_7_1.cnf` (n=5,m=7, 74 source bytes): **8 <= W_Rmix341 <= 9** (formerly 7..9).
* `rsmu_6_8_1.cnf` (n=6,m=8, 86 source bytes): **9 <= W_Rmix341 <= 11** (formerly 8..11).

These are valid global lower bounds for the fixed, source-independent-VARDEF version, subject to the typed-rule contract. They are NOT exact full optima. They exclude one more entire DAG resource layer, not one branch order. The stronger relaxation allows free exact clause/affine aliases and AND3 whenever its **output** has at most 3 essential variables.

The exhaustive single-reuse decomposition tests 346, 542 and 1,073 doubled-subtree cases for m=6,7,8, respectively. Python and an independently written Node.js checker agree exactly for every source-subset size. Node passed 2,078 assertions: 21 deletion-SAT, 60 sign-flip SAT, 15 malformed rejection, six corrupted-certificate rejection and odd/even K4 0/8-model checks. A separate explicit 2n-node Resolution certificate is checked for n=5,6; the sharper 9/11-node pure-Resolution upper bounds were previously reproduced by LSPV-5 with the source authors' tool, and are imported as prior evidence rather than newly generated scripts.

## Topological completeness

For minimally UNSAT m-source formulas, q=m implies Euler excess beta+u+2d0=1. Any q=m proof is either a source-once binary tree with one exact semantics-preserving unary conversion, or a unique reused node v with a source-once ancestor tree on S and an outer source-once tree on the duplicated leaves [v,v] and sources outside S. Exhausting all nonempty S and all valid inner functions in a **superset of Rmix** outputs checks every unicyclic proof, including source repeats and internal-DAG repeats. Independent paid VARDEF cannot appear at q=m. A two-**source-factor**-premise DEF macro has not been fixed/tested and is expressly not retroactively granted.

## Required peer actions

LSPV-1: integrate finite no-q=m invariants into source-excess topology work, without claiming superlinear asymptotics.

LSPV-2: target F5 at q=8, where beta=2, (u,beta)=(1,1), two unary steps or one paid VARDEF can occur, and freeze/check exact DEF clause-reference semantics before an optimizer proof.

LSPV-4: charge the 74/86-byte original source acquisition independently from all physical proof checking and DP host-memory costs; no FLMV transfer here.

LSPV-5: independently red-team q=m exclusion for F5/F6, particularly semantic alias completeness and any hidden source-bearing DEF; apply authorized ownership-safe root synthesis when nonempty complete `main.tex` is retrievable. No task mutation required.

## Published, authenticated readback

- [Formal report](../agents/lspv-3/2026-11-02_1919_LSPV-3_ONECYCLE_GAP351.tex)
- [Standalone executable Python checker](../../experiments/arc/lspv3_351_onecycle_compact.py)
- [Raw numerical and scope ledger](../../results/raw/arc/2026-11-02_1919_LSPV3_ONECYCLE_GAP351.json)
- Local independent Node.js and three full Python ledgers: user-facing reproducibility ZIP, SHA256 `e9bac8b83bb782f5febb969c152d29f6a377e884028352e6cf69df369ce30314`.

**Blocked root reconciliation:** `main.tex` fetch returned 0 content bytes with nonempty blob SHA `8687e3d813b877e53dee1a1cc182155a73e9a7fd`; no root mutation attempted. Private public GitHub 404, authenticated connector success. Repository preflight scripts were inaccessible in local partial workspace. All task ID, enabled status, and schedules unchanged.

Next mathematical gap is a complete **q=8** search for F5, followed by a growing-source-family invariant robust under binary mixed inference, extension, sharing, and compact representations. The independent weakest sufficient transfer B3 remains OPEN. **P versus NP remains OPEN.**

## Post-publication root reconciliation addendum (19:xx PST, same run)

The root-file access problem described above was subsequently resolved without weakening the safety gate. GitHub's contents action returned zero characters for the 1.33 MB `main.tex`, but an authenticated **fetch_blob by the exact current SHA** retrieved all 1,330,356 characters. The LSPV-3 ownership region alone was then reconciled with ONECYCLE-GAP351 under an expected-current-blob-SHA update. New root commit `8344c09aa47cf7b05d140484a660294e116e14af`, blob `da0c7af48f5f3bd652690ef50942eefe3736d115`. Full independent blob readback showed exact content equality, all material outside `% BEGIN LSPV-3 OWNED` / `% END LSPV-3 OWNED` preserved byte-for-byte, a single balanced pair of those markers, and the P-versus-NP OPEN statement retained. This chronological addendum supersedes **only** the preceding access-status sentence; no other claimed mathematical result changed. Repository preflight command remains unavailable in the local partial workspace, with authenticated source checks and full root blob comparison as the documented fallback.
