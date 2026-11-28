// Node.js 20+: node gauge.js benchmarks.json registry.json certificate.json
function sha(s){const K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2],H=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19],n=s.length,L=Math.ceil((n+9)/64)*64,b=new Uint8Array(L),w=new Uint32Array(64);for(let i=0;i<n;i++){let v=s.charCodeAt(i);if(v>127)throw Error("nonASCII");b[i]=v}b[n]=128;let bits=n*8;for(let i=0;i<8;i++){b[L-1-i]=bits%256;bits=Math.floor(bits/256)}const ro=(x,k)=>(x>>>k)|(x<< (32-k));for(let p=0;p<L;p+=64){for(let i=0;i<16;i++){let t=p+4*i;w[i]=(b[t]<<24)|(b[t+1]<<16)|(b[t+2]<<8)|b[t+3]}for(let i=16;i<64;i++){let a=w[i-15],c=w[i-2];w[i]=w[i-16]+(ro(a,7)^ro(a,18)^(a>>>3))+w[i-7]+(ro(c,17)^ro(c,19)^(c>>>10))}let [a,c,d,e,f,g,h,j]=H;for(let i=0;i<64;i++){let t=(j+(ro(f,6)^ro(f,11)^ro(f,25))+((f&g)^(~f&h))+K[i]+w[i])|0,u=((ro(a,2)^ro(a,13)^ro(a,22))+((a&c)^(a&d)^(c&d)))|0;j=h;h=g;g=f;f=(e+t)|0;e=d;d=c;c=a;a=(t+u)|0}for(let i=0;i<8;i++)H[i]=(H[i]+[a,c,d,e,f,g,h,j][i])>>>0}return H.map(x=>x.toString(16).padStart(8,"0")).join("")}


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




// Source-only factor construction and exact bounded pair fusion.
// Parent factor indices refer to deterministic chart or source clause order.
function cf(c){let s=[...new Set(c.map(Math.abs))].sort((a,b)=>a-b);return{s,a:Array.from({length:2**s.length},(_,t)=>t).filter(t=>c.some(l=>((t>>s.indexOf(Math.abs(l)))&1)===+(l>0)))}}
function fuse(F,C,mode,cap=2000){
 let stats={pairTests:0,overlapPairs:0,skips:0,rows:0,projectionRows:0,polyChecks:0,replayRows:0,admitted:0,duplicates:0,peakUnion:0,peakStoredLits:0},T=[],seen=new Set(C.map(c=>canon(c).join(","))),clock=Date.now();
 let by=new Map(),pairs=new Set();for(let i=0;i<F.length;i++)for(let v of F[i].s){if(!by.has(v))by.set(v,[]);by.get(v).push(i)}
 // Avoid arbitrary subset enumeration; each pair encountered through shared variable.
 for(let ids of by.values())for(let a=0;a<ids.length;a++)for(let b=a+1;b<ids.length;b++) {stats.pairTests++;if(stats.pairTests>500000)throw Error("incidence cap");pairs.add(ids[a]+","+ids[b])}
 let work=0;
 function val(f,u,t){return f.a.includes(f.s.reduce((m,v,j)=>m|(((t>>u.indexOf(v))&1)<<j),0))}
 function anf(a,k){a=a.slice();for(let j=0;j<k;j++)for(let i=0;i<a.length;i++)if(i>>j&1)a[i]^=a[i^(1<<j)];return a}
 function evalp(p,t){let b=0;for(let i=0;i<p.length;i++)if(p[i]&&(i&t)===i)b^=1;return b}
 for(let key of pairs){let [i,j]=key.split(",").map(Number),a=F[i],b=F[j],same=a.s.join(",")===b.s.join(",");
  if(mode==="same"?!same:same)continue;if(work++>=cap||T.length>=200)break;
  let u=[...new Set(a.s.concat(b.s))].sort((a,b)=>a-b);if(u.length>6){stats.skips++;continue}stats.overlapPairs++;stats.peakUnion=Math.max(stats.peakUnion,u.length);
  let allowed=[],va=[],vb=[];for(let t=0;t<2**u.length;t++){stats.rows++;let x=val(a,u,t),y=val(b,u,t);va.push(+!x);vb.push(+!y);if(x&&y)allowed.push(t)}
  // Obtain all width <=3 absent projected words, excluding facts implied by either parent alone.
  for(let mask=1;mask<2**u.length&&T.length<200;mask++){
   let pos=u.map((_,j)=>j).filter(j=>mask>>j&1);if(pos.length>3)continue;
   let proj=t=>pos.reduce((m,j,k)=>m|((t>>j&1)<<k),0),p=new Set(allowed.map(proj)),pa=new Set(),pb=new Set();
   for(let t=0;t<va.length;t++){stats.projectionRows++;if(!va[t])pa.add(proj(t));if(!vb[t])pb.add(proj(t))}
   for(let z=0;z<2**pos.length&&T.length<200;z++)if(!p.has(z)&&pa.has(z)&&pb.has(z)){
    let c=canon(pos.map((j,k)=>z>>k&1?-u[j]:u[j])),ck=c.join(",");
    if(seen.has(ck)||c.some((_,k)=>seen.has(c.filter((_,j)=>j!==k).join(",")))){stats.duplicates++;continue}
    // Independent algebra replay: h = h*f + h*g + h*f*g in the Boolean ring.
    // Check coefficient equality by Mobius transform; independently check all parent rows via explicit CNF.
    let h=Array.from({length:va.length},(_,t)=>+c.every(l=>((t>>u.indexOf(Math.abs(l)))&1)!==+(l>0)));
    let x=h.map((v,t)=>v&va[t]),y=h.map((v,t)=>v&vb[t]),zv=h.map((v,t)=>v&va[t]&vb[t]);
    let H=anf(h,u.length),X=anf(x,u.length),Y=anf(y,u.length),Z=anf(zv,u.length);
    for(let k=0;k<H.length;k++){stats.polyChecks++;if(H[k]!== (X[k]^Y[k]^Z[k]))throw Error("polynomial check")}
    // independent truth-table verification using different lookup: existential extension over union words
    for(let t=0;t<va.length;t++){stats.replayRows++;let sat=f=>f.a.some(r=>f.s.every((v,k)=>(r>>k&1)===(t>>u.indexOf(v)&1)));if(h[t]&&sat(a)&&sat(b))throw Error("join check")}
    seen.add(ck);T.push({i,j,u,c});stats.admitted++;stats.peakStoredLits+=c.length;
   }
  }
 }
 return {mode,stats,trace:T,ms:Date.now()-clock};
}
// Degree-2 local vanishing basis and global elimination. Rows are exact GF(2) identities.
// A row is a set of squarefree monomials, each monomial comma-separated sorted IDs.
function algebra(F){
 let started=Date.now(),generators=[],basis=new Map(),ops=0,localRows=0,localTests=0,contradiction=null,lin=[],multiscope=0,peakTerms=0,monoSet=new Set();
 const cmp=(a,b)=>b.split(",").filter(Boolean).length-a.split(",").filter(Boolean).length||a.localeCompare(b);
 const xor=(a,b)=>{for(let t of b){ops++;if(a.has(t))a.delete(t);else a.add(t)}};
 for(let i=0;i<F.length;i++){let {s,a}=F[i];if(s.length>4)continue;let m=[0];for(let x=1;x<2**s.length;x++)if(x.toString(2).replace(/0/g,"").length<=2)m.push(x);
  // local row space of evaluations and nullspace via enumeration of free columns.
  let E=new Map();for(let t of a){let r=0;for(let k=0;k<m.length;k++){localTests++;if((t&m[k])===m[k])r|=1<<k}while(r){let k=31-Math.clz32(r);if(E.has(k))r^=E.get(k);else{E.set(k,r);break}}}
  for(let free=0;free<m.length;free++)if(!E.has(free)){let w=1<<free;
   for(let k=0;k<m.length;k++)if(E.has(k)){let z=E.get(k)&w,p=0;while(z){p^=1;z&=z-1}if(p)w|=1<<k}
   let mons=m.filter((_,k)=>w>>k&1);for(let t of a){localRows++;let p=0;for(let mm of mons)p^=+((t&mm)===mm);if(p)throw Error("local nullspace")}
   let terms=mons.map(mm=>s.filter((_,j)=>mm>>j&1).join(","));let id=generators.length;generators.push({factor:i,terms});for(let t of terms)monoSet.add(t);
   let r=new Set(terms),p=new Set([id]);while(r.size){let k=[...r].sort(cmp)[0];if(!basis.has(k)){basis.set(k,{r,p});peakTerms=Math.max(peakTerms,r.size);break}xor(r,basis.get(k).r);xor(p,basis.get(k).p)}
  }
 }
 for(let [k,{r,p}] of basis){let terms=[...r],degree=Math.max(...terms.map(t=>t?t.split(",").length:0));if(degree<=1){let owners=[...new Set([...p].map(j=>generators[j].factor))];if(owners.length>1)multiscope++;let z=new Set();for(let j of p)xor(z,generators[j].terms);if(z.size!==r.size||terms.some(t=>!z.has(t)))throw Error("global row replay");let info={terms,parents:[...p],factors:owners};if(degree===0)contradiction=info;else lin.push(info)}}
 return {generators:generators.length,basis:basis.size,monomials:monoSet.size,linear:lin.length,multiscopeLinear:multiscope,unary:lin.filter(x=>x.terms.filter(Boolean).length===1).length,contradiction,localRows,localTests,xorOps:ops,peakTerms,ms:Date.now()-started};
}


function orbit(F, guard=[], ordered=[]) {
 const start=Date.now(),V=[...new Set(F.flatMap(f=>f.s))].sort((a,b)=>a-b), idx=new Map(V.map((v,i)=>[v,i])), B=new Map();let tests=0,xors=0,checks=0,eqs=0;
 const par=x=>{let z=0;while(x){z^=1;x&=x-1}return z};
 const parity=x=>{let z=0;while(x){z^=1;x&=x-1n}return z};
 function insert(x){eqs++;while(x){let p=x.toString(2).length-1;if(B.has(p)){x^=B.get(p);xors++}else{B.set(p,x);return}}}
 let local=[];
 for(const f of F){const H=[];for(let h=0;h<2**f.s.length;h++){if(f.a.every(t=>{tests++;return f.a.includes(t^h)}))H.push(h)}
  local.push(H.length);for(let l=1;l<2**f.s.length;l++)if(H.every(h=>{tests++;return par(l&h)===0})){let row=0n;f.s.forEach((v,i)=>{if(l>>i&1)row|=1n<<BigInt(idx.get(v))});insert(row)}}
 for(let v of guard)if(idx.has(v))insert(1n<<BigInt(idx.get(v)));
 let basis=[];for(let i=0;i<V.length;i++)if(!B.has(i)){let x=1n<<BigInt(i);for(let j=0;j<V.length;j++)if(B.has(j)&&parity(x&B.get(j)))x^=1n<<BigInt(j);basis.push(x)}
 for(const x of basis){for(const f of F){let h=f.s.reduce((m,v,i)=>m|Number((x>>BigInt(idx.get(v)))&1n)<<i,0);for(const t of f.a){checks++;if(!f.a.includes(t^h))throw Error("translation replay")}}for(const v of guard)if(idx.has(v)&&(x>>BigInt(idx.get(v))&1n))throw Error("guard replay")}
 const order=[...new Set(ordered.concat(V))].filter(v=>idx.has(v)),pivots=[];
 for(const v of order){let bit=1n<<BigInt(idx.get(v)),j=basis.findIndex((x,i)=>i>=pivots.length&&(x&bit));if(j<0)continue;let k=pivots.length;[basis[j],basis[k]]=[basis[k],basis[j]];for(let i=0;i<basis.length;i++)if(i!==k&&(basis[i]&bit)){basis[i]^=basis[k];xors++}pivots.push(v)}
 if(pivots.length!==basis.length)throw Error("rank");
 const D=basis.map(x=>V.filter((v,i)=>x>>BigInt(i)&1n));
 for(let i=0;i<D.length;i++)for(let j=0;j<pivots.length;j++)if(D[i].includes(pivots[j])!==(i===j))throw Error("systematic basis");
 return{variables:V.length,rank:B.size,dimension:basis.length,pivots,dictionary:D,localStabilizerSizes:[...new Set(local)],tests,xors,checks,eqs,ms:Date.now()-start}
}
function restrict(F,pins){return F.map(f=>{let s=f.s.filter(v=>!pins.has(v)),a=[];for(let t of f.a)if(f.s.every((v,j)=>!pins.has(v)||pins.get(v)===(t>>j&1)))a.push(s.reduce((m,v,j)=>m|((t>>f.s.indexOf(v)&1)<<j),0));return{s,a:[...new Set(a)].sort((a,b)=>a-b)}})}
function trial(F,seeds=[]){let C=clauses(F),t=tree(C,seeds,700000),r=replay(C.concat(seeds),t.proof);if(t.status==="UNSAT"&&!r.unsat)throw Error("empty");return{status:t.status,nodes:t.nodes,visits:t.visits,check:r.visits,proof:t.proof}}
function early(F){let a=new Map(),visits=0,change=true;while(change){change=false;for(let f of F){let rows=f.a.filter(t=>{visits++;return f.s.every((v,j)=>!a.has(v)||a.get(v)===(t>>j&1))});if(!rows.length)return{bad:true,visits,pins:[...a]};for(let j=0;j<f.s.length;j++)if(!a.has(f.s[j])&&rows.every(t=>(t>>j&1)===(rows[0]>>j&1))){a.set(f.s[j],rows[0]>>j&1);change=true}}}return{bad:false,visits,pins:[...a]}}
function runOrbit(corpus,registry,peerRaw,compilePinned){
 if(sha("")!=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"||sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("SHA");
 const L={canon,up,tree,replay,project,clauses,importPrefix},out=[];
 for(let i=0;i<2;i++){
 let start=Date.now(),name=["JOINT-24","RANDOM-3CNF-40"][i],x=corpus.instances.find(x=>x.id===name),reg=registry.instances.find(x=>x.alias==="EB-"+name),obj=compilePinned(x),G=obj.network,s=JSON.stringify(G)+"\n";
 let nativeHash=sha(s),cnfHash=sha(x.dimacs),mapHash=sha(JSON.stringify(obj.source_map)+"\n");
 if(nativeHash!==reg.sha256||s.length*8!==reg.N_bits||cnfHash!==reg.source_cnf.sha256||x.dimacs.length*8!==reg.source_cnf.N_bits||mapHash!==reg.source_map_sha256)throw Error("identity");
 let q=quotient(G),e=early(q.F);if(e.bad||e.pins.length)throw Error("unexpected early reduction");
 let g=gauge(q.F),earlyOther=study(L,G,q,g,{F:g.F},clauses(g.F),[],"EARLY_ONLY",[],name);
 let o=orbit(q.F,[],[g.g]),guardOrbit=orbit(q.F,[g.g],[g.g]),compressed=restrict(q.F,new Map(o.pivots.map(v=>[v,0])));
 if(o.pivots.length!==1||o.pivots[0]!==g.g||JSON.stringify(compressed)!==JSON.stringify(g.F))throw Error("unexpected orbit");
 let b=project(q.F),p=project(compressed),C=clauses(p.F),src=x.dimacs.trimEnd().split("\n").slice(1).map(l=>canon(l.trim().split(/\s+/).map(Number).slice(0,-1))),sf=src.map(cf);
 let base=trial(b.F),own=trial(p.F),srcBase=trial(sf),srcOrbit=orbit(sf);
 let nativeFusion=fuse(p.F,C,"cross",300),same=fuse(p.F,C,"same",300),hybrid=trial(p.F,nativeFusion.trace.map(t=>t.c));
 // Blind phase finishes here; peer contents only now parsed.
 let raw=peerRaw[i],peer=JSON.parse(raw),expected=["75fb830677e51f8bd73b3e77510d7a1eae057a269aae4e333f30f654b2ee7c4b","a1af0f81183d9681db016bbc2381e77273c04da3e16f93e7eb34bbc4de48dda9"][i];
 if(sha(raw)!==expected||peer.instance_id!==reg.instance_id||peer.gauge!==g.g)throw Error("peer ID");
 let orderMatch=JSON.stringify(peer.trace.map(t=>t.v))===JSON.stringify(p.trace);
 let prefix=peer.proof.slice(0,3).map(t=>t.clause),ablation=[];
 for(let mask=0;mask<8;mask++){let seed=prefix.filter((_,j)=>mask>>j&1),checked=importPrefix(C,seed);if(checked.good.length!==seed.length){ablation.push({mask,status:"rejected",checked});continue}ablation.push({mask,importChecks:checked.visits,...trial(p.F,seed)})}
 let localPeer=importPrefix(C,prefix),fullReplay=replay(C,peer.proof.map(t=>t.clause));
 let common=study(L,G,q,g,p,C,localPeer.good,[],src,name);
 let guards=common.guards,intersections=[],union=0;
 for(let mask=1;mask<32;mask++){let M=new Map(),ok=true,n=0;for(let j=0;j<5;j++)if(mask>>j&1){n++;let h=guards[j];if(!common.local.some(t=>canon(t.c.map(l=>-l)).join(",")===canon(h).join(","))){ok=false;break}for(let l of h){if(M.has(Math.abs(l))&&M.get(Math.abs(l))!==+(l>0))ok=false;M.set(Math.abs(l),+(l>0))}}let count=ok?2**(4-M.size):0;intersections.push(count);union+=(n%2?1:-1)*count}
 if(union!==common.covered)throw Error("coverage");
 let map={R:Array.from(q.R),Q:Array.from(q.Q),orbit:o.dictionary,pivots:o.pivots,order:p.trace},chart={factors:p.F,clauses:C},guardArtifact=JSON.stringify([[g.g-1,0]])+"\n",gid="GUARD-v1:sha256:"+sha(JSON.stringify(["PNP-GUARD-v1",reg.instance_id,"EB-PORT-PINS-v1",sha(guardArtifact)])+"\n"),rid="RESIDUAL-v1:sha256:"+sha(JSON.stringify(["PNP-RESIDUAL-v1",reg.instance_id,gid,"T3-ORBIT-CHART-v1",sha(JSON.stringify(chart)+"\n"),sha(JSON.stringify(map)+"\n")])+"\n");
 out.push({name,reg,authentication:{nativeHash,cnfHash,mapHash},early:e,earlyOther,normalization:{arcs:q.arcs,rows:q.rows,carriers:new Set(q.R).size},orbit:o,guardOrbit,srcOrbit,projection:{baseline:{vars:new Set(b.F.flatMap(f=>f.s)).size,trace:b.trace,rows:b.rows,scans:b.scans},compressed:{vars:new Set(p.F.flatMap(f=>f.s)).size,trace:p.trace,rows:p.rows,scans:p.scans}},base,own,srcBase,hybrid,nativeFusion,same,peer:{id:expected,orderMatch,prefix,fullReplay,localPeer,ablation},common,intersections,union,chart,map,identity:{guardArtifact,gid,rid},ms:Date.now()-start})
 }return out;
}



function traceProject(F,order,owners){
 let scans=0,rows=0,peak=0,Fs=F.map((f,i)=>({...f,owners:owners[i]}));
 for(let v of order){let idx=[];for(let i=0;i<Fs.length;i++){scans+=Fs[i].s.length;if(Fs[i].s.includes(v))idx.push(i)}if(!idx.length)continue;
 let u=[...new Set(idx.flatMap(i=>Fs[i].s))].sort((a,b)=>a-b),s=u.filter(w=>w!==v);if(u.length>4)throw Error("trace scope");let a=[];
 for(let t=0;t<2**s.length;t++)for(let z=0;z<2;z++){rows++;if(idx.every(i=>{const f=Fs[i];return f.a.includes(f.s.reduce((m,w,j)=>m|((w===v?z:(t>>s.indexOf(w)&1))<<j),0))})){a.push(t);break}}
 let own=[...new Set(idx.flatMap(i=>Fs[i].owners))].sort((a,b)=>a-b),D=new Set(idx);Fs=Fs.filter((_,i)=>!D.has(i));if(a.length!==2**s.length)Fs.push({s,a,owners:own});if(!a.length){Fs=[{s,a,owners:own}];break}peak=Math.max(peak,Fs.reduce((sum,f)=>sum+f.owners.length,0))
 }return {Fs,scans,rows,peak};
}
function tracedUP(C,h){let A=new Map(h.map(l=>[l,[]])),visits=0,changed=true;while(changed){changed=false;for(let i=0;i<C.length;i++){let c=C[i].c,free=[],parents=[],sat=false;for(let l of c){visits++;if(A.has(l)){sat=true;break}if(!A.has(-l))free.push(l);else parents.push(...A.get(-l))}if(sat)continue;if(free.length===0)return {bad:true,visits,support:[...new Set(parents.concat(C[i].owners))].sort((a,b)=>a-b)};if(free.length===1&&!A.has(free[0])){A.set(free[0],[...new Set(parents.concat(C[i].owners))]);changed=true}}}return {bad:false,visits,forced:A.size-h.length}}
function fromFactors(F){let M=new Map();for(let f of F)for(let t=0;t<2**f.s.length;t++)if(!f.a.includes(t)){let c=f.s.map((v,j)=>t>>j&1?-v:v);M.set(c.join(","),{c,owners:f.owners})}return [...M.values()]}
function auditExtra(corpus,registry,M,compilePinned){
 let out=[];
 for(let i=0;i<2;i++){
 let name=["JOINT-24","RANDOM-3CNF-40"][i],reg=registry.instances.find(x=>x.alias==="EB-"+name),x=corpus.instances.find(x=>x.id===name),G=compilePinned(x).network,bytes=JSON.stringify(G)+"\n",m=M[i];
 if(sha(bytes)!==reg.sha256||bytes.length*8!==reg.N_bits)throw Error("auth");
 let q=quotient(G),g=gauge(q.F),O=new Map();
 for(let v=0;v<G.types.length;v++)if(G.types[v]==="B"){let p=[0,1,2,3].map(j=>4*v+j),s=[...new Set(p.map(j=>q.R[j]+1))].sort((a,b)=>a-b),a=[];for(let t=0;t<2**s.length;t++)if(p.reduce((sum,j)=>sum+(((t>>s.indexOf(q.R[j]+1))&1)^q.Q[j]),0)===2)a.push(t);O.set(JSON.stringify({s,a}),v)}
 let owners=q.F.map(f=>[O.get(JSON.stringify(f))]);if(owners.some(a=>a[0]===undefined))throw Error("owner");
 let tr=traceProject(g.F,m.projection.compressed.trace,owners),C=fromFactors(tr.Fs);
 if(JSON.stringify(tr.Fs.map(({s,a})=>({s,a})))!==JSON.stringify(m.chart.factors)||JSON.stringify(C.map(x=>x.c))!==JSON.stringify(m.chart.clauses))throw Error("chart mismatch");
 let cores=[];for(let z of m.common.local){let h=z.c.map(l=>-l),res=tracedUP(C,h);if(!res.bad)throw Error("core");
 let ids=new Set(res.support),F=g.F.filter((_,j)=>ids.has(owners[j][0])),Oo=owners.filter(x=>ids.has(x[0])),re=traceProject(F,m.projection.compressed.trace,Oo),rr=tracedUP(fromFactors(re.Fs),h);if(!rr.bad)throw Error("core replay");
 // Lift chart guard to root with relative affine tests x_v xor x_g = b; check both gauges on all support words.
 let tests=0;for(let t=0;t<2**h.length;t++)for(let b=0;b<2;b++){let bits=h.map((_,j)=>(t>>j&1)^b),before=h.every((l,j)=>(t>>j&1)===+(l>0)),after=h.every((l,j)=>(bits[j]^b)===+(l>0));tests++;if(before!==after)throw Error("lift")}
 cores.push({guard:h,originalBalanceVertices:res.support,discovery:res.visits,replay:rr.visits,projectionRows:re.rows,projectionScans:re.scans,rootAffineGuard:h.map(l=>[Math.abs(l)-1,g.g-1,+(l>0)]),liftChecks:tests})
 }
 let vars=[...new Set(C.flatMap(f=>f.c.map(Math.abs)))].sort((a,b)=>a-b),random=[];
 for(let seeded=0;seeded<2;seeded++){let rand=0x74197ab1,hit=0,visits=0,checked=0,replayReads=0,fail=0,guards=[],seen=new Set(),seed=seeded?m.peer.prefix:[],S=C.concat(seed.map(c=>({c,owners:[]})));const rnd=()=>{rand^=rand<<13;rand^=rand>>>17;rand^=rand<<5;return rand>>>0};
 for(let n=0;n<128;n++){let a=vars[rnd()%vars.length],bb=vars[rnd()%vars.length];if(a===bb){fail++;continue}let h=[(rnd()&1)?a:-a,(rnd()&1)?bb:-bb];let k=canon(h).join(",");if(seen.has(k)){fail++;continue}seen.add(k);let p=tracedUP(S,h);visits+=p.visits;if(p.bad){let check=replay(C.map(x=>x.c).concat(seed),[canon(h.map(l=>-l))]);replayReads+=check.visits;hit++;guards.push(h)}checked++}
 random.push({seeded:!!seeded,checked,duplicatesOrSame:fail,hit,visits,replayReads,guards});
 }
 out.push({name,instance_id:reg.instance_id,N:reg.N_bits,identity:m.identity,cores,trace:{scans:tr.scans,rows:tr.rows,peakOwnerEntries:tr.peak},random});
 }return out;
}

const fs=require("node:fs"),[corpus,registry,mJ,mR,compiler]=process.argv.slice(2).map(x=>fs.readFileSync(x,"utf8"));const cp=compiler.slice(compiler.indexOf("function compile("),compiler.indexOf("function auditLocal"));console.log(JSON.stringify(auditExtra(JSON.parse(corpus),JSON.parse(registry),[mJ,mR].map(JSON.parse),new Function(cp+"\nreturn compile")())));
