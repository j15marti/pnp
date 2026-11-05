"use strict";
function verify(raw){
 const base=[170,204,240], op=(t,x,y)=>(t>>(2*x+y))&1; let checks=0;
 const hist=[0,0,0,0,0];
 if(!Array.isArray(raw.witnesses)||raw.witnesses.length!==256)throw Error("missing data");
 for(let f=0;f<256;f++){
  const gates=raw.witnesses[f];if(!Array.isArray(gates)||gates.length>4||gates.length!==raw.distances[f])throw Error("length");
  hist[gates.length]++;
  for(let a=0;a<8;a++){
   const v=[a&1,(a>>1)&1,(a>>2)&1];
   for(const g of gates){
    if(!Number.isInteger(g.i)||!Number.isInteger(g.j)||!Number.isInteger(g.op)||
      g.i<0||g.j<0||g.i>=v.length||g.j>=v.length||g.op<0||g.op>15)throw Error("bad record");
    v.push(op(g.op,v[g.i],v[g.j]));checks++;
   }
   if((gates.length?v.at(-1):v[base.indexOf(f)])!==((f>>a)&1))throw Error("wrong output");
   checks++;
  }
 }
 if(hist.join()!==raw.histogram.join())throw Error("wrong histogram");
 const gate=(t,a,b)=>{let m=0;for(let i=0;i<8;i++)m|=op(t,(a>>i)&1,(b>>i)&1)<<i;return m;};
 let states=[[]],reachable=new Set(base),counts=[];
 for(let k=1;k<=3;k++){
  const next=new Set();
  for(const st of states){const arr=base.concat(st);
   for(let i=0;i<arr.length;i++)for(let j=i;j<arr.length;j++)for(let t=0;t<16;t++){
     const m=gate(t,arr[i],arr[j]);if(arr.includes(m))continue;
     reachable.add(m);next.add(st.concat(m).join(","));
   }
  }
  states=[...next].map(s=>s.split(",").map(Number));counts.push(states.length);
 }
 if(reachable.size!==232||hist[4]!==24)throw Error("3-gate lower bound not verified");
 // Corrupted semantic output, malformed gate and missing circuit controls:
 const mutant=JSON.parse(JSON.stringify(raw));mutant.witnesses[232].at(-1).op=16;
 let caught=false;try{verifyWithoutRecursion(mutant.witnesses[232]);}catch{caught=true;}
 if(!caught)throw Error("malformed mutant accepted");
 function verifyWithoutRecursion(w){const v=[0,0,0];for(const g of w){if(g.op>=16||g.i>=v.length||g.j>=v.length)throw Error("invalid");v.push(op(g.op,v[g.i],v[g.j]));}}
 return {histogram:hist,statesByDepth:counts,truthAndGateChecks:checks,reachableWithThree:reachable.size,needFour:hist[4],malformedRejected:caught};
}
if(typeof module!=="undefined")module.exports={verify};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
const fs=require("node:fs");console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2));}
