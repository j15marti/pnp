/* LSPV-2/388 independent proof checker: semantic truth tables
   plus memoized uncovered-assignment recursion, not producer's DP.
   node lspv2_388_independent_verify.js result.json */
"use strict";
const fs=require("fs");
let assertions=0;
function ok(cond,msg){assertions++;if(!cond)throw Error(msg);}
function clauseUniverse(n) {
  const result=[];
  for(let q=0;q<3**n;q++){let a=q, lits=[];
    for(let j=1;j<=n;j++){let t=a%3;a=(a-t)/3;if(t)lits.push((t===1?1:-1)*j);}
    result.push(lits);
  }
  return result;
}
function mask(n,c){
  let bad=0;
  for(let a=0;a<2**n;a++){
    let value=false;
    for(const l of c){const x=Math.abs(l)-1;if(((a>>x)&1)===(l>0?1:0)){value=true;break;}}
    if(!value)bad+=2**a;
  }
  return bad;
}
function check(r) {
  const n=r.n;ok(n===1||n===2||n===3,"n");
  const cs=clauseUniverse(n);
  const ids=r.clause_indices;
  ok(Array.isArray(ids)&&new Set(ids).size===ids.length,"duplicate ids");
  for(const id of ids)ok(Number.isInteger(id)&&id>=0&&id<cs.length,"bad id");
  const cover=ids.map(i=>mask(n,cs[i])),full=2**(2**n)-1;
  const union=cover.reduce((a,b)=>a|b,0);
  if(r.label==="SAT") {
    ok(union!==full,"false SAT label");
    ok(Number.isInteger(r.witness)&&r.witness>=0&&r.witness<2**n,"bad witness");
    ok(!(union&(1<<r.witness)),"witness invalid");
    return "SAT";
  }
  ok(r.label==="UNSAT"&&union===full,"false UNSAT label");
  const cache=new Map();
  function optimum(U) {
    if(!U)return 0;
    if(cache.has(U))return cache.get(U);
    let bit=U&(-U),best=Infinity;
    for(const c of cover)if(c&bit)best=Math.min(best,1+optimum(U&(~c)));
    cache.set(U,best);return best;
  }
  const mu=optimum(full);
  ok(r.mu===mu&&r.paid===mu-1,"nonoptimal proof");
  const core=r.core;
  ok(Array.isArray(core)&&core.length===mu&&new Set(core).size===core.length,"core size");
  const leaves={};
  for(let j=0;j<cover.length;j++)leaves[j]=full^cover[j];
  const anc=core.reduce((a,j)=>a|cover[j],0);
  ok(anc===full,"invalid core");
  ok(r.nodes.length===mu-1,"node count");
  for(let k=0;k<r.nodes.length;k++){
    const v=r.nodes[k],l=k===0?core[0]:"d"+k,rid=core[k+1];
    ok(v.rule==="AND3"&&v.left===l&&v.right===rid,"bad parents");
    let expected=leaves[l]&leaves[rid];
    ok(v.truth===expected,"invalid truth table");
    leaves["d"+(k+1)]=expected;
  }
  ok(mu===1?leaves[core[0]]===0:leaves["d"+(mu-1)]===0,"not refuted");
  return "UNSAT";
}
function main() {
  const d=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
  ok(d.schema==="LSPV2-388-three-variable-optimum-v1","schema");
  const totals={};
  for(const r of d.fixtures){const k=r.n+":"+check(r);totals[k]=(totals[k]||0)+1;}
  ok(d.fixtures.length===1032,"fixture count");
  const cube=d.fixtures.find(r=>r.n===3&&r.paid===7);
  ok(!!cube&&cube.mu===8,"extremal missing");
  let rejects=0;
  for(const field of ["truth","rule","right","paid","mu"]) {
    const fake=JSON.parse(JSON.stringify(cube));
    if(field==="paid"||field==="mu")fake[field]++;
    else if(field==="truth")fake.nodes[fake.nodes.length-1].truth=1;
    else if(field==="rule")fake.nodes[0].rule="OR";
    else fake.nodes[fake.nodes.length-1].right=9999;
    try{check(fake);}catch(e){rejects++;continue;}
    throw Error("corruption accepted: "+field);
  }
  ok(rejects===5,"forgery controls");
  console.log(JSON.stringify({status:"PASS",fixtures:d.fixtures.length,totals,assertions,rejections:rejects}));
}
if(require.main===module)main();
