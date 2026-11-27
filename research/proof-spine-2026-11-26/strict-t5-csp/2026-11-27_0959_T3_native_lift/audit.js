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

if(typeof require==="function"&&typeof module!=="undefined"&&require.main===module){const fs=require("node:fs"),crypto=require("node:crypto");let [cp,bp,rp,...pp]=process.argv.slice(2),c=fs.readFileSync(cp,"utf8"),compile=Function(c.slice(c.indexOf("function compile("),c.indexOf("function auditLocal("))+";return compile")(),B=JSON.parse(fs.readFileSync(bp)),R=JSON.parse(fs.readFileSync(rp)),P={};for(const p of pp){let x=JSON.parse(fs.readFileSync(p));P[x.instance.split("@")[0].slice(3)]=x}for(const id of ["JOINT-24","RANDOM-3CNF-40"]){const x=B.instances.find(z=>z.id===id),g=compile(x),s=JSON.stringify(g.network)+"\n";if(sha(s)!==crypto.createHash("sha256").update(s).digest("hex"))throw Error("host hash discrepancy")}console.log(JSON.stringify(run(compile,B,R,P),null,2))}
