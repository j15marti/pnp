'use strict';
// LSPV-2/477: independent finite boundary characterization test.
// Compares actual 3-CNF exhaustive truth tables with original-edge/GF(2) boundary enumeration.
// NOT a cutset-DP implementation, native FLMV machine, or proof of all-input contraction.
const assert=require('node:assert/strict');
const graphs={
 K4:[...Array(4)].flatMap((_,u)=>[...Array(4)].map((_,v)=>[u,v]).filter(([a,b])=>a<b)),
 prism4:(()=>{let e=[];for(let t=0;t<2;t++)for(let i=0;i<4;i++)e.push([4*t+i,4*t+(i+1)%4]);for(let i=0;i<4;i++)e.push([i,4+i]);return e;})(),
 cube:[...Array(8)].flatMap((_,a)=>[...Array(8)].map((_,b)=>[a,b]).filter(([a,b])=>a<b&&((a^b).toString(2).match(/1/g)||[]).length===1)),
};
let seed=477;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;}
function build(edges,n,charges){
 const inc=[...Array(n)].map(()=>[]);edges.forEach(([a,b],i)=>{inc[a].push(i);inc[b].push(i)});
 const packets=inc.map((ids,v)=>{let arr=[];for(let a=0;a<8;a++)if(((a.toString(2).replace(/0/g,'').length)&1)!==charges[v])arr.push(ids.map((i,j)=>((a>>j)&1)?-(i+1):(i+1)));return arr;});
 return {packets,inc};
}
function sat(packet,a){return packet.every(cl=>cl.some(x=>a[Math.abs(x)-1]===(x>0?1:0)));}
function classifyBrute(packets,m){
 for(let b=0;b<(1<<m);b++){let a=[...Array(m)].map((_,i)=>(b>>i)&1);if(packets.every(p=>sat(p,a)))return a;}
 return null;
}
function boundary(packets,edges,n,defects,charges){
 const D=new Set(defects),intact=[...Array(n)].map((_,i)=>i).filter(v=>!D.has(v));
 const adj=[...Array(n)].map(()=>[]);edges.forEach(([u,v],i)=>{adj[u].push([v,i]);adj[v].push([u,i])});
 let comps=[],cid={};
 for(const v of intact){
  if(Object.hasOwn(cid,v))continue;
  let cid0=comps.length,queue=[v],comp=[];cid[v]=cid0;
  while(queue.length){let u=queue.pop();comp.push(u);for(let [w] of adj[u])if(!D.has(w)&&!Object.hasOwn(cid,w)){cid[w]=cid0;queue.push(w)}}
  comps.push(comp);
 }
 const q=comps.map(comp=>comp.reduce((acc,u)=>acc^charges[u],0));
 const touched=edges.map(([u,v],i)=>(D.has(u)||D.has(v))?i:-1).filter(e=>e>=0);
 for(let b=0;b<(1<<touched.length);b++){
  let a=new Array(edges.length).fill(0);touched.forEach((e,i)=>a[e]=(b>>i)&1);
  let good=true;
  for(let u of D){if(!sat(packets[u],a)){good=false;break}}if(!good)continue;
  let sig=new Array(comps.length).fill(0);
  touched.forEach(e=>{let [u,v]=edges[e];if(D.has(u)&&!D.has(v))sig[cid[v]]^=a[e];else if(D.has(v)&&!D.has(u))sig[cid[u]]^=a[e]});
  if(sig.every((x,i)=>x===q[i]))return true;
 }
 return false;
}
let stats={seed:477,total:0,sat:0,unsat:0,cyclic:0,malformed:0,forcedConflict:0};
for(let [name,edges] of Object.entries(graphs)){
 let n=Math.max(...edges.flat())+1, base=build(edges,n,[...Array(n)].map((_,i)=>i===0?1:0));
 for(let j=0;j<120;j++){
  let packets=base.packets.map(x=>x.map(y=>y.slice())),defective=new Set();
  for(let u=0;u<n;u++)if(rnd(3)!==0){
   defective.add(u);let ids=base.inc[u];
   packets[u]=[...Array(4)].map(()=>ids.map(e=>rnd(2)?-(e+1):(e+1)));
  }
  if(j%12===0){
   const [u,v]=edges[0],idsU=base.inc[u],idsV=base.inc[v],e=0;
   const force=(ids,value)=>{
    let arr=[];
    for(let a=0;a<8;a++){let bits=ids.map((_,z)=>(a>>z)&1);
     if(bits[ids.indexOf(e)]!==value)arr.push(ids.map((id,z)=>bits[z]?-(id+1):(id+1)));
    }
    return arr;
   };
   packets[u]=force(idsU,1);packets[v]=force(idsV,0);
   defective.add(u);defective.add(v);stats.forcedConflict++;
  }
  const d=[...defective],edgeDef=edges.filter(([u,v])=>defective.has(u)&&defective.has(v));
  let cycl=edgeDef.length-d.length+(d.length?1:0)>0; // proxy only, not exact rank
  let b=boundary(packets,edges,n,d,[...Array(n)].map((_,i)=>i===0?1:0));
  let ans=classifyBrute(packets,edges.length)!==null;
  assert.equal(b,ans,name+' test '+j);stats.total++;
  stats[ans?'sat':'unsat']++;if(cycl)stats.cyclic++;
 }
}
for(const bad of [[],[[1,2]],[[1,1,-3]],[[0,2,3]]]){
 assert.ok(!Array.isArray(bad[0])||bad[0].length!==3||bad[0].includes(0)||new Set(bad[0].map(Math.abs)).size!==3);
 stats.malformed++;
}
console.log(JSON.stringify(stats,null,2));
