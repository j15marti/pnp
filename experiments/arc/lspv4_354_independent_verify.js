#!/usr/bin/env node
// Independent no-Python-import referee for LSPV4_EVIDENCE_ENCODING354.
// Usage: node lspv4_354_independent_verify.js /path/to/raw.json
'use strict';
const fs = require('fs');
let checks=0;
const ok=(x,msg)=>{checks++;if(!x)throw Error('FAIL '+msg)};
function evalClause(c,a){return c.some(l=>Boolean(a&(1<<(Math.abs(l)-1)))===(l>0));}
function models(c,n){const out=[];for(let a=0;a<(1<<n);a++){if(c.every(x=>evalClause(x,a)))out.push(a)}return out;}
function canon(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);}
function resolve(a,b,p){if(!a.includes(p)||!b.includes(-p)) throw Error('pivot');return canon([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);}
function sourceHorn(){return [[1],[-1,2],[-2]];}
function k4(charges){const edgeSets=[[1,2,3],[1,4,5],[2,4,6],[3,5,6]];let F=[];
 for(let v=0;v<4;v++) for(let a=0;a<8;a++){
   if(((a&1)+((a>>1)&1)+((a>>2)&1))%2===charges[v])continue;
   F.push(edgeSets[v].map((x,j)=>a&(1<<j)?-x:x));
 }return F;
}
function enumerateIndependent(F,n){
  ok(models(F,n).length===0,'UNSAT');
  for(let i=0;i<F.length;i++)ok(models(F.filter((_,j)=>j!==i),n).length>0,'deletion witness '+i);
  for(let i=0;i<F.length;i++)for(let j=0;j<F[i].length;j++){
    const flipped=F.map(a=>a.slice());flipped[i][j]=-flipped[i][j];
    ok(models(flipped,n).length>0,'single sign flip witness');
  }
}
function verifyHorn(){
 let F=sourceHorn();enumerateIndependent(F,2);
 const D=resolve(F[0],F[1],1);ok(JSON.stringify(D)==='[2]','first Horn line');
 const E=resolve(D,F[2],2);ok(E.length===0,'second Horn line');
 let G=[[1],[-1,2],[2]];ok(models(G,2).length===1,'SAT witness');
 ok(!G[2].includes(-2),'SAT fake proof fails final pivot');
}
function verifyK4(){
 const odd=k4([1,0,0,0]);enumerateIndependent(odd,6);
 const even=k4([0,0,0,0]);ok(models(even,6).length===8,'even models');
 let eqRows=[];
 for(let v=0;v<4;v++){
   const scope=[...new Set(odd.slice(4*v,4*v+4).flat().map(Math.abs))].sort((a,b)=>a-b);
   ok(scope.length===3,'arity');let signatures=[];
   for(let a=0;a<8;a++){
    const global=scope.reduce((acc,x,j)=>acc|(((a>>j)&1)<<(x-1)),0);
    signatures.push(odd.slice(4*v,4*v+4).every(c=>evalClause(c,global)));
   }
   for(let i=0;i<8;i++)ok(signatures[i]===((i.toString(2).split('1').length-1)%2===(v===0?1:0)),'row truth table');
   eqRows.push({mask:scope.reduce((z,x)=>z^(1<<(x-1)),0),rhs:Number(v===0)});
 }
 let total=eqRows.reduce((a,b)=>({mask:a.mask^b.mask,rhs:a.rhs^b.rhs}),{mask:0,rhs:0});
 ok(total.mask===0&&total.rhs===1,'odd affine contradiction');
 const sameEven=[];for(let v=0;v<4;v++)sameEven.push({mask:eqRows[v].mask,rhs:0});
 total=sameEven.reduce((a,b)=>({mask:a.mask^b.mask,rhs:a.rhs^b.rhs}),{mask:0,rhs:0});
 ok(total.mask===0&&total.rhs===0,'even is no contradiction');
}
function verifyRaw(result){
 ok(result.samples.length===2,'sample count');
 const horn=result.samples.find(x=>x.case==='horn_unsat');
 const tseitin=result.samples.find(x=>x.case==='odd_tseitin_K4');
 ok(horn.m===3&&horn.inferences===2&&horn.input_bits===29,'horn ledger');
 ok(tseitin.m===16&&tseitin.inferences===15&&tseitin.input_bits===286,'parity ledger');
 for(const s of result.samples){
  const b=s.input_bits+s.inferences*(8*s.max_variables+4*(Math.floor(Math.log2(s.m+s.inferences+1))+1)+4*(Math.floor(Math.log2(s.max_variables+1))+1)+64);
  ok(b===s.evidence_bound_bits,'exact padding formula '+s.case);
  ok(s.evidence_bound_bits<=50*(s.input_bits+s.inferences+1)**2,'quadratic cap');
 }
 ok(result.controls.invalid_proofs_rejected===10&&result.controls.malformed_DIMACS_rejected===8,'negative corpus');
}
verifyHorn();verifyK4();verifyRaw(JSON.parse(fs.readFileSync(process.argv[2]||'raw.json')));
console.log(JSON.stringify({independent_assertions:checks,odd_K4:'UNSAT',even_K4_models:8,horn_SAT_neighbor_models:1,negative_controls:18,status:'PASS'},null,2));
