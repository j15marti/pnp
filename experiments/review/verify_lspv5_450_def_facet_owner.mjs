#!/usr/bin/env node
'use strict';
// Cross-language replay of the proposed ownerized packet. This is not the
// missing authoritative historical R_mix341 checker.
import fs from 'node:fs';
import assert from 'node:assert/strict';

function norm(xs) {
  assert(!xs.includes(0));
  const s = new Set(xs);
  for (const x of s) assert(!s.has(-x));
  return [...s].sort((a,b) => Math.abs(a)-Math.abs(b) || Number(a<0)-Number(b<0));
}

const d = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
assert.equal(d.status, 'PASS');
const p = d.proposed_ownerized_packet;
const lines = new Map();
for (const s of p.original_sources) {
  assert(!lines.has(s.line_id));
  lines.set(s.line_id, norm(s.clause));
}
assert.equal(lines.size, 8);
const outputs = new Set();
let facets = 0;
for (const g of p.defs) {
  const q=g.output, a=g.left_lit, b=g.right_lit;
  assert.notEqual(Math.abs(a), Math.abs(b));
  assert(q > Math.max(Math.abs(a), Math.abs(b)) && !outputs.has(q));
  outputs.add(q);
  const expected={left:norm([a,-q]),right:norm([b,-q]),back:norm([-a,-b,q])};
  const table=[];
  for (const [av,bv] of [[0,0],[0,1],[1,0],[1,1]]) {
    const va=a>0?av:1-av, vb=b>0?bv:1-bv;
    table.push(va & vb);
  }
  assert.deepEqual(table,g.truth_table_00_01_10_11);
  for (const [name,item] of Object.entries(g.facets)) {
    assert.deepEqual(norm(item.clause),expected[name]);
    assert(!lines.has(item.line_id));
    lines.set(item.line_id,expected[name]); facets++;
  }
}
assert.equal(outputs.size,15); assert.equal(facets,45);
for (const n of p.resolution) {
  const l=lines.get(n.left.line_id), r=lines.get(n.right.line_id), x=n.pivot;
  assert(l && r && l.includes(x) && r.includes(-x));
  const got=norm([...l.filter(y=>y!==x),...r.filter(y=>y!==-x)]);
  assert.deepEqual(got,norm(n.clause));
  lines.set(n.line_id,got);
}
assert.equal(p.resolution.length,131);
assert.deepEqual(d.cost,{distinct_paid_nodes:146,paid_DEF:15,paid_RES:131});
assert.equal(d.raw_packet.nonoriginal_DEF_facets_marked_SOURCE,45);
assert.equal(d.raw_packet.DEF_records,0);
for (const v of Object.values(d.controls)) assert.equal(v,true);
console.log(JSON.stringify({status:'PASS',language:'Node.js',original_sources:8,
  owned_facets:45,paid_defs:15,paid_res:131,historical_raw_DEF_records:0,
  scope:'cross-language proposed-owner adapter replay; historical bytes unauthenticated'}));
