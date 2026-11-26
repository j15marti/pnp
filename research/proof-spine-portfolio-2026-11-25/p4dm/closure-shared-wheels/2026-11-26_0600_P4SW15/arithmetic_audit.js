/* P4SW15 independent arithmetic and routing audit, Node.js 18+ */
function audit(){
 const assert=(p,m)=>{if(!p)throw Error(m)};
 const mod3=x=>((x%3)+3)%3;
 let legal=0,enumerated=0,maxRatio=0,routeChecks=0;
 const byArity={};
 function check(P,route){
  const k=P.length,d=[0,0,0,0],b=[0,0,0,0],out=Array.from({length:4},()=>[0,0]),inc=Array.from({length:4},()=>[0,0]);
  for(const [c,s,x] of P){d[c]+=s;b[c]+=s*x;(s===1?out:inc)[c][x]++}
  if(!d.every(z=>mod3(z)===mod3(d[0]))||!d.every((z,j)=>z-3*b[j]===d[0]-3*b[0]))return false;
  let n=mod3(d[0]),r,a;
  for(;;n+=3){r=d.map(z=>(n-z)/3);a=r[0]+b[0];if(r.every((v,j)=>v>=inc[j][0]+inc[j][1]&&a>=out[j][1]&&n-a>=out[j][0])&&a>=0&&a<=n)break}
  assert(n<=6*k+2,"size");assert(r.every((v,j)=>a-out[j][1]===v-inc[j][1]&&n-a-out[j][0]===2*v-inc[j][0]),"stub balance");
  maxRatio=Math.max(maxRatio,n/Math.max(k,1));
  if(route){
   // Independent lane permutation check; lane IDs paired by xor 1.
   const edges=4*n+inc.flat().reduce((p,q)=>p+q,0),m=2*edges;
   let order=Array.from({length:m},(_,i)=>i);
   for(let i=m-1;i>0;i--){const j=rand()%(i+1);[order[i],order[j]]=[order[j],order[i]]}
   let target=[],seen=new Set();for(const i of order)if(!seen.has(i)){target.push(i,i^1);seen.add(i);seen.add(i^1)}
   let crossings=0;
   for(let p=0;p<m;p++){let q=order.indexOf(target[p],p);while(q>p){assert((order[q]^1)!==order[q-1],"same-edge crossing");[order[q],order[q-1]]=[order[q-1],order[q]];q--;crossings++}}
   assert(order.every((i,p)=>i===target[p]),"routing");assert(n+48*crossings<=250000*(k+1)**2,"cap bound");routeChecks++;
  }
  return true;
 }
 let seed=26112615;function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
 for(let k=1;k<=5;k++){
  let total=0,valid=0,P=[];
  function dfs(){if(P.length===k){total++;if(check(P,false))valid++;return}for(let c=0;c<4;c++)for(const s of [-1,1])for(const x of [0,1]){P.push([c,s,x]);dfs();P.pop()}}
  dfs();enumerated+=total;legal+=valid;byArity[k]={total,valid};
 }
 // Known legal paired interface words with arbitrarily interleaved wires; randomized lane order only for test.
 for(let k=2;k<=40;k+=2)for(let trial=0;trial<5;trial++){
  let P=[];for(let j=0;j<k/2;j++){let c=(rand()>>>8)%4,x=(rand()>>>16)%2;P.push([c,1,x],[c,-1,x])}
  for(let i=P.length-1;i>0;i--){const j=rand()%(i+1);[P[i],P[j]]=[P[j],P[i]]}
  assert(check(P,true),"paired");
 }
 let rec=0;for(let K=2;K<=12;K++){let A=250000n*BigInt(K+1)**2n,p=2n**BigInt(K),c=BigInt(3*(K+1));for(let a=2n;a<=10n;a++){let s=a*A;for(let b=2n;b<=12n;b++){let n=b*s;assert(p*(s+A)**c+(n-s+s/2n)**c<=n**c-1n,"recurrence");rec++}}}
 return {enumerated,legal,byArity,maxInitialTupleToPortRatio:maxRatio,routeChecks,recurrenceChecks:rec,scope:"Independent arithmetic, lane routing and exact integer recurrence audit; no planar graph or SAT solver in this script."}
}
console.log(JSON.stringify(audit(),null,2));
