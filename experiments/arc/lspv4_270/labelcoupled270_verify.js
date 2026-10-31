"use strict";
// Independent formula construction and complete enumeration.
// Usage: node labelcoupled270_verify.js path/to/labelcoupled270_raw.json
const fs=require("fs"),raw=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));let checked=0;
function v(l,a){return ((a>>(Math.abs(l)-1))&1)===(l>0?1:0)}
function model(F,a){for(const C of F){let good=false;for(const l of C)good=good||v(l,a);if(!good)return false;}return true}
function parent(m,h){
 const out=[];for(let i=0;i<m;i++)out.push(i+1!==h?[1,2,3]:[-1,h%2?2:-2,3]);
 for(const [x,y,z] of [[2,4,5],[3,6,7]])for(let k=0;k<4;k++)out.push([-x,(k&1)?y:-y,(k&2)?z:-z]);
 return out;
}
function child(m,h,F){const p=h%2?2:-2;return [[p,3,8],[p,3,-8],...F.slice(m)]}
function emit(F){let n=0;for(const C of F)for(const l of C)n=Math.max(n,Math.abs(l));
 return "N"+String(n).padStart(2,"0")+"M"+String(F.length).padStart(4,"0")+"|"+
 F.map(C=>C.map(l=>(l>0?"+":"-")+String(Math.abs(l)).padStart(2,"0")).join("")).join("|")+"|";
}
function minimax(m){
 const memo=new Map();
 function T(mask){
  if(memo.has(mask))return memo.get(mask);
  let p=0,n=0;for(let i=0;i<m;i++)if(mask&(1<<i)){if(i%2)p++;else n++}
  if(!p||!n)return 0;
  let b=Infinity;for(let i=0;i<m;i++)if(mask&(1<<i))b=Math.min(b,1+T(mask&~(1<<i)));
  memo.set(mask,b);return b;
 }
 return T((1<<m)-1);
}
for(const r of raw.rows){
 const F=parent(r.m,r.h),G=child(r.m,r.h,F);
 let M=0,K=0;for(let a=0;a<128;a++){M+=+model(F,a);checked++}
 for(let a=0;a<256;a++){K+=+model(G,a);checked++}
 if(M!==r.models||K!==r.childModels||(M>0)!==(r.h%2===0))throw Error("independent SAT/UNSAT error");
 if(emit(F).length*8!==r.originalPhysicalBits||emit(G).length*8!==r.childPhysicalBits)throw Error("physical length error");
 const opposite=parent(r.m,r.h===r.m?r.m-1:r.m);
 if(emit(F).length!==emit(opposite).length)throw Error("length leaked");
 if(r.materializedChildClauseWrites!==G.length||r.exactMinimaxBitProbes!==r.m/2)throw Error("tariff");
 if(r.m<=16){
  const src=raw.fullControls.find(s=>s.m===r.m&&s.h===r.h);
  for(let a=0;a<128;a++)for(const C of F){
   if(C.filter(l=>v(l,a)).length+C.filter(l=>v(l,a^127)).length!==3)throw Error("complement");
   checked++;
  }
  for(const p of src.originalClausePairExtremes)for(const t of ["SS","SU","US","UU"]){
   let found=false;
   for(let a=0;a<128;a++)if(F[p.j-1].filter(l=>v(l,a)).length===(t[0]==="S"?3:0)&&F[p.k-1].filter(l=>v(l,a)).length===(t[1]==="S"?3:0)){found=true;break}
   if(found!==p[t])throw Error("pair");checked++;
  }
 }
}
for(const m of [4,6,8,10]){if(minimax(m)!==m/2)throw Error("minimax");checked++}
for(const m of [8,16]){const a=parent(m,m-1),b=parent(m,m);
 if(model(a,1)!==false||model(b,1)!==true)throw Error("corrupted label control");checked+=2}
console.log(JSON.stringify({id:raw.id,status:"PASS",independentChecks:checked,bothLabels:true,minimaxExhaustive:[4,6,8,10]}));
