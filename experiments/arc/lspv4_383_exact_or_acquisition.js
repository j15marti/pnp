// LSPV-4/383: self-contained independent exact-control reproducer (Node >=18).
// Only arithmetic counts of probes; not native FLMV tape measurements.
"use strict";
const assert=require("node:assert/strict");
let checks=0, cases=0, sat=0, unsat=0, probes=0, pivots=0;
function src(m,b){return "CIROR "+m+"\n"+b+"\n";}
function parse(s){
  const a=s.split("\n"), hd=a[0].match(/^CIROR ([1-9][0-9]*)$/);
  if(a.length!==3 || !hd || Number(hd[1])!==a[1].length ||
     !/^[01]+$/.test(a[1]) || a[2]!=="") throw Error("malformed source");
  return a[1];
}
function compile(s){
  const b=parse(s);
  for(let j=0;j<b.length;j++)
    if(b[j]==="1") return ["p cnf 1 1\n1 0\n",j+1];
  return ["p cnf 1 2\n1 0\n-1 0\n",b.length];
}
function satCNF(t){
 const lines=t.trim().split("\n"),hdr=lines.shift().split(" ");
 assert.equal(hdr[0]+" "+hdr[1],"p cnf");checks++;
 const n=Number(hdr[2]),m=Number(hdr[3]);assert.equal(lines.length,m);checks++;
 const cs=lines.map(s=>s.trim().split(/\s+/).map(Number));
 return Array.from({length:1<<n},(_,a)=>a).some(a=>
   cs.every(c=>c.slice(0,-1).some(v=>(((a>>(Math.abs(v)-1))&1)===Number(v>0)))));
}
for(let m=1;m<=9;m++){
  for(let i=0;i<(1<<m);i++){
    const b=Array.from({length:m},(_,j)=>String((i>>j)&1)).join("");
    const [out,nq]=compile(src(m,b)),truth=b.includes("1");
    assert.equal(satCNF(out),truth);checks++;
    assert.equal(nq,truth?b.indexOf("1")+1:m);checks++;
    cases++; sat+=Number(truth);unsat+=Number(!truth);probes+=nq;
  }
  const z="0".repeat(m);
  assert.equal(satCNF(compile(src(m,z))[0]),false);checks++;
  for(let i=0;i<m;i++){
    const b=z.slice(0,i)+"1"+z.slice(i+1);
    assert.equal(satCNF(compile(src(m,b))[0]),true);checks++;pivots++;
  }
}
const malformed=["","CIROR 0\n\n","CIROR 2\n0\n","CIROR 2\n02\n",
"CIROR 02\n00\n","CIROR x\n00\n","CIROR 2\n01\nextra",
"CIROR 2\n01\n\n","CIROR 2\n-1\n","CIROR 2\n01\n1",
"p cnf 1 1\n1 0\n","CIROR 2\n0 1\n"];
for(const b of malformed){assert.throws(()=>parse(b));checks++;}
function k4(odd){
 const E=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)E.push([i,j]);
 let count=0;
 for(let mask=0;mask<64;mask++){
   let good=true;
   for(let v=0;v<4;v++){
     let p=0;for(let e=0;e<6;e++)if(E[e].includes(v))p^=(mask>>e)&1;
     if(p!==Number(odd&&v===0))good=false;
   }
   if(good)count++;
 }
 return count;
}
assert.equal(k4(true),0);assert.equal(k4(false),8);checks+=2;
const rows=[100,1000,10000,100000].map(N=>{
 const b=Math.ceil(N**.6),L=Math.ceil(N**.5);
 const direct=b*L,rescan=b*L*(L+1)/2;
 assert(rescan>=direct);checks++;
 return {N,children:b,child_bits:L,streaming_direct_probes:direct,
 sequential_prefix_rescan_probes:rescan,each_parent_full_scan_probes:b*L*N};
});
const result={status:"COMPUTATIONAL",cases,sat,unsat,probes,pivots,
 malformed_rejections:malformed.length,k4_odd_models:k4(true),
 k4_even_models:k4(false),checks,rows,
 note:"all accesses are declared-source-probe counts; not native TM steps"};
assert.deepEqual([cases,sat,unsat,probes,pivots],[1022,1013,9,2026,45]);
console.log(JSON.stringify(result,null,2));
