"use strict";
// Standalone V8/Node-compatible, exact function run in the GitHub-connector hosted V8 isolate.
const audit = function audit(){
 "use strict";
 const assert=(b,m)=>{if(!b)throw Error(m||"failed assertion")};
 function get(x,p){
  const L=x.length,q=L+1,w=Math.max(1,Math.ceil(Math.log2(L+2)));
  assert(p>=0&&p<=q);
  let addr=Array.from({length:w},(_,i)=>(Math.floor(p/2**i)%2));
  let down=addr.slice(),pop=down.reduce((a,v)=>a+v,0),head=0,charge=5*w,flips=0,largest=pop;
  // Scratch popcount is represented physically by the position of a unary work-tape head.
  while(pop>0){
   let t=0;
   while(down[t]===0){down[t]=1;t++;assert(t<w);charge+=3;}
   down[t]=0;charge+=2;charge+=t; // flip current one, return counter head to LSB
   pop+=t-1;charge+=t+1; // unary work-head: t moves right and one left
   head++;charge+=2; // input head moves one cell, unary zero/marker inspection
   flips+=t;
   largest=Math.max(largest,pop+1);
   assert(head<=q&&pop>=0&&pop<=w,"counter invariant");
  }
  charge+=head; // move physical input head back to the left endmarker
  const physicalRead=head===0?"L":head===q?"R":x[head-1];
  charge++; // read only current source-head position
  assert(head===p&&down.every(v=>v===0),"wrong countdown");
  assert(charge<=12*p+6*w+1,"linear charge bound");
  return {physicalRead,charge,w,flips,auxVisited:3*w+2};
 }
 const samples=[], readback=[];
 let cases=0,charges=0,flips=0,maxRatio=0,maxAux=0,maxP=0,valid=0;
 function test(x,p){
  const z=get(x,p), expected=p===0?"L":p===x.length+1?"R":x[p-1];
  assert(z.physicalRead===expected,"current-cell read mismatch");
  cases++;charges+=z.charge;flips+=z.flips;maxP=Math.max(maxP,p);
  maxAux=Math.max(maxAux,z.auxVisited);
  maxRatio=Math.max(maxRatio,z.charge/(x.length+2));
  if(x.length===24&&p===x.length)readback.push({x,p,symbol:z.physicalRead,charge:z.charge});
 }
 for(let L=0;L<=11;L++)for(let v=0;v<2**L;v++){
  let x=L?v.toString(2).padStart(L,"0"):"";
  for(let p=0;p<=L+1;p++)test(x,p);
 }
 for(let L of [15,24,25,31,32,63,64,127,128,255,256,511,512,1023,1024]){
  for(let j=0;j<5;j++){
   const x=Array.from({length:L},(_,i)=>((i*i+19*i+7*j)%13<6?"1":"0")).join("");
   for(let p of [...new Set([0,1,2,3,4,Math.floor(L/2),L,L+1])]) test(x,p);
  }
 }
 const properUnsat="000001010011100101110111", properSat="000001010011100101110110";
 for(const x of [properUnsat,properSat,"000".repeat(9)]){
  assert(x.length%3===0);
  const masks=new Set(Array.from({length:x.length/3},(_,i)=>x.slice(3*i,3*i+3)));
  const label=masks.size===8?"UNSAT":"SAT";
  assert(x===properUnsat?label==="UNSAT":label==="SAT");
  valid++;
  for(let p=0;p<=x.length+1;p++)test(x,p);
 }
 // Binary trailing-zero accounting independently of the physical scan.
 for(let p=0;p<=2048;p++){
  const z=get("0".repeat(p),p);
  let sum=0;for(let j=1;j<=p;j++){let k=j;while(k%2===0){sum++;k/=2;}}
  assert(z.flips===sum&&sum<=p,"amortized accounting");
 }
 return {status:"COMPUTATIONAL",claim:"One-input-head paid binary countdown with unary popcount-zero detection",sourceLengths:"all binary x length 0..11; five deterministic patterns at 15,24,25,31,32,63,64,127,128,255,256,511,512,1023,1024; SAT/UNSAT sign-stream controls",cases,chargedMicrosteps:charges,binaryCarryMovements:flips,maxTestedSourcePosition:maxP,maxAuxVisitedUpperBound:maxAux,maxChargePerSourceLength:maxRatio,properThreeVariableControls:valid,independentTrailingZeroChecks:2049,readback,assertionFailures:0,chargeBound:"C_fetch(p,w)<=12p+6w+1",scope:"locally moving one-source-head lookup, not a compiled arbitrary 3SAT TM"};
};
console.log(JSON.stringify(audit(),null,2));
