#!/usr/bin/env python3
"""Numerical checks for CLAUDE DIRECTPRODUCT-0001 (runs in a few seconds).

Checks
1. Heavy-projection lemma (Lemma 1 of the submitted note): for random finite
   product spaces mu^r and random events W,
       mu^r(W) <= prod_i mu(G_i(tau)) + r*tau          for several tau,
   and the heavy-coordinate bound max_i mu(G_i(eps/2r)) >= (eps/2)^(1/r).
2. Parameter claim in Theorem 3: tau = eps/(2r) > e^{-gamma r}/r is claimed to
   be >= m^{-gamma C - 1}; the lemma is then invoked with beta = gamma*C.
   We record where m^{-gamma C} fails as a lower bound (so beta must be
   gamma*C + 1).
3. Seed-count claim in Lemma 2: with L = ceil(2/tau) independent uniform
   seeds, the miss probability (1-tau)^L is about e^{-2}, not <= 1/m;
   L = ceil((2/tau) ln m) gives <= m^{-2}.
Writes results to verify_direct_product_results.json next to this file.
"""

import itertools
import json
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
rng = random.Random(20261028)


def check_lemma1(trials=3000):
    violations = 0
    heavy_violations = 0
    worst_slack = math.inf
    for _ in range(trials):
        support = rng.randint(2, 4)
        r = rng.randint(2, 4)
        weights = [rng.random() + 0.05 for _ in range(support)]
        total = sum(weights)
        mu = [w / total for w in weights]
        points = list(itertools.product(range(support), repeat=r))
        density = rng.choice([0.1, 0.3, 0.5, 0.8])
        W = {pt for pt in points if rng.random() < density}

        def prob(pt):
            p = 1.0
            for x in pt:
                p *= mu[x]
            return p

        eps = sum(prob(pt) for pt in W)
        if eps == 0:
            continue

        def heavy(i, tau):
            G = set()
            for f in range(support):
                mass = 0.0
                for rest in itertools.product(range(support), repeat=r - 1):
                    pt = rest[:i] + (f,) + rest[i:]
                    if pt in W:
                        q = 1.0
                        for x in rest:
                            q *= mu[x]
                        mass += q
                if mass >= tau - 1e-15:
                    G.add(f)
            return G

        for tau in (eps / (2 * r), eps / r, 0.05, 0.25):
            prod = 1.0
            for i in range(r):
                prod *= sum(mu[f] for f in heavy(i, tau))
            slack = prod + r * tau - eps
            worst_slack = min(worst_slack, slack)
            if slack < -1e-12:
                violations += 1
        tau = eps / (2 * r)
        best = max(sum(mu[f] for f in heavy(i, tau)) for i in range(r))
        if best < (eps / 2) ** (1 / r) - 1e-12:
            heavy_violations += 1
    return {"trials": trials, "bound_violations": violations,
            "heavy_coordinate_violations": heavy_violations,
            "min_slack_of_bound": worst_slack}


def check_beta(m_values=(10**3, 10**4, 10**6), C=2.0, gamma=0.5):
    rows = []
    for m in m_values:
        r = math.ceil(C * math.log(m))
        tau_floor = math.exp(-gamma * r) / r          # strict lower bound on tau
        rows.append({
            "m": m, "r": r, "tau_lower_bound": tau_floor,
            "m^-(gamma C)": m ** (-gamma * C),
            "m^-(gamma C + 1)": m ** (-gamma * C - 1),
            "beta=gammaC_valid": tau_floor >= m ** (-gamma * C),
            "beta=gammaC+1_valid": tau_floor >= m ** (-gamma * C - 1),
        })
    return rows


def check_seed_count(m=10**4, taus=(1e-2, 1e-3)):
    rows = []
    for tau in taus:
        L_stmt = math.ceil(2 / tau)
        L_proof = math.ceil(2 / tau * math.log(m))
        rows.append({
            "tau": tau, "m": m,
            "L=ceil(2/tau)": L_stmt, "miss_prob_L_stmt": (1 - tau) ** L_stmt,
            "L=ceil((2/tau) ln m)": L_proof, "miss_prob_L_proof": (1 - tau) ** L_proof,
            "1/m": 1 / m,
        })
    return rows


results = {
    "lemma1_heavy_projection": check_lemma1(),
    "theorem3_beta_parameter": check_beta(),
    "lemma2_seed_count": check_seed_count(),
}
out = HERE / "verify_direct_product_results.json"
out.write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
