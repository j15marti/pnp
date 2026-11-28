const fs=require('node:fs');
const pins={
  "compiler": [
    "research/coordination/shared-eb-2026-11-27/compile.js",
    "21b9d53fb8166c819b24e708656c742cd3c24f10"
  ],
  "corpus": [
    "research/coordination/shared-unsat-2026-11-27/benchmarks.json",
    "e315349cd6c1fe3fa696504859f28312f6aab69a"
  ],
  "reg": [
    "research/coordination/shared-eb-2026-11-27/instance-registry-v1.json",
    "0c14cdc57925788cf7a451dcd5aa171dce860f2c"
  ],
  "chart": [
    "research/proof-spine-2026-11-26/algebraic-geometric-closure/2026-11-27_1552_T2_hall_syzygy/native-chart.js",
    "52cae4a54513a67dd9468c7e3ee597cf317d67a3"
  ],
  "hash": [
    "research/coordination/2026-11-27_2300_UCAC_review/gauge-lift.js",
    "4a42c99a37a2a22c1ac36ed204eadce7dfa77908"
  ],
  "joint": [
    "research/hcl201/synthesis/2026-11-27_T4_gauge_factorial/JOINT-24.cert.json",
    "eb3eb5f2098fbfa73cd11540ba270ac997438f78"
  ],
  "random": [
    "research/hcl201/synthesis/2026-11-27_T4_gauge_factorial/RANDOM-3CNF-40.cert.json",
    "f96bea02c40c7545eb32c7fd5ac37afac7e436e8"
  ]
};
function run(d,pins){
const sha=new Function(d.hash.slice(d.hash.indexOf("function sha("),d.hash.indexOf("if(require.main"))+";return sha")(), enc=x=>JSON.stringify(x)+"\n";
if(sha("")!=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"||sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("hash");
const compile=new Function(d.compiler.slice(d.compiler.indexOf("function compile"),d.compiler.indexOf("function auditLocal"))+";return compile")(),{project,verifyProjection,adapter,up,solve,replay}=new Function(d.chart.slice(d.chart.indexOf("const key="),d.chart.indexOf("function checkHall"))+";return {project,verifyProjection,adapter,up,solve,replay}")();
const parity=x=>{let p=0;while(x){p^=1;x&=x-1}return p},key=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(",");
function basis(rows){let b=[];for(let x of rows){for(let y of b)x=Math.min(x,x^y);if(x){b.push(x);b.sort((a,b)=>b-a)}}return b}
function region(F,v,extra=[]){const inc=F.filter(c=>c.some(l=>Math.abs(l)===v)),scope=[...new Set(inc.flat().map(Math.abs))].sort((a,b)=>a-b),boundary=scope.filter(x=>x!==v),S=new Set(scope),local=F.filter(c=>c.every(l=>S.has(Math.abs(l)))),E=extra.filter(c=>c.every(l=>S.has(Math.abs(l)))),R=[...local,...E],exterior=F.filter(c=>!local.includes(c)),sz=2**boundary.length;if(scope.length>12)throw Error("width");
let checks=0,words=new Int32Array(sz),witness=new Int8Array(sz).fill(-1),map=new Map(boundary.map((x,i)=>[x,i]));
const sat=(c,m,b)=>c.some(l=>{checks++;return (Math.abs(l)===v?b:(m>>map.get(Math.abs(l)))&1)===Number(l>0)});
for(let m=0;m<sz;m++)for(let b=0;b<2;b++)if(R.every(c=>sat(c,m,b))){words[m]=1;if(witness[m]<0)witness[m]=b}
const support=Array.from(words).reduce((a,b)=>a+b,0),W=Int32Array.from(words);let butterflies=0;for(let h=1;h<sz;h*=2)for(let a=0;a<sz;a+=2*h)for(let j=a;j<a+h;j++){let x=W[j],y=W[j+h];W[j]=x+y;W[j+h]=x-y;butterflies++}
const freqs=Array.from(W).map((c,i)=>[i,c]).filter(([i,c])=>c!==0),B=basis(freqs.map(([i,c])=>i));let code=m=>B.reduce((z,b,i)=>z|(parity(m&b)<<i),0),Q=new Map();for(let m=0;m<sz;m++){let q=code(m);if(Q.has(q)&&Q.get(q)!==words[m])throw Error("quotient mismatch");Q.set(q,words[m])}
let r0=R.filter(c=>!c.some(l=>Math.abs(l)===v)),plus=R.filter(c=>c.includes(v)),minus=R.filter(c=>c.includes(-v)),pairs=0,D=new Map(r0.map(c=>[key(c),c]));for(let a of plus)for(let b of minus){pairs++;let c=[...new Set([...a.filter(l=>l!==v),...b.filter(l=>l!==-v)])];if(c.some(l=>c.includes(-l)))continue;D.set(key(c),c)}let C=[...D.values()].sort((a,b)=>a.length-b.length),J=[];for(let c of C)if(!J.some(a=>a.every(l=>c.includes(l))))J.push(c);
let bveCheck=0;for(let m=0;m<sz;m++){let good=J.every(c=>c.some(l=>{bveCheck++;return ((m>>map.get(Math.abs(l)))&1)===Number(l>0)}));if(good!==Boolean(words[m]))throw Error("BVE mismatch")}
const T=solve([...exterior,...J]),V=replay([...exterior,...J],T.tree);if(V.nodes!==T.nodes)throw Error("replay");
return {v,originalPort:v-1,scope,boundary,localRows:local.length,extra:E,exteriorRows:exterior.length,support,checks,butterflies,nonzero:freqs.length,rank:B.length,basis:B,response:[...Q],spectrum:freqs,projectionWitness:Array.from(witness),bve:J,bvePairs:pairs,bveCheck,proof:T,replay:V};
}
function rup(F,P){let R=F.slice(),visits=0;for(let c of P){let U=up(R,c.map(l=>[Math.abs(l),Number(l<0)]));visits+=U.work;if(!U.conflict)throw Error("RUP");R.push(c)}return visits}
function feedback(F){let vars=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),A=new Map(vars.map(v=>[v,0])),work=0;function score(){let bad=0,z=0;for(let c of F){let k=0,h=0;for(let l of c){work++;if(A.get(Math.abs(l))===Number(l>0)){k++;h+=Math.sign(l)}}if(!k)bad++;else if(h%3===0)z++}return [bad,z]}
const one=residue=>{for(let v of vars)A.set(v,0);let start=score(),cur=start,flips=[],changes=0;for(;;){let C=[];for(let v of vars){A.set(v,1-A.get(v));let s=score();A.set(v,1-A.get(v));if(s[0]<cur[0])C.push([v,...s])}if(!C.length)break;let base=C.slice().sort((a,b)=>a[1]-b[1]||a[0]-b[0])[0],best=C.sort((a,b)=>a[1]-b[1]||(residue?a[2]-b[2]:0)||a[0]-b[0])[0];if(base[0]!==best[0])changes++;A.set(best[0],1-A.get(best[0]));cur=score();flips.push(best[0]);if(work>1e6)break}return {start,end:cur,flips,changes}};return {table:one(false),residue:one(true),literalVisits:work}}
let cases=[];for(let name of ["joint","random"]){let C=JSON.parse(d[name]),R=JSON.parse(d.reg).instances.find(z=>z.instance_id===C.instance_id),x=JSON.parse(d.corpus).instances.find(z=>"EB-"+z.id===R.alias),G=compile(x),s=enc(G.network);if(sha(s)!==R.sha256||8*s.length!==R.N_bits||sha(x.dimacs)!==R.source_cnf.sha256||x.dimacs.length*8!==R.source_cnf.N_bits||sha(enc(G.source_map))!==R.source_map_sha256)throw Error("auth");let p=project(G.network),check=verifyProjection(G.network,p),F=p.clauses,U=up(F),root=solve(F),rootCheck=replay(F,root.tree),ad=adapter(p,G,x.dimacs,x.nvars),comp=solve(ad.orig),compCheck=replay(ad.orig,comp.tree),chartHash=sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),mapHash=sha(enc({root:p.root,phase:p.phase})),guard="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",R.instance_id,"EB-PORT-PINS-v1",sha(enc([[p.anchor,0]]))])),residual="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",R.instance_id,guard,"EB-CHART-SYZYGY-v1",chartHash,mapHash]));if(guard!==C.internal_guard||residual!==C.internal_residual||chartHash!==C.chartHash||mapHash!==C.mapHash)throw Error("residual");let vars=[...new Set(F.flat().map(Math.abs))],eligible=vars.map(v=>[v,new Set(F.filter(c=>c.some(l=>Math.abs(l)===v)).flat().map(Math.abs)).size]).filter(a=>a[1]<=12).sort((a,b)=>a[1]-b[1]||a[0]-b[0]);let v=eligible[0][0],stand=region(F,v),fb=feedback(F);let anchor=p.anchor+1,P=[];for(let c of C.proof){if(!c.includes(anchor))break;P.push(c.filter(l=>l!==anchor));if(!P.at(-1).length)break}if(P.at(-1)?.length!==0)throw Error("peer slice");
let visits=rup(F,P),seed=P.filter(c=>c.length&&c.every(l=>stand.scope.includes(Math.abs(l)))),hybrid=region(F,v,seed),removed=region(F,v,seed.slice(1));let entry={instance:R,sourcePins:pins,guard,residual,chartHash,mapHash,original_ids:C.original_ids,early:{pins:U.a.size,work:U.work},carrierCount:p.carriers,eliminations:p.steps.length,projectionDiscovery:p.cost,projectionReplay:check,root,rootCheck,comp,compCheck,eligible,stand,hybrid,removed,peer:{id:"CERT-v1:sha256:"+sha(d[name]),visits,seed},feedback:fb};entry.certificate_id="CERT-v1:sha256:"+sha(enc(entry));cases.push(entry)}
// 3-state nonlinear coupled seams. State j uses two response bits, each XOR of two private carriers.
// Cycle transfer map 0->1->2->0, state 3 illegal. DP plus direct enumeration on small response words.
let family=[];for(let k of [3,4,5,6,9,12,16,24,32,48,64]){let trans=[[0,1],[1,2],[2,0]],frontier=Array.from({length:3},(_,i)=>[i,i]),ops=0;for(let i=0;i<k;i++){let next=[];for(let [start,x] of frontier)for(let [a,b] of trans){ops++;if(x===a)next.push([start,b])}frontier=next}let support=frontier.filter(([a,b])=>a===b),count=support.length,exhaustive=null;if(k<=6){let hits=0;for(let m=0;m<4**k;m++){let good=true;for(let i=0;i<k;i++){let a=(m>>(2*i))&3,b=(m>>(2*((i+1)%k)))&3;if(a===3||b!==(a+1)%3){good=false;break}}if(good)hits++}if(hits!==count)throw Error("family count");exhaustive=hits}
let spec={format:"T2-XOR-SEAM-CYCLE-v1",k,states:[0,1,2],transition:trans,physicalCoordinates:4*k,encoding:"each of 2k response bits is XOR of its own two consecutive physical bits; all cycle transitions required"};let bytes=enc(spec),id="T2-XOR-SEAM-CYCLE-v1:sha256:"+sha(bytes);family.push({spec,id,N_bits:8*bytes.length,ops,count,exhaustive,exactPhysicalModels:(BigInt(count)*(1n<<BigInt(2*k))).toString(),nonzeroGlobalIndicatorWalsh:count?(1n<<BigInt(2*k)).toString():"0",witness:count?Array.from({length:k},(_,i)=>i%3):null})}
return {format:"T2-COUPLED-SEAMS-v1",pins,cases,family};
}
const d=Object.fromEntries(Object.keys(pins).map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]));console.log(JSON.stringify(run(d,pins),null,2));
