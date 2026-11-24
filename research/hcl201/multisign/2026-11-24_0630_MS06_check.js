// MS06 reproducible small integer-lattice closure tests. Run: node FILE
function experiment(){
 const seed=0x2010630;let state=seed>>>0;function rnd(n){state=(Math.imul(state,1664525)+1013904223)>>>0;return state%n}
 const assert=(p,m)=>{if(!p)throw Error(m)};
 let metrics={latticeCalls:0,euclidSteps:0,rowRemovals:0,priceRemovals:0,rounds:0};
 const row=(c,g=0)=>({c:c.map(BigInt),g});
 const sum=(a,b)=>a.map((v,i)=>v+b[i]); const sub=(a,b)=>a.map((v,i)=>v-b[i]);const dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0n);
 function member(cols,target){
  metrics.latticeCalls++;let a=cols.map(c=>c.slice()),t=target.slice();
  while(t.length){
   let j=a.findIndex(c=>c[0]!==0n);
   if(j<0){if(t[0]!==0n)return false;a=a.map(c=>c.slice(1));t=t.slice(1);continue;}
   [a[0],a[j]]=[a[j],a[0]];
   for(let k=1;k<a.length;k++)while(a[k][0]!==0n){
    let q=a[k][0]/a[0][0];a[k]=a[k].map((v,i)=>v-q*a[0][i]);metrics.euclidSteps++;
    if(a[k][0]!==0n)[a[k],a[0]]=[a[0],a[k]];
   }
   if(t[0]%a[0][0]!==0n)return false;
   t=sub(t,a[0].map(v=>v*(t[0]/a[0][0]))).slice(1);
   a=a.slice(1).map(c=>c.slice(1));
  }
  return true;
 }
 function vectors(rows,K,T,q,tag,pin=null){
  const target=T.map(i=>K[i]).concat(Array.from({length:q},(_,j)=>BigInt((tag>>j)&1)));
  const zero=target.map(()=>0n);let base=zero.slice(),cols=[];
  function v(r){return T.map(i=>r.c[i]).concat(Array.from({length:q},(_,j)=>BigInt((r.g>>j)&1)))}
  for(let b=0;b<rows.length;b++){let R=pin&&pin[0]===b?[rows[b][pin[1]]]:rows[b];let u=v(R[0]);base=sum(base,u);for(let j=1;j<R.length;j++)cols.push(sub(v(R[j]),u));}
  for(let j=0;j<q;j++){let c=zero.slice();c[T.length+j]=2n;cols.push(c);}
  return {cols,target:sub(target,base)};
 }
 function closure(original,K,q=0,tag=0,useLattice=true){
  let rows=original.map(B=>B.slice());let n=K.length;
  const prices=[Array(n).fill(1n),...Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>BigInt(i===j)))];
  while(true){metrics.rounds++;if(rows.some(B=>!B.length))return {reject:true,rows,why:"empty"};
   let changed=false,T=new Set();
   for(const y of prices){const mins=rows.map(B=>B.map(r=>dot(y,r.c)).reduce((a,b)=>a<b?a:b));let gap=dot(y,K)-mins.reduce((a,b)=>a+b,0n);
    if(gap<0n)return {reject:true,rows,why:"price"};
    y.forEach((v,i)=>{if(v>gap)T.add(i)});
    for(let b=0;b<rows.length;b++){let old=rows[b];rows[b]=old.filter(r=>dot(y,r.c)-mins[b]<=gap);let d=old.length-rows[b].length;if(d){metrics.priceRemovals+=d;changed=true}}
    if(rows.some(B=>!B.length))return {reject:true,rows,why:"price-empty"};
   }
   if(changed)continue;if(!useLattice)return {reject:false,rows,T:[...T]};
   let t=[...T];const test=pin=>{const x=vectors(rows,K,t,q,tag,pin);return member(x.cols,x.target)};
   if(!test(null))return {reject:true,rows,why:"lattice",T:t};
   // Batch removals use a common pre-deletion snapshot.
   let next=rows.map((B,b)=>B.filter((r,j)=>B.length===1||test([b,j])));
   let d=rows.reduce((s,B,b)=>s+B.length-next[b].length,0);
   if(!d)return {reject:false,rows,T:t};
   metrics.rowRemovals+=d;rows=next;
  }
 }
 function exhaustive(R,K,q,tag){let feasible=0,tuples=0,support=R.map(()=>new Set());const mask=(1<<q)-1;
  function rec(b,c,g,p){if(b===R.length){tuples++;if((g&mask)!==tag||c.some((v,i)=>v>K[i]))return;feasible++;p.forEach((r,i)=>support[i].add(r));return;}
   for(const r of R[b])rec(b+1,sum(c,r.c),g^r.g,p.concat(r));
  }rec(0,K.map(()=>0n),0,[]);return {feasible,tuples,support};
 }
 function modSpan(cols,t,p){const mod=x=>Number((x%BigInt(p)+BigInt(p))%BigInt(p));let basis=new Map();function red(c){for(let i=0;i<c.length;i++){if(!c[i])continue;if(!basis.has(i))return c;let v=basis.get(i),k=c[i];c=c.map((a,j)=>(a-k*v[j]+p*p)%p)}return c;}
  for(const c of cols){let v=red(c.map(mod)),i=v.findIndex(x=>x);if(i<0)continue;let inv=1;while((inv*v[i])%p!==1)inv++;basis.set(i,v.map(x=>(x*inv)%p));}return red(t.map(mod)).every(x=>x===0);
 }
 let random={networks:180,queries:0,sat:0,unsat:0,exhaustiveTuples:0,soundRejects:0,priceRejects:0,latticeRejects:0,unresolvedUnsat:0,supportedRowsChecked:0,latticeNewRejected:0,changedSurvivors:0};
 for(let k=0;k<180;k++){let n=2+rnd(3),B=2+rnd(4),R=Array.from({length:B},()=>Array.from({length:2+rnd(2)},()=>row(Array.from({length:n},()=>rnd(4)),rnd(4))));
  // Half have constant row total across all rows of a block.
  if(k%2===0){R=R.map(L=>{let w=1+rnd(5);return L.map(r=>{let c=Array(n).fill(0);for(let j=0;j<w;j++)c[rnd(n)]++;return row(c,r.g)})})}
  let K=Array(n).fill(0n);for(const L of R)K=sum(K,L[rnd(L.length)].c);K=K.map(v=>v+BigInt(rnd(3)-1));K=K.map(v=>v<0n?0n:v);
  for(let q=0;q<=2;q++)for(let tag=0;tag<(1<<q);tag++){
   let ref=exhaustive(R,K,q,tag),pre=closure(R,K,q,tag,false),out=closure(R,K,q,tag,true);random.queries++;random.exhaustiveTuples+=ref.tuples;
   if(ref.feasible){random.sat++;assert(!out.reject,"false UNSAT");for(let b=0;b<B;b++)for(const r of ref.support[b]){random.supportedRowsChecked++;assert(out.rows[b].includes(r),"lost feasible row")}}
   else{random.unsat++;if(out.reject){random.soundRejects++;if(out.why==="lattice")random.latticeRejects++;else random.priceRejects++;if(!pre.reject)random.latticeNewRejected++;}else random.unresolvedUnsat++}
   if(!out.reject&&!pre.reject&&out.rows.some((L,b)=>L.length<pre.rows[b].length))random.changedSurvivors++;
  }
 }
 function make(k,selector){let h=2*k+1,A=[1,1,1,0,0,0],B=[0,0,0,1,1,1],R=Array.from({length:h},()=>[row(A),row(B)]);
  for(let g=0;g<2;g++)for(let j=0;j<3;j++)R.push(Array.from({length:3},(_,i)=>row(Array.from({length:6},(_,l)=>Number(l===3*g+i)))));
  if(selector)R.push([row([1,0,0,0,0,0],1),row([0,0,0,1,0,0],0)]);
  const K=(selector?[k+1,k+1,k+2,k+2,k+2,k+2]:[k+1,k+1,k+2,k+1,k+2,k+2]).map(BigInt);
  return {R,K,h};
 }
 // Exact fractional LP witness, numerator denominator 9; selector index null for no selector, 0 or 1 otherwise.
 function fractionCheck(k,selector,pin){const {R,K,h}=make(k,selector);const u3=selector&&pin===0?3*k:3*k+1,v3=3*h-u3;
  let weights=[];for(let i=0;i<k;i++)weights.push([9n,0n]);for(let i=0;i<k;i++)weights.push([0n,9n]);weights.push([BigInt(3*(u3-3*k)),BigInt(9-3*(u3-3*k))]);
  let rem=K.map((v,i)=>3n*v-BigInt(i<3?u3:v3)-BigInt(selector&&((pin===0&&i===0)||(pin===1&&i===3))?3:0));
  for(let g=0;g<2;g++)for(let j=0;j<3;j++)weights.push(rem.slice(g*3,g*3+3));
  if(selector)weights.push(pin===0?[9n,0n]:[0n,9n]);
  let total=K.map(()=>0n);assert(weights.length===R.length,"fraction size");
  weights.forEach((w,b)=>{assert(w.every(x=>x>=0n)&&w.reduce((a,b)=>a+b,0n)===9n,"bad fraction");w.forEach((x,j)=>{total=sum(total,R[b][j].c.map(v=>v*x))})});
  assert(total.every((v,i)=>v===9n*K[i]),"fraction violates budgets");return true;
 }
 let scaling=[];
 for(const k of [1,2,4,8,16,32,64,128]){
  let U=make(k,false),S=make(k,true);let lpU=fractionCheck(k,false,null),lpA=fractionCheck(k,true,0),lpB=fractionCheck(k,true,1);
  let preU=closure(U.R,U.K,0,0,false),preS=closure(S.R,S.K,0,0,false);assert(!preU.reject&&!preS.reject,"price rejected");assert(preU.rows.every((L,b)=>L.length===U.R[b].length)&&preS.rows.every((L,b)=>L.length===S.R[b].length),"price pruning");
  let uvec=vectors(U.R,U.K,[0,1,2,3,4,5],0,0),bvec=vectors(S.R,S.K,[0,1,2,3,4,5],0,0,[S.R.length-1,1]);
  assert(modSpan(uvec.cols,uvec.target,2)&&modSpan(bvec.cols,bvec.target,2),"mod2 unexpectedly detects");
  assert(!modSpan(uvec.cols,uvec.target,3)&&!modSpan(bvec.cols,bvec.target,3),"mod3 misses");
  let outU=closure(U.R,U.K),outS=closure(S.R,S.K),beforeTag=closure(S.R,S.K,1,0);
  assert(outU.reject&&outU.why==="lattice","missed UNSAT");assert(!outS.reject&&outS.rows.at(-1).length===1&&outS.rows.at(-1)[0]===S.R.at(-1)[0],"selector not forced");assert(beforeTag.reject,"protected contrary tag not rejected");
  // Construct exact SAT witness: k cross A, k+1 cross B, A internal (A2,A3,A3), B internal each owner once, selector A1.
  let chosen=[...Array.from({length:S.h},(_,i)=>i<k?0:1),1,2,2,0,1,2,0];let cost=S.K.map(()=>0n);chosen.forEach((j,i)=>cost=sum(cost,S.R[i][j].c));assert(cost.every((v,i)=>v===S.K[i]),"SAT witness");
  let logCbefore=5*S.h+8,logCafter=5*S.h+7; // independently calculate cycle rank of positive-domain incidence graph
  function rankC(rows){let n=rows.length+6,p=Array.from({length:n},(_,i)=>i),find=x=>{while(p[x]!==x)x=p[x];return x},E=0,rank=0;for(let i=0;i<rows.length;i++)for(let j=0;j<6;j++){if(new Set(rows[i].map(r=>String(r.c[j]))).size<2)continue;E++;let a=find(i),b=find(rows.length+j);if(a!==b){p[a]=b;rank++}}return E-rank}
  assert(rankC(S.R)===logCbefore&&rankC(outS.rows)===logCafter,"cut rank");
  let exact=null;if(k<=2){let a=exhaustive(U.R,U.K,0,0),b=exhaustive(S.R,S.K,0,0);assert(!a.feasible&&b.feasible>0,"scaling reference");exact={unsatTuples:a.tuples,satTuples:b.tuples,satSolutions:b.feasible}}
  scaling.push({k,crossBlocks:S.h,LPfeasibleAllThree:lpU&&lpA&&lpB,mod2Pass:true,mod3Reject:true,forcedSelector:"A",logCbefore,logCafter,exact});
 }
 const hostileR=[4,4,5,7].map(w=>[row([w,0]),row([0,w])]),hostileK=[10n,10n];
 const hostile=closure(hostileR,hostileK),hostileRef=exhaustive(hostileR,hostileK,0,0);
 assert(!hostile.reject&&hostile.rows.every(L=>L.length===2)&&hostileRef.feasible===0,"hostile control");
 // Higher prime-power: mod 2 loses 2*x+4*y+4*z=6, lattice pin forces weight-2 block to A.
 let powR=[2,4,4].map(w=>[row([w,0]),row([0,w])]),powK=[6n,4n],powOut=closure(powR,powK),powRef=exhaustive(powR,powK,0,0);
 assert(!powOut.reject&&powOut.rows[0].length===1&&powOut.rows[0][0]===powR[0][0]&&powRef.feasible===2,"prime power control");
 return {seed,random,scaling,hostile:{weights:[4,4,5,7],budgets:[10,10],exactSolutions:0,latticeSurvives:true},primePower:{weights:[2,4,4],budgets:[6,4],forcedWeightTwoToA:true,exactSolutions:powRef.feasible},metrics};
}
console.log(JSON.stringify(experiment(),null,2));
