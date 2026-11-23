'use strict';
// Run with node; deterministic exact finite controls, no dependencies.
function experiment(){
  const assert=(b,m)=>{if(!b)throw Error(m)};
  const edge=(a,b)=>a<b?[a,b]:[b,a];
  const uniq=es=>[...new Map(es.filter(([a,b])=>a!==b).map(([a,b])=>{const t=edge(a,b);return[t.join(","),t]})).values()];
  function overlay(n,E){
    const s=Math.ceil(Math.sqrt(n)), p=s*s, L=[];
    for(let x=0;x<s;x++)for(let y=0;y<s;y++){
      const u=x*s+y;
      for(const [a,b] of [[(x+2*y)%s,y],[(x+2*y+1)%s,y],[x,(y+2*x)%s],[x,(y+2*x+1)%s]])L.push([u,a*s+b]);
    }
    const O=uniq(L), out=E.slice();
    O.forEach(([u,v],i)=>{out.push([u,p+i],[v,p+i])});
    return {n:p+O.length,E:uniq(out),p,overlayEdges:O.length};
  }
  function color(n,E){
    const adj=Array.from({length:n},()=>[]);
    E.forEach(([u,v])=>{adj[u].push(v);adj[v].push(u)});
    const order=Array.from({length:n},(_,i)=>i).sort((a,b)=>adj[b].length-adj[a].length), a=Array(n).fill(-1);
    function rec(t){if(t===n)return true;const v=order[t];for(let c=0;c<3;c++)if(adj[v].every(u=>a[u]!==c)){a[v]=c;if(rec(t+1))return true;a[v]=-1;}return false;}
    return rec(0)?a:null;
  }
  function build(H){
    const {n,E}=H;const base=[], q0=3*n+3*E.length;
    for(let v=0;v<n;v++)base.push([3*v,3*v+1,3*v+2]);
    E.forEach(([u,v],i)=>{for(let c=0;c<3;c++)base.push([3*u+c,3*v+c,3*n+3*i+c]);});
    const occ=Array.from({length:q0},()=>[]), owner=[], rows=[];
    for(let j=0;j<3;j++)for(const r of base)rows.push(r.map(v=>{const i=owner.length;owner.push(v);occ[v].push(i);return i;}));
    const L=owner.length;let q=L;const links=[];
    for(const ring of occ)for(let i=0;i<ring.length;i++){
      const a=ring[i],b=ring[(i+1)%ring.length],p=q++,s=q++;
      rows.push([a,p,s],[b,p,s]);links.push([a,b,p,s]);
    }
    return {base,q0,rows,q,L,owner,links};
  }
  function rank2(rows){
    const piv=new Map();
    for(const row of rows){let b=0n;for(const v of row)b^=1n<<BigInt(v);while(b){const p=b&(-b);if(piv.has(p))b^=piv.get(p);else{piv.set(p,b);break;}}}
    return piv.size;
  }
  function quotient(B){
    const parent=Array.from({length:B.q},(_,i)=>i);
    function find(x){while(parent[x]!==x){parent[x]=parent[parent[x]];x=parent[x]}return x;}
    function union(a,b){a=find(a);b=find(b);if(a!==b)parent[b]=a;}
    const seen=new Map();
    for(const r of B.rows)for(let j=0;j<3;j++){const k=r.filter((_,i)=>i!==j).sort((a,b)=>a-b).join(",");if(seen.has(k))union(r[j],seen.get(k));else seen.set(k,r[j]);}
    const rows=[...new Map(B.rows.map(r=>{const s=r.map(find).sort((a,b)=>a-b);assert(new Set(s).size===3,"unexpected collapse");return[s.join(","),s]})).values()];
    const deg=Array(B.q).fill(0);rows.forEach(r=>r.forEach(v=>deg[v]++));
    const retained=rows.filter(r=>r.filter(v=>deg[v]===1).length<2), dropped=rows.filter(r=>r.filter(v=>deg[v]===1).length>=2);
    assert(retained.length===B.base.length,"projected rows");
    return {rows:retained,dropped,find,deg};
  }
  function solveExact(rows,q){
    let nodes=0;
    const deg=Array(q).fill(0);rows.forEach(r=>r.forEach(v=>deg[v]++));
    function rec(a){
      nodes++;let changed=true;
      while(changed){changed=false;for(const r of rows){
        const t=r.filter(v=>a[v]===1).length,u=r.filter(v=>a[v]===-1);
        if(t>1||t+u.length<1)return null;
        if(t===1){for(const v of u){a[v]=0;changed=true;}}
        else if(u.length===1){a[u[0]]=1;changed=true;}
      }}
      let best=null,score=-1;
      for(const r of rows)if(!r.some(v=>a[v]===1)){const u=r.filter(v=>a[v]===-1),s=1000*(3-u.length)+u.reduce((z,v)=>z+deg[v],0);if(s>score){best=u;score=s;}}
      if(!best)return a;
      for(const v of best){const b=a.slice();b[v]=1;const x=rec(b);if(x)return x;}return null;
    }
    return {a:rec(Array(q).fill(-1)),get nodes(){return nodes}};
  }
  function checkCase(name,n,E){
    const oracle=color(n,E),H=overlay(n,E), B=build(H), m=B.base.length;
    const counts=Array(B.q).fill(0);
    for(const r of B.rows){assert(new Set(r).size===3,"non-distinct row");r.forEach(v=>counts[v]++);}
    assert(counts.every(x=>x===2||x===3),"occurrence");
    assert(B.q===27*m&&B.rows.length===21*m,"size");
    assert(counts.filter(x=>x===3).length===9*m,"k");
    const iw=Array(B.q0).fill(0);for(let v=0;v<H.n;v++)iw[3*v]=1;
    H.E.forEach(([u,v],i)=>{for(let c=0;c<3;c++)iw[3*H.n+3*i+c]=1-iw[3*u+c]-iw[3*v+c];});
    const lifted=B.owner.map(v=>iw[v]);for(const [a,b,p,s] of B.links){assert(lifted[a]===lifted[b],"integer wire");lifted[p]=0;lifted[s]=1-lifted[a];}
    assert(B.rows.every(r=>r.reduce((s,v)=>s+lifted[v],0)===1),"integer witness");
    const rank=rank2(B.rows);assert(B.q-rank===9*m+2*H.n,"rank GF2");
    const Q=quotient(B), S=solveExact(Q.rows,B.q);
    assert(Boolean(S.a)===Boolean(oracle),"oracle disagreement "+name);
    if(S.a){
      for(const r of Q.dropped){
        const privateV=r.filter(v=>Q.deg[v]===1), other=r.filter(v=>Q.deg[v]!==1);
        for(const v of other)if(S.a[v]===-1)S.a[v]=0;
        const t=other.reduce((z,v)=>z+S.a[v],0);
        privateV.forEach((v,i)=>S.a[v]=t===0&&i===0?1:0);
      }
      const a=Array.from({length:B.q},(_,v)=>S.a[Q.find(v)]);
      assert(B.rows.every(r=>r.reduce((s,v)=>s+a[v],0)===1),"Boolean witness");
    }
    return {name,sourceVertices:n,sourceEdges:E.length,overlayVertices:H.p,Hvertices:H.n,Hedges:H.E.length,q:B.q,m:B.rows.length,k:9*m,nullity:B.q-rank,rankGF2:rank,quotientRows:Q.rows.length,decision:oracle?"SAT":"UNSAT",DPLLnodes:S.nodes};
  }
  const K4=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)K4.push([i,j]);
  const wheel=[];for(let i=0;i<5;i++){wheel.push([i,(i+1)%5],[i,5]);}
  const results=[checkCase("K4",4,K4),...K4.map((_,i)=>checkCase("K4 minus edge "+i,4,K4.filter((_,j)=>i!==j))),checkCase("odd wheel W5 (K4-free)",6,wheel),checkCase("empty 9",9,[]),checkCase("empty 16",16,[])];
  const peer=[[0,1,2],[0,1,3],[0,2,3],[0,4,5],[1,2,4]];
  const count=rr=>Array.from({length:64},(_,x)=>x).filter(x=>rr.every(r=>r.reduce((a,v)=>a+((x>>v)&1),0)===1)).length;
  const deletions=peer.map((_,i)=>count(peer.filter((_,j)=>i!==j)));
  assert(count(peer)===0&&deletions.join(",")==="1,2,2,2,1","peer audit");
  return {results,peerDeletionCounts:deletions,peerRootCount:count(peer)};
}
console.log(JSON.stringify(experiment(),null,2));
