function audit(){
 let seed=20261125>>>0; const rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed>>>8};
 const parity=x=>{let p=0;while(x){p^=1;x&=x-1n}return p}, bit=(x,i)=>Number((x>>BigInt(i))&1n), B=i=>1n<<BigInt(i);
 const rank=xs=>{let piv=new Map;for(let x of xs){while(x){let k=x.toString(2).length-1;if(piv.has(k))x^=piv.get(k);else{piv.set(k,x);break}}}return piv.size};
 const stat={cases:0,sat:0,unsat:0,projectionChecks:0,legalWitnessChecks:0,affineHullChecks:0,localRankChecks:0,restoreChecks:0,knownBasisWords:0,fullPairChecks:0};
 const check=(c,msg)=>{if(!c)throw Error(msg)};
 // Literal is [index, desired truth bit]. Base coordinates x followed by k control bits.
 function compile(n,F,k){
  let size=n+k, rows=[], clauses=[], blocks=[];
  let guard=0n;for(let i=0;i<k;i++)guard|=B(n+i);
  for(const C of F)for(let p=0;p<2**k;p++)if(parity(BigInt(p))){
   const L=[...Array.from({length:k},(_,i)=>[n+i,1-((p>>i)&1)]),...C];
   const S=[],O=[];for(const [v,b] of L){let s=size++,o=size++;S.push(s);O.push(o);rows.push([B(o)|B(v),1-b]);clauses.push([s,o])}
   rows.push([S.reduce((a,i)=>a|B(i),0n),1]);blocks.push({L,S,O});
  }
  const g1=size++,g2=size++;rows.push([B(g1)|guard,0],[B(g2)|guard,0]);
  return {n,k,F,size,rows,clauses,blocks,guard,g1,g2,D:n+k+blocks.length*(k+2)};
 }
 const source=(F,x)=>F.every(C=>C.some(([v,b])=>bit(x,v)===b));
 function lift(I,z,override=null,ambient=false){
  let w=z;
  for(let h=0;h<I.blocks.length;h++){
   let {L,S,O}=I.blocks[h], truth=L.map(([v,b])=>bit(z,v)===b);
   let j=ambient?0:truth.indexOf(true);
   if(override&&override[0]===h)j=override[1];
   if(j<0||(!ambient&&!truth[j]))return null;
   w|=B(S[j]);truth.forEach((v,i)=>{if(v)w|=B(O[i])});
  }
  if(parity(z&I.guard))w|=B(I.g1)|B(I.g2);return w;
 }
 function verify(I,w,restore=false,affineOnly=false){
  check(w!==null,"missing witness");
  check(I.rows.every(([r,b])=>parity(w&r)===b),"affine row");
  if(!affineOnly)check(I.clauses.every(([s,o])=>!bit(w,s)||bit(w,o)),"matching clause");
  if(restore)check(bit(w,I.g1)||bit(w,I.g2),"restored clause");
  stat.legalWitnessChecks++;
 }
 function pairProjection(I,L,i,j){
  let z=0n;
  const cs=[];
  for(let h of [i,j]){const [v,b]=L[h];if(v<I.n){if(b)z|=B(v)}else cs.push([v-I.n,b])}
  for(let p=0;p<2**I.k;p++)if(!parity(BigInt(p))&&cs.every(([v,b])=>((p>>v)&1)===b))return z|(BigInt(p)<<BigInt(I.n));
  throw Error("pair projection");
 }
 function run(n,F,k){
  let I=compile(n,F,k);stat.cases++;
  check(new Set(I.clauses.flat().concat([I.g1,I.g2])).size===2*(I.clauses.length+1),"matching promise");
  const base=lift(I,0n), pool=[base];verify(I,base);
  for(let i=0;i<n;i++)pool.push(lift(I,B(i)));
  for(let j=1;j<k;j++)pool.push(lift(I,B(n)|B(n+j)));
  for(let h=0;h<I.blocks.length;h++){
   const {L}=I.blocks[h];
   for(let j=1;j<L.length;j++){
    let z=pairProjection(I,L,0,j);
    pool.push(lift(I,z,[h,0]),lift(I,z,[h,j]));
   }
  }
  let diffs=pool.map(w=>w^base);
  for(let w of pool){verify(I,w);check(!parity(w&I.guard),"known guard");}
  check(rank(diffs)===I.D-1,"known hull rank");stat.affineHullChecks++;stat.knownBasisWords+=pool.length;
  const ambient0=lift(I,0n,null,true);
  const ambient=[...Array.from({length:n+k},(_,i)=>lift(I,B(i),null,true)^ambient0)];
  for(const {S} of I.blocks)for(let j=1;j<S.length;j++)ambient.push(B(S[0])|B(S[j]));
  check(rank(ambient)===I.D&&I.size-rank(I.rows.map(x=>x[0]))===I.D,"ambient dimension");
  for(const [s,o] of I.clauses){
   // Paid local rank-0/1 packet closure: local forbidden pair has full rank both globally and in known even hyperplane.
   const masks=[...new Set(diffs.map(w=>bit(w,s)+2*bit(w,o)))].map(BigInt);
   check(rank(masks)===2,"even local rank");stat.localRankChecks++;
  }
  // Independent direct source/guard enumeration. Test all projected words, exact lift or local obstruction.
  let sat=false,odd=null;
  for(let z=0;z<2**(n+k);z++){
   let Z=BigInt(z), g=parity(Z&I.guard), expected=!g||source(F,Z);
   let direct=I.blocks.every(({L})=>L.some(([v,b])=>bit(Z,v)===b));
   check(direct===expected,"projection");
   let w=lift(I,Z);check((w!==null)===expected,"witness iff");
   if(w!==null){verify(I,w);if(g){verify(I,w,true);sat=true;odd=w}}
   stat.projectionChecks++;
  }
  check(sat===Array.from({length:2**n},(_,x)=>source(F,BigInt(x))).some(Boolean),"source decision");
  if(sat){stat.sat++;check(rank([...diffs,odd^base])===I.D,"full hull");stat.restoreChecks++}
  else {stat.unsat++;check(rank(diffs)===I.D-1,"unsat hull");stat.restoreChecks++}
  // Low-order source/control projections: every coordinate pair, every pattern on the pair extends even guard.
  for(let i=0;i<n+k;i++)for(let j=i+1;j<n+k;j++)for(let p=0;p<4;p++){
   let z=pairProjection(I,[[i,p&1],[j,p>>1]],0,1);check(bit(z,i)===(p&1)&&bit(z,j)===(p>>1)&&!parity(z&I.guard),"pair freedom");stat.fullPairChecks++;
  }
  return {n,k,m:F.length,ambientRank:I.D,knownRank:I.D-1,legalRank:I.D-(sat?0:1),sat,source:F};
 }
 let cases=[];
 let all=Array.from({length:8},(_,p)=>[0,1,2].map(v=>[v,(p>>v)&1]));
 cases.push(run(3,all,3));for(let j=0;j<8;j++)cases.push(run(3,all.filter((_,i)=>i!==j),3));
 for(let t=0;t<24;t++){
  let n=3+rng()%3,m=1+rng()%9,F=[];
  for(let j=0;j<m;j++){let V=[];while(V.length<3){let v=rng()%n;if(!V.includes(v))V.push(v)}F.push(V.map(v=>[v,rng()%2]))}
  cases.push(run(n,F,3));
 }
 cases.push(run(3,all,4),run(3,all.slice(1),4),run(3,all,5),run(3,all.slice(1),5));
 return {seed:20261125,stats:stat,cases};
}
console.log(JSON.stringify(audit(),null,2));
