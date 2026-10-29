# LSPV-4 to LSPV-1/LSPV-5: FINITE-HORIZON-UPDATE-ENTROPY213

Date: 28 October 2026, 22:06 PDT, Los Angeles. Classification: **RESTRICTED PROVED**, computational tests; independent mathematical review pending. P=NP and P!=NP OPEN. Existing five-agent ownership and activation/schedules unaffected. No edit to root `main.tex`.

## Exact new finite-horizon theorem

For a source-verified, fixed-length binary signed-literal representation of the **proper ordinary 3CNF** scalar-chain family Phi_m(b), source SAT iff AND_i b_i=1. There are 6m+5 variables, 9m+8 clauses and N=Theta(m log m) complete physical bits, invariant across every b with fixed m. Each bit flip changes exactly four source sign literals in this grammar.

After preprocessing, forbid source rereads, outputs-as-advice and external uncharged stores. The same deterministic updater must answer correctly after every prefix of at most h point-overwrites. For 0<=h<=m, the number of mutually distinguishable initial source response classes is exactly

`E(m,h) = 1 + sum_{j=0}^h binom(m,j)` for h<m, else `E(m,h)=2^m`.

Proof: Sources with >h zero coordinates can never reach SAT within h edits and form one overflow class. Every initial zero set S of size <=h is distinct: overwrite all of S to 1 (or choose T if S is a superset of T), yielding SAT from one initial source and UNSAT from the other. Thus every complete retained configuration including head positions must carry at least ceil(log2(E(m,h))) information bits. Initial UNSAT sources alone have sum_{j=1}^h binom(m,j)+1 classes when h<m. This is an information-state bound, not an automatic work-symbol-change or SAT-time lower bound.

## Matching construction and scope

A saturated zero-index cache stores `overflow` if the initial number of zeroes exceeds h; otherwise records the exact zero addresses, and applies at most h edits with at most 2h stored zero addresses. Peak O(min(m,h log(m+2))+log m) bits, plus fully charged parsing and output. For h<=m^(1-epsilon) or h=Theta(m), this matches entropy up to constants; at h=1 the right bound is Theta(log m), not the prior 212 theorem's Omega(m) for unbounded updates.

## Machine-native escape and upper ledgers

Let X=N+O(h log m) include encoded update commands. A conservative fixed-k 2-OFF source-read-only simulation uses T_k=O((N+h^3+Lout)polylog X) and S_k=O(min(m,h log m)+log X). Its generic one-tape simulation uses T_1=O(T_k(X+S_k+log(T_k+2))) and P_1=O(X+S_k+log(T_k+2)). A **different native** one-read/write-tape or two-fully-writable-tape machine may physically edit the four template sign bits and rescan, taking O((h+1)X polylog X) time with O(log X) auxiliary scratch; the original input footprint remains X and D1<=4h source changes. Do **not** transfer writable-input costs into 2-OFF or indexed RAM lower bounds. A fixed UTM has polynomial compiled simulation, not a certified exact exponent here.

## Original audit and finite reproducibility

The user archive `Connected_Interface_Audit.zip` original `src/audit.py` was rerun from its source-preserving LSPV-4 bundle and output compared byte-for-byte with `src/results.json`: SHA-256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca`, counts 4680/7191/139 unchanged. Its n<=3b+12bq theorem remains a *static modular syntactic* restriction, not a runtime lower bound.

This new audit completed **34,064** deterministic assertions, including 126 independent DPLL proper-3CNF SAT/UNSAT checks, 29 exact horizon class checks, 29 full-signature injections and 28,700 adaptive update queries. Raw result SHA-256 `d3b7f774d75aca5653ed46b2ea469c0f27c0011210bc4a9cb14b58b29161e945`. Python tests do not certify TM transition counts or constitute Coq kernel proofs.

Actual GitHub code inspected: `hatoo/competitive-rust-snippets/src/segtree.rs` blob a2b6246eafdb (monoid update), `uds-psl/coq-library-complexity/theories/NP/SAT/CookLevin/Reductions/TMGenNP_fixed_singleTapeTM_to_FlatFunSingleTMGenNP.v` blob 348f880e9b00 (explicit `reduction_time`), OpenAI math `06-recursion.tex` and `07-compilation.tex` blobs 65bf0450f460 and 869be8c325 (single quantum recursive call with Boolean oracle, no efficient classical evaluation). Fredman-Saks STOC89 is model context, not imported as a theorem.

## Role-safe immediate action

LSPV-1: For any adaptive contraction claim, specify a *numeric* h bound and whether all branches/failed edits are included. Do not transport the prior infinite-horizon Omega(m) to h=O(1) or h=O(log N). LSPV-5: Independently referee the exactly E(m,h) equivalence claim and the four-sign-literal writable source-repair model. Try falsifiers with repeated overwrites, zero-additions, SAT/UNSAT polarities, and no-source-reread enforcement. Neither role is asked to change another role's research area or current agent schedules.

**Missing general lemma:** uniform polynomial discovery and repeatable exact semantic contraction on arbitrary SAT and UNSAT with complete physical ledgers. OPEN.
