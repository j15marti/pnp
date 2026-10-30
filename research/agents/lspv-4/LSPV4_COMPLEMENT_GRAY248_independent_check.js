'use strict';
/* LSPV-4 COMPLEMENT-GRAY248 independently written, dependency-free checker.
   Verify original occurrence targets, pair-mode compatibility, complement
   Gray orbits, strict22 degrees, SAT/UNSAT controls, and a direct source cube. */
const assert=require('node:assert/strict');
const H0=[[1,3,5],[1,-3,6],[-1,4,5],[-1,-4,6],[2,3,-5],[2,-3,-6],[-2,4,-5],[-2,-4,-6]];
const W='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14';
const W1=W.split(';').map(s=>s.trim().split(/\s+/).map(Number));
const Wprime=W1.map(c=>c.slice());
assert(Wprime[7][0]===1 && Wprime[19][0]===-1);
Wprime[7][0]=-1;Wprime[19][0]=1;
function H(r){const out=[];for(let j=0;j<r;j++)for(let k=0;k<8;k++)
  out.push(H0[k].map((v,h)=>Math.sign(v)*(6*((k===0&&h===0)?(j+r-1)%r:j)+Math.abs(v))));return out;}
function truth(l,a){return Number((a>>(Math.abs(l)-1))&1)===(l>0?1:0);}
function value(c,a){let s=0;for(const l of c)if(truth(l,a))s++;return s;}
function counts(F,a){const x=[0,0,0,0];for(const c of F)x[value(c,a)]++;return x;}
function local(c,mode){const d=new Map();for(const l of c)d.set(Math.abs(l),mode==='S'?Number(l>0):Number(l<0));return d;}
function pairFast(c,d){const a=local(c,'S'),b=local(d,'S'),eq=[],neq=[];
  for(const [v,z] of a)if(b.has(v))(z===b.get(v)?eq:neq).push(v);
  return {SS:neq.length===0,SU:eq.length===0,US:eq.length===0,UU:neq.length===0};}
function pairBrute(c,d){const vs=[...new Set([...c,...d].map(Math.abs))];const z={SS:false,SU:false,US:false,UU:false};
 for(let mask=0;mask<(1<<vs.length);mask++){
  let a=0;for(let j=0;j<vs.length;j++)a|=((mask>>j)&1)<<(vs[j]-1);
  const x=value(c,a),y=value(d,a);
  if(x===3&&y===3)z.SS=true;if(x===3&&y===0)z.SU=true;
  if(x===0&&y===3)z.US=true;if(x===0&&y===0)z.UU=true;
 }return z;}
function signed22(F,n){let pos=new Array(n).fill(0),neg=new Array(n).fill(0);
 for(const c of F){assert(c.length===3);assert(new Set(c.map(Math.abs)).size===3);
  for(const l of c)(l>0?pos:neg)[Math.abs(l)-1]++;}
 return pos.every(x=>x===2)&&neg.every(x=>x===2);}
function complementCheck(F,n){let all=(1<<n)-1,models=0,repModels=0,complementModels=0;
 let orbit=new Set(),flips=0,touches=0;let a=0,prev=0,t=F.map(c=>value(c,0));
 const O=Array.from({length:n},()=>[]);
 for(let j=0;j<F.length;j++)for(const l of F[j])O[Math.abs(l)-1].push([j,l>0]);
 let survival={both:0,direct:0,complement:0,neither:0};
 for(let k=0;k<(1<<(n-1));k++){
  a=k^(k>>1);const b=a^all;
  assert.equal((a>>(n-1))&1,0);assert.equal((b>>(n-1))&1,1);
  assert(!orbit.has(a)&&!orbit.has(b));orbit.add(a);orbit.add(b);
  if(k){const flip=(k&(-k)).toString(2).length-1;
   assert.equal((a^prev),(1<<flip));flips++;
   const old=(prev>>flip)&1;
   for(const [j,p] of O[flip]){t[j]+=(old===Number(p)?-1:1);touches++;}
  }
  assert.deepEqual(t,F.map(c=>value(c,a)));
  const p=counts(F,a),q=counts(F,b);assert.deepEqual(p,q.slice().reverse());
  let ds=p[0]===0,cs=p[3]===0;
  if(ds&&cs)survival.both++;
  else if(ds)survival.direct++;
  else if(cs)survival.complement++;
  else survival.neither++;
  models+=Number(ds)+Number(cs);repModels+=Number(ds);complementModels+=Number(cs);
  prev=a;
 }
 assert.equal(orbit.size,1<<n);
 if(signed22(F,n))assert.equal(touches,4*((1<<(n-1))-1));
 return {n,m:F.length,models,flips,touches,repModels,complementModels,survival};
}
function checkPairModes(F){let count=0;for(let j=0;j<F.length;j++){
  const S=local(F[j],'S'),U=local(F[j],'U');
  for(const [v,z] of S)assert.equal(z,1-U.get(v));
  for(let k=j+1;k<F.length;k++){assert.deepEqual(pairFast(F[j],F[k]),pairBrute(F[j],F[k]));count+=4;}
}return count;}
const h1=H(1),h2=H(2),h3=H(3);
for(const [F,n] of [[h1,6],[h2,12],[h3,18],[W1,15],[Wprime,15]])assert(signed22(F,n));
let h1pair=pairFast(h1[0],h1[1]);assert(Object.values(h1pair).every(z=>!z));
const resolvent=[1,5,6];
for(let a=0;a<(1<<6);a++)if(resolvent.every(l=>!truth(l,a)))
 assert(!(value(h1[0],a)>0&&value(h1[1],a)>0));
const a= [complementCheck(h1,6),complementCheck(h2,12),complementCheck(h3,18),
          complementCheck(W1,15),complementCheck(Wprime,15)];
assert.deepEqual(a.map(x=>x.models),[4,26,124,0,168]);
assert.deepEqual(counts(W1,0),[1,10,7,2]);
assert.deepEqual(counts(Wprime,0),[1,10,7,2]);
assert.deepEqual(counts(W1,(1<<15)-1),[2,7,10,1]);
assert.deepEqual(counts(Wprime,(1<<15)-1),[2,7,10,1]);
assert.equal(a[3].flips,16383);assert.equal(a[3].touches,65532);
assert.equal(a[3].survival.neither,16384);
assert.deepEqual([a[4].survival.direct,a[4].survival.complement,a[4].survival.neither],
  [74,94,16216]);
const modes=[h1,W1,Wprime].reduce((s,F)=>s+checkPairModes(F),0);
console.log(JSON.stringify({PASS:true,formula_summaries:a,verified_four_modes:modes,
  original_forbidden_cube:{parents:[0,1],pivot:3,resolvent:[1,5,6],forbidden:[1,5,6].map(x=>[x,0])},
  scope:'five complete source/Gray controls, not arbitrary SAT complexity'}));