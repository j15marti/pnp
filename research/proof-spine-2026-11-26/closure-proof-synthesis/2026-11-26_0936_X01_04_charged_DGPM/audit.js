console.log(JSON.stringify((function audit(){
 let checks=0,rawNodes=0;const ck=x=>{if(!x)throw Error("check "+checks);checks++};
 const B=[[[0,4],[1,3]],[[0,5,7],[1,3,8],[1,5,6]]]; // edge indices = 3*r+c; corrected below: B2 offdiag [1,3]
 // B3 permutations (0,2,1),(1,0,2),(1,2,0)
 const dom=B, keys=e=>e.join(":");
 const perms=k=>{const out=[];function p(a,b){if(!b.length){out.push(a);return}for(const x of b)p([...a,x],b.filter(y=>y!==x))}p([],Array.from({length:k},(_,i)=>i));return out};
 function formula(k){
  let n=2*k;const F=[],Z=[],ops=[];const fresh=()=>++n;
  function add(C){if(C.length===3)F.push(C);else if(C.length===2){const u=fresh();F.push([...C,u],[...C,-u])}else{const u=fresh(),v=fresh();for(const a of [u,-u])for(const b of [v,-v])F.push([...C,a,b])}}
  for(let i=0;i<k;i++){const a=i+1,b=k+i+1,z=fresh();Z.push(z);ops.push(["xor",z,a,b]);for(let x=0;x<2;x++)for(let y=0;y<2;y++){const bad=1^(x^y);add([x?-a:a,y?-b:b,bad?-z:z])}}
  let r=Z[0];for(let i=1;i<k;i++){const a=r,b=Z[i],z=fresh();ops.push(["or",z,a,b]);add([a,b,-z]);add([-a,z]);add([-b,z]);r=z}add([r]);ck(F.length===9*k-1&&n===6*k-1);return {F,n,ops,r}
 }
 function compile(k,pi,sigma){
  const {F,n,ops,r}=formula(k),types=[],G=[],used=new Set(),O=Array.from({length:n},()=>[]),V=[],C=[],ext=[],mid=[];
  const add=t=>{types.push(t);return types.length-1};
  const link=(a,b,d=mid)=>{ck(!used.has(keys(a))&&!used.has(keys(b))&&a[0]!==b[0]);used.add(keys(a));used.add(keys(b));d.push([a,b])};
  F.forEach((c,i)=>c.forEach((l,j)=>O[Math.abs(l)-1].push([i,j,l])));
  const Q={};
  O.forEach((o,v)=>{const e=v<2*k?add(0):null;ext.push(e);const ks=o.map(()=>add(0));V.push(ks);const chain=e===null?ks:[e,...ks];for(let i=0;i+1<chain.length;i++){const p=(i%2===0)?1:0;link([chain[i],p],[chain[i+1],p])}o.forEach(([i,j,l],t)=>{const p=(l>0?[1,3]:[0,4]).find(p=>!used.has(keys([ks[t],p])));ck(p!==undefined);Q[i+","+j]=[ks[t],p]})});
  F.forEach((c,i)=>{const s=add(1),I=c.map(()=>add(1));C.push([s,I]);I.forEach((t,j)=>{link([s,3*j],[t,0]);link([t,3],Q[i+","+j])})});
  const base=Array.from({length:k},()=>add(0)),L=[],R=[];
  for(let i=0;i<k;i++){link([ext[i],0],[base[pi[i]],0],L);link([ext[k+i],0],[base[sigma[i]],4],R)}
  G.push(...L,...mid,...R);
  ck(types.length===7*F.length+3*k&&G.length===9*F.length-n+4*k);
  const w=Math.ceil(Math.log2(types.length)),bin=(v,d)=>v.toString(2).padStart(d,"0"),gamma=v=>{const b=(v+1).toString(2);return "0".repeat(b.length-1)+b},rec=([a,b])=>[a,b].map(([i,e])=>bin(i,w)+bin(e,4)).join("");
  const head=gamma(types.length)+gamma(G.length)+types.join(""),ls=L.map(rec).join(""),ms=mid.map(rec).join(""),rs=R.map(rec).join("");
  return {F,n,ops,r,types,G,V,C,ext,base,pi,sigma,head,ls,ms,rs,N:head.length+ls.length+ms.length+rs.length}
 }
 const eq=(a,b)=>a.every((x,i)=>x===b[i]);
 const val=(l,x)=>x[Math.abs(l)]^(l<0);
 function lift(D,bits){
  const x=Array(D.n+1).fill(0);for(let i=0;i<bits.length;i++){x[i+1]=bits[D.pi[i]];x[bits.length+i+1]=bits[D.sigma[i]]}
  for(const [op,z,a,b] of D.ops)x[z]=op==="xor"?x[a]^x[b]:x[a]|x[b];
  ck(D.F.every(c=>c.some(l=>val(l,x)))===!!x[D.r]);
  if(!x[D.r])return false;
  const M=[];D.V.forEach((ks,v)=>ks.forEach(t=>M[t]=dom[0][x[v+1]?0:1]));D.ext.forEach((t,v)=>{if(t!==null)M[t]=dom[0][x[v+1]?0:1]});D.base.forEach((t,i)=>M[t]=dom[0][bits[i]?0:1]);
  const hot=j=>dom[1].find(s=>s.includes(3*j));
  D.F.forEach((c,i)=>{const l=c.map(t=>val(t,x)),j=l.indexOf(1),[s,I]=D.C[i];M[s]=hot(j);I.forEach((t,p)=>M[t]=hot(p===j?0:l[p]===0?1:2))});
  ck(M.length===D.types.length&&M.every((s,i)=>dom[D.types[i]].includes(s)));
  ck(D.G.every(([a,b])=>M[a[0]].includes(a[1])===M[b[0]].includes(b[1])));return true
 }
 function raw(D){
  const adj=D.types.map(()=>[]);D.G.forEach(([a,b])=>{adj[a[0]].push([a[1],b[0],b[1]]);adj[b[0]].push([b[1],a[0],a[1]])});
  function go(ds){rawNodes++;let queue=ds.map((_,i)=>i);for(let q=0;q<queue.length;q++){const i=queue[q];for(const [e,j,f] of adj[i]){const d=ds[j].filter(s=>ds[i].some(t=>s.includes(f)===t.includes(e)));if(!d.length)return false;if(d.length<ds[j].length){ds[j]=d;queue.push(j)}}}let v=-1;for(let i=0;i<ds.length;i++)if(ds[i].length>1&&(v<0||ds[i].length<ds[v].length))v=i;if(v<0)return true;for(const s of ds[v]){const t=ds.slice();t[v]=[s];if(go(t))return true}return false}
  return go(D.types.map(t=>dom[t]));
 }
 let pairs=0,assignments=0,yes=0,no=0,rawJobs=0;const sizes=[];
 for(let k=1;k<=4;k++){const P=perms(k);let head=null,mid=null;for(const p of P)for(const q of P){const D=compile(k,p,q);if(head===null){head=D.head;mid=D.ms}ck(head===D.head&&mid===D.ms);let found=false;for(let a=0;a<2**k;a++){const bits=Array.from({length:k},(_,i)=>(a>>i)&1);found=lift(D,bits)||found;assignments++}ck(found===!eq(p,q));if(k<=2){ck(raw(D)===found);rawJobs++}pairs++;if(found)yes++;else no++}}
 for(const k of [8,16,32,64,128,256,512]){const p=Array.from({length:k},(_,i)=>i),q=p.slice();[q[0],q[k-1]]=[q[k-1],q[0]];const X=compile(k,p,p),Y=compile(k,p,q);ck(X.head===Y.head&&X.ms===Y.ms&&X.ls===Y.ls&&X.rs!==Y.rs);const b=Array(k).fill(0);b[0]=1;ck(!lift(X,b)&&lift(Y,b));let H=0;for(let j=1;j<=k;j++)H+=Math.log2(j);sizes.push({k,bits:X.N,common_gap_bits:X.ms.length,entropy_bits:Math.round(H*100)/100,components:X.types.length,guards:X.G.length})}
 return {checks,exhaustivePermutationPairs:pairs,sourceBitAssignments:assignments,yes,no,rawJobs,rawNodes,scales:sizes};
})(),null,2));
