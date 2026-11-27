function run(){
const C=[];for(let x=0;x<5;x++)for(let y=0;y<5;y++)for(let z=0;z<5;z++){let s=[x,y,z].sort().join("");if(["012","123","234","034","014"].includes(s))C.push([x,y,z]);}
const cs=new Set(C.map(x=>x.join(""))),R=(x,y,z)=>((y-x+5)%5===1||(y-x+5)%5===3)&&((x-z+5)%5===1||(x-z+5)%5===3)||((z-x+5)%5===1||(z-x+5)%5===3)&&((x-y+5)%5===1||(x-y+5)%5===3);
let cr=0,frames=0;for(let x=0;x<5;x++)for(let y=0;y<5;y++)for(let z=0;z<5;z++){if(cs.has([x,y,z].join(""))!==(R(x,y,z)&&R(y,x,z)))throw Error("C/R");cr++;}
for(let j=0;j<3125;j++){let u=Array.from({length:5},(_,i)=>Math.floor(j/5**i)%5);if(u.every((_,i)=>cs.has([u[i],u[(i+1)%5],u[(i+2)%5]].join(""))))frames++;}

function native(F){let {E,t,d}=F,n=5,clauses=[];const fresh=()=>n++,cl=(...v)=>{if(new Set(v).size!==3)throw Error("repeat");clauses.push(v);},wire=()=>{let p=fresh();for(let j=2;j<=4;j++)cl(j,p,fresh());return p;},not=p=>{let x=wire();cl(2,p,x);return x;},or=(p,q)=>{let x=wire(),u=fresh(),v=fresh();cl(1,2,u);cl(0,1,v);cl(4,p,u);cl(3,q,v);cl(x,u,v);return x;},and=(p,q)=>not(or(not(p),not(q))),pin=p=>cl(0,2,p);
for(let i=0;i<5;i++)cl(i,(i+1)%5,(i+2)%5);let one=wire();pin(one);let zero=not(one),X=E.map(wire);
for(let side=0;side<2;side++)for(let i=0;i<t;i++){let p=zero;for(let j=0;j<E.length;j++)if(E[j][side]===i){pin(not(and(p,X[j])));p=or(p,X[j]);}pin(p);}
let s=Array.from({length:d+1},(_,i)=>i?zero:one);for(let j=0;j<E.length;j++){let c=E[j][2];if(!c)continue;let nx=not(X[j]);s=s.map((p,i)=>or(and(nx,p),and(X[j],i<c?zero:s[i-c])));}pin(s[d]);
const m=clauses.length,N=n+2+2*Math.floor(Math.log2(m+1))+3*m*Math.ceil(Math.log2(n+1)),adj=Array.from({length:n},()=>[]);clauses.forEach((c,i)=>c.forEach(v=>adj[v].push(i)));
function gac(pins){let D=new Uint8Array(n).fill(31),queue=Array.from({length:m},(_,i)=>i),inq=new Uint8Array(m).fill(1),checks=0,updates=0;for(let [v,val] of pins)D[v]=1<<val;for(let k=0;k<queue.length;k++){let i=queue[k];inq[i]=0;let v=clauses[i],s=[0,0,0];for(let u of C){checks++;if(u.every((a,j)=>D[v[j]]&(1<<a)))u.forEach((a,j)=>s[j]|=1<<a);}for(let j=0;j<3;j++)if(s[j]!==D[v[j]]){D[v[j]]=s[j];updates++;if(!s[j])return {no:true,checks,updates};for(let h of adj[v[j]])if(!inq[h]){inq[h]=1;queue.push(h)}}}return {no:false,checks,updates};}
let anchor=Array.from({length:5},(_,i)=>[i,i]);return {n,m,N,unpinned:gac([]),anchored:gac(anchor),afterVerifiedOutputZero:gac(anchor.concat([[s[d],0]]))};}


const cap=200000, d=5, bit=i=>1n<<BigInt(i);
function make(R,C,hostile=false){
 let rows=[],cols=[],map=new Map();for(let i=0;i<R;i++)for(let j=0;j<C;j++){let a=(i+j)%2?cols:rows;map.set(i*C+j,a.length);a.push([i,j]);}
 let q=rows.length, t=q, E=[], pieces=[], core=[];
 for(let [u,[i,j]] of rows.entries())for(let [di,dj] of [[0,1],[1,0],[0,-1],[-1,0]]){let x=i+di,y=j+dj;if(x<0||x>=R||y<0||y>=C)continue;let v=map.get(x*C+y),h=t; t+=8;let es=[];
 for(let a=0;a<3;a++)for(let b=0;b<3;b++)es.push([h+a,h+b,0]);
 for(let a=3;a<8;a++)es.push([h+a,h+a,0]);
 for(let cyc of [[0,3,4],[0,5,6,7]])for(let k=0;k<cyc.length;k++)es.push([h+cyc[k],h+cyc[(k+1)%cyc.length],hostile&&core.length===0&&cyc.length===4&&k===0?2:1]);
 es.push([u,h,0],[h,v,0]); core.push({u,v,sign:di!==0&&j%2?-1:1,h});pieces.push(es);E.push([u,v,0],...es);}
 return {R,C,q,t,E,pieces,core,d};
}
const zero=()=>Array(d+1).fill(0n), one=()=>[1n,...Array(d).fill(0n)], plus=(a,b)=>a.map((x,i)=>x+b[i]);
function mul(a,b){let c=zero();for(let i=0;i<=d;i++)for(let j=0;i+j<=d;j++)c[i+j]+=a[i]*b[j];return c;}
function pow(a,n){let p=one();while(n--)p=mul(p,a);return p;}
function edgeDP(F){let {E,t}=F,last=new Map(),M=new Map([[0n,one()]]),ops=0,peak=1;E.forEach((e,i)=>{last.set(e[0],i);last.set(t+e[1],i)});for(let i=0;i<E.length;i++){let e=E[i],b=bit(e[0])|bit(t+e[1]),forget=0n;for(let v of [e[0],t+e[1]])if(last.get(v)===i)forget|=bit(v);let Q=new Map();for(let [m,p] of M)for(let take of [0,1]){if(++ops>cap)return {status:"UNKNOWN",ops,peak};if(take&&(m&b))continue;let u=m|(take?b:0n);if((u&forget)!==forget)continue;let c=take?e[2]:0,k=u&~forget,v=Q.get(k)||zero();for(let j=c;j<=d;j++)v[j]+=p[j-c];if(v.some(x=>x))Q.set(k,v);}M=Q;peak=Math.max(peak,M.size);}return {coeff:(M.get(0n)||zero()).map(String),ops,peak};}
function local(F,i,used,counter){let {u,v,h}=F.core[i],E=F.pieces[i],rs=Array.from({length:8},(_,a)=>h+a),cs=rs.slice();if(used){rs.unshift(u);cs.unshift(v);}let allowed=new Set(cs),p=zero();function rec(k,S,c){if(++counter.n>cap)throw Error("cap");if(k===rs.length){p[c]++;return;}for(let e of E)if(e[0]===rs[k]&&allowed.has(e[1])&&!S.has(e[1])&&c+e[2]<=d){S.add(e[1]);rec(k+1,S,c+e[2]);S.delete(e[1]);}}rec(0,new Set(),0);return p;}
function det(A){let n=A.length,prev=1n,sg=1n,ops=0;A=A.map(r=>r.slice());for(let k=0;k<n-1;k++){let i=k;while(i<n&&!A[i][k])i++;if(i===n)return {value:0n,ops};if(i!==k){[A[i],A[k]]=[A[k],A[i]];sg=-sg;}let p=A[k][k];for(let i=k+1;i<n;i++){for(let j=k+1;j<n;j++){let v=A[i][j]*p-A[i][k]*A[k][j];if(v%prev)throw Error("nonexact");A[i][j]=v/prev;ops++;}A[i][k]=0n;}prev=p;}return {value:sg*A[n-1][n-1],ops};}
function hybrid(F){let count={n:0},sig=F.core.map((_,i)=>[local(F,i,false,count),local(F,i,true,count)]),q=F.q;
 // Uniform signatures permit factoring all unused gadgets and chosen-edge signatures.
 let A=sig[0][0],B=sig[0][1];if(sig.some(([a,b])=>a.join()!=A.join()||b.join()!=B.join()))return {status:"NONUNIFORM",signatures:sig.map(x=>x.map(y=>y.map(String)))};
 let M=Array.from({length:q},()=>Array(q).fill(0n));for(let e of F.core)M[e.u][e.v]=BigInt(e.sign);
 let D=det(M),countCore=D.value<0n?-D.value:D.value;
 let p=mul(pow(A,F.core.length-q),pow(plus(A,B),q)).map(x=>String(x*countCore));
 return {coeff:p,localVisits:count.n,detUpdates:D.ops,coreCount:String(countCore),A:A.map(String),B:B.map(String)};
}
function brute(F){let {t,E}=F,A=Array.from({length:t},()=>[]);E.forEach(e=>A[e[0]].push(e));let p=zero(),visits=0,abort=false;function rec(i,U,c){if(abort)return;if(++visits>cap){abort=true;return;}if(i===t){p[c]++;return;}for(let e of A[i])if(!(U&bit(e[1]))&&c+e[2]<=d)rec(i+1,U|bit(e[1]),c+e[2]);}rec(0,0n,0);return {visits,coeff:abort?null:p.map(String)};}
let out=[];for(let [r,c] of [[2,2],[2,4],[4,4]]){let F=make(r,c),A=edgeDP(F),B=hybrid(F),C=brute(F);if(B.coeff[d]!=="0")throw Error("no output deduction");let T=native(F);if(!T.afterVerifiedOutputZero.no)throw Error("reclosure");if(A.coeff&&A.coeff.join()!=B.coeff.join()||C.coeff&&C.coeff.join()!=B.coeff.join()||B.coeff[d]!=="0")throw Error("disagreement");out.push({r,c,t:F.t,E:F.E.length,pieces:F.pieces.length,A,B,C,T});}
let H=make(2,2,true),HC=edgeDP(H),HB=brute(H);if(!HC.coeff||HC.coeff[d]==="0"||HB.coeff&&HB.coeff.join()!=HC.coeff.join())throw Error("hostile");
return {cr,frames,out,hostile:{HC,HB}};

}
if(typeof module!=='undefined')module.exports=run;if(typeof require!=='undefined'&&require.main===module)console.log(JSON.stringify(run(),null,2));