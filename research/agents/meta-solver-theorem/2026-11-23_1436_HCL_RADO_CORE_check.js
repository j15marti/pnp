"use strict";
const main = function main(){
  const assert=(x,m="assertion")=>{if(!x)throw Error(m)};
  const bit=i=>1n<<BigInt(i);
  function parity(x){let p=0;while(x){p^=1;x&=x-1n}return p}
  function rank(rows){let B=new Map();for(let v of rows){while(v){let k=v.toString(2).length-1;if(B.has(k))v^=B.get(k);else{B.set(k,v);break}}}return B.size}
  function reduce(v,B){while(v){let k=v.toString(2).length-1;if(!B.has(k))break;v^=B.get(k)}return v}
  function solve(rows,bs,d){let B=new Map();for(let j=0;j<rows.length;j++){let v=rows[j],b=bs[j];while(v){let k=v.toString(2).length-1;if(!B.has(k)){B.set(k,[v,b]);break}let [w,c]=B.get(k);v^=w;b^=c}if(!v&&b)return null}
    let x=0n;for(let k=0;k<d;k++)if(B.has(k)){let [v,b]=B.get(k);if(parity(v&x)!==b)x|=bit(k)}return x}
  const rowsOf=(F,D)=>D.flatMap(i=>F[i].rows);
  const good=(f,x)=>f.rows.some((r,j)=>parity(r&x)!==f.b[j]);
  const valid=(F,x)=>F.every(f=>good(f,x));
  const allIdx=F=>F.map((_,i)=>i);
  let calls=0;
  // Linear matroid modulo base, and partition matroid on factor labels.
  function matching(F,D,base=[]){
    calls++;
    let E=D.flatMap(i=>F[i].rows.map((v,j)=>({i,j,v})));
    let I=new Set(),r0=rank(base);
    function linear(J){return rank(base.concat(J.map(a=>E[a].v)))===r0+J.length}
    function partition(J){return new Set(J.map(a=>E[a].i)).size===J.length}
    while(true){
      let A=[...I],O=E.map((_,i)=>i).filter(i=>!I.has(i));
      let src=O.filter(e=>linear(A.concat(e))),sink=new Set(O.filter(e=>partition(A.concat(e))));
      let prev=new Map(src.map(e=>[e,-1])),q=src.slice(),end=-1;
      for(let k=0;k<q.length;k++){
        let v=q[k];if(sink.has(v)){end=v;break}
        let ns=I.has(v)?O.filter(e=>linear(A.filter(a=>a!==v).concat(e))):A.filter(a=>partition(A.filter(b=>b!==a).concat(v)));
        for(let w of ns)if(!prev.has(w)){prev.set(w,v);q.push(w)}
      }
      if(end<0)return [...I].map(e=>E[e]);
      for(let v=end;v>=0;v=prev.get(v)){if(I.has(v))I.delete(v);else I.add(v)}
      assert(I.size===A.length+1&&linear([...I])&&partition([...I]),"augment");
    }
  }
  function core(F){
    let D=allIdx(F),def=D.length-matching(F,D).length;
    for(let i of allIdx(F)){let T=D.filter(j=>j!==i);if(T.length-matching(F,T).length===def)D=T}
    let base=rowsOf(F,D),outside=allIdx(F).filter(i=>!D.includes(i)),rep=matching(F,outside,base);
    assert(rep.length===outside.length,"quotient saturation");
    assert(rank(base.concat(rep.map(e=>e.v)))===rank(base)+outside.length);
    return {D,def,rep,r:rank(base)};
  }
  function lift(F,K,x,d){let base=rowsOf(F,K.D),rhs=base.map(v=>parity(v&x));
    let y=solve(base.concat(K.rep.map(e=>e.v)),rhs.concat(K.rep.map(e=>1^F[e.i].b[e.j])),d);
    assert(y!==null&&K.D.every(i=>F[i].rows.every(v=>parity(v&y)===parity(v&x))),"lift preservation");
    return y}
  function bruteCore(F){let m=F.length,max=-1,min=m+1,answer=[];
    for(let mask=0;mask<2**m;mask++){let D=allIdx(F).filter(i=>(mask>>i)&1),v=D.length-rank(rowsOf(F,D));if(v>max||(v===max&&D.length<min)){max=v;min=D.length;answer=D}}
    return {max,answer}}
  // Polynomial rank-one forced-information closure, via affine substitution.
  // Rebuild every factor under x_p = rhs + lower terms, canonicalize independent rows.
  function closure(F){
    F=F.map(f=>({rows:f.rows.slice(),b:f.b.slice()}));let steps=0;
    function norm(f){let B=new Map();for(let j=0;j<f.rows.length;j++){let v=f.rows[j],b=f.b[j];while(v){let k=v.toString(2).length-1;if(!B.has(k)){B.set(k,[v,b]);break}let [w,c]=B.get(k);v^=w;b^=c}if(!v&&b)return null}let pairs=[...B.values()];return {rows:pairs.map(x=>x[0]),b:pairs.map(x=>x[1])}}
    while(true){F=F.map(norm).filter(f=>f!==null);if(F.some(f=>!f.rows.length))return {unsat:true,steps,F};
      let f=F.find(f=>f.rows.length===1);if(!f)return {unsat:false,steps,F};
      let v=f.rows[0],c=1^f.b[0],p=bit(v.toString(2).length-1);steps++;
      F=F.map(g=>({rows:g.rows.map(r=>(r&p)?r^v:r),b:g.b.map((b,j)=>b^((g.rows[j]&p)?c:0))}));
    }
  }
  let seed=20261123;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
  let counts={random:0,sat:0,unsat:0,forced:0,early:0,allBoundaryLifts:0,parityProfiles:new Set()};
  for(let t=0;t<360;t++){
    let d=2+rand(6),m=1+rand(8),F=[];
    for(let i=0;i<m;i++){let k=1+rand(Math.min(3,d)),rows=[];while(rows.length<k){let v=BigInt(1+rand(2**d-1));if(rank(rows.concat(v))>rows.length)rows.push(v)}F.push({rows,b:rows.map(()=>rand(2))})}
    let orig=F,cl=closure(F);counts.forced+=cl.steps;
    let origSAT=false;for(let x=0n;x<bit(d);x++)if(valid(orig,x)){origSAT=true;break}
    counts.random++;counts[origSAT?"sat":"unsat"]++;
    if(cl.unsat){assert(!origSAT);counts.early++;continue}
    F=cl.F;let K=core(F),B=bruteCore(F);assert(K.def===B.max&&JSON.stringify(K.D)===JSON.stringify(B.answer),"min core");
    let sat=false;let R=rank(rowsOf(F,allIdx(F))),ex=F.reduce((a,f)=>a+f.rows.length,0)-R;
    counts.parityProfiles.add([R%2,(d-R)%2,ex%2,K.r%2].join(""));
    for(let x=0n;x<bit(d);x++)if(K.D.every(i=>good(F[i],x))){sat=true;let y=lift(F,K,x,d);assert(valid(F,y),"valid lift");counts.allBoundaryLifts++}
    assert(sat===origSAT,"SAT equivalence");
  }
  // Fano NAE factors: complement of the monochromatic affine subspace.
  let fano=[];for(let a=1;a<=7;a++)for(let b=a+1;b<=7;b++){let c=a^b;if(c>b)fano.push({rows:[bit(a-1)^bit(b-1),bit(a-1)^bit(c-1)],b:[0,0],line:[a,b,c]})}
  assert(fano.length===7);
  let fanoSAT=0,neighbors=0;for(let x=0n;x<128n;x++)if(valid(fano,x))fanoSAT++;assert(fanoSAT===0);
  for(let i=0;i<7;i++){let F=fano.filter((_,j)=>i!==j),K=core(F);assert(K.D.length===0);assert(valid(F,lift(F,K,0n,7)));neighbors++}
  // Exact bounded-group union check on core's 128 input states. No proper union affine.
  let groups=0;for(let mask=1;mask<127;mask++){let D=allIdx(fano).filter(i=>(mask>>i)&1);if(D.length<2)continue;let U=[];for(let x=0n;x<128n;x++)if(D.some(i=>!good(fano[i],x)))U.push(x);
    let ar=rank(U.map(x=>x^U[0]));assert(BigInt(U.length)!==bit(ar),"proper Fano union affine");groups++}
  let families=[];
  for(let t of [3,4,5,6,7,8,11,12,19,20])for(let degree of [2,4]){
    if(degree===4&&t<5)continue;
    for(let charge of [0,1])for(let e of [0,1]){
      let q=bit(0)^bit(1),extra=[];
      for(let i=0;i<t;i++){let rows=[bit(7+i),bit(7+(i+1)%t),q];if(degree===4)rows.splice(2,0,bit(7+(i+2)%t));let b=rows.map(()=>0);if(i===0)b[0]=charge;extra.push({rows,b})}
      let root=fano.concat(extra),K=core(root),d=7+t+e,R=rank(rowsOf(root,allIdx(root)));
      assert(K.def===1&&K.r===6&&K.D.length===7&&R===6+t);
      assert(root.every((f,i)=>rank(rowsOf(root,allIdx(root).filter(j=>j!==i)))===R),"no private direction");
      let cut=extra.map((_,i)=>i+7),rCut=rank(rowsOf(root,cut))+6-R;assert(rCut===1);
      let nei=root.filter((_,i)=>i!==0),L=core(nei);assert(L.def===0&&L.D.length===0&&valid(nei,lift(nei,L,0n,d)));
      families.push({t,degree,charge,e,rank:R,nullity:d-R,excess:root.reduce((s,f)=>s+f.rows.length,0)-R,core:K.r});
    }
  }
  // Even/odd signed rank-one cycle, dependency charge and forced closure.
  let cycles=0;
  for(let t=3;t<=12;t++)for(let charge of [0,1]){
    let F=Array.from({length:t},(_,i)=>({rows:[bit(i)^bit((i+1)%t)],b:[1^(i===0?charge:0)]}));
    let C=closure(F);assert(C.unsat===Boolean(charge));cycles++;
  }
  return {random:{...counts,parityProfiles:[...counts.parityProfiles].sort()},fano:{rootSAT:fanoSAT,deletionNeighbors:neighbors,properNonaffineUnions:groups},familyPairs:families.length,example:families.filter(x=>x.t===20&&x.charge===1&&x.e===0),rankOneCycleChecks:cycles,matroidCalls:calls};
};
console.log(JSON.stringify(main(),null,2));
