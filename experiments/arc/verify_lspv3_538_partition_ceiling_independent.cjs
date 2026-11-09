#!/usr/bin/env node
// LSPV-3/538 independent verifier; supply FULL Python-generated JSON as argument.
// Does NOT implement historical R_mix341; verifies source and abstract path claims.
const fs=require('fs');let checks=0;
const yes=(a,m)=>{checks++;if(!a)throw Error('FAIL '+m)};
const sat=(cnf,a)=>cnf.every(row=>row.some(l=>a[Math.abs(l)-1]===(l>0)));
function build(n){
 const v=(i,j)=>i*n+j+1,cnf=[];
 for(let i=0;i<n+1;i++)cnf.push(Array.from({length:n},(_,j)=>v(i,j)));
 for(let j=0;j<n;j++)for(let i=0;i<n+1;i++)for(let k=i+1;k<n+1;k++)cnf.push([-v(i,j),-v(k,j)]);
 return cnf;
}
function run(){
 const path=process.argv[2]||'lspv3_538_partition_ceiling_raw.json',r=JSON.parse(fs.readFileSync(path,'utf8'));
 yes(r.instances.length===2,'two examples');
 for(const ex of r.instances){
  const n=ex.n_holes,C=build(n),m=C.length;
  yes(JSON.stringify(C)===JSON.stringify(ex.source_clauses),'rebuild source');
  yes(ex.abstract_paid_merges===m-1,'budget');
  const a0=C[0],b0=C[1];
  yes(!a0.some(l=>b0.includes(-l)),'first pair illegal RES');
  yes(new Set([...a0,...b0].map(Math.abs)).size>3,'not legal AND3');
  let models=0;
  for(let a=0;a<(1<<(n*(n+1)));a++){
   const assignment=Array.from({length:n*(n+1)},(_,k)=>Boolean((a>>k)&1));
   if(sat(C,assignment))models++;
  }
  yes(models===0 && ex.source_models===0,'UNSAT');
  for(let dropped=0;dropped<m;dropped++){
   const witness=ex.exact_deletion_witnesses[dropped].map(Boolean);
   yes(!sat(C,witness),'source falsified');
   yes(sat(C.filter((_,idx)=>idx!==dropped),witness),'deletion satisfiable');
  }
  let comps=Array.from({length:m},(_,i)=>[i]);
  for(const step of ex.abstract_merges){
   yes(JSON.stringify(comps[0])===JSON.stringify(step.left),'left block');
   yes(JSON.stringify(comps[1])===JSON.stringify(step.right),'right block');
   comps=[step.union,...comps.slice(2)];
  }
  yes(comps.length===1 && comps[0].length===m,'partition goal');
  const bad=C.map(x=>x.slice());bad[0][0]=-bad[0][0];
  yes(JSON.stringify(bad)!==JSON.stringify(ex.source_clauses),'corrupt source rejected');
  const changed=ex.abstract_merges.map(x=>({...x}));changed[0]={...changed[0],cost:0};
  yes(changed.reduce((s,x)=>s+x.cost,0)!==m-1,'corrupt cost rejected');
  const w=ex.exact_deletion_witnesses[0].slice();w.fill(0);
  yes(!sat(C.filter((_,i)=>i!==0),w.map(Boolean)),'corrupt witness rejected');
 }
 return {status:'PASS',checks,instances:r.instances.map(x=>({n:x.n_holes,clauses:x.clauses,budget:x.abstract_paid_merges}))};
}
console.log(JSON.stringify(run()));
