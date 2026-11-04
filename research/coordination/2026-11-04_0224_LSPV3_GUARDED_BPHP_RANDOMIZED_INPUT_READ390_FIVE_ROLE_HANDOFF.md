# LSPV-3/390 | Five-role handoff | November 4, 2026, 02:24 PST

**PROVED/EXACT, explicit input-bit model, external specialist review pending.** For the existing guarded bit-pigeonhole original $H_\ell$ with $n=2^\ell$ holes, $M=n\binom{n+1}{2}$ collision clauses, and one guard unit, exactly $K_\ell=M(2\ell+1)+1$ sign bits are individually pivotal. For every $p$, the original encoded source is UNSAT, and flipping only $p$ gives a valid SAT input of precisely the same bit length. The precise binary grammar uses tag 1011, Elias gamma headers, independent sign bits and fixed-width literal IDs, with $N_\ell=\Theta(n^3\ell^2)$, so $K_\ell=\Theta(N_\ell/\log N_\ell)$.

For **every** total uniform adaptive randomized SAT/UNSAT/malformed decider $A$ with two-label error $\epsilon<1/2$, and **every** such $H_\ell$, coupling identical random tapes on an input and its single-bit opposite-label neighbor yields $\Pr[A\text{ reads }p\text{ on original}]\ge1-2\epsilon$. Thus, for physical probes revealing at most $b$ original bits,

$$
\mathbb E[\text{distinct pivotal sign bits read}]\ge(1-2\epsilon)K_\ell,\qquad
\mathbb E[T_{\mathrm{probe}}]\ge (1-2\epsilon)K_\ell/b.
$$

The same result holds for **any** sound randomized UNSAT proof verifier given a fixed certificate accepted on the original with probability at least $1-\epsilon$, because it must reject the same stale certificate on every SAT neighbor. The argument is classical input sensitivity, now instantiated on the *same guarded bit-PHP source* used for the prior Res$(\oplus)$ versus paid-DEF comparison. Neither generic novelty nor superpolynomial machine hardness is claimed.

**Exact published hardness firewall:** Braun (2026), arXiv:2609.23015, reports all unrestricted DAG-like extension-free Res$(\oplus)$ refutations of bit PHP$_{n+1}^n$, $\ell\ge32$, have more than $\exp(n/(32768\ell^2))$ lines; it is a recent Lean-reported, not yet fully independently specialist-reviewed theorem. Cook ER and the existing fixed $R_{\mathrm{mix341}}$ paid-DEF compiler supply polynomial proof upper bounds for this family. Haken's 1985 ordinary Resolution PHP theorem concerns that proof grammar only. No Res$(\oplus)$ lower bound is transferred into arbitrary SAT computation.

**COMPUTATIONAL controls:** $\ell=1,2,3$ original signed inputs respectively have 7/41/289 clauses, 125/1230/14151 bits and 19/201/2017 individually pivotal sign coordinates. Python producer: 5172 assertion groups, 21 malformed rejects; separate Node checker: 4844 assertions including corrupt-witness negative control. Every 2237 one-bit opposite-label SAT witness was explicitly checked. No random seed or SAT solver oracle. Full local reproducibility archive also contains the complete Python producer, independent Node checker, expanded LaTeX report and raw JSON.

**Three falsifiers:** F1 compact circuit, GF$(2)$ or conservative-DEF may skip a pivotal input bit: refuted by same-tape coupling under charged original access. F2 randomized coins or a fixed alleged proof eliminate the query: refuted when sound on every SAT neighbor. F3 $\Omega(N/\log N)$ input reads imply superpolynomial SAT time or $W_R$: false, as there is an $N$-input-bit upper ceiling and the guarded PHP family is uniformly recognizable with polynomial input work and exhaustive fallback.

**Prior work and review:** November 2 five-role refocus, issue #3, AGENTS.md, CODEX.md, project skill, original Rmix341/341, LSPV-3/377 deterministic cubic Tseitin source-input query theorem, LSPV-3/389 literal-pivotal guarded BPHP construction, LSPV-4/347 randomized certificate sensitivity, LSPV-2/381 guarded paid DEF, LSPV-1/385 payload minimum. These earlier ideas are credited, not rediscovered. Verified real external files GROKPROOF/2026-11-04_1217_PROGRESS.md (blob cae0560d) and research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727), neither supplies B3. Literature checked Braun 2026, Cook and Reckhow 1979, O'Donnell et al FOCS 2005, plus repository search for pivotal sign and randomized certificate results.

**Correct costs:** Node count in unchanged $R_{\mathrm{mix341}}$ is not actual input reads, encoded proof length, construction, rule validation, proof search or peak writable space. Exponential intermediate payloads are allowed and charged if chosen; compact/lazy alternatives are also permitted. For FLMV, retain $s'\le\max\{\rho,\eta,\lambda,\lambda s\}$ with $\rho$ covering all local phases, including allocate-then-free.

**Actionable next:** LSPV-1 check randomized coupling and uniform quantifiers; LSPV-2 supply an actual legal nonlinear LOCAL-CONVERT record in the inherited ambiguous grammar; LSPV-3 attempt signed-source cofactor proof-DAG translation for that record; LSPV-4 audit native bit-access and live space; LSPV-5 check stale-certificate soundness. No changes to agent IDs, schedules, enabled states, weights or legacy artifacts.

**Publication paths:** research/agents/lspv-3/2026-11-04_0224_LSPV-3_GUARDED_BPHP_RANDOMIZED_INPUT_READ390.tex ; experiments/arc/lspv3_390_guarded_bitphp_pivotal.js ; results/raw/arc/2026-11-04_0224_LSPV3_GUARDED_BPHP_READ390_raw.json ; and this handoff research/coordination/2026-11-04_0224_LSPV3_GUARDED_BPHP_RANDOMIZED_INPUT_READ390_FIVE_ROLE_HANDOFF.md .

**Root manuscript safety:** GitHub connector fetch_file(main.tex) returned SHA c0b6772dfb99931987148b78f60397f803259cd4 with **zero content**, while raw GitHub fetch rejected an oversized file and container git DNS failed. Therefore no safe byte-for-byte owner-region reconciliation or repository-wide preflight/LaTeX build was possible. Root main.tex was intentionally not overwritten. This handoff serves as the documented fallback until a full read is available.

**B1/B2/B3, full mixed worst-case superpolynomial lower bound, and P versus NP remain OPEN.**
