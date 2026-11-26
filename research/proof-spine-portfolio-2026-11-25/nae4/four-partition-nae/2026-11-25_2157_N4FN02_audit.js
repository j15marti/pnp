// N4FN02 GF(3) chart audit. Run: node <this file> <pinned N4ES07 audit.js>.
function run(peer){
let checks=0,seed=123456789;
function ck(x,s){checks++;if(!x)throw Error(s)}
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
function perm(n){let a=Array.from({length:n},(_,i)=>i);for(let i=n-1;i>0;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
function valid(P,n){let ps=new Set();ck(P.length===4,"partitions");for(let Q of P){let seen=new Set();for(let t of Q){ck(t.length===3&&new Set(t).size===3,"triple");for(let v of t){ck(v>=0&&v<n&&!seen.has(v),"incidence");seen.add(v)}for(let a=0;a<3;a++)for(let b=a+1;b<3;b++){let k=[t[a],t[b]].sort((a,b)=>a-b).join(",");ck(!ps.has(k),"linear");ps.add(k)}}ck(seen.size===n,"cover")}}
function sat(T,x){return T.every(([a,b,c])=>x[a]!==x[b]||x[a]!==x[c])}
function matrix(T,n){
 const W=Math.ceil(n/32), piv=Array(n).fill(null);let rank=0,adds=0;
 for(let t of T){
  let a=new Uint32Array(W),b=new Uint32Array(W);
  for(let v of t)a[v>>>5]|=1<<(v&31);
  for(let w=0;w<W;){
   let u=(a[w]|b[w])>>>0;if(!u){w++;continue}
   let j=31-Math.clz32(u&-u),k=32*w+j,one=(a[w]>>>j)&1;
   if(!piv[k]){piv[k]=one?[a,b]:[b,a];rank++;break}
   let [c,d]=piv[k];if(one)[c,d]=[d,c];
   for(let h=w;h<W;h++){
    let A=a[h],B=b[h],C=c[h],D=d[h],Z=~(A|B),Y=~(C|D);
    a[h]=(A&Y)|(Z&C)|(B&D);b[h]=(B&Y)|(Z&D)|(A&C);
   }adds++;
  }
 }
 let free=[];for(let j=0;j<n;j++)if(!piv[j])free.push(j);
 function vector(vals){
  let x=new Uint8Array(n);free.forEach((j,i)=>x[j]=vals[i]);
  for(let j=n-1;j>=0;j--)if(piv[j]){
   let s=0,[a,b]=piv[j];for(let w=j>>>5;w<W;w++){
    let A=a[w],B=b[w];while(A){let k=31-Math.clz32(A&-A);s+=x[w*32+k];A&=A-1}
    while(B){let k=31-Math.clz32(B&-B);s+=2*x[w*32+k];B&=B-1}
   }x[j]=(3-s%3)%3;
  }ck(T.every(t=>t.reduce((s,v)=>s+x[v],0)%3===0),"kernel vector");return x;
 }
 return {rank,free,vector,adds}
}
function denseRank(T,n){let p=Array(n).fill(null),r=0;for(let t of T){let a=Array(n).fill(0);for(let v of t)a[v]=(a[v]+1)%3;for(let i=0;i<n;i++)if(a[i]){if(!p[i]){let c=a[i];p[i]=a.map(x=>x*c%3);r++;break}let c=a[i];for(let j=i;j<n;j++)a[j]=(a[j]+6-c*p[i][j])%3}}return r}
function graphRank(T,n){let p=Array.from({length:n},(_,i)=>i),r=0;function f(i){while(p[i]!==i){p[i]=p[p[i]];i=p[i]}return i}for(let [a,b,c] of T)for(let v of [b,c]){let x=f(a),y=f(v);if(x!==y){p[x]=y;r++}}return r}
function solve(P,n){
 valid(P,n);let map=perm(n),Q=perm(4).map(j=>perm(P[j].length).map(i=>perm(3).map(k=>map[P[j][i][k]]))),T=Q.flat();
 valid(Q,n);
 // Unguarded local closure, exact tables: unary and pair differences have both values.
 for(let t of T){let v=[[],[],[]],pair=[new Set(),new Set(),new Set()];for(let w=1;w<7;w++){for(let k=0;k<3;k++)v[k].push(w>>k&1);for(let k=0;k<3;k++)pair[k].add((w>>k&1)^(w>>((k+1)%3)&1))}ck(v.every(a=>new Set(a).size===2)&&pair.every(a=>a.size===2),"local closure")}
 let {rank,free,vector,adds}=matrix(T,n);if(n<=170)ck(rank===denseRank(T,n),"rank crosscheck");
 let tested=0,witness=null;
 function test(vals){let x=vector(vals);tested++;if(T.every(([a,b,c])=>x[a]!==x[b]&&x[a]!==x[c]&&x[b]!==x[c])){let y=Array.from(x,v=>+(v===1));ck(sat(T,y),"binary lift");let z=map.map(v=>y[v]);ck(sat(P.flat(),z),"original IDs");witness=z;return true}return false}
 for(let i=0;i<free.length&&!witness;i++){let a=Array(free.length).fill(0);a[i]=1;test(a)}
 if(!witness&&free.length<=8){for(let i=0;i<3**free.length&&!witness;i++){let a=Array.from({length:free.length},(_,j)=>Math.floor(i/3**j)%3);test(a)}}
 return {n,m:T.length,rank,nullity:n-rank,components:n-graphRank(T,n),D:T.length-graphRank(T,n),adds,tested,answer:witness?"SAT":"UNKNOWN",witnessChecked:!!witness}
}
let random=[],rings=[],exact=[];
let marker="let {P,tries}=source(p),n=3*p,T=P.flat();";
let needle="valid(U,33*k);valid(V,33*k);";
ck(peer.includes(marker)&&peer.includes(needle),"peer revision");
let sourcePrefix=peer.slice(peer.indexOf("let seed="),peer.indexOf("function rank(a)"));
let capture= new Function("take","takeRing",sourcePrefix+`
for(let p of [17,53,127,509,1021]){
 let {P,tries}=source(p),T=P.flat(),n=3*p;take(p,tries,P);
 let inc=Array.from({length:n},()=>[]);T.forEach((t,i)=>t.forEach(v=>inc[v].push(i)));
 let adj=T.map(t=>[...new Set(t.flatMap(v=>inc[v]))]);
 for(let q=0;q<100;q++){let ids=[rnd(T.length)],k=1+rnd(7);while(ids.length<k){let a=[...new Set(ids.flatMap(i=>adj[i]))].filter(i=>!ids.includes(i));if(!a.length)break;ids.push(a[rnd(a.length)]);}}
}
`+peer.slice(peer.indexOf("let H="),peer.indexOf("return {seed:20261125,checks,random,rings,Hmodels")).replace(needle,needle+"takeRing(k,U,V,H,models);"));
capture((p,tries,P)=>{let r=solve(P,3*p);random.push({p,tries,...r});ck(r.answer==="SAT"&&r.nullity===2,"peer chart")},(k,U,V,H,models)=>{
 let a=solve(U,33*k),b=solve(V,33*k);ck(a.answer==="UNKNOWN","known NO decline");
 ck(models.length===12&&new Set(models.map(x=>x.slice(0,6).join(""))).size===2&&models.every(x=>x.slice(0,3).every(z=>z===x[0])&&x.slice(3,6).every(z=>z===1-x[0])),"H exact");
 rings.push({k,U:a,V:b,referenceU:"NO by exact H and odd cycle",referenceV:"SAT peer verified"});
 if(k===3){let p=H.flat(),best=-Infinity,proper=-Infinity,at=0,count=0;for(let mask=0;mask<(1<<p.length);mask++){let S=p.filter((_,i)=>mask>>i&1),d=S.length-graphRank(S,9);best=Math.max(best,d);if(mask!==(1<<p.length)-1)proper=Math.max(proper,d);if(d===4)at++;count++}
 ck(best===4&&proper<=3&&at===1,"unique max deficiency");let r=solve(H,9);ck(r.answer==="UNKNOWN","AG decline");let solutions=0;for(let w=0;w<512;w++)solutions+=+sat(p,Array.from({length:9},(_,i)=>w>>i&1));ck(solutions===0,"AG oracle");exact.push({case:"AG(2,3)",subsets:count,D:best,maxProper:proper,maximizers:at,solutions,chart:r});
 }
});
let rankChecks=0;for(let n=3;n<=15;n++)for(let k=0;k<25;k++){let T=Array.from({length:1+rnd(30)},()=>perm(n).slice(0,3));let a=matrix(T,n);ck(a.rank===denseRank(T,n),"random rank");for(let j=0;j<a.free.length;j++){let v=Array(a.free.length).fill(0);v[j]=1;a.vector(v)}rankChecks++}
return {checks,rankChecks,random,rings,exact,notes:"Exact N4ES07 generator and draw sequence, then independent relabel; source chart only accepts verified SAT, never rejects. Ring NO and YES reference via separate exact H relation and peer verified witness; chart UNKNOWN is not UNSAT. No exhaustive large source solving."}
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){console.log(JSON.stringify(run(require("fs").readFileSync(process.argv[2],"utf8")),null,2))}
