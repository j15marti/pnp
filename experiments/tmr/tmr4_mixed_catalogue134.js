"use strict";
// Self-contained Node 22/V8 executable audit, exact BigInt rational arithmetic.
const audit = function audit() {
 "use strict";
 let assertions=0,paid=0,free=0,negativeGamma=0,sccs=0,validCases=0;
 const check=(b,m)=>{assertions++;if(!b)throw Error(m);};
 const pop=n=>{let c=0;while(n){n&=n-1;c++;}return c};
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let z=a%b;a=b;b=z;}return a||1n};
 const Q=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}if(!b)throw Error("zero divisor");let d=gcd(a,b);return [a/d,b/d]};
 const plus=(x,y)=>Q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
 const minus=(x,y)=>Q(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
 const times=(x,y)=>Q(x[0]*y[0],x[1]*y[1]);
 const over=(x,y)=>Q(x[0]*y[1],x[1]*y[0]);
 const le=(x,y)=>x[0]*y[1]<=y[0]*x[1];
 const eq=(x,y)=>x[0]*y[1]===y[0]*x[1];
 const fmt=x=>x[1]===1n?x[0].toString():x[0]+"/"+x[1];
 const gauss=(rows)=>{
  let a=rows.map(r=>r.map(x=>Q(x)));
  for(let k=0;k<3;k++){let j=k;while(j<3&&a[j][k][0]===0n)j++;if(j===3)return null;
   [a[k],a[j]]=[a[j],a[k]];let pv=a[k][k];for(let c=k;c<4;c++)a[k][c]=over(a[k][c],pv);
   for(let i=0;i<3;i++)if(i!==k){let f=a[i][k];for(let c=k;c<4;c++)a[i][c]=minus(a[i][c],times(f,a[k][c]));}
  }return a.map(x=>x[3]);
 };
 const maxwidth=(t,B)=>Math.max(0,...B.filter(b=>b<=t));
 const cover=(U,E,memo)=>{if(!U)return 0;if(memo[U]!==undefined)return memo[U];
  let v=99999;for(const S of E)if(U&S)v=Math.min(v,1+cover(U&~S,E,memo));if(v===99999)throw Error("uncovered");return memo[U]=v;};
 const key=s=>[s.P,s.U,s.h,s.v].join("/");
 const cases=[],seven=["CNF","XOR","SEP","FUS","Gamma","Interface","Machine"];
 let featured=null;
 function run(G,q,E,B,label,feature=false) {
  check(E.every(S=>S>0&&S<(1<<q)),"invalid batch");
  const J=(1<<q)-1,D=(1<<G)-1;
  check(E.reduce((x,y)=>x|y,0)===J,"uncovered family");
  check(B.every(b=>b>=1&&b<=G&&Number.isInteger(b)),"invalid width");
  validCases++;
  const memo=[0];
  function potential(s){let t=G-pop(s.P),credit=(s.h&&s.U===J)?maxwidth(t,B):0;
   return [0,0,cover(s.U,E,memo),0,t-credit,0,s.h];}
  const states=[];
  for(let P=0;P<=D;P++)for(let U=0;U<=J;U++)for(let v=0;v<2;v++)states.push({P,U,h:1,v});
  for(let v=0;v<2;v++)states.push({P:D,U:0,h:0,v});
  const loc=new Map(states.map((s,i)=>[key(s),i]));
  const out=states.map(()=>[]),edges=[];
  function edge(i,s,rule,cost){
   let j=loc.get(key(s));check(j!==undefined,`unknown successor ${rule}`);
   const x=potential(states[i]),y=potential(s),delta=x.map((v,k)=>v-y[k]);
   check(delta[2]+delta[4]+delta[6]<=cost,`tariff ${label}/${rule} ${key(states[i])}`);
   if(delta[4]<0)negativeGamma++;
   if(cost){paid++;}else{free++;check(delta.every(z=>z===0),"zero-cost discount");}
   let e={i,j,cost,rule,delta};edges.push(e);out[i].push(e);
  }
  states.forEach((s,i)=>{
   edge(i,{...s,v:s.v^1},"VIEW",0);edge(i,s,"NOP",0);
   if(!s.h)return;
   for(let g=0;g<G;g++)if(!(s.P&(1<<g)))edge(i,{...s,P:s.P|(1<<g)},"CHECK:"+g,1);
   if(s.P===D)for(let S of E)if(S&s.U)edge(i,{...s,U:s.U&~S},"BATCH:"+S,1);
   let t=G-pop(s.P);
   if(s.U===J&&B.includes(t))for(let S of E)edge(i,{...s,P:D,U:J&~S},"FUSE:"+t+":"+S,1);
   if(s.P===D&&s.U===0)edge(i,{...s,h:0},"HALT",1);
  });
  // Generic Tarjan SCC computed on actual zero-cost transition subgraph.
  let ix=0,num=0,st=[],on=Array(states.length).fill(false),d=Array(states.length).fill(-1),low=[],component=Array(states.length).fill(-1);
  function visit(v){d[v]=low[v]=ix++;st.push(v);on[v]=true;
   for(const e of out[v])if(!e.cost){let w=e.j;if(d[w]<0){visit(w);low[v]=Math.min(low[v],low[w]);}else if(on[w])low[v]=Math.min(low[v],d[w]);}
   if(low[v]===d[v]){let w;do{w=st.pop();on[w]=false;component[w]=num;}while(w!==v);num++;}
  }
  for(let i=0;i<states.length;i++)if(d[i]<0)visit(i);
  sccs+=num;
  const members=Array.from({length:num},()=>[]);
  states.forEach((s,i)=>members[component[i]].push(i));
  for(const m of members){check(m.length===2,"wrong zero SCC");
   check(states[m[0]].P===states[m[1]].P&&states[m[0]].U===states[m[1]].U&&states[m[0]].h===states[m[1]].h,"SCC merged paid state");}
  // Quotient simulation: every zero move maps to empty path; every paid move retains its cost.
  const adj=Array.from({length:num},()=>[]);
  for(const e of edges)if(e.cost){adj[component[e.i]].push([component[e.j],e.cost]);}
   else check(component[e.i]===component[e.j],"zero step not collapsed");
  // Independent shortest-path computation on all quotient states.
  const memoDist=Array(num).fill(null),busy=new Set();
  function shortest(k){if(memoDist[k]!==null)return memoDist[k];check(!busy.has(k),"paid cycle");busy.add(k);
   let s=states[members[k][0]],v=0;
   if(s.h){v=99999;for(let [j,c] of adj[k])v=Math.min(v,c+shortest(j));check(v!==99999,"unreachable goal");}
   busy.delete(k);return memoDist[k]=v;
  }
  for(let k=0;k<num;k++){let s=states[members[k][0]],v=potential(s);
   check(shortest(k)===v[2]+v[4]+v[6],`Bellman mismatch ${label} ${key(s)}`);}
  const initial={P:0,U:J,h:1,v:0},obj=potential(initial),value=obj[2]+obj[4]+obj[6];
  check(shortest(component[loc.get(key(initial))])===value,"initial path");
  check(value===G+cover(J,E,memo)+1-maxwidth(G,B),"catalogue closed form");
  // Exact-rational LP in the 3 active columns; all distinct legal tariff inequalities plus nonnegative weights.
  let distinct=new Map();
  for(const e of edges){let r=[e.delta[2],e.delta[4],e.delta[6],e.cost];distinct.set(r.join(","),r);}
  const constraints=[...distinct.values(),[-1,0,0,0],[0,-1,0,0],[0,0,-1,0]];
  const lhs=(r,x)=>plus(plus(times(Q(r[0]),x[0]),times(Q(r[1]),x[1])),times(Q(r[2]),x[2]));
  const feasible=x=>constraints.every(r=>le(lhs(r,x),Q(r[3])));
  const objective=x=>lhs([obj[2],obj[4],obj[6],0],x);
  const cert=[Q(1),Q(1),Q(1)];check(feasible(cert),"certificate violated");
  let opt=null,xopt=null,vertices=0;
  for(let i=0;i<constraints.length;i++)for(let j=i+1;j<constraints.length;j++)for(let k=j+1;k<constraints.length;k++){
   let x=gauss([constraints[i],constraints[j],constraints[k]]);
   if(!x||!feasible(x))continue;vertices++;
   let z=objective(x);if(opt===null||!le(z,opt)){opt=z;xopt=x;}
  }
  check(opt!==null&&eq(opt,Q(value))&&eq(objective(cert),opt),"LP optimum vs witness");
  const rec={label,G,q,E,B,states:states.length,scc:num,transitions:edges.length,paid:edges.filter(x=>x.cost).length,zero:edges.filter(x=>!x.cost).length,uniqueTariffRows:distinct.size,rationalLPVertices:vertices,optimalLambda:xopt.map(fmt),initialPotential:value,integerCover:cover(J,E,memo)};
  cases.push(rec);
  if(feature)featured={model:rec,columns:seven,fullTariffRows:edges.map(e=>({source:key(states[e.i]),target:key(states[e.j]),rule:e.rule,w:e.cost,delta:e.delta})),uniqueRows:[...distinct.values()]};
 }
 const params=[
  [1,1,[1],[1],"one"],
  [2,1,[1],[1],"two-b1"],
  [2,1,[1],[1,2],"two-catalogue"],
  [3,1,[1],[1,2,3],"three-all"],
  [3,3,[1,2,4],[1],"singleton"],
  [3,3,[3,5,6],[1,2],"triangle"],
  [3,3,[3,5,6],[3],"triangle-wide"],
  [4,3,[3,5,6],[1,3],"triangle-G4-B13",true],
  [4,3,[3,5,6],[1,2,3,4],"triangle-all"],
  [4,3,[1,2,4],[2,4],"single-G4-B24"],
  [4,3,[7],[1,2,4],"full-batch"],
  [4,2,[1,2],[2,3],"two-scales"],
  [3,7,[7,11,21,38,73,82,100],[1,2,3],"seven-scale-cover"]
 ];
 for(const x of params)run(...x);
 // Hostile operations are real only in explicitly expanded models: no CEGAR deletion.
 const J=3,E=[1,2],G=2,B=[1],memo=[0];
 const p=(P,U,h)=>{let t=G-pop(P),credit=h&&U===J?maxwidth(t,B):0;
  return [0,0,cover(U,E,memo),0,t-credit,0,h];};
 const hostile=(from,to,cost)=>{let delta=from.map((x,i)=>x-to[i]);return {delta,cost,chargedDrop:delta[2]+delta[4]+delta[6]};};
 const secondFuse=hostile(p(1,2,1),p(3,0,1),1);
 const freeBatch=hostile(p(3,1,1),p(3,0,1),0);
 const widerFuse=hostile(p(0,3,1),p(3,2,1),1);
 check(secondFuse.chargedDrop===2&&freeBatch.chargedDrop===1&&widerFuse.chargedDrop===2,"expected falsifiers missing");
 let reject=false;try{run(2,2,[1],[1],"INVALID");}catch(e){reject=String(e).includes("uncovered family");}
 check(reject,"uncovered grammar not rejected");
 return {raw:{name:"TMR-4/048 mixed catalogue of last-b fused check and batch events",timestamp:"2026-11-15 08:47 PST",scope:"Fully preauthenticated shared-gate record calculus; not a physical SAT machine",verification:"Native V8 BigInt exact rational three-variable LP, generic zero SCC quotient, independent paid shortest-path recursion",validCases,assertions,paidRows:paid,zeroRows:free,zeroSCCs:sccs,negativeGammaRows:negativeGamma,zeroFailures:true,malformedRejected:reject,hostile:{secondFuse,freeBatch,widerFuse},cases},matrix:featured};
};
const result = audit();
console.log(JSON.stringify(result.raw,null,2));
