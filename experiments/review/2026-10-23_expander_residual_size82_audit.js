#!/usr/bin/env node
"use strict";

// EXPANDER-RESIDUAL-SIZE82 finite hostile-control audit.
// The asymptotic theorem relies on the stated expansion hypothesis.
// These random finite checks prove no complexity-class separation.

let seed = 0x82E11A;
function rand32() {
  seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
  return seed;
}
function shuffle(a) {
  for (let i = a.length - 1; i > 0; i--) {
    const j = rand32() % (i + 1);
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function makeConnectedCubicBipartite(side) {
  for (let attempt = 0; attempt < 10000; attempt++) {
    const p = shuffle([...Array(side).keys()]);
    const q = shuffle([...Array(side).keys()]);
    let simple = true;
    for (let i = 0; i < side; i++) {
      if (p[i] === i || q[i] === i || p[i] === q[i]) {
        simple = false;
        break;
      }
    }
    if (!simple) continue;

    const adj = Array.from({ length: 2 * side }, () => []);
    for (let clause = 0; clause < side; clause++) {
      for (const variable of [clause, p[clause], q[clause]]) {
        adj[side + clause].push(variable);
        adj[variable].push(side + clause);
      }
    }

    const seen = new Uint8Array(2 * side);
    const stack = [0];
    seen[0] = 1;
    let count = 0;
    while (stack.length) {
      const u = stack.pop();
      count++;
      for (const v of adj[u]) {
        if (!seen[v]) {
          seen[v] = 1;
          stack.push(v);
        }
      }
    }
    if (count === 2 * side) return adj;
  }
  throw new Error("connected graph generation failed");
}

function simplifyAllTrue(adj, side, variables) {
  const removed = new Uint8Array(2 * side);
  for (const variable of variables) {
    removed[variable] = 1;
    for (const clause of adj[variable]) removed[clause] = 1;
  }

  const seen = new Uint8Array(2 * side);
  let largest = 0;
  let removedCount = 0;
  for (const bit of removed) removedCount += bit;

  for (let start = 0; start < 2 * side; start++) {
    if (removed[start] || seen[start]) continue;
    let size = 0;
    const stack = [start];
    seen[start] = 1;
    while (stack.length) {
      const u = stack.pop();
      size++;
      for (const v of adj[u]) {
        if (!removed[v] && !seen[v]) {
          seen[v] = 1;
          stack.push(v);
        }
      }
    }
    largest = Math.max(largest, size);
  }
  return { removedCount, largest };
}

let assertions = 0;
let failures = 0;
let tests = 0;
let minimumLargestFraction = 1;
const summaries = [];

for (const side of [64, 96, 128, 160, 192, 256]) {
  const adj = makeConnectedCubicBipartite(side);
  let localMinimum = 1;

  for (let trial = 0; trial < 20000; trial++) {
    const k = rand32() % 5;
    const variables = new Set();
    while (variables.size < k) variables.add(rand32() % side);

    const result = simplifyAllTrue(adj, side, [...variables]);
    if (result.removedCount > 4 * k) failures++;
    assertions++;

    if (result.largest <= side) failures++;
    assertions++;

    const fraction = result.largest / (2 * side);
    localMinimum = Math.min(localMinimum, fraction);
    minimumLargestFraction = Math.min(minimumLargestFraction, fraction);
    tests++;
  }

  summaries.push({
    side,
    incidence_vertices: 2 * side,
    min_largest_fraction: Number(localMinimum.toFixed(6))
  });
}

const output = {
  artifact: "EXPANDER-RESIDUAL-SIZE82",
  seed: "0x82E11A",
  tests,
  assertions,
  failures,
  min_largest_fraction: Number(minimumLargestFraction.toFixed(6)),
  summaries,
  disclaimer:
    "Finite random regular control only; asymptotic result uses the stated vertex-expansion hypothesis."
};

console.log(JSON.stringify(output, null, 2));
if (failures) process.exit(1);
