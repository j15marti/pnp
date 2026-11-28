// Node.js 20+: node gauge.js benchmarks.json registry.json certificate.json
function sha(s){const K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2],H=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19],n=s.length,L=Math.ceil((n+9)/64)*64,b=new Uint8Array(L),w=new Uint32Array(64);for(let i=0;i<n;i++){let v=s.charCodeAt(i);if(v>127)throw Error("nonASCII");b[i]=v}b[n]=128;let bits=n*8;for(let i=0;i<8;i++){b[L-1-i]=bits%256;bits=Math.floor(bits/256)}const ro=(x,k)=>(x>>>k)|(x<< (32-k));for(let p=0;p<L;p+=64){for(let i=0;i<16;i++){let t=p+4*i;w[i]=(b[t]<<24)|(b[t+1]<<16)|(b[t+2]<<8)|b[t+3]}for(let i=16;i<64;i++){let a=w[i-15],c=w[i-2];w[i]=w[i-16]+(ro(a,7)^ro(a,18)^(a>>>3))+w[i-7]+(ro(c,17)^ro(c,19)^(c>>>10))}let [a,c,d,e,f,g,h,j]=H;for(let i=0;i<64;i++){let t=(j+(ro(f,6)^ro(f,11)^ro(f,25))+((f&g)^(~f&h))+K[i]+w[i])|0,u=((ro(a,2)^ro(a,13)^ro(a,22))+((a&c)^(a&d)^(c&d)))|0;j=h;h=g;g=f;f=(e+t)|0;e=d;d=c;c=a;a=(t+u)|0}for(let i=0;i<8;i++)H[i]=(H[i]+[a,c,d,e,f,g,h,j][i])>>>0}return H.map(x=>x.toString(16).padStart(8,"0")).join("")}

function compile(instance){const lines=instance.dimacs.trimEnd().split("\n"),h=lines.shift().split(" ").map((s,i)=>i>=2?Number(s):s);if(h[0]!=="p"||h[1]!=="cnf"||h[2]!==instance.nvars||h[3]!==lines.length)throw Error("header");let n=instance.nvars,next=n,F=[],parents=[];const add=(a,id)=>{F.push(a);parents.push(id)};lines.forEach((line,i)=>{let a=line.split(/\s+/).map(Number);if(a.pop()!==0||a.some(l=>!Number.isInteger(l)||!l||Math.abs(l)>n))throw Error("clause");let id=i+1;if(!a.length){let v=++next;add([v,v,v],id);add([-v,-v,-v],id)}else if(a.length<=3){while(a.length<3)a.push(a[a.length-1]);add(a,id)}else{let prev=++next;add([a[0],a[1],prev],id);for(let j=2;j<a.length-2;j++){let t=++next;add([-prev,a[j],t],id);prev=t}add([-prev,a[a.length-2],a[a.length-1]],id)}});let types=[],used=[],edges=[],groups=new Map();const V=t=>{types.push(t);used.push(0);return types.length-1},P=v=>{if(used[v]>=4)throw Error("port");return 4*v+used[v]++},E=(a,b,s=0)=>edges.push([a,b,s]),wire=(a,b,s)=>{let v=Array.from({length:5},()=>V("E"));for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)if(i!==0||j!==1)E(P(v[i]),P(v[j]));E(a,P(v[0]),s);E(b,P(v[1]),0)},occ=(id,s,p)=>{if(!groups.has(id))groups.set(id,[]);groups.get(id).push([p,s])};F.forEach(([a,b,c],i)=>{let L=x=>["x"+Math.abs(x),+(x<0)],z="z"+i,T=[[L(a),L(b),[z,0]],[[z,1],L(c),["f",0]]];for(let j=0;j<2;j++)for(let k=0;k<2;k++){let v=V("B");for(let [id,s] of T[j])occ(id,s,P(v));occ("w"+i+"_"+j,0,P(v))}});for(let [id,O] of groups){if(O.length%2||O.length<2)throw Error("occurrence");if(O.length===2){wire(O[0][0],O[1][0],O[0][1]^O[1][1]);continue}let a=Array.from({length:(O.length-2)/2},()=>V("E"));for(let i=1;i<a.length;i++)wire(P(a[i-1]),P(a[i]),0);let k=0;for(let v of a)while(used[v]<4){let [p,s]=O[k++];wire(P(v),p,s)}if(k!==O.length)throw Error("fanout")}return {format:"STRICT-EB4-v1",types,edges}}

function quotient(G){let n=4*G.types.length,A=Array.from({length:n},()=>[]),R=new Int32Array(n).fill(-1),Q=new Uint8Array(n),used=new Set(),seen=new Set(),arcs=0,rows=0;function edge(a,b,s){A[a].push([b,s]);A[b].push([a,s])}for(let [a,b,s] of G.edges){let u=a>>2,v=b>>2,k=[Math.min(u,v),Math.max(u,v)].join(",");if(a<0||b<0||a>=n||b>=n||used.has(a)||used.has(b)||u===v||seen.has(k)||![0,1].includes(s))throw Error("edge");used.add(a);used.add(b);seen.add(k);edge(a,b,s)}if(used.size!==n)throw Error("ports");for(let v=0;v<G.types.length;v++){if(G.types[v]==="E")for(let j=1;j<4;j++)edge(4*v,4*v+j,0);else if(G.types[v]!=="B")throw Error("type")}for(let i=0;i<n;i++)if(R[i]<0){let q=[i];R[i]=i;for(let j=0;j<q.length;j++)for(let [v,s] of A[q[j]]){arcs++;let t=Q[q[j]]^s;if(R[v]<0){R[v]=i;Q[v]=t;q.push(v)}else if(R[v]!==i||Q[v]!==t)throw Error("signed cycle")}}let M=new Map();for(let v=0;v<G.types.length;v++)if(G.types[v]==="B"){let p=[0,1,2,3].map(j=>4*v+j),s=[...new Set(p.map(i=>R[i]+1))].sort((a,b)=>a-b),a=[];for(let t=0;t<2**s.length;t++){rows++;if(p.reduce((sum,i)=>sum+(((t>>s.indexOf(R[i]+1))&1)^Q[i]),0)===2)a.push(t)}M.set(JSON.stringify([s,a]),{s,a})}return {F:[...M.values()],arcs,rows,R,Q}}

function gauge(F){let deg=new Map();for(let x of F){let full=(1<<x.s.length)-1;for(let t of x.a)if(!x.a.includes(t^full))throw Error("non complement");for(let v of x.s)deg.set(v,(deg.get(v)||0)+1)}let g=[...deg].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0],visits=0;return {g,degree:deg.get(g),F:F.map(({s,a})=>{let j=s.indexOf(g);if(j<0)return {s,a};let low=(1<<j)-1,b=[];for(let t of a){visits++;if(!(t>>j&1))b.push((t&low)|((t>>(j+1))<<j))}return{s:s.filter(v=>v!==g),a:b}}),getVisits:()=>visits}}

function project(F,forcedTrace=null){F=F.map(x=>({s:x.s.slice(),a:x.a.slice()}));let trace=[],scans=0,rows=0;while(true){let inc=new Map();for(let i=0;i<F.length;i++)for(let v of F[i].s){scans++;if(!inc.has(v))inc.set(v,[]);inc.get(v).push(i)}let best=null;for(let [v,idx] of inc){if(forcedTrace&&v!==forcedTrace[trace.length])continue;let s=[...new Set(idx.flatMap(i=>F[i].s))].sort((a,b)=>a-b);if(s.length<=4&&(!best||s.length<best.s.length||s.length===best.s.length&&v<best.v))best={v,idx,s}}if(!best)break;let {v,idx,s}=best,b=s.filter(x=>x!==v),a=[];for(let t=0;t<2**b.length;t++){let ok=false;for(let z=0;z<2;z++){rows++;if(idx.every(i=>{let x=F[i];let u=x.s.reduce((m,w,j)=>m|((w===v?z:(t>>b.indexOf(w))&1)<<j),0);return x.a.includes(u)})){ok=true;break}}if(ok)a.push(t)}trace.push(v);let del=new Set(idx);F=F.filter((_,i)=>!del.has(i));if(a.length!==2**b.length)F.push({s:b,a});if(!a.length){F=[{s:b,a}];break}}if(forcedTrace&&trace.length!==forcedTrace.length)throw Error("trace");return {F,trace,scans,rows}}

function canon(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}

function clauses(F){let m=new Map();for(let {s,a} of F)for(let t=0;t<2**s.length;t++)if(!a.includes(t)){let c=s.map((v,j)=>(t>>j)&1?-v:v);m.set(c.join(","),c)}return [...m.values()]}

function up(C,g,L,cap){let A=new Set(g);if(g.some(l=>A.has(-l)))return {bad:true,A};let change=true;while(change){change=false;for(let c of C){let sat=false,u=0,n=0;for(let l of c){if(++L.visits>cap)throw Error("cap");if(A.has(l)){sat=true;break}if(!A.has(-l)){u=l;n++}}if(sat)continue;if(!n)return {bad:true,A};if(n===1){A.add(u);change=true}}}return {bad:false,A}}

function tree(base,seed=[],cap=700000){let C=base.concat(seed),L={visits:0,nodes:0,proof:[]};function go(g){L.nodes++;let {bad,A}=up(C,g,L,cap);if(bad){let cl=canon(g.map(x=>-x));C.push(cl);L.proof.push(cl);return true}let scores=new Map();for(let c of C){if(c.some(l=>{if(++L.visits>cap)throw Error("cap");return A.has(l)}))continue;for(let l of c){if(++L.visits>cap)throw Error("cap");if(!A.has(-l)){let v=Math.abs(l);scores.set(v,(scores.get(v)||0)+1)}}}if(!scores.size)return false;let v=[...scores].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];if(!go(g.concat(v))||!go(g.concat(-v)))return false;let cl=canon(g.map(x=>-x));C.push(cl);L.proof.push(cl);return true}try{L.status=go([])?"UNSAT":"UNKNOWN"}catch(e){if(e.message!=="cap")throw e;L.status="UNKNOWN"}return L}

function replay(base,proof){let C=base.map(c=>c.slice()),visits=0;for(let cl of proof){let a=new Map(cl.map(l=>[Math.abs(l),+(l<0)])),change=true,hit=false;while(change&&!hit){change=false;for(let c of C){let u=[],sat=false;for(let l of c){visits++;let b=a.get(Math.abs(l));if(b===undefined)u.push(l);else if(b===+(l>0)){sat=true;break}}if(sat)continue;if(!u.length){hit=true;break}if(u.length===1){a.set(Math.abs(u[0]),+(u[0]>0));change=true}}}if(!hit)throw Error("bad RUP "+cl);C.push(cl)}return{steps:proof.length,visits,unsat:proof.some(c=>!c.length)}}

function importPrefix(C,proof){let good=[],failed=[],visits=0;for(let c of proof){try{let r=replay(C.concat(good),[c]);visits+=r.visits;good.push(c)}catch(e){failed.push(c);break}}return {good,failed,visits}}

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

// Requires Node.js, pinned gauge.js and compile.js; study(L,G,q,g,p,C,seedClauses,[],cnf,caseName). Exported function; exact prior helper extraction described in report.
function study(L,G,q,g,p,C,seedClauses,peerPins,cnf,caseName){
 const {canon,up,tree,replay,project,clauses}=L;
 const vars=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),rank=vs=>vs.map(v=>[v,C.filter(c=>c.includes(v)||c.includes(-v)).length]).sort((a,b)=>b[1]-a[1]||a[0]-b[0]).map(a=>a[0]);
 const top=rank(vars).slice(0,4);
 const guards=top.map((v,i)=>top.slice(0,i).map(x=>-x).concat(v)).concat([top.map(x=>-x)]);
 const pins=h=>new Map(h.map(l=>[Math.abs(l),+(l>0)]));
 function occupancy(F,h){let A=pins(h),visits=0,rounds=0,change=true;while(change){change=false;rounds++;for(const f of F){let rows=f.a.filter(t=>{visits++;return f.s.every((v,j)=>!A.has(v)||A.get(v)===(t>>j&1))});if(!rows.length)return {bad:true,visits,rounds,forced:A.size-h.length};for(let j=0;j<f.s.length;j++)if(!A.has(f.s[j])&&rows.every(t=>(t>>j&1)===(rows[0]>>j&1))){A.set(f.s[j],rows[0]>>j&1);change=true}}}return{bad:false,visits,rounds,forced:A.size-h.length,assign:[...A]}}
 function affine(F,h){const V=[...new Set(F.flatMap(f=>f.s))].sort((a,b)=>a-b),idx=new Map(V.map((v,i)=>[v,i])),A=pins(h),basis=new Map();let tests=0,xors=0,eqs=0;function insert(row,b){eqs++;while(row){let j=row.toString(2).length-1;if(!basis.has(j)){basis.set(j,[row,b]);return true}let [r,t]=basis.get(j);row^=r;b^=t;xors++}return !b}for(let [v,b] of A)if(idx.has(v)&&!insert(1n<<BigInt(idx.get(v)),b))return{bad:true,tests,xors,eqs};for(const f of F){let rows=f.a.filter(t=>f.s.every((v,j)=>!A.has(v)||A.get(v)===(t>>j&1)));if(!rows.length)return{bad:true,tests,xors,eqs};for(let k=1;k<2**f.s.length;k++){let par=x=>{let a=0;while(x){a^=1;x&=x-1}return a};let b=par(k&rows[0]);let same=rows.every(t=>{tests++;return par(k&t)===b});if(same){let mask=0n;f.s.forEach((v,j)=>{if(k>>j&1)mask|=1n<<BigInt(idx.get(v))});if(!insert(mask,b))return{bad:true,tests,xors,eqs,rank:basis.size}}}}return{bad:false,tests,xors,eqs,rank:basis.size}}
 function flow(h){let A=pins([ -g.g,...h ]),bs=[],root=new Map(),scans=0;for(let v=0;v<G.types.length;v++)if(G.types[v]==="B"){let counts=new Map();for(let j=0;j<4;j++){let i=4*v+j,r=q.R[i]+1,s=q.Q[i];if(!counts.has(r))counts.set(r,[0,0]);counts.get(r)[s]++}bs.push([v,counts]);for(let [r,c] of counts){if(!root.has(r))root.set(r,[0,0]);root.get(r)[0]+=c[0];root.get(r)[1]+=c[1]}}let roots=[...root.keys()],rr=new Map(roots.map((v,i)=>[v,i+1])),sink=1+roots.length+bs.length,adj=Array.from({length:sink+1},()=>[]);function edge(a,b,c){let e=[b,c,adj[b].length],f=[a,0,adj[a].length];adj[a].push(e);adj[b].push(f)}function max(r,c){return A.has(r)?c[1-A.get(r)]:Math.max(...c)}for(let r of roots)edge(0,rr.get(r),max(r,root.get(r)));bs.forEach(([v,counts],j)=>{let b=1+roots.length+j;edge(b,sink,2);for(let [r,c] of counts)edge(rr.get(r),b,max(r,c))});let value=0;while(true){let level=new Int32Array(sink+1).fill(-1),queue=[0];level[0]=0;for(let i=0;i<queue.length;i++)for(let e of adj[queue[i]]){scans++;if(e[1]>0&&level[e[0]]<0){level[e[0]]=level[queue[i]]+1;queue.push(e[0])}}if(level[sink]<0)break;let it=new Int32Array(sink+1);function dfs(v,f){if(v===sink)return f;for(;it[v]<adj[v].length;it[v]++){let e=adj[v][it[v]];scans++;if(e[1]&&level[e[0]]===level[v]+1){let x=dfs(e[0],Math.min(f,e[1]));if(x){e[1]-=x;adj[e[0]][e[2]][1]+=x;return x}}}return 0}let z;while(z=dfs(0,1e9))value+=z}return{bad:value<2*bs.length,value,demand:2*bs.length,scans}}
 function sep(F,h){let A=pins(h),F1=F.map(f=>{let s=f.s.filter(v=>!A.has(v)),a=[];for(let t of f.a)if(f.s.every((v,j)=>!A.has(v)||A.get(v)===(t>>j&1))){let z=s.reduce((z,v,j)=>z|((t>>f.s.indexOf(v)&1)<<j),0);if(!a.includes(z))a.push(z)}return{s,a}});if(F1.some(f=>!f.a.length))return{bad:true,pivots:0,scans:0,rows:0};let z=project(F1);return{bad:z.F.some(f=>!f.a.length),pivots:z.trace.length,scans:z.scans,rows:z.rows}}
 if(peerPins==="EARLY_ONLY")return {occupancy:occupancy(g.F,[]),affine:affine(g.F,[]),flow:flow([]),unit:up(clauses(g.F),[],{visits:0},1e7).A.size};
 const early={occupancy:occupancy(g.F,[]),affine:affine(g.F,[]),flow:flow([]),unit:up(clauses(g.F),[],{visits:0},1e7).A.size};delete early.occupancy.assign;
 const lanes=[],local=[],rejects=[];
 for(const h of guards){let O=occupancy(p.F,h),A=affine(p.F,h),M=flow(h),S=sep(p.F,h),counter={visits:0},D=up(C,h,counter,1e7);delete O.assign;let row={h,occupancy:O,affine:A,flow:M,separator:S,dag:{bad:D.bad,forced:D.A.size-h.length,visits:counter.visits}};lanes.push(row);if([O,A,M,S,D].some(x=>x.bad)){let c=canon(h.map(x=>-x));try{let r=replay(C,[c]);local.push({c,check:r.visits})}catch(e){rejects.push({c,reason:"not independently RUP; retained as unimported lead"})}}}
 // Coverage counts for verified local exclusions only. Exact counts on four guard variables.
 let covered=0;for(let t=0;t<16;t++)if(local.some(({c})=>c.every(l=>((t>>top.indexOf(Math.abs(l)))&1)!==+(l>0))))covered++;
 // Independent replay of a limited peer prefix; do not import complete proof.
 let peer=L.importPrefix(C.concat(local.map(x=>x.c)),seedClauses),X=C.concat(local.map(x=>x.c),peer.good);
 let cl={visits:0},closed=up(X,[],cl,1e7);
 function feedback(base,w,mode,limit=2000){
  let F=base.map(c=>canon(c)),seen=new Set(F.map(c=>c.join(","))),T=[],pairs=0,scoreVisits=0,flips=0,checks=0,peakLits=F.reduce((a,c)=>a+c.length,0),start=Date.now(),found=false,ties=0,residueOps=0,changed=[],queuePeak=0;
  let V=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b);let vindex=new Map(V.map((v,i)=>[v,i]));let a=V.map(()=>0);
  function score(f,b){let n=0;for(let l of f){scoreVisits++;if(b[vindex.get(Math.abs(l))]===+(l>0))n++}return n}
  let counts0=F.map(c=>score(c,a)),counts1=F.map(c=>score(c,V.map(()=>1)));let init=[counts0.filter(x=>!x).length,counts1.filter(x=>!x).length];if(init[1]<init[0])a.fill(1);
  function fields(c,flip=-1){let k=0,s=0;for(let l of c){scoreVisits++;let j=vindex.get(Math.abs(l)),bit=a[j]^(j===flip?1:0);if(bit===+(l>0)){k++;s+=Math.sign(l)}}if(mode==="residue")residueOps+=2;return [k,k%3,(s%3+3)%3]}
  function improve(){for(let iter=0;iter<100;iter++){
   let fs=F.map(c=>fields(c)),delta=new Int32Array(V.length),rd=new Int32Array(V.length),bad=fs.filter(r=>!r[0]).length;
   for(let i=0;i<F.length;i++)for(let l of F[i]){
    scoreVisits++;let j=vindex.get(Math.abs(l)),yes=a[j]===+(l>0),r=fs[i],k=r[0]+(yes?-1:1);
    delta[j]+=+(r[0]===0)-+(k===0);
    if(mode==="residue"){let z=(r[2]+(yes?-1:1)*Math.sign(l)+3)%3;rd[j]+=+(k>0&&z===0)-+(r[0]>0&&r[2]===0);residueOps+=3}
   }
   let best=-1,plain=-1;for(let j=0;j<V.length;j++)if(delta[j]>0){if(plain<0||delta[j]>delta[plain])plain=j;if(best<0||delta[j]>delta[best]||delta[j]===delta[best]&&mode==="residue"&&rd[j]<rd[best])best=j}
   if(best<0)break;if(best!==plain){ties++;changed.push([V[plain],V[best],delta[best],rd[plain],rd[best]])}a[best]^=1;flips++;
   if(F.map(c=>fields(c)).filter(r=>!r[0]).length!==bad-delta[best])throw Error("flip audit");
  }}
  if(mode==="flip"||(mode==="feedback"||mode==="residue"))improve();
  if(mode==="deduce"||(mode==="feedback"||mode==="residue")){
   let queue=[],done=new Set();function push(i,j){for(let l of F[i])if(F[j].includes(-l)&&queue.length<100000){queue.push([i,j,Math.abs(l)]);queuePeak=Math.max(queuePeak,queue.length)}}
   for(let j=0;j<F.length;j++)for(let i=0;i<j;i++)push(i,j);
   if((mode==="feedback"||mode==="residue")){let c=F.map(x=>score(x,a));queue.sort((x,y)=>(c[x[0]]+c[x[1]])-(c[y[0]]+c[y[1]])||x[1]-y[1]||x[0]-y[0]||x[2]-y[2])}
   for(let z=0;z<queue.length&&pairs<limit&&T.length<250;z++){let [i,j,v]=queue[z];pairs++;let u=canon(F[i].concat(F[j]).filter(l=>Math.abs(l)!==v));if(u.length>w||u.some(l=>u.includes(-l))||seen.has(u.join(",")))continue;let check=canon([...F[i].filter(l=>Math.abs(l)!==v),...F[j].filter(l=>Math.abs(l)!==v)]);checks+=F[i].length+F[j].length+u.length;if(check.join(",")!==u.join(",")||!((F[i].includes(v)&&F[j].includes(-v))||(F[i].includes(-v)&&F[j].includes(v))))throw Error("resolution");seen.add(u.join(","));T.push({i,j,v,u});let k=F.length;F.push(u);peakLits+=u.length;if(!u.length){found=true;break}for(let x=0;x<k;x++)push(x,k);if((mode==="feedback"||mode==="residue")&&T.length%32===0)improve()}
   if((mode==="feedback"||mode==="residue"))improve();
  }
  let rr=replay(base,T.map(t=>t.u)),search=found?{status:"UNSAT",nodes:0,visits:0,proof:[]}:tree(F,[],700000),verification=replay(F,search.proof);if(search.status==="UNSAT"&&!found&&!verification.unsat)throw Error("no empty");
  let finalFields=F.map(c=>fields(c)),final=finalFields.filter(x=>!x[0]).length;return{mode,w,init,final,sourceDefects:finalFields.slice(0,base.length).filter(x=>!x[0]).length,signedZero:finalFields.filter(x=>x[0]>0&&x[2]===0).length,ties,changed,residueOps,queuePeak,flips,pairs,learned:T.length,checks,scoreVisits,peakLits,search:{status:search.status,nodes:search.nodes,visits:search.visits},verify:rr.visits+verification.visits,ms:Date.now()-start,trace:T,proof:search.proof}
 }
 const modes=[["baseline",2],["flip",2],["deduce",2],["feedback",2],["residue",2],["deduce",4],["feedback",4],["residue",4]];
 let native=closed.bad?[]:modes.map(([mode,w])=>feedback(X,w,mode)),companion=modes.map(([mode,w])=>feedback(cnf,w,mode));
 let fano=[];for(let line of [[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]]){fano.push(line,line.map(x=>-x))}
 let fanoTest=caseName==="JOINT-24"?[feedback(fano,2,"deduce"),feedback(fano,4,"deduce"),feedback(fano,4,"feedback"),feedback(fano,4,"residue")]:[];
 return{early,top,guards,lanes,local,rejects,covered,peer,closed:{bad:closed.bad,forced:closed.A.size,visits:cl.visits},native,companion,fanoTest}
}



function run(corpus,registry,parents){
 const L={canon,up,tree,replay,project,clauses,importPrefix};let out=[];
 if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("sha");
 for(let i=0;i<2;i++){
  let name=["JOINT-24","RANDOM-3CNF-40"][i],x=corpus.instances.find(x=>x.id===name),reg=registry.instances.find(x=>x.alias==="EB-"+name),start=Date.now(),obj=compile(x),G=obj.network,s=JSON.stringify(G)+"\n",map=JSON.stringify(obj.source_map)+"\n";
  if(sha(s)!==reg.sha256||s.length*8!==reg.N_bits||sha(x.dimacs)!==reg.source_cnf.sha256||x.dimacs.length*8!==reg.source_cnf.N_bits||sha(map)!==reg.source_map_sha256)throw Error("identity");
  let q=quotient(G),g=gauge(q.F),early=study(L,G,q,g,{F:g.F},clauses(g.F),[],"EARLY_ONLY",[],name);
  if(early.occupancy.bad||early.affine.bad||early.flow.bad||early.unit||early.occupancy.forced)throw Error("early forced action");
  let p=project(g.F),C=clauses(p.F),t=tree(C),r=replay(C,t.proof);if(!r.unsat)throw Error("standalone");
  let cnf=x.dimacs.trimEnd().split("\n").slice(1).map(line=>canon(line.trim().split(/\s+/).map(Number).slice(0,-1)));
  let result=study(L,G,q,g,p,C,parents[i].trace.slice(0,4),[],cnf,name);
  let guards=result.guards,good=new Set(result.local.map(x=>canon(x.c.map(l=>-l)).join(","))),counts=[],union=0;
  for(let bits=1;bits<32;bits++){let m=new Map(),n=0,ok=true;for(let j=0;j<5;j++)if(bits>>j&1){n++;let h=guards[j];if(!good.has(canon(h).join(","))){ok=false;break}for(let l of h){let v=Math.abs(l),b=+(l>0);if(m.has(v)&&m.get(v)!==b)ok=false;m.set(v,b)}}let z=ok?2**(4-m.size):0;counts.push(z);union+=(n%2?1:-1)*z}
  if(union!==result.covered)throw Error("coverage mismatch");
  out.push({name,instance:reg,authentication:{native:sha(s),cnf:sha(x.dimacs),map:sha(map)},early,normalization:{arcs:q.arcs,rows:q.rows,carriers:new Set(q.R).size,gauge:g.g},projection:{trace:p.trace,scans:p.scans,rows:p.rows,clauses:C.length,active:new Set(C.flat().map(Math.abs)).size},standalone:{nodes:t.nodes,visits:t.visits,proof:t.proof,replay:r},guardIntersectionCounts:counts,...result,ms:Date.now()-start});
 }
 let gaugeCounts=[];for(let k=1;k<=4;k++){let n=0;for(let t=0;t<2**k;t++){let s=0;for(let j=0;j<k;j++)s+=(t>>j&1)?1:-1;if(s%3===0)n++}gaugeCounts.push([k,n,2**k])}
 return {cases:out,gaugeCounts};
}



function audit(corpus,registry,results){
 const out=[],json=x=>JSON.stringify(x)+"\n",digest=x=>sha(json(x));
 for(let item of results.cases){
  let src=corpus.instances.find(x=>x.id===item.name),reg=registry.instances.find(x=>x.alias==="EB-"+item.name),G=compile(src).network,s=json(G);
  if(sha(s)!==reg.sha256||s.length*8!==reg.N_bits)throw Error("source");
  let q=quotient(G),g=gauge(q.F),F=g.F.map(f=>({s:f.s.slice(),a:f.a.slice()})),checks=0,scans=0;
  // Independently replay the recorded order by joining the bucket as an exhaustive truth table.
  for(let v of item.projection.trace){
   const bucket=F.filter(f=>f.s.includes(v));if(!bucket.length)throw Error("unused pivot");
   const scope=[...new Set(bucket.flatMap(f=>f.s))].sort((a,b)=>a-b);if(scope.length>4)throw Error("scope");
   const rest=scope.filter(w=>w!==v),allowed=new Set();
   for(let t=0;t<2**scope.length;t++){
    let assignment=new Map(scope.map((w,j)=>[w,t>>j&1])),ok=true;
    for(let f of bucket){checks++;let i=f.s.reduce((m,w,j)=>m+(assignment.get(w)<<j),0);if(!f.a.includes(i)){ok=false;break}}
    if(ok)allowed.add(rest.reduce((m,w,j)=>m+(assignment.get(w)<<j),0));
   }
   F=F.filter(f=>!f.s.includes(v));let a=[...allowed].sort((a,b)=>a-b);if(a.length!==2**rest.length)F.push({s:rest,a});
  }
  let C=clauses(F),p=project(g.F);if(json(C)!==json(clauses(p.F))||json(p.trace)!==json(item.projection.trace))throw Error("chart");
  // Regenerate the exact map; existential witness lift reverses the stated bucket trace with the original factors.
  let reconstruction={schema:"EB-PORT-QUOTIENT-AND-BUCKET-ORDER-v1",portMap:Array.from(q.R,(v,i)=>[v+1,q.Q[i]]),gaugeLiteral:-g.g,eliminationOrder:p.trace,liftRule:"Reverse recorded bucket order, reconstruct a pivot bit by testing both values against its original bucket and choosing the least legal value. Restore all ports using root literal and parity."};
  let mapSha=digest(reconstruction),schema="EB-GAUGE-PROJECTED-CNF-v1",guardSchema="EB-PORT-PINS-v1",instanceId=reg.instance_id,guardId=pins=>"GUARD-v1:sha256:"+digest(["PNP-GUARD-v1",instanceId,guardSchema,digest(pins)]),rootPins=[[g.g-1,0]],gid=guardId(rootPins);
  const chart={schema,gauge:g.g,clauses:C,projection:p.trace},resid=(guard,artifact)=>"RESIDUAL-v1:sha256:"+digest(["PNP-RESIDUAL-v1",instanceId,guard,schema,digest(artifact),mapSha]),rid=resid(gid,chart);
  let guardRecords=item.guards.map(h=>{let pins=rootPins.concat(h.map(l=>[Math.abs(l)-1,+(l>0)])).sort((a,b)=>a[0]-b[0]),id=guardId(pins),artifact={...chart,clauses:C.concat(h.map(l=>[l]))};return{h,pins,guard_id:id,residual_id:resid(id,artifact),artifact_sha256:digest(artifact)}});
  let X=C.concat(item.local.map(x=>x.c),item.peer.good),post={...chart,clauses:X},postid=resid(gid,post);
  let check=0;
  for(let row of item.native){let learned=row.trace.map(t=>t.u);check+=replay(X,learned).visits;check+=replay(X.concat(learned),row.proof).visits}
  let rootcheck=replay(C,item.standalone.proof);if(!rootcheck.unsat)throw Error("root proof");
  // A small capped independent randomized guard discovery, no reference advice.
  let vars=[...new Set(C.flat().map(Math.abs))],seed=20261127,random=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0},draws=0,visits=0,newClauses=[],verification=0,seen=new Set();
  for(let k=0;k<32;k++){let a=vars[random()%vars.length],b=vars[random()%vars.length];if(a===b)continue;let h=[random()&1?a:-a,random()&1?b:-b],L={visits:0};draws++;let t=up(C,h,L,1000000);visits+=L.visits;if(t.bad){let c=canon(h.map(l=>-l)),key=c.join(",");if(!seen.has(key)){seen.add(key);verification+=replay(C,[c]).visits;newClauses.push(c)}}}
  let residualClosure={visits:0},closure=up(X,[],residualClosure,1000000);
  out.push({name:item.name,problem_id:"STRICT-EB4-v1",instance_id:instanceId,short_id:reg.short_id,original_N_bits:reg.N_bits,source_pin:{registry:"0c14cdc57925788cf7a451dcd5aa171dce860f2c",corpus:"e315349cd6c1fe3fa696504859f28312f6aab69a",compiler:"21b9d53fb8166c819b24e708656c742cd3c24f10"},root:{guard_id:"EMPTY",residual_id:"ROOT",original_ids:{vertices:[0,G.types.length-1],ports:[0,4*G.types.length-1],edges:[0,G.edges.length-1]}},gauge:{pins:rootPins,guard_id:gid},chart:{artifact_sha256:digest(chart),residual_id:rid,representation_schema:schema,chart},reconstruction_map_sha256:mapSha,guards:guardRecords,post_exchange:{residual_id:postid,artifact_sha256:digest(post),artifact:post,closure_bad:closure.bad,closure_visits:residualClosure.visits},independent_projection_factor_checks:checks,standalone_replay_visits:rootcheck.visits,native_second_replay_visits:check,random:{seed:20261127,draws,visits,verification,clauses:newClauses}});
 }
 return out;
}

const fs=require("node:fs"); console.log(JSON.stringify(audit(...process.argv.slice(2,5).map(p=>JSON.parse(fs.readFileSync(p,"utf8"))))));
