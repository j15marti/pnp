// Node.js, no external dependencies.
function audit(){
  const out=[], assert=(b,m)=>{if(!b)throw Error(m)};
  const seq=(n)=>Array.from({length:n},(_,i)=>i);
  function make(blocks){
    let off=0,ch=[];
    for(const [r,s] of (Array.isArray(blocks)?blocks:[])){
      assert(r%2===0&&s%2===0,"parity");
      for(let i=0;i<r;i++)ch.push([off+i,off+2*r+s-1-i]);
      for(let j=0;j<s;j++)ch.push([off+r+j,off+2*r+2*s-1-j]);
      off+=2*(r+s);
    }
    if(blocks.ch){ch=blocks.ch;off=blocks.V;}
    const V=off, adj=seq(V).map(i=>[(i+V-1)%V,(i+1)%V]);
    for(const [u,v] of ch){assert(u%2!==v%2&&!adj[u].includes(v),"bad edge");adj[u].push(v);adj[v].push(u)}
    for(const a of adj)a.sort((a,b)=>a-b);
    assert(adj.every(a=>new Set(a).size===3),"cubic");
    const rows=seq(V/2).map(i=>adj[2*i+1].map(v=>v/2));
    return {V,ch,adj,rows};
  }
  function cross(a,b){let [x,y]=a,[u,v]=b;return (x<u&&u<y)!==(x<v&&v<y)}
  function components(ch){
    const g=ch.map(()=>[]);
    for(let i=0;i<ch.length;i++)for(let j=0;j<i;j++)if(cross(ch[i],ch[j])){g[i].push(j);g[j].push(i)}
    const col=ch.map(()=>-1), comps=[],ids=[];
    for(let i=0;i<ch.length;i++)if(col[i]<0){let q=[i];col[i]=0;for(let j=0;j<q.length;j++){let u=q[j];ids[u]=comps.length;for(let v of g[u]){if(col[v]<0){col[v]=1-col[u];q.push(v)}else assert(col[v]!==col[u],"not two page")}}comps.push(q)}
    // Maximum bipartite matching, then Konig cover.
    const match=ch.map(()=>-1),covers=[];
    for(const C of comps){
      const L=C.filter(v=>col[v]===0);
      function aug(u,seen){for(const v of g[u])if(!seen.has(v)){seen.add(v);if(match[v]<0||aug(match[v],seen)){match[v]=u;match[u]=v;return true}}return false}
      for(const u of L)aug(u,new Set());
      const z=new Set(L.filter(u=>match[u]<0)), q=[...z];
      for(let i=0;i<q.length;i++){const u=q[i];const next=col[u]===0?g[u].filter(v=>v!==match[u]):match[u]<0?[]:[match[u]];for(const v of next)if(!z.has(v)){z.add(v);q.push(v)}}
      const cover=C.filter(u=>col[u]===0?!z.has(u):z.has(u));
      assert(cover.length===L.filter(u=>match[u]>=0).length,"cover matching");
      assert(C.every(u=>g[u].every(v=>cover.includes(u)||cover.includes(v))),"not cover");
      covers.push(cover);
    }
    return {comps,ids,covers};
  }
  function graphOrder(G,local){
    const {V,ch,adj}=G, A=adj.map(a=>new Set(a)),alive=new Set(seq(V)),order=[];let width=0;
    function eliminate(v){const ns=[...A[v]];width=Math.max(width,ns.length);for(const u of ns){A[u].delete(v);for(const w of ns)if(w!==u)A[u].add(w)}A[v].clear();alive.delete(v);order.push(v)}
    function greedy(S,held){let rem=new Set(S);while(rem.size){let best=-1,deg=Infinity;for(const v of rem){const d=[...A[v]].filter(u=>!held.has(u)).length;if(d<deg){deg=d;best=v}}eliminate(best);rem.delete(best)}}
    let meta=components(ch),{comps,ids,covers}=meta,ci=[];
    for(let i=0;i<ch.length;i++)for(const v of ch[i])ci[v]=ids[i];
    if(!local){greedy(seq(V),new Set());return {order,width,k:Math.max(...covers.map(a=>a.length)),total:covers.reduce((a,b)=>a+b.length,0),components:comps.length}}
    function rec(lo,hi){
      if(lo>hi)return;
      const c=ci[lo], ends=comps[c].flatMap(i=>ch[i]).sort((a,b)=>a-b);
      assert(ends[0]===lo&&ends.at(-1)<=hi,"crossing gap violation");
      for(let i=0;i<ends.length-1;i++)rec(ends[i]+1,ends[i+1]-1);
      rec(ends.at(-1)+1,hi);
      const keep=new Set(covers[c].map(i=>ch[i].find(v=>v%2===0)));
      const boundary=new Set([...alive].filter(v=>!ends.includes(v)));
      const held=new Set([...keep,...boundary]);
      greedy(ends.filter(v=>!keep.has(v)),held);
      greedy([...keep],boundary);
    }
    rec(0,V-1);
    assert(order.length===V,"order completeness");
    const k=Math.max(...covers.map(a=>a.length));
    assert(width<=k+4,"width theorem");
    return {order,width,k,total:covers.reduce((a,b)=>a+b.length,0),components:comps.length};
  }
  function close(G,pins){
    const n=G.rows.length,x=Array(n).fill(-1);let steps=0, changed=true,bad=false;
    function set(i,v){if(x[i]>=0){if(x[i]!==v)bad=true}else{x[i]=v;changed=true;steps++}}
    for(const [i,v] of pins)set(i,v);
    while(changed&&!bad){changed=false;
      for(const r of G.rows){const one=r.filter(i=>x[i]===1).length,u=r.filter(i=>x[i]<0);
        if(one>1||one===0&&u.length===0){bad=true;break}
        if(one===1)for(const i of u)set(i,0);else if(u.length===1)set(u[0],1);
      }
      const rows=G.rows.map(r=>r.reduce((a,i)=>a^(1n<<BigInt(i)),1n<<BigInt(n)));
      for(let i=0;i<n;i++)if(x[i]>=0)rows.push((1n<<BigInt(i))^(BigInt(x[i])<<BigInt(n)));
      let at=0;for(let i=0;i<n;i++){let b=1n<<BigInt(i),j=rows.findIndex((r,k)=>k>=at&&(r&b)!==0n);if(j<0)continue;[rows[at],rows[j]]=[rows[j],rows[at]];for(let k=0;k<rows.length;k++)if(k!==at&&(rows[k]&b))rows[k]^=rows[at];at++}
      const rhs=1n<<BigInt(n);for(const a of rows){let v=a&(rhs-1n);if(v===0n){if(a&rhs)bad=true}else if((v&(v-1n))===0n)set(v.toString(2).length-1,Number(Boolean(a&rhs)))}
    }return {x,bad,steps};
  }
  function verify(G,pins,x){return x.length===G.rows.length&&G.rows.every(r=>r.reduce((s,i)=>s+x[i],0)===1)&&pins.every(([i,v])=>x[i]===v)}
  function solve(G,pins,ord,closure,cap){
    if(closure.bad)return {status:"NO",probes:0};
    if(ord.width>8)return {status:"UNKNOWN",probes:0};
    const V=G.V,D=seq(V).map(v=>v%2?[0,1,2]:closure.x[v/2]<0?[0,1]:[closure.x[v/2]]);
    let F=[],history=[],probes=0;
    for(let v=0;v<V;v+=2)for(const c of G.adj[v]){
      const pos=G.adj[c].indexOf(v);
      F.push({vs:[v,c],get:a=>a[0]===Number(a[1]===pos)});
    }
    const a=Array(V).fill(-1);
    function key(ns){return ns.map(v=>a[v]).join("")}
    for(const v of ord.order){
      const bucket=F.filter(f=>f.vs.includes(v));F=F.filter(f=>!f.vs.includes(v));
      const ns=[...new Set(bucket.flatMap(f=>f.vs))].filter(u=>u!==v).sort((a,b)=>a-b),tab=new Map();
      function enumerate(i){if(i<ns.length){for(const b of D[ns[i]]){a[ns[i]]=b;enumerate(i+1)}return}
        for(const b of D[v]){a[v]=b;probes+=1+bucket.length;if(probes>cap)throw Error("cap");if(bucket.every(f=>f.get(f.vs.map(u=>a[u])))){tab.set(key(ns),b);break}}
      }
      try{enumerate(0)}catch(e){if(e.message==="cap")return {status:"UNKNOWN",probes};throw e}
      if(!tab.size)return {status:"NO",probes};
      history.push({v,ns,tab});
      F.push({vs:ns,get:vals=>tab.has(vals.join(""))});
    }
    for(const h of history.reverse()){const val=h.tab.get(key(h.ns));assert(val!==undefined,"lift");a[h.v]=val}
    const x=a.filter((_,i)=>i%2===0);
    assert(verify(G,pins,x),"source lift");
    return {status:"YES",probes,x};
  }
  function brute(G,pins,cap){
    let n=G.rows.length,probes=0;if(n>20)return {status:"UNKNOWN",probes};
    for(let w=0;w<2**n;w++){probes+=1+n;if(probes>cap)return {status:"UNKNOWN",probes};const x=seq(n).map(i=>(w>>i)&1);if(verify(G,pins,x))return {status:"YES",probes,x}}
    return {status:"NO",probes}
  }
  const families=[];
  // True nested chord components, insertion of an even-size block in one gap.
  const base=make([[2,4]]);
  let nested={V:base.V,ch:base.ch};
  for(let b=1;b<=16;b++){
    if([1,2,4,8,16].includes(b))families.push({type:"true-nested",blocks:nested});
    nested={V:nested.V+base.V,ch:[...base.ch.map(a=>a.map(v=>v===0?0:v+nested.V)),...nested.ch.map(a=>a.map(v=>v+1))]};
  }
  let seed=26011732;
  const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
  const seen=new Set();
  for(const n of [6,9,12,15]){
    let kept=0;
    for(let trial=0;trial<20000&&kept<10;trial++){
      let p=seq(n).map(i=>2*i+1);
      for(let i=n-1;i>0;i--){let j=Math.floor(rand()*(i+1));[p[i],p[j]]=[p[j],p[i]]}
      if(p.some((v,i)=>v===(2*i+1)%(2*n)||v===(2*i+2*n-1)%(2*n)))continue;
      let ch=p.map((v,i)=>[2*i,v].sort((a,b)=>a-b)),key=JSON.stringify(ch);
      if(seen.has(key))continue;
      try{components(ch)}catch(e){if(e.message==="not two page")continue;throw e}
      seen.add(key);kept++;
      families.push({type:"random-two-page",blocks:{V:2*n,ch}});
    }
  }
  // Test same native rows/pins in all lanes. All sources have constructive 2-page embeddings.
  for(const {type,blocks} of families){
    const G=make(blocks),n=G.rows.length, A=graphOrder(G,true),B=graphOrder(G,false);
    for(const pins of [[],[[0,1]],[[0,0]],[[0,1],[G.rows[0].find(v=>v!==0),1]]]){
      const N=JSON.stringify([G.rows,pins]).length,cap=Math.min((N+2)**4,1000000);
      const ca=close(G,pins),cb=close(G,pins);
      const a=solve(G,pins,A,ca,cap), b=solve(G,pins,B,cb,cap),c=brute(G,pins,cap);
      const ci=close(G,pins);
      // Import the verified narrower elimination certificate, not a hull or unguarded answer.
      const d=solve(G,pins,A.width<=B.width?A:B,ci,cap);
      const definite=[a,b,c,d].filter(v=>v.status!=="UNKNOWN");
      assert(definite.every(v=>v.status===definite[0].status),"disagree");
      out.push({type,blocks,n,N,pins,rows:G.rows,chords:G.ch,A:{...a,order:A.order,width:A.width},B:{...b,order:B.order,width:B.width},C:c,I:d,forced:ci.steps,k:A.k,total:A.total,components:A.components,cap});
    }
  }
  return out;
}
console.log(JSON.stringify(audit(),null,2));
