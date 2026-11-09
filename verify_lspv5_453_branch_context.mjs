#!/usr/bin/env node
// Independent verifier for the proposed BRANCH_CTX run-453 control packet.
// This is not the historical R_mix341 checker.

import fs from 'node:fs';

const path = process.argv[2];
if (!path) throw new Error('usage: verify_lspv5_453_branch_context.mjs RAW.json');
const doc = JSON.parse(fs.readFileSync(path, 'utf8'));
let checks = 0;

function reject(code, detail='') {
  const e = new Error(`${code}${detail ? `: ${detail}` : ''}`);
  e.code = code;
  throw e;
}
function norm(xs) {
  if (!Array.isArray(xs) || xs.some(x => !Number.isInteger(x) || x === 0)) reject('TYPE');
  const out = [...new Set(xs)].sort((a,b) => Math.abs(a)-Math.abs(b) || a-b);
  if (out.some(x => out.includes(-x))) reject('TAUTOLOGY');
  return out;
}
function same(a,b) { return JSON.stringify(norm(a)) === JSON.stringify(norm(b)); }
function union(a,b) { return norm([...a,...b]); }

function verify(packet) {
  if (packet.calculus !== 'BRANCH_CTX_PROPOSED_CONTROL' || packet.historical_R_mix341_extension !== false)
    reject('HEADER');
  const byId = new Map();
  const depth = new Map();
  const ancestry = new Map();
  let paid = 0, sources = 0;
  const directUses = new Map();

  for (const n of packet.nodes) {
    if (!Number.isInteger(n.id) || byId.has(n.id)) reject('DUPLICATE_ID');
    const ants = [];
    for (const id of n.antecedents) {
      if (!byId.has(id)) {
        const later = packet.nodes.some(z => z.id === id);
        reject(later ? 'FORWARD_REFERENCE' : 'MISSING_REFERENCE');
      }
      ants.push(byId.get(id));
      directUses.set(id, (directUses.get(id) || 0) + 1);
    }
    const clause = norm(n.clause), ctx = norm(n.context);
    let d = 0, anc = new Set();

    if (n.rule === 'SOURCE') {
      if (ants.length !== 0 || ctx.length !== 0) reject('SOURCE_CONTEXT');
      sources++;
      anc.add(n.id);
    } else if (n.rule === 'ASSUME') {
      if (ants.length !== 0 || clause.length !== 1 || !same(clause, ctx)) reject('ASSUME_CONTEXT');
      paid++; d = 1;
    } else if (n.rule === 'RES') {
      if (ants.length !== 2 || !Number.isInteger(n.pivot) || n.pivot <= 0) reject('RES_SHAPE');
      const [l,r] = ants, p = n.pivot;
      const oriented = l.clause.includes(p) && r.clause.includes(-p);
      const reversed = l.clause.includes(-p) && r.clause.includes(p);
      if (!oriented && !reversed) reject('RES_PIVOT');
      const want = norm([...l.clause.filter(x => Math.abs(x)!==p), ...r.clause.filter(x => Math.abs(x)!==p)]);
      if (!same(clause, want)) reject('RES_CLAUSE');
      if (!same(ctx, union(l.context, r.context))) reject('RES_CONTEXT');
      paid++; d = Math.max(depth.get(l.id), depth.get(r.id)) + 1;
      anc = new Set([...ancestry.get(l.id), ...ancestry.get(r.id)]);
    } else if (n.rule === 'SPLIT_AND') {
      if (ants.length !== 2) reject('SPLIT_ARITY');
      if (!Number.isInteger(n.split) || n.split <= 0 || clause.length !== 0) reject('SPLIT_SHAPE');
      const [l,r] = ants;
      if (l.clause.length !== 0 || r.clause.length !== 0) reject('SPLIT_PREMISE');
      const plus = norm([...ctx, n.split]), minus = norm([...ctx, -n.split]);
      const ok = (same(l.context, plus) && same(r.context, minus)) ||
                 (same(r.context, plus) && same(l.context, minus));
      if (!ok) reject('SPLIT_CONTEXT');
      paid++; d = Math.max(depth.get(l.id), depth.get(r.id)) + 1;
      anc = new Set([...ancestry.get(l.id), ...ancestry.get(r.id)]);
    } else {
      reject('UNKNOWN_RULE');
    }
    byId.set(n.id, {...n, clause, context:ctx});
    depth.set(n.id, d);
    ancestry.set(n.id, anc);
    checks++;
  }

  if (!byId.has(packet.root)) reject('ROOT_MISSING');
  const root = byId.get(packet.root);
  if (root.clause.length !== 0) reject('ROOT_NOT_FALSE');
  if (root.context.length !== 0) reject('ROOT_CONTEXT');
  const ledger = packet.ledger;
  const rootAnc = [...ancestry.get(packet.root)].sort((a,b)=>a-b);
  if (ledger.source_nodes !== sources || ledger.paid_distinct_nodes !== paid ||
      ledger.weighted_span !== depth.get(packet.root) ||
      JSON.stringify(ledger.root_source_ancestors) !== JSON.stringify(rootAnc) ||
      directUses.get(ledger.shared_source) !== ledger.shared_source_direct_uses) reject('LEDGER');
  return {paid, sources, span:depth.get(packet.root), root_source_ancestors:rootAnc};
}

if (doc.artifact !== 'LSPV5-BRANCH-CONTEXT-AND-JOIN453') reject('DOCUMENT_HEADER');
const good = verify(doc.valid);
const rejected = [];
for (const m of doc.mutations) {
  let code = 'ACCEPTED';
  try { verify(m.packet); } catch (e) { code = e.code || 'UNCLASSIFIED'; }
  if (m.expected !== 'REJECT' || code !== m.expected_code) reject('MUTATION_RESULT', `${m.label}:${code}`);
  rejected.push({label:m.label, code});
  checks++;
}
console.log(JSON.stringify({
  status:'PASS',
  scope:doc.scope,
  valid:good,
  rejected,
  checks,
}, null, 2));
