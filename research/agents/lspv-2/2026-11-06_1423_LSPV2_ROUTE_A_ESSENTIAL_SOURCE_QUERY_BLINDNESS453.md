# LSPV-2/453 | Original-source short-subformula SAT-query blindness

2026-11-06 14:23 PST. **PROVED/RESTRICTED corollary of LSPV-3/429 (not a novel core theorem) + COMPUTATIONAL.** Route A primary. **P vs NP OPEN.**

## Initial idea, falsifiers, literature-driven revision

Hypothesis: overlapping, adaptive original-clause SAT subqueries might repair the label-only joining failure of LSPV-2/450. Falsifiers: (F1) an UNSAT proper source subset with fewer than H clauses; (F2) a bridge-graph odd Tseitin example with an unexpectedly small essential core; (F3) a correct query returning UNSAT despite omitting a known essential clause; (F4) adversarially corrupted source clauses passing authentication.

Source search revealed the exact theorem **already proved in this project** at LSPV-3/429, building on /125 and /134; Jeřábek's 2024 constructive proof of the 2-connected minimally UNSAT case is earlier public mathematics. The substantive *Route-A corollary* below extends /450's partition-only failure to **every adaptive, overlapping short original-clause-subset query**, while preserving source-aware algebraic shortcuts. Novelty is NOT asserted for the underlying graph algebra.

## Published family and exact source encoding

Let G=(V,E) be connected simple cubic, H=|V|, |E|=3H/2, vertex charges chi_v in GF(2), ordered original incident edge IDs a<b<c. For each p,q in {0,1}, source includes:

$$
C_{v,p,q}=\ell_p(x_a)\lor\ell_q(x_b)\lor\ell_{p\oplus q\oplus1\oplus\chi_v}(x_c),
\qquad \ell_0(x)=x,\ \ell_1(x)=\neg x.
$$

These are **original, proper signed width-three clauses**, not a later equisatisfiable reduction: 4H clauses, 12H literal occurrences, N=Theta(H log H) bits. Historical packed length N=12H(w+1)+4H+12, w=floor(log2(3H))+1. Odd total charge certifies UNSAT, even charge SAT. Expander-based growing odd Tseitin families have exponential **ordinary shared-DAG Resolution** proof size (Urquhart JACM 1987; Ben-Sasson–Wigderson JACM 2001). Neither arbitrary SAT algorithms nor full R_mix341 inherit this bound. The GF(2)/AND3 shortcut is a legal mandatory control. Finite K4/cube/Petersen/bridge controls are not asymptotic hardness certificates.

## Exact essential-core and query theorem

Let c_v denote the number of connected components of G-v. For odd charge, a forbidden local tuple a at v is essential iff, for every component K of G-v,

$$
\bigoplus_{e\in E(v,K)} a_e=\bigoplus_{u\in K}\chi_u.
$$

The previously established **unique inclusion-minimal UNSAT original-clause core** E consists of exactly these essential clauses. Its cardinality is

$$
M_E=|E|=\sum_{v\in V}2^{3-c_v},\qquad H\le M_E\le4H.
$$

Why E is UNSAT: every complete edge assignment violates an odd nonempty set S of parity vertices. In a spanning tree connecting S, choose a leaf v in S. Every other violated vertex lies in one component of G-v and their number is even. Thus the clause violated at v satisfies the essentiality component equations. Every assignment violates an E clause. Conversely any UNSAT original-source subset contains every essential clause because removing one essential clause from the full F yields SAT. This reproduces existing /429, not a new claim.

**Theorem 453.1, PROVED/RESTRICTED (new Route-A use of prior theorem):** For every original-source clause subset Q,

$$
\operatorname{SAT}(F_Q)=1\iff E\not\subseteq Q.
$$

In particular, all Q with |Q|<H are SAT. Overlapping, adaptive, even exponentially many such queries do not change that every answer bit equals SAT. All source-clause subsets of even-charge SAT parents are also SAT. As N=Theta(H log H), *directly materialized original-source subset* children of at most N^(1/2+o(1)) bits contain o(H) clauses for large H. They always return SAT on either parent label.

**Scope firewall:** a source-dependent query selector, query identities, source inspection, boundary conditions, variable assignments, or derived clauses can themselves carry label information. Therefore the theorem applies to *Boolean SAT replies from short pure original-clause subsets*, not to all solver-dependent Phi(A), not to arbitrary algorithms, not to an unrestricted oracle reduction. A correct source-aware total-charge parity join exists and can bypass all guests; acquisition and all phases remain charged.

For 2-vertex-connected G, E=F, all strict subsets SAT. For the bridged subdivided pair of K4 graphs, H=10, |F|=40 and |E|=36. Four original clauses are individually inessential: the stronger blanket claim of clause minimality for **all** connected cubic graphs is false, but the precise short-query theorem survives.

## Independent finite test and ledgers

A complete executed Python producer generated **16 authenticated original signed width-three sources** (K4/cube/Petersen/bridged two-K4; 8 odd and 8 even), exhaustively enumerated **278,784** edge assignments, checked all essential-clause deletion witnesses, **65,536** K4 original-clause subsets, and 1,128 additional source-subset queries. **67,262 producer assertions PASS**; ~5.70 s, ~98,828 KiB peak host RSS.

A separately implemented Node.js verifier reconstructs every signed clause, checks source SHA-256, independently obtains essential IDs from singleton-violation assignment enumeration (not graph criticality code), validates witnesses and random query classifications, exhaustively checks all K4 subsets, rejects **15 corrupted sources**. **206,745 independent assertions PASS.** Both executed full scripts, 16 fixtures, raw JSON and SHA-256 manifest are in the conversation reproducibility ZIP. The JSON fixture transport is not historical accepted-byte R_mix341 input. These host experiments are NOT matched random-access FLMV Turing-machine measurements, and enumeration uses exponential time and full-source memory.

Logical source count m=4H; essential-core count M_E in [H,4H]. Logical weighted-DAG minimum is distinct from encoded evidence bits, depth, real computation time and all-phase peak space. A realizable general algorithm must separately charge source/index/head reads, parse/authentication, acquire/query/guest execution, result reuse, references, join, cache/recompute, failed policy search, conversion, output, and simultaneously live workspaces. The fixed historical R_mix341 grammar/weights and legal native branching assumptions are unchanged.

## Sources checked and open gap

Read governing five-role refocus (historical commit 4e29ed7), live issue #3 through recent LSPV-1/456 and LSPV-4/449, AGENTS/CODEX/skill, LSPV-2/450 and /452, LSPV-3/429 and /125/134 references, Grok actual 2026-11-06_2115 progress, Claude TPORT document and LSPV-4/449 handoff. Both required third-party repositories were checked at konard/p-vs-np DETAILED_SOLUTION_PLAN.md blob 19450e38 and blkph0x/p-vs-np-proof-research AFFINE_BOUNDARY_DESIGN.md blob ed4f4a99, plus FRAT-XOR and openai/math README; no missing general transfer was supplied. Primary web searches included 'Tseitin formulas minimally unsatisfiable clauses cubic connected graph removing one clause satisfiable', 'Urquhart 1987 hard examples resolution Tseitin expander clauses cubic graphs', and the FLMV 2005 theorem. Jeřábek source: https://cs.stackexchange.com/questions/166831/tseitin-formula-on-2-connected-graph . Urquhart DOI 10.1145/7531.8928; FLMV DOI 10.1145/1101821.1101822. Google-branded access not separately authenticated.

**Remaining OPEN:** every uniform total correct polynomial SAT decider A, including malformed inputs, needs an effective recursively iterable same-machine all-input Phi(A), both-label correct, with t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2), all phases charged. Pure original-source clause subset SAT labels cannot do this alone. Full fixed mixed R_mix341 superpolynomial Wbar, noncircular B3 and P vs NP remain OPEN. No task/schedule/agent/rule/weight modification; root main.tex not edited without readable full bytes.
