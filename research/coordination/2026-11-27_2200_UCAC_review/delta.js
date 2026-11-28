// node delta.js compiler corpus registry chart hash joint-cone random-cone
function run(d){
const sha=new Function(d.hash.slice(0,d.hash.indexOf("function quotient"))+";return sha")(),compile=new Function(d.compiler.slice(d.compiler.indexOf("function compile"),d.compiler.indexOf("function auditLocal"))+";return compile")(),{project,verifyProjection}=new Function(d.chart.slice(d.chart.indexOf("const key="),d.chart.indexOf("function up("))+";return {project,verifyProjection}")();
const enc=x=>JSON.stringify(x)+"\n";if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("hash");
const canon=a=>[...a].sort((x,y)=>x-y).join(",");
function scan(rows,A,counts){
let changed=true;
while(changed){changed=false;for(const c of rows){let sat=false,u=0,last=0;for(const l of c){counts.visits++;if(A.has(l)){sat=true;break}if(!A.has(-l)){u++;last=l}}if(sat)continue;if(u===0)return false;if(u===1){A.add(last);counts.assignments++;changed=true}}}
return true;
}
function test(F,P){
let peer={visits:0,assignments:0};let prior=[...F];
for(const c of P){if(scan(prior,new Set(c.map(l=>-l)),peer))throw Error("invalid peer");prior.push(c)}
if(P.at(-1).length!==0)throw Error("no empty");
let n=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),guards=[[]];for(const v of n)guards.push([v],[-v]);
for(let i=0;i<n.length;i++)for(let j=i+1;j<n.length;j++)for(const s of [-1,1])for(const t of [-1,1])guards.push([s*n[i],t*n[j]]);
let seed=P.slice(0,3), counts={visits:0,assignments:0},states=guards.map(g=>{let A=new Set(g);return {A,live:scan(F,A,counts)}});
const status=()=>states.map(x=>!x.live?1:0);
const initial=status(),initialCost={...counts};
let out=[],rows=[...F], fresh={visits:0,assignments:0}, delta={visits:0,assignments:0},tests=0,skipped=0,retired=0;
for(const c of seed){rows.push(c);for(const state of states){if(!state.live)continue;let sat=false,u=0;for(const l of c){delta.visits++;if(state.A.has(l)){sat=true;break}if(!state.A.has(-l))u++}tests++;if(sat||u>=2){skipped++;continue;}state.live=scan(rows,state.A,delta);if(!state.live)retired++;}
let ref=guards.map(g=>{let A=new Set(g),live=scan(rows,A,fresh);return {A,live}});for(let i=0;i<ref.length;i++){let a=states[i],b=ref[i];if(a.live!==b.live||a.live&&(a.A.size!==b.A.size||[...a.A].some(x=>!b.A.has(x))))throw Error("delta mismatch");}
out.push({seed:c,refuted:status().reduce((a,b)=>a+b,0),delta:{...delta},fresh:{...fresh},tests,skipped,retired});
}
let ablations=[];for(let mask=0;mask<8;mask++){let C=seed.filter((_,i)=>mask&(1<<i)),cnt={visits:0,assignments:0},refuted=0,valid=true,R=[...F];for(const c of C){if(scan(R,new Set(c.map(l=>-l)),cnt)){valid=false;break}R.push(c)}if(valid)for(const g of guards){if(!scan(R,new Set(g),cnt))refuted++}ablations.push({mask,valid,refuted:valid?refuted:null,...cnt})}
return {variables:n.length,rows:F.length,guards:guards.length,initialRefuted:initial.reduce((a,b)=>a+b,0),initialCost,peerReplay:peer,steps:out,ablations,seed,finalRefutedGuards:guards.filter((g,i)=>!states[i].live),baseRefutedGuards:guards.filter((g,i)=>initial[i])};
}
let out=[];for(const name of ["joint","random"]){let c=JSON.parse(d[name]),x=JSON.parse(d.corpus).instances.find(x=>c.instance.startsWith("EB-"+x.id+"@")),reg=JSON.parse(d.reg).instances.find(x=>x.instance_id===c.instance_id),G=compile(x);if(sha(enc(G.network))!==reg.sha256||enc(G.network).length*8!==reg.N_bits||sha(x.dimacs)!==reg.source_cnf.sha256||x.dimacs.length*8!==reg.source_cnf.N_bits||sha(enc(G.source_map))!==reg.source_map_sha256)throw Error("auth");
let p=project(G.network),projection=verifyProjection(G.network,p),chartHash=sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),mapHash=sha(enc({root:p.root,phase:p.phase}));let gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",reg.instance_id,"EB-PORT-PINS-v1",sha(enc([[p.anchor,0]]))])),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",reg.instance_id,gid,"EB-CHART-SYZYGY-v1",chartHash,mapHash]));if(gid!==c.guard_id||rid!==c.residual_id||sha(enc(c.proof))!==c.proof_hash)throw Error("peer hash");let native=test(p.clauses,c.proof);
let cnf=x.dimacs.trimEnd().split("\n").slice(1).map(c=>c.trim().split(/\s+/).map(Number).slice(0,-1)),reps=G.source_map.representative_ports,fp=reps.f,ar=p.root[fp[0]],f=p.phase[fp[0]]^fp[1],mapping=[];for(let i=1;i<=x.nvars;i++){let [q,s]=reps["x"+i];mapping.push([i,p.root[q]+1,p.phase[q]^s^f])}let M=new Map(mapping.map(([i,v,s])=>[v,[i,s]]));const convert=c=>c.map(l=>{let m=M.get(Math.abs(l));if(!m)throw Error("mapping");return (l>0?1:-1)*(m[1]?-1:1)*m[0]});let A=new Set(cnf.map(canon)),B=new Set(p.clauses.map(c=>canon(convert(c))));if(ar!==p.anchor||M.size!==x.nvars||A.size!==B.size||![...A].every(x=>B.has(x)))throw Error("adapter");let companion=test(cnf,c.proof.map(convert));
out.push({name:x.id,instance:c.instance,instance_id:c.instance_id,original_N_bits:c.original_N_bits,guard_id:gid,residual_id:rid,chartHash,mapHash,original_ids:c.original_ids,parent_sha:sha(d[name]),projection,source_cnf:reg.source_cnf,native,companion});}
return out;
}
if(typeof require!=='undefined'&&require.main===module){const fs=require('node:fs');const keys=['compiler','corpus','reg','chart','hash','joint','random'];console.log(JSON.stringify(run(Object.fromEntries(keys.map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]))),null,2))}
