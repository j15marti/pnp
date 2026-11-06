#!/usr/bin/env node
/* LSPV-3/441 compact independent full proof replay for LSPV-5/379 raw JSON.
   IMPORTANT: GATE-LOCAL is an explicitly proposed grammar, NOT historical R_mix341.
   node lspv3_441_full_gatelocal_compact_check.mjs 2026-11-05_2253_LSPV5_FULL_COOK_FACETA379.json
*/
import fs from 'node:fs';
import crypto from 'node:crypto';
const must=(b,msg)=>{if(!b)throw Error(msg)};
const norm=x=>[...new Set(x)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const same=(a,b)=>a.length===b.length&&a.every((v,i)=>v===b[i]);
function verify(t) {
  const hash=crypto.createHash('sha256').update(t.dimacs).digest('hex');
  must(hash===t.source_sha256,'original source SHA mismatch');
  const lines=t.dimacs.trim().split('\n'),hdr=lines.shift().split(' ');
  must(hdr[0]==='p'&&hdr[1]==='cnf','not DIMACS');
  const nv=+hdr[2],ns=+hdr[3];
  must(ns===t.strict3_source_clauses&&nv===t.source_variables,'source counts');
  must(t.trace.sources.length===ns&&lines.length===ns,'source identities');
  const C=new Map(),parents=new Map(),dp=new Map(),dp0=new Map(),D=new Map(),W=new Map();
  let checks=0,locals=0,resolutions=0,definitions=0;
  function sourceClause(line) {
    const v=line.trim().split(/\s+/).map(Number);
    must(v.at(-1)===0,'unterminated DIMACS');
    const c=v.slice(0,-1);
    must(c.length===3&&new Set(c.map(Math.abs)).size===3,'source is not proper strict three');
    must(c.every(x=>Math.abs(x)<=nv),'source var exceeds header');
    return norm(c);
  }
  lines.forEach((line,i)=>{
    const id='S'+(i+1),c=sourceClause(line);
    must(t.trace.sources[i].id===id&&same(c,norm(t.trace.sources[i].clause)),'source bytes vs proof');
    C.set(id,c);parents.set(id,[]);dp.set(id,0);dp0.set(id,0);checks++;
  });
  const outowner=new Map(),paid=new Set();
  for(const x of t.trace.nodes){
    must(!paid.has(x.id),'duplicate paid id');paid.add(x.id);
    if(x.kind==='def'){
      definitions++;
      must(x.out>nv&&!outowner.has(x.out)&&Math.abs(x.a)<x.out&&Math.abs(x.b)<x.out,'not fresh');
      must(Math.abs(x.a)!==Math.abs(x.b),'degenerate input');
      const want=[];
      for(const lit of [x.a,x.b])if(Math.abs(lit)>nv){
        const id=outowner.get(Math.abs(lit));must(id,'missing private owner');if(!want.includes(id))want.push(id);
      }
      const have=x.input_owners||[x.parent_owner].filter(Boolean);
      must(want.length===have.length&&want.every(p=>have.includes(p)),'wrong owner dependencies');
      outowner.set(x.out,x.id);D.set(x.id,x);parents.set(x.id,want);
      dp.set(x.id,1+Math.max(0,...want.map(p=>dp.get(p))));
      dp0.set(x.id,1+Math.max(0,...want.map(p=>dp0.get(p))));
      const facets=[[-x.out,x.a],[-x.out,x.b],[x.out,-x.a,-x.b]];
      for(let j=0;j<3;j++){
        const c=norm(facets[j]),id=x.id+'#f'+j,local='LC_'+x.id+'_f'+j;
        C.set(id,c);C.set(local,c);
        parents.set(local,[x.id]);dp.set(local,dp.get(x.id)+1);
        dp0.set(id,dp0.get(x.id));locals++;
        for(let mask=0;mask<8;mask++){
          const a=!!(mask&1),b=!!(mask&2),z=!!(mask&4);
          const v=new Map([[Math.abs(x.a),a],[Math.abs(x.b),b],[x.out,z]]);
          const val=lit=>lit>0?v.get(lit):!v.get(-lit);
          if(z===(val(x.a)&&val(x.b)))must(c.some(val),'false local facet');
          checks++;
        }
      }
    }else if(x.kind==='res'){
      resolutions++;
      const rewire=id=>id.includes('#f')?'LC_'+id.replace('#f','_f'):id;
      const a=rewire(x.left),b=rewire(x.right),A=C.get(a),B=C.get(b);
      must(A&&B,'missing resolution parent');
      must(A.includes(x.pivot)&&B.includes(-x.pivot),'wrong oriented resolution');
      const out=norm([...A.filter(y=>y!==x.pivot),...B.filter(y=>y!==-x.pivot)]);
      must(out.every(y=>!out.includes(-y)),'tautological result');
      C.set(x.id,out);parents.set(x.id,[a,b]);
      dp.set(x.id,1+Math.max(dp.get(a),dp.get(b)));
      const oldDepth=id=>dp0.get(id)||dp0.get(id.split('#')[0]);
      dp0.set(x.id,1+Math.max(oldDepth(x.left),oldDepth(x.right)));checks++;
    }else throw Error('unknown grammar node');
  }
  must(same(C.get(t.final_empty)||[],[]),'not empty final clause');
  must(definitions+resolutions===t.paid_full_refutation_work,'old paid count mismatch');
  must(dp0.get(t.final_empty)===t.critical_path_full,'old span mismatch');
  const seen=new Set(),stack=[t.final_empty];
  while(stack.length){
    const q=stack.pop();if(seen.has(q))continue;must(parents.has(q),'lost AND obligation '+q);
    seen.add(q);stack.push(...parents.get(q));
  }
  must(t.trace.sources.every(x=>seen.has(x.id)),'missing source ancestry');
  must(t.trace.nodes.every(x=>seen.has(x.id)),'dead paid node');
  for(const id of D.keys())for(let j=0;j<3;j++)must(seen.has('LC_'+id+'_f'+j),'dead or double-charged LOCAL');
  must(seen.size===ns+definitions+resolutions+locals,'wrong distinct union');
  return {ell:t.ell,source_hash:t.source_sha256,proper3_sources:ns,
    old_paid:t.paid_full_refutation_work,defs:definitions,res:resolutions,locals_added:locals,
    compiled_paid:definitions+resolutions+locals,old_span:dp0.get(t.final_empty),
    new_span:dp.get(t.final_empty),dependency_union_vertices:seen.size,checks};
}
const f=process.argv[2];
if(!f){console.error('Usage: node lspv3_441_full_gatelocal_compact_check.mjs REFEREE379.json');process.exit(2)}
const doc=JSON.parse(fs.readFileSync(f,'utf8'));
const result=doc.traces.map(verify);
console.log(JSON.stringify({status:'PASS, DECLARED GATE-LOCAL ONLY',result},null,2));
