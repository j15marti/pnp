# LSPV-2/451 | Opaque guest-work barrier despite virtual SAT-child ports

**2026-11-06 12:12 PST. PROVED/RESTRICTED, conditional on SAT in P; COMPUTATIONAL controls. P versus NP OPEN.**

## IDEA, falsifiers, model

Hypothesis: virtual indexed child ports avoid explicit child serialization but cannot erase mandatory actual guest transitions when a compiler faithfully executes an unchanged polynomial SAT decider on every UP-open residual. Falsifiers: F1 fewer than $2^{k/3}$ UP-open branches; F2 sublinear native original-ID residual lengths after only $k=O(\log N)$ decisions; F3 cached input removes guest transitions; F4 legal source or white-box shortcuts avoid the invocations. Prior proved LSPV-4/446-447 and current independent tests eliminate F1/F2 for this specific model. F3 is excluded by the definition of faithful execution, not by any universal computation lower bound. F4 succeeds outside the model, and is expressly allowed.

## Exact known family and hardness qualification

Use a connected simple cubic graph $G=(V,E)$ with $H$ vertices, $3H/2$ original edge variables, and charges $\chi_v$. At vertex $v$ with incident edge IDs $a<b<c$, encode each of the four forbidden triples as the proper signed 3-CNF clause

$$
C_{v,p,q}=\ell_p(x_a)\vee\ell_q(x_b)\vee\ell_{p\oplus q\oplus1\oplus\chi_v}(x_c),
\quad \ell_0(x)=x,\quad \ell_1(x)=\neg x.
$$

There are $4H$ original clauses and $12H$ literal occurrences. The declared original-ID fixed-width packet has $w=\lceil\log_2(3H/2+1)\rceil$ ID bits and $N=12H(w+1)+4H+12=\Theta(H\log H)$ total bits. Connected-source SAT iff $\oplus_v\chi_v=0$. Growing odd-charge cubic expander families satisfying published graph-expansion assumptions have exponential **ordinary shared-DAG Resolution** lower bounds (Urquhart 1987, Ben-Sasson–Wigderson 2001). This establishes nothing for all algorithms, ER, GF(2), or historical fixed mixed $R_{\mathrm{mix341}}$. An authenticated source XOR parity test is a valid efficient bypass. K4, cube, Petersen, 128-vertex prism are finite semantic controls, not certified hard expander instances.

## Restricted theorem

Assume SAT in P, and fix a total uniform same-machine polynomial SAT/UNSAT/malformed decider $A_0$ with time upper bound $O(m^c)$. For any integer $d>\max(c,2)$ define a correct padded decider $A_d$ that spends at least $m^d$ dummy transitions on every binary input of length $m$ and then runs $A_0$. Its time exponent is $d$ with logarithmic additional space.

Consider exactly a compiler which branches on $k=\lceil(3/5)\log_2N\rceil$ selected source edge variables, applies only original-clause unit propagation, and **faithfully executes the unchanged** $A_d$ on each UP-open child encoded as an ordinary original-ID residual. It may use virtual indexed input ports and share read-only original bytes, but cannot skip guest instructions or use an unproved compressed alternative.

Existing LSPV-4/447 proves the exact UP-open count $B=2^{k-r}\ge2^{k/3}$, with $r$ the number of residual tree components, for $k\le H/2$. LSPV-4/446 proves at most $2k$ further forced variables and at least $4(H-6k)$ literally unchanged original ternary clauses per UP-open child. Every such native ordinary child therefore has logical length $\Omega(N)$ for $k=o(H)$. Guest padding then forces

$$
\boxed{T_{\mathrm{guest}}(N)\ge\Omega(BN^d)=\Omega(N^{d+1/5}).}
$$

For $d\ge3$, this exceeds the conditional Route A time target exponent $\max(11/10,3/5+d/2)$ by $d/2-2/5>0$. The ordinary child logical length also violates $N^{1/2+o(1)}$, independently of whether input materialization occurs. **This is only a counterexample to this opaque call-all-UP-open architecture.** A white-box compiler may simplify away padding, use the source parity shortcut, or construct another sound child representation. The missing universal $A\mapsto\Phi(A)$ is not disproved.

## Independent finite verification and costs

A standard-library Python producer executed original signed-CNF UP and compared it to independent graph tree-component predictions: **3,217 assertions PASS**. A second standalone JavaScript implementation passed **88 independent assertions**. First-$k$ selections: K4 $(H,k,r,B)=(4,1,0,2)$, cube $(8,2,0,4)$, Petersen $(10,3,0,8)$, 128-vertex prism $(128,9,0,512)$. The prism source packet has 14,348 bits; each UP-open branch retains at least 12,320 unchanged original-ID bits and the summed one-scan logical input-read floor is 6,307,840. Star-selected edges produce $r=1$ with four open Petersen or 256 open prism branches for both charge parities. Host-executed small dummy-loop control took **21,632 iterations**; large $m^d$ costs are mathematical extrapolations, not executed TM traces. Malformed delimiters reject, while sign-mutated syntactically valid packets are not source authenticated.

Resource firewall: no claimed physical work-tape peak from virtual input length; padding uses $O(\log N)$ additional writable bits; guest transitions are charged separately from local preprocessing, indexing, source reads, failed policies, output, caches, retrieval, ancestors, joining and source/certificate authentication. No native mixed proof or B1/B2/B3 transfer, no inference-weight changes. The shared-DAG minimum still counts the union of legal nodes with assumption-scoped AND-case discharge; this guest-time theorem concerns a distinct algorithm model.

## Sources and continuity

Read governing five-role handoff (2026-11-02, SHA c3889a3e), current issue #3, AGENTS.md, CODEX.md, project skill, LSPV-2/450 SHA cb51b0a8, LSPV-4/446 SHA 01cc78db, LSPV-4/447 SHA 0a5189b6, LSPV-3/125 SHA 35eba48e; Grok actual 2026-11-06_1617_PROGRESS.md SHA b931933c; Claude TPORT-0001 SHA b7150bb9. The earlier LSPV-2/220 two-port profile reduction was checked to avoid duplicating it. External pinned sources inspected: konard/p-vs-np finite machine model SHA 7ee9a11e and status manifest SHA 93b77ed3; blkph0x/p-vs-np-proof-research method index SHA 18d693ea and fixed-width affine theorem SHA 4aba9d94; CNFgen Tseitin source SHA 4bb5fd19; FRAT-XOR README SHA 38a137bc; Cake LPR README SHA e94f45e9; ABC README SHA 88a9d1a3; openai/math README SHA cc5b0a03. Primary literature: Urquhart, JACM 34:209-219 (1987), DOI 10.1145/7531.8928; Ben-Sasson and Wigderson, JACM 48:149-169 (2001), DOI 10.1145/375827.375835; Fortnow, Lipton, van Melkebeek and Viglas, JACM 52:835-865 (2005), DOI 10.1145/1101821.1101822. No separate Google-branded search; indexed research literature was searched.

**Remaining OPEN:** a fully charged white-box solver-dependent all-input, both-label, malformed-aware, recursively iterable **same FLMV machine** transformation with truly $\le N^{1/2+o(1)}$ child inputs and legal joining. P versus NP OPEN.