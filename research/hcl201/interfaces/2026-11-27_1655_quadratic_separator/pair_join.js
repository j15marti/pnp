/* P is the pinned module 2026-11-27_1513_feedback.js. */
function joins(F,guard){
 const A=new Map(guard),R=F.map(f=>{let vs=f.vs.filter(v=>!A.has(v)),rows=[...new Set(f.rows.filter(w=>f.vs.every((v,j)=>!A.has(v)||A.get(v)===((w>>j)&1))).map(w=>vs.reduce((a,v,j)=>a|(((w>>f.vs.indexOf(v))&1)<<j),0)))];return {vs,rows,owners:f.owners}});
 const C=P.cnf(R),keys=new Set(C.map(c=>c.join(","))),learned=[];let pairs=0,eligible=0,words=0,replay=0;
 for(let i=0;i<R.length;i++)for(let j=i+1;j<R.length;j++){
  pairs++;const a=R[i],b=R[j],common=a.vs.filter(v=>b.vs.includes(v)),vs=[...new Set([...a.vs,...b.vs])].sort((a,b)=>a-b);
  if(common.length<2||vs.length>5)continue;eligible++;
  const rows=[];for(let w=0;w<2**vs.length;w++){words++;if([a,b].every(f=>f.rows.includes(f.vs.reduce((z,v,k)=>z|(((w>>vs.indexOf(v))&1)<<k),0))))rows.push(w)}
  const scopes=vs.map(v=>[v]);for(let k=0;k<vs.length;k++)for(let l=k+1;l<vs.length;l++)scopes.push([vs[k],vs[l]]);
  for(const scope of scopes)for(let z=0;z<2**scope.length;z++){
   if(rows.some(w=>scope.every((v,k)=>((w>>vs.indexOf(v))&1)===((z>>k)&1))))continue;
   const c=scope.map((v,k)=>(z>>k)&1?-v:v);if(keys.has(c.join(",")))continue;
   // Verify directly on pairs of original allowed words, not on computed joined response.
   for(const x of a.rows)for(const y of b.rows){replay++;const va=new Map(a.vs.map((v,k)=>[v,(x>>k)&1])),vb=new Map(b.vs.map((v,k)=>[v,(y>>k)&1]));if(common.some(v=>va.get(v)!==vb.get(v)))continue;if(scope.every((v,k)=>(va.has(v)?va.get(v):vb.get(v))===((z>>k)&1)))throw Error("join exclusion replay");}
   keys.add(c.join(","));learned.push({i,j,c});
  }
 }
 return {C,learned,pairs,eligible,words,replay}
}
function coverage(gs,n){let total=0n,counts=[];for(let mask=1;mask<(1<<gs.length);mask++){let A=new Map(),ok=true,k=0;for(let i=0;i<gs.length;i++)if(mask>>i&1){k++;for(const [v,b] of gs[i]){if(A.has(v)&&A.get(v)!==b)ok=false;A.set(v,b)}}const size=ok?1n<<BigInt(n-A.size):0n;total+=k%2?size:-size;counts.push([mask,size.toString()])}return {counts,total:total.toString(),expected:(1n<<BigInt(n)).toString(),ok:total===(1n<<BigInt(n))}}
module.exports={joins,coverage};
