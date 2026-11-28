function audit(ctx,packet,peer){
 const F=ctx.chart,m=F.length;let cnt={pairCandidates:0,tripleCandidates:0,compatibilityBits:0,rowCandidates:0,witnesses:0,packetRows:0,packetProjections:0};let scopes=F.map(f=>new Set(f.vs)),adj=F.map(()=>new Set()),pairs=[],triples=[];
 const intersects=(i,j)=>F[i].vs.some(v=>scopes[j].has(v));const width=ids=>new Set(ids.flatMap(i=>F[i].vs)).size;
 for(let i=0;i<m;i++)for(let j=i+1;j<m;j++){cnt.pairCandidates++;if(intersects(i,j)){adj[i].add(j);adj[j].add(i);if(width([i,j])<=5)pairs.push([i,j])}}
 // Independent enumeration: enumerate all unordered triples, rather than deduplicate centers. Explicit charge.
 for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)for(let k=j+1;k<m;k++){cnt.tripleCandidates++;let links=Number(adj[i].has(j))+Number(adj[i].has(k))+Number(adj[j].has(k));if(links>=2&&width([i,j,k])<=5)triples.push([i,j,k])}
 function assign(f,w,A){let B=new Map(A);for(let j=0;j<f.vs.length;j++){cnt.compatibilityBits++;let v=f.vs[j],bit=(w>>j)&1;if(B.has(v)&&B.get(v)!==bit)return null;B.set(v,bit)}return B}
 // For every row, find a witness with other owner factors simultaneously zero. This proves exact equality
 // of UNCLIPPED conditional minimum and own original row cost, stronger than a clipped fixed point.
 let result=[];
 for(let ids of [...pairs,...triples]){
  let witnesses=[];
  for(let i of ids){let f=F[i],others=ids.filter(j=>j!==i);for(let w=0;w<f.cost.length;w++){
    function seek(t,A,W){if(t===others.length)return W;let g=F[others[t]];for(let z=0;z<g.cost.length;z++){cnt.rowCandidates++;if(g.cost[z])continue;let B=assign(g,z,A);if(B){let out=seek(t+1,B,[...W,z]);if(out)return out}}return null}
    let W=seek(0,assign(f,w,new Map()),[]);if(W===null)throw Error("counterexample "+ids+" "+i+" "+w);cnt.witnesses++;witnesses.push([i,w,...W]);
   }}
  result.push({ids,witnesses})
 }
 if(packet.chartHash!==ctx.chartHash||packet.mapHash!==ctx.mapHash||peer.chart_sha256!==ctx.chartHash||peer.map_sha256!==ctx.mapHash)throw Error("map mismatch");
 // Verify full rational packet on all pair intersections, including multiplicities.
 let supp=packet.support;for(let [i,rows] of supp.entries()){if(rows.length!==4)throw Error("mass denominator");for(let w of rows){cnt.packetRows++;if(F[i].cost[w]!==0)throw Error("not zero row")}}
 let pairChecked=0;for(let i=0;i<m;i++)for(let j of adj[i])if(i<j){let S=F[i].vs.filter(v=>scopes[j].has(v));function project(f,rows){let out=Array(2**S.length).fill(0);for(let w of rows){let x=0;for(let k=0;k<S.length;k++){cnt.packetProjections++;x|=((w>>f.vs.indexOf(S[k]))&1)<<k}out[x]++}return out}if(JSON.stringify(project(F[i],supp[i]))!==JSON.stringify(project(F[j],supp[j])))throw Error("marginal mismatch");pairChecked++}
 const ps=peer.proof,ids=ps.factors.map(f=>f.index),U=ps.union_original_roots,A=new Map(ps.positive_word_original_roots);
 if(ctx.gauge!==10)throw Error("gauge");for(const x of ps.factors){let f=F[x.index];if(JSON.stringify(f.vs)!==JSON.stringify(x.roots)||JSON.stringify(f.ids)!==JSON.stringify(x.owners)||JSON.stringify(supp[x.index])!==JSON.stringify(x.support))throw Error("peer source mismatch")}
 let fixed=F[ps.factor].vs.reduce((w,v,j)=>w|(A.get(v)<<j),0);if(supp[ps.factor].filter(w=>w===fixed).length!==ps.mass_numerator||ps.mass_denominator!==4)throw Error("mass mismatch");
 const rows=[];for(let w=0;w<2**U.length;w++){let a=new Map(U.map((v,j)=>[v,(w>>j)&1]));if([...A].some(([v,x])=>a.get(v)!==x))continue;let ws=ids.map(i=>F[i].vs.reduce((z,v,j)=>z|(a.get(v)<<j),0));rows.push({word:w,assignment:[...a],factorRows:ws,packet:ws.map((z,j)=>supp[ids[j]].includes(z)),cost:ws.map((z,j)=>F[ids[j]].cost[z])})}
 if(rows.some(r=>r.packet.every(Boolean)))throw Error("peer falsified");
 let min=Math.min(...rows.map(r=>r.cost.reduce((a,b)=>a+b,0)));if(min!==0)throw Error("packet versus source distinction not verified");
 // Alternative triple joint probability distribution, local only: delta on exact zero-cost extension.
 const witness=rows.find(r=>r.cost.every(z=>z===0));
 return {cnt,pairs:pairs.length,triples:triples.length,pairChecked,result,peer:{ids,U,fixed,rows,min,witness}};
}
if(typeof module!=="undefined")module.exports={audit};
