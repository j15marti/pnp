function run(){
 const out={local:{queries:0,counts:{},nodes:0,sweeps:0,edgeScans:0,deletions:0},graphs:[],wheel:[],fano:[],physicalWitnesses:0,physicalEdgeChecks:0,source:{nodes:0,sweeps:0,edgeScans:0,deletions:0},assertions:0};const ck=(b,msg)=>{out.assertions++;if(!b)throw Error(msg)};
 const bit=(x,i)=>(x>>i)&1, pop=x=>{let k=0;while(x){k+=x&1;x>>=1}return k};
 function compile(n,edges){
  const vs=[],raw=[],occ=new Map(),splits=[],slacks=[],carrier=new Map();
  const add=(kind,terms)=>{let v=vs.length;vs.push({kind,terms});return v};
  const wire=(u,p,v,q,s)=>raw.push([u,p,v,q,s]);
  function nae3(terms){let r=`r${slacks.length}`;slacks.push([r,terms]);let ts=[...terms,[r,0]];for(let k=0;k<2;k++){let v=add("B",ts);ts.forEach(([id,s],p)=>{if(!occ.has(id))occ.set(id,[]);occ.get(id).push([v,p,s])})}}
  function nae4(A,C,B,D){let z=`z${splits.length}`;splits.push([z,A,C,B,D]);nae3([A,C,[z,0]]);nae3([[z,1],B,D])}
  for(let [u,v,s] of edges){let A=[`${u}:0`,0],C=[`${v}:0`,bit(s,0)],B=[`${u}:1`,0],D=[`${v}:1`,bit(s,1)];nae4(A,C,B,D);nae4(A,C,[B[0],1],[D[0],D[1]^1])}
  for(let [id,ports] of occ){let d=ports.length;ck(d>=2&&d%2===0,"even occurrences");if(d===2){let [a,b]=ports;wire(a[0],a[1],b[0],b[1],a[2]^b[2]);continue}
   let path=Array.from({length:(d-2)/2},()=>add("E",id));carrier.set(id,path[0]);let free=[];
   for(let i=0;i<path.length;i++){if(i+1<path.length)wire(path[i],3,path[i+1],0,0);for(let p=0;p<4;p++)if(!(p===0&&i>0)&&!(p===3&&i+1<path.length))free.push([path[i],p])}
   ck(free.length===d,"fanout");ports.forEach(([v,p,s],i)=>wire(free[i][0],free[i][1],v,p,s))
  }
  let v0=vs.length;ck(raw.length===2*v0,"closed raw");let es=[],portsUsed=[];
  for(let [u,p,v,q,s] of raw){let ids=Array.from({length:5},()=>add("E",null)),next=[0,0,0,0,0];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)if(!(i===0&&j===1))es.push([ids[i],next[i]++,ids[j],next[j]++,0]);es.push([u,p,ids[0],next[0]++,s],[v,q,ids[1],next[1]++,0]);ck(next.every(x=>x===4),"gadget degree")}
  let pairs=new Set();for(let [u,p,v,q,s] of es){let k=[u,v].sort((a,b)=>a-b).join(",");ck(u!==v&&!pairs.has(k),"simple");pairs.add(k);for(let [a,b] of [[u,p],[v,q]]){ck(!portsUsed[4*a+b],"port duplicate");portsUsed[4*a+b]=1}}
  ck(portsUsed.length===4*vs.length&&portsUsed.every(x=>x===1),"ports");
  let noniso=new Set(edges.flatMap(e=>e.slice(0,2))).size;ck(v0===18*edges.length-2*noniso&&vs.length===11*v0,"size formula");
  return {vs,es,raw,v0,splits,slacks,carrier,edges,n};
 }
 function verify(g,w){for(let i=0;i<g.vs.length;i++)ck(g.vs[i].kind==="E"?(w[i]===0||w[i]===15):pop(w[i])===2,"signature");for(let [u,p,v,q,s] of g.es){out.physicalEdgeChecks++;ck((bit(w[u],p)^bit(w[v],q))===s,"wire")}}
 function lift(g,x){let vals=new Map(),w=[];for(let i=0;i<x.length;i++)for(let j=0;j<2;j++)vals.set(`${i}:${j}`,bit(x[i],j));const val=([id,s])=>vals.get(id)^s;
  for(let [z,A,C,B,D] of g.splits){let good=[0,1].filter(t=>{let l=val(A)+val(C)+t,r=(1^t)+val(B)+val(D);return l>0&&l<3&&r>0&&r<3});ck(good.length>0,"split");vals.set(z,good[0])}
  for(let [r,t] of g.slacks)vals.set(r,2-t.reduce((a,b)=>a+val(b),0));
  for(let i=0;i<g.v0;i++){let v=g.vs[i];w[i]=v.kind==="E"?15*vals.get(v.terms):v.terms.reduce((a,b,j)=>a+(val(b)<<j),0)}
  g.raw.forEach(([u,p,v,q,s],i)=>{let a=bit(w[v],q);ck((bit(w[u],p)^a)===s,"raw wire");for(let j=0;j<5;j++)w[g.v0+5*i+j]=15*a});
  verify(g,w);out.physicalWitnesses++;return w;
 }
 function physicalCount(g,x){
  let D=g.vs.map(v=>v.kind==="E"?[0,15]:[3,5,6,9,10,12]);for(let i=0;i<x.length;i++)for(let j=0;j<2;j++){let v=g.carrier.get(`${i}:${j}`);if(v!==undefined)D[v]=[15*bit(x[i],j)]}
  let st=out.local;
  function rec(D){st.nodes++;let changed=true;while(changed){changed=false;st.sweeps++;for(let [u,p,v,q,s] of g.es){st.edgeScans++;let a=D[u].filter(i=>D[v].some(j=>(bit(i,p)^bit(j,q))===s));let b=D[v].filter(j=>a.some(i=>(bit(i,p)^bit(j,q))===s));if(!a.length||!b.length)return 0;if(a.length!==D[u].length||b.length!==D[v].length){st.deletions+=D[u].length+D[v].length-a.length-b.length;D[u]=a;D[v]=b;changed=true}}}
   let k=D.findIndex(a=>a.length>1);if(k<0){verify(g,D.map(a=>a[0]));return 1}let c=0;for(let a of D[k]){let E=D.slice();E[k]=[a];c+=rec(E)}return c
  }return rec(D)
 }
 for(let s=0;s<4;s++){let g=compile(2,[[0,1,s]]);for(let a=0;a<4;a++)for(let b=0;b<4;b++){let d=a^b^s,c=physicalCount(g,[a,b]);out.local.queries++;out.local.counts[c]=(out.local.counts[c]||0)+1;ck(c===(d===0?0:d===3?4:1),"physical multiplicity");if(c)lift(g,[a,b])}}
 function solve(n,edges,visit){let st=out.source;function rec(D){st.nodes++;let ch=true;while(ch){ch=false;st.sweeps++;for(let [u,v,s] of edges){st.edgeScans++;let a=D[u].filter(i=>D[v].some(j=>(i^j)!==s)),b=D[v].filter(j=>a.some(i=>(i^j)!==s));if(!a.length||!b.length)return;if(a.length!==D[u].length||b.length!==D[v].length){st.deletions+=D[u].length+D[v].length-a.length-b.length;D[u]=a;D[v]=b;ch=true}}}let k=D.findIndex(a=>a.length>1);if(k<0){visit(D.map(a=>a[0]));return}for(let a of D[k]){let E=D.slice();E[k]=[a];rec(E)}}rec(Array.from({length:n},()=>[0,1,2,3]))}
 const K=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)K.push([i,j,0]);
 function graphCase(name,n,edges,expected){let g=compile(n,edges),count=0,weighted=0n,raw=0n,ref=0;
  for(let i=0;i<4**n;i++){let x=Array.from({length:n},(_,j)=>Math.floor(i/4**j)%4);if(edges.every(([u,v,s])=>(x[u]^x[v])!==s))ref++}
  solve(n,edges,x=>{count++;lift(g,x);let k=edges.filter(([u,v,s])=>(x[u]^x[v]^s)===3).length;raw+=4n**BigInt(k);weighted+=4n**BigInt(edges.length)});
  ck(count===ref&&(expected===null||count===expected),"graph counts");out.graphs.push({name,n,m:edges.length,vertices:g.vs.length,edges:g.es.length,sourceModels:count,rawPhysicalCountByProvedFiber:raw.toString(),correctedScaledCount:weighted.toString()});return count
 }
 graphCase("K5",5,K,0);
 for(let i=0;i<K.length;i++){graphCase(`K5-e${i}`,5,K.filter((_,j)=>i!==j),24);graphCase(`K5-sign${i}`,5,K.map((e,j)=>j===i?[e[0],e[1],1]:e),24)}
 let seed=20261124;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 for(let t=0;t<16;t++){let n=3+rnd(3),e=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(rnd(3)!==0)e.push([i,j,rnd(4)]);graphCase(`random${t}`,n,e,null)}
 function wheelGraph(n,edges,copies){let e=[],nn=n,regions=[];for(let [a,b,d] of edges)for(let k=0;k<copies;k++){let t=1+k%3,rs=[nn++,nn++,nn++];for(let j=0;j<3;j++){e.push([rs[j],rs[(j+1)%3],0],[rs[j],a,j===0?t:0],[rs[j],b,j===0?d:d^t])}regions.push({a,b,d,t,rs})}return {n:nn,edges:e,regions}}
 function wheelCase(name,edges,copies){let W=wheelGraph(5,edges,copies),g=compile(W.n,W.edges),count=0,localChecks=0,actualLifts=0;for(let R of W.regions)for(let a=0;a<4;a++)for(let b=0;b<4;b++){let good=[];for(let i=0;i<64;i++){let r=[i&3,(i>>2)&3,(i>>4)&3];if(r.every((v,j)=>v!==r[(j+1)%3]&&v!==(a^(j===0?R.t:0))&&v!==(b^(j===0?R.d:R.d^R.t))))good.push(r)}localChecks++;ck(!!good.length===((a^b)!==R.d),"wheel projection")}
  solve(5,edges,x=>{count++;if(actualLifts>=2)return;let y=x.slice();for(let R of W.regions){let good=null;for(let i=0;i<64&&!good;i++){let r=[i&3,(i>>2)&3,(i>>4)&3];if(r.every((v,j)=>v!==r[(j+1)%3]&&v!==(x[R.a]^(j===0?R.t:0))&&v!==(x[R.b]^(j===0?R.d:R.d^R.t))))good=r}ck(good!==null,"wheel lift");R.rs.forEach((id,j)=>y[id]=good[j])}ck(W.edges.every(([u,v,s])=>(y[u]^y[v])!==s),"wheel graph verify");lift(g,y);actualLifts++});
  out.wheel.push({name,copies,sourceModels:count,signedWheelVertices:W.n,signedWheelEdges:W.edges.length,physicalVertices:g.vs.length,physicalEdges:g.es.length,localChecks,actualLifts});ck(count===(edges.length===10?0:24),"wheel source decision");
 }
 for(let copies of [1,2]){wheelCase("K5",K,copies);wheelCase("K5-e",K.slice(1),copies)}
 let fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];for(let skip=-1;skip<14;skip++){let count=0;for(let x=0;x<128;x++){if(fano.every((e,i)=>{let q=e.reduce((a,b)=>a+bit(x,b),0);return (skip===2*i||q>0)&&(skip===2*i+1||q<3)}))count++}ck(count===(skip<0?0:5),"fano");out.fano.push({skip,count})}
 return out;
}
console.log(JSON.stringify(run(),null,2));
