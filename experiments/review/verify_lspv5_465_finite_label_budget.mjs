#!/usr/bin/env node
// Independent V8 reconstruction for LSPV-5/465. Not R_mix341.

let chargeSubsetCases = 0;
let dagHistoryCases = 0;
let fiberMinCases = 0;
let violations = 0;

function vectors(base, length, visit, a = []) {
  if (a.length === length) return visit(a.slice());
  for (let x = 0; x < base; x++) {
    a.push(x); vectors(base, length, visit, a); a.pop();
  }
}

for (let m = 0; m <= 7; m++) {
  vectors(4, m, charges => {
    const total = charges.reduce((a, b) => a + b, 0);
    for (let mask = 0; mask < (1 << m); mask++) {
      chargeSubsetCases++;
      let cost = 0;
      for (let i = 0; i < m; i++) if (mask & (1 << i)) cost += charges[i];
      if (cost > total) violations++;
    }
  });
}

for (let n = 1; n <= 4; n++) {
  const parentChoices = 1 << (n * (n - 1) / 2);
  for (let edgeMask = 0; edgeMask < parentChoices; edgeMask++) {
    vectors(3, n, labels => {
      const used = new Set(labels);
      vectors(4, 3, charges => {
        dagHistoryCases++;
        let cost = 0;
        for (const label of used) cost += charges[label];
        if (cost > charges.reduce((a, b) => a + b, 0)) violations++;
      });
    });
  }
}

for (let n = 1; n <= 6; n++) {
  vectors(3, n, ws0 => {
    const weights = ws0.map(x => x + 1);
    vectors(2, n, quotient => {
      fiberMinCases++;
      const mins = new Map();
      quotient.forEach((q, i) => mins.set(q, Math.min(mins.get(q) ?? weights[i], weights[i])));
      const abstractCost = [...mins.values()].reduce((a, b) => a + b, 0);
      if (abstractCost > weights.reduce((a, b) => a + b, 0)) violations++;
    });
  });
}

const charges = new Map([["S0",0],["S1",0],["L",3],["B0",2],["B1",2],["G",1]]);
const occurrences = ["S0","S1","L","B0","L","B1","G"];
const historyCost = [...new Set(occurrences)].reduce((s, x) => s + charges.get(x), 0);
const treeCost = occurrences.reduce((s, x) => s + charges.get(x), 0);
if (historyCost !== 8 || treeCost !== 11) violations++;

const result = {
  charge_subset_cases: chargeSubsetCases,
  dag_history_cases: dagHistoryCases,
  fiber_min_cases: fiberMinCases,
  shared_diamond: {history_cost: historyCost, tree_unfolded_cost: treeCost, total_label_budget: 8},
  violations,
  checks: chargeSubsetCases + dagHistoryCases + fiberMinCases + 3,
  status: violations === 0 ? "PASS" : "FAIL",
  limitations: "finite combinatorial reconstruction only; not historical R_mix341"
};
console.log(JSON.stringify(result, null, 2));
if (violations) process.exit(1);
