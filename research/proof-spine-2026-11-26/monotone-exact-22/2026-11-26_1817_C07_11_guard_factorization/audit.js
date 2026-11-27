function audit() {
  const assert=(v,s)=>{if(!v)throw Error(s||"assert")};
  let seed=20261126;
  const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
  function compile(k,G){
    let n=0;const rows=[],alloc=()=>n++,add=(...r)=>{assert(r.length===4&&new Set(r).size===4,"row");rows.push(r)};
    const r0=alloc(),r1=alloc(),b=alloc(),u=alloc(),v=alloc();
    add(r0,b,r1,u);add(r0,b,u,v);add(r0,b,v,r1);
    const labels=[],bars=[],ends=[r1],stages=[],nae=(a,b,c)=>{const w=alloc();add(a,b,c,w);return rows.at(-1)};
    for(let i=0;i<2*k;i++){labels.push(alloc());bars.push(alloc());add(labels[i],bars[i],r0,r1)}
    for(let i=1;i<k;i++)ends.push(alloc());ends.push(r0);
    for(let i=0;i<k;i++){
      const mids=[alloc(),alloc()],rr=[];
      for(let j=0;j<2;j++){const l=2*i+j;rr.push(nae(ends[i],mids[j],labels[l]));rr.push(nae(mids[j],ends[i+1],bars[l]));}
      stages.push({mids,rr});
    }
    const phys=l=>l>0?labels[l-1]:bars[-l-1],ctx=[];
    for(const c of G){assert(c.length===2&&Math.abs(c[0])!==Math.abs(c[1]));ctx.push(nae(phys(c[0]),phys(c[1]),r0))}
    const F={n,rows,k,G,r0,r1,b,u,v,labels,bars,ends,stages,ctx};
    assert(new Set(rows.map(r=>r.slice().sort((a,b)=>a-b).join(","))).size===rows.length);
    return F
  }
  const verify=(F,w)=>w.length===F.n&&w.every(x=>x===0||x===1)&&F.rows.every(r=>r.reduce((s,j)=>s+w[j],0)===2);
  function close(F,pins,M){
    const w=Array(F.n).fill(-1);for(const [j,x] of pins){if(w[j]>=0&&w[j]!==x)return null;w[j]=x}
    let changed=true;while(changed){changed=false;for(const r of F.rows){M.rows++;let s=0,un=[];for(const j of r){if(w[j]===-1)un.push(j);else s+=w[j]}
      if(s>2||s+un.length<2)return null;
      if(s===2||s+un.length===2)for(const j of un){w[j]=s===2?0:1;changed=true}
    }}return w
  }
  const litval=(w,l)=>l>0?w[l-1]===1:w[-l-1]===0;
  const satisfies=(w,G)=>G.every(c=>c.some(l=>litval(w,l)));
  function twoSAT(n,G,M){
    M.satcalls++;const a=Array.from({length:2*n},()=>[]),r=a.map(()=>[]),id=l=>2*(Math.abs(l)-1)+(l<0?1:0);
    function edge(i,j){a[i].push(j);r[j].push(i);M.edges++}
    for(const c of G){if(!c.length)return null;assert(c.length<=2);const x=id(c[0]),y=id(c[c.length-1]);edge(x^1,y);edge(y^1,x)}
    const vis=a.map(()=>false),ord=[],comp=a.map(()=>-1);
    function dfs(i){vis[i]=true;for(const j of a[i]){M.edges++;if(!vis[j])dfs(j)}ord.push(i)}
    for(let i=0;i<a.length;i++)if(!vis[i])dfs(i);
    function rev(i,c){comp[i]=c;for(const j of r[i]){M.edges++;if(comp[j]<0)rev(j,c)}}
    let c=0;for(let j=ord.length-1;j>=0;j--)if(comp[ord[j]]<0)rev(ord[j],c++);
    const w=[];for(let i=0;i<n;i++){if(comp[2*i]===comp[2*i+1])return null;w.push(comp[2*i]>comp[2*i+1]?1:0)}
    assert(satisfies(w,G),"2sat witness");return w
  }
  function graph(F){
    const a=Array.from({length:F.n},()=>[]);for(let i=0;i<F.k;i++)for(let j=0;j<2;j++){
      const l=2*i+j+1,m=F.stages[i].mids[j],s=F.ends[i],t=F.ends[i+1];
      a[s].push([m,l]);a[m].push([t,l]);a[m].push([s,-l]);a[t].push([m,-l])
    }return a
  }
  function fromPhase(F,w,y){
    const z=Array(F.n).fill(-1);z[F.r0]=z[F.b]=0;z[F.r1]=z[F.u]=z[F.v]=1;
    F.labels.forEach((j,i)=>{z[j]=w[i];z[F.bars[i]]=1-w[i]});
    F.ends.forEach(j=>{assert(z[j]<0||z[j]===y[j],"end");z[j]=y[j]});
    for(const s of F.stages)for(const m of s.mids)z[m]=1-y[m];
    for(const r of [...F.stages.flatMap(s=>s.rr),...F.ctx]){
      const t=2-r.slice(0,3).reduce((s,j)=>s+z[j],0);if(t!==0&&t!==1)return null;z[r[3]]=t
    }
    assert(verify(F,z),"native lift");return z
  }
  function lift(F,w,M){
    assert(satisfies(w,F.G));const a=graph(F),seen=Array(F.n).fill(0),q=[F.r1];seen[F.r1]=1;
    for(let i=0;i<q.length;i++)for(const [j,l] of a[q[i]]){M.edges++;if(!seen[j]&&litval(w,l)){seen[j]=1;q.push(j)}}
    if(seen[F.r0])return null;return fromPhase(F,w,seen)
  }
  function short(F,M){
    const a=graph(F),states=a.map(()=>new Map()),q=[[F.r1,[]]];states[F.r1].set("",[]);
    function union(g,l){if(g.includes(-l))return null;if(g.includes(l))return g;return [...g,l].sort((a,b)=>a-b)}
    for(let i=0;i<q.length;i++){
      const [u,g]=q[i];M.states++;
      for(const [v,l] of a[u]){M.edges++;const h=union(g,l);if(h&&h.length<=2&&!states[v].has(h.join(","))){states[v].set(h.join(","),h);q.push([v,h])}}
    }
    for(const [u,g] of q)for(const [v,l] of a[u]){
      M.edges++;const h=union(g,l);if(!h)continue;let ok=false;
      for(const z of states[v].values()){M.checks++;if(z.every(t=>h.includes(t))){ok=true;break}}
      if(!ok)return {status:"UNKNOWN",overflow:h}
    }
    const R=[...states[F.r0].values()].map(g=>g.map(l=>-l));
    const w=twoSAT(2*F.k,F.G.concat(R),M);
    if(!w)return {status:"UNSAT"};const z=lift(F,w,M);assert(z);return {status:"SAT",z,w}
  }
  function factor(F,M){
    const P=Array.from({length:F.k},(_,i)=>[2*i+1,2*i+2]);
    // Check existence of a permitted context which blocks extension.
    const blocked=twoSAT(2*F.k,F.G.concat(P),M);
    for(let i=0;i<F.k;i++){
      M.checks++;const w=twoSAT(2*F.k,F.G.concat([[-(2*i+1)],[-(2*i+2)]]),M);
      if(w){const z=lift(F,w,M);assert(z);return {status:"SAT",z,w,blockable:!!blocked,cut:i}}
    }
    return {status:"UNSAT",blockable:!!blocked}
  }
  // Independent native integer stage evaluator: no guarded graph or P formula.
  function local(F,i,a,b,w,M){
    const s=F.stages[i], vals=new Map([[F.ends[i],a],[F.ends[i+1],b]]);
    for(let j=0;j<2;j++){vals.set(F.labels[2*i+j],w[j]);vals.set(F.bars[2*i+j],1-w[j])}
    for(let t=0;t<4;t++){M.trials++;vals.set(s.mids[0],t&1);vals.set(s.mids[1],t>>1);
      if(s.rr.every(r=>{M.rows++;let v=2-r.slice(0,3).reduce((s,j)=>s+vals.get(j),0);return v===0||v===1})){
        return [t&1,t>>1];
      }
    }return null
  }
  function nativeDP(F,M,fixed=null){
    // If context clauses cross stages, fixed full boundary is required.
    if(!fixed&&!F.G.every(c=>c.every(l=>Math.floor((Math.abs(l)-1)/2)===Math.floor((Math.abs(c[0])-1)/2))))return {status:"UNKNOWN"};
    if(fixed&&!satisfies(fixed,F.G))return {status:"UNSAT"};
    let prev=new Map([[1,[]]]);
    for(let i=0;i<F.k;i++){
      const next=new Map();for(const [a,hist] of prev)for(let b=0;b<2;b++)for(let t=0;t<4;t++){
        M.trials++;const w=[t&1,t>>1];if(fixed&&(w[0]!==fixed[2*i]||w[1]!==fixed[2*i+1]))continue;
        if(!fixed&&!F.G.filter(c=>Math.floor((Math.abs(c[0])-1)/2)===i).every(c=>c.some(l=>l>0?w[(l-1)%2]===1:w[(-l-1)%2]===0)))continue;
        const mids=local(F,i,a,b,w,M);if(mids&&!next.has(b))next.set(b,[...hist,{a,b,w,mids}]);
      }prev=next
    }
    if(!prev.has(0))return {status:"UNSAT"};
    const h=prev.get(0),w=h.flatMap(t=>t.w),y=Array(F.n).fill(0);
    for(let i=0;i<F.k;i++){y[F.ends[i]]=h[i].a;y[F.ends[i+1]]=h[i].b;for(let j=0;j<2;j++)y[F.stages[i].mids[j]]=1-h[i].mids[j]}
    const z=fromPhase(F,w,y);assert(z&&satisfies(w,F.G));return {status:"SAT",w,z}
  }
  function bruteBoundary(F,M){
    for(let t=0;t<2**(2*F.k);t++){const w=Array.from({length:2*F.k},(_,i)=>(t>>i)&1);M.trials++;const q=nativeDP(F,M,w);if(q.status==="SAT")return q}return {status:"UNSAT"}
  }
  function fingerprint(F){const str=JSON.stringify(F);let h=2166136261;for(let i=0;i<str.length;i++)h=Math.imul(h^str.charCodeAt(i),16777619)>>>0;return h.toString(16).padStart(8,"0")}
  const meter=()=>({rows:0,edges:0,checks:0,trials:0,states:0,satcalls:0,probes:0});
  function run(F,kind,reference){
    const N=8*JSON.stringify(F).length,cap=BigInt(N)**3n;
    const Ms=Array.from({length:4},meter);
    const copies=Ms.map(()=>JSON.parse(JSON.stringify(F)));const hash=fingerprint(F);
    for(const f of copies)assert(fingerprint(f)===hash);
    const init=(f,M)=>{const pins=[[f.r0,0]];const q=close(f,pins,M);assert(q!==null,"initial guard");
      // Independently certified shared-hub deduction: r1,u,v opposite r0 and b equal r0.
      return close(f,pins.concat([[f.r1,1],[f.b,0],[f.u,1],[f.v,1]]),M)
    };
    for(let i=0;i<4;i++)assert(init(copies[i],Ms[i])!==null);
    const A=short(copies[0],Ms[0]),B=factor(copies[1],Ms[1]);
    const C=kind==="local"?nativeDP(copies[2],Ms[2]):bruteBoundary(copies[2],Ms[2]);
    assert(B.status===C.status&&(A.status==="UNKNOWN"||A.status===B.status),"replica mismatch");
    if(reference)assert(reference===B.status,"reference");
    // Integration imports the exact two-corridor stage predicate and checks source guards;
    // then re-evaluates both alternatives. No arbitrary use of an unknown lane.
    const f=copies[3],I=factor(f,Ms[3]);assert(I.status===B.status);
    if(I.z){assert(verify(f,I.z));const pins=I.w.map((v,i)=>[f.labels[i],v]);assert(close(f,[[f.r0,0],[f.r1,1],...pins],Ms[3])!==null)}
    for(const q of [A,B,C,I])if(q.z)assert(verify(F,q.z));
    for(const m of Ms)assert(BigInt(Object.values(m).reduce((a,b)=>a+b,0))<=cap);
    return {kind,k:F.k,n:F.n,m:F.rows.length,N,hash,A:A.status,B:B.status,C:C.status,I:I.status,blocked:B.blockable,meters:Ms}
  }
  const jobs=[];
  for(const k of [1,2,3,4,8,16,32,64,128]){
    const G=Array.from({length:k},(_,i)=>[2*i+1,2*i+2]);
    jobs.push(run(compile(k,G),"local","UNSAT"));
    jobs.push(run(compile(k,G.slice(0,-1)),"local","SAT"));
  }
  // Correlated boundary contexts, signed 2CNF; skip initial GAC contradictions,
  // which would be solved before the regional comparison.
  let skipped=0;
  for(let a=0;a<80;a++){
    const k=2+rnd(3),G=[],n=2*k;
    for(let j=0;j<1+rnd(10);j++){let p=rnd(n)+1,q=rnd(n-1)+1;if(q>=p)q++;G.push([rnd(2)?p:-p,rnd(2)?q:-q])}
    // Deduplicate equivalent native context rows (fresh completions also make rows distinct).
    const f=compile(k,G);if(!close(f,[[f.r0,0],[f.r1,1],[f.b,0],[f.u,1],[f.v,1]],meter())){skipped++;continue}
    jobs.push(run(f,"correlated"));
  }
  // Exhaustively check fixed-boundary native DP vs exact transmission predicate on empty context.
  let words=0,accepted=0;
  for(let k=1;k<=6;k++){
    const F=compile(k,[]),M=meter();let block=0;
    for(let t=0;t<2**(2*k);t++){
      const w=Array.from({length:2*k},(_,i)=>(t>>i)&1);
      const P=Array.from({length:k},(_,i)=>w[2*i]||w[2*i+1]).every(Boolean);
      const C=nativeDP(F,M,w);assert((C.status==="SAT")===!P);
      words++;if(P)block++;else accepted++;
    }assert(block===3**k)
  }
  return {seed:20261126,jobs,skipped,words,accepted,blocking:words-accepted,
    summary:{jobs:jobs.length,yes:jobs.filter(j=>j.B==="SAT").length,no:jobs.filter(j=>j.B==="UNSAT").length,Aunknown:jobs.filter(j=>j.A==="UNKNOWN").length,Adecided:jobs.filter(j=>j.A!=="UNKNOWN").length,meters:jobs.reduce((a,j)=>{j.meters.forEach((m,i)=>{for(const k of Object.keys(m))a[i][k]+=m[k]});return a},Array.from({length:4},meter))}}
}
console.log(JSON.stringify(audit(),null,2));
