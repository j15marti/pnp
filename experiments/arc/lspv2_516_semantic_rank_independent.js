#!/usr/bin/env node
'use strict';
// Independent finite checker, not native FLMV or historical R_mix341.
const crypto = require('crypto');
const edges = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function source(k,d) {
  let next=7, cls=[], controls=[];
  function alloc(){return next++;}
  for(let j=0;j<k;j++){
    const p=alloc(),u=alloc(),v=alloc();controls.push(p);
    const sig=(d&(1<<j))?p:-p;
    cls.push([sig,u,v],[sig,u,-v],[sig,-u,v],[sig,-u,-v]);
  }
  let g=controls[0];
  for(let j=1;j<k;j++){
    const z=alloc(),u=alloc(),v=alloc(),x=controls[j];
    cls.push([-g,z,u],[-g,z,-u],[-x,z,v],[-x,z,-v],[g,x,-z]);g=z;
  }
  for(let vertex=0;vertex<4;vertex++){
    const e=edges.map((x,i)=>x.includes(vertex)?i+1:0).filter(x=>x);
    for(let mask=0;mask<8;mask++){
      const parity=(((mask>>2)&1)+((mask>>1)&1)+(mask&1))%2;
      if(parity=== (vertex===0?1:0))continue;
      const base=e.map((id,j)=>(mask&(1<<(2-j)))?-id:id);
      const h=alloc();cls.push([g,base[0],h],[-h,base[1],base[2]]);
    }
  }
  return {cls,n:next-1};
}
function bitstring(f) {
 const w=Math.floor(Math.log2(f.n))+1;
 const bits=f.cls.map(c=>c.map(x=>Math.abs(x).toString(2).padStart(w,'0')+(x<0?'1':'0')).join('')).join('');
 return '10110110'+'1'.repeat(f.n)+'0'+bits+'01';
}
function isSat(clauses){
 let count=0;
 function visit(cnf){
   count++;
   while(true){
     if(cnf.length===0)return true;
     if(cnf.some(c=>c.length===0))return false;
     let unit=cnf.find(c=>c.length===1);
     if(!unit)break;
     const lit=unit[0];cnf=cnf.filter(c=>!c.includes(lit)).map(c=>c.filter(t=>t!==-lit));
   }
   const freq=new Map();
   cnf.forEach(c=>c.forEach(l=>freq.set(Math.abs(l),(freq.get(Math.abs(l))||0)+1)));
   let pivot=Array.from(freq).sort((a,b)=>b[1]-a[1] || a[0]-b[0])[0][0];
   for(const lit of [pivot,-pivot]){
     const child=cnf.filter(c=>!c.includes(lit)).map(c=>c.filter(v=>v!==-lit));
     if(visit(child))return true;
   }
   return false;
 }
 return [visit(clauses),count];
}
function rank(rows){let basis=new Map();for(let n of rows){while(n){const pivot=31-Math.clz32(n);if(!basis.has(pivot)){basis.set(pivot,n);break;}n^=basis.get(pivot);}}return basis.size;}
let passes=0, records=[];
for(let k=1;k<=7;k++){
 const seq=[], lab=[];let maxNodes=0;
 for(let d=0;d<(1<<k);d++){
   const f=source(k,d), s=bitstring(f);seq.push(s);
   if(f.cls.some(c=>new Set(c.map(x=>Math.abs(x))).size!==3))throw Error('Nonproper clause');
   const [sat,nodes]=isSat(f.cls);lab.push(sat); maxNodes=Math.max(maxNodes,nodes);
   if(sat!== (d!==0))throw Error('Wrong classification '+k+':'+d);
   passes+=3;
 }
 const anchor=seq[0], masks=Array.from({length:anchor.length},()=>0);
 for(let j=0;j<k;j++){
   const changed=[];for(let pos=0;pos<anchor.length;pos++)if(anchor[pos]!==seq[1<<j][pos]){changed.push(pos);masks[pos]|=(1<<j);}
   if(changed.length!==4)throw Error('Unexpected signed pin field count');passes++;
 }
 if(rank(masks)!==k)throw Error('Rank mismatch');passes++;
 for(let d=0;d<(1<<k);d++)for(let pos=0;pos<anchor.length;pos++){
    const computed=anchor[pos]==='1'?1:0;
    const parity=(masks[pos]&d).toString(2).split('1').length%2===0?1:0;
    const actual=seq[d][pos]==='1'?1:0;
    if((computed^parity)!==actual)throw Error('Not an affine byte family '+k+','+d+','+pos);
 }
 passes+=(1<<k);
 if(lab.filter(x=>!x).length!==1)throw Error('Failed uniqueness');passes++;
 records.push({k,children:1<<k,unsat:1,sat:(1<<k)-1,rank:k,sha256:crypto.createHash('sha256').update(anchor).digest('hex'),bits:anchor.length,maxDpllNodes:maxNodes});
}
console.log(JSON.stringify({status:'PASS',assertion_groups:passes,records,scope:'independent JS strict-3CNF DPLL classifications and affine bit-signature checks'},null,2));
