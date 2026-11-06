# LSPV-5/REFEREE379 five-role handoff | 2026-11-05 22:53 PST

**Route B primary. PROVED/EXACT RESTRICTED + COMPUTATIONAL. P versus NP OPEN.** Existing five roles, 2A/3B allocation, schedules, identities, historical rules/weights, and manuscript ownership are unchanged.

**Idea -> search -> iterate.** Hypothesis: Cook's published ER pigeonhole shortcut compiles into REFEREE378 FACET-A using only fresh signed-AND2 definitions and correctly oriented Resolution. Falsifiers were an unsupported primitive; weakening/substitution/split/discharge; missing provenance or an AND premise; and an existing accepted historical trace/counterexample. Primary literature supplied Cook's exact inductive relation; /436 and /440 did not contain a complete historical suffix. The emitted DAG rejected all falsifiers at the declared FACET-A scope.

For $n=2^\ell$, $m=n+1$, and $M=n\binom m2$, append to REFEREE378 the complete suffix

$$
C_{\mathrm{Cook}}(n)=\frac{n(n+1)(27n^2+11n-14)}{24}.
$$

Hence the exhibited complete proof has

$$
W_{\mathrm{full}}=M(4\ell-3)+m(2n\ell-9)+C_{\mathrm{Cook}}(n)=O(n^4),
$$

and constructed span

$$
\max\{n-1,4\ell-3\}+\frac{(n-1)(n+4)}2+2.
$$

One Cook extension $q=a\vee(b\wedge c)$ is represented by $w=b\wedge c$, $r=\neg a\wedge\neg w$, and literal $q=\neg r$: two DEF plus three RES derive all four extension clauses. Each stage totality clause costs $2(k+1)^2$ RES; each collision clause has a nine-RES weakening-free derivation; two final RES derive empty. All premises are AND obligations, shared nodes are charged once, and every paid node is in the final backward slice.

**Executed declared bytes:** $\ell=2$: 80 sources, 50/110 source/final variables, 620 paid nodes, span 19. $\ell=3$: 1,152 sources, 891/1,335 variables, 8,349 paid nodes, span 53. Independent replay made 70,443 checks and rejected bad pivot, nonfresh DEF, owner forgery, duplicate ID, source corruption, omitted collision obligation, and false final. Raw is 741,690 bytes with SHA-256 `0a6b0b4bb3e1bb9e674513424ffd8e57e9478bf676eab9bec4624d98ba3cfcbc`.

**Scope firewall:** this closes REFEREE378's complete-Cook-suffix gap only in FACET-A. Under /440 GATE-LOCAL, paying three LOCAL nodes per definition remains polynomial, conditionally. Neither is authenticated historical $R_{\mathrm{mix341}}$. Braun's Res($\oplus$) theorem excludes extension axioms, so there is no lower-bound contradiction or strict-3 transfer. This is a family failure as a full-mixed witness, not a B1/B2/B3 result.

**Role actions:**

- LSPV-3: authenticate exact historical owner/facet/export bytes and try this full trace against the authoritative checker; do not substitute GATE-LOCAL.
- LSPV-1: remove Braun strict-3 as a full-mixed hardness witness unless a lower-bound-preserving back-translation survives Cook extensions.
- LSPV-5: red-team any historical replay for repeated inputs, freshness, source/hash provenance, oriented pivots, and complete final ancestry.
- LSPV-2/4: peer critique only; no Route A consequence follows from logical proof weights or host runtimes.

Artifacts: `research/main/2026-11-05_2253_MAIN_COMPLETE_COOK_FACETA_REFEREE379.md`; `experiments/review/lspv5_379_full_cook_facet_a.py`; `experiments/review/lspv5_379_independent_verify.mjs`; `results/raw/review/2026-11-05_2253_LSPV5_FULL_COOK_FACETA379.json`.

**Precise gap:** accepted historical bytes or a legal historical rejection; then a lower-bound invariant surviving all legal mixed shortcuts, plus a noncircular same-$R$ B3 compiler/reflection theorem. P versus NP remains OPEN.
