
function deletionComponents(sha){
const enc=x=>JSON.stringify(x)+"\n",A=(b,m)=>{if(!b)throw Error(m)};
function match(H,q,D=new Set()){let M=Array(q).fill(-1);function aug(i,S){for(let v of H[i])if(!D.has(v)&&!S.has(v)){S.add(v);if(M[v]<0||aug(M[v],S)){M[v]=i;return true}}return false}for(let i=0;i<H.length;i++)if(!aug(i,new Set()))return null;return M}
function brute(H,D,i=0,S=new Set()){if(i===H.length)return true;for(let v of H[i])if(!D.has(v)&&!S.has(v)){S.add(v);let ok=brute(H,D,i+1,S);S.delete(v);if(ok)return true}return false}
function split(H,q){let M=match(H,q);if(!M)return null;let U=M.flatMap((x,i)=>x<0?[i]:[]),T=Array.from({length:q},()=>[]),R=Array.from({length:q},()=>[]),events=0;for(let v=0;v<q;v++)if(M[v]>=0)for(let w of H[M[v]])R[w].push(v);
for(let u of U){let S=new Set([u]),Q=[u];for(let v of Q)for(let w of R[v]){events++;if(!S.has(w)){S.add(w);Q.push(w)}}for(let v of S)T[v].push(u)}
let p=Array.from({length:q},(_,i)=>i);function r(i){while(p[i]!==i)i=p[i];return i}for(let t of T)for(let j=1;j<t.length;j++)p[r(t[j])]=r(t[0]);
let G=new Map(),L=[];for(let v=0;v<q;v++){if(!T[v].length){L.push(v);continue}let k=r(T[v][0]);if(!G.has(k))G.set(k,{V:[],U:[],ids:[],H:[]});let g=G.get(k);g.V.push(v);if(M[v]<0)g.U.push(v);else{g.ids.push(M[v]);g.H.push(H[M[v]].filter(w=>T[w].length&&r(T[w][0])===k))}}
for(let g of G.values())A(g.V.length-g.H.length===g.U.length&&match(g.H,q)!==null,"component");return {M,T,L,G:[...G.values()],events}}
let seed=845071,rng=()=>((seed=(Math.imul(seed,1664525)+1013904223)>>>0)/4294967296),stats={graphs:0,baseNO:0,partition:0,multiFree:0,multiComponent:0,words:0,lifts:0,events:0},records=new Map();
for(let it=0;it<456;it++){let d=it<256?2:3,q=it<256?4:6,H=Array.from({length:d},(_,i)=>Array.from({length:q},(_,j)=>j).filter(j=>it<256?((it>>(i*q+j))&1):rng()<.45)),source={format:"MATCHING-DELETION-v2",q,A:H},id=source.format+":sha256:"+sha(enc(source)),X=split(H,q),rec={instance_id:id,N:enc(source).length*8,source,guard:"EMPTY",residual:"ROOT",parents:[],original_ids:{demands:[0,d-1],resources:[0,q-1]}};stats.graphs++;
if(!X){A(!brute(H,new Set()),"base");stats.baseNO++;records.set(id,{...rec,baseFeasible:false});continue}
stats.partition++;stats.events+=X.events;if(X.G.some(g=>g.U.length>1))stats.multiFree++;if(X.G.length>1)stats.multiComponent++;
for(let s=0;s<2**q;s++){let D=new Set(Array.from({length:q},(_,i)=>i).filter(i=>s>>i&1)),yes=!X.L.some(v=>D.has(v)),pairs=[];for(let g of X.G){let M=match(g.H,q,D);if(!M){yes=false;continue}M.forEach((i,v)=>{if(i>=0)pairs.push([g.ids[i],v])})}A(yes===brute(H,D),"oracle");stats.words++;if(yes){for(let v of X.L)if(X.M[v]>=0)pairs.push([X.M[v],v]);A(pairs.length===d&&new Set(pairs.map(x=>x[0])).size===d&&new Set(pairs.map(x=>x[1])).size===d&&pairs.every(([i,v])=>H[i].includes(v)&&!D.has(v)),"lift");stats.lifts++}}
records.set(id,{...rec,baseFeasible:true,partition:X.G.map(g=>({bins:g.V,free:g.U})),indispensable:X.L,matching:X.M,reachability:X.T})}
return {stats,distinct:records.size,records:[...records.values()]}}
