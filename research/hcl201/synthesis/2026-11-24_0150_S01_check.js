function run(){
let seed=20261124;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
function red(x,B){for(const v of B)if((x^v)<x)x^=v;return x}
function bas(xs){let B=[];for(let x of xs){x=red(x,B);if(x){B.push(x);B.sort((a,b)=>b-a)}}return B}
const rank=x=>bas(x).length, sum=(a,b)=>a^b;
function sums(S){let D=new Set([0]);for(let s of S){let E=new Set();for(let x of D)for(let y of s)E.add(x^y);D=E}return D}
let out={seed:20261124,instances:0,targets:0,sat:0,unsat:0,witnessChecks:0,mismatches:0,widthChecks:0,widthIncreases:0,widthDrops:0,peeled:0,allPeeled:0,cycle:[]};
function solve(S){let a=S.map(s=>s[0]),V=S.map((s,i)=>bas(s.map(x=>x^a[i]))),W=[],rem=[],live=S.map((_,i)=>i),off=0;for(;;){let i=live.find(i=>rank(V[i].map(x=>red(x,W)))<=1);if(i===undefined)break;let alt=S[i].find(x=>red(x^a[i],W));rem.push({i,old:W,alt});W=bas(W.concat(V[i]));off^=a[i];live=live.filter(j=>j!==i);out.peeled++;}
if(!live.length)out.allPeeled++;
for(let k=0;k<=S.length;k++){let A=V.slice(0,k).flat(),B=V.slice(k).flat(),old=rank(A)+rank(B)-rank(A.concat(B));let P=A.map(x=>red(x,W)),Q=B.map(x=>red(x,W)),nw=rank(P)+rank(Q)-rank(P.concat(Q));out.widthChecks++;if(nw>old)out.widthIncreases++;if(nw<old)out.widthDrops++}
let D=new Map([[0,[]]]);for(let i of live){let E=new Map();for(let [x,h] of D)for(let s of S[i]){let q=red(x^s,W);if(!E.has(q))E.set(q,h.concat([[i,s]]))}D=E}
return c=>{let h=D.get(red(c^off,W));if(!h)return null;let ans=h.slice(),need=c^off^h.reduce((v,p)=>v^p[1],0);for(let j=rem.length-1;j>=0;j--){let {i,old,alt}=rem[j],v=a[i];if(red(need,old)){if(alt===undefined)throw Error("no lift");need^=alt^v;v=alt}ans.push([i,v])}if(need)throw Error("residual");return ans};
}
function check(S,d){let ref=sums(S),f=solve(S);out.instances++;for(let c=0;c<2**d;c++){let a=f(c);out.targets++;if(ref.has(c))out.sat++;else out.unsat++;if(!!a!==ref.has(c))out.mismatches++;if(a){out.witnessChecks++;if(a.length!==S.length||new Set(a.map(p=>p[0])).size!==S.length||a.some(([i,x])=>!S[i].includes(x))||a.reduce((z,p)=>z^p[1],0)!==c)throw Error("bad lift")}}}
for(let t=0;t<240;t++){let d=3+rnd(6),h=2+rnd(6),S=[];for(let i=0;i<h;i++)S.push([...new Set(Array.from({length:1+rnd(5)},()=>rnd(2**d)))]);check(S,d)}
// Each edge of an even cycle is an independent region, each vertex appears twice.
// The local support is empty or one edge, including its syndrome bit.
for(let n of [4,6,8,10]){let S=Array.from({length:n},(_,i)=>[0,(1<<i)^(1<<((i+1)%n))^(1<<n)]),f=solve(S),target=(1<<n)-1,good=target^(((n/2)%2)<<n),bad=good^(1<<n);let a=f(good);if(!a||f(bad))throw Error("cycle control");out.cycle.push({n,sat:!!a,unsat:!f(bad),selected:a.filter(p=>p[1]).length})}
return out;
}
console.log(JSON.stringify(run(),null,2));
