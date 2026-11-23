function run(){
 let seed=481; const rnd=()=>((seed=(Math.imul(1664525,seed)+1013904223)>>>0)/4294967296);
 const cycle=n=>Array.from({length:n},(_,i)=>[i,(i+1)%n]);
 const myc=r=>{let e=cycle(r), a=e.slice();for(const [u,v] of e)a.push([u,v+r],[v,u+r]);for(let i=0;i<r;i++)a.push([i+r,2*r]);return [2*r+1,a]};
 const rank=a=>{let b=Array(31).fill(0),k=0;for(let x of a){while(x){let j=31-Math.clz32(x);if(b[j])x^=b[j];else{b[j]=x;k++;break}}}return k};
 const enc=c=>c.reduce((x,v,i)=>x|((v===0?1:v===1?2:0)<<(2*i)),0);
 function solve(n,e,visit){let adj=Array.from({length:n},()=>[]);for(const [u,v] of e){adj[u].push(v);adj[v].push(u)}let ord=Array.from({length:n},(_,i)=>i).sort((a,b)=>adj[b].length-adj[a].length),c=Array(n).fill(-1),count=0;
 function go(i){if(i===n){count++;if(visit)visit(c);return}let u=ord[i];for(let a=0;a<3;a++)if(adj[u].every(v=>c[v]!==a)){c[u]=a;go(i+1);c[u]=-1}}go(0);return count}
 function hull(n,e){let x0=null,b=[];let count=solve(n,e,c=>{let x=enc(c);if(x0===null)x0=x;else if(rank([...b,x^x0])>b.length)b.push(x^x0)});return [count,b.length]}
 function bipWitness(n,e){let adj=Array.from({length:n},()=>[]);for(let [u,v] of e){adj[u].push(v);adj[v].push(u)}let c=Array(n).fill(-1);for(let i=0;i<n;i++)if(c[i]<0){c[i]=0;let q=[i];for(let u of q)for(let v of adj[u]){if(c[v]<0){c[v]=1-c[u];q.push(v)}else if(c[v]===c[u])return null}}
 let a=[...c],base=enc(a),diff=[];for(let i=0;i<n;i++){a=[...c];a[i]=2;diff.push(enc(a)^base);a=c.map(v=>1-v);let b=enc(a);a[i]=2;diff.push(enc(a)^b)}
 return rank(diff)}
 let rows=[],local=0,cuts=0,forestTests=0,forestStates=0,critical=0,forestShrink=0,rankParity=new Set(),cutParity=new Set();
 for(let r of [4,5,6,7]){
  let [n,e]=myc(r);let [models,ar]=hull(n,e);if((models>0)!==(r%2===0))throw Error("myc parity");let neighbors=[];
  if(r%2){for(let i=0;i<e.length;i++){let [cnt,rr]=hull(n,e.filter((_,j)=>j!==i));if(!cnt)throw Error("neighbor");neighbors.push(cnt);critical++}}
  for(let i=0;i<e.length;i++)for(let j=i+1;j<e.length;j++)for(let k=j+1;k<e.length;k++){if(bipWitness(n,[e[i],e[j],e[k]])!==2*n)throw Error("local");local++}
  for(let t=0;t<100;t++){let a=[],b=[];for(let edge of e)(rnd()<.5?a:b).push(edge);let span=es=>[...new Set(es.flat())].flatMap(v=>[1<<(2*v),1<<(2*v+1)]);let A=span(a),B=span(b);let s=rank(A)+rank(B)-rank(A.concat(B));let shared=new Set(a.flat().filter(v=>b.flat().includes(v))).size;if(s!==2*shared)throw Error("cut");cuts++;cutParity.add(s%2)}
  rankParity.add((n+3*e.length)%2);rows.push({r,n,m:e.length,models,affineHullRank:ar,neighbors:neighbors.length,minNeighbor:neighbors.length?Math.min(...neighbors):null,maxNeighbor:neighbors.length?Math.max(...neighbors):null});
 }
 for(let t=0;t<160;t++){
  let n=3+Math.floor(rnd()*7),e=[];for(let v=1;v<n;v++)if(rnd()<.85)e.push([v,Math.floor(rnd()*v)]);let B=Array.from({length:n},(_,i)=>i).filter(()=>rnd()<.45),mark=new Set(B),alive=new Set(Array.from({length:n},(_,i)=>i)),a=e.slice();
  for(;;){let v=[...alive].find(v=>!mark.has(v)&&a.filter(z=>z.includes(v)).length<=2);if(v===undefined)break;alive.delete(v);a=a.filter(z=>!z.includes(v))}
  if(alive.size<n)forestShrink++;
  let p=new Set(),q=new Set(),key=c=>B.map(i=>c[i]).join("");solve(n,e,c=>p.add(key(c)));solve(n,a,c=>q.add(key(c)));
  if(p.size!==q.size||[...p].some(k=>!q.has(k)))throw Error("projection");
  let privateCount=[...alive].filter(v=>!mark.has(v)).length;if(privateCount>Math.max(0,B.length-2))throw Error("forest size");
  forestTests++;forestStates+=3**B.length;
 }
 // regular parity controls, finite only, no expansion assertion
 let reg=[];
 for(let [n,d] of [[9,6],[10,6],[12,6],[10,7],[12,7],[14,7]]){
  let e=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++){let z=Math.min(v-u,n-v+u);if(z<=Math.floor(d/2)||(d%2&&z===n/2))e.push([u,v])}
  let models=solve(n,e);if(models)throw Error("K4 circulant should be unsat");reg.push({n,d,m:e.length,models,eqRank:n+3*e.length,nullity:2*n});
 }
 let satReg=[];for(let d of [6,7]){let n=2*d,e=[];for(let u=0;u<d;u++)for(let v=d;v<n;v++)e.push([u,v]);let [models,ar]=hull(n,e);if(!models||ar!==2*n)throw Error("bipartite regular");satReg.push({n,d,m:e.length,models,affineHullRank:ar})}
 return {seed:481,rows,local,cuts,forestTests,forestStates,forestShrink,critical,rankParity:[...rankParity],cutParity:[...cutParity],reg,satReg};
}
console.log(JSON.stringify(run(),null,2));
