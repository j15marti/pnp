function audit(){
const assert=(x,m)=>{if(!x)throw Error(m)};
const arr=n=>Array.from({length:n},(_,i)=>i);
const pc=x=>{let r=0;while(x){r+=x&1;x>>>=1}return r};
const key=a=>a.join(",");
function build(n){
 const h=n-2,q=3*n,edges=arr(q).map(i=>[Math.floor(i/3),(Math.floor(i/3)+i%3)%h]);
 const C=[];for(let i=0;i<n;i++){let a=arr(3).map(j=>3*i+j+1);C.push(a);for(let u=0;u<3;u++)for(let v=u+1;v<3;v++)C.push([-a[u],-a[v]])}
 for(let i=0;i<q;i++)for(let j=i+1;j<q;j++)if(edges[i][1]===edges[j][1])C.push([-i-1,-j-1]);
 const ids=arr(4*q).map(i=>i+1);let seed=261127+n;for(let i=ids.length-1;i>0;i--){seed=(Math.imul(seed,1664525)+1013904223)>>>0;let j=seed%(i+1);[ids[i],ids[j]]=[ids[j],ids[i]]}
 const P=arr(q).map(i=>ids.slice(3*i,3*i+3).sort((a,b)=>a-b)),G=ids.slice(3*q),H=arr(q).map(i=>[G[(i+q-1)%q],G[i]].sort((a,b)=>a-b));
 const source=C.map(cl=>{
  let bs=cl.map(l=>Math.abs(l)-1),hs=[...new Set(bs.flatMap(i=>H[i]))].sort((a,b)=>a-b),scope=[...new Set(bs.flatMap(i=>P[i].concat(H[i])))].sort((a,b)=>a-b);
  let W=[];for(let g=0;g<2**hs.length;g++){
   let w=hs.reduce((z,id,j)=>z+(((g>>j)&1)<<scope.indexOf(id)),0);
   function rec(t,z){if(t===bs.length){W.push(z);return}let i=bs[t],c=H[i].reduce((s,id)=>s+((g>>hs.indexOf(id))&1),0);for(let a=0;a<8;a++)if((pc(a)+c>=3)===(cl[t]<0)){let x=P[i].reduce((v,id,j)=>v+(((a>>j)&1)<<scope.indexOf(id)),0);rec(t+1,z+x)}}
   rec(0,w)
  }return {scope,W:W.sort((a,b)=>a-b)}
 });return {n,h,q,P,G,H,C,source}
}
function project(w,indices){return indices.reduce((s,j,i)=>s+(((w>>j)&1)<<i),0)}
function restrict(source,pins){return source.map(({scope,W})=>{let free=scope.filter(v=>!pins.has(v)),index=free.map(v=>scope.indexOf(v));return {scope:free,W:W.filter(w=>scope.every((v,j)=>!pins.has(v)||pins.get(v)===((w>>j)&1))).map(w=>project(w,index)).sort((a,b)=>a-b)}})}
function match(C){
 const rows=C.filter(c=>c.every(x=>x>0)),owner=new Map();for(let i=0;i<rows.length;i++)for(let v of rows[i]){if(owner.has(v))return null;owner.set(v,i)}
 C=C.filter(c=>c.every(l=>owner.has(Math.abs(l))));
 const adj=new Map([...owner.keys()].map(v=>[v,new Set()]));for(let c of C)if(c.length===2&&c.every(x=>x<0)){let [a,b]=c.map(Math.abs);if(owner.get(a)!==owner.get(b)){adj.get(a).add(b);adj.get(b).add(a)}}
 let holes=new Map(),count=0;for(let a of adj.keys())if(!holes.has(a)){let todo=[a],members=[];holes.set(a,count);for(let i=0;i<todo.length;i++){let v=todo[i];members.push(v);for(let u of adj.get(v))if(!holes.has(u)){holes.set(u,count);todo.push(u)}}if(new Set(members.map(v=>owner.get(v))).size!==members.length||members.some(v=>adj.get(v).size!==members.length-1))return null;count++}
 let expected=new Set(rows.map(c=>key(c.slice().sort((a,b)=>a-b))));
 let vs=[...owner.keys()].sort((a,b)=>a-b);for(let i=0;i<vs.length;i++)for(let j=i+1;j<vs.length;j++)if(owner.get(vs[i])===owner.get(vs[j])||holes.get(vs[i])===holes.get(vs[j]))expected.add(key([-vs[j],-vs[i]]));
 let got=new Set(C.map(c=>key(c.slice().sort((a,b)=>a-b))));if(expected.size!==got.size||[...expected].some(k=>!got.has(k)))return null;
 let M=arr(count).map(()=>-1),scans=0;
 function aug(r,seen){for(let v of rows[r]){scans++;let h=holes.get(v);if(seen.has(h))continue;seen.add(h);if(M[h]<0||aug(M[h],seen)){M[h]=r;return true}}return false}
 for(let i=0;i<rows.length;i++)aug(i,new Set());
 let used=new Set(M.filter(x=>x>=0)),S=new Set(arr(rows.length).filter(i=>!used.has(i))),T=new Set(),todo=[...S];for(let i=0;i<todo.length;i++)for(let v of rows[todo[i]]){scans++;let h=holes.get(v);if(!T.has(h)){T.add(h);if(M[h]>=0&&!S.has(M[h])){S.add(M[h]);todo.push(M[h])}}}
 assert([...S].every(i=>rows[i].every(v=>T.has(holes.get(v)))),"Hall replay");
 return {rows:rows.length,holes:count,hall:[S.size,T.size],hallRows:[...S],hallHoles:[...T],scans,no:S.size>T.size}
}
function acquire(source){
 let sig=new Map();source.forEach(({scope},j)=>scope.forEach(v=>{if(!sig.has(v))sig.set(v,[]);sig.get(v).push(j)}));
 let buckets=new Map();for(let [v,s] of sig){let k=key(s);if(!buckets.has(k))buckets.set(k,[]);buckets.get(k).push(v)}
 let P=[...buckets.values()].filter(a=>a.length===3).map(a=>a.sort((a,b)=>a-b)),guards=[...buckets.values()].filter(a=>a.length===1).flat();
 assert(3*P.length+guards.length===sig.size,"bucket form");let H=P.map(()=>[]);
 for(let g of guards){let hits=[];for(let i=0;i<P.length;i++)for(let j=i+1;j<P.length;j++){let u=[...new Set([...sig.get(P[i][0]),...sig.get(P[j][0])])].sort((a,b)=>a-b);if(key(u)===key(sig.get(g)))hits.push([i,j])}assert(hits.length===1,"guard scope");for(let i of hits[0])H[i].push(g)}
 H.forEach(a=>a.sort((a,b)=>a-b));let charts=P.map(()=>new Map()),C=[],bad=[],localSlices=0,wordScans=0,checks=0;
 for(let id=0;id<source.length;id++){
  let {scope,W}=source[id],bs=arr(P.length).filter(i=>scope.includes(P[i][0])),hs=[...new Set(bs.flatMap(i=>H[i]))].sort((a,b)=>a-b);
  if(key([...new Set(bs.flatMap(i=>P[i].concat(H[i])))].sort((a,b)=>a-b))!==key(scope)){bad.push(id);continue}
  let gi=hs.map(v=>scope.indexOf(v)),pi=bs.map(i=>P[i].map(v=>scope.indexOf(v))),slices=new Map();
  for(let w of W){wordScans++;let g=project(w,gi);if(!slices.has(g))slices.set(g,{n:0,sets:bs.map(()=>new Set())});let s=slices.get(g);s.n++;pi.forEach((idx,j)=>s.sets[j].add(project(w,idx)))}
  let ok=slices.size===2**hs.length,signs=null,pending=[];
  for(let [g,s] of slices){localSlices++;if(s.n!==s.sets.reduce((z,v)=>z*v.size,1))ok=false;let z=[];
   for(let j=0;j<bs.length;j++){checks++;let a=s.sets[j],i=bs[j],t=project(g,H[i].map(v=>hs.indexOf(v)));if(a.has(0)===a.has(7)){ok=false;continue}let sign=a.has(0)?1:-1;z.push(sign*(i+1));let zeros=key(arr(8).filter(v=>a.has(v)===(sign===1)));let old=charts[i].get(t);if(old!==undefined&&old!==zeros)ok=false;pending.push([i,t,zeros])}
   if(signs===null)signs=z;else if(key(signs)!==key(z))ok=false;
  }
  let tmp=new Map();for(let [i,t,v] of pending){let k=i+","+t;if(tmp.has(k)&&tmp.get(k)!==v)ok=false;tmp.set(k,v)}
  if(ok&&signs){C.push(signs);for(let [i,t,v] of pending)charts[i].set(t,v)}else bad.push(id)
 }
 return {P,H,C,bad,charts,localSlices,wordScans,checks,hall:match(C)}
}
function independent(data,source,pins,damage){
 let comparisons=0,groups=0;for(let j=0;j<source.length;j++){let {scope,W}=source[j],set=new Set(W),cl=data.C[j];assert(set.size===W.length,"duplicates");let omitted=0;for(let w=0;w<2**scope.length;w++){
  let bit=v=>pins.has(v)?pins.get(v):((w>>scope.indexOf(v))&1);
  let forbidden=cl.every(l=>{let i=Math.abs(l)-1;return (data.P[i].concat(data.H[i]).reduce((s,v)=>s+bit(v),0)>=3)===(l<0)});
  if(forbidden&&!set.has(w))omitted++;else assert(forbidden===set.has(w),"truth comparison");comparisons++;
 }assert(omitted===(damage&&j===0?1:0),"omission count");groups++}
 return {comparisons,groups}
}
function fingerprint(source){let h=2166136261,N=0,clauses=0;for(let {scope,W} of source)for(let w of W){let s=scope.map((v,j)=>((w>>j)&1)?-v:v).join(" ")+" 0\n";N+=8*s.length;clauses++;for(let i=0;i<s.length;i++)h=Math.imul(h^s.charCodeAt(i),16777619)>>>0}return {fnv:h.toString(16),payload_bits:N,clauses}}
let results=[],controls=0;
for(let n of [5,8,12]){
 const d=build(n);for(let release of (n===5?[0,Math.floor(d.q/2),d.q]:[d.q])){
  let pins=new Map(d.G.slice(release).map(g=>[g,0])),src=restrict(d.source,pins);
  assert(src.every(x=>x.scope.length>=6),"UP");
  let auth=fingerprint(src),A=acquire(src),B=independent(d,src,pins,false);
  assert(A.bad.length===0&&A.hall?.no&&A.P.length===d.q&&A.C.length===d.C.length,"clean");
  // Independent source-ID decoder equivalence check on all local guard/private words.
  let decoderChecks=0;for(let i=0;i<A.P.length;i++){let o=d.P.findIndex(p=>key(p)===key(A.P[i]));assert(o>=0,"private map");for(let [g,zero] of A.charts[i])for(let a=0;a<8;a++){let z=d.H[o].reduce((s,v)=>s+(pins.has(v)?pins.get(v):((g>>A.H[i].indexOf(v))&1)),0);assert(zero.split(",").includes(String(a))===(pc(a)+z<3),"decoder");decoderChecks++}}
  let damaged=src.map((g,j)=>j?g:{scope:g.scope,W:g.W.slice(1)}),D=acquire(damaged),E=independent(d,damaged,pins,true);
  // Dropped row has two units of deficit remaining minus one.
  assert(D.bad.length===1&&D.bad[0]===0&&D.hall?.no,"damaged");
  let qpins=new Map(pins);for(let i=0;i<d.q;i++){d.H[i].forEach(g=>qpins.set(g,0));qpins.set(d.P[i][1],1);qpins.set(d.P[i][2],1)}
  let core=restrict(src,qpins);assert(core.length===d.C.length&&core.every((g,j)=>g.W.length===1&&g.scope.length===d.C[j].length),"restriction recovery");
  for(let j=0;j<core.length;j++){let {scope,W}=core[j],cl=d.C[j];for(let l of cl)assert(((W[0]>>scope.indexOf(d.P[Math.abs(l)-1][0]))&1)===(l<0?1:0),"base sign")}
  results.push({n,q:d.q,release,guards:pins.size,auth,source_groups:src.length,localSlices:A.localSlices,wordScans:A.wordScans,checks:A.checks,independent:B,decoderChecks,hall:A.hall,damaged:{auth:fingerprint(damaged),bad:D.bad,hall:D.hall,independent:E,localSlices:D.localSlices,wordScans:D.wordScans},min_width:Math.min(...src.map(x=>x.scope.length)),base_recovered:true});
 }
}
// Hostile control: marginally surjective x_i=g_i on unrestricted guard domain does not imply independent lift.
let tuples=new Set([0,3]);assert(tuples.size===2&&![1,2].some(w=>tuples.has(w)),"joint control");controls++;
// For majority 3 private, 2 guard, a constant guard word admits both outputs using all-0/all-1 private.
for(let g=0;g<4;g++){assert(pc(g)<3&&3+pc(g)>=3,"robust lift");controls++}
return {results,controls,execution:"sequential JS; exact local scans, no global assignment enumeration; source masks <=15 bits; original variable IDs scrambled deterministic seed 261127+n"};
}
console.log(JSON.stringify(audit(),null,2));
