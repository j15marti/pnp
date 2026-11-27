function audit(){
 const results=[];
 const range=n=>Array.from({length:n},(_,i)=>i);
 const xor=(n,rows)=>{let B=new Map(),steps=0;for(let [x,b] of rows){while(x){let p=x&-x;if(!B.has(p)){B.set(p,[x,b]);break}let [y,c]=B.get(p);x^=y;b^=c;steps++}if(!x&&b)return {no:true,rank:B.size,steps}}return {no:false,rank:B.size,steps}};
 const bitset=S=>S.reduce((a,i)=>a|(1n<<BigInt(i)),0n);
 function verify(H,cap=20000){
  let {n,E,p,b}=H, L=range(n).map(i=>[]),R=range(n).map(i=>[]),F=[];
  E.forEach(([i,j,w],e)=>{L[i].push(e);R[j].push(e)});
  for(let S of [...L,...R])F.push({S,R:S.map((_,i)=>1<<i)});
  for(let j=0;j<p;j++){let S=range(E.length).filter(e=>E[e][2]>>j&1),words=range(1<<S.length).filter(w=>{let z=0;while(w){z^=1;w&=w-1}return z===(b>>j&1)});F.push({S,R:words})}
  let rows=[...L,...R].map(S=>[bitset(S),1]);for(let j=0;j<p;j++)rows.push([bitset(range(E.length).filter(e=>E[e][2]>>j&1)),b>>j&1]);
  const close=(pins)=>{let D=range(E.length).map(()=>3),del=0;for(let e of pins)D[e]=1;for(;;){let old=del;for(let f of F){let W=f.R.filter(w=>f.S.every((v,i)=>D[v]>>(w>>i&1)&1));if(!W.length)return {no:true,del};f.S.forEach((v,i)=>{let a=W.reduce((z,w)=>z|(1<<(w>>i&1)),0);if(a!==D[v]){D[v]=a;del++}})}if(old===del)return {no:false,del}}};
  let A=xor(E.length,rows),initial=close([]);
  // Independent reference matching supplied by the construction (all diagonal edges).
  // This audit checks the certificate, not acquisition of that matching.
  if(!range(n).every(i=>E.some(e=>e[0]===i&&e[1]===i&&e[2]===0)))throw Error("reference");
  const adj=range(n).map(i=>L[i].map(e=>E[e][1]));
  const reach=s=>{let Q=new Set([s]);for(let v of Q)for(let w of adj[v])Q.add(w);return Q};
  const RS=range(n).map(reach),pins=[],certs=[];
  for(let [i,j,w] of E){if(!RS[j].has(i)){let S=RS[j];if(S.has(i)||!S.has(j)||E.some(([a,c])=>S.has(a)&&!S.has(c)))throw Error("bad tight Hall set");let id=E.findIndex(e=>e[0]===i&&e[1]===j);pins.push(id);certs.push({edge:id,rows:[...S],columns:[...S]})}}
  let afterEach=[],prefix=[];for(let e of pins){prefix.push(e);afterEach.push(close(prefix))}
  let I=xor(E.length,rows.concat(pins.map(i=>[1n<<BigInt(i),0]))),nodes=0,leaves=0,stop=false,found=false,attained=new Set();
  function dfs(i,S,w){if(stop||found)return;if(++nodes>cap){stop=true;return}if(i===n){leaves++;attained.add(w);if(w===b)found=true;return}for(let e of L[i]){let [a,j,v]=E[e];if(!S.has(j)){S.add(j);dfs(i+1,S,w^v);S.delete(j)}}}
  dfs(0,new Set(),0);
  return {n,edges:E.length,initial,affine:A,pins,certs,afterEach,hybrid:I,enumeration:{nodes,leaves,cap,found,stopped:stop,attained:[...attained].sort((a,b)=>a-b)}};
 }
 for(let d of [2,3,4,6,8]){let q=d*d,E=[];for(let s=0;s<2;s++)for(let i=0;i<q;i++)for(let j of [i,Math.floor(i/d)*d+(i%d+1)%d,((Math.floor(i/d)+1)%d)*d+i%d])E.push([s*q+i,s*q+j,0]);for(let i=0;i<4;i++)E.push([i,q+i,Number(i<3)]);
 let z=verify({n:2*q,E,p:1,b:1});if(z.initial.no||z.initial.del||z.affine.no||!z.hybrid.no||z.pins.length!==4||!z.afterEach.some(x=>x.no)||z.enumeration.found)throw Error("family");results.push({d,...z})}
 let E=range(5).map(i=>[i,i,0]);E.push([0,1,1],[1,2,1],[2,0,1],[0,3,2],[3,4,2],[4,0,2]);let hostile=verify({n:5,E,p:2,b:3});if(hostile.initial.no||hostile.affine.no||hostile.hybrid.no||hostile.enumeration.stopped||hostile.enumeration.found||hostile.enumeration.attained.join(",")!=="0,1,2")throw Error("hostile");
 return {results,hostile};
}
console.log(JSON.stringify(audit(),null,2));
