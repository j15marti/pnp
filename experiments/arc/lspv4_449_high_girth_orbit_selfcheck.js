// LSPV-4/449: independent finite self-check of girth/expansion orbit bound.
// Run: node -e 'console.log(require("./lspv4_449_high_girth_orbit_selfcheck.js"))'
// Alternatively: node lspv4_449_high_girth_orbit_selfcheck.js
function run449() {
  const graphs=[];
  const K=[]; for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)K.push([u,v]);
  graphs.push(["K4",4,K]);
  const C=[];for(let u=0;u<8;u++)for(let v=u+1;v<8;v++)if([1,2,4].includes(u^v))C.push([u,v]);
  graphs.push(["cube",8,C]);
  const P=[];for(let u=0;u<5;u++) {
    P.push([u,(u+1)%5].sort((a,b)=>a-b));
    P.push([u+5,5+(u+2)%5].sort((a,b)=>a-b));
    P.push([u,u+5]);
  }
  graphs.push(["Petersen",10,P]);
  const H=[];for(let l=0;l<7;l++)for(let p=0;p<7;p++)
    if([0,1,3].includes((p-l+7)%7))H.push([p,7+l]);
  graphs.push(["Heawood",14,H]);
  function girth(n,E) {
    let best=n+1;
    for(let s=0;s<n;s++) {
      const depth=Array(n).fill(-1),parent=Array(n).fill(-1),q=[s];depth[s]=0;
      for(let i=0;i<q.length;i++)for(const [u,v] of E) {
        const a=q[i],b=u===a?v:(v===a?u:-1);if(b<0)continue;
        if(depth[b]<0){depth[b]=depth[a]+1;parent[b]=a;q.push(b);}
        else if(parent[a]!==b)best=Math.min(best,depth[a]+depth[b]+1);
      }
    }
    return best;
  }
  function expansion(n,E) {
    let num=99,den=1;
    for(let mask=1;mask<(1<<n);mask++) {
      let size=0;for(let i=0;i<n;i++)size+=(mask>>i)&1;
      if(size>n/2)continue;
      let cut=0;for(const [u,v] of E)cut+=(((mask>>u)&1)!==((mask>>v)&1));
      if(cut*den<num*size){num=cut;den=size;}
    }
    return [num,den];
  }
  function components(n,E,omit) {
    const seen=new Set(),out=[];
    for(let s=0;s<n;s++) {
      if(seen.has(s))continue;
      let Q=[s],V=new Set([s]);seen.add(s);
      while(Q.length) {
        const a=Q.pop();
        for(let j=0;j<E.length;j++) {
          if(omit.has(j))continue;
          const [u,v]=E[j],b=u===a?v:(v===a?u:-1);
          if(b>=0&&!seen.has(b)){seen.add(b);V.add(b);Q.push(b);}
        }
      }
      let edges=0;E.forEach(([u,v],j)=>{if(!omit.has(j)&&V.has(u)&&V.has(v))edges++;});
      out.push({size:V.size,cyclic:edges>=V.size});
    }
    return out;
  }
  function subsets(m,k,fn) {
    function rec(start,S) {
      if(S.length===k){fn(S);return;}
      for(let i=start;i<m;i++)rec(i+1,S.concat(i));
    }
    rec(0,[]);
  }
  const counters={subset:0,one_orbit:0,giant:0};const rows=[];
  let cubeSharp=false;
  for(const [name,n,E] of graphs) {
    const g=girth(n,E),[hnum,hden]=expansion(n,E);
    let maxb=0;
    for(let k=0;k<=Math.min(4,n/2);k++)subsets(E.length,k,S=>{
      const parts=components(n,E,new Set(S));
      const b=parts.filter(x=>x.cyclic).length;
      if(b<1||(b-1)*hnum*g>2*k*hden)
        throw Error("girth-expansion bound fails "+name+"/"+k);
      counters.subset++;
      if(k*hden<hnum*g) {
        if(b!==1)throw Error("strict one orbit fails "+name+"/"+k);
        counters.one_orbit++;
      }
      if(2*k*hden<hnum*n) {
        if(parts.filter(x=>x.size>n/2).length!==1)
          throw Error("unique giant fails "+name+"/"+k);
        counters.giant++;
      }
      if(name==="cube"&&k===4&&b===2)cubeSharp=true;
      maxb=Math.max(maxb,b);
    });
    rows.push({name,n,edges:E.length,girth:g,hnum,hden,maxb});
  }
  if(counters.subset!==10304||counters.one_orbit!==9809||
     counters.giant!==9809||!cubeSharp)throw Error("count mismatch");
  return {result:"PASS",counters,rows,cubeSharp,
          note:"Finite structural control; host runtime is not an FLMV trace."};
}
const result449=run449();
if(typeof module!=="undefined"&&module.exports)module.exports=result449;
if(typeof console!=="undefined"&&typeof process!=="undefined"&&require.main===module)
 console.log(JSON.stringify(result449,null,2));
return result449;