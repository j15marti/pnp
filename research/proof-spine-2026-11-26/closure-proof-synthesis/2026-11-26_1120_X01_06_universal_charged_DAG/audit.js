console.log(JSON.stringify((function audit(){
 let checks=0,fullAssignments=0,guardedPrefixes=0,sourceAssignments=0,projectionChecks=0,diagonalPairs=0,bruteJobs=0,bruteAssignments=0;
 const ok=(x,msg="")=>{if(!x)throw Error(`check ${checks} ${msg}`);checks++};
 const lit=(l,x)=>Boolean(x[Math.abs(l)])===(l>0);
 const sat=(C,x)=>C.every(c=>c.some(l=>lit(l,x)));
 function assignment(z,n){return [0,...Array.from({length:n},(_,i)=>(z>>(n-1-i))&1)]}
 const gamma=x=>{let b=x.toString(2);return "0".repeat(b.length-1)+b};
 const enc=(F,n)=>{let w=Math.ceil(Math.log2(n+1));return "1".repeat(n)+"0"+gamma(F.length+1)+F.map(c=>c.map(l=>(l>0?"1":"0")+Math.abs(l).toString(2).padStart(w,"0")).join("")).join("")};
 const good=(C,n)=>C.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3&&c.every(l=>Math.abs(l)>0&&Math.abs(l)<=n));
 function gate(H,n){let p=1,u=n+H.length+2,v=u+1,rows=[];const remap=l=>Math.sign(l)*(Math.abs(l)+1);
  H.forEach((c,j)=>{const [a,b,c0]=c.map(remap),y=n+j+2;rows.push([-p,a,y],[-y,b,c0])});
  rows.push([p,u,v],[p,u,-v],[p,-u,v],[p,-u,-v]);
  return{C:rows,n:v,p,u,v};
 }
 const all=Array.from({length:8},(_,i)=>[1,2,3].map((v,j)=>i>>j&1?v:-v));
 let gateSat=0,gateUnsat=0,lexChecks=0,guardedNeighbors=[];
 for(let mask=0;mask<256;mask++){
  const H=all.filter((_,i)=>(mask>>i)&1),G=gate(H,3),{C,n,p,u,v}=G;
  ok(n===H.length+6&&C.length===2*H.length+4&&good(C,n));
  let first=Array(C.length+1).fill(-1),proj=new Set(),finalCount=0,prevCount=0,sourceCount=0;
  for(let z=0;z<2**n;z++){
   const x=assignment(z,n);fullAssignments++;
   let j=0;while(j<C.length&&C[j].some(l=>lit(l,x)))j++;
   for(let i=0;i<=j;i++)if(first[i]===-1)first[i]=z;
   if(j>=C.length-1)prevCount++;
   if(j===C.length){finalCount++;ok(x[p]===1);ok(sat(H,[0,x[2],x[3],x[4]]));proj.add(4*x[2]+2*x[3]+x[4]);projectionChecks++}
  }
  for(let z=0;z<8;z++){
   const x=assignment(z,3),expected=sat(H,x),pre=Array(n+1).fill(0);
   for(let j=1;j<=3;j++)pre[j+1]=x[j];pre[u]=pre[v]=1;
   ok(sat(C.slice(0,-1),pre)&&!sat(C,pre));sourceAssignments++;
   const lift=pre.slice();lift[p]=1;lift[u]=lift[v]=0;
   H.forEach((c,j)=>{lift[5+j]=lit(c[0],x)?0:1});
   ok(sat(C,lift)===expected);ok(proj.has(z)===expected);sourceCount+=+expected;
  }
  for(let j=0;j<C.length;j++){
   const a=assignment(first[j],n),h=Math.max(0,j-2*H.length);
   const expected=Array(n+1).fill(0);expected[u]=h>=2?1:0;expected[v]=h===1||h>=3?1:0;
   ok(first[j]>=0&&a.every((b,i)=>b===expected[i]));lexChecks++;guardedPrefixes++;
  }
  ok((finalCount>0)===(sourceCount>0));ok(prevCount>=8);
  if(finalCount){gateSat++;ok(first.at(-1)>=0)}else{gateUnsat++;ok(first.at(-1)===-1)}
  if(mask===255||mask===254)guardedNeighbors.push({mask,sourceClauses:H.length,encodedBits:enc(C,n).length,penultimateModels:prevCount,finalModels:finalCount,originalModels:sourceCount});
 }
 function pins(x,a,b,val){return [[val?x:-x,a,b],[val?x:-x,a,-b],[val?x:-x,-a,b],[val?x:-x,-a,-b]]}
 function diag(u,v){const k=u.length,L=[],M=[],R=[];for(let i=0;i<k;i++){
  const x=i+1,la=k+2*i+1,ra=3*k+2*i+1,d=5*k+3*i+1;
  L.push(...pins(x,la,la+1,u[i]));M.push([d,d+1,d+2]);R.push(...pins(x,ra,ra+1,v[i]));
 }return {L,M,R,C:[...L,...M,...R],n:8*k}}
 function decode(G){const {C,n}=G;const k=n/8,seen=new Map();
  for(let i=0;i<k;i++)for(let t of [i*4,5*k+i*4]){let row=C.slice(t,t+4);ok(row.every(c=>c[0]===row[0][0]));ok(new Set(row.map(c=>c.slice(1).join(","))).size===4);let l=row[0][0];if(seen.has(Math.abs(l))&&seen.get(Math.abs(l))!==+(l>0))return null;seen.set(Math.abs(l),+(l>0))}
  const x=Array(n+1).fill(0);for(const [v,b] of seen)x[v]=b;for(let i=0;i<k;i++)x[5*k+3*i+1]=1;ok(sat(C,x));return x;
 }
 let diagYes=0,diagNo=0;const scales=[];
 for(let k=1;k<=5;k++){
  let left=new Map(),right=new Map(),mid=null,N=null;
  for(let a=0;a<2**k;a++)for(let b=0;b<2**k;b++){
   let u=assignment(a,k).slice(1),v=assignment(b,k).slice(1),G=diag(u,v);
   ok(good(G.C,G.n)&&new Set(G.C.map(c=>c.join(","))).size===G.C.length);
   const L=enc(G.L,G.n),M=enc(G.M,G.n),R=enc(G.R,G.n),full=enc(G.C,G.n);
   if(left.has(a))ok(left.get(a)===L);else left.set(a,L);if(right.has(b))ok(right.get(b)===R);else right.set(b,R);if(mid===null){mid=M;N=full.length}ok(mid===M&&N===full.length);
   const q=decode(G),expect=a===b;ok((q!==null)===expect);diagonalPairs++;if(expect)diagYes++;else diagNo++;
   if(k<=2){let found=false;for(let z=0;z<2**G.n;z++){bruteAssignments++;if(sat(G.C,assignment(z,G.n))){found=true;break}}bruteJobs++;ok(found===expect)}
  }
  ok(new Set(left.values()).size===2**k&&new Set(right.values()).size===2**k)
 }
 for(let k of [8,32,128,512,2048]){
  const u=Array.from({length:k},(_,i)=>+(i%3===0)),v=u.slice();v[k-1]^=1;const A=diag(u,u),B=diag(u,v);
  ok(good(A.C,A.n)&&good(B.C,B.n));ok(decode(A)!==null&&decode(B)===null);
  ok(enc(A.C,A.n).length===enc(B.C,B.n).length);
  const w=Math.ceil(Math.log2(A.n+1)),N=enc(A.C,A.n).length,D=k*3*(1+w);
  scales.push({k,variables:A.n,clauses:A.C.length,encodedBits:N,commonGapBits:D,entropyBits:k});
 }
 let budgetProfiles=0,budgetTests=0,maxChargedTrials=0;
 for(let s=0;s<128;s++){
  const times=Array.from({length:511},(_,i)=>((i*31+s*17)%11===0)?Infinity:1+((i*i*13+s*73+i*s*17)%150));
  const length=i=>Math.floor(Math.log2(i+1));
  const best=Math.min(...times.map((t,i)=>2**length(i)*(t+1)));
  for(const B of [1,2,3,7,16,31,64,129,256,511,1024,4096,8192,32768]){
   let found=false,paid=0,trials=0;for(let i=0;i<times.length;i++){const l=length(i),T=Math.floor(B/2**l)-1;if(T<0)continue;trials++;paid+=Math.min(T, times[i]);if(times[i]<=T)found=true}
   ok(found===(best<=B));ok(paid<=(Math.floor(Math.log2(B))+1)*B);budgetTests++;maxChargedTrials=Math.max(maxChargedTrials,trials)
  }budgetProfiles++;
 }
 return {checks,gateFormulas:256,gateSat,gateUnsat,fullAssignments,sourceAssignments,projectionChecks,guardedPrefixes,lexChecks,guardedNeighbors,diagonalPairs,diagYes,diagNo,bruteJobs,bruteAssignments,scales,budgetProfiles,budgetTests,maxChargedTrials}
})(),null,2));
