const fs=require('fs');
const specs=[
  [
    "21b9d53fb8166c819b24e708656c742cd3c24f10",
    "research/coordination/shared-eb-2026-11-27/compile.js"
  ],
  [
    "e315349cd6c1fe3fa696504859f28312f6aab69a",
    "research/coordination/shared-unsat-2026-11-27/benchmarks.json"
  ],
  [
    "0c14cdc57925788cf7a451dcd5aa171dce860f2c",
    "research/coordination/shared-eb-2026-11-27/instance-registry-v1.json"
  ],
  [
    "a830475f2d7b927fe3897079af04ebb99c82106b",
    "research/hcl201/matching/2026-11-27_T1_hall_clause_feedback/experiment.js"
  ],
  [
    "0231a616afbf28cf297c6b9c3f7b509b48d2fe04",
    "research/hcl201/matching/2026-11-27_T1_hall_clause_feedback/JOINT-24-certificate.json"
  ],
  [
    "e4ade84c3056664411885a65e334a550bbc59c93",
    "research/hcl201/matching/2026-11-27_T1_hall_clause_feedback/RANDOM-3CNF-40-certificate.json"
  ]
];
function run(inputs){
 const [co,corpus,reg,base,...certs]=inputs;
 const compile=new Function(co.slice(co.indexOf("function compile("),co.indexOf("function auditLocal"))+";return compile;")();
 const fn=new Function(base.slice(0,base.indexOf("function runCase"))+";return {sha,normalize,independentNormalize,eliminate,verifyTrace,gauge};")();
 const {sha,normalize,independentNormalize,eliminate,verifyTrace,gauge}=fn, A=(b,m)=>{if(!b)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 A(sha("")==="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"&&sha("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","sha vectors");
 const registry=JSON.parse(reg),data=JSON.parse(corpus);
 const entries=registry.instances||registry.native_instances||Object.values(registry).find(x=>Array.isArray(x)&&x.some(y=>y.alias==="EB-JOINT-24"));
 function pin(F,v){return F.map(f=>{let i=f.vs.indexOf(v);if(i<0)return f;return {...f,vs:f.vs.filter(x=>x!==v),ok:f.ok.filter(w=>!(w>>i&1)).map(w=>(w&((1<<i)-1))|((w>>(i+1))<<i))}})}
 function fromClause(c,id){let vs=[...new Set(c.map(Math.abs))].sort((a,b)=>a-b);A(vs.length<=12,"scope cap");let ok=[];for(let w=0;w<2**vs.length;w++)if(c.some(l=>(w>>vs.indexOf(Math.abs(l))&1)===+(l>0)))ok.push(w);return {id,vs,ok}}
 function toCNF(F){let M=new Map();for(let f of F)for(let w=0;w<2**f.vs.length;w++)if(!f.ok.includes(w)){let c=f.vs.map((v,i)=>(w>>i&1)?-v:v);M.set(c.join(),c)}return [...M.values()]}
 function replay(C,proof){
  let Q=C.slice(),scans=0,lit=0;
  for(let r of proof){A(r.kind==="UP","unexpected proof rule");let p=new Map(r.clause.map(l=>[Math.abs(l),+(l<0)])),fail=false;
   for(;;){let change=false;for(let c of Q){scans++;let hit=false,u=[];for(let l of c){lit++;if(!p.has(Math.abs(l)))u.push(l);else if(p.get(Math.abs(l))===+(l>0)){hit=true;break}}if(hit)continue;if(!u.length){fail=true;break}if(u.length===1){p.set(Math.abs(u[0]),+(u[0]>0));change=true}}if(fail||!change)break}
   A(fail,"bad RUP");Q.push(r.clause);
  }return {scans,lit,valid:proof.at(-1).clause.length===0}
 }
 function lane(F,alg,cap=64,learn=true){
  let V=[...new Set(F.flatMap(f=>f.vs))].sort((a,b)=>a-b),n=V.length,ix=new Map(V.map((v,i)=>[v,i])),P=F.map(f=>({vs:f.vs.map(v=>ix.get(v)),ok:f.ok.slice()}));
  const bit=i=>1n<<BigInt(i),high=x=>x.toString(2).length-1, pair=Array.from({length:n},()=>Array(n));let D=n+1;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)pair[i][j]=pair[j][i]=D++;
  let stats={rowScans:0,localRows:0,xors:0,geCalls:0,multiplied:0,probes:0,rootRounds:0},ded=[],root=new Map(),events=[],initial=null;
  function ge(){let B=new Map();return {B,add(v){while(v){let i=high(v),b=B.get(i);if(b===undefined){B.set(i,v);return true}v^=b;stats.xors++}return false},red(v){let out=0n;while(v){let i=high(v),b=B.get(i);if(b===undefined){out|=bit(i);v^=bit(i)}else{v^=b;stats.xors++}}return out}}}
  function gac(a){for(;;){let ch=false,R=[];for(let f of P){let ok=f.ok.filter(w=>{stats.rowScans++;return f.vs.every((v,i)=>!a.has(v)||a.get(v)===(w>>i&1))});if(!ok.length)return null;for(let i=0;i<f.vs.length;i++){let v=f.vs[i],b=ok[0]>>i&1;if(!a.has(v)&&ok.every(w=>(w>>i&1)===b)){a.set(v,b);ch=true}}R.push(ok)}if(!ch)return R}}
  function quad(a,R){
   stats.geCalls++;let G=ge(),constant=1n;
   for(let [i,b]of a)G.add(bit(i+1)^(b?1n:0n));
   for(let fidx=0;fidx<P.length;fidx++){
    let f=P[fidx],free=f.vs.map((v,i)=>[v,i]).filter(([v])=>!a.has(v)),k=free.length;if(!k)continue;
    let cols=[0,...free.map(([v])=>v+1)],localPairs=[];for(let i=0;i<k;i++)for(let j=i+1;j<k;j++){localPairs.push([i,j]);cols.push(pair[free[i][0]][free[j][0]])}
    let L=ge();for(let w of R[fidx]){let z=1n;for(let i=0;i<k;i++)if(w>>free[i][1]&1)z|=bit(i+1);for(let t=0;t<localPairs.length;t++){let [i,j]=localPairs[t];if((w>>free[i][1]&1)&&(w>>free[j][1]&1))z|=bit(k+1+t)}L.add(z);stats.localRows++}
    // Nullspace: each nonpivot coordinate is chosen, pivot variables solved in increasing order.
    for(let j=0;j<cols.length;j++)if(!L.B.has(j)){let z=bit(j);for(let [p,w] of [...L.B].sort((a,b)=>a[0]-b[0])){let u=(w&z),par=0;while(u){par^=1;u&=u-1n}if(par)z|=bit(p)}let g=0n;for(let i=0;i<cols.length;i++)if(z&bit(i))g|=bit(cols[i]);G.add(g)}
   }
   let done=new Set();
   for(let epoch=0;epoch<=n;epoch++){
    if(G.red(constant)===0n)return {conflict:true,rank:G.B.size,forced:[]};
    let lin=[...G.B].filter(([p])=>p<=n).map(x=>x[1]),changed=false;
    for(let z of lin){let key=z.toString();if(done.has(key))continue;done.add(key);
     for(let j=0;j<n;j++)if(!a.has(j)){let p=0n;if(z&1n)p^=bit(j+1);for(let i=0;i<n;i++)if(z&bit(i+1))p^=bit(i===j?j+1:pair[i][j]);stats.multiplied++;if(G.add(p))changed=true}
    }if(!changed)break;
   }
   if(G.red(1n)===0n)return {conflict:true,rank:G.B.size,forced:[]};
   let c=G.red(1n),forced=[],same=0;
   let r=V.map((_,i)=>G.red(bit(i+1)));for(let i=0;i<n;i++)if(!a.has(i)){if(r[i]===0n||r[i]===c)forced.push([i,+(r[i]===c)]);for(let j=0;j<i;j++)if(!a.has(j)&&(r[i]===r[j]||(r[i]^r[j])===c))same++}
   return {conflict:false,rank:G.B.size,forced,same};
  }
  function close(a){for(;;){if(stats.rowScans+stats.xors+stats.localRows>10000000)throw Error("event cap");let R=gac(a);if(!R)return {conflict:true,how:"GAC"};if(!alg)return {conflict:false,how:"GAC"};let q=quad(a,R);if(q.conflict)return {conflict:true,how:"quadratic",rank:q.rank};if(!q.forced.length)return {conflict:false,how:"quadratic",rank:q.rank,same:q.same};for(let [i,b]of q.forced)a.set(i,b)}}
  try{
   while(true){stats.rootRounds++;let r=close(root);if(!initial)initial={...r,rootPins:root.size};if(r.conflict)return {status:"UNSAT",n,D,initial,rootPins:root.size,ded,events,stats};
    if(root.size===n){let ok=P.every(f=>f.ok.includes(f.vs.reduce((w,v,i)=>w|(root.get(v)<<i),0)));A(ok,"bad complete word");return {status:"SAT",n,D,initial,rootPins:root.size,ded,events,stats}}
    if(!learn)return {status:"UNKNOWN",n,D,initial,rootPins:root.size,ded,events,stats};
    let found=false,order=V.map((_,i)=>i).filter(i=>!root.has(i)).sort((a,b)=>P.filter(f=>f.vs.includes(b)).length-P.filter(f=>f.vs.includes(a)).length||a-b);
    for(let i of order){for(let b=0;b<=1;b++){if(stats.probes>=cap)return {status:"UNKNOWN",reason:"probe cap",n,D,initial,rootPins:root.size,ded,events,stats};stats.probes++;let p=new Map(root);p.set(i,b);let t=close(p);if(t.conflict){root.set(i,1-b);ded.push([V[i],1-b]);events.push({pin:[V[i],b],how:t.how,rank:t.rank});found=true;break}}if(found)break}
    if(!found)return {status:"UNKNOWN",reason:"singleton fixed point",n,D,initial,rootPins:root.size,ded,events,stats}
   }
  }catch(e){if(String(e).includes("event cap"))return {status:"UNKNOWN",reason:"event cap",n,D,initial,rootPins:root.size,ded,events,stats};throw e}
 }
 let shared=[];
 for(let k=0;k<2;k++){
  let id=["JOINT-24","RANDOM-3CNF-40"][k],x=data.instances.find(z=>z.id===id),entry=entries.find(e=>e.alias==="EB-"+id),g=compile(x),native=JSON.stringify(g.network)+"\n",map=JSON.stringify(g.source_map)+"\n";
  A(sha(native)===entry.sha256&&native.length*8===entry.N_bits&&sha(x.dimacs)===entry.source_cnf.sha256&&x.dimacs.length*8===entry.source_cnf.N_bits&&sha(map)===entry.source_map_sha256,"instance mismatch");
  let d=normalize(g.network),i=independentNormalize(g.network);A(eq(d.fs,i.fs),"native normalization mismatch");let v=gauge(d.fs),E=eliminate(pin(d.fs,v),false),B=verifyTrace(pin(i.fs,v),E.trace);A(eq(E.fs.map(f=>[f.id,f.vs,f.ok]),B.fs.map(f=>[f.id,f.vs,f.ok])),"trace mismatch");
  // Source-only lanes before consuming the certificate.
  let baseline=lane(B.fs,false),quad=lane(B.fs,true),cnf=x.dimacs.trimEnd().split("\n").slice(1).map((l,i)=>fromClause(l.split(/\s+/).map(Number).slice(0,-1),i)),provenance=lane(cnf,true);
  let raw=certs[k],cert=JSON.parse(raw);A(cert.instance_id===entry.instance_id&&cert.guard_id==="EMPTY"&&cert.residual_id==="ROOT"&&cert.gauge===v&&eq(cert.trace,E.trace),"peer source/trace mismatch");let digest=sha(raw),expected=["75fb830677e51f8bd73b3e77510d7a1eae057a269aae4e333f30f654b2ee7c4b","a1af0f81183d9681db016bbc2381e77273c04da3e16f93e7eb34bbc4de48dda9"][k];A(digest===expected,"peer certificate digest mismatch");
  let rep=replay(toCNF(B.fs),cert.proof);A(rep.valid,"peer proof incomplete");let prefix=cert.proof.slice(0,3).map((r,j)=>fromClause(r.clause,-j-1));let hybridBase=lane([...B.fs,...prefix],false),hybridQuad=lane([...B.fs,...prefix],true);
  shared.push({id,entry,source:{nativeDigest:sha(native),nativeBits:native.length*8,cnfDigest:sha(x.dimacs),mapDigest:sha(map),arcs:d.arcs,local:d.local,independent:i.counts,projection:{count:E.trace.length,checks:E.checks,words:E.words,scans:E.scans,verifyTests:B.tests,verifyScans:B.scans},gauge:v},baseline,quad,provenance,peer:{digest,bytes:raw.length,rep,prefix:cert.proof.slice(0,3)},hybridBase,hybridQuad})
 }
 // SAT and UNSAT controls: three equations x+y=1,y+z=1,x+z=1 (inconsistent); drop third (SAT).
 let controls=[];for(let odd of [false,true]){let f=[[1,2],[2,3],...(odd?[[1,3]]:[])].map((vs,id)=>({id,vs,ok:[1,2]}));let q=lane(f,true),cnt=0;for(let w=0;w<8;w++)if(f.every(t=>t.ok.includes(t.vs.reduce((s,v,i)=>s|((w>>(v-1)&1)<<i),0))))cnt++;A((q.status==="UNSAT")===(cnt===0),"control label");controls.push({odd,cnt,q})}
 return {shared,controls};
}
const inputs=process.argv.slice(2).map(p=>fs.readFileSync(p,'utf8'));if(inputs.length!==specs.length)throw Error('six inputs in listed order');console.log(JSON.stringify(run(inputs),null,2));
