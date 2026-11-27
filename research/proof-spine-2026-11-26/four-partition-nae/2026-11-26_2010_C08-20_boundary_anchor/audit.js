function audit(){
 const out={version:"C08-20-v1",cases:[],controls:{},counts:{assertions:0,wordTrials:0,matchingTerms:0,separatorTrials:0},cap:10000000};
 function check(t,msg){out.counts.assertions++;if(!t)throw Error(msg)}
 function tick(k){out.counts[k]++;if(Object.values(out.counts).reduce((a,b)=>a+b,0)>out.cap)throw Error("reference cap")}
 const rng=n=>Array.from({length:n},(_,i)=>i);
 const pairs=a=>a.flatMap((x,i)=>a.slice(i+1).map(y=>[x,y]));
 const key=a=>a.slice().sort((a,b)=>a-b).join(",");
 const ag=[...rng(3).map(r=>rng(3).map(c=>3*r+c)),...rng(3).map(c=>rng(3).map(r=>3*r+c)),...rng(3).map(k=>rng(3).map(r=>3*r+(r+k)%3)),...rng(3).map(k=>rng(3).map(r=>3*r+(k-r+3)%3))];
 const fano=[];for(let i=1;i<8;i++)for(let j=i+1;j<8;j++){let k=i^j;if(j<k)fano.push([i,j,k])}
 function nae(row,bit){let x=bit(row[0][0])^row[0][1];return row.some(([v,s])=>(bit(v)^s)!==x)}
 function signed(a,s=0){return a.map(v=>[v,s])}
 function canon(row){let a=row.slice().sort((x,y)=>x[0]-y[0]||x[1]-y[1]);let flip=a[0][1];return a.map(([v,s])=>[v,s^flip])}
 function krow(row){return JSON.stringify(canon(row))}
 function dedup(rows){let d=new Map();rows.forEach((row,i)=>{let k=krow(row);if(!d.has(k))d.set(k,{row:canon(row),ids:[]});d.get(k).ids.push(i)});return [...d.values()]}
 function make(k){
  let rows=[];for(let p of [0,1,2,3,0,1])for(let j=0;j<3;j++)rows.push({row:signed(ag[p*3+j],rows.length>=9?1:0),p,j});
  // Signs: first 3 partitions positive, final 3 negative.
  let next=9,regions=[];
  for(let t=0;t<k;t++){
   let p=Math.floor(t/3),j=t%3,b=ag[3*p+j];let matches=rows.filter(x=>x.p===p&&x.j===j);check(matches.length===2,"pair");
   rows=rows.filter(x=>!(x.p===p&&x.j===j));let I=rng(6).map(i=>next+i);next+=6;
   let port=0, rr=fano.map(row=>row.map(v=>v===1?b[port++]:I[v-2]));check(port===3,"fano split");
   for(let row of rr){rows.push({row:signed(row),p:-1,j:-1});rows.push({row:signed(row,1),p:-1,j:-1})}
   regions.push({I,b,rr});
  }
  const logical=rows.map(x=>x.row);
  for(let v=0;v<next;v++)for(let s of [0,1])check(logical.flat().filter(x=>x[0]===v&&x[1]===s).length===3,"balanced ports");
  let native=[],part=[],used=Array.from({length:next},()=>[0,0]);
  for(let v=0;v<next;v++)for(let j=2;j<12;j++){native.push(ag[j].map(w=>9*v+w));part.push(Math.floor(j/3))}
  for(let row of logical){native.push(row.map(([v,s])=>9*v+3*s+used[v][s]++));part.push(0)}
  let nn=9*next, seen=new Set();for(let row of native){check(new Set(row).size===3,"triple");for(let p of pairs(row)){let k=key(p);check(!seen.has(k),"linearity");seen.add(k)}}
  for(let p=0;p<4;p++){let z=native.flatMap((r,i)=>part[i]===p?r:[]);check(z.length===nn&&new Set(z).size===nn,"partition")}
  return {native,part,logical,regions,next};
 }
 function recognize(native,nn){
   let adj=Array.from({length:nn},(_,v)=>new Set([v]));
   for(let row of native)for(let v of row)for(let w of row)adj[v].add(w);
   let caps=new Map();
   for(let a of adj){if(a.size!==9)continue;let ids=[...a].sort((a,b)=>a-b),rows=native.map((r,i)=>({r,i})).filter(x=>x.r.every(v=>a.has(v)));if(rows.length!==10)continue;
    let K=key(ids);if(caps.has(K))continue;
    let covered=new Set(rows.flatMap(x=>pairs(x.r).map(key))),missing=pairs(ids).filter(p=>!covered.has(key(p)));let d=ids.filter(v=>missing.some(p=>p.includes(v)));check(d.length===6&&missing.length===6,"missing triangles");
    let r0=d.filter(v=>v===d[0]||missing.some(p=>p.includes(v)&&p.includes(d[0]))),r1=d.filter(v=>!r0.includes(v)),priv=ids.filter(v=>!d.includes(v));check(r0.length===3&&r1.length===3,"triangles");
    let count=0;for(let w=0;w<512;w++){tick("wordTrials");let bit=v=>(w>>ids.indexOf(v))&1;let ok=rows.every(x=>nae(signed(x.r),bit));let expected=r0.every(v=>bit(v)===bit(r0[0]))&&r1.every(v=>bit(v)!==bit(r0[0]))&&nae(signed(priv),bit);check(ok===expected,"exact cap table");if(ok)count++}
    check(count===12,"cap words");caps.set(K,{ids,r0,r1,priv,owners:rows.map(x=>x.i)});
   }
   let cs=[...caps.values()].sort((a,b)=>a.ids[0]-b.ids[0]),map=new Map(),inOwners=new Set();
   cs.forEach((c,v)=>{for(let id of c.ids){check(!map.has(id),"disjoint caps");map.set(id,[v,c.r0.includes(id)?0:c.r1.includes(id)?1:-1])}for(let i of c.owners)inOwners.add(i)});
   check(map.size===nn,"all covered");let rows=[],source=[];
   native.forEach((r,i)=>{if(!inOwners.has(i)){let z=r.map(v=>map.get(v));check(z.every(x=>x[1]>=0)&&new Set(z.map(x=>x[0])).size===3,"external");rows.push(z);source.push(i)}});
   let ds=dedup(rows);for(let d of ds)d.ids=d.ids.map(i=>source[i]);
   return {cs,ds};
 }
 function matching(rows,vs){
   const owner=new Map();
   function augment(i,seen){for(let v of new Set(rows[i].map(x=>x[0]))){if(seen.has(v))continue;seen.add(v);if(!owner.has(v)||augment(owner.get(v),seen)){owner.set(v,i);return true}}return false}
   for(let i=0;i<rows.length;i++)if(!augment(i,new Set()))return null;
   return owner;
 }
 function regionTable(rows,I,b){
   let ok=[];for(let w=0;w<(1<<b.length);w++){let cnt=0;for(let z=0;z<(1<<I.length);z++){tick("wordTrials");const bit=v=>b.includes(v)?(w>>b.indexOf(v))&1:(z>>I.indexOf(v))&1;if(rows.every(r=>nae(r,bit)))cnt++}ok.push(cnt)}return ok
 }
 // Track B: enumerate determinant matching terms on tiny square anchored geometry, NOT the general RST algorithm.
 function matrixTest(rows,I,b){
   let vs=[...I,-1],outcomes=[];
   const collapsed=rows.map(r=>r.map(([v,s])=>[b.includes(v)?-1:v,s,b.indexOf(v)]));
   let M=matching(collapsed,vs);check(M&&M.size===rows.length&&rows.length===vs.length,"square Hall");
   let reach=new Map(vs.map(v=>[v,new Set([v])]));for(let [v,i] of M)for(let [w] of collapsed[i])reach.get(v).add(w);
   for(let k of vs)for(let v of vs)if(reach.get(v).has(k))for(let w of reach.get(k))reach.get(v).add(w);
   check(vs.every(v=>reach.get(v).size===vs.length),"strict sink");
   let internalEdges=collapsed.map(r=>r.filter(x=>x[0]!==-1)), seenR=new Set([0]), seenV=new Set();
   for(let t=0;t<vs.length;t++){for(let i of seenR)for(let [v] of internalEdges[i])seenV.add(v);internalEdges.forEach((r,i)=>{if(r.some(([v])=>seenV.has(v)))seenR.add(i)})}
   check(seenR.size===rows.length&&seenV.size===I.length,"delete anchor connected");
   let terms=[];function rec(i,used,cols,occ){if(i===rows.length){tick("matchingTerms");let parity=0;for(let a=0;a<cols.length;a++)for(let d=a+1;d<cols.length;d++)parity^=Number(cols[a]>cols[d]);terms.push({parity,occ:occ.slice()});return}for(let x of collapsed[i]){let v=vs.indexOf(x[0]);if(!used.has(v)){used.add(v);rec(i+1,used,[...cols,v],[...occ,x]);used.delete(v)}}}rec(0,new Set(),[],[]);
   for(let w=0;w<(1<<b.length);w++){
    const signs=new Set(terms.map(t=>t.occ.reduce((s,x)=>s^x[1]^(x[2]<0?0:(w>>x[2])&1),t.parity)));
    outcomes.push(signs.size>1);
   }
   return {outcomes,matchingTerms:terms.length}
 }
 function discover(rows,n){
   let all=[];const graph=Array.from({length:n},()=>new Set());for(let r of rows)for(let [v] of r)for(let [w] of r)if(w!==v)graph[v].add(w);
   for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)for(let c=b+1;c<n;c++){
    tick("separatorTrials");let B=[a,b,c],seen=new Set(B);
    for(let v=0;v<n;v++){if(seen.has(v))continue;let I=[v];seen.add(v);for(let i=0;i<I.length;i++)for(let w of graph[I[i]])if(!seen.has(w)){seen.add(w);I.push(w)}if(I.length!==6)continue;
     let R=rows.map((r,i)=>({r,i})).filter(x=>x.r.some(([v])=>I.includes(v)));
     let actualB=[...new Set(R.flatMap(x=>x.r.map(y=>y[0]).filter(v=>!I.includes(v))))].sort((a,b)=>a-b);
     if(key(actualB)!==key(B)||R.length!==I.length+1)continue;
     let cr=R.map(x=>x.r.map(([v,s])=>[B.includes(v)?-1:v,s]));if(!matching(cr,[...I,-1]))continue;
     all.push({I:I.sort((a,b)=>a-b),b:B,indices:R.map(x=>x.i)});
    }
   }
   return all
 }
 function direct(rows,n){let count=0;for(let w=0;w<(1<<n);w++){tick("wordTrials");if(rows.every(r=>nae(r,v=>(w>>v)&1)))count++}return count}
 for(let k of [1,2,3]){
   let a=make(k),r=recognize(a.native,a.next*9);let rows=r.ds.map(x=>x.row);
   check(rows.length===12+6*k,"quotient count");check(!matching(rows,rng(a.next)),"whole Hall fails");
   check(new Set(rows.map(krow)).size===dedup(a.logical).length&&dedup(a.logical).every(x=>rows.some(y=>krow(y)===krow(x.row))),"exact source projection");
   let candidates=discover(rows,a.next),certs=[],removed=new Set(),replacement=[];
   for(let reg of a.regions){
    let cand=candidates.find(c=>key(c.I)===key(reg.I)&&key(c.b)===key(reg.b));check(cand,"separator acquisition");
    let R=cand.indices.map(i=>rows[i]),table=regionTable(R,cand.I,cand.b),mat=matrixTest(R,cand.I,cand.b);
    check(table.every((x,w)=>(x>0)===mat.outcomes[w]),"matching vs exact support");
    check(table.every((x,w)=>(x>0)===(w!==0&&w!==7)),"NAE boundary");
    for(let i of cand.indices){check(!removed.has(i),"disjoint owner regions");removed.add(i)}replacement.push(signed(cand.b));
    certs.push({...cand,ownerIDs:cand.indices.map(i=>r.ds[i].ids),table,matchingTerms:mat.matchingTerms})
   }
   let core=[...rows.filter((_,i)=>!removed.has(i)),...replacement];
   check(core.length===12&&ag.every(x=>core.some(y=>krow(y)===krow(signed(x)))),"AG9 exactly restored");
   let directCount=k===1?direct(rows,a.next):null;if(k===1)check(directCount===0,"whole direct");
   let coreCount=direct(core,9);check(coreCount===0,"core direct");
   out.cases.push({splices:k,nativeVariables:a.next*9,nativeOwners:a.native.length,native:a.native,partitions:a.part,encodedJSONBytes:JSON.stringify({clauses:a.native,partitions:a.part}).length,quotientVariables:a.next,quotientOwners:rows.length,quotient:rows,quotientOwnerIDs:r.ds.map(x=>x.ids),candidates:candidates.length,certs,core,coreCount,directCount})
 }
 // hostile controls: one-anchor Hall fails but nontrivial relation; K5 triple hypergraph all pairs? exact all 10 triples.
 let two=[signed([0,1,2]),signed([3,4,5])];let table=regionTable(two,[],rng(6));check(!matching(two.map(r=>r.map(([v,s])=>[-1,s])),[-1]),"two clauses Hall fails");
 check(table.filter(x=>x).length===36,"two NAE support");
 let k5=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)for(let k=j+1;k<5;k++)k5.push(signed([i,j,k]));
 check(direct(k5,5)===0,"K5 NO");check(!matching(k5,rng(5)),"K5 Hall fails");
 let raw=ag.map(r=>signed(r));check(direct(raw,9)===0,"AG9 NO");check(!matching(raw,rng(9)),"AG9 Hall fails");
 // Minimal signed, duplicate-port controls: 1 owner on anchor with different occurrence signs.
 let tests=[{r:[[[0,0],[1,1],[2,0]]],b:[0,1,2],forbid:[2,5]},{r:[[[0,0],[0,1],[1,0]]],b:[0,1],forbid:[]}];
 for(let t of tests){let z=regionTable(t.r,[],t.b),mat=matrixTest(t.r,[],t.b);check(z.every((x,i)=>(x>0)===mat.outcomes[i]),"parallel arc control");check(JSON.stringify(z.flatMap((x,i)=>x?[]:[i]))===JSON.stringify(t.forbid),"signed control")}
 out.controls={twoClauseBoundarySupport:36,twoClauseBoundaryWords:64,K5clauses:10,K5SAT:0,rawAG9SAT:0,signedParallelControls:2};
 return out;
}
console.log(JSON.stringify(audit(),null,2));
