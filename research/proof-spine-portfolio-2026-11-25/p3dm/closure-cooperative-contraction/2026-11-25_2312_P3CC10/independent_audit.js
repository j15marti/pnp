// Node.js: independent finite gadget and decorated prism incidence rotation/witness audit.
const run=()=>{
let checks=0;const ok=(x)=>{checks++;if(!x)throw Error("assertion "+checks)};
const pairs=[];for(let u=0;u<6;u++)for(let v=u+1;v<6;v++)pairs.push([u,v]);
const even=Array.from({length:16},(_,i)=>i).filter(i=>[0,1,2,3].reduce((a,j)=>a+(i>>j&1),0)%2===0);
function sig(edges,n){let adj=Array(n).fill(0);for(let [u,v] of edges){adj[u]|=1<<v;adj[v]|=1<<u}const memo=new Map([[0,true]]);function pm(x){if(memo.has(x))return memo.get(x);let i=31-Math.clz32(x&-x),found=false;for(let j=i+1;j<n;j++)if((x&adj[i])>>j&1&&pm(x^(1<<i)^(1<<j))){found=true;break}memo.set(x,found);return found}let s=0;for(let i=0;i<even.length;i++)if(pm(((1<<n)-1)^even[i]))s|=1<<i;return s}
function delta(mask){if(!mask)return false;let W=even.filter((x,i)=>mask>>i&1);for(let a of W)for(let b of W){let D=[0,1,2,3].filter(i=>(a^b)>>i&1);for(let i of D)if(!D.some(j=>j!==i&&W.includes(a^(1<<i)^(1<<j))))return false}return true}
let lib=new Map();for(let k=0;k<1<<15;k++){let e=pairs.filter((v,i)=>k>>i&1),s=sig(e,6);if(!lib.has(s))lib.set(s,e);}ok(lib.size===147);ok(!lib.has(1));ok(sig([[0,4],[1,5],[2,6],[3,7]],8)===1);lib.set(1,[[0,4],[1,5],[2,6],[3,7]]);for(let m=0;m<256;m++)ok(lib.has(m)===(m===0||delta(m)));
const B=[[0,0,0],[1,1,1],[0,0,1],[1,1,0],[0,1,0],[1,0,1]];
const R0=[[6,10,8],[7,9,11],[6,8,11],[9,7,10],[10,6,9],[8,7,11],[0,2,4],[5,3,1],[2,0,5],[1,3,4],[3,0,4],[1,2,5]];
function family(k){
let T=[],R=[];for(let i=0;i<5*k;i++){for(let t of B)T.push(t.map(x=>x+2*i));for(let r of R0)R.push((i<2*k&&i%2?r.slice().reverse():r).map(v=>v+12*i));}
let P=[],E=[];for(let v=0;v<2*k;v++){let i=v%k,o=v-i,nb=[o+(i+k-1)%k,o+(i+1)%k,(v+k)%(2*k)];let V=v<k?(i%2?[[5,1],[0,2],[3,2]]:[[3,2],[0,1],[5,1]]):(i%2?[[0,2],[5,1],[3,2]]:[[0,1],[3,2],[5,1]]);P.push(new Map(nb.map((u,i)=>[u,V[i]])));for(let u of nb)if(v<u)E.push([v,u]);}E.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);ok(E.length===3*k);
const swap=(u,i,v,j,c)=>{let a=6*u+i,b=6*v+j,rv=(w)=>12*Math.floor(w/2)+2*c+w%2;let x=12*u+6+i,y=12*v+6+j,A=rv(T[a][c]),D=rv(T[b][c]);let rep=(w,a,b)=>{let z=R[w].indexOf(a);ok(z>=0);R[w][z]=b};rep(x,A,D);rep(A,x,y);rep(y,D,A);rep(D,y,x);[T[a][c],T[b][c]]=[T[b][c],T[a][c]];};
let col=[[],[],[]];for(let e=0;e<E.length;e++){let [u,v]=E[e],[i,c]=P[u].get(v),[j,d]=P[v].get(u);ok(c===d);swap(u,i,v,j,c);col[c].push([u,v]);swap(u,i^1,2*k+e,0,1);col[1].push([u,2*k+e]);}
for(let c of [1,2]){let parent=Array.from({length:5*k},(_,i)=>i);let root=i=>{while(parent[i]!==i)i=parent[i];return i};for(let [u,v] of col[c]){ok(root(u)!==root(v));parent[root(u)]=root(v)}}
ok(new Set(T.map(t=>t.join(","))).size===T.length);
for(let u=0;u<R.length;u++){ok(new Set(R[u]).size===R[u].length);for(let v of R[u])ok(R[v].includes(u));}
for(let i=0;i<T.length;i++){let u=12*Math.floor(i/6)+6+i%6;ok(T[i].every((v,c)=>R[u].includes(12*Math.floor(v/2)+2*c+v%2)));}
let seen=new Set(),F=0;for(let u=0;u<R.length;u++)for(let v of R[u])if(!seen.has(u+","+v)){F++;let a=u,b=v;while(!seen.has(a+","+b)){seen.add(a+","+b);let c=R[b][(R[b].indexOf(a)+1)%R[b].length];a=b;b=c;}ok(a===u&&b===v);}ok(seen.size===180*k);ok(R.length-seen.size/2+F===2);let V=new Set([0]),Q=[0];while(Q.length)for(let u of R[Q.pop()])if(!V.has(u)){V.add(u);Q.push(u)}ok(V.size===R.length);
let edgeIndex=new Map(E.map((e,i)=>[e.join(","),i]));let idx=(u,v)=>edgeIndex.get([Math.min(u,v),Math.max(u,v)].join(","));
let rungs=Array.from({length:k},(_,i)=>idx(i,i+k)),horiz=(a,b)=>{let s=[];for(let [off,p] of [[0,a],[k,b]])for(let j=p;j<k;j+=2)s.push(idx(off+j,off+(j+1)%k));return s};
let M=[rungs,horiz(0,0),horiz(1,1),horiz(0,1),horiz(1,0)];for(let i=0;i<k;i++)M.push(rungs.filter(e=>e!==idx(i,i+k)&&e!==idx((i+1)%k,(i+1)%k+k)).concat(idx(i,(i+1)%k),idx(i+k,(i+1)%k+k)));
let words=[];function lift(W,flip=-1){let set=new Set(W),phase=Array(5*k).fill(-1);for(let e of W){let [u,v]=E[e];ok(phase[u]<0&&phase[v]<0);phase[u]=P[u].get(v)[0]>>1;phase[v]=P[v].get(u)[0]>>1;}for(let e=0;e<E.length;e++)phase[2*k+e]=set.has(e)?0:e===flip?2:1;ok(phase.every(x=>x>=0));let ids=phase.flatMap((p,i)=>[6*i+2*p,6*i+2*p+1]);ok(ids.length===10*k);for(let c=0;c<3;c++)ok(new Set(ids.map(j=>T[j][c])).size===10*k);return new Set(ids)}
for(let m of M)words.push(lift(m));for(let e=0;e<E.length;e++)words.push(lift(M.find(m=>!m.includes(e)),e));
let signs=new Set();for(let i=0;i<T.length;i++){let s=words.map(W=>+W.has(i)).join(""),c=words.map(W=>+!W.has(i)).join("");ok(s.includes("0")&&s.includes("1"));signs.add(s<c?s:c);}ok(signs.size===9*k);
return {k,triples:T.length,incidence_vertices:R.length,faces:F,semantic_signed_classes:signs.size,witnesses:words.length,raw_hubs:3*k,raw_cycle_rank:k+1,basis_hubs:3*k-3,basis_cycle_rank:k-1};
}
let fam=[4,8,16,32,64,128].map(family);return {checks,library_nonempty:147,library_including_empty:lib.size,fam};
};
console.log(JSON.stringify(run(),null,2));
