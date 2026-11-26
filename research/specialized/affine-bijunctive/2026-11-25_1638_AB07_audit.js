function audit(){
let seed=20261125;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
function parity(x){let t=0;while(x){t^=1;x&=x-1}return t}
function rr(rows){let B=new Map();for(let [a,b] of rows){for(let p of [...B.keys()].sort((x,y)=>y-x))if(a&(1<<p)){let [c,d]=B.get(p);a^=c;b^=d}if(!a){if(b)return null;continue}let p=31-Math.clz32(a);B.set(p,[a,b])}return [...B.values()]}
function reduce(row,G){let [a,b]=row;for(let [c,d] of [...G].sort((x,y)=>y[0]-x[0])){let p=31-Math.clz32(c);if(a&(1<<p)){a^=c;b^=d}}return [a,b]}
function holds(P,x){return P.every(([a,b])=>parity(a&x)===b)}
function valid(F,G,x){return holds(G,x)&&F.every(P=>!holds(P,x))}
let C={roots:0,sat:0,unsat:0,closureCalls:0,probes:0,forces:0,projectionJobs:0,forestJobs:0,cyclicJobs:0,guardedJobs:0,projectedWords:0,lifts:0,rankBoundChecks:0,strictDecrease:0,equalDeficit:0,positiveCycleIncrease:0,compilerChecks:0,acceptedEliminations:0,blockedRoots:0};
function close(F,G){C.closureCalls++;G=rr(G);if(!G)return null;while(true){let P=[],add=null;for(let A of F){let R=rr(A.map(row=>reduce(row,G)));if(R===null)continue;if(!R.length)return null;if(R.length===1){add=[R[0][0],R[0][1]^1];break}P.push(R)}if(!add)return {P,G};G=rr([...G,add]);C.forces++;if(!G)return null}}
function paid(F,G,n){while(true){let a=close(F,G);if(!a)return null;let change=false;for(let i=0;i<n;i++){let r=reduce([1<<i,0],a.G);if(!r[0])continue;C.probes+=2;let L=close(F,[...a.G,[1<<i,0]]),R=close(F,[...a.G,[1<<i,1]]);if(!L&&!R)return null;if(!L||!R){G=[...a.G,[1<<i,L?0:1]];C.forces++;change=true;break}}if(!change)return a}}
function rank(P){return rr(P.map(a=>[a,0])).length}
function delta(F){let d=0;for(let mask=1;mask<(1<<F.length);mask++){let rows=[],n=0;for(let j=0;j<F.length;j++)if(mask&(1<<j)){n++;rows.push(...F[j].map(a=>a[0]))}d=Math.max(d,n-rank(rows))}return d}
function project(F,G,v){let p=v&-v;let out=[],T=[],GG=G.map(([a,b])=>[a&~p,b]);for(let A of F){let q=A.find(([a])=>parity(a&v));if(!q){out.push(A.map(([a,b])=>[a&~p,b]));continue}let [a,b]=q;T.push({q:[a&~p,b],g:A.filter(x=>x!==q).map(([c,d])=>parity(c&v)?[(c^a)&~p,d^b]:[c&~p,d])})}let parent=T.map((_,i)=>i);function find(i){while(parent[i]!==i)i=parent[i];return i}let beta=0;for(let i=0;i<T.length;i++)for(let j=i+1;j<T.length;j++){let A=T[i],B=T[j],R=rr([...A.g,...B.g,[A.q[0]^B.q[0],1^A.q[1]^B.q[1]]]);if(R===null)continue;out.push(R);let a=find(i),b=find(j);if(a===b)beta++;else parent[a]=b}return {out,GG,p,beta,touched:T.length}}
function check(ok){if(!ok)throw Error("audit failed "+JSON.stringify(C))}
function test(F,G,n){C.roots++;let words=Array.from({length:1<<n},(_,i)=>i);let truth=words.filter(x=>valid(F,G,x));C[truth.length?"sat":"unsat"]++;let A=paid(F,G,n);if(!A){check(!truth.length);return}check(words.every(x=>valid(A.P,A.G,x)===valid(F,G,x)));let Vs=words.filter(v=>v&&A.G.every(([a])=>!parity(a&v)));if(!Vs.length)return;let forest=false;for(let v of Vs){let R=project(A.P,A.G,v);C.projectionJobs++;if(G.length)C.guardedJobs++;C[R.beta?"cyclicJobs":"forestJobs"]++;if(!R.beta){forest=true;C.acceptedEliminations++}for(let y of words.filter(x=>!(x&R.p))){let b=valid(R.out,R.GG,y),lifts=[y,y^v].filter(x=>valid(F,G,x));check(b===!!lifts.length);C.projectedWords++;if(b){check(valid(F,G,lifts[0]));C.lifts++}}if(R.out.length<=11&&A.P.length<=11){let d=delta(A.P),e=delta(R.out);check(e<=d+R.beta);C.rankBoundChecks++;if(!R.beta){if(e<d)C.strictDecrease++;if(e===d)C.equalDeficit++}else if(e>d)C.positiveCycleIncrease++}let B=paid(R.out,R.GG,n);if(B===null)check(!truth.length);else check(words.every(x=>valid(B.P,B.G,x)===valid(R.out,R.GG,x)))}if(!forest)C.blockedRoots++}
for(let k=0;k<160;k++){let n=3+(k%3),F=[];let m=1+rand(6);for(let i=0;i<m;i++){let a=1+rand((1<<n)-1),b=1+rand((1<<n)-1);while(a===b)b=1+rand((1<<n)-1);F.push([[a,rand(2)],[b,rand(2)]])}let G=k%3===0?[[1+rand((1<<n)-1),rand(2)]]:[];test(F,G,n)}
// All eight source truth tuples, all eight selector tuples, all eight signs.
for(let x=0;x<8;x++)for(let neg=0;neg<8;neg++){let l=x^neg,ok=false;for(let s=0;s<8;s++){let legal=parity(s)===1&&(s&~l)===0;check(!legal||l!==0);ok||=legal;C.compilerChecks++}check(ok===(l!==0))}
// Explicit 4-variable spread; pairwise independent row planes.
let planes=[],used=new Set();for(let a=1;a<16;a++)for(let b=a+1;b<16;b++){let q=[a,b,a^b];if(q.some(x=>used.has(x)))continue;planes.push([a,b]);q.forEach(x=>used.add(x))}check(planes.length===5);
let F=planes.map(([a,b])=>[[a,0],[b,0]]);check(delta(F)===1);check(!Array.from({length:16},(_,x)=>x).some(x=>valid(F,[],x)));
for(let v=1;v<16;v++){let R=project(F,[],v);check(R.touched===4&&R.beta===3)}
test(F,[],4);let F2=F.map((P,i)=>P.map(([a,b],j)=>[a,b^(i===0&&j===0?1:0)]));test(F2,[],4);
// One explicit low-support long chain family, each forbidden packet depends on adjacent coordinates.
for(let n=3;n<=5;n++){let F=[];for(let i=0;i<n-1;i++)F.push([[1<<i,1],[1<<(i+1),0]]);test(F,[],n);test(F,[[1,1],[1<<(n-1),0]],n)}
return {seed:20261125,...C,spreadPlanes:planes,spreadDirections:15,spreadDeficit:1,spreadConflictCycleRank:3,assertions:"passed"}
}
console.log(JSON.stringify(audit(),null,2));
