#!/usr/bin/env node
'use strict';
const fs=require('fs'); const raw=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
function norm(xs){const s=new Set(xs);for(const x of s)if(s.has(-x))return null;return [...s].sort((x,y)=>Math.abs(x)-Math.abs(y)||((x<0)-(y<0)));}
function key(x){return JSON.stringify(x)}
function andSlots(q,a,b){return [[-q,a],[-q,b],[q,-a,-b]].map(norm)}
function xorSlots(q,a,b){return [[a,b,-q],[a,-b,q],[-a,b,q],[-a,-b,-q]].map(norm)}
function resolve(a,b,p){if(!a.includes(p)||!b.includes(-p))throw Error('pivot');return norm(a.filter(x=>x!==p).concat(b.filter(x=>x!==-p)));}
const [a,b,c,x,xp,y,u,v,p,q,r,s]=Array.from({length:12},(_,i)=>i+1);
function allowed(t){
 let z=[];const add=(k,cs)=>cs.forEach(C=>z.push(k+'|'+key(C)));
 if(t==='equality_transitivity'){
  add('ASSUME_q_eq_r',[norm([-q,r]),norm([q,-r])]);add('ASSUME_r_eq_s',[norm([-r,s]),norm([r,-s])]);return new Set(z);
 }
 const gate=t.startsWith('and_')?'and':'xor', slots=gate==='and'?andSlots:xorSlots;
 if(t.includes('commutativity')||t.includes('commuted_miter')){
  add(`DEF_${gate}_q_ab`,slots(q,a,b));add(`DEF_${gate}_r_ba`,slots(r,b,a));
  if(t.includes('miter')){add('UNIT_q',[norm([q])]);add('UNIT_not_r',[norm([-r])]);}
 } else if(t.includes('associativity')||t.includes('associated_miter')){
  add(`DEF_${gate}_u_ab`,slots(u,a,b));add(`DEF_${gate}_v_uc`,slots(v,u,c));
  add(`DEF_${gate}_p_bc`,slots(p,b,c));add(`DEF_${gate}_q_ap`,slots(q,a,p));
  if(t.includes('miter')){add('UNIT_v',[norm([v])]);add('UNIT_not_q',[norm([-q])]);}
 } else if(t.includes('congruence')){
  add('ASSUME_x_eq_xp',[norm([-x,xp]),norm([x,-xp])]);
  add(`DEF_${gate}_q_xy`,slots(q,x,y));add(`DEF_${gate}_r_xpy`,slots(r,xp,y));
 } else throw Error('unknown '+t);
 return new Set(z);
}
let R=0,L=0;
for(const t of raw.templates){
 const ok=allowed(t.name), lines=[];let rcount=0;
 for(let i=0;i<t.lines.length;i++){
  const X=t.lines[i], n=norm(X.clause);if(n===null||key(n)!==key(X.clause))throw Error(t.name+' canonical');
  if(X.kind==='RES'){
   if(!(X.left<i&&X.right<i))throw Error(t.name+' parent');
   const got=resolve(lines[X.left],lines[X.right],X.pivot);if(got===null||key(got)!==key(X.clause))throw Error(t.name+' resolvent');rcount++;
  } else if(!ok.has(X.kind+'|'+key(X.clause)))throw Error(t.name+' source '+X.kind);
  lines.push(X.clause);
 }
 for(const j of t.targets)if(j<0||j>=lines.length)throw Error(t.name+' target');
 if(t.name.includes('miter')&&!t.targets.some(j=>lines[j].length===0))throw Error(t.name+' no empty');
 if(rcount!==t.resolution_lines)throw Error(t.name+' count');R+=rcount;L+=lines.length;
}
if(R!==raw.totals.resolution_lines||L!==raw.totals.certificate_lines)throw Error('totals');
function sat(cnf,n){for(let mask=0;mask<(1<<n);mask++){let good=true;for(const C of cnf){let hit=false;for(const l of C){const bit=(mask>>(Math.abs(l)-1))&1;if((l>0)===Boolean(bit)){hit=true;break}}if(!hit){good=false;break}}if(good)return true}return false}
const xorSame=xorSlots(u,a,b).concat(xorSlots(v,u,c),xorSlots(p,b,c),xorSlots(q,a,p),[[v],[q]]);
const mixed=xorSlots(u,a,b).concat(xorSlots(v,u,c),andSlots(p,b,c),xorSlots(q,a,p),[[v],[-q]]);
if(!sat(xorSame,10)||!sat(mixed,10))throw Error('SAT neighbor');
const em={valid_sat:true,valid_unsat:true,bad_header:false,bad_count:false,bad_var:false,unterminated:false,nonnumeric:false};
for(const [k,vv] of Object.entries(em))if(raw.controls.malformed[k]!==vv)throw Error('malformed '+k);
if(raw.controls.nonclone_structure.input_fixing_gate_isomorphism!==false)throw Error('nonclone');
const B=Math.max(...raw.templates.filter(t=>!t.name.includes('miter')&&(t.name.includes('commutativity')||t.name.includes('associativity'))).map(t=>t.resolution_lines));
const C=Math.max(...raw.templates.filter(t=>t.name.includes('congruence')).map(t=>t.resolution_lines));
if(B!==raw.constants.base_identity_res_max_B||C!==raw.constants.congruence_res_max_C)throw Error('constants');
console.log(JSON.stringify({status:'PASS',templates:raw.templates.length,resolution_lines:R,certificate_lines:L,B,C,sat_controls:2,malformed_controls:7}));
