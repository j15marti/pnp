module.exports=function chart(G,cap=10000000,hybrid=false){
const t=Date.now(),C={edge:0,visit:0,rank:0,xor:0,local:0,mask:0,dep:0,graph:0};let maxBits=0;function tick(k,n=1){C[k]+=n;if(C[k]>cap)throw Error("CAP")}
function hi(x){tick("rank");let n=x.toString(2).length;maxBits=Math.max(maxBits,n);return n-1}
const n=4*G.types.length,adj=Array.from({length:n},()=>[]);function edge(a,b,s){adj[a].push([b,s]);adj[b].push([a,s]);tick("edge")}for(let [a,b,s]of G.edges)edge(a,b,s);for(let i=0;i<G.types.length;i++)if(G.types[i]==="E")for(let j=1;j<4;j++)edge(4*i,4*i+j,0);
let root=Array(n).fill(-1),phase=new Uint8Array(n);for(let i=0;i<n;i++)if(root[i]<0){root[i]=i;let st=[i];while(st.length){let a=st.pop();for(let[b,s]of adj[a]){tick("visit");let q=phase[a]^s;if(root[b]<0){root[b]=i;phase[b]=q;st.push(b)}else if(phase[b]!==q)return {status:"NO-equality",C}}}}
let owners=G.types.flatMap((x,i)=>x==="B"?[i]:[]),carriers=[...new Set(owners.flatMap(v=>root.slice(4*v,4*v+4)))],ix=new Map(carriers.map((r,i)=>[r,i])),r=carriers.length,K=1n<<BigInt(r),V=K-1n;
const port=p=>(1n<<BigInt(ix.get(root[p])))^(phase[p]?K:0n),P=new Map;
function normal(x){let a=x&V,z=x&K;while(a){let j=hi(a),q=P.get(j);if(q===undefined){let b=1n<<BigInt(j);z^=b;a^=b}else{z^=q&K;a^=q&V;tick("xor")}}return z}
function add(x){let y=normal(x),a=y&V;if(!a)return !(y&K);P.set(hi(a),y);return true}
for(let v of owners){let x=0n;for(let j=0;j<4;j++)x^=port(4*v+j);if(!add(x))return{status:"NO-parity",C}}
const baseRank=P.size,history=[],raw=owners.map(v=>({id:v,a:port(4*v)^port(4*v+1),b:port(4*v)^port(4*v+2)}));
let groups=[],round=0,taut=0;
function eq(a,b){return a^(b?K:0n)}
function parity(x){let b=0;while(x){x&=x-1n;b^=1}return b}
function truth(f,u,v,a,b){let x=f&V,c=Number(Boolean(f&K));if(x===0n)return c;if(x===a)return u^c;if(x===b)return v^c;if(x===(a^b))return u^v^c;throw Error("form")}
while(true){round++;let map=new Map,forced=[],ta=0;
for(let h of raw){tick("local");let f=normal(h.a),g=normal(h.b),a=f&V,b=g&V;if(!a||!b||a===b){let z=a||b,ok=[];for(let u=0;u<(z?2:1);u++){let x=Number(Boolean(f&K))^(a?u:0),y=Number(Boolean(g&K))^(b?u:0);if(x||y)ok.push(u)}if(!ok.length)return {status:"NO-local",owner:h.id,baseRank,history,C};if(z&&ok.length===1)forced.push({row:eq(z,ok[0]),owners:[h.id]});else ta++;continue}
let l=[a,b,a^b].sort((x,y)=>x<y?-1:x>y?1:0);let key=l.map(x=>x.toString(16)).join(",");if(!map.has(key))map.set(key,{a:l[0],b:l[1],lines:l,mask:15,ids:[]});let q=map.get(key);q.ids.push(h.id);for(let w=0;w<4;w++){tick("mask");if(!truth(f,w&1,w>>1,q.a,q.b)&&!truth(g,w&1,w>>1,q.a,q.b))q.mask&=~(1<<w)}}
groups=[];for(let q of map.values()){let ok=[0,1,2,3].filter(w=>q.mask>>w&1);if(!ok.length)return{status:"NO-plane-cover",owners:q.ids,baseRank,history,C};if(ok.length===3){groups.push(q);continue}if(ok.length===4){ta+=q.ids.length;continue}for(let f of q.lines){let vals=ok.map(w=>truth(f,w&1,w>>1,q.a,q.b));if(vals.every(x=>x===vals[0]))forced.push({row:eq(f,vals[0]),owners:q.ids})}}

// Each triangle excludes one point. Its three pairs of line coordinates
// express the identical forbidden point. Implication graph is a sound
// relaxation; every SCC equality and literal-to-complement path is exact.
if(hybrid){
let vs=[...new Set(groups.flatMap(q=>q.lines))],idx=new Map(vs.map((f,i)=>[f,i])),L=2*vs.length,A=Array.from({length:L},()=>[]),R=Array.from({length:L},()=>[]);
function arc(a,b){A[a].push(b);R[b].push(a);tick("graph")}
for(let q of groups){let w=[0,1,2,3].find(w=>!(q.mask>>w&1));let a=q.lines.map(f=>2*idx.get(f)+truth(f,w&1,w>>1,q.a,q.b));for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){arc(a[i],a[j]^1);arc(a[j],a[i]^1)}}
let seen=new Uint8Array(L),order=[];function dfs(a){seen[a]=1;for(let b of A[a]){tick("graph");if(!seen[b])dfs(b)}order.push(a)}for(let a=0;a<L;a++)if(!seen[a])dfs(a);let comp=Array(L).fill(-1),parts=[];function back(a,i){comp[a]=i;parts[i].push(a);for(let b of R[a]){tick("graph");if(comp[b]<0)back(b,i)}}for(let a of order.reverse())if(comp[a]<0){parts.push([]);back(a,parts.length-1)}
for(let i=0;i<vs.length;i++)if(comp[2*i]===comp[2*i+1])return{status:"NO-implication-SCC",baseRank,history,C};
for(let part of parts)for(let a of part.slice(1)){let b=part[0];forced.push({row:eq(vs[a>>1]^vs[b>>1],(a^b)&1),owners:[]})}
for(let a=0;a<L;a++){let visited=new Uint8Array(L),st=[a];visited[a]=1;while(st.length&&!visited[a^1]){let x=st.pop();for(let y of A[x]){tick("graph");if(!visited[y]){visited[y]=1;st.push(y)}}}if(visited[a^1])forced.push({row:eq(vs[a>>1],(a&1)^1),owners:[]})}
}

let before=P.size;for(let f of forced)if(!add(f.row))return {status:"NO-forced",baseRank,history,C};history.push({round,groups:map.size,triangles:groups.length,tautOwners:ta,forcedCandidates:forced.length,newRank:P.size-before});taut=ta;
if(P.size===before)break}
function getBasis(xs){let B=new Map;for(let x of xs)while(x){let p=hi(x);if(!B.has(p)){B.set(p,x);break}x^=B.get(p);tick("xor")}return B}
function stats(gs){let a=[],b=[];for(let q of gs)(Math.min(...q.ids)<owners[Math.floor(owners.length/2)]?a:b).push(q.a,q.b);let x=getBasis(a).size,y=getBasis(b).size,z=getBasis([...a,...b]).size;return {rank:z,cut:x+y-z}}
let initial=stats(groups),peel=[],peeled=[];
while(groups.length){
 // Track all linear dependencies between the two basis lines of each factor.
 let B=new Map,seen=Array(groups.length).fill(0),index=0;
 for(let q of groups)for(let x of [q.a,q.b]){let tag=1n<<BigInt(index++);while(x){let p=hi(x),z=B.get(p);if(!z){B.set(p,[x,tag]);break}x^=z[0];tag^=z[1];tick("xor",2)}if(!x){for(let j=0;j<groups.length;j++){tick("dep");let a=Number((tag>>BigInt(2*j))&3n);if(a)seen[j]|=1<<a}}}
 let remove=groups.filter((_,j)=>[0,2,4,8].includes(seen[j]));if(!remove.length)break;peel.push({removed:remove.length,owners:remove.reduce((n,q)=>n+q.ids.length,0)});peeled.push(...remove);groups=groups.filter((_,j)=>![0,2,4,8].includes(seen[j]));
}
let freq=new Map;for(let q of groups)for(let f of q.lines)freq.set(f,(freq.get(f)||0)+1);
let chosen=new Set,three=0;for(let q of groups){let a=q.lines.filter(f=>freq.get(f)>1);if(a.length===3)three++;for(let f of q.lines)if(a.length<2&&!a.includes(f))a.push(f);q.chosen=a;for(let f of a)chosen.add(f)}
let rank=getBasis([...chosen]).size,defect=chosen.size-rank,admitted=three===0&&defect===0,core=stats(groups),status="UNKNOWN",witness=null;
if(admitted){
 let vars=[...chosen],idx=new Map(vars.map((f,i)=>[f,i])),L=2*vars.length,g=Array.from({length:L},()=>[]),rev=Array.from({length:L},()=>[]);function arc(a,b){g[a].push(b);rev[b].push(a);tick("graph")}
 for(let q of groups){let w=[0,1,2,3].find(w=>!(q.mask>>w&1));let [a,b]=q.chosen.map(f=>2*idx.get(f)+truth(f,w&1,w>>1,q.a,q.b));arc(a,b^1);arc(b,a^1)}
 let visit=new Uint8Array(L),order=[];function dfs(a){visit[a]=1;for(let b of g[a])if(!visit[b])dfs(b);order.push(a)}for(let a=0;a<L;a++)if(!visit[a])dfs(a);let comp=Array(L).fill(-1),i=0;function back(a){comp[a]=i;for(let b of rev[a])if(comp[b]<0)back(b)}for(let a of order.reverse())if(comp[a]<0){back(a);i++}
 if(vars.some((_,i)=>comp[2*i]===comp[2*i+1]))status="NO-2SAT";else{
 for(let i=0;i<vars.length;i++)if(!add(eq(vars[i],Number(comp[2*i+1]>comp[2*i]))))throw Error("chart assignment");
 for(let q of peeled.reverse()){let ok=false;for(let w=0;w<4;w++)if(q.mask>>w&1){let old=new Map(P);if(add(eq(q.a,w&1))&&add(eq(q.b,w>>1))){ok=true;break}P.clear();for(let [a,b]of old)P.set(a,b)}if(!ok)throw Error("peel lift")}
 let x=0n;for(let [j,f]of [...P].sort((a,b)=>a[0]-b[0])){let b=parity((f&V)&x)^Number(Boolean(f&K));if(b)x|=1n<<BigInt(j)}
 let bits=root.map((a,p)=>phase[p]^(ix.has(a)?Number((x>>BigInt(ix.get(a)))&1n):0));if(!G.edges.every(([a,b,s])=>(bits[a]^bits[b])===s)||!G.types.every((t,v)=>{let a=bits.slice(4*v,4*v+4);return t==="E"?a.every(x=>x===a[0]):a.reduce((x,y)=>x+y,0)===2}))throw Error("native lift");status="YES-verified";if(n<=20)witness=bits;
 }}
return {status,owners:owners.length,carriers:r,baseRank,closureRank:history.reduce((s,h)=>s+h.newRank,baseRank),history,initial,peel,remaining:groups.length,core,chosen:chosen.size,rank,defect,three,admitted,witness,C,maxBits,ms:Date.now()-t}
};
