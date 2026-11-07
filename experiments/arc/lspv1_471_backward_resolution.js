'use strict';
// LSPV-1/471 source-indexed Resolution certificates; independently executable Node script.
const assert=(b,m)=>{if(!b)throw Error(m||'assert')};
const key=C=>[...new Set(C)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
let checks=0,certs=0,covered=0,uncovered=0,better=0,maxgap=0;
function ck(b,msg){checks++;assert(b,msg)}
function source(k,sets){
 const r=sets.length,a=1,s=j=>2+j,g=i=>2+r+i;
 const src=[{id:'A',clause:[a]}];
 for(let j=0;j<r;j++)src.push({id:'S'+j,clause:key([-a,s(j)])});
 for(let j=0;j<r;j++)for(let i=0;i<k;i++)if(sets[j].includes(i))src.push({id:'M'+j+'_'+i,clause:key([-s(j),g(i)])});
 src.push({id:'Z',clause:key(Array.from({length:k},(_,i)=>-g(i)))});
 return {src,a,s,g,k,r,sets};
}
function resolve(A,B,p){
 assert((A.includes(p)&&B.includes(-p))||(A.includes(-p)&&B.includes(p)),'pivot');
 const C=key([...A.filter(x=>Math.abs(x)!==p),...B.filter(x=>Math.abs(x)!==p)]);
 assert(!C.some(x=>C.includes(-x)),'tautology');return C;
}
function verify(F,steps){
 const tab=new Map(F.src.map(x=>[x.id,x.clause]));
 for(const st of steps){
  assert(!tab.has(st.id)&&st.parents.length===2,'duplicate id or arity');
  const [A,B]=st.parents.map(id=>{assert(tab.has(id),'bad/forward ref');return tab.get(id)});
  const C=resolve(A,B,st.pivot);assert(equal(C,st.clause),'wrong conclusion');
  tab.set(st.id,C);checks++;
 }
 assert(steps.length&&tab.get(steps.at(-1).id).length===0,'not empty');
 certs++;return true;
}
function mincover(k,sets){
 let best=null,full=(1<<k)-1;
 for(let mask=1;mask<(1<<sets.length);mask++){
  let cov=0,J=[];
  for(let j=0;j<sets.length;j++)if((mask>>j)&1){J.push(j);for(let i of sets[j])cov|=1<<i}
  if(cov===full&&(!best||J.length<best.length))best=J;
 }
 return best;
}
function build(F,J,backward){
 let n=0,steps=[],tab=new Map(F.src.map(x=>[x.id,x.clause]));
 function add(p1,p2,p){
  const id='R'+(n++),C=resolve(tab.get(p1),tab.get(p2),p);
  steps.push({id,parents:[p1,p2],pivot:p,clause:C});tab.set(id,C);return id;
 }
 const chosen=Array.from({length:F.k},(_,i)=>J.find(j=>F.sets[j].includes(i)));
 assert(chosen.every(x=>x!==undefined),'uncovered');
 if(backward){
  let cur='Z';
  for(let i=0;i<F.k;i++)cur=add(cur,'M'+chosen[i]+'_'+i,F.g(i));
  for(let j of J)cur=add(cur,'S'+j,F.s(j));
  add(cur,'A',F.a);
 }else{
  const units=new Map(J.map(j=>[j,add('A','S'+j,F.a)]));
  const goals=chosen.map((j,i)=>add(units.get(j),'M'+j+'_'+i,F.s(j)));
  let cur='Z';for(let i=0;i<F.k;i++)cur=add(cur,goals[i],F.g(i));
 }
 verify(F,steps);return steps;
}
function sat(F,omit=-1){
 const n=1+F.r+F.k;
 for(let bits=0;bits<(1<<n);bits++){
  if(F.src.every((c,index)=>index===omit||c.clause.some(l=>(((bits>>(Math.abs(l)-1))&1)===1)===(l>0))))return bits;
 }
 return null;
}
for(let k=1;k<=4;k++)for(let r=1;r<=4;r++)for(let mask=0;mask<(1<<(k*r));mask++){
 const sets=Array.from({length:r},(_,j)=>Array.from({length:k},(_,i)=>i).filter(i=>(mask>>(j*k+i))&1));
 const F=source(k,sets),J=mincover(k,sets);
 if(!J){uncovered++;if(uncovered<=80)ck(sat(F)!==null,'uncovered SAT');continue}
 covered++;const back=build(F,J,true),layer=build(F,J,false);
 ck(back.length===k+J.length+1,'back work');ck(layer.length===2*k+J.length,'layer work');
 if(back.length<layer.length){better++;maxgap=Math.max(maxgap,layer.length-back.length)}
 if(covered<=80)ck(sat(F)===null,'covered UNSAT');
}
let singleton=[];
for(let k=1;k<=10;k++){
 const F=source(k,[Array.from({length:k},(_,i)=>i)]);
 const b=build(F,[0],true),l=build(F,[0],false);
 ck(b.length===k+2&&l.length===2*k+1,'singleton work');
 ck(F.src.length===k+3,'source count');
 if(k<=8){ck(sat(F)===null,'singleton UNSAT');for(let i=0;i<F.src.length;i++)ck(sat(F,i)!==null,'essential '+i)}
 singleton.push({k,source_clauses:F.src.length,backward_paid:b.length,layered_paid:l.length,
 backward_certificate_bytes:Buffer.byteLength(JSON.stringify(b)),layered_certificate_bytes:Buffer.byteLength(JSON.stringify(l))});
}
const F=source(3,[[0,1,2]]),good=build(F,[0],true);
const clones=()=>JSON.parse(JSON.stringify(good)),corrupt=[];
{let c=clones();c[0].pivot=99;corrupt.push(c)}
{let c=clones();c[1].parents[0]='MISSING';corrupt.push(c)}
{let c=clones();c[0].clause=[1];corrupt.push(c)}
{let c=clones();c[0].parents[0]=c.at(-1).id;corrupt.push(c)}
{let c=clones();c.at(-1).clause=[2];corrupt.push(c)}
{let c=clones();c[0].id='Z';corrupt.push(c)}
let rejected=0;for(let c of corrupt){try{verify(F,c)}catch(e){rejected++}}
ck(rejected===corrupt.length,'corruptions');
const result={classification:'PROVED/RESTRICTED symbolic; COMPUTATIONAL tests',source:'LSPV-1/470 original general CNF',
formula:'W_backward <= k+tau+1, W_layer=2k+tau; singleton W_full_binary=k+2 exact',
covered,uncovered,better,maxgap,certificates_verified:certs,checks,corruptions_rejected:rejected,
singleton,native_historical_checker:false};
console.log(JSON.stringify(result));