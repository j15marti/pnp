function closureAudit(){
 const n=18,F=[[3,8,13],[1,5,17],[0,16,17],[6,8,13],[1,5,9],[2,11,13],[3,8,10],[0,7,12],[2,7,12],[5,9,16],[4,6,11],[2,3,7],[4,11,12],[10,14,15],[10,14,16],[9,14,15],[4,6,15],[0,1,17]];
 const base=F.map(r=>[r.reduce((s,i)=>s^(1<<i),0),1]),H=[];for(let r of F)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)H.push([2*r[i],2*r[j]]);
 const rel=[];for(let i=0;i<n;i++){rel.push([1<<i,i,-1]);for(let j=i+1;j<n;j++)rel.push([(1<<i)^(1<<j),i,j])}
 let satCalls=0,checks=0;const ck=x=>{checks++;if(!x)throw Error("assertion "+checks)};
 const hi=x=>31-Math.clz32(x);
 function reduce(p,a,b=0){while(a){let i=hi(a);if(!p[i])break;a^=p[i][0];b^=p[i][1]}return [a,b]}
 function add(p,a,b){let [v,t]=reduce(p,a,b);if(!v)return t?-1:0;p[hi(v)]=[v,t];return 1}
 function cnf(i,j,b){if(j<0)return [[2*i+b,2*i+b]];let a=[];for(let u of [0,1])for(let v of [0,1])if((u^v)!==b)a.push([2*i+(1^u),2*j+(1^v)]);return a}
 function sat(cs){satCalls++;let g=Array.from({length:2*n},()=>[]),rg=Array.from({length:2*n},()=>[]);for(let [a,b] of cs){g[a^1].push(b);g[b^1].push(a);rg[b].push(a^1);rg[a].push(b^1)}let seen=new Set(),order=[];function dfs(i){if(seen.has(i))return;seen.add(i);for(let j of g[i])dfs(j);order.push(i)}for(let i=0;i<2*n;i++)dfs(i);let comp=Array(2*n).fill(-1),k=0;function rev(i){if(comp[i]>=0)return;comp[i]=k;for(let j of rg[i])rev(j)}for(let i of order.reverse())if(comp[i]<0){rev(i);k++}return !Array.from({length:n},(_,i)=>i).some(i=>comp[2*i]===comp[2*i+1])}
 function close(extra){let p=[],rounds=0,learned=[];for(let [a,b] of base.concat(extra))if(add(p,a,b)<0)return {no:true,reason:"Gaussian",rank:p.filter(Boolean).length,rounds,learned};while(true){rounds++;let cs=H.slice(),unknown=[];for(let [a,i,j] of rel){let [v,b]=reduce(p,a);if(!v)cs.push(...cnf(i,j,b));else unknown.push([a,i,j])}if(!sat(cs))return {no:true,reason:"SCC after affine sharing",rank:p.filter(Boolean).length,rounds,learned};let changes=0;for(let [a,i,j] of unknown){let [v]=reduce(p,a);if(!v)continue;for(let b of [0,1])if(!sat(cs.concat(cnf(i,j,b)))){let z=add(p,a,1^b);if(z<0)return {no:true,reason:"joint relaxation conflict",rank:p.filter(Boolean).length,rounds,learned};if(z){learned.push([a,1^b]);changes++}break}}if(!changes)return {no:false,rank:p.filter(Boolean).length,rounds,learned,rows:p.filter(Boolean)};ck(rounds<=n+1)}}
 const bare=close([]),pin0=close([[1<<12,0]]),pin1=close([[1<<12,1]]);
 const allx=[];for(let x=0;x<1<<n;x++)if(F.every(r=>r.reduce((s,i)=>s+(x>>i&1),0)===1))allx.push(x);ck(allx.length===3);ck(!bare.no&&!pin0.no);ck(!pin1.no||allx.every(x=>!(x>>12&1)));
 let guards=[],probeRounds=0,probeRejects=[];while(true){probeRounds++;let now=close(guards);ck(!now.no);let p=[];for(let [a,b] of now.rows)ck(add(p,a,b)>=0);let change=false;for(let i=0;i<n;i++){if(!reduce(p,1<<i)[0])continue;let found=false;for(let b of [0,1]){let z=close(guards.concat([[1<<i,b]]));if(z.no){ck(allx.every(x=>(x>>i&1)!==b));guards.push([1<<i,1^b]);probeRejects.push({i,b,reason:z.reason});change=found=true;break}}if(found)break}if(!change)break;ck(probeRounds<=n+1)}
 return {checks,satCalls,bare,pin0,pin1,probeRounds,probeRejects,forcedPins:guards,remaining:close(guards),actualSolutions:allx};
}
console.log(JSON.stringify(closureAudit(),null,2));
