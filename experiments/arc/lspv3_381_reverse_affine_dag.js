'use strict';
// LSPV-3/381, 2026-11-03 19:24 PST. Run: node experiments/arc/lspv3_381_reverse_affine_dag.js
function req(x,s){if(!x)throw Error(s)}
function pc(x){let n=0;for(;x;x>>=1)n+=x&1;return n}
function reverse(rows,d,gates,root,target){
 const m=rows.length,q=gates.length;
 req(Number.isInteger(d)&&d>=0,'dim');req(Number.isInteger(root)&&root>=0&&root<m+q,'root');
 req(Array.isArray(target)&&target.length===d+1&&target.every(x=>x===0||x===1),'target');
 for(let i=0;i<m;i++){
  let r=rows[i];req(r&&Array.isArray(r.vars)&&(r.b===0||r.b===1),'row');
  let seen=new Set();
  for(let v of r.vars){req(Number.isInteger(v)&&v>=0&&v<d&&!seen.has(v),'index');seen.add(v)}
 }
 for(let j=0;j<q;j++){
  let g=gates[j];req(Array.isArray(g)&&g.length===2,'gate arity');
  for(let p of g)req(Number.isInteger(p)&&p>=0&&p<m+j,'parent');
 }
 let a=new Uint8Array(m+q);a[root]=1;
 for(let j=q-1;j>=0;j--)if(a[m+j]){
  let [u,v]=gates[j];a[u]^=1;a[v]^=1;
 }
 let got=new Uint8Array(d+1);
 for(let i=0;i<m;i++)if(a[i]){
  for(let v of rows[i].vars)got[v]^=1;got[d]^=rows[i].b;
 }
 return {ok:got.every((v,i)=>v===target[i]),coeff:Array.from(a.slice(0,m)),value:Array.from(got)};
}
function forward(rows,d,gates,root,target){
 let v=rows.map(r=>{let a=new Uint8Array(d+1);for(let j of r.vars)a[j]^=1;a[d]=r.b;return a});
 for(let [i,j] of gates){let a=new Uint8Array(d+1);for(let k=0;k<=d;k++)a[k]=v[i][k]^v[j][k];v.push(a)}
 return v[root].every((x,k)=>x===target[k]);
}
function sourceRows(edges,h,odd){
 let a=Array.from({length:h},()=>[]);
 edges.forEach(([u,v],i)=>{a[u].push(i);a[v].push(i)});
 return a.map((vars,i)=>({vars,b:i===0?odd:0}));
}
function clauses(rows){
 return rows.flatMap(r=>{
  req(r.vars.length===3,'cubic');let out=[];
  for(let mask=0;mask<8;mask++)if((pc(mask)&1)!==r.b)
   out.push(r.vars.map((v,i)=>(mask&(1<<i))?-(v+1):v+1));
  return out;
 });
}
function authenticate(c,rows){
 if(!Array.isArray(c)||c.length!==4*rows.length)return false;
 for(let i=0;i<rows.length;i++){
  let r=rows[i];if(!r||!Array.isArray(r.vars)||r.vars.length!==3)return false;
  let expected=clauses([r]);
  for(let j=0;j<4;j++){
   let given=c[4*i+j];if(!Array.isArray(given)||given.length!==3)return false;
   for(let k=0;k<3;k++)if(given[k]!==expected[j][k])return false;
  }
 }
 return true;
}
function models(cla,d){
 let n=0;for(let a=0;a<(1<<d);a++)
  if(cla.every(c=>c.some(l=>l>0?((a>>(l-1))&1):!((a>>(-l-1))&1))))n++;
 return n;
}
function main(){
 let checks=0,trials=0,rejects=0;function check(x,s){req(x,s);checks++}
 let cases=[
  ['K4',4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],
  ['K33',6,[[0,3],[0,4],[0,5],[1,3],[1,4],[1,5],[2,3],[2,4],[2,5]]],
  ['cube',8,Array.from({length:8},(_,i)=>[0,1,2].filter(j=>!(i&(1<<j))).map(j=>[i,i^(1<<j)])).flat()]
 ];
 let control=[];
 for(let [name,h,edges] of cases){
  let d=edges.length,odd=sourceRows(edges,h,1),even=sourceRows(edges,h,0),co=clauses(odd),ce=clauses(even);
  check(authenticate(co,odd)&&authenticate(ce,even),'source auth');
  check(!authenticate(co,even),'wrong parity source');
  let cc=co.map(c=>c.slice());cc[0][0]*=-1;check(!authenticate(cc,odd),'corrupt source');
  check(models(co,d)===0,'odd UNSAT');check(models(ce,d)===(1<<(d-h+1)),'even SAT');
  let gates=Array.from({length:h-1},(_,j)=>[j? h+j-1:0,j+1]);
  let root=h+gates.length-1,target=Array(d).fill(0).concat([1]);
  let ro=reverse(odd,d,gates,root,target),re=reverse(even,d,gates,root,target);
  check(ro.ok&&!re.ok,'opposite label');check(forward(odd,d,gates,root,target)&&!forward(even,d,gates,root,target),'forward');
  check(ro.coeff.every(x=>x===1),'leaf parity');
  control.push({graph:name,h,sourceClauses:co.length,oddModels:0,evenModels:models(ce,d),xorGates:gates.length});
 }
 let seed=381;function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
 let rows=[{vars:[0,1],b:0},{vars:[1,2],b:1},{vars:[2,3],b:1}],d=4,m=rows.length;
 for(let q=1;q<=12;q++)for(let t=0;t<96;t++){
  let gates=[];for(let j=0;j<q;j++)gates.push([rnd()%(m+j),rnd()%(m+j)]);
  let root=m+q-1,target=[0,0,0,0,1];
  check(reverse(rows,d,gates,root,target).ok===forward(rows,d,gates,root,target),'shared DAG');
  trials++;
 }
 let fibRows=[{vars:[0],b:0},{vars:[0],b:1}],fibGates=[];
 for(let i=2;i<=62;i++)fibGates.push([i-1,i-2]);
 check(reverse(fibRows,1,fibGates,62,[0,1]).ok,'fib accept');
 check(forward(fibRows,1,fibGates,62,[0,1]),'fib forward');
 check(!reverse([{vars:[0],b:0},{vars:[0],b:0}],1,fibGates,62,[0,1]).ok,'fib SAT');
 let leaf=[1n,1n];for(let i=2;i<=62;i++)leaf.push(leaf[i-1]+leaf[i-2]);
 check(leaf[62]>1000000000000n,'exp unfolding');
 function bad(f){let failed=false;try{f()}catch(e){failed=true}check(failed,'must reject');rejects++}
 bad(()=>reverse(fibRows,1,[[2,0]],2,[0,1]));
 bad(()=>reverse(fibRows,1,[[0,-1]],2,[0,1]));
 bad(()=>reverse(fibRows,1,[[0,1,0]],2,[0,1]));
 bad(()=>reverse([{vars:[2],b:1}],1,[],0,[0,1]));
 bad(()=>reverse([{vars:[0,0],b:1}],1,[],0,[0,1]));
 bad(()=>reverse([{vars:[0],b:3}],1,[],0,[0,1]));
 bad(()=>reverse(fibRows,1,[],2,[0,1]));
 bad(()=>reverse(fibRows,1,[[0,1]],2,[1]));
 return {run:'LSPV3_381_REVERSE_AFFINE_DAG',revision:'2026-11-03_1924',model:'typed GF2-DAG',seed:381,controls:control,sharedDagForwardReverseAgreement:trials,fibonacci:{lastIndex:62,chargedXorNodes:61,unfoldedLeafOccurrences:leaf[62].toString(),accepted:true,satControlRejected:true},malformedOrCorruptedRejected:rejects,assertions:checks,scope:'finite checks; no algorithm-independent SAT lower bound or B1/B2/B3 proof'};
}
if(typeof module!=='undefined')module.exports={main,reverse,forward,authenticate};
if(typeof process!=='undefined'&&require.main===module)console.log(JSON.stringify(main(),null,2));