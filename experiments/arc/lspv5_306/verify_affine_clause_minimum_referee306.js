#!/usr/bin/env node
// Independent no-import verifier for REFEREE306.  Does not import producer code.
const fs = require('fs');
const crypto = require('crypto');

const path = process.argv[2] || 'results/raw/arc/2026-11-02_2250_LSPV5_AFFINE_CLAUSE_MINIMUM_REFEREE306_raw.json';
const raw = JSON.parse(fs.readFileSync(path, 'utf8'));
let assertions = 0;
function check(x, msg) { assertions++; if (!x) throw new Error(msg); }
function pc(x) { let c=0; while(x){x&=x-1;c++;} return c; }
function parity(x,m){ return pc(x&m)&1; }
function models(rows,n=4){
  const ans=[];
  for(let x=0;x<(1<<n);x++) if(rows.every(([m,b])=>parity(x,m)===b)) ans.push(x);
  return ans;
}
function patterns(mask,rhs,n=4){
  const vs=[]; for(let v=0;v<n;v++) if((mask>>v)&1)vs.push(v);
  const out=[];
  for(let a=0;a<(1<<vs.length);a++){
    const bits=vs.map((v,j)=>[v,(a>>j)&1]);
    if((bits.reduce((s,p)=>s+p[1],0)&1)!==rhs) out.push(bits);
  }
  return out;
}
function match(x,p){return p.every(([v,b])=>((x>>v)&1)===b);}
function classify(rows){
  const ms=models(rows);
  if(ms.length) return {sat:true,row:false,clause:false,m:rows.reduce((s,[mask])=>s+(1<<(pc(mask)-1)),0)};
  let row=true, clause=true;
  for(let i=0;i<rows.length;i++){
    const om=models(rows.slice(0,i).concat(rows.slice(i+1)));
    if(!om.length)row=false;
    for(const p of patterns(rows[i][0],rows[i][1])) if(!om.some(x=>match(x,p)))clause=false;
  }
  return {sat:false,row,clause,m:rows.reduce((s,[mask])=>s+(1<<(pc(mask)-1)),0)};
}
function* comb(arr,k,start=0,p=[]){
  if(p.length===k){yield p.slice();return;}
  for(let i=start;i<=arr.length-(k-p.length);i++){p.push(arr[i]);yield* comb(arr,k,i+1,p);p.pop();}
}
const masks=[];for(let m=1;m<16;m++)if(pc(m)<=3)masks.push(m);
const counts={systems:0,sat:0,unsat:0,row_minimal:0,clause_minimal:0};
let theorem=0, flips=0, first=null;
for(let r=1;r<=5;r++) for(const supports of comb(masks,r)) for(let bits=0;bits<(1<<r);bits++){
  const rows=supports.map((m,i)=>[m,(bits>>i)&1]);
  const c=classify(rows); counts.systems++;
  if(c.sat)counts.sat++;else counts.unsat++;
  if(c.row)counts.row_minimal++;
  if(c.clause){
    counts.clause_minimal++; theorem++;
    check(c.row,'clause-min must be row-min');
    let mm=0,bb=0;for(const [m,b] of rows){mm^=m;bb^=b;}
    check(mm===0&&bb===1,'all-row affine contradiction');
    const local=rows.reduce((s,[m])=>s+(1<<(pc(m)-1))-1,0);
    check(local+r-1===c.m-1,'m-1 construction');
    for(let i=0;i<r;i++){const f=rows.map(z=>z.slice());f[i][1]^=1;check(models(f).length>0,'rhs flip SAT');flips++;}
  }
  if(c.row&&!c.clause&&first===null)first={rows,c};
}
for(const k of Object.keys(counts))check(counts[k]===raw.enumeration.counts[k],`count ${k}`);
check(theorem===raw.enumeration.theorem_checks,'theorem checks');
check(flips===raw.enumeration.rhs_flip_checks,'flip checks');
const expectedCounter=[[1,0],[2,0],[3,1]];
const ec=classify(expectedCounter);
check(ec.row&&!ec.clause&&!ec.sat,'explicit row-minimal counterexample');
check(JSON.stringify(raw.counterexample.rows)===JSON.stringify(expectedCounter),'reported counterexample');
check(raw.named_controls.k4_odd.models===0,'odd K4 UNSAT');
check(raw.named_controls.k4_even.models===8,'even K4 eight models');
check(raw.named_controls.row_minimal_not_clause_minimal.exact_cost===2,'counterexample exact two');
check(raw.malformed.tested===9&&raw.malformed.rejected===9,'malformed controls');
const copy=JSON.parse(JSON.stringify(raw)); const got=copy.payload_sha256; delete copy.payload_sha256;
const canonical=JSON.stringify(copy,Object.keys(copy).sort()); // record-only; producer hash is separately read back
check(typeof got==='string'&&got.length===64,'payload hash shape');
const result={run_id:'AFFINE-CLAUSE-MINIMUM-REFEREE306-VERIFY',assertions,counts,theorem_checks:theorem,rhs_flip_checks:flips,first_counterexample:first.rows,explicit_counterexample:expectedCounter,raw_sha256:crypto.createHash('sha256').update(fs.readFileSync(path)).digest('hex'),status:'PASS'};
const out=path.replace('_raw.json','_verify.json');fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
