'use strict';
// Reproducible fixed-canonical private-chain bit-PHP SAT/UNSAT source controls.
// Python/Node memory is NOT a logspace measurement; theorem is symbolic.
const crypto=require('crypto');
function generate(h,p) {
 if(h<2||(h&(h-1)))throw Error('bad holes');
 const ell=Math.log2(h), v=p*ell;
 let aux=v+1, rows=[];
 for(let i=0;i<p;i++)for(let j=i+1;j<p;j++)for(let a=0;a<h;a++) {
  let lits=[];
  for(const bird of [i,j])for(let b=0;b<ell;b++) {
   const q=bird*ell+b+1, sign=(a>>(ell-b-1))&1;
   lits.push(sign?-q:q);
  }
  if(lits.length<=3)rows.push(lits);
  else {
    let prev=aux++;rows.push([lits[0],lits[1],prev]);
    for(let k=2;k<lits.length-2;k++) {
      const next=aux++;rows.push([-prev,lits[k],next]);prev=next;
    }
    rows.push([-prev,lits.at(-2),lits.at(-1)]);
  }
 }
 const s='p cnf '+(aux-1)+' '+rows.length+'\n'+rows.map(x=>x.join(' ')+' 0\n').join('');
 return {holes:h,pigeons:p,vars:aux-1,clauses:rows.length,chars:s.length,
   sha256:crypto.createHash('sha256').update(s).digest('hex'),text:s};
}
function originalModels(h,p) {
 const ell=Math.log2(h),v=ell*p;
 if(v>14)return null;
 let cnt=0;
 for(let m=0;m<(1<<v);m++){
  const taken=new Set();
  for(let i=0;i<p;i++){
   let a=0;for(let b=0;b<ell;b++)a=(a<<1)|((m>>(i*ell+b))&1);
   taken.add(a);
  }
  if(taken.size===p)cnt++;
 }
 return cnt;
}
const cases=[];
for(const h of [2,4,8])for(const p of [h,h+1]){
 const r=generate(h,p),lab=p===h?'SAT':'UNSAT',models=originalModels(h,p);
 if(models!==null && ((models>0)!==(lab==='SAT')))throw Error('model check');
 cases.push({holes:h,pigeons:p,label:lab,vars:r.vars,clauses:r.clauses,
 chars:r.chars,sha256:r.sha256,models});
}
let local=0;
for(let bits=0;bits<16;bits++) {
 let a=Array.from({length:4},(_,i)=>!!(bits&(1<<i)));
 let lhs=a.some(Boolean),rhs=[false,true].some(z=>(a[0]||a[1]||z)&&(!z||a[2]||a[3]));
 if(lhs!==rhs)throw Error('chain unsound');local++;
}
console.log(JSON.stringify({status:'COMPUTATIONAL',cases,chain_checks:local},null,2));
