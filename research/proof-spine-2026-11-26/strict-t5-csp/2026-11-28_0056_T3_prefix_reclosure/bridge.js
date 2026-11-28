function bridge(s){
const H=Function(s.hybrid.split('if(typeof require==="function"')[0]+";return {sha}")(),sha=x=>H.sha(typeof x==="string"?x:JSON.stringify(x)+"\n"),A=(p,m)=>{if(!p)throw Error(m)},P=JSON.parse(s.old),peer=JSON.parse(s.peer),F=P.chart,V=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b);
A(sha(s.old)==="ed4d5336bf89902532fc422331a620007f6fb1f2bae2d89fb496d7c78dd36f2e"&&sha(s.peer)==="6e51eff6a61d59e11420002279e5e3a89acff9178ff3c1f6680c557553bb23ad","parents");
A(peer.instance_id===P.instance_id&&peer.internal_guard===P.guard_id,"identity");
const seq=peer.proof.slice(0,peer.prefixLength).map(c=>c.map(l=>Math.sign(l)*peer.dense_to_original_port_plus1[Math.abs(l)-1]));
let reads=0;function up(db,g){let a=new Map();for(let l of g){let v=Math.abs(l),b=Number(l>0);if(a.has(v)&&a.get(v)!==b)return true;a.set(v,b)}for(;;){let change=false;for(let c of db){let free=[],hit=false;for(let l of c){reads++;let v=Math.abs(l);if(!a.has(v))free.push(l);else if(a.get(v)===Number(l>0)){hit=true;break}}if(hit)continue;if(!free.length)return true;if(free.length===1){a.set(Math.abs(free[0]),Number(free[0]>0));change=true}}if(!change)return false}}
let db=F.slice();for(let c of seq){A(c.length<=2&&c.every(l=>V.includes(Math.abs(l)))&&up(db,c.map(l=>-l)),"RUP");db.push(c)}
const adj=new Map(V.flatMap(v=>[[v,[]],[-v,[]]]));for(let [i,c] of seq.entries()){if(c.length===1)adj.get(-c[0]).push([c[0],i]);else{adj.get(-c[0]).push([c[1],i]);adj.get(-c[1]).push([c[0],i])}}
function path(a,b){let q=[a],prev=new Map([[a,null]]);for(let i=0;i<q.length;i++)for(let [v,j] of adj.get(q[i]))if(!prev.has(v)){prev.set(v,[q[i],j]);q.push(v)}if(!prev.has(b))return null;let z=[];for(let v=b;v!==a;){let [u,j]=prev.get(v);z.push([u,v,j]);v=u}return z.reverse()}
let v=V.find(v=>path(v,-v)&&path(-v,v));A(v!==undefined,"cycle");let paths=[path(v,-v),path(-v,v)];
function toggle(p,k){if(p.has(k))p.delete(k);else p.add(k)}
function sum(a,b){let r=new Set(a);for(let t of b)toggle(r,t);return r}
function times(a,b){let p=new Set();for(let x of a)for(let y of b){let t=[...new Set([...(x?x.split(",").map(Number):[]),...(y?y.split(",").map(Number):[])])].sort((a,b)=>a-b);A(t.length<=3,"degree");toggle(p,t.join(","))}return p}
function truth(l){return l>0?new Set([String(l)]):new Set(["",String(-l)])}
function falseLit(l){return sum(new Set([""]),truth(l))}
function violation(c){return c.reduce((p,l)=>times(p,falseLit(l)),new Set([""]))}
function eq(a,b){return a.size===b.size&&[...a].every(t=>b.has(t))}
let proofs=[],mulSteps=0;for(let path of paths){let start=path[0][0],p=violation(seq[path[0][2]]);A(eq(p,times(truth(start),falseLit(path[0][1]))),"first");let rows=[{edge:path[0],p:[...p]}];for(let i=1;i<path.length;i++){let [u,w,j]=path[i],q=violation(seq[j]);A(eq(q,times(truth(u),falseLit(w))),"edge");let t=times(p,falseLit(w)),r=times(q,truth(start));mulSteps+=2;p=sum(t,r);A(eq(p,times(truth(start),falseLit(w))),"composition");rows.push({edge:path[i],products:[[...t],[...r]],p:[...p]})}A(eq(p,truth(start)),"opposite endpoint");proofs.push({start,path,rows,terminal:[...p]})}
A(eq(sum(new Set(proofs[0].terminal),new Set(proofs[1].terminal)),new Set([""])),"constant one");
const stats=JSON.parse(s.results)[1].activation;let cert={schema:"T3-BINARY-PATH-PC3-v1",problem_id:P.problem_id,instance:P.instance,instance_id:P.instance_id,original_N_bits:P.original_N_bits,source_pin:P.source_pin,guard_id:P.guard_id,residual_id:P.residual_id,original_ids:P.original_ids,parents:["CERT-v1:sha256:"+sha(s.old),"CERT-v1:sha256:"+sha(s.peer)],claim:"After locally checked RUP binary prefix, two explicit opposite implication paths yield constant one using Boolean multilinear degree<=3; same gauged chart. Full native root discharges complement separately.",seq,paths:proofs,readCounts:reads,formalMultiplications:mulSteps,rankReclosure:stats.prefixes.map(a=>({k:a.k,status:a.status,rank:a.rank,ops:a.ops})),reproducer:"run.js commit 217720792ddb69dfc7a655340b23c30248b16eb0; bridge.js with exact old, peer, hybrid, results bytes; old source projection authenticated by run.js"};
return {cert,sha:sha(cert),paths:paths.map(p=>p.length),v,reads,mulSteps}
}
if(typeof require==='function'){let fs=require('fs'),keys=['old','peer','hybrid','results'];let s=Object.fromEntries(keys.map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]));console.log(JSON.stringify(bridge(s),null,2));}
