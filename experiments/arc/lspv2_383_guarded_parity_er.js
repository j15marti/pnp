// LSPV-2/383: strict signed-Resolution certificates, with six charged AND2 definitions.
// Usage: node experiments/arc/lspv2_383_guarded_parity_er.js [outfile]
'use strict';
function canon(xs){const s=new Set(xs);for(const x of s)if(!Number.isInteger(x)||!x||s.has(-x))return null;return [...s].sort((a,b)=>Math.abs(a)-Math.abs(b)||(a<0?1:-1));}
function views(z,a,b){return [canon([-z,a]),canon([-z,b]),canon([z,-a,-b])];}
function sources(charge){const r=[];for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let z=0;z<2;z++)if((x^y^z)!==charge)r.push(canon([x?-1:1,y?-2:2,z?-3:3,-4]));return r;}
function saturate(src,pivots){const nodes=src.map(c=>({c,parents:null,pivot:null}));const have=new Map(nodes.map((n,i)=>[JSON.stringify(n.c),i]));const stats=[];for(const p of pivots){const old=[...have.entries()].map(([k,i])=>[JSON.parse(k),i]);let count=0;for(const [a,i] of old)if(a.includes(p))for(const [b,j] of old)if(b.includes(-p)){const r=canon([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);if(!r)continue;const k=JSON.stringify(r);if(have.has(k))continue;have.set(k,nodes.length);nodes.push({c:r,parents:[i,j],pivot:p});count++;}stats.push({pivot:p,added:count,total:nodes.length});}return {nodes,have,stats};}
function need(nodes,goals){const seen=new Set();function walk(i){if(seen.has(i))return;seen.add(i);const n=nodes[i];if(n.parents)n.parents.forEach(walk);}goals.forEach(walk);return seen;}
function cert(charge){
 const src=sources(charge),G=[[5,1,-2],[6,-1,2],[7,-5,-6],[8,-7,-3],[9,7,3],[10,-8,-9]];
 const v1=charge===0?[canon([-4,7,3]),canon([-4,-7,-3])]:[canon([-4,-7,3]),canon([-4,7,-3])];
 const p1=saturate([...src,...G.slice(0,3).flatMap(g=>views(...g))],[1,2,5,6]);
 const idx1=v1.map(c=>p1.have.get(JSON.stringify(c)));if(idx1.some(x=>x===undefined))throw Error('phase1 goal missing');
 const p2=saturate([...v1,...G.slice(3).flatMap(g=>views(...g))],[7,3,8,9]);
 const goal=canon([-4,charge===0?10:-10]),idx2=p2.have.get(JSON.stringify(goal));if(idx2===undefined)throw Error('phase2 goal missing');
 const lines=src.map(c=>({kind:'source',c}));
 G.forEach((g,gi)=>views(...g).forEach((c,vi)=>lines.push({kind:'view',gate:gi,view:vi,c})));
 const map1=new Map([...Array(13).keys()].map(i=>[i,i])),selected1=need(p1.nodes,idx1);
 for(let i=13;i<p1.nodes.length;i++)if(selected1.has(i)){const n=p1.nodes[i];map1.set(i,lines.length);lines.push({kind:'res',c:n.c,pivot:n.pivot,parents:n.parents.map(j=>map1.get(j))});}
 const map2=new Map([[0,map1.get(idx1[0])],[1,map1.get(idx1[1])]]);
 for(let i=2;i<11;i++)map2.set(i,11+i);
 const selected2=need(p2.nodes,[idx2]);
 for(let i=11;i<p2.nodes.length;i++)if(selected2.has(i)){const n=p2.nodes[i];map2.set(i,lines.length);lines.push({kind:'res',c:n.c,pivot:n.pivot,parents:n.parents.map(j=>map2.get(j))});}
 return {charge,gates:G.map(g=>({output:g[0],inputs:g.slice(1)})),clauses:lines,guards:v1,goal,goal_id:map2.get(idx2),paid_res:lines.length-22,paid_defs:6,paid_total:lines.length-16,stage1_saturation:p1.stats,stage2_saturation:p2.stats,scope:'upper witness only, not global minimum'};
}
function make(){return {id:'LSPV2-383',model:'charged signed-AND2 conservative DEF plus strict binary Resolution',claim:'source-anchored two-charge local guarded parity output',global_minimum:false,cases:[cert(0),cert(1)]};}
if(typeof require!=='undefined' && typeof module!=='undefined' && require.main===module){
 const fs=require('fs');const out=process.argv[2]||'lspv2_383_local_raw.json';const a=make();
 fs.writeFileSync(out,JSON.stringify(a,null,2)+'\n');console.log(JSON.stringify({output:out,cases:a.cases.map(c=>({charge:c.charge,paid_total:c.paid_total,paid_res:c.paid_res}))}));
}
