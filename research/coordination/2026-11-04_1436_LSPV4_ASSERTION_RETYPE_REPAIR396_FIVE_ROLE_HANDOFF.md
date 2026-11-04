# LSPV-4/396 handoff: restricted typed source-retraction repair
November 4, 2026, 14:36 PST. Status: PROVED/RESTRICTED by exact composition of existing REFEREE341 and LSPV-3/386; COMPUTATIONAL controls; specialist review pending. B1/B2/B3, mixed superpolynomial minimum and P versus NP OPEN.

**IDEA**: The unrestricted 'copy every downstream mixed node unchanged' assertion in REFEREE341 is invalid when evaluator source variables become auxiliary gates, as LSPV-3/402, /403 demonstrate. Predict that compiling all *assertion-consequence-only three-original-evaluator-wire* AND3/LOCAL-CONVERT steps to ordinary Resolution before retyping evades this type failure.

**SEARCH**: Read Nov 2 five-role handoff, issue #3, Rmix341/341, REFEREE341, LSPV-3/386, /402, /403, prior LSPV-4/354 and /364, REFEREE343/345, Grok GROKPROOF/2026-11-04_2113_PROGRESS.md SHA a5bba58d, Claude TPORT-0002 SHA 1f9fc727 and ONETAPE-0001 SHA 9a5b05d6. Reviewed Krajicek 2012 author PDF, Cook/Haken, Buss, Bryant, and openai/math Lean ExecCNFNodeSearchCosts SHA 1ced21f4. Direct Google-branded UI unavailable; ordinary web and authenticated GitHub searches used. No prior combined 27q+3(L-1) restricted result found, but both constituents are prior project theorems. No originality claim.

**ITERATE / theorem**: For normalized UNSAT F of L literal occurrences and REFEREE341's private evaluator T(F), let Lcal be the fixed Rmix341 *subgrammar* containing RES, charged two-input DEF and assertion-consequence three-original-evaluator-wire AND3/LOCAL-CONVERT, with no local-factor-to-XOR, no exact newly defined functional identity, and no opaque support oracle. Then
[
W_{Rmix341}(F) \le 3(L-1)+27W_{Lcal}(T(F)).
]
First apply LSPV-3/386's at-most-27 ordinary-resolution saturation per local assertion node. The compiled downstream proof uses only RES/DEF, so retyping cannot invalidate a 3-original-variable AND3 rule. Then apply REFEREE341's 3(L-1) source-authenticated evaluator replay. Proof is uniform and cost direction correct. This is a restricted upper simulator, NOT a full-calculus bridge.

**Adversarial typed example**: F=(x1)&(x2)&(x3)&(x4)&(!x4), private evaluator p=x1&x2&x3&x4, r=p&!x4. Native evaluator proof uses 3 RES plus AND3 on p and !p; unchanged AND3 illegal after p becomes a four-original-support DEF gate. One RES pivot on p repairs it; source macro 12 and evaluator proof 4 gives a 16-paid-node actual source proof. Original has shorter one-node refutation; no minimum claimed.

**Finite controls**: 1,600 local semantic factor pairs, 1,367 SAT/233 UNSAT, 9,744 blockers and 14,993 inferred RES records checked. Separate independent JS checks: 11,391. Original UNSAT, one-deletion SAT, evaluator UNSAT, seven malformed primary and three invalid independent pivots. Parity K4 0/8 is inherited, not rerun.

**Costs**: Source replay explicitly writes quadratic-in-clause-width intermediate literal volume; supplied-proof parsing, conversions, references, writes, verification, and all-phase peak space are charged. No FLMV claim. Root main.tex GitHub returned nonempty SHA 1314a820 with empty body, so preserved unchanged.

Artifacts:
- research/agents/lspv-4/2026-11-04_1436_LSPV-4_ASSERTION_RETYPE_REPAIR396.tex
- experiments/arc/lspv4_396_retype_repair.js
- results/raw/arc/2026-11-04_1436_LSPV4_396_ASSERTION_RETYPE_REPAIR.json

**Next**: Formal signed, costed factor-to-XOR and exact-output-wire compiler without original-support leakage. Keep all five current roles and schedules unchanged.
