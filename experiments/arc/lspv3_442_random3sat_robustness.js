#!/usr/bin/env node
'use strict';
// LSPV-3/442. Deterministic finite certificate, NOT a proof-hardness checker.
// Replay: node experiments/arc/lspv3_442_random3sat_robustness.js
const crypto=require('crypto');
function next(st){let x=st.x;x^=(x<<13);x^=(x>>>17);x^=(x<<5);st.x=x>>>0;return st.x;}
function sample(n,seed,planted=false){
 const st={x:seed>>>0},out=[];
 for(let i=0;i<8*n;i++){
  let ids=[];while(ids.length<3){let v=1+next(st)%n;if(!ids.includes(v))ids.push(v);}
  let c=ids.map(v=>(next(st)&1)?v:-v);
  if(planted&&c.every(v=>v>0))c[0]=-c[0];
  out.push(c);
 }return out;
}
function dimacs(n,cls){return 'p cnf '+n+' '+cls.length+'\n'+cls.map(c=>c.join(' ')+' 0\n').join('');}
function evaluate(n,cls){
 let lo=Infinity,num=0,who=-1,sat=0,h={};
 for(let a=0;a<2**n;a++){
  let bad=0;
  for(let c of cls){
   let falseClause=true;
   for(let lit of c){let bit=(a>> (Math.abs(lit)-1))&1;if((lit>0&&bit===1)||(lit<0&&bit===0)){falseClause=false;break;}}
   if(falseClause)bad++;
  }
  h[bad]=(h[bad]||0)+1;
  if(bad<lo){lo=bad;num=1;who=a}else if(bad===lo)num++;
  if(bad===0)sat++;
 }
 return {min_falsified:lo,min_count:num,min_assignment:who,sat_assignments:sat,histogram:h};
}
const cases=[[10,113,false],[12,36,false],[14,131,false],[16,131,false],[12,777,true]];
let records=[];
for(let [n,seed,planted] of cases){
 let cls=sample(n,seed,planted),src=dimacs(n,cls);
 if(cls.some(c=>c.length!==3||new Set(c.map(Math.abs)).size!==3))throw Error('invalid strict3');
 let r=evaluate(n,cls);
 if((r.sat_assignments>0)!==planted)throw Error('SAT control mismatch');
 records.push({n,seed,planted,source_sha256:crypto.createHash('sha256').update(src).digest('hex'),source_bytes:Buffer.byteLength(src),clauses:cls.length,...r, deletion_robust_k:Math.max(0,r.min_falsified-1)});
}
console.log(JSON.stringify({run:'LSPV3-442',source:'direct strict3 clauses, xorshift32 fixtures',proof_hardness_certified:false,records},null,2));
