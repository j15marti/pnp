const inputs = [{"n":7,"root":[{"t":[0,1,2],"bad":[0,7]},{"t":[0,3,4],"bad":[0,7]},{"t":[0,5,6],"bad":[0,7]},{"t":[1,3,5],"bad":[0,7]},{"t":[1,4,6],"bad":[0,7]},{"t":[2,3,6],"bad":[0,7]},{"t":[2,4,5],"bad":[0,7]}],"sat":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[0,7]},{"t":[0,5,6],"bad":[0,7]},{"t":[1,3,5],"bad":[0,7]},{"t":[1,4,6],"bad":[0,7]},{"t":[2,3,6],"bad":[0,7]},{"t":[2,4,5],"bad":[0,7]}],"guards":[]},{"n":15,"root":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[1,6]},{"t":[0,5,6],"bad":[3,4]},{"t":[0,7,8],"bad":[2,5]},{"t":[0,9,10],"bad":[3,4]},{"t":[0,11,12],"bad":[3,4]},{"t":[0,13,14],"bad":[1,6]},{"t":[1,3,5],"bad":[2,5]},{"t":[1,4,6],"bad":[3,4]},{"t":[1,7,9],"bad":[1,6]},{"t":[1,8,10],"bad":[3,4]},{"t":[1,11,13],"bad":[1,6]},{"t":[1,12,14],"bad":[2,5]},{"t":[2,3,6],"bad":[1,6]},{"t":[2,4,5],"bad":[2,5]},{"t":[2,7,10],"bad":[3,4]},{"t":[2,8,9],"bad":[2,5]},{"t":[2,11,14],"bad":[1,6]},{"t":[2,12,13],"bad":[1,6]},{"t":[3,7,11],"bad":[3,4]},{"t":[3,8,12],"bad":[3,4]},{"t":[3,9,13],"bad":[3,4]},{"t":[3,10,14],"bad":[3,4]},{"t":[4,7,12],"bad":[1,6]},{"t":[4,8,11],"bad":[2,5]},{"t":[4,9,14],"bad":[2,5]},{"t":[4,10,13],"bad":[1,6]},{"t":[5,7,13],"bad":[1,6]},{"t":[5,8,14],"bad":[3,4]},{"t":[5,9,11],"bad":[2,5]},{"t":[5,10,12],"bad":[2,5]},{"t":[6,7,14],"bad":[3,4]},{"t":[6,8,13],"bad":[2,5]},{"t":[6,9,12],"bad":[2,5]},{"t":[6,10,11],"bad":[0,7]}],"sat":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[1,6]},{"t":[0,5,6],"bad":[3,4]},{"t":[0,7,8],"bad":[2,5]},{"t":[0,9,10],"bad":[3,4]},{"t":[0,11,12],"bad":[3,4]},{"t":[0,13,14],"bad":[1,6]},{"t":[1,3,5],"bad":[2,5]},{"t":[1,4,6],"bad":[3,4]},{"t":[1,7,9],"bad":[1,6]},{"t":[1,8,10],"bad":[3,4]},{"t":[1,11,13],"bad":[1,6]},{"t":[1,12,14],"bad":[2,5]},{"t":[2,3,6],"bad":[1,6]},{"t":[2,4,5],"bad":[2,5]},{"t":[2,7,10],"bad":[3,4]},{"t":[2,8,9],"bad":[2,5]},{"t":[2,11,14],"bad":[1,6]},{"t":[2,12,13],"bad":[1,6]},{"t":[3,7,11],"bad":[3,4]},{"t":[3,8,12],"bad":[3,4]},{"t":[3,9,13],"bad":[3,4]},{"t":[3,10,14],"bad":[3,4]},{"t":[4,7,12],"bad":[1,6]},{"t":[4,8,11],"bad":[2,5]},{"t":[4,9,14],"bad":[2,5]},{"t":[4,10,13],"bad":[1,6]},{"t":[5,7,13],"bad":[1,6]},{"t":[5,8,14],"bad":[3,4]},{"t":[5,9,11],"bad":[2,5]},{"t":[5,10,12],"bad":[2,5]},{"t":[6,7,14],"bad":[3,4]},{"t":[6,8,13],"bad":[2,5]},{"t":[6,9,12],"bad":[2,5]},{"t":[6,10,11],"bad":[2,5]}],"guards":[[4,6,0],[6,8,0],[0,3,0],[1,2,0],[2,3,0],[3,5,1],[5,7,1]]}];
const run = function run(inputs){
 const stats={checks:0,closureScans:0,walshButterflies:0,characterCalls:0,hubModes:0,referenceWords:0};
 function ck(c){stats.checks++;if(!c)throw Error("assert "+stats.checks)}
 const parity=x=>{let p=0;while(x){x&=x-1;p^=1}return p};
 const dot=(a,x)=>parity(a&x);
 function rref(rows){let B=new Map();for(let [a,b] of rows){for(const [i,[c,d]] of [...B].sort((u,v)=>v[0]-u[0]))if(a&(1<<i)){a^=c;b^=d}if(!a){if(b)return null;continue}let i=31-Math.clz32(a);for(const [j,[c,d]] of B)if(c&(1<<i))B.set(j,[c^a,d^b]);B.set(i,[a,b])}return [...B].sort((u,v)=>v[0]-u[0]).map(z=>z[1])}
 const packets=owners=>owners.map(o=>[[1<<o.t[0]^1<<o.t[1],(o.bad[0]&1)^((o.bad[0]>>1)&1)],[1<<o.t[0]^1<<o.t[2],(o.bad[0]&1)^((o.bad[0]>>2)&1)]]);
 function close(E,G){G=rref(G);if(!G)return null;for(;;){let changed=false;for(const e of E){stats.closureScans++;let h=rref([...G,...e]);if(!h)continue;if(h.length===G.length)return null;if(h.length===G.length+1){let a=e.find(z=>{let t=rref([...G,z]);return t&&t.length>G.length});ck(!!a);G=rref([...G,[a[0],a[1]^1]]);changed=true;break}}if(!changed)return G}}
 function edges(owners){return owners.flatMap(o=>[[0,1],[0,2],[1,2]].map(([i,j])=>[o.t[i],o.t[j],1^((o.bad[0]>>i)&1)^((o.bad[0]>>j)&1)]))}
 function solve(n,E,G,hs,cap,target){
   // E is a list of unit preferred pair parities. The planar core is a subgraph of K_{2,n-2} plus the hub edge.
   let core=[],ex=[];for(let e of E)(e[0]<hs||e[1]<hs?core:ex).push(e);
   let rows=rref([...ex.map(([i,j])=>[1<<i^1<<j,0]),...G.map(([a])=>[a,0])]);let basis=rows.map(z=>z[0]),r=basis.length;
   if(r>cap)return {state:"OPEN",r};
   const R=1<<r, B=1n<<BigInt(n+1), pow=Array.from({length:E.length+1},(_,i)=>B**BigInt(i));
   const masks=Array(R).fill(0);for(let q=1;q<R;q++){let l=q&-q;masks[q]=masks[q^l]^basis[31-Math.clz32(l)]}
   const index=new Map(masks.map((v,i)=>[v,i]));
   const exc=ex.map(([i,j,p])=>[index.get(1<<i^1<<j),p]),gg=G.map(([a,b])=>[index.get(a),b]);
   const W=Array.from({length:R},(_,y)=>gg.every(([a,b])=>dot(a,y)===b)?pow[exc.reduce((v,[a,p])=>v+(dot(a,y)!==p),0)]:0n);
   for(let h=1;h<R;h*=2)for(let i=0;i<R;i+=2*h)for(let j=i;j<i+h;j++){let a=W[j],b=W[j+h];W[j]=a+b;W[j+h]=a-b;stats.walshButterflies++}
   const modes=[];
   for(let h=0;h<(1<<hs);h++){let cost=0,leaf=Array.from({length:n-hs},()=>[0,0]);for(let [i,j,p] of core){if(i<hs&&j<hs)cost+=(dot(1<<i^1<<j,h)!==p);else{if(j<hs)[i,j]=[j,i];ck(i<hs&&j>=hs);for(let b=0;b<2;b++)leaf[j-hs][b]+=(((h>>i)&1)^b)!==p}}
     modes.push({h,c:pow[cost],leaf:leaf.map(([a,b])=>[pow[a]+pow[b],pow[a]-pow[b]])})}
   let total=0n;
   for(let q=0;q<R;q++){if(!W[q])continue;stats.characterCalls++;let f=0n,a=masks[q];for(let z of modes){stats.hubModes++;let v=dot(a,z.h)?-z.c:z.c;for(let j=hs;j<n;j++)v*=z.leaf[j-hs][(a>>j)&1];f+=v}total+=W[q]*f}
   ck(total%BigInt(R)===0n);total/=BigInt(R);ck(total>=0n);
   let count=Number((total/pow[target])%B);return {state:count?"SAT":"UNSAT",r,count,core:core.length,exceptions:ex.length,packed:total.toString()};
 }
 function ref(n,E,G,target){let z=0,count=0n,B=1n<<BigInt(n+1),P=Array.from({length:E.length+1},(_,i)=>B**BigInt(i));for(let x=0;x<(1<<n);x++){stats.referenceWords++;if(!G.every(([a,b])=>dot(a,x)===b))continue;let c=E.reduce((s,[i,j,p])=>s+(dot(1<<i^1<<j,x)!==p),0);if(c===target)z++;count+=P[c]}return {count:z,packed:count.toString()}}
 const shared=[];
 for(let u of inputs){let cases=[["root",u.root,[]],["sat",u.sat,[]]];if(u.guards.length)for(let k of [1,u.guards.length])cases.push(["root/"+k,u.root,u.guards.slice(0,k).map(([i,j,b])=>[1<<i^1<<j,b])]);for(let [name,o,g] of cases){let G=close(packets(o),g),E=edges(o),rr=ref(u.n,E,g,o.length);if(!G){ck(rr.count===0);shared.push({n:u.n,name,state:"UNSAT by closure",count:0});continue}let t=solve(u.n,E,G,2,15,o.length),rr2=ref(u.n,E,G,o.length);ck(t.count===rr.count);ck(t.packed===rr2.packed);let small=solve(u.n,E,G,2,5,o.length);if(small.state!=="OPEN")ck(small.count===rr.count);delete t.packed;delete small.packed;shared.push({n:u.n,name,guardRank:G.length,cap5:small.state,...t})}}
 let seed=20261125;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>9)%n};
 let controls=0,labels={SAT:0,UNSAT:0};
 for(let j=0;j<80;j++){let n=3+rand(6),E=[];for(let i=0;i<n;i++)for(let k=i+1;k<n;k++)if(rand(3)!==0)E.push([i,k,rand(2)]);let G=Array.from({length:rand(4)},()=>[1+rand((1<<n)-1),rand(2)]),target=rand(E.length+1),t=solve(n,E,G,2,15,target),rr=ref(n,E,G,target);ck(t.count===rr.count&&t.packed===rr.packed);controls++;labels[t.state]++}
 return {shared,controls,labels,stats,scope:"Exact hub-core Walsh consumer executed; no general Pfaffian implementation; reference enumeration separate."};
};
console.log(JSON.stringify(run(inputs),null,2));
