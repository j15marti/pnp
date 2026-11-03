#!/usr/bin/env node
// Independent replay checker for REFEREE308 JSON certificates.
'use strict';

const fs = require('fs');
const raw = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

function norm(xs) {
  const s = new Set(xs);
  for (const x of s) if (s.has(-x)) return null;
  return [...s].sort((x,y) => Math.abs(x)-Math.abs(y) || ((x<0)-(y<0)));
}
function key(c) { return JSON.stringify(c); }
function eq(a,b) { return key(a) === key(b); }
function xorSlots(q,a,b) {
  return [[a,b,-q],[a,-b,q],[-a,b,q],[-a,-b,-q]].map(norm);
}
function andSlots(q,a,b) {
  return [[-q,a],[-q,b],[q,-a,-b]].map(norm);
}
function parity3(a,b,c,bit) {
  const z=[];
  for (let va=0;va<2;va++) for(let vb=0;vb<2;vb++) for(let vc=0;vc<2;vc++) {
    if ((va^vb^vc)!==bit) z.push(norm([va?-a:a,vb?-b:b,vc?-c:c]));
  }
  return z;
}
function resolve(c1,c2,p) {
  if (!c1.includes(p) || !c2.includes(-p)) throw Error('bad pivot orientation');
  return norm(c1.filter(x=>x!==p).concat(c2.filter(x=>x!==-p)));
}
const [T,x,xp,y,a,b,c,u,v,p,q,r] = Array.from({length:12},(_,i)=>i+1);

function allowedSources(name) {
  let z=[];
  const add=(label,cs)=>{ for(const cl of cs) z.push(label+'|'+key(cl)); };
  if(name==='true_rail_four_gate') {
    const [t0,u0,d0,f0,e0]=[13,14,15,16,17];
    add('DEF_AND_d_tu',andSlots(d0,t0,u0));
    add('DEF_AND_f_dnt',andSlots(f0,d0,-t0));
    add('DEF_AND_e_fu',andSlots(e0,f0,u0));
    add('DEF_AND_T_nfne',andSlots(T,-f0,-e0));
  } else if(name==='xor_commutativity') {
    add('DEF_XOR_q_ab',xorSlots(q,a,b)); add('DEF_XOR_r_ba',xorSlots(r,b,a));
  } else if(name==='xor_associativity') {
    add('DEF_XOR_u_ab',xorSlots(u,a,b)); add('DEF_XOR_v_uc',xorSlots(v,u,c));
    add('DEF_XOR_p_bc',xorSlots(p,b,c)); add('DEF_XOR_q_ap',xorSlots(q,a,p));
  } else if(name==='xor_congruence_left') {
    add('ASSUME_x_iff_xp',[norm([-x,xp]),norm([x,-xp])]);
    add('DEF_XOR_q_xy',xorSlots(q,x,y)); add('DEF_XOR_r_xpy',xorSlots(r,xp,y));
  } else if(name==='and_copy_under_true_rail') {
    add('UNIT_T',[norm([T])]); add('DEF_AND_xp_Tx',andSlots(xp,T,x));
  } else if(name==='xor_copy_cancellation') {
    add('UNIT_T',[norm([T])]); add('DEF_AND_xp_Tx',andSlots(xp,T,x));
    add('DEF_XOR_q_xxp',xorSlots(q,x,xp));
  } else if(name.startsWith('xor_unit_')) {
    const va=+name.at(-2), vb=+name.at(-1);
    add('UNIT_a',[norm([va?a:-a])]); add('UNIT_b',[norm([vb?b:-b])]);
    add('DEF_XOR_q_ab',xorSlots(q,a,b));
  } else if(name.startsWith('parity3_to_xor_output_')) {
    const bit=+name.at(-1); add(`PARITY3_${bit}`,parity3(a,b,c,bit));
    add('DEF_XOR_u_ab',xorSlots(u,a,b)); add('DEF_XOR_q_uc',xorSlots(q,u,c));
  } else throw Error('unknown template '+name);
  return new Set(z);
}

let totalRes=0, totalLines=0;
for(const t of raw.templates) {
  const allowed=allowedSources(t.name);
  const lines=[];
  let res=0;
  for(let i=0;i<t.lines.length;i++) {
    const L=t.lines[i];
    const canonical=norm(L.clause);
    if(canonical===null || !eq(canonical,L.clause)) throw Error(`${t.name}: noncanonical ${i}`);
    if(L.kind==='RES') {
      if(!(L.left<i && L.right<i)) throw Error(`${t.name}: forward parent ${i}`);
      const got=resolve(lines[L.left],lines[L.right],L.pivot);
      if(got===null || !eq(got,L.clause)) throw Error(`${t.name}: bad resolvent ${i}`);
      res++;
    } else if(!allowed.has(L.kind+'|'+key(L.clause))) {
      throw Error(`${t.name}: unauthenticated source ${i} ${L.kind} ${key(L.clause)}`);
    }
    lines.push(L.clause);
  }
  for(const i of t.targets) if(!(i>=0 && i<lines.length)) throw Error(`${t.name}: bad target`);
  if(res!==t.resolution_lines) throw Error(`${t.name}: res count mismatch`);
  totalRes+=res; totalLines+=lines.length;
}
if(totalRes!==raw.template_totals.resolution_lines) throw Error('total RES mismatch');
if(totalLines!==raw.template_totals.retained_certificate_lines) throw Error('total line mismatch');

function evalClause(cl,bits) { return cl.some(x => (x>0)===Boolean(bits[Math.abs(x)])); }
function countModels(cnf,n) {
  let count=0;
  for(let mask=0;mask<(1<<n);mask++) {
    const bits={}; for(let i=1;i<=n;i++) bits[i]=(mask>>(i-1))&1;
    if(cnf.every(cl=>evalClause(cl,bits))) count++;
  }
  return count;
}
const odd=raw.both_label_k4.odd_unsat, even=raw.both_label_k4.even_sat;
if(countModels(odd.clauses,6)!==0 || odd.model_count!==0) throw Error('odd K4 label failed');
if(countModels(even.clauses,6)!==8 || even.model_count!==8) throw Error('even K4 label failed');
const expectedMalformed={valid_sat:true,valid_unsat:true,bad_header:false,bad_clause_count:false,
  bad_variable:false,missing_terminator:false,nonnumeric:false};
for(const [k,v] of Object.entries(expectedMalformed)) {
  if(raw.malformed_controls[k]!==v) throw Error('malformed control mismatch: '+k);
}
if(Object.keys(raw.malformed_controls).length!==Object.keys(expectedMalformed).length)
  throw Error('unexpected malformed control');

console.log(JSON.stringify({status:'PASS',templates:raw.templates.length,
  resolution_lines:totalRes,certificate_lines:totalLines,odd_models:0,even_models:8,
  malformed_controls:Object.keys(expectedMalformed).length}));
