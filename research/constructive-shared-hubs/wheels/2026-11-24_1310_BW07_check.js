"use strict";
function experiment(){
 const stat={gaussianCalls:0,xors:0,closureSweeps:0,forced:0,deleted:0,subsetCalls:0,searchNodes:0,cycleSweeps:0,arcTests:0,dpEdges:0,bruteWords:0,referenceSelectors:0,lifts:0,assertions:0};
 function ok(x){stat.assertions++;if(!x)throw Error("assertion "+stat.assertions);}
 let seed=20261124;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;}
 function par(x){let p=0;while(x){p^=1;x&=x-1n;}return p;}
 function ev(a,z){return par(a&((z<<1n)|1n));}
 function col(a,z){return ev(a[0],z)+2*ev(a[1],z);}
 function con(c){return [BigInt(c&1),BigInt(c>>1)];}
 function add(a,b){return [a[0]^b[0],a[1]^b[1]];}
 function eq(a,b){return add(a,b);}
 function basis(rows){stat.gaussianCalls++;let B=new Map();for(let x of rows){while(x>1n){let j=x.toString(2).length-1;if(!B.has(j)){B.set(j,x);x=0n;break;}x^=B.get(j);stat.xors++;}if(x===1n)return null;}return B;}
 function count(n,rows){let b=basis(rows);return b===null?0n:1n<<BigInt(n-b.size);}
 function bad(C){let {a,b,s}=C,L=a.length;let h=s.reduce((x,y)=>x^y,0);let E=[];for(let d=1;d<4;d++){if(h!==((L%2===0)?d:0))continue;let rows=[];for(let i=0;i<L;i++){rows.push(...eq(add(a[i],b[i]),con(d)));let q=add(add(a[i],a[(i+1)%L]),con(s[i]));rows.push(d===1?q[1]:d===2?q[0]:q[0]^q[1]);}E.push(rows);}return E;}
 function close(n,G,E){G=G.slice();E=E.slice();for(;;){stat.closureSweeps++;let g=count(n,G);if(!g)return null;let restart=false;for(let i=0;i<E.length;i++){let c=count(n,G.concat(E[i]));if(!c){E.splice(i,1);stat.deleted++;restart=true;break;}if(c===g)return null;if(c*2n===g){let f=E[i].find(x=>count(n,G.concat([x]))<g);ok(f!==undefined);G.push(f^1n);stat.forced++;restart=true;break;}}if(!restart)return {G,E};}}
 function small(n,G,E){let ans=0n;for(let mask=0;mask<(1<<E.length);mask++){stat.subsetCalls++;let r=G.slice(),k=0;for(let j=0;j<E.length;j++)if(mask>>j&1){r.push(...E[j]);k++;}ans+=(k%2?-1n:1n)*count(n,r);}return ans;}
 function solve(n,G,E,want=true){stat.searchNodes++;let c=close(n,G,E);if(!c)return {N:0n,z:null};({G,E}=c);if(E.length<=3){let N=small(n,G,E);if(!N||!want)return {N,z:null};let z=0n;for(let i=0;i<n;i++){let bit=1n<<BigInt(i+1),g=G.concat([bit]);let q=close(n,g,E);if(q&&small(n,q.G,q.E)>0n){G=q.G;E=q.E;}else{z|=1n<<BigInt(i);q=close(n,G.concat([bit^1n]),E);ok(q!==null);G=q.G;E=q.E;}}return {N,z};}
 // General fallback: a strict guard-rank increase; exact OR/sum of disjoint children.
 let g=count(n,G),i=0;for(;i<n;i++)if(count(n,G.concat([1n<<BigInt(i+1)]))*2n===g)break;ok(i<n);let bit=1n<<BigInt(i+1),p=solve(n,G.concat([bit]),E,want),q=solve(n,G.concat([bit^1n]),E,want&&!p.N);return {N:p.N+q.N,z:p.N?p.z:q.z};}
 function fixed(C,z){return {a:C.a.map(x=>col(x,z)),b:C.b.map(x=>col(x,z)),s:C.s};}
 function dp(C){let {a,b,s}=C,L=a.length;let D=a.map((v,i)=>[0,1,2,3].filter(x=>x!==v&&x!==b[i]));for(;;){stat.cycleSweeps++;let change=false;for(let i=0;i<L;i++){let j=(i+1)%L;for(let [u,v] of [[i,j],[j,i]]){let keep=D[u].filter(x=>D[v].some(y=>{stat.arcTests++;return (x^y)!==s[i];}));if(!keep.length)return {N:0n,w:null};if(keep.length!==D[u].length){D[u]=keep;change=true;}}}if(!change)break;}
 let N=0n,w=null;for(let start of D[0]){let M=new Map([[start,{N:1n,w:[start]}]]);for(let i=1;i<L;i++){let K=new Map();for(let [x,t] of M)for(let y of D[i]){stat.dpEdges++;if((x^y)===s[i-1])continue;let old=K.get(y);if(old)old.N+=t.N;else K.set(y,{N:t.N,w:t.w.concat(y)});}M=K;}for(let [x,t] of M)if((x^start)!==s[L-1]){N+=t.N;if(!w)w=t.w;}}
 if(w){ok(w.every((x,i)=>x!==a[i]&&x!==b[i]&&(x^w[(i+1)%L])!==s[i]));stat.lifts++;}return {N,w};}
 function brute(C){let {a,b,s}=C,L=a.length;let N=0n;function rec(w){if(w.length===L){stat.bruteWords++;if((w[L-1]^w[0])!==s[L-1])N++;return;}let i=w.length;for(let x=0;x<4;x++)if(x!==a[i]&&x!==b[i]&&(!i||(x^w[i-1])!==s[i-1]))rec(w.concat(x));}rec([]);return N;}
 function hit(E,z){return E.some(e=>e.every(f=>ev(f,z)===0));}
 let triangle={SAT:0,UNSAT:0},randomFixed={SAT:0,UNSAT:0},randomChart={SAT:0,UNSAT:0},cube={SAT:0,UNSAT:0},fano={SAT:0,UNSAT:0};
 function fixedCheck(a,b,s,tot){let C={a:a.map(con),b:b.map(con),s};let N=dp({a,b,s}).N;ok(N===brute({a,b,s}));ok((N===0n)===hit(bad(C),0n));tot[N?"SAT":"UNSAT"]++;}
 for(let k=0;k<4096;k++){let a=[],b=[];for(let i=0;i<3;i++){a.push(k>>(4*i)&3);b.push(k>>(4*i+2)&3);}fixedCheck(a,b,[0,0,0],triangle);}
 for(let k=0;k<800;k++){let L=3+rnd(5);let rand=()=>Number((rnd(65536)>>>8)%4);fixedCheck(Array.from({length:L},rand),Array.from({length:L},rand),Array.from({length:L},rand),randomFixed);}
 // random affine maps, independent exact fixed-color DP as oracle.
 for(let k=0;k<120;k++){let n=1+rnd(5),L=3+rnd(6);let f=()=>BigInt(rnd(1<<(n+1)));let a=Array.from({length:L},()=>[f(),f()]),b=Array.from({length:L},()=>[f(),f()]),s=Array.from({length:L},()=>rnd(4));let C={a,b,s},G=k%3===0?[f()]:[];let E=bad(C),N=0n;for(let z=0n;z<1n<<BigInt(n);z++){stat.referenceSelectors++;if(G.some(f=>ev(f,z)))continue;let r=dp(fixed(C,z));ok((!r.N)===hit(E,z));if(r.N)N++;}let R=solve(n,G,E);ok(R.N===N);if(R.N)ok(G.every(f=>!ev(f,R.z))&&dp(fixed(C,R.z)).N>0n);randomChart[N?"SAT":"UNSAT"]++;}
 function lit(l){return (1n<<BigInt(Math.abs(l)))^(l<0?1n:0n);}
 function clause(C){let a=[con(0),...C.map(l=>[0n,lit(l)]),con(0)];return {a,b:a.map(v=>add(v,con(1))),s:a.map(()=>0)};}
 function source(n,F,tot){let cycles=F.map(clause),E=cycles.flatMap(bad),N=0n;for(let z=0n;z<1n<<BigInt(n);z++){stat.referenceSelectors++;let truth=F.every(c=>c.some(l=>ev(lit(l),z)));ok(truth===!hit(E,z));if(truth)N++;}let R=solve(n,[],E);ok(R.N===N);if(R.N){ok(F.every(c=>c.some(l=>ev(lit(l),R.z))));for(let C of cycles)ok(dp(fixed(C,R.z)).N>0n);}tot[N?"SAT":"UNSAT"]++;return Number(N);}
 let C8=Array.from({length:8},(_,j)=>[1,2,3].map((v,i)=>j>>i&1?-v:v));for(let mask=0;mask<256;mask++)source(3,C8.filter((_,i)=>mask>>i&1),cube);
 let lines=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]],F=lines.flatMap(c=>[c,c.map(x=>-x)]);ok(source(7,F,fano)===0);for(let i=0;i<F.length;i++)ok(source(7,F.filter((_,j)=>i!==j),fano)===5);
 let scaling=[];for(let L of [5,17,65,129,128]){let n=L-1,a=[con(0),...Array.from({length:n},(_,i)=>[0n,1n<<BigInt(i+1)])],s=a.map(()=>0);if(L%2===0)s[0]=1;let C={a,b:a.map(x=>add(x,con(1))),s},E=bad(C),R=solve(n,[],E),G=Array.from({length:n},(_,i)=>1n<<BigInt(i+1));ok(R.N===(1n<<BigInt(n))-1n);ok(dp(fixed(C,R.z)).N>0n);ok(solve(n,G,E).N===0n);scaling.push({L,n,events:E.length,projectedCount:String(R.N),unsatPinned:true});}
 // Explicit duplicate BW06 rim rule, all shared endpoint/sign words, all three twists.
 let wheel={queries:0,balancedTriples:0};for(let L of [3,5,7,9])for(let A=0;A<4;A++)for(let B=0;B<4;B++)for(let S=0;S<4;S++){let M=1n;for(let t=1;t<4;t++){let a=Array.from({length:L},(_,i)=>i===0?A^t:A),b=Array.from({length:L},(_,i)=>i===0?B^S:B^S^t),s=a.map(()=>0);let r=dp({a,b,s}),d=A^B^S;let exact=d===0?0n:d===t?(17n*(1n<<BigInt(L-2))-4n)/3n:4n;ok(r.N===exact);ok((!r.N)===hit(bad({a:a.map(con),b:b.map(con),s}),0n));M*=r.N;wheel.queries++;}ok(M===((A^B^S)===0?0n:16n*(17n*(1n<<BigInt(L-2))-4n)/3n));wheel.balancedTriples++;}
 let mult=[dp({a:[0,0,0],b:[0,0,0],s:[0,0,0]}).N,dp({a:[0,0,0],b:[1,1,2],s:[0,0,0]}).N].map(String);ok(mult[0]==="6"&&mult[1]==="2");
 return {seed:20261124,triangle,randomFixed,randomChart,cube,fano,scaling,wheel,multiplicityCounterexample:mult,stat};
}
console.log(JSON.stringify(experiment(),null,2));
