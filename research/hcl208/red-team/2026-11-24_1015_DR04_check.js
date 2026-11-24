"use strict";
function DR04() {
  const Q=[0,1,2,3], assert=(x,m)=>{if(!x)throw Error(m)};
  let seed=20261124;
  const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
  const stats={graphs:0,vertices:0,rawEdges:0,queries:0,satQueries:0,unsatQueries:0,searchNodes:0,branchNodes:0,closureCalls:0,arcScans:0,colorDeletes:0,tupleChecks:0,verifiedEdges:0,referenceAssignments:0,peakDepth:0,peakDomainEntries:0,cumulativeDomainEntries:0,peakQueryArcs:0};
  const lit=(a,l)=>l>0?a[l]===1:a[-l]===0;
  const source=(n,F)=>{let count=0;for(let i=0;i<2**n;i++){stats.referenceAssignments++;let a=[0,...Array.from({length:n},(_,j)=>(i>>j)&1)];if(F.every(c=>c.some(l=>lit(a,l))))count++}return count};
  function compile(n,F){
    const g={n:1,edges:[],priority:[],ports:[0],bool:[]};
    const v=()=>g.n++;
    const edge=(a,b,s)=>{assert(a!==b,'loop');g.edges.push([a,b,s])};
    const restrict=(a,allowed)=>{for(const s of Q)if(!allowed.includes(s))edge(0,a,s)};
    const bv=()=>{let a=v();g.bool.push(a);restrict(a,[0,1]);return a};
    for(let i=1;i<=n;i++)assert(bv()===i,'source index');
    const l=bv(),h=bv(),w=bv(), clauses=[];
    for(const c of F){let a=bv(),b=bv();clauses.push([l,h,a],[-a,c[0],b],[-b,c[1],c[2]])}
    for(const a of [0,1])for(const b of [0,1])for(const c of [0,1])if((a^b)!==c)clauses.push([a?-l:l,b?-h:h,c?-w:w]);
    g.priority=[l,h,w,...g.bool.filter(x=>![l,h,w].includes(x))];
    function link(x,y,falseColor,trueColor,positive=true){
      const good0=positive?falseColor:trueColor,good1=positive?trueColor:falseColor;
      for(const s of new Set([0^good1,1^good0]))edge(x,y,s);
    }
    for(const c of clauses){
      const hub=v();restrict(hub,[0,1,2]);
      c.forEach((L,j)=>{let o=v();restrict(o,[j,3]);link(Math.abs(L),o,j,3,L>0);edge(hub,o,0)});
    }
    function port(lo,hi){
      const p=v(),t=v();restrict(t,[0,2]);link(hi,t,0,2);
      edge(p,lo,1);edge(p,lo,3);
      edge(p,t,2);edge(p,t,3);g.ports.push(p);
    }
    port(l,h);port(h,w);port(w,l);
    g.selector=[l,h];g.xor=w;
    return g;
  }
  function query(g,pair=null,value=null,glue=false){
    stats.queries++;
    let n=g.n+(glue?1:0), edges=g.edges.slice();
    if(pair)for(const s of Q)if(s!==value)edges.push([pair[0],pair[1],s]);
    if(glue)for(const p of g.ports)edges.push([g.n,p,0]);
    const map=new Map();
    for(let [u,v,s] of edges){if(u>v)[u,v]=[v,u];let k=u+','+v,rec=map.get(k);if(!rec){rec=[u,v,0];map.set(k,rec)}rec[2]|=1<<s}
    const arcs=[...map.values()], adj=Array.from({length:n},()=>[]);
    for(let i=0;i<arcs.length;i++){const [u,v,f]=arcs[i];adj[u].push(2*i+1);adj[v].push(2*i)}
    stats.peakQueryArcs=Math.max(stats.peakQueryArcs,arcs.length);
    function close(d,first=null){
      stats.closureCalls++;
      let q=first===null?Array.from({length:2*arcs.length},(_,i)=>i):adj[first].slice(), pending=new Uint8Array(2*arcs.length);
      for(let x of q)pending[x]=1;
      for(let k=0;k<q.length;k++){
        let a=q[k];pending[a]=0;let [u,v,f]=arcs[a>>1];if(a&1)[u,v]=[v,u];
        stats.arcScans++;
        let keep=0;
        for(let x of Q)if(d[u]>>x&1)for(let y of Q)if(d[v]>>y&1){stats.tupleChecks++;if(!(f>>(x^y)&1)){keep|=1<<x;break}}
        if(keep!==d[u]){
          stats.colorDeletes+=Q.filter(x=>(d[u]>>x&1)&&!(keep>>x&1)).length;
          d[u]=keep;if(!keep)return false;
          for(let b of adj[u])if(!pending[b]){pending[b]=1;q.push(b)}
        }
      }
      return true;
    }
    function rec(d,depth,changed=null){
      stats.searchNodes++;stats.peakDepth=Math.max(stats.peakDepth,depth);
      stats.peakDomainEntries=Math.max(stats.peakDomainEntries,n*(depth+1));stats.cumulativeDomainEntries+=n;
      if(!close(d,changed))return null;
      let u=g.priority.find(i=>(d[i]&(d[i]-1))!==0);
      if(u===undefined)u=d.findIndex(a=>(a&(a-1))!==0);
      if(u<0){const a=Array.from(d,x=>Math.log2(x));for(const [i,j,s] of edges){stats.verifiedEdges++;assert((a[i]^a[j])!==s,'invalid graph model')}return a}
      stats.branchNodes++;
      for(const x of Q)if(d[u]>>x&1){let e=d.slice();e[u]=1<<x;let a=rec(e,depth+1,u);if(a)return a}
      return null;
    }
    let d=new Uint8Array(n);d.fill(15);d[0]=1;
    let a=rec(d,0);
    if(a)stats.satQueries++;else stats.unsatQueries++;
    return a;
  }
  const cases=[];
  const fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
  const full=fano.flatMap(c=>[c,c.map(x=>-x)]);
  cases.push({name:'Fano',n:7,F:full});
  for(let i=0;i<14;i++)cases.push({name:'Fano-owner-'+i,n:7,F:full.filter((_,j)=>j!==i)});
  const cube=[];for(let x=0;x<8;x++)cube.push([1,2,3].map((v,j)=>x>>j&1?-v:v));
  cases.push({name:'cube-UNSAT',n:3,F:cube});
  for(let i=0;i<8;i++)cases.push({name:'cube-delete-'+i,n:3,F:cube.filter((_,j)=>i!==j)});
  for(let i=0;i<20;i++){
    let F=[];for(let j=0;j<3+i%8;j++){let a=[1,2,3,4];a.splice((rnd(65536)>>>8)%4,1);F.push(a.map(v=>((rnd(65536)>>>8)&1)?v:-v))}
    cases.push({name:'random-'+i,n:4,F});
  }
  let rows=[];
  for(const {name,n,F} of cases){
    const count=source(n,F),g=compile(n,F);stats.graphs++;stats.vertices+=g.n;stats.rawEdges+=g.edges.length;
    const masks=[], root=query(g);assert(root,'always SAT');
    for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){
      let mask=0;for(let d of Q){const a=query(g,[g.ports[i],g.ports[j]],d);if(a){mask|=1<<d;assert((a[g.ports[i]]^a[g.ports[j]])===d,'pair witness')}}
      assert(mask===(count?15:14),'mask '+name);masks.push(mask);
    }
    const glued=query(g,null,null,true);assert(Boolean(glued)===Boolean(count),'glue '+name);
    if(glued){assert(F.every(c=>c.some(l=>lit(glued,l))),'source lift');assert(g.ports.every(p=>glued[p]===0),'zero selector')}
    rows.push({name,n,clauses:F.length,sourceModels:count,vertices:g.n,rawEdges:g.edges.length,pairMasks:masks,glueSAT:Boolean(glued)});
  }
  return {seed:20261124,stats,cases:rows,assertionFailures:0,notes:'Actual grouped signed-multigraph AC and guarded exhaustive search; not a polynomial graph solver. Domain-entry counters count allocations, not full memory or CM.'};
}
console.log(JSON.stringify(DR04(),null,2));
