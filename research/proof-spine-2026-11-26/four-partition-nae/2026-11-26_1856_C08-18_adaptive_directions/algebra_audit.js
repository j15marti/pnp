// C08-18 bounded-degree Boolean polynomial refutation audit; node algebra_audit.js
function algebraAudit(){
let checks=0;function ok(t,m){checks++;if(!t)throw Error(m||"check "+checks)}
function par(x){x^=x>>>16;x^=x>>>8;x^=x>>>4;return(0x6996>>>(x&15))&1}
function mul(a,b){let r=0;while(b){if(b&1)r^=a;b>>>=1;a<<=1;if(a&64)a^=67}return r}
function valid(M,z){let y=M.a.map((a,i)=>par(a&z)^M.b[i]);return M.B.every(([a,b])=>y[a>>1]===(a&1)||y[b>>1]===(b&1))}
function exact(M){let w=[];for(let z=0;z<(1<<M.d);z++)if(valid(M,z))w.push(z);return w}
function mons(n,D){let m=[0],p=[0];for(let k=1;k<=D;k++){let next=[];for(let a of p){let hi=a?32-Math.clz32(a):0;for(let j=hi;j<n;j++)next.push(a|(1<<j))}m.push(...next);p=next}return m}
function polynomials(M){function falsifier(l){let i=l>>1,t=l&1,a=M.a[i],b=M.b[i]^t;return [...(b?[0]:[]),...Array.from({length:M.d},(_,j)=>1<<j).filter(r=>a&r)]}return M.B.map(([a,b])=>{let p=new Set;for(let x of falsifier(a))for(let y of falsifier(b)){let v=x|y;if(p.has(v))p.delete(v);else p.add(v)}return [...p].sort((a,b)=>a-b)})}
function evalPoly(p,z){let b=0;for(let a of p)if((a&z)===a)b^=1;return b}
function linearize(M,D){let Q=polynomials(M),monsD=mons(M.d,D),index=new Map(monsD.map((a,i)=>[a,i])),L=mons(M.d,Math.max(0,D-2)),P=Array(monsD.length).fill(null),rank=0,rowCount=0,ops=0,terms=[];
function row(q,a){let r=0n;for(let u of Q[q]){let j=index.get(u|a);ok(j!==undefined);r^=1n<<BigInt(j)}return r}
function add(v,id){let cert=1n<<BigInt(id);while(v){let j=v.toString(2).length-1;if(!P[j]){P[j]=[v,cert];rank++;return}v^=P[j][0];cert^=P[j][1];ops++}}
for(let q=0;q<Q.length;q++)for(let a of L){let r=row(q,a);terms.push([q,a]);add(r,rowCount++)}
let contradiction=!!P[0],certificate=[];if(contradiction){ok(P[0][0]===1n);let v=P[0][1],sum=0n;for(let i=0;i<terms.length;i++)if(v&(1n<<BigInt(i))){certificate.push(terms[i]);sum^=row(...terms[i])}ok(sum===1n);let independent=new Set;for(let [q,a] of certificate)for(let u of Q[q]){let t=a|u;if(independent.has(t))independent.delete(t);else independent.add(t)}ok(independent.size===1&&independent.has(0))}
let affineRows=[];for(let j=1;j<=M.d;j++)if(P[j]){let [v]=P[j];ok((v>>BigInt(M.d+1))===0n);let a=0,b=Number(v&1n);for(let i=1;i<=M.d;i++)if(v&(1n<<BigInt(i)))a|=1<<(i-1);affineRows.push([a,b])}
return{degree:D,variables:M.d,monomials:monsD.length,rowCount,rank,rowXors:ops,contradiction,certificateTerms:certificate.length,affineRows,certificate}}
const col=Array.from({length:64},(_,t)=>1|(t<<1)|(mul(mul(t,t),t)<<7)),hard={d:13,a:col,b:col.map((_,i)=>((i<32?648477357:3348622548)>>>(i%32))&1),B:Array.from({length:32},(_,i)=>[4*i+1,4*i+3])};
function native(F,n){let a=[],B=[];function get(u,v){let h=(u?1<<(u-1):0)^(v?1<<(v-1):0),i=a.indexOf(h);if(i<0){i=a.length;a.push(h)}return i}for(let p of F)for(let c of p){let L=[[0,1],[0,2],[1,2]].map(([i,j])=>2*get(c[i],c[j])+1);B.push([L[0],L[1]],[L[0],L[2]],[L[1],L[2]])}return{d:n-1,a,b:a.map(()=>0),B}}
const AG=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]];
const cyclic=p=>Array.from({length:4},(_,s)=>Array.from({length:p},(_,i)=>[i,p+(i+s)%p,2*p+(i+3*s)%p]));
let results=[];
for(let [name,M] of [["GF64 guard barrier",hard],["raw AG9",native(AG,9)],["raw cyclic15",native(cyclic(5),15)]]){let W=exact(M),Q=polynomials(M);for(let z=0;z<1<<M.d;z++)ok(valid(M,z)===Q.every(q=>!evalPoly(q,z)),`${name} polarity ${z}`);let tests=[];for(let d of [2,3,4]){let z=linearize(M,d);if(z.contradiction)ok(!W.length);for(let [a,b] of z.affineRows)ok(W.every(w=>par(w&a)===b));tests.push(z);if(z.contradiction)break}results.push({name,exactModels:W.length,tests})}
return{checks,results}
}
console.log(JSON.stringify(algebraAudit(),null,2));
