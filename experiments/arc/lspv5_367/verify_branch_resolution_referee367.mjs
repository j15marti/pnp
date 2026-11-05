#!/usr/bin/env node
// Independent replay for REFEREE367.  No Python checker code is imported.

import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../..');
const typedPath = path.join(here, 'k4_tseitin_typed_branch_referee367.json');
const resPath = path.join(here, 'k4_tseitin_resolution_referee367.json');
const rawPath = path.join(root, 'results/raw/arc/2026-11-05_1048_LSPV5_REFEREE367_raw.json');
const outPath = path.join(root, 'results/raw/arc/2026-11-05_1048_LSPV5_REFEREE367_independent.json');

let assertions = 0;
function ok(x, msg) { assertions++; if (!x) throw new Error(msg); }
function canon(xs) {
  return [...new Set(xs.map(Number))].sort((a,b) => Math.abs(a)-Math.abs(b) || (a<0)-(b<0));
}
function eq(a,b) { return JSON.stringify(a) === JSON.stringify(b); }
function subset(a,b) { const s = new Set(b); return a.every(x => s.has(x)); }
function taut(c) { const s = new Set(c); return c.some(x => s.has(-x)); }
function resolve(left,right,pivot) {
  ok(left.includes(pivot), 'left pivot missing');
  ok(right.includes(-pivot), 'right pivot missing');
  return canon([...left.filter(x=>x!==pivot), ...right.filter(x=>x!==-pivot)]);
}
function sha(bytes) { return crypto.createHash('sha256').update(bytes).digest('hex'); }

function parseDimacs(text) {
  const lines = text.trim().split(/\n/).map(x=>x.trim()).filter(x=>x && !x.startsWith('c'));
  const h = lines.shift().split(/\s+/);
  ok(eq(h.slice(0,2), ['p','cnf']) && h.length===4, 'bad header');
  const n = Number(h[2]), m = Number(h[3]);
  const cs = lines.map(line => {
    const a = line.split(/\s+/).map(Number);
    ok(a.at(-1)===0 && !a.slice(0,-1).includes(0), 'bad terminator');
    return canon(a.slice(0,-1));
  });
  ok(cs.length===m, 'clause count mismatch');
  ok(cs.every(c=>c.every(x=>Math.abs(x)<=n)), 'variable out of range');
  return {n, cs};
}

const typedBytes = fs.readFileSync(typedPath);
const resBytes = fs.readFileSync(resPath);
const typed = JSON.parse(typedBytes);
const proof = JSON.parse(resBytes);
const raw = JSON.parse(fs.readFileSync(rawPath));
ok(typed.format === 'LSPV5-BCTX-1', 'typed format');
ok(proof.format === 'LSPV5-RES-1', 'resolution format');
const parsed = parseDimacs(typed.source_utf8);
ok(typed.source_utf8 === proof.source_utf8, 'source mismatch');
ok(sha(Buffer.from(typed.source_utf8)) === typed.source_sha256, 'typed source hash');
ok(typed.source_sha256 === proof.source_sha256, 'proof source hash');
ok(sha(typedBytes) === raw.typed.trace_sha256, 'trace byte hash');
ok(sha(resBytes) === raw.ordinary_resolution.proof_sha256, 'proof byte hash');

// Reconstruct the exact K4 odd-charge Tseitin clauses rather than trusting input.
const edges = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const incident = [[],[],[],[]];
edges.forEach((e,i) => { incident[e[0]].push(i+1); incident[e[1]].push(i+1); });
const expected = [];
for (let v=0; v<4; v++) for (let mask=0; mask<8; mask++) {
  const bits = [0,1,2].map(i => (mask>>i)&1);
  const wanted = v===0 ? 1 : 0;
  if ((bits.reduce((a,b)=>a+b,0)&1) !== wanted)
    expected.push(canon(incident[v].map((x,i)=>bits[i] ? -x : x)));
}
expected.sort((a,b)=>JSON.stringify(a).localeCompare(JSON.stringify(b)));
const got = [...parsed.cs].sort((a,b)=>JSON.stringify(a).localeCompare(JSON.stringify(b)));
ok(eq(got, expected), 'not exact K4 odd-charge encoding');

let models = 0;
for (let mask=0; mask<(1<<parsed.n); mask++) {
  const sat = parsed.cs.every(c => c.some(l => Boolean((mask>>(Math.abs(l)-1))&1)===(l>0)));
  if (sat) models++;
}
ok(models===0, 'odd-charge source is SAT');

// Context-typed DAG checker.
const nodes = typed.nodes;
for (let i=0; i<nodes.length; i++) {
  const n = nodes[i];
  ok(new Set(n.ctx.map(Math.abs)).size===n.ctx.length, `bad context ${i}`);
  ok(!taut(n.clause), `taut typed clause ${i}`);
  if (n.rule==='SRC') {
    ok(n.ctx.length===0 && eq(n.clause,parsed.cs[n.source_index]), `bad SRC ${i}`);
  } else if (n.rule==='ASSUME') {
    ok(n.clause.length===1 && n.ctx.includes(n.clause[0]), `bad ASSUME ${i}`);
  } else if (n.rule==='RES') {
    ok(n.parents.length===2 && n.parents.every(p=>p<i), `bad RES parents ${i}`);
    const a=nodes[n.parents[0]], b=nodes[n.parents[1]];
    ok(subset(a.ctx,n.ctx) && subset(b.ctx,n.ctx), `context leak ${i}`);
    ok(eq(resolve(a.clause,b.clause,n.pivot),n.clause), `bad RES ${i}`);
  } else if (n.rule==='MERGE') {
    ok(n.parents.length===2 && n.parents.every(p=>p<i), `bad MERGE parents ${i}`);
    const a=nodes[n.parents[0]], b=nodes[n.parents[1]], base=new Set(n.ctx);
    ok(eq(a.clause,n.clause) && eq(b.clause,n.clause), `merge clauses ${i}`);
    ok(a.ctx.length===n.ctx.length+1 && b.ctx.length===n.ctx.length+1, `merge sizes ${i}`);
    ok(subset(n.ctx,a.ctx) && subset(n.ctx,b.ctx) && a.ctx.includes(n.pivot) && b.ctx.includes(-n.pivot), `merge contexts ${i}`);
  } else throw new Error(`unknown typed rule ${n.rule}`);
}
ok(typed.final===nodes.length-1 && nodes.at(-1).ctx.length===0 && nodes.at(-1).clause.length===0, 'typed final');

// Ordinary shared-DAG Resolution checker.  No weakening/tautology/branch rule remains.
const lines = proof.lines;
for (let i=0; i<lines.length; i++) {
  const l=lines[i];
  if (l.rule==='SRC') {
    ok(eq(l.clause,parsed.cs[l.source_index]), `ordinary source ${i}`);
  } else if (l.rule==='RES') {
    ok(l.parents.length===2 && l.parents.every(p=>p<i), `ordinary parents ${i}`);
    ok(eq(resolve(lines[l.parents[0]].clause,lines[l.parents[1]].clause,l.pivot),l.clause), `ordinary RES ${i}`);
    ok(!taut(l.clause), `ordinary taut ${i}`);
  } else throw new Error(`non-Resolution rule ${i}`);
}
ok(proof.final===lines.length-1 && lines.at(-1).clause.length===0, 'ordinary final');
ok(lines.length===45 && lines.filter(x=>x.rule==='RES').length===29, 'ordinary count');
ok(nodes.length===283 && nodes.filter(x=>x.rule!=='SRC').length===267, 'typed paid count');

// Independent hostile controls.
const controls = {};
const mergeIndex = nodes.findIndex(x=>x.rule==='MERGE');
const mn = nodes[mergeIndex];
controls.omitted_and_branch = !(mn.parents[0]===mn.parents[1]) && !eq(nodes[mn.parents[0]].ctx,nodes[mn.parents[1]].ctx);
ok(controls.omitted_and_branch, 'merge control setup');
const firstRes = lines.findIndex(x=>x.rule==='RES');
let corruptRejected=false;
try { resolve(lines[lines[firstRes].parents[0]].clause, lines[lines[firstRes].parents[1]].clause, -lines[firstRes].pivot); }
catch { corruptRejected=true; }
controls.corrupt_pivot = corruptRejected;
ok(corruptRejected, 'corrupt pivot accepted');
controls.no_nonresolution_rules = lines.every(x=>x.rule==='SRC'||x.rule==='RES');
ok(controls.no_nonresolution_rules, 'extra ordinary rule');

const independent = {
  status: 'PASS/INDEPENDENT-NODE-REPLAY', assertions,
  typed_nodes: nodes.length, typed_paid: nodes.filter(x=>x.rule!=='SRC').length,
  resolution_lines: lines.length, resolution_inferences: lines.filter(x=>x.rule==='RES').length,
  source_models: models, controls,
  trace_sha256: sha(typedBytes), resolution_sha256: sha(resBytes),
  limitation: 'Declared REFEREE367 formats, not authoritative historical R_mix341.'
};
fs.writeFileSync(outPath, JSON.stringify(independent,null,2)+'\n');
console.log(JSON.stringify(independent,null,2));
