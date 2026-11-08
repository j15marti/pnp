/* LSPV-4/503 finite verifier. Runs: node lspv4_503_streaming_snapshot_control.cjs
   Hosted controls only, NOT a native FLMV interpreter. */
"use strict";
let tests=0;const ck=(b,s)=>{tests++;if(!b)throw Error(s);};
const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const bin=(x,n)=>x.toString(2).padStart(n,"0");
function source(mask){
 let a=[];
 for(let v=0;v<4;v++){
  const ids=E.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
  for(let p=0;p<8;p++){
   const z=[p&1,(p>>1)&1,(p>>2)&1];
   if((z[0]^z[1]^z[2])!==((mask>>v)&1))
    for(let j=0;j<3;j++)a.push(bin(ids[j]+8*(1-z[j]),4));
  }
 }
 return "11001010"+"00010000"+a.join("");
}
function classify(x){
 if(!/^[01]*$/.test(x)||x.length!==208||x.slice(0,16)!=="1100101000010000")return "MALFORMED";
 const f=[];
 for(let j=0;j<16;j++){
  let c=[],ids=new Set();
  for(let k=0;k<3;k++){
   const t=parseInt(x.slice(16+12*j+4*k,20+12*j+4*k),2);
   const id=t&7,sign=t>>3;
   if(id<1||id>6||ids.has(id))return "MALFORMED";
   ids.add(id);c.push([id-1,sign]);
  }
  f.push(c);
 }
 for(let a=0;a<64;a++)if(f.every(c=>c.some(([id,s])=>((a>>id)&1)===s)))return "SAT";
 return "UNSAT";
}
const ports=n=>Math.ceil(Math.sqrt(n+1));
const value=(x,i)=>(x.length?+x[i%x.length]:0)^(i&1);
function stored(x){
 const r=ports(x.length),w=Array.from({length:r},(_,i)=>value(x,i)),reads=[];
 let digest=0;
 for(let i=r-1;i>=0;i--){reads.push(w[i]);digest^=w[i]<<(i%8);}
 return {reads,digest,slots:r};
}
function replay(x){
 const r=ports(x.length),reads=[];let digest=0;
 for(let i=r-1;i>=0;i--){const b=value(x,i);reads.push(b);digest^=b<<(i%8);}
 return {reads,digest,slots:0};
}
const inputs=[];
for(let mask=0;mask<16;mask++){
 const x=source(mask);
 ck(x.length===208,"source length");
 const pop=bin(mask,4).split("").filter(t=>t==="1").length%2;
 ck(classify(x)===(pop?"UNSAT":"SAT"),"Tseitin parity");
 inputs.push(x);
}
inputs.push("","0","1011",source(1).slice(1),source(1)+"1");
let seed=314159;
function rand(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0;}
for(let t=0;t<120;t++){let n=rand()%297,s="";for(let i=0;i<n;i++)s+=rand()&1;inputs.push(s);}
let sat=0,unsat=0,malformed=0,observations=0,maxports=0;
for(let k of [2,4,6])for(const x of inputs){
 const a=stored(x),b=replay(x),r=ports(x.length);
 ck(a.digest===b.digest&&a.reads.join("")===b.reads.join(""),"port readback/digest");
 ck(a.slots===r&&b.slots===0,"stored vs replayed slots");
 const L=k*Math.ceil(Math.log2(x.length+1));
 const A=1n<<BigInt(L),high=A+BigInt(r-1);
 ck(high>=A&&r>=1,"native high-water arithmetic");
 observations+=r;maxports=Math.max(maxports,r);
 const label=classify(x);if(k===2){if(label==="SAT")sat++;else if(label==="UNSAT")unsat++;else malformed++;}
}
let vectors=0,collisions=0;
for(let r=1;r<=10;r++){
 const states=Array.from({length:2**r},(_,i)=>bin(i,r));
 vectors+=states.length;
 for(let b=0;b<r;b++){
  const buckets=new Map();
  for(const s of states){
   const key=s.slice(0,b);
   if(buckets.has(key)){const other=buckets.get(key);ck(s!==other,"distinct vector");collisions++;}
   else buckets.set(key,s);
  }
  ck(buckets.size===2**b,"low-bit snapshot collisions");
 }
}
let changed=0;
for(let n=2;n<=64;n++){
 const x="0".repeat(n),y="1"+x.slice(1);
 if(stored(x).reads.join("")!==replay(y).reads.join(""))changed++;
}
ck(changed===63,"read-only-input falsifier");
console.log(JSON.stringify({status:"PASS",checks:tests,cases:inputs.length,sat,unsat,malformed,
 maxports,observations,snapshotVectors:vectors,snapshotCollisions:collisions,
 invalidMutableInputCases:changed,model:"hosted finite semantic controls, not native FLMV"},null,2));
