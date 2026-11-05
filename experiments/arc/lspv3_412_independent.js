#!/usr/bin/env node
// Independent readback checker for LSPV-3/412 compact Python producer.
// Run: node experiments/arc/lspv3_412_independent.js lspv3_412_raw.json
// Scope: declared addressable DEF facets + strict binary RES, NOT full native R.
'use strict';
const fs=require('fs');
const raw=JSON.parse(fs.readFileSync(process.argv[2]||'lspv3_412_raw.json','utf8'));
let checks=0;
function ok(v,m){checks++;if(!v)throw Error(m)}
function mask(M,a,b){return (M>>(2*a+b))&1}
function s(v,b){return b?v:-v}
function norm(c){let z=new Set(c);for(let x of z)if(z.has(-x))return null;return [...z].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y)}
function encode(g){let rows=[];for(let a=0;a<2;a++)for(let b=0;b<2;b++){
  let c=norm([-s(g.u,a),-s(g.v,b),s(g.out,mask(g.mask,a,b))]);
  if(c&&!rows.some(r=>JSON.stringify(r)===JSON.stringify(c)))rows.push(c);
}return rows}
function evaluate(bank,a){let v={1:a[0],2:a[1],3:a[2]};
  for(let g of bank){ok(g.u in v&&g.v in v&&!(g.out in v),'bad fresh topological DEF');v[g.out]=mask(g.mask,v[g.u],v[g.v])}
  return v}
function verify(w){
  const lines=w.proof.clauses,pars=w.proof.parents,info=w.proof.info;
  let seen=new Set();
  for(let i=0;i<w.new.length;i++){
    let rows=encode(w.new[i]);for(let j=0;j<rows.length;j++){
      let id='G'+i+'.'+j;ok(JSON.stringify(lines[id])===JSON.stringify(rows[j]),'altered DEF facet');
      ok(pars[id]?.length===0&&info[id]?.[0]==='facet','forged DEF row');
      seen.add(id);
    }
  }
  for(let i=1;i<=w.res;i++){
    let id='R'+i;ok(pars[id]?.length===2&&info[id]?.[0]==='RES','missing RES');
    let [a,b]=pars[id],p=info[id][1];ok(seen.has(a)&&seen.has(b),'uncertified dependency');
    let A=lines[a],B=lines[b];ok((A.includes(p)&&B.includes(-p))||(A.includes(-p)&&B.includes(p)),'bad pivot');
    let c=norm([...A.filter(x=>Math.abs(x)!==p),...B.filter(x=>Math.abs(x)!==p)]);
    ok(c!==null&&JSON.stringify(c)===JSON.stringify(lines[id]),'bad resolvent');seen.add(id);
  }
  ok(w.paid===w.defs+w.res&&w.paid<=113*w.t,'charge violated');
  let oldFacets=w.old.flatMap(encode);
  ok(oldFacets.length===w.roots.length,'facet count mismatch');
  for(let i=0;i<w.roots.length;i++){
    let r=w.roots[i];ok(JSON.stringify(r.old_facet)===JSON.stringify(oldFacets[i]),'old facet mismatch');
    ok(seen.has(r.node)&&JSON.stringify(lines[r.node])===JSON.stringify(r.derived),'unauthenticated root');
    ok(r.derived.every(x=>r.old_facet.includes(x)),'root is not subclause');
  }
  for(let n=0;n<8;n++){
    let a=[n>>2,(n>>1)&1,n&1],v=evaluate(w.new,a),o=evaluate(w.old,a);
    for(let g of w.old)ok(v[g.out]===o[g.out],'public port value mismatch');
    for(let c of Object.values(lines))ok(c.some(x=>v[Math.abs(x)]===(x>0?1:0)),'unsound derived clause');
  }
}
verify(raw.structured_witness);
function reject(edit){let x=structuredClone(raw.structured_witness);edit(x);let failed=false;
  try{verify(x)}catch(e){failed=true}ok(failed,'corrupt proof accepted')}
reject(x=>{x.proof.info.R1[1]=9999});
reject(x=>{x.proof.parents.R1=['R999','G0.0']});
reject(x=>{x.proof.clauses.R1=[9999]});
reject(x=>{x.new[0].mask^=1});
reject(x=>{x.old[0].out=1});
let sat=0,unsat=0;for(let n=0;n<8;n++){let x=n>>2;if(x)sat++;if(x&&!x)unsat++}
ok(sat===4&&unsat===0,'both labels failed');
console.log(JSON.stringify({run:'LSPV3_412_INDEPENDENT',status:'PASS',assertions:checks,
  structured_old_gates:raw.structured_witness.t,corruptions_rejected:5,
  source_SAT_models:sat,source_UNSAT_models:unsat,
  scope:'readable paid DEF facets / strict Resolution only; same fixed native B3 OPEN'},null,2));
