// C08-14 nonlocal repair. node repair_audit.js
function repairAudit(){
let checks=0,queries=0,aug=0;
function ok(t,msg){checks++;if(!t)throw Error(msg||"check "+checks)}
const F=Array.from({length:4},(_,s)=>Array.from({length:7},(_,i)=>[i,7+(i+s)%7,14+(i+3*s)%7])),C=F.flat(),n=21;
const B=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,20];
const T=[[10,11,20],[11,12,14],[6,6,13],[13,6,16],[5,5,19],[16,2,15],[4,4,18],[8,9,18],[2,9,16],[12,13,15],[18,4,17],[14,9,20],[19,5,18],[3,3,17],[20,8,19],[1,1,8],[7,0,17],[0,7,14],[9,2,10],[15,10,14]].map(([o,u,v])=>({o,u,v}));
const x=[0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1];
function auth(){let pairs=new Set;for(let p of F){let d=Array(n).fill(0);for(let c of p){ok(new Set(c).size===3);for(let v of c)d[v]++;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let k=Math.min(c[i],c[j])*n+Math.max(c[i],c[j]);ok(!pairs.has(k));pairs.add(k)}}ok(d.every(v=>v===1))}}auth();
const nae=(c,w)=>w[c[0]]!==w[c[1]]||w[c[1]]!==w[c[2]],bad=w=>C.map((c,i)=>nae(c,w)?-1:i).filter(i=>i>=0);
function ds(n){let p=Array.from({length:n},(_,i)=>i);function f(x){while(x!==p[x]){p[x]=p[p[x]];x=p[x]}return x}return{f,add(a,b){a=f(a);b=f(b);if(a===b)return false;p[a]=b;return true}}}
function ind(T,force=[]){let D=ds(n),O=new Set;for(let e of force)if(!D.add(e.u,e.v))return false;return T.every(e=>{if(O.has(e.o)||!D.add(e.u,e.v))return false;O.add(e.o);return true})}
function pairs(o,w=null){let c=C[o];return [[0,1],[0,2],[1,2]].filter(([i,j])=>!w||w[c[i]]!==w[c[j]]).map(([i,j])=>({o,u:c[i],v:c[j]}))}
function color(T){let a=Array.from({length:n},()=>[]),y=Array(n).fill(-1),q=[0];for(let e of T){a[e.u].push(e.v);a[e.v].push(e.u)}y[0]=0;for(let i=0;i<q.length;i++)for(let v of a[q[i]])if(y[v]<0){y[v]=1^y[q[i]];q.push(v)}ok(q.length===n);return y}
ok(ind(T)&&T.length===20&&color(T).every((a,i)=>a===x[i])&&bad(x).length===1);
let immediate=[];for(let i=0;i<T.length;i++)for(let e of pairs(T[i].o)){if(e.u===T[i].u&&e.v===T[i].v)continue;let a=T.slice();a[i]=e;if(ind(a))immediate.push(bad(color(a)).length)}ok(immediate.length===20&&Math.min(...immediate)===1);
// Generic exchange digraph with forced target pair contracted in graphic matroid.
function mi(E,force){queries++;let I=new Set;for(;;){let L=[...I],A=L.map(i=>E[i]),out=E.map((_,i)=>i).filter(i=>!I.has(i)),used=new Map(L.map(i=>[E[i].o,i])),q=[],prev=new Map;for(let j of out)if(ind(A.concat(E[j]),force)){// ind also includes color constraint, so use graphic-only instead for starting vertices.
}function gind(a){let D=ds(n);for(let e of force)if(!D.add(e.u,e.v))return false;return a.every(e=>D.add(e.u,e.v))}
for(let j of out)if(gind(A.concat(E[j]))){q.push(j);prev.set(j,-1)}let end=-1;for(let t=0;t<q.length&&end<0;t++){let i=q[t];if(!I.has(i)){let k=used.get(E[i].o);if(k===undefined){end=i;break}if(!prev.has(k)){q.push(k);prev.set(k,i)}}else{let a=A.filter(e=>e!==E[i]);for(let j of out)if(!prev.has(j)&&gind(a.concat(E[j]))){q.push(j);prev.set(j,i)}}}if(end<0)return A;for(let i=end;i>=0;i=prev.get(i)){if(I.has(i))I.delete(i);else I.add(i)}aug++;ok(I.size===L.length+1&&ind([...I].map(i=>E[i]),force))}}
let candidates=[],success=null,def=bad(x)[0];for(let owner of B){let E=B.filter(o=>o!==owner).flatMap(o=>pairs(o,x));for(let h of pairs(def)){let R=mi(E,[h]);if(R.length!==n-2){candidates.push({owner,edge:[h.u,h.v],status:"no forest"});continue}let D=ds(n);R.forEach(e=>D.add(e.u,e.v));ok(D.f(h.u)!==D.f(h.v));let root=D.f(h.u),y=x.map((v,i)=>v^(D.f(i)===root?1:0));if(y[0])y=y.map(v=>1^v);ok(B.filter(o=>o!==owner).every(o=>nae(C[o],y))&&nae(C[def],y));let score=bad(y).length;candidates.push({owner,edge:[h.u,h.v],score});if(score===0&&!success){let R2=mi(B.flatMap(o=>pairs(o,y)),[]);ok(R2.length===n-1&&color(R2).every((v,i)=>v===y[i]));success={owner,edge:[h.u,h.v],forest:R,word:y,newTree:R2,originalBad:bad(x),newBad:bad(y)}}}}
ok(success!==null,"nonlocal query did not repair trap");
// Independent actual full solution enumeration on the 21-var anchored instance; also verify repair.
let solutions=0;for(let w=0;w<2**(n-1);w++){let y=[0,...Array.from({length:n-1},(_,i)=>(w>>>i)&1)];if(C.every(c=>nae(c,y)))solutions++}ok(solutions>0&&bad(success.word).length===0);
// Count common-support component obstruction on scalable tripartite source (all owners, not a selected basis).
let common=[];for(let p of [5,7,13,31,127]){let c=Array.from({length:4},(_,s)=>Array.from({length:p},(_,i)=>[i,p+(i+s)%p,2*p+(i+3*s)%p])).flat(),a=Array.from({length:3*p},(_,v)=>v>=2*p?1:0),b=Array.from({length:3*p},(_,v)=>v<p||v>=2*p?1:0),D=ds(3*p);ok(c.every(t=>nae(t,a)&&nae(t,b)));for(let t of c)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(a[t[i]]!==a[t[j]]&&b[t[i]]!==b[t[j]])D.add(t[i],t[j]);let components=new Set(Array.from({length:3*p},(_,i)=>D.f(i))).size;ok(components===p+1);common.push({n:3*p,components,minimumReleases:components-1})}
return{checks,queries,augmentations:aug,immediateNeighborScores:immediate,sourceSolutionsUpToComplement:solutions,attempts:candidates.length,acquiredForests:candidates.filter(c=>c.score!==undefined).length,improving:candidates.filter(c=>c.score===0).length,candidates,success,common};
}
console.log(JSON.stringify(repairAudit(),null,2));
