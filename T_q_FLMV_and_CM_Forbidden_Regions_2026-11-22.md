# Forbidden regions for compact T_q: time, workspace, and cumulative memory

22 November 2026, America/Los_Angeles

This note proves scoped forbidden regions for the previously constructed compact odd-tournament language. It derives cumulative-memory consequences from the FLMV time-space tradeoff after specifying the necessary memory-model assumptions. It also proves a separate input-inclusive physical-CM bound. None of these polynomial bounds settles P versus NP, and no historical novelty is claimed.

## 1. The problem and the size parameter

Let Q be the compact language established in the predecessor [3]. An input consists of a binary integer B>=2 and a Boolean circuit H defining the orientation of canonically ordered pairs i<j<B. A fixed interpreter supplies reverse edges and completes the base tournament to a regular tournament on q=2B+1 letters. The decision question has one unknown x and two clauses:

\[
\exists x<q:\quad R(x,0,1)\land R(2B,x,B),
\]

where R(a,b,c) requires a to beat exactly one of b,c and lose to the other; equality fails.

Write N for the complete compact description length. The circuit H is part of the input and varies between instances, even at the same q. The lower bound concerns this family of supplied circuits, not one prescribed cyclic tournament for each q.

The predecessor proves a local reduction from an eligible standard 3SAT source: an n-bit source produces N=O(n log n) output bits, each obtainable on demand in polylog(n) time and O(log n) workspace. The source format is chosen in the local Cook-Levin construction; no arbitrary SAT-text normalization is assumed. The simulator never stores the full reduced instance. This transfers simultaneous time/workspace exclusions with strict exponent slack.

For the reduction of a k-variable formula, q=2^{k+1}+5, but N also depends on the formula/circuit size. Consequently no single conversion from N to q captures every instance. All forbidden exponents below are in N.

## 2. The FLMV time-workspace region

For a>1, set

\[
f_0(a)=1,\qquad f_{j+1}(a)=\frac{a f_j(a)}{1+f_j(a)},
\]
\[
d_j(a)=\min\left\{\frac{1/f_j(a)-a}{j},\ a^{-j}\right\},
\qquad D(a)=\sup_{j\ge2}d_j(a).
\]

FLMV Theorem 5.7, equation (20), supplies the corresponding nondeterministic-linear-time exclusion. Its Section 3 gives the local completeness transfer. Thus, for Q, the simultaneous bounds

\[
T_A(N)\le N^{a+o(1)},\qquad
S_A(N)\le N^{b+o(1)}
\]

are impossible when 1<a<phi=(1+sqrt(5))/2 and b<D(a) [1]. Here A is one uniform correct deterministic algorithm, T_A and S_A are worst-case time and auxiliary workspace, and read-only input is excluded from workspace.

Equivalently, it suffices to exhibit one fixed j>=2 such that

\[
(a+jb)f_j(a)<1,\qquad b a^j<1.
\]

Strict inequalities let us enlarge the exponents slightly before applying the source theorem, absorbing the polylogarithmic costs of reduction and simulation.

The j=2 branch has the particularly simple expression

\[
d_2(a)=\frac12\left(\frac{a+2}{a^2}-a\right).
\]

It approaches 1 as a decreases to 1. Define D(1)=1 by this limiting boundary. We obtain:

**Near-linear-time consequence.** For every fixed epsilon>0, no Q solver has both

\[
T_A(N)\le N^{1+o(1)},\qquad
S_A(N)=O(N^{1-\epsilon}).
\]

Also, subpolynomial workspace excludes every fixed time exponent a<phi. These statements concern the original FLMV-derived region; they are not a claim that this is the sharp or latest known frontier.

## 3. A precise auxiliary-CM model

For an execution on input x, let s_t(x) be its live usable auxiliary storage in bits, including registers, addresses, and memory-management metadata. Define

\[
C_A(x)=\sum_{t=0}^{t_A(x)}\max\{1,s_t(x)\},\qquad
P_A(x)=\max_t s_t(x),
\]
\[
C_A(N)=\max_{|x|=N}C_A(x).
\]

The one-bit baseline charges elapsed steps even if no other workspace is live. The following assumptions are part of the theorem:

1. Input is read-only and excluded from s_t. Initial auxiliary state is s_0=polylog(N), with no free preprocessed table.
2. Each charged step creates at most g(N)=polylog(N) additional usable auxiliary bits. A bit-level charged implementation can take g=O(1). Operations over large blocks are charged throughout their actual execution, including operand residence.
3. The machine can be simulated in the FLMV model with at most polylogarithmic time and peak-workspace overhead. Bounded-word random access with counted addresses and an appropriate sparse-memory implementation is an intended example. This compatibility is an explicit hypothesis.
4. All preprocessing and computation occur inside the charged interval.

Bulk deletion after allocation is allowed. The argument below only requires a bound on upward growth.

**Peak-from-CM lemma.** Under these assumptions, pointwise on each execution,

\[
t_A(x)\le C_A(x),\qquad
P_A(x)=O\left(s_0+\sqrt{g(N)C_A(x)}\right).
\]

**Proof.** The first inequality follows from the baseline. Let P be the first attained peak. If P is comparable to s_0, the second bound is immediate. Otherwise bounded growth forces a preceding interval of order P/g steps during which at least P/2 bits were live. Its contribution is Omega(P^2/g). If P is comparable to g, the single peak snapshot already gives C>=P and the same conclusion up to constants. Rearranging proves the bound. QED.

This is not the generally false inference P<=C/T. Average memory can be far below peak memory. It is also not the inference C>=T*P: the correct general inequality is C<=O(T*max(1,P)). The lower estimate here is the area needed to build a peak under the growth rule.

FLMV's literal largest-ever-index space measure can jump on a random access, so it is not the s_t in this lemma. The stated model simulation connects live footprint to the theorem's workspace resource. Free arbitrary-size words or uncharged high-memory oracles do not satisfy the assumptions.

## 4. The derived time-CM forbidden region

Suppose a proposed Q solver satisfies

\[
T_A(N)\le N^{a+o(1)},\qquad
C_A(N)\le N^{\gamma+o(1)}.
\]

The peak lemma and the model simulation imply workspace at most N^{gamma/2+o(1)}. The time bound can be tightened to N^{r+o(1)}, where r=min(a,gamma), because T<=C. Thus, for a,gamma>=1, a certified forbidden region is

\[
\boxed{\quad r=\min\{a,\gamma\}<\varphi,
\qquad \gamma/2<D(r).\quad}
\]

At r=1 use D(1)=1 and choose a slightly larger fixed time exponent to absorb the overhead. Sublinear exponents can likewise be excluded by comparison with a slightly larger-than-linear cap.

**Near-linear-time CM theorem.** For every fixed epsilon>0, no solver in this model has both

\[
\boxed{T_A(N)\le N^{1+o(1)},\qquad
C_A(N)=O(N^{2-\epsilon}).}
\]

It suffices to prove this for 0<epsilon<1, since larger epsilon impose stronger caps. In that range the CM cap would give workspace N^{1-epsilon/2+o(1)}, which falls inside the near-linear FLMV exclusion. This is a forbidden uniform worst-case upper bound. It is not an assertion that every individual instance requires nearly quadratic CM.

**Standalone auxiliary-CM theorem.** Let alpha be the unique positive root of

\[
2\alpha^3-\alpha-2=0,
\qquad \alpha=1.165373043062414\ldots.
\]

For every fixed gamma<alpha, a bound C_A(N)<=N^{gamma+o(1)} is impossible under this model, without a separately imposed time bound.

To see this, use T<=C and the j=2 branch. For 1<=gamma<alpha,

\[
\gamma/2<d_2(\gamma)
\iff 2\gamma^3-\gamma-2<0.
\]

This puts the simulated algorithm inside the FLMV region. Smaller gamma are covered by a larger exponent below alpha. For example, C_A(N)=O(N^{1.16}) is excluded. This proof does not establish the boundary case gamma=alpha.

One convenient certified time-CM region is consequently

\[
\gamma<\max\{\alpha,2D(a)\}
\]

for 1<=a<phi, with D(1)=1. The first branch is the standalone exclusion; the second uses the separately given time cap. We do not need to assert that this exhausts all possible lower-bound arguments.

## 5. Numerical interior examples

The table uses safely rounded-down thresholds. For example, the row a=1.10 excludes all b<0.7309 and all gamma<1.4619. The two columns represent separate simultaneous exclusions with the displayed time cap; a solver need not satisfy both column caps to be excluded. Auxiliary-CM statements require Section 3's assumptions.

| Time cap | Forbidden workspace cap | Forbidden auxiliary-CM cap |
|---|---|---|
| N^{1+o(1)} | O(N^{1-epsilon}), any fixed epsilon>0 | O(N^{2-epsilon}), any fixed epsilon>0 |
| N^{1.05+o(1)} | N^{b+o(1)}, b<0.8582 | N^{gamma+o(1)}, gamma<1.7164 |
| N^{1.10+o(1)} | b<0.7309 | gamma<1.4619 |
| N^{1.15+o(1)} | b<0.6159 | gamma<1.2318 |
| N^{1.20+o(1)} | b<0.5111 | gamma<1.1653 |
| N^{1.30+o(1)} | b<0.3263 | gamma<1.1653 |
| N^{1.40+o(1)} | b<0.1844 | gamma<1.1653 |
| N^{1.50+o(1)} | b<0.0756 | gamma<1.1653 |
| N^{1.60+o(1)} | b<0.0063 | gamma<1.1653 |

The repeated CM threshold uses T<=C, so a small CM cap improves the nominal time cap. It should not be mistaken for a lower bound C>=T*S.

The finite numerical search is certified by

\[
f_j(a)>a-1,\qquad
d_j(a)<\frac{1/(a-1)-a}{j}.
\]

Once a positive candidate maximum is found, this upper bound rules out sufficiently large j. Numerical values, the cubic root, and exact rational interior examples were checked with the program in the appendix. These checks support arithmetic only; the asymptotic results follow from the proofs.

## 6. The project's input-inclusive physical CM

Let C_physical count all still-needed encoded input plus auxiliary memory over actual charged steps. Its relationship to the auxiliary theorem depends on the input interface.

**Read-only counted input.** If it remains separate from writable workspace, C_physical>=C_aux, so a small physical-CM cap also gives the auxiliary cap. If all N input bits stay resident throughout, C_physical>=N*T additionally holds. That residence term can make a near-quadratic physical cost automatic.

**Input initially usable as writable memory.** The execution starts with N usable bits. One cannot apply the small-initial-workspace peak lemma to that total footprint. Counting those bits for a short time is different from charging their construction. A separate argument is required.

For the self-contained, bounded-acquisition model used in our preceding physical-CM proof, such a separate argument is available even for compact T_q.

**Physical input-residence theorem.** There is a family of compact inputs of lengths N_r=Theta(r log r) forcing

\[
\boxed{C_{\rm physical}=\Omega(r^2)
=\Omega(N_r^2/\log^2N_r).}
\]

Assume each actual charged microstep acquires at most O(1) input-bit dependencies; every storage location initially depends on at most one independent input bit; deletion cannot inspect or aggregate contents for free; and deleted input cannot be recovered through an uncharged external store. Preprocessing is charged. Memory-management and control state also count.

**Construction.** Set k=2, B=6, q=13. Let a supplied circuit F have r independent constant-gate bits beta_1,...,beta_r and compute

\[
F(y)=\bigvee_{i=1}^r\beta_i,
\]

independently of its two assignment inputs. Compile it into

\[
H_F(i,j)=\neg\bigl([i=0]\land[j\ge2]\land
F((j-2)\bmod4)\bigr).
\]

The earlier tournament equivalence makes Q's answer exactly OR_i beta_i. Constant 0/1 gate records differ only in their Boolean value. Fixed-width gate records give N_r=Theta(r log r); structural fields are fixed across the family. The regular completion guarantees that every input is a valid regular tournament description.

**Proof of the bound.** Run a correct deterministic algorithm on the all-zero input. If beta_i has not been acquired, flipping just that bit remains consistent with everything read but changes the answer to SAT. The algorithm therefore must eventually acquire each beta_i. Before acquisition, no computed aggregate, control state, or address can depend on it; any existing representation is a passive surviving copy of its original representation. Deleting its last representation would make the zero input indistinguishable from a yes-input. Hence at least one distinct live bit must remain for each unacquired beta_i. After t bounded-acquisition steps at least r-O(t) such bits remain. Summing this triangular residence bound gives Omega(r^2). Bulk deletion of irrelevant data does not affect the argument. QED.

With g=polylog(N) dependencies acquired per charged step, the proof gives Omega(r^2/g), preserving the exponent-2 exclusion up to polylogarithms. In particular, no uniform physical-CM bound O(N^{2-epsilon}) holds on this family for fixed epsilon>0.

This physical theorem even works at fixed q=13. It is an encoded-input residence lower bound already present for ordinary OR. It does not establish an exponential search requirement or growing-alphabet SAT hardness, and it does not forbid a polynomial-time solver.

## 7. Explicit-table comparison and proof boundary

For the earlier explicit full-row family with d=Theta(q) residual clauses, N=Theta(q^2). The charged block algorithm attains T=Theta(N), O(log N) auxiliary workspace, and Theta(N^2) physical CM under its stated model. This is consistent with every theorem above: it receives the expanded table and does not solve the compact circuit language in the same input length.

The compact local reduction proves a genuine FLMV forbidden region. The peak-from-CM lemma adds an auxiliary-CM forbidden region under a declared growth and simulation model. The OR-family argument independently adds a physical-CM input-residence floor. None justifies importing pebbling or resolution lower bounds into unrestricted SAT solving; the broader CM literature studies several different computational models [2].

The remaining P-versus-NP task would require excluding every polynomial-time bound or supplying a polynomial-time algorithm. The regions proved here have fixed polynomial thresholds and permit either possibility.

## Appendix: complete arithmetic-verification program

```python
from fractions import Fraction


def flmv_curve(a):
    """Use exact rational arithmetic for the input decimal and tail test."""
    if not 1.0 < a < (1.0 + 5.0 ** 0.5) / 2.0:
        raise ValueError("a must lie strictly between 1 and the golden ratio")
    a = Fraction(str(a))
    f = Fraction(1)
    best_value = Fraction(0)
    best_depth = 0
    for depth in range(1, 100000):
        f = a * f / (1 + f)
        if depth < 2:
            continue
        value = min((1 / f - a) / depth, a ** (-depth))
        if value > best_value:
            best_value = value
            best_depth = depth
        future_upper = (1 / (a - 1) - a) / (depth + 1)
        if best_value > 0 and future_upper <= best_value:
            return float(best_value), best_depth
    raise RuntimeError("Stopping bound was not reached")


def cm_crossover():
    lower, upper = 1.0, 1.3
    for _ in range(80):
        middle = (lower + upper) / 2.0
        if 2.0 * middle ** 3 - middle - 2.0 < 0.0:
            lower = middle
        else:
            upper = middle
    return (lower + upper) / 2.0


def main():
    alpha = cm_crossover()
    assert abs(2.0 * alpha ** 3 - alpha - 2.0) < 1e-13
    assert abs(flmv_curve(alpha)[0] - alpha / 2.0) < 1e-12
    print(f"Standalone auxiliary-CM crossover: {alpha:.15f}")
    for a in [1.05, 1.10, 1.15, 1.20, 1.30, 1.40, 1.50, 1.60, 1.61]:
        d, depth = flmv_curve(a)
        cm_threshold = max(alpha, 2.0 * d)
        print(f"a={a:.2f}, D(a)={d:.10f}, depth={depth}, "
              f"certified CM threshold={cm_threshold:.10f}")
    for a, b in [(Fraction(11, 10), Fraction(73, 100)),
                 (Fraction(6, 5), Fraction(51, 100))]:
        f2 = a * a / (2 + a)
        assert (a + 2 * b) * f2 < 1
        assert b * a * a < 1
    print("Crossover and exact rational interior checks passed")


if __name__ == "__main__":
    main()
```

## References

1. Lance Fortnow, Richard Lipton, Dieter van Melkebeek, and Anastasios Viglas. *Time-Space Lower Bounds for Satisfiability*. Journal of the ACM 52(6), 835–865, 2005. Sections 2.1 and 3; Theorem 5.7, equation (20), and Corollary 5.8. https://lance.fortnow.com/papers/files/tst.pdf
2. Paul Beame and Niels Kornerup. *Cumulative Memory Lower Bounds for Randomized and Quantum Computation*. ICALP 2023, LIPIcs 261, Article 17. https://doi.org/10.4230/LIPIcs.ICALP.2023.17
3. Project predecessor: *A resource-preserving FLMV lower bound for the compact odd-tournament problem*, 22 November 2026. https://chatgpt.com/library?file_id=libfile_819cb832841c8191b34eeeb439538d96&account_id=personal