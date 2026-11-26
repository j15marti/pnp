// Standalone Node.js audit. Small random and exhaustive controls; not a universal solver.
function audit(){
const out={seed:3289011,random:0,sat:0,unsat:0,augmentations:0,swaps:0,rankChecks:0,strict:0,strictSat:0,strictUnsat:0,strictCertificateChecks:0,forcedDeductions:0,family:[]};
let seed=out.seed;const rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed};const rand=n=>Math.floor(rng()/4294967296*n);
function check(v,s){if(!v)throw Error(s)}
function rank(v){out.rankChecks++;const B=new Map();for(let a of v){while(a){const i=a.toString(2).length-1;if(!B.has(i)){B.set(i,a);break}a^=B.get(i)}}return B.size}
function parity(a){let p=0;while(a){a&=a-1n;p^=1}return p}
function good(e,x){return parity(e[0]&x)===e[1]}
function sat(G,x){return G.every(g=>g.some(e=>good(e,x)))}
function consistent(F,n){return rank(F.map(e=>e[0]))===rank(F.map(e=>e[0]|(BigInt(e[1])<<BigInt(n))))}
function maxrank(G){let best=0;function rec(i,F){if(i===G.length){best=Math.max(best,rank(F));return}for(const e of G[i])rec(i+1,F.concat(e[0]))}rec(0,[]);return best}
function strict(G){let m=G.length;if(rank(G.flat().map(e=>e[0]))!==m-1)return false;for(let s=1;s<(1<<m)-1;s++){let rows=[];for(let i=0;i<m;i++)if(s>>i&1)rows.push(...G[i].map(e=>e[0]));if(rank(rows)<parityCount(s))return false}return true}
function parityCount(s){let k=0;while(s){s&=s-1;k++}return k}
function upgrade(G,F,n){F=F.slice();while(true){let W=F.map(e=>e[0]),r=rank(W),C=[],J=[];for(let j=0;j<W.length;j++)(rank(W.filter((_,i)=>i!==j))===r?C:J).push(j);
let prev=new Map(C.map(i=>[i,null])),Q=C.slice(),end=null,last=null;
for(let pos=0;pos<Q.length&&end===null;pos++){let i=Q[pos];for(let a of G[i]){if(rank(W.concat(a[0]))>r){end=i;last=a;break}for(let j of J)if(!prev.has(j)&&rank(W.filter((_,l)=>l!==j).concat(a[0]))===r){prev.set(j,[i,a]);Q.push(j)}}}
if(end===null){let S=[...prev.keys()],u=rank(S.flatMap(i=>G[i].map(e=>e[0])));check(S.length-u===F.length-r,"closed set deficiency");return F}
let i=end,a=last;while(true){let old=F[i];F[i]=a;out.swaps++;check(consistent(F,n),"lost consistency");let v=prev.get(i);if(v===null)break;[i,a]=v}
check(rank(F.map(e=>e[0]))===r+1,"augmentation failed");out.augmentations++}}
function brute(G,n){let xs=[];for(let x=0;x<(1<<n);x++)if(sat(G,BigInt(x)))xs.push(BigInt(x));return xs}
function fullCert(G,n){let found=false,m=G.length;function rec(i,F){if(i===m){if(rank(F.map(e=>e[0]))===m-1&&consistent(F,n))found=true;return}for(const e of G[i])if(!found)rec(i+1,F.concat([e]))}rec(0,[]);return found}
for(let trial=0;trial<700;trial++){let n=2+rand(5),m=2+rand(5),G=Array.from({length:m},()=>Array.from({length:2+rand(2)},()=>[BigInt(1+rand((1<<n)-1)),rand(2)]));let xs=brute(G,n);out.random++;if(xs.length){out.sat++;let F=G.map(g=>g.find(e=>good(e,xs[0])));let H=upgrade(G,F,n);check(rank(H.map(e=>e[0]))===maxrank(G),"not maximum rank");check(consistent(H,n),"final consistency")}else out.unsat++;
if(strict(G)){out.strict++;if(xs.length)out.strictSat++;else out.strictUnsat++;check(fullCert(G,n)===(xs.length>0),"strict certificate");out.strictCertificateChecks++}}
const E=(u,v)=>(1n<<BigInt(u))^(1n<<BigInt(v));
let pairs=[[[0,1],[2,3]],[[0,2],[1,4]],[[0,3],[2,4]],[[0,4],[1,3]],[[1,2],[3,4]]],K=pairs.map(g=>g.map(([u,v])=>[E(u,v),1]));
check(strict(K),"K5 strict");check(brute(K,5).length===0,"K5 UNSAT");let C=[K[0][1],K[1][1],K[2][1],K[3][1]];check(rank(C.map(e=>e[0]))===3&&consistent(C,5),"K5 balanced circuit");check(rank(C.map(e=>e[0]).concat(K[4].map(e=>e[0])))===3,"K5 no extension");out.K5={strict:true,satModels:0,circuit:C.map(e=>e[0].toString()),cycleRank:3,quotientRank:0,neighbors:[]};
for(let i=0;i<5;i++)for(let j=0;j<2;j++){let G=K.map(g=>g.map(e=>e.slice()));G[i][j][1]^=1;let xs=brute(G,5);check(xs.length>0,"neighbor SAT");let F=upgrade(G,G.map(g=>g.find(e=>good(e,xs[0]))),5);check(rank(F.map(e=>e[0]))===4,"neighbor full rank");out.K5.neighbors.push(xs.length)}
for(let n of [8,10,14,16,32,64,128,256]){let A=Array.from({length:n},(_,i)=>E(i,(i+1)%n));let c=Array(n).fill(0),make=c=>A.map((a,i)=>[[a,c[i]],[A[(i+3)%n],1^c[(i+3)%n]]]);let G=make(c),F=G.map(g=>g[0]);check(consistent(F,n)&&rank(F.map(e=>e[0]))===n-1,"cycle SAT");c[0]=1;let U=make(c);check(!consistent(U.map(g=>g[0]),n)&&!consistent(U.map(g=>g[1]),n),"cycle UNSAT parity");if(n<=14){check(strict(G),"family strict");check(brute(G,n).length===4&&brute(U,n).length===0,"family brute");}out.family.push({n,shortestBalancedExtendableCircuitSAT:n,UNSAT:"no balanced rainbow circuit",brute:n<=14})}
return out;
}
console.log(JSON.stringify(audit(),null,2));
