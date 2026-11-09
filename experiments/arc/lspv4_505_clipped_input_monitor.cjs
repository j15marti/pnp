"use strict";
// LSPV-4/505 independent hosted controls. Not a native FLMV interpreter.
function assert(v,m){if(!v)throw Error(m||"assertion");}
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function source(charges){
 const clauses=[];
 for(let v=0;v<4;v++){
  const es=edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
  for(let b=0;b<8;b++){const bs=[b&1,(b>>1)&1,(b>>2)&1];
   if(((bs[0]+bs[1]+bs[2])&1)===charges[v])continue;
   clauses.push(bs.map((z,i)=>z?-(es[i]+1):es[i]+1));
  }
 }
 const t="K4:"+clauses.map(c=>c.join(",")).join(";")+";";
 return {clauses,text:t,bits:t.split("").flatMap(c=>Array.from({length:8},(_,i)=>(c.charCodeAt(0)>>(7-i))&1))};
}
function sat(clauses){for(let a=0;a<64;a++){if(clauses.every(c=>c.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0))))return true}return false}
function monitor(bits,events){
 const n=bits.length, B=Math.floor(Math.log2(2*n))+1;
 let real=1n, near=1, far=false, lo=0,hi=0, idx=new Map();
 let scans=0, scanSteps=0, inputMoves=0, checked=0, worstHead=1n;
 let farLeft=0, reads=new Set(), indexWrites=0;
 function observe(){
  checked++;if(real>worstHead)worstHead=real;
  const x=real>=1n&&real<=BigInt(n)?bits[Number(real)-1]:null;
  if(far&&x!==null){const p=Number(real);assert(farLeft>=n,"unamortized recovery");
   scans++;scanSteps+=2*p;near=p;far=false;
  }
  const y=far?null:(near>=1&&near<=n?bits[near-1]:null);
  assert(x===y,"observations differ");
  if(x!==null){assert(!far&&near===Number(real));reads.add(near)}
 }
 for(const e of events){
  if(e[0]==="W"){const k=e[1],bit=e[2],old=idx.get(k)||0;
    if(k>=B)hi+=bit-old;else lo+=(bit-old)*2**k;
    if(bit)idx.set(k,bit);else idx.delete(k);indexWrites++;
  }else if(e[0]==="J"){
    real=[...idx].reduce((s,[k,b])=>s+(BigInt(b)<<BigInt(k)),0n);
    const v=hi>0?2*n+1:lo;far=v>2*n;near=far?null:v;
    idx.clear();lo=0;hi=0;farLeft=0;
  }else{
    const d=e[0];assert(["L","R","S"].includes(d));
    if(d==="L"&&real>0n)real--;if(d==="R")real++;
    if(d!=="S")inputMoves++;
    if(far){if(d==="L")farLeft++;}
    else{
      if(d==="L")near=Math.max(0,near-1);
      if(d==="R")near++;
      if(near>2*n){far=true;near=null;farLeft=0;}
    }
  }
  observe();assert(hi>=0);
 }
 assert(scanSteps<=2*inputMoves+2*n,"amortized scan bound");
 return {n,reads:reads.size,scans,scanSteps,inputMoves,indexWrites,checked,headBits:worstHead.toString(2).length};
}
let summary={status:"PASS",sources:0,sat:0,unsat:0,malformed:0,cases:0,guest_steps:0,input_moves:0,index_writes:0,scans:0,scan_transitions:0,max_head_bits:0,max_read_mask_address:0,samples:[]};
for(let charge=0;charge<16;charge++){
 const ch=Array.from({length:4},(_,i)=>(charge>>i)&1),s=source(ch);
 const truth=sat(s.clauses),want=(ch.reduce((a,b)=>a+b,0)&1)===0;
 assert(truth===want,"Tseitin charge label");summary.sources++;if(truth)summary.sat++;else summary.unsat++;
 for(let mode=0;mode<4;mode++){
   const events=[],n=s.bits.length;
   function jump(a){for(let k=0;k<a.toString(2).length;k++)events.push(["W",k,Number((a>>BigInt(k))&1n)]);events.push(["J"])}
   if(mode===0){jump(BigInt(2*n+5));for(let i=0;i<n+7;i++)events.push(["L"])}
   if(mode===1){jump(1n<<BigInt(67+charge));for(let i=0;i<n+5;i++)events.push(["L"])}
   if(mode===2){jump(BigInt(n>>1));for(let i=0;i<n+10;i++)events.push(["R"])}
   if(mode===3){jump(BigInt(n-1));for(let i=0;i<2*n+11;i++)events.push([i%3===0?"L":i%3===1?"R":"S"])}
   const q=monitor(s.bits,events);summary.cases++;summary.guest_steps+=q.checked;
   summary.input_moves+=q.inputMoves;summary.index_writes+=q.indexWrites;
   summary.scans+=q.scans;summary.scan_transitions+=q.scanSteps;
   summary.max_head_bits=Math.max(summary.max_head_bits,q.headBits);
   summary.max_read_mask_address=Math.max(summary.max_read_mask_address,q.n);
   if(charge===0)summary.samples.push({mode,...q});
 }
}
const validSources=new Set();
for(let charge=0;charge<16;charge++)validSources.add(source(Array.from({length:4},(_,i)=>(charge>>i)&1)).text);
for(const bad of ["","K4?","not a formula","K4:1,2,3;","K4:0,0,0;"]){
 assert(!validSources.has(bad),"malformed source accepted");
 const bits=bad.split("").flatMap(c=>Array.from({length:8},(_,i)=>(c.charCodeAt(0)>>(7-i))&1));
 const q=monitor(bits,Array.from({length:bits.length+2},(_,i)=>[i&1?"S":"R"]));
 assert(q.n===bits.length);summary.malformed++;
}
assert(summary.malformed===5);
globalThis.LSPV4_505_RESULT=summary;
if(typeof module!=="undefined"&&module.exports)module.exports=summary;
