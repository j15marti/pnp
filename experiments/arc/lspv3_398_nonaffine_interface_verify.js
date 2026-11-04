#!/usr/bin/env node
'use strict';
/* Independent enumeration of LSPV-3/398 nonaffine CNF backtranslation controls.
 * Numeric bitmasks and recursive ternary cubes, no Python imports. */
const assert=require('assert');
function parityIP(v,m){let p=0;for(let i=0;i<m;i++)p^=((v>>(2*i))&1)&((v>>(2*i+1))&1);return p;}
function witness(mask,m){let v=0;for(let j=0;j<m;j++)v|= (((mask>>j)&1) ? 1:2) << (2*j);return v;}
function legalCube(cube,assignment){for(let i=0;i<cube.length;i++){if(cube[i]!==-1 && cube[i]!== ((assignment>>i)&1))return false;}return true;}
function run(m){
 let checks=0;
 const zeros=[];
 for(let a=0;a<(1<<(2*m));a++){if(parityIP(a,m)===0) zeros.push(a);checks++;}
 const ws=Array.from({length:1<<m},(_,i)=>witness(i,m));
 for(const v of ws){assert.strictEqual(parityIP(v,m),0);checks++;}
 for(let i=0;i<ws.length;i++)for(let j=i+1;j<ws.length;j++){
   const u=ws[i],v=ws[j],d=Array.from({length:m},(_,k)=>k).find(k=>((u>>(2*k))&3)!==((v>>(2*k))&3));
   assert.notStrictEqual(d,undefined);let hybrid=u|(3<<(2*d));
   assert.strictEqual(parityIP(hybrid,m),1);
   assert.strictEqual(((~(u^v))&(u^hybrid)),0);checks+=3;
 }
 let cubes=0,valid=0,maxwit=0,maxdim=-1;
 function enumerate(cube){if(cube.length===2*m){
   cubes++; const covered=Array.from({length:1<<(2*m)},(_,i)=>i).filter(x=>legalCube(cube,x));
   if(covered.every(x=>parityIP(x,m)===0)){
      valid++;let c=ws.filter(w=>legalCube(cube,w)).length;maxwit=Math.max(maxwit,c);
      assert(c<=1);maxdim=Math.max(maxdim,cube.filter(x=>x===-1).length);checks++;
   }return;
 }for(const d of [-1,0,1])enumerate([...cube,d]);}
 enumerate([]);assert.strictEqual(cubes,3**(2*m));assert.strictEqual(maxdim,m);assert.strictEqual(maxwit,1);
 assert.strictEqual(zeros.length,(4**m+2**m)/2);
 return {m,zeros:zeros.length,pairChecks:ws.length*(ws.length-1)/2,validCubes:valid,allCubes:cubes,maxZeroCubeDim:maxdim,checks};
}
function gateCheck(kind){const rows=[];for(let a=0;a<=1;a++)for(let b=0;b<=1;b++)for(let t=0;t<=1;t++){
 let clauses=kind==='AND' ? [[-3,1],[-3,2],[3,-1,-2]]:[[-1,-2,-3],[1,2,-3],[1,-2,3],[-1,2,3]];
 let truth=(clauses.every(c=>c.some(l=>[0,a,b,t][Math.abs(l)]===(l>0?1:0))));
 let ok=t===(kind==='AND'?(a&b):(a^b)); assert.strictEqual(truth,ok);rows.push([a,b,t,truth]);
}return rows.length;}
function main(){let r=[1,2,3,4].map(run);let gates=gateCheck('AND')+gateCheck('XOR');
const raw=JSON.parse(require('fs').readFileSync(process.argv[2],'utf8'));
assert.strictEqual(gates,raw.gate_truth_rows_checked);
for(let i=0;i<r.length;i++){
  for(const [key,other] of [['zero_assignments','zeros'],['pairwise_hybrid_checks','pairChecks'],['implicate_zero_subcubes','validCubes'],['candidate_falsifying_subcubes','allCubes'],['max_zero_subcube_dimension','maxZeroCubeDim']]) assert.strictEqual(raw.cases[i][key],r[i][other]);
}
for(const mutator of [x=>{x.cases[2].zero_assignments++},x=>{x.cases[1].pairwise_hybrid_checks--},x=>{x.cases[0].implicate_zero_subcubes=0}]){
 let corrupted=structuredClone(raw);mutator(corrupted);
 assert(!r.every((v,i)=>corrupted.cases[i].zero_assignments===v.zeros&&corrupted.cases[i].pairwise_hybrid_checks===v.pairChecks&&corrupted.cases[i].implicate_zero_subcubes===v.validCubes));
}
console.log(JSON.stringify({status:'PASS',independentChecks:r.reduce((s,v)=>s+v.checks,0)+gates+3,gateRows:gates,corruptedLedgersRejected:3,cases:r},null,2));}
main();
