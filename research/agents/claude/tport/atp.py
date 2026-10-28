#!/usr/bin/env python3
"""Alternation-trading proof engine with portfolio residual blocks (CLAUDE TPORT-0001).

Lines follow Williams, "Alternation-Trading Proofs, Linear Programming, and Lower
Bounds" (STACS 2010, arXiv:1001.0746), Definition 3.1:

    (Q_1 n^{a_1})^{b_2} (Q_2 n^{a_2})^{b_3} ... (Q_k n^{a_k})^{b_{k+1}} DTS[n^{a_{k+1}}]

Each block stores its exponent a, its stage-input exponent sigma (= b_i, the
length exponent of the input to the computation that starts at this block),
and, for log-width blocks, a width w (the block ranges over n^w values).  The
predicate stores its input exponent beta (= b_{k+1}) and time exponent t.

Rules (x is a fresh LP variable, 0 <= x <= t):
  S  Speedup Rule 1 on the last block (Williams).  If the last block is a
     residual, this is the free absorption: the residual's O(log n) bits merge
     into the new configuration guess.
  T  Speedup Rule 2 (Williams).  Optional; Williams shows it is never needed in
     his system.
  D  Slowdown under the portfolio assumption SAT in E^{d log N} DTS[N^c]:
     the removed Q_k-computation becomes a residual block (Q_k, width d*M)
     followed by DTS[n^{cM}], M = max{a_{k+1}, a_k, b_k, b_{k+1}}.
     With d = 0 the residual is free and D followed by B is Williams' slowdown.
  B  Brute-force the last residual: DTS[n^t] -> DTS[n^{t+w}].

A proof starts from (E log[e])^{b_1} DTS[n^{a0}] and ends at a single residual
of the same type with time <= a0.  The end is a contradiction by the
limited-nondeterminism time hierarchy (report, Lemma H).  For d = 0 this is the
same end condition as Williams' normal form.

Homogeneous mode (default) sets the original input exponent to 0 and a0 = 1.
It gives the supremum over a0 -> infinity of Williams' non-homogeneous LP,
because every rule is positively homogeneous except the constants b_1 = 1.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import linprog

EXISTS, FORALL = 1, -1


@dataclass
class Block:
    q: int            # EXISTS or FORALL
    kind: str         # 'big', 'log', 'res'
    a: object         # var index or 0.0
    sigma: object     # var index or constant
    w: object = 0.0   # width (log/res blocks)


@dataclass
class LPBuilder:
    nvar: int = 0
    rows: list = field(default_factory=list)   # (coef dict, rhs, c_coef dict)
    xvars: list = field(default_factory=list)  # speedup parameters, in order
    tfinal: object = None

    def var(self):
        self.nvar += 1
        return self.nvar - 1

    def le(self, lhs, rhs):
        """Add constraint sum lhs <= sum rhs, where each side is a list of
        (coef, term) with term a var index, a float constant, or ('c', var)
        meaning c * var (c substituted at solve time)."""
        coef, ccoef, const = {}, {}, 0.0
        for sign, side in ((1.0, lhs), (-1.0, rhs)):
            for k, term in side:
                if isinstance(term, tuple) and term[0] == 'c':
                    ccoef[term[1]] = ccoef.get(term[1], 0.0) + sign * k
                elif isinstance(term, int):
                    coef[term] = coef.get(term, 0.0) + sign * k
                else:
                    const += sign * k * float(term)
        self.rows.append((coef, -const, ccoef))

    def ge(self, lhs_var, *terms):
        """lhs_var >= each term (a term is var, const, or (coef, term))."""
        for t in terms:
            if isinstance(t, tuple) and len(t) == 2 and not (t[0] == 'c'):
                k, tt = t
            else:
                k, tt = 1.0, t
            self.le([(k, tt)], [(1.0, lhs_var)])


class ProofError(Exception):
    pass


def build(annotation, d, homogeneous=True, min1=False):
    """Build the LP skeleton for an annotation string over {S,T,D,B}."""
    L = LPBuilder()
    one = 0.0 if homogeneous else 1.0
    if homogeneous:
        a0 = 1.0
    else:
        a0 = L.var()
        L.ge(a0, 1.0)
    line = [Block(EXISTS, 'res', 0.0, one, 0.0)]   # start log block, width free
    beta, t = one, a0
    speedups = 0
    for op in annotation:
        if not line:
            raise ProofError('empty line before end')
        last = line[-1]
        if op in 'ST':
            x = L.var()
            L.xvars.append(x)
            L.le([(1.0, x)], [(1.0, t)])               # x <= t
            tn = L.var()
            L.le([(1.0, t), (-1.0, x)], [(1.0, tn)])   # tn >= t - x
            if min1:
                L.ge(tn, 1.0)
            if op == 'S':
                an = L.var()
                L.ge(an, last.a if isinstance(last.a, int) else float(last.a), x)
                sig = L.var()
                L.ge(sig, x, beta if isinstance(beta, int) else float(beta))
                line[-1] = Block(last.q, 'big', an, last.sigma, 0.0)
                line.append(Block(-last.q, 'log', 0.0, sig, x))
            else:
                # Rule 2.  After a residual of type Q this appends
                # (not-Q n^x)(Q log) and buries the residual.
                an = L.var()
                L.ge(an, x)
                sig2 = L.var()
                L.ge(sig2, x, beta if isinstance(beta, int) else float(beta))
                line.append(Block(-last.q, 'big', an, beta, 0.0))
                line.append(Block(last.q, 'log', 0.0, sig2, x))
            t = tn
            speedups += 1
        elif op == 'D':
            if last.kind == 'res':
                raise ProofError('D on residual')
            M = L.var()
            for term in (t, last.a, last.sigma, beta):
                L.ge(M, term if isinstance(term, int) else float(term))
            tn = L.var()
            L.le([(1.0, ('c', M))], [(1.0, tn)])       # tn >= c M
            w = L.var()
            L.le([(d, M)], [(1.0, w)])                 # w >= d M
            line[-1] = Block(last.q, 'res', 0.0, last.sigma, w)
            beta, t = last.sigma, tn
        elif op == 'K':
            # Skolemization at the rightmost pattern A, R(res), X(big):
            #   Q r . notQ z . rest  ==  notQ (z_r)_r . Q r . rest
            # The table (n^{x+w} bits) merges into A (same type as X); r merges
            # into the next block Y (same type as R), or stays as a residual
            # in front of the predicate if X was last.  Stage inputs of the
            # merged r-block grow to include the table; deeper stages copy
            # z_r and keep their old inputs.
            pos = None
            for i in range(len(line) - 2, 0, -1):
                if line[i].kind == 'res':
                    pos = i
                    break
            if pos is None:
                raise ProofError('K not applicable')
            A, R, X = line[pos - 1], line[pos], line[pos + 1]
            tbl = L.var()
            # X may be big (exponent a_X) or log/res (exponent 0): the table
            # has n^{a_X + w} bits up to log factors.
            L.le([(1.0, X.a if isinstance(X.a, int) else float(X.a)),
                  (1.0, R.w)], [(1.0, tbl)])         # tbl >= a_X + w
            an = L.var()
            L.ge(an, A.a if isinstance(A.a, int) else float(A.a), tbl)
            Anew = Block(A.q, 'big', an, A.sigma, 0.0)
            if pos + 2 < len(line):
                Y = line[pos + 2]
                sig = L.var()
                L.ge(sig, *[s if isinstance(s, int) else float(s)
                            for s in (Y.sigma, R.sigma)], tbl)
                if Y.kind == 'big':
                    Ynew = Block(Y.q, 'big', Y.a, sig, 0.0)
                else:
                    wn = L.var()
                    L.le([(1.0, Y.w), (1.0, R.w)], [(1.0, wn)])
                    Ynew = Block(Y.q, Y.kind, 0.0, sig, wn)
                line = line[:pos - 1] + [Anew, Ynew] + line[pos + 3:]
            else:
                sig = L.var()
                L.ge(sig, R.sigma if isinstance(R.sigma, int) else float(R.sigma), tbl)
                line = line[:pos - 1] + [Anew, Block(R.q, 'res', 0.0, sig, R.w)]
        elif op == 'B':
            if last.kind != 'res':
                raise ProofError('B on non-residual')
            if len(line) == 1:
                raise ProofError('B on final residual is never needed')
            tn = L.var()
            L.le([(1.0, t), (1.0, last.w)], [(1.0, tn)])
            line.pop()
            beta, t = last.sigma, tn
        else:
            raise ProofError('unknown op ' + op)
    if not (len(line) == 1 and line[0].kind == 'res' and line[0].q == EXISTS
            and speedups > 0):
        raise ProofError('does not end at a single E-residual')
    L.le([(1.0, t)], [(1.0, a0)])                       # final time <= a0
    L.tfinal = t
    return L


def solve(L, c):
    """Minimize the final time at fixed c; returns the scipy result."""
    n = L.nvar
    A = np.zeros((len(L.rows), n))
    b = np.zeros(len(L.rows))
    for i, (coef, rhs, ccoef) in enumerate(L.rows):
        for j, v in coef.items():
            A[i, j] += v
        for j, v in ccoef.items():
            A[i, j] += c * v
        b[i] = rhs
    obj = np.zeros(n)
    if isinstance(L.tfinal, int):
        obj[L.tfinal] = 1.0
    return linprog(obj, A_ub=A, b_ub=b, bounds=[(0, None)] * n, method='highs')


def feasible(L, c):
    n = L.nvar
    if n == 0:
        return True
    A = np.zeros((len(L.rows), n))
    b = np.zeros(len(L.rows))
    for i, (coef, rhs, ccoef) in enumerate(L.rows):
        for j, v in coef.items():
            A[i, j] += v
        for j, v in ccoef.items():
            A[i, j] += c * v
        b[i] = rhs
    res = linprog(np.zeros(n), A_ub=A, b_ub=b, bounds=[(0, None)] * n,
                  method='highs')
    return res.status == 0


def best_c(annotation, d, homogeneous=True, min1=False, lo=1.0, hi=2.2,
           tol=1e-6):
    """Largest c for which the annotation's LP is feasible (bisection).
    Returns lo if infeasible at lo."""
    L = build(annotation, d, homogeneous, min1)
    if not feasible(L, lo):
        return None
    if feasible(L, hi):
        return hi
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if feasible(L, mid):
            lo = mid
        else:
            hi = mid
    return lo


def williams_to_ops(bits):
    """Williams annotation (1 = speedup, 0 = slowdown) -> ops, inserting the
    brute-force step after every slowdown except the last."""
    ops = []
    for i, bit in enumerate(bits):
        if bit == 1:
            ops.append('S')
        else:
            ops.append('D')
            if i < len(bits) - 1:
                ops.append('B')
    return ''.join(ops)


if __name__ == '__main__':
    for bits, expect in (([1, 0, 0], 2 ** 0.5), ([1, 1, 0, 0, 1, 0, 0], 1.6004)):
        ops = williams_to_ops(bits)
        print(bits, ops, 'd=0:', round(best_c(ops, 0.0), 4), 'expected', round(expect, 4),
              'd=1:', best_c(ops, 1.0, lo=0.5))
