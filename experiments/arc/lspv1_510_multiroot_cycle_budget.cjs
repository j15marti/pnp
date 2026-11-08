"use strict";
// LSPV-1/510: multi-goal binary proof DAG exact excess decomposition.
// Ordinary Resolution fixture from LSPV-1/507; abstract fixture from /509.
// No historical R_mix341 checker or arbitrary-algorithm hardness claim.
const S=[[1,2,-4],[1,-2,-4],[-1,2,-4],[-1,-2,4],[2,3,-5],[2,-3,5],[-2,3,5],[-2,-3,-5],[1,5,-6],[1,-5,-6],[-1,5,-6],[-1,-5,6],[4,6,-7],[4,-6,7],[-4,6,7],[-4,-6,-7]];
const Q=[[-1,-3,7],[1,-7],[3,-7]];
const R=[["S13","S02",4],["S10","S07",5],["R01","R02",2],["S11","S05",-5],["S03","S14",4],["R04","R05",2],["R03","R06",-6],["S09","S08",-5],["R08","S12",-6],["S00","S01",2],["R09","R10",4],["S02","S12",-4],["S06","S11",5],["R12","R13",2],["S03","S15",4],["S04","S10",-5],["R15","R16",-2],["R14","R17",6],["R18","R11",-1]];
function norm(xs){return [...new Set(xs)].sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a)}
function calc(rows,goals,checkRes){
 const cls={};S.forEach((c,i)=>cls['S'+String(i).padStart(2,'0')]=norm(c));
 const parents={},depth={};Object.keys(cls).forEach(x=>depth[x]=0);
 rows.forEach((row,i)=>{
  let [a,b,p]=row,id=(checkRes?'R':'M')+String(i+1).padStart(2,'0');
  if(!(a in cls)||!(b in cls)||a===b)throw Error('bad reference or cycle');
  if(checkRes){let A=cls[a],B=cls[b];if(A.includes(-p)&&B.includes(p))[A,B]=[B,A];
   if(!A.includes(p)||!B.includes(-p))throw Error('bad pivot');
   const C=norm([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]);
   if(C.some(x=>C.includes(-x)))throw Error('tautology');cls[id]=C;
  }else cls[id]=[];
  parents[id]=[a,b];depth[id]=1+Math.max(depth[a],depth[b]);
 });
 if(goals.some(x=>!(x in cls)))throw Error('missing goal');
 if(checkRes&&JSON.stringify(goals.map(x=>cls[x]))!==JSON.stringify(Q))throw Error('wrong goal');
 const seen=new Set(goals),todo=[...goals];while(todo.length){for(const p of parents[todo.pop()]||[])if(!seen.has(p)){seen.add(p);todo.push(p)}}
 const m=[...seen].filter(x=>x[0]==='S').length,q=seen.size-m;
 const E=[];for(const [v,P]of Object.entries(parents))if(seen.has(v))for(const a of P)E.push([v,a]);
 const adj={};for(const v of seen)adj[v]=new Set();for(const [v,a]of E){adj[v].add(a);adj[a].add(v)}
 let c=0,left=new Set(seen);while(left.size){c++;let stack=[left.values().next().value];left.delete(stack[0]);while(stack.length)for(const z of adj[stack.pop()])if(left.delete(z))stack.push(z)}
 const mu=E.length-seen.size+c,delta=[...seen].filter(x=>x[0]!=='S').reduce((a,x)=>a+2-parents[x].length,0);
 if(q!==m-c+mu+delta||mu<0||delta<0)throw Error('cycle identity');
 return {m,q,edges:E.length,c,mu,delta,depth:Math.max(...goals.map(x=>depth[x]||0))};
}
function run(){
 const legal=calc(R,['R07','R11','R19'],true);
 if(JSON.stringify([legal.m,legal.q,legal.c,legal.mu,legal.delta,legal.depth])!==JSON.stringify([16,19,1,4,0,4]))throw Error('legal fixture');
 const rows=[];function merge(a,b){rows.push([a,b]);return'M'+String(rows.length).padStart(2,'0')}
 function chain(xs){return xs.slice(1).reduce((x,y)=>merge(x,y),xs[0])}
 const s=x=>'S'+String(x).padStart(2,'0');const A=chain([2,3,10,11].map(s)),B=chain([0,1,8,9,12].map(s));
 const G=[chain([A,...[5,7,13,14].map(s)]),B,chain([A,B,...[4,6,15].map(s)])];
 const abstract=calc(rows,G,false);
 if(JSON.stringify([abstract.m,abstract.q,abstract.c,abstract.mu,abstract.delta])!==JSON.stringify([16,15,1,0,0]))throw Error('abstract fixture');
 let rejected=0;for(const bad of [R.slice(0,2).concat([['R01','R02',7]],R.slice(3)),[['R05','S02',4],...R.slice(1)],R.slice(0,-1)]){
 try{calc(bad,['R07','R11','R19'],true)}catch(e){rejected++}
 }if(rejected!==3)throw Error('hostile checks');
 return {status:'PROVED_RESTRICTED_EXACT_GRAPH_IDENTITY',theorem:'q=m-c+mu+delta',legal19:legal,abstract15:abstract,rejected_controls:rejected,historical_checker_executed:false};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));module.exports={run,calc};
