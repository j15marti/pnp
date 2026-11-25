function run(){
 const E=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const bits=(a,i)=>(a>>i)&1;
 const options=f=>Array.from({length:8},(_,i)=>i).filter(i=>i!==f&&i!==(f^7));
 let stats={cases:0,guards:0,sat:0,unsat:0,root_sat:0,root_unsat:0,positive_coefficients:0,integer_pin_certificates:0,assertions:0,cut_checks:0,wheel_matchings:0};
 function ok(x){stats.assertions++;if(!x)throw Error("assertion "+stats.assertions)}
 function integerRep(A,word,free){let c=Array(8).fill(0),base=A[0];c[base]=1;for(const j of free){let p=A.find(a=>!bits(a,j)&&A.includes(a^(1<<j)));ok(p!==undefined);let d=bits(word,j)-bits(base,j);c[p]-=d;c[p^(1<<j)]+=d}ok(c.reduce((a,b)=>a+b,0)===1);for(let j=0;j<3;j++)ok(A.reduce((s,a)=>s+c[a]*bits(a,j),0)===bits(word,j));return c}
 function verify(E,F,n){
  stats.cases++;
  for(let pin=-1;pin<n;pin++)for(let pv=0;pv<(pin<0?1:2);pv++){
   stats.guards++;let count=0;
   for(let x=0;x<(1<<n);x++){if(pin>=0&&bits(x,pin)!==pv)continue;if(E.every((e,i)=>options(F[i]).includes(e.reduce((a,v,j)=>a+(bits(x,v)<<j),0))))count++}
   stats[count?"sat":"unsat"]++;if(pin<0)stats[count?"root_sat":"root_unsat"]++;
   let mu=Array(n).fill(48);
   if(pin>=0){mu[pin]=96*pv;E.forEach((e,i)=>{let j=e.indexOf(pin);if(j<0)return;let forbidden=bits(F[i],j)===pv?F[i]:F[i]^7;for(let l=0;l<3;l++)if(l!==j)mu[e[l]]=48+(bits(forbidden,l)?-3:3)})}
   let AA=E.map((e,i)=>options(F[i]).filter(a=>pin<0||!e.includes(pin)||bits(a,e.indexOf(pin))===pv));
   AA.forEach((A,i)=>{let e=E[i],w=Array(8).fill(0),j=e.indexOf(pin);
    if(j<0){for(let a of A)w[a]=16;for(let l=0;l<3;l++){let p=A.find(a=>!bits(a,l)&&A.includes(a^(1<<l)));let d=mu[e[l]]-48;w[p]-=d;w[p^(1<<l)]+=d}}
    else {let f=bits(F[i],j)===pv?F[i]:F[i]^7;for(let a of A){let d=0;for(let l=0;l<3;l++)if(l!==j&&bits(a,l)!==bits(f,l))d++;w[a]=d===2?6:45}}
    ok(A.every(a=>w[a]>0));stats.positive_coefficients+=A.length;ok(w.reduce((a,b)=>a+b,0)===96);for(let l=0;l<3;l++)ok(A.reduce((s,a)=>s+w[a]*bits(a,l),0)===mu[e[l]])
   });
   // Every allowed local option has a signed-integer completion under the same guard.
   AA.forEach((A,i)=>A.forEach(a=>{let x=Array(n).fill(0);if(pin>=0)x[pin]=pv;E[i].forEach((v,j)=>x[v]=bits(a,j));AA.forEach((B,k)=>{let e=E[k],word=e.reduce((s,v,j)=>s+(x[v]<<j),0);if(k===i){ok(B.includes(word));ok(word===a)}else integerRep(B,word,[0,1,2].filter(j=>e[j]!==pin))});stats.integer_pin_certificates++}));
  }
 }
 function rank(xs){let b=new Map();for(let x of xs){while(x){let p=x.toString(2).length-1;if(b.has(p))x^=b.get(p);else{b.set(p,x);break}}}return b.size}
 // Actual wheel incidence and tags, one deleted spoke, six allowed configurations.
 function wheel(A){let edges=[];for(let i=0;i<7;i++)edges.push([i,(i+1)%7,-1]);for(let i=0;i<6;i++)edges.push([7,i,A[i]]);
  let out=[];function dfs(mask,tag){if(!mask){out.push(tag);return}let u=0;while(!(mask&(1<<u)))u++;for(let [a,b,t] of edges){let v=a===u?b:b===u?a:-1;if(v>=0&&(mask&(1<<v)))dfs(mask^(1<<u)^(1<<v),t<0?tag:t)}}dfs(255,-1);ok(out.length===6&&out.sort((a,b)=>a-b).join()==A.join());stats.wheel_matchings+=out.length;return edges}
 function cuts(E,F,n){let O=Array.from({length:n},()=>[]);E.forEach((e,i)=>e.forEach((v,j)=>O[v].push([i,j])));let tags=E.map(()=>[0n,0n,0n]);let q=8*E.length;
  for(let L of O)for(let a=1;a<L.length;a++){let [i,j]=L[0],[k,l]=L[a],z=1n<<BigInt(q++);tags[i][j]^=z;tags[k][l]^=z}
  let cols=E.map((e,i)=>wheel(options(F[i])).map(([u,v,t])=>{let z=(1n<<BigInt(8*i+u))^(1n<<BigInt(8*i+v));if(t>=0)for(let j=0;j<3;j++)if(bits(t,j))z^=tags[i][j];return z}));
  for(let mask=1;mask<(1<<E.length)-1;mask++){let A=cols.filter((_,i)=>bits(mask,i)).flat(),B=cols.filter((_,i)=>!bits(mask,i)).flat();let boundary=O.filter(L=>L.some(([i])=>bits(mask,i))&&L.some(([i])=>!bits(mask,i))).length;ok(rank(A)+rank(B)-rank([...A,...B])===boundary);stats.cut_checks++}
 }
 verify(E,Array(7).fill(0),7);cuts(E,Array(7).fill(0),7);
 for(let i=0;i<7;i++)for(let f=1;f<=3;f++){let F=Array(7).fill(0);F[i]=f;verify(E,F,7);cuts(E,F,7)}
 for(let k=3;k<=6;k++){let G=Array.from({length:k},(_,i)=>[i,(i+1)%k,k+i]),F=G.map((_,i)=>i%4);verify(G,F,2*k);cuts(G,F,2*k)}
 return stats;
}
console.log(JSON.stringify(run(),null,2));
