function audit(){
const assert=(x,m="assertion")=>{if(!x)throw Error(m)};
const counts={planarity:0,parity_pairs:0,circuit_components:0,negative_repairs:0,forced_probes:0,matching_calls:0,small_reference_jobs:0};
const pop=x=>{let c=0;while(x){x&=x-1n;c++}return c};
const bit=i=>1n<<BigInt(i);
const has=(x,i)=>!!(x&bit(i));
function make(lengths,links){
  const n=lengths.reduce((a,b)=>a+b,0), off=[];let p=0;
  for(const L of lengths){off.push(p);p+=L}
  const R=Array.from({length:2*n},()=>[]);
  // Prism layers: top variables at even i, bottom variables at odd i.
  for(let k=0;k<lengths.length;k++){
    const L=lengths[k],o=off[k];
    const node=(i,layer)=>o+((i+layer)%2===0?0:n)+i;
    for(let i=0;i<L;i++)for(let layer=0;layer<2;layer++){
      const prev=node((i+L-1)%L,layer),next=node((i+1)%L,layer),rung=node(i,1-layer);
      R[node(i,layer)]=layer===0?[prev,next,rung]:[next,prev,rung];
    }
  }
  function replace(u,v,w){let i=R[u].indexOf(v);assert(i>=0);R[u][i]=w}
  for(const [a,vi,ci,b,vj,cj] of links){
    const x=off[a]+vi,c=n+off[a]+ci,y=off[b]+vj,d=n+off[b]+cj;
    replace(x,c,d);replace(c,x,y);replace(y,d,c);replace(d,y,x);
  }
  for(let u=0;u<2*n;u++){assert(R[u].length===3&&new Set(R[u]).size===3);for(const v of R[u])assert(R[v].includes(u)&&(u<n)!==(v<n))}
  const seen=new Set([0]), q=[0];for(let i=0;i<q.length;i++)for(const v of R[q[i]])if(!seen.has(v)){seen.add(v);q.push(v)}
  assert(seen.size===2*n,"connected");
  let faces=0;const darts=new Set();
  for(let u=0;u<2*n;u++)for(const v of R[u]){
    let a=u,b=v,key=a+","+b;if(darts.has(key))continue;faces++;
    while(!darts.has(key)){darts.add(key);const rr=R[b];const c=rr[(rr.indexOf(a)+1)%3];a=b;b=c;key=a+","+b}
    assert(a===u&&b===v,"face permutation");
  }
  assert(2*n-3*n+faces===2,"rotation genus");counts.planarity++;
  return {n,off,lengths,R,C:R.slice(n).map(x=>x.slice())};
}
function chain(k){return make(Array(k).fill(6),Array.from({length:k-1},(_,i)=>[i,3,3,i+1,0,0]))}
function neighbor(k,sat){return make([4,8,...Array(k).fill(6)],[[0,sat?1:0,0,1,sat?1:0,0],...Array.from({length:k},(_,i)=>i===0?[0,2,2,2,0,0]:[i+1,3,3,i+2,0,0])])}
const masks=F=>F.C.map(c=>c.reduce((s,i)=>s|bit(i),0n));
function defect(F,x){let d=0;for(const c of F.C){const t=c.filter(i=>has(x,i)).length;assert(t===1||t===3,"not parity");d+=t===3?1:0}assert(3*pop(x)===F.n+2*d);return d}
const model=(F,x)=>F.C.every(c=>c.filter(i=>has(x,i)).length===1);
function chart(F,pins=new Map(),rhs=1){
  const n=F.n, b=bit(n), m=b-1n;
  const rows=masks(F).map(x=>x|(rhs?b:0n));for(const [i,t] of pins)rows.push(bit(i)|(t?b:0n));
  let k=0;const piv=[];
  for(let j=0;j<n;j++){let h=k;while(h<rows.length&&!has(rows[h],j))h++;if(h===rows.length)continue;
    [rows[k],rows[h]]=[rows[h],rows[k]];for(let i=0;i<rows.length;i++)if(i!==k&&has(rows[i],j))rows[i]^=rows[k];piv.push(j);k++}
  if(rows.slice(k).some(x=>x===b))return null;
  let a=0n;for(let i=0;i<k;i++)if(rows[i]&b)a|=bit(piv[i]);
  const B=[];for(let j=0;j<n;j++)if(!piv.includes(j)){let v=bit(j);for(let i=0;i<k;i++)if(has(rows[i],j))v|=bit(piv[i]);B.push(v)}
  return {a,B};
}
function words(H){if(!H)return [];let W=[H.a];for(const v of H.B)W=W.concat(W.map(x=>x^v));return W}
function comps(F,u){
  const A=Array.from({length:F.n},()=>[]);for(const c of F.C){const s=c.filter(i=>has(u,i));assert(s.length===0||s.length===2);if(s.length){A[s[0]].push(s[1]);A[s[1]].push(s[0])}}
  const C=[];let seen=0n;
  for(let i=0;i<F.n;i++)if(has(u,i)&&!has(seen,i)){let v=0n;const Q=[i];seen|=bit(i);for(let j=0;j<Q.length;j++){const x=Q[j];v|=bit(x);assert(A[x].length===3);for(const y of A[x])if(!has(seen,y)){seen|=bit(y);Q.push(y)}}C.push(v)}
  assert(seen===u);return C;
}
function matching(F,P){
  counts.matching_calls++;
  const cs=F.C.filter(c=>!c.some(i=>P.get(i)===1));
  const owner=new Map();
  function dfs(j,seen){for(const i of cs[j])if(P.get(i)!==0)for(let k=0;k<3;k++){
    const v=3*i+k;if(seen.has(v))continue;seen.add(v);
    if(!owner.has(v)||dfs(owner.get(v),seen)){owner.set(v,j);return true}
  }return false}
  return cs.every((_,j)=>dfs(j,new Set()));
}
function basic(F,P){
  P=new Map(P);if(F.n%3)return null;
  const put=(i,v)=>{if(P.has(i))return P.get(i)===v;P.set(i,v);return true};
  for(;;){const old=P.size;
    for(const c of F.C){const ones=c.filter(i=>P.get(i)===1),free=c.filter(i=>!P.has(i));
      if(ones.length>1||(!ones.length&&!free.length))return null;
      if(ones.length){for(const i of free)if(!put(i,0))return null}
      else if(free.length===1&&!put(free[0],1))return null;
    }
    const H=chart(F,P);if(!H||!matching(F,P))return null;
    let free=0n;for(const v of H.B)free|=v;
    for(let i=0;i<F.n;i++)if(!has(free,i)&&!put(i,has(H.a,i)?1:0))return null;
    if(P.size===old)return P;
  }
}
function closure(F,P=new Map()){
  P=basic(F,P);if(!P)return null;
  for(;;){let changed=false;
    for(let i=0;i<F.n;i++)if(!P.has(i)){
      const options=[0,1].map(t=>{counts.forced_probes++;return basic(F,new Map([...P,[i,t]]))});
      if(!options[0]&&!options[1])return null;
      if(!options[0]||!options[1]){P=options[0]||options[1];changed=true;break}
    }if(!changed)return P;
  }
}
function checkPairs(F){
 const W=words(chart(F));const S=W.filter(x=>model(F,x));
 const P=closure(F);
 assert(P!==null||!S.length);if(P)for(const x of S)for(const [i,t] of P)assert(has(x,i)===!!t);
 counts.small_reference_jobs++;
 for(const a of W)for(const b of W){const D=defect(F,a),E=defect(F,b),C=comps(F,a^b);let sum=0;
   for(const v of C){const gain=D-defect(F,a^v);assert(gain%3===0);sum+=gain;counts.circuit_components++}
   assert(sum===D-E);if(E<D)assert(C.some(v=>defect(F,a^v)<D));counts.parity_pairs++;
 }
 return {n:F.n,nullity:chart(F).B.length,models:S.length,closure:P===null?"NO":P.size};
}
const small=[chain(1),chain(2),chain(3),neighbor(0,true),neighbor(0,false),neighbor(1,true),neighbor(1,false)].map(checkPairs);
const scaling=[];
for(const k of [1,2,4,8,16,32,64]){
 const F=chain(k),all=bit(F.n)-1n;
 const fixed=closure(F);assert(fixed!==null&&fixed.size===0);
 const assignments=k<=8?Array.from({length:2**k},(_,i)=>BigInt(i)):[0n,1n,(1n<<BigInt(k))-1n,((1n<<BigInt(k))-1n)/3n];
 const unique=new Set();
 for(const a of assignments){
   let x=0n;for(let j=0;j<k;j++){const phase=has(a,j)?1:2;for(let i=phase;i<6;i+=3)x|=bit(6*j+i)}
   assert(model(F,x));const v=all^x;assert(comps(F,v).length===1);assert(pop(v)===4*k&&defect(F,x)===0);unique.add(v.toString());counts.negative_repairs++;
 }assert(unique.size===assignments.length||k===1);
 // Affine hull certificate: XOR three uniform phase source witnesses = all ones.
 let s=0n;for(let p=0;p<3;p++){let x=0n;for(let i=p;i<F.n;i+=3)x|=bit(i);assert(model(F,x));s^=x}assert(s===all);
 scaling.push({k,n:F.n,repair_lower_bound:(1n<<BigInt(k)).toString(),checked:assignments.length,closure_pins:fixed.size});
}
const neighbors=[];
for(const k of [0,1,4,16]){
 for(const sat of [true,false]){
 const F=neighbor(k,sat),P=closure(F);const H=chart(F);assert(H);
 // For these sizes the parity chart is at most 18-dimensional. Use explicit witness for SAT; cut proof for NO.
 if(sat){let x=bit(2);for(let i=1;i<8;i+=3)x|=bit(4+i);for(let j=0;j<k;j++){const p=j===0?0:1;/* use actual port bit from previous block: x2=1 => phase0, next x3=1 likewise */for(let i=0;i<6;i+=3)x|=bit(12+6*j+i)}assert(model(F,x));assert(P!==null);for(const [i,t] of P)assert(has(x,i)===!!t)}
 if(k<=4){const yes=words(H).some(x=>model(F,x));assert(yes===sat)}
 neighbors.push({k,n:F.n,expected:sat?"SAT":"UNSAT",closure:P===null?"NO":P.size,nullity:H.B.length,enumerated:k<=4});
 }}
return {small,scaling,neighbors,counts};
}
console.log(JSON.stringify(audit(),null,2));
