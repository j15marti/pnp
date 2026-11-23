"use strict";
// Node.js, dependency-free. Run: node 2026-11-23_1135_conflict_matching.js
function experiment(){
  let seed=42819; const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
  const check=(x,m)=>{if(!x)throw Error(m)};
  function reach(n,B){
    const idx=l=>l>0?2*(l-1):2*(-l-1)+1;
    const a=Array.from({length:2*n},()=>[]);
    for(const c of B){if(!c.length)return null;let u=idx(c[0]),v=idx(c[c.length-1]);a[u^1].push(v);a[v^1].push(u)}
    const R=a.map((_,i)=>{let seen=new Set([i]),q=[i];for(let j=0;j<q.length;j++)for(const v of a[q[j]])if(!seen.has(v)){seen.add(v);q.push(v)}return seen});
    for(let i=0;i<2*n;i+=2)if(R[i].has(i+1)&&R[i+1].has(i))return null;
    return {ok:l=>!R[idx(l)].has(idx(-l)),bad:(l,m)=>R[idx(l)].has(idx(-m))};
  }
  function graph(n,B,C){
    let R=reach(n,B);if(!R)return null;
    let groups=[],lits=[],owner=[],adj=[];
    for(let i=0;i<C.length;i++){let g=[];for(const l of C[i])if(R.ok(l)){g.push(lits.length);lits.push(l);owner.push(i);adj.push(new Set())}groups.push(g)}
    for(let u=0;u<lits.length;u++)for(let v=0;v<u;v++)if(owner[u]!==owner[v]&&R.bad(lits[u],lits[v])){adj[u].add(v);adj[v].add(u)}
    return {groups,lits,owner,adj};
  }
  function inspect(G,groups){
    const V=groups.flat(),allowed=new Set(V),comp=new Map(),cs=[];
    for(const u of V)if(!comp.has(u)){
      const id=cs.length,q=[u];comp.set(u,id);
      for(let j=0;j<q.length;j++)for(const v of G.adj[q[j]])if(allowed.has(v)&&!comp.has(v)){comp.set(v,id);q.push(v)}
      cs.push(q);
    }
    for(const c of cs)for(const u of c)for(const v of c)if(G.owner[u]!==G.owner[v]&&!G.adj[u].has(v)){
      const prev=new Map([[u,-1]]),q=[u];
      for(let j=0;j<q.length&&!prev.has(v);j++)for(const w of G.adj[q[j]])if(allowed.has(w)&&!prev.has(w)){prev.set(w,q[j]);q.push(w)}
      let p=[];for(let x=v;x!==-1;x=prev.get(x))p.push(x);p.reverse();
      for(let j=0;j+2<p.length;j++)if(G.owner[p[j]]!==G.owner[p[j+2]])return {bad:[...new Set(p.slice(j,j+3).map(w=>G.owner[w]))]};
      check(p.length>=4,"missing P4");return {bad:[...new Set(p.slice(0,4).map(w=>G.owner[w]))]};
    }
    return {comp,cs};
  }
  function matching(G,groups,I){
    const used=new Map(),picked=new Map();
    function aug(i,seen){
      for(const u of groups[i]){const r=I.comp.get(u);if(seen.has(r))continue;seen.add(r);
        if(!used.has(r)||aug(used.get(r),seen)){used.set(r,i);picked.set(i,u);return true}}
      return false;
    }
    for(let i=0;i<groups.length;i++)if(!aug(i,new Set()))return null;
    return [...picked.values()];
  }
  function modulator(G,groups,k,stats){
    stats.discovery++;let I=inspect(G,groups);if(!I.bad)return [];
    if(!k)return null;
    for(const g of I.bad){const ans=modulator(G,groups.filter(a=>G.owner[a[0]]!==g),k-1,stats);if(ans!==null)return [g,...ans]}
    return null;
  }
  function fixed(G,groups,deleteSet,stats,chosen=[]){
    stats.solve++;
    if(groups.some(a=>!a.length))return null;
    let j=groups.findIndex(a=>deleteSet.has(G.owner[a[0]]));
    if(j<0){let I=inspect(G,groups);check(!I.bad,"nonmatching leaf");let z=matching(G,groups,I);return z===null?null:[...chosen,...z]}
    for(const u of groups[j]){
      const a=groups.filter((_,i)=>i!==j).map(g=>g.filter(v=>!G.adj[u].has(v)));
      const z=fixed(G,a,deleteSet,stats,[...chosen,u]);if(z!==null)return z;
    }
    return null;
  }
  function solve(n,B,C){
    let G=graph(n,B,C),stats={discovery:0,solve:0,k:null};
    if(!G||G.groups.some(a=>!a.length))return {sat:false,...stats};
    let D=null;for(let k=0;D===null;k++){D=modulator(G,G.groups,k,stats);if(D!==null)stats.k=k}
    let z=fixed(G,G.groups,new Set(D),stats);
    if(z!==null){check(z.length===C.length,"selection size");let U=z.map(u=>[G.lits[u]]);check(!!reach(n,[...B,...U]),"invalid witness");}
    return {sat:z!==null,...stats};
  }
  function brute(n,B,C){for(let mask=0;mask<2**n;mask++){let good=[...B,...C].every(c=>c.some(l=>Boolean(mask&(1<<(Math.abs(l)-1)))===(l>0)));if(good)return true}return false}
  function color(n,edges){
    let B=[],C=[];for(let i=0;i<n;i++){let a=[3*i+1,3*i+2,3*i+3];C.push(a);for(let j=0;j<3;j++)for(let k=0;k<j;k++)B.push([-a[j],-a[k]])}
    for(const [i,j] of edges)for(let c=1;c<=3;c++)B.push([-(3*i+c),-(3*j+c)]);
    return [3*n,B,C];
  }
  function hall(t,extra=true){
    // connected 3-regular bipartite circulant: group i -> resources i,i+1,i+2; extra group -> 0,1,2.
    let B=[],C=[],res=Array.from({length:t},()=>[]),n=0;
    for(let i=0;i<t+(extra?1:0);i++){let g=[];for(let j=0;j<3;j++){const u=++n;g.push(u);res[(i+j)%t].push(u)}C.push(g);for(let a=0;a<3;a++)for(let b=0;b<a;b++)B.push([-g[a],-g[b]])}
    for(const r of res)for(let a=0;a<r.length;a++)for(let b=0;b<a;b++)B.push([-r[a],-r[b]]);
    return [n,B,C];
  }
  let random={total:0,sat:0,unsat:0,maxK:0,maxDiscovery:0};
  for(let i=0;i<220;i++){let n=5+rnd(4),B=[],C=[];let lit=()=>{let v=1+rnd(n);return rnd(11)<5?-v:v};
    for(let j=0;j<rnd(9);j++)B.push([lit(),lit()]);
    for(let j=0;j<4+rnd(7);j++)C.push([lit(),lit(),lit()]);
    let s=solve(n,B,C);check(s.sat===brute(n,B,C),"random mismatch");random.total++;random[s.sat?"sat":"unsat"]++;random.maxK=Math.max(random.maxK,s.k||0);random.maxDiscovery=Math.max(random.maxDiscovery,s.discovery);
  }
  let structured=[];
  for(let t of [3,5,10,20,40,80]){
    let [n,B,C]=hall(t),s=solve(n,B,C);check(!s.sat&&s.k===0,"Hall root");
    for(let i=0;i<C.length;i++){let z=solve(n,B,C.filter((_,j)=>j!==i));check(z.sat&&z.k===0,"Hall neighbor")}
    structured.push({t,n,clauses:B.length+C.length,root:s,neighbors:C.length});
  }
  let k4=[];for(let i=0;i<4;i++)for(let j=0;j<i;j++)k4.push([i,j]);
  let K=solve(...color(4,k4));check(!K.sat&&K.k===0,"K4");
  for(let i=0;i<k4.length;i++)check(solve(...color(4,k4.filter((_,j)=>i!==j))).sat,"K4 neighbor");
  let wheel=[];for(let i=1;i<=5;i++){wheel.push([0,i],[i,i===5?1:i+1])}
  let [wn,WB,WC]=color(6,wheel),W=solve(wn,WB,WC);check(!W.sat&&W.k>0,"wheel");
  let branches=WC[0].map(l=>{let G=graph(wn,[...WB,[l]],WC.slice(1));check(G.groups.every(g=>g.length===2),"wheel size");let b=[];for(let u=0;u<G.lits.length;u++)for(const v of G.adj[u])if(u<v){let a=G.groups[G.owner[u]],c=G.groups[G.owner[v]],i=G.owner[u]+1,j=G.owner[v]+1;b.push([a[0]===u?-i:i,c[0]===v?-j:j])}return !!reach(5,b)});
  check(branches.every(x=>!x),"wheel branch SCC");
  // Explicit P4 alternating two group labels; all graph edges realizable by binary exclusions.
  let p4=solve(4,[[-1,-2],[-2,-3],[-3,-4]],[[1,3],[2,4]]);
  check(p4.sat&&p4.k===1,"P4 obstruction");
  // Exhaustive all cross-group graphs on two groups of two options; independent graph oracle.
  let small=0;
  for(let mask=0;mask<16;mask++){let B=[],z=0;for(let a of [1,2])for(let b of [3,4])if(mask&(1<<z++))B.push([-a,-b]);let C=[[1,2],[3,4]];check(solve(4,B,C).sat===brute(4,B,C),"small");small++}
  return {random,structured,K4:K,K4neighbors:6,W5:W,W5HubBranches:branches,P4:p4,exhaustiveTwoByTwo:small};
}
console.log(JSON.stringify(experiment(),null,2));
