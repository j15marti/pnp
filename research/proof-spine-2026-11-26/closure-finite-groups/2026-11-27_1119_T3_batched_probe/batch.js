// Node.js 20+; arguments: pinned benchmarks.json, registry.json, JOINT certificate, RANDOM certificate. Source compiler embedded exactly from pinned commit 21b9d53... .
function compile(instance){
 const lines=instance.dimacs.trimEnd().split("\n"),h=lines.shift().split(" ").map((s,i)=>i>=2?Number(s):s);
 if(h[0]!=="p"||h[1]!=="cnf"||h[2]!==instance.nvars||h[3]!==lines.length)throw Error("header");
 const n=instance.nvars,F=[],parents=[];let next=n;
 const add=(a,id)=>{F.push(a);parents.push(id)};
 lines.forEach((line,i)=>{const a=line.split(/\s+/).map(Number);if(a.pop()!==0||a.some(l=>!Number.isInteger(l)||!l||Math.abs(l)>n))throw Error("bad clause");const id=i+1;if(a.length===0){let v=++next;add([v,v,v],id);add([-v,-v,-v],id)}else if(a.length<=3){while(a.length<3)a.push(a[a.length-1]);add(a,id)}else{let prev=++next;add([a[0],a[1],prev],id);for(let j=2;j<a.length-2;j++){let t=++next;add([-prev,a[j],t],id);prev=t}add([-prev,a[a.length-2],a[a.length-1]],id)}});
 const types=[],used=[],edges=[],groups=new Map(),reps={},owners=[];
 const V=(t,owner)=>{types.push(t);used.push(0);owners.push(owner);return types.length-1};
 const P=v=>{if(used[v]>=4)throw Error("port overflow");return 4*v+used[v]++};
 const E=(a,b,s=0)=>edges.push([a,b,s]);
 const wire=(a,b,s)=>{const v=Array.from({length:5},()=>V("E",["wire",a,b]));for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)if(i!==0||j!==1)E(P(v[i]),P(v[j]));E(a,P(v[0]),s);E(b,P(v[1]),0)};
 const occ=(id,s,p)=>{if(!groups.has(id))groups.set(id,[]);groups.get(id).push([p,s])};
 F.forEach(([a,b,c],i)=>{const L=x=>["x"+Math.abs(x),Number(x<0)],z="z"+i,T=[[L(a),L(b),[z,0]],[[z,1],L(c),["f",0]]];for(let j=0;j<2;j++)for(let k=0;k<2;k++){let v=V("B",["clause",parents[i],i,j,k]);for(const [id,s] of T[j])occ(id,s,P(v));occ("w"+i+"_"+j,0,P(v))}});
 for(const [id,O] of groups){if(O.length%2||O.length<2)throw Error("occurrence parity");reps[id]=O[0];if(O.length===2){wire(O[0][0],O[1][0],O[0][1]^O[1][1]);continue}const a=Array.from({length:(O.length-2)/2},()=>V("E",["carrier",id]));for(let i=1;i<a.length;i++)wire(P(a[i-1]),P(a[i]),0);let k=0;for(const v of a)while(used[v]<4){const [p,s]=O[k++];wire(P(v),p,s)}if(k!==O.length)throw Error("fanout")}
 const seen=new Set(),ports=new Set();for(const [a,b,s] of edges){let u=Math.floor(a/4),v=Math.floor(b/4),key=Math.min(u,v)+":"+Math.max(u,v);if(u===v||seen.has(key)||ports.has(a)||ports.has(b)||![0,1].includes(s))throw Error("not simple signed 4-regular");seen.add(key);ports.add(a);ports.add(b)}
 if(used.some(x=>x!==4)||ports.size!==4*types.length)throw Error("degree");
 const network={format:"STRICT-EB4-v1",types,edges};
 return {network,source_map:{original_n:n,ternary_clauses:F,original_clause_ids:parents,representative_ports:reps,vertex_provenance:owners}};
}
function sha(s){
 const K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
 const H=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19],n=s.length;
 const b=new Uint8Array(Math.ceil((n+9)/64)*64);for(let i=0;i<n;i++){if(s.charCodeAt(i)>127)throw Error("non ASCII");b[i]=s.charCodeAt(i)}b[n]=128;let len=BigInt(n)*8n;for(let i=0;i<8;i++){b[b.length-1-i]=Number(len&255n);len>>=8n}
 const rr=(x,k)=>(x>>>k)|(x<<(32-k)),w=new Uint32Array(64);
 for(let j=0;j<b.length;j+=64){for(let i=0;i<16;i++)w[i]=(b[j+4*i]<<24)|(b[j+4*i+1]<<16)|(b[j+4*i+2]<<8)|b[j+4*i+3];for(let i=16;i<64;i++){let a=w[i-15],c=w[i-2];w[i]=(w[i-16]+(rr(a,7)^rr(a,18)^(a>>>3))+w[i-7]+(rr(c,17)^rr(c,19)^(c>>>10)))>>>0}
 let [a,c,d,e,f,g,h,k]=H;for(let i=0;i<64;i++){let t=(k+(rr(f,6)^rr(f,11)^rr(f,25))+((f&g)^(~f&h))+K[i]+w[i])>>>0,u=((rr(a,2)^rr(a,13)^rr(a,22))+((a&c)^(a&d)^(c&d)))>>>0;k=h;h=g;g=f;f=(e+t)>>>0;e=d;d=c;c=a;a=(t+u)>>>0}for(let i=0;i<8;i++)H[i]=(H[i]+[a,c,d,e,f,g,h,k][i])>>>0}
 return H.map(x=>x.toString(16).padStart(8,"0")).join("");
}
function normalize(G){
 const m=4*G.types.length,adj=Array.from({length:m},()=>[]),used=new Uint8Array(m),pairs=new Set();
 const add=(a,b,s)=>{adj[a].push([b,s]);adj[b].push([a,s])};
 for(const [a,b,s] of G.edges){let u=a>>2,v=b>>2,k=Math.min(u,v)+":"+Math.max(u,v);if(a<0||b<0||a>=m||b>=m||used[a]||used[b]||u===v||pairs.has(k)||![0,1].includes(s))throw Error("invalid edge");used[a]=used[b]=1;pairs.add(k);add(a,b,s)}
 if(used.some(x=>!x))throw Error("missing port");
 for(let v=0;v<G.types.length;v++){if(G.types[v]==="E")for(let j=1;j<4;j++)add(4*v,4*v+j,0);else if(G.types[v]!=="B")throw Error("bad type")}
 let root=new Int32Array(m).fill(-1),phase=new Uint8Array(m),parent=new Int32Array(m),ph=new Uint8Array(m),depth=new Int32Array(m),maxDepth=0,components=0,visits=0;
 for(let i=0;i<m;i++){if(root[i]>=0)continue;components++;let queue=[i];root[i]=parent[i]=i;for(let t=0;t<queue.length;t++){let a=queue[t];for(let [b,s] of adj[a]){visits++;if(root[b]<0){root[b]=i;phase[b]=phase[a]^s;parent[b]=a;ph[b]=s;depth[b]=depth[a]+1;maxDepth=Math.max(maxDepth,depth[b]);queue.push(b)}else if(root[b]!==i||(phase[a]^phase[b])!==s)throw Error("parity contradiction")}}}
 let P=parent,Q=ph,rounds=0,gathers=0;
 while(P.some((x,i)=>P[x]!==x)){let A=new Int32Array(m),B=new Uint8Array(m);for(let i=0;i<m;i++){A[i]=P[P[i]];B[i]=Q[i]^Q[P[i]];gathers++}P=A;Q=B;rounds++}
 // Last round is unnecessary when all pointers already point at roots.
 for(let i=0;i<m;i++)if(P[i]!==root[i]||Q[i]!==phase[i])throw Error("jump mismatch");
 let tables=new Map(),rows=0,nonfull=0,forced=0;
 for(let v=0;v<G.types.length;v++)if(G.types[v]==="B"){let ps=[0,1,2,3].map(j=>4*v+j),r=[...new Set(ps.map(i=>P[i]))].sort((a,b)=>a-b),support=[];for(let mask=0;mask<2**r.length;mask++){rows++;let sum=ps.reduce((s,i)=>s+(((mask>>r.indexOf(P[i]))&1)^Q[i]),0);if(sum===2)support.push(mask)}if(!support.length)throw Error("local contradiction");if(support.length<2**r.length)nonfull++;for(let j=0;j<r.length;j++)if(support.every(x=>((x>>j)&1)===((support[0]>>j)&1)))forced++;let key=JSON.stringify([r,support]);tables.set(key,(tables.get(key)||[]).concat(v))}
 return {P,Q,metrics:{ports:m,components,forestMaxDepth:maxDepth,adjacencyVisits:visits,pointerRounds:rounds,pointerGathers:gathers,denseScorePairs:String(BigInt(gathers)*BigInt(m)),localBalanceRows:rows,nonfullFactors:nonfull,distinctTables:tables.size,unconditionalSingletons:forced}};
}
function verify(G,P,Q,c){
 const m=P.length,norm=a=>[...new Set(a)].sort((a,b)=>a-b),eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 let rec=new Map(),L=c.proof.records.length,axioms=0,res=0,reads=0,maxWidth=0,depth=new Map(),bad=0;
 // Static gather permits all rows to check simultaneously once duplicate IDs are rejected.
 for(const [id,r] of c.proof.records){if(!Number.isSafeInteger(id)||rec.has(id))throw Error("duplicate");rec.set(id,r);maxWidth=Math.max(maxWidth,r.c.length)}
 for(const [id,r] of c.proof.records){
 if(!eq(norm(r.c),r.c)||r.c.some(l=>!Number.isSafeInteger(l)||!l||Math.abs(l)>m||r.c.includes(-l)))throw Error("clause");
 if(r.src){axioms++;let [v,j,s]=r.src;if(v==="global-complement-gauge"){if(!Number.isInteger(j)||j<0||j>=m||P[j]!==j||!eq(r.c,[-j-1]))throw Error("gauge")}else{if(G.types[v]!=="B"||![0,1,2,3].includes(j)||![1,-1].includes(s))throw Error("axiom source");let a=[];for(let k=0;k<4;k++)if(k!==j)a.push(s*(P[4*v+k]+1)*(Q[4*v+k]?-1:1));if(!eq(norm(a),r.c))throw Error("axiom")}}
 else{res++;let [a,b,v]=r.p,x=rec.get(a)?.c,y=rec.get(b)?.c;if(!x||!y||a>=id||b>=id||!Number.isInteger(v)||v<=0||!(x.includes(v)&&y.includes(-v)||x.includes(-v)&&y.includes(v)))throw Error("parent");reads+=x.length+y.length;if(!eq(norm(x.concat(y).filter(l=>Math.abs(l)!==v)),r.c))throw Error("resolvent")}
 }
 if(rec.get(c.proof.terminal)?.c.length!==0)throw Error("terminal");
 return {records:L,axioms,resolutionRows:res,parentGathers:2*res,parentLiteralReads:reads,maxWidth,valid:true};
}

function makeFactors(G,P,Q){
 let m=new Map();for(let v=0;v<G.types.length;v++)if(G.types[v]==="B"){let p=[0,1,2,3].map(j=>4*v+j),s=[...new Set(p.map(i=>P[i]+1))].sort((a,b)=>a-b),a=[];for(let t=0;t<2**s.length;t++)if(p.reduce((sum,i)=>sum+(((t>>s.indexOf(P[i]+1))&1)^Q[i]),0)===2)a.push(t);m.set(JSON.stringify([s,a]),{s,a})}return [...m.values()];
}
function project(F,cap=4){
 F=F.map(x=>({s:x.s.slice(),a:x.a.slice()}));let trace=[],scans=0,rows=0;
 while(true){
 let inc=new Map();for(let i=0;i<F.length;i++)for(let v of F[i].s){scans++;if(!inc.has(v))inc.set(v,[]);inc.get(v).push(i)}
 let best=null;for(let [v,idx] of inc){let s=[...new Set(idx.flatMap(i=>F[i].s))].sort((a,b)=>a-b);if(s.length<=cap&&(!best||s.length<best.s.length||s.length===best.s.length&&v<best.v))best={v,idx,s}}
 if(!best)break;let {v,idx,s}=best,b=s.filter(x=>x!==v),a=[];
 for(let t=0;t<2**b.length;t++){let ok=false;for(let z=0;z<2;z++){rows++;if(idx.every(i=>{let x=F[i];let u=x.s.reduce((m,w,j)=>m|((w===v?z:(t>>b.indexOf(w))&1)<<j),0);return x.a.includes(u)})){ok=true;break}}if(ok)a.push(t)}
 trace.push(v);let del=new Set(idx);F=F.filter((_,i)=>!del.has(i));if(a.length!==2**b.length)F.push({s:b,a});if(!a.length){F=[{s:b,a}];break}
 }
 return {F,trace,scans,rows};
}
function clauses(F){let map=new Map();for(let {s,a} of F)for(let t=0;t<2**s.length;t++)if(!a.includes(t)){let c=s.map((v,j)=>(t>>j)&1?-v:v);map.set(JSON.stringify(c),c)}return [...map.values()]}
function up(C,guard){let a=new Map(),steps=0;for(let l of guard){if(a.has(-l))return {bad:true,steps};a.set(l,true)}while(true){let changed=false;for(let c of C){let sat=false,u=0,n=0;for(let l of c){steps++;if(a.has(l)){sat=true;break}if(!a.has(-l)){u=l;n++}}if(sat)continue;if(!n)return {bad:true,steps};if(n===1&&!a.has(u)){a.set(u,true);changed=true}}if(!changed)return {bad:false,steps}}}
function batch(C,guards,maxEvents=10000000){let k=guards.length,all=(1n<<BigInt(k))-1n,T=new Map(),dead=0n,events=0,rounds=0;const get=l=>T.get(l)||0n;for(let i=0;i<k;i++)for(let l of guards[i])T.set(l,get(l)|(1n<<BigInt(i)));while(true){let next=new Map(T),d=dead;for(let c of C){let pre=[all],suf=[all];for(let i=0;i<c.length;i++){pre.push(pre[i]&get(-c[i]));events++}for(let i=c.length-1;i>=0;i--){suf[i]=suf[i+1]===undefined?get(-c[i]):suf[i+1]&get(-c[i]);events++}d|=pre[c.length];for(let i=0;i<c.length;i++){let v=c[i],b=pre[i]&(suf[i+1]??all);next.set(v,(next.get(v)||0n)|b);events+=2}}for(let [l,b] of next){d|=b&(next.get(-l)||0n);events++}rounds++;if(events*Math.ceil(k/32)>maxEvents)return {capped:true,events,rounds,k};let change=d!==dead||next.size!==T.size||[...next].some(([l,b])=>b!==get(l));dead=d;T=next;if(!change||dead===all)break}return {capped:false,dead,events,rounds,k}}
function run(C,maxEpoch=12){
 let initial=C.length,learn=[],metrics=[],replay=0,spent=0,seen=new Set(C.map(c=>JSON.stringify(c)));
 for(let i=0;i<maxEpoch;i++){let x=up(C,[]);replay+=x.steps;if(x.bad)return {status:"UNSAT",initial,learn,metrics,replay,spent};
 let vars=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),lits=vars.flatMap(v=>[-v,v]),added=0;
 for(let width of [1,2]){
 let guards=width===1?lits.map(l=>[l]):lits.flatMap((l,i)=>lits.slice(i+1).filter(k=>Math.abs(k)!==Math.abs(l)).map(k=>[l,k]));
 guards=guards.filter(g=>!seen.has(JSON.stringify(g.map(l=>-l).sort((a,b)=>Math.abs(a)-Math.abs(b)))));
 if(!guards.length)continue;
 let b=batch(C,guards,10000000-spent);let wordEvents=b.events*Math.ceil(b.k/32);spent+=wordEvents;metrics.push({epoch:i,width,guards:b.k,rounds:b.rounds,maskOperations:b.events,wordEvents,capped:b.capped});
 if(b.capped)return {status:"UNKNOWN",initial,learn,metrics,replay,spent};
 for(let j=0;j<guards.length;j++)if((b.dead>>BigInt(j))&1n){let g=guards[j],c=g.map(l=>-l).sort((a,b)=>Math.abs(a)-Math.abs(b)),key=JSON.stringify(c);if(seen.has(key))continue;let a=up(C,g);replay+=a.steps;if(!a.bad)throw Error("mask false positive");C.push(c);seen.add(key);learn.push(c);added++}
 if(added)break;
 }if(!added)break;
 }
 let x=up(C,[]);replay+=x.steps;return {status:x.bad?"UNSAT":"UNKNOWN",initial,learn,metrics,replay,spent};
}
module.exports={compile,sha,normalize,makeFactors,project,clauses,up,batch,run,verify};
