function discover(data){
 const bit=r=>1n<<BigInt(r), assert=(v,m)=>{if(!v)throw Error(m)};
 function recognize(need,bad){let m=need.length,answers=[];for(let i=0;i<m;i++){let S=new Set([i]),q=[i];for(let k=0;k<q.length;k++)for(let j=0;j<m;j++)if(need[q[k]][j]&&!S.has(j)){S.add(j);q.push(j)}let conflict=null;for(let a of q)for(let b of q)if(bad[a][b])conflict=[a,b];answers.push({seed:i,closure:q.sort((a,b)=>a-b),conflict})}return answers}
 // Independent exhaustive validation of the combinatorial selection theorem on small graphs.
 let seed=1729;const rnd=()=>((seed=(Math.imul(seed,1664525)+1013904223)>>>0)/2**32);
 let graphs=0,subsets=0;for(let k=0;k<240;k++){let n=1+Math.floor(rnd()*8),need=Array.from({length:n},()=>Array(n).fill(false)),bad=need.map(x=>x.slice());for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){need[i][j]=rnd()<.25;need[j][i]=rnd()<.25;bad[i][j]=bad[j][i]=rnd()<.2}let possible=Array(n).fill(false);for(let mask=1;mask<1<<n;mask++){subsets++;let ok=true;for(let i=0;i<n;i++)if(mask>>i&1)for(let j=0;j<n;j++){if(need[i][j]&&!(mask>>j&1)||bad[i][j]&&(mask>>j&1))ok=false}if(ok)for(let i=0;i<n;i++)if(mask>>i&1)possible[i]=true}recognize(need,bad).forEach((a,i)=>assert(!a.conflict===possible[i],"closure recognition discrepancy"));graphs++}
 function job(z,delta){let m=z.ownerIDs.length,n=z.rowMap.length,A=z.pairHex.map(h=>BigInt("0x"+h)),D=Array.from({length:m},()=>0n),g=D.map(()=>[]);z.rowMap.forEach(([i],r)=>{g[i].push(r);if(z.live[r])D[i]|=bit(r)});
 let scans=0;function ac(){let ch=true;while(ch){ch=false;scans++;for(let i=0;i<m;i++){for(let r of g[i])if(D[i]&bit(r))for(let j=0;j<m;j++)if(i!==j&&!(A[r]&D[j])){D[i]&=~bit(r);ch=true;break}assert(D[i]!==0n,"empty AC domain")}}}ac();for(let d of delta){for(let [r,h] of d.delta??[])A[r]&=~BigInt("0x"+h);for(let r of d.removedRows??[])D[z.rowMap[r][0]]&=~bit(r);ac()}
 g=g.map((v,i)=>v.filter(r=>Boolean(D[i]&bit(r))));const need=g.map(()=>Array(m).fill(false)),bad=need.map(x=>x.slice());let pairs=0,missing=0;
 function bounds(lo,hi){let l=lo.slice(),h=hi.slice(),u=lo.slice(),v=hi.slice();for(let i=1;i<l.length;i++){l[i]=Math.min(l[i],l[i-1]);h[i]=Math.max(h[i],h[i-1])}for(let i=u.length-2;i>=0;i--){u[i]=Math.min(u[i],u[i+1]);v[i]=Math.max(v[i],v[i+1])}return l.map((a,i)=>[Math.max(a,u[i]),Math.min(h[i],v[i])])}
 for(let i=0;i<m;i++)for(let j=i+1;j<m;j++){
 let a=g[i],b=g[j],mat=a.map(r=>b.map(t=>{pairs++;let ok=Boolean(A[r]&bit(t));assert(ok===Boolean(A[t]&bit(r)),"asymmetry");return ok}));let lo=a.map(()=>b.length),hi=a.map(()=>-1),cnt=a.map(()=>0),l2=b.map(()=>a.length),h2=b.map(()=>-1),c2=b.map(()=>0);
 for(let x=0;x<a.length;x++)for(let y=0;y<b.length;y++)if(mat[x][y]){lo[x]=Math.min(lo[x],y);hi[x]=Math.max(hi[x],y);cnt[x]++;l2[y]=Math.min(l2[y],x);h2[y]=Math.max(h2[y],x);c2[y]++}
 assert(cnt.every(x=>x>0)&&c2.every(x=>x>0),"nonAC");need[j][i]=cnt.some((v,k)=>v!==hi[k]-lo[k]+1);need[i][j]=c2.some((v,k)=>v!==h2[k]-l2[k]+1);
 let B=bounds(lo,hi),C=bounds(l2,h2);for(let x=0;x<a.length;x++)for(let y=0;y<b.length;y++){let hull=y>=B[x][0]&&y<=B[x][1]&&x>=C[y][0]&&x<=C[y][1];assert(!mat[x][y]||hull,"unsound local hull");if(hull&&!mat[x][y]){bad[i][j]=bad[j][i]=true;missing++}}
 }
 let a=recognize(need,bad);return {id:z.id,guard:z.guard,mode:delta.length>0,owners:m,scans,pairs,missing,forcedArcs:need.flat().filter(Boolean).length,badPairs:bad.flat().filter(Boolean).length/2,validSeeds:a.filter(x=>!x.conflict).length,closures:a}
 }
 let jobs=[];for(let i=0;i<5;i++){jobs.push(job(data[i],[]));let b=data[6].jobs.find(j=>j.ref===data[5].refs[i]&&j.mode===true);assert(JSON.stringify(b.guard)===JSON.stringify(data[i].guard),"guard");jobs.push(job(data[i],[data[5].jobs[i].combined,b]))}
 return {graphs,subsets,jobs}
}
const fs=require('node:fs');console.log(JSON.stringify(discover(process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')))),null,2));
