function audit(){
 let seed=28395517,checks=0;const rnd=n=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n};const ck=(b,s)=>{checks++;if(!b)throw Error(s)};
 const pivot=x=>x.toString(2).length-1;
 const parity=x=>{let b=0;while(x){x&=x-1n;b^=1}return b};
 const reduce=(x,B)=>{for(let k of [...B.keys()].sort((a,b)=>b-a))if((x>>BigInt(k))&1n)x^=B.get(k);return x};
 const basis=xs=>{let B=new Map;for(let x of xs){x=reduce(x,B);if(x)B.set(pivot(x),x)}return B};
 function solve(rows,n){let B=new Map;for(let [x,b] of rows){while(x){let j=pivot(x);if(B.has(j)){let [y,c]=B.get(j);x^=y;b^=c}else{B.set(j,[x,b]);break}}if(!x&&b)return null}let z=0n;for(let j of [...B.keys()].sort((a,b)=>a-b)){let [a,b]=B.get(j);if(parity(a&z)!==b)z^=1n<<BigInt(j)}return z}
 function kernel(rows,n){let B=basis(rows),out=[];for(let f=0;f<n;f++)if(!B.has(f)){let x=1n<<BigInt(f);for(let j of [...B.keys()].sort((a,b)=>a-b))if(parity(B.get(j)&x))x^=1n<<BigInt(j);out.push(x)}return out}
 // Unweighted linear/partition matroid intersection using shortest augmenting paths.
 function transversal(G,quota){let es=G.flatMap((a,i)=>a.map((v,j)=>({v,i,j}))),I=new Set;function indep(ids){return basis(ids.map(e=>es[e].v)).size===ids.length}function partition(ids){let n=Array(quota.length).fill(0);return ids.every(e=>++n[es[e].i]<=quota[es[e].i])}
 while(true){let inside=[...I],outside=es.map((_,i)=>i).filter(i=>!I.has(i)),pred=new Map,queue=[];for(let e of outside)if(indep([...inside,e])){pred.set(e,-1);queue.push(e)}let sink=-1;for(let q=0;q<queue.length&&sink<0;q++){let e=queue[q];if(!I.has(e)&&partition([...inside,e])){sink=e;break}let ns=I.has(e)?outside.filter(f=>indep([...inside.filter(x=>x!==e),f])):inside.filter(f=>partition([...inside.filter(x=>x!==f),e]));for(let f of ns)if(!pred.has(f)){pred.set(f,e);queue.push(f)}}if(sink<0)break;for(let e=sink;e!==-1;e=pred.get(e)){if(I.has(e))I.delete(e);else I.add(e)}ck(indep([...I])&&partition([...I]),"intersection invariant")}
 return [...I].map(e=>es[e])}
 function candidate(U,D){let normals=[],offsets=[],hyperplanes=[];for(let i=0;i<D;i++){let v=kernel(normals,D)[0];ck(v!==undefined,"independent normal discovery");let p=pivot(v),quot=U.map(a=>a.map(x=>x^(((x>>BigInt(p))&1n)?v:0n)));let quota=U.map(a=>a.length-1),sel=transversal(quot,quota);ck(sel.length===D-1,"quota transversal");let E=sel.map(e=>U[e.i][e.j]);let normal=kernel(E,D)[0];ck(normal!==undefined&&parity(normal&v)===1,"new normal");let a=0n;for(let j=0;j<U.length;j++){let used=new Set(sel.filter(e=>e.i===j).map(e=>e.j));a^=U[j][U[j].findIndex((_,k)=>!used.has(k))]}normals.push(normal);offsets.push(parity(normal&a));hyperplanes.push({normal,a,E});}
 let t=solve(normals.map((p,i)=>[p,1^offsets[i]]),D);ck(t!==null,"candidate");return {t,hyperplanes}}
 function exactTest(L){let m=L.length,n=m-1,rows=L.flat(),k=rows.length,D=k-n;let dep=kernel(Array.from({length:n},(_,i)=>rows.reduce((a,r,j)=>a^(((r>>BigInt(i))&1n)<<BigInt(j)),0n)),k);
 ck(dep.length===D,"dual dimension");let cols=rows.map((_,j)=>dep.reduce((a,h,i)=>a^(((h>>BigInt(j))&1n)<<BigInt(i)),0n));let off=0,U=L.map(a=>{let u=cols.slice(off,off+a.length);off+=a.length;ck(basis(u).size===a.length,"injectivity");return u});let {t,hyperplanes}=candidate(U,D);let support=new Set([0n]);for(let u of U){let opts=[];for(let s=1;s<(1<<u.length);s++)opts.push(u.reduce((x,h,i)=>s>>i&1?x^h:x,0n));support=new Set([...support].flatMap(x=>opts.map(y=>x^y)));}
 let missing=0;for(let x=0n;x<(1n<<BigInt(D));x++){if(!support.has(x)){ck(x===t,"only candidate");missing++}else if(x!==t)ck(hyperplanes.some(h=>parity(h.normal&(x^h.a))===0),"covered by hyperplane")}
 ck(missing<=1,"at most one");
 return {missing,D,t:Number(t),sizes:L.map(a=>a.length)}}
 let results={seed,strictGeometries:0,mixedGeometries:0,missing:0,covered:0,syndromeChecks:0,explicitMixed:null,starControls:[]};
 for(let z=0;z<800;z++){let m=3+rnd(4),n=m-1,L=[];for(let i=0;i<m;i++){let k=1+rnd(Math.min(n,3)),a=[];while(a.length<k){let x=BigInt(1+rnd((1<<n)-1));if(basis([...a,x]).size>a.length)a.push(x)}L.push(a)}
 let ok=basis(L.flat()).size===n;for(let s=1;s<(1<<m)-1&&ok;s++){let S=L.filter((_,i)=>s>>i&1);if(basis(S.flat()).size<S.length)ok=false}if(!ok)continue;
 let a=exactTest(L);results.strictGeometries++;results.mixedGeometries+=Number(a.sizes.some(k=>k!==2));results.missing+=a.missing;results.covered+=1-a.missing;results.syndromeChecks+=2**a.D;
 }
 // Reproduce exact strict mixed-rank UNSAT witness from independent search.
 let L=[[13,14,2],[10,7],[1,15],[10,7],[13,15]].map(a=>a.map(BigInt));for(let s=1;s<31;s++){let S=L.filter((_,i)=>s>>i&1);ck(basis(S.flat()).size>=S.length,"explicit strict")}
 let a=exactTest(L);ck(a.missing===1,"mixed-rank exception exists");results.explicitMixed={rows:L.map(a=>a.map(Number)),...a};
 // Targeted exposure and physical star controls. Blocks are specified by legal color lists.
 function starNetwork(n,owners){let deg=Array(n).fill(0),directions=Array(n).fill(0),rows=[];for(let o of owners){for(let i=0;i<4;i++){let v=o.ids[i],d=o.ls[i][0]^o.ls[i][1];ck(!directions[v]||directions[v]===d,"same hub direction");directions[v]=d;deg[v]++;}let ref=o.ls.reduce((_,x)=>_,0),B=[];for(let c of o.blocks)for(let j of c.slice(1))B.push((1n<<BigInt(o.ids[c[0]]))^(1n<<BigInt(o.ids[j])));for(let j of o.unary)B.push(1n<<BigInt(o.ids[j]));rows.push(B)}
 ck(deg.every(d=>d<=4),"physical degree");let min=Infinity;for(let C=1;C<(1<<n)-1;C++){let ex=0;for(let o of owners){for(let j of o.unary)ex+=C>>o.ids[j]&1;for(let c of o.blocks){let q=c.reduce((a,j)=>a+(C>>o.ids[j]&1),0);if(q<c.length)ex+=q}}min=Math.min(min,ex)}ck(min>=4,"exposure");
 for(let S=1;S<(1<<owners.length)-1;S++){let A=rows.filter((_,i)=>S>>i&1);ck(basis(A.flat()).size>=A.length,"proper Hall")}
 function sat(flips){for(let x=0;x<1<<n;x++){if(owners.every((o,i)=>new Set(o.ls.map((l,j)=>l[((x>>o.ids[j])^(flips[i]>>j))&1])).size<4))return true}return false}
 return {n,owners:owners.length,exposure:min,rank:basis(rows.flat()).size,base:sat(owners.map(()=>0)),sat}}
 const p1=[0,1],p2=[2,3];
 let pairs=[[[0,1],[2,3]],[[0,2],[1,4]],[[0,3],[2,4]],[[0,4],[1,3]],[[1,2],[3,4]]];
 // Ordered lists reversed on the second port of each pair so bad iff the pair bits are equal.
 let A=pairs.map(pair=>({ids:pair.flat(),ls:[p1,[1,0],p2,[3,2]],blocks:[[0,1],[2,3]],unary:[]}));let K=starNetwork(5,A);ck(!K.base,"K5 UNSAT");let neighbors=0;for(let i=0;i<5;i++)for(let j of [0,2]){let f=Array(5).fill(0);f[i]=1<<j;ck(K.sat(f),"K5 flip neighbor");neighbors++}results.starControls.push({type:"K5",n:K.n,owners:K.owners,exposure:K.exposure,rank:K.rank,baseSAT:K.base,singleEdgeParitySATNeighbors:neighbors});
 let B=Array.from({length:4},()=>({ids:[0,1,2,3],ls:[[0,1],[1,3],[3,2],[2,0]],blocks:[[0,1,2,3]],unary:[]})),C=starNetwork(4,B);let test=0;for(let s=0;s<65536;s++){let f=Array.from({length:4},(_,i)=>s>>(i*4)&15);ck(C.sat(f),"mixed rank3 SAT");test++}results.starControls.push({type:"four-cycle directions",n:C.n,owners:C.owners,exposure:C.exposure,rank:C.rank,baseSAT:C.base,signings:test});
 let U=Array.from({length:4},(_,i)=>({ids:i%2?[3,1,2,0]:[0,1,2,3],ls:[[0,1],[1,3],[0,3],[2,3]],blocks:[[0,1,2]],unary:[3]})),V=starNetwork(4,U);test=0;for(let s=0;s<65536;s++){let f=Array.from({length:4},(_,i)=>s>>(i*4)&15);ck(V.sat(f),"anchor full Hall");test++}results.starControls.push({type:"triangle + forced port",n:V.n,owners:V.owners,exposure:V.exposure,rank:V.rank,baseSAT:V.base,signings:test});
 results.assertions=checks;return results
}
console.log(JSON.stringify(audit(),null,2));
