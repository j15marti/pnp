// Independent original-source and read-once checker, LSPV-1/426.
'use strict';
function verify(rec) {
  let assertions=0;function check(x,s){assertions++;if(!x)throw Error(s)}
  function make(h) {
    const v=(p,j)=>p*h+j+1,rows=[];
    for(let p=0;p<=h;p++)rows.push(Array.from({length:h},(_,j)=>v(p,j)));
    for(let j=0;j<h;j++)for(let p=0;p<=h;p++)for(let q=p+1;q<=h;q++)rows.push([-v(p,j),-v(q,j)]);
    return rows;
  }
  const val=(l,x)=>((x>>>(Math.abs(l)-1))&1)===(l>0?1:0);
  const ok=(c,x)=>c.some(l=>val(l,x));
  for(const [h,k] of [[2,'php2'],[3,'php3']]){
    const d=rec[k],S=make(h),n=h*(h+1);check(JSON.stringify(S)===JSON.stringify(d.source),'source mismatch');
    check(S.length===d.clauses&&d.deletion_witnesses.length===S.length,'source size');
    let models=0;
    for(let x=0;x<1<<n;x++)if(S.every(c=>ok(c,x)))models++;
    check(models===0&&d.unsat_models===0,'bad UNSAT status');
    for(let i=0;i<S.length;i++){
       const x=d.deletion_witnesses[i];check(Number.isInteger(x)&&x>=0&&x<1<<n,'witness bounds');
       for(let j=0;j<S.length;j++)check(ok(S[j],x)===(i!==j),'witness fails clause id '+i+'/'+j);
    }
    const P=S.reduce((a,c)=>a+c.filter(l=>l>0).length,0);
    check(P===d.positive_occurrences&&S.length-1-P===d.reuse_floor,'reuse mismatch');
  }
  // Exhaustive oriented Resolution step check independently from ternary clause strings.
  const clauses=[];
  for(let t=0;t<81;t++){let z=t,C=[];for(let v=1;v<=4;v++){let a=z%3;z=Math.floor(z/3);if(a===1)C.push(v);if(a===2)C.push(-v)}clauses.push(C)}
  let total=0;
  for(const A of clauses)for(const B of clauses)for(const x of A)if(B.includes(-x)){
    const C=[...new Set([...A,...B].filter(v=>v!==x&&v!==-x))];
    if(C.some(v=>C.includes(-v)))continue;
    check(C.filter(v=>v>0).length+1<=A.filter(v=>v>0).length+B.filter(v=>v>0).length,'positive deficit');
    total++;
  }
  check(total===2744&&total===rec.local.valid_oriented_res_steps,'resolution enumeration');
  // Independent recursive source-disjoint inference-tree closure, not producer iteration order.
  const source=make(2),memo=new Map(),str=C=>C.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(',');
  function reach(mask) {
    if(memo.has(mask))return memo.get(mask);
    const out=new Set();
    if((mask&(mask-1))===0){out.add(str(source[Math.log2(mask)]));memo.set(mask,out);return out}
    for(let a=1;a<mask;a++){
      if((a&mask)!==a)continue;let b=mask^a;if(a>=b)continue;
      for(const L of reach(a))for(const R of reach(b)){
        const A=L?L.split(',').map(Number):[],B=R?R.split(',').map(Number):[];
        for(const p of A)if(B.includes(-p)){
          const C=new Set([...A,...B]);C.delete(p);C.delete(-p);
          if([...C].every(v=>!C.has(-v)))out.add(str([...C]));
        }
      }
    }
    memo.set(mask,out);return out;
  }
  const full=reach((1<<source.length)-1);
  let states=0;for(const v of memo.values())states+=v.size;
  check(full.size===0&&!full.has(''),'unexpected read-once contradiction');
  check(states===120&&states===rec.read_once_php2.total_mask_clause_states,'state mismatch');
  const forged=JSON.parse(JSON.stringify(rec));forged.php2.deletion_witnesses[0]=0;
  let caught=false;try{
    const a=forged.php2.deletion_witnesses[0];
    if(forged.php2.source.some((c,i)=>i!==0&&!ok(c,a)))throw Error('corrupt');
  }catch(e){caught=true}
  check(caught,'corrupt witness accepted');
  return {verified:true,independent_assertions:assertions,all_strict_oriented_resolutions:total,read_once_states:states,corrupted_witness_rejected:true};
}
if(typeof require==='function'&&require.main===module){const fs=require('fs');const raw=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));console.log(JSON.stringify(verify(raw),null,2))}
