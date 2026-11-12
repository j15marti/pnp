# Living log: worst-case minimum derivation cost  \overline W_R(N)

Shared target: \overline W_R(N) = max_{F in UNSAT, |<F>|<=N} min_{pi: F |-_R bot} cost_R(pi);
priority bridge: SAT in P => \overline W_R(N) <= poly(N).
P versus NP: **OPEN**. Each entry is append-only.

## 2026-11-11 20:48 PST — CLAUDE-WCDERIV-0001 (red-team lens)
Report: `2026-11-11_2048_CLAUDE_WCDERIV-0001.tex`
- KNOWN THEOREM transfer (new to corpus): Cook 1975 PV reflection. If a polytime A rejects all UNSAT CNFs
  and PV proves the *soundness* of A's rejections, then \overline W_EF is polynomial, and (CONDITIONAL on [P2-D1]
  native authentication of the EF->ER->RES+DEF simulation, LSPV-1/406) so is \overline W_{R_mix341}.
- Corollary: [P2-B1] alone implies "no polytime SAT algorithm has PV-provable soundness", not P != NP.
  The remaining gap is the reflection step from truth to PV-provability (OPEN, no known technique).
- PROVED/EXACT dilemma: for any R whose lower bound is already known (Resolution, regular / bounded-depth Res(xor),
  CP, PC, AC0-Frege) Bridge(R) is *equivalent* to P != NP. Because R_mix341 p-simulates EF, [P2-B1] implies
  superpolynomial EF lower bounds, which have been open since 1979.
- Red-team flag: the Pang arXiv:2610.00837 citation used in the corpus could not be located by an independent search;
  Braun arXiv:2609.23015 exists, is AI-assisted, and has not been refereed.
- Next: (1) Theorem A as the default conditional B3; (4) byte-domination audit of the EF simulation;
  (5) a hostile restricted-class rejector whose soundness is plausibly not provable in PV.
