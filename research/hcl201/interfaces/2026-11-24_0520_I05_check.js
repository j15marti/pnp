function main(){
  let seed=2010520;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
  const assert=(a,b)=>{if(!a)throw Error(b)};
  const eq=(a,b)=>a.every((x,i)=>x===b[i]);
  const dsu=n=>{const p=Array.from({length:n},(_,i)=>i);function find(i){while(p[i]!==i){p[i]=p[p[i]];i=p[i]}return i}return {find,union:(a,b)=>{a=find(a);b=find(b);if(a===b)return false;p[b]=a;return true}}};
  const zero=n=>Array(n).fill(0);
  const boundary=(n,E)=>{const t=zero(n);for(const e of E){t[e.u]^=1;t[e.v]^=1}return t};
  function forest(n,E,t){
    const d=dsu(n),adj=Array.from({length:n},()=>[]),chords=[];
    for(let i=0;i<E.length;i++){const {u,v}=E[i];if(d.union(u,v)){adj[u].push([v,i]);adj[v].push([u,i])}else chords.push(i)}
    const pa=Array(n).fill(-1),pe=Array(n).fill(-1),depth=zero(n),order=[],a=t.slice(),selected=[];
    for(let r=0;r<n;r++)if(pa[r]===-1){pa[r]=r;const st=[r];while(st.length){const u=st.pop();order.push(u);for(const [v,i] of adj[u])if(pa[v]===-1){pa[v]=u;pe[v]=i;depth[v]=depth[u]+1;st.push(v)}}}
    for(const v of order.reverse()){if(pa[v]===v){if(a[v])return null}else if(a[v]){selected.push(E[pe[v]]);a[pa[v]]^=1}}
    return {selected,pa,pe,depth,chords};
  }
  function blocks(n,E,f){
    const d=dsu(E.length);
    for(const i of f.chords){let {u,v}=E[i];while(u!==v){if(f.depth[u]<f.depth[v])[u,v]=[v,u];d.union(i,f.pe[u]);u=f.pa[u]}}
    const bs=new Map;for(let i=0;i<E.length;i++){const r=d.find(i);if(!bs.has(r))bs.set(r,[]);bs.get(r).push(E[i])}return [...bs.values()];
  }
  let calls=0,branches=0,forced=0,lifts=0,freeEdges=0,pureCalls=0;
  // Exact nonnegative minimum T-join by shortest paths and subset pairing.
  // The experiment uses exponential terminal pairing only on small blocks.
  // Replace pairing with minimum weight perfect matching for theorem's polynomial bound.
  function minJoin(n,E,t){
    pureCalls++;const vs=[...new Set(E.flatMap(e=>[e.u,e.v]))];const terms=vs.filter(v=>t[v]);if(!terms.length)return [];
    assert(terms.length<=20,"test terminal cap");
    const a=new Map(vs.map(v=>[v,[]]));for(const e of E)if(e.u!==e.v){a.get(e.u).push([e.v,e]);a.get(e.v).push([e.u,e])}
    const paths=[];
    for(const s of terms){const dist=new Map(vs.map(v=>[v,Infinity])),pred=new Map,done=new Set;dist.set(s,0);
      while(done.size<vs.length){let u=-1,b=Infinity;for(const v of vs)if(!done.has(v)&&dist.get(v)<b){u=v;b=dist.get(v)}if(u<0)break;done.add(u);for(const [v,e] of a.get(u))if(!done.has(v)&&b+e.w<dist.get(v)){dist.set(v,b+e.w);pred.set(v,[u,e])}}
      paths.push(terms.map(v=>{const p=[];let z=v;if(!Number.isFinite(dist.get(v)))return [Infinity,p];while(z!==s){const [u,e]=pred.get(z);p.push(e);z=u}return [dist.get(v),p]}))
    }
    const memo=new Map([[0,[0,[]]]]);function dp(mask){if(memo.has(mask))return memo.get(mask);let i=0;while(!(mask&(1<<i)))i++;let best=[Infinity,[]];for(let j=i+1;j<terms.length;j++)if(mask&(1<<j)){const [c,p]=dp(mask^(1<<i)^(1<<j)),[d,q]=paths[i][j];if(c+d<best[0])best=[c+d,p.concat(q)]}memo.set(mask,best);return best}
    const [cost,walks]=dp((1<<terms.length)-1);assert(Number.isFinite(cost),"no block join");const out=new Map;for(const e of walks){if(out.has(e.id))out.delete(e.id);else out.set(e.id,e)}
    const J=[...out.values()];assert(eq(boundary(n,J),t),"minjoin parity");assert(J.reduce((s,e)=>s+e.w,0)===cost,"pairing cost");return J;
  }
  function residual(n,E,t,K){
    calls++;if(K.some(k=>k<0))return null;
    E=E.filter(e=>e.u!==e.v&&e.w<=K[e.o]);
    const f=forest(n,E,t);if(!f)return null;
    const bs=blocks(n,E,f),chosen=[],rest=[],rem=t.slice(),cap=K.slice(),base=new Set(f.selected.map(e=>e.id));
    for(const B of bs){const owners=new Set(B.map(e=>e.o));if(owners.size!==1){rest.push(B);continue}
      const J0=B.filter(e=>base.has(e.id));const J=B.length===1?J0:minJoin(n,B,boundary(n,J0));if(B.length===1)forced++;
      for(const e of J){cap[e.o]-=e.w;rem[e.u]^=1;rem[e.v]^=1;chosen.push(e)}
    }
    if(cap.some(k=>k<0))return null;
    if(!rest.length){assert(rem.every(x=>!x),"pure residual");return chosen}
    const all=rest.flat();
    // Repeat unconditional closure after pure-block elimination and budget reductions.
    if(all.length<E.length||all.some(e=>e.w>cap[e.o])){const J=residual(n,all,rem,cap);return J===null?null:chosen.concat(J)}
    const B=rest[0],freq=new Map;for(const e of B)freq.set(e.o,(freq.get(e.o)||0)+1);
    const dom=[...freq].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0],e=B.find(e=>e.o!==dom),others=all.filter(x=>x.id!==e.id);
    for(const take of [0,1]){branches++;const tt=rem.slice(),kk=cap.slice();if(take){tt[e.u]^=1;tt[e.v]^=1;kk[e.o]-=e.w}
      const J=residual(n,others,tt,kk);if(J!==null)return chosen.concat(take?[e]:[],J)}
    return null;
  }
  function solve(n,E,t,K){
    if(K.some(k=>k<0))return null;
    E=E.filter(e=>e.w<=K[e.o]);
    const sums=zero(K.length);for(const e of E)sums[e.o]+=e.w;
    const free=E.filter(e=>e.w===0||sums[e.o]<=K[e.o]),paid=E.filter(e=>e.w!==0&&sums[e.o]>K[e.o]);freeEdges+=free.length;
    const d=dsu(n);for(const e of free)d.union(e.u,e.v);
    const tt=zero(n);for(let i=0;i<n;i++)tt[d.find(i)]^=t[i];
    const q=paid.map(e=>({...e,u:d.find(e.u),v:d.find(e.v)})).filter(e=>e.u!==e.v);
    const fq=forest(n,q,tt);if(!fq)return null;
    const p=blocks(n,q,fq).reduce((s,B)=>{const z=zero(K.length);for(const e of B)z[e.o]++;return s+B.length-Math.max(...z)},0);
    const J=residual(n,q,tt,K);if(J===null)return null;
    const orig=new Map(E.map(e=>[e.id,e])),jj=J.map(e=>orig.get(e.id)),r=boundary(n,jj).map((x,i)=>x^t[i]),F=forest(n,free,r);
    assert(F!==null,"free lift");const out=jj.concat(F.selected),cost=zero(K.length);for(const e of out)cost[e.o]+=e.w;
    assert(eq(boundary(n,out),t)&&cost.every((x,i)=>x<=K[i]),"source witness");lifts++;return {out,cost,p};
  }
  function reference(n,E,t,K){
    for(let mask=0;mask<(1<<E.length);mask++){let cost=zero(K.length),b=zero(n);for(let i=0;i<E.length;i++)if(mask&(1<<i)){let e=E[i];b[e.u]^=1;b[e.v]^=1;cost[e.o]+=e.w}if(eq(b,t)&&cost.every((x,i)=>x<=K[i]))return true}return false;
  }
  const make=es=>es.map(([u,v,o,w],id)=>({u,v,o,w,id}));
  let sat=0,unsat=0,comparisons=0,randomPmax=0;for(let r=0;r<320;r++){
    const n=2+rnd(7),k=1+rnd(4),m=1+rnd(12),E=make(Array.from({length:m},()=>[rnd(n),rnd(n),rnd(k),rnd(6)]));
    const K=Array.from({length:k},()=>rnd(13));
    for(let j=0;j<4;j++){const t=j%2?boundary(n,E.filter(()=>rnd(7)<3)):Array.from({length:n},()=>rnd(7)%2);
      const want=reference(n,E,t,K),got=solve(n,E,t,K);assert(Boolean(got)===want,"random "+r+" "+j);comparisons++;if(want){sat++;randomPmax=Math.max(randomPmax,got.p)}else unsat++}
  }
  // Partition reduction: each disjoint pair has two parallel edges, one per owner.
  const partition=[];for(const weights of [[2,2,2],[1,2,3],[1,1,4,4],[2,3,7],[1,3,3,9],[3,5,6,8]]){
    const E=make(weights.flatMap((w,i)=>[[2*i,2*i+1,0,w],[2*i,2*i+1,1,w]])),K=[weights.reduce((s,x)=>s+x,0)/2,weights.reduce((s,x)=>s+x,0)/2],n=weights.length*2,t=Array(n).fill(1);
    const got=solve(n,E,t,K),want=reference(n,E,t,K);assert(Boolean(got)===want,"partition");partition.push({weights,K,sat:want})
  }
  // 2k+1 hubs with separate parity bits. Free owner 0 is a path on a bits.
  // Paid owner 1 and 2 alternate triangles on b bits, meeting at articulation vertices.
  // Both paid owners may use one hub in common. Incidence graph f counts actual
  // distinct (factor,hub) incidences, including the free owner.
  const scaling=[];for(const k of [8,16,32,64,128,256]){
    const h=2*k+1,n=2*h,es=[],t=zero(n),inc=new Set;
    const add=(u,v,o,w)=>{es.push([u,v,o,w]);inc.add(o+":"+Math.floor(u/2));inc.add(o+":"+Math.floor(v/2))};
    for(let j=0;j<h-1;j++)add(2*j,2*j+2,0,1);
    for(let j=0;j<k;j++){const u=4*j+1,v=u+2,w=u+4,o=1+j%2;add(u,v,o,1);add(v,w,o,1);add(u,w,o,1)}
    t[0]=t[2*h-2]=t[1]=t[2*h-1]=1;
    const E=make(es),K=[h-1,k/2,k/2],before=[calls,branches,pureCalls];const good=solve(n,E,t,K),bad=solve(n,E,t,[K[0],K[1]-1,K[2]]);
    assert(good&&good.p===0&&!bad,"scaling");scaling.push({h,k,edges:E.length,feedback:inc.size-(h+3)+1,p:good.p,cost:good.cost,recursiveCalls:calls-before[0],branches:branches-before[1],pureJoinCalls:pureCalls-before[2]})
  }
  return {seed:2010520,random:{comparisons,sat,unsat,randomPmax},partition,scaling,counters:{calls,branches,forced,lifts,freeEdges,pureCalls},disagreements:0,limits:"test pairing DP, not blossom; explicit coefficient graph, no strict geometry or source PM lifts"}
}
console.log(JSON.stringify(main(),null,2));
