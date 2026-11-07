#!/usr/bin/env node
// LSPV-1/464 standalone check. Native binary Resolution only, NOT R_mix341.
'use strict';
let checks=0;
function ok(b,m){checks++;if(!b)throw Error(m||'failed');}
function canon(L){let S=[...new Set(L)];if(S.some(x=>S.includes(-x)))return null;return S.sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);}
function same(a,b){return JSON.stringify(a)===JSON.stringify(b);}
function sub(a,b){return a!==null&&b!==null&&a.every(x=>b.includes(x));}
function resolution(A,B,p){
 if(A.includes(p)&&B.includes(-p))return canon([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]);
 if(A.includes(-p)&&B.includes(p))return canon([...A.filter(x=>x!==-p),...B.filter(x=>x!==p)]);
 throw Error('invalid pivot');
}
function substitute(C,alias){if(C===null)return null;let R=[];for(let l of C){let w=alias[Math.abs(l)]??Math.abs(l);if(typeof w==='string'){let val=(w==='T')===(l>0);if(val)return null;}else R.push(l>0?w:-w);}return canon(R);}
function local(A,B,p,alias){
 let C=resolution(A,B,p);ok(C!==null,'source resolvent taut');let T=substitute(C,alias),a=substitute(A,alias),b=substitute(B,alias);
 if(T===null)return 'taut';
 if(a===null){ok(sub(b,T),'taut left');return 'parent2';}
 if(b===null){ok(sub(a,T),'taut right');return 'parent1';}
 if(sub(a,T))return 'parent1';
 if(sub(b,T))return 'parent2';
 let w=alias[p]??p;ok(typeof w==='number','constant pivot');
 ok(sub(resolution(a,b,Math.abs(w)),T),'mapped resolvent');
 return 'resolve';
}
let all=[];
for(let n=0;n<27;n++){let t=n,A=[];for(let j=1;j<=3;j++){let z=t%3;t=Math.floor(t/3);if(z)A.push(z===1?j:-j);}all.push(canon(A));}
let counts={taut:0,parent1:0,parent2:0,resolve:0};
for(let A of all)for(let B of all)for(let p=1;p<=3;p++){
 if(!((A.includes(p)&&B.includes(-p))||(A.includes(-p)&&B.includes(p))))continue;
 if(resolution(A,B,p)===null)continue;
 for(let v=1;v<=3;v++)for(let a of ['T','F',...[-3,-2,-1,1,2,3].filter(x=>Math.abs(x)!==v)]){
  counts[local(A,B,p,{[v]:a})]++;
 }
}
ok(Object.values(counts).reduce((a,b)=>a+b,0)===5292,'local test count');
ok(counts.taut===936&&counts.parent1===1302&&counts.parent2===1302&&counts.resolve===1752,'local counts');
// Odd K4 Tseitin: 6 edge vars, 4 four-clause signed parity rows.
let edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],F=[];
for(let v=0;v<4;v++){
 let I=edges.flatMap(([a,b],i)=>(a===v||b===v)?[i+1]:[]);
 for(let mask=0;mask<8;mask++){
  let b=[0,1,2].map(j=>(mask>>j)&1);
  if((b.reduce((a,c)=>a+c,0)%2)===(v===0?1:0))continue;
  F.push(canon(I.map((x,j)=>b[j]?-x:x)));
 }
}
ok(F.length===16);
for(let mask=0;mask<64;mask++){
 let sat=F.every(C=>C.some(l=>(((mask>>(Math.abs(l)-1))&1)===1)===(l>0)));
 ok(!sat,'K4 unexpectedly SAT');
}
let seen=new Map(F.map((C,i)=>[JSON.stringify(C),['s',i]])),active=[...F],nodes=[];
for(let p=1;p<=6;p++){
 let pos=active.filter(C=>C.includes(p)),neg=active.filter(C=>C.includes(-p)),rest=active.filter(C=>!C.some(l=>Math.abs(l)===p));
 for(let A of pos)for(let B of neg){
  let C=resolution(A,B,p);if(C===null)continue;
  let k=JSON.stringify(C);
  if(!seen.has(k)){seen.set(k,['n',nodes.length]);nodes.push({C,P:[seen.get(JSON.stringify(A)),seen.get(JSON.stringify(B))],p});}
  if(!rest.some(D=>same(D,C)))rest.push(C);
 }
 active=rest;
}
let root=seen.get('[]');ok(Boolean(root));
let use=new Set(),leaves=new Set();
function visit(ref){let [t,i]=ref;if(t==='s'){leaves.add(i);return;}if(use.has(i))return;use.add(i);nodes[i].P.forEach(visit);}
visit(root);ok(use.size===31,'31 paid expected');
let s=[...leaves].sort((a,b)=>a-b)[0],C=F[s],l=C[0],y=7;
let G=[canon([-y,l]),canon([y,-l])];
ok(G.every(cl=>substitute(cl,{[y]:l})===null),'G not alias-taut');
let C1=resolution(C,G[1],Math.abs(l));ok(same(resolution(C1,G[0],y),C),'detour invalid');
let S=[...F,...G],proof=[{C:C1,P:[['s',s],['s',17]],p:Math.abs(l)},{C,P:[['n',0],['s',16]],p:y}],map=new Map();
for(let i of [...use].sort((a,b)=>a-b)){
 let r=nodes[i],P=r.P.map(a=>a[0]==='s'?(a[1]===s?['n',1]:a):map.get(a[1]));
 map.set(i,['n',proof.length]);proof.push({C:r.C,P,p:r.p});
}
let goal=map.get(root[1]);ok(proof.length===33,'expected 33 inference nodes');
function verify(src,steps,last){
 for(let i=0;i<steps.length;i++){
  let r=steps[i],P=r.P.map(([t,j])=>{ok(t==='s'?j<src.length:j<i,'bad reference');return t==='s'?src[j]:steps[j].C;});
  ok(same(resolution(P[0],P[1],r.p),r.C),'invalid proof inference');
 }
 ok(same(steps[last[1]].C,[]),'no empty final');
}
verify(S,proof,goal);
let rewritten=[],ref=new Map(S.map((x,i)=>['s'+i,i<16?['s',i]:null])),act={taut:0,parent1:0,parent2:0,resolve:0};
for(let i=0;i<proof.length;i++){
 let r=proof[i],P=r.P.map(([t,j])=>t==='s'?S[j]:proof[j].C),kind=local(P[0],P[1],r.p,{[y]:l});act[kind]++;
 if(kind==='taut'){ref.set('n'+i,null);continue;}
 if(kind==='parent1'||kind==='parent2'){ref.set('n'+i,ref.get(r.P[kind==='parent1'?0:1].join('')));continue;}
 let ab=r.P.map(p=>ref.get(p.join('')));ok(ab.every(Boolean),'parent erased');
 let rr=ab.map(([t,j])=>t==='s'?F[j]:rewritten[j].C),pivot=r.p===y?Math.abs(l):r.p;
 let target=substitute(r.C,{[y]:l});ok(same(resolution(rr[0],rr[1],pivot),target),'incorrect projected step');
 ref.set('n'+i,['n',rewritten.length]);rewritten.push({C:target,P:ab,p:pivot});
}
verify(F,rewritten,ref.get(goal.join('')));
ok(rewritten.length===31&&act.parent1+act.parent2===2,'projection not nonexpansive');
for(let wrong of [[['s',999],['s',0]],[['n',900],['s',0]]]){
 let rejected=false;try{verify(S,[{C:[],P:wrong,p:1}],['n',0]);}catch{rejected=true;}ok(rejected,'corrupt refs accepted');
}
console.log(JSON.stringify({status:'COMPUTATIONAL',local_checks:5292,local_counts:counts,original_signed_K4_clauses:F.length,padded_paid:proof.length,projected_paid:rewritten.length,original_unsat:true,hostile_controls:2,assertion_checks:checks,warning:'NOT historical R_mix341 checker'},null,2));
