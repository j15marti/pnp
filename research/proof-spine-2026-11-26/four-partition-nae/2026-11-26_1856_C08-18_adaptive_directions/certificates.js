// C08-18 certificate provenance and polar-rank guard audit. node certificates.js
function certificates(){
let checks=0,seed=20261128;function ok(t,m){checks++;if(!t)throw Error(m||"check "+checks)}
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
function par(x){x^=x>>>16;x^=x>>>8;x^=x>>>4;return(0x6996>>>(x&15))&1}
function mul(a,b){let r=0;while(b){if(b&1)r^=a;b>>>=1;a<<=1;if(a&64)a^=67}return r}
function toggle(S,x){if(S.has(x))S.delete(x);else S.add(x)}
let col=Array.from({length:64},(_,t)=>1|(t<<1)|(mul(mul(t,t),t)<<7)),off=col.map((_,i)=>((i<32?648477357:3348622548)>>>(i%32))&1);
function f(i){return [...(off[i]^1?[0]:[]),...Array.from({length:13},(_,j)=>1<<j).filter(v=>v&col[i])]}
let Q=Array.from({length:32},(_,i)=>{let S=new Set;for(let a of f(2*i))for(let b of f(2*i+1))toggle(S,a|b);return [...S]});
let mons=[0,...Array.from({length:13},(_,j)=>1<<j)];for(let i=0;i<13;i++)for(let j=i+1;j<13;j++)mons.push((1<<i)|(1<<j));
let idx=new Map(mons.map((v,i)=>[v,i])),P=Array(mons.length).fill(null);
for(let i=0;i<Q.length;i++){let v=0n;for(let m of Q[i])v^=1n<<BigInt(idx.get(m));let c=1n<<BigInt(i);while(v){let j=v.toString(2).length-1;if(!P[j]){P[j]=[v,c];break}v^=P[j][0];c^=P[j][1]}}
let rows=[];for(let i=1;i<=13;i++)if(P[i]){let [v,c]=P[i],S=new Set,parents=[];for(let j=0;j<32;j++)if(c&(1n<<BigInt(j))){parents.push(j);for(let t of Q[j])toggle(S,t)}let a=0,b=+(S.has(0));for(let t of S)if(t){ok((t&(t-1))===0);a^=t}let W=new Set;for(let j=0;j<mons.length;j++)if(v&(1n<<BigInt(j)))W.add(mons[j]);ok(S.size===W.size&&[...S].every(t=>W.has(t)));rows.push({mask:a,rhs:b,clauses:parents})}
ok(rows.length===7);
function rank(V,d){let P=Array(d).fill(0),r=0;for(let v of V){for(let i=d-1;i>=0&&v;i--)if(v&(1<<i)){if(P[i])v^=P[i];else{P[i]=v;r++;break}}}return{r,P}}
let tested=0,polys=0,rankCounts={},maxCandidates=0;
for(let t=0;t<220;t++){let d=3+rnd(5),matrix=Array(d).fill(0);
for(let i=0;i<d;i++)for(let j=i+1;j<d;j++)if(rnd(2)){matrix[i]^=1<<j;matrix[j]^=1<<i}
if(t%4===0){let a=1+rnd((1<<d)-1),b=1+rnd((1<<d)-1);matrix=Array.from({length:d},(_,i)=>(((a>>i)&1)?b:0)^(((b>>i)&1)?a:0))}
let {r,P}=rank(matrix,d),span=new Set([0]);for(let a of P)if(a)for(let b of [...span])span.add(a^b);
let c=0;for(let h=1;h<1<<d;h++){let j=31-Math.clz32(h),K=[];for(let i=0;i<d;i++)if(i!==j)K.push((1<<i)^(((h>>i)&1)?1<<j:0));
function B(x,y){let v=0;for(let i=0;i<d;i++)if(x&(1<<i))v^=matrix[i];return par(v&y)}
let zero=K.every(x=>K.every(y=>!B(x,y)));ok(zero===(r===0||(r===2&&span.has(h))));if(zero)c++;tested++}
if(r>0)maxCandidates=Math.max(maxCandidates,c);rankCounts[r]=(rankCounts[r]||0)+1;polys++}
return{checks,rows,polar:{polys,tested,rankCounts,maxNonAffineCandidates:maxCandidates}}
}
console.log(JSON.stringify(certificates(),null,2));
