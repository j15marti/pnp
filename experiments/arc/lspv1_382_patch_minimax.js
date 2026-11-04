'use strict';
// LSPV-1/382: fully deterministic finite controls for per-input finite-program patching.
// Does NOT claim a proof of SAT complexity or an execution-time benchmark.
const assert = (condition, message) => { if (!condition) throw new Error(message); checks++; };
let checks = 0;
function classify(src) {
  if (typeof src !== 'string') return 'MALFORMED';
  const lines=src.split('\n');
  if (!/^p cnf (0|[1-9][0-9]*) (0|[1-9][0-9]*)$/.test(lines[0]||'')) return 'MALFORMED';
  const [,ns,ms]=lines[0].match(/^p cnf (\d+) (\d+)$/), n=Number(ns), m=Number(ms);
  if (!Number.isSafeInteger(n)||!Number.isSafeInteger(m)||n>12||m>200||lines.length!==m+1) return 'MALFORMED';
  let clauses=[];
  for (const line of lines.slice(1)) {
    if (!/^(?:-?[1-9][0-9]* )*0$/.test(line)) return 'MALFORMED';
    const vals=line.split(' ').slice(0,-1).map(Number);
    if (vals.some(v=>!Number.isSafeInteger(v)||v===0||Math.abs(v)>n)) return 'MALFORMED';
    clauses.push(vals);
  }
  for(let mask=0;mask<(1<<n);mask++) {
    if (clauses.every(c=>c.some(v=>v>0? !!(mask&(1<<(v-1))) : !(mask&(1<<(-v-1)))))) return 'SAT';
  }
  return 'UNSAT';
}
function buildPatch(target) {
  const answer = classify(target); // label discovery is deliberately NOT charged in the existential minimum
  const machine = src => src===target ? answer : classify(src);
  const encoding = JSON.stringify({tag:'ONE-EXACT-INPUT-PATCH',target,answer});
  return {machine,answer,encoding};
}
const fixtures=[
 'p cnf 0 0','p cnf 0 1\n0','p cnf 1 1\n1 0','p cnf 1 2\n1 0\n-1 0',
 'p cnf 2 2\n1 2 0\n-1 -2 0','p cnf 2 3\n1 0\n-1 2 0\n-2 0',
 'p cnf 3 2\n1 2 3 0\n-1 -2 -3 0','p cnf 2 1\n0',
 '','p cnf','p cnf 1 1\n2 0','p cnf 1 1\n1 0\n','p cnf 2 1\n1 a 0',
 'p cnf 1 1\n-0 0','p cnf 01 0','p cnf 1 1\n1 -1 0',
];
const patches=fixtures.map(buildPatch);
for(let i=0;i<patches.length;i++) {
  const p=patches[i];
  assert(p.machine(fixtures[i])===p.answer,'patch target result');
  assert(p.encoding.length<=4*fixtures[i].length+80,'program description <= 4n+80 characters');
  for(const s of fixtures) assert(p.machine(s)===classify(s),'patch correctness on cross fixture');
}
const counts={SAT:0,UNSAT:0,MALFORMED:0};
for(const s of fixtures) counts[classify(s)]++;
assert(counts.SAT>0 && counts.UNSAT>0 && counts.MALFORMED>0,'all labels represented');
for(let n=0;n<=8;n++) for(let v=0;v<(1<<n);v++) {
  let s=v.toString(2).padStart(n,'0'); if (n===0) s='';
  for(const p of patches.slice(0,3)) assert(p.machine(s)===classify(s),'binary malformed fallback');
}
function xor3(rhs) {let c=[];for(let m=0;m<8;m++){const par=((m&1)^((m>>1)&1)^((m>>2)&1));if(par===rhs)continue; const literals=[1,2,3].map((v,i)=>(m&(1<<i))? -v:v);c.push(literals.join(' ')+' 0');}return 'p cnf 3 4\n'+c.join('\n')}
const even=xor3(0),odd=xor3(1);
assert(classify(even)==='SAT'&&classify(odd)==='SAT','single parity equations satisfiable');
assert(classify('p cnf 3 8\n'+even.split('\n').slice(1).concat(odd.split('\n').slice(1)).join('\n'))==='UNSAT','opposing parity unsat');
const result={experiment:'LSPV1_LINEAR_INSTANCE_PATCH_MINIMAX382',kind:'finite computational controls; theorem proved separately',seed:null,checks,fixture_count:fixtures.length,class_counts:counts,patch_encoding_char_max:Math.max(...patches.map(x=>x.encoding.length)),patch_target_char_max:Math.max(...fixtures.map(x=>x.length)),binary_fallback_control_strings:511,parser:'strict capped ASCII p cnf n m and signed literal lines; malformed rejected',theorem_scope:'arbitrary total decidable binary languages with fixed fallback; NOT SAT polynomial-time claim',fallback:'exhaustive all valid instances <=12 vars; all other strings malformed in this illustrative bounded grammar',parity:'opposing 3-variable parity equations UNSAT',pass:true};
if(typeof module!=='undefined'&&module.exports)module.exports={classify,buildPatch,result,fixtures};
if(typeof require!=='undefined'&&require.main===module)console.log(JSON.stringify(result,null,2));
