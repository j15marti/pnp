#!/usr/bin/env node
/* LSPV-3/529. Reproducible ordinary-Resolution projection of a signed mod-3 cubic path.
   Native R_mix341 checker acceptance is NOT established. No external packages. */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs');
const tuples=n=>{let o=[[]];for(let i=0;i<n;i++)o=o.flatMap(a=>[0,1,2].map(x=>[...a,x]));return o};
const norm=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
function run(k){
 let names=[],vs=[];
 for(let i=0;i<k;i++){
  let es=i? [`c${i-1}`,`a${i}`,`c${i}`]:['a0','b0','c0'];
  es.forEach(e=>{if(!names.includes(e))names.push(e)});
  vs.push({edges:es,signs:i?[-1,i%2?1:-1,1]:[1,-1,1],charge:(i*i+1)%3});
 }
 const L=(e,t)=>3*names.indexOf(e)+t+1, R=[],ids=new Map();
 function src(key,clause){let id=R.length+1;R.push({id,op:'SOURCE',key,clause:norm(clause)});ids.set(key,id);return id}
 names.forEach(e=>src(`ALO:${e}`,[0,1,2].map(t=>L(e,t))));
 vs.forEach((v,i)=>tuples(3).forEach(t=>{if((v.signs.reduce((s,a,j)=>s+a*t[j],0)-v.charge)%3)src(`V${i}:${t.join(',')}`,t.map((x,j)=>-L(v.edges[j],x)))}));
 let S=R.length,clauses=new Map(R.map(r=>[r.id,r.clause]));
 assert.equal(S,20*k+1);
 function res(p,q,piv){let a=clauses.get(p),b=clauses.get(q);assert(a.includes(piv)&&b.includes(-piv));let c=norm([...a.filter(x=>x!==piv),...b.filter(x=>x!==-piv)]);assert(!c.some(x=>c.includes(-x)));let id=R.length+1;R.push({id,op:'RES',parents:[p,q],pivot:piv,clause:c});clauses.set(id,c);return id}
 let boundary=['a0','b0','c0'],Q=new Map(),v=vs[0];
 tuples(3).forEach(t=>{if((v.signs.reduce((s,a,j)=>s+a*t[j],0)-v.charge)%3)Q.set(t.join(','),ids.get(`V0:${t.join(',')}`))});
 for(let i=1;i<k;i++){
  let old=boundary.slice(0,-1),shared=boundary.at(-1),B=new Map(),vv=vs[i],alo=ids.get(`ALO:${shared}`);
  for(let a of tuples(old.length)){
    let good=[0,1,2].filter(t=>!Q.has([...a,t].join(',')));assert.equal(good.length,1);
    let other=[0,1,2].filter(t=>t!==good[0]);
    let h=res(alo,Q.get([...a,other[0]].join(',')),L(shared,other[0]));
    h=res(h,Q.get([...a,other[1]].join(',')),L(shared,other[1]));
    for(let tail of tuples(2)){
      let ts=[good[0],...tail];if((vv.signs.reduce((s,x,j)=>s+x*ts[j],0)-vv.charge)%3===0)continue;
      let out=res(h,ids.get(`V${i}:${ts.join(',')}`),L(shared,good[0]));
      assert.deepEqual(clauses.get(out),norm([...a.map((x,j)=>-L(old[j],x)),...tail.map((x,j)=>-L(vv.edges[j+1],x))]));
      B.set([...a,...tail].join(','),out);
    }
  }
  Q=B;boundary=[...old,...vv.edges.slice(1)];
 }
 assert.equal(Q.size,2*3**(k+1));assert.equal(R.length-S,4*3**(k+1)-36);
 let charge=vs.reduce((x,v)=>x+v.charge,0),coeff=Object.fromEntries(names.map(e=>[e,0]));
 vs.forEach(v=>v.edges.forEach((e,j)=>coeff[e]+=v.signs[j]));
 let models=0;
 for(let vals of tuples(names.length))if(vs.every(v=>(v.edges.reduce((s,e,j)=>s+v.signs[j]*vals[names.indexOf(e)],0)-v.charge)%3===0))models++;
 assert.equal(models,3**(k+1));
 for(let t of tuples(boundary.length)){
  let valid=(t.reduce((s,x,j)=>s+x*coeff[boundary[j]],0)-charge)%3===0;
  assert.equal(Q.has(t.join(',')),!valid);
 }
 let root=[...Q.values()],dep=new Map();R.forEach(r=>dep.set(r.id,r.op==='SOURCE'?0:1+Math.max(...r.parents.map(p=>dep.get(p)))));
 let anc=new Set(root),pending=[...root];while(pending.length){let n=pending.pop(),r=R[n-1];if(r.op==='RES')for(let p of r.parents)if(!anc.has(p)){anc.add(p);pending.push(p)}}
 let live=[...anc].filter(n=>n<=S).length;assert.equal(live,19*k-1);
 return {k,source_clauses:S,live_sources:live,paid_res:R.length-S,proof_records:R.length,refs:2*(R.length-S),boundary_size:boundary.length,projected_clauses:Q.size,onehot_models:models,depth:Math.max(0,...root.map(x=>dep.get(x))),records:R,boundary,outputs:Object.fromEntries(Q)};
}
let summaries=[];for(let k=1;k<=5;k++){
 let x=run(k);let {records,boundary,outputs,...meta}=x;summaries.push(meta);
 if(process.argv.includes('--cert')&&[2,3,4].includes(k))fs.writeFileSync(`lspv3_529_k${k}.json`,JSON.stringify(x));
}
console.log(JSON.stringify({status:'PROVED/RESTRICTED + COMPUTATIONAL',result:summaries},null,2));
