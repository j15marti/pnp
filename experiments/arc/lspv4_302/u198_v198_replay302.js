#!/usr/bin/env node
"use strict";
// Independent source-based U198 UNSAT, V198 SAT and Y6 SAT replay.
// Requires repo fixture and original independently archived witness, no packages.
// Different DPLL branch order from archived Python verifier. Work measured.
const fs=require("fs"),path=require("path"),assert=require("assert");
const root=path.resolve(__dirname,"../../..");
const src=fs.readFileSync(path.join(root,"research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt"),"utf8");
const U=JSON.parse(src.slice(src.indexOf("[[")));
const witnessFile=fs.readFileSync(path.join(root,"experiments/arc/lspv1_286/verify_three_core286.py"),"utf8");
const m=witnessFile.match(/S='([01]+)'/);
assert(m && m[1].length===198);
const S=m[1];
function grammar(F,n){
  assert(F.length*3===4*n && n%3===0);
  const counts=Array.from({length:n+1},()=>[0,0]),keys=new Set();
  for(const c of F){
    assert(c.length===3 && new Set(c.map(Math.abs)).size===3);
    assert(c.every(x=>Math.sign(x)===Math.sign(c[0])));
    assert(c.every(x=>Math.abs(x)>0 && Math.abs(x)<=n));
    const key=c.slice().sort((a,b)=>a-b).join(",");
    assert(!keys.has(key));keys.add(key);
    for(const x of c)counts[Math.abs(x)][+(x>0)]++;
  }
  for(let v=1;v<=n;v++)assert(counts[v][0]===2&&counts[v][1]===2);
}
function dpllReduce(cs,lit){
  return cs.filter(c=>!c.includes(lit)).map(c=>c.filter(x=>x!==-lit));
}
let nodes=0;
function dpll(cs){
  nodes++;
  while(true){
    if(!cs.length)return true;
    if(cs.some(c=>c.length===0))return false;
    const unit=cs.find(c=>c.length===1);
    if(!unit)break;
    cs=dpllReduce(cs,unit[0]);
  }
  const v=cs[0][0];
  return dpll(dpllReduce(cs,v))||dpll(dpllReduce(cs,-v));
}
function main(){
 grammar(U,198);
 const V=U.map(c=>c.slice());
 [V[2][2],V[44][2]]=[V[44][2],V[2][2]];
 grammar(V,198);
 assert(V.every(c=>c.some(x=>S[Math.abs(x)-1]===String(+(x>0)))));
 const modules=[];
 for(let i=0;i<6;i++){
   const lo=1+32*i,hi=32+32*i;
   const part=U.slice(2,254).filter(c=>c.some(x=>Math.abs(x)>=lo&&Math.abs(x)<=hi));
   assert(part.length===42);
   assert(part.every(c=>c.every(x=>Math.abs(x)>=193||(Math.abs(x)>=lo&&Math.abs(x)<=hi))));
   modules.push(part);
 }
 let direct=0,calls=0,refuted=0;
 for(let b=0;b<64;b++){
   const pins={};
   for(let k=0;k<6;k++)pins[193+k]=(b>>k)&1;
   const directlyFalse=U.slice(0,2).some(c=>c.every(x=>pins[Math.abs(x)]!==+(x>0)));
   if(directlyFalse){direct++;continue;}
   let covered=false;
   for(const M of modules){
     calls++;
     const child=M.filter(c=>!c.some(x=>Math.abs(x)>=193&&pins[Math.abs(x)]===+(x>0)))
       .map(c=>c.filter(x=>Math.abs(x)<193));
     if(!dpll(child)){covered=true;break;}
   }
   assert(covered,"U198 uncovered boundary "+b);
   refuted++;
 }
 const Y=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],
          [-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]];
 grammar(Y,6);
 let yModels=0;
 for(let a=0;a<64;a++)
  if(Y.every(c=>c.some(x=> ((a>>(Math.abs(x)-1))&1)===+(x>0))))yModels++;
 assert(yModels===20);
 assert(direct===16&&refuted===48&&calls===152);
 return {status:"PASS",U198:{source_valid:true,variables:198,clauses:264,
  boundary_total:64,directly_refuted:direct,modules_refuted:refuted,module_dpll_calls:calls,
  dpll_nodes:nodes},
  V198:{source_valid:true,witness_bits:198,witness_clause_checks:264,
    swapped_clause_records:[2,44],source_label:"SAT"},
  Y6:{source_valid:true,models:yModels},method:"fresh independently implemented sequential UP-DPLL, original source and public witness; search nodes are implementation-dependent",
  P_versus_NP:"OPEN"};
}
console.log(JSON.stringify(main(),null,2));
