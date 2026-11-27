function audit(){
 const stats={checks:0,sourceTrials:0,localTrials:0,completionRows:0,matchingEdgeVisits:0},cap=2e6;function tick(k){stats[k]++;if(Object.values(stats).reduce((a,b)=>a+b,0)>cap)throw Error("partial reference cap exceeded")}function ck(v,msg){tick("checks");if(!v)throw Error(msg)}
 const rng=n=>Array.from({length:n},(_,i)=>i), nae=a=>a.some(v=>v!==a[0]),pairKey=(a,b)=>a<b?`${a}:${b}`:`${b}:${a}`;
 const ag=[...rng(3).map(r=>rng(3).map(c=>3*r+c)),...rng(3).map(c=>rng(3).map(r=>3*r+c)),...rng(3).map(k=>rng(3).map(r=>3*r+(r+k)%3)),...rng(3).map(k=>rng(3).map(r=>3*r+(k-r+3)%3))];
 const n=9, source=ag.map((v,id)=>({id,v,p:Math.floor(id/3)}));
 function validate(rows,n,full){let seen=new Set(),deg=Array.from({length:n},()=>[0,0,0,0]);for(let r of rows){ck(r.v.length===3&&new Set(r.v).size===3,"distinct");for(let v of r.v){ck(v>=0&&v<n,"range");ck(++deg[v][r.p]===1,"color conflict")}for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let k=pairKey(r.v[i],r.v[j]);ck(!seen.has(k),"nonlinear");seen.add(k)}}if(full)for(let d of deg)ck(d.every(x=>x===1),"not complete");return deg}
 validate(source,n,true);
 function compile(tails){
  let N=4*n, rows=[],guard={},links=[],M=[],tailIDs=[];
  function owner(v,p,kind,rep,sourceID){let id=rows.length;rows.push({id,v,p,kind,sourceID});M.push(rep);return id}
  for(let r of source)owner(r.v.map(v=>4*v+r.p),2,"source",4*r.v[0]+r.p,r.id);
  for(let v=0;v<n;v++)for(let p=0;p<4;p++){let a=4*v+p,b=4*v+(p+1)%4,u=N++,one=N++,zero=N++;guard[one]=1;guard[zero]=0;let aID=owner([a,u,one],0,"nand",one,v),bID=owner([u,b,zero],1,"or",zero,v);links.push({a,b,u,one,zero,aID,bID,v})}
  for(let t=0;t<tails;t++){let a=t===0?0:tailIDs[t-1].free,b=N++,p=N++;guard[p]=t%2;let id=owner([a,b,p],t%2===0?3:0,"tail",b,-1);tailIDs.push({id,free:b,p})}
  const deg=validate(rows,N,false);
  ck(M.length===rows.length&&new Set(M).size===M.length&&rows.every((r,i)=>r.v.includes(M[i])),"explicit full matching");
  return {N,rows,guard,links,M,deg,tailIDs}
 }
 function match(rows,allowed){
   const M=new Map(),ownerTo=new Map();
   function aug(i,seen){for(let v of rows[i].v){tick("matchingEdgeVisits");if(!allowed(v)||seen.has(v))continue;seen.add(v);if(!M.has(v)||aug(M.get(v),seen)){M.set(v,i);ownerTo.set(i,v);return true}}return false}
   for(let i=0;i<rows.length;i++)aug(i,new Set());
   return {M,ownerTo};
 }
 function dm(rows,guard){
  let {M,ownerTo}=match(rows,v=>!(v in guard)),R=new Set(),V=new Set(),q=[];
  for(let i=0;i<rows.length;i++)if(!ownerTo.has(i)){R.add(i);q.push(i)}
  for(let j=0;j<q.length;j++)for(let v of rows[q[j]].v){if(v in guard||V.has(v))continue;V.add(v);ck(M.has(v),"augmenting path from unmatched row");let i=M.get(v);if(!R.has(i)){R.add(i);q.push(i)}}
  ck(R.size-V.size===rows.length-M.size,"deficiency preservation");
  let outside=rows.filter((r,i)=>!R.has(i));ck(outside.every(r=>ownerTo.has(r.id)&&!V.has(ownerTo.get(r.id))),"outside match");
  return {matching:M.size,defect:rows.length-M.size,coreRows:[...R].sort((a,b)=>a-b),coreFree:[...V].sort((a,b)=>a-b),outside:outside.map(r=>r.id)}
 }
 // Track B: independent exact 2-SAT closure on pinned NAND/OR rows. Literal index 2*v+truth.
 function closure(H){
  const N=H.N*2,A=Array.from({length:N},()=>[]);
  function clause(v,b,w,c){A[2*v+(1-b)].push(2*w+c);A[2*w+(1-c)].push(2*v+b)}
  for(let r of H.rows){let free=r.v.filter(v=>!(v in H.guard)),pins=r.v.filter(v=>v in H.guard);if(free.length===2&&pins.length===1){let c=1-H.guard[pins[0]];clause(free[0],c,free[1],c)}}
  function reach(s){let seen=new Set([s]),q=[s];for(let i=0;i<q.length;i++)for(let v of A[q[i]])if(!seen.has(v)){seen.add(v);q.push(v)}return seen}
  let eq=[];for(let v=0;v<n;v++){let base=4*v,R=reach(2*base+1),Z=reach(2*base);for(let p=1;p<4;p++){let w=base+p;ck(R.has(2*w+1)&&Z.has(2*w)&&reach(2*w+1).has(2*base+1)&&reach(2*w).has(2*base),"SCC equality");eq.push([base,w,0])}
   for(let l of H.links.filter(l=>l.v===v)){ck(R.has(2*l.u)&&Z.has(2*l.u+1)&&reach(2*l.u).has(2*base+1)&&reach(2*l.u+1).has(2*base),"SCC opposition");eq.push([base,l.u,1])}}
  return eq
 }
 // Track C: full constant local truth check and independent 12-copy completion.
 const alpha=[0,2,3,1],phase=k=>k<4?0:1;
 function complete(H){
  const rows=[];for(let k=0;k<12;k++)for(let r of H.rows)rows.push({id:rows.length,v:r.v.map(v=>k*H.N+v),p:r.p,kind:"copy",origin:[k,r.id]});
  for(let v=0;v<H.N;v++)for(let p=0;p<4;p++)if(H.deg[v][p]===0)for(let j=0;j<4;j++){let ks=[j,4+(j^p),8+(j^alpha[p])];rows.push({id:rows.length,v:ks.map(k=>k*H.N+v),p,kind:"fill",origin:[v,p,j]})}
  validate(rows,H.N*12,true);
  // Every copied clause and filler is satisfied under the phase section iff its base row is satisfied (fillers always).
  for(let r of rows){if(r.kind==="fill"){for(let b=0;b<2;b++){tick("localTrials");ck(nae(r.v.map(v=>b^phase(Math.floor(v/H.N)))),"filler phase identity")}}else{for(let w=0;w<8;w++){tick("localTrials");ck(nae(r.v.map((v,i)=>((w>>i)&1)^phase(Math.floor(v/H.N))))===nae(rng(3).map(i=>(w>>i)&1)),"copied clause identity")}}tick("completionRows")}
  return {N:H.N*12,rows,guard:H.guard,centralCopy:0};
 }
 let linkTable=[];for(let a=0;a<2;a++)for(let b=0;b<2;b++){let u=[];for(let x=0;x<2;x++){tick("localTrials");if(nae([a,x,1])&&nae([x,b,0]))u.push(x)}ck((u.length>0)===(a<=b),"implication exact");linkTable.push({a,b,u})}
 let sourceWords=0,sourceNO=0;for(let w=0;w<(1<<n);w++){tick("sourceTrials");let ok=source.every(r=>nae(r.v.map(v=>(w>>v)&1)));if(ok)sourceWords++;else sourceNO++}
 ck(sourceWords===0,"native NO");
 let cases=[];
 for(let tails of [0,2]){
  let H=compile(tails),raw=match(H.rows,()=>true),free=dm(H.rows,H.guard),eq=closure(H);
  ck(raw.M.size===H.rows.length,"raw Hall");ck(free.defect===source.length,"free defect m");ck(free.coreRows.length===source.length+8*n&&free.coreFree.length===8*n&&free.outside.length===tails,"DM expected core");
  let collapsed=H.rows.map(r=>({...r,v:[...new Set(r.v.map(v=>v in H.guard?-1:v))]})),cm=match(collapsed,()=>true);
  ck(H.rows.length-cm.M.size===source.length-1,"one-anchor deficit");
  let Q=source.map(r=>({...r}));let qm=match(Q,()=>true);ck(qm.M.size===n,"quotient column matching");
  // Check exact section for each original word, including NO words: every link satisfied, source rows exactly preserved.
  for(let w=0;w<(1<<n);w++){tick("sourceTrials");let z=Array(H.N).fill(0);for(let [k,v] of Object.entries(H.guard))z[+k]=v;for(let v=0;v<n;v++)for(let p=0;p<4;p++)z[4*v+p]=(w>>v)&1;for(let l of H.links)z[l.u]=1-z[l.a];for(let t of H.tailIDs){let r=H.rows[t.id];z[t.free]=1-z[r.v[0]]}
    for(let r of H.rows){let ok=nae(r.v.map(v=>z[v]));ck(ok===(r.kind==="source"?nae(source[r.sourceID].v.map(v=>(w>>v)&1)):true),"guarded section")}
  }
  let G=complete(H);
  // Actual native source guard pins only central copy; explicit phase projection is exact for every H assignment.
  ck(G.rows.length===4*G.N/3,"native counts");
  // Separate adversarial: ignoring guards makes a satisfying assignment; set each clone chosen independently to make its source triple mixed, then choose each NAND/OR pin opposite equal pair (otherwise arbitrary).
  let unguarded=Array(H.N).fill(0);for(let r of H.rows.filter(x=>x.kind==="source"))unguarded[r.v[0]]=1;
  for(let r of H.rows.filter(x=>x.kind==="nand"||x.kind==="or"||x.kind==="tail")){let p=r.v.find(v=>v in H.guard),rest=r.v.filter(v=>v!==p);unguarded[p]=1-unguarded[rest[0]]}ck(H.rows.every(r=>nae(r.v.map(v=>unguarded[v]))),"unguarded falsifier witness");
  let uFull=rng(12).flatMap(k=>unguarded.map(v=>v^phase(k)));ck(G.rows.every(r=>nae(r.v.map(v=>uFull[v]))),"native unguarded witness");
  ck(Object.entries(H.guard).some(([p,v])=>unguarded[+p]!==v),"witness not guarded");
  cases.push({tails,partial:{variables:H.N,owners:H.rows.length,guard:H.guard,rows:H.rows,links:H.links,matching:H.M},native:G,rawMatching:raw.M.size,freeDeficiency:free.defect,freeCore:free,collapsedDeficiency:H.rows.length-cm.M.size,closureEqualities:eq,quotient:{variables:n,owners:source.length,defect:source.length-qm.M.size,source},unguardedFalsifier:unguarded,guardedResult:"NO by exact source map and exhaustive source count"});
 }
 return {source,n,sourceWords,sourceNO,linkTable,stats,cap,cases};
}
console.log(JSON.stringify(audit(),null,2));
