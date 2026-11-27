/* C06-17 extra standalone chart-only syndrome replay. Run: node replay.js. Native source compiler and original guard verification are in the separate Python evidence archive. */
function replay(){
const parity=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
const bit=i=>1n<<BigInt(i);
function lin(vs){const piv=new Map(),deps=[],basis=[];function reduce(v,c=0n){while(v){const k=v.toString(2).length;const row=piv.get(k);if(!row)break;v^=row[0];c^=row[1]}return [v,c]}
vs.forEach((v,i)=>{const [r,c]=reduce(v,bit(i));if(r){piv.set(r.toString(2).length,[r,c]);basis.push(v)}else deps.push(c)});return {basis,deps,expr:v=>{const [r,c]=reduce(v);return r?null:c}}}
function combine(vs,x){let a=0n;vs.forEach((v,i)=>{if(x&bit(i))a^=v});return a}
function verify(Q,H,cap=2000000){const F=Q.map((q,i)=>[bit(i),q,1,1]).concat(H),W=[],A=[];for(const [b,c,p,q] of F){const B=lin([b,c]).basis,L=lin(B);W.push(B);const allowed=[];for(let x=0;x<2**B.length;x++)if(parity(L.expr(b)&BigInt(x))!==p||parity(L.expr(c)&BigInt(x))!==q)allowed.push(BigInt(x));A.push(allowed)}
const rows=W.flat(),D=lin(rows).deps,cols=rows.map((_,i)=>D.reduce((a,r,j)=>a|(((r>>BigInt(i))&1n)<<BigInt(j)),0n));let pos=0;const C=W.map(w=>{const z=cols.slice(pos,pos+w.length);pos+=w.length;return z});
let probes=0,peak=0,width=0;function rec(lo,hi){const outside=lin(C.slice(0,lo).concat(C.slice(hi)).flat()),inside=lin(C.slice(lo,hi).flat());width=Math.max(width,outside.basis.length+inside.basis.length-lin(cols).basis.length);const out=new Set();function add(z){if(++probes>cap)throw Error("cap");if(outside.expr(z)!==null)out.add(z)}if(hi-lo===1){for(const a of A[lo])add(combine(C[lo],a))}else{const mid=(lo+hi)>>1,l=rec(lo,mid),r=rec(mid,hi);for(const x of l)for(const y of r)add(x^y)}peak=Math.max(peak,out.size);return out}
try{return {status:rec(0,F.length).size?"YES":"NO",probes,peak,width}}catch(e){if(e.message==="cap")return {status:"UNKNOWN_CAP",probes};throw e}}
function generate(k){const base=[7,10,20,15,17],T=[3,7,5],n=1+12*k,groups=Array.from({length:n},(_,i)=>i?1+Math.floor((i-1)/(3*k)):0),a=groups.map((g,i)=>g?5>>((i-1)%3)&1:1),b=groups.map((g,i)=>g?3>>((i-1)%3)&1:1);const Q=groups.map((g,i)=>groups.reduce((v,h,j)=>{const z=g!==h?a[i]*b[j]*(base[g]>>h&1):i===0?Number(j===0):Number(Math.floor((i-1)/3)===Math.floor((j-1)/3))*(T[(i-1)%3]>>((j-1)%3)&1);return v|(BigInt(z)<<BigInt(j))},0n));const norm=x=>groups.reduce((v,g,i)=>v|(BigInt((x>>g&1)*b[i])<<BigInt(i)),0n);return [Q,[[norm(1),norm(26),0,0],[norm(2),norm(28),0,0]]]}
const results=[1,2,4,8,16].map(k=>({k,...verify(...generate(k))}));if(results.some(r=>r.status!=="NO"))throw Error("unexpected result");return results;
}
console.log(JSON.stringify(replay(),null,2));
