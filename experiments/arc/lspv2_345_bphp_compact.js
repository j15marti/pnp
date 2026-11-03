#!/usr/bin/env node
"use strict";
/* LSPV-2 BPHP-MACRO345, self-contained signed BPHP generator and RES proof.
   All widths and source labels preserved; no learned answer oracle. */
const A=require("assert").strict, H=require("crypto");
const canon=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||(x<0?1:-1));
const key=a=>a.join(",");
const bphp=h=>{
 A.ok(h>=2 && !(h&(h-1)));
 let ell=Math.log2(h),n=(h+1)*ell,cs=[],labels=[];
 for(let i=0;i<h+1;i++)for(let j=i+1;j<h+1;j++)for(let hole=0;hole<h;hole++){
   let lits=[];
   for(const p of [i,j])for(let b=0;b<ell;b++)
      lits.push(((hole>>b)&1)?-(p*ell+b+1):(p*ell+b+1));
   cs.push(canon(lits));labels.push([i,j,hole]);
 }
 return {h,ell,n,cs,labels};
};
const modelCount=(cs,n)=>{
 let count=0;
 for(let a=0;a<2**n;a++)if(cs.every(c=>c.some(l=>(((a>>(Math.abs(l)-1))&1)===+(l>0)))))count++;
 return count;
};
const resolve=({n,cs})=>{
 let rows=cs.map((c,i)=>({id:i,op:"source",clause:c}));
 let active=new Map(cs.map((c,i)=>[key(c),i])), trials=0,taut=0,peak=active.size;
 for(let v=1;v<=n;v++){
   const plus=[],minus=[],remain=new Map();
   for(const [k,id] of active){
     let c=rows[id].clause;
     if(c.includes(v))plus.push(id);
     else if(c.includes(-v))minus.push(id);
     else remain.set(k,id);
   }
   for(const i of plus)for(const j of minus){
     trials++;
     const c=canon([...rows[i].clause.filter(x=>x!==v),...rows[j].clause.filter(x=>x!==-v)]);
     if(c.some(x=>c.includes(-x))){taut++;continue;}
     let k=key(c);if(!remain.has(k)){let id=rows.length;rows.push({id,op:"RES",parents:[i,j],pivot:v,clause:c});remain.set(k,id);}
   }
   active=remain;peak=Math.max(peak,active.size);
   if(active.has(""))break;
 }
 A.ok(active.has(""),"no contradiction");
 const sink=active.get(""),used=new Set(),stack=[sink];
 while(stack.length){const i=stack.pop();if(used.has(i))continue;used.add(i);let r=rows[i];if(r.op==="RES")stack.push(...r.parents);}
 let proof=rows.filter(r=>used.has(r.id)&&r.op==="RES");
 A.equal(used.size-proof.length,cs.length);
 return {proof,sink,trials,taut,peak,derived:rows.length-cs.length};
};
const results=[];
for(const h of [2,4]){
 let f=bphp(h),m=f.cs.length,s="p cnf "+f.n+" "+m+"\n"+f.cs.map(c=>c.join(" ")+" 0\n").join("");
 A.equal(modelCount(f.cs,f.n),0);
 const del=f.cs.map((_,i)=>modelCount(f.cs.filter((_,j)=>j!==i),f.n));
 let fac=1;for(let j=2;j<h;j++)fac*=j;
 A.ok(del.every(v=>v===fac));
 let sign=0;for(let i=0;i<m;i++)for(let j=0;j<f.cs[i].length;j++){
   let c=f.cs.map(x=>x.slice());c[i][j]*=-1;A.equal(modelCount(c,f.n),fac);sign++;
 }
 let p=resolve(f),proofBytes=Buffer.byteLength(JSON.stringify(p.proof));
 let record={h,variables:f.n,clauses:m,inputBits:8*Buffer.byteLength(s),
    sourceSHA256:H.createHash("sha256").update(s).digest("hex"),
    deletionModelsEach:fac,signFlipsVerified:sign,lower:m-1,upper:p.proof.length,
    proofBytes,pivotTests:p.trials,tautologicalCandidates:p.taut,
    peakActiveClauses:p.peak,proof:p.proof,source:f.cs};
 results.push(record);
}
A.equal(results[0].upper,5);
A.equal(results[1].upper,159);
console.log(JSON.stringify({run:"LSPV-2 BPHP-MACRO345",results},null,2));
