// run with Node: require this module; pass pinned compile function, corpus and registry separately.
module.exports={sha:function sha(s){const P=[];for(let n=2;P.length<64;n++)if(P.every(p=>n%p))P.push(n);const k=P.map(p=>(Math.cbrt(p)%1*4294967296)|0);let h=P.slice(0,8).map(p=>(Math.sqrt(p)%1*4294967296)|0);const rr=(x,n)=>(x>>>n)|(x<<(32-n));const l=s.length,sz=Math.ceil((l+9)/64)*64,b=new Uint8Array(sz);for(let i=0;i<l;i++){if(s.charCodeAt(i)>127)throw Error("nonascii");b[i]=s.charCodeAt(i)}b[l]=128;for(let i=0;i<8;i++)b[sz-1-i]=Math.floor(l*8/256**i)%256;let w=new Int32Array(64);for(let off=0;off<sz;off+=64){for(let i=0;i<16;i++){let j=off+4*i;w[i]=(b[j]<<24)|(b[j+1]<<16)|(b[j+2]<<8)|b[j+3]}for(let i=16;i<64;i++){let x=w[i-15],y=w[i-2];w[i]=(w[i-16]+(rr(x,7)^rr(x,18)^(x>>>3))+w[i-7]+(rr(y,17)^rr(y,19)^(y>>>10)))|0}let[a,c,d,e,f,g,j,m]=h;for(let i=0;i<64;i++){let t1=(m+(rr(f,6)^rr(f,11)^rr(f,25))+((f&g)^(~f&j))+k[i]+w[i])|0,t2=((rr(a,2)^rr(a,13)^rr(a,22))+((a&c)^(a&d)^(c&d)))|0;m=j;j=g;g=f;f=(e+t1)|0;e=d;d=c;c=a;a=(t1+t2)|0}h=h.map((x,i)=>(x+[a,c,d,e,f,g,j,m][i])|0)}return h.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("")},study:function study(G,cap=10000000){
const t=Date.now(),counts={find:0,word:0,xor:0,pivot:0,join:0,scan:0};let maxBits=0;
const work=()=>Object.values(counts).reduce((a,b)=>a+b,0);
function check(){if(work()>cap)throw Error("CAP")}
function UF(n){let p=Array.from({length:n},(_,i)=>i),r=new Uint8Array(n),s=new Uint8Array(n);function f(x){counts.find++;if(p[x]===x)return[x,0];let [a,b]=f(p[x]);s[x]^=b;p[x]=a;return[a,s[x]]}function u(x,y,z){let[a,b]=f(x),[c,d]=f(y);if(a===c)return (b^d)===z;if(r[a]<r[c]){[a,c]=[c,a];[b,d]=[d,b]}p[c]=a;s[c]=b^d^z;if(r[a]===r[c])r[a]++;return true}return {f,u}}
function pivot(x){counts.pivot++;let n=x.toString(2).length;maxBits=Math.max(maxBits,n);check();return n-1}
function basis(xs){let B=new Map;for(let x of xs){while(x){let i=pivot(x);if(!B.has(i)){B.set(i,x);break}x^=B.get(i);counts.xor++}}return B}
function reduce(x,B){let z=0n;while(x){let i=pivot(x),y=B.get(i);if(y===undefined){let b=1n<<BigInt(i);z|=b;x^=b}else x^=y;counts.xor++}return z}
const bV=G.types.flatMap((x,i)=>x==="B"?[i]:[]),m=bV.length,uf=UF(4*G.types.length);
let before=4*G.types.length;
for(let [p,q,s] of G.edges)if(!uf.u(p,q,s))return {status:"NO-equality",counts,ms:Date.now()-t};
for(let i=0;i<G.types.length;i++)if(G.types[i]==="E")for(let j=1;j<4;j++)if(!uf.u(4*i,4*i+j,0))return {status:"NO-equality",counts,ms:Date.now()-t};
const occ=[],by=new Map,phase=[],root=[],valid=[];
for(let i=0;i<m;i++){let v=bV[i];for(let j=0;j<4;j++){let [r,s]=uf.f(4*v+j),p=4*i+j;root[p]=r;phase[p]=s;if(!by.has(r))by.set(r,[]);by.get(r).push(p)}let words=[];for(let w=0;w<16;w++){counts.word++;if(w.toString(2).replaceAll("0","").length!==2)continue;let a=new Map,ok=true;for(let j=0;j<4;j++){let p=4*i+j,x=((w>>j)&1)^phase[p];if(a.has(root[p])&&a.get(root[p])!==x)ok=false;a.set(root[p],x)}if(ok)words.push(w)}if(!words.length)return {status:"NO-occupancy",owner:v,counts,ms:Date.now()-t};valid.push(words)}
const carr=[...by.keys()],ci=new Map(carr.map((r,i)=>[r,i])),rr=carr.length,constant=1n<<BigInt(rr);
let equations=[];for(let i=0;i<m;i++){let x=0n,p=0;for(let j=0;j<4;j++){x^=1n<<BigInt(ci.get(root[4*i+j]));p^=phase[4*i+j]}equations.push(x^(p?constant:0n))}
 // pivot order keeps RHS out of variable columns
let ge=new Map;for(let x of equations){while(x&(constant-1n)){let j=pivot(x&(constant-1n));if(!ge.has(j)){ge.set(j,x);break}x^=ge.get(j);counts.xor++}if(x===constant)return {status:"NO-parity",counts,ms:Date.now()-t}}
 // Star edges between owner occurrences; quotient by all owner flips using forest-cycle map.
const star=[];for(let a of by.values())for(let j=1;j<a.length;j++)star.push([a[0],a[j]]);
const forest=UF(m),adj=Array.from({length:m},()=>[]),vec=Array(star.length).fill(0n),delta=Array(m).fill(0n);let q=0;
for(let e=0;e<star.length;e++){let [a,b]=star[e].map(x=>x>>2);if(forest.f(a)[0]!==forest.f(b)[0]){forest.u(a,b,0);adj[a].push([b,e]);adj[b].push([a,e])}else{let x=1n<<BigInt(q++);vec[e]=x;delta[a]^=x;delta[b]^=x;counts.xor+=2}}
let par=Array(m).fill(-2),pe=Array(m).fill(-1),order=[];
for(let v=0;v<m;v++)if(par[v]===-2){par[v]=-1;let st=[v];while(st.length){let a=st.pop();order.push(a);for(let [b,e]of adj[a])if(par[b]===-2){par[b]=a;pe[b]=e;st.push(b)}}}
for(let v of order.reverse())if(par[v]>=0){vec[pe[v]]=delta[v];delta[par[v]]^=delta[v];counts.xor++}else if(delta[v])throw Error("forest cycle");
let ov=Array(4*m).fill(0n);for(let i=0;i<star.length;i++){let[a,b]=star[i];ov[a]^=vec[i];ov[b]^=vec[i];counts.xor+=2}
let groups=[];for(let i=0;i<m;i++){let flip=0n;for(let j=0;j<4;j++)flip^=ov[4*i+j];if(flip)throw Error("complement");let set=new Map;for(let w of valid[i]){let x=0n;for(let j=0;j<4;j++)if(((w>>j)&1)^phase[4*i+j]){x^=ov[4*i+j];counts.xor++}if(!set.has(x))set.set(x,w)}groups.push({id:i,vals:[...set.keys()]})}
function direction(g){let a=g.vals[0];return g.vals.slice(1).map(v=>v^a)}
function cutStats(gs){let a=[],b=[];for(let g of gs)(g.id<m/2?a:b).push(...direction(g));let x=basis(a).size,y=basis(b).size,z=basis([...a,...b]).size;return {left:x,right:y,total:z,cut:x+y-z}}
let initial=cutStats(groups),rounds=[],offset=0n,removed=0;
while(groups.length){check();let classes=new Map,aff=[],rest=[];for(let g of groups){counts.scan++;let d=direction(g),B=basis(d),rank=B.size;if(g.vals.length===2**rank){aff.push({owners:[g.id],vals:g.vals,d});continue}if(g.vals.length!==3||rank!==2)throw Error("not triangle");let key=d.concat(d[0]^d[1]).map(v=>v.toString(16)).sort().join(",");if(!classes.has(key))classes.set(key,[]);classes.get(key).push(g)}
for(let list of classes.values()){if(list.length===1){rest.push(list[0]);continue}let [a,b,...other]=list,vals=[...new Set(a.vals.flatMap(x=>b.vals.map(y=>{counts.join++;return x^y})))];let d=vals.slice(1).map(x=>x^vals[0]);if(vals.length!==4||basis(d).size!==2)throw Error("pair cube replay");let o=other.reduce((z,g)=>z^g.vals[0],0n);aff.push({owners:list.map(g=>g.id),vals:vals.map(x=>x^o),d})}
if(!aff.length)break;
let B=basis(aff.flatMap(g=>g.d));for(let g of aff)offset^=g.vals[0];offset=reduce(offset,B);let next=rest.map(g=>({id:g.id,vals:[...new Set(g.vals.map(x=>reduce(x,B)))]}));removed+=aff.reduce((n,g)=>n+g.owners.length,0);rounds.push({groups:aff.length,owners:aff.reduce((n,g)=>n+g.owners.length,0),multiOwner:aff.filter(g=>g.owners.length>1).length,rank:B.size,remaining:next.length,cut:cutStats(next),sample:aff.slice(0,3).map(g=>({owners:g.owners.map(i=>bV[i]),vals:g.vals.map(x=>x.toString(16))}))});groups=next}
let D=basis(groups.flatMap(direction)),shift=groups.reduce((z,g)=>z^g.vals[0],offset),status=reduce(shift,D)?"NO-affine-relaxation":groups.length?"UNKNOWN":"YES-support-only";
return {status,ports:before,owners:m,carriers:rr,parityRank:ge.size,star:star.length,cycle:q,initial,rounds,removed,remaining:groups.length,final:cutStats(groups),counts,work:work(),maxBits,ms:Date.now()-t}
}};
