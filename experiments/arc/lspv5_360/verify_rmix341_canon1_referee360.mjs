#!/usr/bin/env node
// Independent no-import semantic replay of the REFEREE360 K4 certificate.
import fs from "node:fs";
import crypto from "node:crypto";

const p = "results/raw/arc/2026-11-05_0348_LSPV5_REFEREE360_raw.json";
const raw = JSON.parse(fs.readFileSync(p, "utf8"));
const doc = raw.odd_certificate;
let checks = 0;
function ok(x, m) { if (!x) throw new Error(m); checks++; }
function stable(x) {
  if (Array.isArray(x)) return `[${x.map(stable).join(",")}]`;
  if (x && typeof x === "object") return `{${Object.keys(x).sort().map(k => `${JSON.stringify(k)}:${stable(x[k])}`).join(",")}}`;
  return JSON.stringify(x);
}
const h = crypto.createHash("sha256").update(stable(doc.source), "ascii").digest("hex");
ok(h === doc.source_sha256, "source hash");
ok(doc.format === "Rmix341-CANON1", "format");
ok(doc.source.nvars === 6 && doc.source.clauses.length === 16, "K4 dimensions");

const views = new Map();
const key = r => r.src !== undefined ? `s:${r.src}:clause` : `n:${r.node}:${r.view}:${r.facet ?? ""}`;
const clauseEval = (c, env) => c.some(l => env[Math.abs(l)] === +(l > 0));
const factorEval = (f, env) => f.truth[f.support.reduce((z, v, i) => z | (env[v] << i), 0)];
const affineEval = (a, env) => a.mask.reduce((z, v) => z ^ env[v], 0) === a.rhs;
const evalRel = (r, env) => r.kind === "clause" ? clauseEval(r.body, env) : r.kind === "factor" ? factorEval(r.body, env) : affineEval(r.body, env);
for (let i = 0; i < doc.source.clauses.length; i++) {
  const c = doc.source.clauses[i];
  ok(c.every((l, j) => j === 0 || Math.abs(c[j-1]) < Math.abs(l)), `canonical source ${i}`);
  views.set(`s:${i}:clause`, {kind: "clause", body: c});
}
function get(r, before) {
  ok(!("wire" in r) && !("selector" in r), "no wire selector");
  if (r.node !== undefined) ok(Number.isInteger(r.node) && r.node < before, "backward node ref");
  const v = views.get(key(r)); ok(!!v, `view ${key(r)}`); return v;
}
function add(k, v) { ok(!views.has(k), `new view ${k}`); views.set(k, v); }
function support(r) { return r.kind === "clause" ? [...new Set(r.body.map(Math.abs))] : r.body.support ?? r.body.mask; }
function envs(s) { return Array.from({length: 1 << s.length}, (_, z) => Object.fromEntries(s.map((v, i) => [v, (z >> i) & 1]))); }

for (let i = 0; i < doc.nodes.length; i++) {
  const n = doc.nodes[i]; ok(n.id === i, `id ${i}`);
  if (n.rule === "AND3") {
    const a = get(n.left, i), b = get(n.right, i);
    const s = [...new Set([...support(a), ...support(b)])].sort((x,y)=>x-y);
    ok(s.length <= 3 && s.every(v => v <= 6), `AND3 support ${i}`);
    ok(JSON.stringify(n.factor.support) === JSON.stringify(s), `AND3 declared support ${i}`);
    for (const e of envs(s)) ok(factorEval(n.factor, e) === +(evalRel(a,e) && evalRel(b,e)), `AND3 table ${i}`);
    add(`n:${i}:factor:`, {kind:"factor", body:n.factor});
    if (n.affine) {
      for (const e of envs(s)) ok(factorEval(n.factor,e) === +affineEval(n.affine,e), `affine annotation ${i}`);
      add(`n:${i}:affine:`, {kind:"affine", body:n.affine});
    }
  } else if (n.rule === "GF2") {
    const a = get(n.left, i), b = get(n.right, i);
    ok(a.kind === "affine" && b.kind === "affine", `GF2 parents ${i}`);
    const symmetric = [...new Set([...a.body.mask, ...b.body.mask])].filter(v => a.body.mask.includes(v) !== b.body.mask.includes(v)).sort((x,y)=>x-y);
    ok(JSON.stringify(symmetric) === JSON.stringify(n.affine.mask), `GF2 mask ${i}`);
    ok((a.body.rhs ^ b.body.rhs) === n.affine.rhs, `GF2 rhs ${i}`);
    add(`n:${i}:affine:`, {kind:"affine", body:n.affine});
  } else throw new Error(`unexpected rule in K4 replay: ${n.rule}`);
}
const fin = get(doc.final, doc.nodes.length);
ok(fin.kind === "affine" && fin.body.mask.length === 0 && fin.body.rhs === 1, "contradiction");
ok(doc.nodes.length === 15, "4h-1 paid nodes");
ok(raw.odd_k4.paid_nodes === 15 && raw.odd_k4.truth_assignments === 128, "producer ledger");
ok(raw.mutations.length === 7 && raw.controls.length === 7, "negative controls present");
for (const x of [...raw.mutations, ...raw.controls]) ok(typeof x.reason === "string" && x.reason.length > 0, `reason ${x.name}`);
console.log(JSON.stringify({status:"PASS", checks, paid_nodes:doc.nodes.length, final:fin.body, source_sha256:h}));
