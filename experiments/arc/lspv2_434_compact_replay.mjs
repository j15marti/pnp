#!/usr/bin/env node
// Compact semantic verifier only. The full bit-grammar parser, original raw
// sources and independent checker are in the LSPV-2/434 reproducibility archive.
import assert from 'node:assert/strict';
let checks=0;
function ok(b){checks++;assert.equal(Boolean(b),true);}
function makeEdges(name){
 if(name==='K4')return [4,Array.from({length:4},(_,i)=>Array.from({length:4-i-1},(_,j)=>[i,i+j+1])).flat()];
 if(name==='cube'){let a=[];for(let i=0;i<8;i++)for(let j=i+1;j<8;j++)if(((i^j).toString(2).match(/1/g)||[]).length===1)a.push([i,j]);return [8,a];}
 let e=[];for(let i=0;i<5;i++)e.push([i,(i+1)%5],[i,i+5],[i+5,5+(i+2)%5]);return [10,e];
}
function ts(name,odd){const [n,edges]=makeEdges(name),C=[];
 for(let v=0;v<n;v++){
  const at=edges.flatMap(([u,w],i)=>u===v||w===v?[i+1]:[]);
  ok(at.length===3);
  for(let q=0;q<8;q++){
   const a=[q&1,(q>>1)&1,(q>>2)&1];
   if((a[0]^a[1]^a[2])!==(odd&&v===0?1:0))C.push(at.map((id,i)=>({id,neg:Boolean(a[i])})));
  }
 }
 return {C,m:edges.length,n};
}
const h=id=>id.toString(2).length%2===1;
const lit=(id,neg)=>({id,neg});
const tail=[
 [lit(257,false),lit(1,false),lit(2,true)],
 [lit(513,true),lit(1,true),lit(3,false)],
 [lit(257,true),lit(513,false),lit(521,true)],
 [lit(259,false),lit(513,true),lit(4,false)]
];
function typed(T,b=8){return T.every(c=>c.length===3&&new Set(c.map(z=>z.id)).size===3&&c.some(z=>z.id.toString(2).length>b&&(h(z.id)!==z.neg)));}
function val(c,a){return c.some(z=>(z.id>255?h(z.id):a[z.id-1])!==z.neg);}
let cases=0;
for(const name of ['K4','cube','Petersen'])for(const odd of [false,true]){
 const {C,m,n}=ts(name,odd);ok(C.length===4*n);ok(m===3*n/2);ok(typed(tail));
 let satisfiable=false;
 for(let mask=0;mask<(1<<m);mask++){
  const a=Array.from({length:m},(_,i)=>Boolean(mask&(1<<i)));
  const core=C.every(c=>val(c,a));
  const joined=core&&tail.every(c=>val(c,a));
  ok(core===joined);if(core)satisfiable=true;
 }
 ok(satisfiable===!odd);cases++;
}
ok(!typed([[lit(257,true),lit(1,false),lit(2,true)]]));
ok(!typed([[lit(257,false),lit(257,true),lit(2,true)]]));
ok(!typed([[lit(1,false),lit(2,true),lit(3,false)]]));
console.log(JSON.stringify({status:'PASS',cases,checks}));
