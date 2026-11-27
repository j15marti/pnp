function verify(net,cnf,Z,sha){
 const A=(b,m)=>{if(!b)throw Error(m)},J=x=>JSON.stringify(x)+"\n",H=x=>sha(J(x)),sort=a=>[...new Set(a)].sort((a,b)=>a-b),eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),N=4*net.types.length;
 let work={dsu:0,local:0,projection:0,proofRows:0,coverage:0};
 const par=Int32Array.from({length:N},(_,i)=>i),bit=new Uint8Array(N);
 function find(x){let p=par[x];if(p===x)return [x,0];let [r,s]=find(p);bit[x]^=s;par[x]=r;return [r,bit[x]]}
 function union(x,y,b){work.dsu++;let [r,s]=find(x),[t,u]=find(y);if(r===t){A((s^u)===b,"edge parity");return}if(r>t)[r,t]=[t,r];par[t]=r;bit[t]=s^u^b}
 let edges=new Set(),ports=new Set();for(let [a,b,s]of net.edges){let v=a>>2,w=b>>2,k=Math.min(v,w)+":"+Math.max(v,w);A(v!==w&&!edges.has(k)&&!ports.has(a)&&!ports.has(b)&&[0,1].includes(s)&&a>=0&&b>=0&&a<N&&b<N,"native strict");edges.add(k);ports.add(a);ports.add(b);union(a,b,s)}A(ports.size===N,"degree");
 for(let i=0;i<net.types.length;i++){A(["E","B"].includes(net.types[i]),"type");if(net.types[i]==="E")for(let j=1;j<4;j++)union(4*i,4*i+j,0)}
 let roots=[],signs=[];for(let i=0;i<N;i++){let [r,s]=find(i);roots.push(r);signs.push(s)}A(H([roots,signs])===Z.projection.rootMapHash,"map digest");
 function rows(scope,test){let out=[];for(let i=0;i<2**scope.length;i++){let a=new Map(scope.map((v,j)=>[v,(i>>j)&1]));if(test(a))out.push(i)}return out}
 function allowed(f,a){let r=0;for(let i=0;i<f.v.length;i++)r|=a.get(f.v[i])<<i;return f.r.includes(r)}
 let F=[];for(let i=0;i<net.types.length;i++)if(net.types[i]==="B"){let p=[4*i,4*i+1,4*i+2,4*i+3],v=sort(p.map(x=>roots[x]));let r=rows(v,a=>{work.local++;return p.reduce((s,x)=>s+(a.get(roots[x])^signs[x]),0)===2});F.push({v,r,s:[i]})}
 function dedup(F){let M=new Map();for(let f of F){let k=JSON.stringify([f.v,f.r]);if(!M.has(k))M.set(k,f)}return [...M.values()]}
 F=dedup(F);A(F.length===Z.projection.initial,"initial count");
 for(let t of Z.projection.trace){let all=F.filter(f=>f.v.includes(t.pivot));A(eq(all,t.parents),"parent scope");let v=sort(all.flatMap(f=>f.v)).filter(x=>x!==t.pivot);A(eq(v,t.out.v),"retained coordinates");let r=rows(v,a=>{let yes=false;for(let b of [0,1]){a.set(t.pivot,b);work.projection++;if(all.every(f=>allowed(f,a)))yes=true}return yes});A(eq(r,t.out.r)&&eq(sort(all.flatMap(f=>f.s)),t.out.s),"projection");F=dedup(F.filter(f=>!all.includes(f)).concat(t.out))}
 A(eq(F,Z.projection.F),"final registry");
 let cnF=cnf.map((c,i)=>{let v=sort(c.map(Math.abs));return {v,r:rows(v,a=>c.some(l=>a.get(Math.abs(l))===Number(l>0))),s:[i+1]}});
 function checkTree(F,g,t,support){let S=new Set(support),R=F.filter(f=>f.s.every(i=>S.has(i)));let V=new Set(F.flatMap(f=>f.v));function go(g,t){if(!t)return false;if(!t.leaf){if(!V.has(t.x)||g.some(([v])=>v===t.x))return false;return go(g.concat([[t.x,0]]),t.lo)&&go(g.concat([[t.x,1]]),t.hi)}let d=new Map([...V].map(v=>[v,3]));for(let [v,b]of g){if(!V.has(v)||!(d.get(v)&(1<<b)))return false;d.set(v,1<<b)}for(;;){let change=false;for(let f of R){let masks=f.v.map(()=>0),found=false;for(let w of f.r){work.proofRows++;if(f.v.every((v,j)=>d.get(v)&(1<<((w>>j)&1)))){found=true;for(let j=0;j<f.v.length;j++)masks[j]|=1<<((w>>j)&1)}}if(!found)return true;for(let j=0;j<f.v.length;j++){let v=f.v[j],x=d.get(v)&masks[j];if(x!==d.get(v)){d.set(v,x);change=true}}}if(!change)return false}}return go(g,t)}
 function lanes(F,L,instanceId,kind){
  let anchor=L.anchor,base=anchor===null?[]:[[anchor,0]],k=L.V.length-base.length,coverage=0,coord=sort(L.guards.flat().map(x=>x[0]));
  if(anchor!==null)A(F.every(f=>f.r.every(r=>f.r.includes((2**f.v.length-1)^r))),"complement gauge");
  A(eq(sort(F.flatMap(f=>f.v)),sort(L.V)),"carrier");
  for(let w=0;w<2**coord.length;w++){work.coverage++;let x=new Map(coord.map((v,j)=>[v,(w>>j)&1]));A(L.guards.filter(g=>g.every(([v,b])=>x.get(v)===b)).length===1,"partition");coverage++}
  let guardRecords=[];for(let i=0;i<5;i++){let g=L.guards[i],t=L.results[i][4].tree,check=L.checks[i];A(check&&checkTree(F,base.concat(g),t,check.support),"support tree "+i);let artifact=kind==="EB"?{schema:"EB-RELATIVE-PORT-PINS-v1",anchor,pins:g.slice().sort((a,b)=>a[0]-b[0])}:g.slice().sort((a,b)=>a[0]-b[0]);let schema=kind==="EB"?"EB-RELATIVE-PORT-PINS-v1":"CNF-VAR-PINS-v1",guardHash=H(artifact),gid="GUARD-v1:sha256:"+H(["PNP-GUARD-v1",instanceId,schema,guardHash]);let map=kind==="EB"?Z.projection.rootMapHash:"IDENTITY",res={relations:F,guard:artifact},resHash=H(res),rschema="T4-EXACT-ROW-REGISTRY-v1",rid="RESIDUAL-v1:sha256:"+H(["PNP-RESIDUAL-v1",instanceId,gid,rschema,resHash,map]);guardRecords.push({guard_id:gid,guard_schema:schema,guard_artifact:artifact,guard_artifact_sha256:guardHash,residual_id:rid,residual_artifact_sha256:resHash,map_sha256:map,original_support:check.support,proof:t})}
  A(BigInt(L.covered)===1n<<BigInt(k),"coverage count");
  // explicit independent inclusion-exclusion: verify each count against assignment enumeration on the four guard coordinates
  for(let q of L.counts){let num=0;for(let w=0;w<2**coord.length;w++){work.coverage++;let a=new Map(coord.map((v,j)=>[v,(w>>j)&1]));if(L.guards.every((g,i)=>!(q.subset>>i&1)||g.every(([v,b])=>a.get(v)===b)))num++}A(BigInt(q.count)===(BigInt(num)<<BigInt(k-coord.length)),"intersection count")}
  let mutated=checkTree(F,base.concat(L.guards[0]),{leaf:true},[]);A(!mutated,"reject empty support");
  return {guards:guardRecords,union:sort(guardRecords.flatMap(x=>x.original_support)),carrierDimension:k,coveragePatterns:coverage,mutatedRejected:true}
 }
 let native=lanes(F,Z.native,Z.registry.instance_id,"EB"),cn=lanes(cnF,Z.cn,Z.registry.source_cnf.instance_id,"CNF");
 return {work,native,cn};
}
module.exports={verify};
