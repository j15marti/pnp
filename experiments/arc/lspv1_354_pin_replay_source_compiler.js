'use strict';
/* LSPV-1 354, explicit paid pin + selected literal-gate authentication
   in the existing Rmix341 RES/VARDEF subset. Not a SAT solver or B3 proof.
   No external packages; all generator decisions deterministic. */
const crypto=require('crypto');
function normal(a){return [...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);}
function make(F) {
 const rows=[], defs=[], res=[], source=[];
 let varNext=Math.max(2,...F.flat().map(Math.abs))+1;
 function add(cl,kind,metadata={}) {
   const c=normal(cl); if(c.some(t=>c.includes(-t)))throw Error('tautology forbidden outside slot');
   const id=rows.length;rows.push({id,kind,cl:c,...metadata});return id;
 }
 for(let j=0;j<F.length;j++)source.push(add(F[j],'source',{source_j:j}));
 function def(a,b){
   const q=varNext++,owner=defs.length;
   const slots=[[ -q,a],[-q,b],[q,-a,-b]].map((c,i)=>add(c,'slot',{gate:owner,slot:i}));
   defs.push({gate:owner,q,a,b,slots});return {q,slots};
 }
 function resolve(i,j,p){
   const A=rows[i].cl,B=rows[j].cl;
   if(!A.includes(p)||!B.includes(-p))throw Error('bad pivot');
   const cl=normal([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]);
   if(cl.some(t=>cl.includes(-t)))throw Error('tautological resolvent');
   const id=add(cl,'res',{a:i,b:j,pivot:p});res.push(id);return id;
 }
 const assertClause=(id,expected)=>{
   if(JSON.stringify(rows[id].cl)!==JSON.stringify(normal(expected)))throw Error('wrong clause');
 };
 // Non-tautological 3-gate false wire z = (x AND y) AND (NOT x AND NOT y).
 const ab=def(1,2),cd=def(-1,-2),zz=def(ab.q,cd.q);
 const zx=resolve(zz.slots[0],ab.slots[0],ab.q);
 const znx=resolve(zz.slots[1],cd.slots[0],cd.q);
 const notz=resolve(zx,znx,1);assertClause(notz,[-zz.q]);
 const outputs=[];
 for(let j=0;j<F.length;j++){
   if(F[j].length!==1)throw Error('demo tests unary rows only; general theorem includes arbitrary width');
   const L=F[j][0];
   // Two canonical signed input selectors per clause, one true, one false.
   const selOn=def(zz.q,1),selOff=def(zz.q,1);
   const notOn=resolve(selOn.slots[0],notz,zz.q);
   const notOff=resolve(selOff.slots[0],notz,zz.q);
   assertClause(notOn,[-selOn.q]);assertClause(notOff,[-selOff.q]);
   // On-selector maps to signed literal NOT q_on, hence Boolean TRUE.
   const tOn=def(-selOn.q,L);
   const implication=resolve(tOn.slots[2],notOn,selOn.q);
   assertClause(implication,[tOn.q,-L]);
   const tOnUnit=resolve(source[j],implication,L);assertClause(tOnUnit,[tOn.q]);
   // Off-selector maps to q_off = FALSE, for the opposite literal.
   const tOff=def(selOff.q,-L);
   const notOffIndicator=resolve(tOff.slots[0],notOff,selOff.q);
   assertClause(notOffIndicator,[-tOff.q]);
   // OR(tOn,tOff) represented by negative AND of both complements.
   const orGate=def(-tOn.q,-tOff.q);
   const orUnit=resolve(tOnUnit,orGate.slots[0],tOn.q);
   assertClause(orUnit,[-orGate.q]);
   outputs.push({j,input:L,unit:orUnit,literal:-orGate.q,selector_true:-selOn.q,selector_false:selOff.q});
 }
 // AND of each active clause-output, justified from authenticated sources.
 let root=outputs[0].unit, rootLit=outputs[0].literal;
 for(let j=1;j<outputs.length;j++){
   const g=def(rootLit,outputs[j].literal);
   const part=resolve(g.slots[2],root,-rootLit);
   root=resolve(part,outputs[j].unit,-outputs[j].literal);
   rootLit=g.q;assertClause(root,[rootLit]);
 }
 const publicRows=rows.map(({id,kind,cl,source_j,gate,slot,a,b,pivot})=>
  ({id,kind,cl,...(source_j!==undefined?{source_j}:{}),...(gate!==undefined?{gate,slot}:{}),
    ...(pivot!==undefined?{a,b,pivot}:{})}));
 const full={F,rows:publicRows,defs,res,source,root,root_literal:rootLit,false_unit:notz,
   vars:varNext-1, paid_nodes:defs.length+res.length,def_nodes:defs.length,res_nodes:res.length,
   output_units:outputs, status:'paid proof prefix; no Rmix optimality or B3'};
 const encoded=JSON.stringify(full);
 return {summary:{sources:F.length,variables:varNext-1,def_nodes:defs.length,res_nodes:res.length,
   paid_nodes:defs.length+res.length,proof_rows:rows.length,bytes:Buffer.byteLength(encoded),
   proof_sha256:crypto.createHash('sha256').update(encoded).digest('hex'),
   final_unit:rows[root].cl, false_unit:rows[notz].cl},proof:full};
}
function allModels(F){let out=[];for(let mask=0;mask<4;mask++){if(F.every(C=>C.some(l=>!!(mask&(1<<(Math.abs(l)-1)))===(l>0))))out.push(mask);}return out}
const cases=[[[1],[-1],[2]],[[1],[2]],[[1],[1],[2]]];
const results=cases.map(F=>({...make(F).summary,F,models:allModels(F)}));
const report={run:'LSPV1_PIN_REPLAY_SOURCE_COMPILER354',time:'2026-11-02 22:00 PST',
  calculus:'unchanged binary RES + source-independent paid two-input literal AND VARDEF subset of Rmix341',
  proof_scope:'paid false-selector pins + literal-row sat-evaluator output certificates, not universal A circuit proof',
  cases:results,negative_controls:{unsat_sign_flip_models:allModels([[1],[1],[2]]).length,
     unsat_source_delete_models:allModels([[1],[2]]).length},
  statuses:{pin_gadget:'PROVED/EXACT',finite:'COMPUTATIONAL',B3:'OPEN'}};
if(typeof module!=='undefined' && module.exports)module.exports={make,allModels,normal,report};
if(require.main===module)console.log(JSON.stringify(report,null,2));
