#!/usr/bin/env node
"use strict";

// TSEITIN-EXPANDER-PAIR83 finite implementation audit.
// Finite checks prove no complexity-class separation.

let seed = 0x83A11CE;
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

function makeGraph(side) {
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

    const edges = [];
    const incident = Array.from({ length: 2 * side }, () => []);
    const adjacency = Array.from({ length: 2 * side }, () => []);
    for (let i = 0; i < side; i++) {
      for (const j of [i, p[i], q[i]]) {
        const e = edges.length;
        edges.push([i, side + j]);
        incident[i].push(e);
        incident[side + j].push(e);
        adjacency[i].push([side + j, e]);
        adjacency[side + j].push([i, e]);
      }
    }

    const seen = new Uint8Array(2 * side);
    const stack = [0];
    seen[0] = 1;
    let count = 0;
    while (stack.length) {
      const u = stack.pop();
      count++;
      for (const [v] of adjacency[u]) {
        if (!seen[v]) {
          seen[v] = 1;
          stack.push(v);
        }
      }
    }
    if (count === 2 * side) {
      return { n: 2 * side, edges, incident, adjacency };
    }
  }
  throw new Error("graph generation failed");
}

function rank(rows) {
  rows = rows.slice();
  let r = 0;
  for (let col = 0; col < 256; col++) {
    let pivot = -1;
    for (let i = r; i < rows.length; i++) {
      if ((rows[i] >> BigInt(col)) & 1n) {
        pivot = i;
        break;
      }
    }
    if (pivot < 0) continue;
    [rows[r], rows[pivot]] = [rows[pivot], rows[r]];
    for (let i = 0; i < rows.length; i++) {
      if (i !== r && ((rows[i] >> BigInt(col)) & 1n)) rows[i] ^= rows[r];
    }
    r++;
  }
  return r;
}

function parityClauses(variables, charge) {
  const clauses = [];
  for (let assignment = 0; assignment < 8; assignment++) {
    const parity =
      ((assignment >> 0) & 1) ^
      ((assignment >> 1) & 1) ^
      ((assignment >> 2) & 1);
    if (parity === charge) continue;
    clauses.push(
      variables.map((variable, i) => ({
        variable,
        positive: ((assignment >> i) & 1) === 0
      }))
    );
  }
  return clauses;
}

function satisfies(clauses, assignment) {
  return clauses.every(clause =>
    clause.some(literal =>
      literal.positive
        ? assignment[literal.variable] === 1
        : assignment[literal.variable] === 0
    )
  );
}

function largestResidual(graph, deletedEdges) {
  const deleted = new Uint8Array(graph.edges.length);
  for (const e of deletedEdges) deleted[e] = 1;

  const seen = new Uint8Array(graph.n);
  let largest = 0;
  for (let start = 0; start < graph.n; start++) {
    if (seen[start]) continue;
    let size = 0;
    const stack = [start];
    seen[start] = 1;
    while (stack.length) {
      const u = stack.pop();
      size++;
      for (const [v, e] of graph.adjacency[u]) {
        if (!deleted[e] && !seen[v]) {
          seen[v] = 1;
          stack.push(v);
        }
      }
    }
    largest = Math.max(largest, size);
  }
  return largest;
}

let assertions = 0;
let failures = 0;
let bruteAssignments = 0;
let residualTests = 0;
let minimumLargestFraction = 1;

for (const side of [4, 5, 6, 7, 8]) {
  const graph = makeGraph(side);
  const rows = graph.incident.map(edges =>
    edges.reduce((mask, e) => mask | (1n << BigInt(e)), 0n)
  );

  if (rank(rows) !== graph.n - 1) failures++;
  assertions++;

  for (let omitted = 0; omitted < graph.n; omitted++) {
    if (rank(rows.filter((_, i) => i !== omitted)) !== graph.n - 1) failures++;
    assertions++;
  }

  for (let v = 0; v < graph.n; v++) {
    for (let charge = 0; charge < 2; charge++) {
      for (let local = 0; local < 8; local++) {
        const assignment = {};
        graph.incident[v].forEach((e, i) => {
          assignment[e] = (local >> i) & 1;
        });
        const expected =
          (((local & 1) ^ ((local >> 1) & 1) ^ ((local >> 2) & 1)) ===
            charge);
        if (
          satisfies(parityClauses(graph.incident[v], charge), assignment) !==
          expected
        ) {
          failures++;
        }
        assertions++;
      }
    }
  }

  for (let trial = 0; trial < 12; trial++) {
    const charge = Array.from({ length: graph.n }, () => rand32() & 1);
    const currentParity = charge.reduce((a, b) => a ^ b, 0);
    charge[0] ^= trial & 1 ? currentParity : currentParity ^ 1;
    const totalParity = charge.reduce((a, b) => a ^ b, 0);

    const augmented = rows.map(
      (row, i) => row | (BigInt(charge[i]) << BigInt(graph.edges.length))
    );
    const consistent = rank(augmented) === rank(rows);
    if (consistent !== (totalParity === 0)) failures++;
    assertions++;

    if (totalParity === 1) {
      for (let omitted = 0; omitted < graph.n; omitted++) {
        const reducedRows = rows.filter((_, i) => i !== omitted);
        const reducedAugmented = augmented.filter((_, i) => i !== omitted);
        if (rank(reducedRows) !== rank(reducedAugmented)) failures++;
        assertions++;
      }
    }

    if (side <= 5) {
      let found = false;
      const total = 1 << graph.edges.length;
      for (let assignment = 0; assignment < total && !found; assignment++) {
        bruteAssignments++;
        let okay = true;
        for (let v = 0; v < graph.n && okay; v++) {
          let parity = 0;
          for (const e of graph.incident[v]) parity ^= (assignment >> e) & 1;
          if (parity !== charge[v]) okay = false;
        }
        found = okay;
      }
      if (found !== consistent) failures++;
      assertions++;
    }
  }
}

for (const side of [32, 48, 64, 96, 128]) {
  const graph = makeGraph(side);
  for (let trial = 0; trial < 20000; trial++) {
    const k = rand32() % 5;
    const deleted = new Set();
    while (deleted.size < k) deleted.add(rand32() % graph.edges.length);

    const largest = largestResidual(graph, [...deleted]);
    minimumLargestFraction = Math.min(
      minimumLargestFraction,
      largest / graph.n
    );
    if (largest <= graph.n / 2) failures++;
    assertions++;

    const saturated = [];
    for (let v = 0; v < graph.n; v++) {
      if (graph.incident[v].every(e => deleted.has(e))) saturated.push(v);
    }
    if (saturated.length) {
      const edgeIndex = new Map([...deleted].map((e, i) => [e, i]));
      const rows = saturated.map(v =>
        graph.incident[v].reduce(
          (mask, e) => mask | (1n << BigInt(edgeIndex.get(e))),
          0n
        )
      );
      if (rank(rows) !== saturated.length) failures++;
      assertions++;
    }
    residualTests++;
  }
}

const output = {
  artifact: "TSEITIN-EXPANDER-PAIR83",
  seed: "0x83A11CE",
  assertions,
  failures,
  brute_assignments: bruteAssignments,
  residual_tests: residualTests,
  min_largest_fraction: Number(minimumLargestFraction.toFixed(6)),
  disclaimer:
    "Finite implementation audit only; the asymptotic residual theorem assumes edge expansion."
};

console.log(JSON.stringify(output, null, 2));
if (failures) process.exit(1);
