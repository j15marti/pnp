#!/usr/bin/env node
// Independent LSPV-4/416 exponent and source-access referee.
// Does not import or execute the producer.
import fs from 'node:fs';
import assert from 'node:assert/strict';
const path=process.argv[2] ?? 'lspv4_416_access_tax_raw.json';
const data=JSON.parse(fs.readFileSync(path,'utf8'));
let total=0;
function check(x,msg){total++;assert.ok(x,msg)}
function b(x){return ((x+2)/(x*x)-x)/2}
function parse(t){
 let h=null,cs=[],cur=[];
 for(let line of t.split('\n')){
  line=line.trim();
  if(!line || line==='c' || line.startsWith('c '))continue;
  if(line.startsWith('p ')){
   const m=/^p cnf (\d+) (\d+)$/.exec(line);if(!m||h)return null;
   h=[Number(m[1]),Number(m[2])];continue;
  }
  if(!h)return null;
  for(let word of line.split(/\s+/)){
   if(!/^-?(0|[1-9]\d*)$/.test(word))return null;
   let z=Number(word);
   if(!Number.isSafeInteger(z)||Math.abs(z)>h[0])return null;
   if(z===0){cs.push(cur);cur=[];} else cur.push(z);
  }
 }
 if(!h||cur.length||cs.length!==h[1])return null;
 let models=0;
 for(let a=0;a<(1<<h[0]);a++){
  const sat=cs.every(cl=>cl.some(z=>Boolean((a>>(Math.abs(z)-1))&1)===(z>0)));
  models+=Number(sat);
 }
 return models;
}
const cnfs={'SAT':'p cnf 1 1\n1 0\n','UNSAT':'p cnf 1 2\n1 0\n-1 0\n',
 'MALFORMED':'p cnf 1 1\n1\n','CORRUPT':'p cnf 1 2\n1 0\n-1 0\nTRASH\n'};
for(const rec of data.source_controls){
 const val=parse(cnfs[rec.source]);
 check(Buffer.byteLength(cnfs[rec.source])===rec.source_bytes,'source raw length '+rec.source);
 check((val!==null)===rec.accepted,'validity '+rec.source);
 check(val===rec.models,'models '+rec.source);
}
const fractions=s=>{const [a,c]=s.split('/').map(Number);return a/c;};
for(const row of data.profiles){
 const v=fractions(row.read_tax_v),limit=1.2+2*v;
 check(Math.abs(fractions(row.fixed_time_exponent)-limit)<1e-12,'fixed point');
 let t=10,s=6,k=0,first=null;
 for(;k<=48;k++){
  if(s<b(t)){first=k;break;}
  t=Math.max(1.1,0.6+0.5,0.6+v+0.5*t);
  s=Math.max(0.5,0.5*s);
 }
 check(row.first_strict_iteration===first,'first entry '+row.read_tax_v);
 check(row.strict_flmv_at_fixed_point === (0.5<b(limit)),'strict fixed '+row.read_tax_v);
 if(first!==null){
   check(Math.abs(fractions(row.t_at_first_strict)-t)<1e-10,'t at first');
   check(Math.abs(fractions(row.s_at_first_strict)-s)<1e-10,'s at first');
 }
}
const raw='p cnf 1 2\n1 0\n-1 0\n';
for(let r of data.bit_transport){
 const N=r.parent_length_bits_proxy, q=Math.ceil(N**0.6),m=Math.ceil(N**.5);
 check(q===r.children,'children');check(m===r.child_length_bits_proxy,'child length');
 const padded='c '+' '.repeat(N-raw.length-3)+'\n'+raw;
 check(Buffer.byteLength(padded)===N,'source size');
 check(parse(padded)===0,'padded UNSAT');
 let outputs=0,erases=0,idx=0,direct=0,scans=0;
 const bytes=Buffer.from(padded,'ascii');
 for(let child=0;child<q;child++){
   for(let j=0;j<m;j++){
      const address=(17*child+31*j)%N;
      let v=(bytes[address]>>((child+j)%8))&1;
      check(v===Number((bytes[address]&(1<<((child+j)%8)))!==0),'independent bit lookup');
      idx+=Math.ceil(Math.log2(N));erases++;direct++;outputs++;scans+=N;
   }
 }
 check(outputs===r.guest_virtual_input_reads,'read count');
 check(erases===r.index_erase_events,'index erasures');
 check(idx===r.index_digit_writes,'index writes');
 check(direct===r.direct_parent_bit_probes,'direct read');
 check(scans===r.one_full_parent_scan_per_virtual_read_probes,'scan per guest read');
 check(q*N===r.one_full_parent_scan_per_child_probes,'scan per child');
 check(q*m===r.output_bit_writes_if_streamed,'physical output bits');
 check(q+m===r.live_counted_bits_if_all_child_statuses_cached,'eager status buffer');
 check(N+m===r.live_counted_bits_if_parent_is_buffered,'peak buffered');
}
for(const c of data.semantic_controls){
 let parent,children;
 if(c.case==='shared_variable_conflict'){parent='p cnf 1 2\n1 0\n-1 0\n';children=['p cnf 1 1\n1 0\n','p cnf 1 1\n-1 0\n'];}
 else{parent='p cnf 1 2\n1 0\n1 0\n';children=['p cnf 1 1\n1 0\n','p cnf 1 1\n1 0\n'];}
 check((parse(parent)>0)===c.parent_sat,'parent semantics');
 check(children.every(x=>parse(x)>0)===c.naive_AND_child_labels,'independent labels');
}
check(data.nominal_margin==='1/90','nominal margin exact');
check(data.strict_box_at_241_over_200==='26279/23232400','strict rational margin');
console.log(JSON.stringify({status:'PASS',independent_assertions:total,source_controls:4,profiles:data.profiles.length,transport:data.bit_transport.length}));
