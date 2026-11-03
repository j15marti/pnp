#!/usr/bin/env node
// Standalone, standard Node.js only: Peitl selector composition and signed Resolution replay.
// Usage: node experiments/arc/lspv4_352_peitl_selector_compact.js
// Independent detailed referee, binary codec, 10,137 SAT neighbors and timing logs
// are in LSPV4_PEITL_SELECTOR_LINEAR_CAP352_repro.zip.
const S=[[-1,2],[-2,3],[-3,4],[-4,5],[1,-5],[1,2,3,4,5],[-1,-2,-3,-4,-5]];
const P=[[4,6,-4],[5,8,-5],[1,7,2],[1,9,-1],[5,10,1],[2,11,-2],[4,12,5],[3,14,4],[13,15,3]];
function norm(xs){let t=[...new Set(xs)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
 if(t.some(x=>t.includes(-x)))throw Error('tautology');return t}
function resolve(A,B,p){if(!A.includes(p)||!B.includes(-p))throw Error('pivot');
 return norm([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)])}
function tree(k,comb){
 let L=Array.from({length:k},(_,i)=>({leaf:i}));
 if(comb){let p={left:L[0],right:L[1]};for(let i=2;i<k;i++)p={left:p,right:L[i]};return p}
 function go(a,b){if(b-a===1)return L[a];let m=(a+b)/2;return {left:go(a,m),right:go(m,b)}}return go(0,k)}
function nodes(t,parents=[]){if(t.leaf!==undefined)return parents;parents.push(t);
 nodes(t.left,parents);nodes(t.right,parents);return parents}
function gamma(v){let b=v.toString(2);return '0'.repeat(b.length-1)+b}
function run(k,shape){
 const root=k===1?{leaf:0}:tree(k,shape==='comb'),parents=nodes(root);
 parents.forEach((u,i)=>u.var=5*k+i+1);
 const guard={};function go(u,g){if(u.leaf!==undefined){guard[u.leaf]=g;return}
  go(u.left,[...g,u.var]);go(u.right,[...g,-u.var])}go(root,[]);
 const original=[],ids={};
 for(let i=0;i<k;i++){ids[i]=[];for(let c of S){original.push(norm([...guard[i],...c.map(l=>Math.sign(l)*(5*i+Math.abs(l)))]));ids[i].push(original.length)}}
 const db=original.slice(),steps=[],end={};
 function step(a,b,p){const c=resolve(db[a-1],db[b-1],p);db.push(c);steps.push([a,b,p]);return db.length}
 for(let i=0;i<k;i++){const lines={};ids[i].forEach((id,j)=>lines[j+1]=id);
  P.forEach(([a,b,p],j)=>{lines[8+j]=step(lines[a],lines[b],Math.sign(p)*(5*i+Math.abs(p)) )});
  end[i]=lines[16];if(JSON.stringify(db[end[i]-1])!==JSON.stringify(norm(guard[i])))throw Error('guard')}
 function finish(u){if(u.leaf!==undefined)return end[u.leaf];return step(finish(u.left),finish(u.right),u.var)}
 finish(root);if(db.at(-1).length!==0)throw Error('not contradiction');
 const n=6*k-1,m=original.length,q=steps.length,w=Math.ceil(Math.log2(n+1));
 const L=original.reduce((a,c)=>a+c.length,0);
 const N=gamma(n+1).length+gamma(m+1).length+original.reduce((s,c)=>s+gamma(c.length+1).length+c.length*(1+w),0);
 const evidence=q*(2*Math.ceil(Math.log2(m+q+1))+w);
 const inspections=steps.reduce((a,[i,j])=>a+db[i-1].length+db[j-1].length,0);
 if(q!==10*k-1||m!==7*k)throw Error('node count');
 return {k,shape,variables:n,sources:m,N,L,mixed_min_at_least:7*k-1,
  mixed_at_most:q,executed_RES_nodes:q,pivot_evidence_bits:evidence,eager_parent_reads:inspections};
}
const result=[];for(let k of [1,2,4,8,16,32])for(let shape of ['balanced','comb']){
 if(k===1&&shape==='comb')continue;result.push(run(k,shape))}
console.log(JSON.stringify({status:'VALID_SIGNED_RESOLUTION_UPPER',cases:result.length,
 note:'Bounds not exact mixed minima for k>1; no B3 or P-versus-NP result.',rows:result},null,2));
