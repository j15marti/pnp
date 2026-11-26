// N4FN04: exact topology / compiler audit. Run node audit.js.
let seed=20261125,checks=0;
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
function ok(x){checks++;if(!x)throw Error("assertion "+checks)}
function perm(n){let a=Array.from({length:n},(_,i)=>i);for(let i=n-1;i>0;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
const P=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]];
const local=P.flat().slice(2);
function nae(a){return a.some(x=>x!==a[0])}
function valid(F,x){return F.every(p=>p.every(c=>nae(c.map(v=>x[v]))))}
function auth(F,n){ok(F.length===4);let seen=new Set;for(let p of F){let C=Array(n).fill(0);for(let a of p){ok(a.length===3&&new Set(a).size===3);for(let v of a){ok(v>=0&&v<n);C[v]++}for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let s=[a[i],a[j]].sort((a,b)=>a-b).join(",");ok(!seen.has(s));seen.add(s)}}ok(C.every(x=>x===1))}}
function emptyModules(k){let F=Array.from({length:4},()=>[]);for(let i=0;i<k;i++)for(let j=0;j<4;j++)for(let c of (j?P[j]:P[0].slice(2)))F[j].push(c.map(v=>v+9*i));return F}
function ring(pi,sg){let k=pi.length,F=emptyModules(k);for(let i=0;i<k;i++){F[0].push([9*i,9*i+1,9*pi[i]+2],[9*i+3,9*i+4,9*sg[i]+5])}return F}
function shuffle(F,n){let a=perm(n);return perm(4).map(j=>perm(F[j].length).map(i=>F[j][i].map(v=>a[v])))}
function oracle(F,n){let words=[];for(let i=0;i<2**n;i++){let x=Array.from({length:n},(_,v)=>(i>>v)&1);if(valid(F,x))words.push(x)}return words}
function compile(F,n){let G=emptyModules(3*n),pool=[];for(let i=0;i<n;i++){let a=27*i,b=a+9,c=a+18;G[0].push([a,a+1,b+3],[c+3,c+4,b]);pool.push([[a+2,b+1,b+2,c,c+1,c+2],[a+3,a+4,a+5,b+4,b+5,c+5]])}
for(let j=0;j<4;j++)for(let r=0;r<3;r++){let sign=(j<2?r===2:r!==0)?1:0;for(let c of F[j])G[0].push(c.map(i=>pool[i][sign].pop()))}ok(pool.every(p=>p.every(a=>a.length===0)));return G}
function lift(x,k=1){return x.flatMap(z=>Array.from({length:k},()=>[z,z,z,1-z,1-z,1-z,0,0,1]).flat())}
function cyclic(p){return Array.from({length:4},(_,j)=>Array.from({length:p},(_,i)=>[i,p+(i+j)%p,2*p+(i+2*j)%p]))}
function parityGraph(pi,sg){let k=pi.length,g=Array.from({length:k},()=>[]),x=Array(k).fill(-1);for(let i=0;i<k;i++)for(let j of [pi[i],sg[i]]){g[i].push(j);g[j].push(i)}for(let i=0;i<k;i++)if(x[i]<0){x[i]=0;let q=[i];for(let t=0;t<q.length;t++){let u=q[t];for(let v of g[u]){if(x[v]<0){x[v]=1-x[u];q.push(v)}else if(x[v]===x[u])return null}}}return x}
function localClosure(F,n){let x=Array(n).fill(-1),cs=F.flat(),incident=Array.from({length:n},()=>[]);for(let i=0;i<cs.length;i++)for(let v of cs[i])incident[v].push(i);
let nbr=Array.from({length:n},(_,v)=>[...new Set([v,...incident[v].flatMap(i=>cs[i])])].sort((a,b)=>a-b));
let seen=new Set,mods=[];for(let S of nbr){let key=S.join(",");if(seen.has(key))continue;seen.add(key);if(S.length!==9)continue;let ss=new Set(S),owners=[...new Set(S.flatMap(v=>incident[v]))].filter(i=>cs[i].every(v=>ss.has(v)));if(owners.length>=11)return {answer:false,mods:mods.length,reason:"11-lines"};
if(owners.length!==10)continue;let a=Array.from({length:9},()=>[]),ix=new Map(S.map((v,i)=>[v,i])),edges=new Set;for(let i of owners)for(let j=0;j<3;j++)for(let k=j+1;k<3;k++){let [v,w]=[ix.get(cs[i][j]),ix.get(cs[i][k])].sort((a,b)=>a-b);edges.add(v*9+w)}
for(let j=0;j<9;j++)for(let k=j+1;k<9;k++)if(!edges.has(j*9+k)){a[j].push(k);a[k].push(j)}
let A=a.findIndex(t=>t.length===2);if(A<0)continue;let L=[A,...a[A]],R=a.map((t,i)=>t.length===2&&!L.includes(i)?i:-1).filter(i=>i>=0);
let tri=L=>L.length===3&&L.every(i=>a[i].length===2&&L.every(j=>i===j||a[i].includes(j)));
if(!tri(L)||!tri(R)||a.some((t,i)=>t.length&&!L.includes(i)&&!R.includes(i)))continue;
mods.push([L.map(i=>S[i]),R.map(i=>S[i])]);}
let parent=Array.from({length:n},(_,i)=>i),rank=Array(n).fill(0),p=Array(n).fill(0);
function find(i){if(parent[i]===i)return [i,0];let [r,d]=find(parent[i]);p[i]^=d;parent[i]=r;return [r,p[i]]}
function join(i,j,v){let [a,b]=find(i),[c,d]=find(j);if(a===c)return (b^d)===v?0:-1;if(rank[a]<rank[c])[a,c]=[c,a];parent[c]=a;p[c]=b^d^v;if(rank[a]===rank[c])rank[a]++;return 1}
for(let [a,b] of mods)for(let [v,d] of [...a.map(v=>[v,0]),...b.map(v=>[v,1])])if(join(a[0],v,d)<0)return {answer:false,mods:mods.length,reason:"module-parity"};
let residual=[],changes=0;for(;;){let update=0;residual=[];for(let c of cs){let z=c.map(find),same=false,drop=false;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(z[i][0]===z[j][0]){if(z[i][1]!==z[j][1])drop=true;else same=[i,j]}if(drop)continue;if(same){let i=same[0],k=3-same[0]-same[1],r=join(c[i],c[k],1);if(r<0)return {answer:false,mods:mods.length,reason:"phase-parity"};update+=r}else residual.push(c)}changes+=update;if(!update)break}
let groups=new Map;for(let c of residual)for(let v of c){let [r]=find(v);groups.set(r,(groups.get(r)||0)+1)}
if([...groups.values()].some(x=>x>1))return {answer:null,mods:mods.length,residual:residual.length,changes};
for(let c of residual){let z=c.map(find);x[z[0][0]]=z[0][1];x[z[1][0]]=z[1][1];x[z[2][0]]=1^z[2][1]}
let w=Array.from({length:n},(_,i)=>{let [r,d]=find(i);return (x[r]<0?0:x[r])^d});ok(valid(F,w));return {answer:true,mods:mods.length,residual:residual.length,changes}}
let moduleWords=0;for(let i=0;i<512;i++){let x=Array.from({length:9},(_,j)=>(i>>j)&1);let actual=local.every(c=>nae(c.map(v=>x[v])));let expected=x[0]===x[1]&&x[1]===x[2]&&x[3]===x[4]&&x[4]===x[5]&&x[0]!==x[3]&&nae(x.slice(6));ok(actual===expected);moduleWords+=actual}
let controls=[],randSAT=0,randNO=0;
for(let k of [4,5,6,7,16,32,64,128,256,512]){let pi=Array.from({length:k},(_,i)=>(i+1)%k),sg=[...pi];for(let variant of [0,1]){if(variant){if(k<6||k%2)continue;[sg[0],sg[3]]=[sg[3],sg[0]]}
let F=ring(pi,sg);auth(F,9*k);let expected=parityGraph(pi,sg)!==null;let r=localClosure(shuffle(F,9*k),9*k);ok(r.answer===expected);controls.push({k,variant,n:9*k,expected,...r})}}
for(let job=0;job<150;job++){let k=6+2*rnd(16),pi=Array.from({length:k},(_,i)=>(i+1)%k),sg=perm(k);if(job%2===0){let a=perm(k/2),b=perm(k/2);sg=Array.from({length:k},(_,i)=>i%2?2*b[i>>1]:2*a[i>>1]+1)}
let F=ring(pi,sg);auth(F,9*k);let expected=parityGraph(pi,sg)!==null;let r=localClosure(shuffle(F,9*k),9*k);ok(r.answer===expected);if(expected)randSAT++;else randNO++}
let compiler=[];
for(let [name,F,n,w] of [["plane",P,9,null],...([7,11,31,101].map(p=>["cyclic"+p,cyclic(p),3*p,Array.from({length:3*p},(_,i)=>i>=p&&i<2*p?1:0)]))]){
auth(F,n);let G=compile(F,n);auth(G,27*n);if(w)ok(valid(F,w)&&valid(G,lift(w,3)));let res=localClosure(shuffle(G,27*n),27*n);if(!w)ok(res.answer!==true);compiler.push({name,source:n,compiled:27*n,owners:36*n,referenceSAT:!!w,...res});
if(n===9){let base=oracle(F,n);ok(base.length===0);for(let i=0;i<512;i++){let a=Array.from({length:n},(_,j)=>(i>>j)&1);ok(valid(F,a)===valid(G,lift(a,3)))}}}
console.log(JSON.stringify({seed:20261125,checks,moduleWords,controls,random:{sat:randSAT,unsat:randNO},compiler}));