#!/usr/bin/env python3
"""Randomized check of the barrier potential for CLAUDE TPORT-0001.

Lines are simulated numerically (concrete exponents).  For random valid rule
sequences with random parameters we evaluate

  Phi0(L): bottom-up cost; inner big blocks s*max(next, a, sigma, sigma_next),
           inner log/res blocks min(next + w, s*max(next, sigma, sigma_next)),
           outer big block c*max(...), outer residual free;  s = c + d.
  Psi(L):  min of Phi0 over the K-closure of L (Skolemization at any
           residual position, applied any number of times).

Theorem 1 of the report says Phi0 never decreases under S, T, D, B when
c >= 1 and c + d >= 2.  K can decrease Phi0; the check measures whether Psi is
monotone under all five rules (the conjecture that would extend the barrier).
Writes potential_check_results.json.  Runs in a few seconds per setting.
"""

import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
E = 1  # exists


def phi0(line, beta, t, c, d):
    s = c + d
    nxt, nxt_sigma = t, beta
    for i in range(len(line) - 1, -1, -1):
        q, kind, a, sig, w = line[i]
        if i == 0:
            if kind == 'res':
                return nxt
            return c * max(nxt, a, sig, nxt_sigma)
        if kind == 'big':
            cur = s * max(nxt, a, sig, nxt_sigma)
        else:
            cur = min(nxt + w, s * max(nxt, sig, nxt_sigma))
        nxt, nxt_sigma = cur, sig
    return nxt


def apply_K(line, beta, t, pos):
    A, R, X = line[pos - 1], line[pos], line[pos + 1]
    tbl = X[2] + R[4]
    An = (A[0], 'big', max(A[2], tbl), A[3], 0.0)
    if pos + 2 < len(line):
        Y = line[pos + 2]
        sig = max(Y[3], R[3], tbl)
        if Y[1] == 'big':
            Yn = (Y[0], 'big', Y[2], sig, 0.0)
        else:
            Yn = (Y[0], Y[1], 0.0, sig, Y[4] + R[4])
        return line[:pos - 1] + [An, Yn] + line[pos + 3:], beta, t
    Rn = (R[0], 'res', 0.0, max(R[3], tbl), R[4])
    return line[:pos - 1] + [An, Rn], beta, t


def k_positions(line):
    return [i for i in range(1, len(line) - 1) if line[i][1] == 'res']


def psi(line, beta, t, c, d, depth=0):
    best = phi0(line, beta, t, c, d)
    if depth > 6:
        return best
    for pos in k_positions(line):
        l2, b2, t2 = apply_K(line, beta, t, pos)
        best = min(best, psi(l2, b2, t2, c, d, depth + 1))
    return best


def step(line, beta, t, op, c, d, rng):
    last = line[-1]
    q, kind, a, sig, w = last
    if op in 'ST':
        x = rng.uniform(0, t)
        tn = t - x
        if op == 'S':
            line = line[:-1] + [(q, 'big', max(a, x), sig, 0.0),
                                (-q, 'log', 0.0, max(x, beta), x)]
        else:
            line = line + [(-q, 'big', x, beta, 0.0), (q, 'log', 0.0, max(x, beta), x)]
        return line, beta, tn
    if op == 'D':
        M = max(t, a, sig, beta)
        return line[:-1] + [(q, 'res', 0.0, sig, d * M)], sig, c * M
    if op == 'B':
        return line[:-1], sig, t + w
    if op == 'K':
        return apply_K(line, beta, t, rng.choice(k_positions(line)))
    raise ValueError(op)


def legal_ops(line, ops):
    last = line[-1]
    out = []
    if 'S' in ops:
        out.append('S')
    if 'T' in ops:
        out.append('T')
    if 'D' in ops and last[1] != 'res':
        out.append('D')
    if 'B' in ops and last[1] == 'res' and len(line) > 1:
        out.append('B')
    if 'K' in ops and k_positions(line):
        out.append('K')
    return out


def run(c, d, ops, trials, length, seed):
    rng = random.Random(seed)
    viol_phi0, viol_psi, steps = {}, {}, 0
    worst = {}
    for _ in range(trials):
        line, beta, t = [(E, 'res', 0.0, 0.0, 0.0)], 0.0, 1.0
        for _ in range(length):
            if len(line) > 7:
                break
            choices = legal_ops(line, ops)
            op = rng.choice(choices)
            p0, s0 = phi0(line, beta, t, c, d), psi(line, beta, t, c, d)
            line2, beta2, t2 = step(line, beta, t, op, c, d, rng)
            p1, s1 = phi0(line2, beta2, t2, c, d), psi(line2, beta2, t2, c, d)
            steps += 1
            if p1 < p0 - 1e-9:
                viol_phi0[op] = viol_phi0.get(op, 0) + 1
            if s1 < s0 - 1e-9:
                viol_psi[op] = viol_psi.get(op, 0) + 1
                worst[op] = max(worst.get(op, 0.0), s0 - s1)
            line, beta, t = line2, beta2, t2
    return {'c': c, 'd': d, 'ops': ops, 'trials': trials, 'steps': steps,
            'phi0_decreases_by_rule': viol_phi0, 'psi_decreases_by_rule': viol_psi,
            'psi_worst_decrease_by_rule': worst}


if __name__ == '__main__':
    out = []
    for c, d in ((1.0, 1.0), (1.0, 1.5), (1.2, 0.8), (1.5, 0.5), (2.0, 0.0)):
        out.append(run(c, d, 'STDB', 3000, 30, 1))
        out.append(run(c, d, 'STKDB', 1500, 30, 2))
    for c, d in ((0.95, 1.0), (1.3, 0.5)):   # outside the barrier region
        out.append(run(c, d, 'STDB', 1500, 30, 3))
    (HERE / 'potential_check_results.json').write_text(json.dumps(out, indent=2))
    for r in out:
        print(r)


# ---- optimistic Skolem closure (K°: merged block keeps its old stage input) ----
def apply_Kopt(line, beta, t, pos):
    A, R, X = line[pos - 1], line[pos], line[pos + 1]
    tbl = X[2] + R[4]
    An = (A[0], 'big', max(A[2], tbl), A[3], 0.0)
    if pos + 2 < len(line):
        Y = line[pos + 2]
        sig = max(Y[3], R[3])
        Yn = (Y[0], 'big', Y[2], sig, 0.0) if Y[1] == 'big' else (Y[0], Y[1], 0.0, sig, Y[4] + R[4])
        return line[:pos - 1] + [An, Yn] + line[pos + 3:], beta, t
    return line[:pos - 1] + [An, (R[0], 'res', 0.0, R[3], R[4])], beta, t


def psi_opt(line, beta, t, c, d, depth=0):
    best = phi0(line, beta, t, c, d)
    if depth > 6:
        return best
    for pos in k_positions(line):
        l2, b2, t2 = apply_Kopt(line, beta, t, pos)
        best = min(best, psi_opt(l2, b2, t2, c, d, depth + 1))
    return best


def run_opt(c, d, ops, trials, length, seed):
    rng = random.Random(seed)
    viol, worst, steps, end_ok, end_total = {}, {}, 0, 0, 0
    for _ in range(trials):
        line, beta, t = [(E, 'res', 0.0, 0.0, 0.0)], 0.0, 1.0
        for _ in range(length):
            if len(line) > 7:
                break
            op = rng.choice(legal_ops(line, ops))
            s0 = psi_opt(line, beta, t, c, d)
            line2, beta2, t2 = step(line, beta, t, op, c, d, rng)
            s1 = psi_opt(line2, beta2, t2, c, d)
            steps += 1
            if s1 < s0 - 1e-9:
                viol[op] = viol.get(op, 0) + 1
                worst[op] = max(worst.get(op, 0.0), s0 - s1)
            line, beta, t = line2, beta2, t2
            if len(line) == 1 and line[0][1] == 'res' and steps > 0:
                end_total += 1
                end_ok += (t >= 1.0 - 1e-9)
    return {'potential': 'psi_opt', 'c': c, 'd': d, 'ops': ops, 'trials': trials,
            'steps': steps, 'decreases_by_rule': viol, 'worst_decrease': worst,
            'single_residual_lines_seen': end_total,
            'of_which_time_at_least_start': end_ok}


if __name__ == '__main__':
    extra = []
    for c, d in ((1.0, 1.0), (1.0, 1.5), (1.2, 0.8), (1.5, 0.5), (2.0, 0.0)):
        for ops, seed in (('STDB', 1), ('STKDB', 2), ('STKDB', 5)):
            extra.append(run_opt(c, d, ops, 2000, 30, seed))
    prev = json.loads((HERE / 'potential_check_results.json').read_text())
    (HERE / 'potential_check_results.json').write_text(json.dumps(prev + extra, indent=2))
    for r in extra:
        print(r['potential'], r['c'], r['d'], r['ops'], 'steps', r['steps'], 'decreases', r['decreases_by_rule'], 'ends', r['single_residual_lines_seen'], 'ok', r['of_which_time_at_least_start'])
