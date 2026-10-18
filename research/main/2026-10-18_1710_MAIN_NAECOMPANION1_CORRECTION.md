# NAECOMPANION1 correction note

Date: 2026-10-18 17:10 Asia/Seoul

Status: exact typographical correction. No theorem status or asymptotic conclusion changes.

In `research/main/2026-10-18_1655_MAIN_NAECOMPANION1.tex`, the two displayed mixed-width cluster bounds

```tex
J\le W\rho^W\left(1+W\log\frac{eN_s}{W}\right)
```

should read

```tex
J\le (W+1)\rho^W\left(1+W\log\frac{eN_s}{W}\right).
```

Reason: widths range from `0` through `W`, so summing the per-width bounds contributes at most `W+1` width classes. The factor is polynomial and does not affect the logarithmic-width exponent

```tex
\log J \le W\log\rho+o(\log q)
```

or any subsequent asymptotic statement.

The locally compiled TeX, PDF, audit bundle, and SHA-256 manifest already contain the corrected `(W+1)` factor.

`FINAL_VERIFICATION_SENTINEL::MAIN::NAECOMPANION1_CORRECTION::2026-10-18_1710::P_VS_NP_OPEN`
