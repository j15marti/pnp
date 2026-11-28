// node feedback-run.js evidence.json previous-feedback.js previous-checker.js corpus.json compiler.js registry.json native-chart.js fano-manifest.json
function feedbackRun({evidence,src,old,corp,compiler,reg,chart,fano}){
 const sha=new Function(old.slice(old.indexOf("function sha"),old.indexOf("function chart"))+";return sha")(), compile=new Function(compiler.slice(compiler.indexOf("function compile"),compiler.indexOf("function auditLocal"))+";return compile")(),{project,verifyProjection,adapter}=new Function(chart.slice(chart.indexOf("const key="),chart.indexOf("function run("))+";return {project,verifyProjection,adapter}")(),{trial,propagate}=new Function(src.slice(0,src.indexOf("const recorded="))+";return {trial,propagate}")();
 const enc=x=>JSON.stringify(x)+"\n",parse=x=>x.trimEnd().split("\n").slice(1).map(c=>c.trim().split(/\s+/).map(Number).slice(0,-1));
 let out=[];function arms(F){let a=[];for(let width of [2,4])for(let kind of ["baseline","flips","deductions","table","residue"])a.push(trial(F,width,kind));return a}
 for(let q of JSON.parse(evidence)){
 let x=JSON.parse(corp).instances.find(z=>z.id===q.name),r=JSON.parse(reg).instances.find(z=>z.alias==="EB-"+q.name),G=compile(x);
 if(sha(enc(G.network))!==r.sha256||enc(G.network).length*8!==r.N_bits||sha(x.dimacs)!==r.source_cnf.sha256||x.dimacs.length*8!==r.source_cnf.N_bits||sha(enc(G.source_map))!==r.source_map_sha256)throw Error("authentication");
 let p=project(G.network),projectionReplay=verifyProjection(G.network,p);if(enc(p.clauses)!==enc(q.chart))throw Error("chart");
 const t=Date.now(),ad=adapter(p,G,x.dimacs,x.nvars),adapterMs=Date.now()-t;
 let db=p.clauses.slice(),seeds=q.name==="JOINT-24"?[[-594]]:[[362,34],[362,-33],[362,298]],admission={scans:0},early={scans:0},root=propagate(db,new Map(),early);
 if(root===null||root.size)throw Error("expected unchanged initial root");
 for(let c of seeds){if(propagate(db,new Map(c.map(l=>[Math.abs(l),+(l<0)])),admission,true)!==null)throw Error("seed");db.push(c)}
 let close={scans:0},forced=propagate(db,new Map(),close),maps=sha(enc({root:p.root,phase:p.phase})),artifact=sha(enc({parent:q.rid,chart:p.clauses,imported:seeds})),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",r.instance_id,q.gid,"EB-CHART-AUGMENTED-v1",artifact,maps]));
 out.push({name:q.name+" native",problem_id:"STRICT-EB4-v1",instance:r.short_id,instance_id:r.instance_id,N:r.N_bits,guard_id:q.gid,residual_id:rid,base_residual:q.rid,guard:[[p.anchor,0]],mapHash:maps,artifact,original_ids:{vertices:[0,r.vertices-1],ports:[0,4*r.vertices-1],edges:[0,r.edges-1]},seeds,early,admission,reclose:close,forced:forced&&[...forced],projectionReplay,provenanceAdapter:{verified:true,uniqueClauses:ad.unique,mapping:ad.mapping,ms:adapterMs},F:db,arms:arms(db)});
 let F=parse(x.dimacs),st={scans:0},a=propagate(F,new Map(),st);out.push({name:q.name+" CNF",problem_id:"DIMACS-CNF-v1",instance:r.source_cnf.short_id,instance_id:r.source_cnf.instance_id,N:r.source_cnf.N_bits,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{clauses:[1,F.length],variables:[1,x.nvars]},early:st,forced:a&&[...a],F,arms:arms(F)});
 }
 const f=JSON.parse(fano);if(sha(f.dimacs)!==f.instance_id.split(":").at(-1)||f.dimacs.length*8!==f.N_bits)throw Error("Fano auth");let F=parse(f.dimacs),st={scans:0},a=propagate(F,new Map(),st);out.push({name:f.alias,problem_id:f.model,instance:f.short_id,instance_id:f.instance_id,N:f.N_bits,guard_id:"EMPTY",residual_id:"ROOT",original_ids:f.original_ids,early:st,forced:a&&[...a],F,arms:arms(F)});return out;
}
if(typeof require!=='undefined'&&require.main===module){let fs=require('node:fs'),keys=['evidence','src','old','corp','compiler','reg','chart','fano'];console.log(JSON.stringify(feedbackRun(Object.fromEntries(keys.map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]))),null,2))}
