# LSPV-1/446: Exact global mixed-DAG minimum for componentwise charge-chain 3-CNF

**2026-11-06, 04:28 PST. Route B. PROVED/RESTRICTED.** Exact theorem for the separately encoded easy targets of the previously published LSPV-1/444 syntactic reduction, not a superpolynomial mixed proof lower bound or an arbitrary-machine SAT lower bound. The historical R_mix341 rule-level semantics from LSPV-2/341 are used, pending acceptance by its authoritative byte checker.

## IDEA -> SEARCH -> ITERATE

**Hypothesis:** /444's $5k+2$ strict Resolution upper witness is the *global* shared-DAG minimum across every legal mixed rule for an odd component with $k$ charge inputs. For disconnected targets, global work equals that of the smallest odd component.

Four falsifiers: (F1) deleting a force-pad source clause leaves an odd component UNSAT; (F2) deleting the uniquely active XOR-gate clause leaves it UNSAT; (F3) a mixed/cross-component refutation can use a source subset missing at least one core clause in each odd component; (F4) a purported upper proof contains an invalid oriented pivot or double-counts/omits an inference. All four fail in the specified model, by the constructive deletion and source-capacity proofs below. This does not authenticate possible *unrecorded* historical rules.

## Family, published hardness and encoding

Use the established signed cubic-expander Tseitin proper 3-CNF family: for cubic $G=(V,E)$ with $h$ vertices and $3h/2$ edges, each vertex contributes four signed width-three clauses forbidding the four wrong-parity local triples for $\bigoplus_{e\ni v}x_e=\chi_v$. The source has $4h$ clauses, $3h/2$ edge variables, and $\Theta(h\log(h+2))$ indexed encoding bits. Connected odd-charge inputs are UNSAT. Suitable expander instances have $2^{\Omega(h)}$ ordinary *shared-DAG Resolution* proof size by Urquhart (1987) and Ben-Sasson/Wigderson (2001). The original bridgeless family nevertheless has a $4h-1$-node mixed AND3/GF(2) refutation under declared /341; therefore the Resolution lower bound does not transfer to the full mixed calculus. Haken PHP versus Cook ER remains a second mandatory shortcut control.

Reuse the existing /444 syntactic 3-CNF charge-chain *target* transformation. Each connected component $C_j$ of size $k_j\ge2$ gets charge inputs $c_i$ forced to $\chi_i$, $k_j-1$ binary XOR gates in a prefix chain, and a forced zero final output. Encode each XOR gate by its four proper ternary wrong-output clauses. Encode each forced literal $\ell$ using two fresh private bits $p,q$ and the four clauses

$$
(\ell\vee p^s\vee q^t),\qquad (s,t)\in\{0,1\}^2.
$$

Each target component $H_j$ has exactly $8k_j$ original proper width-three clauses and $4k_j+1$ variables. The disjoint target $H=\bigwedge_jH_j$ has $8h$ clauses and $4h+c$ variables for $c$ graph components. /444 already proved SAT equivalence, polynomial-time forward/reverse *satisfying witness* maps, and a strict-Resolution upper bound $5k_j+2$ when component $j$ has odd total charge. Those positive-witness maps are vacuous on UNSAT sources and do not transport Resolution hardness.

## Theorem 446.1: Exact free-choice mixed minimum

Let $R$ be any sound, source-explicit fixed refutation calculus with all inference and conservative definition nodes unit paid, at most **two** antecedents per node, no free semantic oracle/constraint-generating definition, and containing ordinary binary Resolution. Minimize over entire legal source-authenticated acyclic branching/shared DAGs, all AND obligations, all possible OR alternatives, permitted algebraic shortcuts, paid definitions, and optimal reconvergence; count distinct paid nodes once. The declared historical /341 grammar satisfies these mathematical hypotheses (accepted-byte checker qualification remains separate).

Write $\varepsilon_j=\bigoplus_{v\in C_j}\chi_v$. If all $\varepsilon_j=0$, $H$ is SAT. Otherwise the exact global minimum is

$$
\boxed{W_R(H)=\min_{j:\varepsilon_j=1}(5k_j+2).}
$$

### Lower bound, valid across every legal mixed rule

Fix an odd component $C$ with $k$ inputs and evaluate the XOR chain at its forced charge values. Select $E_C$: all four original source clauses for each of the $k$ input pads and the one final output pad, plus **the one active source clause at each of the $k-1$ XOR gates** that forbids the incorrect output under its correct input values. Thus

$$
|E_C|=4(k+1)+(k-1)=5k+3.
$$

Every $D\in E_C$ is indispensable **in the full $8k$-clause original component**, by explicit SAT deletion witnesses:

1. Delete an input-pad facet: flip that input charge, recompute every XOR gate correctly (odd parity changes to zero), and set the two private pad bits to falsify *only* the removed facet.
2. Delete a final-output-pad facet: keep all original inputs and correct gates (output parity one), and set the final private pad bits to falsify *only* the removed facet.
3. Delete the active clause of gate $i$: keep all input charges, flip gate $i$'s output, recompute subsequent gates correctly (final output becomes zero). Only the removed gate clause is violated, all other original clauses hold.

The strict RES construction below uses exactly these $E_C$ source clauses and hence $E_C$ is a minimally UNSAT core.

For any alleged refutation of $H$, collect all its *original source clause ancestors* in $S$. If for every odd component $C_j$ the set $S$ omits some $D_j\in E_{C_j}$, choose the above SAT deletion witness in each odd component, any model in each even component, and combine them over disjoint variables. The resulting assignment satisfies every clause in $S$. Conservative definitions extend without restricting old assignments, contradicting soundness of the root $\bot$. Hence at least one odd component contributes all $5k_j+3$ indispensable ancestors.

The connected ancestry hyper-DAG has $e$ source leaves and $q$ paid inference/definition nodes. Connectedness gives at least $e+q-1$ dependency edges, while indegree at most two bounds edges by $2q$. Hence $q\ge e-1\ge\min_{\varepsilon_j=1}(5k_j+2)$. Cross-component reasoning, sharing and reconvergence cannot evade this lower bound. No heuristic discovery cost is assumed in the ideal optimum.

### Matching original-source strict Resolution proof

Choose an odd component with smallest $k$. Resolve each input's four signed pad clauses into its unit literal in **three** inferences ($3k$). For each of $k-1$ XOR gates, resolve the one active source gate clause with its two already derived input units in **two** inferences ($2k-2$). Resolve the output pad into a negative unit in **three** steps, then resolve the positive and negative final units once. Exactly

$$
3k+2(k-1)+3+1=\boxed{5k+2}
$$

distinct paid RES nodes. Each has correctly oriented complementary literals and original source ancestry. No split, weakening, GF(2) jump, LOCAL-CONVERT, DEF, or cross-context reuse is needed. Lower and upper agree.

## Work, span, computational evidence and safeguards

Ideal paid work is $5k+2$. The exhibited sequential XOR chain has **parallel span at most $2k+2$** under an explicitly unlimited-processor unit-node model, not a proved global minimum span. Input and printed proof use $O(k\log(k+2))$ explicit index bits; all $5k+3$ full deletion assignments stored together take $O(k^2)$ bits. Actual algorithm time and all-phase peak space additionally charge input and head reads, parsing, motif/graph identification, all candidate choices and failed paths, cache/references, clause writes, verification and recomputation. FLMV materialized-child space must still satisfy $s'\le\max\{\rho,\eta,\lambda,\lambda s\}$ with every local phase charged in $\rho$.

**Python producer:** 18 single-component packets (12 UNSAT), 346 full-source clause-deletion models, 334 replayed Resolution nodes, plus 1,075 simultaneous-deletion disjoint-product tests. **Independent Node verifier:** 60 packets, 30 UNSAT source proof traces (700 Resolution nodes), 730 full-source deletion witnesses, 12 small exhaustively enumerated target counts, 4,762 assertions, four corrupted-certificate classes rejected in every UNSAT case. Independently reconstructs signed original K4 Tseitin odd/even formulas (16 clauses, respectively 0 and 8 satisfying models). Observed Python time 6.37s / 97,168 KiB maximum RSS; Node 0.04s / 31,216 KiB maximum RSS. These observations are not same-machine exponent bounds. No authoritative R_mix341 byte checker executed.

**Research reviewed:** Five-role handoff historical commit 4e29ed7646f4, live issue #3, AGENTS.md, CODEX.md and pnp-research skill; LSPV-2/341 historical exact grammar blob c87acd11; LSPV-1/444 blob 6fe33de; LSPV-5/REFEREE384 report blob 231a0ca; Grok report blob 6b32bc3; actual Claude ONETAPE report blob 9a5b05d. New mandatory repos: konard/p-vs-np/scripts/proof_status.json blob 93b77ed3 and blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea. Relevant controls: meelgroup/frat-xor/format.md blob 986a21aa, peitl/short-proof/README.md blob 93d2090d, openai/math concrete Lean SAT-node-cost file blob 1ced21f4. Indexed web literature searched; standalone Google branded interface not used. No repo CI badge or source-status manifest is treated as a mathematical proof.

**Primary sources:** Urquhart, JACM 34 (1987) 209-219, DOI 10.1145/7531.8928; Ben-Sasson & Wigderson, JACM 48 (2001) 149-169, DOI 10.1145/375827.375835; Haken, TCS 39 (1985); Cook, SIGACT News 1976; Cook & Reckhow, JSL 44 (1979). The binary-source capacity method is reused from project LSPV-2/341.

**OPEN:** A superpolynomial $\overline W_{R_{mix341}}$ lower bound surviving *all* legal mixed shortcuts on a hard family; historical accepted-byte authentication; and the NONCIRCULAR same-fixed-calculus B3

$$
\mathrm{SAT}\in P\quad\Longrightarrow\quad\overline W_{R_{mix341}}(N)=N^{O(1)}.
$$

B1 and B2 also OPEN. This result upgrades the already known *easy target* upper witness /444 to an exact optimum and strengthens the disjoint-component lower-bound accounting, but does not transport original hard-family proof lower bounds. **P versus NP OPEN.**