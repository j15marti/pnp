#!/usr/bin/env node
// Independently authored finite verifier for LSPV-5/462.

const states = ["fresh", "cached", "goal"];
const partitions = [
  [0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [0, 1, 2],
];

function shortest(nodes, edges, start, goals) {
  const dist = new Map(nodes.map(x => [x, Infinity]));
  dist.set(start, 0);
  for (let k = 0; k < nodes.length; k++) {
    let changed = false;
    for (const [u, v, w] of edges) {
      const nv = dist.get(u) + w;
      if (nv < dist.get(v)) { dist.set(v, nv); changed = true; }
    }
    if (!changed) break;
  }
  return Math.min(...[...goals].map(g => dist.get(g)));
}

let checks = 0;
let mergedZero = 0;
let separatedExact = 0;
for (let r = 1; r <= 16; r++) {
  const concreteEdges = [["fresh", "cached", r], ["cached", "goal", 0]];
  const concrete = shortest(states, concreteEdges, "fresh", new Set(["goal"]));
  if (concrete !== r) throw new Error("concrete distance mismatch");
  checks++;

  for (const labels of partitions) {
    const alpha = Object.fromEntries(states.map((s, i) => [s, labels[i]]));
    const classes = new Map();
    for (const [u, v, w] of concreteEdges) {
      const key = `${alpha[u]},${alpha[v]}`;
      classes.set(key, Math.min(classes.get(key) ?? Infinity, w));
    }
    const abstractEdges = [...classes.entries()].map(([key, w]) => {
      const [u, v] = key.split(",").map(Number); return [u, v, w];
    });
    const nodes = [...new Set(labels)];
    const abs = shortest(nodes, abstractEdges, alpha.fresh, new Set([alpha.goal]));
    if (!(abs <= concrete)) throw new Error("abstraction overestimates concrete cost");
    if (alpha.fresh === alpha.cached) {
      if (abs !== 0) throw new Error("merged paid history did not collapse");
      mergedZero++;
    }
    if (alpha.fresh !== alpha.cached && alpha.fresh !== alpha.goal) {
      if (abs !== r) throw new Error("separated control failed to recover cost");
      separatedExact++;
    }
    checks += 3;
  }
}

console.log(JSON.stringify({
  schema: "lspv5-462-independent-js-v1",
  paid_costs: 16,
  partitions_per_cost: partitions.length,
  cases: 16 * partitions.length,
  checks,
  merged_history_zero: mergedZero,
  separated_history_exact: separatedExact,
  status: "PASS",
}, null, 2));
