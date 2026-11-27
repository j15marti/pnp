function sha(s){
 const K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
 let H=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19],n=s.length,p=new Uint8Array(Math.ceil((n+9)/64)*64);
 for(let i=0;i<n;i++){if(s.charCodeAt(i)>127)throw Error("ASCII only");p[i]=s.charCodeAt(i)}p[n]=128;let v=new DataView(p.buffer);v.setUint32(p.length-8,Math.floor(n*8/2**32));v.setUint32(p.length-4,n*8>>>0);
 let W=new Uint32Array(64),R=(x,k)=>(x>>>k)|(x<<(32-k));
 for(let t=0;t<p.length;t+=64){for(let i=0;i<16;i++)W[i]=v.getUint32(t+4*i);for(let i=16;i<64;i++){let x=W[i-15],y=W[i-2];W[i]=W[i-16]+(R(x,7)^R(x,18)^(x>>>3))+W[i-7]+(R(y,17)^R(y,19)^(y>>>10))}
 let [a,b,c,d,e,f,g,h]=H;for(let i=0;i<64;i++){let T=(h+(R(e,6)^R(e,11)^R(e,25))+((e&f)^(~e&g))+K[i]+W[i])|0,U=((R(a,2)^R(a,13)^R(a,22))+((a&b)^(a&c)^(b&c)))|0;[a,b,c,d,e,f,g,h]=[(T+U)|0,a,b,c,(d+T)|0,e,f,g]}H=H.map((x,i)=>(x+[a,b,c,d,e,f,g,h][i])>>>0)}
 return H.map(x=>x.toString(16).padStart(8,"0")).join("");
}
function lab(net,cnf,registry,peer){
 const assert=(x,m)=>{if(!x)throw Error(m)},uniq=a=>[...new Set(a)].sort((a,b)=>a-b),mask=(r,s)=>s.reduce((w,j,i)=>w|(((r>>j)&1)<<i),0),jbytes=x=>JSON.stringify(x)+"\n",hash=x=>sha(jbytes(x));
 const cap=1000000; let prep={arcs:0,rows:0,join:0,selection:0,independentJoin:0};
 function source(net){
  let n=4*net.types.length,adj=Array.from({length:n},()=>[]),link=(a,b,s)=>{adj[a].push([b,s]);adj[b].push([a,s])};
  for(const [a,b,s] of net.edges)link(a,b,s);for(let i=0;i<net.types.length;i++)if(net.types[i]==="E")for(let j=1;j<4;j++)link(4*i,4*i+j,0);
  let root=new Int32Array(n).fill(-1),sign=new Uint8Array(n);
  for(let i=0;i<n;i++)if(root[i]<0){root[i]=i;let q=[i];while(q.length){let u=q.pop();for(let [v,s] of adj[u]){prep.arcs++;if(root[v]<0){root[v]=i;sign[v]=sign[u]^s;q.push(v)}else assert(root[v]===i&&sign[v]===(sign[u]^s),"parity")}}}
  let fs=[];for(let i=0;i<net.types.length;i++)if(net.types[i]==="B"){let vs=uniq(Array.from({length:4},(_,j)=>root[4*i+j])),rows=[];for(let w=0;w<2**vs.length;w++){prep.rows++;let sum=0;for(let j=0;j<4;j++)sum+=((w>>vs.indexOf(root[4*i+j]))&1)^sign[4*i+j];if(sum===2)rows.push(w)}fs.push({v:vs,r:rows,s:[i]})}
  return {fs,root,sign};
 }
 function dedup(F){let M=new Map();for(let f of F){let k=JSON.stringify([f.v,f.r]);if(!M.has(k))M.set(k,f); }return [...M.values()]}
 function compact(F,limit=5){
  F=dedup(F);let trace=[],initial=F.length,initialVars=uniq(F.flatMap(f=>f.v)).length;
  while(true){let occ=new Map();for(let f of F)for(let v of f.v){if(!occ.has(v))occ.set(v,[]);occ.get(v).push(f)}
   let best=null;for(let [v,fs] of occ){prep.selection++;if(fs.length>2)continue;let scope=uniq(fs.flatMap(f=>f.v));if(scope.length>limit)continue;if(!best||scope.length<best.scope.length||(scope.length===best.scope.length&&v<best.v))best={v,fs,scope}}
   if(!best)break;let {v,fs,scope}=best,out=scope.filter(x=>x!==v),rows=new Set(),idx=fs.map(f=>f.v.map(x=>scope.indexOf(x)));
   for(let w=0;w<2**scope.length;w++){prep.join++;if(fs.every((f,i)=>f.r.includes(mask(w,idx[i]))))rows.add(mask(w,out.map(x=>scope.indexOf(x))))}
   // independent projection: for each exterior word separately test both extensions, with explicit variable dictionary
   let check=[];for(let w=0;w<2**out.length;w++){let valid=false;for(let b=0;b<2;b++){prep.independentJoin++;let a=new Map(out.map((x,i)=>[x,(w>>i)&1]));a.set(v,b);if(fs.every(f=>f.r.some(r=>f.v.every((x,i)=>a.get(x)===((r>>i)&1)))))valid=true}if(valid)check.push(w)}
   let rr=[...rows].sort((a,b)=>a-b);assert(JSON.stringify(rr)===JSON.stringify(check),"join replay");
   let f={v:out,r:rr,s:uniq(fs.flatMap(f=>f.s))};trace.push({pivot:v,parents:fs,out:f});F=dedup(F.filter(f=>!fs.includes(f)).concat(f));
  }return {F,trace,initial,initialVars};
 }
 function fromCnf(cs){return cs.map((c,i)=>{let v=uniq(c.map(Math.abs)),r=[];for(let w=0;w<2**v.length;w++)if(c.some(l=>((w>>v.indexOf(Math.abs(l)))&1)===(l>0?1:0)))r.push(w);return {v,r,s:[i+1]}})}
 function choose(F){let counts=new Map();for(let f of F)for(let v of f.v)counts.set(v,(counts.get(v)||0)+1);return [...counts].sort((a,b)=>b[1]-a[1]||a[0]-b[0]).map(x=>x[0])}
 function clauses(F){let C=[];for(let f of F){let k=f.v.length;for(let t=0;t<3**k;t++){let z=t,p=[];for(let j=0;j<k;j++){let d=z%3;z=Math.floor(z/3);if(d)p.push([f.v[j],d-1,j])}if(!f.r.some(r=>p.every(([v,b,j])=>((r>>j)&1)===b)))C.push({p:p.map(([v,b])=>[v,1-b]),s:f.s})}}return C}
 function solve(F,model,guards,extra=[]){
  const V=choose(F),C=clauses(F).concat(extra),stats={events:0,nodes:0,peak:0},inc=()=>{if(++stats.events>cap)throw Error("CAP")};
  function gac(g){let a=new Map(g),used=new Set();while(true){let ch=false;for(let f of F){let r=f.r.filter(w=>{inc();return f.v.every((v,i)=>!a.has(v)||a.get(v)===((w>>i)&1))});if(!r.length){f.s.forEach(x=>used.add(x));return {bad:true,a,used}}for(let j=0;j<f.v.length;j++){let v=f.v[j];if(a.has(v))continue;let b=(r[0]>>j)&1;if(r.every(w=>((w>>j)&1)===b)){a.set(v,b);f.s.forEach(x=>used.add(x));ch=true}}}for(let c of extra){inc();if(c.p.some(([v,b])=>a.get(v)===b))continue;let un=c.p.filter(([v])=>!a.has(v));if(!un.length){c.s.forEach(x=>used.add(x));return {bad:true,a,used}}if(un.length===1){a.set(...un[0]);c.s.forEach(x=>used.add(x));ch=true}}if(!ch)return {bad:false,a,used}}}
  function affine(a){let E=new Map(),index=new Map(V.map((v,i)=>[v,i]));function add(m,b){while(m){inc();let i=m.toString(2).length-1;if(!E.has(i)){E.set(i,[m,b]);return false}let [x,y]=E.get(i);m^=x;b^=y}return !!b}
   for(let [v,b] of a)if(add(1n<<BigInt(index.get(v)),b))return true;
   for(let f of F){let R=f.r.filter(w=>f.v.every((v,i)=>!a.has(v)||a.get(v)===((w>>i)&1)));if(!R.length)return true;for(let l=1;l<2**f.v.length;l++){inc();let parity=w=>{let x=w&l,b=0;while(x){b^=1;x&=x-1}return b};let b=parity(R[0]);if(R.every(w=>parity(w)===b)){let m=0n;for(let i=0;i<f.v.length;i++)if((l>>i)&1)m|=1n<<BigInt(index.get(f.v[i]));if(add(m,b))return true}}}return false}
  function two(a){let idx=new Map(V.map((v,i)=>[v,i])),n=2*V.length,G=Array.from({length:n},()=>[]),l=([v,b])=>2*idx.get(v)+b;for(let c of C){inc();if(c.p.some(([v,b])=>a.get(v)===b))continue;let p=c.p.filter(([v])=>!a.has(v));if(!p.length)return true;if(p.length<=2){let x=l(p[0]),y=l(p[p.length-1]);G[x^1].push(y);G[y^1].push(x)}}function reach(x,y){let q=[x],seen=new Set(q);while(q.length){let u=q.pop();inc();if(u===y)return true;for(let v of G[u])if(!seen.has(v)){seen.add(v);q.push(v)}}return false}return V.some((v,i)=>reach(2*i,2*i+1)&&reach(2*i+1,2*i))}
  function bucket(a){let L=F.map(f=>{let v=f.v.filter(x=>!a.has(x)),r=uniq(f.r.filter(w=>f.v.every((x,i)=>!a.has(x)||a.get(x)===((w>>i)&1))).map(w=>mask(w,v.map(x=>f.v.indexOf(x)))));return {v,r}});for(let c of extra){let v=uniq(c.p.map(x=>x[0])).filter(x=>!a.has(x)),r=[];for(let w=0;w<2**v.length;w++)if(c.p.some(([x,b])=>(a.has(x)?a.get(x):((w>>v.indexOf(x))&1))===b))r.push(w);L.push({v,r})}while(true){if(L.some(f=>!f.r.length))return "NO";let vs=uniq(L.flatMap(f=>f.v));if(!vs.length)return "YES";let best=null;for(let x of vs){inc();let fs=L.filter(f=>f.v.includes(x)),u=uniq(fs.flatMap(f=>f.v));if(!best||u.length<best.u.length)best={x,fs,u}}if(best.u.length>7)return "UNKNOWN";let {x,fs,u}=best,v=u.filter(y=>y!==x),r=[];for(let w=0;w<2**u.length;w++){inc();if(fs.every(f=>f.r.includes(mask(w,f.v.map(y=>u.indexOf(y))))))r.push(mask(w,v.map(y=>u.indexOf(y))))}L=L.filter(f=>!fs.includes(f)).concat({v,r:uniq(r)})}}
  function dfs(g){stats.nodes++;let c=gac(g);stats.peak=Math.max(stats.peak,c.a.size);if(c.bad)return {leaf:true};let x=V.find(v=>!c.a.has(v));if(x===undefined)return null;let lo=dfs([...g,[x,0]]);if(!lo)return null;let hi=dfs([...g,[x,1]]);if(!hi)return null;return {x,lo,hi}}
  try{let c=gac(guards);if(c.bad)return {label:"NO",tree:{leaf:true},stats};if(model==="occupancy")return {label:"UNKNOWN",stats};if(model==="affine")return {label:affine(c.a)?"NO":"UNKNOWN",stats};if(model==="bijunctive")return {label:two(c.a)?"NO":"UNKNOWN",stats};if(model==="separator")return {label:bucket(c.a),stats};let t=dfs(guards);return {label:t?"NO":"YES",tree:t,stats}}catch(e){if(String(e).includes("CAP"))return {label:"UNKNOWN",stats};throw e}
 }
 // independent checker uses forbidden partial assignment clauses, not accepted-row filtering
 function replay(F,g,t,extra=[]){let C=clauses(F).concat(extra),scans=0,used=new Set(),nodes=0;function check(g,t){nodes++;if(!t)return false;if(t.leaf){let a=new Map(g);for(;;){let ch=false;for(let c of C){scans++;if(c.p.some(([x,b])=>a.get(x)===b))continue;let p=c.p.filter(([x])=>!a.has(x));if(!p.length){c.s.forEach(x=>used.add(x));return true}if(p.length===1){a.set(...p[0]);c.s.forEach(x=>used.add(x));ch=true}}if(!ch)return false}}if(g.some(([x])=>x===t.x))return false;return check([...g,[t.x,0]],t.lo)&&check([...g,[t.x,1]],t.hi)}return {ok:check(g,t),scans,nodes,support:uniq([...used])}}
 function lanes(F,kind,anchor=null,peerGuards=[]){
  let V=choose(F),g0=anchor===null?[]:[[anchor,0]],xs=V.filter(v=>v!==anchor).slice(0,4);assert(xs.length===4,"guard coordinates");let guards=xs.map((x,i)=>xs.slice(0,i).map(v=>[v,1]).concat([[x,0]])).concat([xs.map(v=>[v,1])]);
  let names=["occupancy","affine","bijunctive","separator","dag"],results=[],checks=[],extras=[];
  for(let g of guards){let gg=g0.concat(g),a=names.map(m=>solve(F,m,gg));let d=a[4];if(d.label==="NO"){let p=replay(F,gg,d.tree);assert(p.ok,"DAG replay");checks.push(p)}else checks.push(null);results.push(a)}
  // Cross-lane export before complete core: import only independently checked immediate occupancy exclusions.
  for(let i=0;i<guards.length;i++)if(results[i][0].label==="NO"){let p=replay(F,g0.concat(guards[i]),{leaf:true});assert(p.ok,"occupancy replay");extras.push({p:guards[i].map(([x,b])=>[x,1-b]),s:p.support})}
  let localImports=extras.length;for(let p of peerGuards)if(p.p.every(([x])=>V.includes(x)))extras.push(p);
  let hybrid=guards.map(g=>solve(F,"dag",g0.concat(g),extras));
  for(let i=0;i<hybrid.length;i++)if(hybrid[i].label==="NO")assert(replay(F,g0.concat(guards[i]),hybrid[i].tree,extras).ok,"hybrid replay");
  let k=V.length-(anchor===null?0:1),counts=[];for(let b=1;b<32;b++){let a=new Map(),ok=true,bits=0;for(let i=0;i<5;i++)if(b>>i&1){bits++;for(let [v,x]of guards[i]){if(a.has(v)&&a.get(v)!==x)ok=false;a.set(v,x)}}counts.push({subset:b,sign:bits%2?1:-1,count:(ok?1n<<BigInt(k-a.size):0n).toString()})}let covered=counts.reduce((s,x)=>s+BigInt(x.sign)*BigInt(x.count),0n);assert(covered===(1n<<BigInt(k)),"coverage");
  let supports=checks.map(x=>x?.support||[]),overlap=supports.map(a=>supports.map(b=>a.filter(x=>b.includes(x)).length));
  let stat=names.map((m,i)=>({method:m,labels:results.map(a=>a[i].label),events:results.reduce((s,a)=>s+a[i].stats.events,0),nodes:results.reduce((s,a)=>s+a[i].stats.nodes,0)}));
  // bounded reproducible randomized guard probe; exact recheck each found conflict
  let seed=271127,random={seed,probes:16,conflicts:0,events:0,replay:0};for(let i=0;i<16;i++){let pool=V.filter(v=>v!==anchor),p=[];for(let j=0;j<3;j++){seed=(Math.imul(seed,1664525)+1013904223)>>>0;let v=pool.splice(seed%pool.length,1)[0];seed=(Math.imul(seed,1664525)+1013904223)>>>0;p.push([v,(seed>>>16)&1])}let z=solve(F,"occupancy",g0.concat(p));random.events+=z.stats.events;if(z.label==="NO"){let r=replay(F,g0.concat(p),{leaf:true});assert(r.ok,"random replay");random.conflicts++;random.replay+=r.scans}}
  return {kind,V,anchor,guards,counts,covered:covered.toString(),results,checks,overlap,stat,localImports,peerImports:extras.length-localImports,hybrid:hybrid.map(x=>({label:x.label,stats:x.stats})),random}
 }
 let src=source(net),P=compact(src.fs),V=choose(P.F),anchor=V[0];
 // all native constraints complement symmetric; projection preserves symmetry. Verify every retained relation.
 assert(P.F.every(f=>f.r.every(w=>f.r.includes((2**f.v.length-1)^w))),"complement");
 let native=lanes(P.F,"native",anchor);
 let Fcnf=fromCnf(cnf),cn=lanes(Fcnf,"cnf");
 // Replay peer conditional supports from original native constraints, not from its chart or reference labels.
 let peerAudit=[],peerExtras=[];
 if(peer){for(let g of peer.guards){let {anchor:a,pins}=g.guard_artifact,orig=g.original_B_ids,raw=src.fs.filter(f=>orig.includes(f.s[0])),pg=new Map([[src.root[a],src.sign[a]]]),ok=true;for(let [p,b]of pins){let x=src.root[p],y=b^src.sign[p];if(pg.has(x)&&pg.get(x)!==y)ok=false;pg.set(x,y)}
  // If own gauge differs, relative relation transformation needs all involved roots and peer anchor.
  // use raw native supports with peer anchor pinned; projection independently recomputed
  let Q=compact(raw); // don't import if guard coordinates retired
  // guard-specific pins must be protected before projection, so put explicit singleton relations into raw, then compact.
  let R=compact(raw.concat([...pg].map(([x,b])=>({v:[x],r:[b],s:[]}))));
  let z=solve(R.F,"dag",[]),p=z.label==="NO"?replay(R.F,[],z.tree):null;
  peerAudit.push({guard:g.guard_id,orig:orig.length,ok:ok&&!!p?.ok,events:z.stats.events,replay:p?.scans||0,projected:R.F.length});
  if(ok&&p?.ok&&src.root[a]===anchor){let q=pins.map(([p,b])=>[src.root[p],1^(b^src.sign[p]^src.sign[a])]);if(q.every(([v])=>V.includes(v)))peerExtras.push({p:q,s:orig})}
 }}
 let peerHybrid=peerExtras.length?native.guards.map(g=>{let z=solve(P.F,"dag",[[anchor,0],...g],peerExtras);if(z.label==="NO")assert(replay(P.F,[[anchor,0],...g],z.tree,peerExtras).ok,"peer hybrid");return {label:z.label,stats:z.stats}}):[];
 return {prep,native,cn,peerAudit,peerExtras,peerHybrid,projection:{initial:P.initial,initialVars:P.initialVars,final:P.F.length,finalVars:V.length,trace:P.trace,F:P.F,rootMapHash:hash([Array.from(src.root),Array.from(src.sign)])}};
}
module.exports={sha,lab};
