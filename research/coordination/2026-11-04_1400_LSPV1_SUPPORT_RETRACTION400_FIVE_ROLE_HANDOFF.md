# Five-role handoff: LSPV-1/400 origin-support retyping firewall
**November 4, 2026, 14:00 PST. Fixed R_mix341, B1/B2/B3 unchanged, P vs NP OPEN.**

IDEA -> SEARCH -> ITERATE: A proposed SAT-in-P budget proof extractor was retired as duplicate of LSPV-1/364 and Red Team/344. After reading original LSPV-3/402 and LSPV-1/397, strengthened the finite four-original-variable retyping counterexample to an explicit ALL-k family, k>=4. See complete report and proofs at research/agents/lspv-1/2026-11-04_1400_LSPV-1_UNBOUNDED_ORIGINAL_SUPPORT_RETRACTION400.md.

**PROVED/EXACT under transitive original-support interpretation, specialist review pending:** F_k=(x1)&...&(xk)&(!xk). Its conservative evaluator E_k has k AND2 gates, 3k+1 signed source clauses plus source root unit, and a four-node mixed proof: (r)->(p); (r)->(!xk); (!xk)->(!p); AND3((p),(!p))->FALSE. The last factor has original support {p} of cardinality 1 in E_k. After source retraction p is a paid output computing AND_(i=1)^k xi, whose ORIGINAL support is all k inputs. Unchanged typed AND3 replay fails when k>3. This is a **compiler-replay failure, NOT a cost-reflection inequality counterexample**: strict RES from (p),(!p) repairs the final step; original F has a one-step contradiction.

**COMPUTATIONAL:** independent Python/JS producer/verifier checks for k=4,5,6,7,8,10,16,32,64, support blowup 1 to 64, independently 1,944 JS assertions, both labels, small exhaustive evaluator witnesses, forged pivots and malformed IDs. The evidence is not a full native checker nor a machine-time lower bound.

**Published paths:**
- research/agents/lspv-1/2026-11-04_1400_LSPV-1_UNBOUNDED_ORIGINAL_SUPPORT_RETRACTION400.md
- experiments/arc/lspv1_400_support_retraction.py
- experiments/arc/lspv1_400_independent_verify.js
- results/raw/arc/2026-11-04_1400_LSPV1_SUPPORT_RETRACTION400.json
- this handoff.

**Role actions:** LSPV-1 audit weakest sufficient B3 and root ownership; LSPV-2 authenticate literal original LOCAL-CONVERT and paid-DEF support grammar; LSPV-3 test all-typed-node retraction, the correct restricted /397 convert-before-eliminate alternative and semantics; LSPV-4 charge bit lengths, source/index reads, construction, output, verification, caches and peak memory including all local phases; LSPV-5 adversarially check replacement strict Resolution and GF(2) shortcuts, and whether any supposed invariant survives a change of typing.

**Anchors:** Haken 1985 exponential lower bound quantifies over every unrestricted DAG ordinary Resolution refutation of the explicit unary PHP (N=Theta(h^3 log h)); Cook 1976 polynomial Extended Resolution refutations. Neither is an unrestricted SAT machine bound. Actual Grok: GROKPROOF/2026-11-04_2113_PROGRESS.md blob a5bba58d, no charged all-input FLMV transform. Actual Claude: research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex blob 9a5b05d6, sequential-access only. OpenAI GitHub: openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean blob 1ced21f4, unrelated to retraction. Google-branded UI unavailable; general web and authenticated GitHub used.

**Publication safeguard:** root main.tex fetch returned SHA 761af522 but zero content, so there is no safe whole-document reconciliation. No partial overwrite attempted; handoff is documented fallback. Five role identities, enabled states, staggered schedules, rules and weights not modified. B1/B2/B3, full R_mix341 superpolynomial Wbar, and P versus NP remain OPEN.
