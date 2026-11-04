#!/usr/bin/env node
/** Independent checker of LSPV-2/400 strict triple input code.
 * Uses no producer logic or external dependency.
 * Run: node experiments/arc/lspv2_400_independent_verify.js results/raw/arc/2026-11-04_1412_LSPV2_STRICT_CODE_INTERFACE400_raw.json
 */
"use strict";
const fs=require("fs"),assert=require("assert").strict;
const raw=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
const prefix="110101";
let total=0,nSAT=0,nUNSAT=0,flips=0,pivots=0,rejects=0;
function g(k){assert(k>=1);let s=k.toString(2);return "0".repeat(s.length-1)+s}
function write(n,formula){
 let s=prefix+g(n)+g(formula.length+1),positions=[],w=n.toString(2).length;
 for(const c of formula){
   s+=g(c.length+1);
   for(const l of c){
     positions.push(s.length);
     s+=(l>0?"1":"0")+Math.abs(l).toString(2).padStart(w,"0")
   }
 }
 return {s,positions};
}
function read(s){
 if(typeof s!=="string"||!s.startsWith(prefix)||!/^[01]+$/.test(s))throw Error("source");
 let p=prefix.length;
 function gamma(){
   let z=0;while(p<s.length&&s[p]==="0"){p++;z++}
   if(p+z>=s.length)throw Error("gamma");
   let v=parseInt(s.slice(p,p+z+1),2);p+=z+1;return v
 }
 let n=gamma(),m=gamma()-1,w=n.toString(2).length,F=[];
 if(n<1||m<0)throw Error("n/m");
 for(let i=0;i<m;i++){
   let len=gamma()-1,c=[];
   for(let j=0;j<len;j++){
     if(p+w>=s.length)throw Error("lit");
     let neg=s[p++]==="0",v=parseInt(s.slice(p,p+w),2);p+=w;
     if(v<1||v>n)throw Error("id");
     c.push(neg?-v:v)
   }
   F.push(c)
 }
 if(p!==s.length)throw Error("trailing");
 return {n,F}
}
function enc3(s){return [...s].map(x=>x+x+x).join("")}
function dec3(t){
 if(typeof t!=="string"||t.length%3!==0||!/^[01]*$/.test(t))throw Error("code");
 let s="";
 for(let i=0;i<t.length;i+=3){
   if(t[i]!==t[i+1]||t[i]!==t[i+2])throw Error("mismatch");
   s+=t[i]
 }
 return read(s)
}
function sat(n,F){
 for(let a=0;a<(1<<n);a++){
   if(F.every(c=>c.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0))))return true
 }
 return false
}
function flip(s,i){return s.slice(0,i)+(s[i]==="0"?"1":"0")+s.slice(i+1)}
const universe=[[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]];
for(let mask=0;mask<256;mask++){
 let F=universe.filter((c,i)=>((mask>>i)&1)!==0),{s}=write(2,F),t=enc3(s);
 assert.deepEqual(read(s),{n:2,F});assert.deepEqual(dec3(t),{n:2,F});total+=2;
 let label=sat(2,F);label?nSAT++:nUNSAT++;
 for(let i=0;i<t.length;i++){assert.throws(()=>dec3(flip(t,i)));flips++;total++}
}
function tseitin(vs,edges,odd){
 let adj=Array.from({length:vs},()=>[]);
 edges.forEach(([u,v],i)=>{adj[u].push(i+1);adj[v].push(i+1)});
 let F=[];
 adj.forEach((ids,v)=>{
   assert.equal(ids.length,3);
   for(let mask=0;mask<8;mask++){
     let charge=(odd&&v===0)?1:0;
     if(((mask&1)+((mask>>1)&1)+((mask>>2)&1))%2!==charge)
       F.push(ids.map((id,j)=>((mask>>j)&1)?-id:id))
   }
 });
 return F
}
const K4=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const K33=Array.from({length:9},(_,i)=>[Math.floor(i/3),3+i%3]);
for(const [name,n,edges] of [["K4",4,K4],["K33",6,K33]]){
 for(const odd of [true,false]){
   let F=tseitin(n,edges,odd),{s,positions}=write(edges.length,F),t=enc3(s);
   assert.equal(sat(edges.length,F),!odd);
   assert.deepEqual(dec3(t),{n:edges.length,F});
   total+=2;
   if(odd)for(const i of positions){
      let x=flip(s,i),z=enc3(x);
      assert.equal(sat(edges.length,read(x).F),true);
      assert.equal([...t].filter((a,j)=>a!==z[j]).length,3);
      assert.deepEqual(dec3(z),read(x));
      total+=3;pivots++
   }
 }
}
for(const t of ["","111","xxx"]){assert.throws(()=>dec3(t));rejects++;total++}
let s=write(2,[[1],[-1]]).s,t=enc3(s);
for(const bad of [t+"0",t.slice(0,-1),flip(t,3)]){
 assert.throws(()=>dec3(bad));rejects++;total++
}
assert.equal(nSAT,raw.counts.SAT);
assert.equal(nUNSAT,raw.counts.UNSAT);
assert.equal(flips,raw.counts.triple_single_bit_malformed);
assert.equal(pivots,raw.counts.Tseitin_source_pivots);
assert.equal(rejects,raw.malformed_rejected);
console.log(JSON.stringify({schema:"LSPV2-400-independent-v1",status:"COMPUTATIONAL",
  assertions:total,SAT:nSAT,UNSAT:nUNSAT,
  three_copy_invalid_single_flips:flips,
  Tseitin_disjoint_opposite_blocks:pivots,
  malformed_rejected:rejects,agreement:true},null,2));
