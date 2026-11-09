"use strict";
/* LSPV-1/527 finite control: full original-source strict 3-CNF K4 mod3
   refutation using ordinary oriented binary Resolution only.
   Not historical R_mix341 accepted-byte checker execution.
   node lspv1_527_k4_original_resolution.cjs > k4_527.json
*/
function canon(a){
 if(!Array.isArray(a)||a.some(z=>!Number.isInteger(z)||z===0))throw Error("bad literal");
 const s=[...new Set(a)];if(s.some(z=>s.includes(-z)))return null;
 return s.sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
}
function source(charge=1){
 const E=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)E.push([i,j]);
 const clauses=E.map((_,i)=>canon([3*i+1,3*i+2,3*i+3]));
 for(let v=0;v<4;v++){
   const I=[];for(let k=0;k<E.length;k++)if(E[k].includes(v))I.push([k,v===E[k][0]?1:-1]);
   if(I.length!==3)throw Error("not cubic");
   for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let c=0;c<3;c++){
     const z=(I[0][1]*a+I[1][1]*b+I[2][1]*c-(v===0?charge:0)+30)%3;
     if(z!==0)clauses.push(canon([-3*I[0][0]-1-a,-3*I[1][0]-1-b,-3*I[2][0]-1-c]));
   }
 }
 if(clauses.length!==78||clauses.some(c=>c.length!==3))throw Error("invalid original strict source");
 return clauses;
}
function proof(order=[2,1,3,6,5,4,12,11,10,8,7,9,13,15,14,17,16,18]){
 const clauses=source(1),lines=clauses.map(c=>({kind:"SOURCE",clause:c})),
       seen=new Map(clauses.map((c,i)=>[c.join(","),i]));
 let active=new Set(lines.map((_,i)=>i)),root=-1;
 function subset(a,b){return a.every(x=>b.includes(x))}
 function lex(a,b){for(let i=0;i<Math.min(a.length,b.length);i++)if(a[i]!==b[i])return a[i]-b[i];return a.length-b.length}
 for(const variable of order){
   const pos=[...active].filter(i=>lines[i].clause.includes(variable));
   const neg=[...active].filter(i=>lines[i].clause.includes(-variable));
   const independent=[...active].filter(i=>!lines[i].clause.includes(variable)&&!lines[i].clause.includes(-variable));
   const proposals=new Map();
   for(const p of pos)for(const n of neg){
     const c=canon(lines[p].clause.filter(x=>x!==variable).concat(lines[n].clause.filter(x=>x!==-variable)));
     if(c===null)continue;const key=c.join(",");
     if(!seen.has(key)&&!proposals.has(key))proposals.set(key,{c,p,n});
   }
   const chosen=new Map(independent.map(i=>[lines[i].clause.join(","),i]));
   const next=[...proposals.values()].sort((a,b)=>a.c.length-b.c.length||lex(a.c,b.c));
   for(const {c,p,n} of next){
     if([...chosen.keys()].some(key=>subset(key===""?[]:key.split(",").map(Number),c)))continue;
     let id=seen.get(c.join(","));
     if(id===undefined){id=lines.length;lines.push({kind:"RES",clause:c,left:p,right:n,pivot:variable});seen.set(c.join(","),id)}
     chosen.set(c.join(","),id);
   }
   active=new Set(chosen.values());
   if(chosen.has("")){root=chosen.get("");break}
 }
 if(root<0)throw Error("not refuted");
 const needed=new Set(),stack=[root];
 while(stack.length){const i=stack.pop();if(needed.has(i))continue;needed.add(i);if(lines[i].kind==="RES")stack.push(lines[i].left,lines[i].right)}
 const result=lines.slice(0,78).map(x=>({...x})),mapping=new Map(result.map((_,i)=>[i,i]));
 for(const i of [...needed].sort((a,b)=>a-b))if(i>=78){
  const x=lines[i];mapping.set(i,result.length);
  result.push({kind:"RES",clause:x.clause,left:mapping.get(x.left),right:mapping.get(x.right),pivot:x.pivot});
 }
 return {name:"K4_mod3_strict3_complete_RES527",classification:"FINITE COMPUTATIONAL UPPER CONTROL; not a native historical byte checker",source_count:78,original_var_count:18,charge:1,paid_res:result.length-78,root:mapping.get(root),order,lines:result};
}
function verify(x){
 const S=source(x.charge);if(!Array.isArray(x.lines)||x.source_count!==78||x.lines.length!==x.paid_res+78)throw Error("shape");
 const depth=[],A=x.lines;for(let i=0;i<A.length;i++){
  const z=A[i],c=canon(z.clause);if(c===null||JSON.stringify(c)!==JSON.stringify(z.clause))throw Error("bad clause");
  if(i<78){if(z.kind!=="SOURCE"||JSON.stringify(c)!==JSON.stringify(S[i]))throw Error("foreign original");depth[i]=0;continue}
  if(z.kind!=="RES"||z.left>=i||z.right>=i||z.left<0||z.right<0||z.pivot<1||z.pivot>18)throw Error("bad parent/pivot");
  const L=A[z.left].clause,R=A[z.right].clause,p=z.pivot;
  if(!L.includes(p)||!R.includes(-p))throw Error("bad oriented pivot");
  if(JSON.stringify(canon(L.filter(t=>t!==p).concat(R.filter(t=>t!==-p))))!==JSON.stringify(c))throw Error("wrong resolvent");
  depth[i]=1+Math.max(depth[z.left],depth[z.right]);
 }
 if(x.root<78||x.root>=A.length||A[x.root].clause.length!==0)throw Error("no contradiction");
 const used=new Set(),pending=[x.root];
 while(pending.length){const i=pending.pop();if(used.has(i))continue;used.add(i);if(A[i].kind==="RES")pending.push(A[i].left,A[i].right)}
 if([...used].filter(i=>i>=78).length!==x.paid_res)throw Error("unused derived nodes");
 return {paid:x.paid_res,root_depth:depth[x.root],total_records:A.length,source_ancestors:[...used].filter(i=>i<78).length,proof_literal_occurrences:A.reduce((s,x)=>s+x.clause.length,0)};
}
if(typeof module!=="undefined")module.exports={source,proof,verify};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const x=proof();console.error(JSON.stringify(verify(x)));console.log(JSON.stringify(x));
}
