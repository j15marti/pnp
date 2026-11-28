function cutActivation(ctx,peer,cap=1800000){
 const {chart:F,V}=ctx,ctr={select:0,rows:0,check:0,rank:0,spectral:0,dual:0},total=()=>Object.values(ctr).reduce((a,b)=>a+b,0),tick=(k,n=1)=>{if(total()+n>cap)throw Error("cap");ctr[k]+=n},m=F.length,idx=(s,U,w)=>s.reduce((z,v,j)=>z|(((w>>U.indexOf(v))&1)<<j),0),key=u=>u.join(","),union=(a,b)=>[...new Set([...a,...b])].sort((a,b)=>a-b),base=F.map(f=>f.cost.map((c,w)=>c===0?w:-1).filter(w=>w>=0));
 // Fixed star-equality incidence coordinates, derived without provenance.
 const masks=F.map(f=>f.vs.map(()=>0n));let edge=0;
 for(const v of V){const occ=[];F.forEach((f,i)=>{tick("select");let j=f.vs.indexOf(v);if(j>=0)occ.push([i,j])});for(let t=1;t<occ.length;t++){let [a,j]=occ[0],[b,k]=occ[t];let bit=1n<<BigInt(edge++);masks[a][j]|=bit;masks[b][k]|=bit}}
 function basis(xs){let B=new Map();for(let x of xs){tick("rank");while(x){tick("rank");let p=x.toString(2).length-1;if(!B.has(p)){B.set(p,x);break}x^=B.get(p)}}return [...B.values()]}
 const vector=(i,w)=>masks[i].reduce((z,b,j)=>z^(((w>>j)&1)?b:0n),0n);
 const directions=S=>S.map((a,i)=>a.length?basis(a.map(w=>vector(i,w)^vector(i,a[0]))):[]);
 const dim=(S,cut)=>{let L=[],R=[];S.forEach((u,i)=>(cut.has(i)?L:R).push(...u));let l=basis(L),r=basis(R),all=basis([...l,...r]);return {left:l.length,right:r.length,ambient:all.length,width:l.length+r.length-all.length}};
 // Integer incidence diffusion, purely ordering; not an eigenvalue certificate.
 let A=F.map((_,i)=>((i*7919)%1009)-504);
 for(let t=0;t<8;t++){let sum=new Map(),num=new Map();for(let i=0;i<m;i++)for(let v of F[i].vs){tick("spectral");sum.set(v,(sum.get(v)||0)+A[i]);num.set(v,(num.get(v)||0)+1)}A=F.map((f,i)=>{tick("spectral",f.vs.length);return Math.trunc((A[i]+f.vs.reduce((z,v)=>z+Math.trunc(sum.get(v)/num.get(v)),0))/Math.max(1,1+f.vs.length))})}
 let order=F.map((_,i)=>i).sort((a,b)=>A[a]-A[b]||a-b),src=F.map((_,i)=>i),cuts=[src.slice(0,Math.floor(m/2)),order.slice(0,Math.floor(m/2))],D0=directions(base),before=cuts.map(c=>dim(D0,new Set(c)));
 let dual=null,peerScopes=[];
 if(peer){let C=new Map();if(peer.chart_sha256!==ctx.chartHash||peer.map_sha256!==ctx.mapHash)throw Error("peer adapter");for(let [U,P] of peer.regional_polynomials){let own=F.filter(f=>f.vs.every(v=>U.includes(v)));for(let [T,n,d] of P){if(d!==1||!T.every(v=>U.includes(v)))throw Error("bad polynomial");let k=key(T);C.set(k,(C.get(k)||0)+n)}for(let w=0;w<2**U.length;w++){let z=0;for(let f of own){tick("dual");z+=f.cost[idx(f.vs,U,w)]}if(z===0){let q=0;for(let [T,n] of P){tick("dual");if(T.every(v=>(w>>U.indexOf(v))&1))q+=n}if(q<0)throw Error("dual negative")}}peerScopes.push(U)}if(C.get("")!==-1||[...C].some(([k,v])=>k!==""&&v!==0))throw Error("dual sum");dual={regions:peerScopes.length,terms:[...C].length,checks:ctr.dual}}
 function run(name,seedOrder,grow,extra=[]){
  let S=base.map(a=>a.slice()),seen=new Set(),cert=[],scopes=0,checked=0,contradiction=null,stopped=false;
  let start=total(),limit=Math.min(cap,start+260000);
  const room=()=>{if(total()>=limit)throw Error("arm cap")};
  function test(U){
   room();let k=key(U);if(seen.has(k))return;seen.add(k);let owners=[];for(let i=0;i<m;i++){tick("select");if(F[i].vs.every(v=>U.includes(v)))owners.push(i)}let good=[],cost=[];
   for(let w=0;w<2**U.length;w++){let z=0;for(let i of owners){tick("rows");z+=F[i].cost[idx(F[i].vs,U,w)]}cost.push(Math.min(2,z));if(!z)good.push(w)}
   let removed=[];for(let i of owners){let allow=new Set(good.map(w=>idx(F[i].vs,U,w)));for(let w of S[i])if(!allow.has(w))removed.push([i,w])}
   // Independent checker: exact integer sum, not clipped, verify all excluded local rows.
   if(removed.length||!good.length){let min=Infinity;for(let w=0;w<2**U.length;w++){let A=new Map(U.map((v,j)=>[v,(w>>j)&1])),z=0;for(let i of owners){let f=F[i],word=f.vs.reduce((s,v,j)=>s+A.get(v)*2**j,0);tick("check");z+=f.cost[word]}min=Math.min(min,z);if(z===0){for(let [i,a] of removed){tick("check");let word=F[i].vs.reduce((s,v,j)=>s+A.get(v)*2**j,0);if(word===a)throw Error("bad exclusion")}}if((z===0)!==(cost[w]===0))throw Error("bad clip")}
    if(!good.length&&min<=0)throw Error("bad contradiction");checked++;cert.push({U,owners,removed,min});for(let [i,w] of removed)S[i]=S[i].filter(a=>a!==w);if(!good.length)contradiction=cert.length-1;
   }scopes++;
  }
  try{for(let U of extra){test(U);if(contradiction!==null)break}if(contradiction===null)for(let i of seedOrder){let U=F[i].vs;for(let step=0;step<grow;step++){test(U);if(contradiction!==null)break;let best=null;for(let j=0;j<m;j++){tick("select");let W=union(U,F[j].vs),over=U.length+F[j].vs.length-W.length;if(over>0&&W.length>U.length&&W.length<=8){let sc=over*100-(W.length-U.length);if(!best||sc>best.sc)best={W,sc}}}if(!best)break;U=best.W}if(contradiction!==null)break}}
  catch(e){if(!/cap/.test(e.message))throw e;stopped=true}
  let after=null,local=null;try{let D=directions(S);after=cuts.map(c=>dim(D,new Set(c)));local=D0.map((u,i)=>({i,before:u.length,after:D[i].length})).filter(o=>o.before!==o.after);for(let j=0;j<cuts.length;j++)if(after[j].width>before[j].width)throw Error("intersection increased")}catch(e){if(!/cap/.test(e.message))throw e;stopped=true}
  return {name,scopes,checked,stopped,contradiction,removed:cert.reduce((s,c)=>s+c.removed.length,0),local,after,events:total()-start,cert};
 }
 const arms=[run("same-scope",src,1),run("source-growth",src,4),run("diffusion-growth",order,4)];if(peerScopes.length){arms.push(run("verified-dual-seeded",[],1,peerScopes));arms.push(run("dual-first-region-removed",[],1,peerScopes.slice(1)))}
 return {edge,cuts,before,dual,arms,ctr,cap,total:total(),originalIds:F.map(f=>f.ids),scopeMap:F.map(f=>f.vs)};
}
if(typeof module!=="undefined")module.exports={cutActivation};
