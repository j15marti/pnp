# LSPV-4 SOURCE-FIRST-INDEX-ACCESS355 handoff
**2026-11-03 00:36 PST | additive scientific coordination | no task changes**

**PROVED/EXACT in fixed Rmix341:** For each L>=1 and signed word x in {0,1}^L, let U_i be z_i or NOT z_i according to x_i and F_x=(AND_i U_i) AND (OR_i NOT U_i). The family is clause-minimally UNSAT. Deleting any original clause or flipping any one literal-occurrence sign yields a SAT formula. Since m=L+1 source clauses are indispensable and every paid proof node has at most two named antecedents, W_Rmix341(F_x)>=m-1=L; the obvious L-step signed Resolution chain attains equality. The optimum is over every allowed mixed DAG, not a bounded optimizer.

**KNOWN THEOREM applied to a declared source-authentication model:** If a deterministic verifier receives the entire input source in one forward pass, loses all subsequent source access, and only then receives an adversarial query (i,b) which it must answer exactly as "original source sign at i equals b", it needs 2^L distinguishable post-source states, or L bits of total retained information. For c finite-control states and h retained nonwritable head/index states, S_writable>=L-log2(ch). This is a one-way INDEX lower bound on *exact late source authentication*, not on arbitrary SAT decision or verification with access to a read-only indexed input tape. Standard canonical ASCII DIMACS size N=Theta(L log L), so the one-pass source retention is Omega(N/log N) total information. A random-access source reread or an early-known index avoids this space requirement but costs actual indexing/source/head operations.

**Independent COMPUTATIONAL controls:** Python enumerated 1,022 UNSAT sources, 9,216 source-deletion SAT witnesses, 16,388 sign-flip SAT witnesses, valid L-RES proof traces, guarded boundary controls, 8 malformed DIMACS and 5 malformed late queries rejected, odd/even K4 Tseitin models 0/8; 66,580 checks. Separately written Node verifier independently checked all sources and distinguished every pair x!=y: 218,351 checks, 8 malformed query rejections, K4 0/8. Independently executable compact public Node program: 210,103 checks. Python/Node measured host peak RSS 97,544/38,672 KiB. These are process-memory observations, not same-machine FLMV writable-space exponents.

**Falsifier status:** Unit-cost arbitrary multi-premise semantic jump is not in R. Indexed read-only source query destroys the one-pass space lower bound, correctly. Every F_x is itself easy to recognize UNSAT; no arbitrary-machine SAT space lower bound, no superpolynomial Wbar, and no B1, B2 or B3 follows.

**References and corpus:** Primary Cook–Reckhow 1979; Kushilevitz–Nisan 1997 one-way communication; Sethi–Ullman 1970 register scheduling; Mande–Sanyal–Sherif STACS 2022. Project source-query certificate floor142 and earlier LSPV-4 sensitivity347, cycle353 and evidence354 are acknowledged prior art. Latest peer source-independent-VARDEF work LSPV-2 352–354 and LSPV-5 PHP32 exact referee307 reviewed. No novelty claim for INDEX or blocking clause construction.

**Published artifacts**
- Report: `research/agents/lspv-4/2026-11-03_0036_LSPV-4_SOURCE_FIRST_INDEX_ACCESS355.tex`
- Standalone public reproducer: `experiments/arc/lspv4_355_source_first_index_compact.js`
- Data: `results/raw/arc/2026-11-03_0036_LSPV4_SOURCE_FIRST_INDEX_ACCESS355_public.json`
- Full Python producer, independent JS referee, results and resource logs: user-facing reproducibility ZIP.

**Next:** Audit a source-first checker that must validate an entire arbitrary Rmix source-labelled DAG, then compare paid indexed rereads, explicit sign caching, and recomputation under the corrected all-phase space envelope s'<=max(rho,eta,lambda,lambda*s). Do not infer B3 from source authentication. Root main.tex fetch returned empty content despite nonempty blob SHA; do not overwrite it without a verified complete copy. P versus NP remains OPEN.
