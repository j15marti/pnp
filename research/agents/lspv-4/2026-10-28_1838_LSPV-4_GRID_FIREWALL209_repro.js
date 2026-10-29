"use strict";
// LSPV-4 GRID FIREWALL209 compact dependency-free Node reproducer.
// Run: node 2026-10-28_1838_LSPV-4_GRID_FIREWALL209_repro.js
function main() {
  let assertions=0;
  function ok(x,why) { assertions++; if(!x) throw Error(why || "failed"); }
  const id=(layer,r,c,L)=>1+layer*L*L+r*L+c;
  function grid(L) {
    const C=[];
    for(let r=0;r<L;r++) for(let c=0;c<L;c++) {
      const a=id(0,r,c,L);
      const b=id(1,r,c,L), d=id(1,(r+1)%L,c,L);
      const e=id(2,r,c,L), f=id(2,r,(c+1)%L,L);
      C.push([a,b,e],[a,d,e],[-a,-b,-f],[-a,-d,-f]);
    }
    return C;
  }
  function graph(C,n) {
    const adj=Array.from({length:n+1},()=>new Set());
    for(const clause of C) for(let i=0;i<3;i++)
      for(let j=0;j<3;j++) if(i!==j) adj[Math.abs(clause[i])].add(Math.abs(clause[j]));
    return adj;
  }
  function width(adj,order) {
    const future=new Set(order), seen=new Set();
    let w=0;
    for(const v of order) {
      future.delete(v); seen.add(v);
      let k=0;
      for(const u of seen) for(const nb of adj[u])
        if(future.has(nb)) { k++; break; }
      w=Math.max(w,k);
    }
    return w;
  }
  function minWidth(adj) {
    const n=adj.length-1;
    ok(n===12,"exact subset search restricted to 12 vertices");
    const full=(1<<n)-1, dp=new Uint8Array(full+1), masks=[];
    for(let v=1;v<=n;v++) {
      let bits=0; for(const x of adj[v]) bits|=1<<(x-1); masks.push(bits);
    }
    for(let S=1;S<=full;S++) {
      const rem=full^S;
      let boundary=0;
      for(let j=0;j<n;j++) if((S&(1<<j))&&(masks[j]&rem)) boundary++;
      let best=n+1;
      for(let bits=S;bits;) {
        const lb=bits&-bits;
        best=Math.min(best,dp[S^lb]);
        bits^=lb;
      }
      dp[S]=Math.max(boundary,best);
    }
    return dp[full];
  }
  let clausesTotal=0,variablesTotal=0;
  const rows=[];
  for(const L of [2,3,4,5,6,8,12]) {
    const n=3*L*L, C=grid(L), adj=graph(C,n);
    ok(C.length===4*L*L,"clause count");
    const positive=new Int32Array(n+1),negative=new Int32Array(n+1);
    for(const c of C) {
      ok(new Set(c.map(Math.abs)).size===3,"proper clause");
      for(const lit of c) (lit>0?positive:negative)[Math.abs(lit)]++;
      ok(c.some(lit=>Math.abs(lit)<=L*L),"A-layer hits clause");
    }
    for(let v=1;v<=n;v++) ok(positive[v]===2 && negative[v]===2,"signed exact22");
    const visited=new Set([1]),stack=[1];
    while(stack.length) for(const x of adj[stack.pop()])
      if(!visited.has(x)){visited.add(x);stack.push(x);}
    ok(visited.size===n,"connected");
    const internal=new Set();
    let gridEdges=0;
    for(let r=0;r<L;r++) for(let c=0;c<L;c++) {
      const a=id(0,r,c,L);
      if(r+1<L) {
        const q=id(1,r+1,c,L), v=id(0,r+1,c,L);
        ok(adj[a].has(q)&&adj[q].has(v)&&!internal.has(q),"B path");
        internal.add(q); gridEdges++;
      }
      if(c+1<L) {
        const q=id(2,r,c+1,L), v=id(0,r,c+1,L);
        ok(adj[a].has(q)&&adj[q].has(v)&&!internal.has(q),"C path");
        internal.add(q); gridEdges++;
      }
    }
    ok(gridEdges===2*L*(L-1),"subdivided grid");
    const A=new Set(Array.from({length:L*L},(_,j)=>j+1));
    for(const c of C)
      ok(c.some(lit=>lit>0&&A.has(lit)) || c.some(lit=>lit<0&&A.has(-lit)),"A hits");
    // All positive-type clauses contain true A; negative-type clauses contain false B,C.
    for(let j=0;j<C.length;j++){
      const c=C[j];
      ok(c.some(lit=>lit>0&&A.has(lit)||lit<0&&!A.has(-lit)),"explicit SAT witness");
    }
    const order=[];
    for(let r=0;r<L;r++)for(let c=0;c<L;c++)for(let layer=0;layer<3;layer++)
      order.push(id(layer,r,c,L));
    const w=width(adj,order);
    ok(w>=L-1&&w<=9*L,"all-orders lower bound / cell upper test");
    const mw=L===2?minWidth(adj):null;
    if(mw!==null) ok(mw===6,"independent exact n=12 subset calculation");
    clausesTotal+=C.length; variablesTotal+=n;
    rows.push({L,n,clauses:C.length,gridEdges,lowerBoundEveryOrdering:L-1,
      cellMajorWidth:w,exactMinimumIfComputed:mw});
  }
  let projectionAssignments=0;
  for(let t=1;t<=4;t++) for(let mask=0;mask<(1<<(4*t));mask++) {
    const A=[],B=[];
    for(let i=0;i<t;i++) {
      A.push(!!((mask>>(2*i))&1 || (mask>>(2*i+1))&1));
      B.push(!!((mask>>(2*t+2*i))&1 || (mask>>(2*t+2*i+1))&1));
    }
    const existsZ=A.every(Boolean)||B.every(Boolean);
    const pairwise=A.every(a=>B.every(b=>a||b));
    ok(existsZ===pairwise,"existential resolution / compact circuit");
    projectionAssignments++;
  }
  ok(projectionAssignments===69904,"identity assignment total");
  return {status:"PASS",assertionGroups:assertions,gridSizes:rows,
    clausesTotal,variablesTotal,projectionAssignments,
    notes:["Grid-width is syntactic, not a SAT runtime lower bound.",
      "Finite checks do not replace the all-size crossing-family proof.",
      "Every displayed grid formula has the explicit A=1 B=C=0 witness."]};
}
if(typeof process!=="undefined"&&process.stdout)
  process.stdout.write(JSON.stringify(main(),null,2)+"\n");
