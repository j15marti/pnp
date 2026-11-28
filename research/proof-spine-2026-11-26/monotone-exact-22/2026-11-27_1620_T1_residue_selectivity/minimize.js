// Node: node minimize.js DIR; files named cert,corpus,native from pins.
const fs=require('node:fs');const files={"cert":["research/proof-spine-2026-11-26/monotone-exact-22/2026-11-27_1620_T1_residue_selectivity/JOINT-24.syzygy.json","d361104d31d73cbe76e30c64d9ac8481171cf240"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"]};const d=Object.fromEntries(Object.keys(files).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
function minimize(d){
 const {sha}=new Function(d.native+";return {sha};")(),a=JSON.parse(d.cert),s=JSON.parse(d.corpus).instances.find(x=>x.id==="JOINT-24"),C=s.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1)),A=(x,m)=>{if(!x)throw Error(m)};
 A(sha(s.dimacs)===a.instance_id.split(":").pop()&&8*s.dimacs.length===a.original_N_bits&&sha(d.cert)==="7a9444e78ccb6c1a04212f4ddfaab8a3381e823f9d9f105309f4876bd1f8f33d","authentication");
 const seteq=(a,b)=>a.length===b.length&&a.every(x=>b.includes(x));
 let checks=0;const exact=r=>{let expected=[r.v,...r.v.flatMap((v,i)=>r.v.slice(i+1).map(w=>[-v,-w]))];for(let c of expected){checks+=r.ids.length;A(r.ids.some(id=>seteq(C[id-1],c)),"row")}};
 for(let p of a.certs){let coef=new Int32Array(s.nvars+1),rhs=0,forced=new Map([p.guard]);for(let [r,t] of p.terms){A(t===1||t===-1,"sign");exact(r);rhs+=t;for(let v of r.v)coef[v]+=t}
  for(let [v,id] of p.zeroReasons){checks++;A(p.guard[1]===1&&seteq(C[id-1],[-p.guard[0],-v]),"zero");forced.set(v,0)}
  let upper=0;for(let v=1;v<=s.nvars;v++)upper+=forced.has(v)?coef[v]*forced.get(v):Math.max(0,coef[v]);
  A(rhs===p.rhs&&upper===p.upper&&upper<rhs&&p.unit===(p.guard[1]?-p.guard[0]:p.guard[0]),"syzygy")
 }
 let trials=0,visits=0,chosen=[],winner=null,bySize=[];
 function prop(U){
  const v=new Map(U.map(l=>[Math.abs(l),+(l>0)])),trace=[];
  while(true){let todo=[];for(let [i,c] of C.entries()){let sat=false,free=[];for(let l of c){visits++;let b=v.get(Math.abs(l));if(b===undefined)free.push(l);else if(b===+(l>0)){sat=true;break}}if(sat)continue;if(!free.length)return {conflict:i+1,trace};if(free.length===1)todo.push([free[0],i+1]);}
   if(!todo.length)return null;
   for(let [l,id] of todo){let x=Math.abs(l),b=+(l>0);if(v.has(x)){if(v.get(x)!==b)return {conflict:id,trace};continue}v.set(x,b);trace.push({l,id})}
  }
 }
 const U=a.certs.map(p=>p.unit).sort((a,b)=>Math.abs(a)-Math.abs(b));
 function dfs(k,j){if(winner)return;if(!k){trials++;const r=prop(chosen);if(r)winner={units:chosen.slice(),...r};return}for(let i=j;i<=U.length-k;i++){chosen.push(U[i]);dfs(k-1,i+1);chosen.pop();if(winner)return}}
 for(let k=0;k<=U.length;k++){let prev=trials;dfs(k,0);bySize.push({size:k,trials:trials-prev,found:!!winner});if(winner)break}
 A(winner,"terminal");let v=new Map(winner.units.map(l=>[Math.abs(l),+(l>0)]));
 for(let {l,id} of winner.trace){let c=C[id-1];A(c.includes(l)&&!v.has(Math.abs(l))&&c.filter(x=>x!==l).every(x=>v.get(Math.abs(x))===+(x<0)),"UP proof");v.set(Math.abs(l),+(l>0))}
 A(C[winner.conflict-1].every(x=>v.get(Math.abs(x))===+(x<0)),"conflict");
 return {problem_id:a.problem_id,instance:a.instance,instance_id:a.instance_id,original_N_bits:a.original_N_bits,source_pin:a.source_pin,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{clauses:[1,C.length],variables:[1,s.nvars]},parents:["CERT-v1:sha256:"+sha(d.cert)],claim:"verified UNSAT by sparse signed exact-one unit certificates and source-clause UP; minimum cardinality within these ten acquired units only",candidateUnits:U,winner,bySize,trials,visits,checks,unitCertificates:a.certs.filter(p=>winner.units.includes(p.unit)),extraUnit:a.certs.find(p=>p.unit===-15)}
}
console.log(JSON.stringify(minimize(d),null,2));
