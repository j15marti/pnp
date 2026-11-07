#!/usr/bin/env node
// Independent no-import replay for LSPV-5/408. Not the historical checker.
import fs from 'node:fs';
import crypto from 'node:crypto';

const path = 'results/raw/review/2026-11-07_0356_LSPV5_AFFINE_COVER408.json';
const bytes = fs.readFileSync(path);
const d = JSON.parse(bytes);
let checks = 0;
const ok = (x,m) => { checks++; if(!x) throw new Error(m); };
const pc = x => { let c=0; while(x){c+=x&1; x>>>=1;} return c; };
const ev = (v,x,n) => (pc((v&((1<<n)-1))&x)&1)^((v>>n)&1);

function rank(rows){
  const b=new Map();
  for(let v0 of rows){ let v=v0; while(v){ const p=31-Math.clz32(v); if(b.has(p)) v^=b.get(p); else {b.set(p,v); break;} } }
  return b.size;
}

function witness(rows,n){
  const b=new Map();
  rows.forEach((v0,i)=>{ let v=v0,c=1<<i; while(v){ const p=31-Math.clz32(v); if(b.has(p)){const [w,d]=b.get(p);v^=w;c^=d;} else {b.set(p,[v,c]);break;} } });
  let t=1<<n,c=0;
  while(t){ const p=31-Math.clz32(t); if(!b.has(p)) return null; const [w,d]=b.get(p);t^=w;c^=d; }
  return rows.map((_,i)=>i).filter(i=>(c>>i)&1);
}

function enumerate(n){
  const assumptions=[];
  for(let mask=1;mask<(1<<n);mask++) for(const c of [0,1]) assumptions.push(mask|(c<<n));
  const us=assumptions.map(g=>g^(1<<n));
  const cells=assumptions.map(g=>{let z=0;for(let x=0;x<(1<<n);x++)if(ev(g,x,n)===0)z|=1<<x;return z;});
  const full=(1<<(1<<n))-1;
  let covers=0,overlaps=0,maxw=0;
  const digest=crypto.createHash('sha256');
  for(let chosen=0;chosen<(1<<assumptions.length);chosen++){
    let covered=0,members=0; const rows=[];
    for(let i=0;i<cells.length;i++) if((chosen>>i)&1){covered|=cells[i];members+=pc(cells[i]);rows.push(us[i]);}
    if(covered!==full) continue;
    covers++; if(members>(1<<n)) overlaps++;
    const w=witness(rows,n); ok(w!==null,'cover must span one'); ok(w.length<=n+1,'rank+1 basis');
    let acc=0; for(const i of w) acc^=rows[i]; ok(acc===(1<<n),'witness xor');
    maxw=Math.max(maxw,w.length); digest.update(`${chosen}:${w.join(',')};`);
  }
  return {variables:n,hyperplanes:assumptions.length,subsets:1<<assumptions.length,covers,overlapping_covers:overlaps,maximum_contradictory_basis_rows:maxw,bound:n+1,digest:digest.digest('hex')};
}

ok(d.run==='LSPV-5/408','run');
ok(d.historical_checker.startsWith('NOT RUN'),'checker scope');
for(let n=1;n<=3;n++){
  const got=enumerate(n), expected=d.exhaustive_affine_covers[n-1];
  for(const [key,value] of Object.entries(got))
    ok(value===expected[key],`enumeration n=${n} ${key}`);
}

const f=d.overlap_fixture, n=f.variables, byId=new Map();
for(const node of f.nodes){
  ok(!byId.has(node.id),'duplicate id');
  if(node.kind==='xor'){
    ok(node.parents.length===2,'binary parent count');
    const [p,q]=node.parents.map(x=>byId.get(x)); ok(p&&q,'acyclic predecessors');
    ok(node.row===(p.row^q.row),'xor row');
    const sym=[...new Set([...p.tag,...q.tag])].filter(x=>!(p.tag.includes(x)&&q.tag.includes(x))).sort();
    ok(JSON.stringify(sym)===JSON.stringify([...node.tag].sort()),'immutable tag');
  }
  byId.set(node.id,node);
}
ok(f.union_paid_q===f.nodes.filter(x=>x.kind==='xor').length,'q distinct nodes');
ok(f.global_query_rank_r===rank(Object.values(f.assumptions).map(v=>v&3)),'query rank');
ok(f.common_upper_q_plus_r===f.union_paid_q+f.global_query_rank_r,'q+r');
for(const [leaf,id] of Object.entries(f.terminals)){
  const t=byId.get(id); ok(t.row===(1<<n),'terminal false');
  ok(t.tag.every(x=>f.contexts[leaf].includes(x)),'scope containment');
  let u=t.row; for(const a of t.tag) u^=f.assumptions[a];
  ok(u===f.discharged_rows[leaf],'discharge');
}
for(let x=0;x<(1<<n);x++){
  const active=Object.keys(f.contexts).filter(l=>f.contexts[l].every(a=>ev(f.assumptions[a],x,n)===0));
  ok(active.length>0,'AND cover');
  ok(active.some(l=>ev(f.discharged_rows[l],x,n)===1),'U active');
}
for(const [k,v] of Object.entries(d.negative_controls)) if(typeof v==='boolean') ok(v,`negative ${k}`);
ok(d.p_vs_np==='OPEN','status');
console.log(JSON.stringify({status:'PASS',checks,raw_sha256:crypto.createHash('sha256').update(bytes).digest('hex')}));
