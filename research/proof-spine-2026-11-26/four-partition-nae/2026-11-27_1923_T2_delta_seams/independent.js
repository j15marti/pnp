function sha(s){const K=[],H=[];for(let p=2;K.length<64;p++){let ok=true;for(let d=2;d*d<=p;d++)if(p%d===0){ok=false;break}if(ok){if(H.length<8)H.push((Math.sqrt(p)*4294967296)|0);K.push((Math.cbrt(p)*4294967296)|0)}}const a=Array.from(s,c=>c.charCodeAt(0));if(a.some(x=>x>127))throw Error("nonascii");let bit=a.length*8;a.push(128);while(a.length%64!==56)a.push(0);for(let j=7;j>=0;j--)a.push(Math.floor(bit/2**(j*8))%256);const r=(x,n)=>(x>>>n)|(x<<(32-n));for(let off=0;off<a.length;off+=64){let w=[];for(let i=0;i<16;i++)w.push((a[off+4*i]<<24)|(a[off+4*i+1]<<16)|(a[off+4*i+2]<<8)|a[off+4*i+3]);for(let i=16;i<64;i++){let x=w[i-15],y=w[i-2];w.push((w[i-16]+(r(x,7)^r(x,18)^(x>>>3))+w[i-7]+(r(y,17)^r(y,19)^(y>>>10)))|0)}let [A,B,C,D,E,F,G,J]=H;for(let i=0;i<64;i++){let t=(J+(r(E,6)^r(E,11)^r(E,25))+((E&F)^(~E&G))+K[i]+w[i])|0,u=((r(A,2)^r(A,13)^r(A,22))+((A&B)^(A&C)^(B&C)))|0;[A,B,C,D,E,F,G,J]=[(t+u)|0,A,B,C,(D+t)|0,E,F,G]}[A,B,C,D,E,F,G,J].forEach((x,i)=>H[i]=(H[i]+x)|0)}return H.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("")}
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


function independent(q,inst,entry,compile,sha,isNative){
const canon=x=>JSON.stringify(x)+"\n",sort=a=>[...new Set(a)].sort((a,b)=>a-b),eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
let n=0,build=0,projection=0,upReads=0,sourceMapHash=null,sourceHash=null,chartHash=null,guardChecks=0,deltaChecks=0,rootReplays=[],crossChecks=0;
function propagate(C,g){let a=new Map(g);while(true){let ch=false;for(let j=C.length-1;j>=0;j--){let c=C[j],s=false,un=[];for(let l of c){upReads++;if(a.get(Math.abs(l))===+(l>0)){s=true;break}if(!a.has(Math.abs(l)))un.push(l)}if(s)continue;if(un.length===0)return {bad:true,a};if(un.length===1){a.set(Math.abs(un[0]),+(un[0]>0));ch=true}}if(!ch)return {bad:false,a}}}
let C;
if(isNative){
 const G=compile(inst),net=G.network,bytes=canon(net);sourceHash=sha(bytes);sourceMapHash=sha(canon(G.source_map));if(sourceHash!==entry.sha256||bytes.length*8!==entry.N_bits||sourceMapHash!==entry.source_map_sha256)throw Error("native auth");
 // Independently traverse parity edges by graph adjacency, rather than disjoint-set operations.
 let P=4*net.types.length,adj=Array.from({length:P},()=>[]);function add(a,b,s){adj[a].push([b,s]);adj[b].push([a,s]);build++}
 for(let [a,b,s] of net.edges)add(a,b,s);net.types.forEach((t,v)=>{if(t==="E")for(let j=1;j<4;j++)add(4*v,4*v+j,0)});
 let map=Array(P);for(let i=0;i<P;i++)if(!map[i]){map[i]=[i,0];let queue=[i];for(let k=0;k<queue.length;k++){let x=queue[k];for(let [y,s] of adj[x]){build++;let b=map[x][1]^s;if(map[y]){if(map[y][0]!==i||map[y][1]!==b)throw Error("bad parity")}else{map[y]=[i,b];queue.push(y)}}}}
 if(sha(canon(map))!==q.mapHash)throw Error("map mismatch");
 let anchor=map[10][0]+1;if(anchor!==q.gauge||map[10][1])throw Error("gauge");let F=new Map();
 net.types.forEach((t,v)=>{if(t!=="B")return;let a=sort([0,1,2,3].map(j=>map[4*v+j][0]+1)),r=[];for(let m=0;m<2**a.length;m++){build++;let k=0;for(let j=0;j<4;j++){let [x,b]=map[4*v+j];k+=((m>>a.indexOf(x+1))&1)^b}if(k===2)r.push(m)}let k=JSON.stringify([a,r]);if(F.has(k))F.get(k).owners.push(v);else F.set(k,{v:a,r,owners:[v]})});
 function restrict(f,x,b){let j=f.v.indexOf(x);if(j<0)return f;let v=f.v.filter(y=>y!==x),r=f.r.filter(m=>((m>>j)&1)===b).map(m=>(m&((1<<j)-1))|((m>>(j+1))<<j));return {v,r:sort(r),owners:f.owners}}
 function toC(F){return F.flatMap(f=>Array.from({length:2**f.v.length},(_,m)=>m).filter(m=>!f.r.includes(m)).map(m=>f.v.map((x,j)=>(m>>j)&1?-x:x)))}
 let factors=[...F.values()].map(f=>restrict(f,anchor,0));let early=propagate(toC(factors),[]);if(early.bad||!eq([...early.a],q.before.early))throw Error("early");for(let [x,b] of early.a)factors=factors.map(f=>restrict(f,x,b));
 for(let st of q.projection){let B=factors.filter(f=>f.v.includes(st.x));if(!eq(B,st.parents))throw Error("incomplete bucket");let v=sort(B.flatMap(f=>f.v)).filter(x=>x!==st.x),r=[],witness=[];for(let m=0;m<2**v.length;m++)for(let b of [0,1]){projection++;let a=new Map(v.map((x,j)=>[x,(m>>j)&1]));a.set(st.x,b);if(B.every(f=>f.r.includes(f.v.reduce((z,x,j)=>z|(a.get(x)<<j),0)))){r.push(m);witness.push([m,b])}}let f={v,r:sort(r),owners:sort(B.flatMap(z=>z.owners))};if(!eq(f,st.out)||!eq(witness,st.witness))throw Error("projection");factors=factors.filter(f=>!f.v.includes(st.x));if(f.r.length!==2**v.length)factors.push(f)}
 if(!eq(factors,q.chart))throw Error("chart");C=toC(factors);chartHash=sha(canon(C));if(chartHash!==q.chartHash)throw Error("chart hash");
}else{sourceHash=sha(inst.dimacs);if(sourceHash!==entry.source_cnf.sha256||inst.dimacs.length*8!==entry.source_cnf.N_bits)throw Error("CNF auth");C=inst.dimacs.trimEnd().split("\n").slice(1).map(x=>x.split(/\s+/).map(Number).slice(0,-1))}
let e=q.experiment,early=propagate(C,[]);if(early.bad)throw Error("root");C=C.filter(c=>!c.some(l=>early.a.get(Math.abs(l))===+(l>0))).map(c=>c.filter(l=>!early.a.has(Math.abs(l))));
function row(c,a){let k=0,s=0;for(let l of c){deltaChecks++;if(a.get(Math.abs(l))===+(l>0)){k++;s+=l>0?1:-1}}return [k,k%3,(s%3+3)%3]}
function E(a){return C.reduce((s,c)=>s+ +(row(c,a)[0]===0),0)}
for(let r of e.records){let a=new Map(r.base),old=E(a),ind=0,joint=new Map(a);for(let d of r.deltas){let b=new Map(a);for(let x of d){b.set(x,1-b.get(x));joint.set(x,1-joint.get(x))}ind+=E(b)-old}let value=E(joint);if(old!==r.e||ind!==r.ind||value!==r.ef||old+ind+r.correction!==value)throw Error("delta record");}
for(let t of Object.values(e.trials))for(let x of t.trials){let v=propagate(C,x.g);guardChecks++;if(v.bad!==x.bad)throw Error("guard outcomes")}
let proven=new Set(e.trials.adaptive.trials.filter(x=>x.bad).map(x=>sort(x.g.map(([v,b])=>b?-v:v)).join(",")));for(let i of e.imported){let u=propagate(C,[i.guard]);guardChecks++;if(u.bad&&!i.refused)proven.add(sort(i.c).join(","));else if(!i.refused)throw Error("peer replay")}
for(let c of e.learned)if(!proven.has(sort(c).join(",")))throw Error("unproved learned");
function replay(C,g,t){let u=propagate(C,g);if(u.bad)return true;if(t[0]!=="B")return false;let x=t[1];if(u.a.has(x))return replay(C,[...u.a],t[2+u.a.get(x)]);return replay(C,[...u.a,[x,0]],t[2])&&replay(C,[...u.a,[x,1]],t[3])}
for(let [name,F,T] of [["base",C,e.base.tree],["hybrid",[...C,...e.learned],e.hybrid.tree],["stochasticOnly",[...C,...e.learned.filter(c=>!e.imported.some(i=>eq(i.c,c)))],null]]){if(!T)continue;let before=upReads;if(!replay(F,[],T))throw Error("tree");rootReplays.push({name,reads:upReads-before})}
return {sourceHash,sourceMapHash,chartHash,build,projection,upReads,deltaChecks,guardChecks,rootReplays,ok:true};
}
const fs=require('node:fs');let q=JSON.parse(fs.readFileSync(process.argv[2],'utf8')),b=JSON.parse(fs.readFileSync(process.argv[3],'utf8')),r=JSON.parse(fs.readFileSync(process.argv[4],'utf8')),id=process.argv[5],e=r.instances.find(x=>x.alias==='EB-'+id);console.log(JSON.stringify(independent(q,b.instances.find(x=>x.id===id),e,compile,sha,q.meta.problem_id==='STRICT-EB4-v1'),null,2));
