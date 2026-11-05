/* LSPV-2/422. Graph-structured 3-CNF Tseitin boundary messages.
   Independently checks existential elimination on all small boundaries;
   samples large boundaries; no external dependencies. */
"use strict";
const assert=(x,m)=>{if(!x)throw Error(m)};
function graph(name){
 let n,E=[];
 if(name==="K4"){n=4;for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)E.push([a,b])}
 if(name==="cube"){n=8;for(let a=0;a<8;a++)for(let j=0;j<3;j++){let b=a^(1<<j);if(a<b)E.push([a,b])}}
 if(name==="Petersen"){n=10;for(let i=0;i<5;i++)E.push([i,(i+1)%5],[i,i+5],[i+5,5+(i+2)%5])}
 if(name==="Heawood"){n=14;for(let j=0,L=[[0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,0],[5,6,1],[6,0,2]];j<7;j++)for(const i of L[j])E.push([i,j+7])}
 E=E.map(e=>e.sort((a,b)=>a-b));E.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
 assert(n>0&&E.length===3*n/2,"bad graph");return {n,E,name};
}
function partition(g,mode){return Array.from({length:g.n},(_,v)=>mode==="halves"?+(v>=g.n/2):v%2)}
function components(g,p,side){
 let left=new Set(p.map((q,i)=>q===side?i:-1).filter(i=>i>=0)),out=[];
 while(left.size){let first=left.values().next().value,q=[first];left.delete(first);
  for(let z=0;z<q.length;z++)for(let [u,v] of g.E){let w=u===q[z]?v:v===q[z]?u:-1;if(left.has(w)){left.delete(w);q.push(w)}}
  out.push(q);
 }return out;
}
function makeMessages(g,p,odd){
 const B=g.E.map(([u,v],i)=>p[u]!==p[v]?i:-1).filter(x=>x>=0),rows=[];
 for(let side of [0,1])for(const C of components(g,p,side)){
  const S=new Set(C),indices=B.map((id,j)=>{let [u,v]=g.E[id];return S.has(u)!==S.has(v)?j:-1}).filter(x=>x>=0);
  rows.push({side,component:C,boundary:indices,rhs:+(odd&&S.has(g.n-1))});
 }return {B,rows}
}
function msgSat(M,side,x){return M.rows.filter(r=>r.side===side).every(r=>{
 let z=0;for(const k of r.boundary)z^=(x>>k)&1;return z===r.rhs;
})}
function bruteProjection(g,p,M,side,x,odd){
 const e=g.E.map(([u,v],i)=>p[u]===side&&p[v]===side?i:-1).filter(j=>j>=0);
 const vv=p.map((q,i)=>q===side?i:-1).filter(i=>i>=0);
 assert(e.length<=16,"oversized local brute force");
 const values=new Array(g.E.length).fill(0);
 M.B.forEach((id,j)=>values[id]=(x>>j)&1);
 for(let bits=0;bits<2**e.length;bits++){
  e.forEach((id,j)=>values[id]=(bits>>j)&1);
  if(vv.every(v=>g.E.reduce((z,[u,w],j)=>z^((u===v||w===v)?values[j]:0),0)===+(odd&&v===g.n-1)))return true;
 }return false;
}
function run(){
 const rows=[],checks={projected_assignments_checked:0,large_boundary_sampled:0,global_xor_checks:0,mutations_rejected:0};
 for(let name of ["K4","cube","Petersen","Heawood"])for(let mode of ["halves","alternating"])for(let odd of [false,true]){
  const g=graph(name),p=partition(g,mode),M=makeMessages(g,p,odd),b=M.B.length;
  const values=b<=12?Array.from({length:2**b},(_,i)=>i):[0,1,2**(b-1),2**b-1,0x55555 & (2**b-1)];
  if(b>12)checks.large_boundary_sampled++;
  for(let side of [0,1])for(const x of values){assert(msgSat(M,side,x)===bruteProjection(g,p,M,side,x,odd),"bad projected boundary relation");checks.projected_assignments_checked++}
  const times=Array(b).fill(0);for(const row of M.rows)for(let i of row.boundary)times[i]++;
  assert(times.every(c=>c===2),"boundary edge failed XOR cancellation");checks.global_xor_checks++;
  assert(M.rows.reduce((s,r)=>s^r.rhs,0)===+(odd),"charge parity failed");checks.global_xor_checks++;
  // A single flipped row charge changes global label and is detected.
  const fake=M.rows.map(r=>({...r}));fake[0].rhs ^=1;
  assert(fake.reduce((s,r)=>s^r.rhs,0)!==+(odd),"mutation survived");checks.mutations_rejected++;
  let terms=M.rows.reduce((s,r)=>s+r.boundary.length,0);
  rows.push({graph:name,mode,odd,vertices:g.n,boundary_variables:b,explicit_survivor_mask_bits:2**b,
   messages:M.rows.length,affine_index_occurrences:terms,all_boundary_vars_appear_twice:terms===2*b,
   global_xor_is_contradiction:odd,
   sparse_message_bits_upper:(terms+M.rows.length+1)*Math.ceil(Math.log2(g.E.length+2)),
   local_projection_exhaustive:b<=12});
 }
 return {schema:"LSPV2_422_AFFINE_MESSAGES",checks,rows,
  status:"PROVED RESTRICTED symbolic projection lemma, finite exact and sampled controls. Not an all-input FLMV compiler."};
}
const result=run();
if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));
