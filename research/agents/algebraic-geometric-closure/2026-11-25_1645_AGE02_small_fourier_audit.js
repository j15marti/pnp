// AGE02 independent small-source Fourier audit. Node.js, no dependencies.
// Supplied sign masks acquired by planar face signing in the Python audit.
// Exhaustive matching list is a small reference only, not part of the terminal.
const fixtures=[
{name:"fixture24",C:[[0,2,1],[0,3,4],[3,5,6],[5,7,8],[7,9,10],[9,11,12],[11,13,14],[13,15,1],[16,2,17],[16,18,4],[18,19,6],[19,20,8],[20,21,10],[21,22,12],[22,23,14],[23,15,17],[0,16,2],[1,11,9],[7,5,3],[6,18,4],[10,20,8],[14,22,12],[13,15,23],[19,21,17]],P:[1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,2,2,2,2,2,2,2,2],sign:[0x90000,0x200000,0x7f2000],base:[0x23319,0x20634c,0xd554]},
{name:"base12",C:[[0,5,6],[0,1,7],[1,2,8],[2,5,9],[3,4,10],[3,4,11],[0,3,6],[1,7,8],[2,8,9],[7,9,10],[4,10,11],[5,6,11]],P:[0,1,0,2,1,0,2,2,1,0,2,1],sign:[0x800,0x600,0x200],base:[0x80e,0x42a,0x22a]}];
const pc=x=>{let n=0;while(x){x&=x-1;n++}return n}, bit=(x,i)=>(x>>>i)&1, hi=x=>31-Math.clz32(x), parity=x=>pc(x)&1;
const check=(a,msg)=>{if(!a)throw Error(msg)};
function basis(cols){let B=new Map(),ker=[];for(let j=0;j<cols.length;j++){let z=cols[j],w=1<<j;while(z){let i=hi(z);if(!B.has(i)){B.set(i,[z,w]);break}let [a,b]=B.get(i);z^=a;w^=b}if(!z)ker.push(w)}return {B,ker}}
function reduce(B,z){let w=0;for(let i of [...B.keys()].sort((a,b)=>b-a))if(bit(z,i)){let [a,b]=B.get(i);z^=a;w^=b}return [z,w]}
function det(A){A=A.map(r=>r.map(BigInt));let n=A.length,p=1n,s=1n;for(let k=0;k<n-1;k++){let i=k;while(i<n&&!A[i][k])i++;if(i===n)return 0n;if(i!==k){[A[i],A[k]]=[A[k],A[i]];s=-s}let q=A[k][k];for(i=k+1;i<n;i++){for(let j=k+1;j<n;j++){let v=A[i][j]*q-A[i][k]*A[k][j];check(v%p===0n,"Bareiss division");A[i][j]=v/p}A[i][k]=0n}p=q}return s*(n?A[n-1][n-1]:1n)}
function audit(F,q){
 let {C,P}=F,n=C.length,k=n/3,parts=[0,1,2].map(p=>P.flatMap((v,i)=>v===p?[i]:[])),[a,b]=[0,1,2].filter(p=>p!==q);
 let E=Array.from({length:n},(_,v)=>[parts[a].findIndex(c=>C[c].includes(v)),parts[b].findIndex(c=>C[c].includes(v)),parts[q].findIndex(c=>C[c].includes(v))]);
 check(E.every(e=>e.every(v=>v>=0)),"partition");
 let syn=z=>E.reduce((s,e,v)=>s^(bit(z,v)?1<<e[2]:0),0);
 let cyc=basis(E.map(e=>(1<<e[0])^(1<<(k+e[1])))).ker;
 let {B,ker}=basis(cyc.map(syn)),d=B.size,h=ker.length,base=F.base[q],sign=F.sign[q];
 let [rem,target]=reduce(B,((1<<k)-1)^syn(base));check(!rem,"target in span");
 let piv=[...B.values()].map(x=>hi(x[1])).sort((a,b)=>a-b);
 let coord=z=>{let w=reduce(B,z)[1];return piv.reduce((s,j,i)=>s|(bit(w,j)<<i),0)};
 let normal=m=>{let p=[];for(let i=0;i<k;i++){let es=E.flatMap((e,j)=>bit(m,j)&&e[0]===i?[e[1]]:[]);check(es.length===1,"left matching");p.push(es[0])}check(new Set(p).size===k,"right matching");let inv=0;for(let i=0;i<k;i++)for(let j=i+1;j<k;j++)inv+=p[i]>p[j];return (-1)**(inv+pc(m&sign))};
 let norm=normal(base),ell=E.map(e=>coord(1<<e[2])),need=coord((1<<k)-1);
 let refs=[];function walk(i,used,m){if(i===k){refs.push(m);return}E.forEach((e,v)=>{if(e[0]===i&&!bit(used,e[1]))walk(i+1,used|(1<<e[1]),m|(1<<v))})}walk(0,0,0);
 check(refs.every(m=>normal(m)===norm),"signed monomials");
 let calls=0;
 function count(pin){let tot=0n;for(let s=0;s<(1<<d);s++){let A=Array.from({length:k},()=>Array(k).fill(0));E.forEach((e,v)=>{if(pin===0&&v===0)return;if(pin===1&&v!==0&&(e[0]===E[0][0]||e[1]===E[0][1]))return;A[e[0]][e[1]]+=(-1)**(bit(sign,v)+parity(s&ell[v]))});let z=BigInt(norm)*det(A);calls++;let exact=refs.filter(m=>pin===null||bit(m,0)===pin).reduce((z,m)=>z+BigInt((-1)**parity(coord(syn(m))&s)),0n);check(z===exact,'signed evaluation');
 tot+=BigInt((-1)**parity(s&need))*z;}check(tot%(1n<<BigInt(d))===0n,"Fourier division");return tot>>BigInt(d)}
 // independent exhaustive references per pin
 let all=[null,0,1].map(pin=>{let ref=refs.filter(m=>(pin===null||bit(m,0)===pin)&&syn(m)===(1<<k)-1).length;let got=count(pin);check(got===BigInt(ref),"Fourier count");return Number(got)});
 return {q,rank:d,nullity:h,baseMatchings:refs.length,count:all[0],pin0:all[1],pin1:all[2],determinants:calls};
}
const results=fixtures.map(F=>({name:F.name,charts:[0,1,2].map(q=>audit(F,q))}));
console.log(JSON.stringify(results,null,2));