function audit(){
const C=(n,k)=>{if(k<0||k>n)return 0n;let r=1n;for(let j=1;j<=k;j++)r=r*BigInt(n-j+1)/BigInt(j);return r;};
const fixtures={U:"000 002 010 011 021 022 100 101 111 201 202 221",V:"000 002 010 011 021 022 100 101 111 201 202 221 110",MF01:"000 001 012 020 110 120 122 200 201 210 211",neutral:"002 011 020 101 102 112 212 220"};
const out={fixtures:{},rings:[]};
for(const [name,s] of Object.entries(fixtures)){
const T=s.split(" ").map(x=>[...x].map(Number)),lanes=[];
for(const [a,b,c] of [[0,1,2],[0,2,1],[1,2,0]]){
const hist={},support=new Set();for(const x of T.filter(t=>t[a]===0))for(const y of T.filter(t=>t[a]===1))for(const z of T.filter(t=>t[a]===2)){
const L=[x,y,z];if(new Set(L.map(t=>t[b])).size!==3)continue;
let d=0,v=0;for(let i=0;i<3;i++){v^=1<<L[i][c];for(let j=0;j<i;j++)if(L[i][c]===L[j][c])d++;}
hist[d]=(hist[d]??0)+1;support.add(v);}
let B=[0n,0n,0n];for(const [d,m] of Object.entries(hist))for(let i=0;i<=2;i++)B[i]+=BigInt(m)*C(Number(d),i);
if(3n*(B[0]-B[1])+2n*B[2]!==3n*BigInt(hist[0]??0))throw Error("moment identity");
lanes.push({lane:[a,b,c],hist,support:[...support].sort(),moments:B.map(String)});
}
const P=Array.from({length:9},(_,k)=>T.map((t,i)=>t[Math.floor(k/3)]===k%3?i:-1).filter(x=>x>=0));const N=[];for(let i=0;i<T.length;i++)for(let j=0;j<i;j++)if(T[i].some((x,a)=>x===T[j][a]))N.push([i,j]);let bad=0,solutions=0;
for(let mask=0;mask<1<<T.length;mask++){const b=i=>(mask>>i)&1;const covered=P.map(p=>p.reduce((s,i)=>s+b(i),0));const frozen=covered.every(c=>c>0)&&N.every(([i,j])=>!b(i)||!b(j));const coarse=T.reduce((s,_,i)=>s^b(i),0);const fine=covered.reduce((s,c)=>s^Number(c>0),0);const isBad=frozen&&coarse===1&&fine!==0;const isSol=covered.every(c=>c===1);if(isBad!==isSol)throw Error("bad fiber");bad+=Number(isBad);solutions+=Number(isSol);}
out.fixtures[name]={lanes,bad,solutions,assignments:1<<T.length};
}
for(let k=1;k<=8;k++){let n=4*(k+1),a=Array.from({length:n/2+1},(_,i)=>2n*C(n,2*i)),b=a.slice();b[0]=0n;for(let i=1;i<=k+1;i++)b[i]+=2n*BigInt(i%2?1:-1)*C(k+1,i);if(b.some(x=>x<0n))throw Error("negative");
const mom=(L,r)=>L.reduce((s,x,i)=>s+x*C(i,r),0n);for(let r=0;r<=k;r++)if(mom(a,r)!==mom(b,r))throw Error("ring moment");
out.rings.push({n,k,zeroA:String(a[0]),zeroB:String(b[0]),moments:Array.from({length:k+1},(_,r)=>String(mom(a,r)))});
}
return out;
}
console.log(JSON.stringify(audit(),null,2));
