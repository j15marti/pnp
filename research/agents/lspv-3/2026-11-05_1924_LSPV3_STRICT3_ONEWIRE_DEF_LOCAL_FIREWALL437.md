# LSPV-3/437: Strict3 original-source one-wire DEF/LOCAL firewall

**November 5, 2026, 19:24 PST. Route B.** PROVED/EXACT elementary reduction, COMPUTATIONAL 256-case replay, PROVED/RESTRICTED conditional FACET-A clause derivation. Historical native R_mix341 byte grammar, full mixed hardness, B3 and P versus NP OPEN.

## IDEA -> SEARCH -> ITERATE

**Hypothesis:** a supposed LOCAL-CONVERT that concludes a one-wire clause using all original source models might hide a coNP-complete global entailment test. **Four falsifiers:** guarded strict-3 source fails to remain SAT; projected gate outputs fail to distinguish base SAT from UNSAT; local gate relation alone implies the proposed output; a proposed source-checked paid derivation requires wrong pivots or forged facets.

Read governing five-role handoff at historical commit 4e29ed7646f484707767acb6e63ec5f38afd98a8, current issue #3, historical R_mix341 source research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex at blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb, LSPV-3/436, LSPV-5/375, LSPV-1/432 handoff, AGENTS.md, CODEX.md, pnp-research skill, actual GROKPROOF/2026-11-06_0215_PROGRESS.md and research/agents/claude/tport/README.md. Also inspected konard/p-vs-np/proofs/complexity/README.md at blob 7ee9a11e and proofs/experiments/README.md at 4c8752aa; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md at 18d693ea and RESIDUAL_EQUIVALENCE_BARRIER_REPORT.md at 46413596; meelgroup/frat-xor/format.md at 986a21aa; tanyongkiam/cake_lpr/README.md at e94f45e9; openai/math/README.md at cc5b0a03; Braun preprint README at kbr-/math-research blob a21e7e4a. Indexed research and GitHub searches were used; Google-branded search unavailable and container git DNS unavailable.

**Search changed the claim:** historical /341 explicitly restricts LOCAL-CONVERT to ONE already derived constant-original-support factor, not the global source. Thus the proposed semantic one-step rule is **not legal**. LSPV-3/382 already proved semantic-circuit-support coNP-completeness; LSPV-1/422 already gave a distinct one-public-bit global projection gadget; REFEREE330 already distinguished guarded entailment from SAT decision. No novelty over those results is claimed. The increment is a strict3 original-source + one separately paid DEF specific control and an independently replayed source-attached paid derivation under an explicitly **proposed** facet grammar.

## Precise strictly-3CNF reduction and proof

For any valid CNF G(y) of clause width at most 3, construct H_G on original source variables y,s,t plus fresh per-clause splitter/padding variables. Guard every clause C by (NOT s OR C). For a proper 3-clause (a OR b OR c), represent its guarded width-4 clause by (NOT s OR a OR w) AND (NOT w OR b OR c) using fresh w. For width 2, use (NOT s OR a OR b); for width 1, conjoin both (NOT s OR a OR p) and (NOT s OR a OR NOT p); for empty clauses pad the unit NOT s by four signed triples. For t=1 conjoin the four signed three-literal padding clauses (t OR +/-p OR +/-q), using two fresh names. Remove tautologies, duplicate literals and repeated-variable source clauses by sound normalization. Every emitted source clause has exactly three **distinct** signed variable occurrences, and existential projection exactly satisfies

$$
\exists\,\mathrm{padding}\ H_G(y,s,t,\mathrm{padding})\ \equiv\ t \land(\neg s\lor G(y)).
$$

H_G is always SAT via s=0,t=1. One **paid, fresh, conservative** DEF z=s AND t extends every source assignment uniquely. Its feasible output values are exactly

$$
\operatorname{Proj}_z(H_G\land \mathrm{DEF}_z)=
\begin{cases}
\{0,1\}, & G\in \mathrm{SAT},\\
\{0\}, & G\in \mathrm{UNSAT}.
\end{cases}
$$

Consequently source-relative entailment H_G AND DEF_z entails NOT z is coNP-complete, even when the original source is SAT strict3 and only one paid gate exists. The complement has a polynomial witness: an original source assignment plus its uniquely evaluated z=1; 3UNSAT reduces uniformly with polynomial source encoding. However **the gate's own 3-wire truth table does not imply NOT z**, as (s,t,z)=(1,1,1) satisfies the DEF. A LOCAL step reading the entire original source or implicitly checking this hard entailment would be an unlicensed rule; historical native LOCAL is one antecedent with bounded original support, so this is a proposed-extension obstruction, NOT a historical accepted refutation or machine lower bound.

## Source-authenticated proof-carrying control

Use G=(y1) AND (NOT y1), yet H_G is SAT. Original literal names y1=1,y2=2,s=3,t=4,pads 5,6,7,8, and one paid auxiliary z=9=s AND t. Exact DIMACS (the SHA256 of these actual ASCII bytes is 060c990f6b2e89326901cd2aee51f138d1fba293523a16c85c712bff071fda0b):

    p cnf 8 8
    4 5 6 0
    4 5 -6 0
    4 -5 6 0
    4 -5 -6 0
    -3 1 7 0
    -3 1 -7 0
    -3 -1 8 0
    -3 -1 -8 0

With **declared FACET-A**, and only IF its owner-qualified defining clauses are legal Resolution antecedents, the following four paid RES steps derive NOT z from original authenticated sources plus a **fifth paid DEF**: resolve source clauses 4/5 on variable 7 to obtain (NOT s OR y1); resolve clauses 6/7 on variable 8 to obtain (NOT s OR NOT y1); resolve these on variable 1 to obtain NOT s; resolve with charged DEF facet (NOT z OR s) on variable 3 to obtain NOT z. This is a derived implied unit on a satisfiable formula, not an UNSAT refutation or proof of any global W_R minimum. It requires no free case split, free weakening, forged proof premise or semantic oracle. Under the separate declared GATE-B+LOCAL completion, LSPV-5/375 already gives a paid LOCAL materialization of the same facet, raising this certificate to 6 paid nodes **conditional on full gate export**. Historical acceptance remains OPEN.

## Reproducibility and paid/physical resource distinctions

Python full producer and independent Node checker: all 256 subsets of eight unary/binary clauses on two variables, **95 base SAT, 161 base UNSAT**, yet all 256 H_G sources SAT. Original source assignments checked 82,944; each output projection matches base SAT status. Full raw file: **72,604 bytes**, SHA256 f5162ef7aec4c474812239d38459b457fe268a9623c6ef61ee702800dcafab19, binding every per-formula hash to **exact ASCII DIMACS** rather than to JSON metadata (corrects LSPV-5/375's source-hash critique of /436). Independently authored verifier: **4,071** assertions, seven malformed/semantic negative controls and four additional corrupted conditional-certificate rejections. Focused certificate: 1,459 explicit JSON bytes, five charged nodes (1 DEF, 4 RES). A separate standalone JS reproducer rechecks all 256 projections and the five-node certificate. None ran a historical authoritative R_mix341 parser, and no finite optimum was inferred.

For n original variables and m clauses, strict3 source generation uses O(n+m) names/clauses, O((n+m) log(n+m)) explicit indexed bits beyond the original literal data, with polynomial parsing, construction, output and proof checking. The exhaustive enumerator, source/hash/index reads, malformed controls, witness acquisition, intermediate encodings, proof output and caches are actual physical work not included in the free after-the-fact minimum W_R. Share a DAG node once in W_R, but count reference/lookup, retention and recomputation separately for machine time and peak space. No native time-space exponent or FLMV contraction follows.

## Established family/theorem/model/encoding/shortcut ledger

| Family | Exact encoding and published restricted lower bound | Legal shortcut and transfer gap |
| --- | --- | --- |
| Bridgeless cubic odd Tseitin on suitable h-vertex expander | n=3h/2 edge bits, 4h exact three-literal clauses, binary-index N=Theta(h log h); Urquhart 1987 and Ben-Sasson/Wigderson 2001 give exponential shared-DAG **ordinary Resolution** length for appropriate expanders. | Historical /341 proves exact **mixed** W=4h-1 through AND3 and GF(2). Not a full mixed hard family. |
| Unary PHP(h+1,h) | h(h+1) variables; h+1 pigeon clauses and h*binom(h+1,2) binary collision clauses, N=Theta(h^3 log h). Haken 1985 exponential unrestricted DAG ordinary Resolution. Some clauses width h, NOT proper strict3. | Cook 1976 polynomial Extended Resolution. Paid native DEF+RES shortcut established in earlier project; converting to 3CNF needs a proof-size-reflecting direction. |
| Original bit PHP with n=2^ell holes | (n+1)ell bits; n*binom(n+1,2) signed width-2ell collision clauses. Braun 2026 **preprint** claims DAG Res(XOR) length > exp(n/(32768 ell^2)) for ell>=32, separately Lean-reported. NOT strict3. | Earlier project /346 and /369 established polynomial mixed DEF proof and conditional backtranslation obstruction; no hard family for all mixed rules. |
| Sparse graph PHP expander (de Rezende/Nordström/Risse/Sokolov, CCC 2020) | One bit per permitted graph edge, pigeon disjunctions, binary hole collisions; exponential ordinary Resolution on specified sparse expanders. Degree <=3 not assumed without checking graph construction. | Frege/ER upper controls; native paid facet/export authentication open. Strict3 clause conversion must preserve lower bounds, not just SAT status. |
| This run's H_G | Proper strict3 original source SAT for every G; one paid gate. Only global one-wire entailment coNP complete. | Negative interface test, NOT a candidate UNSAT-hard family. |

Primary sources: Haken, The Intractability of Resolution, TCS 39 (1985), DOI 10.1016/0304-3975(85)90144-6; Cook, A Short Proof of the Pigeon Hole Principle Using Extended Resolution, SIGACT News 8(4) (1976); Urquhart, Hard Examples for Resolution, JACM 34(1) (1987); Ben-Sasson and Wigderson, Short Proofs Are Narrow, JACM 48(2) (2001); de Rezende et al., CCC 2020 DOI 10.4230/LIPIcs.CCC.2020.28; Braun, arXiv:2609.23015, September 2026 preprint. Proof-model and status qualifiers are essential.

**Next exact obligation:** authenticate the historical original byte grammar for DEF facet selectors, whole-gate LOCAL parent/output type, private/exported wires and globally fresh ports; then seek an original-source-retracting polynomial proof-to-proof translation over arbitrary nested/shared legal DAGs, or a genuinely legal typed obstruction. Noncircular B3, superpolynomial Wbar_R over ALL fixed mixed rules and P versus NP are OPEN. Root main.tex unchanged: full contents not safely readable for outside-byte-preserving ownership patch. All five task identities/schedules/states, weights and ownership unchanged.
