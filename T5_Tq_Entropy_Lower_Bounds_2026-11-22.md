# Entropy lower bounds for ordered T5 and compact T_q

22 November 2026, America/Los_Angeles.

Status: scoped symbolic theorems with finite semantic checks. No unrestricted superpolynomial decision lower bound, P versus NP resolution, historical novelty, or independent review is claimed.

## 1. What can be proved

For both the ordered fixed T5 problem and the compact regular-tournament language Q defined below, there are encoded instances consisting of an initial part depending on k independent bits Z, followed by a short query selecting one bit. Their satisfiability answer is exactly Z_i.

Consequently, a summary that must answer every later query without rereading the initial input needs k bits when exact. If each query has error at most epsilon < 1/2, its information capacity is at least

$$
k(1-h_2(\epsilon)),
\qquad h_2(p)=-p\log_2p-(1-p)\log_2(1-p).
$$

A one-pass sequential streaming solver must preserve this information at every intermediate prefix. Under the faithful state-accounting convention in Section 4, this gives expected, hence worst-case, cumulative auxiliary memory Omega(k^2) for any fixed epsilon < 1/2. The constructed encodings have N = Theta(k log(k+2)) bits, so these are Omega(N/log N) retained-space and Omega(N^2/log^2 N) cumulative-memory bounds on that family.

These are continuation/streaming theorems. An unrestricted offline solver can read the query first or revisit the initial data. The same family then has a simple small-workspace solution. This limitation is demonstrated explicitly below.

## 2. Exact ordered T5 embedding

Use values 0,...,4, with a beating b exactly when (b-a) mod 5 belongs to {1,3}. The ordered clause R(a,b,c) requires three distinct values and one win and one loss for its first value.

Define a derived clause

$$
C(a,b,c)=R(a,b,c)\land R(b,a,c).
$$

This means that the three values form a directed cycle. Its unordered satisfying triples are 012, 123, 234, 340, 401. This conversion is essential: C has 30 ordered tuples and R has 40. They are different relations.

Introduce anchor variables a_0,...,a_4 and impose

$$
\mathcal A=\bigwedge_{j=0}^4 C(a_j,a_{j+1},a_{j+2}),
$$

with subscripts modulo 5. Every anchor pair occurs in a clause, forcing all five values to differ. The satisfying frames are exactly a_j=s+j or a_j=s-j modulo 5, for ten frames. One way to see completeness is that the complements of the allowed triples are the edges of a five-cycle; the frame assignment must be an automorphism of this cycle.

Relative to any frame, the pin clauses

$$
P_0(X)=C(a_1,a_4,X),\qquad P_1(X)=C(a_2,a_4,X)
$$

force X=a_0 and X=a_3, respectively. No input constants, primitive domain restrictions, NOT literals, or additional clause types are required: each C is expanded into two ordinary R clauses.

For z in {0,1}^k define the prefix

$$
F_z=\mathcal A\land\bigwedge_{j=1}^kP_{z_j}(X_j).
$$

The suffix query selecting i is P_1(X_i). Therefore

$$
\boxed{\operatorname{SAT}(F_z\land P_1(X_i))=z_i.}
$$

If z_i=1, there are exactly ten satisfying assignments, one per anchor frame. If z_i=0, the two pins on X_i conflict in every frame. There are k+5 variables and 2k+12 ordered R clauses, including the query. Fixed-width identifiers give N=Theta(k log(k+2)). The query is two clauses occupying O(log(k+2)) bits. Headers can have the same length and values for every z and i.

The exact query-answer vector is z. Thus the 2^k prefixes are pairwise distinguishable by legitimate future T5 constraints. Large distinguishability is established by these explicit suffixes, not inferred from the number of potential witnesses.

## 3. Embedding in the compact T_q definition

Use the actual compact language from the companion chat. Its input is B in binary and a Boolean circuit H defining the orientation of canonical base pairs a<b<B. A fixed interpreter supplies reverse edges and makes the base tournament regular on q=2B+1 vertices. The question is

$$
\exists x<q:\ R(x,0,1)\land R(2B,x,B).
$$

For completeness, the regular completion has originals v_a, copies v'_a, and vertex w=2B. Within originals and within copies keep the base tournament. For a!=b, v_a beats v'_b iff v_b beats v_a. Each original beats its own copy; w beats all originals; every copy beats w. Every vertex has B wins. The second displayed clause permits exactly the original vertices as x.

Take k=2^ell, ell>=1, B=k+2, and q=2k+5. Let z be a k-bit table and i an ell-bit query. Construct

$$
F_{z,i}(y)=z_y\land[y=i],\qquad 0\le y<k.
$$

A binary multiplexer tree evaluates z_y using O(k) bounded-fan-in Boolean gates; the equality test costs O(ell) gates. Store the z bits in constant-gate records and the query bits in a later block of constant-gate records. Include gates for arithmetic and guards as in the prior compiler, and define on canonical pairs

$$
H_{z,i}(a,b)=\neg\bigl([a=0]\land[b\ge2]\land
F_{z,i}((b-2)\bmod k)\bigr).
$$

All topology and record positions are fixed for a given k. The z constants and all their multiplexer gates can precede the i constants, with the equality and final guard gates following those constants. Thus the encoded input factors into a prefix depending only on z and a suffix depending only on i. All gate references can be topological. The full description has O(k) gates and N=Theta(k log k) bits in a fixed-width gate-list encoding.

Vertex u_y=2+y passes the first clause precisely when F_{z,i}(y)=1, and the second clause excludes the copied and special vertices. Hence

$$
\boxed{Q(H_{z,i},B)=z_i.}
$$

The unique possible witness is u_i. The alphabet size is linear in k on this INDEX family. The earlier SAT reduction instead used q exponential in the Boolean variable count. Those are different parameterizations of the same compact language, not contradictory formulas.

This concerns a supplied orientation circuit varying with the instance, not a single prescribed cyclic tournament at each q. No unproved transfer to that different fixed-cyclic problem is made.

## 4. Entropy theorem for retained summaries

Let Z be uniform on {0,1}^k. Let M be the complete information retained after the z-dependent prefix and before seeing i. Assume the decoder sees M and i but cannot revisit the prefix. Include all continuation-relevant private state, addresses and stored information in M. Public random coins W may be independent of Z; condition on W throughout. Hidden input-dependent clocks or storage locations are not free side channels.

For an exact deterministic solver, two different z vectors cannot give the same M: choose a differing coordinate as the suffix query. Thus M determines Z and

$$
H(Z\mid M)=0,\qquad H(M)\ge I(Z;M)=k.
$$

For bounded error, suppose every z,i is answered with error at most epsilon<1/2. The decoder for each coordinate yields, by the binary Fano inequality,

$$
H(Z_i\mid M,W)\le h_2(\epsilon).
$$

Fresh decoder randomness cannot beat the optimal estimator based on M,W, so the inequality applies also to randomized continuations. Conditional subadditivity gives

$$
H(Z\mid M,W)\le\sum_iH(Z_i\mid M,W)\le k h_2(\epsilon),
$$

and independence of Z and W implies

$$
\boxed{I(Z;M\mid W)\ge k(1-h_2(\epsilon)).}
$$

If the state uses a fixed S-bit representation, then I(Z;M|W)<=S. For variable-length states, use a faithful prefix-free serialization and charge its length L(M). The source-coding inequality gives E L(M)>=H(M|W), and hence the same lower bound on expected charged length. Ordinary fully accounted physical storage simulates such a serialization up to constants and routine bookkeeping terms. A physical convention that gives arbitrary addresses, free timing information, or an external original-input oracle away does not satisfy this theorem's interface.

For illustration, epsilon=0 gives k bits; epsilon=0.1 gives about 0.5310k; epsilon=1/3 gives about 0.0817k. A 2^k family forces k retained bits, not 2^k retained bits.

This is the classical random-access-code/one-way INDEX entropy argument embedded into these exact constraint languages. Nayak's primary paper proves the stronger quantum random-access-code bound in its own setting [3]. We use the elementary classical proof above and assert no new general information theorem.

## 5. A cumulative entropy theorem along the same execution

Consider a one-pass forward sequential stream. The prefix reveals z_1,...,z_k in order, followed later by the query i. For T5 the revealed item is a complete two-R-clause pin block; for compact T_q it can be a constant-gate record. The solver may compute arbitrarily between arrivals but cannot reread consumed input or inspect the suffix early. Each record boundary occurs at a distinct charged transition. All computation, including preprocessing, is inside the accounting interval.

Let M_j be the complete state just after consuming the j-th data record. At this point the solver must still handle every later query. The unread future z_{j+1},...,z_k is independent of the first j bits and of M_j, conditional on independent public coins. A decoder can supply those future independent bits and any chosen index i<=j, then simulate the continuation. Correctness on all completions yields

$$
I(Z_1,\ldots,Z_j;M_j\mid W)\ge j(1-h_2(\epsilon)).
$$

For exact solvers this also follows directly: if two length-j prefixes share a state, use the same remaining data and query a coordinate on which the prefixes differ.

Charge a faithful prefix-free state serialization at every step, as above. Averaging over the same uniform data distribution and independent query/coins, and summing only the distinct boundary times on each execution,

$$
\begin{aligned}
\mathbb E[CM_{\rm aux}]
&\ge\sum_{j=1}^k\mathbb E[L(M_j)]\\
&\ge(1-h_2(\epsilon))\sum_{j=1}^kj\\
&=(1-h_2(\epsilon))\frac{k(k+1)}2.
\end{aligned}
$$

Fixed control and physical-serialization conventions can add constant-factor or bookkeeping adjustments without changing the quadratic asymptotic result. This is not a product of separately attained worst cases: all selected events belong to the same execution, and the expectation uses a single distribution. Randomized bounds concern expected costs, with a corresponding worst-case expectation over inputs.

Therefore, under this streaming interface, there is a genuine forbidden region

$$
S_{\rm retained}=o(k)\quad\text{or}\quad CM_{\rm aux}=o(k^2)
$$

for any fixed error bounded below 1/2 by a constant. In encoded length, the corresponding family bounds are Omega(N/log N) and Omega(N^2/log^2 N).

This auxiliary-CM argument excludes the read-only input from storage. It uses obligatory retention of information already consumed, rather than the older theorem requiring unread physical input to remain resident. It requires sequential acquisition and later unknown queries, so it is not an unrestricted offline CM theorem.

## 6. Rereading defeats the proposed unrestricted transfer

For the constructed T5 family, an offline algorithm can read i first, then inspect the pin on X_i. On the promised family this uses O(log N) workspace and only a constant number of fixed-width record accesses. With bit-cost addressing, the query can be resolved in polylogarithmic time. A general solver can recognize the template with a scan and dispatch to this method, without mistaking the promise shortcut for an algorithm on every T5 input.

For the compact circuit family, the fixed layout makes the i constants and the selected z_i constant directly locatable. The same shortcut applies on the promised templates. If input is available only as a resettable sequential stream, a second pass can recover z_i using O(log k) auxiliary bits and linear scanning work. Both are legal alternatives outside the one-pass theorem.

For a single INDEX query, one must not assert S + communication >= k after allowing communication in both directions. The query index itself can be sent in O(log k) bits, and the selected bit returned in one bit. This is precisely why a one-way summary bound is not a general time-space lower bound.

## 7. Why ordinary Shannon entropy does not finish the SAT argument

For an N-bit encoded random instance F and any deterministically specified solution table V(F),

$$
H(V(F))\le H(F)\le N.
$$

The vector may have exponentially many entries. Its entries need not be independent, and its Shannon entropy cannot exceed the entropy of its compact source. For a decision bit B=SAT(F), H(B)<=1 and H(B|F)=0. Likewise, a complete self-contained deterministic configuration determines its eventual answer even when computing that answer is expensive.

These observations do not prove efficient computation. Shannon entropy allows arbitrarily expensive decoding. They explain why counting candidate assignments or measuring uncertainty conditional on the full input cannot by itself produce the sought runtime lower bound.

Entropy can nevertheless support superlinear or larger computation bounds when a model forces repeated costly movement of the same information. The sole-tape crossing proofs in the earlier handoff are an example. The current theorem gives another, explicitly one-pass, mechanism. Neither mechanism follows merely from the SAT/UNSAT output having to be correct.

## 8. The exact missing unrestricted lemma

An unrestricted continuation would need, for every candidate fast solver, genuine reconstruction tasks U_j with allowed side information V_j and charged records R_j such that the record really permits decoding U_j. If total conditional information demand is D and every charged event can supply at most b bits and is counted in at most rho records, an appropriate coding/overlap proof would give

$$
T\ge D/(b\rho)
$$

up to explicitly accounted coding overhead. A residence version must instead force the information to remain in the counted live state at distinct execution times, as Section 5 does.

The open requirement is to derive those compulsory tasks and bounded overlap from unrestricted T5/Q decision correctness despite rereading, query reordering, shared circuits, algebraic summaries, caching and recomputation. It is not enough that hypothetical separate queries could reconstruct a large object: their costs cannot be charged to an execution that answers only one query.

Another route is computational or time-bounded information rather than ordinary entropy. That requires a target-specific hardness or decoder-cost theorem; assuming that useful summaries are computationally inaccessible would assume the main missing conclusion.

## 9. Validation and relation to the newest CM note

The companion verification script exhaustively found the ten anchor frames and checked the pin identities. It then enumerated all assignments for 98 T5 data/query instances with k=1,...,4, confirming counts 10 z_i, and checked 2,120 compact tournament instances for k in {2,4,8}, confirming regularity and the exact witness set {i+2} when z_i=1, empty otherwise. Query signatures had size 2^k for the T5 tests. These are finite semantic checks, not empirical evidence for asymptotic entropy bounds. The O(k)-gate circuit layout is established symbolically; the script evaluates the semantic orientation rule rather than serializing a gate-level compiler.

The newer companion note [2] derives an auxiliary-CM forbidden region from FLMV using a bounded-growth peak-from-CM lemma. That advances beyond the earlier GitHub status note's statement that no such compact-target CM consequence had been established. This report does not independently re-audit the FLMV numerical frontier and does not rely on it: the entropy results here follow from the explicit INDEX embeddings and their stated interface restrictions.

No new GitHub publication, agent activation, or independent formal verification is claimed in this run.

## References

1. Project, T5 Resource Lower Bounds Exhaustive Handoff, 2026-11-21, Sections 3 and 7. https://chatgpt.com/library?file_id=libfile_2cf919dee5408191b085987af47517b5&account_id=personal
2. Project, T_q FLMV and CM Forbidden Regions, 2026-11-22. https://chatgpt.com/library?file_id=libfile_12e7c9e98f948191a775423cc98dcfc8&account_id=personal
3. Ashwin Nayak, Optimal lower bounds for quantum automata and random access codes, FOCS 1999; arXiv:quant-ph/9904093. Primary author manuscript: https://www.math.uwaterloo.ca/~anayak/papers/Nayak99.pdf . Used for context on random-access-code entropy bounds; the proof in Section 4 is classical and supplied here.
4. Paul Beame and Niels Kornerup, Cumulative Memory Lower Bounds for Randomized and Quantum Computation, ICALP 2023, LIPIcs 261, Article 17. https://doi.org/10.4230/LIPIcs.ICALP.2023.17 . Used to distinguish cumulative memory from peak-space products and restricted pebbling models; no SAT-specific theorem is imported from this paper.

## Appendix: executed verification program

```python
from itertools import product
import json


def beats5(a, b):
    return (b - a) % 5 in (1, 3)


def ordered5(a, b, c):
    return len({a, b, c}) == 3 and beats5(a, b) != beats5(a, c)


def cyclic5(a, b, c):
    return ordered5(a, b, c) and ordered5(b, a, c)


def anchor_ok(a):
    return all(cyclic5(a[i], a[(i+1) % 5], a[(i+2) % 5])
               for i in range(5))


def pinned(a, value, bit):
    return cyclic5(a[1 if bit == 0 else 2], a[4], value)


def compact_wins(z, query, a, b):
    k = len(z)
    base = k + 2
    special = 2 * base
    if a == b:
        return False
    if a == special:
        return b < base
    if b == special:
        return a >= base
    a_copy, b_copy = a >= base, b >= base
    i, j = a % base, b % base

    def original(u, v):
        if u == v:
            return False
        if u > v:
            return not original(v, u)
        if u == 0 and v >= 2:
            y = v - 2
            return not (z[y] and y == query)
        return True

    if a_copy == b_copy:
        return original(i, j)
    if not a_copy:
        return True if i == j else original(j, i)
    return False if i == j else original(j, i)


def main():
    frames = [a for a in product(range(5), repeat=5) if anchor_ok(a)]
    assert len(frames) == 10
    for a in frames:
        for bit in (0, 1):
            accepted = [v for v in range(5) if pinned(a, v, bit)]
            assert accepted == [a[0 if bit == 0 else 3]]

    t5_cases = 0
    for k in range(1, 5):
        signatures = set()
        for z in product((0, 1), repeat=k):
            signature = []
            for query in range(k):
                count = 0
                for a in frames:
                    for values in product(range(5), repeat=k):
                        if (all(pinned(a, values[j], z[j]) for j in range(k))
                                and pinned(a, values[query], 1)):
                            count += 1
                assert count == 10 * z[query], (k, z, query, count)
                signature.append(int(count > 0))
                t5_cases += 1
            signatures.add(tuple(signature))
        assert len(signatures) == 2 ** k

    compact_cases = 0
    for k in (2, 4, 8):
        base, q = k + 2, 2 * k + 5
        for z in product((0, 1), repeat=k):
            for query in range(k):
                w = [[compact_wins(z, query, a, b) for b in range(q)]
                     for a in range(q)]
                assert all(sum(row) == base for row in w)
                assert all(w[a][b] != w[b][a]
                           for a in range(q) for b in range(a))

                def rel(a, b, c):
                    return len({a, b, c}) == 3 and w[a][b] != w[a][c]

                accepted = [x for x in range(q)
                            if rel(x, 0, 1) and rel(2 * base, x, base)]
                assert accepted == ([query + 2] if z[query] else [])
                compact_cases += 1
    print(json.dumps({'anchor_frames': len(frames),
                      't5_instances_exhaustively_counted': t5_cases,
                      'compact_tq_instances_checked': compact_cases,
                      'status': 'all checks passed'}, indent=2))


if __name__ == '__main__':
    main()
```
