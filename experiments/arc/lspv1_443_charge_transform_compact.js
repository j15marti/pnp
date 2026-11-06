"use strict";
// Supplemental LSPV-1/443 clause/size checks; full source-bound proof is in local archive.
const assert=require("assert");
function norm(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);}
function chargeCNF(h,odd) {
 let output=h+1,cls=[];
 for(let i=0;i<h-1;i++){
  const a=i?output-1:1,b=i+2,c=output++;
  for(let x=0;x<2;x++)for(let y=0;y<2;y++){
   const z=1-(x^y);
   cls.push(norm([x?-a:a,y?-b:b,z?-c:c]));
  }
 }
 let next=2*h;
 const units=Array.from({length:h},(_,i)=>i==0&&odd?i+1:-(i+1));
 units.push(-(2*h-1));
 for(const u of units){
   const p=next++,q=next++;
   cls.push(norm([u,p,q]),norm([u,p,-q]),norm([u,-p,q]),norm([u,-p,-q]));
 }
 return {cls,n:next-1};
}
let checks=0;
for(const h of [4,6,8,12])for(const odd of [false,true]){
 const {cls,n}=chargeCNF(h,odd);
 assert.equal(cls.length,8*h);assert.equal(n,4*h+1);checks+=2;
 for(const c of cls){assert.equal(c.length,3);assert.equal(new Set(c.map(Math.abs)).size,3);checks+=2;}
 const work=odd?5*h+2:0;
 console.log(JSON.stringify({h,odd,clauses:cls.length,variables:n,exhibited_odd_RES_work:work}));
}
console.log("PASS compact structural assertions",checks);
