'use strict';
// Independent no-import-from-producer finite referee for LSPV-4/391.
// Checks Cook gate expansion, source deletion, malformed pivots and Tseitin.
const assert=require('assert');
function trueClause(C,a){return C.some(x=>x>0?!!a[x]:!a[-x]);}
function key(C){return [...new Set(C)].sort((x,y)=>x-y).join(',');}
function resolve(A,B,p){
 if(!(A.includes(p)&&B.includes(-p))&&!(A.includes(-p)&&B.includes(p)))throw Error('illegal pivot');
 const C=[...new Set([...A,...B].filter(x=>Math.abs(x)!==Math.abs(p)))];
 if(C.some(x=>C.includes(-x)))throw Error('tautological resolvent');
 return C;
}
function gate(a,b,c,t,q){
 const G=[[-t,b],[-t,c],[t,-b,-c]];
 const O=[[-q,a,t],[q,-a],[q,-t]];
 const D=[O[1],resolve(O[2],G[2],t),resolve(O[0],G[0],t),resolve(O[0],G[1],t)];
 const E=[[q,-a],[q,-b,-c],[-q,a,b],[-q,a,c]];
 assert.deepStrictEqual(D.map(key).sort(),E.map(key).sort());
 let checks=1;
 for(let mask=0;mask<32;mask++){
  let A={};[a,b,c,t,q].forEach((v,i)=>A[v]=(mask>>i)&1);
  assert.strictEqual([...G,...O].every(x=>trueClause(x,A)),A[t]===(A[b]&A[c])&&A[q]===(A[a]|(A[b]&A[c])));
  assert.strictEqual(D.every(x=>trueClause(x,A)),A[q]===(A[a]|(A[b]&A[c])));
  checks+=2;
 }
 return checks;
}
function php(h){
 const C=[],v=(p,j)=>(p-1)*h+j;
 for(let p=1;p<=h+1;p++)C.push(Array.from({length:h},(_,j)=>v(p,j+1)));
 for(let j=1;j<=h;j++)for(let p=1;p<=h+1;p++)for(let k=p+1;k<=h+1;k++)C.push([-v(p,j),-v(k,j)]);
 return C;
}
function sat(C,n){
 for(let mask=0;mask<2**n;mask++){
  const a={};for(let j=1;j<=n;j++)a[j]=(mask>>(j-1))&1;
  if(C.every(c=>trueClause(c,a)))return true;
 }return false;
}
let checks=0;
for(const v of [[1,2,3,4,5],[13,7,37,9,29],[101,61,3,2,1001]])checks+=gate(...v);
for(let h=1;h<=3;h++){
 const C=php(h),n=h*(h+1);
 assert.strictEqual(C.length,h+1+h*h*(h+1)/2);
 assert.strictEqual(sat(C,n),false);
 checks+=2;
 for(let j=0;j<C.length;j++){
  assert.strictEqual(sat(C.filter((_,i)=>i!==j),n),true);checks++;
 }
}
for(const [a,b,p] of [[[1,2],[2,3],1],[[1,2],[-1,3],2]]){
 assert.throws(()=>resolve(a,b,p));checks++;
}
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
for(const [charge,goal] of [[[1,0,0,0],0],[[0,0,0,0],8]]){
 let found=0;for(let mask=0;mask<64;mask++){
  if(charge.every((r,v)=>edges.reduce((s,e,i)=>s+(e.includes(v)?((mask>>i)&1):0),0)%2===r))found++;
 }
 assert.strictEqual(found,goal);checks++;
}
assert.strictEqual(checks,239);
console.log(JSON.stringify({status:'PASS',checks,control:'Cook q=a OR (b AND c), PHP and odd/even K4'}));
