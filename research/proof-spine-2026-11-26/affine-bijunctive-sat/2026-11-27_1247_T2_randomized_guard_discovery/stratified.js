// node randomized.js compile.js benchmarks.json registry.json experiment.js
function run(c,b,r,h){
const compile=Function(c.slice(c.indexOf("function compile"),c.indexOf("function auditLocal"))+";return compile")();
const {sha,normalize,independentNormalize,eliminate,verifyTrace,gauge}=Function(h.slice(0,h.indexOf("// Node runner"))+";return {sha,normalize,independentNormalize,eliminate,verifyTrace,gauge}")();
if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("sha");
const B=JSON.parse(b),R=JSON.parse(r),CAP=400000,seeds=[1,2,3,4,5,6,7,8,9,10,11,12],out={};
function rng(seed,ct){let s=seed>>>0;if(!s)throw Error("zero seed");return n=>{if(n<1||n>4294967295)throw Error("rng range");let limit=Math.floor(4294967296/n)*n,x;do{s^=s<<13;s^=s>>>17;s^=s<<5;x=s>>>0;ct.draws++;}while(x>=limit);return x%n}}
function factor(vs,ok,id){let a=0n,Z=vs.map(()=>0n),O=vs.map(()=>0n);for(let w of ok){let q=1n<<BigInt(w);a|=q;for(let j=0;j<vs.length;j++){if(w>>j&1)O[j]|=q;else Z[j]|=q}}return{vs,id,mask:a,Z,O}}
function decode(m){let a=[];for(let i=0;m;m>>=1n,i++)if(m&1n)a.push(i);return a}
function pc(m){let n=0;while(m){m&=m-1n;n++}return n}
function clauseFactor(g,id){let vs=g.map(a=>a[0]),bad=g.reduce((s,a,i)=>s+(a[1]<<i),0);return factor(vs,Array.from({length:2**vs.length},(_,i)=>i).filter(w=>w!==bad),id)}
function key(g){return g.map(a=>a.join(":")).join(",")}
function close(F,D,g,r,ct,cap){let P=new Int8Array(r).fill(-1),M=D.slice();for(let [i,v] of g){if(P[i]!==-1&&P[i]!==v)return null;P[i]=v}for(;;){let change=false;for(let i=0;i<F.length;i++){if(++ct.visits>cap)throw Error("CAP");let f=F[i],q=M[i];for(let j=0;j<f.vs.length;j++){let a=P[f.vs[j]];ct.filters++;if(a===0)q&=f.Z[j];else if(a===1)q&=f.O[j]}if(!q)return null;M[i]=q;for(let j=0;j<f.vs.length;j++){let v=f.vs[j];if(P[v]!==-1)continue;ct.forceChecks++;let b=(q&f.O[j])===0n?0:(q&f.Z[j])===0n?1:-1;if(b!==-1){P[v]=b;change=true}}}if(!change)return{P,M}}}
function testOne(F,D,v,r,ct,cap,union){ct.probes+=2;let a=close(F,D,[[v,0]],r,ct,cap),b=close(F,D,[[v,1]],r,ct,cap);if(!a&&!b)return{kind:"split",v};if(!union){if(!a||!b)return{kind:"learn",g:[[v,a?1:0]]};return null}
let changes=[];for(let i=0;i<F.length;i++){let q=(a?a.M[i]:0n)|(b?b.M[i]:0n);if(q!==D[i])changes.push([i,decode(q)])}return changes.length?{kind:"rows",v,changes}:null}
function testPair(F,D,g,r,ct,cap){ct.probes++;return close(F,D,g,r,ct,cap)?null:{kind:"learn",g}}
function discover(initial,r,mode,seed,cap=CAP){let F=initial.slice(),D=F.map(f=>f.mask),ct={visits:0,filters:0,forceChecks:0,probes:0,draws:0,candidates:0,poolEntries:0,swaps:0},rand=seed===null?null:rng(seed,ct),proof=[],seen=new Set(),removed=0,learned=0,epochs=0,terminal="UNKNOWN",first=null,orig=F.length;
try{for(;;){epochs++;let root=close(F,D,[],r,ct,cap);if(!root){proof.push({kind:"root"});terminal="UNSAT";break}
let live=Array.from(root.P).map((x,i)=>x===-1?i:-1).filter(i=>i!==-1),pool=[];for(let v of live)pool.push({v});if(mode!=="single")for(let i=0;i<live.length;i++)for(let j=i+1;j<live.length;j++)for(let a=0;a<2;a++)for(let b=0;b<2;b++){let g=[[live[i],a],[live[j],b]];if(!seen.has(key(g)))pool.push({g})}ct.poolEntries+=pool.length;
// Lazy stratified scheduling: one single-bit candidate then four pair candidates; no shuffling untried entries.
let firstPool=pool.filter(x=>!x.g),pairPool=pool.filter(x=>x.g),si=0,pi=0,turn=0;
function* order(){while(si<firstPool.length||pi<pairPool.length){let isSingle=si<firstPool.length&&(pi===pairPool.length||mode==="priority"||turn%5===0);let A=isSingle?firstPool:pairPool,j=isSingle?si:pi;if(rand){let k=j+rand(A.length-j);[A[j],A[k]]=[A[k],A[j]];ct.swaps++}let z=A[j];if(isSingle)si++;else pi++;turn++;yield z}}
let found=false;
for(let cand of order()){ct.candidates++;let z=cand.g?testPair(F,D,cand.g,r,ct,cap):testOne(F,D,cand.v,r,ct,cap,mode!=="pair");if(!z)continue;
if(z.kind==="split"){proof.push(z);terminal="UNSAT";found=true;break}
if(z.kind==="learn"){let k=key(z.g);if(seen.has(k))continue;seen.add(k);F.push(clauseFactor(z.g,100000+learned));D.push(F.at(-1).mask);learned++}
else{let changes=[];for(let [i,ok] of z.changes){if(i>=orig)continue;let q=ok.reduce((s,w)=>s|(1n<<BigInt(w)),0n);if(q!==D[i]){removed+=pc(D[i])-pc(q);D[i]=q;changes.push([i,ok])}}if(!changes.length)continue;z.changes=changes}
proof.push(z);if(!first)first={visits:ct.visits,candidates:ct.candidates,kind:z.kind};found=true;break}
if(terminal==="UNSAT"||!found)break}
}catch(e){if(e.message!=="CAP")throw e;terminal="UNKNOWN_CAP"}
return{mode,seed,terminal,ct,proof,removed,learned,epochs,first}}
function verify(initial,r,res){let F=initial.map(f=>({vs:f.vs,ok:decode(f.mask)})),rows=0,scans=0,checks=0,orig=F.length;function cl(g){let A=new Map(g);if(A.size!==g.length)throw Error("duplicate guard");for(;;){let again=false,S=[];for(let i=0;i<F.length;i++){scans++;let f=F[i],q=[];for(let w of f.ok){rows++;let hit=true;for(let j=0;j<f.vs.length;j++)if(A.has(f.vs[j])&&A.get(f.vs[j])!==(w>>j&1)){hit=false;break}if(hit)q.push(w)}if(!q.length)return null;S.push(q);for(let j=0;j<f.vs.length;j++){let v=f.vs[j];if(A.has(v))continue;let b=q[0]>>j&1;if(q.every(w=>(w>>j&1)===b)){A.set(v,b);again=true;break}}if(again)break}if(!again)return S}}
let terminal=false;for(let z of res.proof){checks++;if(z.kind==="root"){if(cl([]))throw Error("bad root");terminal=true;break}if(z.kind==="learn"){if(cl(z.g))throw Error("bad learned guard");let f=clauseFactor(z.g,F.length);F.push({vs:f.vs,ok:decode(f.mask)});continue}let a=cl([[z.v,0]]),b=cl([[z.v,1]]);if(z.kind==="split"){if(a||b)throw Error("bad split");terminal=true;break}if(z.kind!=="rows")throw Error("proof kind");for(let [i,ok] of z.changes){if(i>=orig||ok.some(w=>!F[i].ok.includes(w)))throw Error("bad table");for(let q of [a,b])if(q&&q[i].some(w=>!ok.includes(w)))throw Error("discarded row");F[i].ok=ok}}
if(terminal!==(res.terminal==="UNSAT"))throw Error("terminal mismatch");return{terminal,rows,scans,checks}}
function census(F,r){let D=F.map(f=>f.mask),ct={visits:0,filters:0,forceChecks:0,probes:0},P=close(F,D,[],r,ct,10000000),live=Array.from(P.P).map((v,i)=>v===-1?i:-1).filter(v=>v>=0),one=0,pair=0,totalPair=0,split=0;
for(let v of live){let z=testOne(F,D,v,r,ct,10000000,true);if(z){one++;if(z.kind==="split")split++}}
for(let i=0;i<live.length;i++)for(let j=i+1;j<live.length;j++)for(let a=0;a<2;a++)for(let b=0;b<2;b++){totalPair++;if(testPair(F,D,[[live[i],a],[live[j],b]],r,ct,10000000))pair++}
return{live:live.length,singleProductive:one,singleTotal:live.length,singleConflict:split,pairProductive:pair,pairTotal:totalPair,ct}}
function doCase(F,ids,includeAll){let r=ids.length,rows=F.reduce((s,f)=>s+pc(f.mask),0),root=census(F,r),runs=[];let modes=includeAll?["balanced","priority"]:["balanced"];for(let mode of modes){for(let seed of [null,...(includeAll?seeds:[1,2,3])]){let a=discover(F,r,mode,seed),v=verify(F,r,a);runs.push({...a,verify:v})}}return{r,ids,rows,root,runs}}
function hostileControl(){
 // All sixteen forbidden words on four variables; the source CNF is UNSAT by direct cover.
 let dimacs="p cnf 4 16\n"+Array.from({length:16},(_,w)=>[1,2,3,4].map((v,i)=>(w>>i&1)?-v:v).join(" ")+" 0\n").join("");
 let cf=Array.from({length:16},(_,w)=>({id:w,vs:[1,2,3,4],ok:Array.from({length:16},(_,i)=>i).filter(i=>i!==w)}));let d=fromTables(cf),exact=census(d.F,4),control=discover(d.F,4,"balanced",1),check=verify(d.F,4,control);
 for(let w=0;w<16;w++)if(cf.every(f=>f.ok.includes(w)))throw Error("control label");
 let g=compile({nvars:4,dimacs}),s=JSON.stringify(g.network)+"\n",m=JSON.stringify(g.source_map)+"\n",D=normalize(g.network),I=independentNormalize(g.network);if(JSON.stringify(D.fs)!==JSON.stringify(I.fs))throw Error("control normalize");if(!D.fs.every(f=>f.ok.every(w=>f.ok.includes(w^(2**f.vs.length-1)))))throw Error("gauge");
 let id=gauge(D.fs);const pin=(F,v)=>F.map(f=>{let i=f.vs.indexOf(v);if(i<0)return f;return{...f,vs:f.vs.filter(x=>x!==v),ok:f.ok.filter(w=>!(w>>i&1)).map(w=>(w&((1<<i)-1))|((w>>(i+1))<<i))}});
 let E=eliminate(pin(D.fs,id),false),V=verifyTrace(pin(I.fs,id),E.trace);if(JSON.stringify(E.fs)!==JSON.stringify(V.fs))throw Error("control projection");let n=fromTables(V.fs),nc=census(n.F,n.ids.length),nr=discover(n.F,n.ids.length,"balanced",1),nv=verify(n.F,n.ids.length,nr);
 let assignments=0;for(let w=0;w<2**n.ids.length;w++){if(n.F.every(f=>Boolean(f.mask&(1n<<BigInt(f.vs.reduce((a,v,i)=>a+((w>>v&1)<<i),0))))))assignments++}if(assignments!==0)throw Error("native control label");
 return{model:"STRICT-EB4-v1",nativeId:"STRICT-EB4-v1:sha256:"+sha(s),nativeSha:sha(s),N:8*s.length,sourceMapSha:sha(m),dimacs,cnfId:"DIMACS-CNF-v1:sha256:"+sha(dimacs),cnfN:8*dimacs.length,original_ids:{vertices:[0,g.network.types.length-1],ports:[0,4*g.network.types.length-1],edges:[0,g.network.edges.length-1]},gauge:id,trace:E.trace,chartIds:n.ids,rootFactors:V.fs,cnf:{exact,control,check},native:{exact:nc,control:nr,check:nv,referenceAssignments:2**n.ids.length,solutions:assignments}}
}
function fromTables(fs){let ids=[...new Set(fs.flatMap(f=>f.vs))].sort((a,b)=>a-b),ix=new Map(ids.map((v,i)=>[v,i]));return{F:fs.map(f=>factor(f.vs.map(v=>ix.get(v)),f.ok,f.id)),ids}}
for(let name of ["JOINT-24","RANDOM-3CNF-40"]){let x=B.instances.find(z=>z.id===name),e=R.instances.find(z=>z.alias==="EB-"+name),g=compile(x),s=JSON.stringify(g.network)+"\n",m=JSON.stringify(g.source_map)+"\n";if(sha(s)!==e.sha256||8*s.length!==e.N_bits||sha(x.dimacs)!==e.source_cnf.sha256||8*x.dimacs.length!==e.source_cnf.N_bits||sha(m)!==e.source_map_sha256)throw Error("identity");
let D=normalize(g.network),I=independentNormalize(g.network);if(JSON.stringify(D.fs)!==JSON.stringify(I.fs))throw Error("normalizer");
if(!D.fs.every(f=>f.ok.every(w=>f.ok.includes(w^(2**f.vs.length-1)))))throw Error("gauge");let id=gauge(D.fs);const pin=(F,v)=>F.map(f=>{let i=f.vs.indexOf(v);if(i<0)return f;return{...f,vs:f.vs.filter(x=>x!==v),ok:f.ok.filter(w=>!(w>>i&1)).map(w=>(w&((1<<i)-1))|((w>>(i+1))<<i))}});
let E=eliminate(pin(D.fs,id),false),V=verifyTrace(pin(I.fs,id),E.trace);if(JSON.stringify(E.fs)!==JSON.stringify(V.fs))throw Error("projection");
let {F,ids}=fromTables(V.fs);let native=doCase(F,ids,true);
let cf=x.dimacs.trimEnd().split("\n").slice(1).map((l,id)=>{let c=l.split(/\s+/).map(Number).slice(0,-1),vs=[...new Set(c.map(Math.abs))].sort((a,b)=>a-b),ok=[];for(let w=0;w<2**vs.length;w++)if(c.some(l=>((w>>vs.indexOf(Math.abs(l)))&1)===+(l>0)))ok.push(w);return{id,vs,ok}}),cn=fromTables(cf),cnf={skipped:"direct CNF comparator in previous pinned run; this experiment changes only native scheduling"};
out[name]={instance:e.short_id,instance_id:e.instance_id,N:e.N_bits,source_cnf:e.source_cnf,original_ids:{vertices:[0,g.network.types.length-1],ports:[0,4*g.network.types.length-1],edges:[0,g.network.edges.length-1]},gauge:id,trace:E.trace,normalization:{arcs:D.arcs,local:D.local,independent:I.counts},projection:{steps:E.trace.length,checks:E.checks,scans:E.scans,verifyTests:V.tests,verifyScans:V.scans},native,cnf};}
return{cap:CAP,seeds,out,hostile:hostileControl()}
}
if(typeof module!=="undefined"){module.exports={run};if(require.main===module){const fs=require("node:fs");console.log(JSON.stringify(run(...process.argv.slice(2).map(p=>fs.readFileSync(p,"utf8")))))}}
