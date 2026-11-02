'use strict';
// LSPV-3 SPLIT-GAP344. Deterministic source-labelled family and Resolution
// refutations. Unit-node exactness in the full mixed calculus is NOT assumed.
const G=[[-3,1,4],[-1,2],[1,3],[-4,-3],[-2,-1,3],[-2,4]];
const cases=[0,1,2,3,7,15,31,63,127];
const canon=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
const evalC=(c,a)=>c.some(v=>a[Math.abs(v)]===(v>0?1:0));
function res(A,B,p){
 if(!((A.includes(p)&&B.includes(-p))||(B.includes(p)&&A.includes(-p))))throw Error('missing pivot');
 const z=canon([...A,...B].filter(v=>Math.abs(v)!==p));
 if(z.some(v=>z.includes(-v)))throw Error('tautological resolvent');
 return z;
}
function baseWitness(i){
 for(let a=0;a<16;a++){
  const bits=Array(5).fill(0);for(let j=1;j<=4;j++)bits[j]=(a>>(j-1))&1;
  if(!evalC(G[i],bits)&&G.every((c,j)=>j===i||evalC(c,bits)))return bits;
 }throw Error('base not minimal');
}
function build(t){
 const root={depth:0,lit:G[0].slice(),path:[]},leaves=[root];
 for(let i=1;i<=t;i++){
  const ix=leaves.reduce((best,o,j)=>o.depth<leaves[best].depth?j:best,0);
  const z=leaves.splice(ix,1)[0];z.pivot=4+i;
  z.left={depth:z.depth+1,lit:[...z.lit,z.pivot],path:[...z.path,[z.pivot,0]]};
  z.right={depth:z.depth+1,lit:[...z.lit,-z.pivot],path:[...z.path,[z.pivot,1]]};
  leaves.push(z.left,z.right);
 }
 const ordered=[];function walk(z){if(z.left){walk(z.left);walk(z.right)}else ordered.push(z)}walk(root);
 const source=ordered.map((z,i)=>({id:'s'+i,clause:canon(z.lit),kind:'leaf',path:z.path}));
 for(let i=1;i<6;i++)source.push({id:'s'+source.length,clause:canon(G[i]),kind:'original',original:i});
 const all=new Map(source.map(x=>[x.id,x.clause])),nodes=[];
 function add(a,b,p){const out=res(all.get(a),all.get(b),p),id='d'+nodes.length;
  nodes.push({id,rule:'RES',parents:[a,b],pivot:p,clause:out});all.set(id,out);return id}
 const leafIds=new Map(ordered.map((z,i)=>[z,'s'+i]));
 function compile(z){return z.left?add(compile(z.left),compile(z.right),z.pivot):leafIds.get(z)}
 const c0=compile(root),s=i=>source[ordered.length+i-1].id;
 const d0=add(c0,s(3),4),d1=add(s(2),d0,3),d2=add(s(3),s(5),4);
 const d3=add(s(4),d2,3),d4=add(s(1),d3,2),d5=add(d1,d4,1);
 if(all.get(d5).length!==0||nodes.length!==t+6)throw Error('upper proof failure');
 const bw=G.map((_,i)=>baseWitness(i)),witnesses=[];
 for(const o of source){
  const a=Array(t+5).fill(0),b=bw[o.kind==='leaf'?0:o.original];
  for(let j=1;j<=4;j++)a[j]=b[j];
  if(o.kind==='leaf')for(const [v,bit]of o.path)a[v]=bit;
  if(evalC(o.clause,a)||!source.every(y=>y.id===o.id||evalC(y.clause,a)))throw Error('bad deletion witness');
  for(let j=0;j<o.clause.length;j++){const f=o.clause.slice();f[j]=-f[j];if(!evalC(f,a))throw Error('bad sign control')}
  witnesses.push(a.slice(1).join(''));
 }
 const dimacs='p cnf '+(4+t)+' '+source.length+'\n'+source.map(o=>o.clause.join(' ')+' 0\n').join('');
 return {t,n:4+t,m:source.length,Nbits:dimacs.length*8,q:nodes.length,
  sourceLiterals:source.reduce((a,o)=>a+o.clause.length,0),
  maxWidth:Math.max(...source.map(o=>o.clause.length)),
  source:source.map(o=>o.clause),nodes,witnesses,
  proofBytes:JSON.stringify({source:source.map(o=>o.clause),nodes}).length};
}
function verify(z){
 const seen=new Map(z.source.map((c,i)=>['s'+i,canon(c)]));
 for(let i=0;i<z.nodes.length;i++){
  const x=z.nodes[i];if(x.id!=='d'+i||x.rule!=='RES'||!seen.has(x.parents[0])||!seen.has(x.parents[1]))throw Error('invalid DAG');
  const c=res(seen.get(x.parents[0]),seen.get(x.parents[1]),x.pivot);
  if(JSON.stringify(c)!==JSON.stringify(x.clause))throw Error('wrong output');
  seen.set(x.id,c);
 }
 if(!z.nodes.length||seen.get(z.nodes.at(-1).id).length)throw Error('not contradiction');
 for(let i=0;i<z.m;i++){
  const a=Array.from('0'+z.witnesses[i],Number);
  if(evalC(z.source[i],a)||!z.source.every((c,j)=>j===i||evalC(c,a)))throw Error('bad deletion');
 }
}
const result={version:'LSPV3-SPLIT-GAP344/v1',
 R:'Rmix341 has RES and other unit-cost rules. Mixed optimum remains a one-node interval.',
 base_dependency:'LSPV2 MIXED-NONAFFINE-GAP342: W_Rmix341(G)=6',
 cases:[],corruptionsRejected:0};
for(const t of cases){
 const z=build(t);verify(z);
 if(t<=3){
  const bad=JSON.parse(JSON.stringify(z));bad.nodes[0].pivot=999;
  try{verify(bad);throw Error('accepted mutation')}catch(e){if(e.message==='accepted mutation')throw e;result.corruptionsRejected++}
 }
 const out={t,n:z.n,m:z.m,Nbits:z.Nbits,q:z.q,sourceLiterals:z.sourceLiterals,
 maxWidth:z.maxWidth,proofBytes:z.proofBytes,allDeletionWitnesses:true,allSignFlipsSAT:true};
 if(t<=3)out.sample={source:z.source,nodes:z.nodes,witnesses:z.witnesses};
 result.cases.push(out);
}
console.log(JSON.stringify(result,null,2));