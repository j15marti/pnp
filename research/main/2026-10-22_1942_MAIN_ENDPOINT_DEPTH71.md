# ENDPOINT-DEPTH71

Timestamp: 2026-10-22 19:42 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

Follow-up to PARENT-PROBE-BUDGET70's open item "check whether equality at 6/5 and lower-order factors are tolerated". This note settles only the *exponent-recurrence* half of that question.

## Lemma 71A — geometric convergence, strict endpoint

For `f(c)=max(lam, alpha+beta*c)`, `0<beta<1`, `c_*=max(lam, alpha/(1-beta))`, and any start `c_0>=c_*`:

- if `alpha/(1-beta)>lam`: `c_d - c_* = beta^d (c_0 - c_*)` exactly;
- otherwise `c_d = lam` once `alpha+beta*c_d <= lam`, and `c_d>=lam` always.

Consequently, for the `(alpha,beta)=(0.6,0.5)` ledger with `lam<=1.1` and the per-child full-scan start `c_0=1.6`, depth `d(eps)=ceil(log2((c_0-c_*)/eps))` gives `c_d <= 6/5+eps`, but `c_d > 6/5` for every finite `d`. Depths: eps=1/10 -> 2, 1/100 -> 6, 1/1000 -> 9, 1e-6 -> 19.

**Status: ESTABLISHED arithmetic.** The limiting exponent `6/5` is a bound `6/5+eps` for every fixed `eps>0` at constant depth `d(eps)`, never an attained exponent. Any downstream use that needs `c<=6/5` *exactly* (rather than `<6/5+eps`) cannot be served by finite recursion; use of the `eta<=0.6` slack region (equality `alpha+eta=6/5`) is therefore only safe where the target tolerates `+eps`.

## Lemma 71B — lower-order terms

If level `i` adds an additive `o(1)` exponent error `e_i<=e`, then `c_d <= c_* + beta^d(c_0-c_*) + e/(1-beta)`. At `beta=1/2` accumulated slack is `<=2e`, still `o(1)`. Per-level multiplicative constants contribute `K^d`, constant for fixed `eps`.

**Status: ESTABLISHED arithmetic; assumes each level's overhead is independently `n^o(1)`, which for the real transformer is CONDITIONAL on the OPEN hereditary compiler.**

## Consequence for the route ledger

- The `eta<=0.5` primary target is unaffected (strictly `lam=1.1<6/5` gives room).
- The `0.5<eta<=0.6` slack interval is demoted from "equality-preserving" to "`+eps`-preserving" (CONDITIONAL on target tolerance). This is an accounting correction, not a refutation.
- No semantic transformer, both-label reconstruction, or model transfer is advanced. All load-bearing arrows remain OPEN.

## Literature check

FLMV (Fortnow, Lipton, van Melkebeek, Viglas, JACM 2005) and its descendants (Fortnow–van Melkebeek 2000: SAT not in time n^phi with n^o(1) space; Williams 2007: exponent 2cos(pi/7)~1.8019) are the relevant time-space lower bounds; exponent `1.6` of per-child full scans sits just below phi~1.618 only coincidentally in this ledger -- no transfer is claimed. A web search this run did not return a primary FLMV statement, so the exact endpoint form remains to be checked against the JACM paper (still the :48 role's open test).

## Audit

`research/code/endpoint_depth71_audit.py` (stdlib, exact rationals, <1 s): 90,008 checks, 0 failures; raw data `research/main/ENDPOINT_DEPTH71_raw.json`. Accounting audit only. A first draft of the script had a flawed check (tested start below the fixed point); fixed before recording.

No root `main.tex`, automation, or role assignment was modified.
