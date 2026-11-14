# TMR-1/009: preserving linear input-bit sensitivity under a no-unused-variable 3-CNF grammar

**Run:** 2026-11-13 19:05 PST, America/Los_Angeles. **Role:** TMR-1 Machine Model Lead. **New theorem:** TMR1-NU9, **CANDIDATE pending independent TMR-2/TMR-5 mathematical review**. Independent review of TMR-2/008's even-parity fresh-variable argument: **PROVED/RESTRICTED at the permissive-unused-ID grammar**, subject to the original TMR-2/005/TMR-5/005 minimal-UNSAT hypotheses. Finite source tests: **COMPUTATIONAL**. The unrestricted all-exponent 3-SAT lower bound and P versus NP are **OPEN**.

## 1. Precise change and falsification question

TMR-2/008 obtains $Q=(1-o(1))L$ individually opposite-label-sensitive source bits by declaring spare identifiers that never occur. It explicitly leaves transfer to grammars that *require every declared variable to occur* OPEN. TMR1-NU9 closes a weaker but substantive bridge: **a constant fraction of the entire encoded input remains individually bit-sensitive, with all declared identifiers used, and all one-bit opposite-label neighbors still valid under that stricter grammar**.

The repair deliberately does NOT claim near-unit sensitivity density, a superlinear lower bound, or a general algorithm. It appends small all-positive clauses using every previously unused identifier. These filler clauses are satisfiable independently of one constrained spare identifier, so an original clause-deletion witness extends to every changed source. The extra clauses dilute density but do not destroy the original Hamming-one SAT/UNSAT contrasts.

## 2. Exact binary grammar and machine model

Use the actual project explicit source grammar $1^N0\,1^D0$ followed by $D$ ordered proper 3-clauses, each a concatenation of three literal fields, each field one polarity bit followed by a $w=\max(1,\lceil\log_2 N\rceil)$-bit binary positive variable ID. All IDs must be in $[1,N]$; a clause's three IDs must be distinct. **Additional strengthened validity rule:** each declared ID $1,\ldots,N$ must occur in at least one clause. The encoded bit length is

$$
L=N+D+2+3D(w+1).
$$

Fix one finite **total** correct uniform deterministic multitape decider $A$ on *all* binary inputs at *all* lengths, deciding valid SAT, valid UNSAT and malformed strings consistently. All finite control, work-tape cells, head movements, rereads, indices, stacks, cached tables, preprocessing and fallback are charged. Assume $h\ge1$ physically local read-only binary source heads, with at most $h$ original source-bit values observable in a transition. Other finite machine models require a separately charged translation. Time $T_A(x)$ counts physical transitions and $S_A(x)$ counts all visited writable cells of the **same** run. No workspace restriction is imposed.

## 3. Lemma: every variable of a clause-minimally UNSAT CNF occurs at least twice

Let $F$ be clause-minimally UNSAT, meaning $F$ is UNSAT but $F\setminus\{C\}$ is SAT for every clause $C$. Suppose a variable $x$ occurs in precisely one literal of one clause $C$. Choose a satisfying assignment of $F\setminus\{C\}$ and change only $x$ to satisfy its literal in $C$. No other clause contains $x$, so all remain true and $F$ would be SAT, contradiction. Hence each occurring variable appears at least twice (and indeed with both polarities, though that stronger fact is not needed). For a proper width-three source with $t$ occurring variables and $M$ clauses,

$$
2t\le3M.
$$

This is a useful **valid-source preservation** fact for identifier-bit mutations, rather than a computation-time argument.

## 4. New theorem candidate TMR1-NU9, all identifiers used

Let $F$ be any clause-minimally UNSAT proper 3-CNF with $t\ge3$ occurring variables and $M$ clauses. Relabel its original variables $1,\ldots,t$ and let

$$
w=\lceil\log_2(2t+2)\rceil,\quad N=2^w-1,\quad
\rho(i)=2i+(\operatorname{popcount}(i)\bmod2).
$$

Every $\rho(i)$ is a nonzero even-parity $w$-bit identifier; $\rho$ is injective. Write $E=\{\rho(1),\ldots,\rho(t)\}$ and $U=[1,N]\setminus E$. Since $N\ge2t+1$, $|U|\ge t+1\ge4$.

Construct an explicit filler $H_U$ consisting of $D_U=\lceil|U|/3\rceil$ all-positive **proper** 3-clauses: group unused IDs in triples, and for a final one or two IDs, form one more triple with two or one distinct IDs from the first group. Every ID in $U$ occurs, and every filler clause uses three distinct IDs entirely in $U$. Set

$$
G=\rho(F)\land H_U,\qquad D=M+D_U,
$$

and encode $G$ using the strict no-unused-variable grammar above.

**Claim 1 (source validity and original label).** Every ID in $[1,N]$ occurs in $G$ and each clause is proper. The source is UNSAT because $\rho(F)$ already is UNSAT.

**Claim 2 (valid same-length SAT neighbors).** For every sign bit and every identifier bit in the $3M$ **original core literal fields**, changing exactly that one bit yields a syntactically valid *no-unused-variable*, proper width-three CNF of the **same length**, and the altered CNF is SAT.

Proof. Fix the altered core clause $C$ and choose $\alpha$ satisfying $F\setminus\{C\}$. It falsifies $C$, since $F$ is UNSAT. If a polarity bit is flipped, the corresponding literal becomes true; set every filler variable to true. All filler clauses and every other core clause are satisfied.

If an identifier bit in some $\rho(i)$ is flipped, its parity changes from even to odd. The resulting positive integer $j$ lies in $[1,N]$ and belongs to $U$, hence was not used in the core. It is distinct from the other two IDs of $C$. The old ID $\rho(i)$ remains used in the core because of the preceding at-least-two-occurrences lemma, so **the no-unused-ID validity rule is preserved**. Keep $\alpha$ on original variables, assign the now-referenced filler variable $j$ to satisfy the changed literal, and assign *all other* filler variables true. Every filler clause contains two IDs different from $j$, both true if $j$ is present; if $j$ is absent, all its literals are true. Thus all filler clauses hold, as do all unaltered core clauses. This completes the witness and preserves the exact source length and grammar. QED at the explicitly scoped source level, subject to peer review.

There are

$$
Q=3M(w+1)
$$

independently one-bit opposite-label-sensitive coordinates. The full length is

$$
L'=N+(M+D_U)+2+3(M+D_U)(w+1).
$$

Since $N<4t+3$, $D_U\le t+1$, and $2t\le3M$, on every unbounded family with $t\to\infty$,

$$
\liminf\frac{Q}{L'}\ge \frac25.
$$

This is a **conservative asymptotic density bound**, not a claim that *every* bit is sensitive; filler literal and unary-header bits need not be. On the cubic-prism Tseitin family, $t=3r$, $M=8r$, $D_U\le3r+1$, so the sharper bound is

$$
\liminf_{r\to\infty}\frac{Q}{L'}\ge\frac8{11}.
$$

The formula remains easy to solve on an authenticated affine/prism fast path, as below.

## 5. Direct unrestricted-workspace observation implication, and its ceiling

Take the concrete original UNSAT input $x$ and any sensitive coordinate $j$. If $A(x)$ never observes source position $j$, compare it with the valid equal-length SAT source $x^{(j)}$. At each transition their read symbols, complete finite control, all input-head positions, and all writable tapes coincide by induction: the inputs agree on every position actually observed. Their final answers would coincide, contradicting correctness on both labels. Therefore every one of the $Q$ coordinates is observed on the SAME UNSAT execution. Thus

$$
T_A(x)+1\ge Q/h=\Omega(L')
$$

for every fixed correct total $A$ with $h$ local binary input heads, even if $S_A(x)$ is any polynomial or greater. This argument does not identify two work states without their original readable input, does not impose streaming/one-pass access, and does not charge witness counts or proof-system size as runtime.

**Crucial ceiling:** $Q\le L'$, so this entire source-observation method proves at most linear first-observation work. It does not establish an unavoidable cost of *processing already read data*, and thus does not reach the shared all-exponent target

$$
\forall A\ \forall k\ge1\ \forall C>0\ \forall L_0\
\exists \text{ valid } x:\ |x|\ge L_0,\
T_A(x)>C(|x|+1)^k.
$$

Any machine-space bound must remain same-run. This theorem covers all writable space for the **reading** implication, not all possible computational processing. A small-space restriction or one fixed superlinear exponent could not establish the unrestricted target.

## 6. Explicit efficient hostile counteralgorithm

For the canonically ordered cubic-prism, odd-charge XOR3 family (one source instance per $r$ and charge vector), use a **single fixed program** across all lengths: parse the complete source and verify the expected sequence of core clauses, even-parity IDs and the sorted all-positive filler construction; accumulate the XOR of decoded vertex charges; check the endmarker. The grammar and filler schedule can be regenerated from $r$ in binary counters of $O(\log L')$ bits. The ordinary sequential input scan and all literal comparisons take $O(L')$ paid steps; binary increments have an amortized linear cost in the total bit stream. If authentication succeeds, classify by global charge XOR. Otherwise rewind using charged moves and invoke a fully paid exhaustive total proper-3CNF solver, including malformed handling. This gives a **CANDIDATE symbolic** $T=O(L')$, $S=O(\log L')$ *on the authenticated family*, while remaining total/correct for all strings. No general polynomial SAT decider is claimed; native machine-transition compilation was not executed.

This counters stronger hypotheses based only on near-maximal read necessity, clause indispensability, dense variable occurrence, high treewidth, or source-header coverage. Renaming, filler, product factors, algebraic shortcut, padding, sharing and recomputation remain permitted.

## 7. Reproduction and actual finite executions

**Published hosted-V8 executable:** \`experiments/tmr/tmr1_no_unused_sensitive009.cjs\`. This is an independently authored standalone source, not a wrapper around TMR-2/008. It constructs the original odd-charge prism source and all-positive filler, parses **every declared ID**, verifies the original inconsistency with BigInt GF(2) elimination and checks every changed source with complete satisfying witnesses. It executed:

- 10 sources for $r=3,4,6,8,12$ and two distinct odd-charge vertices.
- 528 original core-clause deletion witnesses.
- 1,584 sign-bit flips and 9,744 identifier-bit flips, **11,328 actual parsed no-unused-variable SAT neighbors**, zero failures.
- 148 added filler clauses, 10 filler-only mutation controls that remain UNSAT, 512 exhaustive small-source UNSAT assignments.
- Maximum length $L'=3304$ bits, $Q=2304$ sensitive bits; observed densities $0.673947$ through $0.764070$.

**Separate native Python 3.13.5 independent reimplementation, local-only:** brute-forced *every* original-core assignment for $r=3,4$ (two charge placements each) to recover clause-deletion witnesses, rebuilt every changed encoded source and tested syntax, all-ID occurrence and complete SAT witnesses. Four sources and **2,016 Hamming-one SAT neighbors**, zero failures. Local file \`/mnt/data/tmr1_no_unused_independent009.py\` was executed, but is not claimed to be a GitHub artifact. This independently used brute force instead of the V8 GF(2) witness solver. No native Node replay of the published JavaScript and no physical multitape machine simulation were performed. These counts are COMPUTATIONAL, not proofs of asymptotic runtime.

**Immutable raw:** \`results/raw/tmr/2026-11-13_1904_TMR1_NO_UNUSED_SENSITIVITY009_RAW.json\`. Reproducer has fixed deterministic input cases, no random seed. Python chunks each completed under the project's 25-second rule.

## 8. Dependency DAG, manuscript reconciliation and literature

Dependencies: **TMR-2/005, TMR-5/005, TMR-1/007** (odd-charge clause-minimally UNSAT core) $\to$ **TMR-2/006 and /008** (polarity and even-parity relabeling) $\to$ **new no-unused filler and at-least-two-occurrences lemma** $\to$ valid one-bit SAT neighbor witnesses $\to$ **same-machine deterministic unread-source coupling** $\to$ $\Omega(L')$ acquisition only. The missing final arrow from source acquisition to all-exponent computation remains **OPEN**. TMR-3 should audit the paid fast path and alternative clause orders; TMR-4 should incorporate the stricter neighbor set without multiplying input-acquisition costs; TMR-5 should independently review the filler validity and density constants.

Root canonical \`main.tex\` is TMR-5 whole-document synthesis territory; this run makes no unsanctioned edit. Original TMR-2 EPI8 grammar dependence remains in history: it was not retroactively replaced. The new result is narrower in sensitivity fraction, stronger in input grammar validity.

Sources:
[1] H. Buhrman and R. de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, TCS 288 (2002), 21-43; author preprint https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf . This supplies the decision-tree sensitivity context, not an arbitrary-TM superpolynomial theorem.
[2] L. Fortnow, R. Lipton, D. van Melkebeek and A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6) (2005), 835-865; https://doi.org/10.1145/1101821.1101822 . Its small-space/random-access lower-bound scope is distinct from unrestricted all-exponent separation.
[3] Primary project sources: TMR-2/008 report \`research/agents/tmr-2/2026-11-13_1823_TMR2_DENSE_SOURCE_BIT_SENSITIVITY008.md\`; TMR-5/005 graph proof; TMR-1/007 exact component lemma; TMR-2/006 polarity lemma. Exact original code and data were inspected, not merely chat citations.

**Research reads/limits:** Replacement directive read FIRST and rechecked (SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4). Complete proof1.txt: 28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343. Complete proof2.txt recovered from actual Git blob: 1,051,196 characters, SHA 930c5eeddafce656717f28055a7a9a755f44737c; ordinary fetch's empty text was not treated as an empty tracker. Complete main.tex recovered from Git blob: 2,497,977 characters SHA 4e0dc7a81c3757289e87661b6df29e458cd03daa. Current issue #3 (1,965 comments at read), AGENTS.md, CODEX.md, repository research skill, five latest handoffs and original relevant TMR reports/code/raw were inspected. No mounted repository checkout, so repo preflight and report validator were not executed. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No tasks or schedules created, revived or changed.

**ONE next target:** TMR-5 independent review of no-unused-ID validity for every original identifier flip and of the $2/5$, $8/11$ density bounds, then test whether any representation-independent post-acquisition processing potential is available. **P versus NP remains OPEN.**

END_OF_REPORT::TMR1::NO_UNUSED009::2026-11-13_1905_PST
