#!/usr/bin/env node
/* Independent REFEREE380 verifier.  Reconstructs every clause and owner facet. */
'use strict';

import fs from 'node:fs';
import crypto from 'node:crypto';

const path = process.argv[2] || 'results/raw/review/2026-11-05_2352_LSPV5_GUARD_LIFT_FACETA380.json';
const original = JSON.parse(fs.readFileSync(path, 'utf8'));
let checks = 0;
const ck = (x, m='check') => { checks++; if (!x) throw Error(m); };
const norm = c => [...new Set(c)].sort((x,y)=>Math.abs(x)-Math.abs(y)||(x<0?-1:1));
const eq = (a,b) => JSON.stringify(a)===JSON.stringify(b);
const sha = s => crypto.createHash('sha256').update(s).digest('hex');
const proper = c => c.length===3 && new Set(c.map(Math.abs)).size===3 && !c.some(x=>c.includes(-x));

function dimacs(v, clauses) {
  return `p cnf ${v} ${clauses.length}\n${clauses.map(c=>c.join(' ')+' 0').join('\n')}\n`;
}

function verify(doc) {
  ck(doc.run==='LSPV-5/REFEREE380','run');
  ck(doc.historical_authoritative_checker===false,'historical scope');
  ck(doc.target_is_refutation===false,'target scope');
  for (const t of doc.traces) {
    const n=1<<t.ell, pairs=n*n*(n+1)/2;
    const S=pairs*(2*t.ell-2);
    ck(t.old_source_clauses===S,'old S');
    ck(t.guard_variable===t.old_source_variables+1,'guard freshness');
    ck(t.auxiliary_shift===S+1,'shift');
    ck(t.source_variables===t.old_source_variables+S+1,'source max');
    ck(t.final_variables_after_def===t.old_final_variables+S+1,'final max');
    ck(t.trace.sources.length===2*S,'guard source count');
    const sourceClauses=t.trace.sources.map(x=>x.clause);
    ck(sourceClauses.every(proper),'proper 3');
    const text=dimacs(t.source_variables,sourceClauses);
    ck(text===t.dimacs,'dimacs exact');
    ck(Buffer.byteLength(text)===t.source_bytes,'source bytes');
    ck(sha(text)===t.source_sha256,'source hash');
    const ids=new Set(), clauses=new Map(), depth=new Map(), deps=new Map(), ownerByVar=new Map();
    for (const s of t.trace.sources) {
      ck(!ids.has(s.id),'duplicate source'); ids.add(s.id);
      ck(s.clause.every(l=>Math.abs(l)<=t.source_variables),'source bound');
      clauses.set(s.id,norm(s.clause)); depth.set(s.id,0); deps.set(s.id,[]);
    }
    const oldRecovered=[];
    for(let i=1;i<=S;i++){
      const y=t.old_source_variables+1+i;
      const L=clauses.get(`GS${2*i-1}`), R=clauses.get(`GS${2*i}`);
      ck(L.includes(t.guard_variable)&&L.includes(y),'left guard shape');
      ck(R.includes(-y),'right guard shape');
      const a=L.find(x=>x!==t.guard_variable&&x!==y);
      const bc=R.filter(x=>x!==-y);
      ck(bc.length===2,'right arity');
      oldRecovered.push(norm([a,...bc]));
    }
    const oldText=dimacs(t.old_source_variables,oldRecovered);
    ck(sha(oldText)===t.old_source_sha256,'old source identity');

    // Construct every one-source-deletion g=0 witness.  The old strict-3
    // sources are private chains of the bit-PHP collision clauses.
    const chainLen=2*t.ell-2, auxPerWide=2*t.ell-3, pigeons=n+1;
    const wideMeta=[];
    for(let i=0;i<pigeons;i++) for(let j=i+1;j<pigeons;j++) for(let a=0;a<n;a++) wideMeta.push([i,j,a]);
    ck(wideMeta.length*chainLen===S,'wide source layout');
    const litTrue=(l,A)=>A.get(Math.abs(l))===(l>0);
    function deletionAssignment(targetClause){
      const tw=Math.floor(targetClause/chainLen), tp=targetClause%chainLen;
      const [pi,pj,addr]=wideMeta[tw];
      const address=new Array(pigeons), rest=[];
      for(let a=0;a<n;a++) if(a!==addr) rest.push(a);
      address[pi]=addr; address[pj]=addr;
      let z=0; for(let p=0;p<pigeons;p++) if(p!==pi&&p!==pj) address[p]=rest[z++];
      const A=new Map();
      for(let p=0;p<pigeons;p++) for(let bit=0;bit<t.ell;bit++) A.set(1+p*t.ell+bit,Boolean((address[p]>>(t.ell-1-bit))&1));
      for(let w=0;w<wideMeta.length;w++){
        const [i,j,a]=wideMeta[w], bits=Array.from({length:t.ell},(_,bit)=>(a>>(t.ell-1-bit))&1);
        const wide=[];
        for(const p of [i,j]) for(let bit=0;bit<t.ell;bit++){
          const v=1+p*t.ell+bit; wide.push(bits[bit]?-v:v);
        }
        for(let q=0;q<auxPerWide;q++){
          const v=pigeons*t.ell+w*auxPerWide+q+1;
          const val=w===tw ? q<tp : wide.slice(0,q+2).every(l=>!litTrue(l,A));
          A.set(v,val);
        }
      }
      return A;
    }
    let deletionWitnesses=0;
    for(let q=0;q<S;q++){
      const A=deletionAssignment(q);
      for(let k=0;k<S;k++) ck(oldRecovered[k].some(l=>litTrue(l,A))===(k!==q),'old deletion witness');
      for(let side=0;side<2;side++){
        const B=new Map(A); B.set(t.guard_variable,false);
        for(let k=0;k<S;k++){
          const [a,b,c]=oldRecovered[k];
          const y=t.old_source_variables+2+k;
          B.set(y,k===q ? side===1 : !litTrue(a,B));
        }
        const removed=2*q+side;
        for(let k=0;k<2*S;k++) ck(sourceClauses[k].some(l=>litTrue(l,B))===(k!==removed),'guard deletion witness');
        deletionWitnesses++;
      }
    }
    ck(deletionWitnesses===2*S,'all deletion witnesses');
    ck(t.all_rule_binary_premise_source_floor===2*S-1,'source floor');

    function facet(ref) {
      const m=/^(.+)#f([0-2])$/.exec(ref); if(!m) return null;
      const d=nodeById.get(m[1]); ck(d&&d.kind==='def','facet owner');
      const z=d.out,a=d.a,b=d.b;
      return [norm([-z,a]),norm([-z,b]),norm([z,-a,-b])][Number(m[2])];
    }
    function clause(ref){ return ref.includes('#f')?facet(ref):clauses.get(ref); }
    function depId(ref){ return ref.split('#f')[0]; }
    const nodeById=new Map();
    let guardNodes=0, defCount=0, resCount=0;
    for(const node of t.trace.nodes){
      ck(!ids.has(node.id),'duplicate node'); ids.add(node.id); nodeById.set(node.id,node);
      if(node.kind==='def'){
        defCount++;
        ck(node.out>t.source_variables&&node.out<=t.final_variables_after_def,'def freshness range');
        ck(!ownerByVar.has(node.out),'def unique output');
        for(const lit of [node.a,node.b]){
          const v=Math.abs(lit);
          ck(v<=t.old_source_variables || v>t.source_variables,'alpha-renamed input');
          if(v>t.source_variables) ck(ownerByVar.has(v),'owned auxiliary input');
        }
        const owners=[...new Set([node.a,node.b].map(Math.abs).filter(v=>v>t.source_variables).map(v=>ownerByVar.get(v)))].sort();
        if(Object.hasOwn(node,'parent_owner')) ck((node.parent_owner===null&&owners.length===0)||(owners.length===1&&node.parent_owner===owners[0]),'parent owner');
        if(Object.hasOwn(node,'input_owners')) ck(eq([...node.input_owners].sort(),owners),'input owners');
        ownerByVar.set(node.out,node.id);
        clauses.set(node.id,null);
        depth.set(node.id,1+Math.max(0,...owners.map(o=>depth.get(o))));
        deps.set(node.id,owners);
      } else {
        ck(node.kind==='res','node kind'); resCount++;
        const c1=clause(node.left), c2=clause(node.right);
        ck(Array.isArray(c1)&&Array.isArray(c2),'antecedents');
        ck(c1.includes(node.pivot)&&c2.includes(-node.pivot),'oriented pivot');
        const out=norm([...c1.filter(x=>x!==node.pivot),...c2.filter(x=>x!==-node.pivot)]);
        ck(!out.some(x=>out.includes(-x)),'tautological resolvent');
        clauses.set(node.id,out);
        const dl=depId(node.left), dr=depId(node.right);
        ck(depth.has(dl)&&depth.has(dr),'dependency order');
        depth.set(node.id,1+Math.max(depth.get(dl),depth.get(dr)));
        deps.set(node.id,[dl,dr]);
        if(node.id.startsWith('G_R')){
          guardNodes++;
          const i=Number(node.id.slice(3));
          ck(node.left===`GS${2*i-1}`&&node.right===`GS${2*i}`,'guard parents');
          ck(node.pivot===t.old_source_variables+1+i,'guard pivot');
          ck(eq(out,t.recovered_guarded_clauses[i-1]),'guarded clause');
        } else {
          ck(!node.left.match(/^S\d+$/)&&!node.right.match(/^S\d+$/),'no old source leak');
        }
      }
    }
    ck(guardNodes===S,'guard node count');
    ck(defCount+resCount===t.paid_guarded_unit_work,'work count');
    const cook=n*(n+1)*(27*n*n+11*n-14)/24;
    const oldWork=pairs*(4*t.ell-3)+(n+1)*(2*n*t.ell-9)+cook;
    ck(t.base_refutation_work===oldWork,'base formula');
    ck(t.paid_guarded_unit_formula===oldWork+S,'guard formula');
    ck(eq(clauses.get(t.final_guard_unit),[t.guard_variable]),'final guard unit');
    ck(depth.get(t.final_guard_unit)===t.critical_path_guarded_unit,'span');
    ck(t.critical_path_formula===t.critical_path_guarded_unit,'span formula');
    const live=new Set(), stack=[t.final_guard_unit];
    while(stack.length){ const x=stack.pop(); if(live.has(x))continue; live.add(x); for(const y of deps.get(x)||[])stack.push(y); }
    ck(t.trace.nodes.every(x=>live.has(x.id)),'all paid nodes live');
    ck(t.trace.sources.every(x=>live.has(x.id)),'all sources live');
  }
  return true;
}

verify(original);
const attacks=[];
function hostile(name, mut){
  const d=structuredClone(original); mut(d);
  let rejected=false; try{verify(d);}catch{rejected=true;} ck(rejected,`hostile accepted: ${name}`); attacks.push(name);
}
hostile('wrong guard pivot',d=>d.traces[0].trace.nodes[0].pivot++);
hostile('nonfresh guard variable',d=>d.traces[0].guard_variable=1);
hostile('unshifted DEF output',d=>{const x=d.traces[0].trace.nodes.find(n=>n.kind==='def');x.out=d.traces[0].old_source_variables+1;});
hostile('corrupt source hash',d=>d.traces[0].source_sha256='00');
hostile('corrupt guarded source',d=>d.traces[0].trace.sources[0].clause[0]*=-1);
hostile('old source reference leak',d=>{const x=d.traces[0].trace.nodes.find(n=>n.id==='R1');x.left='S1';});
hostile('false final target',d=>d.traces[0].final_guard_unit='G_R1');

const summary={
  status:'COMPUTATIONAL complete declared FACET-A guarded-unit derivations accepted',
  checks, hostile_rejected:attacks.length,
  raw_sha256:sha(fs.readFileSync(path)), raw_bytes:fs.statSync(path).size,
  traces:original.traces.map(t=>({ell:t.ell,guarded_sources:t.strict3_guarded_source_clauses,work:t.paid_guarded_unit_work,span:t.critical_path_guarded_unit,final:t.final_guard_unit}))
};
console.log(JSON.stringify(summary,null,2));
