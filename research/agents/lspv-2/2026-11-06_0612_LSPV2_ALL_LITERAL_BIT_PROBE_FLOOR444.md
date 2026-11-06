# LSPV-2/444 | Full literal-field bit-probe floor for source authentication
**2026-11-06 06:12 PST | Route A primary | PROVED/RESTRICTED and COMPUTATIONAL | P vs NP OPEN**

## IDEA -> SEARCH -> ITERATE

**Hypothesis (pre-search):** for the fixed original signed cubic-Tseitin 3-CNF binary format of LSPV-2/440, each literal sign **and identifier** bit must be queried by any exact deterministic member/nonmember recognizer, even on an indexed-input machine. Falsifiers: (1) a one-bit flip leaves a member; (2) a changed field is actually unobservable/not in the source; (3) the proof secretly restricts input to sequential streams; (4) the statement duplicates prior SAT-label or streaming bounds.

**Historical firewall:** Reading issue #3 disclosed that /441 already obtained canonical source-only graph/tree extraction in standard logspace, /442 extended it to unordered strict DIMACS, and /443 proved the sequential multipass source-membership equality tradeoff. /435 already gave a *SAT-label* one-charge-bit-per-vertex sensitivity result. None of those is a floor on **every** literal field in the fixed canonical member/nonmember language under indexed access. No novelty is claimed for the classical deterministic query adversary.

## Family and theorem ledger

**Family and source:** Fix a suitable growing cubic-expander $G_H$, with $H$ even vertices, $3H/2$ edges, one variable $x_e$ per edge, and charges $\chi_v\in\{0,1\}$. For each vertex, include the four distinct proper signed width-3 clauses falsified by assignments with parity opposite to $x_{e_1}\oplus x_{e_2}\oplus x_{e_3}=\chi_v$. Thus $4H$ original clauses, not a bespoke hardness family. Connected odd total charge is certified UNSAT; even total charge is SAT. Disconnected graphs require componentwise parity.

**Published hardness:** For suitable growing odd-charge cubic expanders, Urquhart 1987 gives exponential ordinary shared-DAG Resolution lower bounds; Ben-Sasson and Wigderson 2001 provide the resolution width-size framework. This is *not* a lower bound on unrestricted algorithms, Extended Resolution, GF(2), or the full fixed historical $R_{\mathrm{mix341}}$. The algebraic summation shortcut is always permitted as an upper-bound control.

**Exact source encoding:** Retain LSPV-2/440 original packet: 8 magic bits, unary $H$, unary $3H$, $4H$ canonical vertex-grouped triples with one sign bit plus $w=\lfloor\log_2(3H)\rfloor+1$ fixed-width identifier bits per literal, and two trailer bits. IDs are $3u+\operatorname{slot}_u(v)+1$ for the lesser endpoint $u$, a source-authenticated injective edge renaming. The exact binary packet length is

$$
N_H=12H(w+1)+4H+12=\Theta(H\log H).
$$

**Theorem 444.1, PROVED/RESTRICTED.** Every one of the $12H(w+1)$ literal-field bits is *pivotal* for exact membership in this original canonical packet language. Flipping one sign bit makes one of a vertex's four parity-forbidding clauses wrong; the remaining three retain the original charge. Flipping one ID bit makes exactly one clause differ in unsigned support from the other three, or renders the packet malformed (out-of-range/zero/repeated identifier). Therefore no single literal-field bit may be changed while remaining a member.

**Corollary 444.2, PROVED/RESTRICTED.** On *every* member $F$, every deterministic total exact-member/nonmember recognizer must inspect every literal-field bit:

$$
Q_{\mathrm{member}}(F)\ge 12H(w+1)
=N_H-(4H+12)=(1-O(1/\log H))N_H.
$$

Proof: if bit $i$ is unqueried on a member, flipping it yields a nonmember with the identical deterministic computation trace and acceptance, contradiction. The argument allows arbitrary adaptive indexed bit queries, unlimited memory, arbitrary precomputation based on the *fixed program* and multiple passes. It does not assume a one-pass streamer. In an input-bit observation machine this also implies $T\ge Q$ for exact source authentication. It is **not** a SAT decision lower bound, because a SAT decider need not authenticate this family explicitly.

## Computational attempt and red-team checks

A Python producer emitted 12 exact original packets from K4, cube, Petersen and disconnected K4+K4 (three charge vectors apiece). It flipped each of the $6,336$ literal-field positions separately, and every perturbed packet failed original-source membership: 5,136 were well-framed but outside-family, 1,200 malformed. It also rejected 36 header/length/trailer controls. A disconnected source with two odd components has globally even charge but is UNSAT. Brute force verified SAT labels on all 12 small packets. **Producer: 6,460 assertions; independently authored Node referee: 6,422 assertions.** Raw fixture JSON SHA-256: `86b6837d4caffe13e80b7a072f329aeefb4937dfd360fb3e6863868f6e209f18`. Full executed producer, referee, raw source packets, report and manifest are preserved in the LSPV-2/444 reproducibility ZIP. Host experiments are NOT native FLMV TM executions.

## Resources, prior art, external audit, and transfer

This lower bound charges *input-bit reads* regardless of available writable space and cannot by itself bound machine space. The actual host fixture producer, brute force and independent checker **materialize** full strings and have no asserted FLMV-space upper bound. Prior /441 and /442 provide standard $O(\log N)$-workspace membership algorithms with an unspecified polynomial time exponent; this result gives an independent near-$N$ read floor. It does not exclude the sought $N^{11/10}$ local-time envelope, which admits a complete original-source scan.

Read original project handoff Nov. 2, current issue #3 through /443, AGENTS.md, CODEX.md, research skill, LSPV-2/440, actual `GROKPROOF/2026-11-06_0920_PROGRESS.md` (blob `6b32bc3`) and `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (blob `1f9fc72`). External repository files authenticated: `konard/p-vs-np/proofs/complexity/README.md` blob `7ee9a11` (different finite one-tape machine); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693e`, `CERTIFIED_RESIDUAL_QUOTIENT_REPORT.md` blob `b37da20` (bounded certificate quotient); `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` blob `4bb5fd`; `meelgroup/frat-xor/format.md` blob `986a21`; `berkeley-abc/abc/README.md` blob `88a9d1`; `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` blob `1ced21` (fixed-driver cost proof, no universal solver transformation). Primary literature searched through publisher/author web sources; no Google-branded search, Reingold implementation, FLMV native execution, or authoritative mixed-checker replay claimed.

**Work/space/certificate separation:** no mixed derivation or certified minimum calculated. The proof is an indexed **source-membership query** lower bound, not a lower bound for UNSAT proof weight or circuit simulation. Actual upper bounds must charge parser/head/index writes and erasure, guest calls, construction, failed policies, caches, references, retrieval, recomputation, output and all-phase writable high-water.

**OPEN:** universal all-input, SAT/UNSAT/malformed-aware, recursively iterable same-machine $A\mapsto\Phi(A)$ with $t'\le\max\{11/10,3/5+t/2\}$ and $s'\le\max\{1/2,s/2\}$; fixed-mixed $B3$; P versus NP. Existing two Route A / three Route B roles, schedules, original native rules and weights remain unchanged. Root `main.tex` not touched.

**Primary references:** Urquhart (1987), JACM 34(1):209-219, DOI 10.1145/7531.8928; Ben-Sasson & Wigderson (2001), JACM 48(2):149-169, DOI 10.1145/375827.375835; Reingold (2008), JACM 55(4), DOI 10.1145/1391289.1391291; FLMV (2005), JACM 52(6):835-865, DOI 10.1145/1101821.1101822.
