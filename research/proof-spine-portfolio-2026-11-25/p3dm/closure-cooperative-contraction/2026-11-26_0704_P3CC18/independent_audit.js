// Standalone Node.js check of genuine majority barrier and binary union entailment.
const run=()=>{
let checks=0;const ok=x=>{checks++;if(!x)throw Error("assert "+checks)};
const T=[[0,0,8],[4,0,0],[1,1,1],[4,1,1],[0,0,1],[4,1,2],[2,2,10],[5,2,2],[3,3,3],[5,3,3],[2,2,3],[5,3,0],[0,5,5],[6,5,5],[1,4,4],[6,4,4],[0,5,4],[6,4,5],[2,7,7],[7,7,7],[3,6,6],[7,6,6],[2,7,6],[7,6,7],[8,8,0],[8,8,9],[8,9,8],[8,9,9],[9,8,8],[9,8,9],[9,9,8],[9,9,9],[10,10,2],[10,10,11],[10,11,10],[10,11,11],[11,10,10],[11,10,11],[11,11,10],[11,11,11]];
const bounds=[[0,0],[0,1],[0,1],[-1,0],[0,1],[-1,1],[0,0],[0,1],[0,0],[0,1]];
const E=[[[0,0],2,1,0],[[0,1],1,0,0],[[0,8],0,2,1],[[1,1],0,1,1],[[1,2],1,0,0],[[2,2],0,3,0],[[2,3],1,0,0],[[2,10],3,1,1],[[3,0],1,0,0],[[3,3],0,1,1],[[4,4],6,7,1],[[4,5],7,6,0],[[5,4],7,6,0],[[5,5],6,7,1],[[6,6],8,9,1],[[6,7],9,8,0],[[7,6],9,8,0],[[7,7],8,9,1],[[8,0],0,2,1],[[8,8],2,4,0],[[8,9],4,0,0],[[9,8],4,0,0],[[9,9],0,4,1],[[10,2],3,1,1],[[10,10],1,5,0],[[10,11],5,3,0],[[11,10],5,3,0],[[11,11],3,5,1]];
const W=[[1,2,7,8,17,16,21,18,28,27,36,35],[0,3,7,8,14,13,21,18,24,31,36,35],[4,5,10,11,14,13,20,19,28,27,36,35]];
const B=[[0,1,0,0,0,0,1,0],[0,0,0,0,0,0,0,0],[1,1,1,0,1,0,0,0]];
const scope=[];for(let f=0;f<bounds.length;f++)for(let k=bounds[f][0]+1;k<=bounds[f][1];k++)scope.push([f,k]);
function pairs(w){let h=bounds.map(x=>x[0]);for(let i=0;i<w.length;i++)h[scope[i][0]]+=w[i];let P=[];for(let [p,a,b,r] of E){let x=r+h[a]-h[b];ok(x===0||x===1);if(x)P.push(p.join(","))}ok(P.length===12&&new Set(P.map(p=>p.split(",")[0])).size===12&&new Set(P.map(p=>p.split(",")[1])).size===12);return P.sort()}
for(let i=0;i<3;i++){ok(W[i].length===12&&!W[i].includes(15));for(let c=0;c<3;c++)ok(new Set(W[i].map(j=>T[j][c])).size===12);ok(JSON.stringify(pairs(B[i]))===JSON.stringify(W[i].map(j=>T[j].slice(1).join(",")).sort()))}
const majority=B[0].map((_,i)=>+(B[0][i]+B[1][i]+B[2][i]>=2)),p=pairs(majority),bad=["0,0","1,1","4,4"];ok(bad.every(v=>p.includes(v)));const owners=new Set(T.filter((t,j)=>j!==15&&bad.includes(t.slice(1).join(","))).map(t=>t[0]));ok(owners.size===2);
let state=26112618;function rnd(n){state=(Math.imul(1664525,state)+1013904223)>>>0;return state%n}
let formulas=0,clauseTests=0,unionTests=0;
for(let trial=0;trial<500;trial++){let n=1+rnd(6),L=Array.from({length:2*n},(_,i)=>i<n?i+1:-(i-n+1)),C=Array.from({length:rnd(15)},()=>[L[rnd(L.length)],L[rnd(L.length)]]),bit=(w,a)=>Boolean(w>>(Math.abs(a)-1)&1)===(a>0),models=C=>Array.from({length:1<<n},(_,w)=>w).filter(w=>C.every(([a,b])=>bit(w,a)||bit(w,b)));
const A=models(C);if(!A.length)continue;formulas++;
function reach(C){let R=new Map(L.map(a=>[a,new Set([a])]));for(let[a,b]of C){R.get(-a).add(b);R.get(-b).add(a)}for(let k of L)for(let a of L)if(R.get(a).has(k))for(let b of R.get(k))R.get(a).add(b);return R}
const R=reach(C);for(let a of L)for(let b of L){let predicted=R.get(-a).has(a)||R.get(-b).has(b)||R.get(-a).has(b)||R.get(-b).has(a);ok(predicted===A.every(w=>bit(w,a)||bit(w,b)));clauseTests++}
let branches=Array.from({length:1+rnd(4)},()=>C.concat([[L[rnd(L.length)],L[rnd(L.length)]]]));let U=branches.flatMap(models);
for(let a of L)for(let b of L){let expected=U.every(w=>bit(w,a)||bit(w,b));let actual=branches.every(D=>{let S=models(D);if(!S.length)return true;let R=reach(D);return R.get(-a).has(a)||R.get(-b).has(b)||R.get(-a).has(b)||R.get(-b).has(a)});ok(expected===actual);unionTests++}
}
return {checks,formulas,clauseTests,unionTests,seed:26112618,barrier:{index:46,triples:40,guard:"15=0",words:B,majority,deficientPairs:bad,neighborOwners:[...owners].sort()}};
};
console.log(JSON.stringify(run(),null,2));
