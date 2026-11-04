// LSPV-2/385: finite strict-resolution producer and source/pivot checker.
// Usage: node experiments/arc/lspv2_385_guarded_tseitin_public.js OUT_DIRECTORY
'use strict';
const fs=require('fs'),path=require('path');
function edges(name){if(name==="K4"){let e=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)e.push([i,j]);return e}
if(name==="K33"){let e=[];for(let i=0;i<3;i++)for(let j=3;j<6;j++)e.push([i,j]);return e}
if(name==="CUBE"){let e=[];for(let i=0;i<8;i++)for(let k=0;k<3;k++){let j=i^(1<<k);if(i<j)e.push([i,j])}return e}
if(name==="PRISM6"){let e=[];for(let i=0;i<6;i++){e.push([i,(i+1)%6]);e.push([i,i+6]);e.push([i+6,(i+1)%6+6])}return e}throw Error(name)}
function generate(name){
 const E=edges(name).map(e=>e.slice().sort((a,b)=>a-b)).sort((a,b)=>a[0]-b[0]||a[1]-b[1]),h=Math.max(...E.flat())+1,n=E.length,t=n+1,chi=Array.from({length:h},(_,v)=>+(v===0));
 const cn=a=>{let r=[...new Set(a)];if(r.some(x=>!x||r.includes(-x)))return null;return r.sort((a,b)=>Math.abs(a)-Math.abs(b)||(a<0?1:-1))},key=a=>JSON.stringify(a);
 const lines=[],seen=new Map();
 function add(kind,c,rest={}){let r=cn(c);if(!r)throw Error("bad clause");let k=key(r);if(seen.has(k))return seen.get(k);let i=lines.length;lines.push({kind,c:r,...rest});seen.set(k,i);return i}
 let sources=[];
 for(let v=0;v<h;v++){let ids=E.map((e,i)=>e.includes(v)?i+1:null).filter(x=>x!==null);if(ids.length!==3)throw Error("not cubic");
 for(let mask=0;mask<8;mask++){let b=[mask&1,(mask>>1)&1,(mask>>2)&1];if((b[0]^b[1]^b[2])!==chi[v])sources.push(add("source",ids.map((x,i)=>b[i]?-x:x).concat([-t]),{vertex:v}))}}
 let active=new Set(sources),profile=[];
 for(let p=1;p<=n;p++){let pos=[...active].filter(i=>lines[i].c.includes(p)),neg=[...active].filter(i=>lines[i].c.includes(-p)),added=[];
 for(let i of pos)for(let j of neg){let r=cn(lines[i].c.filter(x=>x!==p).concat(lines[j].c.filter(x=>x!==-p)));if(r)added.push(add("res",r,{pivot:p,parents:[i,j]}))}
 for(let i of pos)active.delete(i);for(let i of neg)active.delete(i);for(let i of added)active.add(i);
 profile.push({pivot:p,positive:pos.length,negative:neg.length,active:active.size,generated:added.length});if(lines.length>200000)throw Error("upper cap exceeded")}
 let target=seen.get(key([-t]));if(target===undefined)throw Error("missing guarded contradiction");
 let unit=add("source",[t],{vertex:"guard"}),end=add("res",[],{pivot:t,parents:[target,unit]}),used=new Set();
 function trace(i){if(used.has(i))return;used.add(i);if(lines[i].kind==="res")lines[i].parents.forEach(trace)}trace(end);
 let order=[...used].sort((a,b)=>a-b),lookup=new Map(order.map((x,i)=>[x,i])),proof=order.map(i=>{let r={...lines[i]};if(r.parents)r.parents=r.parents.map(j=>lookup.get(j));return r});
 let paid=proof.filter(r=>r.kind==="res").length,src=proof.filter(r=>r.kind==="source").length;if(src!==4*h+1)throw Error("missing essential source");
 let out={id:"LSPV2-385",model:"strict source-authenticated ordinary binary Resolution; R_mix341 subcalculus",status:"upper witness only, never a claimed minimum",graph:name,graph_edges:E,charges:chi,guard:t,source_clauses:src,paid_RES:paid,proof,steps:profile,encoded_proof_bytes:0};
 let z;do{z=JSON.stringify(out).length+1;if(out.encoded_proof_bytes===z)break;out.encoded_proof_bytes=z}while(true);return out
}
function verify(d){
 let E=d.graph_edges,h=d.charges.length,n=E.length,t=d.guard;
 let cn=x=>[...new Set(x)].sort((a,b)=>Math.abs(a)-Math.abs(b)||(a<0?1:-1)),k=x=>JSON.stringify(x);
 if(d.charges.reduce((a,b)=>a^b,0)!==1||t!==n+1)throw Error("charge/guard");
 let sources=new Map();
 for(let v=0;v<h;v++){let a=E.map((e,i)=>e.includes(v)?i+1:null).filter(x=>x!==null);if(a.length!==3)throw Error("cubic");for(let z=0;z<8;z++){let b=[z&1,(z>>1)&1,(z>>2)&1];if((b[0]^b[1]^b[2])!==d.charges[v])sources.set(k(cn(a.map((x,j)=>b[j]?-x:x).concat([-t]))),v)}}
 sources.set(k([t]),"guard");let got=new Set(),count=0;
 for(let i=0;i<d.proof.length;i++){let r=d.proof[i];if(k(cn(r.c))!==k(r.c))throw Error("canon");if(r.kind==="source"){let a=k(r.c);if(!sources.has(a)||got.has(a)||r.vertex!==sources.get(a))throw Error("source");got.add(a)}else{count++;let [a,b]=r.parents;if(!(Number.isInteger(a)&&Number.isInteger(b)&&0<=a&&a<i&&0<=b&&b<i))throw Error("parents");let A=d.proof[a].c,B=d.proof[b].c,p=r.pivot;if(!((A.includes(p)&&B.includes(-p))||(A.includes(-p)&&B.includes(p))))throw Error("pivot");let R=cn(A.filter(x=>Math.abs(x)!==p).concat(B.filter(x=>Math.abs(x)!==p)));if(R.some(x=>R.includes(-x))||k(R)!==k(r.c))throw Error("resolvent")}}
 if(got.size!==sources.size||count!==d.paid_RES||d.proof[d.proof.length-1].c.length||d.encoded_proof_bytes!==JSON.stringify(d).length+1)throw Error("ledger");
 return {graph:d.graph,vertices:h,edges:n,sources:got.size,paid_RES:count,records:d.proof.length,bytes:d.encoded_proof_bytes}
}
const out=process.argv[2]||'.';fs.mkdirSync(out,{recursive:true});
for(const name of ['K4','K33','CUBE','PRISM6']){
  const cert=generate(name),result=verify(cert),f=path.join(out,'lspv2_385_'+name.toLowerCase()+'_raw.json');
  fs.writeFileSync(f,JSON.stringify(cert)+'\n');console.log(JSON.stringify({file:f,...result}));
}
