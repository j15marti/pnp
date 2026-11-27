console.log(JSON.stringify((function audit(){
  const assert=x=>{if(!x)throw Error("audit failed")};
  const out=[];
  for(const r of [2,4,8,16,32,64]){
    const n=7*r+2, adj=Array.from({length:n},()=>[]), edges=[], good=new Set();
    function add(u,v,a){assert(u!==v&&!adj[u].includes(v));adj[u].push(v);adj[v].push(u);const k=edges.length;edges.push([u,v]);if(a)good.add(k);}
    for(let i=0;i<r;i++)for(let j=0;j<6;j++)add(6*i+j,6*i+(j+1)%6,true);
    for(let i=0;i<r;i+=2){const u=6*r+i,v=u+1;add(u,v,true);add(u,6*i,false);add(u,6*i+1,false);add(v,6*i+6,false);add(v,6*i+7,false);}
    add(7*r,7*r+1,true);
    for(let i=0;i<r;i++)for(const [p,q,k] of [[2,5,0],[3,4,1]]){const a=6*i+p,b=6*((i+1)%r)+q;if(i===0){add(a,7*r+k,false);add(7*r+k,b,false);}else add(a,b,false);}
    assert(adj.every(x=>x.length===3));
    const conn=new Set([0]),queue=[0];for(const u of queue)for(const v of adj[u])if(!conn.has(v)){conn.add(v);queue.push(v);}assert(conn.size===n);
    const pm=new Set();
    for(let i=0;i<r;i++){const u=6*i,v=u+1;const z=adj[u].filter(x=>adj[v].includes(x));assert(z.length===1);const w=z[0];
      const ix=(a,b)=>edges.findIndex(([x,y])=>(x===a&&y===b)||(x===b&&y===a));
      assert(!good.has(ix(u,w))&&!good.has(ix(v,w)));
      for(const j of [0,2,4]){const k=ix(u+j,u+j+1);assert(good.has(k));pm.add(k);}
    }
    for(const k of good){const [u,v]=edges[k];if(u>=6*r&&v>=6*r)pm.add(k);}
    const d=Array(n).fill(0),C=Array.from({length:n},()=>[]);
    edges.forEach(([u,v],k)=>{if(pm.has(k)){d[u]++;d[v]++;}else{C[u].push(v);C[v].push(u);}});
    assert(d.every(x=>x===1)&&C.every(x=>x.length===2));
    const visited=new Set(),sizes=[];
    for(let i=0;i<n;i++)if(!visited.has(i)){const q=[i];visited.add(i);for(const u of q)for(const v of C[u])if(!visited.has(v)){visited.add(v);q.push(v);}sizes.push(q.length);}
    sizes.sort((a,b)=>a-b);assert(sizes[0]===2*r+1&&sizes[1]===5*r+1);
    out.push({r,n,guardedMatchings:(2n**BigInt(r)).toString(),complementCycles:sizes});
  }
  const pairings=[[[0,1],[2,3],[4,5]],[[1,2],[3,4],[5,0]]];
  const bit=(w,i)=>(w>>i)&1;
  const R=Array.from({length:64},(_,i)=>i).filter(w=>pairings.some(P=>P.every(([a,b])=>bit(w,a)===bit(w,b))));
  assert(R.length===14);
  const hist={};let checks=0;
  for(let a=0;a<6;a++)for(let b=a+1;b<6;b++)for(let s=0;s<2;s++){
    const keep=[0,1,2,3,4,5].filter(x=>x!==a&&x!==b);
    const Q=new Set(R.filter(w=>(bit(w,a)^bit(w,b))===s).map(w=>keep.reduce((v,x,i)=>v|(bit(w,x)<<i),0)));
    const recon=new Set();
    for(const P of pairings){
      const adj=Array.from({length:6},()=>[]);for(const [x,y,t] of [...P.map(([x,y])=>[x,y,0]),[a,b,s]]){adj[x].push([y,t]);adj[y].push([x,t]);}
      const comps=[],seen=new Map();let ok=true;
      for(let x=0;x<6;x++)if(!seen.has(x)){const q=[x];seen.set(x,0);for(const u of q)for(const [v,t] of adj[u]){const val=seen.get(u)^t;if(seen.has(v)){if(seen.get(v)!==val)ok=false;}else{seen.set(v,val);q.push(v);}}const ends=q.filter(z=>keep.includes(z));assert(ends.length===0||ends.length===2);if(ends.length===2)comps.push([keep.indexOf(ends[0]),keep.indexOf(ends[1]),seen.get(ends[0])^seen.get(ends[1])]);}
      if(ok)for(let w=0;w<16;w++)if(comps.every(([x,y,t])=>(bit(w,x)^bit(w,y))===t))recon.add(w);
    }
    assert(Q.size===recon.size&&[...Q].every(x=>recon.has(x)));hist[Q.size]=(hist[Q.size]||0)+1;checks++;
  }
  return {out,contractions:checks,cardinalityHistogram:hist};
})(), null, 2));
