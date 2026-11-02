#!/usr/bin/env node
/* LSPV-1 336 no-import independent verifier. Run:
   node experiments/arc/lspv1_336_independent.js results/raw/arc/2026-11-02_1256_LSPV1_CLOCKED_OPTIMALITY_REFLECTION336.json
 */
const fs=require('fs');
const file=process.argv[2];
if(!file)throw Error('Provide raw JSON path');
const data=JSON.parse(fs.readFileSync(file,'utf8'));
let checks=0;
function ok(condition,reason){checks++;if(!condition)throw Error(reason);}
function parse(text){
 if(typeof text!=='string')return null;
 const lines=text.split(/\r?\n/).filter(x=>x.trim()).map(x=>x.trim().split(/\s+/));
 if(lines.length===0)return null;
 const h=lines.shift();
 if(h.length!==4||h[0]!=='p'||h[1]!=='cnf'||!h.slice(2).every(x=>/^\d+$/.test(x)))return null;
 const n=+h[2],m=+h[3];if(n>20||m>500||m!==lines.length)return null;
 const clauses=[];
 for(const line of lines){
   if(!line.every(x=>/^-?\d+$/.test(x)))return null;
   const z=line.map(Number);
   if(z.length<1||z[z.length-1]!==0||z.slice(0,-1).some(x=>x===0||Math.abs(x)>n))return null;
   clauses.push(z.slice(0,-1));
 }
 return {n,clauses};
}
function sat(f,mask){return f.clauses.every(c=>c.some(l=>l>0?!!(mask&(1<<(l-1))):!(mask&(1<<(-l-1)))))}
function models(f){let total=0;for(let x=0;x<(1<<f.n);x++)if(sat(f,x))total++;return total;}
function work(f){for(let k=0;k<(1<<f.n);k++){let mask=0;for(let i=0;i<f.n;i++)if(k&(1<<(f.n-1-i)))mask|=(1<<i);if(sat(f,mask))return k+1;}return 1<<f.n;}
for(const [name,r] of Object.entries(data.inputs)){
 const f=parse(r.source);
 if(!r.valid){ok(f===null,'malformed accepted '+name);continue;}
 ok(f!==null,'bad source '+name);
 ok(f.n===r.variables,'bad variable count '+name);
 ok(f.clauses.length===r.clause_count,'bad clause count '+name);
 ok(models(f)===r.models,'wrong model count '+name);
 ok(work(f)===r.toy_work_units,'wrong toy work '+name);
 ok(r.clock===(1<<f.n),'wrong clock '+name);
 ok(r.proof_returns_input===(r.models===0),'wrong proof return '+name);
}
ok(data.inputs.k4_odd.models===0,'odd should be UNSAT');
ok(data.inputs.k4_even.models===8,'even should have 8 models');
const odd=parse(data.inputs.k4_odd.source);
let sensitive=0;
for(let i=0;i<odd.clauses.length;i++){
 const del={n:odd.n,clauses:odd.clauses.filter((_,j)=>i!==j)};
 ok(models(del)>0,'clause deletion remained UNSAT');sensitive++;
 for(let j=0;j<odd.clauses[i].length;j++){
  const c=odd.clauses.map(a=>a.slice());c[i][j]*=-1;
  ok(models({n:odd.n,clauses:c})>0,'sign flip remained UNSAT');sensitive++;
 }
}
ok(sensitive===64&&data.k4_sensitive_checks===64,'sensitivity ledger');
for(const name of ['guard_odd','guard_even']){
 const f=parse(data.inputs[name].source);let z0=0,z1=0;
 for(let mask=0;mask<(1<<f.n);mask++)if(sat(f,mask)){if(mask&(1<<(f.n-1)))z1++;else z0++;}
 ok(JSON.stringify([z0,z1])===JSON.stringify(data.inputs[name].guard_boundary),'guard boundary '+name);
}
for(const x of data.sentinels){
 const len=('p cnf 1 '+x.k+'\n').length + x.k*4;
 ok(x.length===len,'sentinel length');
 ok(x.halt_50===(len>=50?'UNSAT':'SAT'),'synthetic halt label');
}
ok(data.malformed_rejected===3,'malformed count');
console.log(JSON.stringify({verdict:'PASS',independent_assertions:checks,source_cases:Object.keys(data.inputs).length,sign_and_deletion_controls:sensitive}));
