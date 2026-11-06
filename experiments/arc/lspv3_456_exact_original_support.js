#!/usr/bin/env node
'use strict';
// LSPV-3/456; original-coordinate support audit of LSPV-5/379 FACET-A (NOT historical native R_mix341).
// Run: node experiments/arc/lspv3_456_exact_original_support.js results/raw/review/2026-11-05_2253_LSPV5_FULL_COOK_FACETA379.json
function ck(p,msg){if(!p)throw Error(msg);}
function audit(t){
 const rows=t.dimacs.trim().split(/\r?\n/),head=rows.shift().trim().split(/\s+/);
 ck(head[0]==='p'&&head[1]==='cnf'&&+head[2]===t.source_variables&&+head[3]===t.strict3_source_clauses,'bad DIMACS header');
 ck(rows.length===t.trace.sources.length&&rows.length===t.strict3_source_clauses,'source count');
 const clauses=new Map(),defs=t.trace.nodes.filter(x=>x.kind==='def'),owners=new Map(),ids=new Set();
 for(let j=0;j<rows.length;j++){
  const a=rows[j].trim().split(/\s+/).map(Number),s=t.trace.sources[j];
  ck(a.length===4&&a[3]===0&&a.slice(0,3).every(x=>Number.isInteger(x)&&x!==0&&Math.abs(x)<=t.source_variables),'source width/range/terminator');
  ck(s.id==='S'+(j+1)&&JSON.stringify(s.clause)===JSON.stringify(a.slice(0,3)),'source mismatch');
  clauses.set(s.id,s.clause);ids.add(s.id);
 }
 const nodes=[null,null],unique=new Map(),vs=new Map(),roots=new Map(),notmemo=new Map(),andmemo=new Map();let and_calls=0;
 function mk(v,lo,hi){if(lo===hi)return lo;const k=v+','+lo+','+hi;if(unique.has(k))return unique.get(k);const i=nodes.length;nodes.push({v,lo,hi});unique.set(k,i);return i;}
 function nt(i){if(i<2)return 1-i;if(notmemo.has(i))return notmemo.get(i);const n=nodes[i],v=mk(n.v,nt(n.lo),nt(n.hi));notmemo.set(i,v);return v;}
 function an(a,b){and_calls++;if(a===0||b===0)return 0;if(a===1)return b;if(b===1||a===b)return a;if(a>b){let t=a;a=b;b=t;}const k=a+','+b;if(andmemo.has(k))return andmemo.get(k);const x=nodes[a],y=nodes[b],v=Math.min(x.v,y.v),r=mk(v,an(x.v===v?x.lo:a,y.v===v?y.lo:b),an(x.v===v?x.hi:a,y.v===v?y.hi:b));andmemo.set(k,r);return r;}
 function lit(s){let k=Math.abs(s),r=roots.get(k);if(r===undefined){ck(k<=t.source_variables&&k>0,'forward DEF wire');if(!vs.has(k))vs.set(k,mk(k,0,1));r=vs.get(k);}return s>0?r:nt(r);}
 for(const d of defs){
  ck(!ids.has(d.id)&&!roots.has(d.out)&&d.out>t.source_variables&&Number.isInteger(d.out),'bad DEF owner/output');
  const r=an(lit(d.a),lit(d.b));roots.set(d.out,r);owners.set(d.id,d);ids.add(d.id);
 }
 const cache=new Map();
 function supp(r){if(r<2)return new Set();if(cache.has(r))return cache.get(r);const n=nodes[r],s=new Set([n.v,...supp(n.lo),...supp(n.hi)]);cache.set(r,s);return s;}
 const details=defs.map(d=>({id:d.id,out:d.out,a:d.a,b:d.b,essential:[...supp(roots.get(d.out))].sort((a,b)=>a-b)}));
 const supportByOwner=new Map(details.map(d=>[d.id,d.essential]));
 const hist={};for(const d of details)hist[d.essential.length]=(hist[d.essential.length]||0)+1;
 const refCount={count:0,wide:0,byType:{},unique:new Set(),owners:new Set()};
 function parent(id){
  if(typeof id!=='string')throw Error('untyped parent');
  if(id.includes('#f')){
   const p=id.split('#f');ck(p.length===2&&/^[012]$/.test(p[1]),'invalid facet index');
   const d=owners.get(p[0]);ck(d!==undefined,'no paid DEF owner');
   const f=+p[1],v=f===0?[-d.out,d.a]:f===1?[-d.out,d.b]:[d.out,-d.a,-d.b];
   refCount.count++;refCount.unique.add(id);refCount.owners.add(d.id);
   if(supportByOwner.get(d.id).length>3){refCount.wide++;refCount.byType[f]=(refCount.byType[f]||0)+1;}
   return v;
  }
  ck(clauses.has(id),'missing/forward RES/SOURCE parent '+id);return clauses.get(id);
 }
 let paid=0;
 for(const x of t.trace.nodes){
  if(x.kind==='def'){paid++;continue;}
  ck(x.kind==='res'&&!ids.has(x.id),'bad RES node type/ID');
  const l=parent(x.left),r=parent(x.right),p=x.pivot;
  ck(l.includes(p)&&r.includes(-p),'wrong oriented pivot: '+x.id);
  const c=[...new Set([...l.filter(v=>v!==p),...r.filter(v=>v!==-p)])];
  ck(!c.some(v=>c.includes(-v)),'tautological resolvent: '+x.id);
  clauses.set(x.id,c);ids.add(x.id);paid++;
 }
 ck(paid===t.paid_full_refutation_work,'paid count');
 ck(clauses.has(t.final_empty)&&clauses.get(t.final_empty).length===0,'missing empty-clause root');
 let brute=null;
 if(t.ell===2){
  const original=[...new Set(defs.flatMap(d=>[Math.abs(d.a),Math.abs(d.b)]).filter(x=>x<=t.source_variables))].sort((a,b)=>a-b);
  ck(original.length===10,'unexpected address-bit count');
  const index=new Map(original.map((x,i)=>[x,i])),num=1<<original.length,values=defs.map(()=>new Uint8Array(num));
  for(let a=0;a<num;a++){
   const val=new Map();function v(s){let u=Math.abs(s),b=val.has(u)?val.get(u):((a>>index.get(u))&1);return s>0?b:1-b;}
   for(let j=0;j<defs.length;j++){const d=defs[j],out=v(d.a)&v(d.b);val.set(d.out,out);values[j][a]=out;}
  }
  for(let j=0;j<defs.length;j++){
   const ess=[];
   for(let k=0;k<original.length;k++){
    let seen=false;for(let a=0;a<num;a++){if(values[j][a]!==values[j][a^(1<<k)]){seen=true;break;}}
    if(seen)ess.push(original[k]);
   }
   ck(JSON.stringify(ess)===JSON.stringify(details[j].essential),'brute/BDD mismatch '+defs[j].id);
  }
  brute={pass:true,assignments:num,evaluations:num*defs.length,bit_flip_comparisons:num*original.length*defs.length};
 }
 const gt3=details.filter(d=>d.essential.length>3);
 const uniqWide=[...refCount.unique].filter(s=>supportByOwner.get(s.split('#f')[0]).length>3);
 return {ell:t.ell,source_sha256_as_stated:t.source_sha256,source_variables:t.source_variables,source_clauses:t.strict3_source_clauses,
  verified_empty_root:true,paid_nodes:paid,def_count:defs.length,essential_support_histogram:hist,max_essential_original_support:Math.max(...details.map(d=>d.essential.length)),
  def_essential_support_gt3:gt3.length,total_facet_references:refCount.count,wide_owner_facet_references:refCount.wide,
  wide_owner_facet_references_by_facet:refCount.byType,unique_wide_owner_facets:uniqWide.length,all_unique_owner_facets:refCount.unique.size,
  owners_used:refCount.owners.size,first_essential_gt3:gt3[0],bdd_nodes:nodes.length,bdd_and_calls:and_calls,independent_truth_table:brute};
}
if(typeof module!=='undefined'&&require.main===module){
 const fs=require('fs'),p=process.argv[2];if(!p){console.error('Provide LSPV-5/379 raw JSON path');process.exit(2);}
 const start=process.hrtime.bigint(),raw=JSON.parse(fs.readFileSync(p,'utf8')),result=raw.traces.map(audit);
 console.log(JSON.stringify({run_id:'LSPV-3/456',status:'COMPUTATIONAL, model Rmix341 historical acceptance OPEN',results:result,
 elapsed_ms:Number(process.hrtime.bigint()-start)/1e6,rss_sample_bytes:process.memoryUsage().rss},null,2));
}
