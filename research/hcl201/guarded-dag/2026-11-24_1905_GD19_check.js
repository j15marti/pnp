"use strict";
function run(){
const K=4, stats={eventTransitions:0,merges:0,peakKeys:0,hankelSystems:0,closureScans:0,forcedPins:0,referenceWords:0,witnessChecks:0,alphabetDeclines:0};
const abs=x=>x<0n?-x:x;
function gcd(a,b){a=abs(a);b=abs(b);while(b){[a,b]=[b,a%b]}return a||1n}
function q(a,b=1n){if(!b)throw Error("zero denominator");if(b<0n){a=-a;b=-b}let g=gcd(a,b);return [a/g,b/g]}
const add=(a,b)=>q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]), neg=a=>[-a[0],a[1]], mul=(a,b)=>q(a[0]*b[0],a[1]*b[1]), div=(a,b)=>q(a[0]*b[1],a[1]*b[0]);
function solve(A,b){stats.hankelSystems++;let n=b.length,M=A.map((r,i)=>[...r,b[i]].map(z=>q(z)));for(let i=0;i<n;i++){let j=M.findIndex((r,j)=>j>=i&&r[i][0]);if(j<0)return null;[M[i],M[j]]=[M[j],M[i]];let a=M[i][i];M[i]=M[i].map(x=>div(x,a));for(j=0;j<n;j++)if(j!==i){let c=M[j][i];M[j]=M[j].map((x,k)=>add(x,neg(mul(c,M[i][k]))))}}return M.map(r=>r[n])}
const choose=Array.from({length:2*K+1},(_,i)=>Array.from({length:i+1},(_,j)=>{let r=1n;for(let a=1;a<=j;a++)r=r*BigInt(i-a+1)/BigInt(a);return r}));
function assert(b,msg){if(!b)throw Error(msg)}
function ev(v,pat,a){return {v,pat,a:BigInt(a)}}
const scope=S=>[...new Set(S.flatMap(e=>e.v))].sort((a,b)=>a-b);
function weight(e,x){let p=0;for(let i=0;i<e.v.length;i++)if((x>>BigInt(e.v[i]))&1n)p|=1<<i;return p===e.pat?e.a:0n}
function value(S,x){return S.reduce((a,e)=>a+weight(e,x),0n)}
function schedule(stages){let es=stages.flat(), first=new Map(),last=new Map();es.forEach((e,i)=>e.v.forEach(v=>{if(!first.has(v))first.set(v,i);last.set(v,i)}));return {es,first,last}}
function sweep(stages,D,polys=null,pins=new Map()){
 let {es,first,last}=schedule(stages),T=new Map([[0n,[1n,...Array(D).fill(0n)]]]),i=0;
 for(let si=0;si<stages.length;si++){
  for(const e of stages[si]){
   let fresh=e.v.filter(v=>first.get(v)===i),dead=e.v.filter(v=>last.get(v)===i),R=new Map();
   for(const [key,M] of T){
    for(let b=0;b<2**fresh.length;b++){
     let x=key,ok=true;for(let j=0;j<fresh.length;j++){let v=fresh[j],bit=(b>>j)&1;if(pins.has(v)&&pins.get(v)!==bit){ok=false;break}if(bit)x|=1n<<BigInt(v)}if(!ok)continue;
     stats.eventTransitions++;let g=weight(e,x),pw=[1n];for(let k=1;k<=D;k++)pw.push(pw[k-1]*g);
     let V=M.map((_,k)=>{let s=0n;for(let j=0;j<=k;j++)s+=choose[k][j]*M[j]*pw[k-j];return s});
     for(let v of dead)x&=~(1n<<BigInt(v));let old=R.get(x);if(old){stats.merges++;V=V.map((z,k)=>z+old[k])}R.set(x,V);
    }
   }T=R;stats.peakKeys=Math.max(stats.peakKeys,T.size);i++;
  }
  if(polys){let R=new Map();for(let [key,M] of T){let z=polys[si].reduce((s,a,j)=>add(s,mul(a,q(M[j]))),q(0n));assert(z[1]===1n&&z[0]>=0n,"invalid projected mass");if(z[0])R.set(key,[z[0],...Array(D).fill(0n)])}T=R}
 }return T.get(0n)||Array(D+1).fill(0n);
}
function polynomial(S){
 let m=sweep([S],2*K);
 for(let k=1;k<=K;k++){let c=solve(Array.from({length:k},(_,i)=>Array.from({length:k},(_,j)=>m[i+j])),Array.from({length:k},(_,i)=>-m[i+k]));if(!c)continue;let p=[...c,q(1n)],norm=q(0n);for(let i=0;i<=k;i++)for(let j=0;j<=k;j++)norm=add(norm,mul(mul(p[i],p[j]),q(m[i+j])));if(norm[0]!==0n)continue;
  if(p[0][0]!==0n)return {k,zero:[q(0n)]};assert(p[1][0]!==0n,"multiple zero root");return {k,zero:p.slice(1).map(a=>div(a,p[1]))};
 }stats.alphabetDeclines++;return null
}
function closure(stages,pins){
 let archive=new Set(),change=true;
 while(change){change=false;for(let si=0;si<stages.length;si++){
  let S=stages[si],vs=scope(S);if(vs.length>12)continue;stats.closureScans++;let allowed=[];
  for(let b=0;b<2**vs.length;b++){let x=0n,ok=true;vs.forEach((v,j)=>{let bit=(b>>j)&1;if(pins.has(v)&&pins.get(v)!==bit)ok=false;if(bit)x|=1n<<BigInt(v)});if(ok&&value(S,x)===0n)allowed.push(b)}
  if(!allowed.length)return {ok:false,archive};
  const parity=x=>{let p=0;while(x){p^=1;x&=x-1}return p};
  for(let a=1;a<2**vs.length;a++){let rhs=parity(a&allowed[0]);if(allowed.every(b=>parity(a&b)===rhs)){archive.add(vs.filter((_,j)=>(a>>j)&1).join(",")+"="+rhs);if((a&(a-1))===0){let v=vs[Math.log2(a)];if(!pins.has(v)){pins.set(v,rhs);stats.forcedPins++;change=true}}}}
  if(change)break; // restart after a deduction pass
 }}return {ok:true,archive}
}
function count(n,stages,polys,pins0=new Map(),close=true){let pins=new Map(pins0);if(close&&!closure(stages,pins).ok)return 0n;if(!polys||polys.some(p=>!p))return null;let M=sweep(stages,K,polys.map(p=>p.zero),pins),used=new Set(stages.flatMap(scope));let free=0;for(let i=0;i<n;i++)if(!used.has(i)&&!pins.has(i))free++;return M[0]*(1n<<BigInt(free))}
function brute(n,stages){let c=0n;for(let b=0;b<2**n;b++){stats.referenceWords++;if(stages.every(S=>value(S,BigInt(b))===0n))c++}return c}
function check(n,stages,expected=null,witness=true){let rootpins=new Map();let cl=closure(stages,rootpins);let polys=stages.map(polynomial);assert(polys.every(Boolean),"unexpected alphabet decline");let c=count(n,stages,polys,rootpins);let ref=expected===null?brute(n,stages):expected;assert(c===ref,"count mismatch "+c+" "+ref);if(c&&witness){let pins=new Map(rootpins);for(let i=0;i<n;i++){if(pins.has(i))continue;let trial=new Map(pins);trial.set(i,0);if(count(n,stages,polys,trial)>0n)pins=trial;else pins.set(i,1);assert(closure(stages,pins).ok,"witness closure");}let x=0n;for(let [v,b] of pins)if(b)x|=1n<<BigInt(v);assert(stages.every(S=>value(S,x)===0n),"bad witness");stats.witnessChecks++}return {count:c.toString(),alphabetMax:Math.max(0,...polys.map(p=>p.k)),initialClosure:cl.ok,initialPins:rootpins.size}}
const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
function fStages(flip=-1,del=-1){return fano.map((v,i)=>{let p=Math.floor(flip/3)===i?1<<(flip%3):0;let a=1n<<BigInt(i*3);return [ev(v,p,a),ev(v,p^7,a)].filter((_,j)=>2*i+j!==del)})}
let results={fano:[],random:[],scaling:[],kernel:[]};
results.fano.push(check(7,fStages()));for(let i=0;i<21;i++)results.fano.push(check(7,fStages(i)));for(let i=0;i<14;i++)results.fano.push(check(7,fStages(-1,i)));
let seed=1919;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
for(let t=0;t<40;t++){let ss=[];for(let j=0;j<5;j++){let v=[...new Set([rand(7),rand(7),rand(7)])];let a=BigInt(1+rand(20));ss.push([ev(v,rand(2**v.length),a),ev(v,rand(2**v.length),-a),ev(v,rand(2**v.length),a)])}results.random.push(check(7,ss))}
for(let m of [8,32,128]){let ss=Array.from({length:m},(_,i)=>[ev([2*i,2*i+1],3,1n<<BigInt(i))]);results.scaling.push({m,label:"SAT",...check(2*m,ss,3n**BigInt(m),false),globalSumDistinct:(1n<<BigInt(m)).toString()});let tt=[...ss,[ev([],0,1n)]];results.scaling.push({m,label:"UNSAT",...check(2*m,tt,0n,false)})}
// High-local-rank kernel: 96 private coordinates cancel pairwise, final output depends on one bit.
let S=[];for(let i=0;i<96;i++)S.push(ev([i],1,1n<<BigInt(i)),ev([i],1,-(1n<<BigInt(i))));S.push(ev([96],1,1n<<200n));
let p=polynomial(S);assert(p&&p.k===2,"high-rank alphabet");let c=count(97,[S],[p],new Map(),false);assert(c===1n<<96n,"high-rank count");results.kernel.push({case:"96 canceling bits plus one",count:c.toString(),alphabet:p.k,closure:"not executed for this kernel-only test"});
let U=Array.from({length:8},(_,i)=>ev([i],1,1n<<BigInt(i)));assert(polynomial(U)===null,"unbounded alphabet accepted");results.kernel.push({case:"256 distinct outputs",result:"UNKNOWN at K=4"});
return {K,results,stats};
}
console.log(JSON.stringify(run(),null,2));
