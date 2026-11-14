'use strict';
// Independent TMR-1/010 audit of TMR5-TR7 expanded to all literal-field bits.
const assert=(c,s)=>{if(!c)throw Error(s)};
const pop=x=>{let k=0;while(x){k+=x&1;x>>=1}return k};
const rho=i=>2*i+(pop(i)&1);
const flip=(s,p)=>s.slice(0,p)+(s[p]==='0'?'1':'0')+s.slice(p+1);
function make(r){
 const t=3*r,w=Math.ceil(Math.log2(2*t+2)),N=(1<<w)-1;
 const core=Array.from({length:t},(_,i)=>rho(i+1)),seen=new Set(core),spare=[];
 for(let i=1;i<=N;i++)if(!seen.has(i))spare.push(i);
 const clauses=[],positions=[];
 for(let g=0;g<r;g++)for(let m of [1,2,3,4,5,6,7,7])clauses.push([0,1,2].map(j=>[core[3*g+j],(m>>j)&1]));
 for(let i=0;i<spare.length;i+=3){const a=spare.slice(i,i+3);for(const v of spare){if(a.length===3)break;if(!a.includes(v))a.push(v)}assert(a.length===3,'filler');clauses.push(a.map(v=>[v,0]));}
 const M=clauses.length,header='1'.repeat(N)+'0'+'1'.repeat(M)+'0';let s=header;
 for(let c=0;c<M;c++)for(let j=0;j<3;j++){
  const [id,sign]=clauses[c][j];positions.push({offset:s.length,kind:'sign',c,j});s+=sign;
  const bin=id.toString(2).padStart(w,'0');for(let b=0;b<w;b++)positions.push({offset:s.length+b,kind:'id',c,j,b});s+=bin;
 }
 return {r,t,w,N,M,header,s,clauses,positions,core,spare};
}
function parse(s,d){
 if(s.length!==d.s.length || !s.startsWith(d.header))return null;
 let p=d.header.length,occ=new Uint16Array(d.N+1),clauses=[];
 for(let c=0;c<d.M;c++){
  const row=[];
  for(let j=0;j<3;j++){
   const sign=+s[p++],id=parseInt(s.slice(p,p+d.w),2);p+=d.w;
   if(id===0||id>d.N||row.some(v=>v[0]===id))return null;
   row.push([id,sign]);occ[id]++;
  }
  clauses.push(row);
 }
 for(let i=1;i<=d.N;i++)if(!occ[i])return null;
 return clauses;
}
function holds(clauses,assign){return clauses.every(row=>row.some(([v,neg])=>(assign[v]^neg)===1));}
// Exhaustive test of all core variables; only filler IDs in edited core clauses
// can need to be zero. This is independent of the symbolic proof case split.
function findWitness(rows,d){
 const spareSet=new Set(d.spare),affected=new Set();
 for(let c=0;c<8*d.r;c++)for(const [id] of rows[c])if(spareSet.has(id))affected.add(id);
 const targets=[...affected];assert(targets.length<=2,'at most two core ID targets');
 const arr=new Uint8Array(d.N+1);for(let id of d.spare)arr[id]=1;
 for(let a=0;a<(1<<d.t);a++){
  for(let i=0;i<d.t;i++)arr[d.core[i]]=(a>>i)&1;
  for(let b=0;b<(1<<targets.length);b++){
   for(let j=0;j<targets.length;j++)arr[targets[j]]=(b>>j)&1;
   if(holds(rows,arr))return {a,b};
  }
 }
 return null;
}
function run(){
 let cases=[],total={pairs:0,valid:0,invalid:0,sat:0,unsat3:0,classes:{}};
 for(let r of [1,2,3]){
  const d=make(r),p=d.positions;assert(parse(d.s,d),'source invalid');
  let valid=0,invalid=0,sat=0,pairs=0,unsat3=0;
  const enumerated=(r<=2);
  let pairIndices=[];
  if(enumerated){for(let i=0;i<p.length;i++)for(let j=i+1;j<p.length;j++)pairIndices.push([i,j]);}
  else {
   for(let i=0;i<p.length;i+=7)for(let j=i+1;j<p.length;j+=13)pairIndices.push([i,j]);
  }
  for(const [i,j] of pairIndices){
   let s=flip(flip(d.s,p[i].offset),p[j].offset),rows=parse(s,d);pairs++;
   const kind=[p[i].kind,p[j].kind].sort().join('+');
   if(!rows){invalid++;continue;}
   valid++;const witness=findWitness(rows,d);
   assert(witness!==null,'Unexpected UNSAT r='+r+' positions '+p[i].offset+','+p[j].offset+' '+kind);
   sat++;total.classes[kind]=(total.classes[kind]||0)+1;
  }
  for(let g=0;g<r;g++){
   let x=d.s;const clause=8*g+7;
   for(const field of d.positions.filter(v=>v.c===clause&&v.kind==='sign'))x=flip(x,field.offset);
   const rows=parse(x,d);assert(rows,'triple must parse');
   assert(findWitness(rows,d)===null,'triple should be UNSAT');unsat3++;
  }
  cases.push({r,L:d.s.length,N:d.N,M:d.M,allPairs:enumerated,fields:p.length,pairs,valid,invalid,sat,unsat3});
  total.pairs+=pairs;total.valid+=valid;total.invalid+=invalid;total.sat+=sat;total.unsat3+=unsat3;
 }
 return {tag:'TMR1-LITERAL-FIELD-RADIUS010',date:'2026-11-13 PST',status:'COMPUTATIONAL',scope:'valid same-length strict proper 3-CNF two literal-field bit flips, including signs and IDs',cases,total,failures:0};
}
console.log(JSON.stringify(run(),null,2));
