module.exports=function check(compile,corpus,registry,sha,raw){
const M=x=>(x%3+3)%3,enc=x=>JSON.stringify(x)+"\n";
function require(b,s){if(!b)throw Error(s)}
function chart(G){
let n=4*G.types.length,adj=Array.from({length:n},()=>[]),root=new Int32Array(n),phase=new Uint8Array(n),edgeVisits=0;
const add=(a,b,s)=>{adj[a].push([b,s]);adj[b].push([a,s])};
G.edges.forEach(e=>add(...e));G.types.forEach((t,v)=>{if(t==="E")for(let j=1;j<4;j++)add(4*v,4*v+j,0)});
for(let p=0;p<n;p++)if(!root[p]){root[p]=p+1;let q=[p];for(let a of q)for(let [b,s] of adj[a]){edgeVisits++;let x=phase[a]^s;if(!root[b]){root[b]=p+1;phase[b]=x;q.push(b)}else require(root[b]===p+1&&phase[b]===x,"parity cycle")}}
let g=root[10],gbit=phase[10],A=[],localChecks=0;
G.types.forEach((t,v)=>{if(t!=="B")return;let z=new Map,b=2;for(let j=0;j<4;j++){let p=4*v+j,x=root[p],s=phase[p];if(x===g)b-=s^gbit;else{b-=s;z.set(x,M((z.get(x)||0)+(s?-1:1)))}}let a=[...z].filter(x=>x[1]).sort((u,v)=>u[0]-v[0]),vars=[...new Set(Array.from(root.slice(4*v,4*v+4)))].filter(v=>v!==g);
for(let w=0;w<2**vars.length;w++){localChecks++;let x=new Map(vars.map((v,i)=>[v,(w>>i)&1])),sum=0;for(let j=0;j<4;j++){let p=4*v+j;sum+=(root[p]===g?gbit:x.get(root[p]))^phase[p]}require((sum===2)===(M(a.reduce((t,[v,c])=>t+c*x.get(v),0))===M(b)),"balance")}
A.push({a,b:M(b),id:v})});
return{A,root:Array.from(root),phase:Array.from(phase),g,gbit,edgeVisits,localChecks}}
function verify(A,H,run){
let B=new Map(),ops=0,maxTerms=0,membership=0,contractions=0,conflict=false;
function reduce(a,b){let q=new Map();for(let [v,k] of a)q.set(v,M((q.get(v)||0)+k));for(let [v,k] of q)if(!k)q.delete(v);b=M(b);while(q.size){let v=Math.max(...q.keys()),c=q.get(v);if(!B.has(v)){if(c===2){for(let [j,k] of q){q.set(j,M(2*k));ops++}b=M(2*b)}break}let r=B.get(v);for(let [j,k] of r.q){let s=M((q.get(j)||0)-c*k);if(s)q.set(j,s);else q.delete(j);ops++}b=M(b-c*r.b);ops++}maxTerms=Math.max(maxTerms,q.size);return{q,b}}
function insert(a,b){let r=reduce(a,b);if(!r.q.size)return r.b===0;B.set(Math.max(...r.q.keys()),r);return true}
function entails(a,b){membership++;let r=reduce(a,b);return !r.q.size&&r.b===0}
for(let r of A)require(insert(r.a,r.b),"root inconsistent unexpectedly");for(let l of H)require(insert([[Math.abs(l),1]],+(l>0)),"guard inconsistent unexpectedly");
function exclusion(a,f,v){return [1,2].some(c=>entails([[v,1],...a.map(([j,k])=>[j,-c*k])],2-c*f))}
for(let step of run.steps||[]){
require(step.rank===B.size,"rank mismatch");
for(let [v,b] of step.forced)require(entails([[v,1]],b),"wrong pin");
for(let r of step.newrows){let fs=r.witness.map(x=>x[0]);require(fs.length===2&&new Set(fs).size===2&&[0,1,2].includes(r.b)&&!fs.includes(r.b),"bad two exclusions");for(let [f,v] of r.witness)require(exclusion(r.a,f,v),"false exclusion")}
for(let r of step.newrows){contractions++;if(!insert(r.a,r.b))conflict=true}
}
if(run.status==="UNSAT"){
if(run.reason==="parallel-cover"){let c=run.cover;require(new Set(c.forbid.map(x=>x[0])).size===3,"not all values excluded");for(let [f,v] of c.forbid)require(exclusion(c.a,f,v),"bad terminal");conflict=true}
else if(run.reason==="nonBoolean"){require(entails([[run.coordinate,1]],2),"nonBoolean unsupported");conflict=true}
require(conflict,"unverified UNSAT")
}
return{verified:true,contradiction:conflict,ops,membership,contractions,maxTerms,rank:B.size}
}
let out=[];for(let r of raw){let x=corpus.instances.find(x=>x.id===r.id),reg=registry.instances.find(x=>x.alias==="EB-"+r.id),G=compile(x);require(sha(enc(G.network))===reg.sha256&&enc(G.network).length*8===reg.N_bits&&sha(x.dimacs)===reg.source_cnf.sha256&&sha(enc(G.source_map))===reg.source_map_sha256,"authentication");let c=chart(G.network),m={root:c.root,phase:c.phase},mapSha=sha(enc(m)),schema="T1-EB-F3-BOOL-LINEAR-v1",chartArtifact={schema,gauge:[10,0],equations:c.A},chartSha=sha(enc(chartArtifact));
let runs=[{H:[],...r.root},...r.runs].map(run=>{let pins=[[10,0],...run.H.map(l=>[Math.abs(l)-1,+(l>0)])].sort((a,b)=>a[0]-b[0]);for(let [v,b] of pins)require(v===10||c.root[v]===v+1&&c.phase[v]===0,"guard map");let artifactSha=sha(enc(pins)),guard_id="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",reg.instance_id,"EB-PORT-PINS-v1",artifactSha])),residual_id="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",reg.instance_id,guard_id,schema,chartSha,mapSha]));return{H:run.H,pins,artifactSha,guard_id,residual_id,status:run.status,reason:run.reason||null,discoveryOps:run.ops,...verify(c.A,run.H,run)}});
out.push({format:"T1-EB-F3-BOOL-REPLAY-v1",model:"STRICT-EB4-v1",instance_id:reg.instance_id,short_id:reg.short_id,N:reg.N_bits,guard_id:"EMPTY",residual_id:"ROOT",source_pin:{registry:"0c14cdc57925788cf7a451dcd5aa171dce860f2c",corpus:"e315349cd6c1fe3fa696504859f28312f6aab69a",compiler:"21b9d53fb8166c819b24e708656c742cd3c24f10"},parents:[],original_ids:{vertices:[0,reg.vertices-1],ports:[0,4*reg.vertices-1],edges:[0,reg.edges-1],balance:c.A.map(a=>a.id)},proof_pin:"95fd2f1d63f607287a0bd899bfed3bd29bd8c6c6",schema,chartSha,mapSha,edgeVisits:c.edgeVisits,localChecks:c.localChecks,runs,scope:"Verified conditional deductions in native source; root gauge is complement symmetry, not forced. UNKNOWN runs certify individual deductions, not completeness. Chart and map reproducible by checker."})}return out;
}
