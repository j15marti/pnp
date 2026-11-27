// Run node replay.js benchmarks.json compile.js instance-registry-v1.json
const fs=require('fs'); const compiler=fs.readFileSync(process.argv[3],'utf8');
function sha(s){
 const K=Uint32Array.from(Array.from({length:64},(_,i)=>{let n=2,c=-1;for(;;n++){let p=true;for(let d=2;d*d<=n;d++)if(n%d===0){p=false;break}if(p&&++c===i)return Math.floor((Math.cbrt(n)%1)*4294967296)}}));
 let H=Uint32Array.from([0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]);
 const b=new Uint8Array(Math.ceil((s.length+9)/64)*64); for(let i=0;i<s.length;i++){if(s.charCodeAt(i)>127)throw Error("non ASCII");b[i]=s.charCodeAt(i)}b[s.length]=128;let dv=new DataView(b.buffer);dv.setUint32(b.length-4,s.length*8);dv.setUint32(b.length-8,Math.floor(s.length*8/4294967296));
 const rr=(x,n)=>(x>>>n)|(x<<(32-n));const w=new Uint32Array(64);
 for(let j=0;j<b.length;j+=64){for(let i=0;i<16;i++)w[i]=dv.getUint32(j+4*i);for(let i=16;i<64;i++){let x=w[i-15],y=w[i-2];w[i]=w[i-16]+(rr(x,7)^rr(x,18)^(x>>>3))+w[i-7]+(rr(y,17)^rr(y,19)^(y>>>10))}
 let [a,c,d,e,f,g,h,l]=H;for(let i=0;i<64;i++){let t1=(l+(rr(f,6)^rr(f,11)^rr(f,25))+((f&g)^(~f&h))+K[i]+w[i])>>>0,t2=((rr(a,2)^rr(a,13)^rr(a,22))+((a&c)^(a&d)^(c&d)))>>>0;l=h;h=g;g=f;f=(e+t1)>>>0;e=d;d=c;c=a;a=(t1+t2)>>>0} [a,c,d,e,f,g,h,l].forEach((x,i)=>H[i]+=x)}
 return Array.from(H,x=>x.toString(16).padStart(8,"0")).join("")
}
function native(G){
 const n=G.types.length*4,adj=Array.from({length:n},()=>[]);let ev=0;
 function link(a,b,s){adj[a].push([b,s]);adj[b].push([a,s])}
 for(const [a,b,s] of G.edges)link(a,b,s);G.types.forEach((t,v)=>{if(t==="E")for(let j=1;j<4;j++)link(4*v,4*v+j,0)});
 let root=new Int32Array(n).fill(-1),phase=new Uint8Array(n);let roots=[];
 for(let i=0;i<n;i++)if(root[i]<0){roots.push(i);root[i]=i;const Q=[i];for(let k=0;k<Q.length;k++)for(const [b,s] of adj[Q[k]]){ev++;let a=Q[k];if(root[b]<0){root[b]=i;phase[b]=phase[a]^s;Q.push(b)}else if(root[b]!==i||phase[b]!== (phase[a]^s))throw Error("parity contradiction")}}
 let rows=new Map();
 G.types.forEach((t,i)=>{if(t!=="B")return;const ports=[4*i,4*i+1,4*i+2,4*i+3],vs=[...new Set(ports.map(p=>root[p]))].sort((a,b)=>a-b),key=vs.join(","),words=[];
 for(let k=0;k<2**vs.length;k++){ev++;if(ports.reduce((s,p)=>s+(((k>>vs.indexOf(root[p]))&1)^phase[p]),0)===2)words.push(k)}
 if(rows.has(key)){let r=rows.get(key);r.words=r.words.filter(w=>words.includes(w));r.owners.push(i)}else rows.set(key,{vs,words,owners:[i]})});
 const R=[...rows.values()],inc=new Map();for(const r of R)for(const v of r.vs)inc.set(v,(inc.get(v)||0)+1);
 function close(R,pins){let changed=true,scans=0;while(changed){changed=false;for(const r of R){let w=r.words.filter(x=>{scans++;return r.vs.every((v,i)=>!pins.has(v)||pins.get(v)===((x>>i)&1))});if(!w.length)return {ok:false,scans};if(w.length<r.words.length){r.words=w;changed=true}r.vs.forEach((v,i)=>{if(!pins.has(v)&&w.every(x=>((x>>i)&1)===((w[0]>>i)&1))){pins.set(v,(w[0]>>i)&1);changed=true}})}}return {ok:true,scans}}
 const pins=new Map(),initial=close(R,pins);
 const rootStats={components:roots.length,balanceRows:R.length,duplicateRows:G.types.filter(x=>x==="B").length-R.length,initial,forced:pins.size,highIncidence:[...inc.values()].filter(x=>x>2).length,private:[...inc.values()].filter(x=>x===1).length};
 if(!initial.ok)return {rootStats,ev};
 const gauge=[...inc].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];pins.set(gauge,0);let cl=close(R,pins);ev+=initial.scans+cl.scans;
 // exact local projection, including all incident relations; width cap 7, at most two nontrivial owners
 const steps=[];let active=R.map(r=>({vs:r.vs.slice(),words:r.words.slice(),owners:r.owners.slice()}));
 for(let [v,b] of pins){active=active.map(r=>{let i=r.vs.indexOf(v);if(i<0)return r;let vs=r.vs.filter(x=>x!==v),words=[...new Set(r.words.filter(w=>((w>>i)&1)===b).map(w=>(w&((1<<i)-1))|((w>>(i+1))<<i)))];return {...r,vs,words}})}
 let capped=false;
 for(;;){let ix=new Map();active.forEach((r,i)=>r.vs.forEach(v=>{if(!ix.has(v))ix.set(v,[]);ix.get(v).push(i)}));let best=null;
 for(const [v,ids] of ix){ev++;if(ids.length>2)continue;let vs=[...new Set(ids.flatMap(i=>active[i].vs))].filter(x=>x!==v).sort((a,b)=>a-b);if(vs.length>7)continue;const score=[ids.length,vs.length,v];if(!best||score[0]<best.score[0]||score[0]===best.score[0]&&(score[1]<best.score[1]||score[1]===best.score[1]&&v<best.v))best={v,ids,vs,score}}
 if(!best)break;if(ev>7000000){capped=true;break}let {v,ids,vs}=best,rs=ids.map(i=>active[i]),words=[];
 for(let w=0;w<2**vs.length;w++){let ok=false;for(let b=0;b<2;b++){ev++;if(rs.every(r=>r.words.includes(r.vs.reduce((a,x,i)=>a|((x===v?b:(w>>vs.indexOf(x))&1)<<i),0))))ok=true}if(ok)words.push(w)}
 steps.push({v,vs,words,owners:rs.flatMap(r=>r.owners)});active=active.filter((_,i)=>!ids.includes(i));if(words.length!==2**vs.length)active.push({vs,words,owners:rs.flatMap(r=>r.owners)});
 if(!words.length)break;
 }
 const p2=new Map(),post=close(active,p2);ev+=post.scans;
 // All-different matching recognition refuses when reduced row scopes have >2 incidences or not exactly-one.
 const postInc=new Map();for(let r of active)for(let v of r.vs)postInc.set(v,(postInc.get(v)||0)+1);
 return {rootStats,gauge,afterGaugeForced:pins.size-1,projections:steps.length,activeRows:active.length,activeVars:postInc.size,postForced:p2.size,post,exactOneRows:active.filter(r=>r.words.length===r.vs.length&&r.words.every(w=>w>0&&(w&(w-1))===0)).length,postHighIncidence:[...postInc.values()].filter(x=>x>2).length,ev,capped,steps,active}
}
function matchingCNF(x){
 const C=x.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));
 const neg=new Set(C.filter(c=>c.length===2&&c.every(x=>x<0)).map(c=>c.map(x=>-x).sort((a,b)=>a-b).join(",")));
 const groups=C.map((c,i)=>({c,i:i+1})).filter(({c})=>c.length>=2&&c.every(v=>v>0)&&c.every((a,i)=>c.slice(i+1).every(b=>neg.has([a,b].sort((a,b)=>a-b).join(",")))));
 const parts=[];let remaining=groups.slice();while(remaining.length){let used=new Set(),part=[],rest=[];for(const g of remaining){if(g.c.some(v=>used.has(v)))rest.push(g);else{part.push(g);g.c.forEach(v=>used.add(v))}}if(used.size!==x.nvars)return {status:"UNKNOWN",reason:"no partition into authenticated exact-one groups",groups:groups.length};parts.push(part);remaining=rest}
 if(parts.length!==3||parts.some(p=>p.length!==parts[0].length))return {status:"UNKNOWN",reason:"no three equal partitions",groups:groups.length};
 let loc=parts.map(p=>{let z={};p.forEach((g,i)=>g.c.forEach(v=>z[v]=i));return z});
 let ev=0,proof=[],calls=0;
 // matching failure has a Hall witness using alternating reachable vertices
 function hall(live,a,b,forced){let k=parts[a].length,banA=forced?loc[a][forced]:-1,banB=forced?loc[b][forced]:-1,adj=Array.from({length:k},()=>[]);
 for(let v of live){ev++;let i=loc[a][v],j=loc[b][v];if(i!==banA&&j!==banB&&!adj[i].includes(j))adj[i].push(j)}
 let mr=Array(k).fill(-1),ml=Array(k).fill(-1);
 function aug(i,seen){for(let j of adj[i]){ev++;if(seen.has(j))continue;seen.add(j);if(mr[j]===-1||aug(mr[j],seen)){mr[j]=i;ml[i]=j;return true}}return false}
 for(let i=0;i<k;i++)if(i!==banA)aug(i,new Set());
 let U=[];for(let i=0;i<k;i++)if(i!==banA&&ml[i]===-1)U.push(i);if(!U.length)return null;
 const L=new Set(U),B=new Set();for(let i of L)for(let j of adj[i]){ev++;B.add(j);if(mr[j]>=0)L.add(mr[j])}
 if(B.size>=L.size)throw Error("bad Hall");return {a,b,forced:forced||0,L:[...L].sort((a,b)=>a-b),B:[...B].sort((a,b)=>a-b)}
 }
 function checkHall(live,h){const {a,b,forced,L,B}=h;let actual=new Set();for(let v of live){if(forced&&(loc[a][v]===loc[a][forced]||loc[b][v]===loc[b][forced]))continue;if(L.includes(loc[a][v]))actual.add(loc[b][v])}if(B.length>=L.length||actual.size!==B.length||B.some(j=>!actual.has(j))||new Set(L).size!==L.length||forced&&L.includes(loc[a][forced]))throw Error("certificate mismatch")}
 function closure(live){let deletes=[];for(;;){let drop=null;for(let [a,b] of [[0,1],[0,2],[1,2]]){calls++;let h=hall(live,a,b,0);if(h){checkHall(live,h);return {live,deletes,fail:h}}for(let v of live){calls++;h=hall(live,a,b,v);if(h){checkHall(live,h);drop={v,h};break}}if(drop)break}if(!drop)return {live,deletes};deletes.push(drop);live=live.filter(v=>v!==drop.v)}}
 let initial=Array.from({length:x.nvars},(_,i)=>i+1),r=closure(initial);proof.push({guard:[],...r});let rootDeleted=r.deletes.length,guardCuts=0;
 while(!r.fail){let rejected=null;for(let v of r.live){let guarded=r.live.filter(w=>w===v||loc.every(l=>l[w]!==l[v]));let t=closure(guarded);if(t.fail){rejected=v;proof.push({guard:[v],...t});guardCuts++;break}}if(rejected===null)break;r=closure(r.live.filter(v=>v!==rejected));proof.push({guard:[],rejected,...r})}
 return {status:r.fail?"UNSAT":"UNKNOWN",groups:parts.map(p=>p.map(g=>g.i)),rootDeleted,guardCuts,remaining:r.live,calls,ev,proof};
}
const compile=new Function(compiler.slice(compiler.indexOf("function compile("),compiler.indexOf("function auditLocal("))+"\nreturn compile")();
const corpus=JSON.parse(fs.readFileSync(process.argv[2],'utf8')), registry=JSON.parse(fs.readFileSync(process.argv[4],'utf8')); const arr=Object.values(registry).find(a=>Array.isArray(a)&&a.some(x=>x.alias==="EB-JOINT-24"));for(const id of ["JOINT-24","RANDOM-3CNF-40"]){let x=corpus.instances.find(y=>y.id===id),reg=arr.find(z=>z.alias==="EB-"+id),G=compile(x),bytes=JSON.stringify(G.network)+"\n",map=JSON.stringify(G.source_map)+"\n";if(sha(bytes)!==reg.sha256||bytes.length*8!==reg.N_bits||sha(map)!==reg.source_map_sha256||sha(x.dimacs)!==reg.source_cnf.sha256||x.dimacs.length*8!==reg.source_cnf.N_bits)throw Error("authentication mismatch");console.log(JSON.stringify({id,native:native(G.network),matching:matchingCNF(x)}))}
