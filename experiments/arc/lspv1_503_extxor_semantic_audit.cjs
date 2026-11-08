#!/usr/bin/env node
"use strict";
// LSPV-1/503 independent SEMANTIC projection audit. This is NOT the syntactic
// Res(PC1/F2) checker; that separate Python DAG builder is in the run artifacts.
const X = ["x","y","t","u","v"];
const G = {z:["and","x","y"],w:["xor","y","t"],r:["and","z","t"]};
function check(c,desc) {if(!c) throw Error(desc||"assertion failed");}
function ancestors(w,stack=[]) {
  if(X.includes(w)) return new Set([w]);
  check(Object.hasOwn(G,w),"malformed/undefined gate");
  check(!stack.includes(w),"cyclic gate definition");
  const s=new Set();
  for(const q of G[w].slice(1))for(const a of ancestors(q,[...stack,w]))s.add(a);
  return s;
}
function value(w,a,stack=[]) {
  if(X.includes(w)) return a[w];
  check(Object.hasOwn(G,w)&&!stack.includes(w),"invalid gate");
  const [op,u,v]=G[w];
  const p=value(u,a,[...stack,w]),q=value(v,a,[...stack,w]);
  return op==="and"?(p&q):op==="xor"?(p^q):(()=>{throw Error("gate")})();
}
function parity(mask,a){let r=0;for(let i=0;i<X.length;i++) if(mask&(1<<i))r^=a[X[i]];return r;}
function supp(r) {let s=new Set();for(const w of r.ext) for(const x of ancestors(w))s.add(x);return [...s].sort();}
function sat(r,a) {let v=parity(r.mask,a);for(const w of r.ext)v^=value(w,a);return v===r.rhs;}
function row(mask,ext,rhs) {
  check(Number.isInteger(mask)&&mask>=0&&mask<(1<<X.length),"malformed original mask");
  check((rhs===0||rhs===1)&&ext.every(w=>Object.hasOwn(G,w)),"malformed row");
  check(new Set(ext).size===ext.length,"duplicate auxiliary");
  return {mask,ext:ext.slice().sort(),rhs};
}
function xor(A,B) {
  const extras=A.ext.filter(z=>!B.ext.includes(z)).concat(B.ext.filter(z=>!A.ext.includes(z)));
  return row(A.mask^B.mask,extras,A.rhs^B.rhs);
}
function projections(r){
  const s=supp(r),result=[];
  for(let i=0;i<(1<<s.length);i++){
    const a=Object.fromEntries(s.map((v,k)=>[v,(i>>k)&1]));
    const restricted=Object.assign(Object.fromEntries(X.map(x=>[x,0])),a);
    const mask=r.mask & ~s.reduce((m,x)=>m|(1<<X.indexOf(x)),0);
    let rhs=r.rhs^parity(r.mask & ~mask,restricted);
    for(const z of r.ext)rhs^=value(z,restricted);
    result.push({restricted:a,mask,rhs});
  }
  return result;
}
function projectSat(r,a) {
  return projections(r).every(p=>Object.keys(p.restricted).some(k=>a[k]!==p.restricted[k])||
    (parity(p.mask,a)===p.rhs));
}
const orig=[];
for(let i=0;i<32;i++)orig.push(Object.fromEntries(X.map((x,k)=>[x,(i>>k)&1])));
const rows=[];
for(let mask=0;mask<8;mask++)for(const ext of [[],["z"],["w"],["z","w"]])
 for(const rhs of [0,1])rows.push(row(mask,ext,rhs));
let pairs=0,semanticChecks=0,implicationChecks=0;
for(const A of rows)for(const B of rows){
 const C=xor(A,B);pairs++;
 for(const a of orig){
  for(const R of [A,B,C]) {
   check(projectSat(R,a)===sat(R,a),"projection mismatch");
   semanticChecks++;
  }
  if(sat(A,a)&&sat(B,a)){check(sat(C,a),"unsound XOR");implicationChecks++;}
 }
}
for(const R of [row(8,["z"],0),row(1,["z"],0),row(0,["z"],0),row(4,["w"],0),row(8,["r"],1)])
 for(const a of orig)check(projectSat(R,a)===sat(R,a),"nested gate mismatch");
let negatives=0;
for(const action of [
 ()=>row(32,[],0),()=>row(0,["ghost"],0),()=>row(0,[],2),
 ()=>ancestors("no_such_wire"),()=>{const old=G.r;G.r=["and","r","t"];try{ancestors("r");}finally{G.r=old;}}
]){let rejected=false;try{action();}catch{rejected=true;}check(rejected,"negative accepted");negatives++;}
const summary={type:"COMPUTATIONAL independent semantic controls",rows:rows.length,
 orderedPairs:pairs,projectionEquivalenceChecks:semanticChecks,
 selectedImplicationChecks:implicationChecks,malformedControlsRejected:negatives,
 limits:"Semantic audit only. Detailed syntactic paid-node audit is separate Python artifact; not historical R_mix341."};
if (typeof process!=="undefined") console.log(JSON.stringify(summary,null,2));
