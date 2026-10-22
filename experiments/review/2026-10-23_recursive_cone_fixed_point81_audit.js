#!/usr/bin/env node
"use strict";

// RECURSIVE-CONE-FIXED-POINT81 finite arithmetic/partition audit.
// Finite checks validate implementation only and prove no complexity separation.

let seed = 0x81C0FFEE;
function rnd() {
  seed = (Math.imul(1664525, seed) + 1013904223) >>> 0;
  return seed / 2 ** 32;
}

let assertions = 0;
let failures = 0;
let maxRatio = 0;
const partitions = 120000;

for (let trial = 0; trial < partitions; trial++) {
  const x = 100 + Math.floor(rnd() * 19900);
  const beta = 0.30 + rnd() * 0.40;
  const sigma = 0.01 + rnd() * 0.19;
  const c = 1 + rnd() * 0.45;
  const cap = Math.max(1, Math.floor(x ** beta));

  let remaining = x;
  let sumPow = 0;
  let pieces = 0;
  while (remaining > 0 && pieces < 20000) {
    const y = Math.min(remaining, 1 + Math.floor(rnd() * cap));
    sumPow += y ** c;
    remaining -= y;
    pieces++;
  }

  const assignments = Math.floor(x ** sigma);
  const lhs = assignments * sumPow;
  const rhs = x ** (1 + sigma + beta * (c - 1));
  maxRatio = Math.max(maxRatio, lhs / rhs);
  if (lhs > rhs * (1 + 1e-11)) failures++;
  assertions++;
}

const points = [
  { name: "baseline", beta: 1 / 2, sigma: 1 / 10, expected: 6 / 5 },
  { name: "retuned", beta: 101 / 200, sigma: 1 / 10, expected: 119 / 99 }
];
const endpoints = [];

for (const point of points) {
  let exponent = 1;
  for (let depth = 1; depth <= 80; depth++) {
    exponent = 1 + point.sigma + point.beta * (exponent - 1);
    const closed =
      1 +
      point.sigma * (1 - point.beta ** depth) / (1 - point.beta);
    if (Math.abs(exponent - closed) > 2e-14) failures++;
    assertions++;
  }
  const limit = 1 + point.sigma / (1 - point.beta);
  if (Math.abs(limit - point.expected) > 2e-14) failures++;
  assertions++;
  endpoints.push({
    name: point.name,
    beta: point.beta,
    sigma: point.sigma,
    limit,
    depth80: exponent,
    error: Math.abs(limit - exponent)
  });
}

const result = {
  artifact: "RECURSIVE-CONE-FIXED-POINT81",
  seed: "0x81C0FFEE",
  partitions,
  assertions,
  failures,
  max_ratio: Number(maxRatio.toFixed(12)),
  endpoints,
  disclaimer:
    "Finite validation of arithmetic and implementation only; P vs NP and P vs RP remain open."
};

console.log(JSON.stringify(result, null, 2));
if (failures) process.exit(1);
