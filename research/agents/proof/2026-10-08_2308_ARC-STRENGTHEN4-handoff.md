# ARC-STRENGTHEN4 handoff

- Result: **PROVED/EXACT** local adapter from a clause-indexed exactly-3CNF stream to canonical `CNF1`. Offset renaming makes all zig-zag literals fixed-width ULEB128; virtual random access costs polylogarithmic time and `O(log n)` space with no materialized formula.
- Endpoint: primary FLMV Theorem 3.1/model and Corollary 5.8 reverified. At `c=1201/1000`, `d(c)=1468676399/2884802000 > 1/2`.
- Remaining encoding gap: **OPEN** direct oblivious Cook/Pippenger–Fischer tableau to a clause-indexed exactly-3CNF stream, or an equivalent local locator for FLMV's formula serialization. Do not claim generic variable-length transcoding.
- Construction audit: cyclic complete-parity 3CNFs form an infinite easy family missed by the current portfolio. The present parity-star rejection path costs `Omega(N^2/log^2 N)`, so that member cannot remain uncapped in an `N^(6/5+o(1))` phase.
- Marker audit: current tags 1/2 cannot nest literally. A new quoted/fresh-tag grammar with charged rebasing is required. The nested HMCB proposal is still **CANDIDATE** and promise-relative.
- Validation: 10 width boundaries, 320 brute-force semantic cases, and all 15,956 addressed bytes passed in 0.034 seconds; see companion script/JSON.
- Proof status: conditional completed-phase composition and conditional `K` elimination remain exact. Unrestricted all-input acquisition from `SAT in P`, finite ARC entry, and `P versus NP` remain **OPEN**.
- Next ARC target: source-check the direct clause-indexed Cook stream. Next Construction target: all-input PRE-A acquisition without a parent-scale semantic call.
