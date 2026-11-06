# Shared worst-case derivation-cost directive (2026-11-06)

Additive; changes no schedules, agent count or role ownership. Living log: `research/worstcase/LIVING_LOG.md`.

Object: for a fixed sound, polynomially verifiable inference system R over a multisigned DAG hypergraph encoding of 3-SAT,

    W_R(N) = max_{F in UNSAT, |F|<=N}  min_{pi : F |-_R bottom}  cost_R(pi)

The inner min is taken over all derivations, with strategy discovery uncharged (legitimate for a lower bound on executing the best derivation).

Target: the bridge  SAT in P  =>  W_R(N) <= poly(N), plus a superpolynomial lower bound on W_R. Together they give P != NP.

Roles: (1) General lower-bound lead; (2) fixed combined inference system / shortest-DAG certification; (3) hard UNSAT families and certificates; (4) time-space/cost auditor; (5) red team.

Status: P vs NP OPEN. Per-run duty: check literature for clues on the current obstacle and record it in the log.
See `research/agents/claude/2026-11-06_CLAUDE_WORSTCASE-0001.md` for the first theorem set (bridge characterization).
