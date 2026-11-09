#!/usr/bin/env node
import fs from "node:fs";

const started = process.hrtime.bigint();
const rawPath = process.argv[2];
if (!rawPath) throw new Error("usage: node verify...mjs RAW.json");
const raw = JSON.parse(fs.readFileSync(rawPath, "utf8"));

function delta(state, origin, weights) {
  if (!Number.isInteger(origin) || origin < 0 || origin >= weights.length)
    throw new Error("origin out of range");
  return (state & (1 << origin)) ? 0 : weights[origin];
}

function* partitions(size) {
  const labels = Array(size).fill(0);
  function* visit(pos, maximum) {
    if (pos === size) { yield labels.slice(); return; }
    for (let label = 0; label <= maximum + 1; label++) {
      labels[pos] = label;
      yield* visit(pos + 1, Math.max(maximum, label));
    }
  }
  if (size === 0) yield [];
  else yield* visit(1, 0);
}

function getBlocks(labels) {
  const count = Math.max(...labels) + 1;
  const result = Array.from({length: count}, () => []);
  labels.forEach((label, state) => result[label].push(state));
  return result;
}

function exactCharge(labels, weights) {
  return getBlocks(labels).every(block =>
    weights.every((_, i) => new Set(block.map(s => delta(s, i, weights))).size === 1));
}

function exactMarkov(labels, weights) {
  if (!exactCharge(labels, weights)) return false;
  return getBlocks(labels).every(block => weights.every((_, i) =>
    new Set(block.map(s => labels[s | (1 << i)])).size === 1));
}

let pairChecks = 0;
for (let n = 1; n <= 10; n++) {
  const weights = Array.from({length: n}, (_, i) => i + 1);
  for (let a = 0; a < 2 ** n; a++) for (let b = a + 1; b < 2 ** n; b++) {
    const diff = a ^ b;
    let i = 0; while (((diff >>> i) & 1) === 0) i++;
    if (delta(a, i, weights) === delta(b, i, weights)) throw new Error("pair not distinguished");
    pairChecks++;
  }
}

const partitionStats = [];
let totalPartitions = 0, exactChargeTotal = 0, exactMarkovTotal = 0, mayChecks = 0;
for (let n = 1; n <= 3; n++) {
  const weights = Array.from({length: n}, (_, i) => i + 1);
  const stat = {origins:n, partitions:0, exact_charge:0, exact_markov:0, safe_may_checks:0};
  for (const labels of partitions(2 ** n)) {
    stat.partitions++;
    if (exactCharge(labels, weights)) stat.exact_charge++;
    if (exactMarkov(labels, weights)) stat.exact_markov++;
    for (const block of getBlocks(labels)) for (let i = 0; i < n; i++) {
      const charge = Math.min(...block.map(s => delta(s, i, weights)));
      for (const s of block) {
        if (charge > delta(s, i, weights)) throw new Error("MAY overcharge");
        stat.safe_may_checks++;
      }
    }
  }
  if (stat.exact_charge !== 1 || stat.exact_markov !== 1) throw new Error("non-discrete exact quotient");
  partitionStats.push(stat);
  totalPartitions += stat.partitions;
  exactChargeTotal += stat.exact_charge;
  exactMarkovTotal += stat.exact_markov;
  mayChecks += stat.safe_may_checks;
}

let joinChecks = 0;
for (let n = 1; n <= 8; n++) {
  const weights = Array.from({length: n}, (_, i) => i + 1);
  for (let a = 0; a < 2 ** n; a++) for (let b = 0; b < 2 ** n; b++) {
    const joined = a | b;
    for (let i = 0; i < n; i++) {
      const expected = (joined & (1 << i)) ? 0 : weights[i];
      if (delta(joined, i, weights) !== expected) throw new Error("join mismatch");
      joinChecks++;
    }
  }
}

const expected = {
  pair_checks: pairChecks,
  total_partitions: totalPartitions,
  total_exact_charge_partitions: exactChargeTotal,
  total_exact_markov_partitions: exactMarkovTotal,
  safe_may_inequality_checks: mayChecks,
  join_checks: joinChecks,
};
for (const [key, value] of Object.entries(expected)) {
  if (raw[key] !== value) throw new Error(`${key}: raw=${raw[key]} replay=${value}`);
}
for (let i = 0; i < partitionStats.length; i++) {
  for (const key of Object.keys(partitionStats[i])) {
    if (raw.partition_stats[i]?.[key] !== partitionStats[i][key])
      throw new Error(`partition stats mismatch at n=${i + 1}, key=${key}`);
  }
}
if (raw.status !== "PASS" || raw.node !== "P2-L5-468") throw new Error("raw identity/status mismatch");

const elapsedSeconds = Number(process.hrtime.bigint() - started) / 1e9;
console.log(JSON.stringify({status:"PASS", ...expected, partition_stats:partitionStats,
  elapsed_seconds:Number(elapsedSeconds.toFixed(6)), peak_rss_kib:process.resourceUsage().maxRSS}));
