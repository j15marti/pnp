// Independent matching-support and charged-prefix audit; node controls.js.
function audit(){
let checks=0;const check=(v,m)=>{checks++;if(!v)throw Error(m)};
function matching(a){
  const n=a.length,own=Array(n).fill(-1);
  function go(i,seen){for(const j of a[i])if(!seen[j]){seen[j]=true;if(own[j]<0||go(own[j],seen)){own[j]=i;return true}}return false}
  for(let i=0;i<n;i++)if(!go(i,Array(n).fill(false)))return false;
  return true;
}
const clone=a=>a.map(r=>r.slice());
function reach(a,reverse){const n=a.length,b=reverse?Array.from({length:n},(_,j)=>a.flatMap((r,i)=>r.includes(j)?[i]:[])):a,seen=new Set([0]),q=[0];for(let k=0;k<q.length;k++)for(const j of b[q[k]])if(!seen.has(j)){seen.add(j);q.push(j)}return seen.size===n}
const controls=[];
for(const n of [9,17,25,49]){
 const h=(n-1)/2,a=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>j).filter(j=>i!==j&&(i===0||j===0||((i<=h)===(j<=h)))));
 check(matching(a),"base PM");check(reach(a,false)&&reach(a,true),"SCC");check(a.every(r=>r.length>=2),"no singleton");
 let count=0;for(let i=0;i<n;i++)for(const j of a[i]){
  const pin=clone(a);pin[i]=[j];check(matching(pin),"supported PM edge");
  const del=clone(a);del[i]=del[i].filter(t=>t!==j);check(matching(del),"avoidable PM edge");count++;
 }
 check(a.slice(1).every((r,k)=>r.every(j=>j===0||((k+1<=h)===(j<=h)))),"articulation certificate");
 controls.push({n,edges:count,PMTests:1+2*count,HC:false});
}
function perms(n){const out=[],p=[],u=Array(n).fill(false);function rec(){if(p.length===n){let j=0,k=0;do{j=p[j];k++}while(j!==0&&k<=n);if(k===n)out.push(p.slice());return}for(let j=0;j<n;j++)if(!u[j]){u[j]=true;p.push(j);rec();p.pop();u[j]=false}}rec();return out}
function enumerate(a,decide,cap){
 let calls=0,overflow=false;const out=[];
 const ask=b=>{calls++;return decide(b)};
 function rec(b,i){
  if(i===b.length){out.push(b.map(r=>r[0]));if(out.length>cap)overflow=true;return}
  for(const j of b[i]){
   const c=clone(b);c[i]=[j];if(ask(c))rec(c,i+1);
   if(overflow)return;
  }
 }
 if(ask(a))rec(a,0);
 return {calls,overflow,out};
}
const prefix=[];
for(const n of [3,4]){
 const E=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i!==j)E.push([i,j]);const P=perms(n);
 const dec=a=>P.some(p=>p.every((j,i)=>a[i].includes(j)));
 let calls=0,capped=0,graphs=0;
 for(let mask=0;mask<(1<<E.length);mask++){
  const a=Array.from({length:n},()=>[]);for(let k=0;k<E.length;k++)if(mask&(1<<k))a[E[k][0]].push(E[k][1]);
  const W=P.filter(p=>p.every((j,i)=>a[i].includes(j)));
  for(const cap of [0,1,2,100]){
   const r=enumerate(a,dec,cap);check(r.overflow===(W.length>cap),"overflow");
   check(r.out.length===Math.min(W.length,cap+1),"enumeration");
   check(new Set(r.out.map(p=>p.join(","))).size===r.out.length,"distinct");
   check(r.out.every(p=>W.some(q=>q.every((j,i)=>p[i]===j))),"lift");
   check(r.calls<=1+n*n*(Math.min(W.length,cap+1)+1),"call bound");
   calls+=r.calls;if(r.overflow)capped++;
  }graphs++;
 }
 prefix.push({n,graphs,queries:calls,overflowRuns:capped});
}
return {checks,controls,prefix,notes:"HC oracle in small prefix tests is explicit permutation enumeration, not a claimed polynomial general decider. Large articulation NO is symbolic certificate, not exhaustive HC enumeration."};
}
const result=audit();if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));
