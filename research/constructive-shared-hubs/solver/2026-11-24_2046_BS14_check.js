// Run: node 2026-11-24_2046_BS14_check.js
function experiment(){
 const L={nodes:0,scans:0,gauss:0,pairs:0,single:0,fused:0,pins:0,branches:0,match:0,aug:0,count:0,countWords:0,reference:0,verified:0,maxMass:0,assertions:0};
 const bit=i=>1n<<BigInt(i);
 const parity=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
 const ev=(r,x)=>parity(r[0]&x)===r[1];
 const bad=(P,x)=>P.every(r=>ev(r,x));
 const sat=(F,x)=>F.every(P=>!bad(P,x));
 function ok(b){L.assertions++;if(!b)throw Error("assertion "+L.assertions)}
 function rref(rows,n){L.gauss++;let a=rows.map(r=>r.slice()),k=0,piv=[];for(let j=0;j<n;j++){let i=a.findIndex((r,i)=>i>=k&&(r[0]&bit(j))!==0n);if(i<0)continue;[a[k],a[i]]=[a[i],a[k]];for(let h=0;h<a.length;h++)if(h!==k&&(a[h][0]&bit(j)))a[h]=[a[h][0]^a[k][0],a[h][1]^a[k][1]];piv.push(j);k++}if(a.slice(k).some(r=>r[1]))return null;return {rows:a.slice(0,k),piv}}
 function solution(rows,n){const a=rref(rows,n);if(!a)return null;return a.rows.reduce((x,r,i)=>x|(r[1]?bit(a.piv[i]):0n),0n)}
 function nullspace(rows,n){let a=rref(rows.map(r=>[r[0],0]),n);let p=new Set(a.piv),B=[];for(let j=0;j<n;j++)if(!p.has(j)){let v=bit(j);a.rows.forEach((r,i)=>{if(r[0]&bit(j))v|=bit(a.piv[i])});B.push(v)}return B}
 function canon(F,n){let out=[],seen=new Set;for(let P of F){let a=rref(P,n);if(!a)continue;let k=a.rows.map(r=>r.join(":")).join(",");if(!seen.has(k)){out.push(a.rows);seen.add(k)}}return out}
 function transform(F,v,c){let j=0;while(!(v&bit(j)))j++;let b=bit(j);return {F:F.map(P=>P.map(([a,d])=>[a&~b,d^(parity(a&v)*c)])),j}}
 function restrict(F,a,b,n){let j=0;while(!(a&bit(j)))j++;let p=bit(j);return {F:F.map(P=>P.map(([r,s])=>(r&p)?[r^a,s^b]:[r,s])),lift:z=>z|(parity(a&z)^b? p:0n)}}
 // Repeated packet-unit closure: unit complement is necessary, not a guessed guard.
 function solve(F,n,allowCount=true){L.nodes++;F=canon(F,n);L.maxMass=Math.max(L.maxMass,F.reduce((s,P)=>s+P.length,0));L.scans++;
 if(F.some(P=>!P.length))return null;if(!F.length)return 0n;
 const unit=F.find(P=>P.length===1);
 if(unit){L.pins++;let q=restrict(F,unit[0][0],1^unit[0][1],n);let z=solve(q.F,n,allowCount);return z===null?null:q.lift(z)}
 // Find a private direction affecting one or two packets, on the same chart.
 let sel=null;
 for(let size=1;size<=2&&!sel;size++)for(let i=0;i<F.length&&!sel;i++)for(let j=(size===1?i:i+1);j<(size===1?i+1:F.length)&&!sel;j++){
 L.pairs++;let B=nullspace(F.filter((_,k)=>k!==i&&k!==j).flat(),n);
 let u=B.find(v=>F[i].some(r=>parity(r[0]&v)));if(!u)continue;
 if(i===j){sel={i,j,v:u};break}
 let w=B.find(v=>F[j].some(r=>parity(r[0]&v)));if(!w)continue;
 let v=F[j].some(r=>parity(r[0]&u))?u:F[i].some(r=>parity(r[0]&w))?w:u^w;
 sel={i,j,v};
 }
 if(sel){let {i,j,v}=sel;let p=1n;while(!(p&v))p<<=1n;
 function split(P){let a=P.find(r=>parity(r[0]&v));return {a,rest:P.filter(r=>r!==a).map(r=>parity(r[0]&v)?[r[0]^a[0],r[1]^a[1]]:r).map(([m,b])=>[m&~p,b])}}
 let G=F.filter((_,k)=>k!==i&&k!==j).map(P=>P.map(([m,b])=>[m&~p,b]));
 if(i===j)L.single++;
 else {L.fused++;let A=split(F[i]),B=split(F[j]);G.push([...A.rest,...B.rest,[(A.a[0]^B.a[0])&~p,A.a[1]^B.a[1]^1]])}
 let z=solve(G,n,allowCount);if(z===null)return null;z&=~p;
 if(sat(F,z))return z;if(sat(F,z^v))return z^v;throw Error("lift");
 }
 // Coordinate-clause matching/flow terminal. Distinct owner pivot satisfies each clause.
 if(F.every(P=>P.every(([a])=>(a&(a-1n))===0n))){
 let occ=new Map;for(let P of F)for(let [a] of P)occ.set(a,(occ.get(a)||0)+1);
 if([...occ.values()].every(c=>c<=2)){
 L.match++;let owner=new Map;
 function augment(i,seen){for(let [a] of F[i])if(!seen.has(a)){seen.add(a);if(!owner.has(a)||augment(owner.get(a),seen)){owner.set(a,i);return true}}return false}
 for(let i=0;i<F.length;i++){ok(augment(i,new Set));L.aug++}
 let x=0n;for(let [a,i] of owner){let r=F[i].find(r=>r[0]===a);if(!r[1])x|=a}ok(sat(F,x));return x;
 }}
 // Bounded observation-rank support count. Enumerate syndrome, not hidden coordinates.
 let A=rref(F.flat().map(r=>[r[0],0]),n).rows;
 if(allowCount && A.length<=Math.floor(Math.log2(2+n+F.length))){L.count++;let witness=null;for(let t=0;t<2**A.length;t++){L.countWords++;let x=solution(A.map((r,i)=>[r[0],(t>>i)&1]),n);if(sat(F,x)&&witness===null)witness=x}return witness}
 // Complete guarded fallback: branch on one observed linear form, not a free hidden coordinate.
 L.branches++;let a=F[0][0][0];for(let b of [0,1]){let q=restrict(F,a,b,n);let z=solve(q.F,n,allowCount);if(z!==null)return q.lift(z)}return null;
 }
 const clause=ls=>ls.map(v=>[bit(Math.abs(v)-1),v<0?1:0]);
 const nae=(a,b,c,sign=0)=>[[bit(a)^bit(b),((sign>>0)^(sign>>1))&1],[bit(a)^bit(c),((sign>>0)^(sign>>2))&1]];
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const original=fano.map(t=>nae(...t));
 let results={fano:[],sign:[],budget:[],random:{SAT:0,UNSAT:0},scaling:[],dense:[],counterexample:null};
 function test(F,n,expected,ref=true){let x=solve(F,n);let cnt=0;if(ref){for(let y=0n;y<bit(n);y++){L.reference++;if(sat(F,y))cnt++}ok((x!==null)===(cnt>0));if(expected!==undefined)ok(cnt===expected)}else if(expected!==undefined)ok((x!==null)===expected);if(x!==null){ok(sat(F,x));L.verified++}return ref?cnt:x!==null}
 results.fano.push(test(original,7,0));
 for(let i=0;i<7;i++){for(let s of [1,2,4])results.sign.push(test(original.map((P,j)=>j===i?nae(...fano[i],s):P),7,10));for(let b of [0,1]){let P=fano[i].map(j=>[bit(j),b]);results.budget.push(test(original.map((Q,j)=>j===i?P:Q),7,5))}}
 let seed=314159;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 for(let t=0;t<160;t++){let n=3+rnd(5),F=[];for(let i=0,m=2+rnd(12);i<m;i++){let P=[];for(let j=0,r=1+rnd(3);j<r;j++)P.push([BigInt(1+rnd(2**n-1)),rnd(2)]);F.push(P)}let c=test(F,n);results.random[c?"SAT":"UNSAT"]++}
 // Dense change of basis hides all ordinary coordinate-private pivots.
 for(let n of [8,16,32]){let form=i=>i===0?bit(0):bit(i)^bit(0);let F=[];for(let i=1;i<n-1;i+=2){F.push([[form(i),0],[form(i+1),0]],[[form(i),1],[form(i+1),0]])}let before=L.fused;let z=test(F,n,true,false);results.dense.push({n,SAT:z,fusions:L.fused-before})}
 // A long resolution chain. Add endpoint pins only after construction: closure may solve those controls.
 for(let n of [16,32,64]){let F=[];for(let i=1;i<n;i++)F.push(clause([-i,i+1]));let before=L.single+L.fused;let yes=test(F,n,true,false);let no=test([...F,clause([1]),clause([-n])],n,false,false);results.scaling.push({n,yes,no,eliminations:L.single+L.fused-before})}
 // All seven NAE planes remain when no <=2-private direction exists.
 let base=canon(original,7),eligible=0;
 for(let i=0;i<7;i++)for(let j=i;j<7;j++){let B=nullspace(base.filter((_,k)=>k!==i&&k!==j).flat(),7);if(B.some(v=>base[i].some(r=>parity(r[0]&v))&&base[j].some(r=>parity(r[0]&v))))eligible++}
 ok(eligible===0);results.counterexample={fanoEligiblePairs:eligible};
 return {results,ledger:L,seed:314159};
}
console.log(JSON.stringify(experiment(), null, 2));
