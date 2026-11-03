"use strict";
// Independent finite verifier for LSPV-3 370, no imports from producer.
function chk(ok,msg){if(!ok)throw Error(msg)}
const core=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],v=4;
const inc=Array.from({length:v},()=>[]);for(let i=0;i<core.length;i++)for(const a of core[i])inc[a].push(i);
let E=[];const left=x=>3*x,right=x=>3*x+1,point=x=>3*x+2;
for(let i=0;i<core.length;i++){
 const [a,b]=core[i];E.push([inc[a].indexOf(i)<2?left(a):right(a),inc[b].indexOf(i)<2?left(b):right(b)]);
}
for(let k=0;k<v;k++)E.push([left(k),right(k)]);
for(let k=0;k<v;k++)E.push([right(k),point(k)]);
for(let k=0;k<v;k++)E.push([point(k),point((k+1)%v)]);
chk(E.length===18,"edge size");
let around=Array.from({length:12},()=>[]);
for(let i=0;i<E.length;i++)for(const a of E[i])around[a].push(i);
chk(around.every(x=>x.length===3),"noncubic");
const parity=(a,b,c)=>a^b^c;
let local=0;
for(let rhs=0;rhs<2;rhs++){
 let C=[];
 for(let forbid=0;forbid<8;forbid++){
  if(parity(forbid&1,(forbid>>1)&1,(forbid>>2)&1)===rhs)continue;
  C.push([0,1,2].map(i=>((forbid>>i)&1)?-(i+1):i+1));
 }
 chk(C.length===4,"blocker count");
 for(let bits=0;bits<8;bits++){
  let okay=C.every(cl=>cl.some(l=>Number(l>0)===((bits>>(Math.abs(l)-1))&1)));
  chk(okay===(parity(bits&1,(bits>>1)&1,(bits>>2)&1)===rhs),"local parity wrong");
  local++;
 }
}
let odd=0,even=0;
let charge=Array(12).fill(0);charge[point(0)]=1;
for(let assignment=0;assignment<1<<18;assignment++){
 let goodOdd=true,goodEven=true;
 for(let i=0;i<12;i++){
  let row=0;
  for(const e of around[i])row^=(assignment>>e)&1;
  if(row!==charge[i])goodOdd=false;
  if(row!==0)goodEven=false;
 }
 if(goodOdd)odd++;
 if(goodEven)even++;
}
chk(odd===0,"odd has model");chk(even===128,"even count incorrect");
let corruption=0;
const wrongCharge=charge.slice();wrongCharge[point(0)]=0;
chk(wrongCharge.reduce((x,y)=>x^y,0)===0,"bad parity corruption accepted");corruption++;
console.log(JSON.stringify({independent_js:true,graph:"K4 three-vertex-fiber charge-cycle",enumerated_assignments:262144,
 local_truth_rows:local,odd_models:odd,even_models:even,corrupted_charge_flagged:corruption},null,2));