function audit(){
let seed=20261125;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
const par=x=>{let b=0;while(x){b^=1;x&=x-1}return b};
const piv=x=>31-Math.clz32(x);
function red(x,B){for(let i=B.length-1;i>=0;i--)if((x>>>i)&1)x^=B[i]||0;return x}
function bas(X){let B=[];for(let x of X){x=red(x,B);if(x)B[piv(x)]=x}return B}
const rows=B=>B.filter(Boolean), rank=X=>rows(bas(X)).length;
const span=(F,I)=>I.flatMap(i=>F[i].slice(0,2));
function eq(R){let B=[];for(let [x,t] of R){for(let i=B.length-1;i>=0;i--)if(((x>>>i)&1)&&B[i]){x^=B[i][0];t^=B[i][1]}if(!x){if(t)return null}else B[piv(x)]=[x,t]}return B}
function er(x,t,B){for(let i=B.length-1;i>=0;i--)if(((x>>>i)&1)&&B[i]){x^=B[i][0];t^=B[i][1]}return [x,t]}
function word(R){let B=eq(R);if(!B)return null;let x=0;for(let i=0;i<B.length;i++)if(B[i]&&(par(B[i][0]&x)^B[i][1]))x|=1<<i;return x}
const sat=(F,I,x)=>I.every(i=>{let [a,b,p,q]=F[i];return par(a&x)!==p||par(b&x)!==q});
const all=n=>Array.from({length:1<<n},(_,i)=>i);
let c={roots:0,sat:0,unsat:0,mi_calls:0,projections:0,projection_lifts:0,guard_jobs:0,guard_sat:0,guard_unsat:0,nesting:0,deficiency_gt1:0,closure_rounds:0,forced:0,probe_calls:0,core_words:0,compiler_checks:0};
function mi(F,I,Q){c.mi_calls++;let E=I.flatMap(i=>{let [a,b,p,q]=F[i];return [[i,a,1^p],[i,b,1^q],[i,a^b,1^p^q]].map(([j,v,t])=>[j,v,t,red(v,Q)])});let S=new Set();
 const lin=A=>rank([...A].map(e=>E[e][3]))===A.size,part=A=>new Set([...A].map(e=>E[e][0])).size===A.size;
 while(true){let O=E.map((_,i)=>i).filter(e=>!S.has(e)),P=new Map(),q=[];for(let e of O)if(lin(new Set([...S,e]))){P.set(e,-1);q.push(e)}let end=-1;
 for(let k=0;k<q.length;k++){let v=q[k];if(!S.has(v)&&part(new Set([...S,v]))){end=v;break}let nbr=S.has(v)?O.filter(e=>lin(new Set([...S].filter(x=>x!==v).concat(e)))):[...S].filter(e=>part(new Set([...S].filter(x=>x!==e).concat(v))));for(let e of nbr)if(!P.has(e)){P.set(e,v);q.push(e)}}
 if(end<0)return [...S].map(e=>E[e]);while(end>=0){if(S.has(end))S.delete(end);else S.add(end);end=P.get(end)}if(!lin(S)||!part(S))throw Error("bad augmentation");
 }}
const delta=(F,I,Q)=>I.length-mi(F,I,Q).length;
function core(F,I,Q){let d=delta(F,I,Q),C=I.slice();for(let i of I){let T=C.filter(j=>j!==i);if(delta(F,T,Q)===d)C=T}return [d,C]}
function check(b){if(!b)throw Error("assertion failed")}
function proj(F,I,W){let Q=bas(W),[d,C]=core(F,I,Q),U=rows(bas(span(F,C))),J=I.filter(i=>!C.includes(i)),R=mi(F,J,bas([...U,...W]));check(R.length===J.length);return {d,C,U,R}}
function solve(F,I,guards){let B=eq(guards);if(!B)return null;let W=B.filter(Boolean).map(e=>e[0]);let {C,U,R}=proj(F,I,W),D=[],Q=bas(W);for(let u of U)if(red(u,Q)){D.push(u);Q=bas([...rows(Q),u])}
 for(let k of all(D.length)){c.core_words++;let A=guards.concat(D.map((u,j)=>[u,(k>>>j)&1]));let x=word(A);check(x!==null);if(sat(F,C,x)){let y=word(A.concat(R.map(e=>[e[1],e[2]])));check(y!==null&&sat(F,I,y)&&guards.every(([v,t])=>par(v&y)===t));return y}}return null}
function normalize(F,n,G){let R=G.slice();while(true){c.closure_rounds++;let B=eq(R);if(!B)return null;let Q=new Map(),added=false;for(let [a,b,p,q] of F){let [u,s]=er(a,1^p,B),[v,t]=er(b,1^q,B);let l=(s?v:0)^(t?u:0)^(u&v),z=s&t,k=0,j=0;for(let i=0;i<n;i++)for(let h=i+1;h<n;h++,j++)if((((u>>>i)&1)*((v>>>h)&1))^(((u>>>h)&1)*((v>>>i)&1)))k^=1<<j;
 while(k&&Q.has(piv(k))){let [kk,ll,zz]=Q.get(piv(k));k^=kk;l^=ll;z^=zz}
 if(k)Q.set(piv(k),[k,l,z]);else if(l){R.push([l,z]);added=true;break}else if(z)return null;
 }if(!added)return R}}
function closure(F,n,G){let R=normalize(F,n,G);if(R===null)return null;while(true){let B=eq(R),hit=false;for(let i=0;i<n;i++){if(!er(1<<i,0,B)[0])continue;for(let t=0;t<2;t++){c.probe_calls++;if(normalize(F,n,R.concat([[1<<i,t]]))===null){c.forced++;R=normalize(F,n,R.concat([[1<<i,1^t]]));if(R===null)return null;hit=true;break}}if(hit)break}if(!hit)return R}}
for(let n=2;n<=6;n++)for(let job=0;job<30;job++){
 let m=1+rnd(n+3),F=[];for(let i=0;i<m;i++){let a=1+rnd((1<<n)-1),b=1+rnd((1<<n)-1);while(b===a)b=1+rnd((1<<n)-1);F.push([a,b,rnd(2),rnd(2)])}
 // Deliberate both-label controls: full set of four forbidden pairs on a plane.
 if(job===0||job===1){F=[[1,2,0,0],[1,2,0,1],[1,2,1,0]];if(job===0)F.push([1,2,1,1])}
 let I=F.map((_,i)=>i),X=all(n),models=X.filter(x=>sat(F,I,x));c.roots++;c[models.length?"sat":"unsat"]++;
 let W=rows(bas(Array.from({length:rnd(n+1)},()=>rnd(1<<n)))),H=W.slice(0,rnd(W.length+1));
 let P=proj(F,I,W),A=proj(F,I,H);check(A.C.every(i=>P.C.includes(i)));c.nesting++;
 let subs=all(m=F.length).map(k=>I.filter(i=>(k>>>i)&1)),def=S=>S.length-rank([...span(F,S),...W])+W.length,dd=Math.max(...subs.map(def));let mins=subs.filter(S=>def(S)===dd),CC=I.filter(i=>mins.every(S=>S.includes(i)));check(dd===P.d&&CC.join()===P.C.join());if(dd>1)c.deficiency_gt1++;
 let signature=(V,x)=>V.map(v=>par(v&x)).join("");let real=new Set(models.map(x=>signature(W,x))),pred=new Set();
 for(let x of X)if(sat(F,P.C,x)){let y=word(P.U.concat(W).map(v=>[v,par(v&x)]).concat(P.R.map(e=>[e[1],e[2]])));check(y!==null&&sat(F,I,y)&&signature(W,x)===signature(W,y));pred.add(signature(W,x));c.projection_lifts++}
 check(real.size===pred.size&&[...real].every(x=>pred.has(x)));c.projections++;
 for(let k of all(W.length)){let G=W.map((v,i)=>[v,(k>>>i)&1]),want=models.some(x=>G.every(([v,t])=>par(v&x)===t)),R=closure(F,n,G),got=R===null?null:solve(F,I,R);check((got!==null)===want);c.guard_jobs++;c[want?"guard_sat":"guard_unsat"]++}
}
for(let bits=0;bits<8;bits++)for(let signs=0;signs<8;signs++){let l=bits^signs,ok=false;for(let s=0;s<8;s++){let legal=par(s)===1&&(s&~l)===0;if(legal)ok=true;c.compiler_checks++}check(ok===(l!==0))}
return c
}
console.log(JSON.stringify(audit(),null,2));
