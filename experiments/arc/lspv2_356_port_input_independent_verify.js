"use strict";
/* Independent authenticated signed-Tseitin clause and resolution verifier. */
function key(a){return [...new Set(a)].sort((x,y)=>x-y).join(",")}
function expected(t){
 const E=[];
 for(const [ci,gates] of [t.A,t.B].entries()){
  const off=ci?t.k+t.A.length:t.k;
  for(let j=0;j<gates.length;j++){
   const g=gates[j],w=v=>Math.sign(v)*(Math.abs(v)<=t.k?Math.abs(v):off+Math.abs(v)-t.k);
   const a=w(g.a),b=w(g.b),z=off+j+1;
   if(!["A","X"].includes(g.op)||!a||!b||Math.abs(a)===Math.abs(b)||Math.abs(a)>=z||Math.abs(b)>=z)throw Error("invalid gate");
   const cs=g.op==="A"?[[-z,a],[-z,b],[z,-a,-b]]:[[a,b,-z],[a,-b,z],[-a,b,z],[-a,-b,-z]];
   E.push(...cs.map(key));
  }
 }
 E.push(key([t.k+t.A.length]),key([-t.k-t.A.length-t.B.length]));
 return E.sort();
}
function check(r){
 const t=r.test;
 if(!Number.isInteger(t.k)||t.k<2||!t.A?.length||!t.B?.length)throw Error("invalid circuit");
 const e=expected(t),a=r.source.map(key).sort();
 if(e.length!==a.length||e.some((x,i)=>x!==a[i]))throw Error("source authenticity mismatch");
 const lines=r.source.map(c=>[...c]);let checked=0;
 for(const node of r.lines){
  if(!Array.isArray(node.p)||node.p.length!==2)throw Error("parents absent");
  const [a,b]=node.p,v=node.v;
  if(!Number.isInteger(a)||!Number.isInteger(b)||a<0||b<0||a>=lines.length||b>=lines.length||a===b)throw Error("nonprevious parent");
  if(!Number.isInteger(v)||v<1||v>t.k+t.A.length+t.B.length)throw Error("pivot range");
  const A=lines[a],B=lines[b];
  if(!((A.includes(v)&&B.includes(-v))||(A.includes(-v)&&B.includes(v))))throw Error("no complementary pivot");
  const cl=[...new Set([...A,...B].filter(x=>Math.abs(x)!==v))].sort((x,y)=>x-y);
  if(cl.some(x=>cl.includes(-x)))throw Error("tautological");
  if(key(cl)!==key(node.c))throw Error("wrong exact resolvent");
  lines.push([...node.c]);checked++;
 }
 if(r.root!==null){
  if(r.root!==lines.length-1||lines[r.root].length!==0||r.satWitness!==null)throw Error("invalid proof target");
 }else{
  if(!Array.isArray(r.satWitness)||r.satWitness.length!==t.k+t.A.length+t.B.length)throw Error("missing model");
  if(!r.source.every(c=>c.some(x=>x>0?r.satWitness[x-1]===1:r.satWitness[-x-1]===0)))throw Error("invalid model");
 }
 if(r.metrics.derived!==r.lines.length||r.lines.length>r.metrics.bound)throw Error("bad logical cost");
 return checked;
}
function evaluate(gates,a0){const a=[null,...a0];for(const g of gates){const x=g.a>0?a[g.a]:1-a[-g.a],y=g.b>0?a[g.b]:1-a[-g.b];a.push(g.op==="X"?x^y:x&y)}return a.at(-1)}
let checks=0,corruptRejected=0,malformedRejected=0,proofs=0,satCases=0;
for(const r of data.cases){
 checks+=check(r);
 const t=r.test;let agree=true,orientedMismatch=false;
 for(let m=0;m<2**t.k;m++){
  let bits=Array.from({length:t.k},(_,j)=>m>>j&1),a=evaluate(t.A,bits),b=evaluate(t.B,bits);
  if(a!==b)agree=false;if(a===1&&b===0)orientedMismatch=true;
  if(r.truth[m].A!==a||r.truth[m].B!==b)throw Error("truth table mismatches");
  checks++;
 }
 if(r.root!==null){
  proofs++;if(!agree)throw Error("proof for inequivalent circuits");
  const mutations=[];
  if(r.lines.some(l=>l.c.length)){const x=JSON.parse(JSON.stringify(r)),i=x.lines.findIndex(l=>l.c.length);x.lines[i].c[0]*=-1;mutations.push(x)}
  {const x=JSON.parse(JSON.stringify(r));x.lines[0].v=0;mutations.push(x)}
  {const x=JSON.parse(JSON.stringify(r));x.lines[0].p[0]=999999;mutations.push(x)}
  {const x=JSON.parse(JSON.stringify(r));x.root=0;mutations.push(x)}
  {const x=JSON.parse(JSON.stringify(r));x.source[0][0]*=-1;mutations.push(x)}
  for(const x of mutations){let err=false;try{check(x)}catch{err=true}if(!err)throw Error("accepted corruption");corruptRejected++;checks++}
 }else{satCases++;if(agree||!orientedMismatch)throw Error("SAT control wrong")}
}
for(const t of [{k:0,A:[],B:[]},{k:3,A:[{op:"A",a:1,b:1}],B:[{op:"A",a:1,b:2}]},{k:2,A:[{op:"Z",a:1,b:2}],B:[{op:"A",a:1,b:2}]},{k:2,A:[{op:"A",a:1,b:5}],B:[{op:"A",a:1,b:2}]}]){
 let err=false;try{check({test:t,source:[],lines:[],root:null})}catch{err=true}if(!err)throw Error("malformed accepted");malformedRejected++;checks++;
}
return {status:"PASS",checks,proofs,satCases,corruptRejected,malformedRejected,rawBlob:raw.sha};

