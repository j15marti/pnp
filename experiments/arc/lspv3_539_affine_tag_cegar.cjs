#!/usr/bin/env node
'use strict';
// LSPV-3/539. Independent local semantic verifier, NOT historical R_mix341 checker.
// Invoke node experiments/arc/lspv3_539_affine_tag_cegar.cjs results/raw/arc/2026-11-09_1124_LSPV3_539_AFFINE_TAG_RAW.json
const fs=require('fs'), assert=require('assert');
const pop=m=>{let s=0;for(;m;m&=m-1)s++;return s};
const bit=t=>1<<t;
function hull(m){
  const pts=[];for(let t=0;t<8;t++)if(m&bit(t))pts.push(t);
  if(!pts.length)return 0;
  const v=pts[0],span=new Set([0]);
  for(const t of pts){const d=t^v;for(const e of [...span])span.add(e^d)}
  let h=0;for(const d of span)h|=bit(v^d);return h;
}
function clause(forbidden){return [1,2,3].map(i=>(forbidden&(1<<(i-1)))?-i:i)}
function clauseMask(c){
  let m=0;for(let t=0;t<8;t++){
    const ok=c.some(l=>l>0?((t>>(l-1))&1):!((t>>(-l-1))&1));
    if(ok)m|=bit(t);
  }return m;
}
function parity(t){let s=0;for(;t;t&=t-1)s++;return s%2}
function row(a,r){let m=0;for(let t=0;t<8;t++)if(parity(a&t)===r)m|=bit(t);return m}
const record=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
let checks=0,imp=0,strict=0;
for(let m=0;m<256;m++){
  const H=hull(m);assert.equal(m&~H,0);assert.equal(hull(H),H);checks+=2;
  if(m){assert.equal(m===H,pop(m)===pop(H));checks++}
  for(let a=1;a<8;a++)for(let r=0;r<2;r++){
    const E=row(a,r);
    assert.equal(m!==0&&m===E,m!==0&&pop(m)===4&&H===E);checks++;
  }
  for(let n=0;n<256;n++){
    const j=m&n;
    assert.equal(hull(j)&~(H&hull(n)),0);
    strict+=Number(hull(j)!==(H&hull(n)));
    imp+=Number((m&~n)===0);checks++;
  }
}
const P=row(7,0),Q=P&~1;
assert.equal(P,105);assert.equal(Q,104);checks+=2;
assert.equal(hull(P),hull(Q));checks++;
const A=P&~bit(0),B=P&~bit(3);
assert.deepEqual([hull(A),pop(A)],[hull(B),pop(B)]);
assert.notEqual(pop(A&A),pop(A&B));checks+=2;
const sources=[];for(let t=0;t<8;t++)if(!(P&bit(t)))sources.push(clause(t));
assert.equal(sources.length,4);checks++;
let product=255;for(const c of sources){product&=clauseMask(c);checks++}
assert.equal(product,P);checks++;
const stronger=product&clauseMask(clause(0));
assert.equal(stronger,Q);assert.notEqual(stronger,row(7,0));checks+=2;
assert.equal(imp,record.cases.true_unary_implications);
assert.equal(strict,record.cases.hull_meet_strict_loss_pairs);checks+=2;
assert.equal(stronger,record.witness.extra_and3_factor);checks++;
console.log(JSON.stringify({status:'PASS',checks,unary_implications:imp,strict_hull_meet_losses:strict,
  method:'Independent XOR-span affine hull; local semantics only, not native R_mix341 checker'},null,2));
