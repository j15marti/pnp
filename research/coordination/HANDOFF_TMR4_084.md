# TMR-4/084 compact handoff: T5 three-bit block-transfer reverse lemma

Keep TMR-4 title PNP Cost-Sound Abstraction, owner, living manuscript, enabled state and existing hourly schedule unchanged. All previous material retained, branch stacked on PR #262.

**D4-T5-BLOCK-REVERSE-084 [restricted exact theorem]:** For complete source-variable FBDDs, the direct 3-bit encoding has 5 valid words (000 through 100) and 3 invalid words, always rejected. A complete 5-ary FBDD of S nodes expands into a *full-decoder block-respecting* Boolean FBDD of <=6S nodes, improving the earlier 7S bound. Conversely, each such Boolean FBDD collapses to a complete 5-ary FBDD without increasing node count. Therefore **S5<=S_block<=6S5**. This is a restricted two-way model equivalence, **NOT** a bound on arbitrary interleaved binary FBDDs or arbitrary machines.

Six decoder nodes are *locally tight for five distinct continuation ports plus invalid rejection*: at least seven decision-tree leaves required. Genuine T5 source x->y has five distinct continuation predicates. Do not claim a global minimum FBDD size.

**32 unary masks:** direct color domain support filtering and validity-restricted Boolean coded mask filtering agree for each of 2x32x32=2048 pair/orientation cases. No unary-mask asymptotic advantage for five-symbol versus valid 3-bit code representation. Direct CNF still needs 3n Boolean variables and 3n+15m clauses.

**Four falsifiers:** (1) early accept ignores invalid codewords, 8 vs 5 on an edgeless one-vertex source; (2) illicit adaptive reject-state cache merge that forgets the visited variable set, discovered and fixed in the reference test; (3) interleaved binary bits invalidate reverse proof; (4) six-node local decoder bound does not imply any global representation or machine lower bound.

**SAME_REALIZATION + four gates:** byte-verified canonical source input; 138 source graphs, 10 invalid preflight rejections; 109,330 native assignment comparisons, 1,048,528 full binary-code comparisons and 45,008 literal CNF checks; 21 extra *adaptive* source-derived FBDD cases (2,625 native, 10,752 code, 17 branch-dependent order); 2,048 mask checks; independent Node.js with 109,330 native checks, 1,048,528 coded and literal CNF checks, 2,048 mask checks. Python and JavaScript repeated with identical summaries, zero unexpected failures. Generic reference source compiler is **exponential** in n and its time/peak memory are charged. The compiled representation transducer alone is linear in explicit node count up to bit-ID overhead; no implied polynomial general CSP algorithm.

Artifacts: full ZIP evidence package for the run; GitHub contains manuscript plus report/handoff. No external formal proof or native TM step trace claimed.

**Next D4-T5-INTERLEAVED-CODE-FBDD-SEPARATION:** find mixed SAT/UNSAT source-authenticated test families with genuine asymptotic binary interleaving advantage after source-aware reductions, or give quantified reverse transfer. Published Barto-Kozik-Niven T5-CSP NP-completeness remains, but P versus NP and unrestricted time lower bounds remain OPEN.
