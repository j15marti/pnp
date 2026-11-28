const fs=require('node:fs');
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

function sha(s){const H=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19],K=[];for(let n=2;K.length<64;n++){let prime=true;for(let j=2;j*j<=n;j++)if(n%j===0){prime=false;break}if(prime)K.push((Math.cbrt(n)%1*4294967296)>>>0)}let bytes=Array.from(s,x=>x.charCodeAt(0));if(bytes.some(x=>x>127))throw Error("ASCII only");let bits=bytes.length*8;bytes.push(128);while(bytes.length%64!==56)bytes.push(0);for(let i=7;i>=0;i--)bytes.push(Math.floor(bits/2**(8*i))&255);const R=(x,n)=>(x>>>n)|(x<<(32-n));for(let i=0;i<bytes.length;i+=64){let w=[];for(let j=0;j<16;j++)w[j]=(bytes[i+4*j]<<24)|(bytes[i+4*j+1]<<16)|(bytes[i+4*j+2]<<8)|bytes[i+4*j+3];for(let j=16;j<64;j++){let x=w[j-15],y=w[j-2];w[j]=(w[j-16]+(R(x,7)^R(x,18)^(x>>>3))+w[j-7]+(R(y,17)^R(y,19)^(y>>>10)))|0}let [A,B,C,D,E,F,G,J]=H;for(let j=0;j<64;j++){let t=(J+(R(E,6)^R(E,11)^R(E,25))+((E&F)^(~E&G))+K[j]+w[j])|0,u=((R(A,2)^R(A,13)^R(A,22))+((A&B)^(A&C)^(B&C)))|0;[A,B,C,D,E,F,G,J]=[(t+u)|0,A,B,C,(D+t)|0,E,F,G]}[A,B,C,D,E,F,G,J].forEach((x,j)=>H[j]=(H[j]+x)|0)}return H.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("")}
function experiment(network, dimacs){
 const sorted=a=>[...a].sort((x,y)=>x-y),uniq=a=>sorted(new Set(a)),key=a=>a.join(","),t=network.types.length,pa=Array.from({length:4*t},(_,i)=>i),par=new Uint8Array(4*t);let links=0;
 function find(x){if(pa[x]!==x){let [r,s]=find(pa[x]);par[x]^=s;pa[x]=r}return [pa[x],par[x]]}
 function join(x,y,s){let [a,u]=find(x),[b,v]=find(y);links++;if(a===b){if((u^v)!==s)throw Error("parity contradiction");return}if(a>b){[a,b]=[b,a]}pa[b]=a;par[b]=u^v^s}
 network.edges.forEach(([x,y,s])=>join(x,y,s));network.types.forEach((x,v)=>{if(x==="E")for(let j=1;j<4;j++)join(4*v,4*v+j,0)});
 let rows=new Map();network.types.forEach((x,v)=>{if(x==="B"){let a=sorted(Array.from({length:4},(_,j)=>{let [r,s]=find(4*v+j);return (r+1)*(s?-1:1)}));let k=key(a);if(!rows.has(k))rows.set(k,{a,owners:[]});rows.get(k).owners.push(v)}});
 let R=[...rows.values()],carriers=new Set(R.flatMap(r=>r.a.map(Math.abs))).size,inc=new Map();for(let i=0;i<R.length;i++)for(let v of new Set(R[i].a.map(Math.abs))){if(!inc.has(v))inc.set(v,[]);inc.get(v).push(i)}
 let nae=R.map((r,i)=>{let priv=r.a.filter(l=>inc.get(Math.abs(l)).length===1 && r.a.filter(z=>Math.abs(z)===Math.abs(l)).length===1);if(priv.length!==1)throw Error("private port");return {a:r.a.filter(l=>l!==priv[0]),owners:r.owners,private:priv[0]}});
 let ni=new Map();for(let i=0;i<nae.length;i++)for(let v of new Set(nae[i].a.map(Math.abs))){if(!ni.has(v))ni.set(v,[]);ni.get(v).push(i)}
 let anchor=[...ni].sort((a,b)=>b[1].length-a[1].length||a[0]-b[0])[0][0],used=new Set(),sewn=[];
 for(let [v,b] of ni){if(v===anchor||b.length!==2||b.some(i=>used.has(i)))continue;let [i,j]=b, x=nae[i].a.filter(l=>Math.abs(l)===v),y=nae[j].a.filter(l=>Math.abs(l)===v);if(x.length!==1||y.length!==1||x[0]!==-y[0])continue;used.add(i);used.add(j);sewn.push({a:[...nae[i].a.filter(l=>l!==x[0]),...nae[j].a.filter(l=>l!==y[0])],owners:[...nae[i].owners,...nae[j].owners],pivot:v})}
 if(used.size!==nae.length)throw Error("incomplete sewing");
 let F=[],owners=[];for(let r of sewn){for(let s of [1,-1]){let a=uniq(r.a.map(l=>s*l));if(a.includes(-anchor)||a.some(l=>a.includes(-l)))continue;a=a.filter(l=>l!==anchor);F.push(a);owners.push(r.owners)}}
 // anchor=0, sign +/- literal semantics. Early UP on each snapshot.
 const cnf=dimacs.trimEnd().split("\n").slice(1).map(x=>uniq(x.split(" ").map(Number).slice(0,-1)));
 function run(f){
 let vars=[...new Set(f.flat().map(Math.abs))].sort((a,b)=>a-b),freq=new Map(vars.map(v=>[v,f.filter(c=>c.includes(v)||c.includes(-v)).length])),order=vars.slice().sort((a,b)=>freq.get(b)-freq.get(a)||a-b);
 let pairs=new Map(),pairTests=0;f.forEach((c,i)=>{if(c.length!==3)return;for(let j=0;j<3;j++){let core=c.filter((_,k)=>k!==j),k=key(core);if(!pairs.has(k))pairs.set(k,{core,items:[]});pairs.get(k).items.push([i,c[j]]);pairTests++}});
 let claimed=new Set(),groups=[],learned=[],learnParents=[];for(let g of [...pairs.values()].sort((a,b)=>b.items.length-a.items.length||key(a.core).localeCompare(key(b.core)))){let it=g.items.filter(([i])=>!claimed.has(i));if(it.length<2)continue;it.forEach(([i])=>claimed.add(i));groups.push({core:g.core,items:it});}
 for(let g of pairs.values()){let pos=new Map(g.items.map(([i,l])=>[l,i]));for(let [i,l] of g.items)if(l>0&&pos.has(-l)&&!learned.some(c=>key(c)===key(g.core))&&!f.some(c=>key(c)===key(g.core))){learned.push(g.core);learnParents.push([i,pos.get(-l)])}}
 let reconstructed=[...groups.flatMap(g=>g.items.map(([i,l])=>[i,uniq([...g.core,l])])),...f.map((c,i)=>[i,c]).filter(([i])=>!claimed.has(i))].sort((a,b)=>a[0]-b[0]);if(JSON.stringify(reconstructed.map(x=>x[1]))!==JSON.stringify(f))throw Error("decode");
 for(let i=0;i<learned.length;i++){let [a,b]=learnParents[i].map(j=>f[j]);let v=a.find(l=>b.includes(-l));if(!v||key(uniq([...a.filter(l=>l!==v),...b.filter(l=>l!==-v)]))!==key(learned[i]))throw Error("bad resolvent")}
 const plain=f.map((c,i)=>({core:c,tails:null,ids:[i]})),compressed=[...groups.map(g=>({core:g.core,tails:g.items.map(x=>x[1]),ids:g.items.map(x=>x[0])})),...plain.filter((_,i)=>!claimed.has(i))];
 function up(rows,guard,ledger){let A=new Map(guard.map(l=>[Math.abs(l),l>0]));function val(l){let x=A.get(Math.abs(l));ledger.visits++;return x===undefined?0:x===(l>0)?1:-1}let change=true;
 while(change){change=false;for(let row of rows){ledger.rows++;let vv=row.core.map(val);if(vv.includes(1))continue;let free=row.core.filter((_,i)=>vv[i]===0);for(let l of row.tails??[null]){let z=l===null?-1:val(l);if(z===1)continue;let u=free.length+(z===0?1:0);if(!u)return null;if(u===1){let p=free[0]??l,v=Math.abs(p),b=p>0;if(A.has(v)&&A.get(v)!==b)return null;if(!A.has(v)){A.set(v,b);change=true;ledger.forced++}}}}}return A}
 function solve(rows,guard=[]){let ledger={visits:0,rows:0,forced:0,nodes:0};function rec(g){if(++ledger.nodes>10000||ledger.visits>2000000)return {unknown:true};let A=up(rows,g,ledger);if(!A)return {conflict:true};let v=order.find(v=>!A.has(v));if(v===undefined)return {sat:[...A]};let left=rec([...g,-v]);if(left.unknown||left.sat)return left;let right=rec([...g,v]);if(right.unknown||right.sat)return right;return {v,left,right}}let tree=rec(guard);return {tree,ledger}}
 // Independently check trees by explicit clauses, different closure routine.
 function verify(tree,ff,guard=[]){let visits=0,nodes=0;function check(t,g){nodes++;let A=new Map(g.map(l=>[Math.abs(l),l>0]));let changes=true,bad=false;while(changes&&!bad){changes=false;for(let c of ff){let free=[],yes=false;for(let l of c){visits++;if(!A.has(Math.abs(l)))free.push(l);else if(A.get(Math.abs(l))===(l>0)){yes=true;break}}if(yes)continue;if(!free.length){bad=true;break}if(free.length===1){A.set(Math.abs(free[0]),free[0]>0);changes=true}}}if(t.conflict)return bad;if(t.unknown||t.sat||bad||A.has(t.v))return false;return check(t.left,[...g,-t.v])&&check(t.right,[...g,t.v])}return {ok:check(tree,guard),visits,nodes}}
 let early={visits:0,rows:0,forced:0},A=up(plain,[],early);let arms=[];for(let [name,rows,ff] of [["explicit",plain,f],["motif",compressed,f],["hybrid",[...compressed,...learned.map(core=>({core,tails:null}))],[...f,...learned]]]){let d=solve(rows),v=verify(d.tree,ff);arms.push({name,ledger:d.ledger,verify:v,tree:d.tree})}
 // Exact guard partition: 4 prefixes + last cell.
 let guards=order.slice(0,4).map((v,i)=>[...order.slice(0,i),-v]);guards.push(order.slice(0,4));
 let gl=guards.map(g=>{let l1={visits:0,rows:0,forced:0},l2={visits:0,rows:0,forced:0};let a=up(plain,g,l1),b=up(compressed,g,l2);if(Boolean(a)!==Boolean(b)||a&&JSON.stringify([...a].sort())!==JSON.stringify([...b].sort()))throw Error("UP mismatch");return {guard:g,conflict:!a,plain:l1,motif:l2}});
 let literalSlots=f.reduce((s,c)=>s+c.length,0),compressedSlots=compressed.reduce((s,x)=>s+x.core.length+(x.tails?.length??0),0);
 return {vars:vars.length,clauses:f.length,early,earlyFree:A?vars.length-A.size:0,pairTests,groups:groups.length,groupedRows:claimed.size,literalSlots,compressedSlots,explicitBytes:JSON.stringify(f).length,motifBytes:JSON.stringify(compressed).length,learned,learnParents,guards:gl,arms};
 }
 return {carriers,links,rawB:network.types.filter(x=>x==="B").length,uniqueB:R.length,sewn:sewn.length,anchor,sourceOnly:run(F),companion:run(cnf),nativeOwners:owners,nativeClauses:F};
}
const corpus=JSON.parse(fs.readFileSync(process.argv[2],'utf8')), registry=JSON.parse(fs.readFileSync(process.argv[3],'utf8')); for(const id of ['JOINT-24','RANDOM-3CNF-40']){const x=corpus.instances.find(z=>z.id===id), y=registry.instances.find(z=>z.alias==='EB-'+id),g=compile(x),s=JSON.stringify(g.network)+'\n',m=JSON.stringify(g.source_map)+'\n';if(sha(s)!==y.sha256||s.length*8!==y.N_bits||sha(m)!==y.source_map_sha256||sha(x.dimacs)!==y.source_cnf.sha256)throw Error('auth');console.log(JSON.stringify({id,registry:y,...experiment(g.network,x.dimacs)}));}
