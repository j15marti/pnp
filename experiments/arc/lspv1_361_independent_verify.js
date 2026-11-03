#!/usr/bin/env node
// Independent source-authenticated signed-CNF/RES verifier for LSPV-1 361.
// Run: python experiments/arc/lspv1_361_reflection_toy.py > proof361.json
//      node experiments/arc/lspv1_361_independent_verify.js proof361.json
'use strict';
const fs=require('fs'), crypto=require('crypto');
const raw=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
let checks=0;
function ok(x,msg){checks++;if(!x)throw Error(msg||'assertion failed');}
function parse(text){
  const lines=text.trimEnd().split('\n');
  ok(lines.shift()==='p cnf 3 4','bad DIMACS header');
  ok(lines.length===4,'wrong clause count');
  return lines.map(line=>{
    const xs=line.trim().split(/\s+/).map(Number);
    ok(xs[xs.length-1]===0&&xs.slice(0,-1).every(x=>Number.isInteger(x)&&x!==0&&Math.abs(x)<=3),'bad DIMACS clause');
    return xs.slice(0,-1);
  });
}
const source=parse(raw.source_dimacs);
ok(JSON.stringify(source)===JSON.stringify(raw.source),'source mismatch');
ok(crypto.createHash('sha256').update(raw.source_dimacs).digest('hex')===raw.source_sha256,'SHA mismatch');
function sat(cs,a){return cs.every(c=>c.some(x=>a[Math.abs(x)]===(x>0)));}
function model(cs){
  for(let m=0;m<8;m++){
    const a={1:!!(m&1),2:!!(m&2),3:!!(m&4)};
    if(sat(cs,a))return a;
  }
  return null;
}
ok(model(source)===null,'universal H is SAT');
function sorted(c){return c.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);}
function resolution(a,b,p){
  const aa=new Set(a),bb=new Set(b),plus=aa.has(p)&&bb.has(-p),minus=aa.has(-p)&&bb.has(p);
  if(!plus&&!minus)throw Error('invalid signed pivot');
  const out=new Set([...aa,...bb]);out.delete(p);out.delete(-p);
  for(const x of out)if(out.has(-x))throw Error('tautological resolvent');
  return sorted([...out]);
}
function replay(proof){
  const rows=source.map(x=>x.slice());
  for(const step of proof){
    const [u,v]=step.parents;
    if(!Number.isInteger(u)||!Number.isInteger(v)||u<0||v<0||u>=rows.length||v>=rows.length)throw Error('bad parent');
    const got=resolution(rows[u],rows[v],step.pivot);
    if(JSON.stringify(got)!==JSON.stringify(sorted(step.clause)))throw Error('corrupt conclusion');
    rows.push(got);checks++;
  }
  return rows[rows.length-1].length===0;
}
ok(replay(raw.proof),'no contradiction');
ok(raw.paid_nodes===3&&source.length===4,'incorrect node count');
for(const row of raw.delete_witnesses){
  const cs=source.filter((_,i)=>i!==row.clause_index);
  const a=Object.fromEntries(Object.entries(row.witness).map(([k,v])=>[k,!!v]));
  ok(sat(cs,a),'bad clause deletion repair');ok(!sat(source,a),'not an essential clause');
}
for(const row of raw.flip_witnesses){
  const cs=source.map((c,i)=>c.map((x,j)=>i===row.clause_index&&j===row.literal_index?-x:x));
  const a=Object.fromEntries(Object.entries(row.witness).map(([k,v])=>[k,!!v]));
  ok(sat(cs,a),'bad signed repair');ok(!sat(source,a),'source label wrong');
}
function label(s){return typeof s==='string'&&/^[01]{2}$/.test(s)?(s==='11'?'UNSAT':'SAT'):'MALFORMED';}
for(const row of raw.input_labels){
  ok(label(row.code)===row.label,'parser/label mismatch');
  if(row.label!=='MALFORMED'){
    const f=[];if(row.code[0]==='1')f.push([3]);if(row.code[1]==='1')f.push([-3]);
    ok((model(f)===null?'UNSAT':'SAT')===row.label,'wrong original SAT status');
  }
}
for(const bad of [
  [{parents:[0,3],pivot:1,clause:[3]},...raw.proof.slice(1)],
  [...raw.proof.slice(0,2),{parents:[4,5],pivot:2,clause:[]}],
  [...raw.proof.slice(0,2),{parents:[4,5],pivot:3,clause:[3]}]
]){
  let failed=false;try{replay(bad);}catch(e){failed=true;}ok(failed,'corrupted proof accepted');
}
for(const bad of [
  'p cnf 3 3\n1 0\n2 0\n-1 3 0\n-2 -3 0\n',
  'p cnf 3 4\n1 0\n2 0\n-1 3 0\n-2 -4 0\n'
]){
  let failed=false;try{parse(bad);}catch(e){failed=true;}ok(failed,'malformed DIMACS accepted');
}
console.log(JSON.stringify({status:'PASS',checks,source_sha256:raw.source_sha256,paid_nodes:raw.paid_nodes,unsat:true}));
