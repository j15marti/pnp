#!/usr/bin/env node
// LSPV-4/422: independent no-package finite control. Not a physical FLMV machine.
let assertions=0;
const verify=(p,msg)=>{assertions++;if(!p)throw Error(msg)};
function tseitin(which,odd){
 const h=which==='K4'?4:8;
 const edges=which==='K4'?Array.from({length:4},(_,i)=>Array.from({length:3-i},(_,j)=>[i,i+j+1])).flat():Array.from({length:8},(_,i)=>Array.from({length:3},(_,j)=>[i,i^(1<<j)]).filter(([a,b])=>a<b)).flat();
 const near=Array.from({length:h},()=>[]);
 edges.forEach(([a,b],i)=>{near[a].push(i+1);near[b].push(i+1)});
 const clauses=[];
 for(let j=0;j<h;j++){
  verify(near[j].length===3,'cubic graph');
  for(let mask=0;mask<8;mask++){
    if((((mask&1)+((mask>>1)&1)+((mask>>2)&1))&1)===(j===0&&odd?1:0))continue;
    clauses.push(near[j].map((e,k)=>mask&(1<<k)?-e:e));
  }
 }
 return {v:edges.length,clauses,h};
}
const lit=(l,x)=>l>0?Boolean(x&(1<<(l-1))):!Boolean(x&(1<<(-l-1)));
const sat=(formula,x)=>formula.every(cl=>cl.some(l=>lit(l,x)));
function guardBranch(formula,x,z){
 return formula.every(([a,b,c])=>[false,true].some(y=>(z||lit(a,x)||y)&&(!y||lit(b,x)||lit(c,x))));
}
function validCNF(cs,v){return Array.isArray(cs)&&cs.length>0&&cs.every(row=>row.length===3&&row.every(n=>Number.isSafeInteger(n)&&n!==0&&Math.abs(n)<=v)&&new Set(row.map(Math.abs)).size===3)}
const output=[];
for(let which of ['K4','cube'])for(let odd of [false,true]){
 const {v,clauses,h}=tseitin(which,odd);
 verify(clauses.length===4*h,'width3 source count');verify(validCNF(clauses,v),'source grammar');
 let count=0,zero=false,one=false;
 for(let x=0;x<2**v;x++){
  const q=sat(clauses,x),b0=guardBranch(clauses,x,false),b1=guardBranch(clauses,x,true);
  verify(q===b0,'z=0 must project to F');verify(b1,'z=1 must be SAT for all x');
  if(q)count++;zero ||= b0;one ||= b1;
 }
 verify(zero===(!odd),'odd/even SAT control');verify(one,'parent SAT via branch1');
 verify((zero===one)===zero,'equality is SAT label');
 output.push({graph:which,odd,variables:v,clauses:clauses.length,models:count,labels:[zero,one]});
}
verify(!validCNF([[1,1,2]],3),'duplicate malformed rejected');
verify(!validCNF([[1,2,0]],3),'zero ID malformed rejected');
verify(!validCNF([[1,2,4]],3),'out-of-range malformed rejected');
console.log(JSON.stringify({passed:true,assertions,output},null,2));
