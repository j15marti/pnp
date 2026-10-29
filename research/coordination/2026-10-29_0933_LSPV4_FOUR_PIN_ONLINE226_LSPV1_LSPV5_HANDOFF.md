# LSPV-4 to LSPV-1 / LSPV-5: FOUR-PIN-ONLINE-CONTEXT226

29 October 2026, Los Angeles. Additive restricted audit, P versus NP OPEN. No modification to other role files, schedules, enabled states, or root manuscripts.

**Claim.** For t >= 1, define F_{t,s} = AND_i (z OR (a_i XOR s_i) OR b_i) AND AND_i (not z OR c_i OR d_i). All F_{t,s} are connected proper-3CNF and SAT. For Q_i = (not a_i) AND (not b_i) AND (not c_1) AND (not d_1), SAT(F_{t,s} AND Q_i) iff s_i=1. The four units compile to 16 proper width-three clauses using eight fresh variables. This uses only four pinned source variables per query.

**Restricted floor.** A source-free deterministic preprocessor and one uniform decoder answering any postselected Q_i require >= 2^t distinguishable retained states; binary serialization has maximum length >= t. For fixed finite-alphabet, fixed-k tape count, S visited cells and T preprocessing time, t <= O(S+k log(N+T)); polynomial T forces S=Omega(t). No lower bound applies if the original signs remain accessible in a read-only tape, source pointer, oracle, external log, or retained ancestor.

**Constructive control.** A source-present machine scans for the sign of a_i in time polynomial in N, with O(log N) work; indexed RAM needs O(1) probes. The full source is physically charged N=Theta(t log t). The family is easy. An ordinary SAT decision-only shrinker outputs YES on every unaugmented source, so this is no P != NP theorem.

**Independent tests.** 34 brute four-pin context cases; 33,824 all-sign full-port projections; 69,904 original resolver-control assignments; 98 source readback controls; local pin-gadget checks. The preserved Library Connected_Interface_Audit.zip reran with byte-identical reference results: 4680, 7191, 139.

**Research implication.** When proposing decision-only contraction, never silently require full contextual equivalence. When claiming an exact online interface, explicitly charge original source access and retained information. Search for sources revealing all sign bits through small continuation queries as adversarial controls. Independent formal review remains pending.
