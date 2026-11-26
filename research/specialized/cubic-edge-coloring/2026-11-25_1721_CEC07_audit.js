"use strict";
function audit(){
 const assert=(b,m)=>{if(!b)throw Error(m);stats.assertions++};
 const stats={assertions:0,nodes:0,scans:0,forces:0,failed:0,closureCalls:0};
 const cyc=n=>Array.from({length:n},(_,i)=>[i,(i+1)%n]);
 const gadget=cyc(7).concat([[2,5],[3,6]]), ports=[0,1,4];
 function verify(n,E,c){let a=Array.from({length:n},()=>[]);E.forEach(([u,v],i)=>{a[u].push(c[i]);a[v].push(c[i])});return a.every(x=>x.length===3&&new Set(x).size===3&&x.every(v=>v>=0&&v<3))}
 function solve(n,E,pins=[]){
  let inc=Array.from({length:n},()=>[]);E.forEach(([u,v],i)=>{inc[u].push(i);if(v<n)inc[v].push(i)});
  if(inc.some(x=>x.length!==3))throw Error("not cubic");
  let init=E.map(()=>7);for(let [i,c] of pins)init[i]=1<<c;
  function closure(d){stats.closureCalls++;let change=true;while(change){change=false;for(let ids of inc){stats.scans++;let allowed=[0,0,0];for(let a=0;a<3;a++)for(let b=0;b<3;b++)if(a!==b){let c=3-a-b;if((d[ids[0]]>>a&1)&&(d[ids[1]]>>b&1)&&(d[ids[2]]>>c&1)){allowed[0]|=1<<a;allowed[1]|=1<<b;allowed[2]|=1<<c}}for(let i=0;i<3;i++){let k=ids[i],v=d[k]&allowed[i];if(!v)return false;if(v!==d[k]){d[k]=v;stats.forces++;change=true}}}}return true}
  function rec(d){stats.nodes++;if(!closure(d)){stats.failed++;return null}let k=d.findIndex(v=>(v&(v-1))!==0);if(k<0)return d.map(v=>Math.log2(v));for(let c=0;c<3;c++)if(d[k]>>c&1){let q=d.slice();q[k]=1<<c;let ans=rec(q);if(ans)return ans}return null}
  return rec(init)
 }
 const capE=gadget.concat(ports.map((v,i)=>[v,7+i]));
 const perms=[];for(let a=0;a<3;a++)for(let b=0;b<3;b++)if(a!==b)perms.push([a,b,3-a-b]);
 let cap={};
 for(const p of perms){let w=solve(7,capE,p.map((c,i)=>[9+i,c]).concat([]));assert(w,"cap extension");let fixed=null;for(let a=0;a<2;a++)for(let b=0;b<2;b++){let z=solve(7,capE,p.map((c,i)=>[9+i,c]).concat([[7,a],[8,b]]));if(z)fixed=z}assert(fixed,"one hit cap");cap[p.join("")]=fixed}
 let capTable=[];for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let c=0;c<3;c++){let p=[a,b,c],w=solve(7,capE,p.map((x,i)=>[9+i,x]));assert(!!w===(new Set(p).size===3),"cap table");if(w)capTable.push(p)}
 function matchings(n,E){let inc=Array.from({length:n},()=>[]);E.forEach(([u,v],i)=>{inc[u].push([v,i]);inc[v].push([u,i])});let out=[];function rec(used,L){let v=used.indexOf(false);if(v<0){out.push(L.slice());return}used[v]=true;for(let [w,i] of inc[v])if(!used[w]){used[w]=true;L.push(i);rec(used,L);L.pop();used[w]=false}used[v]=false}rec(Array(n).fill(false),[]);return out}
 function colorComplement(n,E,L){let s=new Set(L),inc=Array.from({length:n},()=>[]),c=E.map((_,i)=>s.has(i)?2:-1);E.forEach(([u,v],i)=>{if(!s.has(i)){inc[u].push([v,i]);inc[v].push([u,i])}});if(inc.some(a=>a.length!==2))return null;for(let i=0;i<n;i++)for(let [j,e] of inc[i])if(c[e]<0){let u=i,v=j,k=e,col=0;while(c[k]<0){c[k]=col;col^=1;let next=inc[v].find(([_,h])=>h!==k);u=v;[v,k]=next}if(col!==0)return null}return verify(n,E,c)?c:null}
 function expand(n,E){let inc=Array.from({length:n},()=>[]);E.forEach(([u,v],i)=>{inc[u].push(i);inc[v].push(i)});let edges=[],M=[],cycles=[];for(let v=0;v<n;v++){let start=edges.length;for(let [a,b] of gadget)edges.push([7*v+a,7*v+b]);cycles.push(Array.from({length:7},(_,i)=>7*v+i));M.push(start+7,start+8)}let ext=[];for(let i=0;i<E.length;i++){let [u,v]=E[i];ext.push(edges.length);M.push(edges.length);edges.push([7*u+ports[inc[u].indexOf(i)],7*v+ports[inc[v].indexOf(i)]])}return {edges,M,cycles,ext,inc}}
 function fixed(n,E,M,cycles,S){let chosen=new Set(S),at=new Map(),lookup=new Map();E.forEach(([a,b],i)=>{lookup.set([Math.min(a,b),Math.max(a,b)].join(","),i)});for(let i of M){let [u,v]=E[i];at.set(u,i);at.set(v,i)}let L=S.slice();for(let C of cycles){let hits=C.map(v=>chosen.has(at.get(v))),j=hits.indexOf(true);if(j<0)return {status:"UNKNOWN"};let run=[];for(let k=1;k<=C.length;k++){let i=(j+k)%C.length;if(hits[i]){if(run.length%2)return {status:"NO_MATCH"};for(let p=0;p<run.length;p+=2)L.push(lookup.get([Math.min(run[p],run[p+1]),Math.max(run[p],run[p+1])].join(",")));run=[]}else run.push(C[i])}}
 let w=colorComplement(n,E,L);return {status:w?"SAT":"NO_COLOR",L,w}}
 const k4=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]], k33=Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>[i,j+3])).flat();
 const prism=n=>cyc(n).concat(cyc(n).map(([u,v])=>[u+n,v+n]),Array.from({length:n},(_,i)=>[i,i+n]));
 const pet=cyc(5).concat(Array.from({length:5},(_,i)=>[i+5,(i+2)%5+5]),Array.from({length:5},(_,i)=>[i,i+5]));
 const flower=[];for(let i=0;i<5;i++){for(let j=1;j<4;j++)flower.push([4*i,4*i+j]);flower.push([4*i+1,4*((i+1)%5)+1]);if(i<4){flower.push([4*i+2,4*(i+1)+2],[4*i+3,4*(i+1)+3])}else flower.push([4*i+2,3],[4*i+3,2])}
 let rows=[];
 for(let [name,n,E] of [["K4",4,k4],["K33",6,k33],["prism3",6,prism(3)],["prism5",10,prism(5)],["Petersen",10,pet],["flowerJ5",20,flower]]){
  let source=solve(n,E),A=expand(n,E),N=7*n,Ms=matchings(n,E),yes=0,minimum=0,lifts=0,sourceWitness=source;
  assert(A.edges.length===3*N/2,"degree count");assert(new Set(A.edges.map(([a,b])=>[Math.min(a,b),Math.max(a,b)].join(","))).size===A.edges.length,"simple");
  let inc=Array.from({length:N},()=>[]);A.edges.forEach(([u,v],i)=>{inc[u].push(v);inc[v].push(u)});assert(inc.every(a=>a.length===3),"cubic");assert(inc.every((a,i)=>a.every(j=>!inc[j].some(k=>a.includes(k)))),"triangle free");
  for(let P of Ms){let sw=colorComplement(n,E,P),r=fixed(N,A.edges,A.M,A.cycles,P.map(i=>A.ext[i]));assert(r.status!=="NO_MATCH"&&r.status!=="UNKNOWN","minimum matching exists");minimum++;assert(r.L.length===N/2&&new Set(r.L).size===N/2,"perfect matching length");let deg=Array(N).fill(0);for(let i of r.L){let [u,v]=A.edges[i];deg[u]++;deg[v]++}assert(deg.every(x=>x===1),"actual minimum PM");assert((r.status==="SAT")===!!sw,"guarded equivalence");if(sw){yes++;assert(verify(N,A.edges,r.w),"fixed lift");assert(verify(n,E,A.ext.map(i=>r.w[i])),"decoded");let w=Array(A.edges.length);A.ext.forEach((e,i)=>w[e]=sw[i]);for(let v=0;v<n;v++){let local=cap[A.inc[v].map(i=>sw[i]).join("")];for(let i=0;i<9;i++)w[9*v+i]=local[i]}assert(verify(N,A.edges,w),"cap lift");lifts++}}
  assert(!!source===(yes>0),"source reference");rows.push({name,n,sourceEdges:E,expandedVertices:N,sourceSAT:!!source,sourcePerfectMatchings:Ms.length,minimumIntersectionMatchingsTested:minimum,successful:yes,verifiedBothDirectionLifts:lifts,sourceWitness})
 }
 return {capEdges:capE,capWitnesses:cap,capTable,rows,stats,scope:"Finite source reference solver and exhaustive source matching controls; no unrestricted polynomial solver, no general blossom or square chart implemented."}
}
console.log(JSON.stringify(audit(),null,2));
