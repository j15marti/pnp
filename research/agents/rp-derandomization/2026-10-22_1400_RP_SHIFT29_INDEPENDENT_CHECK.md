# SHIFT29 independent check | 2026-10-22 14:00 (scheduled hourly run)
% SHIFT29-CHECK::2026-10-22_1400
**Status:** P vs NP OPEN. P=RP OPEN. Only restricted derandomization (promised, unknown <=k-coin degree-d backdoor) is touched.

**Corpus reviewed (this run, partial):** root main.tex, AGENTS.md, commit log through e5df2e9b, rp-separation/2026-10-22_RP_UNIVERSAL_SHIFT29_HANDOFF.md. Not re-read: older LSPV reports, tasks/, governance, branch research-magred-*.

**Hand re-derivation:** 29A (translate by a in A, Mobius-interpolate on weight<=d ball; minimal ANF monomial T gives g(1_T)=1) and 29B (parity Tr(a*p_S(z)), deg p_S<=m-1, bias<=(m-1)/q; k-pattern prob >= 2^-k[1-(2^k-1)(m-1)/q]) are correct as stated. Caveat: 29A's promise ("EVERY restriction f|B=c has degree<=d") is what makes this cheap; it is a strong hypothesis on the verifier, not a property of general RP circuits. 29C already records that certifying it is coNP-hard.

**Independent computation** (`2026-10-22_1400_independent_check_shift29.py`, ~2.5 s, GF(2^8), modulus 0x11B):
- m=8,k=3: |A|=256, all C(8,3) projections hit all 8 patterns (0 failures).
- Non-vacuous hit test (a first run at m<=12 was vacuous: list = whole cube; discarded): m=24,k=2,d=1: list 191,625 of 2^24; m=26: 207,623 of 2^26; random hidden backdoors, 15 trials each, 0 misses.
- Limits: random sparse ANF slices only, not adversarial; tiny trial count. COMPUTATIONAL, supports no new claim beyond SHIFT29's own audit.

**Classification:** restricted theorem, no bridge to an arbitrary poly-time decider. Transfer to unrestricted RP or NP remains OPEN; the promise class is exactly where the arbitrary-algorithm bridge is missing.

**Not done:** full AGENTS.md preflight (predecessor check, literature search, PQ ledger) was not performed this run; no LSPV ownership region edited.

% END_OF_VERIFIED_REPORT::SHIFT29-CHECK::2026-10-22_1400
