function experiment(){
let seed=8152026; const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
let stats={seed:8152026,random:0,accepted:0,declined:0,empty:0,satTargets:0,unsatTargets:0,verifiedLifts:0,fullTuples:0,thinTuples:0,conditionalFiberChecks:0,scaling:[],hostile:null};
const assert=(x,m)=>{if(!x)throw Error(m)};
const sum=(n,E,x)=>{let b=Array(n).fill(0);E.forEach(([u,v],i)=>{b[u]-=x[i];b[v]+=x[i]});return b};
const tag=(E,x)=>E.reduce((t,e,i)=>t^((x[i]&1)?e[3]:0),0);
const eq=(a,b)=>a.every((x,i)=>x===b[i]);
function enumerate(E,fn){let x=Array(E.length).fill(0);function rec(i){if(i===E.length){fn(x.slice());return}for(let k=0;k<=E[i][2];k++){x[i]=k;rec(i+1)}}rec(0)}
function structure(n,H){
 let p=Array.from({length:n},(_,i)=>i), find=x=>p[x]===x?x:p[x]=find(p[x]);
 let tree=[], chords=[]; H.forEach(([u,v],i)=>{if(find(u)===find(v))chords.push(i);else{p[find(u)]=find(v);tree.push(i)}});
 let roots=p.map((_,i)=>find(i)), adj=Array.from({length:n},()=>[]);for(let i of tree){let [u,v]=H[i];adj[u].push([v,i]);adj[v].push([u,i])}
 let h=Array(n).fill(null);for(let r=0;r<n;r++)if(h[r]===null){h[r]=0;let q=[r];for(let u of q)for(let [v,i] of adj[u])if(h[v]===null){h[v]=h[u]^H[i][3];q.push(v)}}
 let cuts=tree.map(i=>{let seen=new Set([H[i][1]]), q=[H[i][1]];for(let u of q)for(let [v,j] of adj[u])if(j!==i&&!seen.has(v)){seen.add(v);q.push(v)}return seen});
 function cycle(i){let [u,v]=H[i];let par=new Map([[u,null]]),q=[u];for(let a of q)for(let [z,j] of adj[a])if(!par.has(z)){par.set(z,[a,j]);q.push(z)}let s=[i];while(v!==u){let [a,j]=par.get(v);s.push(j);v=a}return s}
 return {tree,chords,roots,h,cuts,cycle}
}
function run(n,H,K,b,qbits,kind){
 let st=structure(n,H), {tree,chords,roots,h,cuts,cycle}=st;let Q=K.map(([u,v,c,g])=>[roots[u],roots[v],c,g^h[u]^h[v]]);
 let cb=Array(n).fill(0);b.forEach((z,i)=>cb[roots[i]]+=z);
 let ys=[];enumerate(Q,y=>{stats.thinTuples++;if(eq(sum(n,Q,y),cb))ys.push(y)});
 let actual=new Map();enumerate(H.concat(K),x=>{stats.fullTuples++;if(eq(sum(n,H.concat(K),x),b)){let key=x.slice(H.length).join(",");if(!actual.has(key))actual.set(key,new Set());actual.get(key).add(tag(H.concat(K),x))}});
 if(!ys.length){assert(actual.size===0,"empty quotient");stats.empty++;return}
 let y0=ys[0],k0=sum(n,K,y0),corr=y=>{let z=sum(n,K,y);return cuts.map(S=>[...S].reduce((a,v)=>a+k0[v]-z[v],0))};
 let cs=ys.map(corr),lo=H.map(()=>1),hi=H.map(e=>e[2]-1);
 tree.forEach((i,j)=>{lo[i]-=Math.min(...cs.map(x=>x[j]));hi[i]-=Math.max(...cs.map(x=>x[j]))});
 let f=null;enumerate(H,x=>{if(f===null&&x.every((z,i)=>z>=lo[i]&&z<=hi[i])&&eq(sum(n,H,x),b.map((z,i)=>z-k0[i])))f=x});
 if(f===null){stats.declined++;if(kind==="hostile"){let bad=[1,1,0,0], forced=[1,1];stats.hostile={accepted:false,naiveMidpoint:bad,thinChoice:forced,actualTags:[...actual.get("1,1")],incorrectNaiveTag:3};assert(!actual.get("1,1").has(3),"hostile")};return}
 stats.accepted++;
 let basis=new Map([[0,[]]]);for(let i of chords){let g=H[i][3]^h[H[i][0]]^h[H[i][1]],c=cycle(i);for(let [t,s] of [...basis])if(!basis.has(t^g)){let z=new Set(s);for(let j of c)z.has(j)?z.delete(j):z.add(j);basis.set(t^g,[...z])}}
 let offset=b.reduce((a,z,i)=>a^((z&1)?h[i]:0),0),all=new Set();
 for(let j=0;j<ys.length;j++){
 let y=ys[j],x=f.slice();tree.forEach((i,k)=>x[i]+=cs[j][k]);assert(x.every((z,i)=>z>=1&&z<H[i][2]),"margin");
 let base=tag(H.concat(K),x.concat(y));let predicted=new Set();
 for(let [w,edges] of basis){let d=Array(H.length).fill(0),unused=new Set(edges);
 while(unused.size){let i=unused.values().next().value,start=H[i][0],v=start;do{let k=[...unused].find(j=>H[j][0]===v||H[j][1]===v);assert(k!==undefined,"Euler");unused.delete(k);let [a,b]=H[k];d[k]=a===v?1:-1;v=a===v?b:a}while(v!==start)}
 let lift=x.map((z,i)=>z+d[i]).concat(y);let t=base^w;assert(eq(sum(n,H.concat(K),lift),b)&&lift.every((z,i)=>z>=0&&z<=H.concat(K)[i][2])&&tag(H.concat(K),lift)===t,"bad lift");stats.verifiedLifts++;predicted.add(t);all.add(t)}
 let a=actual.get(y.join(","));assert(a&&a.size===predicted.size&&[...a].every(t=>predicted.has(t)),"fiber");stats.conditionalFiberChecks++;
 let qtag=tag(Q,y)^offset;assert(basis.has(qtag^base),"gauge");
 }
 for(let t=0;t<(1<<qbits);t++){if(all.has(t))stats.satTargets++;else stats.unsatTargets++}
}
for(let k=0;k<220;k++){let n=2+rnd(3),H=[],K=[],m=2+rnd(5);for(let i=0;i<m;i++){let u=rnd(n),v=rnd(n),e=[u,v,1+rnd(4),rnd(16)];(i<Math.ceil(m/2)?H:K).push(e)}let E=H.concat(K),x=E.map(e=>rnd(e[2]+1)),b=sum(n,E,x);if(k%11===0){b[0]+=5;b[1]-=5}stats.random++;run(n,H,K,b,4,"random")}
run(2,[[0,1,2,1],[0,1,2,2]],[[0,1,1,0],[0,1,1,0]],[-2,2],2,"hostile");
run(2,[[0,1,8,1],[0,1,8,2]],[[0,1,1,4],[0,1,1,8]],[-9,9],4,"control");
for(let r of [8,16,32,64,128]){ // r thick chords, one thick tree, two thin unit loops after contraction; all independent tags except tree=0
 let H=Array.from({length:r+1},(_,i)=>[0,1,8,i?1n<<BigInt(i-1):0n]),K=[[0,1,1,1n<<BigInt(r)],[0,1,1,0n]],b=4*(r+1)+1;
 for(let y of [[0,0],[0,1],[1,0],[1,1]])for(let mode=0;mode<3;mode++){let t=mode===0?0n:mode===1?(1n<<BigInt(r))-1n:0x55n&((1n<<BigInt(r))-1n);let x=H.map((_,i)=>i===0?5-y[0]-y[1]:4);let d=0;for(let i=1;i<=r;i++)if((t>>BigInt(i-1))&1n){let s=(d===0?1:-1);x[i]+=s;d+=s}x[0]-=d;assert(x.every(z=>z>=0&&z<=8)&&x.reduce((a,z)=>a+z,0)+y[0]+y[1]===b,"scale balance");let tg=H.reduce((a,e,i)=>a^((x[i]&1)?e[3]:0n),0n)^((y[0]&1)?K[0][3]:0n);assert(tg===(t^((y[0]&1)?K[0][3]:0n)),"scale tag");stats.verifiedLifts++}
 stats.scaling.push({thickRank:r,originalCycleRank:r+2,quotientCycleRank:2,thinStates:4,verifiedLifts:12,unavailableTag:(1n<<BigInt(r+1)).toString()});
}
return stats
}
console.log(JSON.stringify(experiment(),null,2));
