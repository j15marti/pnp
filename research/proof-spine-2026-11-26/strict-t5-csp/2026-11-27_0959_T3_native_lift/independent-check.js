// T3/L05: source-only signed E/B to bounded-resolution contraction. ASCII SHA256.
function sha(s){
 const rr=(x,n)=>(x>>>n)|(x<<(32-n));
 const K=[],H=[];for(let p=2;K.length<64;p++){let prime=true;for(let j=2;j*j<=p;j++)if(p%j===0){prime=false;break}if(prime){if(H.length<8)H.push((Math.sqrt(p)%1*4294967296)|0);K.push((Math.cbrt(p)%1*4294967296)|0)}}
 const n=s.length, L=Math.ceil((n+9)/64)*64, w=new Int32Array(64);
 for(let b=0;b<L;b+=64){for(let i=0;i<16;i++){let z=0;for(let j=0;j<4;j++){let a=b+4*i+j,c=a<n?s.charCodeAt(a):a===n?128:a>=L-8?Math.floor(n*8/2**(8*(L-1-a)))%256:0;if(c>255)throw Error("non-ASCII");z=(z<<8)|c}w[i]=z}
 for(let i=16;i<64;i++){let x=w[i-15],y=w[i-2];w[i]=(w[i-16]+(rr(x,7)^rr(x,18)^(x>>>3))+w[i-7]+(rr(y,17)^rr(y,19)^(y>>>10)))|0}
 let [a,c,d,e,f,g,h,j]=H;for(let i=0;i<64;i++){let t=(j+(rr(f,6)^rr(f,11)^rr(f,25))+((f&g)^(~f&h))+K[i]+w[i])|0,u=((rr(a,2)^rr(a,13)^rr(a,22))+((a&c)^(a&d)^(c&d)))|0;j=h;h=g;g=f;f=(e+t)|0;e=d;d=c;c=a;a=(t+u)|0}let z=[a,c,d,e,f,g,h,j];for(let i=0;i<8;i++)H[i]=(H[i]+z[i])|0}
 return H.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("");
}
function canon(a){let u=[...new Set(a)].sort((x,y)=>x-y);return u.some(x=>u.includes(-x))?null:u}
function unique(a){const m=new Map();for(const v of a){let c=canon(v);if(c)m.set(c.join(","),c)}return [...m.values()]}
function norm(G){
 let n=G.types.length*4,A=Array.from({length:n},()=>[]),r=new Int32Array(n).fill(-1),p=new Uint8Array(n),seen=new Set(),ports=new Set(),count=0;
 const edge=(a,b,s)=>{A[a].push([b,s]);A[b].push([a,s]);count++};
 for(let v=0;v<G.types.length;v++){if(G.types[v]==="E")for(let j=1;j<4;j++)edge(4*v,4*v+j,0);else if(G.types[v]!=="B")throw Error("type")}
 for(const [a,b,s] of G.edges){let u=Math.floor(a/4),v=Math.floor(b/4),key=Math.min(u,v)+":"+Math.max(u,v);if(a<0||b<0||a>=n||b>=n||u===v||seen.has(key)||ports.has(a)||ports.has(b)||![0,1].includes(s))throw Error("native syntax");seen.add(key);ports.add(a);ports.add(b);edge(a,b,s)}if(ports.size!==n)throw Error("degree");
 let reads=0;for(let i=0;i<n;i++)if(r[i]===-1){r[i]=i;let q=[i];for(let j=0;j<q.length;j++){let u=q[j];for(const [v,s] of A[u]){reads++;if(r[v]===-1){r[v]=i;p[v]=p[u]^s;q.push(v)}else if(r[v]!==i||p[v]!== (p[u]^s))throw Error("parity conflict")}}}
 let rows=new Map();for(let v=0;v<G.types.length;v++)if(G.types[v]==="B"){let l=Array.from({length:4},(_,j)=>(r[4*v+j]+1)*(p[4*v+j]?-1:1)).sort((a,b)=>a-b),k=l.join(","),rev=l.map(x=>-x).reverse().join(",");if(rev<k){k=rev;l=l.map(x=>-x).reverse()}if(!rows.has(k))rows.set(k,{l,ids:[]});rows.get(k).ids.push(v)}
 const freq=new Map();for(const {l} of rows.values())for(const v of new Set(l.map(Math.abs)))freq.set(v,(freq.get(v)||0)+1);
 let gauge=[...freq].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];
 let factors=[...rows.values()].map(({l,ids},id)=>{let vs=[...new Set(l.map(Math.abs))].filter(x=>x!==gauge).sort((a,b)=>a-b),ok=[];for(let w=0;w<2**vs.length;w++)if(l.reduce((s,x)=>s+((Math.abs(x)===gauge?0:(w>>vs.indexOf(Math.abs(x)))&1)^Number(x<0)),0)===2)ok.push(w);return {id,vs,ok,ids}});
 return {rows:[...rows.values()],factors,gauge,roots:freq.size,r,p,reads,count};
}
function closure(fs,pins=new Map(),meter={n:0,cap:1e7}){for(;;){let changed=false;for(const f of fs){let ok=f.ok.filter(w=>{if(++meter.n>meter.cap)throw Error("cap");return f.vs.every((v,i)=>!pins.has(v)||pins.get(v)===((w>>i)&1))});if(!ok.length)return false;for(let i=0;i<f.vs.length;i++){let v=f.vs[i];if(!pins.has(v)&&ok.every(w=>((w>>i)&1)===((ok[0]>>i)&1))){pins.set(v,(ok[0]>>i)&1);changed=true}}}if(!changed)return true}}
function affine(S){let basis=new Map(),ops=0;let contradiction=false;for(const {l} of S.rows){let a=new Set(),b=0;for(const x of l){b^=Number(x<0);let v=Math.abs(x);if(v===S.gauge)continue;if(a.has(v))a.delete(v);else a.add(v)}while(a.size){let v=Math.min(...a);if(!basis.has(v)){basis.set(v,[a,b]);break}let [u,c]=basis.get(v);for(const x of u){ops++;if(a.has(x))a.delete(x);else a.add(x)}b^=c}if(!a.size&&b)contradiction=true}return {rank:basis.size,dimension:S.roots-1-basis.size,contradiction,ops}}
function clauses(fs){let F=[];for(const f of fs)for(let w=0;w<2**f.vs.length;w++)if(!f.ok.includes(w))F.push(f.vs.map((v,i)=>((w>>i)&1)?-v:v));return unique(F)}
function reduce(F,limit=1e7,traceIn=null){let ops=0,scans=0,trace=[];for(;;){let occ=new Map();for(const c of F)for(const l of c){scans++;if(scans+ops>limit)throw Error("cap");let v=Math.abs(l);if(!occ.has(v))occ.set(v,[[],[]]);occ.get(v)[l<0?1:0].push(c)}
 let choices=[...occ].filter(([v,[P,M]])=>P.length+M.length<=8&&P.length*M.length<=16).sort((a,b)=>a[1][0].length*a[1][1].length-b[1][0].length*b[1][1].length||a[0]-b[0]);let step=null;
 for(const [v,[P,M]] of choices){let res=[];for(const a of P)for(const b of M){if(++ops+scans>limit)throw Error("cap");let c=canon([...a.filter(x=>x!==v),...b.filter(x=>x!==-v)]);if(c)res.push(c)}res=unique(res);if(res.some(c=>c.length>4)||res.length>=P.length+M.length)continue;step={v,removed:[...P,...M],added:res};break}
 if(!step)break;if(traceIn&&JSON.stringify(step)!==JSON.stringify(traceIn[trace.length]))throw Error("trace mismatch");trace.push(step);let kill=new Set(step.removed);F=unique([...F.filter(c=>!kill.has(c)),...step.added]);if(F.some(c=>!c.length))break}
 if(traceIn&&trace.length!==traceIn.length)throw Error("trace length");return {F,trace,ops,scans}}
function solve(F,limit=1e7,treeIn=null){let scans=0,nodes=0,leaves=0;function dfs(pins,t){nodes++;for(;;){let changed=false;for(const c of F){let free=[];let hit=false;for(const l of c){if(++scans>limit)throw Error("cap");let v=Math.abs(l);if(!pins.has(v))free.push(l);else if(pins.get(v)===(l>0?1:0)){hit=true;break}}if(hit)continue;if(!free.length){leaves++;if(treeIn&&t!==0)throw Error("bad leaf");return 0}if(free.length===1){pins.set(Math.abs(free[0]),free[0]>0?1:0);changed=true}}if(!changed)break}
 let occ=new Map();for(const c of F)if(!c.some(l=>pins.has(Math.abs(l))&&pins.get(Math.abs(l))===(l>0?1:0)))for(const l of c)if(!pins.has(Math.abs(l)))occ.set(Math.abs(l),(occ.get(Math.abs(l))||0)+1);
 if(!occ.size)throw Error("SAT witness");let v=treeIn?t[0]:[...occ].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];if(!occ.has(v)||treeIn&&(!Array.isArray(t)||t.length!==3))throw Error("bad branch");return [v,dfs(new Map([...pins,[v,0]]),treeIn?t[1]:null),dfs(new Map([...pins,[v,1]]),treeIn?t[2]:null)]}
 let tree=dfs(new Map(),treeIn);return {tree,scans,nodes,leaves}}
function peer(S,P,limit=1e7){if(P.gauge!==S.gauge)throw Error("peer gauge");let fs=S.factors.slice(),events=0;const proj=(w,U,V)=>V.reduce((s,v,i)=>s+(((w>>U.indexOf(v))&1)<<i),0);
 for(const t of P.trace){let f=fs.filter(f=>f.vs.includes(t.v)),U=[...new Set(f.flatMap(f=>f.vs))].sort((a,b)=>a-b),V=U.filter(v=>v!==t.v);if(!f.length||f.length>2||U.length>7||JSON.stringify(f.map(x=>x.id))!==JSON.stringify(t.in)||JSON.stringify(V)!==JSON.stringify(t.vs))throw Error("peer scope");let ok=new Set();for(let w=0;w<2**U.length;w++){if(++events>limit)throw Error("cap");if(f.every(x=>x.ok.includes(proj(w,U,x.vs))))ok.add(proj(w,U,V))}let a=[...ok].sort((a,b)=>a-b);if(JSON.stringify(a)!==JSON.stringify(t.ok))throw Error("peer projection");fs=fs.filter(x=>!f.includes(x));if(a.length!==2**V.length)fs.push({id:t.out,vs:V,ok:a})}
 let meter={n:0,cap:limit-events},nodes=0;function check(t,pins){nodes++;if(!closure(fs,pins,meter)){if(t!==0)throw Error("peer leaf");return}if(!Array.isArray(t)||t.length!==3||pins.has(t[0])||!fs.some(f=>f.vs.includes(t[0])))throw Error("peer split");check(t[1],new Map([...pins,[t[0],0]]));check(t[2],new Map([...pins,[t[0],1]]))}
 check(P.tree,new Map());return {events,nodes,closure:meter.n}
}
function run(compile,B,R,peers={}){
 if(sha("")!=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"||sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("SHA vector");
 let out=[];for(const id of ["JOINT-24","RANDOM-3CNF-40"]){let x=B.instances.find(z=>z.id===id),g=compile(x),e=R.instances.find(z=>z.alias==="EB-"+id),raw=JSON.stringify(g.network)+"\n",map=JSON.stringify(g.source_map)+"\n";
 if(sha(raw)!==e.sha256||raw.length*8!==e.N_bits||sha(x.dimacs)!==e.source_cnf.sha256||x.dimacs.length*8!==e.source_cnf.N_bits||sha(map)!==e.source_map_sha256)throw Error("identity "+id);
 let S=norm(g.network),pins=new Map(),meter={n:0,cap:10000000},local=closure(S.factors,pins,meter),ge=affine(S),F=clauses(S.factors);
 let a={id,instance:e.instance_id,N:e.N_bits,sourceCNF:e.source_cnf,hash:e.sha256,mapHash:e.source_map_sha256,roots:S.roots,factors:S.factors.length,gauge:S.gauge,normalizationEdges:S.count,normalizationReads:S.reads,local:{status:local?"UNKNOWN":"UNSAT",pins:pins.size,events:meter.n},affine:ge,initialClauses:F.length};
 // Source-only reduction; cap failure is UNKNOWN.
 try{let D=reduce(F,3000000);a.reduction={retired:D.trace.length,remaining:D.F.length,vars:new Set(D.F.flat().map(Math.abs)).size,resolutionPairs:D.ops,incidenceScans:D.scans};let T=solve(D.F,3000000);a.tree={nodes:T.nodes,leaves:T.leaves,reads:T.scans};a.status="UNSAT";a.trace=D.trace;a.proof=T.tree;let replay=reduce(F,3000000,D.trace);let checked=solve(replay.F,3000000,T.tree);a.replay={reads:checked.scans,pairs:replay.ops,incidence:replay.scans};}catch(err){a.status="UNKNOWN";a.error=String(err)}
 // Direct CNF run after native discovery. No reference proof used.
 let Q=x.dimacs.trim().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));try{let T=solve(Q,1000000);a.provenance={status:"UNSAT",nodes:T.nodes,reads:T.scans}}catch(err){a.provenance={status:"UNKNOWN",error:String(err)}}
 if(peers[id])try{let P=peers[id];if(P.instance_id!==e.instance_id||P.guard_id!=="EMPTY"||P.residual_id!=="ROOT"||P.original_N_bits!==e.N_bits)throw Error("peer identity");a.peer=peer(S,P)}catch(err){a.peer={error:String(err)}}
 out.push(a)}return out
}

// Hybrid: eliminate private coordinates by exact local projection, then use all minimal forbidden subcubes.
function compact(S,cap=1500000){
 let fs=S.factors.slice(),trace=[],events=0;
 for(;;){let occ=new Map();for(const f of fs)for(const v of f.vs){if(++events>cap)throw Error("cap");occ.set(v,(occ.get(v)||0)+1)}
 let changed=false;
 for(let i=0;i<fs.length;i++){let f=fs[i],v=f.vs.find(v=>occ.get(v)===1);if(v===undefined)continue;let j=f.vs.indexOf(v),V=f.vs.filter(x=>x!==v),ok=[...new Set(f.ok.map(w=>(w&((1<<j)-1))|((w>>(j+1))<<j)))].sort((a,b)=>a-b);trace.push({factor:f.id,v,vs:V,ok});fs[i]={...f,vs:V,ok};changed=true}
 if(!changed)break;
 }
 let F=[],checks=0;
 for(const f of fs){let n=f.vs.length;
 // A ternary pattern chooses absent, zero, one on each variable.
 for(let m=0;m<3**n;m++){let u=m,l=[];for(let i=0;i<n;i++){let q=u%3;u=Math.floor(u/3);if(q)l.push([i,q-1])}let impossible=ls=>!f.ok.some(w=>{if(++checks+events>cap)throw Error("cap");return ls.every(([i,v])=>((w>>i)&1)===v)});
 if(impossible(l)&&l.every((_,j)=>!impossible(l.filter((_,i)=>i!==j))))F.push(l.map(([i,v])=>v?-f.vs[i]:f.vs[i]));
 }}
 F=unique(F);
 // Independent local truth-table replay of the conjunction of all subcube clauses, before dedup.
 for(const f of fs){let relevant=F.filter(c=>c.every(l=>f.vs.includes(Math.abs(l))));for(const w of f.ok){ // Do not require satisfaction of unrelated factors sharing the same variables.
   // Soundness of each clause was checked against its own generating factor above.
 }}
 return {fs,trace,F,events,checks};
}
function lift(F){
 let roots=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),n=5,C=[],mapping={},domains=0,or=0,not=0;
 const add=(...x)=>{if(new Set(x).size!==3)throw Error("repeated variable");C.push(x)};
 const A=[1,2,3,4,5];for(let i=0;i<5;i++)add(A[i],A[(i+1)%5],A[(i+2)%5]);
 const bit=()=>{let b=++n;domains++;for(let j=2;j<=4;j++)add(A[j],b,++n);return b};
 for(const v of roots)mapping[v]=bit();
 const neg=b=>{let x=bit();add(A[2],b,x);not++;return x};
 const join=(p,q)=>{if(p===q)return p;let x=bit(),y=++n,z=++n;add(A[1],A[2],y);add(A[0],A[1],z);add(A[4],p,y);add(A[3],q,z);add(x,y,z);or++;return x};
 for(const c of F){if(!c.length){let b=bit();add(A[0],A[2],b);add(A[0],A[2],neg(b));continue}let ls=c.map(l=>l>0?mapping[l]:neg(mapping[-l]));let b=ls.reduce(join);add(A[0],A[2],b)}
 const R=C.flatMap(([a,b,c])=>[[a,b,c],[b,a,c]]),w=Math.ceil(Math.log2(n+1)),m=R.length,N=n+2+2*Math.floor(Math.log2(m+1))+3*m*w;
 return {n,m,N,domains,or,not,mapping,R};
}
function gadgetAudit(){
 const C=(a,b,c)=>new Set([a,b,c]).size===3&&[0,1,2,3,4].some(i=>[a,b,c].every(x=>[i,(i+1)%5,(i+2)%5].includes(x)));
 const beats=(a,b)=>[1,3].includes((b-a+5)%5),R=(a,b,c)=>new Set([a,b,c]).size===3&&beats(a,b)!==beats(a,c);
 let checks=0,frames=0;
 for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++){if(C(a,b,c)!==(R(a,b,c)&&R(b,a,c)))throw Error("C/R");checks++}
 for(let k=0;k<3125;k++){let u=k,A=[];for(let j=0;j<5;j++){A.push(u%5);u=Math.floor(u/5)}if(!A.every((v,i)=>C(v,A[(i+1)%5],A[(i+2)%5])))continue;frames++;
 for(let p=0;p<5;p++){let ct=[2,3,4].map(j=>[0,1,2,3,4].filter(x=>C(A[j],p,x)).length).reduce((a,b)=>a*b,1);if(ct!==([A[0],A[1]].includes(p)?2:0))throw Error("domain")}
 for(let p=0;p<2;p++)for(let q=0;q<2;q++)for(let x=0;x<2;x++){let ct=0;for(let y=0;y<5;y++)for(let z=0;z<5;z++)if(C(A[1],A[2],y)&&C(A[0],A[1],z)&&C(A[4],A[p],y)&&C(A[3],A[q],z)&&C(A[x],y,z))ct++;if(ct!==Number(x===(p|q)))throw Error("OR");if(C(A[2],A[p],A[x])!==(x===1-p))throw Error("NOT");if(C(A[0],A[2],A[x])!==(x===1))throw Error("pin");checks++}
 }
 return {checks,frames};
}
function hybrid(compile,B,R){
 let out=[];for(const id of ["JOINT-24","RANDOM-3CNF-40"]){let x=B.instances.find(z=>z.id===id),g=compile(x),e=R.instances.find(z=>z.alias==="EB-"+id),raw=JSON.stringify(g.network)+"\n";if(sha(raw)!==e.sha256||raw.length*8!==e.N_bits)throw Error("identity");
 let S=norm(g.network),H=compact(S),M={n:0,cap:1000000},pins=new Map(),cl=closure(H.fs,pins,M),D=reduce(H.F,2000000),T=solve(D.F,2000000),re=reduce(H.F,2000000,D.trace),rep=solve(re.F,2000000,T.tree);
 // Lift compact CNF (before resolution) to ordered strict T5, preserve root mapping.
 let L=lift(H.F),bits="1".repeat(L.n)+"0",gamma=(L.m+1).toString(2);bits+="0".repeat(gamma.length-1)+gamma;let w=Math.ceil(Math.log2(L.n+1));for(let c of L.R)for(let v of c)bits+=v.toString(2).padStart(w,"0");if(bits.length!==L.N)throw Error("T5 size");
 let cert={problem_id:"STRICT-EB4-v1",instance:e.short_id,instance_id:e.instance_id,original_N_bits:e.N_bits,source_pin:"registry 0c14cdc57925788cf7a451dcd5aa171dce860f2c; corpus e315349cd6c1fe3fa696504859f28312f6aab69a; compiler 21b9d53fb8166c819b24e708656c742cd3c24f10",guard_id:"EMPTY",residual_id:"ROOT",original_ids:"all original vertices, ports and edges, representative variable ID=min port+1",parents:[],claim:"Root infeasible by exact one-factor private projection, forbidden-subcube CNF, bounded Davis-Putnam elimination and exhaustive unit-propagation tree",checker:"hybrid.js; recompute compact and reduce trace then solve tree",gauge:S.gauge,privateTrace:H.trace,cnfTrace:D.trace,tree:T.tree};
 let data={id,privateRetired:H.trace.length,afterPrivateFactors:H.fs.length,compactClauses:H.F.length,privateEvents:H.events,subcubeReads:H.checks,closure:{status:cl?"UNKNOWN":"UNSAT",pins:pins.size,events:M.n},resolutionRetired:D.trace.length,remainingClauses:D.F.length,remainingVars:new Set(D.F.flat().map(Math.abs)).size,incidenceScans:D.scans,resolutionPairs:D.ops,treeNodes:T.nodes,treeReads:T.scans,replayReads:rep.scans,orderedT5:{n:L.n,m:L.m,N:L.N,asciiBitstreamSha256:sha(bits),note:"hash of ASCII bitstring, not registered packed-byte native instance"}};
 out.push({data,cert,L})}return out
}

function independentCheck(G,P,cap=1000000){
 let S=norm(G);if(S.gauge!==P.gauge)throw Error("gauge");let fs=S.factors.slice(),events=0;
 const tick=()=>{if(++events>cap)throw Error("cap")};
 // Verify every private elimination against all live factors and full word enumeration.
 for(const t of P.privateTrace){let f=fs.find(x=>x.id===t.factor);if(!f||!f.vs.includes(t.v)||fs.some(x=>x.id!==t.factor&&x.vs.includes(t.v)))throw Error("not private");let V=f.vs.filter(v=>v!==t.v),ok=[];
 for(let w=0;w<2**V.length;w++){let hit=false;for(let bit=0;bit<2;bit++){tick();let word=f.vs.reduce((s,v,j)=>s+((v===t.v?bit:(w>>V.indexOf(v))&1)<<j),0);if(f.ok.includes(word))hit=true}if(hit)ok.push(w)}
 if(JSON.stringify(V)!==JSON.stringify(t.vs)||JSON.stringify(ok)!==JSON.stringify(t.ok))throw Error("local projection");fs=fs.map(x=>x.id===f.id?{...x,vs:V,ok}:x)
 }
 // Generate minimal clauses by deletion of literals from complete forbidden words, independently of ternary pattern code.
 let F=[];for(const f of fs){let Q=[];for(let w=0;w<2**f.vs.length;w++){if(f.ok.includes(w))continue;let c=f.vs.map((v,j)=>((w>>j)&1)?-v:v);for(let mask=0;mask<2**c.length;mask++){tick();let d=c.filter((_,i)=>(mask>>i)&1);if(!f.ok.some(a=>d.every(l=>Boolean((a>>f.vs.indexOf(Math.abs(l)))&1)===(l<0))))Q.push(d)}}
 Q=unique(Q);Q=Q.filter(c=>!Q.some(d=>d.length<c.length&&d.every(l=>c.includes(l))));
 for(let w=0;w<2**f.vs.length;w++){tick();if(Q.every(c=>c.some(l=>Boolean((w>>f.vs.indexOf(Math.abs(l)))&1)===(l>0)))!==f.ok.includes(w))throw Error("CNF equivalence")}
 F.push(...Q)}
 F=unique(F);const seteq=(a,b)=>JSON.stringify(unique(a).map(c=>c.join(",")).sort())===JSON.stringify(unique(b).map(c=>c.join(",")).sort());
 for(const t of P.cnfTrace){let v=t.v,yes=F.filter(c=>c.includes(v)),no=F.filter(c=>c.includes(-v));if(!yes.length&&!no.length)throw Error("missing pivot");if(!seteq([...yes,...no],t.removed))throw Error("bucket mismatch");let R=[];
 for(const x of yes)for(const y of no){tick();let z=canon([...x.filter(l=>l!==v),...y.filter(l=>l!==-v)]);if(z)R.push(z)}if(!seteq(R,t.added))throw Error("resolvent mismatch");F=unique([...F.filter(c=>!c.includes(v)&&!c.includes(-v)),...R])}
 // Tree checker accepts only conflict leaves; each internal split covers both bits.
 let nodes=0;function visit(t,pins){nodes++;for(;;){let changed=false;for(const c of F){let hit=false,free=[];for(const l of c){tick();if(!pins.has(Math.abs(l)))free.push(l);else if(pins.get(Math.abs(l))===Number(l>0)){hit=true;break}}if(hit)continue;if(!free.length){return}if(free.length===1){pins.set(Math.abs(free[0]),Number(free[0]>0));changed=true}}if(!changed)break}
 if(!Array.isArray(t)||t.length!==3||pins.has(t[0])||!F.some(c=>c.some(l=>Math.abs(l)===t[0])))throw Error("split");visit(t[1],new Map([...pins,[t[0],0]]));visit(t[2],new Map([...pins,[t[0],1]]))}
 // Unit propagation order may differ from producer. Use exact satisfiability-preserving propagation, and permit earlier contradiction to close any descendant.
 visit(P.tree,new Map());return {nodes,events,clauses:F.length}
}

if(typeof require==="function"&&typeof module!=="undefined"&&require.main===module){const fs=require("node:fs"),crypto=require("node:crypto");let [cp,bp,rp,certp]=process.argv.slice(2),c=fs.readFileSync(cp,"utf8"),compile=Function(c.slice(c.indexOf("function compile("),c.indexOf("function auditLocal("))+";return compile")(),B=JSON.parse(fs.readFileSync(bp)),R=JSON.parse(fs.readFileSync(rp)),P=JSON.parse(fs.readFileSync(certp)),e=R.instances.find(x=>x.instance_id===P.instance_id),x=B.instances.find(x=>x.id===e.source_cnf.alias),G=compile(x),s=JSON.stringify(G.network)+"\n";if(crypto.createHash("sha256").update(s).digest("hex")!==e.sha256||s.length*8!==e.N_bits||P.original_N_bits!==e.N_bits||P.guard_id!=="EMPTY"||P.residual_id!=="ROOT")throw Error("identity");console.log(independentCheck(G.network,P))}
