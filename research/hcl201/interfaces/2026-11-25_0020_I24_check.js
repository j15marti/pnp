// Node: node I24_check.js DR18_M24_reclosed.json S23_inputs.json
function run(raw,sources){
const stats={xors:0,evals:0,probes:0,pairScans:0,products:0};
const bit=i=>1n<<BigInt(i), high=x=>x.toString(2).length-1;
function reduce(x,B){while(x){let p=high(x);if(!B[p])break;x^=B[p];stats.xors++;}return x}
function insert(x,B){x=reduce(x,B);if(x){B[high(x)]=x;return true}return false}
// Full remainder, unlike insertion's early stop at an empty pivot.
function remainder(x,B){let out=0n;while(x){let p=high(x);if(B[p]){x^=B[p];stats.xors++}else{x^=bit(p);out|=bit(p)}}return out}
function parity(x){let p=0;while(x){x&=x-1n;p^=1}return p}
function dependencies(cols){let B=[],P=[],D=[];for(let j=0;j<cols.length;j++){let x=cols[j],v=bit(j);while(x){let p=high(x);if(!B[p]){B[p]=x;P[p]=v;break}x^=B[p];v^=P[p];stats.xors++}if(!x)D.push(v)}return D}
function subsets(v,d){let out=[[]];function rec(start,a){if(a.length===d)return;for(let j=start;j<v.length;j++){let b=[...a,v[j]];out.push(b);rec(j+1,b)}}rec(0,[]);return out}
function close(T,guard){let changed=true;while(changed){changed=false;for(let i=0;i<T.length;i++){let t=T[i],a=t.a.filter(w=>guard.every(([v,b])=>!t.v.includes(v)||Number(w[t.v.indexOf(v)])===b));if(a.length!==t.a.length){t.a=a;changed=true}if(!a.length)return false}for(let i=0;i<T.length;i++)for(let j=0;j<T.length;j++){if(i===j)continue;let a=T[i],b=T[j],shared=a.v.filter(x=>b.v.includes(x));if(!shared.length)continue;let ia=shared.map(x=>a.v.indexOf(x)),ib=shared.map(x=>b.v.indexOf(x)),key=(w,I)=>I.map(k=>w[k]).join("");stats.pairScans+=a.a.length+b.a.length;let S=new Set(b.a.map(w=>key(w,ib))),z=a.a.filter(w=>S.has(key(w,ia)));if(z.length!==a.a.length){a.a=z;changed=true}if(!z.length)return false}}return true}
function norm(job,d){let T=job.T.map(t=>({id:t.id,v:t.v.slice(),a:t.a.slice()})), guard=job.guard, active=[...new Set(T.flatMap(t=>t.v).concat(guard.map(g=>g[0])))].sort((a,b)=>a-b), G=subsets(active,d), idx=new Map(G.map((s,i)=>[s.join(","),i])), B=[], rounds=0, logs=[], status="OPEN", before=T.reduce((s,t)=>s+t.a.length,0), rank=0;
function embed(v,I){let x=0n;for(let j=0;j<I.length;j++)if(v&bit(j))x|=bit(I[j]);return x}
function prepare(t,k){let L=subsets(t.v.map((_,i)=>i),k), I=L.map(s=>idx.get(s.map(j=>t.v[j]).sort((a,b)=>a-b).join(","))), C=L.map(()=>0n), F=[];for(let i=0;i<t.a.length;i++){let w=t.a[i],f=0n;for(let j=0;j<L.length;j++){stats.evals++;if(L[j].every(k=>w[k]==="1")){C[j]|=bit(i);f|=bit(j)}}F.push(f)}return {I,C,F}}
function product(eq,v){let out=0n;while(eq){let p=high(eq);eq^=bit(p);let m=[...new Set([...G[p],v])].sort((a,b)=>a-b);let k=idx.get(m.join(","));if(k===undefined)throw Error("degree overflow");out^=bit(k)}stats.products++;return out}
if(!close(T,guard))status="UNSAT";
while(status==="OPEN"){rounds++;B=[];let low=[];for(const t of T){let p=prepare(t,d);for(const e of dependencies(p.C))insert(embed(e,p.I),B);if(d===3){let q=prepare(t,2);for(const e of dependencies(q.C))low.push(embed(e,q.I))}}
for(const [v,b] of guard){let e=bit(idx.get(String(v)))^(b?1n:0n);insert(e,B);if(d===3)low.push(e);if(d===2)for(const u of active)insert(product(e,u),B)}
if(d===3)for(const e of low)for(const v of active)insert(product(e,v),B);
rank=B.filter(Boolean).length;if(remainder(1n,B)===0n){status="UNSAT";break}
let del=[];for(const t of T){let p=prepare(t,d),D=dependencies(p.I.map(i=>remainder(bit(i),B))),keep=[];for(let i=0;i<t.a.length;i++){stats.probes++;if(D.every(e=>parity(e&p.F[i])===0))keep.push(t.a[i]);else del.push([t.id,t.a[i]])}t.a=keep}
logs.push({rank,deleted:del});if(T.some(t=>!t.a.length)){status="UNSAT";break}if(!del.length)break;if(!close(T,guard)){status="UNSAT";break}}
return {status,before,after:T.reduce((s,t)=>s+t.a.length,0),rounds,rank,features:G.length,logs,T}}
function witness(T,w,g){return g.every(([i,b])=>w[i]===b)&&T.every(t=>t.a.includes(t.v.map(i=>w[i]).join("")))}
function sourceOK(s,w){return s.O.every(o=>{let a=o.t.reduce((v,i,j)=>v+(w[i]<<j),0);return !(o.bad||[0,7]).includes(a)})}
let jobs=raw.results.filter(x=>x.mode==="pair"&&x.cap===0).map(x=>({id:x.id,guard:x.guard,T:x.finalTables,w:x.witness,lifted:x.lifted}));
function nae(t,flip=0){return {id:t.join(","),v:t,a:Array.from({length:8},(_,i)=>[0,1,2].map(j=>(i>>j)&1).join("")).filter(w=>{let z=[...w].map((x,j)=>Number(x)^(j===0?flip:0));return !(z.every(x=>x===z[0]))})}}
let fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
let plane=[];for(let slope=0;slope<3;slope++)for(let b=0;b<3;b++)plane.push([0,1,2].map(x=>3*x+(slope*x+b)%3));for(let x=0;x<3;x++)plane.push([0,1,2].map(y=>3*x+y));
for(const [id,triples,flip] of [["Fano",fano,0],["FanoSigned",fano,1],["Plane",plane,0],["PlaneDelete",plane.slice(1),0]]){let T=triples.map((t,i)=>nae(t,i===0?flip:0)),n=Math.max(...triples.flat())+1,models=[];for(let i=0;i<2**n;i++){let w=Array.from({length:n},(_,j)=>(i>>j)&1);if(witness(T,w,[]))models.push(w)}jobs.push({id,guard:[],T,w:models[0],models})}
let results=[];for(const job of jobs){let modes=[];for(const d of [1,2,3]){let old={...stats},a=norm(job,d);if(job.w&&(!witness(a.T,job.w,job.guard)||a.status==="UNSAT"))throw Error("lost witness "+job.id);if(job.models)for(const w of job.models)if(!witness(a.T,w,job.guard))throw Error("lost control");if(job.lifted){let w=[...job.lifted].map(Number);if(!sourceOK(sources.find(x=>x.id===job.id),w)||!job.guard.every(([i,b])=>w[i]===b))throw Error("source lift mismatch "+job.id)}modes.push({...a,T:undefined,degree:d,cost:Object.fromEntries(Object.keys(stats).map(k=>[k,stats[k]-old[k]]))})}results.push({id:job.id,guard:job.guard,reference:job.models?job.models.length:"peer SAT witness verified",modes})}return {results,stats}}
if(typeof module!=="undefined"&&require.main===module){const fs=require("fs");console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2],"utf8")),JSON.parse(fs.readFileSync(process.argv[3],"utf8"))),null,2))}
