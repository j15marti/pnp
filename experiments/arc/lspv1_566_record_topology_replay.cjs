'use strict';
// LSPV-1/566: original archived /386 checkProof topological permutation test.
// Run: node experiments/arc/lspv1_566_record_topology_replay.cjs [out.json]
// This is NOT the missing full historical five-rule R_mix341 checker.
const fs=require('fs'),path=require('path'),crypto=require('crypto'),assert=require('assert');
const root=path.resolve(__dirname,'../..');
const vf='experiments/arc/lspv2_386_independent_verify.js';
const pf='results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json';
const source=fs.readFileSync(path.join(root,vf)),raw=fs.readFileSync(path.join(root,pf));
const check=new Function('require','process','console',
  source.toString('utf8')+'\nreturn {proof:checkProof,count:()=>tests};')(
    require,{argv:['node','archived-checker']},console);
const orig=JSON.parse(raw.toString('utf8')),cp=x=>JSON.parse(JSON.stringify(x));
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function permutation(d,ord){
  assert.strictEqual(new Set(ord).size,d.records.length);
  const pos=new Map(ord.map((old,i)=>[old,i]));
  const z=cp(d);
  z.records=ord.map(i=>({...cp(d.records[i]),parents:d.records[i].parents.map(j=>{
    assert(pos.has(j));return pos.get(j);
  })}));
  return z;
}
function normal(d){
  const i=d.records.map((_,k)=>k);
  return permutation(d,['SOURCE','DEF','RES'].flatMap(t=>i.filter(j=>d.records[j].kind===t)));
}
function topological(d,seed){
  let n=seed>>>0;const rnd=()=>((n=Math.imul(n,1664525)+1013904223>>>0));
  const seen=new Set(),order=[],last=d.records.length-1;
  for(let j=0;j<d.records.length;j++){
    const ready=d.records.map((r,i)=>i).filter(i=>
      !seen.has(i)&&(i!==last||j===last)&&d.records[i].parents.every(p=>seen.has(p)));
    assert(ready.length);
    const id=ready[rnd()%ready.length];seen.add(id);order.push(id);
  }
  return permutation(d,order);
}
function reject(d,f){
  let x=cp(d);f(x);
  try{check.proof(x,{control:true});return false;}catch(_e){return true;}
}
const before=check.count(),base=check.proof(orig,{control:true});
assert.deepStrictEqual([base.paid,base.sources,base.records],[53,17,74]);
const canon=normal(orig);
assert.deepStrictEqual(check.proof(canon,{control:true}),base);
assert(same(canon,normal(canon)));
const ids=orig.records.map((r,i)=>r.kind==='SOURCE'?i:-1).filter(i=>i>=0);
const ds=orig.records.map((r,i)=>r.kind==='DEF'?i:-1).filter(i=>i>=0);
const rs=orig.records.map((r,i)=>r.kind==='RES'?i:-1).filter(i=>i>=0);
const facetFirst=permutation(orig,[...ds,...ids,...rs]);
assert.deepStrictEqual(check.proof(facetFirst,{control:true}),base);
let accepted=0,changed=0,paidBeforeLastSource=0,firstIsFacet=0;const examples=[];
for(let seed=1;seed<=128;seed++){
  let q=topological(orig,seed);
  assert.deepStrictEqual(check.proof(q,{control:true}),base);
  accepted++;
  if(!same(q.records,orig.records))changed++;
  const firstRes=q.records.findIndex(r=>r.kind==='RES');
  const lastSource=q.records.map(r=>r.kind).lastIndexOf('SOURCE');
  if(firstRes<lastSource)paidBeforeLastSource++;
  if(q.records[0].kind==='DEF')firstIsFacet++;
  assert(same(normal(normal(q)),normal(q)));
  if(seed<=3)examples.push({seed,firstRes,lastSource,firstTen:q.records.slice(0,10).map(r=>r.kind)});
}
const hostile={
  forwardParent:reject(canon,q=>{let i=q.records.findIndex(r=>r.kind==='RES');q.records[i].parents[0]=i;}),
  invalidFacet:reject(canon,q=>{q.records.find(r=>r.kind==='DEF').c=[999];}),
  missingOwner:reject(canon,q=>{q.gate_defs.pop();}),
  underpayment:reject(canon,q=>{q.summary.paid_total--;}),
  forgedSource:reject(canon,q=>{q.records.find(r=>r.kind==='SOURCE').source=99999;}),
  mismatchedCharge:reject(canon,q=>{q.spec.charge=[0,1,0,0];})
};
assert(Object.values(hostile).every(Boolean));
const out={
  status:'PROVED/RESTRICTED + COMPUTATIONAL',
  model:'unchanged original archived /386 checkProof({control:true}); NOT full /341 or full CLI harness',
  checker:{path:vf,sha256:sha(source)},certificate:{path:pf,sha256:sha(raw)},
  base,acceptedTopologicalOrders:accepted,changedOrders:changed,
  paidBeforeLastSource,firstIsFacet,facetFirstControlAccepted:true,normalIdempotent:true,
  hostile,examples,originalCheckerAssertions:check.count()-before,
  limitations:['No complete historical R_mix341 dispatcher.',
    'Original /386 CLI automatic corruption-test loop not run as OS subprocess.',
    'Only logical work, not physical time/space or minimum proof complexity.']
};
const json=JSON.stringify(out,null,2)+'\n';
if(process.argv[2])fs.writeFileSync(process.argv[2],json);
process.stdout.write(json);
