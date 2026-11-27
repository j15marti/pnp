function audit(){
 const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const pop=x=>{let a=0;while(x){x&=x-1;a++}return a};
 const rows=F.map((_,e)=>F.reduce((a,T,j)=>a|(T.includes(e)?1<<j:0),0));
 const words=Array.from({length:128},(_,x)=>x).filter(x=>rows.every(r=>pop(x&r)%2===1));
 const word=z=>words.find(x=>(x&1)===(z&1)&&((x>>3)&1)===((z>>1)&1)&&((x>>1)&1)===((z>>2)&1));
 const check=(x,msg)=>{if(!x)throw Error(msg)};
 const A=[3,5],B=[0,1,2,4,6], table=J=>Array.from({length:8},(_,z)=>Number(J.every(e=>pop(word(z)&rows[e])===1)));
 const a=table(A),b=table(B);
 function algebra(M){
  const mod=x=>(x%M+M)%M, inv2=(M+1n)/2n;
  function pow(a,n){let r=1n;for(;n;n>>=1){if(n&1)r=mod(r*a);a=mod(a*a)}return r}
  function fft(v){let n=v.length,scale=pow(inv2,Math.log2(n));return v.map((_,u)=>mod(scale*v.reduce((s,x,z)=>s+BigInt(x)*(pop(u&z)%2?-1n:1n),0n)))}
  function mul(a,b){let c=Array(a.length).fill(0n),ops=0;for(let i=0;i<a.length;i++)if(a[i])for(let j=0;j<b.length;j++)if(b[j]){c[i^j]=mod(c[i^j]+a[i]*b[j]);ops++}return {c,ops}}
  function val(a,z){return mod(a.reduce((s,x,u)=>s+x*(pop(u&z)%2?-1n:1n),0n))}
  return {mod,fft,mul,val};
 }
 function source(k){
  const T=[];for(let i=0;i<k;i++)for(let j=0;j<7;j++)T.push(F[j].map(e=>7*((j===0&&e===0)?(i+1)%k:(j===3&&e===1)?(i+k-1)%k:i)+e));
  const inc=Array.from({length:7*k},()=>[]);T.forEach((t,j)=>t.forEach(e=>inc[e].push(j)));
  let p=[],swap=[],owner=[],centers=[],s=0;
  for(let e=0;e<inc.length;e++){let c=s++,L=inc[e].map(()=>s++),d=s++,R=inc[e].map(()=>s++).reverse();centers.push([c,d]);L.forEach((l,i)=>{swap[l]=R[i];swap[R[i]]=l;owner[l]=owner[R[i]]=inc[e][i]})}
  for(let i=0;i<s;i++){p[i]=(i+1)%s;if(swap[i]===undefined)swap[i]=i}
  for(let [c,d] of centers)[p[c],p[d]]=[p[d],p[c]];
  let lifts=0;
  if(k<=6)for(let z=0;z<2**(k+2);z++){let x=[];for(let i=0;i<k;i++){let w=word((z&3)|(((z>>(i+2))&1)<<2));for(let j=0;j<7;j++)x.push((w>>j)&1)}
   let occ=inc.map(I=>I.reduce((s,j)=>s+x[j],0));check(occ.every(v=>v%2===1),"odd");
   check(A.every(e=>occ[e]===1)===Boolean(a[(z&3)|(((z>>2)&1)<<2)]),"A map");
   check(B.every(e=>occ[7+e]===1)===Boolean(b[(z&3)|(((z>>3)&1)<<2)]),"B map");
   let perm=p.map((v,i)=>owner[i]!==undefined&&x[owner[i]]?p[swap[i]]:v),seen=new Set(),cycles=0;
   check(new Set(perm).size===s,"perm");
   for(let i=0;i<s;i++)if(!seen.has(i)){cycles++;for(let j=i;!seen.has(j);j=perm[j])seen.add(j)}
   check(cycles===1+occ.reduce((s,v)=>s+Math.abs(v-1),0)&&cycles>1,"cycle");lifts++;
  }
  let M=(1n<<BigInt(k+2))+1n,{fft,mul,val}=algebra(M),P=fft(a).slice(0,4),Q=fft(b).slice(0,4),J=mul(P,Q);
  check(J.c.every(x=>x===0n),"joint zero");
  let countA=Array.from({length:4},(_,i)=>a[i]+a[i+4]),countB=Array.from({length:4},(_,i)=>b[i]+b[i+4]);
  for(let i=0;i<4;i++){check((val(P,i)!==0n)===(countA[i]>0),"A support");check((val(Q,i)!==0n)===(countB[i]>0),"B support")}
  return {k,n:3*s,d:k+2,modulus:M.toString(),countA,countB,termsA:P.filter(Boolean).length,termsB:Q.filter(Boolean).length,productOps:J.ops,compressedLifts:lifts};
 }
 let seed=2627;const rand=()=>seed=(Math.imul(seed,1664525)+1013904223)>>>0;let checks=0,smallPrimeFalse=0;
 for(let j=0;j<400;j++){
   let f=Array.from({length:8},()=>Number((rand()>>>24)%4!==0)),g=Array.from({length:8},()=>Number((rand()>>>24)%3!==0));
   const {fft,mul,val,mod}=algebra(17n),small=algebra(3n);
   let P=fft(f).slice(0,2),Q=fft(g).slice(0,2),J=mul(P,Q);
   // Shared observation s=x XOR y; private coordinates x and z,w respectively.
   for(let s=0;s<2;s++){let cf=0,cg=0;for(let h=0;h<4;h++){cf+=f[s+2*h];cg+=g[s+2*h]}
    check((val(P,s)!==0n)===(cf>0),"random f");check((val(Q,s)!==0n)===(cg>0),"random g");
    check((val(J.c,s)!==0n)===(cf*cg>0),"random joint");
    if(cf>0&&small.val(small.fft(f).slice(0,2),s)===0n)smallPrimeFalse++;
    checks+=3;
   }
   let expected=0;for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let h=0;h<2;h++)for(let z=0;z<2;z++)for(let w=0;w<2;w++){let s=x^y;expected+=f[s+2*x+4*h]*g[s+2*z+4*w]}
   // Modulus 17 is enough for each 4x4 conditioned fiber, but not global 32; rerun with M=33.
   let R=algebra(33n),D=R.mul(R.fft(f).slice(0,2),R.fft(g).slice(0,2)).c;
   check(R.mod(D[0]*32n)===BigInt(expected),"global count");checks++;
 }
 let cap=100000,trap=[];
 for(let k of [1,2,4,6,8,12,24]){
  let ops=0,size=1,done=true;for(let i=0;i<k;i++){if(ops+5*size>cap){done=false;break}ops+=5*size;size*=5}
  // Symbolic tensor size and rank, not materialized. Local AND-graph factor verified directly.
  let t=Array.from({length:8},(_,z)=>Number(((z>>2)&1)===((z&1)&((z>>1)&1))));
  let C=algebra(17n).fft(t);check(C.filter(Boolean).length===5&&C.slice(0,4).filter(Boolean).length===1,"AND");
  trap.push({k,expandedTerms:(5n**BigInt(k)).toString(),rowRank:(2n**BigInt(k)).toString(),simulatedExpansionOps:ops,underCap:done,earlyProjectionTermVisits:5*k});
 }
 return {words,a,b,scales:[3,6,12,24,48].map(source),random:{checks,smallPrimeFalse},trap,cap};
}
console.log(JSON.stringify(audit(),null,2));
