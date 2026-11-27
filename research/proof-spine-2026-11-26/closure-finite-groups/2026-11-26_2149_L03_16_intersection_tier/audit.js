function audit(){
 const assert=(b)=>{if(!b)throw Error("audit failed")};
 const source=m=>{let C=[];for(let i=1;i<=m;i++)C.push([-i,m+i],[-i,-(m+i)]);for(let i=1;i<=m;i++)C.push([...(i>1?[-(2*m+i-1)]:[]),i,...(i<m?[2*m+i]:[])]);return C};
 const fp=(C)=>{let h=14695981039346656037n;for(const c of JSON.stringify(C)){h^=BigInt(c.charCodeAt(0));h=BigInt.asUintN(64,h*1099511628211n)}return h.toString(16).padStart(16,"0")};
 const up=(C,initial)=>{let a=new Map(initial),passes=0,scans=0;while(true){passes++;let changed=false,R=[];for(let j=0;j<C.length;j++){const c=C[j];scans+=c.length;let q=c.filter(l=>!a.has(Math.abs(l)));if(c.some(l=>a.get(Math.abs(l))===Number(l>0)))continue;if(!q.length)return{no:true,a,passes,scans,R};R.push({id:j,c:q});if(q.length===1){a.set(Math.abs(q[0]),Number(q[0]>0));changed=true}}if(!changed)return{no:false,a,passes,scans,R}}};
 const sat=(c,a)=>c.some(l=>a.get(Math.abs(l))===Number(l>0));
 const sum=(...ps)=>{let z=new Set();for(let p of ps)for(let v of p){if(z.has(v))z.delete(v);else z.add(v)}return z};
 const mul=(p,q)=>sum(...[...p].map(a=>new Set([...q].map(b=>a|b))));
 // Products of a single monomial and q can collide: correct using per-pair parity.
 const times=(p,q)=>{let z=new Set();for(let a of p)for(let b of q){let c=a|b;if(z.has(c))z.delete(c);else z.add(c)}return z};
 const one=new Set([0n]),zero=new Set(),v=i=>new Set([1n<<BigInt(i-1)]),neg=p=>sum(one,p);
 const indicator=c=>c.reduce((p,l)=>times(p,l>0?neg(v(l)):v(-l)),one);
 const eq=(p,q)=>sum(p,q).size===0;
 let exhaustive=0,slice=0,dual=0,polynomialChecks=0,rows=[];
 const m=256,C=source(m);
 for(let r of [0,1,2,3,4,5,8,16,32,64,128,256]){
  let pins=new Map();for(let i=r+1;i<=m;i++)pins.set(i,0);
  let u=up(C,pins);
  if(r<2){assert(u.no);rows.push({r,initialNO:true,scans:u.scans});continue}
  assert(!u.no&&u.R.length===3*r);
  const R=u.R.map(x=>x.c), byID=new Map(u.R.map(x=>[x.id,x.c]));
  // A: explicit resolution units, then reclose.
  let units=[];for(let i=1;i<=r;i++){let p=byID.get(2*i-2),q=byID.get(2*i-1);assert(p.length===2&&q.length===2&&p[0]===-i&&q[0]===-i&&p[1]===-q[1]);units.push([-i])}
  let end=up(R.concat(units),new Map());assert(end.no);
  // B: independently reconstruct dynamic algebra on the same residual.
  let previous=zero;let steps=0;
  for(let i=1;i<=r;i++){
   let x=v(i),prev=i===1?one:v(2*m+i-1),next=i===r?zero:v(2*m+i);
   let a=indicator(byID.get(2*i-2)),b=indicator(byID.get(2*i-1)),q=indicator(byID.get(2*m+i-1));
   let learned=sum(a,b);assert(eq(learned,x));polynomialChecks++;
   let corrected=sum(q,times(times(learned,prev),neg(next)));assert(eq(corrected,times(prev,neg(next))));polynomialChecks++;
   assert(eq(previous,neg(prev)));previous=sum(corrected,times(previous,neg(next)));assert(eq(previous,neg(next)));polynomialChecks++;steps+=1+(i===1?2:3)+(i===r?0:3);
  }assert(eq(previous,one));
  // C: independent truth-table violation patterns; no SAT label assumed.
  if(r<=5){
   let ids=[...new Set(R.flat().map(Math.abs))].sort((a,b)=>a-b);assert(ids.length===3*r-1);let max=0;
   for(let bits=0;bits<2**ids.length;bits++){let a=new Map(ids.map((x,j)=>[x,(bits>>j)&1]));let h=R.filter(c=>!sat(c,a)).length;assert(h>=1&&h<=r);max=Math.max(max,h);exhaustive++}assert(max===r);
   // witness slice: a=0, first true transition of s.
   let masks=[];
   for(let bits=1;bits<2**r;bits++){let a=new Map(),j=1;while(!((bits>>(j-1))&1))j++;
    for(let i=1;i<=r;i++){a.set(i,(bits>>(i-1))&1);a.set(m+i,0);if(i<r)a.set(2*m+i,Number(i<j))}
    let violated=u.R.filter(z=>!sat(z.c,a)).map(z=>z.id);let expected=Array.from({length:r},(_,i)=>i).filter(i=>(bits>>i)&1).map(i=>2*i);assert(JSON.stringify(violated)===JSON.stringify(expected));masks.push(bits);slice++;
   }
   // dual check: for every nonempty subset S, sum evaluations of monomials on its nonzero subcube.
   for(let S=1;S<2**r;S++)for(let T=1;T<2**r;T++){let parity=0;for(let a of masks)if((a&S)===a&&(a&T)===T)parity^=1;assert(parity===Number(S===T));dual++}
  }
  rows.push({r,initialNO:false,residualClauses:R.length,initialScans:u.scans,learnedUnits:units.length,closureScans:end.scans,algebraChecks:3*r,pcStepUpperBound:8*r,minimumTier:r,minimumExplicitTerms:(2n**BigInt(r)-1n).toString(),allProductUpperBound:(4n**BigInt(r)-1n).toString(),fingerprint:fp(u.R)})
 }
 // Width two/three Horn recognition of each residual; positive literal count <=1? chain contains x and s -> not Horn. Renaming x positive to negative makes all Horn, pair has x positive after renaming with a positive -> not Horn; use resolution above.
 return{parent:{m,variables:3*m-1,clauses:C.length,fingerprint:fp(C)},rows,exhaustiveAssignments:exhaustive,sliceChecks:slice,dualChecks:dual,polynomialChecks}
}
console.log(JSON.stringify(audit(),null,2));
