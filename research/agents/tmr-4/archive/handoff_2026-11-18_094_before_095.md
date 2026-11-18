# TMR-4 compact handoff, 2026-11-18, /094

**Stable identity:** TMR-4 / PNP Cost-Sound Abstraction; no title, owner, enabled state or hourly Pacific schedule change. Preserve main4_PNP_COST_SOUND_ABSTRACTION.tex and all /083-/093 sections. Primary exact template T5 = Z5 with R(a,b) iff (b-a) mod 5 in {1,3}. P versus NP OPEN.

**NEW PROVED/EXACT RESTRICTED SOURCE THEOREM, peer review OPEN:** For loopless directed adjacency matrices with M=n(n-1) independent ordered-arc bits, the exact minimum source probes on the empty graph by **any globally correct deterministic bit-probe T5 satisfiability decider** is

    C_SAT(empty) = n(n-1) - floor(2n^2/5).

On its zero-input branch let H contain all unread arcs. H must be T5 SAT or its input would be indistinguishable from the empty graph. For any 5-coloring, at most one arc across each differently colored vertex pair is permitted, giving at most floor(2n^2/5) unread arcs. The matching total algorithm preselects balanced coloring h(i)=i mod5, probes all forbidden arcs, accepts with witness if all zero, and otherwise reads the remainder and brute-force decides. This **does not yield an all-input polynomial solver**. The same empty G has a constant-TRUE *assignment* predicate with 5^n accepting assignments and a complete five-way OBDD of width 1 and n nodes. Reverse semantic/source transfer also fails.

**STRICTLY SEPARATE forward-only promise:** If only arcs i->j for i<j are allowed, the exact zero-source certificate is binom(n,2)-floor(n^2/3), via transitive K4 obstruction, Turán extremality, and balanced consecutive intervals colored (0,3,1). n=100 full model needs 5900/9900 probes; forward model needs 1617/4950. Both are input-length-scale only.

**Four falsifiers:** source grammar or loop switch invalidates formulas; exact assignment-OBDD width does not imply source complexity or vice versa; individual bit-probe oracle excludes free packed reads, batches and compulsory full-source hashes; minimal zero-source YES certificate is not a general polynomial-time decider. Physical/Turing-machine transfer OPEN. Grouped three-bit Boolean decoding at most 6 binary nodes/native node; arbitrary interleaved/adaptive FBDD transfer OPEN. Fixed-CNF clauses 3n+15m, literals 9n+90m; all 32 masks remain validity-code exact.

**SAME_REALIZATION:** charge source authentication, matrix address computation, probes, preselected witness, fallback full read and at most 5^n coloring checks, sharing/caching, integer arithmetic, output, any conversion. No Fourier or source-solver oracle. Raw SHA-256 authentication of all M bits consumes all M reads, distinct from the formal minimum *query certificate*.

**Four COMPUTATIONAL gates:** independent Python superset zeta and JavaScript direct submask enumeration agreed on all 1,052,741 full directed matrices n<=5 (n=5 SAT 33,369, UNSAT 1,015,207; q=10 of 20) and 2,131,019 forward matrices n<=7 (n=7 SAT 709,097, UNSAT 1,388,055; q=5 of 21). All 1,099 and 69,931 certificate completions SAT. CNF pointwise evaluations: full 2000+3000, forward 1880+1568; each of four implementations verifies 2048 oriented 32-mask cases. 12 independent source hashes (5 full,7 forward) with canonical parity, 15 malformed controls, zero unexpected failures. Full scripts, raw JSON, hashes, standalone section TeX and locally compiled three-page PDF retained in /094 evidence package.

**Four foundational gates:** DISJ PASS cheap-source control; relativization OPEN for stronger oracle model; simultaneous DTISP PASS only same-realization UPPER time/space; deterministic config counting NOT APPLICABLE as lower bound. Independent mathematical review and physical standard-TM microstep analysis OPEN. Full owner manuscript preflight not executed without a repository checkout; standalone /094 LaTeX section compiled.

**Publication:** research/agents/tmr-4/2026-11-18_TMR4_T5_SOURCE_DECISION_CERTIFICATE094.md; updated main4; archived exact /093 handoff at archive/handoff_pre_2026-11-18_094.md. PR is draft, NOT merged to main unless later verified.

**Next named dependency:** D4-T5-UNIFORM-DECIDER-ADVERSARY-095: an all-input original-source decision adversary beyond input-access cost, with universal arbitrary-machine transfer and complete cost accounting, if one exists. P versus NP OPEN.
