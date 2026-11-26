/* P4SW09 independently executable exact local C54/phase count audit. Node.js 18+. */
function audit(C){
 const assert=(x,m)=>{if(!x)throw Error(m)}, bit=i=>1n<<BigInt(i);
 const n=C.length/3,m=C.length,R=Array.from({length:4*n},()=>[]);C.forEach((t,j)=>t.forEach((v,c)=>R[c*n+v].push(j)));assert(R.every(a=>a.length===3),"degree");
 function local(holes){
   let cut=holes.reduce((s,i)=>s|bit(i),0n),cols=C.map(t=>t.reduce((s,v,c)=>s|bit(c*n+v),0n)&~cut),ports=holes.flatMap(i=>R[i]),P=ports.reduce((s,j)=>s|bit(j),0n),words=[];
   function rec(left,s){if(!left){words.push(s);return}let best=null;for(let i=0;i<R.length;i++)if(left&bit(i)){let a=R[i].filter(j=>(cols[j]&left)===cols[j]);if(best===null||a.length<best.length)best=a;if(!best.length)break}for(let j of best)rec(left^cols[j],s|bit(j))}
   rec((bit(4*n)-1n)&~cut,0n);return{ports,P,words};
 }
 const a=local([0,6]),b=local([0]);const pairPrev=[1,19],pairExt=[2,20],pairNext=[0,18],singlePrev=[1],singleExt=[2],singleNext=[18];
 function mask(A){return A.reduce((s,i)=>s|bit(i),0n)}
 function count(T,A,zero){return T.words.filter(w=>(w&T.P)===mask(A)&&!(w&mask(zero))).length}
 const weights={p:[count(a,pairExt,pairPrev),count(a,pairNext,pairPrev)],s:[count(b,singleExt,singlePrev),count(b,singleNext,singlePrev)]};
 assert(JSON.stringify(weights)==='{"p":[11,5],"s":[23,5]}',"actual local count");
 function graph(k){
  const dirs=[[0,1],[1,0],[0,-1],[-1,0]],key=(i,j,u,v)=>[i,j,u,v].join(","),groups=[],parent=new Map(),degree=new Map();
  function root(x){while(parent.get(x)!==x)x=parent.get(x);return x}
  function unite(a,b){parent.set(root(b),root(a));degree.set(a,(degree.get(a)||0)+1);degree.set(b,(degree.get(b)||0)+1)}
  for(let i=0;i<k;i++)for(let j=0;j<k;j++){let A=dirs.map(([u,v])=>[i+u,j+v]).filter(([u,v])=>u>=0&&v>=0&&u<k&&v<k).map(([u,v])=>key(i,j,u,v));for(let a of A)parent.set(a,a);for(let t=0;t<A.length;t+=2)groups.push(A.slice(t,t+2))}
  for(let a of parent.keys()){let [i,j,u,v]=a.split(",").map(Number),b=key(u,v,i,j);if(a<b)unite(a,b)}
  for(let g of groups)if(g.length===2)unite(...g);
  assert([...degree.values()].every(d=>d===1||d===2),"paths");
  let C=new Map();for(let g of groups){let r=root(g[0]);if(!C.has(r))C.set(r,[0,0]);C.get(r)[g.length===2?0:1]++}
  let W=[...C.values()].sort((a,b)=>a[0]-b[0]);assert(W.filter(x=>x[1]===2).length===2*(k-2),"boundary paths");assert(W.every(([p,s])=>p>=1&&(s===0||s===2)),"visible phase");let Z=1n;
  for(let [p,s] of W)Z*=BigInt(weights.p[0])**BigInt(p)*BigInt(weights.s[0])**BigInt(s)+BigInt(weights.p[1])**BigInt(p)*BigInt(weights.s[1])**BigInt(s);
  return{k,slots:parent.size,paired:groups.filter(g=>g.length===2).length,components:W.length,paths:2*(k-2),profile:W,count:Z.toString(),bits:Z.toString(2).length};
 }
 const scales=Array.from({length:19},(_,i)=>graph(i+2));
 const expected={2:"15266",3:"7414564363210816",4:"54163529956843163837348824857856",6:"8970005677237719565232358943718053796657388525642185013955548599144082374656"};
 for(let s of scales)if(expected[s.k])assert(s.count===expected[s.k],"Python independent exact count");
 let maj=0;for(let t=1;t<256;t++){let A=Array.from({length:8},(_,i)=>i).filter(i=>t>>i&1),S=new Set(A),closed=A.every(a=>A.every(b=>A.every(c=>S.has((a&b)|(a&c)|(b&c))))),hull=Array.from({length:8},(_,i)=>i).filter(x=>[1,2,4,3,5,6].every(q=>A.some(a=>(a&q)===(x&q))));assert(closed===(hull.length===A.length),"majority hull");if(closed)maj++}
 return{weights,scales,majority_nonempty_arity3:255,majority_closed:maj,raw_projection_counterexample:{states:[1,2,4],majority:0},limitations:"Independent local C54 exact enumeration and phase quotient counts. Native planar embedding, all-six projection closure, GF2/GF3, actual matching and source lifts tested in separate Python archive."};
}
const C=[[6,0,5,1],[0,1,0,1],[0,1,1,0],[1,0,0,1],[1,0,1,0],[1,1,0,0],[2,2,3,3],[2,3,2,3],[2,4,3,2],[3,2,2,3],[3,2,3,2],[3,3,2,13],[4,3,5,5],[4,5,4,5],[4,5,5,4],[5,4,4,5],[5,4,11,4],[5,5,4,4],[0,12,1,7],[6,7,6,7],[6,7,7,6],[7,12,6,7],[7,6,7,6],[7,7,6,6],[8,8,9,9],[8,9,8,9],[8,10,9,8],[9,8,8,9],[9,8,9,8],[9,6,8,8],[10,9,11,11],[10,11,10,11],[10,11,11,10],[11,10,10,11],[11,10,7,10],[11,11,10,10],[12,9,17,2],[12,13,12,13],[12,13,17,12],[13,12,12,13],[13,6,13,12],[13,13,12,12],[14,14,15,15],[14,15,14,15],[14,16,15,14],[15,14,14,15],[15,14,15,14],[15,15,14,14],[16,15,13,17],[16,17,16,17],[16,17,17,16],[17,16,16,17],[17,16,13,16],[17,17,16,16]];
console.log(JSON.stringify(audit(C),null,2));
