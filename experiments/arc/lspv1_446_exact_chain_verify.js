// LSPV-1/446: standalone exact original-source core and strict-Resolution verifier
"use strict";
let checks=0;
const ok=(p,m)=>{if(!p)throw Error(m);checks++};
const truth=(l,a)=>l>0?a[Math.abs(l)]===1:a[Math.abs(l)]===0;
const sat=(F,a,omit=-1)=>F.every((c,i)=>i===omit||c.some(l=>truth(l,a)));
const bad=(v,b)=>v.map((x,i)=>b[i]?-x:x);
function build(k,bits){
 const F=[],gates=[],pads=[];let next=k+1,acc=1;
 for(let i=2;i<=k;i++){
  const o=next++,ids=[];
  for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let z=0;z<2;z++)if(z!==(x^y)){
   ids.push(F.length);F.push(bad([acc,i,o],[x,y,z]));
  }
  gates.push({a:acc,b:i,o,ids});acc=o;
 }
 for(let i=1;i<=k+1;i++){
  const id=i<=k?i:acc,lit=i<=k?(bits[i-1]?id:-id):-id,p=next++,q=next++,ids=[];
  for(let x=0;x<2;x++)for(let y=0;y<2;y++){
   ids.push(F.length);F.push([lit,x?-p:p,y?-q:q]);
  }
  pads.push({id,lit,p,q,ids,input:i<=k});
 }
 ok(F.length===8*k&&next-1===4*k+1,"full original target sizes");
 const a=Array(next).fill(0);bits.forEach((x,i)=>a[i+1]=x);
 for(const g of gates)a[g.o]=a[g.a]^a[g.b];
 const core=pads.flatMap(p=>p.ids);
 for(const g of gates){
  let w=a.slice();w[g.o]^=1;
  let sel=g.ids.filter(i=>!sat([F[i]],w));
  ok(sel.length===1,"one active gate source clause");g.active=sel[0];core.push(g.active);
 }
 ok(new Set(core).size===5*k+3,"source capacity");
 return {k,F,gates,pads,a,core,output:acc};
}
function verify(t){
 const F=t.F,derived=[],refs=new Map();
 const get=r=>r>=0?F[r]:derived[-r-1].c;
 function res(a,b,p){
  const A=get(a),B=get(b);
  ok(A.includes(p)&&B.includes(-p),"oriented legal RES pivot");
  const c=[...new Set(A.concat(B).filter(x=>x!==p&&x!==-p))];
  ok(!c.some(x=>c.includes(-x)),"proper non-tautological resolvent");
  const id=-derived.length-1;derived.push({id,a,b,p,c});return id;
 }
 function pad(p){
  const [a,b,c,d]=p.ids;
  const x=res(a,b,p.q),y=res(c,d,p.q),z=res(x,y,p.p);
  ok(get(z).length===1&&get(z)[0]===p.lit,"recover padded unit");
  return z;
 }
 for(const p of t.pads.filter(x=>x.input))refs.set(p.id,pad(p));
 for(const g of t.gates){
  const al=get(refs.get(g.a))[0],bl=get(refs.get(g.b))[0];
  const out=(al>0)!==(bl>0)?g.o:-g.o;
  const cl=F[g.active];
  ok(cl.includes(-al)&&cl.includes(-bl)&&cl.includes(out),"gate facet authenticated");
  let x=res(refs.get(g.a),g.active,al),y=res(refs.get(g.b),x,bl);
  ok(get(y).length===1&&get(y)[0]===out,"derived exact XOR output");
  refs.set(g.o,y);
 }
 const plus=refs.get(t.output),minus=pad(t.pads.at(-1)),root=res(plus,minus,t.output);
 ok(get(root).length===0&&derived.length===5*t.k+2,"root and paid work");
 const sources=new Set(),visited=new Set();
 function visit(r){if(r>=0){sources.add(r);return}if(visited.has(r))return;
  visited.add(r);const z=derived[-r-1];ok(z&&z.id===r,"valid DAG");
  visit(z.a);visit(z.b);
 }
 visit(root);
 ok(sources.size===t.core.length&&t.core.every(i=>sources.has(i)),"only essential sources");
 const replay=trace=>{
  const D=[];
  for(const z of trace){
   const get=r=>r>=0?F[r]:D[-r-1];
   const A=get(z.a),B=get(z.b);
   if(!A||!B||!A.includes(z.p)||!B.includes(-z.p))return false;
   const C=[...new Set(A.concat(B).filter(x=>x!==z.p&&x!==-z.p))];
   if(C.length!==z.c.length||!C.every(x=>z.c.includes(x)))return false;
   D.push(C);
  }
  return D.length>0&&D.at(-1).length===0;
 };
 ok(replay(derived),"replayed complete source proof");
 const forged=derived.map(x=>({...x}));forged[0].p+=1000;
 ok(!replay(forged),"corrupted pivot rejected");
 ok(!replay(derived.slice(0,-1)),"omitted conclusion rejected");
}
function deletion(t,id){
 const a=t.a.slice(),pad=t.pads.find(p=>p.ids.includes(id));
 if(pad){
  if(pad.input){a[pad.id]^=1;for(const g of t.gates)a[g.o]=a[g.a]^a[g.b]}
  const C=t.F[id];a[pad.p]=C.includes(pad.p)?0:1;a[pad.q]=C.includes(pad.q)?0:1;
 }else{
  const g=t.gates.find(x=>x.active===id);ok(g!==undefined,"active source gate");
  a[g.o]^=1;
  for(let j=t.gates.indexOf(g)+1;j<t.gates.length;j++){
   const h=t.gates[j];a[h.o]=a[h.a]^a[h.b];
  }
 }
 ok(!sat(t.F,a)&&sat(t.F,a,id),"deleted source essential IN FULL FORMULA");
}
let cases=0,proofs=0,deletions=0;
for(let k=2;k<=5;k++)for(let mask=0;mask<(1<<k);mask++){
 const bits=Array.from({length:k},(_,i)=>(mask>>i)&1),t=build(k,bits);
 if(bits.reduce((a,b)=>a^b,0)){
  ok(!sat(t.F,t.a),"odd charge UNSAT");
  for(const j of t.core){deletion(t,j);deletions++}
  verify(t);proofs++;
 }else ok(sat(t.F,t.a),"even SAT control");
 cases++;
}
console.log(JSON.stringify({pass:true,cases,proofs,deletions,checks,scope:"Restricted original-source RES and complete-source deletion witness; not historical accepted-byte /341 checker"}));
