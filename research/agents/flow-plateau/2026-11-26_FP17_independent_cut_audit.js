'use strict';
// Independent FP17 source verification; direct full phase tracing and edge-cut deletion.
function audit(){
  const results=[];
  for(const [d,h] of [[3,3],[3,8],[4,4],[6,6],[10,8],[16,12]]){
    const L=2*d,s=L*h,t=s+1,n=t+1,edges=[],types=[];
    function add(u,v,type){edges.push([u,v]);types.push(type)}
    for(let i=0;i<h;i++)for(let j=0;j<L;j++)add(i*L+j,i*L+(j+1)%L,0);
    for(let i=0;i<h;i++)for(let j=0;j<d;j++){
      const u=i*L+2*j+1,v=((i+1)%h)*L+2*j;
      if(i===h-1&&(j===0||j===(d===3?1:2))){add(u,s,1);add(v,t,1)}else add(u,v,1)
    }
    add(s,t,2);
    const adj=Array.from({length:n},()=>[]);
    edges.forEach(([u,v],e)=>{adj[u].push([v,e]);adj[v].push([u,e])});
    if(adj.some(a=>a.length!==3)||new Set(edges.map(([u,v])=>[Math.min(u,v),Math.max(u,v)].join(","))).size!==edges.length)throw Error("not simple cubic");
    const ports=edges.filter((e,i)=>types[i]===1&&(e.includes(s)||e.includes(t))).map(e=>e[0]);
    let min=Infinity,cutTests=0;
    for(let S=1;S<(1<<h)-1;S++){
      const inside=v=>v<s&&!!((S>>Math.floor(v/L))&1);
      let cut=0;for(let e=0;e<edges.length;e++)if(types[e]===1){const [u,v]=edges[e];cut+=inside(u)!==inside(v)?1:0}
      if(cut<min)min=cut;cutTests++;
    }
    if(min!==2*d)throw Error("cut");
    const pairings=new Set(),guarded=new Set();
    let feasible=0;
    for(let bits=0;bits<(1<<h);bits++){
      const chosen=Array.from({length:n},()=>[]);
      edges.forEach(([u,v],e)=>{
        const ok=types[e]===1||(types[e]===0&&((e%L)&1)===((bits>>Math.floor(e/L))&1));
        if(ok){chosen[u].push(v);chosen[v].push(u)}
      });
      if(chosen.some(a=>a.length!==2))throw Error("not factor");
      const seen=new Set();let good=true;
      for(let v=0;v<n;v++)if(!seen.has(v)){
        let size=0,queue=[v];seen.add(v);
        for(let j=0;j<queue.length;j++){size++;for(const w of chosen[queue[j]])if(!seen.has(w)){seen.add(w);queue.push(w)}}
        if(size%2)good=false;
      }
      if(!good)throw Error("odd factor");feasible++;
      const pairs=[];
      for(const p of ports){
        let prev=-1,u=p;
        while(true){
          const v=chosen[u].find(v=>v!==prev&&v!==s&&v!==t);
          if(v===undefined)throw Error("lost boundary");
          prev=u;u=v;if(ports.includes(u)){if(p<u)pairs.push([p,u]);break}
        }
      }
      const key=pairs.map(x=>x.join(",")).sort().join(";");pairings.add(key);
      let ok=true;for(let i=0;i<h-1;i+=2)if(((bits>>i)^(bits>>(i+1)))&1)ok=false;
      if(ok)guarded.add(key)
    }
    let tripleTests=0;
    if(d===4&&h===4){
      const m=edges.length;
      for(let x=0;x<m;x++)for(let y=x+1;y<m;y++)for(let z=y+1;z<m;z++){
        const seen=new Set(),sizes=[];
        for(let v=0;v<n;v++)if(!seen.has(v)){const q=[v];seen.add(v);for(let j=0;j<q.length;j++)for(const [w,e] of adj[q[j]])if(e!==x&&e!==y&&e!==z&&!seen.has(w)){seen.add(w);q.push(w)}sizes.push(q.length)}
        if(sizes.length>1&&(sizes.length!==2||Math.min(...sizes)!==1))throw Error("nontrivial small cut");
        tripleTests++;
      }
    }
    results.push({d,h,n,minimumProperCut:min,cutTests,evenFactors:feasible,boundaryWords:pairings.size,guardedWords:guarded.size,tripleTests})
  }
  return results;
}
console.log(JSON.stringify(audit(),null,2));
