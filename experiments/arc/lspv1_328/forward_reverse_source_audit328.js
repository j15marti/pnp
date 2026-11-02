// LSPV-1 328: standalone source/Circuit-SAT check (Node >=18, no dependencies).
// Independent Python verifier and full false-clause leaves in user-facing archive.
"use strict";
const fs = require("fs");
const P9=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9]];
const N9=[[4,6,8],[1,6,7],[2,3,4],[3,5,8],[1,2,9],[5,7,9]];
const P6=[[1,2,3],[1,4,5],[2,4,6],[3,5,6]];
const mk=(p,n)=>p.map(x=>x.slice()).concat(n.map(x=>x.map(z=>-z)));
const F9=mk(P9,N9), Z6=mk(P6,P6);
const union=F9.concat(Z6.map(c=>c.map(x=>Math.sign(x)*(Math.abs(x)+9))));
function check(f,n){
 if(3*f.length!==4*n || n<1) throw Error("size");
 const seen=new Set(),pos=Array(n).fill(0),neg=Array(n).fill(0);
 for(const c of f){
  if(c.length!==3 || new Set(c.map(Math.abs)).size!==3 ||
    !c.every(x=>x>0) && !c.every(x=>x<0) ||
    !c.every(x=>Number.isInteger(x)&&Math.abs(x)>=1&&Math.abs(x)<=n))throw Error("clause");
  const key=c.slice().sort((a,b)=>a-b).join(",");
  if(seen.has(key))throw Error("duplicate"); seen.add(key);
  for(const x of c)(x>0?pos:neg)[Math.abs(x)-1]++;
 }
 if(pos.some(x=>x!==2)||neg.some(x=>x!==2))throw Error("quota");
 return true;
}
function sat(f,a){return f.every(c=>c.some(x=>x>0?a[Math.abs(x)-1]===1:a[Math.abs(x)-1]===0));}
function gate(f,a){
 const lit=x=>x>0?a[x-1]:1-a[-x-1];
 let gates=0;
 const vals=f.map(c=>{let t=lit(c[0])|lit(c[1]);gates++; t=t|lit(c[2]);gates++; return t;});
 let out=vals[0]; for(let j=1;j<vals.length;j++){out=out&vals[j];gates++;}
 return [out,gates];
}
function count(f,n,pins={}){
 let count=0;for(let q=0;q<2**n;q++){
  const a=Array.from({length:n},(_,i)=>(q>>i)&1);
  if(Object.entries(pins).some(([key,v])=>a[Number(key)-1]!==v))continue;
  if(sat(f,a))count++;
 }return count;
}
function serialize(f,n){
 const w=(x,b)=>x.toString(2).padStart(b,"0");
 return w(n,16)+w(f.length,16)+f.flatMap(c=>c.map(x=>w(Math.abs(x),16)+Number(x<0))).join("");
}
function parse(s){
 if(typeof s!=="string"||s.length<32||!/^[01]+$/.test(s))throw Error("binary");
 const n=parseInt(s.slice(0,16),2),m=parseInt(s.slice(16,32),2);
 if(s.length!==32+51*m)throw Error("length");
 const f=[];
 for(let j=0;j<m;j++){let c=[];for(let k=0;k<3;k++){
  const q=s.slice(32+j*51+k*17,32+j*51+(k+1)*17);
  const x=parseInt(q.slice(0,16),2);c.push(q[16]==="1"?-x:x);
 }f.push(c);}
 check(f,n);return [n,f];
}
function pairs(f){
 let total=0,compatible=0;
 for(let i=0;i<f.length;i++)for(let j=i+1;j<f.length;j++)for(const s of [0,1])for(const t of [0,1]){
  const d=new Map();let ok=true;
  for(const [c,kind] of [[f[i],s],[f[j],t]])for(const x of c){
    const v=(x>0?1:0)^(kind===1?1:0),id=Math.abs(x);
    if(d.has(id)&&d.get(id)!==v)ok=false; d.set(id,v);
  }
  const same=f[i].some(x=>f[j].some(y=>Math.abs(x)===Math.abs(y)&&x*y>0));
  const opposite=f[i].some(x=>f[j].some(y=>Math.abs(x)===Math.abs(y)&&x*y<0));
  const expected=s===t?!opposite:!same;
  if(ok!==expected)throw Error("pair mode");
  total++;if(ok)compatible++;
 }
 return {total,compatible};
}
function run(){
 check(F9,9);check(Z6,6);check(union,15);
 let checks=0,gateOps=0;
 for(const [f,n] of [[F9,9],[Z6,6]])for(let x=0;x<2**n;x++){
  const a=Array.from({length:n},(_,j)=>(x>>j)&1);
  const [v,g]=gate(f,a);if(Boolean(v)!==sat(f,a)||g!==3*f.length-1)throw Error("gate");
  checks++;gateOps+=g;
 }
 const [a,b,c]=[count(F9,9),count(Z6,6),count(union,15)];
 if(a!==70||b!==18||c!==1260)throw Error("models");
 const pins={3:0,5:1,6:0,7:0,8:0};
 const cs=count(F9,9,{...pins,1:0}),cu=count(F9,9,{...pins,1:1});
 const us=count(union,15,{...pins,1:0}),uu=count(union,15,{...pins,1:1});
 if(cs!==2||cu!==0||us!==36||uu!==0)throw Error("pins");
 const q=pairs(F9);if(q.total!==264||q.compatible!==172)throw Error("pairs");
 const binary=serialize(F9,9);const [n,restored]=parse(binary);
 if(n!==9||JSON.stringify(restored)!==JSON.stringify(F9))throw Error("binary roundtrip");
 const bad=[binary.slice(0,-1),binary+"0",binary.slice(0,16)+(13).toString(2).padStart(16,"0")+binary.slice(32),
  "x"+binary.slice(1),binary.slice(0,32)+"0".repeat(16)+binary.slice(48),
  binary.slice(0,32)+(10).toString(2).padStart(16,"0")+binary.slice(48),
  binary.slice(0,48)+(binary[48]==="0"?"1":"0")+binary.slice(49),
  binary.slice(0,83)+binary.slice(32,83)+binary.slice(134),
  binary.slice(0,32)+(9).toString(2).padStart(16,"0")+binary.slice(48),"","0","1".repeat(11)];
 for(const s of bad){let rejected=false;try{parse(s);}catch(_){rejected=true;}if(!rejected)throw Error("malformed accepted");}
 let leaves=0;for(let q=0;q<8;q++){
  const a=Array(9).fill(0);for(const [v,b] of Object.entries({...pins,1:1}))a[+v-1]=b;
  [2,4,9].forEach((id,i)=>a[id-1]=(q>>i)&1);
  if(sat(F9,a))throw Error("invalid UNSAT leaf");leaves++;
 }
 return {status:"PASS",F9_models:a,Z6_models:b,F15_models:c,forward_rows:checks,gate_executions:gateOps,
  pair_modes:q,source_binary_bits:binary.length,malformed_rejected:bad.length,
  F9_same_original:{SAT:cs,UNSAT:cu,refutation_leaves:leaves},F15_same_original:{SAT:us,UNSAT:uu}};
}
const output=run();process.stdout.write(JSON.stringify(output,null,2)+"\n");
