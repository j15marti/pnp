/* LSPV-3/558 | polynomial-size source-bound canonical fixture builder.
   Exact scope: recovered /341 SOURCE/AND3/XOR cubic fixture checker, NOT full R_mix341.
   Run from j15marti/pnp repository root: node experiments/arc/lspv3_558_external_source_canonical.cjs
*/
"use strict";
function insist(t,m){if(!t)throw Error(m)}
function litSat(c,a){return c.some(x=>a[Math.abs(x)-1]===(x>0?1:0))}
function formatCNF(f){return "p cnf "+f.graph.edges.length+" "+f.clauses.length+"\n"+f.clauses.map(c=>c.literals.join(" ")+" 0").join("\n")+"\n"}
function parseCNF(s){insist(typeof s==="string","external source not string");
 const z=s.trim().split(/\s+/),h=z.slice(0,4); insist(h[0]==="p"&&h[1]==="cnf"&&/^\d+$/.test(h[2])&&/^\d+$/.test(h[3]),"header");
 const n=Number(h[2]),m=Number(h[3]);insist(Number.isSafeInteger(n)&&Number.isSafeInteger(m),"header range");
 let a=[],cl=[];for(const q of z.slice(4)){insist(/^-?\d+$/.test(q),"literal token");const k=Number(q);insist(Number.isSafeInteger(k),"unsafe integer");if(k===0){insist(cl.length===3&&new Set(cl.map(Math.abs)).size===3,"not proper 3CNF");a.push(cl);cl=[]}else{insist(Math.abs(k)<=n&&k!==0,"literal range");cl.push(k)}}insist(!cl.length&&a.length===m,"source counts");return {n,clauses:a}}
function validateGraph(g){insist(Number.isSafeInteger(g.n)&&g.n>=4&&g.n%2===0,"V");
 const V=g.n,E=g.edges.length;insist(2*E===3*V,"cubic size");
 const inc=Array.from({length:V},()=>[]),seen=new Set();
 for(let i=0;i<E;i++){const [u,v]=g.edges[i];insist(Number.isSafeInteger(u)&&Number.isSafeInteger(v)&&u>=0&&v>=0&&u<V&&v<V&&u!==v,"edge");
 const key=Math.min(u,v)+":"+Math.max(u,v);insist(!seen.has(key),"multi-edge");seen.add(key);inc[u].push(i);inc[v].push(i)}
 insist(inc.every(a=>a.length===3),"degree");
 const seenV=new Set([0]),q=[0];for(let j=0;j<q.length;j++)for(const e of inc[q[j]]){const [u,v]=g.edges[e];const w=u===q[j]?v:u;if(!seenV.has(w)){seenV.add(w);q.push(w)}}
 insist(seenV.size===V,"connected");return inc}
function solve(g,charges,pins={},skip=-1){const E=g.edges.length,V=g.n;
 const basis=Array(E).fill(null),one=1n;
 for(let v=0;v<V;v++){if(v===skip)continue;let mask=0n,rhs=charges[v];
 for(let e=0;e<E;e++){const [a,b]=g.edges[e];if(a!==v&&b!==v)continue;
 if(Object.prototype.hasOwnProperty.call(pins,e))rhs^=pins[e];else mask|=(one<<BigInt(e))}
 for(let e=0;e<E&&mask!==0n;e++){if(!(mask&(one<<BigInt(e))))continue;
 if(basis[e]){mask^=basis[e].mask;rhs^=basis[e].rhs}else{basis[e]={mask,rhs};break}}
 if(mask===0n&&rhs)return null}
 const ans=Array(E).fill(0);for(const [k,v] of Object.entries(pins))ans[Number(k)]=v;
 for(let e=E-1;e>=0;e--)if(basis[e]){let x=basis[e].rhs;for(let j=e+1;j<E;j++)if(basis[e].mask&(one<<BigInt(j)))x^=ans[j];ans[e]=x}
 for(let v=0;v<V;v++)if(v!==skip){let p=0;for(let e=0;e<E;e++)if(g.edges[e].includes(v))p^=ans[e];insist(p===charges[v],"GF2 witness")}
 return ans}
function canonicalFixture(f,externalDIMACS){
 const source=parseCNF(externalDIMACS),g=f.graph,inc=validateGraph(g),V=g.n,E=g.edges.length;
 insist(source.n===E&&source.clauses.length===4*V,"external size");
 insist(Array.isArray(f.charges)&&f.charges.length===V&&f.charges.every(x=>typeof x==="number"&&(x===0||x===1)),"G2 charge");
 insist(f.charges.reduce((a,b)=>a^b,0)===1,"charge parity");
 insist(f.clauses.length===4*V,"fixture length");
 const groups=Array.from({length:V},()=>[]),sourceNodes=[];
 for(let i=0;i<4*V;i++){const c=f.clauses[i],lits=source.clauses[i];
 insist(JSON.stringify(c.literals)===JSON.stringify(lits),"G1 signed external source");
 const v=c.vertex;insist(Number.isSafeInteger(v)&&v>=0&&v<V,"vertex");
 insist(lits.length===3&&lits.every(x=>inc[v].includes(Math.abs(x)-1)),"source incidence");
 const pattern=inc[v].reduce((sum,e,j)=>sum|((lits.find(x=>Math.abs(x)===e+1)<0?1:0)<<j),0);
 const parity=((pattern&1)^((pattern>>1)&1)^((pattern>>2)&1));
 insist(parity!==f.charges[v],"source parity");
 const rec={id:"s"+i,vertex:v,pattern,literals:lits.slice()};groups[v].push(rec);
 let table=0;for(let z=0;z<8;z++){let a=Array(E).fill(0);inc[v].forEach((e,j)=>a[e]=(z>>j)&1);if(litSat(lits,a))table|=1<<z}
 sourceNodes.push({id:rec.id,kind:"factor",support:inc[v],table});
 }
 insist(groups.every(x=>x.length===4&&new Set(x.map(y=>y.pattern)).size===4),"missing local clause");
 const map=new Map(sourceNodes.map(x=>[x.id,x])),proof=[],rows=[];
 for(let v=0;v<V;v++){let cur=map.get(groups[v][0].id);
 for(let j=1;j<4;j++){const b=map.get(groups[v][j].id);
 const p={id:"d"+proof.length,kind:"factor",rule:"AND3",parents:[cur.id,b.id],support:inc[v].slice(),table:cur.table&b.table};
 proof.push(p);cur=p}
 const mask=inc[v].reduce((m,e)=>m|(1n<<BigInt(e)),0n);
 let expected=0;for(let z=0;z<8;z++)if((((z&1)^((z>>1)&1)^((z>>2)&1)))===f.charges[v])expected|=1<<z;
 insist(cur.table===expected,"factor row");cur.row={mask:"0x"+mask.toString(16),rhs:f.charges[v]};rows.push(cur)}
 let acc=rows[0],mask=BigInt(acc.row.mask),rhs=acc.row.rhs;
 for(let j=1;j<rows.length;j++){mask^=BigInt(rows[j].row.mask);rhs^=rows[j].row.rhs;
 const p={id:"d"+proof.length,kind:"affine",rule:"XOR",parents:[acc.id,rows[j].id],row:{mask:"0x"+mask.toString(16),rhs}};proof.push(p);acc=p}
 insist(mask===0n&&rhs===1&&proof.length===4*V-1,"terminal contradiction");
 const clauses=groups.flat().sort((a,b)=>Number(a.id.slice(1))-Number(b.id.slice(1)));
 const deleted=[];let essential=0;
 for(const c of clauses){const pins={};inc[c.vertex].forEach((e,j)=>pins[e]=(c.pattern>>j)&1);
 const a=solve(g,f.charges,pins,c.vertex);if(a)essential++;
 deleted.push({sourceId:c.id,assignment:a?a.join(""):null})}
 const graph={name:"CANON_G"+V,n:V,edges:g.edges.map(a=>a.slice())};
 return {graph,charges:f.charges.slice(),clauses,proof,deleted,evenWitness:"0".repeat(E),
 properties:{variables:E,sourceClauses:4*V,inferences:4*V-1,essential,oddUnsat:true,evenSat:true,predictedMinimum:essential===4*V?4*V-1:null}}
}
function packetFor(f){return {version:"LSPV2-MIXED-TSEITIN-MINDAG341/v1",definition:"source-only rebuilt G0/G1/G2 canonical SOURCE/AND3/XOR proof",fixtures:[f],summary:[{name:f.graph.name,vertices:f.graph.n,variables:f.graph.edges.length,sourceClauses:f.clauses.length,inferences:f.proof.length}]}}
function runProducer(js){let out="";new Function("console",js)({log:x=>{out=x}});return JSON.parse(out)}
function runChecker(js,o){let out="";const fs={readFileSync:()=>JSON.stringify(o)};
 new Function("require","process","console",js)(n=>{insist(n==="fs","unrecognized module");return fs},{argv:["node","checker","packet"]},{log:x=>{out=x}});
 return JSON.parse(out)}
function audit(producerSrc,checkerSrc,k4IndependentDIMACS){
 const orig=runProducer(producerSrc),rows=[];let total=0;
 for(const sourceFix of orig.fixtures){
 const external=(sourceFix.graph.name==="K4"&&k4IndependentDIMACS!==undefined)?k4IndependentDIMACS:formatCNF(sourceFix),canonical=canonicalFixture(sourceFix,external),packet=packetFor(canonical);
 const verdict=runChecker(checkerSrc,packet),byteCount=JSON.stringify(packet).length;
 insist(verdict.checks>0&&verdict.cases.length===1,"canonical rejected");total+=verdict.checks;
 const corrupted=JSON.parse(JSON.stringify(sourceFix));corrupted.proof[0].table^=1;
 const rerun=canonicalFixture(corrupted,external);insist(JSON.stringify(rerun)===JSON.stringify(canonical),"proof dependence");
 const decorated=packetFor(canonical);decorated.fixtures[0].ignoredMetadata="x".repeat(40000);
 insist(runChecker(checkerSrc,decorated).checks===verdict.checks,"metadata input rejected");
 const opposite=formatCNF(sourceFix).replace(/([1-9]\d*) 0/, "0");let mismatch=false;try{canonicalFixture(sourceFix,opposite)}catch(e){mismatch=true}insist(mismatch,"external substitution accepted");
 const malformed=JSON.parse(JSON.stringify(sourceFix));malformed.charges[0]=String(malformed.charges[0]);
 let guarded=false;try{canonicalFixture(malformed,external)}catch(e){guarded=true}insist(guarded,"string charge accepted");
 const W=4*canonical.graph.n-1;insist(canonical.proof.length===W,"cost");
 rows.push({graph:sourceFix.graph.name,V:sourceFix.graph.n,E:sourceFix.graph.edges.length,
 sourceBits:external.length*8,outputBytes:byteCount,paidNodes:W,independentVerifierChecks:verdict.checks,
 essential:canonical.properties.essential,sourceMismatchRejected:mismatch,chargeTypeRejected:guarded,
 corruptProofIgnored:true,ignoredMetadataBytes:40000})}
 return {theorem:"source-only canonical G0-G1-G2 fixture construction, not full Rmix341",cases:rows.length,totalOriginalBodyAssertions:total,rows,
 execution:"pinned original producer/checker bodies in V8, only fs/console I/O adapted",
 limits:"Source input must be separately authenticated proper cubic Tseitin DIMACS and graph/charge witnesses; no full RES, DEF, LOCAL-CONVERT or branch grammar."}}
module.exports={audit,canonicalFixture,packetFor,formatCNF,parseCNF};
if(require.main===module){
 const fs=require("fs"),path=require("path");
 const base=process.cwd(),a=fs.readFileSync(path.join(base,"experiments/arc/lspv2_341_mixed_tseitin_min_dag.js"),"utf8"),
 b=fs.readFileSync(path.join(base,"experiments/arc/lspv2_341_independent_verify.js"),"utf8");
 const independent=fs.readFileSync(path.join(base,"results/raw/arc/2026-11-10_1824_LSPV3_558_K4_EXTERNAL.cnf"),"utf8");
 console.log(JSON.stringify(audit(a,b,independent),null,2));
}