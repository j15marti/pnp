#!/usr/bin/env node
'use strict';
// Fixed-source ER2: paid signed AND2 definitions, strict binary resolution.
// Independent theorem/label/normalization controls. No external packages.
const norm=a=>{const b=[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);if(b.some(x=>b.includes(-x)))throw Error('tautology');return b};
let checks=0;function yes(v){checks++;if(!v)throw Error('failed check '+checks)}
const eq=(a,b)=>JSON.stringify(norm(a))===JSON.stringify(norm(b));
function res(A,B,p){yes(A.includes(p)&&B.includes(-p));return norm(A.filter(x=>x!==p).concat(B.filter(x=>x!==-p)))}
function sat(F,m){return F.every(C=>C.some(x=>(!!(m&(1<<(Math.abs(x)-1))))===(x>0)))}
function nmodels(F,n){let t=0;for(let i=0;i<2**n;i++)t+=sat(F,i)?1:0;return t}
let cases=0,un=0,sa=0,projection=0,forwardNodes=0,reverseNodes=0;
for(let k=4;k<=8;k++)for(let pol=0;pol<=1;pol++)for(const label of ['SAT','UNSAT']){
 const C=Array.from({length:k},(_,j)=>(pol&&(j+1)%2===0)?-(j+1):j+1);
 const F=[C,...C.slice(0,label==='SAT'?-1:undefined).map(x=>[-x])];
 const g={};let fresh=k;
 for(let i=k-2;i>=2;i--){const a=-C[i],b=i===k-2?-C[i+1]:g[i+1].q,q=++fresh;
   g[i]={q,a,b,slots:[norm([-q,a]),norm([-q,b]),norm([q,-a,-b])]};
 }
 let top=C.slice();for(let i=k-2;i>=2;i--){
   top=res(top,g[i].slots[0],C[i]);
   top=res(top,g[i].slots[1],i===k-2?C[i+1]:-g[i+1].q);
 }
 yes(eq(top,[C[0],C[1],-g[2].q]));
 const split=[top,...Array.from({length:k-3},(_,j)=>g[j+2].slots[2])];
 let rec=split[0];for(let i=1;i<split.length;i++)rec=res(rec,split[i],-g[i+1].q);
 yes(eq(rec,C));
 const G=[...split,...F.slice(1)];
 const m=nmodels(F,k),m3=nmodels(G,fresh);
 yes((m===0)===(label==='UNSAT'));yes((m3===0)===(label==='UNSAT'));
 if(k<=6)for(let a=0;a<2**k;a++){
   let exists=false;for(let z=0;z<2**(k-3);z++)exists ||=sat(G,a+(z<<k));
   yes(exists===sat(F,a));projection++;
 }
 forwardNodes+=3*(k-3);reverseNodes+=k-3;cases++;
 if(label==='SAT')sa++;else un++;
}
yes(new Set([3,4,5]).size===3);
for(const bad of ['p cnf 2 1\n3 0','p cnf 2 1\n1 0\n2 0','p cnf 2 1\n0 0','p cnf x 1\n1 0']){
 function parse(s){
   const t=s.split(/\s+/).filter(Boolean);
   if(t[0]!=='p'||t[1]!=='cnf')throw Error('header');
   const n=Number(t[2]),m=Number(t[3]);
   if(!Number.isInteger(n)||n<0||!Number.isInteger(m)||m<0)throw Error('count');
   let c=0,cur=0;
   for(const v of t.slice(4)){
     if(!/^[-]?\d+$/.test(v))throw Error('token');
     const a=Number(v);
     if(a===0){c++;cur=0}else{if(Math.abs(a)>n)throw Error('range');cur++}
   }
   if(c!==m||cur)throw Error('shape');
 }
 let rejected=false;try{parse(bad)}catch(_){rejected=true}yes(rejected);
}
console.log(JSON.stringify({run:'LSPV4_ER2_NORMALIZATION368_COMPACT',status:'PASS',checks,cases,SAT:sa,UNSAT:un,projection,forwardNodes,reverseNodes,full_mixed_backtranslation:'OPEN',B1:'OPEN',B2:'OPEN',B3:'OPEN'}));
