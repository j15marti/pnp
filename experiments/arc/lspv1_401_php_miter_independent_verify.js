#!/usr/bin/env node
// Independently reconstructs PHP and checks all finite raw controls.
const fs = require('fs');
const loc = process.argv[2] || 'results/raw/arc/2026-11-04_1500_LSPV1_PHP_COFAC_MITER401_raw.json';
const data = JSON.parse(fs.readFileSync(loc, 'utf8'));
let checks=0;function ck(b,msg){++checks;if(!b)throw Error(msg||'control failed')}
function variables(h){return h*(h+1)}
function clauses(h){let a=[];
  for(let i=0;i<=h;i++){let clause=[];for(let j=1;j<=h;j++)clause.push(i*h+j);a.push(clause)}
  for(let j=1;j<=h;j++)for(let i=0;i<=h;i++)for(let k=i+1;k<=h;k++)a.push([-(i*h+j),-(k*h+j)]);
  return a;
}
function sat(cs,as){return cs.every(c=>c.some(l=>as[Math.abs(l)-1]===(l>0?1:0)))}
function assignment(h){let n=variables(h),arr=Array(n).fill(0);for(let p=1;p<=h+1;p++){let hole=p<=2?1:p-1;arr[(p-1)*h+hole-1]=1;}return arr}
function evalBits(h,cs){let n=variables(h),found=0;for(let mask=0;mask<(1<<n);mask++){let a=Array.from({length:n},(_,i)=>(mask>>i)&1);if(sat(cs,a))found++;}return found}
function checkRecord(r){let h=r.holes,k=r.k,i=r.pivot_x;
  let P=clauses(h),n=variables(h),del=P.filter(c=>!(c.length==2&&c[0]==-1&&c[1]==-(h+1)));
  ck(r.pigeons===h+1&&r.variables_php===n,'shape');
  ck(r.php_clauses===P.length,'PHP m');
  ck(r.php_literal_occurrences===P.reduce((s,c)=>s+c.length,0),'lit count');
  ck(r.full_miter_variables===n+k,'V');
  ck(r.miter_clauses===P.length+k-1,'miter m');
  let wit=assignment(h);ck(sat(del,wit),'deleted witness');ck(!sat(P,wit),'unsat original witness');
  ck(r.source_php_models===0,'model ledger');
  ck(r.deleted_clause.join(',')===[-1,-(h+1)].join(','),'target clause');
  ck(r.witness_pigeon_locations.join(',')===Array.from({length:h+1},(_,t)=>t<2?1:t).join(','),'witness map');
  let D=P.concat(Array.from({length:k},(_,j)=>j+1).filter(j=>j!=i).map(j=>[-(n+j)]));
  ck(sat(del.concat(D.slice(P.length)),wit.concat(Array(k).fill(0))),'SAT sibling miter');
  for(let mask=0;mask<(1<<n);mask++){
    let u=Array.from({length:n},(_,j)=>(mask>>j)&1),p=sat(P,u)?1:0,pdel=sat(del,u)?1:0;
    ck(!p,'PHP has no models');
    for(let xmask=0;xmask<(1<<k);xmask++){
      let xa=Array.from({length:k},(_,j)=>(xmask>>j)&1),other=xa.some((v,j)=>v&&j!=(i-1))?1:0;
      let c=p*(xa.some(Boolean)?1:0);
      let d=(other*p)^p, target=(1-other)*p;
      ck(c===0&&d===target,'function truth');
      if(xa[i-1]===0)ck(sat(D,u.concat(xa))===(target===1),'miter CNF');
      if(pdel&&!other)ck(((other*pdel)^pdel)===1,'positive control');
    }
  }
  ck(r.miter_checked_assignments===(1<<n)*(1<<k),'count assignments');
  if(h===1)ck(r.strict_res_upper_nodes_if_h1===2,'two step upper');
  else ck(r.strict_res_upper_nodes_if_h1===null,'not claiming optimum');
}
ck(data.identifier==='LSPV1_401_PHP_COFAC_MITER_FIREWALL','id');ck(data.rows.length===12,'length');
for(let h of [1,2,3]){let P=clauses(h); ck(evalBits(h,P)===0,'all model enumeration');}
for(let r of data.rows)checkRecord(r);
for(let mutate of [r=>r.php_clauses++,r=>r.miter_clauses++,r=>r.source_php_models++,r=>r.deleted_clause[0]--]){
  let bad=structuredClone(data),row=bad.rows[0];mutate(row);
  try{checkRecord(row);throw new Error('corruption not rejected');}catch(e){if(e.message==='corruption not rejected')throw e;ck(true,'corruption rejected');}
}
console.log(JSON.stringify({result:'PASS',independent_assertions:checks,rows:data.rows.length,producer_assertions:data.producer_assertions}));
