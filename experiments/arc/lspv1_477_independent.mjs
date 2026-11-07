/* LSPV-1/477 independent no-dependency ordinary polynomial identity and Boolean control.
   This is not an authoritative historical R_mix341 checker. */
import assert from 'node:assert/strict';
const primes=[2,3,5,7];let checks=0, negative=0;
// Each monomial retains repeated variables, including x*x.
function mod(z,p){return ((z%p)+p)%p}
function pack(a,p){const m=new Map();for(const [k,v] of a) {let q=mod((m.get(k)||0)+v,p);if(q)m.set(k,q);else m.delete(k)}return m}
function c(v,p){return pack([['',v]],p)}
function X(i,p){return pack([[String(i),1]],p)}
function plus(a,b,p){return pack([...a,...b],p)}
function times(a,b,p){const raw=[];for(const [i,x] of a)for(const[j,y]of b){const z=[...i,...j].sort().join('');raw.push([z,x*y])}return pack(raw,p)}
function s(a,k,p){return pack([...a].map(([m,x])=>[m,k*x]),p)}
function literal(i,positive,p){return positive? X(i,p):plus(c(1,p),s(X(i,p),-1,p),p)}
function negation(i,b,p){return literal(i,!b,p)}
function clause(l,p){return l.reduce((a,[i,b])=>times(a,negation(i,b,p),p),c(1,p))}
function apply(f,im,p){let out=new Map();for(const [m,v] of f){let cur=c(v,p);for(const k of m){cur=times(cur,k==='3'?im:X(+k,p),p)}out=plus(out,cur,p)}return out}
function equals(a,b,label){assert.deepEqual([...a].sort(),[...b].sort(),label);checks++}
for(let sign=0;sign<8;sign++){
  const source=[0,1,2].map(i=>[i,!!(sign&(1<<i))]);
  const [l1,l2,l3]=source;
  const P=[l1,l2,[3,true]],Q=[l1,l3,[3,false]];
  for(const p of primes){
    const pc=clause(source,p), pp=clause(P,p),qp=clause(Q,p);
    const im=literal(2,l3[1],p);
    equals(apply(pp,im,p),pc,'first projection');
    const xb=plus(times(X(2,p),X(2,p),p),s(X(2,p),-1,p),p);
    const qb=s(times(negation(0,l1[1],p),xb,p),-1,p);
    equals(apply(qp,im,p),qb,'tautology needs Boolean axiom');
    const ab=plus(times(X(3,p),X(3,p),p),s(X(3,p),-1,p),p);
    equals(apply(ab,im,p),xb,'Boolean axiom maps to Boolean axiom');
    equals(plus(times(pp,negation(2,l3[1],p),p),times(qp,negation(1,l2[1],p),p),p),pc,'degree4 forward');
  }
  for(let values=0;values<8;values++){
    const bits=[0,1,2].map(i=>!!(values&(1<<i)));
    function ev(C,a){return C.some(([i,b])=>(i===3?a:bits[i])===b)}
    const cv=ev(source,false);
    const existential=[false,true].some(a=>ev(P,a)&&ev(Q,a));
    const section=ev(P,bits[2]===l3[1])&&ev(Q,bits[2]===l3[1]);
    assert.equal(cv,existential);assert.equal(cv,section);checks+=2;
  }
  const invalid=source.map(([i,b])=>!b);
  function check(C,a){return C.some(([i,b])=>(i===3?a:invalid[i])===b)}
  const wrongQ=[l1,l3,[3,true]];
  assert.equal([false,true].some(a=>check(P,a)&&check(Q,a)),false);
  assert.equal([false,true].some(a=>check(P,a)&&check(wrongQ,a)),true);checks+=2;negative++;
}
console.log(JSON.stringify({status:'PASS',fields:primes,polynomial_identities:128,boolean_assertions:144,total_checks:checks,deliberate_polarity_rejections:negative}));
