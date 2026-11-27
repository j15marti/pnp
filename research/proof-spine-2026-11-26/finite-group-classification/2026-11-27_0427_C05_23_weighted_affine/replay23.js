// C05-23 independent replay, no dependencies. Run node replay23.js.
const core=[[2,2,0],[0,2,2],[1,2,0],[0,2,1],[0,0,1],[2,2,1],[1,1,0],[2,1,1],[1,0,2]];
const bit=i=>1n<<BigInt(i), has=(x,i)=>Boolean(x&bit(i));
function check(v){if(!v)throw Error("check failed")}
function weight(x){let c=0;while(x){x&=x-1n;c++}return c}
function family(k){
 const T=Array.from({length:k},(_,j)=>core.map(t=>t.map(v=>v+3*j))).flat();
 for(let j=0;j<k-1;j++){let b=j%2?8:0,u=9*j+b,v=9*(j+1)+b;[T[u][0],T[v][0]]=[T[v][0],T[u][0]]}
 return T
}
function affineWeight(T,n){
 const m=T.length,R=[];
 for(let c=0;c<3;c++)for(let z=0;z<n;z++){
  let row=bit(m);for(let i=0;i<m;i++)if(T[i][c]===z)row|=bit(i);R.push(row)
 }
 const p=[];let r=0;
 for(let j=0;j<m;j++){
  let i=R.findIndex((v,i)=>i>=r&&has(v,j));if(i<0)continue;
  [R[r],R[i]]=[R[i],R[r]];
  for(let t=0;t<R.length;t++)if(t!==r&&has(R[t],j))R[t]^=R[r];
  p.push(j);r++
 }
 check(R.every(v=>v!==bit(m)));
 const P=new Set(p),free=Array.from({length:m},(_,i)=>i).filter(i=>!P.has(i)),classes=new Map();
 function add(f,s){let a=classes.get(f)||[0,0];a[s]++;classes.set(f,a)}
 for(let j=0;j<free.length;j++)add(bit(j),0);
 for(let i=0;i<p.length;i++){
  let f=0n;for(let j=0;j<free.length;j++)if(has(R[i],free[j]))f|=bit(j);
  add(f,Number(has(R[i],m)))
 }
 let off=(classes.get(0n)||[0,0])[1];classes.delete(0n);
 for(let [a,b] of classes.values()){check(a===b);off+=Math.min(a,b)}
 return {nullity:free.length,constantWeight:off}
}
function main(){
 const words=[];
 for(let x=0n;x<512n;x++){
  let ok=true;for(let c=0;c<3;c++)for(let z=0;z<3;z++){let s=0;for(let i=0;i<9;i++)if(has(x,i)&&core[i][c]===z)s++;if(s%2!==1)ok=false}
  if(ok)words.push(Number(x))
 }
 check(JSON.stringify(words)===JSON.stringify([122,158,333,425]));check(words.every(x=>weight(BigInt(x))===5&&has(BigInt(x),0)===has(BigInt(x),8)));
 const rows=[];
 for(let k of [1,2,4,8,16,32,64,128]){
  let T=family(k),v=affineWeight(T,3*k);check(v.nullity===k+1&&v.constantWeight===5*k);
  for(let j=1;j<k;j++){let l=0,r=0;for(let i=0;i<T.length;i++){if(i<9*j&&T[i][0]>=3*j)l++;if(i>=9*j&&T[i][0]<3*j)r++}check(l===1&&r===1)}
  rows.push({k,m:T.length,n:3*k,...v})
 }
 return {words,rows};
}
console.log(JSON.stringify(main()));