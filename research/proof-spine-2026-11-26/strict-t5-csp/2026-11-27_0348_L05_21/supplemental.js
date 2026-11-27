function supplemental(){
const assert=(x,m)=>{if(!x)throw Error(m)};
function sccSupport(n,arcs,d){
  const E=arcs.filter(([i,j,s])=>i!==j&&s<=d), adj=Array.from({length:n},()=>[]),rev=Array.from({length:n},()=>[]);
  for(let [i,j,s] of E){adj[i].push([j,s]);rev[j].push(i)}
  let seen=new Set(),order=[];function dfs(i){seen.add(i);for(let [j] of adj[i])if(!seen.has(j))dfs(j);order.push(i)}for(let i=0;i<n;i++)if(!seen.has(i))dfs(i);
  seen.clear();let blocks=[];function back(i,B){seen.add(i);B.push(i);for(let j of rev[i])if(!seen.has(j))back(j,B)}for(let i of order.reverse())if(!seen.has(i)){let B=[];back(i,B);blocks.push(B)}
  let joined=new Set([0]),ops=0,cert=[];
  for(let B of blocks){let set=new Set(B);if(B.length===1){cert.push({size:1,support:[0]});continue}
    let hub=-1,top;
    for(let h of B){let deg=new Map(B.filter(i=>i!==h).map(i=>[i,0]));for(let i of deg.keys())for(let [j] of adj[i])if(deg.has(j))deg.set(j,deg.get(j)+1);
      let Q=[...deg].filter(([i,z])=>z===0).map(([i])=>i);for(let k=0;k<Q.length;k++)for(let [j] of adj[Q[k]])if(deg.has(j)){deg.set(j,deg.get(j)-1);if(deg.get(j)===0)Q.push(j)}
      if(Q.length===B.length-1){hub=h;top=Q;break}}
    if(hub<0)return {status:"UNKNOWN",blocks:blocks.map(x=>x.length)};
    let D=new Map(top.map(i=>[i,new Set()]));for(let [j,s] of adj[hub])if(D.has(j))D.get(j).add(s);
    let S=new Set([0]);for(let i of top)for(let a of D.get(i))for(let [j,s] of adj[i])if(set.has(j)){ops++;if(a+s>d)continue;if(j===hub)S.add(a+s);else D.get(j).add(a+s)}
    let next=new Set();for(let x of joined)for(let y of S){ops++;if(x+y<=d)next.add(x+y)}joined=next;cert.push({size:B.length,hub,support:[...S].sort((x,y)=>x-y)})
  }
  return {status:joined.has(d)?"YES":"NO",support:[...joined].sort((a,b)=>a-b),ops,cert}
}
function ref(n,arcs,d){let adj=Array.from({length:n},(_,i)=>[[i,0]]);for(let [i,j,s] of arcs)adj[i].push([j,s]);let used=new Set(),S=new Set(),visits=0;function go(i,c){if(i===n){S.add(c);return}for(let [j,s] of adj[i]){visits++;if(used.has(j)||c+s>d)continue;used.add(j);go(i+1,c+s);used.delete(j)}}go(0,0);return {support:[...S].sort((a,b)=>a-b),visits}}
let cases=0,unknown=0,admitted=0,refVisits=0;let seed=20261127;function rng(m){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%m}
for(let n=2;n<=8;n++)for(let rep=0;rep<60;rep++){let arcs=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i!==j&&rng(7)<3)arcs.push([i,j,rng(6)]);let d=1+rng(8);let A=sccSupport(n,arcs,d),B=ref(n,arcs,d);cases++;refVisits+=B.visits;if(A.status==="UNKNOWN")unknown++;else{admitted++;assert(A.support.join(",")===B.support.join(","),"general SCC mismatch")}}
let multi=[[0,1,1],[1,0,1],[2,3,1],[3,2,2],[1,2,0],[3,0,10]];
let M=sccSupport(4,multi,5);assert(M.support.join(",")==="0,2,3,5","SCC join");
let family=[];
for(let q=4;q<=9;q++){let a=q-1,L=2*a+3,d=2*a,arcs=[];for(let i=1;i<q;i++){arcs.push([0,i,1]);arcs.push([i,0,i<=2?a-1:a]);}for(let i=1;i<q;i++)for(let j=1;j<q;j++)if(i!==j)arcs.push([i,j,d+1]);let A=sccSupport(q,arcs,d),B=ref(q,arcs,d);assert(A.status==="NO"&&A.support.join(",")===[0,a,a+1].join(",")&&B.support.join(",")===A.support.join(","),"family");let cycles=[[0,1,0],[0,2,0]];assert(cycles.every(c=>arcs.find(x=>x[0]===c[0]&&x[1]===c[1])[2]+arcs.find(x=>x[0]===c[1]&&x[1]===c[2])[2]===a),"distinct cycles");
family.push({q,a,d,support:A.support,dpOps:A.ops,refVisits:B.visits,distinctCostACycles:cycles});
}
// Explicit grid wire/accumulator check, square padding and boundary pinning. Count valid table paths against truth assignments.
let gridCases=0,gridRows=0;for(let n=1;n<=3;n++)for(let m=1;m<=3;m++)for(let rep=0;rep<20;rep++){
 let c=Array.from({length:m},()=>Array.from({length:3},()=>[rng(n),rng(2)])),s=Math.max(n,m),tables=[];
 for(let i=0;i<s;i++)for(let j=0;j<s;j++){let A=[];for(let w=0;w<16;w++){let [W,E,N,S]=[w&1,(w>>1)&1,(w>>2)&1,(w>>3)&1],lit=j<m&&i<n&&c[j].some(([v,b])=>v===i&&W===b)?1:0;let good=W===E&&S===(N|lit)&&(i!==0||N===0)&&(i!==s-1||S===+(j<m));if(good)A.push(w)}tables.push(A)}
 for(let mask=0;mask<2**n;mask++){let state=Array(s).fill(0),possible=true;for(let i=0;i<s;i++)for(let j=0;j<s;j++){let W=i<n?mask>>i&1:0,N=state[j],opts=tables[i*s+j].filter(w=>(w&1)===W&&((w>>2)&1)===N);if(!opts.length){possible=false;break}assert(opts.length===1,"deterministic grid");state[j]=opts[0]>>3&1;gridRows++}let truth=c.every(cl=>cl.some(([i,b])=>(mask>>i&1)===b));assert(possible===truth,"grid");gridCases++}
}
return {cases,admitted,unknown,refVisits,multi:M,family,gridCases,gridRows}
}
console.log(JSON.stringify(supplemental(),null,2));
