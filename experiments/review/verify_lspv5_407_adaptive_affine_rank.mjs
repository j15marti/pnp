#!/usr/bin/env node
// Independent no-import replay for LSPV-5/407. Not the historical checker.
import fs from 'node:fs';
import crypto from 'node:crypto';

const path = 'results/raw/review/2026-11-07_0248_LSPV5_ADAPTIVE_AFFINE_RANK407.json';
const d = JSON.parse(fs.readFileSync(path, 'utf8'));
let checks = 0;
const ok = (x, m) => { checks++; if (!x) throw new Error(m); };
const pc = x => { let c=0; while(x){c+=x&1; x>>>=1;} return c; };
const parity = x => pc(x)&1;

function rank(vs){
  const b = new Map();
  for(let v of vs){
    while(v){ const p=31-Math.clz32(v); if(b.has(p)) v ^= b.get(p); else {b.set(p,v); break;} }
  }
  return b.size;
}

function build(n, code=null){
  const nodes=[], leaves=[];
  function rec(depth,prefix,path){
    if(depth===n){leaves.push({assignment:prefix,path:[...path]}); return;}
    let twist;
    if(code===null) twist=(((prefix*0x9E3779B1)>>>0)^(prefix>>>1))&((1<<depth)-1);
    else { const base=1<<depth; twist=code%base; code=Math.floor(code/base); }
    const mask=(1<<depth)^twist, id=nodes.length;
    nodes.push({id,depth,prefix,mask});
    for(const value of [0,1]){
      const bit=value^parity(twist&prefix);
      rec(depth+1,prefix|(bit<<depth),path.concat([{node:id,mask,value}]));
    }
  }
  rec(0,0,[]); return {nodes,leaves};
}

ok(d.run==='LSPV-5/407','run');
ok(d.historical_checker.startsWith('NOT RUN'),'checker scope');
for(const f of d.fixtures){
  const t=build(f.n);
  ok(t.nodes.length===f.internal_nodes,'internal nodes');
  ok(t.leaves.length===f.leaves,'leaves');
  ok(rank(t.nodes.map(x=>x.mask))===f.query_rank,'rank');
  ok(f.common_upper_q_plus_r===f.union_paid_q+f.query_rank,'q+r');
  ok(f.contradictory_basis_rows<=f.query_rank+1,'basis dimension');
  ok(f.final_joins===f.contradictory_basis_rows-1,'join count');
  const got=t.leaves.map(x=>x.assignment).sort((a,b)=>a-b);
  ok(got.every((x,i)=>x===i),'coverage');
  for(const leaf of t.leaves) for(const e of leaf.path)
    ok((parity(e.mask&leaf.assignment)^e.value)===0,'path assumption');
}

let policies=0, digest=crypto.createHash('sha256');
for(let code=0; code<1024; code++){
  const t=build(3,code);
  ok(rank(t.nodes.map(x=>x.mask))===3,'policy rank');
  const got=t.leaves.map(x=>x.assignment).sort((a,b)=>a-b);
  ok(got.every((x,i)=>x===i),'policy coverage');
  for(const leaf of t.leaves) for(const e of leaf.path)
    ok((parity(e.mask&leaf.assignment)^e.value)===0,'policy path');
  digest.update(t.nodes.map(nd=>`${nd.mask},${nd.prefix}`).join(';'));
  policies++;
}
ok(policies===d.exhaustive_adaptive_policies_n3.policies,'policy count');
ok(digest.digest('hex')===d.exhaustive_adaptive_policies_n3.digest,'policy digest');
for(const [k,v] of Object.entries(d.negative_controls)) if(typeof v==='boolean') ok(v,`negative ${k}`);
ok(d.p_vs_np==='OPEN','status');
console.log(JSON.stringify({status:'PASS',checks,raw_sha256:crypto.createHash('sha256').update(fs.readFileSync(path)).digest('hex')}));
