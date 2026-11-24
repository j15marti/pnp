// RT07 deterministic tests, node RT07_check.js
function run(){
let seed=0x57a71329;const rnd=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0;};
const A=(x,m)=>{if(!x)throw Error(m);},bit=i=>1n<<BigInt(i),tag=(n,x,z)=>bit(x)^(z===n-1?0n:bit(n+z)),target=n=>bit(2*n-1)-1n,key=t=>t.join(",");
function cyc(n){return Array.from({length:n*n},(_,i)=>[i%n,Math.floor(i/n),(i%n+Math.floor(i/n))%n]);}
function extra(n){return [n/2,n-1,n-1];}
function witness(n){return [...Array.from({length:n-1},(_,y)=>{let x=y+(y>=n/2?1:0);return [x,y,(x+y)%n];}),extra(n)];}
function group(n,T){let a=Array.from({length:n},()=>[]);for(let t of T)a[t[1]].push(t);return a;}
function verify(n,T,W){let D=new Set(T.map(key)),Y=new Set(),s=0n;for(let [x,y,z] of W){if(!D.has(key([x,y,z]))||Y.has(y))return false;Y.add(y);s^=tag(n,x,z);}return s===target(n);}
let tuples=0,nodes=0;
function support(n,T){let a=group(n,T),s=new Set();function rec(y,v){if(y===n){tuples++;s.add(v);return;}rec(y+1,v);for(let [x,,z] of a[y])rec(y+1,v^tag(n,x,z));}rec(0,0n);return s;}
function perfect(n,T){let a=group(n,T);function rec(y,X,Z){nodes++;if(y===n)return true;for(let [x,,z] of a[y])if(!(X&bit(x))&&!(Z&bit(z))&&rec(y+1,X|bit(x),Z|bit(z)))return true;return false;}return rec(0,0n,0n);}
function parity(a){let b=0;while(a){a&=a-1n;b^=1;}return b;}
function add(B,v,w=0n){while(v){let j=v.toString(2).length-1;if(B[j]){v^=B[j][0];w^=B[j][1];}else{B[j]=[v,w];return true;}}return false;}
function solve(B,v){let w=0n;while(v){let j=v.toString(2).length-1;A(B[j],"span");v^=B[j][0];w^=B[j][1];}return w;}
function rank(V){let B=[];for(let v of V)add(B,v);return B.filter(Boolean).length;}
function masks(d,k){let B=[],m=[];while(m.length<k){let v=0n;for(let j=0;j<d;j+=32)v|=BigInt(rnd())<<BigInt(j);v&=bit(d)-1n;if(add(B,v))m.push(v);}return m;}
function proj(v,m){let p=0n;for(let i=0;i<m.length;i++)if(parity(v&m[i]))p|=bit(i);return p;}
let sat=0,unsat=0,oneBit=0,projections=0,guarded=0,exactProjections=0,pairRanks=0;
for(let n of [2,3,4])for(let it=0;it<24;it++){let T=[];for(let y=0;y<n;y++)for(let x=0;x<n;x++)for(let z=0;z<n;z++)if(rnd()%100<(it%2?30:12))T.push([x,y,z]);let S=support(n,T),b=perfect(n,T);A(S.has(target(n))===b,"3DM");b?sat++:unsat++;
for(let m=1n;m<bit(2*n-1);m++){let a=parity(target(n)&m)===0||T.some(([x,,z])=>parity(tag(n,x,z)&m)===1);A(a===[...S].some(s=>parity(s&m)===parity(target(n)&m)),"1bit");oneBit++;}}
let exact=[];
for(let n of [2,4,6]){let T=cyc(n),S=support(n,T),T2=[...T,extra(n)],S2=support(n,T2);A(!S.has(target(n))&&!perfect(n,T),"UNSAT");A(S2.has(target(n))&&perfect(n,T2)&&verify(n,T2,witness(n)),"SAT neighbor");
for(let k=1;k<=n/2;k++)for(let i=0;i<8;i++){let m=masks(2*n-1,k),P=new Set();for(let s of S){P.add(proj(s,m));if(P.size===2**k)break;}A(P.size===2**k,"exact projected support");exactProjections++;}
exact.push({n,support:S.size,neighborSupport:S2.size});}
let scaling=[];
for(let n of [2,4,8,16,32,64]){let T=cyc(n),a=group(n,T);A(verify(n,[...T,extra(n)],witness(n)),"lift");A((n*(n-1)/2)%n===n/2,"modular");
for(let y=0;y<n;y+=2){A(rank([...a[y],...a[y+1]].map(([x,,z])=>tag(n,x,z)))===2*n-1,"pair rank");pairRanks++;}
for(let p of [...new Set([0,Math.floor(n/4),n/2-1])]){let k=n/2-p,m=masks(2*n-1,k),pins=[],used=new Set(),fixed=[],base=0n;
while(pins.length<p){let y=rnd()%n;if(used.has(y))continue;used.add(y);let row=a[y][rnd()%n],v=rnd()%2;pins.push([row,v]);if(v){fixed.push(row);base^=tag(n,row[0],row[2]);}}
let B=[],rows=[];for(let y=0;y<n&&rows.length<k;y+=2){if(used.has(y)||used.has(y+1))continue;let ok=false;for(let row of [...a[y],...a[y+1]])if(add(B,proj(tag(n,row[0],row[2]),m),bit(rows.length))){rows.push(row);ok=true;break;}A(ok,"basis");}
A(rows.length===k,"rank");let w=solve(B,proj(target(n)^base,m)),W=[...fixed];for(let j=0;j<k;j++)if(w&bit(j))W.push(rows[j]);let Y=new Set(),v=0n,keys=new Set(W.map(key));for(let [x,y,z] of W){A(!Y.has(y),"cap");Y.add(y);v^=tag(n,x,z);}for(let [row,b] of pins)A(keys.has(key(row))===!!b,"pin");A(proj(v,m)===proj(target(n),m),"witness");projections++;if(p)guarded++;}
scaling.push({n,blocks:n*n,effectiveTags:2*n-1,projectionRank:n/2});}
let squareMasks=0;for(let mask=0;mask<16;mask++){let d=[0,0,0,0];for(let e=0;e<4;e++)if(mask>>e&1){d[e]^=1;d[(e+1)%4]^=1;}A((d.join("")==="1010")===(mask===3||mask===12),"square");squareMasks++;}
return {seed:"0x57a71329",sat,unsat,tuples,nodes,oneBit,exactProjections,projections,guarded,pairRanks,squareMasks,exact,scaling,disagreements:0};}
if(typeof module!=="undefined")module.exports=run;
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
