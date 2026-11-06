/* LSPV-2/431 independent verifier. Run: node lspv2_431_independent_verify.mjs RAW.json */
import fs from 'node:fs';
const verifyIndependent = function verifyIndependent(out){
let assertions=0;const check=(p,s)=>{assertions++;if(!p)throw Error("independent verifier: "+s);};
function core(data){
 check(data.schema==="LSPV2-431/shared-checkpoint-AND/1","schema");
 for(const r of data.records){
  const {q,k,M,queries,counts,trace,sat,unsat,victim}=r;
  check(M>=4*k+8&&queries===q*k-1,"budget");check(trace.length===queries,"trace");
  check(counts.reduce((a,b)=>a+b,0)===queries&&counts[victim]<k,"counts");
  check(sat.length===q&&unsat.length===q,"q arrays");
  for(const [i,v,ans] of trace){check(i>=0&&i<q&&v>=0&&v<M,"query range");check(sat[i][v]===ans&&unsat[i][v]===ans,"same trace");}
  const endpoint=(f)=>{let x=0;for(let j=0;j<k;j++){check(Number.isInteger(f[x])&&f[x]>=0&&f[x]<M,"total successor");x=f[x];}return x&1;};
  check(sat.every(f=>f.length===M&&endpoint(f)===1),"yes");check(unsat.filter(f=>endpoint(f)===0).length===1,"no");
 }
 for(const a of data.aliases){check(a.alias_indices.length===a.q&&a.alias_indices.every(i=>i===0),"alias source");check(a.verified_alias_oracle_cost===a.k&&a.independent_oracle_cost===a.q*a.k,"sharing");}
 check(data.controls.length===4,"Tseitin fixtures");for(const c of data.controls){check(c.clauses===4*c.vertices,"source arity");check(c.sat===(c.charge==="even"),"parity labels");if(c.charge==="odd")check(c.deletionWitnesses===c.clauses,"essential clauses");}
}
core(out);
const corrupted=JSON.parse(JSON.stringify(out));corrupted.records[0].trace[0][2]=-1;
let rejected=false;try{core(corrupted);}catch{rejected=true;}check(rejected,"corrupted answer rejection");
const malformed=JSON.parse(JSON.stringify(out));malformed.records[0].trace[0][1]=malformed.records[0].M;
rejected=false;try{core(malformed);}catch{rejected=true;}check(rejected,"invalid query rejection");
const falsified=JSON.parse(JSON.stringify(out));falsified.records[0].unsat=falsified.records[0].sat;
rejected=false;try{core(falsified);}catch{rejected=true;}check(rejected,"false UNSAT rejection");
const badalias=JSON.parse(JSON.stringify(out));badalias.aliases[0].alias_indices[0]=1;
rejected=false;try{core(badalias);}catch{rejected=true;}check(rejected,"unverified alias rejection");
return {independent_assertions:assertions,mutation_controls:4,records:out.records.length};
};
const payload=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
console.log(JSON.stringify(verifyIndependent(payload)));
