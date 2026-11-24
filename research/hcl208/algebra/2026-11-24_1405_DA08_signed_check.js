"use strict";
function run(){
 const R={seed:9042026,cases:0,sat:0,unsat:0,assertions:0,closurePasses:0,forcedPins:0,refWords:0,dpPairs:0,dpAssignments:0,scales:[]};let seed=R.seed;
 function rng(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296}
 function check(a){R.assertions++;if(!a)throw Error("assertion "+R.assertions)}
 function parity(x){let p=0;while(x){p^=1;x&=x-1n}return p}
 // Chart: a_v = row_v dot z XOR const_v. q is required b parity if a_u XOR a_v=p.
 function solve(n,d,rows,cs,edges){
  let pins=[];
  function reduce(row,rhs){for(const [p,a,b] of pins)if(row&p){row^=a;rhs^=b}return [row,rhs]}
  function pin(row,b){[row,b]=reduce(row,b);if(!row)return !b;let p=row&-row;pins.push([p,row,b]);pins.sort((a,b)=>a[0]<b[0]?-1:1);R.forcedPins++;return true}
  let opt,root,offset,nr;
  while(true){
   R.closurePasses++;
   const parent=Array.from({length:n},(_,i)=>i),pot=Array(n).fill(0);
   function find(v){let a=0;while(parent[v]!==v){a^=pot[v];v=parent[v]}return [v,a]}
   function join(u,v,q){const [a,x]=find(u),[b,y]=find(v);if(a===b)return (x^y)===q;parent[b]=a;pot[b]=q^x^y;return true}
   opt=[];
   for(const [u,v,p,q] of edges){const [a,h]=reduce(rows[u]^rows[v],p^cs[u]^cs[v]);if(!a){if(h===0&&!join(u,v,q))return null}else opt.push([u,v,a,h,q])}
   let changed=false;for(const [u,v,a,h,q] of opt){const [r,x]=find(u),[s,y]=find(v);if(r===s&&(x^y)!==q){if(!pin(a,h^1))return null;changed=true;break}}
   if(changed)continue;
   const roots=new Map();root=[];offset=[];for(let i=0;i<n;i++){const [v,b]=find(i);if(!roots.has(v))roots.set(v,roots.size);root.push(roots.get(v));offset.push(b)}nr=roots.size;
   opt=opt.filter(([u,v])=>root[u]!==root[v]).map(([u,v,a,h,q])=>[root[u],root[v],a,h,q^offset[u]^offset[v]]);
   break;
  }
  // Each optional row is nonzero. Build a basis of dependencies on the optional bits.
  const bases=new Map(),rels=[];
  for(let i=0;i<opt.length;i++){let a=opt[i][2],c=1n<<BigInt(i);while(a){let p=a&-a;if(!bases.has(p)){bases.set(p,[a,c]);break}const [b,f]=bases.get(p);a^=b;c^=f}if(!a)rels.push(c)}
  const delta=rels.length;if(delta>12)return {unknown:true,delta};
  const labels=opt.map((_,i)=>rels.reduce((s,r,j)=>s+((r>>BigInt(i)&1n)?2**j:0),0));
  // Spanning forest; one endpoint per nonforest edge is a feedback set.
  const parent=Array.from({length:nr},(_,i)=>i),find=v=>{while(parent[v]!==v)v=parent[v];return v};
  const K=new Set();let cycles=0;for(const [u,v] of opt){const a=find(u),b=find(v);if(a===b){K.add(u);cycles++}else parent[b]=a}
  check(cycles<=delta);
  const F=[...K],adj=Array.from({length:nr},()=>[]);for(let i=0;i<opt.length;i++){let [u,v]=opt[i];adj[u].push([v,i]);adj[v].push([u,i])}
  function merge(A,B){let C=new Map();for(const [a,x] of A)for(const [b,y] of B){R.dpPairs++;if(!C.has(a^b))C.set(a^b,x.concat(y))}return C}
  function edge(i,a,b){let e=opt[i],ys=(a^b)===e[4]?[0,1]:[e[3]^1];let M=new Map();for(const y of ys)M.set(y?labels[i]:0,[[i,y]]);return M}
  for(let mask=0;mask<(1<<F.length);mask++){
   R.dpAssignments++;
   const fixed=new Map(F.map((v,i)=>[v,mask>>i&1])),seen=new Set(F);let M=new Map([[0,[]]]);
   for(let i=0;i<opt.length;i++){const [u,v]=opt[i];if(fixed.has(u)&&fixed.has(v))M=merge(M,edge(i,fixed.get(u),fixed.get(v)))}
   function tree(v,p){
    seen.add(v);
    let A=[new Map([[0,[[~v,0]]]]),new Map([[0,[[~v,1]]]])];
    for(const [w,i] of adj[v]){
     if(fixed.has(w)){for(let b=0;b<2;b++)A[b]=merge(A[b],edge(i,b,fixed.get(w)));continue}
     if(w===p)continue;check(!seen.has(w));let B=tree(w,v);
     for(let b=0;b<2;b++){let C=new Map();for(let c=0;c<2;c++)for(const [s,x] of merge(B[c],edge(i,b,c)))if(!C.has(s))C.set(s,x);A[b]=merge(A[b],C)}
    }return A
   }
   for(let v=0;v<nr;v++)if(!seen.has(v)){const [A,B]=tree(v,-1);for(const [s,x] of B)if(!A.has(s))A.set(s,x);M=merge(M,A)}
   if(M.has(0)){
    let bv=Array(nr),ys=Array(opt.length);for(const [v,b] of fixed)bv[v]=b;
    for(const [i,y] of M.get(0)){if(i<0)bv[~i]=y;else ys[i]=y}
    // All retained guards and selected observations are affine equations. Solve by the same pin basis.
    for(let i=0;i<opt.length;i++)check(pin(opt[i][2],ys[i]));
    let z=0n;for(let i=pins.length-1;i>=0;i--){const [p,a,b]=pins[i];if(parity(a&z)!==b)z^=p}
    let b=offset.map((x,i)=>x^bv[root[i]]),a=rows.map((r,i)=>parity(r&z)^cs[i]);
    check(edges.every(([u,v,p,q])=>(a[u]^a[v])!==p||(b[u]^b[v])===q));
    return {a,b,delta,cycles};
   }
  }
  return null
 }
 function brute(n,d,rows,cs,edges){
  for(let z=0;z<(1<<d);z++){const a=rows.map((r,i)=>parity(r&BigInt(z))^cs[i]);for(let b=0;b<(1<<n);b++){R.refWords++;if(edges.every(([u,v,p,q])=>(a[u]^a[v])!==p||(((b>>u)^(b>>v))&1)===q))return true}}
  return false
 }
 function test(n,d,rows,cs,e,label,scale=false){
  let x=solve(n,d,rows,cs,e);check(!x?.unknown);check(!!x===label);R.cases++;R[label?"sat":"unsat"]++;
  if(scale)R.scales.push({n,d,label,delta:x?.delta??null,cycles:x?.cycles??null});
 }
 for(let t=0;t<400;t++){
  const n=3+Math.floor(rng()*5),d=1+Math.floor(rng()*5),rows=Array.from({length:n},()=>BigInt(Math.floor(rng()*(1<<d)))),cs=Array.from({length:n},()=>Math.floor(rng()*2)),e=[];
  for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(rng()<.37)e.push([u,v,Math.floor(rng()*2),Math.floor(rng()*2)]);
  test(n,d,rows,cs,e,brute(n,d,rows,cs,e))
 }
 // Opposite-label controls: two mandatory inconsistent edges on a signed cycle vs one flipped parity; plus long free cycle.
 for(const n of [8,32,64,128]){
  const rows=Array.from({length:n},(_,i)=>1n<<BigInt(i)),cs=Array(n).fill(0),e=Array.from({length:n},(_,i)=>[i,(i+1)%n,0,i===n-1?1:0]);
  test(n,n,rows,cs,e,true,true);
  const zero=rows.map(()=>0n);test(n,n,zero,cs,e,false,true);
 }
 return R
}
console.log(JSON.stringify(run(),null,2));
