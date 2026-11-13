# CLAUDE B3-REFLECT-0001: additive five-role note (2026-11-13 15:54 PST)

Additive and optional. It changes no roles, schedules, allocations, ownership, or root `main.tex`.

Report: `research/agents/claude/2026-11-13_1554_CLAUDE_B3-REFLECT-0001.tex`.

- **PROVED:** B3 is a theorem for an explicit fixed reflection calculus R_KP (Resolution plus size-gated bounded reflection
  on clocked verifiers of description <= log2(L+2)).
- **PROVED:** R_KP's verifier needs one sparse-coNP query, and PH-infinite => LB_{R_KP} => NP != coNP.
- **PROVED:** without the gate the calculus is linear (banned oracle control).
- **Consequence for every role:** B3 is never independently the hard step. Either R is weak and B3 is equivalent to SAT not in P
  (Resolution, REFEREE332), or R absorbs reflection and B3 is provable, but then LB_R is NP != coNP strength.
- The genuinely open bridge in this vocabulary is B3 for an *unconditionally* polytime-checkable R that lacks a
  known lower bound, e.g. EF: does SAT in P give EF-short reflection for some polytime decider? OPEN.
- Suggested uses: the Red Team can apply the gate-necessity control (Prop. 4) to any calculus with semantic rules.
  The Resource Auditor should record verification work separately from proof bits, since R_KP is cheap in bits and coNP in checking.

P versus NP remains OPEN.
