function verifierAudit(){
let checks=0;const ck=x=>{checks++;if(!x)throw Error("failure "+checks)};
const B=(1<<0)|(1<<5)|(1<<10)|(1<<15),C=(B&~1)|(1<<6);
function perms(n){let r=[];function rec(a,b){if(!b.length){r.push(a);return}for(let j=0;j<b.length;j++)rec(a.concat(b[j]),b.slice(0,j).concat(b.slice(j+1)))}rec([],Array.from({length:n},(_,i)=>i));return r}
function nativePositive(q,n){const masks=Array(n*n).fill(B),inv=Array(n);q.forEach((j,i)=>{masks[i*n+j]=C;inv[j]=i});for(let i=0;i<n;i++)for(let j=0;j<n;j++){const word=8*(inv[j]<i)+4*(q[i]<=j)+2*(inv[j]<=i)+(q[i]<j);ck(!!(masks[i*n+j]>>word&1))}return masks}
function h(m,n){if(m.some(x=>x!==B&&x!==C))return false;for(let i=0;i<n;i++){let r=0,c=0;for(let j=0;j<n;j++){r+=+(m[i*n+j]===C);c+=+(m[j*n+i]===C)}if(r!==1||c!==1)return false}return true}
function pos(m,n){let oneLine=ids=>ids.some(i=>(m[i]&C)===C&&ids.every(j=>i===j||(m[j]&B)===B));let rows=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i*n+j));let cols=Array.from({length:n},(_,j)=>Array.from({length:n},(_,i)=>i*n+j));return rows.every(oneLine)&&cols.every(oneLine)}
let out=[];for(let n=1;n<=4;n++){const P=perms(n),M=P.map(q=>nativePositive(q,n));let yes=0,no=0;for(let x=0;x<(1<<(n*n));x++){let a=Array.from({length:n*n},(_,i)=>x>>i&1),z=a.map(b=>b?C:B),g=a.map(b=>b?B|(1<<6):B);ck(h(z,n)===pos(z,n));let lo=M.some(m=>m.every((v,i)=>(v&g[i])===v));let ref=P.some(q=>q.every((j,i)=>a[i*n+j]));ck(lo===ref);ck(!lo||a.some(Boolean));if(lo)yes++;else no++}out.push({n,yes,no,permutationMasks:M.length})}
return {checks,out,scope:"core masks only; padding and full native lift separately checked in audit.js. Polynomial positive verifier on exact-four slice, canonical lower completion matching on the padded projection."}
}
console.log(JSON.stringify(verifierAudit(), null, 2));
