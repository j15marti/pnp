#!/usr/bin/env node
// Independent V8/Node replay for LSPV-5/470. Not the native R_mix341 checker.

function relation(m, parity) {
  if (!Number.isInteger(m) || m < 1) throw new Error("bad m");
  if (parity !== 0 && parity !== 1) throw new Error("bad parity");
  const d = m + 1;
  const rows = [];
  for (let x = 0; x < 2 ** d; x++) {
    const row = Array.from({ length: d }, (_, i) => (x >> i) & 1);
    if ((row.reduce((a, b) => a + b, 0) & 1) === parity) rows.push(row);
  }
  return rows;
}

function projection(rows, mask) {
  const d = rows[0].length;
  if (!Number.isInteger(mask) || mask < 0 || mask >= 2 ** d) throw new Error("bad mask");
  const idx = Array.from({ length: d }, (_, i) => i).filter(i => mask & (1 << i));
  return new Set(rows.map(r => idx.map(i => r[i]).join("")));
}

function equalSets(a, b) {
  return a.size === b.size && [...a].every(x => b.has(x));
}

function guardedCharge(rows, m, weight) {
  if (!Number.isInteger(weight) || weight <= 0) throw new Error("bad weight");
  const guarded = rows.filter(r => r.slice(0, m).every(b => b === 1));
  if (guarded.length === 0) throw new Error("unreachable guard");
  return Math.min(...guarded.map(r => r[m] ? 0 : weight));
}

let checks = 0;
let projectionChecks = 0;
const rows = [];
for (let m = 1; m <= 8; m++) {
  const d = m + 1;
  const r0 = relation(m, 0), r1 = relation(m, 1);
  if (r0.length !== 2 ** m || r1.length !== 2 ** m) throw new Error("size");
  checks++;
  for (let mask = 0; mask < 2 ** d - 1; mask++) {
    const a = projection(r0, mask), b = projection(r1, mask);
    const k = mask.toString(2).split("1").length - 1;
    if (!equalSets(a, b) || a.size !== 2 ** k) throw new Error(`projection m=${m} mask=${mask}`);
    checks += 2;
    projectionChecks++;
  }
  const full = 2 ** d - 1;
  if (equalSets(projection(r0, full), projection(r1, full))) throw new Error("full relation collapsed");
  checks++;
  const h0 = r0.find(r => r.slice(0, m).every(b => b === 1))[m];
  const h1 = r1.find(r => r.slice(0, m).every(b => b === 1))[m];
  const c0 = guardedCharge(r0, m, 11), c1 = guardedCharge(r1, m, 11);
  if (h0 === h1 || [c0, c1].sort((x, y) => x - y).join(",") !== "0,11") throw new Error("guard");
  checks += 2;
  const unionMap = new Map([...r0, ...r1].map(r => [r.join(""), r]));
  const union = [...unionMap.values()];
  if (union.length !== 2 ** d || guardedCharge(union, m, 11) !== 0) throw new Error("join");
  checks += 2;
  rows.push({ m, d, properProjections: 2 ** d - 1, h0, h1, c0, c1 });
}

let rejected = 0;
for (const f of [
  () => relation(0, 0),
  () => relation(2, 3),
  () => projection(relation(2, 0), 8),
  () => guardedCharge(relation(2, 0), 2, 0),
]) {
  try { f(); } catch { rejected++; }
}
if (rejected !== 4) throw new Error("malformed acceptance");
checks++;

process.stdout.write(JSON.stringify({
  status: "PASS",
  scope: "independent finite relational precision control; not R_mix341",
  mRange: [1, 8],
  checks,
  projectionChecks,
  malformedRejections: rejected,
  rows,
  limitation: "compact parity representation; no proof/time/space lower bound"
}, null, 2) + "\n");
