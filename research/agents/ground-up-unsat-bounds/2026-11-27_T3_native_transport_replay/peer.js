
function sha(s){
 const H=[],K=[];for(let p=2;K.length<64;p++){let prime=true;for(let j=2;j*j<=p;j++)if(p%j===0){prime=false;break}if(prime){if(H.length<8)H.push((Math.sqrt(p)%1*4294967296)|0);K.push((Math.cbrt(p)%1*4294967296)|0)}}
 const a=Array.from(s,c=>c.charCodeAt(0));if(a.some(x=>x>127))throw Error("ASCII required");let n=a.length*8;a.push(128);while(a.length%64!==56)a.push(0);for(let i=7;i>=0;i--)a.push(Math.floor(n/2**(8*i))%256);
 const rr=(x,k)=>(x>>>k)|(x<<(32-k));
 for(let j=0;j<a.length;j+=64){let w=[];for(let i=0;i<16;i++)w[i]=(a[j+4*i]<<24)|(a[j+4*i+1]<<16)|(a[j+4*i+2]<<8)|a[j+4*i+3];
 for(let i=16;i<64;i++){let x=w[i-15],y=w[i-2];w[i]=(w[i-16]+(rr(x,7)^rr(x,18)^(x>>>3))+w[i-7]+(rr(y,17)^rr(y,19)^(y>>>10)))|0}
 let [A,B,C,D,E,F,G,I]=H;
 for(let i=0;i<64;i++){let t=(I+(rr(E,6)^rr(E,11)^rr(E,25))+((E&F)^(~E&G))+K[i]+w[i])|0,u=((rr(A,2)^rr(A,13)^rr(A,22))+((A&B)^(A&C)^(B&C)))|0;[A,B,C,D,E,F,G,I]=[(t+u)|0,A,B,C,(D+t)|0,E,F,G]}
 [A,B,C,D,E,F,G,I].forEach((x,i)=>H[i]=(H[i]+x)|0)}
 return H.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("")
}
const canon=a=>Array.from(new Set(a)).sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const key=a=>a.join(",");
function norm(g){
 let n=g.types.length*4,adj=Array.from({length:n},()=>[]),ports=new Set(),pairs=new Set();
 const link=(a,b,s)=>{adj[a].push([b,s]);adj[b].push([a,s])};
 for(let [a,b,s] of g.edges){let u=a>>2,v=b>>2,k=[Math.min(u,v),Math.max(u,v)].join(",");if(a<0||b<0||a>=n||b>=n||u===v||ports.has(a)||ports.has(b)||pairs.has(k)||!(s===0||s===1))throw Error("edge");ports.add(a);ports.add(b);pairs.add(k);link(a,b,s)}
 if(ports.size!==n)throw Error("ports");
 for(let v=0;v<g.types.length;v++)if(g.types[v]==="E"){for(let j=1;j<4;j++)link(4*v,4*v+j,0)}else if(g.types[v]!=="B")throw Error("type");
 let root=new Int32Array(n),sign=new Int8Array(n),vis=0,components=0;
 for(let p=0;p<n;p++)if(!root[p]){components++;root[p]=p+1;let q=[p];for(let j=0;j<q.length;j++){let a=q[j];for(let [b,s] of adj[a]){vis++;let t=sign[a]^s;if(root[b]){if(sign[b]!==t)throw Error("signed contradiction")}else{root[b]=p+1;sign[b]=t;q.push(b)}}}}
 let C=new Map(),rows=0,deg=new Map();
 for(let v=0;v<g.types.length;v++)if(g.types[v]==="B"){let p=Array.from({length:4},(_,j)=>4*v+j),vs=canon(p.map(j=>root[j]));
 for(let u of vs)deg.set(u,(deg.get(u)||0)+1);
 for(let a=0;a<2**vs.length;a++){rows++;let sum=p.reduce((t,j)=>t+(((a>>vs.indexOf(root[j]))&1)^sign[j]),0);if(sum!==2){let c=vs.map((x,i)=>a>>i&1?-x:x);C.set(key(c),c)}}}
 let gauge=[...deg].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];C.set(String(-gauge),[-gauge]);
 return {C:[...C.values()],gauge,vis,rows,components,root:[...root],sign:[...sign]}
}
function resolve(a,b,v){let c=canon([...a.filter(x=>x!==v),...b.filter(x=>x!==-v)]);return c.some(x=>c.includes(-x))?null:c}
function project(base,cap=16){
 let active=new Map(base.map(c=>[key(c),c])),trace=[],pairs=0,scans=0,peak=active.size;
 for(;;){let inc=new Map();for(let c of active.values())for(let l of c){scans++;let v=Math.abs(l);if(!inc.has(v))inc.set(v,[[],[]]);inc.get(v)[l>0?0:1].push(c)}
 let chosen=null;
 for(let [v,[p,n]] of [...inc].sort((a,b)=>a[1][0].length*a[1][1].length-b[1][0].length*b[1][1].length||a[0]-b[0])){
 if(p.length*n.length>cap)break;let add=new Map(),wide=false;
 for(let a of p)for(let b of n){pairs++;let c=resolve(a,b,v);if(c){if(c.length>8)wide=true;add.set(key(c),c)}}
 if(!wide&&add.size<=p.length+n.length){chosen={v,p,n,add};break}}
 if(!chosen)break;let {v,p,n,add}=chosen;for(let c of [...p,...n])active.delete(key(c));for(let [k,c] of add)active.set(k,c);trace.push(v);peak=Math.max(peak,active.size)
 }
 return {C:[...active.values()],trace,pairs,scans,peak}
}
function replay(base,trace){let A=new Map(base.map(c=>[key(c),c])),pairs=0,scans=0;
 for(let v of trace){let p=[],n=[];for(let c of A.values()){scans++;if(c.includes(v))p.push(c);if(c.includes(-v))n.push(c)}if(!p.length&&!n.length)throw Error("stale");
 for(let c of [...p,...n])A.delete(key(c));
 for(let a of p)for(let b of n){pairs++;let s=new Set([...a,...b]);s.delete(v);s.delete(-v);if([...s].some(x=>s.has(-x)))continue;let c=canon([...s]);A.set(key(c),c)}}
 return {C:[...A.values()],pairs,scans}
}
function up(C,pins,m){let A=new Map(pins);for(;;){let change=false,score=new Map(),all=true;for(let i=0;i<C.length;i++){m.scans++;if(m.scans>m.cap)throw Error("cap");let c=C[i],free=[],sat=false;for(let l of c){m.lits++;let x=A.get(Math.abs(l));if(x===undefined)free.push(l);else if(x===Number(l>0)){sat=true;break}}
 if(sat)continue;all=false;if(!free.length)return {conflict:true};if(free.length===1){A.set(Math.abs(free[0]),Number(free[0]>0));change=true}else for(let l of free)score.set(Math.abs(l),(score.get(Math.abs(l))||0)+1)}
 if(!change)return {A,all,score}}
}
function solve(C,cap=500000){let m={scans:0,lits:0,nodes:0,cap};function visit(pins){m.nodes++;let r=up(C,pins,m);if(r.conflict)return null;if(r.all)throw Error("SAT");let v=[...r.score].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];return [v,visit([...pins,[v,0]]),visit([...pins,[v,1]])]}
 try{return {status:"UNSAT",tree:visit([]),...m}}catch(e){return {status:String(e.message),...m}}}
function check(C,tree){let m={scans:0,lits:0,nodes:0,cap:10000000};function visit(pins,t){m.nodes++;let r=up(C,pins,m);if(t===null){if(!r.conflict)throw Error("false leaf");return}if(r.conflict||r.A.has(t[0]))throw Error("invalid branch");visit([...pins,[t[0],0]],t[1]);visit([...pins,[t[0],1]],t[2])}visit([],tree);return m}
function run(g){let b=norm(g),p=project(b.C),s=solve(p.C);let q=replay(b.C,p.trace);if([...p.C].map(key).sort().join(";")!==q.C.map(key).sort().join(";"))throw Error("projection mismatch");let c=s.status==="UNSAT"?check(q.C,s.tree):null;
 return {gauge:b.gauge,components:b.components,normalizationVisits:b.vis,localWords:b.rows,baseClauses:b.C.length,remainingClauses:p.C.length,remainingVars:new Set(p.C.flat().map(Math.abs)).size,projection:{steps:p.trace.length,pairs:p.pairs,scans:p.scans,peak:p.peak},solve:s,replay:{pairs:q.pairs,scans:q.scans,check:c},trace:p.trace}
}

if(typeof module!=="undefined") module.exports={sha,run,norm,project,solve,check,replay};

function peerReplay(g,b,cert){
 let factors=new Map(),seen=new Set(),rows=0,proj=0,entail=0,scan=0;
 for(let v=0;v<g.types.length;v++)if(g.types[v]==="B"){let p=[0,1,2,3].map(j=>4*v+j),vs=canon(p.map(j=>b.root[j])),ok=[];
 for(let w=0;w<2**vs.length;w++){rows++;if(p.reduce((a,j)=>a+(((w>>vs.indexOf(b.root[j]))&1)^b.sign[j]),0)===2)ok.push(w)}
 let k=JSON.stringify([vs,ok]);if(!seen.has(k)){seen.add(k);factors.set(factors.size,{vs,ok})}}
 for(let t of cert.trace){
 let inc=[...factors].filter(([id,f])=>f.vs.includes(t.v));scan+=factors.size;if(inc.map(x=>x[0]).sort((a,b)=>a-b).join(",")!==t.in.slice().sort((a,b)=>a-b).join(","))throw Error("incomplete bucket");
 let vs=canon(inc.flatMap(([id,f])=>f.vs).filter(x=>x!==t.v)),ok=[];
 if(vs.join(",")!==t.vs.join(","))throw Error("scope");
 for(let w=0;w<2**vs.length;w++){let hit=false;for(let z=0;z<2;z++){proj++;if(inc.every(([id,f])=>f.ok.includes(f.vs.reduce((a,x,i)=>a|((x===t.v?z:(w>>vs.indexOf(x))&1)<<i),0))))hit=true}if(hit)ok.push(w)}
 if(ok.join(",")!==t.ok.join(","))throw Error("projection");
 for(let [id] of inc)factors.delete(id);if(factors.has(t.out))throw Error("duplicate factor");factors.set(t.out,{vs,ok})
 }
 if(cert.gauge!==b.gauge)throw Error("gauge mismatch");
 for(let c of cert.base){if(c.length===1&&c[0]===-cert.gauge)continue;
 if(![...factors.values()].some(f=>c.every(l=>f.vs.includes(Math.abs(l)))&&f.ok.every(w=>{entail++;return c.some(l=>((w>>f.vs.indexOf(Math.abs(l)))&1)===Number(l>0))})))throw Error("base entailment")}
 let db=cert.base.slice(),m={scans:0,lits:0,cap:10000000};
 for(let c of cert.proof){if(!up(db,c.map(l=>[Math.abs(l),Number(l<0)]),m).conflict)throw Error("RUP");db.push(c)}
 if(cert.proof.at(-1).length)throw Error("no empty");
 return {rows,proj,scan,entail,rup:m}
}
function hybrid(C,proof){let live=new Set(C.flat().map(Math.abs)),chosen=[],seen=new Set(C.map(key));for(let c of proof.slice(0,Math.floor(proof.length/2))){let a=canon(c);if(a.length&&a.every(l=>live.has(Math.abs(l)))&&!seen.has(key(a))){seen.add(key(a));chosen.push(a)}}
 let db=C.slice(),closure={scans:0,lits:0,cap:10000000};for(let c of chosen){db.push(c);up(db,[],closure)}let s=solve(db);return {chosen,closure,solve:s,check:s.status==="UNSAT"?check(db,s.tree):null}}

if(typeof module!=="undefined")module.exports={sha,norm,replay,peerReplay,hybrid};
