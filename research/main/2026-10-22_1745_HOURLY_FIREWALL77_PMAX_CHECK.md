# HOURLY-FIREWALL77-PMAX-CHECK

Timestamp: 2026-10-22 17:45 UTC (scheduled hourly check)

**Global status: P versus NP OPEN. No load-bearing arrow closed by this note.**

Repository accessible; newest activity is PADDING-SELF-REDUCTION-FIREWALL77 (01:48 KST) and the Grok 4.7 review (02:11 KST). No open-PR work was inspected beyond branch listing.

## Check performed (COMPUTATIONAL)
Independent bisection of the root of `p*s = d_F(p*c)`, `d_F(x)=((x+2)/x^2-x)/2`, for the three envelopes in Lemma 77B (`scripts/check_firewall77_pmax.py`, output `results/firewall77_pmax_independent_check.json`; single run, well under 30 s).

| Envelope | p_max | beta*p_max |
|---|---|---|
| baseline (1.2,.5,.5) | 1.0038366955668923 | 0.5019183477834461 |
| safe (1.205,.5,.5) | 1.0003908750570747 | 0.5001954375285373 |
| retuned (1.2021,.505,.505) | 1.0006572899254427 | 0.5053319314123486 |

All three agree with the Lemma 77B table to the printed digits. This checks arithmetic only; the FLMV curve `d_F` itself was taken from FLMV-PROBE-MARGIN71 and not re-derived here.

## Not done
No literature search or corpus-wide reconciliation was performed this run; root `main.tex` was not edited (no new verified mathematical content). The OPEN items (exact source compression, compact witness premise) are unchanged.
