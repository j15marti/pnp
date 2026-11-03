#!/usr/bin/env node
// Standalone public compact calculator; full independent signed-DAG verifier is in reproducibility archive.
function example(name){
let h,edges=[],V;
if(name==='K4'){h=4;for(let i=0;i<h;i++)for(let j=i+1;j<h;j++)edges.push([i,j]);}
else if(name==='K33'){h=6;for(let i=0;i<3;i++)for(let j=3;j<6;j++)edges.push([i,j]);}
else if(name==='cube'){h=8;for(let i=0;i<8;i++)for(let b=0;b<3;b++){let j=i^(1<<b);if(i<j)edges.push([i,j]);}}
else {let r=Number(name.slice(5));h=2*r;for(let i=0;i<r;i++){edges.push([i,(i+1)%r],[i+r,((i+1)%r)+r],[i,i+r]);}}
const adj=Array.from({length:h},()=>[]);edges.forEach(([u,v],i)=>{adj[u].push(i+1);adj[v].push(i+1)}); if(adj.some(x=>x.length!==3))throw Error('not cubic');
let count=0,max=0,levels=0,nodes=0;
function fold(a,depth){if(a.length===1)return new Set(adj[a[0]]);let m=Math.floor(a.length/2),L=fold(a.slice(0,m),depth+1),R=fold(a.slice(m),depth+1);for(const e of R){if(L.has(e))L.delete(e);else L.add(e)}count+=L.size;max=Math.max(max,L.size);levels=Math.max(levels,depth+1);nodes++;return L}
let result=fold(Array.from({length:h},(_,i)=>i),0);if(result.size)throw Error('terminal not empty');let bound=3*h*Math.ceil(Math.log2(h));if(count>bound||nodes!==h-1)throw Error('budget');return {graph:name,h,n:edges.length,logical_nodes:4*h-1,xor_output_width_sum:count,xor_max_width:max,bound};}
for(const n of ['K4','K33','cube','prism6','prism10','prism20'])console.log(JSON.stringify(example(n)));
