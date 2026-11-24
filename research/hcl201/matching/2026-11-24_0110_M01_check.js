"use strict";
function run(){
 let seed=20261124;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 const basis=()=>new Map(), reduce=(B,x)=>{for(let i=x.toString(2).length-1;i>=0;i--)if((x&(1n<<BigInt(i)))&&B.has(i))x^=B.get(i);return x};
 const add=(B,x)=>{x=reduce(B,x);if(!x)return false;B.set(x.toString(2).length-1,x);return true};
 const affine=(C,W)=>{let B=basis();for(let c of C.cycles)add(B,reduce(W,c.d));return B};
 const graph=(n,r,edges)=>{let G=Array.from({length:n},()=>Array(n).fill(null));for(let [i,j,g] of edges)G[i][j]=BigInt(g);return {n,r,G}};
 function components({n,G}){
  let R=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>G[i][j]!==null||i===j));
  for(let k=0;k<n;k++)for(let i=0;i<n;i++)if(R[i][k])for(let j=0;j<n;j++)R[i][j] ||= R[k][j];
  let seen=new Set(),out=[];
  for(let root=0;root<n;root++)if(!seen.has(root)){
   const vs=Array.from({length:n},(_,i)=>i).filter(i=>R[root][i]&&R[i][root]);vs.forEach(v=>seen.add(v));
   const path=(s,t)=>{let q=[s],p=new Map([[s,null]]);for(let k=0;k<q.length&&!p.has(t);k++)for(let v of vs)if(G[q[k]][v]!==null&&!p.has(v)){p.set(v,q[k]);q.push(v)}let a=[t];while(a.at(-1)!==s)a.push(p.get(a.at(-1)));return a.reverse()};
   const from=new Map(vs.map(v=>[v,path(root,v)])),to=new Map(vs.map(v=>[v,path(v,root)]));
   let cycles=[],offset=vs.reduce((s,i)=>s^G[i][i],0n);
   const emit=walk=>{let stack=[],pos=new Map();for(let v of walk){if(pos.has(v)){let k=pos.get(v),cy=stack.slice(k);let d=0n;for(let j=0;j<cy.length;j++)d^=G[cy[j]][cy[(j+1)%cy.length]]^G[cy[j]][cy[j]];if(d)cycles.push({d,cy});for(let a of stack.slice(k+1))pos.delete(a);stack.length=k+1}else{pos.set(v,stack.length);stack.push(v)}}};
   for(let i of vs){emit([...from.get(i),...to.get(i).slice(1)]);for(let j of vs)if(G[i][j]!==null)emit([...from.get(i),j,...to.get(j).slice(1)])}
   out.push({vs,cycles,offset});
  }return out;
 }
 function peel(I){
  let C=components(I), W=basis(), chosen=[], offset=C.reduce((s,c)=>s^c.offset,0n), initial=C.map(c=>affine(c,W).size),rounds=0,queries=0;
  let rest=C.slice();while(true){let hit=-1,cy=null;for(let j=0;j<rest.length;j++){queries++;let a=affine(rest[j],W);if(a.size<=1){hit=j;cy=rest[j].cycles.find(c=>reduce(W,c.d))||null;break}}
   if(hit<0)break;const c=rest.splice(hit,1)[0];if(cy){chosen.push(cy);add(W,cy.d)}rounds++;
  }
  const full=basis();for(let d of W.values())add(full,d);for(let c of rest)for(let z of c.cycles)add(full,z.d);
  const decide=t=>{let z=t^offset;if(reduce(full,z))return "UNSAT";if(rest.length)return "OPEN";
   // Construct witness using tagged Gaussian basis; coefficients record original chosen cycles.
   let B=new Map();for(let j=0;j<chosen.length;j++){let d=chosen[j].d,k=1n<<BigInt(j);for(let i=I.r-1;i>=0;i--)if(d&(1n<<BigInt(i))){if(B.has(i)){let [a,b]=B.get(i);d^=a;k^=b}else{B.set(i,[d,k]);break}}}
   let mask=0n;for(let i=I.r-1;i>=0;i--)if(z&(1n<<BigInt(i))){let [a,b]=B.get(i);z^=a;mask^=b}if(z)throw Error("basis");
   let p=Array.from({length:I.n},(_,i)=>i);chosen.forEach((c,j)=>{if(mask&(1n<<BigInt(j)))c.cy.forEach((v,k)=>p[v]=c.cy[(k+1)%c.cy.length])});
   if(new Set(p).size!==I.n||p.some((j,i)=>I.G[i][j]===null)||p.reduce((s,j,i)=>s^I.G[i][j],0n)!==t)throw Error("witness");
   return "SAT";
  };
  return {C,W,full,rest,offset,initial,rounds,queries,decide};
 }
 function reference({n,G}){let S=new Set();function rec(i,used,s){if(i===n){S.add(s);return}for(let j=0;j<n;j++)if(!(used&(1n<<BigInt(j)))&&G[i][j]!==null)rec(i+1,used|(1n<<BigInt(j)),s^G[i][j])}rec(0,0n,0n);return S}
 function check(I,stats){let P=peel(I),S=reference(I),B=basis();for(let s of S)add(B,s^P.offset);if(B.size!==P.full.size||[...B.values()].some(x=>reduce(P.full,x)))throw Error("hull");stats.instances++;if(P.rest.length===0)stats.closed++;for(let t=0n;t<(1n<<BigInt(I.r));t++){let a=P.decide(t),v=S.has(t);stats.targets++;if(a==="OPEN")stats.open++;else{if((a==="SAT")!==v)throw Error("decision");stats[a.toLowerCase()]++}}return {rank:B.size,remaining:P.rest.length,initial:P.initial,support:[...S].map(String).sort()}}
 let stats={instances:0,closed:0,targets:0,open:0,sat:0,unsat:0};
 for(let k=0;k<240;k++){let n=2+rnd(6),r=1+rnd(6),edges=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i===j||rnd(100)<35)edges.push([i,j,rnd(1<<r)]);check(graph(n,r,edges),stats)}
 // Three perfect matchings, syndrome set {0,1,2}. Diagonal + two transpositions sharing vertex 0.
 const tri=[[0,0,0],[1,1,0],[2,2,0],[0,1,1],[1,0,0],[0,2,2],[2,0,0]];
 let hole=check(graph(3,2,tri),stats);
 // Add one rank-one square tagged 1, attached by a one-way edge (not allowed in a PM).
 const extra=[[3,3,0],[4,4,0],[3,4,1],[4,3,0],[2,3,0]];
 let cascade=check(graph(5,2,[...tri,...extra]),stats);
 // Independent rank-one SCCs with graph connected by one-way edges; all target directions independent.
 let scaling=[];for(let h of [4,8,16,32,64]){let edges=[];for(let k=0;k<h;k++){let i=2*k,j=i+1;edges.push([i,i,0],[j,j,0],[i,j,1n<<BigInt(k)],[j,i,0]);if(k)edges.push([i-1,i,0])}let I=graph(2*h,h+1,edges),P=peel(I);let a=P.decide((1n<<BigInt(h))-1n),b=P.decide(1n<<BigInt(h));if(a!=="SAT"||b!=="UNSAT"||P.rest.length)throw Error("scale");scaling.push({h,vertices:4*h,rank:P.W.size,remaining:P.rest.length,componentRankChecks:P.queries,sat:a,unsat:b})}
 return {seed:20261124,stats,hole,cascade,scaling,scope:"Bipartite graphs with supplied diagonal perfect matching; SCC/cycle span, quotient peeling and explicit SAT witness tested. General-graph Lovasz/CPM implementation not executed."};
}
console.log(JSON.stringify(run(),null,2));
