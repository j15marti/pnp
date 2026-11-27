// Run node audit.js benchmarks.json; faithful transcription of compiler 21b9d53fb8166c819b24e708656c742cd3c24f10
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
 return {network:{format:"STRICT-EB4-v1",types,edges},source_map:{original_n:n,ternary_clauses:F,original_clause_ids:parents,representative_ports:reps,vertex_provenance:owners}};
}
function run(instance,compile){
 const G=compile(instance),net=G.network,bytes=JSON.stringify(net)+"\n";let hash=2166136261;for(let i=0;i<bytes.length;i++)hash=Math.imul(hash^bytes.charCodeAt(i),16777619)>>>0;
 const n=net.types.length*4, adj=Array.from({length:n},()=>[]);let eqEdges=0;
 const link=(a,b,s)=>{adj[a].push([b,s]);adj[b].push([a,s]);eqEdges++};
 for(const [a,b,s] of net.edges)link(a,b,s);
 net.types.forEach((t,v)=>{if(t==="E")for(let j=1;j<4;j++)link(4*v,4*v+j,0)});
 const root=new Int32Array(n).fill(-1),sign=new Uint8Array(n);let roots=0,visits=0;
 for(let i=0;i<n;i++)if(root[i]<0){roots++;let q=[i];root[i]=i;for(let h=0;h<q.length;h++){let a=q[h];for(const [b,s] of adj[a]){visits++;let t=sign[a]^s;if(root[b]<0){root[b]=i;sign[b]=t;q.push(b)}else if(root[b]!==i||sign[b]!==t)throw Error("signed contradiction")}}}
 // Independent union-find parity reconstruction of same equality network.
 const par=Int32Array.from({length:n},(_,i)=>i),sg=new Uint8Array(n),size=new Int32Array(n).fill(1);let ufReads=0;
 function find(x){let s=0;while(par[x]!==x){ufReads++;s^=sg[x];x=par[x]}return [x,s]}
 function union(a,b,s){let [x,u]=find(a),[y,v]=find(b);if(x===y){if((u^v)!==s)throw Error("UF contradiction");return}if(size[x]<size[y])[x,y]=[y,x];par[y]=x;sg[y]=u^v^s;size[x]+=size[y]}
 for(const [a,b,s] of net.edges)union(a,b,s);
 net.types.forEach((t,v)=>{if(t==="E")for(let j=1;j<4;j++)union(4*v,4*v+j,0)});
 for(let i=0;i<n;i++){let [a,s]=find(i),[b,t]=find(root[i]);if(a!==b||(s^t)!==sign[i])throw Error("UF mismatch")}
 const rows=[];const freq=new Map();
 net.types.forEach((t,v)=>{if(t==="B"){let p=[0,1,2,3].map(j=>4*v+j);let lits=p.map(i=>[root[i],sign[i]]);rows.push({v,lits});for(const [r] of lits)freq.set(r,(freq.get(r)||0)+1)}});
 const anchor=[...freq].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];
 function evalAt(f,values){let k=0;for(let j=0;j<f.s.length;j++)k|=values.get(f.s[j])<<j;return f.t[k]}
 let initial=rows.map(({v,lits})=>{let s=[...new Set(lits.map(l=>l[0]).filter(x=>x!==anchor))].sort((a,b)=>a-b);let t=Array.from({length:1<<s.length},(_,w)=>Number(lits.reduce((a,[r,z])=>a+((r===anchor?0:(w>>s.indexOf(r))&1)^z),0)!==2));return {s,t,ids:[v]}});
 // Lane A: zero-energy table arc consistency, unconditional after gauge.
 function closure(fs,as,ledger){let changed=true;while(changed){changed=false;for(const f of fs){let masks=f.s.map(()=>0),count=0;for(let w=0;w<f.t.length;w++){ledger.events++;if(f.t[w]!==0)continue;let ok=true;for(let j=0;j<f.s.length;j++)if(as.has(f.s[j])&&as.get(f.s[j])!==((w>>j)&1)){ok=false;break}if(!ok)continue;count++;for(let j=0;j<f.s.length;j++)masks[j]|=1<<((w>>j)&1)}
 if(!count)return false;for(let j=0;j<f.s.length;j++)if(masks[j]!==3&&!as.has(f.s[j])){as.set(f.s[j],masks[j]===2?1:0);changed=true}
 if(ledger.events>ledger.cap)throw Error("cap")
 }}return true}
 const cap=1e7,L={events:0,cap};let assignments=new Map();let local=closure(initial,assignments,L);
 // Lane B: exact necessary parity equations (one-bit coefficients, BigInt rows).
 let vars=[...freq.keys()].filter(x=>x!==anchor).sort((a,b)=>a-b),ix=new Map(vars.map((x,i)=>[x,i])),basis=new Map(),pops=0,parityConflict=false;
 for(const row of rows){let b=0n,rhs=0;for(const [r,s] of row.lits){rhs^=s;if(r!==anchor)b^=1n<<BigInt(ix.get(r))}for(let j=vars.length-1;j>=0;j--)if((b>>BigInt(j))&1n){pops++;if(!basis.has(j)){basis.set(j,[b,rhs]);b=0n;rhs=0;break}let [a,c]=basis.get(j);b^=a;rhs^=c}if(!b&&rhs)parityConflict=true}
 // Hybrid: exact min-sum bucket elimination, width <= 3 output. Keep duplicates, so objective counts original B vertices.
 function eliminate(fs,pins,width,ledger){
  let out=fs.map(f=>{let s=f.s.filter(v=>!pins.has(v));let t=Array.from({length:1<<s.length},(_,w)=>{let a=new Map(pins);s.forEach((v,j)=>a.set(v,(w>>j)&1));ledger.events++;return evalAt(f,a)});return {s,t,ids:f.ids}});
  let log=[],peak=out.reduce((a,f)=>a+f.t.length,0);
  for(;;){let buckets=new Map();for(let i=0;i<out.length;i++)for(const v of out[i].s){ledger.scans++;if(!buckets.has(v))buckets.set(v,[]);buckets.get(v).push(i)}
   let best=null;
   for(const [v,b] of buckets){let s=[...new Set(b.flatMap(i=>out[i].s))].filter(x=>x!==v).sort((a,b)=>a-b);ledger.scans+=b.length;if(s.length<=width&&(!best||s.length<best.s.length||s.length===best.s.length&&(b.length<best.b.length||b.length===best.b.length&&v<best.v)))best={v,b,s}}
   if(!best)break;let {v,b,s}=best,t=[],check=[];
   for(let w=0;w<1<<s.length;w++){let a=new Map(s.map((x,j)=>[x,(w>>j)&1]));let costs=[0,0];for(let bit=0;bit<2;bit++){a.set(v,bit);for(const i of b){costs[bit]+=evalAt(out[i],a);ledger.events++}}t.push(Math.min(...costs));check.push(costs)}
   let ids=b.flatMap(i=>out[i].ids);log.push({v,s,t,costs:check,ids});let gone=new Set(b);out=out.filter((_,i)=>!gone.has(i));out.push({s,t,ids});peak=Math.max(peak,out.reduce((a,f)=>a+f.t.length,0));if(ledger.events+ledger.scans>ledger.cap)throw Error("cap")
  }return {out,log,peak}
 }
 // Independent min-sum checker: derive each output row by enumerating the full joint assignment,
 // using a different projection routine and checking exact factor partition.
 function replay(fs,pins,log){let out=fs.map(f=>{let s=f.s.filter(v=>!pins.has(v)),t=new Array(1<<s.length).fill(-1);for(let w=0;w<f.t.length;w++){if(f.s.some((v,j)=>pins.has(v)&&pins.get(v)!==((w>>j)&1)))continue;let k=0;s.forEach((v,j)=>k|=((w>>f.s.indexOf(v))&1)<<j);t[k]=f.t[w]}return {s,t,ids:f.ids}});let reads=0;
 for(const r of log){let b=out.filter(f=>f.s.includes(r.v));let s=[...new Set(b.flatMap(f=>f.s))].filter(v=>v!==r.v).sort((a,b)=>a-b);if(String(s)!==String(r.s)||String(b.flatMap(f=>f.ids))!==String(r.ids))throw Error("bucket provenance");let joint=[r.v,...s],t=new Array(1<<s.length).fill(Infinity);for(let w=0;w<1<<joint.length;w++){let cost=0;for(const f of b){let k=0;f.s.forEach((v,j)=>k|=((w>>joint.indexOf(v))&1)<<j);cost+=f.t[k];reads++}t[w>>1]=Math.min(t[w>>1],cost)}if(String(t)!==String(r.t))throw Error("cost mismatch");out=out.filter(f=>!f.s.includes(r.v));out.push({s,t,ids:r.ids})}return {out,reads}}
 const H={events:0,scans:0,cap},hy=eliminate(initial,assignments,3,H),audit=replay(initial,assignments,hy.log);
 if(JSON.stringify(hy.out)!==JSON.stringify(audit.out))throw Error("final mismatch");
 // Hybrid search over zero-energy rows. Exact finite exhaustive branches, not claimed poly.
 function search(fs,cap){let l={events:0,cap},nodes=0,leaves=0,forced=0;
 function go(a){nodes++;let before=a.size;if(!closure(fs,a,l)){leaves++;return ["conflict"]}forced+=a.size-before;let count=new Map();for(const f of fs)for(const v of f.s)if(!a.has(v))count.set(v,(count.get(v)||0)+1);if(!count.size)return ["sat",[...a]];
 let v=[...count].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];let x=new Map(a);x.set(v,0);let left=go(x);if(left[0]!=="conflict"&&left[0]!=="split")return left;x=new Map(a);x.set(v,1);let right=go(x);if(right[0]!=="conflict"&&right[0]!=="split")return right;return ["split",v,left,right]}
 try{let tree=go(new Map());return {status:tree[0]==="sat"?"SAT":"UNSAT",events:l.events,nodes,leaves,forced,tree}}catch(e){if(e.message!=="cap")throw e;return {status:"UNKNOWN",events:l.events,nodes,leaves,forced}}}
 let hres=search(hy.out,cap-H.events-H.scans),post={events:0,cap};let postpins=new Map();let postok=closure(hy.out,postpins,post);
 // provenance lane: verify every representative equality identity and local clause compiler mapping by matching actual row literals.
 const mp=G.source_map, rep=new Map(Object.entries(mp.representative_ports).map(([id,[p,s]])=>[id,[root[p],sign[p]^s]]));
 let mapChecks=0;
 for(const row of rows){let [_,orig,i,j,k]=mp.vertex_provenance[row.v], [a,b,c]=mp.ternary_clauses[i],lit=x=>["x"+Math.abs(x),Number(x<0)];if(orig!==mp.original_clause_ids[i])throw Error("parent mismatch");let expected=j===0?[lit(a),lit(b),["z"+i,0]]:[["z"+i,1],lit(c),["f",0]];expected.push(["w"+i+"_"+j,0]);for(let h=0;h<4;h++){let [id,s]=expected[h],[r,z]=rep.get(id);if(row.lits[h][0]!==r||row.lits[h][1]!== (z^s))throw Error("map mismatch");mapChecks++}}
 // Exact source CNF tables; no reference proofs used.
 const cnf=instance.dimacs.trim().split("\n").slice(1).map((l,i)=>{let a=l.split(/\s+/).map(Number);a.pop();let s=[...new Set(a.map(Math.abs))].sort((a,b)=>a-b),t=Array.from({length:1<<s.length},(_,w)=>Number(!a.some(l=>Boolean((w>>s.indexOf(Math.abs(l)))&1)===(l>0))));return {s,t,ids:[i+1]}});
 const prov=search(cnf,cap);
 // Replay peer JOINT quadratic XOR certificate from original CNF via direct chart enumeration, independent of solver.
 let peer=null;
 if(instance.id==="JOINT-24"){const group=[1,12,23,30,52,56,60,76,87,91,113,117,124,135,142],negative=[6,7,9,13,14,18,20,27,32,33,40,42,43,46,57,66,68,78,81,99,100,101,114,127,143,145,151,153];let B=new Map();for(let id of group){let f=cnf[id-1];if(f.t[0]!==1||f.t.slice(1).some(x=>x!==0))throw Error("group");for(let i=0;i<f.s.length;i++)for(let j=i+1;j<f.s.length;j++)if(!cnf.some(g=>g.s.length===2&&g.s[0]===f.s[i]&&g.s[1]===f.s[j]&&String(g.t)==="0,0,0,1"))throw Error("missing pair");let b=f.s.reduce((a,x)=>a^(1<<(x-1)),0),r=1;for(let j=23;j>=0;j--)if((b>>>j)&1){if(!B.has(j)){B.set(j,[b,r]);b=0;r=0;break}let [u,v]=B.get(j);b^=u;r^=v}if(!b&&r)throw Error("unexpected parity contradiction")}
 let free=Array.from({length:24},(_,i)=>i).filter(i=>!B.has(i)),checks=0;for(let w=0;w<1<<free.length;w++){let x=free.reduce((a,j,k)=>a|(((w>>k)&1)<<j),0);for(let j=0;j<24;j++)if(B.has(j)){let [b,r]=B.get(j),v=r,y=(b&x)>>>0;while(y){v^=1;y&=y-1}x|=v<<j}let sum=0;for(let id of negative){let f=cnf[id-1];let k=f.s.reduce((a,j,i)=>a|(((x>>>(j-1))&1)<<i),0);sum^=f.t[k];checks++}if(sum!==1)throw Error("peer XOR identity") }peer={rank:B.size,chartWords:1<<free.length,checks,scope:"original CNF, provenance lane only"}}
 return {id:instance.id,N:bytes.length*8,fnv:hash.toString(16).padStart(8,"0"),vertices:net.types.length,edges:net.edges.length,B:rows.length,roots,anchor,anchorFrequency:freq.get(anchor),eqEdges,visits,ufReads,local:{ok:local,forced:[...assignments],events:L.events},parity:{rank:basis.size,nullity:vars.length-basis.size,conflict:parityConflict,pivotEvents:pops},hybrid:{eliminated:hy.log.length,remainingVariables:new Set(hy.out.flatMap(f=>f.s)).size,factors:hy.out.length,peakTableEntries:hy.peak,events:H.events,scans:H.scans,replayReads:audit.reads,postClosure:{ok:postok,pins:[...postpins],events:post.events},search:hres,log:hy.log},provenance:{mapChecks,mapBytes:JSON.stringify(mp).length+1,sourceBits:instance.dimacs.length*8,search:prov},peer};
}
const corpus=JSON.parse(require('fs').readFileSync(process.argv[2],'utf8')); console.log(JSON.stringify(['JOINT-24','RANDOM-3CNF-40'].map(id=>run(corpus.instances.find(x=>x.id===id),compile)),null,2));
