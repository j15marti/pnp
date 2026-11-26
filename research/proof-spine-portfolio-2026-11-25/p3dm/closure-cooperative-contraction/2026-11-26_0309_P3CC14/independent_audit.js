// P3CC14 independent local footprint, phase-lift and dual certificate audit.
// Run with node independent_audit.js.
const run=()=>{
let checks=0;const ok=x=>{checks++;if(!x)throw Error("assertion "+checks)};
const W=[0,6,9,0,2,-5,3,9,-6,8,-1,-3,2,0,-3,2,-1,9,-4,-5,6,6,0,3];
function source(k,gap=false){let T=[];for(let a=0;a<k;a++)for(let j=0;j<8;j++)T.push([2*a+(j>>2),2*a+(j>>1&1),2*a+(j&1)]);let swaps=gap?[[6,8],[14,18],...(k>=4?[[23,24]]:[]),...Array.from({length:Math.max(0,k-4)},(_,j)=>[8*(j+3)+7,8*(j+4)])]:Array.from({length:k-1},(_,j)=>[8*j+7,8*(j+1)]);for(let [u,v] of swaps)[T[u][0],T[v][0]]=[T[v][0],T[u][0]];ok(new Set(T.map(t=>t.join(","))).size===T.length);return {T,swaps,w:T.map((_,i)=>gap?(W[i]??0):0)}}
function local(T,w,k){let P=[];for(let a=0;a<k;a++){let Q=new Map();for(let i=8*a;i<8*a+8;i++)for(let j=i+1;j<8*a+8;j++)if(T[i].every((x,c)=>x!==T[j][c])){let B=[T[i][0],T[j][0]].sort((a,b)=>a-b),key=B.join(","),cost=w[i]+w[j];if(!Q.has(key)||cost<Q.get(key).cost)Q.set(key,{B,cost,ids:[i,j]})}P.push([...Q.values()])}return P}
function close(P,n){for(;;){let sup=Array.from({length:n},()=>[]),all=Array.from({length:n},()=>[]);for(let a=0;a<P.length;a++){ok(P[a].length>0);for(let x of new Set(P[a].flatMap(q=>q.B))){sup[x].push(a);if(P[a].every(q=>q.B.includes(x)))all[x].push(a)}}let old=P.reduce((s,q)=>s+q.length,0);for(let x=0;x<n;x++){ok(sup[x].length>0&&all[x].length<=1);if(sup[x].length===1){let a=sup[x][0];P[a]=P[a].filter(q=>q.B.includes(x))}if(all[x].length===1)for(let a of sup[x])if(a!==all[x][0])P[a]=P[a].filter(q=>!q.B.includes(x))}if(old===P.reduce((s,q)=>s+q.length,0))return P}}
const key=B=>B.slice().sort((a,b)=>a-b).join(",");
function exch(Q,valuated=false){let M=new Map(Q.map(q=>[key(q.B),q.cost]));for(let a of Q)for(let b of Q)for(let x of a.B.filter(x=>!b.B.includes(x))){let good=false;for(let y of b.B.filter(y=>!a.B.includes(y))){let d=key(a.B.filter(z=>z!==x).concat(y)),e=key(b.B.filter(z=>z!==y).concat(x));if(M.has(d)&&(!valuated||(M.has(e)&&a.cost+b.cost>=M.get(d)+M.get(e))))good=true}if(!good)return false}return true}
const phase=j=>Math.min(j%8,7-j%8);
function verify(T,S,k){ok(S.length===2*k);for(let c=0;c<3;c++)ok(new Set(S.map(j=>T[j][c])).size===2*k)}
function witness(swaps,k,a,p){let V=Array(k).fill(-1);V[a]=p;for(let i=a-1;i>=0;i--){let [u,v]=swaps[i],bit=V[i+1]===phase(v);V[i]=bit?phase(u):(phase(u)+1)%4}for(let i=a;i<k-1;i++){let [u,v]=swaps[i],bit=V[i]===phase(u);V[i+1]=bit?phase(v):(phase(v)+1)%4}return V.flatMap((p,i)=>[8*i+p,8*i+7-p])}
function ref(swaps,w,k){let D=Array(4).fill(1n),C=Array.from({length:4},(_,p)=>w[p]+w[7-p]);for(let i=1;i<k;i++){let [u,v]=swaps[i-1],D2=[],C2=[];for(let p=0;p<4;p++){let cand=[0,1,2,3].filter(q=>(q===phase(u))===(p===phase(v)));D2.push(cand.reduce((s,q)=>s+D[q],0n));C2.push(Math.min(...cand.map(q=>C[q]))+w[8*i+p]+w[8*i+7-p])}D=D2;C=C2}return {count:D.reduce((s,c)=>s+c,0n).toString(),cost:Math.min(...C)}}
let out=[];
for(let k of [3,4,8,16,32,64,128,256]){
for(let gap of [false,true]){let {T,swaps,w}=source(k,gap),P=close(local(T,w,k),2*k);ok(P.every(q=>exch(q)));let witnesses=0;for(let a=0;a<k;a++)for(let p=0;p<4;p++){verify(T,witness(swaps,k,a,p),k);witnesses++}
let result=ref(swaps,w,k);if(!gap){ok(result.count===(3n**BigInt(k)+1n).toString());for(let a=1;a<k-1;a++){let U=new Set(T.slice(8*a,8*a+8).map(t=>t[0]));ok(U.size===4);for(let x of U)ok(T.some((t,j)=>Math.floor(j/8)!==a&&t[0]===x))}}
else {ok(result.cost===2);let prices=[0,-8,-1,-1,-2,0,...Array(2*k-6).fill(0)],alpha=P.map(Q=>Math.min(...Q.map(q=>q.cost-q.B.reduce((s,x)=>s+prices[x],0))));ok(alpha.reduce((s,x)=>s+x,0)+prices.reduce((s,x)=>s+x,0)===1);let twice=Array(2*k).fill(0),cost2=0;let pairs=[[[3,4],[1,6]],[[8,11],[13,14]],[[19,20],[18,21]]];for(let a=0;a<k;a++){let J=a<3?pairs[a]:[[8*a+1,8*a+6],[8*a+1,8*a+6]];for(let ids of J){ok(ids.every(i=>Math.floor(i/8)===a));ok(T[ids[0]].every((x,c)=>x!==T[ids[1]][c]));let B=ids.map(i=>T[i][0]);let q=P[a].find(q=>key(q.B)===key(B));ok(q&&q.cost===ids.reduce((s,i)=>s+w[i],0));for(let x of B)twice[x]++;cost2+=q.cost}}ok(twice.every(x=>x===2));ok(cost2===2);ok(P.some(q=>!exch(q,true)));let tight=P.map((Q,a)=>Q.filter(q=>q.cost-q.B.reduce((s,x)=>s+prices[x],0)===alpha[a]));ok(tight.some(q=>!exch(q)));}
out.push({k,triples:8*k,gap,words:P.reduce((s,q)=>s+q.length,0),witnesses,integerOptimum:result.cost,count:result.count,lpOptimum:gap?1:null});}}
return {checks,cases:out};
};
console.log(JSON.stringify(run(),null,2));
