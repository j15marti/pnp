function ledgerAudit(c,b,r,h,p,raw){
const compile=Function(c.slice(c.indexOf("function compile"),c.indexOf("function auditLocal"))+";return compile")();
const {sha,normalize,independentNormalize,verifyTrace}=Function(h.slice(0,h.indexOf("// Node runner"))+";return {sha,normalize,independentNormalize,verifyTrace}")();
const B=JSON.parse(b),R=JSON.parse(r),P=JSON.parse(p),T=JSON.parse(raw),out={};
if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"||sha(p)!=="a1af0f81183d9681db016bbc2381e77273c04da3e16f93e7eb34bbc4de48dda9")throw Error("digest");
for(const name of ["JOINT-24","RANDOM-3CNF-40"]){
let x=B.instances.find(z=>z.id===name),e=R.instances.find(z=>z.alias==="EB-"+name),g=compile(x),s=JSON.stringify(g.network)+"\n",m=JSON.stringify(g.source_map)+"\n";
if(sha(s)!==e.sha256||8*s.length!==e.N_bits||sha(x.dimacs)!==e.source_cnf.sha256||8*x.dimacs.length!==e.source_cnf.N_bits||sha(m)!==e.source_map_sha256)throw Error("identity");
let a=normalize(g.network),i=independentNormalize(g.network);if(JSON.stringify(a.fs)!==JSON.stringify(i.fs))throw Error("map");
const id=T[name].gauge,pin=(F,v)=>F.map(f=>{let j=f.vs.indexOf(v);if(j<0)return f;return {...f,vs:f.vs.filter(x=>x!==v),ok:f.ok.filter(w=>!(w>>j&1)).map(w=>(w&((1<<j)-1))|((w>>(j+1))<<j))}});
if(!a.fs.every(f=>f.ok.every(w=>f.ok.includes(w^(2**f.vs.length-1)))))throw Error("gauge");
let F=verifyTrace(pin(i.fs,id),T[name].trace).fs,ids=[...new Set(F.flatMap(f=>f.vs))].sort((a,b)=>a-b),idx=new Map(ids.map((v,j)=>[v,j])),db=[],rows=[],stages=[],rankBasis=new Map(),dense=new Map(),cols=new Map(),work={sparseXor:0,denseXor:0,terms:0,expansionChecks:0};
function toggle(S,x){S.has(x)?S.delete(x):S.add(x)}
function addPoly(poly,desc){let A=new Set(poly),D=0n;for(let u of A){if(!cols.has(u))cols.set(u,cols.size);D^=1n<<BigInt(cols.get(u))}let orig=rows.length;rows.push(desc);work.terms+=A.size;
let cert=1n<<BigInt(orig);while(A.size){let q=[...A].reduce((a,b)=>a>b?a:b);if(!rankBasis.has(q)){rankBasis.set(q,[A,cert]);break}let [S,c]=rankBasis.get(q);for(let z of S){toggle(A,z);work.sparseXor++}cert^=c}
while(D){let q=D.toString(2).length-1;if(!dense.has(q)){dense.set(q,D);break}D^=dense.get(q);work.denseXor++}
if(rankBasis.size!==dense.size)throw Error("rank mismatch")}
function guard(vs,w,desc){let Q=new Set([0n]);for(let j=0;j<vs.length;j++){let u=1n<<BigInt(idx.get(vs[j])),A=new Set();for(let q of Q){if(!(w>>j&1))toggle(A,q);toggle(A,q|u)}Q=A}
for(let z=0;z<2**vs.length;z++){let val=0,word=vs.reduce((a,v,j)=>a|((z>>j&1)?1n<<BigInt(idx.get(v)):0n),0n);for(let q of Q)if((word&q)===q)val^=1;work.expansionChecks++;if(val!==+(z===w))throw Error("bad polynomial")}
addPoly(Q,desc)}
function constantProof(){let A=new Set([0n]),w=0n;while(A.size){let q=[...A].reduce((a,b)=>a>b?a:b);if(!rankBasis.has(q))return null;let [S,c]=rankBasis.get(q);for(let z of S)toggle(A,z);w^=c}let L=[];for(let j=0;j<rows.length;j++)if(w>>BigInt(j)&1n)L.push(j);return L}
function stage(name){stages.push({stage:name,rows:rows.length,rank:rankBasis.size,constantProof:constantProof()})}
for(let f of F){for(let w=0;w<2**f.vs.length;w++)if(!f.ok.includes(w))guard(f.vs,w,{factor:f.id,word:w,source:"original-forbidden"})}stage("initial");
let res=T[name].base;
if(name==="RANDOM-3CNF-40"){for(let z of P.proof.slice(0,6)){let vs=[...new Set(z.clause.map(Math.abs))].sort((a,b)=>a-b),w=vs.reduce((a,v,j)=>a|((z.clause.includes(-v)?1:0)<<j),0);guard(vs,w,{clause:z.clause,source:"checked-prefix"});let ok=Array.from({length:2**vs.length},(_,i)=>i).filter(i=>i!==w);F.push({vs,ok,id:100000+F.length-184})}stage("six-imports");res=T[name].imports["6"].a}
let D=F.map(f=>f.ok);
for(let j=0;j<res.steps.length;j++){let t=res.steps[j];if(!t.rows)break;
for(let i=0;i<F.length;i++)for(let w of D[i])if(!t.rows[i].includes(w))guard(F[i].vs,w,{factor:F[i].id,word:w,source:"checked-row-removal",step:j});
D=t.rows;stage("row-epoch-"+j)}
let last=constantProof();if(last){let Q=new Set();for(let j of last){let desc=rows[j],vs,w;if(desc.clause){vs=[...new Set(desc.clause.map(Math.abs))].sort((a,b)=>a-b);w=vs.reduce((a,v,i)=>a|((desc.clause.includes(-v)?1:0)<<i),0)}else{vs=F.find(f=>f.id===desc.factor).vs;w=desc.word}let A=new Set([0n]);for(let i=0;i<vs.length;i++){let u=1n<<BigInt(idx.get(vs[i])),R=new Set();for(let q of A){if(!(w>>i&1))toggle(R,q);toggle(R,q|u)}A=R}for(let q of A)toggle(Q,q)}if(Q.size!==1||!Q.has(0n))throw Error("proof replay")}
out[name]={instance_id:e.instance_id,N:e.N_bits,carrier_count:ids.length,carrier_ids:ids,width:Math.max(...F.map(f=>f.vs.length)),stages,work,columns:cols.size,rank:rankBasis.size,constantBeforeTerminal:last,descriptors:rows};
}
return out
}
if(typeof module!=="undefined"){module.exports={ledgerAudit};if(require.main===module){const fs=require("node:fs");console.log(JSON.stringify(ledgerAudit(...process.argv.slice(2).map(p=>fs.readFileSync(p,"utf8")))))}}
