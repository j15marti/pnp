function C(a,b,c){return a!==b&&b!==c&&a!==c&&[0,1,2,3,4].some(i=>[a,b,c].every(x=>(x-i+5)%5<=2))}
function R(a,b,c){const w=(x,y)=>[1,3].includes((y-x+5)%5);return a!==b&&b!==c&&a!==c&&w(a,b)!==w(a,c)}
function assert(b,m){if(!b)throw Error(m)}
function make(ell,positive){
 const H=2**ell,P=H+1,V=[],K=[],pairs=[],a=[0,1,2,3,4].map(nv);
 function nv(v){V.push(v);return V.length-1}
 function add(i,j,k){assert(i!==j&&j!==k&&i!==k,"distinct IDs");K.push([i,j,k])}
 for(let i=0;i<5;i++)add(a[i],a[(i+1)%5],a[(i+2)%5]);
 function wire(v){const p=nv(v);for(const j of [2,3,4])add(a[j],p,nv([0,1,2,3,4].find(t=>C(j,v,t))));return p}
 function pin(p,v){if(v)add(a[0],a[2],p);else add(a[1],a[4],p)}
 function or(p,q){const z=wire(V[p]|V[q]),u=nv(V[p]===0?3:0),w=nv(V[q]===0?4:2);add(a[1],a[2],u);add(a[0],a[1],w);add(a[4],p,u);add(a[3],q,w);add(z,u,w);return z}
 const raw=Array.from({length:P},(_,i)=>Array.from({length:ell},(_,j)=>wire(((i===0?0:i-1)>>j)&1)));
 for(let i=0;i<P;i++)for(let j=i+1;j<P;j++){
   const begin=V.length,cb=K.length,neg=new Map();
   function nt(p){if(!neg.has(p)){const z=wire(1-V[p]);add(a[2],p,z);neg.set(p,z);neg.set(z,p)}return neg.get(p)}
   function xor(p,q){const z=wire(V[p]^V[q]);for(let w=0;w<8;w++){const b=[w&1,(w>>1)&1,(w>>2)&1];if((b[0]^b[1]^b[2])===0)continue;const ids=[p,q,z].map((u,t)=>b[t]?nt(u):u);pin(or(or(ids[0],ids[1]),ids[2]),1)}return z}
   const ds=raw[i].map((p,t)=>xor(p,raw[j][t]));let f=ds[0];for(let t=1;t<ell;t++)f=or(f,ds[t]);
   pin(f,positive&&i===0&&j===1?0:1);
   pairs.push({i,j,begin,end:V.length,cb,ce:K.length,output:f});
 }
 return {V,K,a,raw,pairs,ell,H}
}
function arc(F){
 const D=Array(F.V.length).fill(31);F.a.forEach((p,i)=>D[p]=1<<i);
 const W=[];for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++)if(C(a,b,c))W.push([1<<a,1<<b,1<<c]);
 let passes=0;for(;;){passes++;let changed=false;for(const ids of F.K){const S=[0,0,0];for(const w of W)if(w.every((v,i)=>D[ids[i]]&v))for(let i=0;i<3;i++)S[i]|=w[i];if(!S[0])return {contradiction:true,passes};for(let i=0;i<3;i++)if(D[ids[i]]!==S[i]){D[ids[i]]=S[i];changed=true}}if(!changed)return {contradiction:false,passes,rawBoth:F.raw.flat().every(p=>D[p]===3)}}
}
function rank(vectors){const basis=new Map();for(let x of vectors){while(x){let p=31-Math.clz32(x);if(!basis.has(p)){basis.set(p,x);break}x^=basis.get(p)}}return basis.size}
function pairRanks(ell){const H=2**ell,neq=[],eq=[];for(let x=0;x<H;x++)for(let y=0;y<H;y++)(x===y?eq:neq).push(x+(y<<ell));return {ell,neqPoints:neq.length,neqRank:rank(neq.map(x=>x^neq[0])),eqRank:rank(eq.map(x=>x^eq[0]))}}
function audit(){
 let triples=0,frames=0,orChecks=0;for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++){assert(C(a,b,c)===(R(a,b,c)&&R(b,a,c)),"C/R");triples++}
 for(let w=0;w<3125;w++){let t=w;const a=[];for(let i=0;i<5;i++){a.push(t%5);t=Math.floor(t/5)}if(a.every((v,i)=>C(v,a[(i+1)%5],a[(i+2)%5]))){frames++;assert([1,4].some(d=>a.every((v,i)=>v===(a[0]+d*i)%5)),"frame")}}assert(frames===10,"frames")
 for(let p=0;p<2;p++)for(let q=0;q<2;q++)for(let z=0;z<2;z++){let n=0;for(let u=0;u<5;u++)for(let v=0;v<5;v++){orChecks++;if(C(1,2,u)&&C(0,1,v)&&C(4,p,u)&&C(3,q,v)&&C(z,u,v))n++}assert(n===Number(z===(p|q)),"OR")}
 const scales=[];for(const ell of [1,2,3,4,5]){const Y=make(ell,true),U=make(ell,false),n=Y.V.length,m=Y.K.length;const bad=f=>f.K.filter(c=>!C(...c.map(i=>f.V[i]))).length;assert(bad(Y)===0&&bad(U)===1,"neighbor witness");assert(Y.K.every(c=>{const [x,y,z]=c.map(i=>Y.V[i]);return R(x,y,z)&&R(y,x,z)}),"R witness");assert(U.K.filter((c,i)=>c.join()!==Y.K[i].join()).length===1,"one edit");assert(Y.pairs.every(p=>Y.V[p.output]===Number(!(p.i===0&&p.j===1))),"pair gates");const v=5*n,N=n+1+2*Math.floor(Math.log2(m+1))+1+3*m*Math.ceil(Math.log2(n+1));const maxPrivate=Math.max(...Y.pairs.map(p=>p.end-p.begin));const d0=Y.raw.flat().length+25+5*(maxPrivate+8*ell);scales.push({ell,pigeons:Y.H+1,n,m,N,v,maxPrivate,d0,oneHotBound:d0/2+1<v/5,arcY:ell<=4?arc(Y):null,arcU:ell<=4?arc(U):null});}
 const ranks=[1,2,3,4,5,6,7].map(pairRanks);for(const r of ranks)assert(r.eqRank===r.ell&&r.neqRank===(r.ell===1?1:2*r.ell),"affine rank");
 return {triples,frames,orChecks,scales,ranks}
}
console.log(JSON.stringify(audit(),null,2));
