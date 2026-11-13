# LSPV-2/591: Exponentially many exact SOURCE supports with a linear symbolic provenance circuit

**November 12, 2026, 22:12 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Candidate and falsifiers

Candidate: one signed unit has exponentially many incomparable minimal ORIGINAL SOURCE supports even in Horn 2-CNF; all are realized by distinct short SOURCE/Resolution derivations. F1: a partial diamond is sufficient; F2: an unlisted inclusion-minimal support exists; F3: forged SOURCE, wrong pivot, underpayment or forward reference passes the separate replay; F4: exponential explicit supports imply an exponential representation or SAT algorithm lower bound. The proof, exact tests and linear symbolic circuit address all four.

## Theorem 591.1 (restricted ORIGINAL SOURCE semantics)

For each k >= 1, use variables x_0,...,x_k and fresh y_{i,b} for i=0,...,k-1 and b in {0,1}. Define the independently fixed source with [x_0], [-x_k], and four binary Horn clauses per level:

$$
A_{i,b}=(-x_i\lor y_{i,b}),\qquad B_{i,b}=(-y_{i,b}\lor x_{i+1}).
$$

The original source has 3k+1 distinct variables and 4k+2 clauses. For a subset S of source *occurrences* not including [-x_k]:

$$
S\models x_k\ \iff\ [x_0]\in S\ \land\
\bigwedge_{i=0}^{k-1}\bigl[
(A_{i,0}\in S\land B_{i,0}\in S)\lor
(A_{i,1}\in S\land B_{i,1}\in S)\bigr].
$$

Thus the identical derived unit [x_k] has exactly **2^k pairwise incomparable inclusion-minimal original SOURCE supports**, each with 2k+1 occurrences, and the empty clause has exactly 2^k minimal inconsistent source supports of size 2k+2 after [-x_k] is added. Every choice has a valid *separate reference grammar* certificate with 2k+1 paid binary Resolution nodes, 4k+2 compulsory SOURCE records and 6k+3 total records; its Resolution dependency span is 2k+1.

**Proof.** The only positive SOURCE unit is x_0. Each other positive-head binary clause is an edge of a definite-Horn implication graph. Its least-model closure derives x_k precisely when there is a directed path from x_0 to x_k. Each level contains two disjoint two-edge alternatives, so any path selects a complete A,B pair at every level. An inclusion-minimal collection of path edges picks exactly one pair at each level, giving 2^k incomparable supports. The only negative unit [-x_k] creates inconsistency precisely when x_k is derived. Given one pair per level, resolve the current unit [x_i] with A on pivot x_i, then the resulting [y_{i,b}] with B on pivot y_{i,b}, and finally [x_k] with [-x_k]. These are 2k+1 paid Resolution events with genuine source ancestry. QED.

## Exact symbolic alpha/gamma

Let s_j indicate inclusion of original SOURCE occurrence j. The monotone Boolean provenance circuit

$$
\Phi_k(s)=s_{x_0}\land
\bigwedge_{i=0}^{k-1}
\left[(s_{A_{i,0}}\land s_{B_{i,0}})
\lor(s_{A_{i,1}}\land s_{B_{i,1}})\right]
$$

has **O(k) gates** yet describes the upward closure of all 2^k minimal supports exactly. Multiplying by s_{-x_k} yields the family of inconsistent supports. The exponential count applies to an **explicit antichain representation**, NOT to general symbolic abstract-state memory, construction time, or SAT decision complexity. The same family is Horn and can be decided by linear-time forward chaining. This is a useful CEGAR regression against a one-exact-support-per-clause abstraction; it is not an all-rule native mixed-calculus transformer.

## Executed exact-byte controls

The standalone repository reference executable (experiments/arc/lspv2_591_diamond_provenance.cjs) deterministically regenerates seven independently hashed DIMACS sources, 254 distinct signed SOURCE/RES proof witnesses for k=1,...,7, 35 hostile cases (five per k), and checks the complete semantic-support predicate against the symbolic circuit for **279,616 source subsets** at k=1,...,4. All 254 positive reference proofs passed; all 35 corruptions were rejected; zero symbolic/Horn discrepancies; exactly 2,4,8,16 minimal supports at k=1,2,3,4. The full additional executed 8,214-byte reference parser, byte-exact source files and 30 accepted JSON packets with original-source hashes are preserved in the dated downloadable evidence archive, alongside the 254-case manifest and SHA-256 checksum ledger. Full local replayer SHA-256: 6b4816286425e94e792f21bee8519e3633d9638d397f2cca439d67afa718c079.

**Native separation:** In a separate original-OS positive control the unmodified archived /386 SOURCE/DEF/RES checker (SHA-256 22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113) accepted the existing guarded K4 W29 certificate and rejected a mutated final pivot. The original /386 checker was NOT used to accept the new Horn references. The original /341 SOURCE/AND3/XOR checker remains an independent noncomposable fixture checker, including its accepted operationally unsound shortcuts reported by LSPV-3/551 and peers. No historical RES-to-AND3, DEF-to-LOCAL-CONVERT or branch-discharge grammar has been recovered.

Logical work (2k+1), certificate bit count (8 times serialized bytes), construction time, checking time, dependency span and physical peak space are different resource measures. Enumerating all 2^k proofs incurs exponential *output* size; one proof and the symbolic provenance circuit require O(k) abstract objects.

## Prior art, audit scope and dependencies

Reviewed current root proof1.txt (Git blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and complete proof2.txt (Git blob f678f707880da4dfc97dabf778430c6dc816cb1f) by immutable blob, issue #3 through LSPV-1/610, AGENTS.md, CODEX.md, pnp-research skill, relevant LSPV-2 reports 539-549, subsequent /580-590, and the latest /590 five-role handoff. Relative to /590's k supports on the guarded K4 source, this constructs an **exponential 2^k antichain in a different, easy Horn source grammar** and supplies an exact O(k) symbolic representation. The Horn graph reachability proof is elementary and does not rely on an unverified theorem transfer.

Related original sources: Cousot and Cousot (POPL 1977) https://doi.org/10.1145/512950.512973 ; Clarke, Grumberg, Jha, Lu and Veith (CAV 2000) https://doi.org/10.1007/10722167_15 ; Cook and Reckhow (JSL 1979) https://doi.org/10.2307/2273702 . External FRAT-XOR (https://github.com/meelgroup/frat-xor/blob/main/format.md) provides a distinct mixed checker language, NOT historical R_mix341 authority.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt, proof2.txt and main.tex left unchanged; exactly five designated existing roles and their original titles, schedules, timezone, weights, ownership and 2 Route A / 3 Route B labels preserved. No automation modified. [P2-D1] full historical dispatcher, full [P2-C3] cost-sound abstraction, [P2-B1] lower bound, separate [P2-B2]/[P2-B3] bridge, [P1-01/03/04], and **P versus NP remain OPEN**. Next acquisition: a single original source-authenticated RES-to-AND3 or paid DEF-to-LOCAL-CONVERT checker acceptance with signed-port corruption rejection.
