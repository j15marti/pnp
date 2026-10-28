#!/usr/bin/env python3
"""Numerical verification of conditional FLMV contraction parameters."""
import math

def beta(t):
    """FLMV space exponent upper bound function (approximate form from objective)."""
    if t <= 1:
        return float('inf')
    return ((t + 2) / (t * t) - t) / 2

def check_parameters(K_values):
    results = []
    for K in K_values:
        lam = 1.0 / (5 * K)
        zeta = 0.1
        t_prime = 1.3 - lam
        s_prime = 0.2
        b = beta(t_prime)
        inside = s_prime < b
        results.append({
            'K': K,
            'lambda': lam,
            't_prime': t_prime,
            's_prime': s_prime,
            'beta(t_prime)': b,
            'inside_forbidden': inside
        })
    return results

if __name__ == '__main__':
    Ks = [2, 3, 5, 10, 20, 100]
    res = check_parameters(Ks)
    for r in res:
        print(f"K={r['K']:3d}  t'={r['t_prime']:.4f}  s'={r['s_prime']:.1f}  "
              f"beta(t')={r['beta(t_prime)']:.4f}  inside={r['inside_forbidden']}")
    print("All tested K yield profiles inside the forbidden region:", all(r['inside_forbidden'] for r in res))
