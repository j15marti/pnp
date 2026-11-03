#!/usr/bin/env node
// LSPV-2 368 compact public regeneration of source counts and exact restriction.
// Scope: this file is NOT the complete paid-node certificate checker.
// The full independent verifier and producer are in the reproducibility archive.
"use strict";
const crypto=require("crypto");
const assert=(x,m)=>{if(!x)throw Error(m)};
function canonical(C){let s=[...new Set(C)].sort((a,b)=>Math.abs(a)-Math.abs(b)||(a<0)-(b<0));assert(!s.some(v=>s.includes(-v)),"tautology");return s}
function parityCNF(rows){let F=[];for(let [vs,rhs] of rows){assert(vs.length===3 && new Set(vs).size===3,"proper row");for(let a=0;a<8;a++){let bits=[(a>>2)&1,(a>>1)&1,a&1];if((bits[0]^bits[1]^bits[2])===rhs)continue;F.push(canonical(vs.map((v,i)=>bits[i]?-v:v)))}}return F}
function models(n,F){let q=0;for(let a=0;a<(1<<n);a++)if(F.every(C=>C.some(v=>Boolean(a&(1<<(Math.abs(v)-1)))===(v>0))))q++;return q}
function build(n,F){
 let m=F.length,K=3*m, vals=Array.from({length:n},(_,i)=>[i+1,-i-1]).flat();
 let vix=new Map(vals.map((v,i)=>[v,i])), xend=n+K*(2*n), vcount=xend+K-1;
 let x=(j,t,l)=>n+1+(3*j+t)*(2*n)+vix.get(l), g=k=>xend+k;
 let S=[],add=C=>(S.push(canonical(C)),S.length-1);
 for(let j=0;j<m;j++){
   for(let t=0;t<3;t++){
     add(vals.map(l=>x(j,t,l)));
     for(let a=0;a<vals.length;a++)for(let b=a+1;b<vals.length;b++)
       add([-x(j,t,vals[a]),-x(j,t,vals[b])]);
   }
   for(let a of vals)for(let b of vals)for(let c of vals){
     if(new Set([Math.abs(a),Math.abs(b),Math.abs(c)]).size!==3)continue;
     add([-x(j,0,a),-x(j,1,b),-x(j,2,c),a,b,c])
   }
 }
 for(let k=1;k<K;k++){
   let left=k===1?x(0,0,F[0][0]):g(k-1);
   let right=k===1?x(0,1,F[0][1]):x(Math.floor(k/3),k%3,F[Math.floor(k/3)][k%3]);
   add([-g(k),left]);add([-g(k),right]);add([g(k),-left,-right])
 }
 add([g(K-1)]);
 // This is the exact restriction on all selectors and all chain outputs, NOT a SAT oracle.
 let asn=new Map();
 for(let j=0;j<m;j++)for(let t=0;t<3;t++)for(let l of vals)asn.set(x(j,t,l),F[j][t]===l);
 for(let k=1;k<K;k++)asn.set(g(k),true);
 let residual=[];
 for(let c of S){
   let w=c.filter(z=>Math.abs(z)<=n), external=c.filter(z=>Math.abs(z)>n);
   assert(external.every(z=>asn.has(Math.abs(z))),"complete restriction");
   if(!external.some(z=>asn.get(Math.abs(z))===(z>0)))residual.push(w);
 }
 assert(JSON.stringify(residual)===JSON.stringify(F),"source-exact residue");
 let ascii="p cnf "+vcount+" "+S.length+"\n"+S.map(c=>c.join(" ")+" 0").join("\n")+"\n";
 return {variables:vcount,source_clauses:S.length,source_ascii_bytes:Buffer.byteLength(ascii),
   source_sha256:crypto.createHash("sha256").update(ascii).digest("hex"),restricted_clauses:residual.length}
}
const fixtures=[
 {name:"opposite_3xor",n:3,rows:[[[1,2,3],1],[[1,2,3],0]]},
 {name:"odd_K4_tseitin",n:6,rows:[[[1,2,3],1],[[1,4,5],0],[[2,4,6],0],[[3,5,6],0]]},
 {name:"even_K4_tseitin",n:6,rows:[[[1,2,3],0],[[1,4,5],0],[[2,4,6],0],[[3,5,6],0]]}
];
let output=[];
for(let f of fixtures){let F=parityCNF(f.rows),b=build(f.n,F),sat=models(f.n,F);
  let deleted=(sat===0)?F.filter((_,j)=>models(f.n,F.filter((_,k)=>j!==k))===0).length:0;
  assert(!deleted,"all original clauses indispensable in tested UNSAT formulas");
  output.push({name:f.name,n:f.n,m:F.length,models:sat,paid_upper:sat===0?(40*f.rows.length-3):null,...b});
}
console.log(JSON.stringify({status:"PASS",scope:"source construction/restriction and symbolic upper-cost only; complete proof DAG replay is in archive",results:output},null,2));