#!/usr/bin/env node
"use strict";

const fs = require("fs");
const crypto = require("crypto");
const started = process.hrtime.bigint();
const path = "results/raw/arc/lspv5_312/semantic_cnf_basis_compiler_referee312.json";
const payload = fs.readFileSync(path, "utf8");
const data = JSON.parse(payload);
const FULL = 255;
const weights = {1: 3, 2: 4, 3: 6};

function canon(xs) {
  if (!Array.isArray(xs)) throw new Error("not clause");
  const out = [...new Set(xs)].sort((a, b) => Math.abs(a) - Math.abs(b) || (a < 0) - (b < 0));
  if (out.some(x => !Number.isInteger(x) || x === 0 || Math.abs(x) > 1000000 || out.includes(-x)))
    throw new Error("noncanonical clause");
  return out;
}
function eq(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
function key(c) { return JSON.stringify(canon(c)); }
function truth(c, a) {
  return c.some(l => Boolean((a >> (Math.abs(l) - 1)) & 1) === (l > 0));
}
function mask(c) {
  let result = 0;
  for (let a = 0; a < 8; a++) if (truth(c, a)) result |= (1 << a);
  return result;
}
function pop(x) { let n = 0; for (; x; x >>>= 1) n += x & 1; return n; }
function slots(out, left, right) {
  return [canon([-out, left]), canon([-out, right]), canon([out, -left, -right])];
}
function resolve(left, right, pivot) {
  left = canon(left); right = canon(right);
  if (!left.includes(pivot) || !right.includes(-pivot)) throw new Error("bad pivot");
  return canon([...left.filter(x => x !== pivot), ...right.filter(x => x !== -pivot)]);
}

const clauses = [];
for (const a of [0, 1, -1]) for (const b of [0, 1, -1]) for (const c of [0, 1, -1]) {
  if (a === 0 && b === 0 && c === 0) continue;
  clauses.push(canon([a && a * 1, b && b * 2, c && c * 3].filter(Boolean)));
}
clauses.sort((x, y) => x.length - y.length || key(x).localeCompare(key(y)));
if (clauses.length !== 26 || new Set(clauses.map(key)).size !== 26) throw new Error("clause catalog");
const masks = clauses.map(mask);

function independentOpt(target) {
  if (target === 0) return 7;
  let dp = new Map([[FULL, 0]]);
  for (let i = 0; i < clauses.length; i++) {
    if ((target & (~masks[i] & FULL)) !== 0) continue;
    const next = new Map(dp);
    for (const [cur, cost] of dp.entries()) {
      const nm = cur & masks[i], nc = cost + weights[clauses[i].length];
      if (!next.has(nm) || nc < next.get(nm)) next.set(nm, nc);
    }
    dp = next;
  }
  if (!dp.has(target)) throw new Error("no basis");
  return dp.get(target);
}

let maxCost = -1, maxMasks = [], costHist = new Map(), maxBasisSize = 0;
for (let target = 0; target < 256; target++) {
  const rec = data.relations[target];
  if (rec.mask !== target || rec.models !== pop(target)) throw new Error("record identity");
  const optimum = independentOpt(target);
  if (rec.cost !== optimum) throw new Error("nonoptimal basis cost");
  if (target === 0) {
    if (rec.mode !== "early_contradiction" || rec.basis.length !== 0) throw new Error("false mode");
  } else {
    let represented = FULL, paid = 0;
    for (const raw of rec.basis) {
      const c = canon(raw);
      if (!eq(c, raw)) throw new Error("noncanonical basis clause");
      const cm = mask(c);
      if ((target & (~cm & FULL)) !== 0) throw new Error("not implicate");
      represented &= cm; paid += weights[c.length];
    }
    if (represented !== target || paid !== optimum) throw new Error("basis semantics/cost");
  }
  maxBasisSize = Math.max(maxBasisSize, rec.basis.length);
  costHist.set(optimum, (costHist.get(optimum) || 0) + 1);
  if (optimum > maxCost) { maxCost = optimum; maxMasks = [target]; }
  else if (optimum === maxCost) maxMasks.push(target);
}
if (maxCost !== 24 || !eq(maxMasks, [105, 150]) || maxBasisSize !== 4) throw new Error("global maxima");

let pairs = 0, maxPairs = 0;
for (let source = 0; source < 256; source++) for (let output = 0; output < 256; output++) {
  if ((source & (~output & FULL)) !== 0) continue;
  pairs++;
  const cost = source === 0 ? 7 : independentOpt(output);
  if (cost === 24) maxPairs++;
}
if (pairs !== 6561 || maxPairs !== 30) throw new Error("pair counts");

function replayWeakening(cert, source, usedFresh) {
  const known = new Set(source.map(key));
  if (!known.has(key(cert.base)) || cert.base.length !== 2 || cert.target.length !== 3) throw new Error("base");
  let paid = 0;
  for (const d of cert.defs) {
    if (Math.abs(d.out) <= 3 || usedFresh.has(d.out)) throw new Error("freshness");
    usedFresh.add(d.out);
    const expected = slots(d.out, d.left, d.right);
    if (!eq(d.slots.map(canon), expected)) throw new Error("definition slots");
    expected.forEach(c => known.add(key(c))); paid++;
  }
  for (const r of cert.res) {
    if (!known.has(key(r.left)) || !known.has(key(r.right))) throw new Error("parent");
    const out = resolve(r.left, r.right, r.pivot);
    if (!eq(out, canon(r.out))) throw new Error("resolvent");
    known.add(key(out)); paid++;
  }
  if (!known.has(key(cert.target)) || paid !== cert.cost) throw new Error("root/cost");
  return paid;
}

const ctl = data.explicit_24_node_control;
const sourceModels = [...Array(8).keys()].filter(a => ctl.source.every(c => truth(c, a)));
if (!eq(sourceModels, [0]) || !eq(ctl.source_models, [0]) || ctl.output_mask !== 105)
  throw new Error("explicit source");
let replayed = 0; const fresh = new Set();
for (const cert of ctl.certificates) {
  if (truth(cert.target, cert.falsifying_assignment) || truth(cert.base, cert.falsifying_assignment))
    throw new Error("falsifier provenance");
  replayed += replayWeakening(cert, ctl.source, fresh);
}
if (replayed !== 24 || ctl.certificates.length !== 4) throw new Error("explicit 24");

const fp = data.false_factor_control, lines = fp.sources.map(canon);
for (const n of fp.nodes) {
  if (n.left_id >= lines.length || n.right_id >= lines.length) throw new Error("false parent");
  const out = resolve(lines[n.left_id], lines[n.right_id], n.pivot);
  if (!eq(out, canon(n.out))) throw new Error("false resolvent");
  lines.push(out);
}
if (fp.cost !== 1 || fp.root_id !== 2 || lines[2].length !== 0) throw new Error("false proof");

const labels = data.both_label_controls;
if (labels.even_parity_mask !== 105 || labels.odd_parity_mask !== 150 ||
    labels.even_models !== 4 || labels.odd_models !== 4 ||
    labels.even_entails_odd !== false || labels.odd_entails_even !== false ||
    labels.both_weighted_basis_cost !== 24) throw new Error("labels");

function parseRecord(obj) {
  if (!obj || typeof obj !== "object" || Array.isArray(obj) ||
      Object.keys(obj).sort().join(",") !== "basis,mask") throw new Error("schema");
  if (!Number.isInteger(obj.mask) || typeof obj.mask === "boolean" || obj.mask < 0 || obj.mask > 255)
    throw new Error("mask");
  if (!Array.isArray(obj.basis)) throw new Error("basis");
  const seen = new Set();
  for (const raw of obj.basis) {
    if (!Array.isArray(raw) || raw.length === 0 || raw.some(x => !Number.isInteger(x) || typeof x === "boolean" || Math.abs(x) < 1 || Math.abs(x) > 3))
      throw new Error("literal");
    const c = canon(raw);
    if (!eq(c, raw) || seen.has(key(c))) throw new Error("canonical/duplicate");
    seen.add(key(c));
  }
}
const malformed = [null, {}, {mask:-1,basis:[]}, {mask:256,basis:[]}, {mask:true,basis:[]},
  {mask:1.5,basis:[]}, {mask:1,basis:null}, {mask:1,basis:[[]]}, {mask:1,basis:[[0]]},
  {mask:1,basis:[[1,-1]]}, {mask:1,basis:[[2,1]]}, {mask:1,basis:[[1],[1]]}];
let malformedRejected = 0;
for (const m of malformed) { try { parseRecord(m); } catch (_) { malformedRejected++; } }
parseRecord({mask:105,basis:data.relations[105].basis});
if (malformedRejected !== 12 || data.malformed.rejected !== 12) throw new Error("malformed controls");

let corruptRejected = 0;
function expectReject(mutator, kind) {
  const clone = JSON.parse(JSON.stringify(data)); mutator(clone);
  try {
    if (kind === "weak") replayWeakening(clone.explicit_24_node_control.certificates[0], clone.explicit_24_node_control.source, new Set());
    else {
      const p = clone.false_factor_control, ls = p.sources.map(canon);
      for (const n of p.nodes) ls.push(resolve(ls[n.left_id], ls[n.right_id], n.pivot));
      if (ls[p.root_id].length !== 0) throw new Error("not contradiction");
    }
  } catch (_) { corruptRejected++; return; }
  throw new Error("corruption accepted");
}
expectReject(x => { x.explicit_24_node_control.certificates[0].base = [1,2]; }, "weak");
expectReject(x => { x.explicit_24_node_control.certificates[0].defs[0].out = 2; }, "weak");
expectReject(x => { x.explicit_24_node_control.certificates[0].defs[0].slots[0][0] *= -1; }, "weak");
expectReject(x => { x.explicit_24_node_control.certificates[0].res[0].pivot *= -1; }, "weak");
expectReject(x => { x.false_factor_control.nodes[0].pivot = -1; }, "false");

console.log(JSON.stringify({
  status: "PASS",
  raw_sha256: crypto.createHash("sha256").update(payload).digest("hex"),
  independent_relations: 256,
  independent_pairs: pairs,
  max_weighted_basis_cost: maxCost,
  max_masks: maxMasks,
  max_cost_pairs: maxPairs,
  max_basis_clauses: maxBasisSize,
  replayed_paid_nodes: replayed + 1,
  malformed_rejected: malformedRejected,
  corrupt_rejected: corruptRejected,
  verifier_wall_seconds: Number(process.hrtime.bigint() - started) / 1e9,
  verifier_peak_rss_kib: process.resourceUsage().maxRSS
}));
