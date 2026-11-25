// BD12 exact signed arithmetic DAG second-moment trellis; node >=18.
const assert=require('node:assert/strict');
const bit=i=>1n<<BigInt(i);
const stats={queries:0,gauss:0,pairs:0,transitions:0,positive:0,merges:0,entries:0,closure:0,pins:0,reference:0,assertions:0,peakKeys:0};
function check(a,b){stats.assertions++;assert.deepEqual(a,b)}
function parity(x){let y=0;while(x){x&=x-1n;y^=1}return y}
function count(eq,d){stats.gauss++;let basis=new Map;for(let [a,b] of eq){while(a){const p=a.toString(2).length-1;if(!basis.has(p)){basis.set(p,[a,b]);break}const [u,v]=basis.get(p);a^=u;b^=v}if(!a&&b)return 0n}return 1n<<BigInt(d-basis.size)}
const packet=(c,eq=[])=>({c:BigInt(c),eq});
const edge=(u,v,scope,terms)=>({u,v,scope,terms});
function words(scope){let a=[0n];for(const j of scope)a=a.concat(a.map(x=>x|bit(j)));return a}
function fixed(scope,x){return scope.map(j=>[bit(j),Number(!!(x&bit(j)))])}
function guard(e,x){let v=0n;for(const t of e.terms)if(t.eq.every(([a,b])=>parity(a&x)===b))v+=t.c;return v}
function moments(e,H,d){stats.queries++;const c0=count(H,d);let c1=0n,c2=0n;if(c0){for(const a of e.terms){c1+=a.c*count(H.concat(a.eq),d);for(const b of e.terms){stats.pairs++;c2+=a.c*b.c*count(H.concat(a.eq,b.eq),d)}}}return [c0,c1,c2]}
function closure(clauses,pins){let p=new Map(pins);for(;;){stats.closure++;let change=false;for(const C of clauses){if(C.some(([j,b])=>p.get(j)===b))continue;const L=C.filter(([j])=>!p.has(j));if(!L.length)return null;if(L.length===1){p.set(...L[0]);stats.pins++;change=true;break}}if(!change)return p}}
function evaluate(n,D,events,pins=new Map){const first=Array(n).fill(Infinity),last=Array(n).fill(-1);for(let i=0;i<events.length;i++)for(const j of events[i].scope){first[j]=Math.min(first[j],i);last[j]=i}
const front=i=>Array.from({length:n},(_,j)=>j).filter(j=>first[j]<=i&&last[j]>i);
let initial=Array(D*D).fill(0n);initial[0]=1n;let states=new Map([[0n,initial]]);
for(let i=0;i<events.length;i++){const e=events[i],old=front(i-1),next=front(i),B=[...new Set(old.concat(e.scope))],newStates=new Map;
for(const [s,Q] of states)for(const t of words(next)){stats.transitions++;const H=fixed(old,s).concat(fixed(next,t),B.filter(j=>pins.has(j)).map(j=>[bit(j),pins.get(j)]));const [c0,c1,c2]=moments(e,H,B.length);if(!c0)continue;stats.positive++;
let A=newStates.get(t);if(!A){A=Array(D*D).fill(0n);newStates.set(t,A)}else stats.merges++;
for(let a=0;a<D;a++)for(let b=0;b<D;b++){const idx=a*D+b;let z=c0*Q[idx];if(a===e.v)z+=c1*Q[e.u*D+b];if(b===e.v)z+=c1*Q[a*D+e.u];if(a===e.v&&b===e.v)z+=c2*Q[e.u*D+e.u];A[idx]+=z;stats.entries++}}
states=newStates;stats.peakKeys=Math.max(stats.peakKeys,states.size)}
let Q=states.get(0n)||Array(D*D).fill(0n);const free=first.filter((v,j)=>v===Infinity&&!pins.has(j)).length;return Q.map(x=>x<<BigInt(free))}
function energy(Q,D,r){let v=0n;for(let a=0;a<D;a++)for(let b=0;b<D;b++)v+=BigInt(r[a]||0)*BigInt(r[b]||0)*Q[a*D+b];return v}
function direct(n,D,E,pins){let Q=Array(D*D).fill(0n);for(const x of words(Array.from({length:n},(_,j)=>j))){if([...pins].some(([j,b])=>Number(!!(x&bit(j)))!==b))continue;stats.reference++;let v=Array(D).fill(0n);v[0]=1n;for(const e of E)v[e.v]+=guard(e,x)*v[e.u];for(let a=0;a<D;a++)for(let b=0;b<D;b++)Q[a*D+b]+=v[a]*v[b]}return Q}
function cnf(n,C){return C.map((L,i)=>edge(i,i+1,L.map(x=>x[0]),[packet(1),packet(-1,L.map(([j,b])=>[bit(j),1-b]))]))}
function solve(n,C){let pins=closure(C,new Map);if(!pins)return {count:0};let E=cnf(n,C),D=C.length+1,r=Array(D).fill(0);r[D-1]=1;const Q=evaluate(n,D,E,pins);check(Q,direct(n,D,E,pins));let k=energy(Q,D,r);check(k,Q[D-1]); // Boolean readout: square and first moment agree, source compilation proves Booleanity
if(k){for(let j=0;j<n;j++){if(pins.has(j))continue;let p=closure(C,new Map([...pins,[j,0]]));if(p&&energy(evaluate(n,D,E,p),D,r)>0n)pins=p;else{pins=closure(C,new Map([...pins,[j,1]]));assert(pins)}}check(C.every(L=>L.some(([j,b])=>pins.get(j)===b)),true)}
return {count:Number(k),pins:[...pins]}}
function main(){const lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],C=lines.flatMap(L=>[L.map(j=>[j,0]),L.map(j=>[j,1])]);const fano=[solve(7,C),...C.map((_,i)=>solve(7,C.filter((_,j)=>i!==j)))];check(fano.map(x=>x.count),[0,...Array(14).fill(5)]);
let seed=12026;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};const random=[];
for(let k=0;k<32;k++){let n=5,D=5,E=[];for(let i=0;i<8;i++){let u=rnd(D-1),v=u+1+rnd(D-u-1);let scope=[...new Set([rnd(n),rnd(n),rnd(n)])];let a=scope.reduce((s,j)=>s|bit(j),0n);E.push(edge(u,v,scope,[packet(rnd(5)-2),packet(rnd(5)-2,[[a,rnd(2)]]),packet(rnd(5)-2,[[bit(scope[0]),rnd(2)]])]))}let p=new Map(k%2?[[rnd(n),rnd(2)]]:[]);check(evaluate(n,D,E,p),direct(n,D,E,p));random.push(k)}
let scaling=[];for(const n of [8,16,32,64]){let D=n+2,E=[];for(let j=0;j<n;j++)E.push(edge(0,j+1,[j],[packet(1,[[bit(j),1]])]));for(let j=0;j<n;j++){E.push(edge(j+1,n+1,[],[packet(1)]));E.push(edge(j+1,n+1,[],[packet(-1)]))}let r=Array(D).fill(0);r[n+1]=1;const A=evaluate(n,D,E);check(energy(A,D,r),0n);E.push(edge(0,n+1,[],[packet(1)]));const B=evaluate(n,D,E);check(energy(B,D,r),1n<<BigInt(n));scaling.push({n,liveVectors:(1n<<BigInt(n)).toString(),gramEntries:D*D,zeroEnergy:'0',oneEnergy:energy(B,D,r).toString()})}
let n=128,D=2,a=(1n<<128n)-1n,E=[edge(0,1,Array.from({length:n},(_,j)=>j),[packet(2),packet(-3,[[a,1]]),packet(5,[[bit(0),0]])])];let Q=evaluate(n,D,E),expected=(4n+1n+49n+16n)*(1n<<126n);check(Q[3],expected);return {fanoCounts:fano.map(x=>x.count),fanoWitnesses:fano.slice(1).map(x=>x.pins),randomSignedGramControls:random.length,scaling,highRank:{n,energy:Q[3].toString()},stats}}
const results=main();console.log(JSON.stringify(results,null,2));