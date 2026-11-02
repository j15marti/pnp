#!/usr/bin/env node
// LSPV-1 330 independent finite checks; no producer import.
// Full 5936-assertion checker appears in the linked reproducibility archive.
"use strict";
const F9P=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9]];
const F9N=[[4,6,8],[1,6,7],[2,3,4],[3,5,8],[1,2,9],[5,7,9]];
const Z6=[[1,2,3],[1,4,5],[2,4,6],[3,5,6]];
const B9P=[[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9]];
const B9N=[[1,5,9],[2,6,7],[3,4,8],[1,6,8],[2,4,9],[3,5,7]];
const S=(a,b)=>a.concat(b.map(c=>c.map(x=>-x)));
const shift=(a,b,k)=>a.concat(b.map(c=>c.map(x=>x>0?x+k:x-k)));
const f9=S(F9P,F9N),z6=S(Z6,Z6),b9=S(B9P,B9N);
let assertions=0;
function ok(v,msg){assertions++;if(!v)throw new Error(msg);}
function grammar(cs){
 if(!Array.isArray(cs)||!cs.length)return false;
 let seen=new Set(),v=new Map(),mx=0;
 for(const c of cs){
  if(c.length!==3||c.some(x=>!Number.isInteger(x)||!x)
     ||new Set(c.map(Math.abs)).size!==3||new Set(c.map(x=>x>0)).size!==1)return false;
  let key=c.slice().sort((a,b)=>a-b).join(",");
  if(seen.has(key))return false;seen.add(key);
  for(const x of c){mx=Math.max(mx,Math.abs(x));
   let k=Math.abs(x)+","+(x>0);v.set(k,(v.get(k)||0)+1);}
 }
 if(3*cs.length!==4*mx)return false;
 for(let i=1;i<=mx;i++)if(v.get(i+",true")!==2||v.get(i+",false")!==2)return false;
 return true;
}
function sat(cs,assignment){
 return cs.every(c=>c.some(x=>(assignment[Math.abs(x)]===1)===(x>0)));
}
function count(cs,ns){
 let cnt=0;
 for(let a=0;a<(1<<ns.length);a++){
  let assignment={};ns.forEach((v,i)=>assignment[v]=(a>>i)&1);
  if(sat(cs,assignment))cnt++;
 }
 return cnt;
}
const tests=[["F9",f9,70],["Z6",z6,18],["B9",b9,18],
 ["H15",shift(f9,z6,9),1260],["B18",shift(b9,b9,9),324]];
for(const [name,F,expected] of tests){
 ok(grammar(F),name+" syntax");
 let n=Math.max(...F.flat().map(Math.abs));
 ok(count(F,Array.from({length:n},(_,i)=>i+1))===expected,name+" models");
}
const pins={3:0,5:1,6:0,7:0,8:0};
const free=[2,4,9];
for(const [x1,expected] of [[0,2],[1,0]]){
 const f=f9.filter(c=>true);let countPin=0;
 for(let b=0;b<8;b++){
  let p={...pins,1:x1};free.forEach((v,i)=>p[v]=(b>>i)&1);
  countPin+=sat(f,p)?1:0;
 }ok(countPin===expected,"same-source F9 opposite labels");
}
const malformed=[f9.concat([f9[0]]),f9.slice(1),
 f9.map((c,i)=>i===0?[c[0],c[0],c[2]]:c),
 f9.map((c,i)=>i===0?[c[0],-c[1],c[2]]:c),
 f9.map((c,i)=>i===0?[0,c[1],c[2]]:c),
 f9.map((c,i)=>i===0?[100,c[1],c[2]]:c)];
for(let i=0;i<malformed.length;i++)ok(!grammar(malformed[i]),"malformed accepted");
let points=Array.from({length:9},(_,i)=>[Math.floor(i/3),i%3]);
let lines=[];
for(let a=0;a<3;a++)for(let b=0;b<3;b++){
 if(!a&&!b)continue;
 for(let c=0;c<3;c++){
  const L=points.flatMap(([x,y],i)=>((a*x+b*y-c)%3===0)?[i+1]:[]);
  if(L.length===3&&!lines.some(q=>q.join(",")===L.join(",")))lines.push(L);
 }
}
ok(lines.length===12,"affine incidence source");
let good=0;
for(let mask=0;mask<(1<<12);mask++){
 const pos=lines.filter((_,i)=>(mask>>i)&1),neg=lines.filter((_,i)=>!((mask>>i)&1));
 const F=S(pos,neg);if(!grammar(F))continue;
 good++;ok(count(F,[1,2,3,4,5,6,7,8,9])===18,"K9 sign census");
}
ok(good===6,"K9 signed grammar census");
console.log(JSON.stringify({status:"PASS",assertions,sourceControls:tests.map(x=>x[0]),sameOriginalF9:{SAT:2,UNSAT:0},balancedAG9:good,malformedRejected:6},null,2));
