// N4FN09: source-only rank-one wide seams and exact joint residual audit.
// node audit.js
function audit(){
let checks=0,seed=20261126;
const ok=(x)=>{checks++;if(!x)throw Error("assertion "+checks)};
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
function perm(n){let a=Array.from({length:n},(_,i)=>i);for(let i=n-1;i>0;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
const P=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]];
const nae=a=>a.some(x=>x!==a[0]);
const valid=(F,x)=>F.every(p=>p.every(c=>nae(c.map(v=>x[v]))));
function auth(F,n){ok(F.length===4);const pairs=new Set;for(const p of F){let f=new Uint8Array(n);for(const c of p){ok(c.length===3&&new Set(c).size===3);for(const v of c){ok(Number.isInteger(v)&&v>=0&&v<n);f[v]++}for(let i=0;i<3;i++)for(let j=0;j<i;j++){let a=Math.min(c[i],c[j]),b=Math.max(c[i],c[j]),s=a*n+b;ok(!pairs.has(s));pairs.add(s)}}ok(f.every(x=>x===1))}}
function base(k,yes){let F=[[],[],[],[]],x=[];for(let b=0;b<2*k;b++){let o=9*b;for(let i=0;i<9;i++)x.push((i<3?0:i<6?1:i===8?1:0)^(b%2));for(let j=0;j<4;j++)for(const c of P[j])F[j].push(c.map(v=>v+o))}
function sw(j,a,b){let u=F[j][a],v=F[j][b];[u[0],v[0]]=[v[0],u[0]]}
for(let i=0;i<k;i++){sw(0,6*i,6*i+3);if(yes||i>0)sw(0,6*i+1,6*i+4)}
for(let i=0;i<k-1;i++)sw(1,6*i+3,6*(i+1)+4);
auth(F,x.length);if(yes)ok(valid(F,x));else{let C=F.flat().filter(c=>c.every(v=>v<9));ok(C.length===11);for(let w=0;w<512;w++)ok(!C.every(c=>nae(c.map(v=>(w>>v)&1))))}
return {F,x,n:x.length,yes}}
function inflate(F,n,t){let G=[[],[],[],[]],pool=[],L=4*t;
for(let i=0;i<n;i++){let a=[[],[]];for(let j=0;j<L;j++){let o=9*(i*L+j),next=9*(i*L+(j+1)%L);for(let k=0;k<4;k++)for(const c of (k?P[k]:P[0].slice(2)))G[k].push(c.map(v=>v+o));G[0].push([o,o+1,next+2]);for(let v=3;v<6;v++)a[1^(j%2)].push(o+v)}pool.push(a)}
for(let j=0;j<4;j++)for(let r=0;r<3*t;r++){let s=r<(j<2?2*t:t)?0:1;for(const c of F[j])G[0].push(c.map(i=>pool[i][s].pop()))}
ok(pool.every(a=>a.every(b=>b.length===0)));return G}
function shuffle(F,n){let p=perm(n);return perm(4).map(j=>perm(F[j].length).map(i=>perm(3).map(k=>p[F[j][i][k]])))}
function ref(F,n){if(n>18)return null;for(let w=0;w<2**n;w++)if(F.every(p=>p.every(c=>{let a=(w>>c[0])&1;return ((w>>c[1])&1)!==a||((w>>c[2])&1)!==a})))return true;return false}
function exactQ(C,n,cap=24){
 if(n>cap)return {answer:null,word:null,probes:0,nodes:0};
 let probes=0,nodes=0;
 function prop(x){let change=true;while(change){change=false;for(let c of C){let v=c.map(([i,s])=>x[i]<0?-1:x[i]^s);if(v.includes(0)&&v.includes(1))continue;let U=v.map((b,i)=>b<0?i:-1).filter(i=>i>=0);if(!U.length)return false;if(U.length===1){let j=U[0],[i,s]=c[j],b=v.find(y=>y>=0)^1^s;if(x[i]!==b){if(x[i]>=0)return false;x[i]=b;change=true}}}}return true}
 let x=Array(n).fill(-1); // unguarded complement symmetry, no absolute guard imported
 if(n)x[0]=0;
 if(!prop(x))return {answer:false,word:null,probes,nodes};
 let changed=true;while(changed){changed=false;for(let i=0;i<n;i++)if(x[i]<0){let a=x.slice(),b=x.slice();a[i]=0;b[i]=1;probes+=2;let u=prop(a),v=prop(b);if(!u&&!v)return {answer:false,word:null,probes,nodes};for(let j=0;j<n;j++){let z=!u?b[j]:!v?a[j]:a[j]===b[j]?a[j]:-1;if(x[j]<0&&z>=0){x[j]=z;changed=true}}if(changed&&!prop(x))return {answer:false,word:null,probes,nodes}}}
 function dfs(y){nodes++;if(!prop(y))return null;let i=y.indexOf(-1);if(i<0)return y;for(let b=0;b<2;b++){let z=y.slice();z[i]=b;let w=dfs(z);if(w)return w}return null}
 let word=dfs(x);return {answer:word!==null,word,probes,nodes}}
function solve(F,n,cap=24){const C=F.flat(),I=Array.from({length:n},()=>[]);C.forEach((c,i)=>c.forEach(v=>I[v].push(i)));
let parent=Array.from({length:n},(_,i)=>i),p=new Uint8Array(n),rank=new Uint8Array(n);
function find(v){if(parent[v]===v)return [v,0];let [r,s]=find(parent[v]);p[v]^=s;parent[v]=r;return [r,p[v]]}
function join(v,w,s){let [a,b]=find(v),[c,d]=find(w);if(a===c)return (b^d)===s?0:-1;if(rank[a]<rank[c])[a,c]=[c,a];parent[c]=a;p[c]=b^d^s;if(rank[a]===rank[c])rank[a]++;return 1}
let mods=[],seen=new Set,covered=new Int32Array(n).fill(-1);
for(let v=0;v<n;v++){let S=[...new Set([v,...I[v].flatMap(i=>C[i])])].sort((a,b)=>a-b);if(S.length!==9)continue;let key=S.join(",");if(seen.has(key))continue;seen.add(key);let M=new Set(S),cs=[...new Set(S.flatMap(x=>I[x]))].filter(i=>C[i].every(x=>M.has(x)));if(cs.length>=11)return {answer:false,stage:"11-line"};if(cs.length!==10)continue;let ix=new Map(S.map((x,i)=>[x,i])),E=new Set;for(let i of cs)for(let a=0;a<3;a++)for(let b=0;b<a;b++){let u=ix.get(C[i][a]),v=ix.get(C[i][b]);E.add(Math.min(u,v)*9+Math.max(u,v))}
let A=Array.from({length:9},()=>[]);for(let i=0;i<9;i++)for(let j=i+1;j<9;j++)if(!E.has(i*9+j)){A[i].push(j);A[j].push(i)}
let a=A.findIndex(x=>x.length===2);if(a<0)continue;let L=[a,...A[a]],R=A.map((x,i)=>x.length===2&&!L.includes(i)?i:-1).filter(i=>i>=0);
let tri=L=>L.length===3&&L.every(i=>A[i].length===2&&L.every(j=>i===j||A[i].includes(j)));
if(!tri(L)||!tri(R)||A.some((x,i)=>x.length&&!L.includes(i)&&!R.includes(i)))continue;
if(S.some(x=>covered[x]>=0))return {answer:null,stage:"overlap"};
let q={S,L:L.map(i=>S[i]),R:R.map(i=>S[i]),U:S.filter((_,i)=>!L.includes(i)&&!R.includes(i))};
for(const x of S)covered[x]=mods.length;mods.push(q);
for(const [v,s] of [...q.L.map(v=>[v,0]),...q.R.map(v=>[v,1])])ok(join(q.L[0],v,s)>=0)}
if(covered.some(v=>v<0))return {answer:null,stage:"uncovered",mods:mods.length};
let joins=0;
for(;;){let changed=0;for(const c of C){let z=c.map(find),eq=null,opp=false;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(z[i][0]===z[j][0]){if(z[i][1]!==z[j][1])opp=true;else eq=[i,j]}if(opp)continue;if(eq){let [i,j]=eq,r=join(c[i],c[3-i-j],1);if(r<0)return {answer:false,stage:"parity",mods:mods.length};changed+=r}}joins+=changed;if(!changed)break}
let groups=new Map;for(let m of mods){let root=find(m.L[0])[0];if(!groups.has(root))groups.set(root,{mods:[],inside:[],ports:[],w0:new Map});groups.get(root).mods.push(m)}
let roots=[...groups.keys()],ri=new Map(roots.map((r,i)=>[r,i])),vg=new Int32Array(n).fill(-1);
for(let [r,g] of groups)for(let m of g.mods)for(let v of m.S)vg[v]=ri.get(r);
const ext=[];
for(let i=0;i<C.length;i++){let c=C[i],g=c.map(v=>vg[v]);if(g.every(x=>x===g[0]))groups.get(roots[g[0]]).inside.push(i);else{if(new Set(g).size!==3)return {answer:null,stage:"mixed-regions"};let q=[];for(let j=0;j<3;j++){let [r,s]=find(c[j]);if(r!==roots[g[j]])return {answer:null,stage:"nonphase-port"};groups.get(r).ports.push({eid:3*i+j,v:c[j],s});q.push([g[j],s])}ext.push(q)}}
let minPorts=Infinity,maxPorts=0;
for(let [r,g] of groups){for(let m of g.mods){for(let v of [...m.L,...m.R]){let [a,s]=find(v);ok(a===r);g.w0.set(v,s)}for(let j=0;j<3;j++)g.w0.set(m.U[j],j===2?1:0)}
// Exact joint profile: all boundary occurrences depend on ONE certified parity class.
// Both antipodal rows have actual local extensions; verify every local owner twice.
for(let b=0;b<2;b++)for(let i of g.inside)ok(nae(C[i].map(v=>g.w0.get(v)^b)));
for(let e of g.ports)ok(g.w0.get(e.v)===e.s);
minPorts=Math.min(minPorts,g.ports.length);maxPorts=Math.max(maxPorts,g.ports.length)}
// Canonicalize signed NAE triples by actual group IDs, then global complement.
let uq=new Map;for(let c of ext){c.sort((a,b)=>a[0]-b[0]);if(c[0][1])c=c.map(([i,s])=>[i,s^1]);uq.set(JSON.stringify(c),c)}
let q=[...uq.values()],res=exactQ(q,roots.length,cap);
if(res.word){let x=Array(n);for(let [r,g] of groups)for(let [v,s] of g.w0)x[v]=s^res.word[ri.get(r)];ok(x.every(v=>v===0||v===1));ok(valid(F,x))}
return {answer:res.answer,stage:"joint",mods:mods.length,groups:roots.length,joins,minPorts,maxPorts,external:ext.length,quotient:q.length,probes:res.probes,nodes:res.nodes}}
let cases=[];
for(let k of [1,2,4])for(let yes of [true,false]){let B=base(k,yes),r=ref(B.F,B.n);if(r!==null)ok(r===yes);for(let t of (k===1?[1,2,4,16,64]:[1,4])){let G=inflate(B.F,B.n,t),n=36*t*B.n;auth(G,n);let s=solve(shuffle(G,n),n);ok(s.stage==="joint");ok(s.groups===B.n&&s.quotient===4*B.n/3);ok(s.minPorts===12*t&&s.maxPorts===12*t);if(B.n<=24)ok(s.answer===yes);else ok(s.answer===null);cases.push({base:B.n,t,n,clauses:4*n/3,expected:yes,...s})}}
// Generic recurrence, including logarithmic rank on unbalanced shores.
let recurrence=0;for(let u=1;u<=64;u++)for(let v=u;v<=128;v++){let a=BigInt(u),b=BigInt(v);for(let r=1;r<=5;r++){let c=BigInt(r+1);ok((1n<<BigInt(r-1))*a**c+b**c<=(a+b)**c-1n);ok((1n<<BigInt(r))*a**c+b**c<=(a+b)**c-1n);recurrence+=2}
let m=u+v;if(u*u<=m&&m>=16){let r=Math.floor(Math.log2(m));ok((1n<<BigInt(r))*a**4n+b**4n<=(a+b)**4n-1n);recurrence++}}
return {checks,seed:20261126,cases,recurrence,limits:"source-only exact ring-profile acquisition; bounded 24-phase reference terminal; general rank-cut recursive backend and affine-profile discovery not executed; same ES13 generator adapted as source for new inflation"}
}
console.log(JSON.stringify(audit(),null,2));