/* C03-10 independent constant-size certificate; run node audit.js */
function audit(){
 const R={n:8,e:[[0,1],[0,5],[1,2],[1,6],[2,7],[3,5],[3,6],[4,6],[4,7],[5,7]],p:[2,3,0,4]};
 const blocked={edges:[[0,10],[0,6],[0,2],[1,4],[1,7],[1,9],[2,8],[3,4],[3,6],[4,10],[5,7],[5,10],[6,7],[8,9],[11,12],[11,18],[11,14],[12,16],[13,15],[13,17],[14,19],[14,15],[16,19],[17,19],[17,18],[3,18],[9,13],[5,16],[8,15],[2,12]],flow:[1,2,3,3,1,2,2,1,1,2,2,3,3,3,3,2,1,2,2,3,2,3,3,1,2,0,1,1,1,1],proper:[2,1,3,2,1,3,2,3,2,1,2,3,3,1,2,3,1,3,1,3,3,2,2,1,2,1,2,1,3,1]};
 let checks=0;const assert=(x)=>{checks++;if(!x)throw Error("assert "+checks)};
 function ext(w){let d=Array(R.n).fill(0);for(let i=0;i<4;i++)d[R.p[i]]^=w[i];function dfs(k){if(k===R.e.length)return d.every(x=>!x);let [u,v]=R.e[k];for(let c=1;c<=3;c++){d[u]^=c;d[v]^=c;let ok=dfs(k+1);d[u]^=c;d[v]^=c;if(ok)return true}return false}return dfs(0)}
 let words=0;
 for(let a=0;a<4;a++)for(let b=0;b<4;b++)for(let c=0;c<4;c++)for(let d=0;d<4;d++){
  if(a^b^c^d)continue;words++;let w=[a,b,c,d],zero=w.filter(x=>!x).length;
  if(zero===0)assert(ext(w)===(a===b&&c===d));if(zero===1)assert(ext(w));
 }
 for(let f of [blocked.flow,blocked.proper]){let d=Array(20).fill(0),deg=Array(20).fill(0);for(let [i,[u,v]] of blocked.edges.entries()){d[u]^=f[i];d[v]^=f[i];deg[u]++;deg[v]++}assert(d.every(x=>!x));assert(deg.every(x=>x===3))}assert(blocked.flow.filter(x=>!x).length===1);assert(blocked.proper.every(x=>x!==0));
 let components=[];
 for(let [lo,hi,start] of [[0,11,3],[11,20,18]]){let p=blocked.edges.map((e,i)=>e.includes(start)?blocked.flow[i]:0).find(x=>x);for(let delta of [1,2,3]){if(delta===p)continue;let q=[start],seen=new Set(q);for(let v of q){for(let [i,[a,b]] of blocked.edges.entries()){if(!blocked.flow[i]||blocked.flow[i]===delta)continue;let u=a===v?b:b===v?a:-1;if(u<0)continue;assert(u>=lo&&u<hi);if(!seen.has(u)){seen.add(u);q.push(u)}}}components.push({start,p,delta,vertices:[...seen].sort((a,b)=>a-b)})}}
 let t=0;for(let n=38;n<=400;n+=2)for(let s=19;s<=n/2;s++){assert(75n*BigInt(s+17)**160n+BigInt(n-s+17)**160n<BigInt(n)**160n);t++}
 assert(1350n*18n**159n<19n**159n);
 return {relay_words:words,checks,tariff_cases:t,blocked,components,R};
}
console.log(JSON.stringify(audit(),null,2));
