#!/usr/bin/env node
'use strict';
// Compact source-authenticated LSPV-3/473 finite control, self-contained.
// Independent full Python ANF and Node truth-table replay in reproducibility archive.
// NOT an authoritative historical R_mix341 checker.
const assert=require('assert');
const cases=[
  [3,[[1,2,3]]],
  [5,[[1,-2,3],[-2,4,5]]],
  [7,[[1,-2,3],[2,4,-5],[-3,5,6],[-1,-6,7]]],
  [8,[[1,-2,3],[2,4,-5],[-3,5,6],[-1,-6,7],[1,-4,8]]]
];
let checks=0;const ok=(v,m)=>{checks++;assert.ok(v,m)};
function sat(a,clauses){return clauses.every(c=>c.some(l=>((a>>(Math.abs(l)-1))&1)===Number(l>0)))}
function popc(x){let k=0;while(x){x&=x-1;k++}return k}
function anf(v,n){v=v.slice();for(let j=0;j<n;j++)for(let a=0;a<(1<<n);a++)if(a&(1<<j))v[a]^=v[a^(1<<j)];
return v.flatMap((x,i)=>x?[i]:[])}
function rank(rows){const b=new Map();let r=0;for(let v of rows){while(v){const h=v.toString(2).length-1;if(b.has(h))v^=b.get(h);else{b.set(h,v);r++;break}}}return r}
function peel(C){let r=C.map(c=>c.slice());while(r.length){let d=new Map();for(const c of r)for(const l of c)d.set(Math.abs(l),(d.get(Math.abs(l))||0)+1);
const i=r.findIndex(c=>c.some(l=>d.get(Math.abs(l))===1));if(i<0)return false;r.splice(i,1)}return true}
for(const [n,C] of cases){
 ok(peel(C),'peel');const M=Array.from({length:1<<n},(_,i)=>i).filter(a=>sat(a,C));
 ok(M.length>0,'models');
 const mon=Array.from({length:1<<n},(_,i)=>i).filter(i=>popc(i)<3);
 const rows=M.map(a=>mon.reduce((v,m,j)=>v|(((a&m)===m)?1n<<BigInt(j):0n),0n));
 ok(rank(rows)===mon.length,'full rank degree<=2');
 for(const m of mon){const v=Array.from({length:1<<n},(_,a)=>Number((a&m)===m));
 if(m!==0)ok(anf(v,n).includes(m),'Mobius monomial');}
 // Branch guards for one or two original variables, all polarity choices.
 const atoms=[];for(let i=0;i<n;i++)for(const bit of [0,1])atoms.push([i,bit]);
 for(const [i,a] of atoms){const guard=x=>Number(((x>>i)&1)===a);
 ok(M.some(x=>guard(x)),'single branch still SAT');
 for(const [j,b] of atoms)if(j>i){const G=x=>guard(x)&&(((x>>j)&1)===b);
 ok(M.some(x=>G(x)),'double branch still SAT')}
 }
}
const C=[[1,2,3]],bad=a=>Number(((a&7)===0));
ok(Array.from({length:8},(_,a)=>a).filter(a=>sat(a,C)).every(a=>!bad(a)),'degree3 boundary');
ok(anf(Array.from({length:8},(_,a)=>bad(a)),3).some(m=>popc(m)===3),'guard degree3');
const count=checks;let corruptRejected=0;
for(const dirty of [[[1,1,3]],[[1,2,0]],[[1,2,2]]]){try{ok(dirty.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3&&c.every(x=>x!==0)),'malformed source')}catch(_){corruptRejected++}}
ok(corruptRejected===3,'negative controls');
console.log(JSON.stringify({status:'PASS',checks,corruptRejected,scope:'finite peelable source and original-variable 1/2-literal context controls; not native R_mix341'}));
