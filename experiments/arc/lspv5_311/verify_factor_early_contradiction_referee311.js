#!/usr/bin/env node
"use strict";

const fs = require("fs");
const crypto = require("crypto");
const started = process.hrtime.bigint();

const path = "results/raw/arc/lspv5_311/factor_early_contradiction_referee311.json";
const payload = fs.readFileSync(path, "utf8");
const data = JSON.parse(payload);

function canon(xs) {
  const s = [...new Set(xs)].sort((a, b) => Math.abs(a) - Math.abs(b) || (a < 0) - (b < 0));
  if (s.some(x => x === 0 || s.includes(-x))) throw new Error("nonclause");
  return s;
}
function eq(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
function key(c) { return JSON.stringify(canon(c)); }
function resolve(left, right, pivot) {
  left = canon(left); right = canon(right);
  if (!left.includes(pivot) || !right.includes(-pivot)) throw new Error("bad pivot");
  return canon([...left.filter(x => x !== pivot), ...right.filter(x => x !== -pivot)]);
}
function truth(clause, assignment) {
  return clause.some(l => Boolean((assignment >> (Math.abs(l) - 1)) & 1) === (l > 0));
}
function blocker(a) {
  return canon([1, 2, 3].map(v => ((a >> (v - 1)) & 1) ? -v : v));
}
function slots(out, left, right) {
  return [canon([-out, left]), canon([-out, right]), canon([out, -left, -right])];
}

function replayWeakening(cert, source) {
  const known = new Set(source.map(key));
  if (!known.has(key(cert.base))) throw new Error("base not source");
  let paid = 0;
  const fresh = new Set();
  for (const d of cert.defs) {
    if (Math.abs(d.out) <= 3 || fresh.has(d.out)) throw new Error("freshness");
    fresh.add(d.out);
    const want = slots(d.out, d.left, d.right);
    if (!eq(d.slots.map(canon), want)) throw new Error("bad definition slots");
    for (const c of want) known.add(key(c));
    paid++;
  }
  for (const r of cert.res) {
    if (!known.has(key(r.left)) || !known.has(key(r.right))) throw new Error("missing parent");
    const out = resolve(r.left, r.right, r.pivot);
    if (!eq(out, canon(r.out))) throw new Error("bad resolvent");
    known.add(key(out));
    paid++;
  }
  if (!known.has(key(cert.target)) || paid !== cert.cost) throw new Error("bad root/cost");
  return paid;
}

function replayCube(proof) {
  const lines = proof.sources.map(canon);
  let paid = 0;
  for (const n of proof.nodes) {
    if (!Number.isInteger(n.left_id) || !Number.isInteger(n.right_id) ||
        n.left_id < 0 || n.right_id < 0 || n.left_id >= lines.length || n.right_id >= lines.length)
      throw new Error("bad parent id");
    const out = resolve(lines[n.left_id], lines[n.right_id], n.pivot);
    if (!eq(out, canon(n.out))) throw new Error("bad cube resolvent");
    lines.push(out); paid++;
  }
  if (paid !== proof.cost || proof.root_id !== lines.length - 1 || lines[proof.root_id].length !== 0)
    throw new Error("bad cube root/cost");
  return paid;
}

let pairs = 0, satPairs = 0, unsatPairs = 0, max = -1, extrema = 0;
for (let input = 0; input < 256; input++) {
  for (let output = 0; output < 256; output++) {
    if ((input & (~output & 255)) !== 0) continue;
    pairs++;
    const cost = input === 0 ? 7 : 6 * (8 - output.toString(2).replace(/0/g, "").length);
    if (input === 0) unsatPairs++; else satPairs++;
    if (cost > max) { max = cost; extrema = 1; } else if (cost === max) extrema++;
  }
}
if (!eq([pairs, satPairs, unsatPairs, max, extrema], [6561, 6305, 256, 42, 8]))
  throw new Error("independent enumeration mismatch");

const ctl = data.explicit_42_node_control;
const models = [...Array(8).keys()].filter(a => ctl.source.every(c => truth(c, a)));
if (!eq(models, [0]) || !eq(ctl.models, [0])) throw new Error("unique model control");
let explicitCost = 0;
for (const cert of ctl.certificates) {
  if (truth(cert.base, cert.assignment) || !eq(canon(cert.target), blocker(cert.assignment)))
    throw new Error("wrong blocker provenance");
  explicitCost += replayWeakening(cert, ctl.source);
}
if (explicitCost !== 42 || ctl.certificates.length !== 7) throw new Error("42 control");
if (replayCube(data.false_factor_control) !== 7) throw new Error("false control");

const labels = data.both_label_controls;
const pop = x => x.toString(2).replace(/0/g, "").length;
if (pop(labels.even_parity_mask) !== 4 || pop(labels.odd_parity_mask) !== 4 ||
    (labels.even_parity_mask & (~labels.odd_parity_mask & 255)) === 0 || labels.wrong_label_entailment !== false)
  throw new Error("both-label control");
if (data.malformed.rejected !== 10 || data.malformed.valid !== 1) throw new Error("malformed control");

let corruptRejected = 0;
function expectReject(mutator, kind) {
  const clone = JSON.parse(JSON.stringify(data));
  mutator(clone);
  try {
    if (kind === "weak") replayWeakening(clone.explicit_42_node_control.certificates[0], clone.explicit_42_node_control.source);
    else replayCube(clone.false_factor_control);
  } catch (_) { corruptRejected++; return; }
  throw new Error("corruption accepted");
}
expectReject(x => { x.explicit_42_node_control.certificates[0].base = [1, 2]; }, "weak");
expectReject(x => { x.explicit_42_node_control.certificates[0].defs[0].slots[0][0] *= -1; }, "weak");
expectReject(x => { x.explicit_42_node_control.certificates[0].res[0].pivot *= -1; }, "weak");
expectReject(x => { x.false_factor_control.nodes[0].out = []; }, "cube");
expectReject(x => { x.false_factor_control.nodes[0].left_id = 99; }, "cube");

console.log(JSON.stringify({
  status: "PASS",
  raw_sha256: crypto.createHash("sha256").update(payload).digest("hex"),
  independent_pairs: pairs,
  max_bound: max,
  extremal_pairs: extrema,
  replayed_weakening_nodes: explicitCost,
  replayed_cube_nodes: 7,
  corrupt_rejected: corruptRejected,
  verifier_wall_seconds: Number(process.hrtime.bigint() - started) / 1e9,
  verifier_peak_rss_kib: process.resourceUsage().maxRSS
}));
