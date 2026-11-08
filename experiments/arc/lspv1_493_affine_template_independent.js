'use strict';
/* Independent finite audit LSPV-1/493, Node >= 18. No dependencies.
Usage: node experiments/arc/lspv1_493_affine_template_independent.js \
results/raw/arc/2026-11-07_1900_LSPV1_493_AFFINE_COVER_RAW.json */
const fs = require('fs');
const raw = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
let assertions = 0;
function check(cond,msg){assertions++;if(!cond)throw Error(msg||'failed');}
function predict(k,u,v){switch(k){case 0:return 0;case 1:return u;case 2:return v;case 3:return 1^u^v;default:throw Error('bad template');}}
function good(g,code,x){
  for(let j=0;j<g;j++){
    const u=(x>>(2*j))&1,v=(x>>(2*j+1))&1;
    if(predict((code>>(2*j))&3,u,v)!==(u&v))return false;
  }
  return true;
}
for(const row of raw.rows){
  const {g,input_assignments:n,greedy_indices:picks}=row;
  check(n===4**g,'assignment count');
  check(picks.length===row.greedy_K,'length');
  check(new Set(picks).size===picks.length,'unique');
  const covered=new Uint8Array(n);
  for(const code of picks){
    check(Number.isInteger(code)&&code>=0&&code<n,'index range');
    let agree=0;
    for(let x=0;x<n;x++){if(good(g,code,x)){covered[x]=1;agree++;}}
    check(agree===3**g,'agreement count');
  }
  for(let x=0;x<n;x++)check(covered[x]===1,'uncovered g='+g+' x='+x);
  check(row.greedy_K>=Math.ceil((4/3)**g-1e-9),'Fourier lower');
  check(row.greedy_K<=Math.ceil((4/3)**g*(g*Math.log(4)+1)),'greedy upper');
}
check(JSON.stringify(raw.g3_explicit_certificate)===JSON.stringify([0,21,42,63]),'explicit four');
for(let x=0;x<64;x++)check(raw.g3_explicit_certificate.some(c=>good(3,c,x)),'3 gate hole');
for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++)
  check([0,1,2,3].some(x=>((a*(x&1))^(b*((x>>1)&1))^c)!==((x&1)&((x>>1)&1))),'AND affine false');
function models(charges){
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  let z=0;
  for(let x=0;x<64;x++){
    let ok=true;
    for(let v=0;v<4;v++){
      let bit=0;
      for(let i=0;i<6;i++)if(edges[i].includes(v))bit^=(x>>i)&1;
      if(bit!==charges[v])ok=false;
    }
    if(ok)z++;
  }
  return z;
}
check(models([1,0,0,0])===0,'odd K4 UNSAT');
check(models([0,0,0,0])===8,'even K4 count');
check(raw.result_id==='LSPV-1/493','schema');
console.log(JSON.stringify({result_id:'LSPV-1/493',status:'PASS',assertions,verified_g:raw.rows.map(r=>r.g),K:raw.rows.map(r=>r.greedy_K),source_controls:raw.source_controls}));
