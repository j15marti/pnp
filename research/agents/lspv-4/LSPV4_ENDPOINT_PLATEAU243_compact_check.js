"use strict";
/* LSPV-4 ENDPOINT-PLATEAU243 independent compact JS verifier, 2026-10-30.
   Standard Node.js; no dependencies; exhaustive where stated. This compact
   checker is independent of the larger local Python reproducer. */
const assert=require("assert");
const base=[[1,3,5],[1,-3,6],[-1,4,5],[-1,-4,6],[2,3,-5],[2,-3,-6],[-2,4,-5],[-2,-4,-6]];
function ring(r){
  const clauses=[];
  for(let j=0;j<r;j++)for(let k=0;k<8;k++){
    clauses.push(base[k].map((l,h)=>{
      const q=(k===0&&h===0)?(j+r-1)%r:j;
      return Math.sign(l)*(6*q+Math.abs(l));}));
  }
  return {n:6*r,clauses};
}
function signed22(F){
 const t=new Map();
 for(const c of F.clauses){assert.equal(c.length,3);assert.equal(new Set(c.map(Math.abs)).size,3);
  for(const l of c)t.set(l,(t.get(l)||0)+1);}
 return F.clauses.length*3===4*F.n&&
  [...Array(F.n)].every((_,i)=>t.get(i+1)===2&&t.get(-i-1)===2);
}
function connected(F){
 let seenV=new Set([1]), seenC=new Set(), stack=[1];
 while(stack.length){
  const v=stack.pop();
  for(let j=0;j<F.clauses.length;j++)if(F.clauses[j].some(l=>Math.abs(l)===v)){
    if(!seenC.has(j)){seenC.add(j);for(const l of F.clauses[j])
      if(!seenV.has(Math.abs(l))){seenV.add(Math.abs(l));stack.push(Math.abs(l));}}
  }
 }
 return seenV.size===F.n&&seenC.size===F.clauses.length;
}
function count(c,a){return c.reduce((s,l)=>s+(((a>>>(Math.abs(l)-1))&1)===(l>0?1:0)?1:0),0);}
function counts(F,a){const N=[0,0,0,0];for(const c of F.clauses)N[count(c,a)]++;return N;}
function local(c,mode){const d={};for(const l of c)d[Math.abs(l)]=mode==="S"?(l>0?1:0):(l>0?0:1);return d;}
function modes(c,d){const z={};for(const p of ["S","U"])for(const q of ["S","U"]){
  const a=local(c,p),b=local(d,q);
  z[p+q]=Object.keys(a).every(v=>!(v in b)||a[v]===b[v]);}
 return z;
}
function bruteModes(c,d){let vars=[...new Set([...c,...d].map(Math.abs))];let flags={SS:false,SU:false,US:false,UU:false};
 for(let mask=0;mask<(1<<vars.length);mask++){let a={};vars.forEach((v,k)=>a[v]=(mask>>k)&1);
  const k=c.filter(l=>a[Math.abs(l)]===(l>0?1:0)).length;
  const h=d.filter(l=>a[Math.abs(l)]===(l>0?1:0)).length;
  if(k===3&&h===3)flags.SS=true;if(k===3&&h===0)flags.SU=true;
  if(k===0&&h===3)flags.US=true;if(k===0&&h===0)flags.UU=true;
 }
 return flags;
}
function checkTriples(F){
 let z=0;
 for(let i=0;i<F.clauses.length;i++)
  for(let j=i+1;j<F.clauses.length;j++)
   for(let k=j+1;k<F.clauses.length;k++){
     const cs=[F.clauses[i],F.clauses[j],F.clauses[k]];
     for(let modesMask=0;modesMask<8;modesMask++){
       const A={};let feasible=true;
       for(let h=0;h<3;h++){
        let partial=local(cs[h],((modesMask>>h)&1)?"S":"U");
        for(const [v,w] of Object.entries(partial)){if(v in A&&A[v]!==w)feasible=false;A[v]=w;}
       }
       const vars=[...new Set(cs.flat().map(Math.abs))];let found=false;
       for(let assignment=0;assignment<(1<<vars.length);assignment++){
         const state={};vars.forEach((v,h)=>state[v]=(assignment>>h)&1);
         if(cs.every((c,h)=>c.every(l=>state[Math.abs(l)]===
              ((((modesMask>>h)&1)!==0)?(l>0?1:0):(l>0?0:1))))){found=true;break;}
       }
       assert.equal(feasible,found);
       z++;
     }
   }
 return z;
}
function audit(F){
 assert(signed22(F));assert(connected(F));
 const all=(1<<F.n)-1;const zero=counts(F,0),one=counts(F,all);
 let pair=0, triple=0;
 for(let i=0;i<F.clauses.length;i++){
   const C=F.clauses[i],S=local(C,"S"),U=local(C,"U");
   for(const [v,val] of Object.entries(S)){assert.equal(1-val,U[v]);}
   for(let j=i+1;j<F.clauses.length;j++){
     assert.deepEqual(modes(C,F.clauses[j]),bruteModes(C,F.clauses[j]));pair+=4;
   }
 }
 if(F.n<=6)triple=checkTriples(F);
 let complement=0,models=0,masks=[];
 for(let a=0;a<=all;a++){
  const p=counts(F,a),q=counts(F,all^a);
  for(let h=0;h<4;h++)assert.equal(p[h],q[3-h]);
  if(p[0]===0){models++;if(F.n===6)masks.push(a);}
  complement++;
 }
 for(let v=1;v<=F.n;v++){
   assert.equal(counts(F,1<<(v-1))[0],zero[0]);
   assert.equal(counts(F,all^(1<<(v-1)))[0],one[0]);
 }
 return {n:F.n,m:F.clauses.length,zero,one,pair_modes:pair,triple_modes:triple,
        complement_pairs:complement,models,small_model_masks:masks};
}
const r1=audit(ring(1)),r2=audit(ring(2)),r3=audit(ring(3));
assert.deepEqual(r1.small_model_masks,[21,26,38,41]);
assert.deepEqual(r1.zero,[1,3,3,1]);
assert.equal(r2.zero[0],2);assert.equal(r3.zero[0],3);
assert.deepEqual(modes(base[0],base[1]),{SS:false,SU:false,US:false,UU:false});
const resolvent=[1,5,6];
for(let a=0;a<64;a++)if(resolvent.every(l=>((a>>(l-1))&1)===0))
 assert(!(count(base[0],a)>0&&count(base[1],a)>0));
const out={result:"PASS",family:[r1,r2,r3],
 source_parent_resolvent:{parents:[0,1],pivot:3,clause:resolvent,
 forbidden_cube:{"1":0,"5":0,"6":0}},
 scope:"Finite exhaustive H1/H2/H3 source-status and all assignment complements, no general SAT complexity claim"};
process.stdout.write(JSON.stringify(out)+"\n");