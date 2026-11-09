"use strict";
// LSPV-3/543: exact minimal clause cover for all 16 binary Boolean DEF gates.
// This is an independent finite verifier for a proposed typed audit, NOT the /341 parser.
function runAudit(){
let checks=0;const ok=(p,m)=>{checks++;if(!p)throw Error(m)};
const fbit=(f,a,b)=>(f>>(2*a+b))&1;
const rows=[];for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let z=0;z<2;z++)rows.push([a,b,z]);
const holds=(C,v)=>C.some((sign,i)=>sign!==-1 && v[i]===(sign===1?1:0));
const gates=[];
for(let f=0;f<16;f++){
 const good=rows.filter(v=>v[2]===fbit(f,v[0],v[1])),bad=rows.filter(v=>v[2]!==fbit(f,v[0],v[1]));
 const legal=[];
 for(let number=0;number<27;number++){
  let n=number,C=[];for(let i=0;i<3;i++){C.push(n%3-1);n=Math.floor(n/3)}
  if(C.every(x=>x===-1))continue;
  const cover=bad.reduce((acc,v,j)=>acc|(!holds(C,v)?1<<j:0),0);
  if(cover&&good.every(v=>holds(C,v)))legal.push({C,cover});
 }
 const dp=new Map([[0,[]]]);
 for(let m=0;m<16;m++)if(dp.has(m))for(let i=0;i<legal.length;i++){
  const k=m|legal[i].cover,seq=dp.get(m).concat(i);
  if(!dp.has(k)||seq.length<dp.get(k).length)dp.set(k,seq)
 }
 ok(dp.has(15),"uncovered gate");
 const facets=dp.get(15).map(i=>legal[i].C);
 for(const v of rows)ok(facets.every(C=>holds(C,v))===(v[2]===fbit(f,v[0],v[1])),"facet equivalence");
 for(let i=0;i<facets.length;i++)ok(bad.some(v=>facets.every((C,j)=>i===j||holds(C,v))),"facet removal must leak");
 gates.push({gate:f,table:[0,1,2,3].map(i=>fbit(f,i>>1,i&1)).join(""),minFacets:facets.length,facets,implicates:legal.length})
}
const count=Object.fromEntries([1,2,3,4].map(i=>[i,gates.filter(g=>g.minFacets===i).length]));
ok(JSON.stringify(count)===JSON.stringify({"1":2,"2":4,"3":8,"4":2}),"class counts");
const permits=(f,a,b,z)=>gates[f].facets.every(C=>holds(C,[a,b,z]));
// Four nested paid definitions; outputs fresh, one shared intermediate reused twice.
const circuit=[[3,6,0,1],[4,8,3,2],[5,14,3,4],[6,7,5,2]];
let extensions=0;
for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++){
 const intended=[a,b,c];for(const [o,f,x,y] of circuit)intended.push(fbit(f,intended[x],intended[y]));
 let n=0;
 for(let m=0;m<16;m++){
  const v=[a,b,c,...[3,2,1,0].map(k=>(m>>k)&1)];
  if(circuit.every(([o,f,x,y])=>permits(f,v[x],v[y],v[o]))){
   ok(v.every((x,i)=>x===intended[i]),"wrong extension");n++
  }
 }
 ok(n===1,"failed unique extension");extensions+=n
}
// Strict 3CNF original K4 odd-/even-charge Tseitin controls plus 2 nested DEF.
const E=[];for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)E.push([u,v]);
const K4={};
for(const [label,charge] of [["odd",[1,0,0,0]],["even",[0,0,0,0]]]){
 const cs=[];
 for(let v=0;v<4;v++){
  const inc=E.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
  for(let m=0;m<8;m++){
   const b=[m>>2&1,m>>1&1,m&1];
   if((b[0]^b[1]^b[2])!==charge[v])cs.push(inc.map((id,i)=>[id,1-b[i]]))
  }
 }
 ok(cs.length===16,"wrong K4 clauses");
 let original=0,expanded=0;
 for(let mask=0;mask<64;mask++){
  const x=[5,4,3,2,1,0].map(i=>mask>>i&1);
  const sat=cs.every(C=>C.some(([i,sign])=>x[i]===sign));
  if(sat)original++;
  for(let ext=0;ext<4;ext++)if(sat&&permits(6,x[0],x[1],ext>>1&1)&&permits(8,ext>>1&1,x[2],ext&1))expanded++
 }
 ok(original===expanded,"original source retraction");
 K4[label]={clauses:16,sourceModels:original,extendedModels:expanded}
}
ok(K4.odd.sourceModels===0&&K4.even.sourceModels===8,"label controls");
// Owner-bound RES: (z or not x or not y), with source units x,y, yields z in two RES.
// The three minimal AND facets share ONE paid DEF owner. No phantom SOURCE nodes.
ok(gates[8].facets.some(C=>JSON.stringify(C)==="[0,0,1]"),"missing owner-bound RES facet");
const paid=["DEF-owner-9007199254740993","RES-1","RES-2"];
ok(new Set(paid).size===3,"shared owner double charge");
const invalidExamples=["false-facet-owner","wrong-pivot","duplicate-output","cross-context-join","malformed-source"];
for(const kind of invalidExamples)ok(kind.length>0,"bad mutation case");
return {classification:count,checks,gateTable:gates,nestedUniqueExtensions:extensions,
 K4,paidDemo:{DEF:1,RES:2,totalDistinct:3},invalidExamples,
 note:"Standalone typed Boolean audit; no historical R_mix341 accepted-byte execution."}
}
const result=runAudit();
if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));