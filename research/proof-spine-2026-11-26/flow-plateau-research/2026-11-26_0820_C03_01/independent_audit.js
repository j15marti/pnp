"use strict";
function audit(){
  let checks=0;function ck(x){checks++;if(!x)throw Error("check "+checks)}
  // Independent compiler: each gate has four integer ports, wiring recorded by port lists.
  function make(C,disable=-1){
    let r=C.length+4,g=[];for(let i=0;i<r-1;i++)g.push([i,i+1,0,0]);
    C.forEach((cl,k)=>{let w=cl.map((l,i)=>[i,i+1,l,0]);g.push(...w,[3,4+k,0,+(k!==disable)],...w.slice().reverse())});
    let m=g.length,s=8*m,t=s+1,edges=[],fixed=[],phase=[],inc=Array.from({length:t+1},()=>[]);
    function add(u,v,a,b,k=-1){let i=edges.length;edges.push([u,v]);fixed.push([a,b]);phase.push(k);inc[u].push(i);inc[v].push(i)}
    let ports=[];
    for(let c=0;c<2;c++){let tracks=Array.from({length:r},()=>[]);
      g.forEach(([i,j],k)=>{let p=4*(c*m+k);add(p,p+2,1,1,c*m+k);add(p+1,p+3,1,1,c*m+k);add(p,p+3,1,0,c*m+k);add(p+1,p+2,1,0,c*m+k);tracks[i].push([p,p+2]);tracks[j].push([p+1,p+3])});
      tracks.forEach(T=>{for(let i=1;i<T.length;i++)add(T[i-1][1],T[i][0],0,1)});ports.push(tracks.map(T=>[T[0][0],T.at(-1)[1]]))
    }
    for(let k=0;k<r;k++)for(let side=0;side<2;side++){let u=ports[0][k][side],v=ports[1][k][side];if(k===0){let w=side===0?s:t;add(u,w,0,1);add(v,w,0,1)}else add(u,v,0,1)}
    add(s,t,0,0);ck(inc.every(I=>I.length===3));ck(new Set(edges.map(([u,v])=>[Math.min(u,v),Math.max(u,v)].join(","))).size===edges.length);
    function color(x){
      const b=fixed.map(([a,v],i)=>v^(phase[i]<0?0:x[phase[i]%m]));
      ck(fixed.filter(([a],i)=>!a&&!b[i]).length===1);ck(inc.every(I=>I.reduce((z,e)=>z+fixed[e][0],0)%2===0&&I.reduce((z,e)=>z+b[e],0)===2));
      // Independent XOR equality system for the other flow: y_e=1 on b=0, XOR of other two =1.
      const adj=b.map(()=>[]),y=b.map(v=>v?-1:1);
      for(const I of inc){let [u,v]=I.filter(e=>b[e]);adj[u].push(v);adj[v].push(u)}
      for(let i=0;i<b.length;i++)if(y[i]<0){y[i]=0;let queue=[i];for(const u of queue)for(const v of adj[u]){if(y[v]===y[u])return false;if(y[v]<0){y[v]=1-y[u];queue.push(v)}}}
      ck(inc.every(I=>new Set(I.map(e=>b[e]+2*y[e])).size===3&&I.every(e=>b[e]+2*y[e]!==0)));return true
    }
    ck(color(g.map(()=>0)));
    return {g,color,n:t+1};
  }
  const all=Array.from({length:8},(_,i)=>[1,2,3].map((v,j)=>((i>>j)&1)?v:-v));
  let cases=0,words=0,yes=0;
  for(let mask=1;mask<256;mask++){let C=all.filter((_,i)=>(mask>>i)&1),G=make(C);
    for(let x=0;x<8;x++){let w=G.g.map(([,,l,p])=>l?(((x>>(Math.abs(l)-1))&1)^(l>0?1:0)):p);
      let expected=C.every(cl=>cl.some(l=>Boolean((x>>(Math.abs(l)-1))&1)===(l>0)));ck(G.color(w)===expected);yes+=+expected;words++}
    cases++;
  }
  let a=make(all),b=make(all,0);ck(a.n===b.n);ck(!a.color(a.g.map(([,,l,p])=>l?(1^(l>0?1:0)):p)));ck(b.color(b.g.map(([,,l,p])=>l?(1^(l>0?1:0)):p)));
  return {cases,words,yes,checks,neighborVertices:a.n}
}
console.log(JSON.stringify(audit()));
