"use strict";
// LSPV-1/476: source-exact split-clause alias projection, ordinary Resolution only.
const assert=(p,m)=>{if(!p)throw Error(m||"assertion failed");checks++};
let checks=0;
const norm=a=>{const t=[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);return t.some(x=>t.includes(-x))?null:t};
const key=a=>a===null?"TOP":a.join(",");
const subset=(a,b)=>a!==null&&b!==null&&a.every(x=>b.includes(x));
function res(a,b,p){
  if(a===null||b===null||!a.includes(p)||!b.includes(-p))throw Error("wrong pivot");
  return norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
}
function graph(kind){
 if(kind==="K4")return [4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]];
 if(kind==="K33")return [6,[[0,3],[0,4],[0,5],[1,3],[1,4],[1,5],[2,3],[2,4],[2,5]]];
 if(kind==="cube")return [8,[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]]];
 throw Error("unknown graph");
}
function tseitin(kind,odd=true){
 const [h,E]=graph(kind),F=[];
 for(let v=0;v<h;v++){
  const is=E.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
  assert(is.length===3,"noncubic");
  for(let mask=0;mask<8;mask++){
   const parity=((mask&1)!==0)^((mask&2)!==0)^((mask&4)!==0);
   if(Number(parity)!==(odd&&v===0?1:0)){
    const c=norm(is.map((id,j)=>(mask&(1<<j))?-id:id));assert(c!==null&&c.length===3);
    F.push(c);
   }
  }
 }
 return {h,E,F};
}
function build(F,nvars){
 const source=[],srcMap=new Map(),clauses=[],nodes=[],pool=[];
 const add=(clause,parents,pivot,sourceIndex)=>{
  assert(clause!==null,"taut node");
  const id=nodes.length;nodes.push({clause,parents,pivot,sourceIndex});
  return id;
 };
 for(let i=0;i<F.length;i++){
  const [l1,l2,l3]=F[i],a=nvars+i+1;
  source.push(norm([l1,l2,a]),norm([l1,l3,-a]));
 }
 source.forEach((c,i)=>add(c,null,null,i));
 for(let i=0;i<F.length;i++){
  const id=add(res(source[2*i],source[2*i+1],nvars+i+1),[2*i,2*i+1],nvars+i+1,null);
  assert(key(nodes[id].clause)===key(F[i]),"split resolvent differs");
  pool.push(id);
 }
 // Deterministic Davis-Putnam elimination. Every generated node is checked.
 let empty=-1;
 for(let x=1;x<=nvars && empty<0;x++){
  const pos=pool.filter(id=>nodes[id].clause.includes(x));
  const neg=pool.filter(id=>nodes[id].clause.includes(-x));
  const next=pool.filter(id=>!nodes[id].clause.includes(x)&&!nodes[id].clause.includes(-x));
  const seen=new Set(next.map(id=>key(nodes[id].clause)));
  for(const u of pos)for(const v of neg){
   const c=res(nodes[u].clause,nodes[v].clause,x);if(c===null)continue;
   const k=key(c);if(seen.has(k))continue;seen.add(k);
   const id=add(c,[u,v],x,null);next.push(id);
   if(c.length===0){empty=id;break;}
  }
  pool.splice(0,pool.length,...next);
 }
 assert(empty>=0&&nodes[empty].clause.length===0,"UNSAT refutation missing");
 return {source,nodes,empty,nvars};
}
function project(F,P){
 const fkeys=new Map(F.map((c,i)=>[key(c),i])),memo=[],out=[];
 const sigma=p=>Math.abs(p)<=P.nvars?p: (p>0?F[Math.abs(p)-P.nvars-1][2]:-F[Math.abs(p)-P.nvars-1][2]);
 const sub=c=>norm(c.map(sigma));
 function add(c,parents,pivot,src){
  const id=out.length;out.push({clause:c,parents,pivot,src});return id;
 }
 for(let i=0;i<F.length;i++)add(F[i],null,null,i);
 for(let i=0;i<P.nodes.length;i++){
  const node=P.nodes[i],target=sub(node.clause);
  if(node.parents===null){
   if(target===null){memo.push(null);continue;}
   assert(fkeys.has(key(target)),"transformed source not from F");
   memo.push(fkeys.get(key(target)));continue;
  }
  if(target===null){memo.push(null);continue;}
  const [u,v]=node.parents,A=memo[u],B=memo[v];
  if(A!==null && subset(out[A].clause,target)){memo.push(A);continue;}
  if(B!==null && subset(out[B].clause,target)){memo.push(B);continue;}
  assert(A!==null&&B!==null,"both parents top, non-top conclusion");
  const q=sigma(node.pivot),a=out[A].clause,b=out[B].clause;
  assert(a.includes(q)&&b.includes(-q),"projected pivot unsupported");
  const c=res(a,b,q);
  assert(c!==null&&subset(c,target),"projected resolvent mismatch");
  memo.push(add(c,[A,B],q,null));
 }
 let root=memo[P.empty];assert(root!==null&&out[root].clause.length===0);
 const visited=new Set();
 function walk(i){if(visited.has(i))return;visited.add(i);if(out[i].parents)out[i].parents.forEach(walk);}
 walk(root);
 for(const i of visited){const n=out[i];if(n.parents){const [u,v]=n.parents;assert(key(res(out[u].clause,out[v].clause,n.pivot))===key(n.clause),"illegal output RES");}}
 const paid=[...visited].filter(i=>out[i].parents!==null).length;
 const originalPaid=P.nodes.filter(n=>n.parents!==null).length;
 assert(paid<=originalPaid,"projection increased work");
 return {paid,originalPaid,usedSources:[...visited].filter(i=>out[i].sourceIndex!==undefined),proofNodes:out.length,root};
}
function isSat(F,n){
 for(let k=0;k<(1<<n);k++)if(F.every(c=>c.some(l=>l>0?((k>>(l-1))&1)===1:((k>>(-l-1))&1)===0)))return true;
 return false;
}
function main(){
 const results=[];
 for(const kind of ["K4","K33","cube"]){
  const {h,E,F}=tseitin(kind,true);const P=build(F,E.length),r=project(F,P);
  assert(!isSat(F,E.length),"odd Tseitin SAT");
  const even=tseitin(kind,false);
  assert(isSat(even.F,E.length),"even Tseitin UNSAT");
  for(let i=0;i<F.length;i++){
   const a=E.length+i+1,[l1,l2,l3]=F[i];
   assert(key(norm([l1,l2,l3]))===key(norm([l1,l2,l3])),"identity");
   const p=P.source[2*i],q=P.source[2*i+1];
   assert(key(res(p,q,a))===key(F[i]),"orientation");
   assert(key(norm(p.map(x=>Math.abs(x)===a?(x>0?l3:-l3):x)))===key(F[i]),"alias first");
   assert(norm(q.map(x=>Math.abs(x)===a?(x>0?l3:-l3):x))===null,"alias second");
  }
  assert(h>=4&&F.length===4*h&&P.source.length===8*h,"encoding dimensions");
  results.push({graph:kind,h,variables:E.length,source3CNF:4*h,splitVariables:E.length+4*h,split3CNF:8*h,originalPaid:r.paid,splitProofPaid:r.originalPaid,projectionNodes:r.proofNodes,idealMixedUpper:8*h-1});
 }
 // Corruptions: wrong signed pivot, malformed source, altered clause/split.
 let rejected=0;
 const {E,F}=tseitin("K4");const Q=build(F,E.length);
 for(const mutate of [
  P=>{P.nodes[P.empty].pivot=9999;},
  P=>{P.nodes[P.empty].parents=[0,1];},
  P=>{P.source[0]=norm([1]);P.nodes[0].clause=P.source[0];},
 ]){
  const P=JSON.parse(JSON.stringify(Q));mutate(P);
  try{
   // An adversarial proof requires BOTH input legality and projection checking.
   for(let i=0;i<P.nodes.length;i++){const n=P.nodes[i];if(n.parents){const [u,v]=n.parents;assert(key(res(P.nodes[u].clause,P.nodes[v].clause,n.pivot))===key(n.clause),"corrupted input proof");}}
   project(F,P);
  }catch(e){rejected++;}
 }
 assert(rejected===3,"corruptions escaped");
 return {status:"PASS",checks,results,corruptedRejected:rejected,model:"ordinary source-authenticated DAG Resolution; NOT historical R_mix341 accepted bytes"};
}

console.log(JSON.stringify(main(),null,2));
