#!/usr/bin/env node
/* Independent parser/referee for LSPV-2/435. Uses original immutable binary
   sources, does not import the Python producer. Host resources are not FLMV. */
import fs from 'node:fs';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const path = new URL('../../results/raw/arc/2026-11-05_2216_LSPV2_PIVOTAL435.json', import.meta.url);
const raw = JSON.parse(fs.readFileSync(path, 'utf8'));
let count = 0;
function ok(a,b) { assert.deepEqual(a,b); count++; }
function parse(bits) {
  if (!/^[01]+$/.test(bits) || bits.slice(0,8)!=='10100111') throw Error('magic');
  let i=8;
  function unary() {let x=0;while(i<bits.length && bits[i]==='1'){i++;x++;}if(bits[i++]!=='0'||x<1)throw Error('unary');return x;}
  function read(w) {if(i+w>bits.length)throw Error('truncated');const n=Number.parseInt(bits.slice(i,i+w),2);i+=w;return n;}
  const h=unary(),m=unary(),w=Math.max(1,Math.floor(Math.log2(m))+1);
  if(m*2!==3*h)throw Error('not cubic');
  const edges=[];
  for(let j=0;j<m;j++){
    let u=read(w),v=read(w);if(!(u<v && v<h))throw Error('edge');
    if(j>0 && (edges[j-1][0]>u || (edges[j-1][0]===u && edges[j-1][1]>=v)))throw Error('edge order');
    edges.push([u,v]);
  }
  const slots=Array.from({length:h},()=>[]);
  edges.forEach(([u,v],j)=>{slots[u].push(j);slots[v].push(j)});
  if(!slots.every(z=>z.length===3))throw Error('degree');
  const reached=new Set([0]);let frontier=[0];
  while(frontier.length){const v=frontier.pop();for(const eid of slots[v]){
    const [a,b]=edges[eid],other=a===v?b:a;
    if(!reached.has(other)){reached.add(other);frontier.push(other)}
  }}
  if(reached.size!==h)throw Error('disconnected');
  const charge=[],pivots=[];
  for(let v=0;v<h;v++){
    slots[v].sort((a,b)=>a-b);
    const [a,b,c]=slots[v], points=[];
    let ch=null;
    for(let row=0;row<4;row++){
      const p=(row>>1)&1,q=row&1;
      const sigs=[],ids=[];
      for(let z=0;z<3;z++){
        if(z===2)points.push(i);
        sigs.push(read(1)); ids.push(read(w));
      }
      if(ids[0]!==a||ids[1]!==b||ids[2]!==c||sigs[0]!==p||sigs[1]!==q)throw Error('row');
      const present=p^q^1^sigs[2];
      if(ch===null)ch=present;
      if(ch!==present)throw Error('charge inconsistent');
    }
    charge.push(ch);pivots.push(points);
  }
  if(bits.slice(i)!=='00')throw Error('terminator');
  return {h,m,edges,charge,pivots,bits};
}
const parsed=[];
for(const fixture of raw.fixtures){
  const r=parse(fixture.source_bits);parsed.push(r);
  ok(r.charge.join(''),fixture.charge_bits);
  ok(crypto.createHash('sha256').update(fixture.source_bits).digest('hex'),fixture.sha256);
  ok((r.charge.reduce((a,b)=>a^b,0)===0)?'SAT':'UNSAT',fixture.label);
  ok(r.pivots.length,r.h);
  for(let v=0;v<r.h;v++){
    const y=r.bits.split('');
    r.pivots[v].forEach(p=>{y[p]=y[p]==='0'?'1':'0'});
    const flip=parse(y.join(''));
    ok(flip.charge[v],r.charge[v]^1);
    ok(flip.charge.reduce((a,b)=>a^b,0),1^r.charge.reduce((a,b)=>a^b,0));
    for(let z=0;z<r.h;z++)if(z!==v)ok(flip.charge[z],r.charge[z]);
    ok(r.pivots[v].length,4);
  }
  const seen=new Set();
  for(let assignment=0;assignment<2**r.m;assignment++){
    const vector=Array(r.h).fill(0);
    r.edges.forEach(([u,v],eid)=>{let bit=(assignment>>eid)&1;vector[u]^=bit;vector[v]^=bit});
    seen.add(vector.join(''));
    ok(vector.reduce((a,b)=>a^b,0),0);
  }
  ok(seen.size,2**(r.h-1));
  const y=r.bits.split(''); const first=r.pivots[0][0];y[first]=y[first]==='0'?'1':'0';
  assert.throws(()=>parse(y.join('')));count++;
  for(const bad of [r.bits.slice(1),r.bits.slice(0,-1),r.bits+'1',r.bits.slice(0,10)+'x'+r.bits.slice(11)]){
    assert.throws(()=>parse(bad));count++;
  }
}
const groupBy=Object.fromEntries(raw.families.map(g=>[g.name,g]));
for(let j=0;j<parsed.length;j+=2){
  const x=parsed[j],y=parsed[j+1],g=groupBy[raw.fixtures[j].graph];
  ok(x.h,g.vertices);ok(x.m,g.edges);ok(x.bits.length,g.encoding_bits);
  ok(x.bits.length,y.bits.length);
  const changed=x.bits.split('').flatMap((c,p)=>c===y.bits[p]?[]:[p]);
  ok(changed.join(','),x.pivots[0].join(','));
  for(let mask=1;mask<(1<<x.h);mask++){
    const modified=x.bits.split('');
    for(let v=0;v<x.h;v++)if(mask&(1<<v))for(const p of x.pivots[v])modified[p]=modified[p]==='0'?'1':'0';
    const c=parse(modified.join(''));
    const reads=x.pivots.map(pos=>pos[0]);
    ok(reads.some(pos=>modified[pos]!==x.bits[pos]),true);
    ok(c.charge.reduce((a,b)=>a^b,0),mask.toString(2).split('1').length%2===0?1:0);
  }
}
console.log(JSON.stringify({independent_assertions:count,fixture_count:parsed.length,groups:raw.families.map(x=>x.name)},null,2));
