#!/usr/bin/env node
// LSPV-4/390. Deterministic, no dependencies, no random seed.
// Full symbolic argument in role report. Exact finite controls only.
"use strict";
let checks=0;
const ok=(v,msg)=>{checks++;if(!v)throw Error(msg)};
function src(bits,N) {
 let Q=bits.length,s="p cnf "+Q+" "+2*Q+"\n";
 for(let i=0;i<Q;i++)s+="+"+(i+1)+" 0\n"+(bits[i]?"+":"-")+(i+1)+" 0\n";
 if(N!==undefined){let d=N-s.length;if(d<0||d===1||d===2)throw Error("bad padding");
 if(d>0)s+="c "+"P".repeat(d-3)+"\n";}
 return s;
}
function parse(s) {
 if(typeof s!=="string")throw Error("not text");
 const lines=s.split("\n"); if(lines.pop()!=="")throw Error("no newline");
 let h=lines.shift().split(" ");
 if(h.length!==4||h[0]!=="p"||h[1]!=="cnf"||!/^[0-9]+$/.test(h[2])||!/^[0-9]+$/.test(h[3]))throw Error("header");
 let Q=Number(h[2]);if(Q<1||Number(h[3])!==2*Q)throw Error("count");
 let b=[];for(let i=1;i<=Q;i++){
 if(lines.shift()!=="+"+i+" 0")throw Error("source 1");
 let v=lines.shift();if(v!=="+"+i+" 0"&&v!=="-"+i+" 0")throw Error("source 2");
 b.push(Number(v[0]==="+"));
 }
 if(lines.length&&(lines.length!==1||!/^c P+$/.test(lines[0])))throw Error("trailing");
 return b;
}
function cnfModelCount(bits) {
 const Q=bits.length;let count=0;
 for(let a=0;a<2**Q;a++)if(bits.every((b,i)=>((a>>i)&1)&&b))count++;
 return count;
}
let parents=0,children=0;
for(let Q=1;Q<=8;Q++)for(let mask=0;mask<2**Q;mask++){
 let b=Array.from({length:Q},(_,i)=>(mask>>i)&1),input=src(b);
 ok(JSON.stringify(parse(input))===JSON.stringify(b),"parse");
 ok((cnfModelCount(b)>0)===b.every(Boolean),"parent");
 for(let i=0;i<Q;i++){
  let child=src([b[i]]);
  ok(parse(child)[0]===b[i],"child");
  ok(cnfModelCount([b[i]])===b[i],"child label");
  children++;
 }
 parents++;
}
let malformed=0;const good=src([1,0,1]);
for(const s of [good.replace("cnf","cnd"),good.replace("3 6","3 5"),
 good.replace("+1 0","+0 0"),good.replace("-2 0","?2 0"),
 good.slice(0,-1),good+"bad\n",good.replace("+3 0","-3 0"),
 good.replace("+1 0","+9 0"),good.replace("+2 0","+2 -3 0"),
 good.replace("p cnf","P cnf")]){
 try{parse(s)}catch(e){malformed++;}}
ok(malformed===10,"malformed");
let scales=[];
for(const N of [1024,4096,16384,65536]){
 let Q=Math.floor(N**.6),B=Math.floor(N**.5);
 const bits=Array.from({length:Q},(_,i)=>Number(i%7!==3));
 const input=src(bits,N);
 ok(input.length===N,"N bytes");ok(parse(input).join("")===bits.join(""),"sign decode");
 const childBase=i=>"p cnf "+Q+" 2\n+"+(i+1)+" 0\n"+(bits[i]?"+":"-")+(i+1)+" 0\n";
 for(let i=0;i<Q;i++){const d=B-childBase(i).length;ok(d===0||d>=3,"child pad");ok(childBase(i).length+d===B,"length");}
 scales.push({source_bytes:N,Q,child_bytes:B,serialized_portfolio_bytes:Q*B,yes:bits.reduce((a,b)=>a+b,0),no:Q-bits.reduce((a,b)=>a+b,0)});
}
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
let k4={};
for(const [label,c] of [["even",[0,0,0,0]],["odd",[1,0,0,0]]]){
 let models=0;for(let a=0;a<64;a++)if(c.every((v,i)=>edges.reduce((p,e,j)=>p^(e.includes(i)?((a>>j)&1):0),0)===v))models++;
 k4[label]=models;
}
ok(k4.even===8&&k4.odd===0,"K4 hostile parity");
console.log(JSON.stringify({run:"390",checks,parents,children,malformed,k4,scales,status:"restricted finite control; B1/B2/B3 OPEN"},null,2));
