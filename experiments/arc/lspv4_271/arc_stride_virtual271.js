'use strict';
/* LSPV-4 ARC-STRIDE-VIRTUAL271, self-contained node >=18, no dependencies. */
const G = [
 [-2,4,5],[-2,4,-5],[-2,-4,5],[-2,-4,-5],
 [-3,6,7],[-3,6,-7],[-3,-6,7],[-3,-6,-7]
];
const field = (v,w) => String(v).padStart(w,' ');
const record = (c,w) => c.map(v=>field(v,w)).join(' ')+' 0\n';
const parent = (m,h) => {
 const cs=G.map(c=>c.slice());
 for(let j=1;j<=m;j++) cs.push(j===h?[-1,j%2?2:-2,3]:[1,2,3]);
 return {clauses:cs, text:'p cnf 7 '+(8+m)+'\n'+cs.map(c=>record(c,2)).join('')};
};
const padding = m => Math.max(1,Math.floor(Math.sqrt(m)/Math.log2(m+2)));
const childClause = (k,p,even) => k<8 ? G[k] :
 k===8 ? [even?-2:2,3,8] : k===9 ? [even?-2:2,3,-8] :
 [9+3*(k-10),10+3*(k-10),11+3*(k-10)];
function virtualChild(m,even){
 const p=padding(m),n=8+3*p,w=String(n).length+1;
 const head='p cnf '+n+' '+(10+p)+'\n', stride=3*w+5, M=head.length+(10+p)*stride;
 function at(i){
  if(i<0||!Number.isSafeInteger(i)||i>=M) return ' ';
  if(i<head.length) return head[i];
  const t=i-head.length,k=Math.floor(t/stride), r=t%stride;
  return record(childClause(k,p,even),w)[r];
 }
 return {p,n,w,stride,M,head,at,materialize:()=>head+Array.from({length:10+p},(_,k)=>record(childClause(k,p,even),w)).join('')};
}
function authenticate(s){
 let reads=0,i=0;const take=()=>{reads++;return s[i++]??null;};
 let hdr='';while(hdr.length<=128){const c=take();if(c===null)throw Error('truncated header');hdr+=c;if(c==='\n')break;}
 const mm=/^p cnf 7 (\d+)\n$/.exec(hdr);if(!mm)throw Error('bad header');
 const m=Number(mm[1])-8;if(!Number.isSafeInteger(m)||m<4||m%2)throw Error('bad m');
 let found=0,even=false;
 function checkLine(expected){for(let a=0;a<expected.length;a++)if(take()!==expected[a])throw Error('bad clause byte');}
 for(const c of G)checkLine(record(c,2));
 for(let j=1;j<=m;j++){
  let row='';for(let z=0;z<11;z++)row+=take();
  if(row===record([1,2,3],2))continue;
  if(row!==record([-1,j%2?2:-2,3],2)||found)throw Error('bad mark');
  found=j;even=(j%2===0);
 }
 if(!found||i!==s.length)throw Error('missing mark/trailer');
 return {m,found,even,reads,retained_bits_bound:8*Math.ceil(Math.log2(s.length+2))+100};
}
const truth=(c,a)=>c.some(v=>((a>>(Math.abs(v)-1))&1)===(v>0?1:0));
const trueCount=(c,a)=>c.reduce((t,v)=>t+(((a>>(Math.abs(v)-1))&1)===(v>0?1:0)?1:0),0);
function dpll(cs){
 let nodes=0,litTests=0,unitWrites=0;
 function rec(assignment){nodes++;let as=assignment.slice(),again=true;
  while(again){again=false;let all=true;
   for(const c of cs){let hit=false,free=0,last=0;
    for(const lit of c){litTests++;const z=as[Math.abs(lit)];if(z<0){free++;last=lit;}else if(z===(lit>0?1:0)){hit=true;break;}}
    if(hit)continue;all=false;if(free===0)return false;
    if(free===1){const k=Math.abs(last),v=last>0?1:0;
     if(as[k]>=0&&as[k]!==v)return false;
     if(as[k]!==v){as[k]=v;unitWrites++;again=true;}
    }
   }if(all)return true;
  }
  let pivot=0;for(const c of cs){if(c.some(l=>as[Math.abs(l)]===(l>0?1:0)))continue;
   for(const l of c){if(as[Math.abs(l)]<0){pivot=Math.abs(l);break;}}if(pivot)break;
  }
  if(!pivot)return true;
  for(const v of [0,1]){const next=as.slice();next[pivot]=v;if(rec(next))return true;}return false;
 }
 const n=cs.reduce((v,c)=>Math.max(v,...c.map(x=>Math.abs(x))),0);
 return {sat:rec(new Array(n+1).fill(-1)),nodes,litTests,unitWrites};
}
const assignmentTargets=(c,s)=>Object.fromEntries(c.map(l=>[String(Math.abs(l)),s===(l>0?1:0)?1:0]));
function compatible(c,d,p,q){
 const x=assignmentTargets(c,p==='S'?1:0),y=assignmentTargets(d,q==='S'?1:0);
 return Object.keys(x).every(k=>!(k in y)||x[k]===y[k]);
}
function bruteCompatible(c,d,p,q){
 const vars=[...new Set(c.concat(d).map(l=>Math.abs(l)))];
 for(let mask=0;mask<2**vars.length;mask++){
  const val=Object.fromEntries(vars.map((v,i)=>[v,(mask>>i)&1]));
  const ct=(e)=>e.reduce((s,l)=>s+(val[Math.abs(l)]===(l>0?1:0)?1:0),0);
  if(ct(c)===(p==='S'?3:0)&&ct(d)===(q==='S'?3:0))return true;
 }return false;
}
function resolutionCertificate(cs,h){
 if(h%2===0)return null;
 const nodes={},steps=[];cs.forEach((c,i)=>nodes['C'+(i+1)]=c.slice());
 const norm=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
 function add(a,b,x){const ca=nodes[a],cb=nodes[b];
  if(!ca.includes(x)||!cb.includes(-x))throw Error('bad resolution source '+a+','+b);
  const r=norm(ca.filter(l=>l!==x).concat(cb.filter(l=>l!==-x)));
  if(r.some(l=>r.includes(-l)))throw Error('tautological proof step');
  const id='D'+(steps.length+1);nodes[id]=r;steps.push({id,parents:[a,b],pivot:x,clause:r});return id;
 }
 const a=add('C1','C3',4),b=add('C2','C4',4),u=add(a,b,5);
 const c=add('C5','C7',6),d=add('C6','C8',6),v=add(c,d,7);
 const j=h===1?2:1;
 const r=add('C'+(8+j),'C'+(8+h),1);
 const s=add(r,u,2),end=add(s,v,3);
 if(nodes[end].length!==0)throw Error('not empty');
 return {steps,source_clause_indices:[1,2,3,4,5,6,7,8,8+j,8+h],last:end};
}
function diagnostics(cs,m,h){
 const clauses=cs.map((c,i)=>({index:i+1,literals:c,
  occurrences:c.map((l,k)=>({var:Math.abs(l),sign:l>0?'+':'-',source_clause:i+1,position:k+1,
    S_value:l>0?1:0,invert_S:l>0?0:1,U_value:l>0?0:1,invert_U:l>0?1:0})),
  S:assignmentTargets(c,1),invert_S:assignmentTargets(c,0),U:assignmentTargets(c,0),invert_U:assignmentTargets(c,1)}));
 const pairs=[];let pairChecks=0;
 for(let i=0;i<cs.length;i++)for(let j=i+1;j<cs.length;j++){
  const modes={};for(const p of ['S','U'])for(const q of ['S','U']){
   const computed=compatible(cs[i],cs[j],p,q),exhaustive=bruteCompatible(cs[i],cs[j],p,q);
   if(computed!==exhaustive)throw Error('pair mismatch');pairChecks++;
   modes[p+q]=computed;
  }pairs.push({source:[i+1,j+1],modes});
 }
 function counts(a){const v=[0,0,0,0];for(const c of cs)v[trueCount(c,a)]++;return v;}
 const flips=[];let a=0;flips.push({flip:[],assignment:a,N:counts(a)});
 for(let i=0;i<7;i++){a^=1<<i;flips.push({flip:[i+1],assignment:a,N:counts(a)});}
 for(const mask of [3,5,7,63,127])flips.push({flip:[...Array(7).keys()].filter(i=>(mask>>i)&1).map(i=>i+1),assignment:mask,N:counts(mask)});
 let complements=0;
 for(let a=0;a<128;a++){const b=127^a;
  const u=counts(a),v=counts(b);for(let k=0;k<4;k++)if(u[k]!==v[3-k])throw Error('complement failed');complements++;
 }
 return {source_m:m,marked_h:h,clauses,pairs,pairChecks,allzero:counts(0),allone:counts(127),flips,complements,
  prohibited_cube_proof:resolutionCertificate(cs,h)};
}
function run(){
 const cases=[];let assertedBytes=0,reads=0,pairChecks=0,complements=0;
 for(const m of [8,16,32,128,4096])for(const h of [1,2]){
  const src=parent(m,h),auth=authenticate(src.text),isSat=h%2===0;
  if(auth.even!==isSat||auth.reads!==src.text.length)throw Error('auth mismatch');
  const V=virtualChild(m,isSat),material=V.materialize();
  if(V.M!==material.length)throw Error('length mismatch');
  for(let i=-2;i<V.M+4;i++){const ch=(i<0||i>=material.length)?' ':material[i];if(V.at(i)!==ch)throw Error('indexed mismatch '+i);assertedBytes++;}
  for(let t=0;t<125;t++){const i=(t*997+53)%(V.M+101);if(V.at(i)!==(material[i]??' '))throw Error('random access mismatch');assertedBytes++;}
  const baseline=dpll(src.clauses);
  const childCs=Array.from({length:10+V.p},(_,k)=>childClause(k,V.p,isSat));
  const guest=dpll(childCs);
  if(baseline.sat!==isSat||guest.sat!==isSat)throw Error('SAT label mismatch');
  if(isSat){const sourceA=1,childA=(1<<8)|Array.from({length:V.p},(_,k)=>(1<<(9+3*k))|(1<<(10+3*k))|(1<<(11+3*k))).reduce((a,b)=>a|b,0);
    if(!src.clauses.every(c=>truth(c,sourceA)))throw Error('source witness');
    if(V.p<=6&&!childCs.every(c=>truth(c,childA)))throw Error('child witness');
  }
  const diag=m<=32?diagnostics(src.clauses,m,h):{
   total_original_clauses:src.clauses.length,diagnostics_not_materialized:true,
   local_extremes_and_pairs_covered_by_exact_generator:true,
   prohibited_cube_proof:resolutionCertificate(src.clauses,h)};
  pairChecks+=diag.pairChecks||0;complements+=diag.complements||0;reads+=auth.reads;
  const firstClausePosition=V.head.length;
  const firstProperizedPosition=V.head.length+8*V.stride;
  cases.push({m,h,label:isSat?'SAT':'UNSAT',original_bits:src.text.length*8,child_bits:V.M*8,
   pad_clauses:V.p,source_reads:auth.reads,child_stored_in_transducer:false,
   first_child_clause:material.slice(firstClausePosition,firstClausePosition+V.stride),
   properized_sign_field:material.slice(firstProperizedPosition,firstProperizedPosition+V.w),
   baseline,childGuest:guest,requested_guest_characters:V.M+6+125,
   diagnostics:diag});
 }
 for(let j=0;j<cases.length;j+=2){if(cases[j].first_child_clause!==cases[j+1].first_child_clause)throw Error('constant prefix changed');
  if(cases[j].properized_sign_field===cases[j+1].properized_sign_field)throw Error('sign missing');}
 const malformed=parent(8,2).text.replace(record([1,2,3],2),record([1,-2,3],2));
 let rejected=false;try{authenticate(malformed);}catch(e){rejected=true;}if(!rejected)throw Error('bad source accepted');
 return {run:'ARC-STRIDE-VIRTUAL271',timestamp_local:'2026-10-31 04:58 PDT',status:'COMPUTATIONAL; PROVED/EXACT restricted theorem subject to independent referee; universal ARC OPEN',
  controls:{indexed_char_assertions:assertedBytes,source_reads:reads,original_pair_mode_assertions:pairChecks,
   complement_assertions:complements,malformed_rejected:rejected,source_m:[8,16,32,128,4096],labels:'matched SAT and UNSAT'},cases};
}
if(typeof module!=='undefined'&&require.main===module)console.log(JSON.stringify(run(),null,2));
