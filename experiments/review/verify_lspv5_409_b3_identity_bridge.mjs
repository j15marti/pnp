#!/usr/bin/env node
// Independent no-import replay for LSPV-5/409. Not historical R_mix341.
import fs from 'node:fs';
import crypto from 'node:crypto';

const path='results/raw/review/2026-11-07_0455_LSPV5_B3_IDENTITY409.json';
const bytes=fs.readFileSync(path), d=JSON.parse(bytes);
let checks=0;
const ok=(x,m)=>{checks++;if(!x)throw new Error(m);};
const graphs={
  K4:[4,Array.from({length:4},(_,i)=>i).flatMap(i=>Array.from({length:4-i-1},(_,k)=>[i,i+k+1]))],
  'K3,3':[6,Array.from({length:3},(_,i)=>i).flatMap(i=>Array.from({length:3},(_,k)=>[i,k+3]))],
  cube:[8,Array.from({length:8},(_,v)=>[1,2,4].map(b=>[v,v^b]).filter(e=>e[0]<e[1])).flat()]
};

function tseitin(nv,edges,odd){
  const inc=Array.from({length:nv},()=>[]);
  edges.forEach(([u,v],i)=>{inc[u].push(i+1);inc[v].push(i+1);});
  ok(inc.every(x=>x.length===3),'cubic');
  const cs=[];
  inc.forEach((es,v)=>{const charge=odd&&v===0?1:0;for(let a=0;a<8;a++){
    const pc=(a.toString(2).match(/1/g)||[]).length;
    if((pc&1)===charge)continue;
    cs.push(es.map((e,i)=>((a>>i)&1)?-e:e));
  }});
  return cs;
}
function encode(cs){
  const n=Math.max(...cs.flat().map(Math.abs));
  return `p cnf ${n} ${cs.length}\n`+cs.map(c=>`${c.join(' ')} 0\n`).join('');
}
function models(source){
  const ls=source.trimEnd().split('\n'), h=ls[0].split(' '), n=+h[2], m=+h[3];
  if(h[0]!=='p'||h[1]!=='cnf'||ls.length-1!==m)return null;
  const cs=ls.slice(1).map(l=>l.split(' ').map(Number).slice(0,-1)); let count=0;
  for(let a=0;a<(1<<n);a++) if(cs.every(c=>c.some(l=>(((a>>(Math.abs(l)-1))&1)===+(l>0)))))count++;
  return count;
}

ok(d.run==='LSPV-5/409','run');
ok(d.historical_checker.startsWith('NOT RUN'),'scope');
let idx=0;
for(const [name,[nv,edges]] of Object.entries(graphs)) for(const odd of [false,true]){
  const row=d.established_tseitin_controls[idx++], cs=tseitin(nv,edges,odd), source=encode(cs);
  const digest=crypto.createHash('sha256').update(source).digest('hex');
  ok(row.graph===name,'graph'); ok(row.charge===(odd?'odd':'even'),'charge');
  ok(row.clauses===4*nv,'clauses'); ok(row.variables===edges.length,'variables');
  ok(row.models===models(source),'models'); ok(row.source_sha256===digest,'digest');
  ok(row.encoded_bits_N===Buffer.byteLength(source)*8,'N');
  ok(row.Q_A_identity_proof_bits===row.encoded_bits_N,'identity proof');
  ok(row.Q_A_accepts===odd,'Q acceptance'); ok(row.reject_all_trace_accepts,'trace local');
}
ok(idx===6,'source count');
for(const row of d.inherited_clock_controls){
  ok(row.Q_A_identity_bits===row.encoded_bits_N,'Q padded identity');
  ok(row.R_clock_log2_lower===row.encoded_bits_N,'clock exponent');
  const expected=(1n<<BigInt(row.encoded_bits_N))+BigInt(row.declared_mixed_fast_upper)+1n;
  ok(expected.toString()===row.R_clock_exact_paid_nodes_decimal,'clock exact');
  for(const v of Object.values(row.log2_margin_over_Nplus1_to_k))ok(v>0,'finite clock margin');
}
for(const [k,v] of Object.entries(d.negative_controls))if(typeof v==='boolean')ok(v,`negative ${k}`);
ok(d.symbolic_claims.exact_boundary.includes('equivalent'),'boundary statement');
ok(d.p_vs_np==='OPEN','status');
console.log(JSON.stringify({status:'PASS',checks,raw_sha256:crypto.createHash('sha256').update(bytes).digest('hex')}));
