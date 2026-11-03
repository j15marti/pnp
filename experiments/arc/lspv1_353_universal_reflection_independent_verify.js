#!/usr/bin/env node
'use strict';
// Independent no-producer-import verifier for LSPV-1 353 Rmix341 AND3+XOR.
// Run: node experiments/arc/lspv1_353_universal_reflection_independent_verify.js
//      results/raw/arc/2026-11-02_2100_LSPV1_UNIVERSAL_REFLECTION_SINGLE_FAMILY353.json
const fs=require('fs'),crypto=require('crypto');
let n=0;
function chk(ok,msg){n++;if(!ok)throw Error('FAIL '+msg);}
const d=JSON.parse(fs.readFileSync(process.argv[2],'utf8')),C=d.source_clauses;
const assignments=Array.from({length:8},(_,i)=>[i&1,(i>>1)&1,(i>>2)&1]);
const clause=(c,a)=>c.some(x=>((a[Math.abs(x)-1]===1)===(x>0)));
const satisfy=(cs,a)=>cs.every(c=>clause(c,a));
const count=cs=>assignments.filter(a=>satisfy(cs,a));
const pt=(mask,rhs,a)=>Number((a.reduce((t,x,i)=>t+((mask>>i&1)?x:0),0)%2)===rhs);
const table=(mask,rhs)=>assignments.reduce((s,a,i)=>s|(pt(mask,rhs,a)<<i),0);
const sourceTruth=c=>assignments.reduce((s,a,i)=>s|(Number(clause(c,a))<<i),0);
chk(d.source_count===6,'sources');chk(d.variables===3,'variables');
chk(C.length===6&&C.every(c=>c.length===2),'clauses');
const serial='p cnf 3 6\n'+C.map(c=>c.join(' ')+' 0\n').join('');
chk(serial===d.dimacs,'DIMACS');chk(Buffer.byteLength(serial)===52,'ASCII bytes');
chk(crypto.createHash('sha256').update(serial).digest('hex')===d.source_sha256,'source SHA256');
chk(count(C).length===0,'source UNSAT');
for(let i=0;i<C.length;i++){
 const w=count(C.filter((_,j)=>j!==i));
 chk(w.length===1,'clause deletion exact SAT witness');
 chk(w.some(a=>JSON.stringify(a)===JSON.stringify(d.source_deletion_sat_witnesses[i].witness_bits)),'signed witness');
 for(let j=0;j<2;j++){
  const clone=C.map(c=>c.slice());clone[i][j]*=-1;
  const z=count(clone);
  chk(z.length>0,'one literal sign flip SAT');
  const r=d.one_literal_sign_flip_sat_neighbors.find(x=>x.clause===i+1&&x.literal===j+1);
  chk(r&&r.models===z.length,'neighbor count');
 }
}
const initial=C.map((c,i)=>({type:'SOURCE',t:sourceTruth(c),mask:null,rhs:null,anc:1<<i}));
function replay(steps){
 let db=initial.map(x=>({...x}));
 try {
  for(const p of steps){
   if(p.id!==db.length||!Array.isArray(p.parents)||p.parents.length!==2)return false;
   const [i,j]=p.parents;if(!Number.isInteger(i)||!Number.isInteger(j)||i<0||j<0||i>=p.id||j>=p.id)return false;
   const a=db[i],b=db[j];let mask,rhs,t;
   if(p.rule==='AND3'){
    if(a.type!=='SOURCE'||b.type!=='SOURCE')return false;
    mask=p.mask;rhs=p.rhs;t=a.t&b.t;
    if(t!==table(mask,rhs))return false;
    for(const v of assignments){
     const actual=Number(clause(C[i],v)&&clause(C[j],v));
     if(actual!==pt(mask,rhs,v))return false;
    }
   }else if(p.rule==='XOR'){
    if(a.mask===null||b.mask===null)return false;
    mask=a.mask^b.mask;rhs=a.rhs^b.rhs;t=table(mask,rhs);
    if(p.mask!==mask||p.rhs!==rhs||((a.t&b.t)&~t)!==0)return false;
   }else return false;
   db.push({type:p.rule,t,mask,rhs,anc:a.anc|b.anc});
  }
  const end=db.at(-1);
  return steps.length===5&&end.t===0&&end.mask===0&&end.rhs===1&&end.anc===63;
 }catch(e){return false;}
}
chk(d.certified_global_lower===5&&d.legal_mixed_upper===5,'analytic m-1 lower and legal upper');
chk(replay(d.proof),'legal five-node AND3/XOR full DAG');
for(const step of d.proof){chk(step.parents.length===2,'arity');chk(step.id>=6,'paid derived node');}
for(let a=0;a<2;a++)for(let b=0;b<2;b++){
 const z=[0,1].filter(x=>x!==a&&x!==b);
 const rec=d.original_two_signed_unit_both_labels.find(x=>x.a===a&&x.b===b);
 chk(rec&&rec.label===(a===b?'SAT':'UNSAT')&&rec.original_models===z.length,'both-label control');
}
const fail=[...assignments].filter(x=>x[2]!==x[0]&&x[2]!==x[1]);
chk(fail.length===2,'unsound reject-all is satisfiable');
const parse=t=>{
 const lines=t.split('\n');if(lines.at(-1)!=='')return false;lines.pop();
 if(lines.length!==7||lines[0]!=='p cnf 3 6')return false;
 return lines.slice(1).every(s=>/^[-]?[1-3] [-]?[1-3] 0$/.test(s));
};
chk(parse(serial),'valid original syntax');
for(const s of [serial.slice(0,-2),serial.replace('p cnf 3 6','p cnf 3 5'),
 serial.replace('p cnf 3 6','p cnf 2 6'),serial+'2\n',
 serial.replace(' 0\n',' 0 0\n'),serial+'0\n'])chk(!parse(s),'malformed source rejected');
let v=d.proof.map(x=>({...x,parents:x.parents.slice()}));v[0].rhs=0;chk(!replay(v),'corrupt AND3 output');
v=d.proof.map(x=>({...x,parents:x.parents.slice()}));v[3].mask=1;chk(!replay(v),'corrupt XOR mask');
v=d.proof.map(x=>({...x,parents:x.parents.slice()}));v[4].parents=[9,7];chk(!replay(v),'corrupt XOR parent');
chk(!replay(d.proof.slice(0,-1)),'truncated DAG');
v=d.proof.map(x=>({...x,parents:x.parents.slice()}));v[1].parents=[1,999];chk(!replay(v),'future parent rejected');
console.log(JSON.stringify({status:'PASS',assertions:n,exact_minimum:5,source_sha256:d.source_sha256,
 malformed_rejected:6,corrupted_proofs_rejected:5},null,2));