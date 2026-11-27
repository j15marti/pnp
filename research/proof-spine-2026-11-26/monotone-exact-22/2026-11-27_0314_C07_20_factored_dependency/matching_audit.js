function matchingAudit(){
 const assert=(x,m)=>{if(!x)throw Error(m||"assert")};
 function source(k){
  let n=5,rows=[[0,1,2,3],[0,1,3,4],[0,1,4,2]],pins=[[0,0]],x=Array.from({length:k},()=>Array.from({length:k},()=>n++)),chains=[];
  function chain(ids){let p=Array.from({length:k+1},()=>n++),bar=Array.from({length:k+1},()=>n++);pins.push([p[0],0],[p[k],1]);for(let i=0;i<=k;i++)rows.push([p[i],bar[i],0,2]);for(let i=1;i<=k;i++)rows.push([p[i-1],ids[i-1],bar[i],2]);chains.push({ids,p,bar})}
  for(let i=0;i<k;i++)chain(x[i]);for(let j=0;j<k;j++)chain(x.map(r=>r[j]));
  for(const r of rows)assert(r.length===4&&new Set(r).size===4);
  return {k,n,rows,pins,x,chains};
 }
 function lift(F,perm,deleted){const z=Array(F.n).fill(0);z[2]=z[3]=z[4]=1;for(let i=0;i<F.k;i++)z[F.x[i][perm[i]]]=1;
  for(const c of F.chains){let s=0;for(let i=0;i<c.p.length;i++){if(i)s+=z[c.ids[i-1]];z[c.p[i]]=s;z[c.bar[i]]=1-s}}
  assert(z.every(v=>v===0||v===1)&&F.rows.every(r=>r.reduce((s,i)=>s+z[i],0)===2)&&F.pins.every(([i,b])=>z[i]===b)&&deleted.every(i=>z[i]===0));return z}
 function permute(a){if(!a.length)return [[]];return a.flatMap((x,i)=>permute(a.filter((_,j)=>i!==j)).map(p=>[x,...p]))}
 function augment(F,D,M){let match=Array(F.k).fill(-1);function dfs(i,seen){for(let j=0;j<F.k;j++){M.augment++;if(D.has(F.x[i][j])||seen.has(j))continue;seen.add(j);if(match[j]<0||dfs(match[j],seen)){match[j]=i;return true}}return false}
  for(let i=0;i<F.k;i++)if(!dfs(i,new Set()))return null;let p=[];match.forEach((i,j)=>p[i]=j);return p}
 function hall(F,D,M){for(let s=1;s<2**F.k;s++){let ns=0,a=0;for(let i=0;i<F.k;i++)if(s&(1<<i)){a++;for(let j=0;j<F.k;j++){M.hall++;if(!D.has(F.x[i][j]))ns|=1<<j}}let b=0;for(let j=0;j<F.k;j++)if(ns&(1<<j))b++;if(b<a)return true}return false}
 const F=source(3),P=permute([0,1,2]),M={augment:0,hall:0,perm:0},out={contexts:512,no:0,witnessControls:0};
 for(let s=0;s<512;s++){const d=F.x.flat().filter((_,i)=>s&(1<<i)),D=new Set(d),p=augment(F,D,M),h=hall(F,D,M);let w=null;for(const q of P){M.perm++;if(q.every((j,i)=>!D.has(F.x[i][j]))){w=q;break}}assert(!p===h&&!!p===!!w);if(p){lift(F,p,d);out.witnessControls++}else out.no++}
 return {source:F,result:out,meter:M}
}
console.log(JSON.stringify(matchingAudit(),null,2));
