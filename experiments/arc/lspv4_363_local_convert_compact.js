#!/usr/bin/env node
// LSPV-4 LOCAL-CONVERT-CVP363. Node.js >=18. Standard library only.
// Run: node lspv4_363_local_convert_compact.js out.json
// This checks a fixed, source-authenticated LOCAL-CONVERT subrule.
// Under the explicitly conditional unbounded-output syntax U, the gate DAG
// is one output record, not independently paid DEF nodes.
'use strict';
const fs=require('fs');
const X=170, Y=204, tests={};
function ok(v,tag){ if(!v) throw Error('failed '+tag);tests[tag]=(tests[tag]||0)+1; }
function annotate(gs){
  const rows=[];
  for(let i=0;i<gs.length;i++){
    const g=gs[i];
    let v;
    if(g.op==='C')v=g.bit?255:0;
    else if(g.op==='X')v=X;
    else if(g.op==='Y')v=Y;
    else if(g.op==='N')v=255^rows[g.a];
    else if(g.op==='A')v=rows[g.a]&rows[g.b];
    else if(g.op==='O')v=rows[g.a]|rows[g.b];
    else throw Error('unknown gate');
    rows.push(v);
  }
  return rows;
}
function pack(cv,unsat){
  const gates=cv.map(g=>({...g})),t=gates.length-1;
  gates.push({op:'X'});const x=gates.length-1;
  gates.push({op:'A',a:t,b:x});
  return {sources:[[1],[1,2],...unsat?[[-1]]:[]],
          parents:[0,1],and_mask:X,gates,rows:annotate(gates)};
}
function check(p){
  if(!p||JSON.stringify(p.parents)!=='[0,1]'||p.and_mask!==X)return false;
  if(!['[[1],[1,2]]','[[1],[1,2],[-1]]'].includes(JSON.stringify(p.sources)))return false;
  if(!Array.isArray(p.gates)||!p.gates.length||!Array.isArray(p.rows)||p.rows.length!==p.gates.length)return false;
  for(let i=0;i<p.gates.length;i++){
    const g=p.gates[i],r=p.rows[i];
    if(!g||!Number.isInteger(r)||r<0||r>255)return false;
    const ks=Object.keys(g).sort().join(',');
    let v;
    if(g.op==='C'){
      if(ks!=='bit,op'||![0,1].includes(g.bit))return false;
      v=g.bit?255:0;
    }else if(g.op==='X'||g.op==='Y'){
      if(ks!=='op')return false;
      v=g.op==='X'?X:Y;
    }else if(g.op==='N'){
      if(ks!=='a,op'||!Number.isInteger(g.a)||g.a<0||g.a>=i)return false;
      v=255^p.rows[g.a];
    }else if(g.op==='A'||g.op==='O'){
      if(ks!=='a,b,op'||!Number.isInteger(g.a)||!Number.isInteger(g.b)||
         Math.min(g.a,g.b)<0||Math.max(g.a,g.b)>=i)return false;
      v=g.op==='A'?(p.rows[g.a]&p.rows[g.b]):(p.rows[g.a]|p.rows[g.b]);
    }else return false;
    if(v!==r)return false;
  }
  return (X&(255^p.rows[p.rows.length-1]))===0;
}
function chain(bits){
  const out=[];
  for(const bit of bits){
    out.push({op:'C',bit});
    if(out.length>1)out.push({op:'A',a:out.length-2,b:out.length-1});
  }
  return out;
}
let m=0,flips=0;
const samples=[];
for(const size of [1,2,3,5,8,16,32,64,128,256]){
  const all=Array(size).fill(1);
  for(const unsat of [false,true]){
    const good=pack(chain(all),unsat);
    ok(check(good),'authentic_chain');
    ok(good.sources.length===(unsat?3:2),'both_label_source');
    if(size===256)samples.push({size,unsat,gates:good.gates.length,
                               truth_annotation_bits:8*good.gates.length,
                               proof_nodes_under_U:2,
                               serialized_bytes:Buffer.byteLength(JSON.stringify(good))});
    m++;
    for(let i=0;i<size;i++){
      const wrong=all.slice();wrong[i]=0;
      ok(!check(pack(chain(wrong),unsat)),'flipped_constant');
      flips++;
    }
    let corrupt=structuredClone(good);
    corrupt.rows[corrupt.rows.length-1]^=1;
    ok(!check(corrupt),'forged_annotation');
    corrupt=structuredClone(good);corrupt.gates.at(-1).a=good.gates.length;
    ok(!check(corrupt),'forward_reference');
    corrupt=structuredClone(good);corrupt.parents=[0,2];
    ok(!check(corrupt),'untrusted_source');
  }
}
for(let b of [0,1]){
  const p=pack([{op:'C',bit:b}],false);
  ok(check(p)===(b===1),'cvp_value');
}
const result={id:'LSPV4_LOCAL_CONVERT_CVP363_COMPACT',status:'PASS',
  tested_chains:m,flipped_constant_neighbors:flips,
  counts:tests,examples:samples,
  reminder:'P-completeness applies to an unbounded-circuit output syntax U; does not prove L!=P or B3.',
  host_rss_kib:Math.round(process.memoryUsage().rss/1024)};
const path=process.argv[2]||'local_convert_compact363.json';
fs.writeFileSync(path,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({path,checks:tests,host_rss_kib:result.host_rss_kib},null,2));
