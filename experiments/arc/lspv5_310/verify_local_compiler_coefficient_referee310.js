#!/usr/bin/env node
'use strict';

// No-import independent verifier for REFEREE310.
const fs = require('fs');
const crypto = require('crypto');
const assert = require('assert');
const path = 'results/raw/arc/lspv5_310/local_compiler_coefficient_referee310.json';
const bytes = fs.readFileSync(path);
const raw = JSON.parse(bytes.toString('utf8'));

let assertions = 0;
function ok(x, msg) { assertions++; assert(x, msg); }
function eq(a, b, msg) { assertions++; assert.deepStrictEqual(a, b, msg); }
function canon(xs) {
  const u = [...new Set(xs)].sort((a,b)=>Math.abs(a)-Math.abs(b) || Number(a<0)-Number(b<0));
  ok(!u.some(x=>u.includes(-x)), 'tautology');
  return u;
}
function key(c) { return canon(c).join(','); }
function satLit(lit,a) { const v=Boolean((a>>(Math.abs(lit)-1))&1); return lit>0?v:!v; }
function satClause(c,a) { return c.some(l=>satLit(l,a)); }
function blocker(a) { return canon([1,2,3].map(v=>((a>>(v-1))&1)?-v:v)); }
function resolve(a,b,p) {
  ok(a.includes(p) && b.includes(-p), 'pivot absent');
  const s = new Set([...a.filter(x=>x!==p), ...b.filter(x=>x!==-p)]);
  ok(![...s].some(x=>s.has(-x)), 'tautological resolvent');
  return canon([...s]);
}
function gateSlots(out,left,right) {
  return [canon([-out,left]), canon([-out,right]), canon([out,-left,-right])];
}

const clauses=[];
for(const a of [-1,0,1])for(const b of [-1,0,1])for(const c of [-1,0,1]) {
  const ss=[a,b,c], out=[];
  for(let i=0;i<3;i++)if(ss[i])out.push(ss[i]*(i+1));
  clauses.push(canon(out));
}
clauses.sort((a,b)=>a.length-b.length || key(a).localeCompare(key(b)));
eq(new Set(clauses.map(key)).size,27,'27 clauses');

function verifyCert(cert) {
  const base=canon(cert.base), target=canon(cert.target);
  ok(base.length>0 && base.every(x=>target.includes(x)), 'base subset target');
  const avail=new Map([[key(base),base]]);
  const fresh=new Set();
  let defs=0;
  for(const d of cert.defs) {
    ok(Number.isInteger(d.out) && d.out>=4 && !fresh.has(d.out), 'fresh output');
    ok(Math.abs(d.left)!==Math.abs(d.right), 'distinct gate inputs');
    fresh.add(d.out); defs++;
    const slots=gateSlots(d.out,d.left,d.right);
    eq(d.slots.map(canon),slots,'gate slots');
    for(const s of slots)avail.set(key(s),s);
  }
  let res=0, last=base;
  for(const line of cert.res) {
    const l=canon(line.left), r=canon(line.right), out=canon(line.out);
    ok(avail.has(key(l)) && avail.has(key(r)), 'antecedent availability');
    eq(resolve(l,r,line.pivot),out,'resolution output');
    avail.set(key(out),out); last=out; res++;
  }
  eq(last,target,'final target');
  eq(defs+res,cert.cost,'paid cost');
  ok(cert.cost<=6,'six-node blocker bound');
  return true;
}

let falsePairs=0;
const hist={};
for(const cert of raw.blocker_certificates) {
  ok(cert.assignment>=0 && cert.assignment<8,'assignment range');
  ok(!satClause(cert.base,cert.assignment),'base false');
  eq(canon(cert.target),blocker(cert.assignment),'complete blocker');
  verifyCert(cert);
  falsePairs++;
  hist[cert.cost]=(hist[cert.cost]||0)+1;
}
eq(falsePairs,56,'all false clause/assignment pairs');
eq(hist,{'0':8,'5':24,'6':24},'blocker cost histogram');

// Independent exhaustive semantic count.  For canonical factor CNFs, every
// full blocker needed for an entailed target is already a source; cube
// elimination therefore costs exactly 2^(3-|C|)-1 in this construction.
let entailed=0, maxCanonical=0, satRelations=0, unsatRelations=0;
const canonicalHist={};
for(let mask=0;mask<256;mask++) {
  const models=[];
  for(let a=0;a<8;a++)if((mask>>a)&1)models.push(a);
  models.length?satRelations++:unsatRelations++;
  for(const c of clauses) {
    if(models.every(a=>satClause(c,a))) {
      entailed++;
      const count=(2**(3-c.length))-1;
      maxCanonical=Math.max(maxCanonical,count);
      canonicalHist[count]=(canonicalHist[count]||0)+1;
    }
  }
}
eq([entailed,satRelations,unsatRelations,maxCanonical],[1889,255,1,7],'semantic exhaustive totals');
eq(raw.finite_audit.entailed_clause_cases,entailed,'raw entailed total');
eq(raw.finite_audit.observed_max_compiler_cost_on_canonical_relations,7,'raw canonical max');
eq(raw.symbolic_bounds.single_complete_blocker,6,'single blocker coefficient');
eq(raw.symbolic_bounds.factor_translation_coefficient,48,'factor coefficient');
eq(raw.symbolic_bounds.general_local_implicate_coefficient,32,'general coefficient');
eq(raw.finite_audit.parity_even_models,4,'even parity');
eq(raw.finite_audit.parity_odd_models,4,'odd parity');
eq(raw.finite_audit.malformed_rejected,11,'malformed controls');

// Corruption tests must fail locally and independently.
const seed=raw.blocker_certificates.find(x=>x.cost===6);
ok(Boolean(seed),'cost-six seed');
let corruptRejected=0;
for(let kind=0;kind<5;kind++) {
  const x=JSON.parse(JSON.stringify(seed));
  if(kind===0)x.target[0]*=-1;
  if(kind===1)x.cost++;
  if(kind===2)x.defs[0].slots[0][0]*=-1;
  if(kind===3)x.res[0].pivot*=-1;
  if(kind===4)x.res[x.res.length-1].out=[];
  try { verifyCert(x); } catch (_) { corruptRejected++; }
}
eq(corruptRejected,5,'corrupt certificates rejected');

const digest=crypto.createHash('sha256').update(bytes).digest('hex');
console.log(JSON.stringify({
  status:'PASS', assertions, raw_sha256:digest,
  blocker_certificates:falsePairs, entailed_cases:entailed,
  max_blocker_cost:6, max_canonical_cost:7,
  malformed_rejected:11, corrupt_rejected:corruptRejected
}));
