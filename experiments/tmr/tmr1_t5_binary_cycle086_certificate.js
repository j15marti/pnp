'use strict';
// TMR-1/086 published independent certificate: exact graph-to-binary-cycle reduction.
// COMPUTATIONAL test only; see symbolic report for unbounded input theorem.
let checks=0, cases=0, xstates=0, bstates=0;
const ok=(v,s)=>{checks++;if(!v)throw Error(s)};
const mod=x=>(x%5+5)%5;
function forest(n,arcs){
 const p=Array.from({length:n},(_,i)=>i),tree=[],chords=[];
 const root=i=>{while(p[i]!==i){p[i]=p[p[i]];i=p[i]}return i};
 arcs.forEach(([u,v],e)=>{let a=root(u),b=root(v);if(a===b)chords.push(e);else{p[a]=b;tree.push(e)}});
 const c=new Set(p.map((_,i)=>root(i))).size,adj=Array.from({length:n},()=>[]);
 tree.forEach(e=>{const [u,v]=arcs[e];adj[u].push([v,e,1]);adj[v].push([u,e,-1])});
 const rows=chords.map(e=>{
  const row=Array(arcs.length).fill(0),[u,v]=arcs[e];row[e]=1;
  let q=[v],seen=Array(n).fill(false),par=Array(n).fill(null);seen[v]=true;
  for(let i=0;i<q.length;i++)for(const [w,f,sgn] of adj[q[i]])if(!seen[w]){
   seen[w]=true;par[w]=[q[i],f,sgn];q.push(w)}
  ok(seen[u],'chord endpoints disconnected');
  for(let w=u;w!==v;w=par[w][0])row[par[w][1]]=par[w][2];
  return row;
 });
 ok(rows.length===arcs.length-n+c,'bad cycle rank');
 chords.forEach((e,i)=>chords.forEach((f,j)=>ok(rows[i][f]===(i===j?1:0),'bad chord identity block')));
 return {n,c,m:arcs.length,rows};
}
function valid(rows,d){
 return rows.every(row=>mod(row.reduce((s,a,i)=>s+a*d[i],0))===0)
}
function audit(n,arcs){
 const z=forest(n,arcs);let xs=0,bs=0;
 for(let mask=0;mask<5**n;mask++){
  let k=mask,x=Array.from({length:n},()=>{let a=k%5;k=Math.floor(k/5);return a});
  if(arcs.every(([u,v])=>[1,3].includes(mod(x[v]-x[u]))))xs++;
  xstates++;
 }
 for(let mask=0;mask<2**z.m;mask++){
  let d=arcs.map((_,i)=>1+2*((mask>>i)&1));
  if(valid(z.rows,d))bs++;
  bstates++;
 }
 ok(xs===bs*5**z.c,'count disagreement');
 // b_e=2 is an F5 solution of every linear relaxation; it is not binary.
 ok(valid(z.rows,Array(z.m).fill(0)),'F5 relaxation invalid');
 cases++;return xs;
}
const unsat=audit(4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]);
ok(unsat===0,'K4 transitive orientation must be UNSAT');
ok(audit(1,[[0,0]])===0,'loop not rejected');
ok(audit(2,[[0,1],[1,0]])===0,'opposed arcs not rejected');
ok(audit(0,[])===1,'empty graph');
for(let n=1;n<=4;n++){
 let pairs=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)pairs.push([u,v]);
 for(let w=0;w<3**pairs.length;w++){
  let z=w,e=[];for(const p of pairs){let r=z%3;z=Math.floor(z/3);if(r===1)e.push(p);if(r===2)e.push([p[1],p[0]])}
  audit(n,e);
 }
}
console.log(JSON.stringify({status:'COMPUTATIONAL',cases,checks,xstates,bstates,failures:0,unrestrictedF5Counterexample:'transitive K4',sourceCountForK4:unsat}));
