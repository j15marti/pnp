#!/usr/bin/env node
'use strict';
/* LSPV-3 365: independent source grammar and charged-bound checker.
   The complete gate/Resolution DAG producer and independently written
   verifier for k=2,3,4 are in the attached reproducibility archive.
   This public compact runner does not claim to check those full DAGs. */
const assert=require('assert');
const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const inc=v=>E.map((x,i)=>x.includes(v)?i:-1).filter(i=>i>=0);
const norm=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||Number(x<0)-Number(y<0));
const tuples=(k,p)=>p===0?[[]]:tuples(k,p-1).flatMap(a=>Array.from({length:k},(_,j)=>[...a,j]));
function source(k,odd){
 const s=[odd?1:0,0,0,0],clauses=[],meta=[];
 for(let v=0;v<4;v++){
  const ee=inc(v);
  for(let a=0;a<8;a++){
   const b=[(a>>2)&1,(a>>1)&1,a&1];
   if((b[0]^b[1]^b[2])===s[v])continue;
   const z=b.map((bit,i)=>bit?-1:i).filter(i=>i>=0);
   for(const j of tuples(k,z.length)){
    let C=[];
    for(let i=0;i<3;i++){
     const e=ee[i];
     if(b[i])for(let t=0;t<k;t++)C.push(-(e*k+t+1));
     else C.push(e*k+j[z.indexOf(i)]+1);
    }
    clauses.push(norm(C));meta.push({v,b,j});
   }
  }
 }
 return {clauses,meta,charge:s};
}
const evalClause=(x,C)=>C.some(t=>(x[Math.abs(t)-1]===1)===(t>0));
function deletionControl(k,obj){
 let signs=0;
 for(let i=0;i<obj.clauses.length;i++){
  const {v,b,j}=obj.meta[i],ee=inc(v);
  let out;
  for(let t=0;t<64;t++){
   let y=Array.from({length:6},(_,e)=>(t>>e)&1);
   if(ee.some((e,n)=>y[e]!==b[n]))continue;
   if([0,1,2,3].some(w=>w!==v && inc(w).reduce((s,e)=>s^y[e],0)!==obj.charge[w]))continue;
   out=y;break;
  }
  assert(out);
  const z=Array(6*k).fill(1),zero=b.map((bit,i)=>bit?-1:i).filter(i=>i>=0);
  for(let e=0;e<6;e++)if(!out[e]){
   const loc=ee.indexOf(e);
   const t=loc<0?0:j[zero.indexOf(loc)];
   z[e*k+t]=0;
  }
  let wrong=0;
  obj.clauses.forEach((c,loc)=>{if(!evalClause(z,c)){wrong++;assert.strictEqual(loc,i)}});
  assert.strictEqual(wrong,1);
  for(let loc=0;loc<obj.clauses[i].length;loc++){
   const c=[...obj.clauses[i]];c[loc]*=-1;
   assert(evalClause(z,c));signs++;
  }
 }
 return signs;
}
function run(k){
 const odd=source(k,true),even=source(k,false);
 assert.strictEqual(odd.clauses.length,k**3+3*k+3*(3*k*k+1));
 assert.strictEqual(even.clauses.length,4*(3*k*k+1));
 assert(even.clauses.every(c=>evalClause(Array(6*k).fill(0),c)));
 const signChecks=deletionControl(k,odd);
 const defs=6*(k-1);
 const gateAndTemplates=6*(k*k+3*k-8)/2;
 const localOdd=k**3+7*k*k+4*k;
 const localEven=3*k**3+3*k*k+6*k;
 const local=localOdd+3*localEven;
 // K4 parity rows admit 31 extra pure-Resolution nodes.
 const q=gateAndTemplates+local+31;
 const expected={2:[53,225,216],3:[120,541,576],4:[223,1075,1200]}[k];
 assert.deepStrictEqual([odd.clauses.length,q,signChecks],expected);
 return {k,source_clauses:odd.clauses.length,even_clauses:even.clauses.length,
   paid_gates:defs,derived_resolution_nodes:q-defs,logical_upper:q,
   source_floor:odd.clauses.length-1,source_deletion_checks:odd.clauses.length,
   source_sign_repair_checks:signChecks};
}
const cases=[2,3,4].map(run);
console.log(JSON.stringify({id:'LSPV3-365',status:'PUBLIC_COMPACT_SOURCE_AND_COUNT_CHECK',
note:'Full independently checked signed gate/RES proof DAGs in local archive',
cases},null,2));
