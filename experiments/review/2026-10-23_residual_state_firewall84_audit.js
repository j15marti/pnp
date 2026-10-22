"use strict";

// RESIDUAL-STATE-FIREWALL84 finite audit.
// This validates finite arithmetic, a restricted point-query adversary, and a
// structured parity bypass.  It does not establish an unrestricted SAT lower bound.

let seed = 0x84c0ffee >>> 0;
function rnd() {
  seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
  return seed;
}

let assertions = 0;
let failures = 0;
let blackBoxTrials = 0;
let exponentTrials = 0;
let conventionTrials = 0;
let parityInstances = 0;
let parityAssignments = 0;

function check(cond, msg) {
  assertions++;
  if (!cond) {
    failures++;
    if (failures <= 20) process.stderr.write(`FAIL: ${msg}\n`);
  }
}

// 84A: additive elimination and multiplicative compression are different.
for (let trial = 0; trial < 100000; trial++) {
  const n = 1 + (rnd() % 1000000);
  const k = rnd() % (n + 1);
  const r = n - k;
  check(r === n - k, "r=n-k");
  check(r >= 0 && r <= n, "residual range");
  if (r > 0) {
    const v = n / r;
    check(Math.abs(n / v - r) <= 1e-9 * Math.max(1, r), "v=n/r convention");
  }
  conventionTrials++;
}

// 84B: deterministic point-query EMPTY-vs-SINGLETON adversary.
// Any transcript with q<2^r all-zero replies leaves an unqueried singleton.
for (let trial = 0; trial < 100000; trial++) {
  const r = 1 + (rnd() % 20);
  const domain = 2 ** r;
  const qCap = Math.min(domain - 1, 64);
  const q = rnd() % (qCap + 1);
  const queried = new Set();
  while (queried.size < q) queried.add(rnd() % domain);
  let hidden = 0;
  while (queried.has(hidden)) hidden++;
  check(hidden < domain, "unqueried singleton exists");
  for (const x of queried) {
    check(x !== hidden, "EMPTY and singleton transcripts agree on queried points");
  }
  blackBoxTrials++;
}

// 84C: if T >= 2^(a r)/N^b and r/log_2 N is unbounded, then the
// lower-bound exponent a*r/log_2(N)-b is unbounded.
for (let trial = 0; trial < 100000; trial++) {
  const logN = 8 + (rnd() % 120);
  const aNum = 1 + (rnd() % 8); // a=aNum/16 > 0
  const a = aNum / 16;
  const b = rnd() % 20;
  const ratio = 1 + (rnd() % 200); // r/log_2 N
  const r = ratio * logN;
  const exponent = a * r / logN - b;
  check(Math.abs(exponent - (a * ratio - b)) < 1e-12, "exponent identity");
  const targetDegree = rnd() % 40;
  if (ratio > (targetDegree + b) / a) {
    check(exponent > targetDegree, "conditional lower bound beats chosen polynomial degree");
  }
  exponentTrials++;
}

// 84D: a connected cubic prism Tseitin system has 2^r edge assignments but
// SAT is decided by one O(|V|) charge-parity scan.
function prismEdges(m) {
  const edges = [];
  for (let i = 0; i < m; i++) {
    edges.push([i, (i + 1) % m]);
    edges.push([m + i, m + ((i + 1) % m)]);
    edges.push([i, m + i]);
  }
  return edges;
}

function bruteSat(vertices, edges, charge) {
  const limit = 2 ** edges.length;
  for (let mask = 0; mask < limit; mask++) {
    parityAssignments++;
    const got = new Array(vertices).fill(0);
    for (let e = 0; e < edges.length; e++) {
      if ((mask >>> e) & 1) {
        got[edges[e][0]] ^= 1;
        got[edges[e][1]] ^= 1;
      }
    }
    let ok = true;
    for (let v = 0; v < vertices; v++) if (got[v] !== charge[v]) { ok = false; break; }
    if (ok) return true;
  }
  return false;
}

for (let m = 3; m <= 5; m++) {
  const vertices = 2 * m;
  const edges = prismEdges(m);
  check(edges.length === 3 * m, "cubic prism edge count");
  for (let trial = 0; trial < 24; trial++) {
    const charge = Array.from({length: vertices}, () => rnd() & 1);
    const scan = charge.reduce((a, b) => a ^ b, 0) === 0;
    const brute = bruteSat(vertices, edges, charge);
    check(brute === scan, "Tseitin SAT iff total charge parity is even");
    check((2 ** edges.length) >= (2 ** (vertices - 1)), "exponential assignment space retained");
    parityInstances++;
  }
}

const result = {
  artifact: "RESIDUAL-STATE-FIREWALL84",
  seed: "0x84c0ffee",
  assertions,
  failures,
  convention_trials: conventionTrials,
  black_box_trials: blackBoxTrials,
  exponent_trials: exponentTrials,
  parity_instances: parityInstances,
  parity_assignments_checked: parityAssignments,
  status: failures === 0 ? "PASS_RESTRICTED_ONLY" : "FAIL",
  disclaimer: "Finite validation only; no unrestricted SAT lower bound and no P-vs-NP resolution."
};

process.stdout.write(JSON.stringify(result, null, 2) + "\n");
process.exitCode = failures === 0 ? 0 : 1;
