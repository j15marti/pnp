'use strict';
// Independent source-indexed checker, no imported Python or third-party packages.
const assert=require('node:assert/strict');
const base=[[1,3,5],[1,-3,6],[-1,4,5],[-1,-4,6],[2,3,-5],[2,-3,-6],[-2,4,-5],[-2,-4,-6]];
const w1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'.split(';').map(s=>s.trim().split(' ').map(Number));
const w1prime=w1.map(c=>c.slice()); w1prime[9][1]=6;w1prime[13][1]=-6;
const k4=[[1,2,3],[1,4,5],[2,4,6],[3,5,6]];const paired=k4.concat(k4.map(c=>c.map(l=>-l)));
function tr(l,a){return ((a>>>(Math.abs(l)-1))&1)===(l>0?1:0)}
function tc(c,a){return c.reduce((z,l)=>z+Number(tr(l,a)),0)}
function N(F,a){let h=[0,0,0,0];for(let c of F)h[tc(c,a)]++;return h}
function score(F,a,i){
 let r=0,b=0;
 for(let c of F)if(c.some(l=>Math.abs(l)===i)){
  let z=tc(c,a);if(z===0)r++;
  if(z===1&&c.some(l=>Math.abs(l)===i && tr(l,a)))b++;
 }
 return r-b;
}
function local(c,mode){let m={};for(let l of c)m[Math.abs(l)]= mode==='S'?(l>0?1:0):(l>0?0:1);return m}
function compatibility(c,d){let out={};for(let m of ['S','U'])for(let n of ['S','U']){
 let a=local(c,m),b=local(d,n);out[m+n]=Object.keys(a).every(k=>!(k in b)||a[k]===b[k]);
}return out}
function bruteModes(c,d){let vars=[...new Set(c.concat(d).map(Math.abs))];let flags={SS:false,SU:false,US:false,UU:false};
 for(let z=0;z<(1<<vars.length);z++){
  let a={};vars.forEach((v,i)=>a[v]=(z>>i)&1);
  let t=[c,d].map(q=>q.reduce((s,l)=>s+Number(a[Math.abs(l)]===(l>0?1:0)),0));
  if(t[0]===c.length&&t[1]===d.length)flags.SS=true;
  if(t[0]===c.length&&t[1]===0)flags.SU=true;
  if(t[0]===0&&t[1]===d.length)flags.US=true;
  if(t[0]===0&&t[1]===0)flags.UU=true;
 }return flags;
}
let countPairs=0,countComplements=0,countGains=0;
for(let F of [base,paired,w1,w1prime]){
 let n=Math.max(...F.flat().map(Math.abs)),all=(1<<n)-1;
 for(let j=0;j<F.length;j++)for(let k=j+1;k<F.length;k++){
   assert.deepEqual(compatibility(F[j],F[k]),bruteModes(F[j],F[k]));countPairs+=4;
 }
 for(let a=0;a<(1<<n);a++){
   let p=N(F,a),q=N(F,all^a);assert.deepEqual(q,p.slice().reverse());countComplements++;
   if(n<=6)for(let i=1;i<=n;i++){
       assert.equal(N(F,a^(1<<(i-1)))[0]-p[0]+score(F,a,i),0);countGains++;
   }
 }
}
assert.deepEqual(N(base,0),[1,3,3,1]);assert.deepEqual(N(base,63),[1,3,3,1]);
for(let i=1;i<=6;i++)assert.equal(N(base,1<<(i-1))[0],1);
assert.equal(N(base,41)[0],0);
assert.equal(N(paired,0)[0],4);
const models=F=>{let n=Math.max(...F.flat().map(Math.abs)),res=0;for(let a=0;a<(1<<n);a++)if(F.every(c=>tc(c,a)>0))res++;return res};
assert.equal(models(w1),0);assert.equal(models(w1prime),54);
let signed22=F=>{let n=Math.max(...F.flat().map(Math.abs));for(let i=1;i<=n;i++){
 let p=0,q=0;for(let c of F)for(let l of c){if(l===i)p++;if(l===-i)q++;}
 if(p!==2||q!==2)return false;}return 3*F.length===4*n;};
assert(signed22(base)&&signed22(paired)&&signed22(w1)&&signed22(w1prime));
const status={result:'PASS',pair_mode_checks:countPairs,complement_checks:countComplements,independent_gain_checks:countGains,
                  W1_models:0,W1_swap6_models:54,example_H1_witness_mask:41,
                  scope:'Finite source-indexed 4-mode, complement, make-break and strict22 audit; no all-algorithm complexity conclusion'};
process.stdout.write(JSON.stringify(status)+'\n');