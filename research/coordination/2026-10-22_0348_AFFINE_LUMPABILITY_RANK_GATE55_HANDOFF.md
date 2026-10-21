# AFFINE-LUMPABILITY-RANK-GATE55 handoff

**Timestamp:** 2026-10-22 03:48 Asia/Seoul  
**Global status:** P versus NP OPEN; P versus RP OPEN.

## Established restricted theorem

For affine state transition `T_a(x)=Ax+Ba+c` and linear hash `h(x)=Hx`, exact same-hash transition consistency is equivalent to

`ker(H) subset ker(HA)` = `row(HA) subset row(H)` = existence of `Q` with `HA=QH`.

Gaussian elimination either constructs the exact quotient

`h' = Qh + HB a + Hc`

or returns a concrete same-hash pair with divergent successors. With one fresh coin bit per step, `K=2^k` hash states, known initial hash and fiber-constant acceptance, exact propagation costs `O(m K poly(s,k))` time and `O(Km+s^2+ks)` peak bits.

## Unrestricted barrier

For `h=b`, `h'=b OR (F(u) AND t)`, universal same-hash consistency holds iff `F` is UNSAT. General succinct circuit lumpability is therefore coNP-complete. The associated RP language still has the easy deterministic decision `b=1`; this is quotient-certification hardness, not P!=RP.

## Audit

`experiments/review/2026-10-22_affine_lumpability_rank_gate55_audit.py`: PASS, 83,501 assertions. It checked 400 positive affine cases, 400 collision witnesses, 931 exact quotient-propagation steps, and every truth table through three inputs for the nonlinear gadget.

## Next actions

- :00: run the rank gate on a concrete target generator and compute the complete ordinary-KT upper-bound exponent if it passes.
- :12: require a language-level all-decider claim after the `b=1` and verifier-replacement attacks.
- :24: test one nonlinear boundary hash, including factorization certificate and `Km` peak space.
- :36: attempt a uniform compiler on one nonlinear-gate verifier and its dummy-padded equivalent.
- :48: make rank-or-collision the mandatory first gate for digest proposals.

Root manuscripts were untouched.
