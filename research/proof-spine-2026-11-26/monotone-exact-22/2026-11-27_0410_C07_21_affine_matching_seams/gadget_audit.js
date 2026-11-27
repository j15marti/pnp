function gadgetAudit(){
 const assert=(v,m)=>{if(!v)throw Error(m||"assert")};
 const defs=[
  {id:"parallel-equal-imbalance",d:[1,2],groups:[[[0,0],[3,0]],[[1,0],[4,0]],[[2,0],[5,0]]]},
  {id:"parallel-opposite-imbalance",d:[1,1],groups:[[[0,0],[3,1]],[[1,0],[4,1]],[[2,0],[5,1]]]},
  {id:"mixed-parity-imbalance",d:[1,1],groups:[[[0,0],[3,1]],[[1,0],[4,0]],[[2,0],[5,0]]]},
  {id:"loops-and-singleton",d:[1,2,1],groups:[[[0,0],[1,0]],[[3,0],[4,1]],[[2,0],[6,0]],[[5,0],[7,0]],[[8,0]]]},
  {id:"minimal-correctness-control",d:[1,2,2],groups:[[[0,0],[1,0]],[[3,0],[4,1]],[[2,0],[6,0]],[[5,0],[7,0]],[[8,0]]]}
 ];
 const out=[];
 for(const def of defs){
  const P=3*def.d.length;let n=P+2,rows=[],guards=[[0,0],[1,1]],aux=[];
  for(const group of def.groups){if(group.length===1){aux.push(-1);continue}const [[a,s],[b,t]]=group;
   if(s===t){let h=n++;aux.push(h);rows.push([2+a,h,0,1],[2+b,h,0,1])}
   else {aux.push(-1);rows.push([2+a,2+b,0,1])}}
  def.d.forEach((d,i)=>rows.push([2+3*i,3+3*i,4+3*i,d===1?1:0]));
  const F={n,rows,guards,def,aux};let h=2166136261;for(const c of JSON.stringify(F))h=Math.imul(h^c.charCodeAt(0),16777619)>>>0;
  // Exact native reference: enumerate independent group phases and lift all private IDs.
  let native=0,trials=0,checks=0;
  for(let m=0;m<2**def.groups.length;m++){
   let v=Array(n).fill(-1);v[0]=0;v[1]=1;
   for(let i=0;i<def.groups.length;i++){let bit=(m>>i)&1;for(let [p,s] of def.groups[i])v[p+2]=bit^s;if(aux[i]>=0)v[aux[i]]=1-v[def.groups[i][0][0]+2]}
   assert(v.every(x=>x===0||x===1));trials++;
   if(rows.every(r=>{checks++;return r.reduce((a,j)=>a+v[j],0)===2}))native++;
  }
  // Port matching gadget; matching enumeration is only a small independent test, not the claimed poly solver.
  let a=Array.from({length:P},()=>[]),pool=[],opp=0;
  function addV(){a.push([]);return a.length-1}
  function edge(u,v){a[u].push(v);a[v].push(u)}
  for(let i=0;i<def.d.length;i++)for(let j=0;j<3-def.d[i];j++){let v=addV();for(let p=3*i;p<3*i+3;p++)edge(v,p)}
  for(let group of def.groups){
   if(group.length===1){let q=addV();pool.push(q);edge(group[0][0],q)}
   else if(group[0][1]===group[1][1])edge(group[0][0],group[1][0]);
   else{let v=addV();edge(v,group[0][0]);edge(v,group[1][0]);opp++}}
  if(a.length%2)pool.push(addV());
  for(let i=0;i<pool.length;i++)for(let j=i+1;j<pool.length;j++)edge(pool[i],pool[j]);
  let visited=0,tries=0,memo=new Map();
  function pm(mask){visited++;if(!mask)return true;if(memo.has(mask))return memo.get(mask);let u=0;while(!(mask&(1<<u)))u++;for(let v of a[u]){tries++;if((mask&(1<<v))&&pm(mask^(1<<u)^(1<<v))){memo.set(mask,true);return true}}memo.set(mask,false);return false}
  assert(a.length<30);let got=pm((1<<a.length)-1);assert(got===(native>0));assert((native>0)===(def.id==="minimal-correctness-control"),"unexpected witness classification");
  out.push({id:def.id,fingerprint:h.toString(16),nativeVariables:n,nativeRows:rows.length,nativeTrials:trials,nativeChecks:checks,nativeWitnesses:native,matchingVertices:a.length,oppositePairs:opp,singletons:def.groups.filter(g=>g.length===1).length,matchingVisited:visited,matchingEdgeTries:tries,matchingExists:got,source:F});
 }
 return out;
}
console.log(JSON.stringify(gadgetAudit(),null,2));
