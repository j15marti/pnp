"use strict";
const fs=require('fs');
function verifyIndependent(record){
 let checks=0,increment=(b,why)=>{if(!b)throw Error("independent: "+why);checks++},nS=0,nN=0;
 for(const s of record.sources){
  const n=s.n,clauses=s.original_clauses;let models=[];
  function lv(l,a){const x=(a>>(Math.abs(l)-1))&1;return l>0?x===1:x===0}
  function satisfied(C,a){return C.every(c=>c.some(l=>lv(l,a)))}
  function ct(c,a){return c.filter(l=>lv(l,a)).length}
  for(let a=0;a<(1<<n);a++){if(satisfied(clauses,a))models.push(a);for(let c of clauses)increment(ct(c,a)+ct(c,((1<<n)-1)^a)===c.length,"complement");}
  increment(JSON.stringify(models)===JSON.stringify(s.witnesses),"models");increment(s.sat===(models.length>0),"label");
  if(s.sat)nS++;else nN++;
  for(const t of s.targets){const c=clauses[t.source_clause-1];increment(t.occurrences.length===c.length,"occ size");for(let k=0;k<c.length;k++){const lit=c[k],o=t.occurrences[k],v=Math.abs(lit),sv=lit>0?1:0;increment(o.literal===lit && o.S_target===sv && o.S_inverted_U===1-sv && o.U_target===1-sv && o.U_inverted_S===sv,"occ");increment(t.S_target[v]===sv && t.U_target[v]===1-sv,"targets");}}
  for(const x of s.pair_compatibility){const [j,k]=x.source_clauses;let a=clauses[j-1],b=clauses[k-1];for(const m of ["SS","SU","US","UU"]){let realized=false;for(let z=0;z<(1<<n);z++){let ra=ct(a,z),rb=ct(b,z);if((m[0]==="S"?ra===a.length:ra===0)&&(m[1]==="S"?rb===b.length:rb===0))realized=true}increment(realized===x.modes[m],"pair");}}
  for(const b of s.source_resolution_blockers){let [j,k]=b.source_clauses,x=b.pivot;increment(clauses[j-1].includes(x)&&clauses[k-1].includes(-x),"pivot");for(let a of models){const extend=Object.entries(b.forbidden_cube).every(([key,val])=>((a>>(Number(key)-1))&1)===val);increment(!extend,"blocker")}}
  for(const t of s.flip_trail){let a=0;for(let i=0;i<t.flipped_prefix;i++)a|=1<<i;const v=clauses.map(c=>ct(c,a));increment(v.join(",")===t.true_literal_counts.join(","),"trail");increment(v.filter(x=>x===0).length===t.N0,"trail0");}
  let branchSat=false;
  for(const c of s.children){const v=c.value;const ch=clauses.filter(cl=>!cl.includes(v?1:-1)).map(cl=>cl.filter(l=>l!==(v?-1:1)));increment(JSON.stringify(ch)===JSON.stringify(c.clauses),"cofactor");let models2=0;for(let a=0;a<(1<<n);a++)if(satisfied(ch,a))models2++;increment((models2>0)===c.sat,"child SAT");increment(c.ordinary_child_dimacs.startsWith(`p cnf ${n} ${ch.length}\n`),"physical child");branchSat=branchSat||c.sat;
   const lg=c.tape_log;let get=(what)=>lg.find(o=>o.what===what);
   increment(get("fresh work[4]").bit===0,"fresh work");
   increment(get("jump work via indexed bit2").address===4,"indexed jump");
   increment(get("erased index bit2").bit===0,"index erasure");
   increment(get("work[4] after write").bit===1,"work write");
   increment(get("index head preserved").position===2,"head retained");
   increment(get("return work to bit2").address===4 && get("work[4] survives index erasure").bit===1,"same-run work");
   increment(get("far input blank").address===16,"far input addr");
   increment(get("input index bit4 erased").bit===0,"input idx erased");
   increment(get("input at one").symbol===c.ordinary_child_dimacs[1],"read exact child");
   increment(get("fresh work[8] blank").bit===0,"fresh work at eight");
  }
  increment(branchSat===s.sat,"OR join");
 }
 increment(nS===record.counters.sat && nN===record.counters.unsat,"source counts");
 increment(record.falsifiers.untagged_reuse_exposes_stale_work_cell,"stale");
 increment(record.falsifiers.modulo_four_epoch_wrap_resurrects_stale_cell,"wrap");
 return {passed:true,checks,sources:record.sources.length,source_sat:nS,source_unsat:nN}
}
const raw=JSON.parse(fs.readFileSync(process.argv[2]||'arc_unknown_exponent_epoch274_raw.json','utf8'));
const result=verifyIndependent(raw);
process.stdout.write(JSON.stringify(result,null,2)+'\n');
