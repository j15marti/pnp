function checkBA13(){
 const stats={assertions:0,querySAT:0,queryUNSAT:0,closureScans:0,forcedRows:0,edgeVisits:0,referenceWords:0,graphCases:0,chain:[],affineSubspacesChecked:0};function ok(c){stats.assertions++;if(!c)throw Error("assertion "+stats.assertions)}
 function solve(n,edges){ // each edge [u,v,p,active] and vertex 0 is fixed reference
   const adj=Array.from({length:n},()=>[]);stats.closureScans++;
   for(const [u,v,p,a] of edges)if(a){adj[u].push([v,p]);adj[v].push([u,p]);stats.forcedRows++}
   const h=Array(n).fill(-1);
   for(let u=0;u<n;u++)if(h[u]<0){h[u]=0;const q=[u];for(let j=0;j<q.length;j++){const v=q[j];for(const [w,p] of adj[v]){stats.edgeVisits++;if(h[w]<0){h[w]=h[v]^p;q.push(w)}else if(h[w]!=(h[v]^p))return null}}}
   stats.closureScans++;ok(edges.every(([u,v,p,a])=>!a||(h[u]^h[v])===p));return h
 }
 function ref(n,edges){for(let x=0;x<(1<<n);x++){stats.referenceWords++;if(edges.every(([u,v,p,a])=>!a||(((x>>u)^(x>>v))&1)===p))return true}return false}
 function doubled(n,edges){const d=Array.from({length:2*n},()=>[]);for(const [u,v,p,a] of edges)if(a)for(let b=0;b<2;b++){const s=2*u+b,t=2*v+(b^p);d[s].push(t);d[t].push(s)}
   const c=Array(2*n).fill(-1);for(let i=0;i<2*n;i++)if(c[i]<0){c[i]=i;const q=[i];for(let j=0;j<q.length;j++)for(const w of d[q[j]])if(c[w]<0){c[w]=i;q.push(w)}}return !Array.from({length:n},(_,i)=>c[2*i]===c[2*i+1]).some(Boolean)
 }
 function query(n,e,reference){const h=solve(n,e),s=h!==null;ok(s===doubled(n,e));if(reference!==null)ok(s===reference);if(s)stats.querySAT++;else stats.queryUNSAT++;return s}
 function chain(k,word){const e=[[0,k,1,true]];for(let i=0;i<k;i++){e.push([i,i+1,0,Boolean(word&(1n<<BigInt(2*i)))]);e.push([i,i+1,0,Boolean(word&(1n<<BigInt(2*i+1)))])}return e}
 for(let k=1;k<=5;k++){let sat=0,unsat=0;for(let w=0;w<4**k;w++){let z=BigInt(w),expected=Array.from({length:k},(_,i)=>((z>>BigInt(2*i))&3n)===0n).some(Boolean),e=chain(k,z);ok(query(k+1,e,ref(k+1,e))===expected);if(expected)sat++;else unsat++}ok(unsat===3**k);stats.chain.push({k,sat,unsat})}
 for(const k of [16,64,256]){let all=(1n<<BigInt(2*k))-1n;ok(!query(k+1,chain(k,all),null));ok(query(k+1,chain(k,all^3n),null));stats.chain.push({k,selectedSAT:1,selectedUNSAT:1})}
 let seed=20813;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
 for(let t=0;t<120;t++){const n=2+rand(6),e=[];for(let j=0;j<2*n;j++){const u=rand(n);let v=rand(n-1);if(v>=u)v++;e.push([u,v,rand(2),Boolean(rand(2))])}query(n,e,ref(n,e));stats.graphCases++}
 // Fano signed NAE: condition on the seven protected low bits; encode each active clause as
 // two opposite parity rows on private endpoints, preserving guard (BW13 duplicated stars).
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const fanoCounts=[];for(let flip=-1;flip<21;flip++){let count=0;for(let x=0;x<128;x++){const e=[];for(let i=0;i<7;i++){const [a,b,c]=fano[i],vals=[a,b,c].map((v,j)=>((x>>v)&1)^Number(flip===3*i+j));const active=vals.every(v=>v===vals[0]);e.push([b,c,0,active],[b,c,1,active])}const original=fano.every((cl,i)=>{let v=cl.map((a,j)=>((x>>a)&1)^Number(flip===3*i+j));return !v.every(b=>b===v[0])});if(query(7,e,ref(7,e)))count++;ok(original===!e.some((r,i)=>i%2===0&&r[3]));}ok(count===(flip<0?0:10));fanoCounts.push(count)}
 // Enumerate every affine flat of GF(2)^6 by growing linear spaces, then translating.
 let spaces=new Map([["0",[0]]]);for(let a=1;a<64;a++){for(const U of [...spaces.values()]){if(U.includes(a))continue;let V=[...U,...U.map(x=>x^a)].sort((a,b)=>a-b);spaces.set(V.join(","),V)}}
 let max=0,contained=0;const bad=x=>[0,1,2].every(i=>((x>>(2*i))&3)!==0);
 for(const U of spaces.values()){const seen=new Set();for(let a=0;a<64;a++){if(seen.has(a))continue;const A=U.map(u=>u^a);A.forEach(x=>seen.add(x));stats.affineSubspacesChecked++;if(A.every(bad)){contained++;max=Math.max(max,A.length);ok(A.length<=8)}}}
 ok(max===8);return {...stats,fanoCounts,flatControl:{k:3,contained,max,lowerBound:Math.ceil(27/8)}}
}
console.log(JSON.stringify(checkBA13(),null,2));
