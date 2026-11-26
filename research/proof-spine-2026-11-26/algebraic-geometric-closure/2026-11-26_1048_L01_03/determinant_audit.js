function determinantAudit(){
let seed=20261126,checks=0;const ck=(x,msg)=>{checks++;if(!x)throw Error(msg)},rnd=m=>{seed=(Math.imul(1103515245,seed)+12345)>>>0;return(seed>>>12)%m};
const R=n=>Array.from({length:n},(_,i)=>i);function perms(n){let a=[],out=[];function go(){if(a.length===n){out.push(a.slice());return}for(let j=0;j<n;j++)if(!a.includes(j)){a.push(j);go();a.pop()}}go();return out}
function sign(p){let v=0;for(let i=0;i<p.length;i++)for(let j=i+1;j<p.length;j++)if(p[i]>p[j])v++;return v%2?-1:1}
function ring(p,D){const norm=x=>((x%p)+p)%p;function add(a,b){let o=new Map(a);for(let [i,v] of b){let c=norm((o.get(i)||0)+v);if(c)o.set(i,c);else o.delete(i)}return o}function neg(a){return new Map([...a].map(([i,v])=>[i,norm(-v)]))}function mul(a,b){let o=new Map;for(let [i,v] of a)for(let [j,w] of b)if(i+j<=D){let c=norm((o.get(i+j)||0)+v*w);if(c)o.set(i+j,c);else o.delete(i+j)}return o}return {norm,add,neg,mul,one:new Map([[0,1]]),zero:new Map}}
function berk(A,r){let n=A.length;if(!n)return[r.one];let B=A.slice(1).map(x=>x.slice(1)),v=A.slice(1).map(x=>x[0]),row=A[0].slice(1),q=[r.one,r.neg(A[0][0])];for(let k=0;k<n-1;k++){let s=r.zero;for(let j=0;j<n-1;j++)s=r.add(s,r.mul(row[j],v[j]));q.push(r.neg(s));if(k<n-2)v=B.map(row=>row.reduce((s,a,j)=>r.add(s,r.mul(a,v[j])),r.zero))}let c=berk(B,r);return R(n+1).map(i=>c.reduce((s,x,j)=>j<=i?r.add(s,r.mul(q[i-j],x)):s,r.zero))}
function same(a,b){return a.size===b.size&&[...a].every(([k,v])=>b.get(k)===v)}
function mobius(a,n,p){let b=a.slice();for(let i=0;i<n;i++)for(let mask=0;mask<b.length;mask++)if(mask&(1<<i))b[mask]=((b[mask]-b[mask^(1<<i)])%p+p)%p;return b}
function pop(m){let s=0;while(m){m&=m-1;s++}return s}
const n=3,m=n*n,W=2*m,tracks=m+1,ws=R(tracks).map(()=>R(m).map(()=>1+rnd(W))),ps=perms(n),summary=[];
for(let p of [2,3,101]){const r=ring(p,n*W);let truth=[],mismatchSum=0,unisolated=0,overlap=0,coeffTracks=0;
for(let mask=0;mask<2**m;mask++){let active=ps.filter(q=>q.every((j,i)=>mask&(1<<(i*n+j)))),votes=0,iso=0;
for(let w of ws){let A=R(n).map(i=>R(n).map(j=>mask&(1<<(i*n+j))?new Map([[w[i*n+j],1]]):r.zero));let c=berk(A,r)[n];if(n%2)c=r.neg(c);let ref=r.zero,weights=[];for(let q of active){let k=q.reduce((s,j,i)=>s+w[i*n+j],0);weights.push(k);ref=r.add(ref,new Map([[k,r.norm(sign(q))]]))}ck(same(c,ref),"Berkowitz vs signed enumeration");if(weights.length&&weights.filter(x=>x===Math.min(...weights)).length===1){iso++;ck(c.has(Math.min(...weights)),"unique minimum coefficient")}if(c.size)votes++;coeffTracks++}
const yes=+(votes>0);ck(yes===+!!active.length,"exact coefficient OR");if(yes!==votes%p)mismatchSum++;if(votes>1)overlap++;if(yes&&!iso)unisolated++;truth.push(yes)}
let ml=mobius(truth,m,p),leading=0;for(let mask=0;mask<2**m;mask++)if(pop(mask)<=n){let expected=pop(mask)===n&&ps.some(q=>q.every((j,i)=>mask&(1<<(i*n+j))))?1:0;ck(ml[mask]===expected,"leading permanent coefficient");if(ml[mask])leading++}
summary.push({field:p,graphs:truth.length,coeffTracks,leading,mismatchSum,unisolated,overlap})}
return{seed:20261126,checks,n,weights:ws,summary,limitations:"ring Berkowitz coefficient calculation on Boolean masks only; symbolic circuit upper bound proved separately; not a circuit lower bound or uniform asymptotic list search"}
}
console.log(JSON.stringify(determinantAudit(),null,2));
