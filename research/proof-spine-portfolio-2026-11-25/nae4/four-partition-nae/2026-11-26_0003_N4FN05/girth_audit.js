// N4FN05 high-girth obstruction. Run node girth_audit.js.
let checks=0,ck=b=>{if(!b)throw Error("assert "+checks);checks++};
const E=Array.from({length:7},()=>[]);
for(let v=0;v<3;v++)for(let j=0;j<4;j++){let id=v&&j?2*(j-1)+v-1:-1;E[v].push([3+j,id,1]);E[3+j].push([v,id,-1])}
let vectors=new Map;
for(let s=0;s<7;s++){
 function dfs(v,prev,first,d,w){if(d>=4&&v===s&&prev!==first){ck(w.some(Boolean));let a=w.find(Boolean)<0?w.map(x=>-x):w;vectors.set(a.join(","),a)}
 if(d===8)return;
 for(let [u,i,e] of E[v])if(u!==prev){let a=w.slice();if(i>=0)a[i]+=e;dfs(u,v,d?first:u,d+1,a)}
 }dfs(s,-1,-1,0,Array(6).fill(0))
}
let V=[...vectors.values()],seed=20261126;
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
let p=1009,offsets=null,attempts=0;
while(!offsets&&attempts++<10000){let a=Array.from({length:6},()=>rnd(p));if(V.every(w=>w.reduce((s,x,i)=>s+x*a[i],0)%p!==0))offsets=a}
ck(!!offsets);
function instance(q){let F=Array.from({length:4},(_,j)=>Array.from({length:q},(_,i)=>[i,q+(i+(j?offsets[2*(j-1)]:0))%q,2*q+(i+(j?offsets[2*(j-1)+1]:0))%q]));return F}
function audit(q){
 let F=instance(q),n=3*q,cs=F.flat(),inc=Array.from({length:n},()=>[]),pairs=new Set;
 for(let j=0;j<4;j++){let a=F[j].flat();ck(new Set(a).size===n);for(let c of F[j]){ck(c.filter(v=>v<q).length===1);for(let i=0;i<3;i++)for(let k=i+1;k<3;k++){let s=[c[i],c[k]].sort((a,b)=>a-b).join(",");ck(!pairs.has(s));pairs.add(s)}}}
 cs.forEach((c,i)=>c.forEach(v=>inc[v].push(i)));let N=Array.from({length:n},(_,v)=>[...new Set(inc[v].flatMap(i=>cs[i]).filter(w=>w!==v))]);ck(N.every(a=>a.length===8));
 let q0=[0],seen=new Set(q0);for(let v of q0)for(let w of N[v])if(!seen.has(w)){seen.add(w);q0.push(w)}ck(seen.size===n);
 // All base nonbacktracking closed walks length <=8 have nonzero voltage.
 ck(V.every(w=>w.reduce((s,x,i)=>s+x*offsets[i],0)%q!==0));
 // Independently verify no 4/6/8 incidence cycles by local nonbacktracking walks
 // for one representative of each vertex orbit (cyclic shift symmetry).
 let G=[...inc.map(a=>a.map(i=>n+i)),...cs];
 for(let s of [0,q,2*q,n,n+q,n+2*q,n+3*q]){
  function walk(v,prev,d){if(d>0&&v===s){ck(d>8);return}if(d===8)return;for(let u of G[v])if(u!==prev)walk(u,v,d+1)}
  walk(s,-1,0)
 }
 let maxPins=0,minLargest=n,contradicted=0;
 for(let trial=0;trial<160;trial++){
  let a=new Map;while(a.size<3)a.set(rnd(n),rnd(2));
  if(trial<16){let c=cs[trial],d=cs.find(r=>r.includes(c[2])&&r!==c);a=new Map([[c[0],0],[c[1],0],[d.find(v=>v!==c[2]),1]])}
  let go=true,bad=false;while(go&&!bad){go=false;for(let c of cs){let f=c.filter(v=>a.has(v));if(f.length===3&&f.every(v=>a.get(v)===a.get(f[0]))){bad=true;break}if(f.length===2&&a.get(f[0])===a.get(f[1])){a.set(c.find(v=>!a.has(v)),1^a.get(f[0]));go=true}}}
  ck(a.size<=5);maxPins=Math.max(maxPins,a.size);if(bad){contradicted++;continue}
  let visited=new Set(a.keys()),largest=0;for(let v=0;v<n;v++)if(!visited.has(v)){let b=[v];visited.add(v);for(let u of b)for(let w of N[u])if(!visited.has(w)){visited.add(w);b.push(w)}largest=Math.max(largest,b.length)}
  ck(largest>3);minLargest=Math.min(minLargest,largest)
 }
 return {q,n,owners:4*q,maxPins,minLargest,contradicted}
}
let results=[p,2*p,4*p].map(audit);console.log(JSON.stringify({checks,baseVoltageVectors:V.length,p,offsets,attempts,results},null,2));