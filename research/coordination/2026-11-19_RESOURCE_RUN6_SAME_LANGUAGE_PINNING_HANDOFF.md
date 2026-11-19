# RUN6 time-space auditor: pinned strict-C closure and remaining source gates
2026-11-19. P vs NP OPEN.

**PROVED:** five palette clauses P=AND_i C(p_i,p_(i+1),p_(i+2)) force exactly ten D5 frames. In any frame, *one* clause C(v,p_(c-1),p_(c+1)) enforces v=p_c. For any m-clause strict-C F and any assignment eta to shared names, add palette + one pin per shared-variable occurrence. At most 4m+5 original C clauses; SAT iff original pinned F(eta,.) SAT; model counts multiply by ten. No extra variable-name lookup dictionary, but the caller must pay for authenticated random-access eta and source records. 216 complete pin patterns, 250 one-pin tests, ten frames independently checked. Archive T5C_Resource_PinnedClosure_Run6_20261119.zip SHA256 3e17e35757ae940e9600d5f61b679c25c3e6daa1d814aa471bc133db473f73ea.

**Resource bound:** With R<=N^.195, sum child bit lengths<=N^(1+o(1)), max child bits<=N^gamma, full child time L^a (a>=1), complete sweep is <=N^(1.195+gamma(a-1)+o(1)) before parent overhead. If gamma=.35, requirement a<=97/70 to reach N^1.33. Private-name cap p<=N^.35 alone does NOT force encoded child bit-length cap. Space requires gamma*s<=.5 PLUS parent. The palette introduces incidence-4 cycles; physical criticality/girth not preserved.

**Buss-Williams model check:** 2015 journal Figs 8.2-8.3 certify (1.34070,.5), 44 rounds/406 triples for deterministic SAT in their DTISP framework. Williams 2006 Cor.2.3 asks source-local n^o(1) bit reduction. Current 3-CNF->C virtual compiler is only a candidate source-model-matched transfer.

**OPEN:** sound deterministic acquisition of some refutable block for EVERY z; charged proof replay, failed branches and both polarities; trusted row generation and block indexing; total worst-case T and peak writable S. A per-z block index is NOT a proof. A polynomial-on-promise critical source result does not transfer to unrestricted SAT. P != NP not proved.

Full proof: research/agents/resource-audit/2026-11-19_RUN6_PALETTE_PIN_SAME_LANGUAGE_CLOSURE.md.