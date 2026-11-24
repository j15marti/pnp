function runBA07(){
 const stats={gauss:0,xor:0,energyQueries:0,energyPairs:0,massQueries:0,massTerms:0,closurePasses:0,forcedPins:0,sharedWords:0,witnessPins:0,assertions:0,referenceWords:0};
 const bit=i=>1n<<BigInt(i), pow=i=>bit(i), dot=(a,b)=>{let x=a&b,p=0;while(x){x&=x-1n;p^=1}return p};
 function assert(x){stats.assertions++;if(!x)throw Error("assert "+stats.assertions)}
 function gauss(n,eq){
  stats.gauss++;let b=Array(n).fill(null);
  for(let [x,y] of eq){for(let i=0;i<n&&x;i++)if(x&bit(i)){if(b[i]){x^=b[i][0];y^=b[i][1];stats.xor++}else{b[i]=[x,y];x=0n;y=0;break}}if(!x&&y)return null}
  for(let i=n-1;i>=0;i--)if(b[i])for(let j=0;j<i;j++)if(b[j]&&(b[j][0]&bit(i))){b[j][0]^=b[i][0];b[j][1]^=b[i][1];stats.xor++}
  let a=0n,K=[];for(let i=0;i<n;i++)if(b[i]&&b[i][1])a|=bit(i);
  for(let i=0;i<n;i++)if(!b[i]){let x=bit(i);for(let j=0;j<n;j++)if(b[j]&&(b[j][0]&bit(i)))x|=bit(j);K.push(x)}
  return {a,K,B:b.filter(Boolean).map(z=>z[0]),r:n-K.length}
 }
 const basis=(n,V)=>gauss(n,V.map(x=>[x,0])).B;
 const orth=(n,V)=>gauss(n,V.map(x=>[x,0])).K;
 const inter=(n,V,W)=>orth(n,[...orth(n,V),...orth(n,W)]);
 const term=(c,E=[])=>({c:BigInt(c),E});
 function val(F,x){return F.reduce((s,t)=>s+(t.E.every(([a,b])=>dot(a,x)===b)?t.c:0n),0n)}
 function mass(n,F,Q=[]){stats.massQueries++;let z=0n;for(const t of F){stats.massTerms++;let g=gauss(n,[...t.E,...Q]);if(g)z+=t.c*pow(n-g.r)}return z}
 function spectrum(n,F){
  let D=F.map(t=>({c:t.c,g:gauss(n,t.E)})).filter(t=>t.g&&t.c);
  let P=[];for(let i=0;i<D.length;i++)for(let j=i;j<D.length;j++){
   let a=D[i],b=D[j];P.push({E:[...a.g.K,...b.g.K].map(x=>[x,0]),s:a.g.a^b.g.a,c:a.c*b.c*pow(2*n-a.g.r-b.g.r)*(i===j?1n:2n)})}
  function energy(Q){stats.energyQueries++;let z=0n;for(const p of P){stats.energyPairs++;let g=gauss(n,[...p.E,...Q]);if(g&&!g.K.some(x=>dot(x,p.s)))z+=p.c*pow(n-g.r)*(dot(g.a,p.s)?-1n:1n)}assert(z>=0n);return z}
  let W=[];while(true){let v=orth(n,W).find(x=>energy([[x,1]])>0n);if(v===undefined)break;
   let Q=[[v,1]],w=0n;for(let i=0;i<n;i++){let q=[bit(i),0];if(energy([...Q,q])>0n)Q.push(q);else{Q.push([bit(i),1]);w|=bit(i)}}W=basis(n,[...W,w]);}
  return W;
 }
 function chart(n,F,G){let g=gauss(n,G);if(!g)return null;
  let fs=F.map(f=>f.map(t=>term(t.c,t.E.map(([a,b])=>[g.K.reduce((s,v,i)=>s|(dot(a,v)?bit(i):0n),0n),b^dot(a,g.a)]))));
  return {d:g.K.length,F:fs,lift:x=>g.K.reduce((s,v,i)=>s^((x&bit(i))?v:0n),g.a)}
 }
 // First paid local closure: test every coordinate support on each actual factor, restart on any forced pin.
 function close(n,F,G){let Q=G.slice();while(true){stats.closurePasses++;let g=gauss(n,Q);if(!g)return null;let changed=false;
  outer:for(const f of F){let total=mass(n,f,Q);if(total===0n)return null;assert(total>0n);
   for(let i=0;i<n;i++){let a=bit(i);if(g.K.every(v=>!dot(v,a)))continue;let m=mass(n,f,[...Q,[a,0]]);assert(m>=0n&&m<=total);if(m===0n||m===total){Q.push([a,m===0n?1:0]);stats.forcedPins++;changed=true;break outer}}}
  if(!changed)return Q;
 }}
 function solve(n,F,G=[]){
  let Q=close(n,F,G);if(!Q)return {count:0n,w:null,r:null};let ch=chart(n,F,Q),d=ch.d,fs=ch.F;
  let W=fs.map(f=>spectrum(d,f)),U=basis(d,W.flatMap((v,i)=>inter(d,v,basis(d,W.filter((_,j)=>j!==i).flat()))));
  if(U.length>16)throw Error("test cap");
  let z=0n,first=null;
  for(let j=0;j<2**U.length;j++){stats.sharedWords++;let P=U.map((a,i)=>[a,(j>>i)&1]);let size=pow(d-U.length),m=fs.map(f=>mass(d,f,P));if(m.some(v=>v===0n))continue;
   let num=m.reduce((a,b)=>a*b,1n),den=size**BigInt(Math.max(0,fs.length-1));if(!fs.length)num=size;
   assert(num%den===0n);z+=num/den;if(first===null)first=P}
  if(first===null)return {count:z,w:null,r:U.length,ranks:W.map(w=>w.length)};
  let P=first.slice();
  for(let j=0;j<fs.length;j++)for(const a of W[j]){
   let g=gauss(d,P);if(g.K.every(v=>!dot(v,a)))continue;
   // Exact conditional support test, guard retained; no arbitrary global recompilation.
   let q=[...P,[a,0]];if(mass(d,fs[j],q)>0n)P=q;else{P.push([a,1]);assert(mass(d,fs[j],P)>0n)}stats.witnessPins++;
  }
  let w=ch.lift(gauss(d,P).a);assert(G.every(([a,b])=>dot(a,w)===b)&&F.every(f=>val(f,w)>0n));return {count:z,w,r:U.length,ranks:W.map(w=>w.length)}
 }
 function brute(n,F,G=[]){let z=0n;for(let x=0n;x<pow(n);x++){stats.referenceWords++;if(G.every(([a,b])=>dot(a,x)===b))z+=F.reduce((a,f)=>a*val(f,x),1n)}return z}
 const cube=Array.from({length:8},(_,w)=>[term(1),term(-1,[0,1,2].map(i=>[bit(i),(w>>i)&1]))]);
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].flatMap(L=>[0,1].map(b=>[term(1),term(-1,L.map(i=>[bit(i),b]))]));
 let groups={cube:{sat:0,unsat:0},fano:{sat:0,unsat:0},random:{sat:0,unsat:0}},scales=[];
 function check(k,n,F,G=[]){let a=solve(n,F,G);assert(a.count===brute(n,F,G));groups[k][a.count?"sat":"unsat"]++;return a}
 for(let s=0;s<256;s++)check("cube",3,cube.filter((_,i)=>s&(1<<i)));
 check("fano",7,fano);for(let i=0;i<14;i++)check("fano",7,fano.filter((_,j)=>j!==i));
 let seed=2080730;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 for(let i=0;i<36;i++){
  let n=5,F=Array.from({length:3+rand(4)},()=>[term(1),term(-1,Array.from({length:1+rand(3)},()=>[BigInt(1+rand(31)),rand(2)]))]);
  let G=i%2?[[BigInt(1+rand(31)),rand(2)]]:[];check("random",n,F,G)
 }
 // Independent direct Fourier transform check of semantic rank on signed, not necessarily nonnegative functions.
 for(let i=0;i<40;i++){let n=4,F=Array.from({length:5},()=>term(rand(5)-2,Array.from({length:rand(4)},()=>[BigInt(1+rand(15)),rand(2)])));
  let W=spectrum(n,F),ref=[];for(let a=0n;a<pow(n);a++){let c=0n;for(let x=0n;x<pow(n);x++)c+=val(F,x)*(dot(a,x)?-1n:1n);if(c)ref.push(a)}
  assert(W.length===basis(n,ref).length&&basis(n,[...W,...ref]).length===W.length)
 }
 // Cancellation controls: both raw observation spaces full, effective three-bit nonaffine support.
 for(const n of [8,16,32,64]){
  let core=w=>[0,1,2].map(i=>[bit(i),(w>>i)&1]);
  let A=Array.from({length:n-3},(_,i)=>[bit(i+3),0]),cancel=[term(1,A),term(-1,[...A,[1n,0]]),term(-1,[...A,[1n,1]])];
  let lo=[0,1,2,4].map(w=>term(1,core(w))),hi=[3,5,6,7].map(w=>term(1,core(w)));
  for(const sat of [false,true]){
   let F=[[...lo,...cancel],[...hi,...(sat?[term(1,core(0))]:[]),...cancel]];
   let a=solve(n,F);assert(a.count===(sat?pow(n-3):0n));assert(a.r===3&&a.ranks.every(r=>r===3));scales.push({n,sat,rawShared:n,effectiveShared:a.r,count:String(a.count)});
  }
 }
 // pairwise-zero intersections do not imply independent factors: x=0,y=0,x+y=1.
 let triple=[[term(1,[[1n,0]])],[term(1,[[2n,0]])],[term(1,[[3n,1]])]];assert(solve(2,triple).count===0n);
 // Support-period hardness control on all source cubes: f=#violations+t; t direction is a support period iff UNSAT.
 let supportPeriod={yes:0,no:0};
 for(let s=0;s<256;s++){let F=cube.filter((_,i)=>s&(1<<i));let f=[term(1,[[8n,1]]),...F.map(c=>term(1,c[1].E))];
  let p=true;for(let x=0n;x<8n;x++)if((val(f,x)>0n)!==(val(f,x|8n)>0n))p=false;
  assert(p===(s===255));supportPeriod[p?"yes":"no"]++;
 }
 return {groups,scales,supportPeriod,stats,seed:2080730,notes:"Exact BigInt; no time/space instrumentation; local coordinate-support closure, not complete affine semantic closure. Physical source adapters not executed."};
}
console.log(JSON.stringify(runBA07(),null,2));
