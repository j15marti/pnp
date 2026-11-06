# REFEREE380: strict-3 positive-guard lifting of a shared FACET-A Cook DAG

**November 5, 2026, 23:52 PST. LSPV-5 Independent Proof Red Team, Route B.**

**Status. PROVED/EXACT, RESTRICTED to the declared FACET-A grammar; COMPUTATIONAL complete finite traces.** Let $F=\{C_1,\ldots,C_S\}$ be a proper 3-CNF and let $P$ be a source-authenticated clausal FACET-A refutation DAG using fresh signed-AND2 definitions and correctly oriented binary Resolution. Its LSPV-1 positive guard is

$$
G_3(F)=\bigwedge_{i=1}^S
  (g\vee a_i\vee y_i)\wedge(\neg y_i\vee b_i\vee c_i),
\qquad C_i=(a_i\vee b_i\vee c_i),
$$

where $g,y_1,\ldots,y_S$ are globally fresh. After alpha-renaming every old auxiliary above the enlarged source header, $P$ compiles to a shared FACET-A derivation $G_3(F)\vdash g$ with exactly $S$ additional Resolution nodes and critical-path increase at most one. No shared subproof is unfolded; no split, discharge, weakening, substitution, semantic oracle, or answer axiom is used.

Applied to the completed REFEREE379 Cook proof for Braun's strict-3 bit-pigeonhole source, with $n=2^\ell$, $M=n\binom{n+1}{2}$ and $S=M(2\ell-2)$, the exhibited guarded-unit DAG has

$$
\boxed{
W_{\rm guard}=
M(6\ell-5)+(n+1)(2n\ell-9)
+\frac{n(n+1)(27n^2+11n-14)}{24}=O(n^4).
}
$$

For every clause-minimally UNSAT proper 3-CNF $F$, all $2S$ guarded source clauses are indispensable for the consequence $g$. Hence every sound source-authenticated proof of $g$ whose paid inference nodes have at most two premises and whose source leaves are free has at least $2S-1$ paid nodes in its final dependency union. This is an **all-legal-rule source-ancestry floor under the stated arity and soundness assumptions**, but it is linear in the guarded source size and supplies no superpolynomial mixed lower bound.

The target $G_3(F)\vdash g$ is a unit derivation from a satisfiable formula (set $g=1$), not a refutation and not an instance of $W_R(F)$ for UNSAT sources. Exact historical $R_{\mathrm{mix341}}$ acceptance, a superpolynomial $\overline W_R$, B1/B2/B3, and P versus NP remain **OPEN**.

## IDEA -> SEARCH -> ITERATE

### Initial hypothesis and falsifiers

The initial hypothesis was that REFEREE379 could not yet be promoted to historical $R_{\mathrm{mix341}}$ because the archived grammar does not determine an owner/facet selector. Its falsifiable prediction was that no exact historical selector or authoritative accepted trace could be located. Precise falsifiers were:

1. an exact historical byte clause selecting all three defining facets;
2. an authoritative historical checker accepting equivalent bytes;
3. a current LSPV-1 or LSPV-3 accepted historical trace;
4. a facet-free native LOCAL/Resolution derivation of the same relation.

Project search showed that this is not a new result: LSPV-3/436 already records the native DEF-facet underdetermination, and LSPV-3/440--441 explicitly use a separately declared GATE-LOCAL calculus. No falsifier was found, but repeating the grammar objection would add no advance.

The hypothesis was therefore revised: test whether LSPV-1's established strict-3 positive guard defeats the completed Cook shortcut, while preserving original-source identity, globally fresh IDs, shared-DAG work, and native FACET-A rules. The result is the general guard-lift theorem above. The positive guard preserves ordinary-Resolution hardness when a substitution theorem applies, as LSPV-1/437 proves; it does **not** block a separately legal extension proof.

## Governing continuity and authenticated search

Read the governing five-role handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`; current issue #3 through LSPV-3/441 and LSPV-4/433; historical /341; LSPV-1/436--437; LSPV-3/436 and /440--441; REFEREE379 and its raw trace; the actual current Grok and Claude files; `AGENTS.md`, `CODEX.md`, and the repository research instructions. LSPV-4/433 correctly withdraws a Route A comparison made with inconsistent input-size baselines; it does not alter this Route B theorem.

Primary sources checked:

- Alasdair Urquhart, “Hard examples for resolution,” *JACM* 34(1), 1987, pp. 209--219: exponential ordinary Resolution lower bounds for expander-based Tseitin contradictions.
- Eli Ben-Sasson and Avi Wigderson, “Short proofs are narrow---resolution made simple,” *JACM* 48(2), 2001, pp. 149--169: the width-size method supporting ordinary Resolution lower bounds.
- Stephen Cook, “A short proof of the pigeon hole principle using extended resolution,” *SIGACT News* 8(4), 1976: the mandatory polynomial ER shortcut.
- Kamil Braun, “An exponential lower bound for the bit pigeonhole principle in resolution over parities,” arXiv:2609.23015, Theorem 1.1: for $\ell\ge32$, $n=2^\ell$, DAG-like Res($\oplus$) needs more than $\exp(n/(32768\ell^2))$ lines; extension axioms are outside that theorem.

Direct Google-branded access was unavailable. Indexed web search was used for the primary papers; no claim of Google execution is made.

Change-aware repository review pinned or rechecked: `konard/p-vs-np` at `ecedd2b45f1c524d85c00b2da27a9c140025550c`; `blkph0x/p-vs-np-proof-research` at `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; `meelgroup/frat-xor` at `18cd6bc17af10a9891c10a846ce966166f9fe0dc`; `tanyongkiam/cake_lpr` at `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`; `peitl/short-proof` at `2c524cfceecf68b56f51d23f6b63255b502856d3`; `marijnheule/drat-trim` at `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; `MassimoLauria/cnfgen` at `24e633bdbed0d0998493bee99c42faf480c7dc96`; `openai/math` at `4eaee87548250b2682affda7d05d947c05554bae`; and `anthropics/formal-math` at `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`.

Actual files inspected include the two required repositories' method/proof-status material, FRAT-XOR's typed clause/XOR format, and CakeLPR's verified-checker resource documentation. They reinforce typed provenance and verification boundaries but provide neither the historical /341 grammar nor a noncircular same-$R$ B3 bridge. Repository titles, prose claims, and successful builds are not proof of P versus NP.

## Established-family / theorem / encoding / shortcut ledger

| Family | Exact 3-CNF encoding and size | Published lower bound and model | Known shortcut control | Remaining transfer |
| --- | --- | --- | --- | --- |
| Cubic odd Tseitin | For each vertex $v$ of a cubic graph, one edge variable per incident edge and the four proper width-3 clauses forbidding assignments of parity different from charge $\chi(v)$. For $h$ vertices: $3h/2$ variables, $4h$ clauses, $\Theta(h\log h)$ encoded bits under indexed literals. Odd total charge is UNSAT. | Urquhart/BW: $2^{\Omega(h)}$ ordinary unrestricted shared-DAG Resolution on suitable expanders. Rules are clauses plus Resolution; no extension or GF(2) shortcut is covered. | The historical semantic AND3/GF(2) candidate derives the parity contradiction in $4h-1$ paid nodes. | Mandatory negative control: ordinary Resolution hardness does not transfer to the full mixed calculus. |
| Braun bit-PHP | $m=n+1$, $n=2^\ell$, variables $x_{i,b}$. For every $i<j$ and address $a\in\{0,1\}^\ell$, the width-$2\ell$ collision clause says $i$ or $j$ differs from $a$. There are $M=n\binom m2$ wide clauses. Each $(l_1\vee\cdots\vee l_{2\ell})$ is replaced by the private chain $(l_1\vee l_2\vee z_1),\ldots,(\neg z_{2\ell-3}\vee l_{2\ell-1}\vee l_{2\ell})$, giving $S=M(2\ell-2)$ proper 3-clauses and $M(2\ell-3)$ private variables. | Braun Theorem 1.1: $>\exp(n/(32768\ell^2))$ lines in DAG-like Res($\oplus$), $\ell\ge32$, with affine clauses/semantic weakening but without extension axioms. | REFEREE379 gives a complete $O(n^4)$ Cook proof in FACET-A; LSPV-3/441 gives a full polynomial proof in proposed GATE-LOCAL. This report preserves it under $G_3$. | Equisatisfiability is insufficient. No lower-bound-preserving back-translation survives the chain plus legal extension variables. |
| Unary $PHP_{n+1}^{n}$ | Totality $\bigvee_{j<n}p_{i,j}$ and collision $\neg p_{i,j}\vee\neg p_{i',j}$. It is not 3-CNF for $n>3$ without a specified encoding. | Haken: exponential ordinary shared-DAG Resolution. | Cook: polynomial extended Resolution. REFEREE379 compiles the full shortcut without weakening. | Haken does not imply hardness for a calculus admitting Cook's definitions. |

Certified UNSAT, a certified proof-size lower bound in one named system, and empirical solver difficulty are distinct claims. No empirical difficulty claim is used here.

## Guard-lift theorem

**Theorem (FACET-A positive-guard lift).** Fix a proper 3-CNF $F=\{C_i\}_{i=1}^S$, with a designated literal order $C_i=(a_i\vee b_i\vee c_i)$. Let $P$ be a finite acyclic FACET-A refutation DAG whose leaves are authenticated source clauses or owner-qualified facets of globally fresh signed-AND2 definitions and whose non-definition inferences are correctly oriented binary Resolution. Then one can construct a DAG $P^g$ deriving $(g)$ from $G_3(F)$ such that:

1. every old auxiliary variable is alpha-renamed above the new source maximum;
2. every guarded source pair yields $g\vee C_i$ by one Resolution on $y_i$;
3. every old definition/facet is retained with renamed variables;
4. every old Resolution is replayed once, replacing a source reference by its recovered guarded clause;
5. $|P^g|=|P|+S$ in paid distinct-node work and $\operatorname{span}(P^g)\le\operatorname{span}(P)+1$ under unit-latency unlimited parallelism.

**Proof.** Resolve $(g\vee a_i\vee y_i)$ with $(\neg y_i\vee b_i\vee c_i)$ on $y_i$ to obtain $g\vee C_i$. The new variables are fresh, so no old pivot is $g$ or any $y_i$. Replay the old topological order. A source-independent clause remains unchanged; a clause with source ancestry is its old clause with $g$ adjoined. Resolution deletes the same old pivot and preserves at most one copy of $g$. Conservative signed-AND2 definitions alone cannot refute, so the old empty root has source ancestry and becomes $(g)$. Exactly $S$ recovery nodes are new. Prepending one unit-depth recovery to any source-to-root path increases depth by at most one. The dependency DAG and all shared references remain unchanged otherwise. $\square$

All multi-premise inferences are AND obligations. Alternative proofs are OR choices outside this exhibited DAG. There are no branch assumptions, so no contextual discharge or cross-branch reuse occurs. The paid work is the union of distinct inference nodes once, not a sum over unfolded paths.

## General indispensable-source lemma

**Lemma.** If $F$ is clause-minimally UNSAT, each of the $2S$ clauses of $G_3(F)$ is indispensable for the consequence $g$.

**Proof.** Fix $i$. Since $F\setminus\{C_i\}$ is satisfiable and $F$ is not, choose an assignment satisfying every other clause and falsifying $C_i$. Set $g=0$. For each $k\ne i$, choose $y_k=\neg a_k$; because $C_k$ is true, both guarded clauses are satisfied. If the first clause of block $i$ is deleted, set $y_i=0$, satisfying the second by $\neg y_i$. If the second is deleted, set $y_i=1$, satisfying the first. Thus deletion of either guarded source permits a model with $g=0$. $\square$

Consequently every sound source-authenticated derivation of $g$ must have all $2S$ source leaves in its final backward dependency union. If paid inferences have at most two premises, a rooted acyclic dependency graph joining $L=2S$ indispensable leaves has at least $L-1=2S-1$ internal inference nodes: connectedness gives $L+I-1\le E$, while premise arity gives $E\le2I$. Definitions or unary nodes cannot improve the inequality. This lower floor permits every legal shortcut, reconvergence, and after-the-fact proof choice satisfying the assumptions; it is still only linear.

The Braun strict-3 source is clause-minimal by a direct structural witness: for a deleted chain clause, map the two selected pigeons to its target address, bijectively map all others to the remaining holes, and set the private chain variables so that exactly the deleted chain facet is false. The verifier constructs every such witness for the finite traces rather than relying on SAT calls.

## Exact application to REFEREE379

REFEREE379 has

$$
W_{\rm full}=M(4\ell-3)+(n+1)(2n\ell-9)
+\frac{n(n+1)(27n^2+11n-14)}{24}.
$$

The guard compiler adds $S=M(2\ell-2)$ source-recovery resolutions and no other node, yielding the displayed $W_{\rm guard}$. The guarded source has $2S$ proper 3-clauses. If the old source maximum is $v$, the compiler assigns $g=v+1$, $y_i=v+1+i$, and shifts every old auxiliary by $S+1$. This prevents a source/definition collision after the source header grows.

| $\ell$ | guarded sources | source / final variables | paid work | span | final | source floor |
| ---: | ---: | ---: | ---: | ---: | --- | ---: |
| 2 | 160 | 131 / 191 | 700 | 20 | `E_R345` = $(g)$ | 159 |
| 3 | 2,304 | 2,044 / 2,488 | 9,501 | 54 | `E_R5070` = $(g)$ | 2,303 |

## Relation to LSPV-1/437 and LSPV-3/441

LSPV-1/437 proves, for established hard cubic Tseitin $F_h$, that ordinary Resolution needs $2^{\Omega(h)}$ to derive $g$ from $G_3(F_h)$, using a whole-DAG substitution back to an ordinary refutation of $F_h$. This report neither disputes nor generalizes that restricted lower bound. It proves that when the unguarded source already has a legal polynomial FACET-A extension proof, the same proof lifts through $G_3$ with only linear overhead.

LSPV-3/441 independently translates REFEREE379 into a polynomial proof under the proposed GATE-LOCAL interface. That strengthens the shortcut control but still does not authenticate the historical /341 bytes. Neither result establishes the minimum in the full historical mixed calculus.

## Independent executable verification

The Python producer imports the REFEREE379 construction, guard-lifts it, alpha-renames old auxiliaries, and emits complete raw traces. The independent Node verifier reconstructs and checks:

- exact guarded DIMACS, source hash, proper width three, and header bounds;
- recovery of the exact old source and its published SHA-256;
- globally fresh guard/private variables and the exact $S+1$ auxiliary shift;
- every signed-AND2 owner facet, owner provenance, oriented pivot, and exact resolvent;
- final unit $(g)$, exact work and span, and the complete backward union;
- all 2,464 one-source-deletion witnesses across $\ell=2,3$;
- rejection of wrong guard pivot, nonfresh guard, unshifted definition, corrupted source hash, corrupted guarded source, old-source reference leakage, and false final target.

Two generations were byte-identical. The independent replay made **6,890,330 checks** and rejected **7/7** hostile mutations. This is an independent reimplementation of the declared grammar, not execution of an authoritative historical checker.

Artifact hashes:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| producer `lspv5_380_guard_lift_facet_a.py` | 5,875 | `a590583fd3a3d6545e72f3e33fe3ff74e277f854411aacd9ea72a59c23c6a925` |
| independent verifier `lspv5_380_independent_verify.mjs` | 10,123 | `47d9effee153586bf8f2c9125a60561bf941983eb4465937f37db0ea0509ddcd` |
| complete raw traces | 2,231,726 | `bd3ee81fca7152410873c925221d4e90f3e428d45ae9f141cfa8d62c87b61564` |

## Resource ledger

| Resource | Charged observation / limitation |
| --- | --- |
| Logical nodes | 700 and 9,501 paid distinct nodes; 160 and 2,304 free authenticated source leaves. All are live in the final backward union. |
| Explicit evidence | Raw trace 2,231,726 bytes = 17,853,808 bits. Producer + verifier + raw total 2,247,724 bytes. Deterministically reconstructed clauses/facets still incur parsing/checking work. |
| Construction/search | Deterministic construction, no optimizer, restarts, SAT oracle, or failed search policies. The ideal proof minimum continues to grant free after-the-fact legal proof choice. |
| Parsing/source/index/head reads | Executed over the complete raw file; verifier maintains source, owner, node, clause, depth, and dependency maps and rereads each deletion-witness clause. |
| Conversion/update | Exactly $S$ guard recoveries and one global alpha-renaming pass per trace. |
| Verification | 6,890,330 explicit checks and seven negative controls. |
| Output | Full JSON serialization and stdout summary charged in host execution. |
| Cache/retrieval/recomputation | Full clauses and dependencies retained; each deletion witness is recomputed and checked against every guarded source. No space-saving schedule is claimed. |
| Peak space/time | Observed producer about 0.31 host s / 29,440 KiB cumulative child max RSS; verifier about 1.11 host s / 139,596 KiB cumulative child max RSS in the instrumented run. These are host observations, not native TM bounds or FLMV exponents. |
| Failed policies | Initial grammar-undertermination idea was identified as duplicate prior work and retired before publication. |

The ideal logical minimum, critical-path span under unlimited parallelism, and a realizable time/space schedule are different quantities. This report supplies an exhibited work/span upper bound and a separate source floor, not an optimal space schedule.

## Classification and precise remaining gap

- **KNOWN:** Urquhart/BW ordinary Resolution hardness; Haken ordinary Resolution PHP hardness; Cook polynomial ER shortcut; Braun Res($\oplus$) lower bound without extension axioms.
- **PROVED/RESTRICTED here:** exact shared-DAG FACET-A positive-guard lift; exact $W_{\rm guard}$ upper bound; indispensable-source and $2S-1$ binary-premise floor.
- **COMPUTATIONAL:** complete $\ell=2,3$ declared-grammar traces and hostile-mutation/deletion-witness audit.
- **CONDITIONAL:** the GATE-LOCAL polynomial shortcut if that proposed calculus is adopted.
- **OPEN:** exact historical /341 owner/facet/LOCAL byte grammar and checker acceptance; any lower-bound invariant surviving every legal historical extension, GF(2), LOCAL, Resolution, sharing, temporary growth, and optimal proof choice; a noncircular same-$R$ B3 theorem.

**Actual advance:** a general strict-3 positive guard is no hardness shield against an already legal extension shortcut, and the exact shared-DAG overhead is only one recovery inference per old source clause. The all-rule source floor is rigorous but linear. **P versus NP remains OPEN.**
