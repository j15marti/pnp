# SELECTOR-ELIMINATION-QUANTIFIERS11 handoff

2026-10-20 09:48 Asia/Seoul. Two routes only. P versus NP OPEN.

**New PROVED composition lemma:** a fastest universal selector is unnecessary for the contradiction route. Under `P=NP`, existentially fix any one polynomial solver `A` for the single standard MMW query language, with fixed exponents `C,D`. If total charged fixed-`k` reductions `R_k` exist for an unbounded set of `k`, choose one sufficiently large fixed `k` after `C,D` and hardwire both machines. Required order: `exists A,C,D exists k,R_k forall inputs`.

For `M=N^(a+o(1))`, ideal exponents are

`t=a(1+(C+1)/k)`, `s=a max(1,D)/k`.

Entry into `t<241/200,s<1/2` is possible for any fixed `C,D` only when `a<241/200`; explicit output blocks it for `a>=241/200`.

**Hutter boundary:** published time bound is `5t_p+d_p time_(t_p)+c_p`, so effective exponent is `H=max(C,E)` where `E` evaluates the proved bound. It does not reduce `C`, prove simultaneous space, or cover uncertified programs. SPACE-CAPPED-UNIVERSAL-RACE2 preserves candidate exponent and requires rewindable input for its clean space ledger.

Audit: 65,536 fixed `(C,D)` cases; powers-of-two cofinal controls; 65,536 Hutter `(C,E,D)` cases; `C_k=k^2` failed for all `k<=4096`; finite `k<=100` failed at `C=1000`; exact stretch thresholds reproduced; 331,789 assertions, zero failures.

Assignments:

* :00 -- build/refute total both-promise `R_k` for an unbounded fixed-`k` set; give output stretch.
* :12 -- one fixed MMW query encoding and one capped certified candidate; ledger `E` and peak space; do not optimize fastest selection.
* :24 -- all-input hereditary ARC successor with full same-machine ledger, two iterations.
* :36 -- attack `k`-dependent language/exponent, output stretch, hidden source tables, quantifier inversion.
* :48 -- compose only `exists fixed A` then `exists fixed k`, both valid for all inputs.

Open: total deterministic ordinary-MKTP `R_k`; standard-model Ilango replacement; no `M`-bit side table; stretch below target; all-input ARC contractor; actual diagonal shared-witness lower bound. Root `main.tex` remains unsafe and untouched.
