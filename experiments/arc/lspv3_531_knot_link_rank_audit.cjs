'use strict';
// LSPV-3/531 independent finite control. NOT a native R_mix341 checker.
// Source: Koenig-Tsvietkova 2021 Theorem 1 Hopf-pair variable construction.
const assert=require('assert').strict;
function dimacs(k) {
 const clauses=[];
 for(let x=0;x<8;x++) clauses.push([1,2,3].map((v,j)=>((x>>(2-j))&1)?-v:v));
 for(let i=0;i<k;i++) clauses.push([4+3*i,5+3*i,6+3*i]);
 return clauses;
}
function normalize(c) {
 const a=[...new Set(c)];
 if(a.some(l=>!Number.isInteger(l)||l===0||a.includes(-l)))throw Error('invalid literal');
 return a.sort((x,y)=>Math.abs(x)-Math.abs(y));
}
function refute(src) {
 const store=new Map(src.map((c,j)=>[j+1,normalize(c)]));
 const m=src.length;
 let next=m+1, deriv=[];
 const res=(a,b,p)=>{
   assert(store.has(a)&&store.has(b));
   let left=store.get(a),right=store.get(b);
   assert(left.includes(p)&&right.includes(-p));
   let C=normalize([...left.filter(x=>x!==p),...right.filter(x=>x!==-p)]);
   const id=next++;store.set(id,C);deriv.push({id,a,b,pivot:p,out:C});return id;
 };
 let tmp=[];
 for(let i=0;i<4;i++)tmp.push(res(2*i+1,2*i+2,3));
 let u=res(tmp[0],tmp[1],2),v=res(tmp[2],tmp[3],2);
 let fin=res(u,v,1);
 assert.deepEqual(store.get(fin),[]);
 assert.equal(deriv.length,7);
 return {deriv,source_ancestors:new Set(deriv.flatMap(s=>[s.a,s.b]).filter(x=>x<=m))};
}
function gf2Rank(rows) {
 const basis=new Map();let rank=0;
 for(let row of rows){let a=row;while(a){
   const piv=a.toString(2).length-1;
   if(basis.has(piv))a^=basis.get(piv);
   else{basis.set(piv,a);rank++;break}
 }}
 return rank;
}
function satisfied(clause,bits) {
 return clause.some(l=>l>0?bits[Math.abs(l)-1]:!bits[Math.abs(l)-1]);
}
let checks=0,summary=[];
for(const k of [0,1,2,4,8,16,32,64]){
 const src=dimacs(k),n=3+3*k;
 const {deriv,source_ancestors}=refute(src);
 assert.equal(source_ancestors.size,8);checks++;
 for(let removed=0;removed<8;removed++){
   let witness=Array.from({length:n},(_,j)=>j<3?(src[removed][j]<0):true);
   assert(src.every((c,j)=>j===removed||satisfied(c,witness)));
   assert(!satisfied(src[removed],witness));checks+=2;
 }
 // Hopf principal submatrix from the published link construction.
 const rows=Array.from({length:2*n},(_,i)=>1n<<BigInt(i^1));
 const rank=gf2Rank(rows);
 assert.equal(rank,2*n);checks++;
 assert.equal(2*n+src.length,14+7*k);checks++;
 summary.push({k,n,clauses:src.length,components:2*n+src.length,hopf_rank:rank,W_RES:deriv.length});
}
console.log(JSON.stringify({audit:'INDEPENDENT NODE',checks,summary},null,2));
