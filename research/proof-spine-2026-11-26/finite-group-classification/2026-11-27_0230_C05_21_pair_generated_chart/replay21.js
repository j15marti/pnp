// Independent row-elimination and explicit Tutte barrier replay; run with node replay21.js.
function audit(){
 const core=[[2,2,0],[0,2,2],[1,2,0],[0,2,1],[0,0,1],[2,2,1],[1,1,0],[2,1,1],[1,0,2]];
 const ck=(v,msg)=>{if(!v)throw Error(msg)};
 const bit=i=>1n<<BigInt(i);
 const has=(x,i)=>(x&bit(i))!==0n;
 const parity=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
 const basis=xs=>{const B=new Map();for(let x of xs){while(x){let j=x.toString(2).length-1;if(B.has(j))x^=B.get(j);else{B.set(j,x);break}}}return B};
 const rem=(B,x)=>{for(const j of [...B.keys()].sort((a,b)=>b-a))if(has(x,j))x^=B.get(j);return x};
 function affineRows(rows,m){
  let r=0;const piv=[];
  for(let j=0;j<m;j++){
   let i=r;while(i<rows.length&&!has(rows[i],j))i++;if(i===rows.length)continue;
   [rows[r],rows[i]]=[rows[i],rows[r]];
   for(let t=0;t<rows.length;t++)if(t!==r&&has(rows[t],j))rows[t]^=rows[r];
   piv.push(j);r++;
  }
  for(let i=r;i<rows.length;i++)ck(!has(rows[i],m),"inconsistent");
  let a=0n;for(let i=0;i<r;i++)if(has(rows[i],m))a|=bit(piv[i]);
  const P=new Set(piv),K=[];
  for(let j=0;j<m;j++)if(!P.has(j)){let z=bit(j);for(let i=0;i<r;i++)if(has(rows[i],j))z|=bit(piv[i]);K.push(z)}
  return [a,K];
 }
 let exact=0;
 for(let m=0;m<512;m++){
  let occ=Array(9).fill(0);
  for(let j=0;j<9;j++)if((m>>j)&1)for(let c=0;c<3;c++)occ[c*3+core[j][c]]++;
  if(occ.every(z=>z===1))exact++;
 }
 ck(exact===0,"core SAT");
 const out=[];
 for(const k of [0,1,2,4,8,16,32,64,128]){
  const T=new Map(core.map((t,i)=>[i,[...t]]));
  for(let j=0;j<k;j++)for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let z=0;z<2;z++)T.set(100+8*j+4*x+2*y+z,[3+2*j+x,3+2*j+y,3+2*j+z]);
  for(let j=0;j<k;j++){const b=j%2?7:0,u=j===0?0:100+8*(j-1)+b,v=100+8*j+b;[T.get(u)[2],T.get(v)[2]]=[T.get(v)[2],T.get(u)[2]]}
  const n=3+2*k,I=new Set([2,3,4,5,...Array.from({length:k},(_,j)=>101+8*j)]),ids=[...T.keys()],m=ids.length;
  const rows=Array(3*n).fill(bit(m));
  for(let j=0;j<m;j++)for(let c=0;c<3;c++)rows[c*n+T.get(ids[j])[c]]|=bit(j);
  const [a,K]=affineRows(rows,m);
  function project(x){let p=0n;for(let j=0;j<m;j++)if(I.has(ids[j])&&has(x,j)){const t=T.get(ids[j]);p^=bit(t[0])^bit(n+t[1])}return p}
  const A=project(a)^((1n<<BigInt(2*n))-1n),B=basis(K.map(project));
  const classes=[[[0,n],1],[[1,2],1],[[n+1],1],[[n+2],1]];
  for(let j=0;j<k;j++){let x=3+2*j,y=n+x;classes.push([[x,y],0],[[x+1],1],[[y+1],1])}
  let base=0n;const dirs=[];for(const [p,b] of classes){if(b)base^=bit(p[0]);if(p.length===2)dirs.push(bit(p[0])^bit(p[1]))}
  ck(B.size===k+2&&B.size===dirs.length,"chart rank");
  ck(rem(B,base^A)===0n&&dirs.every(x=>rem(B,x)===0n),"chart equality");
  const adj=Array.from({length:2*n},()=>new Set());
  function edge(i,j){adj[i].add(j);adj[j].add(i)}
  for(const id of I){const t=T.get(id);edge(t[0],n+t[1])}
  for(const [p,b] of classes){if(p.length===2)edge(p[0],p[1]);if(b){const d=adj.length;adj.push(new Set());for(const i of p)edge(d,i)}}
  const deleted=n+2,seen=new Set([deleted]),odd=[];
  for(let v=0;v<adj.length;v++)if(!seen.has(v)){const S=[v];seen.add(v);for(let j=0;j<S.length;j++)for(const w of adj[S[j]])if(!seen.has(w)){seen.add(w);S.push(w)}if(S.length%2)odd.push(S.sort((x,y)=>x-y))}
  ck(odd.length===3,"Tutte barrier");
  out.push({k,tuples:m,owners_per_color:n,rank:B.size,quotient:0,odd_components:odd,barrier:[deleted]});
 }
 return {core_subsets:512,core_exact_covers:exact,family:out};
}
console.log(JSON.stringify(audit(), null, 2));
