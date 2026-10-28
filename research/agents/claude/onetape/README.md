# One-tape crossing-sequence notes (CLAUDE ONETAPE-0001)

Added 2026-10-28 at the user's request. Reference/research artifact; changes no schedules, allocations or ownership. **P versus NP remains OPEN.**

Report: `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`.

| File | Purpose |
|---|---|
| `SOURCE_note1_onetape_lower_bound.txt` | Owner's note: Ω(N²/log N) for one-tape 3-SAT deciders via the equality family F_{a,b}. Verbatim. |
| `SOURCE_note2_tightness_and_limits.txt` | Owner's note: matching O(kN) upper bound, padding/repetition limits, single-cut O(N) cap. Verbatim. |
| `verify_family.py` | Builds F_{a,b} in an exact-width-3 encoding; checks uniform lengths, SAT ⇔ a = b (k ≤ 5), growth of N_k, and where the union bound starts. |
| `verify_family_results.json` | Output. |

## Findings

| Item | Status |
|---|---|
| Both notes | PROVED/EXACT (known type: Hennie; Santhanam IPL 2001 for SAT on multitape machines) |
| The bound holds for nondeterministic one-tape machines and is tight there up to polylog | PROVED/EXACT |
| Sequential-access portfolios: T·S = Ω(N²/log N), so the UWI small-space portfolio statement holds up to exponent 2 with sequential input | PROVED/EXACT |
| Beyond N² on one tape ⇒ superlinear multitape lower bound for SAT | PROVED/EXACT (translation); the target itself is OPEN |
