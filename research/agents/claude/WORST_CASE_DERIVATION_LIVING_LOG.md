# CLAUDE living log: worst-case minimum derivation directive

Target (shared five-role directive, 2026-11-02 12:04 PST):
`Wbar_R(N) = max_{F in UNSAT, |<F>| <= N} min_{pi: F |-_R bot} cost_R(pi)`, with free optimal proof
choice, and the weakest bridge **B3: SAT in P => Wbar_R(N) <= poly(N)** for the same preselected R.
Status vocabulary: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.
**P versus NP remains OPEN.** Newest entry first. Each entry links its verified report.

---

## 2026-11-13 15:54 PST: B3-REFLECT-0001

Report: `research/agents/claude/2026-11-13_1554_CLAUDE_B3-REFLECT-0001.tex`
Control: `research/agents/claude/b3-reflect/toy_reflection_control.py` (+ `_results.json`, PASS, <1 s)

- **PROVED/EXACT:** B3 holds as an implication for one explicit fixed, sound, complete calculus R_KP
  (Resolution plus a size-gated, padded, bounded-reflection rule: a proof may cite any clocked verifier
  (M,k) with description <= log2(L+2) that is sound on all inputs up to length L).
  Under SAT in P, the decider A yields linear-padded proofs and the reflection check is a coNP check, so in P.
- **PROVED/EXACT:** R_KP's verifier is P with one query to a sparse coNP set; it is a Cook-Reckhow system
  only conditionally.
- **PROVED/EXACT (with known theorems):** PH infinite at level 3 => LB_{R_KP} => NP != coNP.
  The lower bound for R_KP is therefore NP != coNP strength.
- **PROVED/EXACT control:** without the size gate the system is linear (`Wbar = O(N)`) unconditionally. This is the banned
  hidden validity oracle.
- **Lesson:** B3 is never the bottleneck by itself. For a weak R with a known lower bound, B3 is equivalent to SAT not in P.
  For a reflection-strong R, B3 is provable but LB_R is at least NP != coNP strength. Classify as a reformulation,
  not progress.
- **Literature:** Krajicek-Pudlak 1989 (E=NE => p-optimal), Kobler-Messner-Toran, Egidy arXiv:2602.02294
  (2026 oracles for optimal proof systems), Cook-Reckhow 1979, Yap 1983; "P=NP => EF p-bounded" is not a known theorem.
- **Next target:** B3 for EF = EF-provability of reflection for some polytime SAT decider; open.
- Root `main.tex` and trackers: no material change (this routine owns no region).
