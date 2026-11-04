#!/usr/bin/env node
"use strict";

// Independent finite replay for REFEREE340. Clauses are sorted integer arrays.
const assignments = [[0, 0], [0, 1], [1, 0], [1, 1]];
const clauses = assignments.map(a => a.map((bit, i) => bit === 0 ? i + 1 : -(i + 1)));
const K = 15;
let checks = 0;

function formula(mask) {
  if (!Number.isInteger(mask) || mask < 0 || mask > K) throw new Error("malformed mask");
  return clauses.filter((_, i) => mask & (1 << i));
}

function clauseValue(c, a) {
  return c.some(lit => (lit > 0) === Boolean(a[Math.abs(lit) - 1]));
}

function sat(mask, a) {
  return formula(mask).every(c => clauseValue(c, a));
}

function satStar(mask, a) {
  return mask !== K && sat(mask, a);
}

function key(c) {
  return [...c].sort((x, y) => Math.abs(x) - Math.abs(y) || x - y).join(",");
}

function parse(k) {
  return k === "" ? [] : k.split(",").map(Number);
}

function resolvents(a, b) {
  const out = new Set();
  for (const pivot of a) {
    if (!b.includes(-pivot)) continue;
    const child = [...new Set(a.filter(x => x !== pivot).concat(b.filter(x => x !== -pivot)))];
    if (child.some(x => child.includes(-x))) continue;
    out.add(key(child));
  }
  return out;
}

function minResolution(source) {
  let initial = new Set(source.map(key));
  if (initial.has("")) return 0;
  const queue = [[initial, 0]];
  const seen = new Set([[...initial].sort().join("|")]);
  while (queue.length) {
    const [known, depth] = queue.shift();
    const arr = [...known];
    for (let i = 0; i < arr.length; i++) {
      for (let j = i + 1; j < arr.length; j++) {
        for (const child of resolvents(parse(arr[i]), parse(arr[j]))) {
          if (known.has(child)) continue;
          if (child === "") return depth + 1;
          const next = new Set(known); next.add(child);
          const state = [...next].sort().join("|");
          if (!seen.has(state)) { seen.add(state); queue.push([next, depth + 1]); }
        }
      }
    }
  }
  return null;
}

for (let mask = 0; mask <= K; mask++) {
  for (const a of assignments) {
    if (sat(mask, a) !== satStar(mask, a)) throw new Error("semantic mismatch");
    checks++;
  }
}
if (assignments.some(a => sat(K, a))) throw new Error("K is SAT"); checks++;
if (!assignments.some(a => sat(1, a))) throw new Error("SAT control failed"); checks++;
const sourceCost = minResolution(formula(K));
if (sourceCost !== 3) throw new Error(`source cost ${sourceCost}`); checks++;
const poisonCost = minResolution([[3], [-3]]);
if (poisonCost !== 1) throw new Error(`poison cost ${poisonCost}`); checks++;
for (const malformed of [-2, -1, 16, 17, 255]) {
  let rejected = false;
  try { formula(malformed); } catch (_) { rejected = true; }
  if (!rejected) throw new Error("malformed mask accepted");
  checks++;
}

console.log(JSON.stringify({result: "PASS", checks, sourceCost, poisonCost}));
