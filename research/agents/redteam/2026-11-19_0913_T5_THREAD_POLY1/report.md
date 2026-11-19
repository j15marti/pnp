# T5-REDTEAM-THREAD-POLY1: compact quotient and paid canonical lifting

Date: 2026-11-19 KST. Role: Independent Red Team. P versus NP remains OPEN. Independent external mathematical review is pending.

## Claim card

Target pipeline: authenticated explicit oriented source \(H\), promised connected and edge-minimal T5-UNSAT; designated original arc \(e\); deletion \(G=H-e\); source parsing and thread suppression; branch-candidate acquisition; original-vertex witness lifting; full verification and output.

Quantifiers: for every such \(H\) and every original arc \(e\) in a maximal degree-two thread \(P\), the statements below apply. The algorithmic experiment is on one separately authenticated 33-vertex source and is finite evidence only.

Model: word-RAM accounting for a full explicit vertex/arc source, with a separate fixed-source Boolean-circuit observation. Colors are \(\mathbb F_5\), and \(R(a,b)\) means \(b-a\in\{1,3\}\).

Candidate: after one branch assignment is acquired for the deletion of a thread, every deletion position in that thread has a canonical linear-work original-label extension. Each intact thread constraint has one constant-degree \(\mathbb F_5\) polynomial equation. Therefore neither internal-thread multiplicity nor the nine-relation alphabet is an information or circuit lower bound for witness construction. The unresolved work is acquisition of a satisfying branch assignment.

Falsifiers fixed before the final run:

1. An orientation word whose endpoint support differs from the claimed translate of \(\{0,2,\ldots,2L\}\).
2. A polynomial root set that differs from the exact endpoint relation.
3. A satisfying branch assignment that cannot be lifted after deleting an internal edge, or a lifted witness that satisfies the missing arc.
4. Different deletion positions in one thread requiring different branch searches.

The first draft formula did fail a test: it assigned a backward traversal base increment of \(-1\). The correct set is \(\{-1,-3\}=\{4,2\}=2+\{0,2\}\). This correction changed only the symbolic formula check; the solver always evaluated original arcs directly.

## Exact theorem 1: polynomial thread normal form

Let a thread \(P=v_0\ldots v_L\) have \(r\) arcs directed backward under this traversal. For an assignment, put \(d=x_{v_L}-x_{v_0}\). A forward traversal increment is \(1+2z_i\), and a backward traversal increment is \(2+2z_i\), where \(z_i\in\{0,1\}\). Hence the attainable endpoint differences are

\[
S_P=(L+r)+\{0,2,\ldots,2L\}\pmod 5.
\]

For \(L\le 3\), define

\[
F_P(x_{v_0},x_{v_L})
=\prod_{j=0}^{L}\left(x_{v_L}-x_{v_0}-(L+r+2j)\right)
\quad\text{over }\mathbb F_5.
\]

Then \(P\) extends if and only if \(F_P=0\). The polynomial has degree at most four. Thus a q-thread core has an explicit \(O(q)\)-size arithmetic verifier over \(\mathbb F_5\), with constant degree per constraint. A fixed finite Boolean encoding gives an \(O(q)\)-size Boolean verifier as well.

Status: PROVED/EXACT. This is a compact representation and verifier, not an algorithm for finding a common zero. Project reports already contain GF(5) cycle and Fourier formulations; no priority claim is made for the general algebraic viewpoint. The exact product normal form above is recorded as a red-team control.

## Exact theorem 2: critical complement pinning and canonical lift

Suppress all maximal degree-two threads of \(H\). The verified structural theorem gives \(1\le L(P)\le3\). Let \(e\) be any edge of \(P\). A branch assignment extends to \(H-e\) exactly when it satisfies every intact thread relation \(S_Q\), \(Q\ne P\). The broken thread consists of two rooted path fragments, and each fragment extends greedily from its fixed branch endpoint.

Any such branch assignment must violate \(S_P\); otherwise all intact threads and \(P\) would extend and color \(H\), contradicting UNSAT. Therefore, after using global rotation to set \(x_{v_0}=0\),

\[
x_{v_L}\in\mathbb F_5\setminus S_P,\qquad
|\mathbb F_5\setminus S_P|=4-L.
\]

In particular, deleting an edge from a length-three thread uniquely fixes the other endpoint color modulo rotation. Length-two and length-one threads leave two and three endpoint differences, respectively.

For each intact thread, choose the lexicographically least internal color tuple satisfying its at most three arcs. For the broken thread, choose the lexicographically least tuple satisfying all arcs except \(e\). These are constant-size lookups. After a branch assignment is available, parsing/suppression and lifting take \(O(n+m)\) word operations and \(O(n+m)\) words under a simple adjacency representation, including the \(n\)-symbol output and an \(m\)-arc verifier.

For a fixed parsed source and fixed deleted edge, the map from a supplied branch assignment to all original vertex colors has a Boolean circuit of \(O(n+m)\) gates: each internal output is a constant-table function of two three-bit endpoint colors, its orientation word and the deleted position. This circuit does not acquire the branch assignment.

A direct exhaustive candidate upper bound follows:

\[
O\!\left(q(4-L)5^{b-2}+n+m\right)
\]

work for one designated deletion, using rotation and complement pinning, and polynomial space. This is an exact upper bound, not the best project upper bound: the existing spanning-tree enumeration bound \(4^{b-1}\operatorname{poly}(n+m)\) may be asymptotically smaller. One branch search per thread suffices for all edge positions in that thread, but writing all \(m\) complete witnesses has its own \(\Omega(mn)\) output cost.

Status: PROVED/EXACT. The thread-position equivalence and independent extension were already proved in LSPV-1; the present run independently implements them and isolates the endpoint-complement restriction. This theorem is an upper-bound control, not an unrestricted circuit or time lower bound.

## Independent executable audit

The final script uses no project solver. It authenticates

\[
\operatorname{SHA256}(\texttt{source079.t5})
=\texttt{0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac}.
\]

Executed results:

* Exhausted all 30 orientation words of lengths one through four. It recovered exactly nine nontrivial relations for lengths at most three, proved every length-four word unrestricted in the finite check, and verified the polynomial root identity for all five endpoint differences.
* Parsed the 33-vertex, 44-arc source into 19 branch vertices and 30 threads: 20 of length one, six of length two and four of length three.
* An independently written five-domain propagation/DFS solver found the full core UNSAT in 39 recursive nodes.
* It performed 30 complement-pinned branch searches, one per omitted thread, totaling 335 recursive nodes with maximum 43.
* It canonically lifted those 30 assignments to all 44 original edge deletions. Every output satisfies every retained original arc and violates the omitted original arc. The full 33-color witnesses are in the raw JSON.

Status: COMPUTATIONAL for the finite source. The symbolic theorems do not depend on these node counts. This is an independent algorithmic reproduction, not independent external peer review.

## Literature and promise boundary

Bang-Jensen, Hell and MacGillivray prove NP-completeness of \(T\)-coloring for semicomplete \(T\) with more than one directed cycle:
https://doi.org/10.1137/0401029

Kun's Theorem 2 gives, for each fixed girth threshold and finite target-size bound, a polynomial construction preserving CSP membership:
https://arxiv.org/abs/0706.1701

Neither statement supplies a polynomial transformation whose output is a connected edge-minimal UNSAT source with a designated critical deletion, nor a uniform growing-girth reduction with a paid critical-edge finder and witness decoder. The literature search therefore does not close intrinsic-critical promise NP-hardness.

## Resource ledger and gates

Source acquisition is explicit; the source hash is recorded. Parsing, degrees, adjacency, suppression, relation construction, rotation choice, propagation, failed DFS branches, canonical lifting, output and verification are all executed in one run. Candidate acquisition is not treated as advice. The finite script stores the parsed source, domains, thread maps and complete witnesses; its asymptotic simple implementation uses linear words plus DFS state.

DISJ sanity: PASS as a control. A compact verifier does not imply a finder, and a large representation statistic does not imply general circuit hardness.

Relativization and algebrization: no separation is claimed. The GF(5) polynomial is itself a legal algebraic shortcut that any lower-bound candidate must accommodate. An unrestricted nonrelativizing bridge remains OPEN.

Simultaneous DTISP: PASS for the stated upper-bound realization only. No forbidden-region lower conclusion is drawn.

Deterministic configuration counting: NOT USED as a lower bound. The run and fixed-source lift circuits are consistent with standard upper configuration bounds.

Natural Proofs and proof-complexity transfer: NOT APPLICABLE to the exact structural upper lemmas; OPEN for any proposed unrestricted circuit lower bound.

## Status ledger and next blocker

PROVED/EXACT: polynomial thread normal form; critical endpoint-complement pinning; canonical linear-work lift given a branch assignment; one branch search serves every deletion position in its thread.

COMPUTATIONAL: exact path census and all 44 deletion witnesses for authenticated H33.

FALSIFIED: a backward traversal contributes base \(-1\); internal-thread multiplicity or the nine-relation alphabet alone forces large witness circuits; deletion positions in one thread require separate branch candidate acquisition.

OPEN: a uniform polynomial branch-assignment finder for the promised intrinsic-critical family; a source-preserving intrinsic-critical growing-girth NP-hardness reduction; an unrestricted witness-time lower bound; P versus NP.

Next blocker: attack branch-candidate acquisition on a genuinely growing family after quotienting every thread, using GF(5) polynomial-system structure, separator/treewidth DP and arbitrary elimination orders. Any lower-bound proposal must survive the compact \(O(q)\) verifier and the paid canonical lift without conflating verification with search.

Governance: additive red-team report only. No owner manuscript, title, schedule, role state or automation state was changed. A local repository checkout was unavailable, so repository preflight and LaTeX compilation were not run; connected source reads and publication readback are used instead.
